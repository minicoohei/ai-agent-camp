#!/bin/bash
# OpenClaw Gateway Watchdog v6
# Detects six failure modes:
#   1. HTTP unresponsive (container hung or crashed)
#   2. Log stale (HTTP responds but LINE messages not processed)
#   3. LLM timeout (gateway running but AI backend unreachable)
#   4. Main lane timeout (session state corruption - LINE stops responding)
#   5. LLM proxy down (proxy server itself unreachable)
#   6. Container resource exhaustion (memory)
# Run via cron every 1 minute.
#
# v6 changes: Added restart cooldown (15min) to prevent session context loss
#             from cascading restarts. Relaxed LLM timeout thresholds.

CONTAINER="openclaw-openclaw-gateway-1"
ENDPOINT="http://127.0.0.1:18789/line/webhook"
PROXY_ENDPOINT="http://172.18.0.1:3456/v1/models"
LOG="/var/log/openclaw-watchdog.log"
PUSH_TOKEN="BscM23uOHHe06F66hD6S0O2y1kXDQN2E"
COMPOSE_DIR="/opt/openclaw"

MAX_HTTP_FAILURES=3
MAX_STALE_MINUTES=60
MAX_LLM_TIMEOUTS=10
MAX_MAIN_TIMEOUTS=5
MAX_MEMORY_PCT=90
RESTART_COOLDOWN_MIN=15

STATE_FILE="/tmp/openclaw-watchdog-failures"
STALE_FILE="/tmp/openclaw-watchdog-stale"
TIMEOUT_FILE="/tmp/openclaw-watchdog-llm-timeouts"
MAIN_TIMEOUT_FILE="/tmp/openclaw-watchdog-main-timeouts"
PROXY_FILE="/tmp/openclaw-watchdog-proxy-down"
LAST_RESTART_FILE="/tmp/openclaw-watchdog-last-restart"

log() {
  echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') $1" >> "$LOG"
}

push_notify() {
  curl -s -X POST https://api.getmoshi.app/api/webhook \
    -H "Content-Type: application/json" \
    -d "{\"token\": \"$PUSH_TOKEN\", \"title\": \"OpenClaw Watchdog\", \"message\": \"$1\"}" \
    >/dev/null 2>&1
}

do_restart() {
  local reason="$1"

  # Cooldown: skip restart if one happened recently
  local last_restart now cooldown_sec
  last_restart=$(cat "$LAST_RESTART_FILE" 2>/dev/null || echo "0")
  now=$(date +%s)
  cooldown_sec=$((RESTART_COOLDOWN_MIN * 60))
  if [ $((now - last_restart)) -lt "$cooldown_sec" ]; then
    log "SKIP: Restart suppressed by cooldown (${RESTART_COOLDOWN_MIN}min). Reason: $reason"
    return 0
  fi

  log "ALERT: Restarting container. Reason: $reason"
  date +%s > "$LAST_RESTART_FILE"
  docker restart "$CONTAINER" >> "$LOG" 2>&1
  sleep 15

  # Verify recovery (POST with empty JSON body - expects 400 or 200)
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$ENDPOINT" \
    -X POST -H "Content-Type: application/json" -d '{}' 2>/dev/null)
  if [ "$HTTP_CODE" = "400" ] || [ "$HTTP_CODE" = "200" ]; then
    log "OK: Container recovered after restart"
    push_notify "Gateway restarted ($reason). Recovered OK."
  else
    log "CRITICAL: Still unhealthy after restart (HTTP=$HTTP_CODE)"
    push_notify "Gateway restarted ($reason) but still unhealthy (HTTP=$HTTP_CODE)."
  fi
  echo "0" > "$STATE_FILE"
  echo "0" > "$STALE_FILE"
  echo "0" > "$TIMEOUT_FILE"
  echo "0" > "$MAIN_TIMEOUT_FILE"
}

# --- Check 0: Workspace file integrity ---
WORKSPACE="/root/.openclaw/workspace"
AGENTS_FILE="$WORKSPACE/AGENTS.md"
NEED_RECREATE=0

if [ ! -f "$AGENTS_FILE" ]; then
  NEED_RECREATE=1
elif [ ! -s "$AGENTS_FILE" ]; then
  # File exists but is empty
  NEED_RECREATE=1
  log "WARN: AGENTS.md is empty, will recreate"
elif ! grep -q "LINE" "$AGENTS_FILE" 2>/dev/null; then
  # File exists but missing LINE keyword - may have been overwritten
  NEED_RECREATE=1
  log "WARN: AGENTS.md missing LINE keyword, will recreate"
fi

if [ "$NEED_RECREATE" -eq 1 ]; then
  cat > "$AGENTS_FILE" << 'AGENTSEOF'
# OpenClaw LINE Agent

あなたはLINE経由でユーザーと対話するAIアシスタントです。

## 基本ルール

- 日本語で回答すること
- 簡潔で親しみやすいトーンで応答
- ユーザーの質問に対して的確に回答する
- 不明な点があれば確認する

## 注意事項

- この環境にはgit, gh, gogcli, gcloud等のCLIツールはインストールされていません
- シェルコマンドの実行は最小限にしてください
- ファイル操作が必要な場合は /home/node/.openclaw/workspace/ 内で行ってください
AGENTSEOF
  chown 1000:1000 "$AGENTS_FILE" 2>/dev/null
  log "FIX: Recreated AGENTS.md file"
fi

# Ensure uid 1000 (container node user) can access workspace files
if ! getfacl -p "$AGENTS_FILE" 2>/dev/null | grep -q "user:1000:rw"; then
  setfacl -R -m u:1000:rwX "$WORKSPACE" 2>/dev/null
  setfacl -R -d -m u:1000:rwX "$WORKSPACE" 2>/dev/null
  log "FIX: Reapplied ACL for uid 1000 on workspace"
fi

# --- Check 1: Container running? ---
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  log "ALERT: Container not running. Starting..."
  docker start "$CONTAINER" >> "$LOG" 2>&1
  push_notify "Container was stopped. Restarted."
  echo "0" > "$STATE_FILE"
  echo "0" > "$STALE_FILE"
  exit 0
fi

# --- Check 2: HTTP health ---
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$ENDPOINT" \
  -X POST -H "Content-Type: application/json" -d '{}' 2>/dev/null)

if [ "$HTTP_CODE" != "400" ] && [ "$HTTP_CODE" != "200" ]; then
  FAILURES=$(cat "$STATE_FILE" 2>/dev/null || echo "0")
  FAILURES=$((FAILURES + 1))
  echo "$FAILURES" > "$STATE_FILE"
  log "WARN: HTTP check failed (HTTP=$HTTP_CODE, failures=$FAILURES/$MAX_HTTP_FAILURES)"

  if [ "$FAILURES" -ge "$MAX_HTTP_FAILURES" ]; then
    do_restart "HTTP unresponsive ($HTTP_CODE) x${FAILURES}"
  fi
  exit 0
fi
echo "0" > "$STATE_FILE"

# --- Check 3: Internal log freshness ---
# The gateway logs to /tmp/openclaw/openclaw-YYYY-MM-DD.log inside the container.
# If no log entry for MAX_STALE_MINUTES, the gateway is alive but frozen.
TODAY=$(date -u '+%Y-%m-%d')
LAST_LOG_TIME=$(docker exec "$CONTAINER" tail -1 "/tmp/openclaw/openclaw-${TODAY}.log" 2>/dev/null \
  | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('time',''))" 2>/dev/null)

if [ -n "$LAST_LOG_TIME" ]; then
  LAST_EPOCH=$(date -d "$LAST_LOG_TIME" +%s 2>/dev/null || echo "0")
  NOW_EPOCH=$(date -u +%s)
  DIFF_MIN=$(( (NOW_EPOCH - LAST_EPOCH) / 60 ))

  if [ "$DIFF_MIN" -ge "$MAX_STALE_MINUTES" ]; then
    STALE_COUNT=$(cat "$STALE_FILE" 2>/dev/null || echo "0")
    STALE_COUNT=$((STALE_COUNT + 1))
    echo "$STALE_COUNT" > "$STALE_FILE"
    log "WARN: Log stale for ${DIFF_MIN}min (threshold=${MAX_STALE_MINUTES}min, count=$STALE_COUNT)"

    # Restart on second consecutive stale detection (= 4 min with no activity)
    if [ "$STALE_COUNT" -ge 2 ]; then
      do_restart "log stale ${DIFF_MIN}min"
    fi
  else
    echo "0" > "$STALE_FILE"
  fi
else
  # Can't read log - not fatal, just skip stale check
  echo "0" > "$STALE_FILE"
fi

# --- Check 4: LLM timeout detection ---
# Count "timed out" errors in last 50 log lines.
# If consecutive watchdog runs detect timeouts, restart to reset connections.
RECENT_TIMEOUTS=$(docker exec "$CONTAINER" tail -50 "/tmp/openclaw/openclaw-${TODAY}.log" 2>/dev/null \
  | grep -c "timed out" 2>/dev/null | tr -d '[:space:]')
RECENT_TIMEOUTS=${RECENT_TIMEOUTS:-0}

if [ "$RECENT_TIMEOUTS" -ge 2 ]; then
  LLM_COUNT=$(cat "$TIMEOUT_FILE" 2>/dev/null || echo "0")
  LLM_COUNT=$((LLM_COUNT + 1))
  echo "$LLM_COUNT" > "$TIMEOUT_FILE"
  log "WARN: LLM timeouts detected (recent=$RECENT_TIMEOUTS, consecutive=$LLM_COUNT/$MAX_LLM_TIMEOUTS)"

  if [ "$LLM_COUNT" -ge "$MAX_LLM_TIMEOUTS" ]; then
    do_restart "LLM timed out (${RECENT_TIMEOUTS} in recent logs, ${LLM_COUNT} consecutive checks)"
  fi
else
  echo "0" > "$TIMEOUT_FILE"
fi

# --- Check 4b: Main lane timeout detection (session state corruption) ---
# "Request timed out after 300000ms" on lane=main means LINE message processing failed.
# This may corrupt session state and cause LINE unresponsiveness.
# Require consecutive detections to avoid restarting on stale log entries.
MAIN_TIMEOUT=$(docker exec "$CONTAINER" tail -100 "/tmp/openclaw/openclaw-${TODAY}.log" 2>/dev/null \
  | grep -c "timed out after 300000ms" 2>/dev/null | tr -d '[:space:]')
MAIN_TIMEOUT=${MAIN_TIMEOUT:-0}

if [ "$MAIN_TIMEOUT" -ge 1 ]; then
  MAIN_COUNT=$(cat "$MAIN_TIMEOUT_FILE" 2>/dev/null || echo "0")
  MAIN_COUNT=$((MAIN_COUNT + 1))
  echo "$MAIN_COUNT" > "$MAIN_TIMEOUT_FILE"
  log "WARN: Main lane timeout detected (recent=$MAIN_TIMEOUT, consecutive=$MAIN_COUNT/$MAX_MAIN_TIMEOUTS)"

  if [ "$MAIN_COUNT" -ge "$MAX_MAIN_TIMEOUTS" ]; then
    do_restart "main lane timeout (300s) x${MAIN_TIMEOUT} - ${MAIN_COUNT} consecutive checks"
  fi
else
  echo "0" > "$MAIN_TIMEOUT_FILE"
fi

# --- Check 5: LLM proxy health ---
# The proxy at 172.18.0.1:3456 routes LLM requests. If down, gateway can't reach AI.
# Notify only (restart won't fix a proxy issue).
PROXY_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$PROXY_ENDPOINT" 2>/dev/null)

if [ "$PROXY_CODE" = "000" ] || [ "$PROXY_CODE" = "502" ] || [ "$PROXY_CODE" = "503" ]; then
  PROXY_DOWN=$(cat "$PROXY_FILE" 2>/dev/null || echo "0")
  PROXY_DOWN=$((PROXY_DOWN + 1))
  echo "$PROXY_DOWN" > "$PROXY_FILE"
  log "WARN: LLM proxy unreachable (HTTP=$PROXY_CODE, consecutive=$PROXY_DOWN)"

  # Notify on first detection, then every 5th check (10 min)
  if [ "$PROXY_DOWN" -eq 1 ] || [ $((PROXY_DOWN % 5)) -eq 0 ]; then
    push_notify "LLM proxy down (HTTP=$PROXY_CODE). Gateway can't reach AI backend. Check proxy at 172.18.0.1:3456."
  fi
else
  if [ "$(cat "$PROXY_FILE" 2>/dev/null || echo "0")" -gt 0 ]; then
    log "OK: LLM proxy recovered"
    push_notify "LLM proxy recovered."
  fi
  echo "0" > "$PROXY_FILE"
fi

# --- Check 6: Container resource monitoring ---
# Check memory usage percentage. High memory can cause OOM or sluggish responses.
MEM_STATS=$(docker stats --no-stream --format '{{.MemPerc}}' "$CONTAINER" 2>/dev/null | tr -d '% \n')

if [ -n "$MEM_STATS" ]; then
  MEM_INT=${MEM_STATS%.*}
  if [ -n "$MEM_INT" ] && [ "$MEM_INT" -ge "$MAX_MEMORY_PCT" ] 2>/dev/null; then
    log "WARN: Container memory at ${MEM_STATS}% (threshold=${MAX_MEMORY_PCT}%)"
    push_notify "Gateway memory high: ${MEM_STATS}%. Consider restarting."
  fi
fi

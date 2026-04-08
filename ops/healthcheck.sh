#!/usr/bin/env bash
# OpenClaw Gateway ヘルスチェック & 自動復旧 (Plan B: Clean Gateway)
#
# cron: */5 * * * * /opt/openclaw/healthcheck.sh >> /opt/openclaw/logs/healthcheck.log 2>&1
#
# チェック:
#   1. Docker コンテナ running
#   2. HTTP 200 応答
#   3. 致命的エラー検出 (EACCES/ENOENT)
#   4. 必須 Markdown ファイル
#   5. Tailscale Funnel 状態 (LINE Webhook 受信に必須)
#
# 復旧:
#   - コンテナ停止 → docker compose up -d (override 自動読み込み)
#   - AGENTS.md 消失 → CLAUDE.md からコピー

set -uo pipefail

OPENCLAW_DIR="/opt/openclaw"
REPO_DIR="/home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata"
WORKSPACE_LINK="$HOME/.openclaw/workspace"
CONTAINER_NAME="openclaw-openclaw-gateway-1"
HEALTH_URL="http://127.0.0.1:18789/"
LOG_PREFIX="[healthcheck]"
MAX_RESTART_PER_HOUR=3
RESTART_COUNTER_FILE="/tmp/openclaw-healthcheck-restart-count"

ts()   { date '+%Y-%m-%d %H:%M:%S'; }
log()  { echo "$(ts) $LOG_PREFIX $*"; }
warn() { echo "$(ts) $LOG_PREFIX [WARN] $*"; }
err()  { echo "$(ts) $LOG_PREFIX [ERROR] $*" >&2; }

get_restart_count() {
  [ ! -f "$RESTART_COUNTER_FILE" ] && echo 0 && return
  local cutoff
  cutoff=$(date -d '1 hour ago' '+%s' 2>/dev/null || date -v-1H '+%s' 2>/dev/null || echo "")
  if [ -z "$cutoff" ]; then
    err "date コマンド失敗。安全側に倒し再起動を禁止します"
    echo "$MAX_RESTART_PER_HOUR"
    return
  fi
  awk -v cutoff="$cutoff" '$1 >= cutoff { count++ } END { print count+0 }' "$RESTART_COUNTER_FILE"
}

record_restart() {
  date '+%s' >> "$RESTART_COUNTER_FILE"
  if [ -f "$RESTART_COUNTER_FILE" ]; then
    local cutoff
    cutoff=$(date -d '24 hours ago' '+%s' 2>/dev/null || date -v-24H '+%s' 2>/dev/null || echo "")
    if [ -n "$cutoff" ]; then
      awk -v cutoff="$cutoff" '$1 >= cutoff' "$RESTART_COUNTER_FILE" > "${RESTART_COUNTER_FILE}.tmp"
      mv "${RESTART_COUNTER_FILE}.tmp" "$RESTART_COUNTER_FILE"
    fi
    # cutoff 取得失敗時はクリーンアップをスキップ (ファイルは肥大するが安全)
  fi
}

restart_gateway() {
  local reason="$1"
  local count; count=$(get_restart_count)
  if [ "$count" -ge "$MAX_RESTART_PER_HOUR" ]; then
    err "再起動スキップ: ${count}/${MAX_RESTART_PER_HOUR} 回 (理由: $reason)"
    return 1
  fi
  # Respect watchdog cooldown to avoid double-restart
  local last_wd_restart
  last_wd_restart=$(cat /tmp/openclaw-watchdog-last-restart 2>/dev/null || echo "0")
  local now; now=$(date +%s)
  if [ $((now - last_wd_restart)) -lt 900 ]; then
    log "再起動スキップ: watchdog cooldown中 (理由: $reason)"
    return 1
  fi
  warn "Gateway 再起動: $reason"
  # Use docker restart instead of compose down+up to preserve session state
  docker restart "$CONTAINER_NAME" 2>&1 | while read -r l; do log "  restart: $l"; done
  record_restart
  log "再起動完了 (理由: $reason)"
}

# --- チェック 1: コンテナ ---
check_container() {
  local status
  status=$(docker inspect "$CONTAINER_NAME" --format '{{.State.Status}}' 2>/dev/null)
  [ "$status" = "running" ]
}

# --- チェック 2: HTTP ---
check_http() {
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 "$HEALTH_URL" 2>/dev/null)
  [ "$code" = "200" ]
}

# --- チェック 3: 致命的エラー ---
check_fatal_errors() {
  local errors
  errors=$(docker logs --since 5m "$CONTAINER_NAME" 2>&1 \
    | grep -cE 'EACCES|ENOENT.*AGENTS\.md|ENOENT.*SOUL\.md|auto-reply failed' 2>/dev/null || true)
  errors="${errors##*$'\n'}"; errors="${errors:-0}"
  [[ "$errors" =~ ^[0-9]+$ ]] || errors=0
  [ "$errors" -eq 0 ]
}

# --- チェック 4: 必須 Markdown ---
check_workspace_md() {
  local ws
  [ -L "$WORKSPACE_LINK" ] && ws=$(readlink -f "$WORKSPACE_LINK") || ws="$WORKSPACE_LINK"
  local needs_fix=false

  for md in AGENTS.md SOUL.md TOOLS.md USER.md MEMORY.md; do
    if [ ! -e "${ws}/${md}" ]; then
      warn "${md} 消失"
      case "$md" in
        AGENTS.md)
          if [ -f "${ws}/CLAUDE.md" ]; then
            cp "${ws}/CLAUDE.md" "${ws}/${md}"
            chmod g+rw "${ws}/${md}"
            log "${md} を CLAUDE.md からコピー"
            needs_fix=true
          fi ;;
        *)
          (cd "$ws" && git checkout -- "$md" 2>/dev/null) && {
            chmod g+rw "${ws}/${md}" 2>/dev/null || true
            log "${md} を Git から復元"
            needs_fix=true
          } ;;
      esac
    fi
  done
  $needs_fix && return 2 || return 0
}

# --- チェック 5: Tailscale Funnel (LINE Webhook に必須) ---
# NOTE: Funnel は OS レベルの設定のため、Gateway 再起動では復旧できない。
#       手動復旧: sudo tailscale funnel --bg --set-path / http://127.0.0.1:18789
check_funnel() {
  if command -v tailscale >/dev/null 2>&1; then
    local out
    out=$(tailscale funnel status 2>&1 || true)
    echo "$out" | grep -q "Funnel on"
  fi
}

# --- メイン ---
main() {
  local needs_restart=false restart_reason="" all_ok=true

  if ! check_container; then
    needs_restart=true; restart_reason="コンテナ停止"; all_ok=false
  fi

  if [ "$needs_restart" = false ] && ! check_http; then
    needs_restart=true; restart_reason="HTTP 失敗"; all_ok=false
  fi

  check_workspace_md; local ws_result=$?
  if [ "$ws_result" -eq 2 ]; then
    # MD files were restored - no restart needed, gateway reads on next request
    log "MD ファイル修復済み (再起動不要)"
    all_ok=false
  elif [ "$ws_result" -eq 1 ]; then all_ok=false; fi

  if [ "$needs_restart" = false ] && ! check_fatal_errors; then
    [ "$ws_result" -ne 0 ] && { needs_restart=true; restart_reason="${restart_reason:+$restart_reason + }致命的エラー"; }
    all_ok=false
  fi

  if ! check_funnel; then
    warn "Tailscale Funnel OFF (LINE Webhook 受信不可)"
    warn "  復旧: sudo tailscale funnel --bg --set-path / http://127.0.0.1:18789"
    all_ok=false
  fi

  [ "$needs_restart" = true ] && restart_gateway "$restart_reason"

  # 1時間に1回だけ OK ログ
  if [ "$all_ok" = true ]; then
    local min; min=$(date '+%M')
    [ "$((min % 60))" -eq 0 ] && log "全チェック OK"
  fi
}

main "$@"

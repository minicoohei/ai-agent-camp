#!/bin/bash
# gh_token.sh - GH_TOKEN取得ヘルパー（フォールバックチェーン）
# Usage: export GH_TOKEN=$(bash tools/gh_token.sh)
#
# 優先順位:
#   1. 環境変数 GH_TOKEN（既に設定済みならそのまま使用）
#   2. git remote URL から抽出（aiagent-base リポジトリ）
#   3. openclaw.json の GITHUB_TOKEN フィールド

set -euo pipefail

# 1. 環境変数が既に設定されていればそのまま返す
if [ -n "${GH_TOKEN:-}" ]; then
  echo "$GH_TOKEN"
  exit 0
fi

# 2. git remote URL から抽出
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
REMOTE_URL=$(git -C "$REPO_DIR" remote get-url origin 2>/dev/null || true)
TOKEN=""
if [[ "$REMOTE_URL" =~ https://([^@]+)@github\.com ]]; then
  TOKEN="${BASH_REMATCH[1]}"
  TOKEN="${TOKEN#x-access-token:}"
fi

if [ -n "$TOKEN" ]; then
  echo "$TOKEN"
  exit 0
fi

# 3. openclaw.json からネスト検索
TOKEN=$(python3 -c "
import json, sys
def find_key(d, t):
    if isinstance(d, dict):
        for k, v in d.items():
            if k == t: return v
            r = find_key(v, t)
            if r: return r
    return None
try:
    v = find_key(json.load(open('/root/.openclaw/openclaw.json')), 'GITHUB_TOKEN')
    if v: print(v)
    else: sys.exit(1)
except Exception:
    sys.exit(1)
" 2>/dev/null || true)

if [ -n "$TOKEN" ]; then
  echo "$TOKEN"
  exit 0
fi

echo "ERROR: GH_TOKEN を取得できませんでした" >&2
exit 1

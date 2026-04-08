#!/usr/bin/env bash
# lint-skills-sync.sh — skills/ と .claude/skills/ の同期を検証
# sync-skills.sh --check のラッパー。CIで使用。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== Lint: Skills Sync Verification ==="
echo ""

if bash "$REPO_ROOT/scripts/sync-skills.sh" --check; then
    echo ""
    echo "PASS: skills/ and .claude/skills/ are in sync."
else
    echo ""
    echo "FAIL: skills/ and .claude/skills/ are out of sync."
    echo "Run 'bash scripts/sync-skills.sh' to fix."
    exit 1
fi

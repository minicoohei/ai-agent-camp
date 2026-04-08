#!/usr/bin/env bash
# lint-all.sh — 全 lint スクリプトをまとめて実行
# CI / pre-push で使用

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
failed=0

echo "==============================="
echo "  aiagent-base Lint Suite"
echo "==============================="
echo ""

# 1. Skills SKILL.md 構造検証
echo "--- [1/5] lint-skills.sh ---"
if bash "$REPO_ROOT/scripts/lint-skills.sh"; then
    echo "PASS"
else
    ((failed++)) || true
fi
echo ""

# 2. Skills 同期検証 (skills/ → .claude/skills/)
echo "--- [2/5] lint-skills-sync.sh ---"
if bash "$REPO_ROOT/scripts/lint-skills-sync.sh"; then
    echo "PASS"
else
    ((failed++)) || true
fi
echo ""

# 3. Commands 同期検証
echo "--- [3/5] lint-commands.sh ---"
if bash "$REPO_ROOT/scripts/lint-commands.sh"; then
    echo "PASS"
else
    ((failed++)) || true
fi
echo ""

# 4. openai.yaml 存在検証
echo "--- [4/5] lint-openai-yaml.sh ---"
if bash "$REPO_ROOT/scripts/lint-openai-yaml.sh"; then
    echo "PASS"
else
    ((failed++)) || true
fi
echo ""

# 5. Rules 同期検証
echo "--- [5/5] lint-rules.sh ---"
if bash "$REPO_ROOT/scripts/lint-rules.sh"; then
    echo "PASS"
else
    ((failed++)) || true
fi
echo ""

echo "==============================="
if [ "$failed" -gt 0 ]; then
    echo "  FAILED: $failed lint(s)"
    exit 1
else
    echo "  ALL PASSED"
fi

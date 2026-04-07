#!/usr/bin/env bash
# migrate-skills.sh — .claude/skills/ → skills/ への一括移行
# Phase 1: Skills ディレクトリ統一
#
# 手順:
# 1. .claude/skills/ の全スキルを skills/ に移動
# 2. .claude/skills/<name> → ../../skills/<name> のシンボリックリンク作成
# 3. 既存の skills/ スキルはそのまま維持

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_SKILLS="$REPO_ROOT/.claude/skills"
ROOT_SKILLS="$REPO_ROOT/skills"

# カウンター
moved=0
skipped=0
already=0

echo "=== Skills Migration: .claude/skills/ → skills/ ==="
echo "Source: $CLAUDE_SKILLS"
echo "Target: $ROOT_SKILLS"
echo ""

for skill_dir in "$CLAUDE_SKILLS"/*/; do
    skill_name="$(basename "$skill_dir")"

    # .DS_Store 等のファイルはスキップ
    [ ! -d "$skill_dir" ] && continue

    # _template はスキップ
    [[ "$skill_name" == _* ]] && continue

    # 既にシンボリックリンクならスキップ
    if [ -L "$CLAUDE_SKILLS/$skill_name" ]; then
        echo "SKIP (symlink): $skill_name"
        ((skipped++)) || true
        continue
    fi

    # skills/ に同名ディレクトリが既にある場合
    if [ -d "$ROOT_SKILLS/$skill_name" ]; then
        echo "SKIP (exists in skills/): $skill_name"
        ((already++)) || true
        continue
    fi

    # 移動 + シンボリックリンク作成
    echo "MOVE: $skill_name"
    mv "$CLAUDE_SKILLS/$skill_name" "$ROOT_SKILLS/$skill_name"
    ln -s "../../skills/$skill_name" "$CLAUDE_SKILLS/$skill_name"
    ((moved++)) || true
done

echo ""
echo "=== Summary ==="
echo "Moved:   $moved"
echo "Skipped: $skipped (already symlink)"
echo "Exists:  $already (already in skills/)"
echo ""
echo "Verification:"
echo "  skills/ count: $(find "$ROOT_SKILLS" -maxdepth 1 -type d | wc -l | tr -d ' ')"
echo "  .claude/skills/ symlinks: $(find "$CLAUDE_SKILLS" -maxdepth 1 -type l | wc -l | tr -d ' ')"
echo "  .claude/skills/ dirs: $(find "$CLAUDE_SKILLS" -maxdepth 1 -type d -not -path "$CLAUDE_SKILLS" | wc -l | tr -d ' ')"

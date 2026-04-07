#!/usr/bin/env bash
# generate-commands.sh — .cursor/commands/lesson/ を正本として
# .claude/commands/lesson/ にコピーを生成する
#
# 正本: .cursor/commands/lesson/{lessonId}.md
# 生成: .claude/commands/lesson/{lessonId}.md
#
# Claude Code のコマンドは .claude/commands/ に配置する必要がある。
# Cursor は .cursor/commands/ を使う。両方で同じレッスンを利用可能にする。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/.cursor/commands/lesson"
TARGET_DIR="$REPO_ROOT/.claude/commands/lesson"

# カウンター
copied=0
skipped=0
updated=0
errors=0

echo "=== Command Generation: .cursor → .claude ==="
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo ""

# ソースが存在するか確認
if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# ターゲットディレクトリ作成
mkdir -p "$TARGET_DIR"

for src_file in "$SOURCE_DIR"/*.md; do
    [ ! -f "$src_file" ] && continue

    filename="$(basename "$src_file")"
    target_file="$TARGET_DIR/$filename"

    # 既存ファイルがあり、内容が同じならスキップ
    if [ -f "$target_file" ]; then
        if diff -q "$src_file" "$target_file" >/dev/null 2>&1; then
            ((skipped++)) || true
            continue
        else
            # 内容が異なる場合は更新
            cp "$src_file" "$target_file"
            echo "UPDATE: $filename"
            ((updated++)) || true
        fi
    else
        # 新規コピー
        cp "$src_file" "$target_file"
        echo "COPY:   $filename"
        ((copied++)) || true
    fi
done

echo ""
echo "=== Summary ==="
echo "New:     $copied"
echo "Updated: $updated"
echo "Skipped: $skipped (unchanged)"
echo "Errors:  $errors"
echo ""
echo "Total in source:  $(find "$SOURCE_DIR" -name '*.md' -maxdepth 1 | wc -l | tr -d ' ')"
echo "Total in target:  $(find "$TARGET_DIR" -name '*.md' -maxdepth 1 | wc -l | tr -d ' ')"

#!/usr/bin/env bash
# lint-commands.sh — .claude/commands/lesson/ が .cursor/commands/lesson/ と同期しているか検証
# generate-commands.sh の実行忘れを検出する

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/.cursor/commands/lesson"
TARGET_DIR="$REPO_ROOT/.claude/commands/lesson"

errors=0
warnings=0

echo "=== Command Sync Lint ==="

# ソースが存在するか確認
if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# ターゲットが存在するか確認
if [ ! -d "$TARGET_DIR" ]; then
    echo "ERROR: Target directory does not exist: $TARGET_DIR"
    echo "  Run: bash scripts/generate-commands.sh"
    exit 1
fi

# ソースにあってターゲットにないファイル
for src_file in "$SOURCE_DIR"/*.md; do
    [ ! -f "$src_file" ] && continue
    filename="$(basename "$src_file")"
    if [ ! -f "$TARGET_DIR/$filename" ]; then
        echo "ERROR: Missing in .claude/commands/lesson/: $filename"
        ((errors++)) || true
    fi
done

# 内容の差分チェック
for src_file in "$SOURCE_DIR"/*.md; do
    [ ! -f "$src_file" ] && continue
    filename="$(basename "$src_file")"
    target_file="$TARGET_DIR/$filename"
    [ ! -f "$target_file" ] && continue

    if ! diff -q "$src_file" "$target_file" >/dev/null 2>&1; then
        echo "ERROR: Out of sync: $filename"
        ((errors++)) || true
    fi
done

# ターゲットにあってソースにないファイル（孤立ファイル）
for target_file in "$TARGET_DIR"/*.md; do
    [ ! -f "$target_file" ] && continue
    filename="$(basename "$target_file")"
    if [ ! -f "$SOURCE_DIR/$filename" ]; then
        echo "ERROR: Orphaned in .claude/commands/lesson/: $filename"
        ((errors++)) || true
    fi
done

echo ""
echo "=== Lint Summary ==="
echo "Source files:  $(find "$SOURCE_DIR" -name '*.md' -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')"
echo "Target files:  $(find "$TARGET_DIR" -name '*.md' -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')"
echo "Errors:   $errors"
echo "Warnings: $warnings"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "Fix: bash scripts/generate-commands.sh"
    exit 1
fi

#!/usr/bin/env bash
# lint-commands.sh — Cursor/Claude 共通コマンドが同期しているか検証
# generate-commands.sh の実行忘れを検出する

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/.cursor/commands/lesson"
TARGET_DIR="$REPO_ROOT/.claude/commands/lesson"
TOP_SOURCE_DIR="$REPO_ROOT/.cursor/commands"
TOP_TARGET_DIR="$REPO_ROOT/.claude/commands"

errors=0
warnings=0
shared_top_level=0

is_shared_top_level_command() {
    case "$1" in
        setup-api-key*.md|check-setup*.md|verify-module*.md|next_lesson*.md|module-18-*.md)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

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

# Top-level commands are maintained by both tools only when the same filename
# exists in both directories. .cursor/commands/utility/ remains Cursor-only and
# is intentionally excluded from this synchronization gate.
for src_file in "$TOP_SOURCE_DIR"/*.md; do
    [ ! -f "$src_file" ] && continue
    filename="$(basename "$src_file")"
    is_shared_top_level_command "$filename" || continue

    target_file="$TOP_TARGET_DIR/$filename"
    [ ! -f "$target_file" ] && continue
    ((shared_top_level++)) || true

    if ! diff -q "$src_file" "$target_file" >/dev/null 2>&1; then
        echo "ERROR: Top-level command out of sync: $filename"
        ((errors++)) || true
    fi
done

echo ""
echo "=== Lint Summary ==="
echo "Source files:  $(find "$SOURCE_DIR" -name '*.md' -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')"
echo "Target files:  $(find "$TARGET_DIR" -name '*.md' -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')"
echo "Shared top-level files: $shared_top_level"
echo "Errors:   $errors"
echo "Warnings: $warnings"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "Fix: bash scripts/generate-commands.sh"
    exit 1
fi

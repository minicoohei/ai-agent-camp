#!/usr/bin/env bash
# 全レッスン × 3 CLI テストランナー
# Usage: bash tools/run_lesson_tests.sh [cli] [lesson]
#   cli:    claude-code | codex | cursor-alt | all (default: all)
#   lesson: start-X-Y (default: all)
#
# 例: bash tools/run_lesson_tests.sh claude-code start-1-1

set -uo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_LESSONS="$BASE_DIR/.claude/commands/lesson"
CURSOR_LESSONS="$BASE_DIR/.cursor/commands/lesson"
OUTPUT_DIR="$BASE_DIR/output/test-results"
TIMEOUT=300  # 5分タイムアウト

# CLI指定
TARGET_CLI="${1:-all}"
TARGET_LESSON="${2:-all}"

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SUFFIX_PROMPT='

---
【自動テスト指示】
上記レッスンの全ステップを自動で実行し、各ステップの結果を出力してください。
対話的な質問にはデフォルトの選択肢（最初の選択肢）で自動応答してください。
外部APIの実行も含めて全て実行してください。
最後に以下の形式で実行結果サマリーを出力してください:
---
## 実行結果サマリー
- レッスン名:
- 実行ステップ数: X/Y
- 成功ステップ:
- 失敗ステップ:
- エラー詳細:
- 教材改善提案:
---'

mkdir -p "$OUTPUT_DIR/claude-code" "$OUTPUT_DIR/codex" "$OUTPUT_DIR/cursor"

# レッスン一覧取得
get_lessons() {
    if [ "$TARGET_LESSON" != "all" ]; then
        echo "$TARGET_LESSON"
    else
        ls "$CLAUDE_LESSONS"/start-*.md 2>/dev/null | \
            sed 's|.*/||; s|\.md$||' | sort -t- -k2,2n -k3,3n
    fi
}

# 一時ファイルにプロンプトを書き出してstdinで渡すヘルパー
write_prompt_file() {
    local md_file="$1"
    local prefix="$2"
    local tmpfile
    tmpfile=$(mktemp "${TMPDIR:-/tmp}/lesson-test.XXXXXXXXXX")
    {
        [ -n "$prefix" ] && echo "$prefix"
        cat "$md_file"
        echo "$SUFFIX_PROMPT"
    } > "$tmpfile"
    echo "$tmpfile"
}

# Claude Code 実行
run_claude_code() {
    local lesson="$1"
    local md_file="$CLAUDE_LESSONS/${lesson}.md"
    local out_file="$OUTPUT_DIR/claude-code/${lesson}.txt"

    if [ ! -f "$md_file" ]; then
        echo -e "${RED}SKIP${NC} $lesson: MD file not found"
        return 1
    fi

    # Skip if already has valid result (>5 lines)
    if [ -f "$out_file" ] && [ "$(wc -l < "$out_file")" -gt 5 ]; then
        echo -e "${GREEN}[claude-code] SKIP (already done)${NC} $lesson"
        return 0
    fi

    echo -e "${YELLOW}[claude-code]${NC} Running $lesson..."

    local tmpfile
    tmpfile=$(write_prompt_file "$md_file" "")

    timeout "$TIMEOUT" claude -p - \
        --allowedTools '*' \
        < "$tmpfile" \
        > "$out_file" 2>&1 || {
        echo -e "${RED}[claude-code] TIMEOUT/ERROR${NC} $lesson"
        echo "TIMEOUT or ERROR" >> "$out_file"
    }

    rm -f "$tmpfile"
    echo -e "${GREEN}[claude-code]${NC} Done: $lesson -> $out_file"
}

# Codex CLI 実行
run_codex() {
    local lesson="$1"
    local md_file="$CLAUDE_LESSONS/${lesson}.md"
    local out_file="$OUTPUT_DIR/codex/${lesson}.txt"

    if [ ! -f "$md_file" ]; then
        echo -e "${RED}SKIP${NC} $lesson: MD file not found"
        return 1
    fi

    # Skip if already has valid result (>5 lines)
    if [ -f "$out_file" ] && [ "$(wc -l < "$out_file")" -gt 5 ]; then
        echo -e "${GREEN}[codex] SKIP (already done)${NC} $lesson"
        return 0
    fi

    echo -e "${YELLOW}[codex]${NC} Running $lesson..."

    local tmpfile
    tmpfile=$(write_prompt_file "$md_file" "")

    # codex exec reads prompt from stdin when - is used
    timeout "$TIMEOUT" codex exec - \
        --full-auto \
        < "$tmpfile" \
        > "$out_file" 2>&1 || {
        echo -e "${RED}[codex] TIMEOUT/ERROR${NC} $lesson"
        echo "TIMEOUT or ERROR" >> "$out_file"
    }

    rm -f "$tmpfile"
    echo -e "${GREEN}[codex]${NC} Done: $lesson -> $out_file"
}

# Cursor 代替検証 (Claude Code で .cursor/ を使用)
run_cursor_alt() {
    local lesson="$1"
    local md_file="$CURSOR_LESSONS/${lesson}.md"
    local out_file="$OUTPUT_DIR/cursor/${lesson}.txt"

    if [ ! -f "$md_file" ]; then
        echo -e "${RED}SKIP${NC} $lesson: MD file not found"
        return 1
    fi

    # Skip if already has valid result (>5 lines)
    if [ -f "$out_file" ] && [ "$(wc -l < "$out_file")" -gt 5 ]; then
        echo -e "${GREEN}[cursor-alt] SKIP (already done)${NC} $lesson"
        return 0
    fi

    echo -e "${YELLOW}[cursor-alt]${NC} Running $lesson..."

    local tmpfile
    tmpfile=$(write_prompt_file "$md_file" "【Cursor代替検証】以下はCursorのレッスンコマンドです。Cursorユーザーとして全ステップを実行してください。")

    timeout "$TIMEOUT" claude -p - \
        --allowedTools '*' \
        < "$tmpfile" \
        > "$out_file" 2>&1 || {
        echo -e "${RED}[cursor-alt] TIMEOUT/ERROR${NC} $lesson"
        echo "TIMEOUT or ERROR" >> "$out_file"
    }

    rm -f "$tmpfile"
    echo -e "${GREEN}[cursor-alt]${NC} Done: $lesson -> $out_file"
}

# メイン実行
main() {
    local lessons
    lessons=$(get_lessons)
    local total
    total=$(echo "$lessons" | wc -l | tr -d ' ')
    local count=0

    echo "=== 全レッスン × 3 CLI テスト開始 ==="
    echo "対象: $total レッスン"
    echo "CLI: $TARGET_CLI"
    echo ""

    for lesson in $lessons; do
        count=$((count + 1))
        echo "--- [$count/$total] $lesson ---"

        case "$TARGET_CLI" in
            claude-code)
                run_claude_code "$lesson"
                ;;
            codex)
                run_codex "$lesson"
                ;;
            cursor-alt)
                run_cursor_alt "$lesson"
                ;;
            all)
                run_claude_code "$lesson"
                run_codex "$lesson"
                run_cursor_alt "$lesson"
                ;;
        esac

        echo ""
    done

    echo "=== テスト完了 ==="
    echo "結果: $OUTPUT_DIR/"
    ls -la "$OUTPUT_DIR/claude-code/" | wc -l
    ls -la "$OUTPUT_DIR/codex/" | wc -l
    ls -la "$OUTPUT_DIR/cursor/" | wc -l
}

main

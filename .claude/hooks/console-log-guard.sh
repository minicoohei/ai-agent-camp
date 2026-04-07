#!/bin/bash
# ==============================================================================
# Claude Code Hook: Console.log Guard
# ==============================================================================
#
# PostToolUse hook for Edit/Write on .ts/.tsx/.js/.jsx files.
# Warns when console.log statements are left in the edited file.
#
# Ref: cloudnative-co/claude-code-starter-kit (features/console-log-guard)
# ==============================================================================

set -euo pipefail

main() {
    local input
    input=$(cat)

    if ! command -v jq &> /dev/null; then
        exit 0
    fi

    local tool_name
    tool_name=$(echo "$input" | jq -r '.tool_name // .tool // ""')

    # Only inspect Edit and Write
    case "$tool_name" in
        Edit|Write|edit|write) ;;
        *) exit 0 ;;
    esac

    # Get file path
    local file_path
    file_path=$(echo "$input" | jq -r '.tool_input.file_path // .input.file_path // ""')

    # Only check ts/tsx/js/jsx files
    if [[ ! "$file_path" =~ \.(ts|tsx|js|jsx)$ ]]; then
        exit 0
    fi

    if [[ ! -f "$file_path" ]]; then
        exit 0
    fi

    # Check for console.log
    local console_logs
    console_logs=$(grep -n "console\.log" "$file_path" 2>/dev/null || true)

    if [[ -n "$console_logs" ]]; then
        echo "[console-log-guard] WARNING: console.log found in $file_path" >&2
        echo "$console_logs" | head -5 >&2
        if [[ $(echo "$console_logs" | wc -l) -gt 5 ]]; then
            echo "[console-log-guard] ... and more" >&2
        fi
    fi

    exit 0
}

main "$@"

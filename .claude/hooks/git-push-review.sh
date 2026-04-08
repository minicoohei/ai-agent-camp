#!/bin/bash
# ==============================================================================
# Claude Code Hook: Git Push Review Guard
# ==============================================================================
#
# PreToolUse hook for Bash commands containing "git push".
# Shows a diff summary of what will be pushed and requires confirmation.
#
# Ref: cloudnative-co/claude-code-starter-kit (features/git-push-review)
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

    if [[ ! "$tool_name" =~ ^[Bb]ash$ ]]; then
        exit 0
    fi

    local command
    command=$(echo "$input" | jq -r '.tool_input.command // .input.command // ""')

    # Only intercept git push commands (not git push --help, etc.)
    if ! echo "$command" | grep -qE '(^|[;&|] *)git push(\s|$)'; then
        exit 0
    fi

    # Show what will be pushed
    local branch remote
    branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    remote=$(git remote 2>/dev/null | head -1 || echo "origin")

    # Block push to main/master
    if [[ "$branch" == "main" || "$branch" == "master" ]]; then
        cat << EOF
{
    "decision": "block",
    "reason": "GIT PUSH REVIEW: Direct push to ${branch} is forbidden.\nCreate a feature branch and use a PR instead."
}
EOF
        exit 0
    fi

    # Show summary for review
    local summary=""
    summary+="[git-push-review] Branch: ${branch}\n"

    # Count commits ahead of remote
    local ahead_count
    ahead_count=$(git rev-list --count "${remote}/${branch}..HEAD" 2>/dev/null || echo "?")
    summary+="[git-push-review] Commits to push: ${ahead_count}\n"

    # Show changed files summary
    local changed_files
    changed_files=$(git diff --stat "${remote}/${branch}..HEAD" 2>/dev/null | tail -1 || echo "")
    if [[ -n "$changed_files" ]]; then
        summary+="[git-push-review] Changes: ${changed_files}\n"
    fi

    echo -e "$summary" >&2

    # Allow (don't block) - the summary is informational
    exit 0
}

main "$@"

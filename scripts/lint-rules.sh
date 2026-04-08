#!/usr/bin/env bash
# lint-rules.sh — .cursor/rules/ を正本として検証

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/.cursor/rules"

errors=0

echo "=== Rules Lint ==="

if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: Rules directory does not exist: $SOURCE_DIR"
    exit 1
fi

# frontmatter チェック（alwaysApply の有無）
for rule_file in "$SOURCE_DIR"/*.mdc; do
    [ ! -f "$rule_file" ] && continue
    filename="$(basename "$rule_file")"

    if ! head -1 "$rule_file" | grep -q '^---'; then
        echo "ERROR: Missing frontmatter: $filename"
        ((errors++)) || true
    fi
done

echo ""
echo "=== Lint Summary ==="
echo "Rule files: $(find "$SOURCE_DIR" -name '*.mdc' -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')"
echo "Errors:     $errors"

if [ "$errors" -gt 0 ]; then
    exit 1
fi

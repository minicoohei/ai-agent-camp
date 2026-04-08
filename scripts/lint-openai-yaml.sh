#!/usr/bin/env bash
# lint-openai-yaml.sh — SKILL.md があるスキルに agents/openai.yaml があるか検証

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

errors=0
checked=0

echo "=== openai.yaml Lint ==="

for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name="$(basename "$skill_dir")"
    [[ "$skill_name" == _* ]] && continue

    skill_md="$skill_dir/SKILL.md"
    [ ! -f "$skill_md" ] && continue

    # frontmatter に name があるスキルのみ対象
    fm_name=$(awk '/^---$/{n++; next} n==1 && /^name:/{sub(/^name: */, ""); gsub(/^"|"$/, ""); print; exit}' "$skill_md")
    [ -z "$fm_name" ] && continue

    ((checked++)) || true

    if [ ! -f "$skill_dir/agents/openai.yaml" ]; then
        echo "ERROR [$skill_name]: agents/openai.yaml が見つかりません"
        ((errors++)) || true
    fi
done

echo ""
echo "=== Lint Summary ==="
echo "Checked: $checked skills"
echo "Errors:  $errors"

if [ "$errors" -gt 0 ]; then
    echo ""
    echo "Fix: bash scripts/generate-openai-yaml.sh"
    exit 1
fi

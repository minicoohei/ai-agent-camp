#!/usr/bin/env bash
# lint-skills.sh — SKILL.md の構造検証
# 必須: frontmatter (name, description), Overview セクション
# 推奨: Usage, Workflow, Troubleshooting, Success Criteria

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

errors=0
warnings=0
checked=0

for skill_md in "$SKILLS_DIR"/*/SKILL.md; do
    skill_name="$(basename "$(dirname "$skill_md")")"

    # _template はスキップ
    [[ "$skill_name" == _* ]] && continue

    ((checked++)) || true

    # frontmatter チェック
    if ! head -1 "$skill_md" | grep -q "^---"; then
        echo "ERROR [$skill_name]: frontmatter がありません"
        ((errors++)) || true
        continue
    fi

    # pipefail 下でも安定するよう、frontmatter を一度変数化して判定
    frontmatter="$(sed -n '/^---$/,/^---$/p' "$skill_md")"

    # name フィールド
    if ! grep -q "^name:" <<< "$frontmatter"; then
        echo "ERROR [$skill_name]: frontmatter に name がありません"
        ((errors++)) || true
    fi

    # description フィールド
    if ! grep -q "^description:" <<< "$frontmatter"; then
        echo "ERROR [$skill_name]: frontmatter に description がありません"
        ((errors++)) || true
    fi

    # 推奨セクション (h1 or h2)
    for section in "Overview" "Usage" "Troubleshooting"; do
        if ! grep -qE "^#{1,2} $section" "$skill_md"; then
            echo "WARN  [$skill_name]: # $section セクションがありません"
            ((warnings++)) || true
        fi
    done
done

echo ""
echo "=== Lint Summary ==="
echo "Checked:  $checked skills"
echo "Errors:   $errors"
echo "Warnings: $warnings"

if [ "$errors" -gt 0 ]; then
    exit 1
fi

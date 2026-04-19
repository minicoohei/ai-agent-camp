#!/usr/bin/env bash
# generate-openai-yaml.sh — SKILL.md の frontmatter から agents/openai.yaml を一括生成
#
# Codex CLI は skills/{name}/agents/openai.yaml を読み込んでスキルを認識する。
# SKILL.md の name / description から display_name / short_description を生成する。
# 既存の openai.yaml がある場合は上書きしない（--force で上書き可能）。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

# オプション
FORCE=false
if [ "${1:-}" = "--force" ]; then
    FORCE=true
fi

created=0
skipped=0
existing=0
no_skill_md=0

echo "=== openai.yaml Generation ==="
echo "Source: $SKILLS_DIR/*/SKILL.md"
echo "Target: $SKILLS_DIR/*/agents/openai.yaml"
echo ""

for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name="$(basename "$skill_dir")"

    # _template はスキップ
    [[ "$skill_name" == _* ]] && continue

    skill_md="$skill_dir/SKILL.md"
    target_dir="$skill_dir/agents"
    target_file="$target_dir/openai.yaml"

    # SKILL.md がなければスキップ
    if [ ! -f "$skill_md" ]; then
        echo "SKIP (no SKILL.md): $skill_name"
        ((no_skill_md++)) || true
        continue
    fi

    # 既存の openai.yaml がある場合
    if [ -f "$target_file" ] && [ "$FORCE" = false ]; then
        ((existing++)) || true
        continue
    fi

    # frontmatter から name と description を抽出 (macOS sed 互換, マルチライン YAML 対応)
    fm_name=$(awk '/^---$/{n++; next} n==1 && /^name:/{sub(/^name: */, ""); gsub(/^"|"$/, ""); print; exit}' "$skill_md")
    fm_desc=$(awk '
      /^---$/{n++; next}
      n==1 && /^description:/{
        sub(/^description: */, "")
        gsub(/^"|"$/, "")
        if ($0 == "|" || $0 == ">") {
          # マルチライン: 次行を使用
          getline; sub(/^ +/, ""); gsub(/^"|"$/, ""); print; exit
        }
        print; exit
      }
    ' "$skill_md")

    if [ -z "$fm_name" ]; then
        echo "SKIP (no name in frontmatter): $skill_name"
        ((no_skill_md++)) || true
        continue
    fi

    # display_name: ケバブケースをタイトルケースに変換
    display_name=$(echo "$fm_name" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

    # short_description: 80文字で切る (マルチバイト安全)
    short_desc=$(printf '%s' "$fm_desc" | LC_ALL=en_US.UTF-8 cut -c1-80)

    # YAML エスケープ: ダブルクォート内の " を \" に置換
    display_name_escaped=$(echo "$display_name" | sed 's/"/\\"/g')
    short_desc_escaped=$(echo "$short_desc" | sed 's/"/\\"/g')

    # ディレクトリ作成 + YAML 書き込み
    mkdir -p "$target_dir"
    cat > "$target_file" <<YAML
interface:
  display_name: "$display_name_escaped"
  short_description: "$short_desc_escaped"
YAML

    echo "CREATE: $skill_name/agents/openai.yaml"
    ((created++)) || true
done

echo ""
echo "=== Summary ==="
echo "Created:  $created"
echo "Existing: $existing (use --force to overwrite)"
echo "Skipped:  $no_skill_md (no SKILL.md or no name)"

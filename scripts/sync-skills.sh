#!/usr/bin/env bash
# sync-skills.sh — skills/ (root) を正本として .claude/skills/ にコピーを生成
#
# 正本: skills/<name>/
# 生成: .claude/skills/<name>/  (rsync によるディレクトリコピー)
#
# Windows 互換: symlink を使わず実ディレクトリコピーで同期する。
# べき等: 差分がある場合のみ更新。既存の symlink は実コピーに置換する。
#
# Usage:
#   bash scripts/sync-skills.sh            # 同期実行
#   bash scripts/sync-skills.sh --dry-run  # 差分表示のみ (変更しない)
#   bash scripts/sync-skills.sh --check    # CI用: 差分があれば exit 1

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/skills"
TARGET_DIR="$REPO_ROOT/.claude/skills"

# 除外リスト: .claude/skills/ にコピーしないスキル
EXCLUDE_PATTERNS=(
    "_template"
    "README.md"
    "aiagent-*"
)

# rsync 除外パターン (ランタイム・キャッシュ)
RSYNC_EXCLUDES=(
    "--exclude=.venv"
    "--exclude=venv"
    "--exclude=node_modules"
    "--exclude=__pycache__"
    "--exclude=.pytest_cache"
    "--exclude=.DS_Store"
    "--exclude=*.pyc"
)

# オプション
DRY_RUN=false
CHECK_MODE=false
if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN=true
elif [ "${1:-}" = "--check" ]; then
    CHECK_MODE=true
fi

# カウンター
copied=0
updated=0
skipped=0
symlink_replaced=0
errors=0
out_of_sync=0

echo "=== Skills Sync: skills/ → .claude/skills/ ==="
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
if [ "$DRY_RUN" = true ]; then
    echo "Mode: DRY-RUN (no changes)"
elif [ "$CHECK_MODE" = true ]; then
    echo "Mode: CHECK (verify sync, exit 1 on diff)"
fi
echo ""

# ソースが存在するか確認
if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# ターゲットディレクトリ作成
mkdir -p "$TARGET_DIR"

# スキル名が除外リストに含まれるかチェック
is_excluded() {
    local name="$1"
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        case "$name" in
            $pattern) return 0 ;;
        esac
    done
    return 1
}

for skill_dir in "$SOURCE_DIR"/*/; do
    [ ! -d "$skill_dir" ] && continue

    skill_name="$(basename "$skill_dir")"

    # 除外チェック
    if is_excluded "$skill_name"; then
        continue
    fi

    # SKILL.md がないディレクトリはスキップ
    if [ ! -f "$skill_dir/SKILL.md" ]; then
        continue
    fi

    target_skill="$TARGET_DIR/$skill_name"

    # 既存の symlink を検出・置換
    if [ -L "$target_skill" ]; then
        if [ "$DRY_RUN" = true ] || [ "$CHECK_MODE" = true ]; then
            echo "SYMLINK→COPY: $skill_name (would replace symlink)"
            ((out_of_sync++)) || true
            continue
        fi
        rm "$target_skill"
        echo "SYMLINK→COPY: $skill_name"
        ((symlink_replaced++)) || true
    fi

    # rsync で同期 (--dry-run で差分チェック)
    if [ -d "$target_skill" ]; then
        # 既存ディレクトリとの差分チェック（タイムスタンプのみの差分は無視）
        # rsync itemize format: YXcstpoguax where t=timestamp only
        # タイムスタンプのみの差分を除外 (macOS openrsync=8文字, GNU rsync=11文字)
        diff_output=$(rsync -a --delete "${RSYNC_EXCLUDES[@]}" --itemize-changes "$skill_dir" "$target_skill/" 2>&1 | grep -v '^$' | grep -vE '^[.<>ch*][fdL]\.\.[t.][\. ]+' || true)

        if [ -z "$diff_output" ]; then
            ((skipped++)) || true
            continue
        fi

        if [ "$CHECK_MODE" = true ]; then
            echo "OUT OF SYNC: $skill_name"
            echo "$diff_output" | head -5
            ((out_of_sync++)) || true
            continue
        fi

        if [ "$DRY_RUN" = true ]; then
            echo "UPDATE (dry-run): $skill_name"
            echo "$diff_output" | head -5
            ((updated++)) || true
            continue
        fi

        rsync -a --delete "${RSYNC_EXCLUDES[@]}" "$skill_dir" "$target_skill/"
        echo "UPDATE: $skill_name"
        ((updated++)) || true
    else
        # 新規コピー
        if [ "$DRY_RUN" = true ] || [ "$CHECK_MODE" = true ]; then
            echo "NEW (would copy): $skill_name"
            ((out_of_sync++)) || true
            continue
        fi

        rsync -a "${RSYNC_EXCLUDES[@]}" "$skill_dir" "$target_skill/"
        echo "COPY: $skill_name"
        ((copied++)) || true
    fi
done

# .claude/skills/ に存在するが skills/ にないスキルを検出 (孤児チェック)
orphans=0
for target_dir in "$TARGET_DIR"/*/; do
    [ ! -d "$target_dir" ] && continue
    target_name="$(basename "$target_dir")"

    # 除外パターンはスキップ
    if is_excluded "$target_name"; then
        continue
    fi

    if [ ! -d "$SOURCE_DIR/$target_name" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "ORPHAN (would delete): .claude/skills/$target_name"
        elif [ "$CHECK_MODE" = true ]; then
            echo "ORPHAN: .claude/skills/$target_name (not in skills/)"
        else
            rm -rf "$target_dir"
            echo "ORPHAN DELETED: .claude/skills/$target_name"
        fi
        ((orphans++)) || true
    fi
done

echo ""
echo "=== Summary ==="
if [ "$DRY_RUN" = true ] || [ "$CHECK_MODE" = true ]; then
    echo "Out of sync: $out_of_sync"
    echo "Orphans:     $orphans"
    echo "Skipped:     $skipped (in sync)"
else
    echo "New:              $copied"
    echo "Updated:          $updated"
    echo "Symlink replaced: $symlink_replaced"
    echo "Skipped:          $skipped (unchanged)"
    echo "Orphans:          $orphans"
    echo "Errors:           $errors"
fi
echo ""
echo "Total in source:  $(find "$SOURCE_DIR" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')"
echo "Total in target:  $(find "$TARGET_DIR" -maxdepth 1 -mindepth 1 \( -type d -o -type l \) | wc -l | tr -d ' ')"

# CHECK モード: 差分があれば exit 1
if [ "$CHECK_MODE" = true ] && [ "$((out_of_sync + orphans))" -gt 0 ]; then
    echo ""
    echo "FAIL: skills/ and .claude/skills/ are out of sync."
    echo "Run 'bash scripts/sync-skills.sh' to fix."
    exit 1
fi

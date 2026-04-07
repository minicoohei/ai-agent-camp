#!/bin/bash
# =============================================================================
# pre-commit フックインストーラ
#
# `.githooks/pre-commit` を `.git/hooks/pre-commit` に同期する。
# 正本は `.githooks/pre-commit`。
#
# 使い方:
#   bash scripts/install_hooks.sh
# =============================================================================
set -euo pipefail

HOOK_PATH=".git/hooks/pre-commit"
BACKUP_PATH=".git/hooks/pre-commit.bak"
SOURCE_HOOK=".githooks/pre-commit"

# プロジェクトルートに移動
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo '.')"

# .git ディレクトリの存在確認
if [ ! -d ".git/hooks" ]; then
    echo "エラー: .git/hooks ディレクトリが見つかりません。Git リポジトリ内で実行してください。"
    exit 1
fi

# 既存フックのバックアップ
if [ -f "$HOOK_PATH" ]; then
    echo "既存の pre-commit フックをバックアップ: $BACKUP_PATH"
    cp "$HOOK_PATH" "$BACKUP_PATH"
fi

if [ ! -f "$SOURCE_HOOK" ]; then
    echo "エラー: $SOURCE_HOOK が見つかりません。"
    exit 1
fi

cp "$SOURCE_HOOK" "$HOOK_PATH"

chmod +x "$HOOK_PATH"

# core.hooksPath が設定されている場合は警告
HOOKS_PATH=$(git config core.hooksPath 2>/dev/null || true)
if [ -n "$HOOKS_PATH" ] && [ "$HOOKS_PATH" != ".git/hooks" ]; then
    echo "⚠️  core.hooksPath が '$HOOKS_PATH' に設定されています。"
    echo "   .git/hooks/pre-commit にコピーしましたが、実際には '$HOOKS_PATH' が使用されます。"
    echo "   以下のいずれかで対応してください:"
    echo "     1) git config --unset core.hooksPath  # .git/hooks を使用"
    echo "     2) cp .githooks/pre-commit $HOOKS_PATH/pre-commit  # 設定先にもコピー"
else
    echo "✅ pre-commit フックをインストールしました: $HOOK_PATH"
fi
echo "   正本: $SOURCE_HOOK"

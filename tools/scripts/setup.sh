#!/usr/bin/env bash
# setup.sh - Python 環境セットアップスクリプト（uv ベース）
# Usage: bash tools/scripts/setup.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"

echo "=== aiagent-base Python 環境セットアップ ==="
echo "Project root: $PROJECT_ROOT"

# Python3 チェック
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 が見つかりません。Python 3.10+ をインストールしてください。"
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_OK=$(python3 -c 'import sys; print(1 if sys.version_info >= (3, 10) else 0)')
echo "Python version: $PYTHON_VERSION"

if [ "$PYTHON_OK" -eq 0 ]; then
  echo "ERROR: Python 3.10 以上が必要です（現在: $PYTHON_VERSION）"
  exit 1
fi

# uv インストール
if ! command -v uv &>/dev/null; then
  echo ">>> uv をインストール中..."
  if curl -LsSf https://astral.sh/uv/install.sh | sh; then
    # インストール直後はPATHに反映されていない場合がある
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    if command -v uv &>/dev/null; then
      echo "uv $(uv --version) をインストールしました"
    else
      echo "ERROR: uv のインストールに成功しましたが、PATH に見つかりません。"
      echo "  シェルを再起動するか、以下を実行してください:"
      echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
      exit 1
    fi
  else
    echo "ERROR: uv のインストールに失敗しました。"
    echo "  手動インストール: https://docs.astral.sh/uv/getting-started/installation/"
    echo "  macOS: brew install uv"
    exit 1
  fi
else
  echo "uv: $(uv --version) (インストール済み)"
fi

# venv 作成 + 依存パッケージインストール
cd "$PROJECT_ROOT"

if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
  if [ ! -d "$VENV_DIR" ]; then
    echo ">>> uv venv .venv"
    uv venv "$VENV_DIR"
  fi
  echo ">>> uv pip install -r requirements.txt"
  uv pip install -r "$PROJECT_ROOT/requirements.txt"
  if [ -f "$PROJECT_ROOT/requirements-test.txt" ]; then
    echo ">>> uv pip install -r requirements-test.txt"
    uv pip install -r "$PROJECT_ROOT/requirements-test.txt"
  fi
else
  echo "ERROR: requirements.txt が見つかりません。"
  exit 1
fi

# gomi（安全削除ツール）インストール
if ! command -v gomi &>/dev/null; then
  echo ">>> gomi（安全削除ツール）をインストール中..."
  if command -v brew &>/dev/null; then
    if ! brew install gomi 2>/dev/null; then
      echo "WARNING: gomi のインストールに失敗しました。後で手動インストールしてください:"
      echo "  brew install gomi"
    fi
  elif command -v go &>/dev/null; then
    if ! go install github.com/b4b4r07/gomi@latest 2>/dev/null; then
      echo "WARNING: gomi のインストールに失敗しました。後で手動インストールしてください:"
      echo "  go install github.com/b4b4r07/gomi@latest"
    fi
  else
    echo "WARNING: gomi をインストールできません（brew または go が必要です）"
    echo "  macOS: brew install gomi"
    echo "  Go:    go install github.com/b4b4r07/gomi@latest"
  fi
else
  echo "gomi: $(command -v gomi) (インストール済み)"
fi

# Git hooks 設定
echo ">>> git config core.hooksPath .githooks"
cd "$PROJECT_ROOT"
git config core.hooksPath .githooks 2>/dev/null || true

# 完了メッセージ
echo ""
echo "=== セットアップ完了 ==="
echo "uv:     $(uv --version)"
echo "Python: $("$VENV_DIR/bin/python" --version 2>/dev/null || echo '(venv 未作成)')"
echo ""
echo "Python スクリプトの実行には uv run を使ってください:"
echo "  uv run python tools/credential_manager.py status"
echo ""
echo "🔐 APIキーの管理:"
echo "  uv run python tools/api_setup_wizard.py setup gemini   # 標準セットアップ"
echo "  uv run python tools/credential_manager.py status       # 状態確認"
if [ -f "$PROJECT_ROOT/.env" ]; then
  echo ""
  echo "⚠️  .env ファイルが検出されました。秘密情報を Credential Store へ移行してください:"
  echo "  uv run python tools/credential_manager.py migrate   # .env → Credential Store"
  echo "  uv run python tools/credential_manager.py cleanup   # .env から秘密情報だけ除去"
fi

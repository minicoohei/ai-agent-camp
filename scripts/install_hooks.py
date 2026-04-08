#!/usr/bin/env python3
# =============================================================================
# pre-commit フックインストーラ (Python版 / クロスプラットフォーム)
#
# `.githooks/pre-commit` を `.git/hooks/pre-commit` に同期する。
# 正本は `.githooks/pre-commit`。
#
# 使い方:
#   python scripts/install_hooks.py
# =============================================================================

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    # プロジェクトルートに移動
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("エラー: Git リポジトリが見つかりません。Git リポジトリ内で実行してください。")
        return 1
    repo_root = Path(result.stdout.strip())
    os.chdir(repo_root)

    hook_path = Path(".git/hooks/pre-commit")
    backup_path = Path(".git/hooks/pre-commit.bak")
    source_hook = Path(".githooks/pre-commit")

    # .git ディレクトリの存在確認
    if not Path(".git/hooks").is_dir():
        print("エラー: .git/hooks ディレクトリが見つかりません。Git リポジトリ内で実行してください。")
        return 1

    # 既存フックのバックアップ
    if hook_path.is_file():
        print(f"既存の pre-commit フックをバックアップ: {backup_path}")
        shutil.copy2(hook_path, backup_path)

    if not source_hook.is_file():
        print(f"エラー: {source_hook} が見つかりません。")
        return 1

    shutil.copy2(source_hook, hook_path)

    # Windows 以外では実行権限を付与
    if platform.system() != "Windows":
        os.chmod(hook_path, 0o755)

    # core.hooksPath が設定されている場合は警告
    result = subprocess.run(
        ["git", "config", "core.hooksPath"],
        capture_output=True,
        text=True,
    )
    hooks_path = result.stdout.strip() if result.returncode == 0 else ""

    if hooks_path and hooks_path != ".git/hooks":
        print(f"⚠️  core.hooksPath が '{hooks_path}' に設定されています。")
        print(f"   .git/hooks/pre-commit にコピーしましたが、実際には '{hooks_path}' が使用されます。")
        print("   以下のいずれかで対応してください:")
        print("     1) git config --unset core.hooksPath  # .git/hooks を使用")
        print(f"     2) cp .githooks/pre-commit {hooks_path}/pre-commit  # 設定先にもコピー")
    else:
        print(f"✅ pre-commit フックをインストールしました: {hook_path}")

    print(f"   正本: {source_hook}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""setup.py - Python 環境セットアップスクリプト (クロスプラットフォーム版, uv ベース)

Usage: uv run python tools/scripts/setup.py
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
VENV_DIR = PROJECT_ROOT / ".venv"
IS_WINDOWS = platform.system() == "Windows"

# venv 内パス（互換性のため残す。uv が利用可能なら uv run を優先）
if IS_WINDOWS:
    PIP_PATH = VENV_DIR / "Scripts" / "pip.exe"
    PYTHON_PATH = VENV_DIR / "Scripts" / "python.exe"
else:
    PIP_PATH = VENV_DIR / "bin" / "pip"
    PYTHON_PATH = VENV_DIR / "bin" / "python"


def run(cmd: list[str], *, check: bool = False, **kwargs) -> subprocess.CompletedProcess:
    """subprocess.run のラッパー。check=True で失敗時に終了。"""
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0 and check:
        sys.exit(result.returncode)
    return result


def check_python_version():
    """Python 3.10+ が使われているか確認。"""
    major, minor = sys.version_info.major, sys.version_info.minor
    version_str = f"{major}.{minor}"
    print(f"Python version: {version_str}")

    if (major, minor) < (3, 10):
        print(f"ERROR: Python 3.10 以上が必要です（現在: {version_str}）")
        sys.exit(1)


def check_uv():
    """uv がインストールされているか確認。なければ自動インストール。"""
    if shutil.which("uv"):
        uv_ver = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        print(f"uv: {uv_ver.stdout.strip()} (インストール済み)")
        return

    print(">>> uv をインストール中...")
    if IS_WINDOWS:
        # Windows: PowerShell 経由でインストール
        result = run(
            ["powershell", "-ExecutionPolicy", "ByPass", "-c",
             "irm https://astral.sh/uv/install.ps1 | iex"],
            capture_output=True, text=True,
        )
    else:
        # macOS / Linux: curl 経由でインストール
        result = run(
            ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
            capture_output=True, text=True,
        )

    if result.returncode != 0:
        print("ERROR: uv のインストールに失敗しました。")
        print("  手動インストール: https://docs.astral.sh/uv/getting-started/installation/")
        if IS_WINDOWS:
            print("  Windows: winget install --id=astral-sh.uv -e")
        else:
            print("  macOS: brew install uv")
        sys.exit(1)

    # PATH を更新（インストール直後は反映されていない場合がある）
    home = Path.home()
    extra_paths = [str(home / ".local" / "bin"), str(home / ".cargo" / "bin")]
    os.environ["PATH"] = os.pathsep.join(extra_paths) + os.pathsep + os.environ.get("PATH", "")

    if not shutil.which("uv"):
        print("ERROR: uv のインストールに成功しましたが、PATH に見つかりません。")
        print("  シェルを再起動してください。")
        sys.exit(1)

    uv_ver = subprocess.run(["uv", "--version"], capture_output=True, text=True)
    print(f"uv {uv_ver.stdout.strip()} をインストールしました")


def setup_venv():
    """uv venv で仮想環境を作成。"""
    if VENV_DIR.is_dir():
        print(".venv は既に存在します。依存パッケージを確認します...")
        return

    print(">>> uv venv .venv")
    result = run(["uv", "venv", str(VENV_DIR)])
    if result.returncode != 0:
        print("ERROR: venv の作成に失敗しました。")
        sys.exit(1)
    print(".venv を作成しました。")


def install_requirements():
    """uv pip install で requirements.txt をインストール。"""
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.is_file():
        print("ERROR: requirements.txt が見つかりません。")
        sys.exit(1)

    print(">>> uv pip install -r requirements.txt")
    run(["uv", "pip", "install", "-r", str(req_file), "--quiet"])

    req_test = PROJECT_ROOT / "requirements-test.txt"
    if req_test.is_file():
        print(">>> uv pip install -r requirements-test.txt")
        run(["uv", "pip", "install", "-r", str(req_test), "--quiet"])


def install_gomi():
    """gomi（安全削除ツール）のインストール。"""
    if shutil.which("gomi"):
        print(f"gomi: {shutil.which('gomi')} (インストール済み)")
        return

    print(">>> gomi（安全削除ツール）をインストール中...")
    system = platform.system()

    if system == "Darwin" and shutil.which("brew"):
        result = run(["brew", "install", "gomi"], capture_output=True)
        if result.returncode != 0:
            print("WARNING: gomi のインストールに失敗しました。後で手動インストールしてください:")
            print("  brew install gomi")
    elif shutil.which("go"):
        result = run(
            ["go", "install", "github.com/b4b4r07/gomi@latest"],
            capture_output=True,
        )
        if result.returncode != 0:
            print("WARNING: gomi のインストールに失敗しました。後で手動インストールしてください:")
            print("  go install github.com/b4b4r07/gomi@latest")
    else:
        print("WARNING: gomi をインストールできません")
        if system == "Darwin":
            print("  macOS: brew install gomi")
        elif system == "Windows":
            print("  Windows: go install github.com/b4b4r07/gomi@latest")
        else:
            print("  Linux: go install github.com/b4b4r07/gomi@latest")


def setup_git_hooks():
    """Git hooks のパスを .githooks に設定。"""
    print(">>> git config core.hooksPath .githooks")
    result = run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
    )
    if result.returncode != 0:
        print("WARNING: git config の設定に失敗しました（Git リポジトリ外の可能性）")


def print_completion():
    """完了メッセージを表示。"""
    uv_ver = subprocess.run(["uv", "--version"], capture_output=True, text=True)
    py_ver = subprocess.run(
        [str(PYTHON_PATH), "--version"], capture_output=True, text=True
    )

    print()
    print("=== セットアップ完了 ===")
    print(f"uv:     {uv_ver.stdout.strip()}")
    print(f"Python: {py_ver.stdout.strip() or '(venv 未作成)'}")
    print()
    print("Python スクリプトの実行には uv run を使ってください:")
    print("  uv run python tools/credential_manager.py status")
    print()
    print("APIキーの管理:")
    print("  uv run python tools/api_setup_wizard.py setup gemini           # 標準セットアップ")
    print("  uv run python tools/credential_manager.py status               # 状態確認")

    env_file = PROJECT_ROOT / ".env"
    if env_file.is_file():
        print()
        print("  .env ファイルが検出されました。秘密情報を Credential Store へ移行してください:")
        print("  uv run python tools/credential_manager.py migrate   # .env -> Credential Store")
        print("  uv run python tools/credential_manager.py cleanup   # .env から秘密情報だけ除去")


def main():
    print("=== aiagent-base Python 環境セットアップ ===")
    print(f"Project root: {PROJECT_ROOT}")

    check_python_version()
    check_uv()
    setup_venv()
    install_requirements()
    install_gomi()
    setup_git_hooks()
    print_completion()


if __name__ == "__main__":
    main()

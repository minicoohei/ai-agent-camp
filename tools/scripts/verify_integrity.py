#!/usr/bin/env python3
"""ai-agent-camp リポジトリの完全性検証ツール。

OSS 公開後、攻撃者が fork して README / lesson / skill を改ざん、SNS で「改良版」と
拡散して被害者にクローンさせる経路（Fork Supply Chain）への対策。

実行例:
    uv run python tools/scripts/verify_integrity.py
    uv run python tools/scripts/verify_integrity.py --json   # CI/ツール連携用

終了コード:
    0 — origin が公式リストに一致し、主要ファイルも改ざんなし
    1 — 警告あり（fork / 改変検知）。学習者は内容を確認してから実行すること
    2 — 致命的エラー（git 未インストール、リポ外実行など）

注意:
    本スクリプト自体も fork 先で書き換えられうる。`docs/security-guardrails.md` の
    「公式リポジトリ URL」セクションを目視で確認することが最終的な信頼の基点。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


OFFICIAL_REPO_URLS: tuple[str, ...] = (
    "github.com/TokenPocket/ai-agent-camp",
    "github.com/minicoohei/ai-agent-camp",
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(cmd: list[str]) -> str:
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True
    ).stdout.strip()


def _normalize_url(url: str) -> str:
    """git remote URL を比較用に正規化。HTTPS/SSH どちらも同じ形に揃える。"""
    url = url.strip()
    if url.startswith("git@"):
        url = url.replace(":", "/").replace("git@", "https://")
    if url.endswith(".git"):
        url = url[:-4]
    return url.lower()


def check_origin() -> tuple[str, str, bool]:
    """origin URL を取得し、公式リストと照合する。

    Returns:
        (status, remote_url, is_official)
        status: "ok" / "missing-origin" / "fork" / "no-git"
    """
    try:
        raw = _run(["git", "remote", "get-url", "origin"])
    except FileNotFoundError:
        return "no-git", "", False
    if not raw:
        return "missing-origin", "", False

    normalized = _normalize_url(raw)
    for official in OFFICIAL_REPO_URLS:
        if official.lower() in normalized:
            return "ok", raw, True
    return "fork", raw, False


def check_manifest_exists() -> list[str]:
    """必須の manifest / 安全ドキュメントの存在確認。

    Returns:
        存在しないファイルパスのリスト（空なら全て OK）
    """
    required = [
        "courses/lessons.manifest.yaml",
        "docs/security-guardrails.md",
        ".claude/hooks/bash_guard.py",
        ".claude/hooks/write_guard.py",
    ]
    missing: list[str] = []
    for rel in required:
        if not (REPO_ROOT / rel).exists():
            missing.append(rel)
    return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON で出力")
    args = parser.parse_args(argv)

    origin_status, origin_url, is_official = check_origin()
    missing_files = check_manifest_exists()

    report = {
        "origin_url": origin_url,
        "origin_status": origin_status,
        "is_official_origin": is_official,
        "missing_required_files": missing_files,
        "official_urls": list(OFFICIAL_REPO_URLS),
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("=== ai-agent-camp 完全性チェック ===")
        print(f"origin URL : {origin_url or '(未設定)'}")
        print(f"origin 状態 : {origin_status}")
        print(f"公式リポか  : {'yes' if is_official else 'no'}")
        if missing_files:
            print(f"欠落ファイル: {missing_files}")
        else:
            print("欠落ファイル: なし")
        print()
        if is_official and not missing_files:
            print("✅ このリポジトリは公式リストのいずれかに一致しています。")
        else:
            print("⚠️  公式リストに一致しない / 必須ファイルが欠落しています。")
            print("   fork または改変版の可能性があります。以下を確認してください:")
            for url in OFFICIAL_REPO_URLS:
                print(f"     - https://{url}")
            print("   レッスン・スキルを実行する前に差分を確認することを強く推奨します:")
            print("     git remote add upstream https://<公式URL>.git")
            print("     git fetch upstream")
            print("     git diff upstream/main -- .claude/ skills/ tools/ scripts/")

    if origin_status in ("no-git",):
        return 2
    if not is_official or missing_files:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

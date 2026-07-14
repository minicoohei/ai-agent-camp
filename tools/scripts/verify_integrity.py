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
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


OFFICIAL_REPO_URLS: tuple[str, ...] = (
    "github.com/minicoohei/ai-agent-camp",
)

REPO_ROOT = Path(__file__).resolve().parents[2]

# ハッシュ検証対象ファイル。
# 学習者が fork をクローンしたとき、upstream origin/main の同ファイルと
# 比較して差分があれば警告する。公式ハッシュは同梱しない (時間経過で陳腐化
# するため) — 代わりに `git fetch upstream && git diff upstream/main` で
# 動的に比較する方針。
INTEGRITY_TRACKED_FILES: tuple[str, ...] = (
    "courses/lessons.manifest.yaml",
    "courses/lessons.manifest.en.yaml",
    "courses/lessons.manifest.es.yaml",
    ".claude/hooks/bash_guard.py",
    ".claude/hooks/write_guard.py",
    ".claude/hooks/README.md",
    ".claude/settings.json",
    "tools/scripts/verify_integrity.py",
    "SECURITY.md",
)


def _run(cmd: list[str]) -> str:
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=False, capture_output=True, text=True
    ).stdout.strip()


def _normalize_url(url: str) -> str:
    """git remote URL を比較用に正規化。HTTPS/SSH どちらも同じ形に揃える。"""
    url = url.strip().lower()
    if url.startswith("git@"):
        url = url.replace(":", "/").replace("git@", "https://")
    if url.endswith(".git"):
        url = url[:-4]
    return url


def check_origin() -> tuple[str, str, bool]:
    """origin URL を取得し、公式リストと照合する。

    Returns:
        (status, remote_url, is_official)
        status: "ok" / "missing-origin" / "fork" / "no-git"
    """
    try:
        repo_check = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=REPO_ROOT, check=False, capture_output=True, text=True,
        )
        if repo_check.returncode != 0:
            return "no-git", "", False
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


def _sha256(path: Path) -> str | None:
    """ファイルの SHA256 を返す。存在しない / 読めない場合は None。"""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except (OSError, FileNotFoundError):
        return None


def compute_tracked_hashes() -> dict[str, str | None]:
    """INTEGRITY_TRACKED_FILES の SHA256 を計算する。

    Returns:
        {相対パス: "sha256ハッシュ" or None (欠落時)}
    """
    return {rel: _sha256(REPO_ROOT / rel) for rel in INTEGRITY_TRACKED_FILES}


def check_upstream_drift(upstream_remote: str = "upstream") -> list[dict[str, str]]:
    """upstream リモートが設定されていれば、追跡ファイルの upstream/main との
    差分をリストで返す。

    upstream が未設定の場合は空リストを返す (本関数ではエラー扱いしない)。
    """
    drift: list[dict[str, str]] = []
    # upstream リモートの有無を確認
    ret = subprocess.run(
        ["git", "remote"],
        cwd=REPO_ROOT, check=False, capture_output=True, text=True,
    )
    if upstream_remote not in ret.stdout.split():
        return drift  # upstream 未設定は呼び出し側のヒント表示に任せる

    for rel in INTEGRITY_TRACKED_FILES:
        ret = subprocess.run(
            ["git", "diff", "--quiet", f"{upstream_remote}/main", "--", rel],
            cwd=REPO_ROOT, check=False, capture_output=True, text=True,
        )
        # exit 0 = 差分なし / exit 1 = 差分あり / それ以外 = エラー
        if ret.returncode == 1:
            drift.append({"path": rel, "status": "diff"})
        elif ret.returncode not in (0, 1):
            drift.append({"path": rel, "status": "error"})
    return drift


def check_pre_commit_hook() -> tuple[bool, str]:
    """Git が実際に使用する pre-commit hook の有効性を確認する。

    `git rev-parse --git-path hooks` は linked worktree と core.hooksPath の
    両方を反映する。相対パスの場合はリポジトリルート基準で解決する。

    Returns:
        (is_active, hook_path)
    """
    try:
        raw_hooks_path = _run(["git", "rev-parse", "--git-path", "hooks"])
    except FileNotFoundError:
        return False, ""
    if not raw_hooks_path:
        return False, ""

    hooks_path = Path(raw_hooks_path)
    if not hooks_path.is_absolute():
        hooks_path = REPO_ROOT / hooks_path
    hook_path = hooks_path / "pre-commit"
    is_active = hook_path.is_file() and os.access(hook_path, os.X_OK)
    return is_active, str(hook_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON で出力")
    parser.add_argument(
        "--hashes", action="store_true",
        help="追跡対象ファイルの SHA256 を出力",
    )
    parser.add_argument(
        "--upstream", default="upstream",
        help="差分比較に使う upstream リモート名 (default: upstream)",
    )
    args = parser.parse_args(argv)

    origin_status, origin_url, is_official = check_origin()
    missing_files = check_manifest_exists()
    tracked_hashes = compute_tracked_hashes()
    drift = check_upstream_drift(upstream_remote=args.upstream)
    pre_commit_active, pre_commit_path = check_pre_commit_hook()

    report = {
        "origin_url": origin_url,
        "origin_status": origin_status,
        "is_official_origin": is_official,
        "missing_required_files": missing_files,
        "official_urls": list(OFFICIAL_REPO_URLS),
        "tracked_hashes": tracked_hashes,
        "upstream_drift": drift,
        "pre_commit_hook": {
            "active": pre_commit_active,
            "path": pre_commit_path,
        },
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.hashes:
        for rel, h in tracked_hashes.items():
            print(f"{h or '(missing)':<64}  {rel}")
    else:
        print("=== ai-agent-camp 完全性チェック ===")
        print(f"origin URL : {origin_url or '(未設定)'}")
        print(f"origin 状態 : {origin_status}")
        print(f"公式リポか  : {'yes' if is_official else 'no'}")
        if missing_files:
            print(f"欠落ファイル: {missing_files}")
        else:
            print("欠落ファイル: なし")

        if drift:
            drift_paths = [d["path"] for d in drift]
            print(f"upstream 差分: {drift_paths}")
        else:
            print("upstream 差分: (未計測 — upstream remote 未設定、または差分なし)")

        print(
            f"pre-commit : {'有効' if pre_commit_active else '無効'}"
            f" ({pre_commit_path or '解決できません'})"
        )
        if not pre_commit_active:
            print("⚠️  pre-commit 秘密情報スキャンが有効ではありません。")
            print("   次を実行してください: bash scripts/install_hooks.sh")

        print()
        if is_official and not missing_files and not drift:
            print("✅ このリポジトリは公式リストに一致し、追跡ファイルにも改変なしです。")
        else:
            print("⚠️  公式リストに一致しない / 必須ファイルが欠落 / upstream と差分があります。")
            print("   fork または改変版の可能性があります。以下を確認してください:")
            for url in OFFICIAL_REPO_URLS:
                print(f"     - https://{url}")
            print("   レッスン・スキルを実行する前に差分を確認することを強く推奨します:")
            print("     git remote add upstream https://<公式URL>.git")
            print("     git fetch upstream")
            print("     git diff upstream/main -- .claude/ skills/ tools/ scripts/")
            print()
            print("   各ファイルの SHA256 を表示:")
            print("     uv run python tools/scripts/verify_integrity.py --hashes")

    if origin_status in ("no-git",):
        return 2
    if not is_official or missing_files or drift:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

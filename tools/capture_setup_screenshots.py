#!/usr/bin/env python3
"""セットアップ系コマンドで操作するWebサイト画面のスクリーンショットを自動撮影する。

教材用スクリーンショットを取得し、公開教材向けアセットとして保存する。

方式: Playwright persistent context でユーザーの Chrome プロファイルを利用。
認証済みセッション（GitHub, Google, Slack 等）のスクリーンショットを撮影できる。

前提: Chrome を閉じた状態で実行すること（プロファイルロック回避）。

Usage:
    uv run python tools/capture_setup_screenshots.py
    uv run python tools/capture_setup_screenshots.py --step setup-gemini
    uv run python tools/capture_setup_screenshots.py --list
    uv run python tools/capture_setup_screenshots.py --auth-only
"""

import argparse
import asyncio
import subprocess
import sys
import time
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "course" / "assets" / "images" / "module0"

# Chrome プロファイルパス（macOS）
CHROME_USER_DATA = Path.home() / "Library" / "Application Support" / "Google" / "Chrome"
DEFAULT_CHROME_PROFILE = "Profile 1"  # アクティブプロファイル
CHROME_PROFILE = DEFAULT_CHROME_PROFILE

SCREENSHOTS = [
    # ── setup-start ──
    {"step": "setup-start", "filename": "setup-start-homebrew.png",
     "url": "https://brew.sh/", "description": "Homebrew 公式サイト",
     "wait": 3, "auth": False},

    # ── setup-github ── (認証必要)
    {"step": "setup-github", "filename": "setup-github-top.png",
     "url": "https://github.com/", "description": "GitHub トップページ（ログイン済み）",
     "wait": 4, "auth": True},
    {"step": "setup-github", "filename": "setup-github-new-repo.png",
     "url": "https://github.com/new", "description": "GitHub 新規リポジトリ作成ページ",
     "wait": 4, "auth": True},
    {"step": "setup-github", "filename": "setup-github-login.png",
     "url": "https://github.com/login", "description": "GitHub ログインページ（参考用）",
     "wait": 3, "auth": False},

    # ── setup-gemini ── (認証必要)
    {"step": "setup-gemini", "filename": "setup-gemini-aistudio-top.png",
     "url": "https://aistudio.google.com/", "description": "Google AI Studio トップ",
     "wait": 5, "auth": True},
    {"step": "setup-gemini", "filename": "setup-gemini-apikey-page.png",
     "url": "https://aistudio.google.com/apikey", "description": "Google AI Studio API キー管理",
     "wait": 5, "auth": True},

    # ── setup-slack ── (認証必要)
    {"step": "setup-slack", "filename": "setup-slack-api-top.png",
     "url": "https://api.slack.com/apps", "description": "Slack API Your Apps",
     "wait": 4, "auth": True},
    {"step": "setup-slack", "filename": "setup-slack-create-app.png",
     "url": "https://api.slack.com/apps?new_app=1", "description": "Slack App 新規作成ダイアログ",
     "wait": 4, "auth": True},
    {"step": "setup-slack", "filename": "setup-slack-bot-scopes.png",
     "url": "https://api.slack.com/scopes", "description": "Slack Bot Token Scopes",
     "wait": 3, "auth": False},

    # ── setup-extensions ──
    {"step": "setup-extensions", "filename": "setup-ext-marketplace.png",
     "url": "https://marketplace.visualstudio.com/vscode", "description": "VS Code Marketplace",
     "wait": 4, "auth": False},
    {"step": "setup-extensions", "filename": "setup-ext-japanese-lang.png",
     "url": "https://marketplace.visualstudio.com/items?itemName=MS-CEINTL.vscode-language-pack-ja",
     "description": "Japanese Language Pack", "wait": 4, "auth": False},

    # ── setup-security ──
    {"step": "setup-security", "filename": "setup-security-gitignore-templates.png",
     "url": "https://github.com/github/gitignore", "description": "GitHub .gitignore テンプレート",
     "wait": 3, "auth": False},

    # ── Claude for Chrome ──
    {"step": "claude-for-chrome", "filename": "setup-claude-chrome-webstore.png",
     "url": "https://chromewebstore.google.com/search/Claude%20Anthropic",
     "description": "Chrome Web Store Claude 検索結果", "wait": 4, "auth": False},
    {"step": "claude-for-chrome", "filename": "setup-claude-chrome-extension.png",
     "url": "https://chromewebstore.google.com/detail/claude/danfoobkemhkhlglmdnkbkgbhiionnpe",
     "description": "Claude for Chrome 拡張機能ページ", "wait": 4, "auth": False},
    {"step": "claude-for-chrome", "filename": "setup-claude-ai-top.png",
     "url": "https://claude.ai/", "description": "Claude.ai トップページ",
     "wait": 4, "auth": True},

    # ── check-setup ── (認証必要)
    {"step": "check-setup", "filename": "setup-check-github-settings.png",
     "url": "https://github.com/settings/tokens", "description": "GitHub PAT 設定ページ",
     "wait": 4, "auth": True},
]


def is_chrome_running() -> bool:
    result = subprocess.run(["pgrep", "-x", "Google Chrome"],
                            capture_output=True)
    return result.returncode == 0


def close_chrome():
    """Chrome を安全に閉じる"""
    if not is_chrome_running():
        return
    print("Chrome を閉じています...")
    subprocess.run(["osascript", "-e",
                     'tell application "Google Chrome" to quit'],
                    timeout=10)
    # 完全終了を待つ
    for _ in range(20):
        if not is_chrome_running():
            return
        time.sleep(0.5)
    # 強制終了
    subprocess.run(["pkill", "-9", "Google Chrome"], capture_output=True)
    time.sleep(1)


async def capture_with_persistent_context(targets: list, step_filter: str | None = None):
    """Playwright persistent context で認証済みスクリーンショットを撮影"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("ERROR: playwright がインストールされていません")
        print("  pip install playwright && playwright install chromium")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n撮影対象: {len(targets)} 件")
    print(f"保存先: {OUTPUT_DIR}")
    print(f"Chrome プロファイル: {CHROME_USER_DATA / CHROME_PROFILE}\n")

    # Chrome を閉じる
    close_chrome()
    time.sleep(1)

    success = 0
    failed = 0

    async with async_playwright() as p:
        # Chrome のユーザープロファイルを使って起動
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(CHROME_USER_DATA),
            channel="chrome",
            headless=False,  # ヘッドレスだとCookieが復号できない場合がある
            viewport={"width": 1280, "height": 900},
            args=[
                f"--profile-directory={CHROME_PROFILE}",
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            ignore_default_args=["--enable-automation"],
        )

        page = context.pages[0] if context.pages else await context.new_page()

        for i, shot in enumerate(targets, 1):
            filepath = OUTPUT_DIR / shot["filename"]
            print(f"[{i}/{len(targets)}] {shot['step']}: {shot['description']}")
            print(f"  URL: {shot['url']}")

            try:
                await page.goto(shot["url"], wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(shot.get("wait", 3) * 1000)

                await page.screenshot(path=str(filepath), full_page=False)

                if filepath.exists() and filepath.stat().st_size > 1000:
                    size_kb = filepath.stat().st_size / 1024
                    print(f"  OK: {filepath.name} ({size_kb:.0f} KB)")
                    success += 1
                else:
                    print(f"  FAIL: ファイルが小さすぎます")
                    failed += 1

            except Exception as e:
                print(f"  FAIL: {e}")
                failed += 1

        await context.close()

    print(f"\n{'=' * 50}")
    print(f"完了: {success} 成功, {failed} 失敗")
    print(f"保存先: {OUTPUT_DIR}")

    if success > 0:
        print(f"\n撮影済みファイル:")
        for f in sorted(OUTPUT_DIR.glob("setup-*.png")):
            size_kb = f.stat().st_size / 1024
            print(f"  {f.name} ({size_kb:.0f} KB)")

    return failed


def list_screenshots(step_filter: str | None = None):
    targets = SCREENSHOTS if not step_filter else [s for s in SCREENSHOTS if s["step"] == step_filter]
    print(f"\n撮影対象: {len(targets)} 件")
    print(f"保存先: {OUTPUT_DIR}\n")
    print(f"{'Step':<20} {'Filename':<45} {'Auth':<5} Description")
    print("-" * 110)
    for s in targets:
        auth = "Yes" if s.get("auth") else ""
        print(f"{s['step']:<20} {s['filename']:<45} {auth:<5} {s['description']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="セットアップ画面のスクリーンショット撮影（Chrome プロファイル使用）")
    parser.add_argument("--step", help="特定ステップのみ (例: setup-gemini)")
    parser.add_argument("--list", action="store_true", help="撮影対象一覧")
    parser.add_argument("--auth-only", action="store_true",
                        help="認証が必要なページのみ撮影")
    parser.add_argument("--profile", default=DEFAULT_CHROME_PROFILE,
                        help=f"Chrome プロファイル名 (default: {DEFAULT_CHROME_PROFILE})")
    args = parser.parse_args()

    global CHROME_PROFILE  # noqa: PLW0603
    CHROME_PROFILE = args.profile  # type: ignore[name-defined]

    if args.list:
        list_screenshots(args.step)
        return

    targets = SCREENSHOTS
    if args.step:
        targets = [s for s in targets if s["step"] == args.step]
    if args.auth_only:
        targets = [s for s in targets if s.get("auth")]

    if not targets:
        print(f"ERROR: 対象スクリーンショットがありません。")
        sys.exit(1)

    failed = asyncio.run(capture_with_persistent_context(targets, args.step))
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""setup_progress.py - セットアップ進捗トラッキング

セットアップの完了状態を .setup-progress.json に記録・表示する。
各 setup コマンド（setup-start, setup-github 等）の冒頭/末尾から呼び出される。

Usage:
    uv run python tools/setup_progress.py show                          # 進捗サマリー表示
    uv run python tools/setup_progress.py complete setup-start          # ステップを完了マーク
    uv run python tools/setup_progress.py complete setup-start --details '{"python":"3.12"}'
    uv run python tools/setup_progress.py skip setup-slack --reason '後で設定する'
    uv run python tools/setup_progress.py next                          # 次のステップを表示
    uv run python tools/setup_progress.py status setup-gemini           # 特定ステップの状態
    uv run python tools/setup_progress.py reset                         # 全リセット
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from i18n_common import setup_gettext
except ImportError:
    try:
        from tools.i18n_common import setup_gettext
    except ImportError:
        def setup_gettext():
            return lambda x: x

_ = setup_gettext()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = PROJECT_ROOT / ".setup-progress.json"

# 推奨実行順序
SETUP_ORDER = [
    {"step": "setup-start", "label": "基本ツール確認", "required": True,
     "command": "/setup-start", "description": "Python / Node.js / Git / GitHub CLI"},
    {"step": "setup-github", "label": "GitHub設定", "required": True,
     "command": "/setup-github", "description": "GitHub認証 & リポジトリ作成"},
    {"step": "setup-gemini", "label": "Gemini API", "required": True,
     "command": "/setup-gemini", "description": "Gemini APIキーの取得・設定"},
    {"step": "setup-slack", "label": "Slack API", "required": False,
     "command": "/setup-slack", "description": "Slack App作成・トークン設定"},
    {"step": "setup-fal", "label": "fal.ai API", "required": False,
     "command": "/setup-fal", "description": "fal.ai APIキーの取得・設定（動画生成用）"},
    {"step": "setup-elevenlabs", "label": "ElevenLabs API", "required": False,
     "command": "/setup-elevenlabs", "description": "ElevenLabs APIキーの取得・設定（音声合成用）"},
    {"step": "setup-notion", "label": "Notion API", "required": False,
     "command": "/setup-notion", "description": "Notion インテグレーション作成・トークン設定"},
    {"step": "setup-clasp", "label": "Clasp (GAS)", "required": False,
     "command": "/setup-clasp", "description": "Google Apps Script CLI セットアップ"},
    {"step": "setup-typefully", "label": "Typefully API", "required": False,
     "command": "/setup-typefully", "description": "Typefully APIキーの取得・設定（SNS投稿管理用）"},
    {"step": "setup-x-api", "label": "X API", "required": False,
     "command": "/setup-x-api", "description": "X API Bearer Token の取得・設定"},
    {"step": "setup-gogcli", "label": "gogcli (Google)", "required": False,
     "command": "/setup-gogcli", "description": "Google Workspace CLI（Gmail/Calendar/Drive）セットアップ"},
    {"step": "setup-bigquery", "label": "BigQuery/GCP", "required": False,
     "command": "/setup-bigquery", "description": "gcloud CLI & BigQuery 認証セットアップ"},
    {"step": "setup-vercel", "label": "Vercel CLI", "required": False,
     "command": "/setup-vercel", "description": "Vercel CLI インストール & ログイン（デプロイ用）"},
    {"step": "setup-remotion", "label": "Remotion", "required": False,
     "command": "/setup-remotion", "description": "Remotion 動画制作環境セットアップ"},
    {"step": "setup-extensions", "label": "拡張機能", "required": True,
     "command": "/setup-extensions", "description": "VS Code / Cursor 拡張機能"},
    {"step": "setup-security", "label": "セキュリティ", "required": True,
     "command": "/setup-security", "description": ".gitignore & pre-commit フック"},
    {"step": "check-setup", "label": "最終チェック", "required": True,
     "command": "/check-setup", "description": "環境全体の自動チェック"},
]

STEP_NAMES = [s["step"] for s in SETUP_ORDER]


def load_progress() -> dict:
    """進捗ファイルを読み込む。存在しなければ初期状態を返す。"""
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return _init_progress()


def _init_progress() -> dict:
    """初期状態の進捗データを生成。"""
    return {
        "version": 1,
        "last_updated": datetime.now().isoformat(timespec="seconds"),
        "steps": {
            s["step"]: {"status": "not_started", "completed_at": None, "details": {}}
            for s in SETUP_ORDER
        },
    }


def save_progress(data: dict) -> None:
    """進捗ファイルを保存。"""
    data["last_updated"] = datetime.now().isoformat(timespec="seconds")
    PROGRESS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _bar(done: int, total: int, width: int = 20) -> str:
    """プログレスバー文字列を生成。"""
    filled = int(width * done / total) if total > 0 else 0
    return "\u2588" * filled + "\u2591" * (width - filled)


def show_progress(data: dict, *, current_step: str | None = None) -> None:
    """進捗サマリーを表示。"""
    steps = data["steps"]
    done = sum(1 for s in steps.values() if s["status"] in ("completed", "skipped"))
    total = len(SETUP_ORDER)
    pct = int(100 * done / total) if total > 0 else 0

    print()
    print("\u2554" + "\u2550" * 58 + "\u2557")
    print(f"\u2551  {_('セットアップ進捗')}: {_bar(done, total)} {done}/{total} {_('完了')} ({pct}%)".ljust(59) + "\u2551")
    print("\u2560" + "\u2550" * 58 + "\u2563")

    for entry in SETUP_ORDER:
        name = entry["step"]
        label = _(entry["label"])
        st = steps.get(name, {}).get("status", "not_started")
        optional = "" if entry["required"] else _(" (任意)")

        if st == "completed":
            icon = "\u2705"
        elif st == "skipped":
            icon = "\u23ed\ufe0f "
        elif name == current_step:
            icon = "\U0001f449"
        else:
            icon = "\u2b1c"

        pointer = _("  \u2190 今ここ") if name == current_step else ""
        line = f"\u2551  {icon} {label:<18}{optional}{pointer}"
        print(line.ljust(59) + "\u2551")

    print("\u255a" + "\u2550" * 58 + "\u255d")

    if done == total:
        print()
        print(_("\U0001f389 セットアップ全完了！ /start-1-1 でレッスンを始めましょう！"))
    elif done > 0:
        nxt = _get_next(data)
        if nxt:
            info = next(s for s in SETUP_ORDER if s["step"] == nxt)
            print()
            print(_("\U0001f449 次のステップ: {cmd} ({label})").format(cmd=info['command'], label=_(info['label'])))
    print()


def _get_next(data: dict) -> str | None:
    """次に実行すべきステップ名を返す。"""
    steps = data["steps"]
    for entry in SETUP_ORDER:
        st = steps.get(entry["step"], {}).get("status", "not_started")
        if st == "not_started":
            return entry["step"]
    return None


def mark_complete(data: dict, step: str, details: dict | None = None) -> dict:
    """ステップを完了マーク。"""
    if step not in STEP_NAMES:
        print(_("ERROR: 不明なステップ: {step}").format(step=step))
        print(_("有効なステップ: {steps}").format(steps=', '.join(STEP_NAMES)))
        sys.exit(1)
    data["steps"][step] = {
        "status": "completed",
        "completed_at": datetime.now().isoformat(timespec="seconds"),
        "details": details or {},
    }
    return data


def mark_skipped(data: dict, step: str, reason: str = "") -> dict:
    """ステップをスキップマーク。"""
    if step not in STEP_NAMES:
        print(_("ERROR: 不明なステップ: {step}").format(step=step))
        print(_("有効なステップ: {steps}").format(steps=', '.join(STEP_NAMES)))
        sys.exit(1)
    data["steps"][step] = {
        "status": "skipped",
        "completed_at": datetime.now().isoformat(timespec="seconds"),
        "details": {"reason": reason},
    }
    return data


def get_step_status(data: dict, step: str) -> str:
    """特定ステップの状態を返す。"""
    return data["steps"].get(step, {}).get("status", "not_started")


def main():
    parser = argparse.ArgumentParser(description="セットアップ進捗管理")
    sub = parser.add_subparsers(dest="command")

    # show
    p_show = sub.add_parser("show", help="進捗サマリー表示")
    p_show.add_argument("--current", help="現在のステップ名をハイライト")

    # complete
    p_complete = sub.add_parser("complete", help="ステップを完了マーク")
    p_complete.add_argument("step", help="ステップ名")
    p_complete.add_argument("--details", default="{}", help="詳細情報 (JSON)")

    # skip
    p_skip = sub.add_parser("skip", help="ステップをスキップ")
    p_skip.add_argument("step", help="ステップ名")
    p_skip.add_argument("--reason", default="", help="スキップ理由")

    # next
    sub.add_parser("next", help="次のステップを表示")

    # status
    p_status = sub.add_parser("status", help="特定ステップの状態を表示")
    p_status.add_argument("step", help="ステップ名")

    # reset
    sub.add_parser("reset", help="全ステップをリセット")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    data = load_progress()

    if args.command == "show":
        show_progress(data, current_step=args.current)

    elif args.command == "complete":
        try:
            details = json.loads(args.details)
        except json.JSONDecodeError:
            details = {}
        data = mark_complete(data, args.step, details)
        save_progress(data)
        show_progress(data)

    elif args.command == "skip":
        data = mark_skipped(data, args.step, args.reason)
        save_progress(data)
        show_progress(data)

    elif args.command == "next":
        nxt = _get_next(data)
        if nxt:
            info = next(s for s in SETUP_ORDER if s["step"] == nxt)
            print(_("次のステップ: {cmd} — {label} ({desc})").format(
                cmd=info['command'], label=_(info['label']), desc=_(info['description'])))
        else:
            print(_("全ステップが完了しています！"))

    elif args.command == "status":
        st = get_step_status(data, args.step)
        print(_("{step}: {status}").format(step=args.step, status=st))

    elif args.command == "reset":
        data = _init_progress()
        save_progress(data)
        print(_("進捗をリセットしました。"))
        show_progress(data)


if __name__ == "__main__":
    main()

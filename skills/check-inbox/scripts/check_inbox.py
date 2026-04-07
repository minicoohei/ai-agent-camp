#!/usr/bin/env python3
"""
check-inbox: メールとSlackからタスク抽出

統合型スキル - メールとSlack両方を確認し、返信が必要な項目を
優先度付きでリストアップ

Usage:
  python check_inbox.py
  python check_inbox.py --days 7
  python check_inbox.py --email-only
  python check_inbox.py --slack-only
  python check_inbox.py --output /path/to/output
"""

import argparse
import json
import sys
from datetime import datetime
from dataclasses import asdict
from pathlib import Path

# スクリプトディレクトリとプロジェクトルートをパスに追加
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
_ROOT_DIR = Path(__file__).resolve().parents[3]
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from common import (
    load_dotenv,
    get_date_range,
    get_output_path,
    generate_output_markdown,
    TaskItem,
)
from email_parser import (
    load_emails,
    filter_human_emails,
    find_email_data_dir,
)
from slack_parser import (
    load_mentions,
    find_slack_data_dir,
    DEFAULT_TARGET_USERS,
)
from llm_analyzer import (
    batch_analyze_emails,
    batch_analyze_slack,
)

# .envを読み込み
try:
    from tools.credential_manager import inject_to_environ
    inject_to_environ()
except ImportError:
    try:
        from credential_manager import inject_to_environ
        inject_to_environ()
    except ImportError:
        pass
load_dotenv()



def progress_callback(current: int, total: int, item: str):
    """進捗表示コールバック"""
    print(f"  [{current}/{total}] {item}...")


def main():
    parser = argparse.ArgumentParser(
        description="メールとSlackからタスクを抽出"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=3,
        help="過去何日分を確認するか（デフォルト: 3日）"
    )

    # --email-only と --slack-only は相互排他
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--email-only",
        action="store_true",
        help="メールのみを確認"
    )
    source_group.add_argument(
        "--slack-only",
        action="store_true",
        help="Slackのみを確認"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="出力ファイルパス（省略時は自動生成）"
    )
    parser.add_argument(
        "--output-json",
        nargs="?",
        const="",
        type=str,
        help="JSON出力ファイルパス（省略時はMarkdown出力の拡張子を.jsonにして保存）"
    )
    parser.add_argument(
        "--gmail-dir",
        type=str,
        help="Gmailデータディレクトリ（省略時は自動検出）"
    )
    parser.add_argument(
        "--slack-dir",
        type=str,
        help="Slackデータディレクトリ（省略時は自動検出）"
    )
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        help="Slackワークスペース（省略時は全て）"
    )
    parser.add_argument(
        "--users", "-u",
        type=str,
        help="Slack検索対象ユーザー（カンマ区切り）"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="LLM分析をスキップ（高速だが精度低下）"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="進捗表示を抑制"
    )
    parser.add_argument(
        "--notify-line",
        action="store_true",
        help="結果をLINE Messaging APIで通知"
    )

    args = parser.parse_args()

    # 日付範囲
    start_date, end_date = get_date_range(args.days)

    print("📬 Inbox タスク抽出")
    print(f"   期間: {start_date.strftime('%Y-%m-%d')} 〜 {end_date.strftime('%Y-%m-%d')}")
    print()

    all_tasks: list[TaskItem] = []
    email_count = 0
    slack_count = 0

    # メール処理
    if not args.slack_only:
        print("📧 メールを確認中...")

        gmail_dir = Path(args.gmail_dir) if args.gmail_dir else find_email_data_dir()

        if gmail_dir and gmail_dir.exists():
            print(f"   データ: {gmail_dir}")

            # メール読み込み
            emails = load_emails(gmail_dir, start_date, end_date)
            print(f"   {len(emails)} 件のメールを検出")

            # 人からのメールをフィルタリング
            human_emails = filter_human_emails(emails)
            print(f"   {len(human_emails)} 件が人からのメール（マーケティング除外後）")
            email_count = len(human_emails)

            if human_emails and not args.no_llm:
                print("\n🤖 メールをLLMで分析中...")
                callback = None if args.quiet else progress_callback
                email_tasks = batch_analyze_emails(human_emails, callback)
                all_tasks.extend(email_tasks)
                print(f"   {len(email_tasks)} 件が返信必要")
            elif human_emails and args.no_llm:
                print("   ⚠️ --no-llm のため分析スキップ")
        else:
            print("   ⚠️ メールデータディレクトリが見つかりません")
            print("   --gmail-dir オプションで指定してください")

        print()

    # Slack処理
    if not args.email_only:
        print("💬 Slackを確認中...")

        slack_dir = Path(args.slack_dir) if args.slack_dir else find_slack_data_dir()

        if slack_dir and slack_dir.exists():
            print(f"   データ: {slack_dir}")

            # 検索対象ユーザー
            if args.users:
                users = [u.strip() for u in args.users.split(",")]
            else:
                users = DEFAULT_TARGET_USERS

            print(f"   対象ユーザー: {', '.join(users)}")

            # メンション読み込み
            mentions = load_mentions(
                slack_dir,
                users,
                start_date,
                end_date,
                args.workspace
            )
            print(f"   {len(mentions)} 件のメンションを検出")
            slack_count = len(mentions)

            if mentions and not args.no_llm:
                print("\n🤖 SlackをLLMで分析中...")
                callback = None if args.quiet else progress_callback
                slack_tasks = batch_analyze_slack(mentions, callback)
                all_tasks.extend(slack_tasks)
                print(f"   {len(slack_tasks)} 件が返信必要")
            elif mentions and args.no_llm:
                print("   ⚠️ --no-llm のため分析スキップ")
        else:
            print("   ⚠️ Slackデータディレクトリが見つかりません")
            print("   --slack-dir オプションで指定してください")

        print()

    # 結果出力
    if all_tasks:
        # 優先度でソート
        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_tasks.sort(key=lambda t: priority_order.get(t.priority, 3))

        # Markdown生成
        markdown = generate_output_markdown(
            all_tasks,
            start_date,
            end_date,
            email_count,
            slack_count
        )

        # ファイル出力
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = get_output_path("inbox")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")

        print("✅ 完了！")
        print(f"   出力: {output_path}")
        print()

        # JSON出力（オプション）
        if args.output_json is not None:
            if args.output_json:
                json_path = Path(args.output_json)
            else:
                json_path = output_path.with_suffix(".json")

            json_payload = {
                "generated_at": datetime.now().isoformat(),
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "email_count": email_count,
                "slack_count": slack_count,
                "tasks": [asdict(t) for t in all_tasks],
            }
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"   JSON出力: {json_path}")

        # サマリー表示
        high = len([t for t in all_tasks if t.priority == "high"])
        medium = len([t for t in all_tasks if t.priority == "medium"])
        low = len([t for t in all_tasks if t.priority == "low"])

        print("📊 サマリー:")
        print(f"   🔴 高優先度: {high} 件")
        print(f"   🟡 中優先度: {medium} 件")
        print(f"   🟢 低優先度: {low} 件")

        # LINE通知
        if args.notify_line:
            print()
            print("📱 LINE通知を送信中...")
            try:
                from line_notifier import notify_tasks
                notify_tasks(all_tasks, email_count, slack_count)
            except Exception as e:
                print(f"   ⚠️ LINE通知エラー: {e}")

        # コンソールにも出力（--quietでなければ）
        if not args.quiet:
            print()
            print("=" * 60)
            print(markdown)

    else:
        print("✨ 対応が必要なタスクはありません!")

        # タスクがない場合もLINE通知（オプション）
        if args.notify_line:
            try:
                from line_notifier import send_line_notification
                now = datetime.now().strftime("%Y/%m/%d %H:%M")
                send_line_notification(f"【TODOダイジェスト】{now}\n\n✨ 対応が必要なタスクはありません！")
            except Exception as e:
                print(f"   ⚠️ LINE通知エラー: {e}")

        # JSON出力（タスクが0件でも保存）
        if args.output_json is not None:
            if args.output_json:
                json_path = Path(args.output_json)
            else:
                json_path = get_output_path("inbox").with_suffix(".json")

            json_payload = {
                "generated_at": datetime.now().isoformat(),
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "email_count": email_count,
                "slack_count": slack_count,
                "tasks": [],
            }
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"   JSON出力: {json_path}")


if __name__ == "__main__":
    main()

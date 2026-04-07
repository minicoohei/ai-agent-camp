#!/usr/bin/env python3
"""
LINE通知モジュール

check-inboxの結果をLINE Messaging APIで通知
"""

import json
import os
import urllib.request
import urllib.error
from typing import Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
# プロジェクトルートをパスに追加（credential_manager 解決用）
_ROOT_DIR = Path(__file__).resolve().parents[3]
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from common import load_dotenv, TaskItem

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



def get_line_credentials() -> tuple[str, str]:
    """LINE APIの認証情報を取得

    Returns:
        (access_token, user_id) のタプル

    Raises:
        RuntimeError: 環境変数が設定されていない場合
    """
    access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    if not access_token or not user_id:
        raise RuntimeError(
            "LINE_CHANNEL_ACCESS_TOKEN または LINE_USER_ID が設定されていません。\n"
            ".env ファイルまたは環境変数に設定してください。"
        )

    return access_token, user_id


def format_tasks_for_line(
    tasks: list[TaskItem],
    email_count: int = 0,
    slack_count: int = 0,
    max_length: int = 5000
) -> str:
    """タスクをLINE用にフォーマット（全文表示版）

    Args:
        tasks: TaskItemのリスト
        email_count: メール総数
        slack_count: Slackメンション総数
        max_length: 最大文字数（LINE APIの上限は5000文字）

    Returns:
        フォーマットされたテキスト
    """
    from datetime import datetime

    now = datetime.now().strftime("%Y/%m/%d %H:%M")

    # 優先度でグループ化
    high = [t for t in tasks if t.priority == "high"]
    medium = [t for t in tasks if t.priority == "medium"]
    low = [t for t in tasks if t.priority == "low"]

    lines = [f"【TODOダイジェスト】{now}", ""]

    def add_tasks(items: list[TaskItem], emoji: str, label: str):
        if not items:
            return

        lines.append(f"{emoji} {label} ({len(items)}件)")
        lines.append("-" * 20)

        for task in items:
            source_icon = "📧" if task.source == "email" else "💬"

            if task.source == "email":
                # メール: From（送信者）を明確に表示
                lines.append(f"{source_icon} {task.title}")
                lines.append(f"  From: {task.sender}")
                lines.append(f"  日時: {task.date} {task.time}")
            else:
                # Slack: チャンネルと送信者を表示
                lines.append(f"{source_icon} [{task.channel}]")
                lines.append(f"  From: {task.sender}")
                lines.append(f"  日時: {task.date} {task.time}")
                if task.content:
                    content_preview = task.content[:150]
                    if len(task.content) > 150:
                        content_preview += "..."
                    lines.append(f"  内容: {content_preview}")

            # 判定理由
            if task.reason:
                lines.append(f"  理由: {task.reason}")

            # 返信案（全文）
            if task.draft_reply:
                lines.append(f"  返信案:")
                lines.append(f"  「{task.draft_reply}」")

            lines.append("")

    add_tasks(high, "🔴", "高優先度")
    add_tasks(medium, "🟡", "中優先度")
    add_tasks(low, "🟢", "低優先度")

    # サマリー
    lines.append("=" * 20)
    total_tasks = len(tasks)
    lines.append(f"📊 対応必要: {total_tasks}件")

    if email_count > 0:
        email_tasks = len([t for t in tasks if t.source == "email"])
        lines.append(f"  メール: {email_count}件 → {email_tasks}件要対応")

    if slack_count > 0:
        slack_tasks = len([t for t in tasks if t.source == "slack"])
        lines.append(f"  Slack: {slack_count}件 → {slack_tasks}件要対応")

    text = "\n".join(lines)

    # 長さ制限（LINE APIの上限は5000文字）
    if len(text) > max_length:
        text = text[:max_length - 50] + "\n\n...(以下省略)"

    return text


def send_line_notification(
    message: str,
    access_token: Optional[str] = None,
    user_id: Optional[str] = None
) -> bool:
    """LINE Messaging APIで通知を送信

    Args:
        message: 送信するメッセージ
        access_token: アクセストークン（省略時は環境変数から取得）
        user_id: ユーザーID（省略時は環境変数から取得）

    Returns:
        成功時True、失敗時False
    """
    if not access_token or not user_id:
        access_token, user_id = get_line_credentials()

    payload = json.dumps({
        "to": user_id,
        "messages": [{"type": "text", "text": message}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/push",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("✅ LINE通知を送信しました")
                return True
            else:
                print(f"❌ LINE API エラー: {response.status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"❌ LINE API エラー: {e.code} - {e.read().decode()}")
        return False
    except urllib.error.URLError as e:
        print(f"❌ ネットワークエラー: {e.reason}")
        return False


def notify_tasks(
    tasks: list[TaskItem],
    email_count: int = 0,
    slack_count: int = 0
) -> bool:
    """タスクをLINEで通知

    Args:
        tasks: TaskItemのリスト
        email_count: メール総数
        slack_count: Slackメンション総数

    Returns:
        成功時True、失敗時False
    """
    if not tasks:
        print("📭 通知するタスクがありません")
        return True

    message = format_tasks_for_line(tasks, email_count, slack_count)
    return send_line_notification(message)


def notify_task_issue(task: TaskItem, issue_url: str) -> bool:
    """Notify a single task with Issue URL."""
    source_label = "Email" if task.source == "email" else "Slack"
    title = task.title or "(no title)"
    sender = task.sender or "(unknown)"
    date = f"{task.date} {task.time}".strip()
    reason = f"\n理由: {task.reason}" if task.reason else ""

    message = (
        "【新規タスク】\n"
        f"種別: {source_label}\n"
        f"件名: {title}\n"
        f"From: {sender}\n"
        f"日時: {date}\n"
        f"{reason}\n\n"
        f"👉 {issue_url}"
    )
    return send_line_notification(message)


if __name__ == "__main__":
    # テスト用
    print("LINE Notifier module loaded successfully.")

    try:
        access_token, user_id = get_line_credentials()
        print("✅ LINE credentials found")
        print(f"   User ID: {user_id[:8]}...")
    except Exception as e:
        print(f"❌ LINE credentials error: {e}")

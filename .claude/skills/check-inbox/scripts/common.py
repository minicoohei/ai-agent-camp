#!/usr/bin/env python3
"""
共通ユーティリティモジュール

メール・Slackタスク抽出スキルで共通して使用する機能を提供。
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional

# プロジェクトルートをパスに追加
_ROOT_DIR = Path(__file__).resolve().parents[3]
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))


def load_dotenv(env_path: Path = None):
    """シンプルな.env読み込み"""
    paths_to_try = [
        env_path,
        Path.cwd() / ".env",
        Path.home() / "githubactions_fordata" / ".env",
        Path(__file__).parent.parent.parent.parent.parent / ".env",
        Path.home() / ".env",
    ]
    for p in paths_to_try:
        if p and p.exists():
            with open(p, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        value = value.strip().strip('"').strip("'")
                        os.environ.setdefault(key.strip(), value)
            break


# .envを読み込む
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



def get_gemini_api_key() -> str:
    """Gemini APIキーを取得"""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY または GOOGLE_API_KEY が設定されていません。\n"
            ".env ファイルに設定するか、環境変数を設定してください。"
        )
    return api_key


def get_date_range(days: int = 3) -> tuple[datetime, datetime]:
    """過去N日間の日付範囲を取得

    Args:
        days: 過去何日分を取得するか（1以上）

    Returns:
        (start_date, end_date) のタプル

    Raises:
        ValueError: days が 0 以下の場合
    """
    if days <= 0:
        raise ValueError("days must be a positive integer")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days - 1)
    return start_date.replace(hour=0, minute=0, second=0, microsecond=0), end_date


def get_output_path(prefix: str = "inbox") -> Path:
    """出力ファイルパスを生成（日付付き）"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{prefix}-{date_str}.md"

    # 出力ディレクトリ候補
    candidates = [
        Path.cwd() / "output",
        Path.home() / "output",
        Path.cwd(),
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate / filename

    return Path.cwd() / filename


@dataclass
class TaskItem:
    """タスクアイテム（メール・Slack共通）"""
    source: str  # "email" or "slack"
    title: str
    content: str
    sender: str
    date: str
    time: str
    priority: str  # "high", "medium", "low"
    reason: str
    draft_reply: str
    link: str = ""
    channel: str = ""  # Slack用
    workspace: str = ""  # Slack用
    email_id: str = ""  # メール用


def format_task_markdown(task: TaskItem) -> str:
    """タスクをMarkdown形式でフォーマット"""
    lines = []
    if task.source == "email":
        lines.append(f"- **[{task.title}]** from: {task.sender} ({task.date})")
    else:
        lines.append(f"- **[{task.channel}]** {task.sender} ({task.date} {task.time})")
        lines.append(f"  - 内容: {task.content[:80]}..." if len(task.content) > 80 else f"  - 内容: {task.content}")

    lines.append(f"  - 理由: {task.reason}")
    lines.append(f"  - 返信案: 「{task.draft_reply}」")

    if task.link:
        lines.append(f"  - リンク: {task.link}")

    return "\n".join(lines)


def generate_output_markdown(
    tasks: list[TaskItem],
    start_date: datetime,
    end_date: datetime,
    email_count: int = 0,
    slack_count: int = 0
) -> str:
    """最終出力のMarkdownを生成"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 優先度でグループ化
    high_priority = [t for t in tasks if t.priority == "high"]
    medium_priority = [t for t in tasks if t.priority == "medium"]
    low_priority = [t for t in tasks if t.priority == "low"]

    lines = [
        f"# Inbox Tasks - {today}",
        "",
    ]

    def add_priority_section(items: list[TaskItem], title: str, emoji: str):
        if not items:
            return

        lines.append(f"## {emoji} {title}")
        lines.append("")

        # メールとSlackに分離
        emails = [t for t in items if t.source == "email"]
        slacks = [t for t in items if t.source == "slack"]

        if emails:
            lines.append("### 📧 メール")
            for task in emails:
                lines.append(format_task_markdown(task))
            lines.append("")

        if slacks:
            lines.append("### 💬 Slack")
            for task in slacks:
                lines.append(format_task_markdown(task))
            lines.append("")

    add_priority_section(high_priority, "高優先度", "🔴")
    add_priority_section(medium_priority, "中優先度", "🟡")
    add_priority_section(low_priority, "低優先度", "🟢")

    if not tasks:
        lines.append("## ✨ 対応が必要なタスクはありません")
        lines.append("")

    # サマリー
    lines.append("---")
    lines.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"対象期間: {start_date.strftime('%Y-%m-%d')} 〜 {end_date.strftime('%Y-%m-%d')}")

    email_tasks = len([t for t in tasks if t.source == "email"])
    slack_tasks = len([t for t in tasks if t.source == "slack"])

    if email_count > 0:
        lines.append(f"メール件数: {email_count}件 → 要対応: {email_tasks}件")
    if slack_count > 0:
        lines.append(f"Slack件数: {slack_count}件 → 要対応: {slack_tasks}件")

    return "\n".join(lines)

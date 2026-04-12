#!/usr/bin/env python3
"""
Slack TODO自動抽出スクリプト

slack-sync/data/ のMarkdown同期データから、メンションと依頼メッセージを抽出し、
優先度・対応ステータスを判定したMarkdown / JSONレポートを生成する。

Usage:
    uv run python tools/slack_todo_extractor.py
    uv run python tools/slack_todo_extractor.py --days 7
    uv run python tools/slack_todo_extractor.py --end-date 2026-02-02 --days 14
    uv run python tools/slack_todo_extractor.py --workspace my-workspace --output outputs/custom.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "check-inbox" / "scripts"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from slack_parser import (  # type: ignore
    DEFAULT_TARGET_USERS,
    SlackMessage,
    find_slack_data_dir,
    get_slack_files,
    has_reply_from_user,
    parse_date_section,
)


DEFAULT_OUTPUT = "output/slack_todo_report.md"
DEFAULT_JSON_OUTPUT = "output/slack_todo_report.json"

HIGH_PRIORITY_KEYWORDS = [
    "至急",
    "今日中",
    "asap",
    "緊急",
    "urgent",
    "早急",
]
MEDIUM_PRIORITY_KEYWORDS = [
    "してください",
    "お願いします",
    "確認お願いします",
    "レビューお願いします",
    "対応をお願いします",
    "確認",
    "レビュー",
    "対応",
    "今週中",
    "来週まで",
    "期限",
    "締め切り",
    "〆切",
    "見積もり",
]
ACTION_PATTERNS = [
    "してください",
    "お願いします",
    "確認お願いします",
    "レビューお願いします",
    "対応をお願いします",
    "ご確認",
    "確認",
    "レビュー",
    "見積もり",
    "作成",
    "修正",
    "調査",
    "返信",
    "回答",
    "相談",
    "依頼",
    "お願い",
]
DONE_PATTERNS = ["完了", "完了しました", "対応しました", "完了です", "done", "対応済み"]
IN_PROGRESS_PATTERNS = ["承知", "対応中", "進めます", "やります", "確認します", "対応します"]
THANKS_PATTERNS = ["ありがとう", "ありがとうございます", "助かります", "thanks"]


@dataclass
class TodoItem:
    title: str
    summary: str
    workspace: str
    channel: str
    sender: str
    date: str
    time: str
    body: str
    priority: str
    status: str
    needs_reply: bool
    mentioned_user: str | None
    matched_rules: list[str]
    slack_link: str
    thread_reply_count: int

    @property
    def key(self) -> str:
        return f"{self.workspace}/{self.channel}|{self.date}|{self.time}|{self.sender}|{self.summary}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Slack TODO自動抽出")
    parser.add_argument("--days", type=int, default=14, help="対象日数 (default: 14)")
    parser.add_argument("--start-date", help="開始日 (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="終了日 (YYYY-MM-DD, default: now)")
    parser.add_argument("--workspace", default=None, help="特定ワークスペースのみ")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Markdown出力先")
    parser.add_argument(
        "--json-output",
        default=DEFAULT_JSON_OUTPUT,
        help="JSON出力先 (default: outputs/slack_todo_report.json)",
    )
    parser.add_argument(
        "--users",
        nargs="+",
        default=DEFAULT_TARGET_USERS,
        help="対象ユーザー名。空白区切りで複数指定可能",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=50,
        help="レポート詳細に含める最大件数 (default: 50)",
    )
    return parser.parse_args()


def parse_date_arg(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def resolve_date_window(args: argparse.Namespace) -> tuple[datetime, datetime]:
    end_date = parse_date_arg(args.end_date) if args.end_date else datetime.now()
    if args.start_date:
        start_date = parse_date_arg(args.start_date)
    else:
        start_date = end_date - timedelta(days=args.days)
    return start_date, end_date


def matches_user(text: str, user: str) -> bool:
    patterns = [f"@{user}", f"@{user.lower()}", f"@{user.upper()}"]
    if "(" in user:
        escaped = user.replace("(", "\\(").replace(")", "\\)")
        patterns.append(f"@{escaped}")
    lower_text = text.lower()
    return any(pattern.lower() in lower_text for pattern in patterns)


def contains_target_mention(text: str, target_users: list[str]) -> tuple[bool, str | None]:
    for user in target_users:
        if matches_user(text, user):
            return True, user
    return False, None


def extract_summary(body: str, max_length: int = 80) -> str:
    text = re.sub(r"@\S+", "", body)
    text = re.sub(r"https?://\S+", "[URL]", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_length:
        text = text[:max_length].rstrip() + "..."
    return text or "(内容なし)"


def infer_priority(message: SlackMessage, target_users: list[str]) -> tuple[str, list[str]]:
    text = message.body.lower()
    reasons: list[str] = []

    if any(keyword in text for keyword in HIGH_PRIORITY_KEYWORDS):
        reasons.append("high-keyword")
        return "high", reasons

    if re.search(r"\d{1,2}/\d{1,2}|今日|明日|今週中|来週まで", message.body):
        reasons.append("deadline")
        return "medium", reasons

    if any(keyword in text for keyword in MEDIUM_PRIORITY_KEYWORDS):
        reasons.append("request-keyword")
        return "medium", reasons

    if contains_target_mention(message.body, target_users)[0]:
        reasons.append("mention")
        return "medium", reasons

    reasons.append("informational")
    return "low", reasons


def infer_status(message: SlackMessage, target_users: list[str]) -> str:
    if not message.thread_replies:
        return "未対応"

    user_replies = [
        reply for reply in message.thread_replies
        if any(user.lower() in reply.sender.lower() for user in target_users)
    ]

    for reply in user_replies:
        lower = reply.body.lower()
        if any(pattern in lower for pattern in DONE_PATTERNS):
            return "対応済み"

    for reply in message.thread_replies:
        lower = reply.body.lower()
        if any(pattern in lower for pattern in THANKS_PATTERNS) and user_replies:
            return "対応済み"

    if user_replies:
        return "対応中"

    for reply in message.thread_replies:
        lower = reply.body.lower()
        if any(pattern in lower for pattern in IN_PROGRESS_PATTERNS):
            return "対応中"

    return "未対応"


def is_actionable(message: SlackMessage, target_users: list[str]) -> tuple[bool, list[str]]:
    rules: list[str] = []
    body = message.body
    lower = body.lower()
    has_mention, mentioned_user = contains_target_mention(body, target_users)

    if has_mention:
        rules.append(f"mention:{mentioned_user}")

    for pattern in ACTION_PATTERNS:
        if pattern.lower() in lower:
            rules.append(f"action:{pattern}")

    if "?" in body or "でしょうか" in body or "できますか" in body:
        rules.append("question")

    return bool(rules), rules


def load_messages(
    data_dir: Path,
    start_date: datetime,
    end_date: datetime,
    workspace: str | None = None,
) -> list[SlackMessage]:
    messages: list[SlackMessage] = []
    for file_path in get_slack_files(data_dir, workspace):
        content = file_path.read_text(encoding="utf-8")
        channel = file_path.stem
        current_workspace = file_path.parent.name
        sections = re.split(r"^## (\d{4}-\d{2}-\d{2})$", content, flags=re.MULTILINE)
        current_date = None
        for section in sections:
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", section):
                current_date = section
                continue
            if current_date is None:
                continue
            date_obj = datetime.strptime(current_date, "%Y-%m-%d")
            if not (start_date.date() <= date_obj.date() <= end_date.date()):
                continue
            parsed = parse_date_section(section, current_date)
            for msg in parsed:
                messages.append(
                    SlackMessage(
                        date=msg["date"],
                        time=msg["time"],
                        sender=msg["sender"],
                        body=msg["body"],
                        channel=channel,
                        workspace=current_workspace,
                        slack_link=msg["slack_link"],
                        mentioned_user="",
                        thread_replies=msg["thread_replies"],
                    )
                )
    return messages


def extract_todos(
    messages: list[SlackMessage],
    target_users: list[str],
) -> list[TodoItem]:
    todos: list[TodoItem] = []
    seen_keys: set[str] = set()

    for message in messages:
        actionable, rules = is_actionable(message, target_users)
        if not actionable:
            continue

        priority, priority_rules = infer_priority(message, target_users)
        status = infer_status(message, target_users)
        mentioned_user = contains_target_mention(message.body, target_users)[1]
        todo = TodoItem(
            title=extract_summary(message.body, max_length=48),
            summary=extract_summary(message.body, max_length=80),
            workspace=message.workspace,
            channel=message.channel,
            sender=message.sender,
            date=message.date,
            time=message.time,
            body=message.body,
            priority=priority,
            status=status,
            needs_reply=status != "対応済み" or not has_reply_from_user(message, target_users),
            mentioned_user=mentioned_user,
            matched_rules=sorted(set(rules + priority_rules)),
            slack_link=message.slack_link,
            thread_reply_count=len(message.thread_replies),
        )
        if todo.key in seen_keys:
            continue
        seen_keys.add(todo.key)
        todos.append(todo)

    priority_order = {"high": 0, "medium": 1, "low": 2}
    status_order = {"未対応": 0, "対応中": 1, "対応済み": 2}
    todos.sort(key=lambda item: (priority_order[item.priority], status_order[item.status], item.date, item.time))
    return todos


def parse_previous_report(output_path: Path) -> set[str]:
    if not output_path.exists():
        return set()

    content = output_path.read_text(encoding="utf-8")
    keys: set[str] = set()
    current_context = ""
    for line in content.splitlines():
        if line.startswith("### "):
            current_context = line[4:].strip()
        elif line.startswith("- チャンネル: "):
            channel = line.removeprefix("- チャンネル: #").strip()
            keys.add(f"{channel}|{current_context}")
    return keys


def build_diff_summary(previous_keys: set[str], current_items: list[TodoItem]) -> dict[str, int]:
    current_keys = {f"{item.workspace}/{item.channel}|{item.title}" for item in current_items}
    return {
        "new": len(current_keys - previous_keys),
        "removed": len(previous_keys - current_keys),
        "unchanged": len(current_keys & previous_keys),
    }


def build_markdown(
    todos: list[TodoItem],
    target_users: list[str],
    start_date: datetime,
    end_date: datetime,
    diff_summary: dict[str, int],
    max_items: int,
) -> str:
    priority_counts = Counter(item.priority for item in todos)
    status_counts = Counter(item.status for item in todos)
    channel_counts = Counter(f"{item.workspace}/{item.channel}" for item in todos)

    lines = [
        "# Slack TODO レポート",
        f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"対象期間: {start_date:%Y-%m-%d} 〜 {end_date:%Y-%m-%d}",
        f"対象ユーザー: {', '.join(target_users)}",
        "",
        "## サマリー",
        f"- 総TODO数: {len(todos)}件",
        f"- 高優先度: {priority_counts.get('high', 0)}件",
        f"- 中優先度: {priority_counts.get('medium', 0)}件",
        f"- 低優先度: {priority_counts.get('low', 0)}件",
        f"- 未対応: {status_counts.get('未対応', 0)}件",
        f"- 対応中: {status_counts.get('対応中', 0)}件",
        f"- 対応済み: {status_counts.get('対応済み', 0)}件",
        "",
        "## 前回レポートとの差分",
        f"- 新規: {diff_summary['new']}件",
        f"- 解消: {diff_summary['removed']}件",
        f"- 継続: {diff_summary['unchanged']}件",
        "",
    ]

    for label, key in [("高優先度", "high"), ("中優先度", "medium"), ("低優先度", "low")]:
        items = [item for item in todos if item.priority == key][:max_items]
        lines.append(f"## {label}")
        lines.append("")
        if not items:
            lines.append("- なし")
            lines.append("")
            continue
        for index, item in enumerate(items, 1):
            lines.extend(
                [
                    f"### {index}. {item.title}",
                    f"- チャンネル: #{item.workspace}/{item.channel}",
                    f"- 依頼者: {item.sender}",
                    f"- 日時: {item.date} {item.time}",
                    f"- 内容: {item.summary}",
                    f"- ステータス: {item.status}",
                    f"- 判定ルール: {', '.join(item.matched_rules)}",
                    f"- スレッド返信数: {item.thread_reply_count}",
                ]
            )
            if item.slack_link:
                lines.append(f"- Slackリンク: {item.slack_link}")
            lines.append("")

    lines.append("## チャンネル別集計")
    lines.append("")
    for channel, count in channel_counts.most_common(10):
        lines.append(f"- #{channel}: {count}件")
    if not channel_counts:
        lines.append("- なし")
    lines.append("")

    lines.append("## 対応ステータス別")
    lines.append("")
    for status in ["未対応", "対応中", "対応済み"]:
        items = [item for item in todos if item.status == status][:10]
        lines.append(f"### {status}")
        if not items:
            lines.append("- なし")
            lines.append("")
            continue
        for item in items:
            lines.append(f"- {item.title} (#{item.workspace}/{item.channel}, {item.date} {item.time})")
        lines.append("")

    return "\n".join(lines)


def write_outputs(
    todos: list[TodoItem],
    markdown: str,
    output_path: Path,
    json_output_path: Path,
    start_date: datetime,
    end_date: datetime,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    json_output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "todos": [asdict(item) for item in todos],
    }
    json_output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    start_date, end_date = resolve_date_window(args)
    data_dir = find_slack_data_dir()
    if data_dir is None:
        print("エラー: Slackデータディレクトリが見つかりません")
        return 1

    print(f"期間: {start_date:%Y-%m-%d} 〜 {end_date:%Y-%m-%d}")
    print(f"対象ユーザー: {args.users}")
    print(f"Slackデータ: {data_dir}")

    output_path = Path(args.output)
    json_output_path = Path(args.json_output)
    previous_keys = parse_previous_report(output_path)

    messages = load_messages(data_dir, start_date, end_date, args.workspace)
    print(f"対象メッセージ数: {len(messages)}")
    todos = extract_todos(messages, args.users)
    print(f"抽出TODO数: {len(todos)}")

    diff_summary = build_diff_summary(previous_keys, todos)
    markdown = build_markdown(
        todos=todos,
        target_users=args.users,
        start_date=start_date,
        end_date=end_date,
        diff_summary=diff_summary,
        max_items=args.max_items,
    )
    write_outputs(todos, markdown, output_path, json_output_path, start_date, end_date)

    print(f"Markdown出力: {output_path.absolute()}")
    print(f"JSON出力: {json_output_path.absolute()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

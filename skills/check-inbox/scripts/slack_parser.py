#!/usr/bin/env python3
"""
Slackパーサーモジュール

slack-sync/data/ 配下のMarkdownファイルからメンションを抽出
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SlackMessage:
    """Slackメッセージデータ"""
    date: str
    time: str
    sender: str
    body: str
    channel: str
    workspace: str
    slack_link: str
    mentioned_user: str
    thread_replies: list = field(default_factory=list)


@dataclass
class ThreadReply:
    """スレッド返信"""
    time: str
    sender: str
    body: str
    slack_link: str = ""


def parse_date_section(content: str, current_date: str) -> list[dict]:
    """
    日付セクション内のメッセージをパース

    Args:
        content: セクション内容
        current_date: 日付文字列 (YYYY-MM-DD)

    Returns:
        メッセージの辞書リスト
    """
    messages = []

    # メッセージパターン: ### HH:MM - Sender [[Slack]](url)
    message_pattern = re.compile(
        r"### (\d{2}:\d{2}) - ([^\[\n]+?)(?:\s*\[\[Slack\]\]\(([^)]+)\))?\n(.*?)(?=\n### \d{2}:\d{2}|\n---|\n## \d{4}|$)",
        re.DOTALL
    )

    for match in message_pattern.finditer(content):
        time_str = match.group(1)
        sender = match.group(2).strip()
        slack_link = match.group(3) or ""
        body = match.group(4)

        # メイン本文（スレッド返信より前の部分）
        main_body = body.split("> #### ")[0] if "> #### " in body else body
        main_body = main_body.strip()

        # スレッド返信を抽出
        thread_replies = []
        reply_pattern = re.compile(
            r"> #### (\d{2}:\d{2}) - ([^\[\n]+?)(?:\s*\[\[Slack\]\]\(([^)]+)\))?\n((?:> [^\n]*\n?)*)"
        )

        seen_replies = set()
        for reply_match in reply_pattern.finditer(body):
            reply_time = reply_match.group(1)
            reply_sender = reply_match.group(2).strip()
            reply_link = reply_match.group(3) or ""
            reply_body = reply_match.group(4)

            # 重複チェック
            reply_key = f"{reply_time}:{reply_sender}"
            if reply_key in seen_replies:
                continue
            seen_replies.add(reply_key)

            # "> " プレフィックスを除去
            reply_body = "\n".join(
                line[2:] if line.startswith("> ") else line
                for line in reply_body.split("\n")
            ).strip()

            thread_replies.append({
                "time": reply_time,
                "sender": reply_sender,
                "body": reply_body,
                "slack_link": reply_link
            })

        messages.append({
            "date": current_date,
            "time": time_str,
            "sender": sender,
            "body": main_body,
            "slack_link": slack_link,
            "thread_replies": thread_replies
        })

    return messages


def find_mentions_in_file(
    file_path: Path,
    users: list[str],
    start_date: datetime,
    end_date: datetime
) -> list[SlackMessage]:
    """
    ファイル内でユーザーへのメンションを検索

    Args:
        file_path: Markdownファイルのパス
        users: 検索対象ユーザーリスト
        start_date: 開始日
        end_date: 終了日

    Returns:
        SlackMessageオブジェクトのリスト
    """
    mentions = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # チャンネル名を取得（ファイル名から）
    channel = file_path.stem
    workspace = file_path.parent.name

    def matches_user(text: str, user: str) -> bool:
        user_patterns = [
            f"@{user}",
            f"@{user.lower()}",
            f"@{user.upper()}",
        ]
        if "(" in user:
            escaped_user = user.replace("(", "\\(").replace(")", "\\)")
            user_patterns.append(f"@{escaped_user}")

        for pattern in user_patterns:
            if pattern.lower() in text.lower():
                return True

        return False

    # 日付セクションごとに分割
    date_sections = re.split(r"^## (\d{4}-\d{2}-\d{2})$", content, flags=re.MULTILINE)

    current_date = None
    for i, section in enumerate(date_sections):
        # 日付ヘッダー
        if re.match(r"^\d{4}-\d{2}-\d{2}$", section):
            current_date = section
            continue

        if current_date is None:
            continue

        # 期間チェック
        try:
            date_obj = datetime.strptime(current_date, "%Y-%m-%d")
            if not (start_date.date() <= date_obj.date() <= end_date.date()):
                continue
        except ValueError:
            continue

        # セクション内のメッセージをパース
        messages = parse_date_section(section, current_date)

        # メンションを検索
        for msg in messages:
            body = msg["body"]
            matched = False  # 同じメッセージが複数回追加されるのを防ぐフラグ

            for user in users:
                if matched:
                    break  # 既にマッチしていたら次のメッセージへ

                if matches_user(body, user):
                    mentions.append(SlackMessage(
                        date=msg["date"],
                        time=msg["time"],
                        sender=msg["sender"],
                        body=body,
                        channel=channel,
                        workspace=workspace,
                        slack_link=msg["slack_link"],
                        mentioned_user=user,
                        thread_replies=[
                            ThreadReply(**r) for r in msg["thread_replies"]
                        ]
                    ))
                    matched = True  # フラグを立てる
                    break  # パターンループを抜ける

            reply_mentions_seen = set()
            for reply in msg["thread_replies"]:
                reply_body = reply.get("body", "")
                for user in users:
                    if matches_user(reply_body, user):
                        reply_key = f"{reply.get('time')}:{reply.get('sender')}:{user.lower()}"
                        if reply_key in reply_mentions_seen:
                            continue
                        reply_mentions_seen.add(reply_key)

                        mentions.append(SlackMessage(
                            date=msg["date"],
                            time=reply.get("time", msg["time"]),
                            sender=reply.get("sender", msg["sender"]),
                            body=reply_body,
                            channel=channel,
                            workspace=workspace,
                            slack_link=msg["slack_link"] or reply.get("slack_link"),
                            mentioned_user=user,
                            thread_replies=[]
                        ))

    return mentions


def find_slack_data_dir() -> Optional[Path]:
    """
    Slackデータディレクトリを探す

    Returns:
        見つかったディレクトリのパス、見つからない場合は None
    """
    candidates = [
        Path.cwd() / "slack-sync" / "data",
        Path(__file__).parent.parent.parent.parent.parent / "slack-sync" / "data",
        Path.home() / "githubactions_fordata" / "slack-sync" / "data",
        Path.home() / "slack-sync" / "data",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            # 中身があるかチェック
            if any(candidate.iterdir()):
                return candidate

    return None


def get_slack_files(
    data_dir: Path,
    workspace: str = None
) -> list[Path]:
    """
    Slackデータファイルを取得

    Args:
        data_dir: slack-sync/data/ ディレクトリ
        workspace: 特定のワークスペース（Noneの場合は全て）

    Returns:
        ファイルパスのリスト
    """
    files = []

    if workspace:
        ws_dir = data_dir / workspace
        if ws_dir.exists():
            files.extend(ws_dir.glob("*.md"))
    else:
        for ws_dir in data_dir.iterdir():
            if ws_dir.is_dir() and not ws_dir.name.startswith("."):
                files.extend(ws_dir.glob("*.md"))

    return sorted(files)


def load_mentions(
    data_dir: Path,
    users: list[str],
    start_date: datetime,
    end_date: datetime,
    workspace: str = None
) -> list[SlackMessage]:
    """
    指定期間のメンションを読み込み

    Args:
        data_dir: slack-sync/data/ ディレクトリ（Noneの場合は自動検出）
        users: 検索対象ユーザーリスト
        start_date: 開始日
        end_date: 終了日
        workspace: 特定のワークスペース（Noneの場合は全て）

    Returns:
        SlackMessageオブジェクトのリスト
    """
    if data_dir is None:
        data_dir = find_slack_data_dir()
        if data_dir is None:
            raise FileNotFoundError(
                "Slackデータディレクトリが見つかりません。\n"
                "以下のいずれかにデータを配置してください:\n"
                "  - ./slack-sync/data/\n"
                "  - ~/githubactions_fordata/slack-sync/data/"
            )

    all_mentions = []

    files = get_slack_files(data_dir, workspace)

    for file_path in files:
        try:
            mentions = find_mentions_in_file(file_path, users, start_date, end_date)
            all_mentions.extend(mentions)
        except Exception as e:
            print(f"  ⚠️ ファイル読み込みエラー: {file_path}: {e}")

    return all_mentions


def has_reply_from_user(message: SlackMessage, users: list[str]) -> bool:
    """
    ユーザーからの返信があるかチェック

    Args:
        message: SlackMessageオブジェクト
        users: ユーザーリスト

    Returns:
        返信がある場合True
    """
    for reply in message.thread_replies:
        for user in users:
            if user.lower() in reply.sender.lower():
                return True
    return False


def extract_task_summary(body: str, max_length: int = 100) -> str:
    """
    メッセージ本文からタスク要約を抽出

    Args:
        body: メッセージ本文
        max_length: 最大文字数

    Returns:
        要約テキスト
    """
    # @メンションを除去
    text = re.sub(r"@\S+", "", body)
    # URLを除去
    text = re.sub(r"https?://\S+", "[URL]", text)
    # 改行を空白に
    text = re.sub(r"\n+", " ", text)
    # 先頭の空白を除去
    text = text.strip()

    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text


# デフォルトの検索対象ユーザー
# 自分の Slack 表示名・ユーザー名に書き換えてください
# 例: ["Taro Yamada", "taro.yamada", "taro"]
DEFAULT_TARGET_USERS = [
    u.strip() for u in os.environ.get("CHECK_INBOX_SLACK_USERS", "").split(",")
    if u.strip()
] if os.environ.get("CHECK_INBOX_SLACK_USERS") else []


if __name__ == "__main__":
    # テスト用
    import sys

    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        users = DEFAULT_TARGET_USERS
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()

        mentions = find_mentions_in_file(file_path, users, start_date, end_date)
        print(f"💬 {len(mentions)} 件のメンションを検出")
        for m in mentions[:5]:
            print(f"  - [{m.channel}] {m.sender} -> @{m.mentioned_user} ({m.date} {m.time})")
    else:
        print("Usage: python slack_parser.py <slack_channel.md>")

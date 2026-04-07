#!/usr/bin/env python3
"""
Slack メッセージ取得スクリプト（複数ワークスペース対応）

GitHub Actionsから定期実行され、新規メッセージをMarkdown形式で保存します。

使い方:
  python fetch_slack.py                    # 全ワークスペースを処理
  python fetch_slack.py --workspace yoake  # 特定のワークスペースのみ
  python fetch_slack.py --workspace infobox
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# パス設定
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent

# .envファイルを読み込み（slack-sync/.env または親ディレクトリの.env）
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR.parent / ".env")

# ワークスペース設定
# 方法1: SLACK_WORKSPACES 環境変数にJSON配列で設定（推奨）
#   SLACK_WORKSPACES='[{"name":"myteam","token_env":"SLACK_USER_TOKEN","domain":"myteam"}]'
# 方法2: SLACK_USER_TOKEN だけ設定すると "default" ワークスペースとして動作
# 方法3: SLACK_USER_TOKEN_{NAME} を複数設定（自動検出）
def _load_workspaces() -> dict:
    """環境変数からワークスペース設定を動的に構築"""
    workspaces = {}

    # 方法1: JSON設定（最優先）
    ws_json = os.getenv("SLACK_WORKSPACES", "").strip()
    if ws_json:
        import json as _json
        for entry in _json.loads(ws_json):
            name = entry["name"]
            workspaces[name] = {
                "token_env": entry.get("token_env", f"SLACK_USER_TOKEN_{name.upper()}"),
                "display_name": entry.get("display_name", name),
                "slack_domain": entry.get("domain", ""),
            }
        return workspaces

    # 方法2/3: 環境変数から自動検出
    # SLACK_USER_TOKEN（デフォルト）
    if os.getenv("SLACK_USER_TOKEN"):
        workspaces["default"] = {
            "token_env": "SLACK_USER_TOKEN",
            "display_name": "Default",
            "slack_domain": os.getenv("SLACK_DOMAIN", ""),
        }

    # SLACK_USER_TOKEN_{NAME} パターンを検出
    prefix = "SLACK_USER_TOKEN_"
    for key in os.environ:
        if key.startswith(prefix) and key != "SLACK_USER_TOKEN":
            name = key[len(prefix):].lower()
            workspaces[name] = {
                "token_env": key,
                "display_name": name.replace("_", " ").title(),
                "slack_domain": os.getenv(f"SLACK_DOMAIN_{name.upper()}", ""),
            }

    return workspaces


WORKSPACES = _load_workspaces()

# 特定チャンネルのみ取得する場合（カンマ区切り）、空なら全チャンネル
TARGET_CHANNELS = os.getenv("SLACK_TARGET_CHANNELS", "").split(",") if os.getenv("SLACK_TARGET_CHANNELS") else []

# スレッド返信取得のカットオフ日時（2025-11-01 00:00:00 UTC）
# これ以降に更新されたスレッドのみ返信を取得
THREAD_CUTOFF_TS = str(datetime(2025, 11, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp())


def get_my_user_id(client: WebClient) -> Optional[str]:
    """自分のユーザーIDを取得（auth.test API使用）
    
    User Tokenを使用しているため、そのトークンの所有者のIDを返します。
    
    Args:
        client: Slack WebClient
    
    Returns:
        ユーザーID（例: U12345678）、取得失敗時はNone
    """
    try:
        result = client.auth_test()
        return result.get("user_id")
    except SlackApiError as e:
        print(f"⚠️ auth.test エラー: {e.response['error']}")
        return None


def get_workspace_paths(workspace_name: str) -> tuple[Path, Path]:
    """ワークスペースごとのデータディレクトリと同期ファイルパスを取得"""
    data_dir = ROOT_DIR / "data" / workspace_name
    data_dir.mkdir(parents=True, exist_ok=True)
    sync_file = ROOT_DIR / f".last_sync_{workspace_name}.json"
    return data_dir, sync_file


def load_sync_state(sync_file: Path) -> dict:
    """同期状態を読み込み
    
    構造:
    {
        "channels": {
            "CHANNEL_ID": {
                "name": "channel-name",
                "latest_ts": "1234567890.123456",
                "threads": {
                    "THREAD_TS": {
                        "latest_reply": "1234567890.123456",
                        "reply_count": 5
                    }
                },
                "my_tracked_posts": {
                    "THREAD_TS": {
                        "type": "my_post" | "mentioned",
                        "last_checked_reply_count": 0
                    }
                }
            }
        },
        "last_updated": "2025-01-01T00:00:00+00:00"
    }
    """
    if sync_file.exists():
        with open(sync_file, "r", encoding="utf-8") as f:
            state = json.load(f)
            # 既存の構造にthreadsやmy_tracked_postsがない場合は追加（後方互換）
            for ch_id, ch_data in state.get("channels", {}).items():
                if "threads" not in ch_data:
                    ch_data["threads"] = {}
                if "my_tracked_posts" not in ch_data:
                    ch_data["my_tracked_posts"] = {}
            return state
    return {"channels": {}, "last_updated": None}


def save_sync_state(state: dict, sync_file: Path):
    """同期状態を保存"""
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(sync_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_user_name(client: WebClient, user_id: str, user_cache: dict) -> str:
    """ユーザーIDから表示名を取得（キャッシュ付き）"""
    if user_id in user_cache:
        return user_cache[user_id]
    
    try:
        result = client.users_info(user=user_id)
        user = result["user"]
        # 表示名 > 実名 > ユーザー名 の優先順位
        name = (
            user.get("profile", {}).get("display_name") or
            user.get("real_name") or
            user.get("name") or
            user_id
        )
        user_cache[user_id] = name
        return name
    except SlackApiError:
        user_cache[user_id] = user_id
        return user_id


def format_timestamp(ts: str) -> tuple[str, str]:
    """Slackタイムスタンプを日付と時刻に変換"""
    dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
    # ローカルタイムに変換（JSTを想定）
    dt_jst = dt + timedelta(hours=9)
    date_str = dt_jst.strftime("%Y-%m-%d")
    time_str = dt_jst.strftime("%H:%M")
    return date_str, time_str


def is_my_post_or_mentioned(msg: dict, my_user_id: str) -> tuple[bool, str]:
    """
    自分の投稿またはメンションされた投稿かどうかを判定
    
    Args:
        msg: Slackメッセージ
        my_user_id: 自分のユーザーID
    
    Returns:
        tuple: (追跡対象かどうか, タイプ "my_post" | "mentioned" | "")
    """
    if not my_user_id:
        return False, ""
    
    user = msg.get("user", "")
    text = msg.get("text", "")
    
    if user == my_user_id:
        return True, "my_post"
    elif f"<@{my_user_id}>" in text:
        return True, "mentioned"
    return False, ""


def fetch_thread_replies(
    client: WebClient,
    channel_id: str,
    thread_ts: str,
    user_cache: dict,
    slack_domain: str = ""
) -> list[str]:
    """
    スレッドの返信を取得（親メッセージは除外）
    
    Args:
        client: Slack WebClient
        channel_id: チャンネルID
        thread_ts: スレッドの親メッセージのタイムスタンプ
        user_cache: ユーザー名キャッシュ
        slack_domain: Slackドメイン（リンク生成用）
    
    Returns:
        返信メッセージのMarkdown文字列リスト
    """
    replies_md = []
    
    try:
        result = client.conversations_replies(
            channel=channel_id,
            ts=thread_ts,
            limit=200
        )
        
        for reply in result.get("messages", []):
            # 親メッセージは除外（thread_tsと同じtsのメッセージ）
            if reply.get("ts") == thread_ts:
                continue
            
            # フォーマット
            formatted = format_message_to_markdown(
                reply, client, user_cache,
                channel_id=channel_id,
                slack_domain=slack_domain,
                is_thread_reply=True
            )
            if formatted:
                replies_md.append(formatted)
        
        # レート制限回避のため1秒待機
        time.sleep(1)
        
    except SlackApiError as e:
        print(f"    ⚠️ スレッド返信の取得エラー: {e.response['error']}")
    
    return replies_md


def format_message_to_markdown(
    message: dict,
    client: WebClient,
    user_cache: dict,
    channel_id: str = "",
    slack_domain: str = "",
    is_thread_reply: bool = False
) -> Optional[str]:
    """メッセージをMarkdown形式に変換
    
    Args:
        message: Slackメッセージオブジェクト
        client: Slack WebClient
        user_cache: ユーザー名キャッシュ
        channel_id: チャンネルID（リンク生成用）
        slack_domain: Slackドメイン（リンク生成用）
        is_thread_reply: スレッド返信の場合True（インデント付きで出力）
    """
    # ボットメッセージやシステムメッセージは除外
    if message.get("subtype") in ["bot_message", "channel_join", "channel_leave"]:
        return None
    
    text = message.get("text", "")
    if not text.strip():
        return None
    
    user_id = message.get("user", "unknown")
    user_name = get_user_name(client, user_id, user_cache)
    ts = message.get("ts", "0")
    date_str, time_str = format_timestamp(ts)
    
    # ユーザーメンションを解決 <@U123> -> @username
    def replace_mention(match):
        uid = match.group(1)
        return f"@{get_user_name(client, uid, user_cache)}"
    
    text = re.sub(r"<@(U[A-Z0-9]+)>", replace_mention, text)
    
    # チャンネルメンションを解決 <#C123|channel-name> -> #channel-name
    text = re.sub(r"<#[A-Z0-9]+\|([^>]+)>", r"#\1", text)
    
    # URLリンクを解決 <http://...|label> -> [label](http://...)
    text = re.sub(r"<(https?://[^|>]+)\|([^>]+)>", r"[\2](\1)", text)
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)
    
    # SlackリンクをURLに変換（ts: 1234567890.123456 -> p1234567890123456）
    slack_link = ""
    if channel_id and slack_domain:
        ts_for_url = ts.replace(".", "")
        slack_url = f"https://{slack_domain}.slack.com/archives/{channel_id}/p{ts_for_url}"
        slack_link = f" [[Slack]]({slack_url})"
    
    if is_thread_reply:
        # スレッド返信はインデント（引用形式）で出力
        # 複数行のテキストも各行をインデント
        indented_text = "\n".join(f"> {line}" for line in text.split("\n"))
        return f"> #### {time_str} - {user_name}{slack_link}\n{indented_text}\n"
    else:
        return f"### {time_str} - {user_name}{slack_link}\n{text}\n"


def fetch_channel_messages(
    client: WebClient,
    channel_id: str,
    channel_name: str,
    oldest: Optional[str] = None,
    user_cache: dict = None,
    slack_domain: str = "",
    sync_state: dict = None,
    my_user_id: Optional[str] = None
) -> tuple[list[dict], str, dict, dict]:
    """チャンネルのメッセージを取得（スレッド返信含む）
    
    Returns:
        tuple: (メッセージリスト, 最新タイムスタンプ, スレッド情報dict, 自分の追跡投稿dict)
    """
    if user_cache is None:
        user_cache = {}
    
    messages = []
    latest_ts = oldest or "0"
    thread_count = 0
    threads_info = {}  # スレッド情報を収集
    my_tracked_posts = {}  # 自分の投稿/メンション追跡
    
    try:
        # メッセージを取得（oldest以降の新しいメッセージ）
        kwargs = {
            "channel": channel_id,
            "limit": 200,
        }
        if oldest:
            kwargs["oldest"] = oldest
        
        result = client.conversations_history(**kwargs)
        
        for msg in result.get("messages", []):
            ts = msg.get("ts", "0")
            if float(ts) > float(latest_ts):
                latest_ts = ts
            
            # 親メッセージをフォーマット
            formatted = format_message_to_markdown(
                msg, client, user_cache,
                channel_id=channel_id,
                slack_domain=slack_domain
            )
            
            # 自分の投稿/メンションを追跡
            is_tracked, track_type = is_my_post_or_mentioned(msg, my_user_id)
            if is_tracked:
                # スレッドの親TS（スレッドでない場合はメッセージ自体のTS）
                thread_ts = msg.get("thread_ts") or ts
                reply_count = msg.get("reply_count", 0)
                my_tracked_posts[thread_ts] = {
                    "type": track_type,
                    "last_checked_reply_count": reply_count
                }
            
            # スレッド返信を取得（2025年11月以降に更新されたスレッドのみ）
            thread_replies_md = ""
            reply_count = msg.get("reply_count", 0)
            latest_reply = msg.get("latest_reply", "0")
            
            # スレッド情報を記録（返信がある場合）
            if reply_count >= 1:
                thread_ts = msg.get("thread_ts") or ts
                threads_info[thread_ts] = {
                    "latest_reply": latest_reply,
                    "reply_count": reply_count,
                    "creator": msg.get("user", "unknown")  # 親メッセージの投稿者
                }
                
                # 2025年11月以降のスレッドのみ返信を取得
                if float(latest_reply) >= float(THREAD_CUTOFF_TS):
                    replies = fetch_thread_replies(
                        client, channel_id, thread_ts, user_cache, slack_domain
                    )
                    if replies:
                        thread_replies_md = "\n" + "\n".join(replies)
                        thread_count += 1
            
            if formatted:
                date_str, _ = format_timestamp(ts)
                messages.append({
                    "date": date_str,
                    "ts": ts,
                    "content": formatted + thread_replies_md
                })
        
        # 古い順にソート
        messages.sort(key=lambda x: float(x["ts"]))
        
        if thread_count > 0:
            print(f"    🧵 {thread_count} 件のスレッド返信を取得")
        
        if my_tracked_posts:
            print(f"    👤 {len(my_tracked_posts)} 件の自分の投稿/メンションを追跡")
        
    except SlackApiError as e:
        print(f"⚠️ チャンネル {channel_name} の取得エラー: {e.response['error']}")
    
    return messages, latest_ts, threads_info, my_tracked_posts


def append_to_markdown_file(data_dir: Path, channel_name: str, messages: list[dict]):
    """Markdownファイルにメッセージを追記"""
    if not messages:
        return
    
    file_path = data_dir / f"{channel_name}.md"
    
    # 既存のコンテンツを読み込み
    existing_content = ""
    existing_dates = set()
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
            # 既存の日付セクションを抽出
            existing_dates = set(re.findall(r"^## (\d{4}-\d{2}-\d{2})$", existing_content, re.MULTILINE))
    
    # 日付ごとにグループ化
    by_date = {}
    for msg in messages:
        date = msg["date"]
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(msg["content"])
    
    # 新しいコンテンツを生成
    new_sections = []
    for date in sorted(by_date.keys(), reverse=True):
        if date in existing_dates:
            # 既存の日付セクションに追記（ファイル内の該当箇所を更新）
            section_content = "\n".join(by_date[date])
            # 既存セクションの末尾に追加
            existing_content = existing_content.replace(f"## {date}\n", f"## {date}\n{section_content}\n", 1)
        else:
            # 新しい日付セクション
            section = f"## {date}\n\n" + "\n".join(by_date[date])
            new_sections.append(section)
    
    # ファイルに書き込み
    if not existing_content:
        # 新規ファイル
        content = f"# {channel_name}\n\n" + "\n---\n\n".join(new_sections)
    else:
        # 既存ファイルに新しいセクションを先頭に追加
        if new_sections:
            # ヘッダーの後に挿入
            header_end = existing_content.find("\n\n") + 2
            content = (
                existing_content[:header_end] +
                "\n---\n\n".join(new_sections) +
                "\n---\n\n" +
                existing_content[header_end:]
            )
        else:
            content = existing_content
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  📝 {len(messages)} 件のメッセージを追加")


def append_thread_replies_to_markdown(
    data_dir: Path,
    channel_name: str,
    thread_ts: str,
    replies_md: list[str],
    slack_domain: str = ""
):
    """
    既存のMarkdownファイルにスレッド返信を追記
    
    親メッセージの直後（次のメッセージの前、または日付セクションの区切り前）に
    スレッド返信を挿入します。
    
    Args:
        data_dir: データディレクトリ
        channel_name: チャンネル名
        thread_ts: 親メッセージのタイムスタンプ
        replies_md: 返信メッセージのMarkdown文字列リスト
        slack_domain: Slackドメイン（リンク生成用）
    """
    if not replies_md:
        return False
    
    file_path = data_dir / f"{channel_name}.md"
    if not file_path.exists():
        return False
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 親メッセージのSlackリンクからURLパターンを生成
    # ts: 1234567890.123456 -> p1234567890123456
    ts_for_url = thread_ts.replace(".", "")
    slack_url_pattern = f"p{ts_for_url}"
    
    # 親メッセージを見つける
    # パターン: ### HH:MM - username [[Slack]](https://...archives/CHANNEL/pTIMESTAMP)
    parent_pattern = rf"(### \d{{2}}:\d{{2}} - .+\[\[Slack\]\]\([^)]*{slack_url_pattern}\)[^\n]*\n(?:.*?\n)*?)"
    
    match = re.search(parent_pattern, content, re.DOTALL)
    if not match:
        # Slackリンクなしの場合も探す（古い形式）
        # タイムスタンプから時刻を計算して検索
        dt = datetime.fromtimestamp(float(thread_ts), tz=timezone.utc)
        dt_jst = dt + timedelta(hours=9)
        time_str = dt_jst.strftime("%H:%M")
        date_str = dt_jst.strftime("%Y-%m-%d")
        
        # 日付セクション内で時刻が一致するメッセージを探す
        date_section_pattern = rf"## {date_str}\n(.*?)(?=\n---\n|\n## \d{{4}}-\d{{2}}-\d{{2}}\n|$)"
        date_match = re.search(date_section_pattern, content, re.DOTALL)
        if not date_match:
            return False
        
        # 該当時刻のメッセージを探す
        time_pattern = rf"(### {time_str} - [^\n]+\n(?:.*?\n)*?)(?=### \d{{2}}:\d{{2}}|\n---\n|\n## |$)"
        time_match = re.search(time_pattern, date_match.group(1), re.DOTALL)
        if not time_match:
            return False
        
        # 挿入位置を計算
        insert_pos = date_match.start(1) + time_match.end()
    else:
        # 親メッセージの末尾位置を取得
        # 次のメッセージ（### で始まる行）または日付区切り（---）または日付見出し（## ）の前
        parent_end = match.end()
        remaining = content[parent_end:]
        
        # 親メッセージの本文を取得（次の見出しまで）
        next_msg_match = re.search(r"^(### \d{2}:\d{2}|---\n|## \d{4})", remaining, re.MULTILINE)
        if next_msg_match:
            insert_pos = parent_end + next_msg_match.start()
        else:
            insert_pos = len(content)
    
    # 既にスレッド返信が存在する場合は、新しい返信のみ追加
    # 返信は > で始まる行で識別
    check_range = content[match.end() if match else insert_pos:insert_pos + 500] if match else ""
    
    # 返信を挿入
    replies_content = "\n" + "\n".join(replies_md)
    new_content = content[:insert_pos] + replies_content + content[insert_pos:]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return True


def append_to_my_thread_replies(
    data_dir: Path,
    channel_name: str,
    replies_info: list[dict],
):
    """
    自分のスレッドへの返信を専用ファイルに記録
    
    Args:
        data_dir: データディレクトリ
        channel_name: チャンネル名
        replies_info: 返信情報のリスト（各要素は{"date", "time", "sender", "message", "slack_url"}）
    """
    if not replies_info:
        return
    
    file_path = data_dir / "_my_thread_replies.md"
    
    # 既存のコンテンツを読み込み
    existing_content = ""
    existing_dates = set()
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
            existing_dates = set(re.findall(r"^## (\d{4}-\d{2}-\d{2})$", existing_content, re.MULTILINE))
    
    # 日付ごとにグループ化
    by_date = {}
    for info in replies_info:
        date = info["date"]
        if date not in by_date:
            by_date[date] = []
        
        # フォーマット: ### #channel-name - HH:MM - ユーザー名 [[Slack]](URL)
        entry = f"### #{channel_name} - {info['time']} - {info['sender']}"
        if info.get("slack_url"):
            entry += f" [[Slack]]({info['slack_url']})"
        entry += f"\n{info['message']}\n"
        by_date[date].append(entry)
    
    # 新しいコンテンツを生成
    new_sections = []
    for date in sorted(by_date.keys(), reverse=True):
        if date in existing_dates:
            # 既存の日付セクションに追記
            section_content = "\n".join(by_date[date])
            existing_content = existing_content.replace(
                f"## {date}\n", f"## {date}\n\n{section_content}\n", 1
            )
        else:
            # 新しい日付セクション
            section = f"## {date}\n\n" + "\n".join(by_date[date])
            new_sections.append(section)
    
    # ファイルに書き込み
    if not existing_content:
        # 新規ファイル
        content = "# 自分のスレッドへの返信\n\n" + "\n---\n\n".join(new_sections)
    else:
        # 既存ファイルに新しいセクションを先頭に追加
        if new_sections:
            header_end = existing_content.find("\n\n") + 2
            content = (
                existing_content[:header_end] +
                "\n---\n\n".join(new_sections) +
                "\n---\n\n" +
                existing_content[header_end:]
            )
        else:
            content = existing_content
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  📩 自分のスレッドへの返信 {len(replies_info)} 件を記録")


def check_and_update_thread_replies(
    client: WebClient,
    channel_id: str,
    channel_name: str,
    sync_state: dict,
    user_cache: dict,
    data_dir: Path,
    slack_domain: str = "",
    my_user_id: Optional[str] = None
) -> tuple[int, list[dict]]:
    """
    既存スレッドの返信更新をチェックし、新しい返信があればMarkdownに追記
    自分の投稿/メンション追跡対象も含めてチェック
    
    Args:
        client: Slack WebClient
        channel_id: チャンネルID
        channel_name: チャンネル名
        sync_state: 同期状態
        user_cache: ユーザー名キャッシュ
        data_dir: データディレクトリ
        slack_domain: Slackドメイン
        my_user_id: 自分のユーザーID（自分のスレッドへの返信を検出するため）
    
    Returns:
        tuple: (更新されたスレッド数, 自分のスレッドへの返信情報リスト)
    """
    channel_state = sync_state["channels"].get(channel_id, {})
    saved_threads = channel_state.get("threads", {})
    # my_tracked_posts を sync_state から直接参照（更新が反映されるように）
    if "my_tracked_posts" not in channel_state:
        channel_state["my_tracked_posts"] = {}
    my_tracked_posts = channel_state["my_tracked_posts"]
    my_thread_replies = []  # 自分のスレッドへの返信を収集
    
    updated_count = 0
    
    # 最近のメッセージを取得して、スレッドの更新をチェック
    # 過去14日間のメッセージを対象（追跡投稿のカバレッジを広げる）
    oldest_ts = str((datetime.now(timezone.utc) - timedelta(days=14)).timestamp())
    
    try:
        result = client.conversations_history(
            channel=channel_id,
            limit=200,
            oldest=oldest_ts
        )
        
        for msg in result.get("messages", []):
            thread_ts = msg.get("thread_ts") or msg.get("ts")
            if not thread_ts:
                continue
            
            current_reply_count = msg.get("reply_count", 0)
            current_latest_reply = msg.get("latest_reply", "0")
            
            # 自分の投稿/メンションを検出して追跡対象に追加（過去メッセージも含む）
            is_tracked, track_type = is_my_post_or_mentioned(msg, my_user_id)
            if is_tracked and thread_ts not in my_tracked_posts:
                my_tracked_posts[thread_ts] = {
                    "type": track_type,
                    "last_checked_reply_count": 0  # 初回は0から開始
                }
            
            # 追跡対象かどうかをチェック
            is_saved_thread = thread_ts in saved_threads
            is_tracked_post = thread_ts in my_tracked_posts
            
            if not is_saved_thread and not is_tracked_post:
                # 追跡対象でなければスキップ
                continue
            
            # 保存済みの返信数を取得
            saved_reply_count = 0
            if is_saved_thread:
                saved_reply_count = saved_threads[thread_ts].get("reply_count", 0)
                saved_latest_reply = saved_threads[thread_ts].get("latest_reply", "0")
            elif is_tracked_post:
                saved_reply_count = my_tracked_posts[thread_ts].get("last_checked_reply_count", 0)
                saved_latest_reply = "0"  # 追跡投稿は初回チェック時
            
            # 新しい返信があるかチェック
            has_new_replies = (
                current_reply_count > saved_reply_count or
                (is_saved_thread and float(current_latest_reply) > float(saved_latest_reply))
            )
            
            if has_new_replies and current_reply_count > 0:
                source = "追跡投稿" if is_tracked_post and not is_saved_thread else "スレッド"
                print(f"    🔄 {source}更新検出: {thread_ts}")
                
                # スレッド返信を取得
                all_replies = fetch_thread_replies(
                    client, channel_id, thread_ts, user_cache, slack_domain
                )
                
                if all_replies:
                    # 新しい返信のみをフィルタリング
                    new_replies = all_replies[saved_reply_count:]
                    
                    if new_replies:
                        # Markdownファイルに追記
                        success = append_thread_replies_to_markdown(
                            data_dir, channel_name, thread_ts, new_replies, slack_domain
                        )
                        
                        if success:
                            updated_count += 1
                            print(f"      ✅ {len(new_replies)} 件の新しい返信を追加")
                        
                        # 自分のスレッドへの返信かチェック
                        is_my_thread = (
                            (is_saved_thread and saved_threads[thread_ts].get("creator") == my_user_id) or
                            (is_tracked_post and my_tracked_posts[thread_ts].get("type") == "my_post")
                        )
                        
                        if my_user_id and is_my_thread:
                            # 新しい返信の詳細情報を収集
                            try:
                                thread_result = client.conversations_replies(
                                    channel=channel_id,
                                    ts=thread_ts,
                                    limit=200
                                )
                                # 新しい返信のみを抽出（saved_reply_count以降）
                                reply_messages = [
                                    m for m in thread_result.get("messages", [])
                                    if m.get("ts") != thread_ts
                                ][saved_reply_count:]
                                
                                for reply_msg in reply_messages:
                                    reply_ts = reply_msg.get("ts", "0")
                                    date_str, time_str = format_timestamp(reply_ts)
                                    sender = get_user_name(client, reply_msg.get("user", "unknown"), user_cache)
                                    
                                    # Slack URL生成
                                    slack_url = ""
                                    if slack_domain:
                                        ts_for_url = reply_ts.replace(".", "")
                                        slack_url = f"https://{slack_domain}.slack.com/archives/{channel_id}/p{ts_for_url}"
                                    
                                    my_thread_replies.append({
                                        "date": date_str,
                                        "time": time_str,
                                        "sender": sender,
                                        "message": reply_msg.get("text", ""),
                                        "slack_url": slack_url
                                    })
                            except SlackApiError:
                                pass  # エラー時はスキップ
                
                # スレッド状態を更新
                if is_saved_thread:
                    existing_creator = saved_threads.get(thread_ts, {}).get("creator", msg.get("user", "unknown"))
                    saved_threads[thread_ts] = {
                        "latest_reply": current_latest_reply,
                        "reply_count": current_reply_count,
                        "creator": existing_creator
                    }
                
                # 追跡投稿の状態を更新
                if is_tracked_post:
                    my_tracked_posts[thread_ts]["last_checked_reply_count"] = current_reply_count
        
    except SlackApiError as e:
        print(f"    ⚠️ スレッド更新チェックエラー: {e.response['error']}")
    
    return updated_count, my_thread_replies


def sync_workspace(workspace_name: str, workspace_config: dict) -> bool:
    """単一ワークスペースを同期"""
    token_env = workspace_config["token_env"]
    display_name = workspace_config["display_name"]
    slack_domain = workspace_config.get("slack_domain", "")
    token = os.getenv(token_env)
    
    if not token:
        print(f"⏭️  {display_name}: {token_env} が設定されていないためスキップ")
        return False
    
    print(f"\n{'='*50}")
    print(f"🔄 {display_name} ワークスペースの同期を開始...")
    print(f"{'='*50}")
    
    data_dir, sync_file = get_workspace_paths(workspace_name)
    client = WebClient(token=token)
    sync_state = load_sync_state(sync_file)
    user_cache = {}
    
    # 自分のユーザーIDを取得
    my_user_id = get_my_user_id(client)
    if my_user_id:
        print(f"👤 自分のユーザーID: {my_user_id}")
    
    # チャンネル一覧を取得
    try:
        channels = []
        
        # パブリックチャンネル
        result = client.conversations_list(types="public_channel", limit=1000)
        channels.extend(result.get("channels", []))
        
        # プライベートチャンネル
        result = client.conversations_list(types="private_channel", limit=1000)
        channels.extend(result.get("channels", []))
        
        print(f"📋 {len(channels)} 個のチャンネルを検出")
        
    except SlackApiError as e:
        print(f"❌ チャンネル一覧の取得エラー: {e.response['error']}")
        return False
    
    # 各チャンネルを処理
    updated_channels = 0
    thread_updated_count = 0
    all_my_thread_replies = []  # 全チャンネルの自分のスレッドへの返信を収集
    
    for channel in channels:
        channel_id = channel["id"]
        channel_name = channel["name"]
        
        # 特定チャンネルのみ処理（設定されている場合）
        if TARGET_CHANNELS and channel_id not in TARGET_CHANNELS and channel_name not in TARGET_CHANNELS:
            continue
        
        # アーカイブ済みチャンネルはスキップ
        if channel.get("is_archived"):
            continue
        
        print(f"📂 {channel_name} を処理中...")
        
        # チャンネル状態を初期化（存在しない場合）
        if channel_id not in sync_state["channels"]:
            sync_state["channels"][channel_id] = {
                "name": channel_name,
                "latest_ts": None,
                "threads": {},
                "my_tracked_posts": {}
            }
        else:
            if "threads" not in sync_state["channels"][channel_id]:
                sync_state["channels"][channel_id]["threads"] = {}
            if "my_tracked_posts" not in sync_state["channels"][channel_id]:
                sync_state["channels"][channel_id]["my_tracked_posts"] = {}
        
        # 前回の同期タイムスタンプを取得
        oldest = sync_state["channels"][channel_id].get("latest_ts")
        
        # Step 1: 既存スレッドの更新をチェック
        thread_updates, my_replies = check_and_update_thread_replies(
            client, channel_id, channel_name, sync_state,
            user_cache, data_dir, slack_domain, my_user_id
        )
        if thread_updates > 0:
            thread_updated_count += thread_updates
        
        # 自分のスレッドへの返信を収集（チャンネル名を追加）
        for reply in my_replies:
            reply["channel_name"] = channel_name
        all_my_thread_replies.extend(my_replies)
        
        # Step 2: 新しいメッセージを取得
        messages, latest_ts, new_threads_info, new_tracked_posts = fetch_channel_messages(
            client, channel_id, channel_name, oldest, user_cache,
            slack_domain=slack_domain, sync_state=sync_state, my_user_id=my_user_id
        )
        
        if messages:
            append_to_markdown_file(data_dir, channel_name, messages)
            updated_channels += 1
        
        # 同期状態を更新
        sync_state["channels"][channel_id]["name"] = channel_name
        sync_state["channels"][channel_id]["latest_ts"] = latest_ts
        
        # 新しいスレッド情報をマージ
        sync_state["channels"][channel_id]["threads"].update(new_threads_info)
        
        # 自分の投稿/メンション追跡情報をマージ
        sync_state["channels"][channel_id]["my_tracked_posts"].update(new_tracked_posts)
    
    # 同期状態を保存
    save_sync_state(sync_state, sync_file)
    
    # 自分のスレッドへの返信を専用ファイルに記録
    if all_my_thread_replies:
        # チャンネル名でグループ化して記録
        by_channel = {}
        for reply in all_my_thread_replies:
            ch = reply.pop("channel_name")
            if ch not in by_channel:
                by_channel[ch] = []
            by_channel[ch].append(reply)
        
        for ch_name, replies in by_channel.items():
            append_to_my_thread_replies(data_dir, ch_name, replies)
    
    print()
    print(f"✅ {display_name}: {updated_channels} チャンネル更新, {thread_updated_count} スレッド返信追加")
    if all_my_thread_replies:
        print(f"   📩 自分のスレッドへの返信: {len(all_my_thread_replies)} 件")
    
    return True


def refresh_threads_for_channel(
    client: WebClient,
    channel_id: str,
    channel_name: str,
    sync_state: dict,
    user_cache: dict,
    data_dir: Path,
    slack_domain: str = "",
    days_back: int = 14
) -> int:
    """
    過去N日間のスレッド返信を再取得してMarkdownを更新
    
    既に同期済みの親メッセージに対して、スレッド返信を後追いで取得します。
    
    Args:
        client: Slack WebClient
        channel_id: チャンネルID
        channel_name: チャンネル名
        sync_state: 同期状態
        user_cache: ユーザー名キャッシュ
        data_dir: データディレクトリ
        slack_domain: Slackドメイン
        days_back: 何日前まで遡るか
    
    Returns:
        追加されたスレッド返信数
    """
    # チャンネル状態を初期化
    if channel_id not in sync_state["channels"]:
        sync_state["channels"][channel_id] = {
            "name": channel_name,
            "latest_ts": None,
            "threads": {}
        }
    elif "threads" not in sync_state["channels"][channel_id]:
        sync_state["channels"][channel_id]["threads"] = {}
    
    saved_threads = sync_state["channels"][channel_id]["threads"]
    
    # 過去N日間のメッセージを取得
    oldest_ts = str((datetime.now(timezone.utc) - timedelta(days=days_back)).timestamp())
    updated_count = 0
    
    try:
        result = client.conversations_history(
            channel=channel_id,
            limit=500,
            oldest=oldest_ts
        )
        
        for msg in result.get("messages", []):
            reply_count = msg.get("reply_count", 0)
            if reply_count < 1:
                continue
            
            thread_ts = msg.get("thread_ts") or msg.get("ts")
            latest_reply = msg.get("latest_reply", "0")
            
            # 2025年11月以降のスレッドのみ対象
            if float(latest_reply) < float(THREAD_CUTOFF_TS):
                continue
            
            # 既にスレッド情報があり、返信数が変わっていなければスキップ
            if thread_ts in saved_threads:
                saved_reply_count = saved_threads[thread_ts].get("reply_count", 0)
                if reply_count <= saved_reply_count:
                    continue
            
            print(f"    🧵 スレッド検出: {thread_ts} ({reply_count} 返信)")
            
            # スレッド返信を取得
            replies = fetch_thread_replies(
                client, channel_id, thread_ts, user_cache, slack_domain
            )
            
            if replies:
                # 既存の返信数以降の新しい返信のみ
                saved_reply_count = saved_threads.get(thread_ts, {}).get("reply_count", 0)
                new_replies = replies[saved_reply_count:]
                
                if new_replies:
                    success = append_thread_replies_to_markdown(
                        data_dir, channel_name, thread_ts, new_replies, slack_domain
                    )
                    if success:
                        updated_count += len(new_replies)
                        print(f"      ✅ {len(new_replies)} 件の返信を追加")
            
            # スレッド情報を更新（creatorも保存）
            existing_creator = saved_threads.get(thread_ts, {}).get("creator", msg.get("user", "unknown"))
            saved_threads[thread_ts] = {
                "latest_reply": latest_reply,
                "reply_count": reply_count,
                "creator": existing_creator
            }
    
    except SlackApiError as e:
        print(f"    ⚠️ エラー: {e.response['error']}")
    
    return updated_count


def main():
    parser = argparse.ArgumentParser(
        description="Slackメッセージ取得ツール（複数ワークスペース対応）"
    )
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        choices=list(WORKSPACES.keys()) if WORKSPACES else None,
        help="特定のワークスペースのみ処理（省略時は全ワークスペース）"
    )
    parser.add_argument(
        "--refresh-threads",
        action="store_true",
        help="過去14日間のスレッド返信を再スキャンして更新"
    )
    parser.add_argument(
        "--channel", "-c",
        type=str,
        help="特定チャンネルのみ処理（--refresh-threads と併用）"
    )
    
    args = parser.parse_args()
    
    print("🚀 Slack同期を開始...")
    
    # 処理対象ワークスペースを決定
    if args.workspace:
        workspaces_to_sync = {args.workspace: WORKSPACES[args.workspace]}
    else:
        workspaces_to_sync = WORKSPACES
    
    # 各ワークスペースを処理
    success_count = 0
    for ws_name, ws_config in workspaces_to_sync.items():
        if args.refresh_threads:
            # スレッド返信の再スキャンモード
            token = os.getenv(ws_config["token_env"])
            if not token:
                print(f"⏭️  {ws_config['display_name']}: トークン未設定でスキップ")
                continue
            
            print(f"\n{'='*50}")
            print(f"🔄 {ws_config['display_name']} スレッド再スキャン...")
            print(f"{'='*50}")
            
            data_dir, sync_file = get_workspace_paths(ws_name)
            client = WebClient(token=token)
            sync_state = load_sync_state(sync_file)
            user_cache = {}
            slack_domain = ws_config.get("slack_domain", "")
            
            # チャンネル一覧を取得
            try:
                channels = []
                result = client.conversations_list(types="public_channel,private_channel", limit=1000)
                channels.extend(result.get("channels", []))
            except SlackApiError as e:
                print(f"❌ エラー: {e.response['error']}")
                continue
            
            total_updated = 0
            for channel in channels:
                if channel.get("is_archived"):
                    continue
                
                channel_id = channel["id"]
                channel_name = channel["name"]
                
                # 特定チャンネルのフィルタ
                if args.channel and channel_name != args.channel:
                    continue
                
                print(f"📂 {channel_name} をスキャン中...")
                
                updated = refresh_threads_for_channel(
                    client, channel_id, channel_name, sync_state,
                    user_cache, data_dir, slack_domain
                )
                total_updated += updated
            
            save_sync_state(sync_state, sync_file)
            print(f"\n✅ {total_updated} 件のスレッド返信を追加")
            success_count += 1
        else:
            # 通常の同期モード
            if sync_workspace(ws_name, ws_config):
                success_count += 1
    
    print()
    print("=" * 50)
    print(f"🎉 全体完了: {success_count}/{len(workspaces_to_sync)} ワークスペースを同期")
    print("=" * 50)
    
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

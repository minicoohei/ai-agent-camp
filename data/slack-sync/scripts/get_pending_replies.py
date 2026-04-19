#!/usr/bin/env python3
"""
Slack返信が必要な投稿を取得するスクリプト

以下のカテゴリの投稿を取得します：
1. 自分へのメンション（@ユーザー名）を含むメッセージ（未返信）
2. 自分のスレッドへの他人からの返信（未返信）
3. DMで自分に来たメッセージ

使い方:
  python get_pending_replies.py                    # 全ワークスペース
  python get_pending_replies.py --workspace my-workspace  # 特定ワークスペースのみ
  python get_pending_replies.py --days 3           # 過去3日間のみ
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# パス設定
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent

# .envファイルを読み込み
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR.parent / ".env")

# ワークスペース設定
# 自分のワークスペースに合わせて追加・変更してください。
# slack_domain はワークスペースの Slack URL に含まれるドメイン部分です。
WORKSPACES = {
    "my-workspace": {
        "token_env": "SLACK_USER_TOKEN",
        "display_name": "My Workspace",
        "slack_domain": "my-workspace",
    },
    # 複数ワークスペースを使う場合は以下のように追加:
    # "my-workspace-2": {
    #     "token_env": "SLACK_USER_TOKEN_WS2",
    #     "display_name": "My Workspace 2",
    #     "slack_domain": "my-workspace-2",
    # },
}


@dataclass
class PendingReply:
    """返信が必要な投稿"""
    workspace: str
    channel_name: str
    channel_id: str
    sender: str
    message: str
    timestamp: str
    slack_url: str
    category: str  # "mention", "thread_reply", "dm"
    thread_ts: Optional[str] = None


def get_my_user_id(client: WebClient) -> Optional[str]:
    """自分のユーザーIDを取得"""
    try:
        result = client.auth_test()
        return result.get("user_id")
    except SlackApiError as e:
        print(f"⚠️ auth.test エラー: {e.response['error']}")
        return None


def get_user_name(client: WebClient, user_id: str, user_cache: dict) -> str:
    """ユーザーIDから表示名を取得（キャッシュ付き）"""
    if user_id in user_cache:
        return user_cache[user_id]
    
    try:
        result = client.users_info(user=user_id)
        user = result["user"]
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


def format_timestamp_jst(ts: str) -> str:
    """Slackタイムスタンプを日本時間の日時文字列に変換"""
    dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
    dt_jst = dt + timedelta(hours=9)
    return dt_jst.strftime("%Y-%m-%d %H:%M")


def generate_slack_url(slack_domain: str, channel_id: str, ts: str, thread_ts: Optional[str] = None) -> str:
    """SlackのメッセージURLを生成"""
    ts_for_url = ts.replace(".", "")
    url = f"https://{slack_domain}.slack.com/archives/{channel_id}/p{ts_for_url}"
    if thread_ts and thread_ts != ts:
        thread_ts_for_url = thread_ts.replace(".", "")
        url += f"?thread_ts={thread_ts}&cid={channel_id}"
    return url


def get_pending_mentions(
    client: WebClient,
    my_user_id: str,
    workspace_name: str,
    slack_domain: str,
    user_cache: dict,
    days_back: int = 7
) -> list[PendingReply]:
    """自分へのメンションを取得"""
    pending = []
    oldest_ts = str((datetime.now(timezone.utc) - timedelta(days=days_back)).timestamp())
    
    try:
        # チャンネル一覧を取得
        channels = []
        result = client.conversations_list(types="public_channel,private_channel", limit=1000)
        channels.extend(result.get("channels", []))
        
        for channel in channels:
            if channel.get("is_archived"):
                continue
            
            channel_id = channel["id"]
            channel_name = channel["name"]
            
            try:
                # チャンネルのメッセージを取得
                hist_result = client.conversations_history(
                    channel=channel_id,
                    oldest=oldest_ts,
                    limit=200
                )
                
                for msg in hist_result.get("messages", []):
                    text = msg.get("text", "")
                    user_id = msg.get("user")
                    
                    # 自分の投稿は除外
                    if user_id == my_user_id:
                        continue
                    
                    # 自分へのメンションをチェック
                    if f"<@{my_user_id}>" in text:
                        ts = msg.get("ts", "0")
                        thread_ts = msg.get("thread_ts")
                        
                        pending.append(PendingReply(
                            workspace=workspace_name,
                            channel_name=channel_name,
                            channel_id=channel_id,
                            sender=get_user_name(client, user_id, user_cache),
                            message=text[:500],  # 500文字まで
                            timestamp=format_timestamp_jst(ts),
                            slack_url=generate_slack_url(slack_domain, channel_id, ts, thread_ts),
                            category="mention",
                            thread_ts=thread_ts
                        ))
            
            except SlackApiError as e:
                if e.response.get("error") != "not_in_channel":
                    print(f"  ⚠️ {channel_name}: {e.response['error']}")
                continue
        
    except SlackApiError as e:
        print(f"⚠️ チャンネル一覧取得エラー: {e.response['error']}")
    
    return pending


def get_thread_replies_to_me(
    client: WebClient,
    my_user_id: str,
    workspace_name: str,
    slack_domain: str,
    user_cache: dict,
    days_back: int = 7
) -> list[PendingReply]:
    """自分のスレッドへの返信を取得"""
    pending = []
    oldest_ts = str((datetime.now(timezone.utc) - timedelta(days=days_back)).timestamp())
    
    try:
        channels = []
        result = client.conversations_list(types="public_channel,private_channel", limit=1000)
        channels.extend(result.get("channels", []))
        
        for channel in channels:
            if channel.get("is_archived"):
                continue
            
            channel_id = channel["id"]
            channel_name = channel["name"]
            
            try:
                hist_result = client.conversations_history(
                    channel=channel_id,
                    oldest=oldest_ts,
                    limit=200
                )
                
                for msg in hist_result.get("messages", []):
                    # 自分が投稿したスレッドで、返信があるもの
                    user_id = msg.get("user")
                    reply_count = msg.get("reply_count", 0)
                    
                    if user_id == my_user_id and reply_count > 0:
                        thread_ts = msg.get("ts")
                        latest_reply = msg.get("latest_reply", "0")
                        
                        # 最新の返信が自分以外からのものかチェック
                        try:
                            replies_result = client.conversations_replies(
                                channel=channel_id,
                                ts=thread_ts,
                                limit=10
                            )
                            
                            # 最新の返信を取得
                            replies = [r for r in replies_result.get("messages", []) if r.get("ts") != thread_ts]
                            if replies:
                                last_reply = replies[-1]
                                last_reply_user = last_reply.get("user")
                                
                                # 最後の返信が自分以外なら「返信が必要」
                                if last_reply_user != my_user_id:
                                    pending.append(PendingReply(
                                        workspace=workspace_name,
                                        channel_name=channel_name,
                                        channel_id=channel_id,
                                        sender=get_user_name(client, last_reply_user, user_cache),
                                        message=last_reply.get("text", "")[:500],
                                        timestamp=format_timestamp_jst(last_reply.get("ts", "0")),
                                        slack_url=generate_slack_url(slack_domain, channel_id, last_reply.get("ts", "0"), thread_ts),
                                        category="thread_reply",
                                        thread_ts=thread_ts
                                    ))
                        
                        except SlackApiError:
                            continue
            
            except SlackApiError as e:
                if e.response.get("error") != "not_in_channel":
                    print(f"  ⚠️ {channel_name}: {e.response['error']}")
                continue
    
    except SlackApiError as e:
        print(f"⚠️ チャンネル一覧取得エラー: {e.response['error']}")
    
    return pending


def get_dm_messages(
    client: WebClient,
    my_user_id: str,
    workspace_name: str,
    slack_domain: str,
    user_cache: dict,
    days_back: int = 7
) -> list[PendingReply]:
    """DMで受信したメッセージを取得"""
    pending = []
    oldest_ts = str((datetime.now(timezone.utc) - timedelta(days=days_back)).timestamp())
    
    try:
        # DM一覧を取得
        result = client.conversations_list(types="im", limit=200)
        ims = result.get("channels", [])
        
        for im in ims:
            channel_id = im["id"]
            other_user_id = im.get("user")
            
            if not other_user_id:
                continue
            
            try:
                hist_result = client.conversations_history(
                    channel=channel_id,
                    oldest=oldest_ts,
                    limit=50
                )
                
                messages = hist_result.get("messages", [])
                if not messages:
                    continue
                
                # 最新のメッセージが自分以外からのものかチェック
                last_msg = messages[0]  # 新しい順
                last_msg_user = last_msg.get("user")
                
                if last_msg_user and last_msg_user != my_user_id:
                    ts = last_msg.get("ts", "0")
                    pending.append(PendingReply(
                        workspace=workspace_name,
                        channel_name=f"DM: {get_user_name(client, other_user_id, user_cache)}",
                        channel_id=channel_id,
                        sender=get_user_name(client, last_msg_user, user_cache),
                        message=last_msg.get("text", "")[:500],
                        timestamp=format_timestamp_jst(ts),
                        slack_url=generate_slack_url(slack_domain, channel_id, ts),
                        category="dm"
                    ))
            
            except SlackApiError:
                continue
    
    except SlackApiError as e:
        print(f"⚠️ DM一覧取得エラー: {e.response['error']}")
    
    return pending


def process_workspace(
    workspace_name: str,
    workspace_config: dict,
    days_back: int = 7
) -> list[PendingReply]:
    """ワークスペースを処理して返信が必要な投稿を取得"""
    token_env = workspace_config["token_env"]
    display_name = workspace_config["display_name"]
    slack_domain = workspace_config.get("slack_domain", "")
    token = os.getenv(token_env)
    
    if not token:
        print(f"⏭️  {display_name}: {token_env} が設定されていないためスキップ")
        return []
    
    print(f"\n{'='*60}")
    print(f"🔍 {display_name} をスキャン中...")
    print(f"{'='*60}")
    
    client = WebClient(token=token)
    user_cache = {}
    
    # 自分のユーザーIDを取得
    my_user_id = get_my_user_id(client)
    if not my_user_id:
        print("❌ ユーザーID取得に失敗")
        return []
    
    print(f"👤 自分のユーザーID: {my_user_id}")
    
    all_pending = []
    
    # 1. メンションを取得
    print("\n📬 メンションをチェック中...")
    mentions = get_pending_mentions(client, my_user_id, workspace_name, slack_domain, user_cache, days_back)
    print(f"   → {len(mentions)} 件のメンション")
    all_pending.extend(mentions)
    
    # 2. スレッド返信を取得
    print("\n💬 スレッド返信をチェック中...")
    thread_replies = get_thread_replies_to_me(client, my_user_id, workspace_name, slack_domain, user_cache, days_back)
    print(f"   → {len(thread_replies)} 件のスレッド返信")
    all_pending.extend(thread_replies)
    
    # 3. DMを取得
    print("\n📩 DMをチェック中...")
    dms = get_dm_messages(client, my_user_id, workspace_name, slack_domain, user_cache, days_back)
    print(f"   → {len(dms)} 件のDM")
    all_pending.extend(dms)
    
    return all_pending


def format_results(pending_list: list[PendingReply]) -> str:
    """結果を見やすい形式で出力"""
    if not pending_list:
        return "✅ 返信が必要な投稿はありません"
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"📋 返信が必要な投稿: {len(pending_list)} 件")
    output.append(f"{'='*60}\n")
    
    # カテゴリ別にグループ化
    by_category = {"mention": [], "thread_reply": [], "dm": []}
    for p in pending_list:
        by_category[p.category].append(p)
    
    category_labels = {
        "mention": "📬 メンション",
        "thread_reply": "💬 スレッド返信",
        "dm": "📩 DM"
    }
    
    for category, items in by_category.items():
        if not items:
            continue
        
        output.append(f"\n{category_labels[category]} ({len(items)} 件)")
        output.append("-" * 50)
        
        for i, p in enumerate(items, 1):
            output.append(f"\n{i}. [{p.workspace}] #{p.channel_name}")
            output.append(f"   📅 {p.timestamp}")
            output.append(f"   👤 {p.sender}")
            output.append(f"   💬 {p.message[:200]}{'...' if len(p.message) > 200 else ''}")
            output.append(f"   🔗 {p.slack_url}")
    
    return "\n".join(output)


def save_results_json(pending_list: list[PendingReply], output_path: Path):
    """結果をJSONファイルに保存"""
    data = [
        {
            "workspace": p.workspace,
            "channel_name": p.channel_name,
            "channel_id": p.channel_id,
            "sender": p.sender,
            "message": p.message,
            "timestamp": p.timestamp,
            "slack_url": p.slack_url,
            "category": p.category,
        }
        for p in pending_list
    ]
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 結果を保存しました: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Slackで返信が必要な投稿を取得"
    )
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        choices=list(WORKSPACES.keys()),
        help="特定のワークスペースのみ処理"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=7,
        help="過去何日間をスキャンするか（デフォルト: 7）"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="結果をJSONファイルに保存"
    )
    
    args = parser.parse_args()
    
    print("🚀 返信が必要な投稿を検索中...")
    print(f"📅 対象期間: 過去{args.days}日間")
    
    # 処理対象ワークスペースを決定
    if args.workspace:
        workspaces_to_scan = {args.workspace: WORKSPACES[args.workspace]}
    else:
        workspaces_to_scan = WORKSPACES
    
    all_pending = []
    
    for ws_name, ws_config in workspaces_to_scan.items():
        pending = process_workspace(ws_name, ws_config, args.days)
        all_pending.extend(pending)
    
    # 結果を表示
    print(format_results(all_pending))
    
    # JSONに保存（オプション）
    if args.output:
        save_results_json(all_pending, Path(args.output))
    
    # 終了コード
    if all_pending:
        print(f"\n⚠️ {len(all_pending)} 件の返信が必要な投稿があります")
    else:
        print("\n✅ 返信が必要な投稿はありません")


if __name__ == "__main__":
    main()

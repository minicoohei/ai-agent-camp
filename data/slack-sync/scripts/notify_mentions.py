#!/usr/bin/env python3
"""
Slackメンション検出 & LINE通知スクリプト

GitHub Actionsでslack-sync/data/**/*.mdへのpush時に実行され、
自分宛のメンションを検出してLINEに通知します。

使い方:
  python notify_mentions.py
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class MentionInfo:
    """検出されたメンション情報"""
    channel_name: str
    workspace: str
    sender: str
    message: str
    slack_url: str
    time: str


# メンション検出対象のパターン（大文字小文字無視）
# 環境変数 MENTION_NAMES から取得するか、デフォルト値を使用
_mention_names = os.environ.get("MENTION_NAMES", "Your Name,your-username").split(",")
MENTION_PATTERNS = [rf"@{name.strip()}" for name in _mention_names]


def get_git_diff() -> str:
    """前回コミットからの差分を取得"""
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1", "--", "slack-sync/data/**/*.md"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"⚠️ git diff 実行エラー: {e}")
        # 初回コミットの場合など
        return ""


def parse_diff_for_mentions(diff_output: str) -> list[MentionInfo]:
    """git diffの出力からメンションを検出"""
    mentions = []
    
    # 追加された行のみを対象（+で始まる行）
    current_file = ""
    current_workspace = ""
    current_channel = ""
    current_header = ""  # ### HH:MM - ユーザー名 [[Slack]](URL) 形式
    current_slack_url = ""
    current_sender = ""
    current_time = ""
    message_lines = []
    
    for line in diff_output.split("\n"):
        # ファイル名を取得
        if line.startswith("+++ b/"):
            current_file = line[6:]
            # slack-sync/data/{workspace}/{channel}.md からワークスペースとチャンネル名を抽出
            match = re.match(r"slack-sync/data/([^/]+)/(.+)\.md$", current_file)
            if match:
                current_workspace = match.group(1)
                current_channel = match.group(2)
            continue
        
        # 追加された行のみ処理
        if not line.startswith("+") or line.startswith("+++"):
            continue
        
        added_line = line[1:]  # 先頭の+を除去
        
        # ヘッダー行の検出: ### HH:MM - ユーザー名 [[Slack]](URL)
        header_match = re.match(
            r"^### (\d{2}:\d{2}) - (.+?) \[\[Slack\]\]\((https://[^)]+)\)$",
            added_line
        )
        if header_match:
            current_time = header_match.group(1)
            current_sender = header_match.group(2)
            current_slack_url = header_match.group(3)
            message_lines = []
            continue
        
        # メッセージ行（ヘッダーの後に続く行）
        if current_slack_url and added_line.strip():
            message_lines.append(added_line)
            
            # メンションパターンをチェック
            for pattern in MENTION_PATTERNS:
                if re.search(pattern, added_line, re.IGNORECASE):
                    mentions.append(MentionInfo(
                        channel_name=current_channel,
                        workspace=current_workspace,
                        sender=current_sender,
                        message="\n".join(message_lines),
                        slack_url=current_slack_url,
                        time=current_time
                    ))
                    # 同じメッセージで複数パターンにマッチしても1回だけ通知
                    break
    
    return mentions


def send_line_notification(mentions: list[MentionInfo]) -> bool:
    """LINE Messaging APIで通知を送信"""
    access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    
    if not access_token or not user_id:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN または LINE_USER_ID が設定されていません")
        return False
    
    # メッセージを構築
    messages = []
    for mention in mentions[:5]:  # 最大5件まで（LINE APIの制限）
        # メッセージテキストを短縮（最大200文字）
        msg_preview = mention.message[:200]
        if len(mention.message) > 200:
            msg_preview += "..."
        
        text = (
            f"【Slackメンション】\n\n"
            f"#{mention.channel_name} ({mention.workspace})\n"
            f"投稿者: {mention.sender}\n"
            f"時刻: {mention.time}\n\n"
            f"「{msg_preview}」\n\n"
            f"{mention.slack_url}"
        )
        messages.append({"type": "text", "text": text})
    
    if not messages:
        return True
    
    # LINE API リクエスト
    payload = json.dumps({
        "to": user_id,
        "messages": messages
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
                print(f"✅ LINE通知を送信しました（{len(messages)}件）")
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


def main():
    print("🔍 メンション検出を開始...")
    
    # git diffを取得
    diff_output = get_git_diff()
    if not diff_output:
        print("📭 差分がありません")
        return
    
    # メンションを検出
    mentions = parse_diff_for_mentions(diff_output)
    
    if not mentions:
        print("📭 メンションは検出されませんでした")
        return
    
    print(f"📬 {len(mentions)} 件のメンションを検出:")
    for m in mentions:
        print(f"  - #{m.channel_name} ({m.workspace}): {m.sender}")
    
    # LINE通知を送信
    if not send_line_notification(mentions):
        sys.exit(1)


if __name__ == "__main__":
    main()

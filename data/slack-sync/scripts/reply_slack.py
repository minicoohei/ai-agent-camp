#!/usr/bin/env python3
"""
Slack Reply Script
スレッドに返信を送信するスクリプト

使用方法:
    python reply_slack.py --channel C0A3WAFQG7M --thread_ts 1767780615.901749 --message "返信内容"

    # ドライラン（実際には送信しない）
    python reply_slack.py --channel C0A3WAFQG7M --thread_ts 1767780615.901749 --message "返信内容" --dry-run

環境変数:
    SLACK_USER_TOKEN: xoxp-で始まるSlack User Token（chat:writeスコープが必要）
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def extract_channel_and_ts_from_url(slack_url: str) -> tuple[str, str]:
    """
    SlackのURLからチャンネルIDとthread_tsを抽出する

    例: https://workspace.slack.com/archives/C0A3WAFQG7M/p1767780615901749
    → channel_id: C0A3WAFQG7M, thread_ts: 1767780615.901749
    """
    # URLパターン: /archives/{channel_id}/p{timestamp}
    pattern = r'/archives/([A-Z0-9]+)/p(\d+)'
    match = re.search(pattern, slack_url)

    if not match:
        raise ValueError(f"Invalid Slack URL format: {slack_url}")

    channel_id = match.group(1)
    # タイムスタンプを変換 (p1767780615901749 → 1767780615.901749)
    raw_ts = match.group(2)
    thread_ts = f"{raw_ts[:-6]}.{raw_ts[-6:]}"

    return channel_id, thread_ts


def send_reply(token: str, channel: str, thread_ts: str, message: str, dry_run: bool = False) -> dict:
    """
    Slackのスレッドに返信を送信する

    Args:
        token: Slack User Token (xoxp-...)
        channel: チャンネルID (例: C0A3WAFQG7M)
        thread_ts: 親メッセージのタイムスタンプ (例: 1767780615.901749)
        message: 送信するメッセージ
        dry_run: Trueの場合、実際には送信しない

    Returns:
        APIレスポンス（dry_runの場合はダミーレスポンス）
    """
    if dry_run:
        print("\n" + "=" * 50)
        print("DRY RUN - 以下の内容で送信されます:")
        print("=" * 50)
        print(f"Channel: {channel}")
        print(f"Thread TS: {thread_ts}")
        print(f"Message:\n{message}")
        print("=" * 50)
        return {"ok": True, "dry_run": True}

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "thread_ts": thread_ts,
        "text": message
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if not result.get("ok"):
        error = result.get("error", "Unknown error")
        print(f"Error sending message: {error}", file=sys.stderr)

        if error == "missing_scope":
            print("\nRequired scope: chat:write", file=sys.stderr)
            print("Please add this scope to your Slack App and regenerate the token.", file=sys.stderr)
        elif error == "channel_not_found":
            print(f"\nChannel {channel} not found or not accessible.", file=sys.stderr)
        elif error == "thread_not_found":
            print(f"\nThread {thread_ts} not found in channel {channel}.", file=sys.stderr)

    return result


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Slackのスレッドに返信を送信する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # チャンネルIDとthread_tsを直接指定
  python reply_slack.py -c C0A3WAFQG7M -t 1767780615.901749 -m "返信です"

  # Slack URLから自動抽出
  python reply_slack.py --url "https://xxx.slack.com/archives/C0A3WAFQG7M/p1767780615901749" -m "返信です"

  # ドライラン（送信せずに確認のみ）
  python reply_slack.py --url "..." -m "返信です" --dry-run
        """
    )

    parser.add_argument("-c", "--channel", help="チャンネルID (例: C0A3WAFQG7M)")
    parser.add_argument("-t", "--thread_ts", help="スレッドのタイムスタンプ (例: 1767780615.901749)")
    parser.add_argument("--url", help="SlackのメッセージURL（--channelと--thread_tsの代わりに使用可能）")
    parser.add_argument("-m", "--message", required=True, help="送信するメッセージ")
    parser.add_argument("--dry-run", action="store_true", help="実際には送信せず、内容を確認するだけ")
    parser.add_argument("--token", help="Slack User Token（省略時は環境変数SLACK_USER_TOKENを使用）")

    args = parser.parse_args()

    # URLからチャンネルとthread_tsを抽出
    if args.url:
        try:
            channel, thread_ts = extract_channel_and_ts_from_url(args.url)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.channel and args.thread_ts:
        channel = args.channel
        thread_ts = args.thread_ts
    else:
        print("Error: --url または --channel と --thread_ts の両方を指定してください", file=sys.stderr)
        sys.exit(1)

    # トークンの取得
    token = args.token or os.getenv("SLACK_USER_TOKEN")
    if not token:
        print("Error: SLACK_USER_TOKEN環境変数またはを設定するか、--tokenオプションを使用してください", file=sys.stderr)
        sys.exit(1)

    # 送信
    result = send_reply(token, channel, thread_ts, args.message, dry_run=args.dry_run)

    if result.get("ok"):
        if args.dry_run:
            print("\nDry run completed. Use without --dry-run to actually send.")
        else:
            print("Message sent successfully!")
            print(f"Timestamp: {result.get('ts')}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

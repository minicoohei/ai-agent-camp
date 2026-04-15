#!/usr/bin/env python3
"""ニュース取得スクリプト — RSS フィードからニュースを収集

Lesson 11-3 の演習テンプレート。
受講者はこのスクリプトを拡張してメール/Slack配信を追加する。
"""
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

# RSS フィード URL（例: Hacker News, TechCrunch）
RSS_FEEDS = [
    {"name": "Hacker News", "url": "https://hnrss.org/newest?count=5"},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
]


def fetch_rss(url, max_items=5):
    """RSS フィードからニュース取得"""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    items = []
    for item in root.iter("item"):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        items.append({"title": title, "link": link, "pubDate": pub_date})
        if len(items) >= max_items:
            break
    return items


def send_email(news_data):
    """ニュースダイジェストをメール送信"""
    import smtplib
    from email.mime.text import MIMEText

    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    to_email = os.environ.get("NOTIFY_EMAIL", smtp_user)

    if not smtp_user or not smtp_pass:
        print("[SKIP] SMTP 認証情報が未設定のため、メール送信をスキップ")
        return

    # メール本文作成
    body_lines = [f"# ニュースダイジェスト ({news_data['generated_at'][:10]})\n"]
    for feed in news_data["feeds"]:
        body_lines.append(f"\n## {feed['source']}")
        for item in feed["items"]:
            body_lines.append(f"- [{item['title']}]({item['link']})")

    body = "\n".join(body_lines)
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"ニュースダイジェスト {news_data['generated_at'][:10]}"
    msg["From"] = smtp_user
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
    print(f"メール送信完了: {to_email}")


def send_slack(news_data):
    """Slack Webhook でニュース通知"""
    webhook_url = os.environ.get("SLACK_WEBHOOK", "")
    if not webhook_url:
        print("[SKIP] SLACK_WEBHOOK が未設定のため、Slack 通知をスキップ")
        return

    # Slack メッセージ構築
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": "ニュースダイジェスト"}}
    ]
    for feed in news_data["feeds"]:
        items_text = "\n".join(
            f"• <{i['link']}|{i['title']}>" for i in feed["items"]
        )
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{feed['source']}*\n{items_text}"},
            }
        )

    payload = {"blocks": blocks}
    resp = requests.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()
    print("Slack 通知送信完了")


def main():
    all_news = []
    for feed in RSS_FEEDS:
        try:
            items = fetch_rss(feed["url"])
            all_news.append({"source": feed["name"], "items": items})
        except Exception as e:
            print(f"[WARN] {feed['name']}: {e}")

    # JSON 出力
    output = {
        "generated_at": datetime.utcnow().isoformat(),
        "feeds": all_news,
    }
    os.makedirs("output", exist_ok=True)
    with open("output/news_digest.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"取得完了: {sum(len(f['items']) for f in all_news)} 件のニュース")
    return output


if __name__ == "__main__":
    main()

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
duration: "約25分"
prerequisites: ["start-11-2"]
level: "intermediate"
tags: ["github-actions", "news", "email", "slack", "webhook", "cron"]
---

# 🎓 Lesson 11-3: ニュース取得→メール/Slack配信ワークフロー

## 📍 このセッションでやること

**Lesson 11-3: ニュース取得→メール/Slack配信** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GitHub Actions でニュースを自動取得し、メールと Slack に配信するワークフローを構築する |
| 所要時間 | 約25分 |
| 使うスキル | GitHub Actions, Python (requests), Slack Webhook, smtplib |
| 前提条件 | Lesson 11-2 完了（Secrets 設定の理解） |

**このセッションの流れ:**
1. ニュース取得スクリプトの作成
2. メール送信処理の実装
3. Slack Webhook 通知の設定
4. GitHub Actions ワークフロー作成
5. Secrets 設定と動作テスト

セッション終了時には、定期的にニュースを収集してメールと Slack に自動配信するパイプラインが完成しています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## 🎯 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → Lesson 11-2 完了確認。`.github/workflows/` ディレクトリの存在確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: ニュース取得スクリプトの作成

```json
{
  "title": "🚀 Step 1: ニュース取得スクリプト",
  "questions": [{
    "id": "step_action",
    "prompt": "RSS フィードまたは News API からニュースを取得する Python スクリプトを作成します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "RSS/API の仕組みを確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`scripts/fetch_news.py` を作成:

```python
#!/usr/bin/env python3
"""ニュース取得スクリプト — RSS フィードからニュースを収集"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

# RSS フィード URL（例: はてなテクノロジー）
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
        "feeds": all_news
    }
    with open("output/news_digest.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"取得完了: {sum(len(f['items']) for f in all_news)} 件のニュース")
    return output

if __name__ == "__main__":
    main()
```

```bash
mkdir -p output && python scripts/fetch_news.py
```

**期待される結果**: `output/news_digest.json` にニュースデータが保存される。

---

## 🚀 Step 2: メール送信処理の実装

```json
{
  "title": "🚀 Step 2: メール送信",
  "questions": [{
    "id": "step_action",
    "prompt": "取得したニュースをメールで送信する処理を追加します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "smtplib の使い方を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`scripts/fetch_news.py` に送信関数を追加:

```python
import smtplib
from email.mime.text import MIMEText
import os

def send_email(news_data):
    """ニュースダイジェストをメール送信"""
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
```

**ポイント**: Gmail の場合、アプリパスワードが必要。Secrets に `SMTP_USER` と `SMTP_PASS` を設定する。

**期待される結果**: ニュースダイジェストがメールで送信される。

---

## 🚀 Step 3: Slack Webhook 通知の設定

```json
{
  "title": "🚀 Step 3: Slack 通知",
  "questions": [{
    "id": "step_action",
    "prompt": "Slack Incoming Webhook でニュース通知を送信します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "Slack Webhook の作成方法を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

```python
def send_slack(news_data):
    """Slack Webhook でニュース通知"""
    webhook_url = os.environ.get("SLACK_WEBHOOK", "")
    if not webhook_url:
        print("[SKIP] SLACK_WEBHOOK が未設定のため、Slack 通知をスキップ")
        return

    # Slack メッセージ構築
    blocks = [{"type": "header", "text": {"type": "plain_text", "text": "📰 ニュースダイジェスト"}}]
    for feed in news_data["feeds"]:
        items_text = "\n".join(f"• <{i['link']}|{i['title']}>" for i in feed["items"])
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{feed['source']}*\n{items_text}"}
        })

    payload = {"blocks": blocks}
    resp = requests.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()
    print("Slack 通知送信完了")
```

**Webhook URL の作成手順:**
1. Slack App の「Incoming Webhooks」を有効化
2. 「Add New Webhook to Workspace」で通知先チャンネルを選択
3. 生成された URL を GitHub Secrets `SLACK_WEBHOOK` に設定

**期待される結果**: 指定チャンネルにニュースダイジェストが投稿される。

---

## 🚀 Step 4: GitHub Actions ワークフロー作成

```json
{
  "title": "🚀 Step 4: ワークフロー作成",
  "questions": [{
    "id": "step_action",
    "prompt": "cron スケジュールでニュースを取得・配信するワークフローを作成します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "cron 式の書き方を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`.github/workflows/news-digest.yml` を作成:

```yaml
name: News Digest
on:
  schedule:
    - cron: '0 0 * * *'  # UTC 0:00 = JST 9:00
  workflow_dispatch:
    inputs:
      skip_email:
        description: 'メール送信をスキップ'
        type: boolean
        default: false

jobs:
  news-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests

      - name: Fetch news
        run: |
          mkdir -p output
          python scripts/fetch_news.py

      - name: Send email notification
        if: ${{ !inputs.skip_email }}
        env:
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASS: ${{ secrets.SMTP_PASS }}
          NOTIFY_EMAIL: ${{ secrets.NOTIFY_EMAIL }}
        run: python -c "from scripts.fetch_news import *; send_email(main())"

      - name: Send Slack notification
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        run: python -c "from scripts.fetch_news import *; send_slack(main())"

      - uses: actions/upload-artifact@v4
        with:
          name: news-digest-${{ github.run_number }}
          path: output/news_digest.json
          retention-days: 7
```

**期待される結果**: ワークフローファイルが作成され、`gh workflow list` に表示される。

---

## 🚀 Step 5: Secrets 設定と動作テスト

```json
{
  "title": "🚀 Step 5: テスト実行",
  "questions": [{
    "id": "step_action",
    "prompt": "Secrets を設定し、ワークフローを手動実行してテストします。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "Secrets の設定方法を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

1. **Secrets 設定**（GitHub Web UI: Settings → Secrets and variables → Actions）:
   - `SLACK_WEBHOOK`: Slack Incoming Webhook URL
   - `SMTP_USER`: Gmail アドレス（メール送信する場合）
   - `SMTP_PASS`: Gmail アプリパスワード（メール送信する場合）
   - `NOTIFY_EMAIL`: 送信先メールアドレス

2. **手動実行テスト**:
```bash
# ワークフローを手動実行
gh workflow run "News Digest"

# 実行結果を確認
gh run list --limit 3
```

3. **ログ確認**:
```bash
gh run view <run_id> --log
```

**期待される結果**: ワークフローが正常に完了し、Slack 通知（設定済みの場合はメールも）が届く。

---

## ⚠️ よくあるトラブルと解決方法

```json
{
  "title": "⚠️ トラブルシューティング",
  "questions": [{
    "id": "trouble",
    "prompt": "問題が発生しましたか？",
    "options": [
      {"id": "trouble_1", "label": "RSS フィードの取得に失敗"},
      {"id": "trouble_2", "label": "Slack Webhook がエラー"},
      {"id": "trouble_3", "label": "メール送信に失敗"},
      {"id": "trouble_4", "label": "cron スケジュールが動かない"}
    ]
  }]
}
```

### トラブル1: 「RSS フィードの取得に失敗」
**原因**: フィード URL が変更・廃止されている、またはタイムアウト。
**解決プロンプト**:
```text
RSS_FEEDS の URL をブラウザで開いて XML が返ることを確認してください。タイムアウトの場合は timeout 値を 60 に増やしてください。
```

### トラブル2: 「Slack Webhook がエラー」
**原因**: Webhook URL が無効、または Secret が正しく設定されていない。
**解決プロンプト**:
```text
curl -X POST -H "Content-Type: application/json" -d '{"text":"テスト"}' $SLACK_WEBHOOK でローカルから直接テストしてください。404 の場合は Webhook を再作成してください。
```

### トラブル3: 「メール送信に失敗」
**原因**: Gmail のアプリパスワードが未設定、または2段階認証が無効。
**解決プロンプト**:
```text
Gmail のアプリパスワードを生成してください（Google アカウント → セキュリティ → アプリパスワード）。2段階認証が有効になっている必要があります。
```

### トラブル4: 「cron スケジュールが動かない」
**原因**: GitHub Actions の cron はデフォルトブランチでのみ動作。また、リポジトリに60日以上アクティビティがないと無効化される。
**解決プロンプト**:
```text
ワークフローファイルが main ブランチにマージされているか確認してください。まず workflow_dispatch で手動実行が成功することを確認してください。
```

---

## ✅ チェックポイント

- [ ] `scripts/fetch_news.py` でニュースが取得できる
- [ ] `output/news_digest.json` にデータが保存される
- [ ] Slack Webhook で通知が送信できる（設定済みの場合）
- [ ] `.github/workflows/news-digest.yml` が作成されている
- [ ] `gh workflow run` で手動実行が成功する

---

## 📋 成果物プレビュー

**作成されるファイル:**
```text
scripts/
└── fetch_news.py          # ニュース取得・配信スクリプト

.github/workflows/
└── news-digest.yml        # 定期配信ワークフロー

output/
└── news_digest.json       # ニュースデータ（実行時生成）
```

---

## ➡️ 次のステップ

```json
{
  "title": "➡️ 次のステップ",
  "questions": [{
    "id": "next_step",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_auto", "label": "Lesson 11-4（AI CLI を GitHub Actions で呼ぶ）に進む → /start-11-4"},
      {"id": "review_module", "label": "このレッスンの成果物を確認したい"},
      {"id": "finish", "label": "今日はここまで"}
    ]
  }]
}
```

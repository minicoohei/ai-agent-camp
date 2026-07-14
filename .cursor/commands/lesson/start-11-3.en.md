---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
duration: "~25 min"
prerequisites: ["start-11-2"]
level: "intermediate"
tags: ["github-actions", "news", "email", "slack", "webhook", "cron"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 11-3: News Fetching → Email/Slack Distribution Workflow

## 📍 What You'll Do

**Lesson 11-3: News Fetching → Email/Slack Distribution**!

| Item | Details |
|------|------|
| Goal | Build a GitHub Actions workflow that automatically fetches news and distributes it via email and Slack |
| Duration | ~25 min |
| Skills used | GitHub Actions, Python (requests), Slack Webhook, smtplib |
| Prerequisites | Lesson 11-2 completed (understanding of Secrets configuration) |

**Session flow:**
1. Create the news fetching script
2. Implement email sending
3. Set up Slack Webhook notifications
4. Create the GitHub Actions workflow
5. Configure Secrets and test

By the end of this session, you'll have a complete pipeline that periodically collects news and automatically distributes it to email and Slack.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume.

---

## 🎯 Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Verify Lesson 11-2 completion. Check that the `.github/workflows/` directory exists)
(different_lesson → Display module list)

---

## 🚀 Step 1: Create the News Fetching Script

```json
{
  "title": "🚀 Step 1: News Fetching Script",
  "questions": [{
    "id": "step_action",
    "prompt": "Create a Python script that fetches news from RSS feeds or a News API.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review how RSS/APIs work"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Create `tools/fetch_news.py`:

```python
#!/usr/bin/env python3
"""News fetching script — collects news from RSS feeds"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

# RSS feed URLs (e.g., Hacker News, TechCrunch)
RSS_FEEDS = [
    {"name": "Hacker News", "url": "https://hnrss.org/newest?count=5"},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
]

def fetch_rss(url, max_items=5):
    """Fetch news from an RSS feed"""
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
    
    # JSON output
    output = {
        "generated_at": datetime.utcnow().isoformat(),
        "feeds": all_news
    }
    with open("output/news_digest.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Fetch complete: {sum(len(f['items']) for f in all_news)} news items")
    return output

if __name__ == "__main__":
    main()
```

```bash
mkdir -p output && python tools/fetch_news.py
```

**Expected result:** News data is saved to `output/news_digest.json`.

---

## 🚀 Step 2: Implement Email Sending

```json
{
  "title": "🚀 Step 2: Email Sending",
  "questions": [{
    "id": "step_action",
    "prompt": "Add email sending functionality for the fetched news.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review how smtplib works"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Add a sending function to `tools/fetch_news.py`:

```python
import smtplib
from email.mime.text import MIMEText
import os

def send_email(news_data):
    """Send a news digest email"""
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    to_email = os.environ.get("NOTIFY_EMAIL", smtp_user)
    
    if not smtp_user or not smtp_pass:
        print("[SKIP] SMTP credentials not configured, skipping email")
        return

    # Build email body
    body_lines = [f"# News Digest ({news_data['generated_at'][:10]})\n"]
    for feed in news_data["feeds"]:
        body_lines.append(f"\n## {feed['source']}")
        for item in feed["items"]:
            body_lines.append(f"- [{item['title']}]({item['link']})")
    
    body = "\n".join(body_lines)
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"News Digest {news_data['generated_at'][:10]}"
    msg["From"] = smtp_user
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
    print(f"Email sent: {to_email}")
```

**Note**: For Gmail, an app password is required. Set `SMTP_USER` and `SMTP_PASS` in Secrets.

**Expected result:** The news digest is sent by email.

---

## 🚀 Step 3: Set Up Slack Webhook Notifications

```json
{
  "title": "🚀 Step 3: Slack Notifications",
  "questions": [{
    "id": "step_action",
    "prompt": "Send news notifications via a Slack Incoming Webhook.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review how to create a Slack Webhook"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

```python
def send_slack(news_data):
    """Send news notification via Slack Webhook"""
    webhook_url = os.environ.get("SLACK_WEBHOOK", "")
    if not webhook_url:
        print("[SKIP] SLACK_WEBHOOK not configured, skipping Slack notification")
        return

    # Build Slack message
    blocks = [{"type": "header", "text": {"type": "plain_text", "text": "📰 News Digest"}}]
    for feed in news_data["feeds"]:
        items_text = "\n".join(f"• <{i['link']}|{i['title']}>" for i in feed["items"])
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{feed['source']}*\n{items_text}"}
        })

    payload = {"blocks": blocks}
    resp = requests.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()
    print("Slack notification sent")
```

**Steps to create a Webhook URL:**
1. Enable "Incoming Webhooks" in your Slack App
2. Click "Add New Webhook to Workspace" and select the target channel
3. Set the generated URL as the GitHub Secret `SLACK_WEBHOOK`

**Expected result:** The news digest is posted to the specified channel.

---

## 🚀 Step 4: Create the GitHub Actions Workflow

```json
{
  "title": "🚀 Step 4: Create the Workflow",
  "questions": [{
    "id": "step_action",
    "prompt": "Create a workflow that fetches and distributes news on a cron schedule.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review cron expression syntax"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Create `.github/workflows/news-digest.yml`:

```yaml
name: News Digest
on:
  schedule:
    - cron: '0 0 * * *'  # UTC 0:00 = JST 9:00
  workflow_dispatch:
    inputs:
      skip_email:
        description: 'Skip email sending'
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
        run: uv add requests

      - name: Fetch news
        run: |
          mkdir -p output
          python tools/fetch_news.py

      - name: Send email notification
        if: ${{ !inputs.skip_email }}
        env:
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASS: ${{ secrets.SMTP_PASS }}
          NOTIFY_EMAIL: ${{ secrets.NOTIFY_EMAIL }}
        run: python -c "from tools.fetch_news import *; send_email(main())"

      - name: Send Slack notification
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        run: python -c "from tools.fetch_news import *; send_slack(main())"

      - uses: actions/upload-artifact@v4
        with:
          name: news-digest-${{ github.run_number }}
          path: output/news_digest.json
          retention-days: 7
```

**Expected result:** The workflow file is created and appears in `gh workflow list`.

---

## 🚀 Step 5: Configure Secrets and Test

```json
{
  "title": "🚀 Step 5: Test Run",
  "questions": [{
    "id": "step_action",
    "prompt": "Set up Secrets and manually run the workflow to test.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review how to configure Secrets"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

1. **Configure Secrets** (GitHub Web UI: Settings → Secrets and variables → Actions):
   - `SLACK_WEBHOOK`: Slack Incoming Webhook URL
   - `SMTP_USER`: Gmail address (if sending email)
   - `SMTP_PASS`: Gmail app password (if sending email)
   - `NOTIFY_EMAIL`: Recipient email address

2. **Manual test run:**
```bash
# Manually trigger the workflow
gh workflow run "News Digest"

# Check execution results
gh run list --limit 3
```

3. **Check logs:**
```bash
gh run view <run_id> --log
```

**Expected result:** The workflow completes successfully, and Slack notifications (and email if configured) are received.

---

## ⚠️ Common Issues and Solutions

```json
{
  "title": "⚠️ Troubleshooting",
  "questions": [{
    "id": "trouble",
    "prompt": "Are you experiencing any issues?",
    "options": [
      {"id": "trouble_1", "label": "RSS feed fetch failed"},
      {"id": "trouble_2", "label": "Slack Webhook error"},
      {"id": "trouble_3", "label": "Email sending failed"},
      {"id": "trouble_4", "label": "Cron schedule not running"}
    ]
  }]
}
```

### Issue 1: "RSS feed fetch failed"
**Cause**: The feed URL has been changed or discontinued, or a timeout occurred.
**Solution prompt:**
```text
Open the RSS_FEEDS URLs in a browser and verify that XML is returned. If timing out, increase the timeout value to 60.
```

### Issue 2: "Slack Webhook error"
**Cause**: The Webhook URL is invalid, or the Secret is not configured correctly.
**Solution prompt:**
```text
Test directly from local with curl -X POST -H "Content-Type: application/json" -d '{"text":"test"}' $SLACK_WEBHOOK. If you get a 404, recreate the Webhook.
```

### Issue 3: "Email sending failed"
**Cause**: Gmail app password is not set, or 2-step verification is disabled.
**Solution prompt:**
```text
Generate a Gmail app password (Google Account → Security → App Passwords). 2-step verification must be enabled.
```

### Issue 4: "Cron schedule not running"
**Cause**: GitHub Actions cron only works on the default branch. Also, if there has been no repository activity for 60+ days, it gets disabled.
**Solution prompt:**
```text
Verify that the workflow file has been merged to the main branch. First confirm that manual execution via workflow_dispatch succeeds.
```

---

## ✅ Checkpoint

- [ ] `tools/fetch_news.py` can fetch news
- [ ] Data is saved to `output/news_digest.json`
- [ ] Slack Webhook notifications can be sent (if configured)
- [ ] `.github/workflows/news-digest.yml` has been created
- [ ] `gh workflow run` manual execution succeeds

---

## 📋 Deliverable Preview

**Files created:**
```text
tools/
└── fetch_news.py          # News fetching and distribution script

.github/workflows/
└── news-digest.yml        # Scheduled distribution workflow

output/
└── news_digest.json       # News data (generated at runtime)
```

---

## ➡️ Next Steps

```json
{
  "title": "➡️ Next Steps",
  "questions": [{
    "id": "next_step",
    "prompt": "What would you like to do next?",
    "options": [
      {"id": "next_auto", "label": "Move on to Lesson 11-4 (AI CLI in GitHub Actions) → /start-11-4"},
      {"id": "review_module", "label": "Review this lesson's deliverables"},
      {"id": "finish", "label": "Finish for today"}
    ]
  }]
}
```

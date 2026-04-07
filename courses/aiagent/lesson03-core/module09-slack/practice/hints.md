# Slack 検索・分析のヒント

## JSON データの読み込み

```python
import json
from datetime import datetime

with open("data/sample-conversations.json", encoding="utf-8") as f:
    messages = json.load(f)

# メッセージ数の確認
print(f"Total messages: {len(messages)}")
```

## キーワード検索

```python
def search_messages(messages, keyword):
    """キーワードでメッセージを検索"""
    results = []
    for msg in messages:
        if keyword.lower() in msg.get("text", "").lower():
            results.append(msg)
    return results

# 使用例
results = search_messages(messages, "デプロイ")
for r in results:
    print(f"[{r['channel']}] {r['user']}: {r['text'][:50]}")
```

## 複数キーワード検索

```python
def search_any(messages, keywords):
    """いずれかのキーワードに一致"""
    results = []
    for msg in messages:
        text = msg.get("text", "").lower()
        if any(kw.lower() in text for kw in keywords):
            results.append(msg)
    return results

# 「ミーティング」OR「MTG」OR「打ち合わせ」
results = search_any(messages, ["ミーティング", "MTG", "打ち合わせ"])
```

## タスク抽出パターン

```python
import re

TASK_PATTERNS = [
    r"お願い",
    r"してください",
    r"〜まで|までに",
    r"TODO|タスク",
    r"対応.*お願い",
    r"期限|締切",
    r"確認.*お願い",
]

def extract_tasks(messages):
    """タスクらしいメッセージを抽出"""
    tasks = []
    for msg in messages:
        text = msg.get("text", "")
        for pattern in TASK_PATTERNS:
            if re.search(pattern, text):
                tasks.append({
                    "message_id": msg["id"],
                    "user": msg["user"],
                    "text": text,
                    "channel": msg["channel"],
                    "timestamp": msg["timestamp"],
                    "matched_pattern": pattern,
                })
                break
    return tasks
```

## チャネル別集計

```python
from collections import Counter

channel_counts = Counter(msg["channel"] for msg in messages)
for channel, count in channel_counts.most_common():
    print(f"#{channel}: {count} messages")
```

## 日付別集計

```python
date_counts = Counter(
    msg["timestamp"][:10] for msg in messages
)
for date, count in sorted(date_counts.items()):
    print(f"{date}: {count} messages")
```

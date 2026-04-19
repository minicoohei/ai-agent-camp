# Module 6: Slack検索・タスク抽出 - 成果物（Final）

Slack検索、タスク抽出、メッセージ分析の例です。

## 学習目標
- Slack APIを使ってメッセージを検索できる
- 会話からタスクを自動抽出できる
- 検索結果を構造化してエクスポートできる

## 成果物一覧

| ファイル | 種類 | 内容 |
|---------|------|------|
| `search_results.json` | JSON | Slack検索結果 |
| `extracted_tasks.md` | Markdown | 抽出タスク一覧 |
| `channel_summary.json` | JSON | チャンネルサマリー |
| `slack_search.py` | スクリプト | 検索スクリプト |
| `task_extractor.py` | スクリプト | タスク抽出スクリプト |

## Slack API設定

### 必要なトークン
```
SLACK_BOT_TOKEN=xoxb-xxxx  # Bot Token
SLACK_USER_TOKEN=xoxp-xxxx # User Token（検索用）
```

### 必要なスコープ
```
Bot Token Scopes:
- channels:history
- channels:read
- chat:write
- users:read

User Token Scopes:
- search:read
```

## 検索クエリ構文

```
┌─────────────────────────────────────────────────────────┐
│  Slack検索クエリ構文                                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  基本検索                                               │
│    "キーワード"                                         │
│                                                         │
│  チャンネル指定                                         │
│    in:#channel-name                                    │
│                                                         │
│  ユーザー指定                                           │
│    from:@username                                      │
│    to:@username                                        │
│                                                         │
│  日付指定                                               │
│    after:2025-01-01                                    │
│    before:2025-02-01                                   │
│    on:2025-01-15                                       │
│                                                         │
│  ファイル検索                                           │
│    has:link                                            │
│    has:attachment                                      │
│    type:pdf                                            │
│                                                         │
│  リアクション検索                                        │
│    has::emoji:                                         │
│    has::white_check_mark:                             │
│                                                         │
│  複合例                                                 │
│    "プロジェクト" in:#general from:@john               │
│    after:2025-01-01                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 実行コマンド例

### メッセージ検索
```bash
uv run python tools/slack_search.py search \
  --query "プロジェクト進捗 in:#general after:2025-01-01" \
  --output examples/final/module-06-search/search_results.json
```

### タスク抽出
```bash
uv run python tools/extract_tasks.py \
  --channel "#project-alpha" \
  --date-range "2025-01-01:2025-01-31" \
  --output examples/final/module-06-search/extracted_tasks.md
```

### チャンネルサマリー
```bash
uv run python tools/slack_search.py summarize \
  --channel "#general" \
  --period "7d" \
  --output examples/final/module-06-search/channel_summary.json
```

## 検索スクリプト例

```python
#!/usr/bin/env python3
"""Slack検索スクリプト"""
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json

def search_messages(query, count=100):
    """メッセージを検索"""
    client = WebClient(token=os.environ["SLACK_USER_TOKEN"])
    
    try:
        response = client.search_messages(
            query=query,
            count=count,
            sort="timestamp",
            sort_dir="desc"
        )
        
        results = []
        for match in response["messages"]["matches"]:
            results.append({
                "channel": match["channel"]["name"],
                "user": match.get("username", "unknown"),
                "text": match["text"],
                "timestamp": match["ts"],
                "permalink": match["permalink"]
            })
        
        return {
            "query": query,
            "total": response["messages"]["total"],
            "results": results
        }
        
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")
        return None

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "プロジェクト"
    result = search_messages(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

## タスク抽出スクリプト例

```python
#!/usr/bin/env python3
"""タスク抽出スクリプト"""
import re
from datetime import datetime

# タスクパターン
TASK_PATTERNS = [
    r"TODO[:：]\s*(.+)",
    r"タスク[:：]\s*(.+)",
    r"【依頼】\s*(.+)",
    r"お願い[:：]\s*(.+)",
    r"確認お願い[:：]\s*(.+)",
    r"(.+)してください",
    r"(.+)をお願いします",
]

# 期限パターン
DEADLINE_PATTERNS = [
    r"(\d{1,2}/\d{1,2})まで",
    r"(\d{4}-\d{2}-\d{2})まで",
    r"(今週中|今月中|明日まで|本日中)",
]

def extract_tasks(messages):
    """メッセージからタスクを抽出"""
    tasks = []
    
    for msg in messages:
        text = msg["text"]
        
        for pattern in TASK_PATTERNS:
            matches = re.findall(pattern, text)
            for match in matches:
                task = {
                    "description": match.strip(),
                    "source_message": text[:100],
                    "channel": msg["channel"],
                    "assignee": extract_mention(text),
                    "deadline": extract_deadline(text),
                    "timestamp": msg["timestamp"],
                    "status": "pending"
                }
                tasks.append(task)
    
    return tasks

def extract_mention(text):
    """メンションを抽出"""
    mentions = re.findall(r"<@(\w+)>", text)
    return mentions[0] if mentions else None

def extract_deadline(text):
    """期限を抽出"""
    for pattern in DEADLINE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None

def format_as_markdown(tasks):
    """タスクをMarkdown形式で出力"""
    output = "# 抽出タスク一覧\n\n"
    output += f"抽出日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    output += "| # | タスク | 担当 | 期限 | ステータス |\n"
    output += "|---|--------|------|------|------------|\n"
    
    for i, task in enumerate(tasks, 1):
        output += f"| {i} | {task['description'][:50]} | "
        output += f"{task['assignee'] or '-'} | "
        output += f"{task['deadline'] or '-'} | "
        output += f"{task['status']} |\n"
    
    return output
```

## 検索結果JSON例

```json
{
  "query": "プロジェクト進捗 in:#general after:2025-01-01",
  "total": 42,
  "results": [
    {
      "channel": "general",
      "user": "tanaka",
      "text": "プロジェクトAの進捗報告です。現在80%完了しています。",
      "timestamp": "1706745600.000100",
      "permalink": "https://workspace.slack.com/archives/C01234/p1706745600000100"
    },
    {
      "channel": "general",
      "user": "suzuki",
      "text": "TODO: @tanaka 明日までにレビューお願いします",
      "timestamp": "1706745500.000200",
      "permalink": "https://workspace.slack.com/archives/C01234/p1706745500000200"
    }
  ]
}
```

## 抽出タスクMarkdown例

```markdown
# 抽出タスク一覧

抽出日時: 2025-02-03 12:00

| # | タスク | 担当 | 期限 | ステータス |
|---|--------|------|------|------------|
| 1 | レビューお願いします | tanaka | 明日まで | pending |
| 2 | 資料を作成 | suzuki | 1/31 | pending |
| 3 | MTG日程調整 | - | 今週中 | pending |
```

## チェックリスト

- [ ] Slack APIトークンが設定されている
- [ ] メッセージ検索ができる
- [ ] 日付やチャンネルでフィルタできる
- [ ] タスクが自動抽出される
- [ ] 結果がエクスポートできる

## 関連レッスン

- `/start-6-1`: Slack検索基礎
- `/start-6-2`: タスク抽出・分析

## 参考リンク

- [Slack API Documentation](https://api.slack.com/)
- [Slack Search Modifiers](https://slack.com/help/articles/202528808)
- [slack-sdk Python](https://slack.dev/python-slack-sdk/)

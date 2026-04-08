# Module 10: Notion連携 - 成果物（Final）

Notion APIを使ったデータベース操作、ページ作成の例です。

## 学習目標
- Notion APIでデータベースを操作できる
- プログラムからページを作成・更新できる
- Notionデータを外部システムと連携できる

## 成果物一覧

| ファイル | 種類 | 内容 |
|---------|------|------|
| `notion_client.py` | スクリプト | Notion APIクライアント |
| `database_schema.json` | JSON | DBスキーマ定義 |
| `sample_pages/` | JSON | サンプルページデータ |
| `sync_script.py` | スクリプト | 同期スクリプト |

## Notion API設定

### 1. インテグレーション作成
1. [Notion Integrations](https://www.notion.so/my-integrations) にアクセス
2. 「New integration」をクリック
3. 名前を入力、ワークスペースを選択
4. 「Submit」→ Internal Integration Token をコピー

### 2. データベースへのアクセス許可
1. 対象のNotionページを開く
2. 右上「...」→「Add connections」
3. 作成したインテグレーションを選択

### 3. 環境変数設定
```bash
export NOTION_API_KEY="secret_xxxxx"
export NOTION_DATABASE_ID="xxxxx-xxxx-xxxx"
```

## データベース構造

```
┌─────────────────────────────────────────────────────────┐
│  Notion Database Schema                                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  プロパティ          タイプ         説明                │
│  ─────────────────────────────────────────────────────  │
│  Name               title          タスク名             │
│  Status             select         未着手/進行中/完了   │
│  Priority           select         高/中/低             │
│  Assignee           people         担当者               │
│  Due Date           date           期限                 │
│  Tags               multi_select   タグ                 │
│  Description        rich_text      説明                 │
│  Progress           number         進捗率(0-100)        │
│  Related            relation       関連タスク           │
│  Created            created_time   作成日時             │
│  Updated            last_edited    更新日時             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Notion APIクライアント例

```python
#!/usr/bin/env python3
"""Notion APIクライアント"""
import os
import requests
from datetime import datetime
from typing import Optional, List, Dict

class NotionClient:
    """Notion API クライアント"""
    
    BASE_URL = "https://api.notion.com/v1"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("NOTION_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def get_database(self, database_id: str) -> dict:
        """データベース情報を取得"""
        url = f"{self.BASE_URL}/databases/{database_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def query_database(
        self, 
        database_id: str, 
        filter: dict = None,
        sorts: list = None,
        page_size: int = 100
    ) -> List[dict]:
        """データベースをクエリ"""
        url = f"{self.BASE_URL}/databases/{database_id}/query"
        
        payload = {"page_size": page_size}
        if filter:
            payload["filter"] = filter
        if sorts:
            payload["sorts"] = sorts
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["results"]
    
    def create_page(
        self,
        database_id: str,
        properties: dict,
        content: list = None
    ) -> dict:
        """ページを作成"""
        url = f"{self.BASE_URL}/pages"
        
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        
        if content:
            payload["children"] = content
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def update_page(self, page_id: str, properties: dict) -> dict:
        """ページを更新"""
        url = f"{self.BASE_URL}/pages/{page_id}"
        
        payload = {"properties": properties}
        
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_page(self, page_id: str) -> dict:
        """ページを取得"""
        url = f"{self.BASE_URL}/pages/{page_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


# ヘルパー関数
def build_title_property(text: str) -> dict:
    """titleプロパティを構築"""
    return {
        "title": [{"text": {"content": text}}]
    }

def build_select_property(name: str) -> dict:
    """selectプロパティを構築"""
    return {"select": {"name": name}}

def build_date_property(date: str) -> dict:
    """dateプロパティを構築（ISO 8601形式）"""
    return {"date": {"start": date}}

def build_number_property(value: int) -> dict:
    """numberプロパティを構築"""
    return {"number": value}

def build_rich_text_property(text: str) -> dict:
    """rich_textプロパティを構築"""
    return {
        "rich_text": [{"text": {"content": text}}]
    }


# 使用例
if __name__ == "__main__":
    client = NotionClient()
    database_id = os.environ.get("NOTION_DATABASE_ID")
    
    # データベース情報取得
    db_info = client.get_database(database_id)
    print(f"Database: {db_info['title'][0]['plain_text']}")
    
    # 未完了タスクを取得
    filter = {
        "property": "Status",
        "select": {
            "does_not_equal": "完了"
        }
    }
    tasks = client.query_database(database_id, filter=filter)
    print(f"未完了タスク: {len(tasks)}件")
    
    # 新規タスク作成
    new_task = client.create_page(
        database_id=database_id,
        properties={
            "Name": build_title_property("新しいタスク"),
            "Status": build_select_property("未着手"),
            "Priority": build_select_property("中"),
            "Due Date": build_date_property("2025-02-15"),
            "Progress": build_number_property(0)
        }
    )
    print(f"作成完了: {new_task['id']}")
```

## データベーススキーマJSON

```json
{
  "database_id": "xxxxx-xxxx-xxxx",
  "title": "タスク管理",
  "properties": {
    "Name": {
      "type": "title",
      "title": {}
    },
    "Status": {
      "type": "select",
      "select": {
        "options": [
          {"name": "未着手", "color": "gray"},
          {"name": "進行中", "color": "blue"},
          {"name": "完了", "color": "green"}
        ]
      }
    },
    "Priority": {
      "type": "select",
      "select": {
        "options": [
          {"name": "高", "color": "red"},
          {"name": "中", "color": "yellow"},
          {"name": "低", "color": "gray"}
        ]
      }
    },
    "Assignee": {
      "type": "people",
      "people": {}
    },
    "Due Date": {
      "type": "date",
      "date": {}
    },
    "Tags": {
      "type": "multi_select",
      "multi_select": {
        "options": [
          {"name": "開発", "color": "blue"},
          {"name": "ドキュメント", "color": "green"},
          {"name": "レビュー", "color": "purple"}
        ]
      }
    },
    "Progress": {
      "type": "number",
      "number": {
        "format": "percent"
      }
    }
  }
}
```

## 同期スクリプト例

```python
#!/usr/bin/env python3
"""外部システムとの同期スクリプト"""
from notion_client import NotionClient, build_title_property, build_select_property
import json

def sync_from_json(client, database_id, json_file):
    """JSONファイルからNotionに同期"""
    with open(json_file, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    for task in tasks:
        properties = {
            "Name": build_title_property(task["title"]),
            "Status": build_select_property(task.get("status", "未着手")),
            "Priority": build_select_property(task.get("priority", "中"))
        }
        
        client.create_page(database_id, properties)
        print(f"同期完了: {task['title']}")

def export_to_json(client, database_id, output_file):
    """Notionからエクスポート"""
    pages = client.query_database(database_id)
    
    tasks = []
    for page in pages:
        props = page["properties"]
        tasks.append({
            "id": page["id"],
            "title": props["Name"]["title"][0]["plain_text"] if props["Name"]["title"] else "",
            "status": props["Status"]["select"]["name"] if props["Status"]["select"] else "",
            "priority": props["Priority"]["select"]["name"] if props["Priority"]["select"] else ""
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    print(f"エクスポート完了: {len(tasks)}件 → {output_file}")
```

## チェックリスト

- [ ] Notion Integrationが作成されている
- [ ] データベースへのアクセスが許可されている
- [ ] APIキーが環境変数に設定されている
- [ ] データベースの取得ができる
- [ ] ページの作成ができる
- [ ] ページの更新ができる

## 関連レッスン

- `/start-10-1`: Notion API基礎
- `/start-10-2`: データベース操作・同期

## 参考リンク

- [Notion API Documentation](https://developers.notion.com/)
- [Notion API Reference](https://developers.notion.com/reference)
- [Property Types](https://developers.notion.com/reference/property-object)

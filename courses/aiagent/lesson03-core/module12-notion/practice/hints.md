# ヒント: Notion API

## Notion Integration の作成手順

1. https://www.notion.so/my-integrations にアクセス
2. 「New integration」をクリック
3. 名前を入力（例: "Task Manager"）
4. ワークスペースを選択
5. 「Submit」で作成
6. Internal Integration Token（`secret_xxx`）をコピー

## ワークスペースへの接続

Integration を作成しただけでは、ページやデータベースにアクセスできません。

1. 対象のページを Notion で開く
2. 右上の「...」メニュー → 「Connections」
3. 作成した Integration を選択して接続

## API の基本

### 認証ヘッダー
```
Authorization: Bearer secret_xxxxxxxxxxxxx
Content-Type: application/json
Notion-Version: 2022-06-28
```

### ベース URL
```
https://api.notion.com/v1/
```

### Python での基本セットアップ
```python
import requests
import os

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
```

## ページネーション

Notion API はデフォルトで最大100件を返します。それ以上のデータがある場合:

```python
def get_all_pages(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        body = {}
        if start_cursor:
            body["start_cursor"] = start_cursor

        response = requests.post(url, headers=headers, json=body)
        data = response.json()

        all_results.extend(data["results"])
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    return all_results
```

## リッチテキストの作成

### シンプルなテキスト
```json
{
  "type": "text",
  "text": { "content": "プレーンテキスト" }
}
```

### リンク付きテキスト
```json
{
  "type": "text",
  "text": {
    "content": "リンクテキスト",
    "link": { "url": "https://example.com" }
  }
}
```

### 太字・斜体
```json
{
  "type": "text",
  "text": { "content": "太字テキスト" },
  "annotations": { "bold": true }
}
```

## ページ作成のフォーマット

```python
page_data = {
    "parent": {"database_id": "<database_id>"},
    "properties": {
        "タイトル": {
            "title": [{"text": {"content": "タスク名"}}]
        },
        "ステータス": {
            "select": {"name": "未着手"}
        },
        "担当者": {
            "select": {"name": "田中太郎"}
        },
        "期限": {
            "date": {"start": "2026-02-15"}
        },
        "優先度": {
            "select": {"name": "高"}
        },
        "カテゴリ": {
            "multi_select": [{"name": "開発"}, {"name": "改善"}]
        },
        "見積もり時間": {
            "number": 8
        },
        "GitHub Issue": {
            "url": "https://github.com/owner/repo/issues/1"
        }
    }
}
```

## トラブルシューティング

| エラー | 原因 | 対処 |
|--------|------|------|
| 401 Unauthorized | APIキーが無効 | キーを再確認 |
| 403 Forbidden | Integration 未接続 | ページの Connections で接続 |
| 404 Not Found | ページ/DB ID が不正 | ID をURLから再取得 |
| 400 Validation Error | プロパティ名の不一致 | DBスキーマと照合 |
| Rate limit exceeded | リクエスト過多 | 1秒待って再実行 |

### ページ/データベース ID の取得方法

Notion の URL からIDを取得:
```
https://www.notion.so/workspace/ページ名-<32文字のID>
                                      ^^^^^^^^^^^^^^^^
                                      これがページID

https://www.notion.so/workspace/<32文字のID>?v=xxx
                                 ^^^^^^^^^^^^^^^^
                                 これがデータベースID
```

ハイフン区切りの UUID 形式に変換:
```
32文字 → 8-4-4-4-12 形式
例: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
  → a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6
```

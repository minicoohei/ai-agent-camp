# Notion API セットアップガイド

NotionのデータベースやページにアクセスするためのAPI設定手順です。

---

## 概要

| 項目 | 内容 |
|------|------|
| API名 | Notion API |
| 用途 | データベース操作、ページ作成・更新 |
| 無料枠 | 無制限（レート制限あり） |
| 必要時間 | 約15分 |

---

## ステップ1: Notion インテグレーションの作成

1. [Notion Integrations](https://www.notion.so/my-integrations) にアクセス
2. 「**新しいインテグレーション**」をクリック
3. 基本情報を入力:
   - 名前: `AI Agent Integration`（任意）
   - ロゴ: 任意
   - 関連するワークスペース: 対象のワークスペースを選択
4. 「**送信**」をクリック

---

## ステップ2: 機能の設定

インテグレーションページで機能を設定します。

### 基本設定

| 項目 | 推奨設定 |
|------|---------|
| コンテンツ機能 - 読み取り | ON |
| コンテンツ機能 - 更新 | ON |
| コンテンツ機能 - 挿入 | ON |
| ユーザー情報 | 必要に応じて |
| コメント機能 | 必要に応じて |

### Internal Integration Token の取得

1. 「**シークレット**」セクションを確認
2. 「**Internal Integration Token**」をコピー

```
例: secret_xxx...（約50文字）
```

> **重要**: トークンは `secret_` で始まります。

---

## ステップ3: データベース/ページとの接続

Notionのインテグレーションは、明示的に接続されたページにのみアクセスできます。

### ページ/データベースへのインテグレーション追加

1. Notionでアクセスしたいページ/データベースを開く
2. 右上の「**...**」メニューをクリック
3. 「**接続を追加**」を選択
4. 作成したインテグレーション名を選択（例: `AI Agent Integration`）
5. 「**確認**」をクリック

> **注意**: 親ページに接続を追加すると、子ページにもアクセスできます。

---

## ステップ4: 環境変数の設定

### .env ファイル

```bash
# .env
NOTION_API_KEY=secret_xxx...your_token_here
```

または

```bash
NOTION_TOKEN=secret_xxx...your_token_here
```

### シェル環境変数

```bash
export NOTION_API_KEY=secret_xxx...your_token_here
```

---

## ステップ5: データベースIDの取得

Notion APIでデータベースを操作するには、データベースIDが必要です。

### URLから取得

データベースのURLは以下の形式です：
```
https://www.notion.so/workspace/DATABASE_ID?v=VIEW_ID
```

または
```
https://www.notion.so/DATABASE_ID?v=VIEW_ID
```

`DATABASE_ID` の部分（32文字のハイフンなし文字列）がデータベースIDです。

### 例

```
URL: https://www.notion.so/myworkspace/a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4?v=...
Database ID: a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4
```

---

## ステップ6: 動作確認

### Pythonで確認

```python
import os
import requests

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = "your_database_id_here"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# データベース情報を取得
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Database: {data['title'][0]['plain_text']}")
    print(f"Properties: {list(data['properties'].keys())}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### curlで確認

```bash
curl -X GET "https://api.notion.com/v1/databases/$DATABASE_ID" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

---

## 基本的なAPI操作

### データベースからページを取得

```python
def query_database(database_id, filter=None):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    payload = {}
    if filter:
        payload["filter"] = filter

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# 例: 全ページ取得
results = query_database(DATABASE_ID)
for page in results["results"]:
    print(page["id"])
```

### 新しいページを作成

```python
def create_page(database_id, properties):
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# 例: タイトルとステータスを持つページを作成
properties = {
    "Name": {
        "title": [{"text": {"content": "新しいタスク"}}]
    },
    "Status": {
        "select": {"name": "Not Started"}
    }
}
new_page = create_page(DATABASE_ID, properties)
```

### ページを更新

```python
def update_page(page_id, properties):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": properties}

    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

# 例: ステータスを更新
update_page(page_id, {
    "Status": {"select": {"name": "In Progress"}}
})
```

---

## レート制限

| 制限 | 値 |
|------|-----|
| リクエスト/秒 | 3 |
| バースト | 短時間で多くのリクエストは制限される |

### レート制限への対応

```python
import time
from functools import wraps

def rate_limited(max_per_second=3):
    min_interval = 1.0 / max_per_second

    def decorator(func):
        last_called = [0.0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limited(max_per_second=2)
def api_call():
    # API呼び出し
    pass
```

---

## トラブルシューティング

### unauthorized エラー

```
{"code": "unauthorized", "message": "API token is invalid."}
```

**解決策**:
1. トークンが `secret_` で始まっているか確認
2. トークンをコピーし直す
3. インテグレーションが有効か確認

### object_not_found エラー

```
{"code": "object_not_found", "message": "Could not find database..."}
```

**解決策**:
1. データベースIDが正しいか確認
2. インテグレーションがデータベースに接続されているか確認
   - ページの「接続を追加」でインテグレーションを追加

### validation_error エラー

```
{"code": "validation_error", "message": "..."}
```

**解決策**:
1. リクエストのJSON形式を確認
2. プロパティ名がデータベースと一致しているか確認
3. プロパティの型（title, select, date等）が正しいか確認

### rate_limited エラー

```
{"code": "rate_limited", "message": "Rate limited..."}
```

**解決策**:
1. リクエスト間に待機時間を追加
2. バッチ処理を検討

---

## Pythonライブラリの利用

### notion-client パッケージ

```bash
pip install notion-client
```

```python
from notion_client import Client

notion = Client(auth=os.getenv("NOTION_API_KEY"))

# データベースクエリ
results = notion.databases.query(database_id=DATABASE_ID)

# ページ作成
new_page = notion.pages.create(
    parent={"database_id": DATABASE_ID},
    properties={
        "Name": {"title": [{"text": {"content": "タスク名"}}]}
    }
)
```

---

## セキュリティ注意事項

1. **トークンを公開しない**
   ```
   # .gitignore
   .env
   ```

2. **最小限の権限を使用**
   - 必要なページにのみインテグレーションを接続

3. **機密データの取り扱い**
   - 機密情報を含むページには接続しない

---

## 使用するスキル

以下のスキルでNotion APIを使用します：

- `notion-fetch` - Notionデータ取得

---

## 次のステップ

- [Module 10: Notion連携](../../course/CURRICULUM.md) - Notion連携の学習
- [GEMINI_API_SETUP.md](./GEMINI_API_SETUP.md) - Gemini API設定
- [SLACK_TOKEN_SETUP.md](./SLACK_TOKEN_SETUP.md) - Slack Token設定

---

## 参考リンク

- [Notion API 公式ドキュメント](https://developers.notion.com/)
- [Notion API リファレンス](https://developers.notion.com/reference/intro)
- [notion-client (Python)](https://github.com/ramnes/notion-sdk-py)

# ヒント: Notion 連携

## 認証は OAuth に統一

このモジュールでは Notion 公式 Hosted MCP（OAuth）と ncli（OAuth）を使います。
API キー（`secret_xxx`）の作成や、ページ単位の「Add connections」共有は **行いません**。

セットアップが終わっていない場合は、まず `/setup-notion` を実行してください。

## ncli の基本コマンド

```bash
# 初回ログイン（ブラウザで OAuth 承認）
ncli login

# 現在のログインユーザーを確認
ncli whoami

# ワークスペース内検索
ncli search "キーワード"

# ログアウト
ncli logout
```

## MCP 経由での操作

`/setup-notion` 完了後、Claude Code / Cursor から Notion MCP のツール（検索／ページ取得／ページ作成など）を直接呼び出せます。具体的なツール名はお使いのクライアントの MCP リストで確認してください。

## API を直接叩きたい場合（参考）

学習目的で REST API を直接呼びたい場合は、ncli が払い出す OAuth アクセストークンを使う、もしくはコードから ncli/MCP を経由します。**新たに `secret_xxx` を発行する必要はありません。**

参考までに API の基本構造を示します（実際のリクエストは ncli または MCP に任せる方が安全です）:

### ベース URL とバージョンヘッダー

```
https://api.notion.com/v1/
Notion-Version: 2022-06-28
```

### ページネーション

Notion API はデフォルトで最大100件を返します。それ以上のデータがある場合の擬似コード:

```python
def get_all_pages(query_fn, database_id):
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        body = {}
        if start_cursor:
            body["start_cursor"] = start_cursor

        data = query_fn(database_id, body)  # ncli/MCP 経由のラッパー想定

        all_results.extend(data["results"])
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    return all_results
```

### リッチテキストの作成例

シンプルなテキスト:
```json
{
  "type": "text",
  "text": { "content": "プレーンテキスト" }
}
```

リンク付きテキスト:
```json
{
  "type": "text",
  "text": {
    "content": "リンクテキスト",
    "link": { "url": "https://example.com" }
  }
}
```

太字:
```json
{
  "type": "text",
  "text": { "content": "太字テキスト" },
  "annotations": { "bold": true }
}
```

### ページ作成のフォーマット例

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
| OAuth 認証が失敗する | ブラウザでポップアップがブロックされている／承認をキャンセルした | ポップアップを許可し、`ncli login` または MCP ツールから再試行 |
| MCP から応答がない | 設定ファイルの記述ミス、ツール未再起動 | `/setup-notion` の Step 4〜5 を確認、ツールを完全再起動 |
| object_not_found | 別ワークスペースで OAuth 承認した／対象ページが存在しない | `ncli logout` → `ncli login` で正しいワークスペースを選択 |
| validation_error | リクエスト本文の形式不正 | プロパティ名・型がデータベーススキーマと一致しているか確認 |
| rate_limited | リクエスト過多（3 req/s 程度） | 待機時間を入れる／バッチ化 |

### ページ／データベース ID の取得方法

Notion の URL から ID を取得:
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

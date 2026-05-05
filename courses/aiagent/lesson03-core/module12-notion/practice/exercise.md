# 演習: Notion API 連携

![Notion API連携ワークフロー](images/exercise-hero.png)

## 概要

Notion API を使ったデータベース操作とページ管理を学びます。タスク管理データベースの作成、ページの CRUD 操作、フィルタ検索を行い、最終的に GitHub Issue と Notion を連携する自動化スクリプトを作成します。

## 前提条件

- Notion アカウントがあること
- `/setup-notion` 完了済み（**OAuth 統一**: ncli login と Notion Hosted MCP のセットアップ）
- `ncli whoami` でログインユーザーが表示できる
- ターゲットのワークスペースで OAuth 承認済み（ワークスペース全体に権限付与）
- Python 3.8+ と `requests` パッケージ（API を直接叩く演習を行う場合）

> 旧方式（Internal Integration Token, `secret_xxx`, ページ単位の Add connections 共有）は使いません。すべて OAuth ベースで進めます。

## タスク

### タスク 1: データベース作成

Notion にタスク管理データベースを API 経由で作成します。

1. `data/database-schema.json` のスキーマを確認する
2. Notion API の `POST /v1/databases` を使ってデータベースを作成する
3. 作成されたデータベースの ID を記録する

```bash
# 推奨: ncli または MCP 経由で実行する
# 例: ncli database create --schema data/database-schema.json
#
# 直接 REST API を呼ぶ場合は ncli が払い出す OAuth アクセストークンを使う。
# 新たに secret_xxx を発行する必要はない。
```

### タスク 2: ページ CRUD 操作

データベースにタスクページを追加・更新・検索・削除します。

1. `data/sample-pages.json` の10件のタスクをデータベースに追加する
2. 追加したページの1つを更新する（ステータス変更）
3. `data/sample-queries.md` のクエリ例を参考にフィルタ検索を実行する

```python
# Python から呼び出す場合の擬似コード（OAuth トークンは ncli から取得した値を使う）
import requests

# OAuth アクセストークンを ncli の認証ストアから取得する想定
# 例: token = subprocess.run(["ncli", "token"], capture_output=True, text=True).stdout.strip()

headers = {
    "Authorization": f"Bearer {access_token}",  # OAuth で取得したトークン
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# ページ作成
response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=page_data)
```

### タスク 3: GitHub Issue → Notion 自動登録

GitHub Issue が作成されたときに自動で Notion データベースにタスクを登録するスクリプトを作成します。

1. GitHub API で Issue 情報を取得する処理を実装する
2. Issue の情報を Notion ページ形式に変換する
3. Notion API でページを作成する
4. 動作確認として、既存の Issue 情報を使ってテスト実行する

## 完了条件

- [ ] タスク 1: Notion にタスク管理データベースが作成される
- [ ] タスク 2: 10件のタスクが追加され、フィルタ検索が動作する
- [ ] タスク 3: GitHub Issue の情報が Notion に自動登録される
- [ ] 各タスクの API レスポンスを確認できる

## ヒント

- 詳しくは `hints.md` を参照してください
- Notion API のバージョンは `2022-06-28` を使用
- データベースの親ページ ID は事前に取得しておく必要があります

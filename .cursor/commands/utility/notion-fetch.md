---
nonInteractiveMode: compliant
---

# Notion Fetch - Notion連携

Notionのページやデータベースを取得し、Markdown形式で出力します。

## 機能

- 単一ページの取得・Markdown変換
- データベースのテーブル形式出力
- Notion内検索
- リッチテキスト（太字・斜体・コード等）の変換
- 各種ブロックタイプ対応（見出し、リスト、コード、引用等）

## 実行手順

### Step 1: パラメータの抽出

ユーザーの入力から以下を抽出してください：
- **コマンド**: page / database / search
- **ID/URL**: NotionのページIDまたはURL
- **出力先**: ファイルパス（省略時は画面表示）

### Step 2: ツールの実行

```bash
# ページ取得
python src/notion_fetcher.py page <page_id_or_url>

# データベース取得
python src/notion_fetcher.py database <database_id_or_url>

# 検索
python src/notion_fetcher.py search "キーワード"
```

### Step 3: 結果の表示

出力されたMarkdownをユーザーに提示します。

## オプション

### page コマンド

| オプション | 説明 |
|------------|------|
| `--output PATH` / `-o` | 出力ファイルパス |

### database コマンド

| オプション | 説明 |
|------------|------|
| `--output PATH` / `-o` | 出力ファイルパス |
| `--include-content` / `-c` | 各ページの内容も含める |

### search コマンド

| オプション | 説明 |
|------------|------|
| `--type TEXT` / `-t` | フィルタ: page / database |

## 使用例

### ページ取得

```
/notion-fetch https://www.notion.so/myworkspace/Page-Name-abc123
```

### データベース取得

```
/notion-fetch database abc123def456 --output tasks.md
```

### 検索

```
/notion-fetch search "プロジェクト計画"
```

### データベースの詳細出力

```
/notion-fetch database abc123 --include-content
```

## 出力形式

### ページ

```markdown
---
id: abc123...
created: 2026-01-15T10:00:00.000Z
modified: 2026-01-16T14:30:00.000Z
title: ページタイトル
url: https://www.notion.so/...
---

# ページタイトル

## セクション1

本文テキスト...

- リスト項目1
- リスト項目2

> 引用テキスト

```python
コードブロック
```
```

### データベース

```markdown
---
id: def456...
type: database
title: タスク管理
total_items: 25
---

# タスク管理

| タスク名 | ステータス | 担当者 | 期限 |
|----------|-----------|--------|------|
| タスクA | 進行中 | 田中 | 2026-01-20 |
| タスクB | 完了 | 佐藤 | 2026-01-18 |
```

## 前提条件

`NOTION_API_KEY` 環境変数の設定が必要です。

### 設定手順

1. https://www.notion.so/my-integrations でインテグレーションを作成
2. APIキーを取得（`secret_` で始まる）
3. 対象ページ/データベースにインテグレーションを接続

詳細:

```bash
uv run python tools/api_setup_wizard.py guide notion
```

## 対応ブロックタイプ

| タイプ | 対応状況 |
|--------|---------|
| paragraph | ✅ |
| heading_1/2/3 | ✅ |
| bulleted_list_item | ✅ |
| numbered_list_item | ✅ |
| to_do | ✅ |
| toggle | ✅ |
| code | ✅ |
| quote | ✅ |
| callout | ✅ |
| divider | ✅ |
| image | ✅ |
| bookmark | ✅ |
| child_page | ✅ (タイトルのみ) |
| child_database | ✅ (タイトルのみ) |
| table | ⚠️ (基本対応) |

## 関連コマンド

- `/api-setup-wizard` - Notion API設定
- `/extract-tasks` - タスク抽出（Notionも統合予定）

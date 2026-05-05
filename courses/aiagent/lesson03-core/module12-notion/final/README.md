# module12-notion 完成例

## 概要

Notion API を使ったデータベース管理と GitHub Issue 連携の完成例です。タスク管理データベースの構築、ページの CRUD 操作、自動登録スクリプトを含みます。

## 成果物一覧

| ファイル | 説明 |
|----------|------|
| `output/database-setup.json` | データベース作成の API レスポンスサンプル |
| `output/created-pages.json` | ページ作成の API レスポンスサンプル |
| `output/automation-script.py` | GitHub Issue → Notion 自動登録スクリプト |

## 主な機能

### automation-script.py
- GitHub API で Issue 一覧を取得
- Issue のラベルから優先度・カテゴリを自動判定
- Notion API でページを自動作成
- 重複登録の防止（既存 URL チェック）
- コマンドライン引数対応（--repo, --database-id, --dry-run）

## 使い方

```bash
# 認証は OAuth 統一（事前に /setup-notion を完了しておくこと）
#   - ncli login（ブラウザ OAuth）
#   - Notion 公式 Hosted MCP（https://mcp.notion.com/mcp）
# REST API を直接叩く場合は、ncli が払い出す OAuth アクセストークンを使う想定。
export GITHUB_TOKEN="ghp_xxx"

# 実行
python output/automation-script.py \
    --repo owner/repo \
    --database-id <notion_db_id>

# ドライラン（実際には登録しない）
python output/automation-script.py \
    --repo owner/repo \
    --database-id <notion_db_id> \
    --dry-run
```

## 使用ツール

- Notion API（Python `requests` ライブラリ）
- GitHub API

## 学習ポイント

1. **Notion 認証（OAuth 統一）**: ncli login と Notion 公式 Hosted MCP（API キーは使用しない）
2. **データベーススキーマ設計**: プロパティタイプの選択と設定
3. **ページ CRUD**: 作成・読取・更新・削除の全操作
4. **フィルタクエリ**: AND/OR 条件、日付フィルタ、ソート
5. **外部 API 連携**: GitHub API と Notion API の組み合わせ

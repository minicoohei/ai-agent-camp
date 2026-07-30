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
#
# REST API を直接叩く場合は、ncli が払い出す OAuth アクセストークンを
# 環境変数 NOTION_ACCESS_TOKEN として渡す。取得手順:
#
#   # ncli の認証ストアからアクセストークンを取り出す
#   export NOTION_ACCESS_TOKEN="$(ncli token)"
#
#   # 確認
#   echo "${NOTION_ACCESS_TOKEN:0:6}..."  # 先頭数文字だけ表示してコピペ事故を防ぐ
#
# `ncli token` が利用できないバージョンを使っている場合は、
# `ncli whoami --json` の出力やローカル設定ファイル（~/.config/ncli/config.json 等）から
# アクセストークンを取り出すか、Notion Hosted MCP 経由で操作してください。
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

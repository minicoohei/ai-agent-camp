# Google Sync

gogcli を使って Gmail/Drive/Docs/Sheets/Slides/Calendar の出力を
Markdown/CSV として保存し、Git で差分管理できる形に整形します。

## 必要環境
- Python 3.11+
- gogcli（`gog` コマンド）

## 必要な環境変数
- `GOG_KEYRING_PASSWORD`
- `GOG_ACCOUNT`（単一アカウントの場合）
- `GOG_ACCOUNTS_CONFIG`（複数アカウントの場合）

## 実行例
```
python scripts/sync_google.py --days 1
```

## 出力レイアウト
```
data/{label}/
  gmail/{thread_id}.md
  calendar/{YYYY-MM-DD}.md
  docs/{doc_title}.md
  slides/{deck_title}.md
  sheets/{sheet_name}/{tab_name}.csv
```

`{label}` は `GOG_ACCOUNTS_CONFIG` の `label`、単一アカウントの場合は `default` になります。

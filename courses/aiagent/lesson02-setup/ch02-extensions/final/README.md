# ch02-extensions: 拡張機能設定 - 完成例

## 概要

VS Code / Cursor の推奨拡張機能リストと設定ファイルの完成例です。

## 成果物

| ファイル | 説明 |
|----------|------|
| `extensions-config.json` | `.vscode/extensions.json` 形式の推奨拡張リスト |
| `settings.json` | 推奨 `.vscode/settings.json` |

## 使い方

```bash
# プロジェクトの .vscode/ にコピー
cp extensions-config.json .vscode/extensions.json
cp settings.json .vscode/settings.json

# CLI で一括インストール
cat extensions-config.json | jq -r '.recommendations[]' | xargs -I {} cursor --install-extension {}
```

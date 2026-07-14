---
description: When the user says /module-24-soql — Module 24 SOQL — sf data query で Account / Opportunity を取得
nonInteractiveMode: incompatible
---
## まずこれ（最短）

チャットで **`/module-24-soql`** を実行すると、SOQL 演習用の指示が一括でコンテキストに載ります。

# Module 24 — SOQL でデータ取得

ユーザーが教材「SOQL でデータ取得」に取り組んでいます。**エージェントがターミナルで sf コマンドを実行**し、結果を要約してください。

## 前提

- Sandbox（`-o dev` または `target-org=dev`）に `sf org login web` 済み
- 本番 Org には `-o prod` を明示しない限りクエリしない

## 手順

1. `sf org list` で接続 Org を確認
2. `sf data query -o dev -q "SELECT Id, Name, Industry FROM Account LIMIT 5"`
3. 進行中商談: `IsClosed = false`, `ORDER BY Amount DESC LIMIT 20`
4. 先月クローズ商談の合計: `--json` + `SUM(Amount)`（必要なら jq）
5. `MALFORMED_QUERY` 時は `-f query.soql` に切替

## 参照

- コース: `slideId=soql`（例: `/ja/course/module-24?slideId=soql`）

---
description: When the user says /module-24-metadata-retrieve — Module 24 — Apex / Flow / Layout を retrieve
nonInteractiveMode: incompatible
---
## まずこれ（最短）

チャットで **`/module-24-metadata-retrieve`** を実行すると、メタデータ retrieve 用の指示が載ります。

# Module 24 — メタデータ retrieve

ユーザーが教材「メタデータ deploy/retrieve」の **retrieve** 部分に取り組んでいます。

## 手順

1. 未作成なら `sf project generate --name my-sf-project`
2. `cd my-sf-project`
3. `sf project retrieve start -o dev --metadata ApexClass --metadata Flow --metadata Layout`
4. `force-app/main/default/` 配下の追加ファイルを要約
5. `git status` で主要パスを報告

## 注意

- Sandbox の UI 変更とズレる場合は先に `sf org open -o dev` で確認
- 本番 retrieve は `-o prod` 明示時のみ

## 参照

- コース: `slideId=project-deploy`（例: `/ja/course/module-24?slideId=project-deploy`）

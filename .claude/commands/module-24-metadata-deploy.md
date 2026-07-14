---
description: When the user says /module-24-metadata-deploy — Module 24 — Sandbox へメタデータ deploy
nonInteractiveMode: incompatible
---
## まずこれ（最短）

チャットで **`/module-24-metadata-deploy`** を実行すると、deploy 用の指示が載ります。

# Module 24 — メタデータ deploy

ユーザーが教材「メタデータ deploy/retrieve」の **deploy** 部分に取り組んでいます。

## 手順

1. `sf project deploy start -o dev --dry-run` で検証
2. 問題なければ `sf project deploy start -o dev`
3. 単一クラス: `--metadata ApexClass:MyController`

## 注意

- 学習中は Sandbox（`-o dev`）のみ
- 本番 deploy はユーザーが明示的に `-o prod` を指定した場合のみ

## 参照

- コース: `slideId=project-deploy`

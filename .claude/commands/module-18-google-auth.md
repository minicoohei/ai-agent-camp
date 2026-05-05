---
description: スラッシュ /module-18-google-auth — Module 18 Lesson 4-1 — Google 認証（gog auth）と Gmail/Calendar 動作確認を支援
nonInteractiveMode: incompatible
---
## まずこれ（最短）

チャットで **`/module-18-google-auth`** を実行すると、このレッスン用の指示が一括でコンテキストに載ります。**長文プロンプトを手入力するより早く、確実です。**

# Module 18 — Google 認証テスト（Lesson 4-1 認証）

ユーザーが教材「モジュール18・認証テスト」に取り組んでいます。**このコマンド経由で**、**ターミナルに利用者が直接入力する必要はありません。** エージェントが `gog`（gogcli）を実行して結果を報告してください。

## 手順

1. 未認証の場合は先に **`/module-18-gcp-quick`**（同梱 OAuth の登録と `gog auth add`）を完了させる。
2. `gog gmail search --query "is:inbox" --max 5` で受信トレイが取得できるか確認する。
3. `gog calendar events --days 7` で予定が取得できるか確認する。
4. 失敗時は教材の `slideId=lesson-18-1-gcp-appendix`（GCP 自分運用）の OAuth 設定と照合する。

## 参照

- コース: `slideId=lesson-18-1-auth`（例: `/ja/course/module-18?slideId=lesson-18-1-auth`）

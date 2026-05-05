---
description: スラッシュ /module-18-gcp-appendix — Module 18 — GCP を自分で運用する（コンソール手順のチェックリスト）
nonInteractiveMode: incompatible
---
## まずこれ（最短）

チャットで **`/module-18-gcp-appendix`** を実行すると、GCP コンソール手順の支援用コンテキストが載ります。

# Module 18 — GCP 自分運用（Appendix）

ユーザーが教材「モジュール18・GCP を自分で運用したい方へ（`slideId=lesson-18-1-gcp-appendix`）」に取り組んでいます。Google Cloud Console の操作は **ユーザーのブラウザで手動**、エージェントは **各ステップのチェックリスト・つまずき対処・用語の短い説明**を行ってください。

## 手順（教材の 4 ステップに対応）

1. **プロジェクトと API**: プロジェクトを作成し、Gmail / Calendar / Drive / Sheets / Google Docs API を有効化したか確認する。
2. **課金**: 請求先アカウントをプロジェクトにリンクしたか確認する。
3. **OAuth クライアント**: 「認証情報を作成」→ OAuth クライアント ID → **外部**・**デスクトップアプリ** → JSON をダウンロードしたか確認する。
4. **OAuth 同意画面**: Branding で必須項目を入力し、**テストユーザー**に自分の Google アカウントを追加したか確認する。

## つまずき

- ウィザードの順序で同意画面の入力が先に必要な場合は、手順4の Branding を先に済ませてから手順3に戻るよう案内する。
- ダウンロードした JSON は **Git にコミットしない**。`.env` や Credential Manager 経由で参照する。

## 参照

- コース: `/ja/course/module-18?slideId=lesson-18-1-gcp-appendix`（ロケールに合わせて読み替え）

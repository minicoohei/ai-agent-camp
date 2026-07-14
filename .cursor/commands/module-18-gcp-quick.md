---
description: スラッシュ /module-18-gcp-quick — Module 18 Lesson 4-1 — ai-agent-camp 同梱 OAuth で gog 認証まで（ターミナル手入力不要）
nonInteractiveMode: incompatible
---
## まずこれ（最短）

**受講者が意識するのはチャットでの `/module-18-gcp-quick` だけで構いません。** 下の bash はエージェント（または自分で切り分けたい人）向けです。

チャットで **`/module-18-gcp-quick`** を実行すると、このレッスン用の指示が一括でコンテキストに載ります。

# Module 18 — Google 認証クイック（Lesson 4-1 GCP メイン）

ユーザーが教材「モジュール18・Google 認証クイック（`slideId=lesson-18-1-gcp`）」に取り組んでいます。**利用者がターミナルに直接コマンドを打つ必要はありません。** エージェントが `gog`（gogcli）を実行して結果を報告してください。

## 前提

- 作業ディレクトリは **ai-agent-camp リポジトリのルート**（クローン済み）を想定する。
- OAuth クライアント JSON のパス（教材どおり）: `credentials/google-workspace-desktop-oauth.json`

## 手順

### エージェント向け: gog の有無・認証状態の確認

次のコマンドを **この順で**実行し、結果をユーザーに要約する（受講者にターミナル入力を求めない）。

```bash
# PATH に gog があるか（見つからなければインストールが必要）
command -v gog || echo "gog: not found in PATH"

gog --version

gog auth --help

gog auth list
```

- `gog` が見つからない → **Module 15-1** などで gogcli（gog）のインストールを案内してから続行。
- `gog auth list` に既にアカウントがあれば、重複追加を避け、必要なときだけ `gog auth add` を実行。

### OAuth セットアップ

1. `credentials/google-workspace-desktop-oauth.json` が存在するか確認する。無い場合はユーザーに教材の Appendix（`slideId=lesson-18-1-gcp-appendix`）へ進むか、運営から JSON を入手するよう案内する。
2. `gog auth credentials set credentials/google-workspace-desktop-oauth.json` を **リポジトリルートから**実行し、共有クライアントを登録する。
3. ユーザーに **ログインに使う Google アカウントのメール**を確認し、`gog auth add <メールアドレス>` を実行する。ブラウザが開いたら、教材スライド `lesson-18-1-gcp`（Google 認証クイック）の **OAuth 画面キャプチャ 4 枚**に沿って案内する（表示順は前後しうる）:
   - **未確認アプリ**: 「詳細」→ 下部の **Cursor Bootcamp** への続行リンク（開発者表示は想定どおり `user@example.com` など）。
   - **基本同意**: プロフィール・メールの確認後、「次へ」等で進む。
   - **スコープ**: 必要に応じ「すべて選択」して許可・続行。
   - **Gog アカウント UI**（表示される場合）: DEFAULT とサービス別バッジで接続と権限を確認。
4. `gog auth list` でアカウントが登録されたことを確認する（必要なら Gog のローカル管理 UI も併用）。
5. 成功したら次は **`/module-18-google-auth`**（認証テスト）へ進み、Gmail / Calendar の疎通を確認する。

## 参照

- コース: `slideId=lesson-18-1-gcp`（メイン）、`slideId=lesson-18-1-gcp-appendix`（自分で GCP を運用する場合）
- 例: `/ja/course/module-18?slideId=lesson-18-1-gcp`

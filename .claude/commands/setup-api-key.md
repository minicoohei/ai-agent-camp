---
description: APIキー・トークンを安全に設定する手順を案内する（初学者向け）
nonInteractiveMode: incompatible
---
# APIキー設定の案内

ユーザーが「APIキーを設定したい」「Gemini のキーを入れたい」などと依頼したとき、**この手順だけ**で案内する。秘密をチャットに貼らせない。

## 最優先ルール

- **APIキーやトークンをチャットに貼らせない**。貼られたら「その考え方は危険です。チャットではなく `.env.local` に貼ってください」とだけ伝える。

## 案内する手順（この順で）

1. **用意**  
   プロジェクトルートで次を実行し、`.env.local` にキー行を追加する:
   ```bash
   uv run python tools/credential_manager.py prepare-dotenv KEY_NAME
   ```
   （`KEY_NAME` は例: `GEMINI_API_KEY`, `GITHUB_TOKEN`。複数なら `KEY_NAME1 KEY_NAME2` と並べる。）

2. **貼り付け**  
   「[`.env.local`](.env.local) を開き、`KEY_NAME=` の**右側だけ**に値を貼り付けて保存してください。保存できたら『保存した』と送ってください」と伝える。  
   チャットには値もファイル全体も貼らせない。

3. **移行**  
   ユーザーが「保存した」と言ったら、次を実行する:
   ```bash
   uv run python tools/credential_manager.py import-dotenv --delete KEY_NAME
   ```
   これで値は OS の Credential Store に移り、`.env.local` の該当行は削除される。

4. **確認**  
   ```bash
   uv run python tools/credential_manager.py status
   ```
   で、対象キーが stored と出ることを確認する。

5. **秘密を使うスクリプトの実行**  
   各レッスンやプロジェクトの手順に従う。Credential Store から環境変数へ注入する場合は `inject_to_environ` を使う（例: `setup-fal.md` 等のレッスンコマンド参照）。

## 補足

- `NEXT_PUBLIC_*` や Firebase 用の公開設定は `.env.local` に残してよい。削除するのは import したキー行だけ。
- ターミナルだけで完結させたい場合は `uv run python tools/credential_manager.py store KEY_NAME` でも登録できる（入力は画面に表示されない）。

## 参照

- コース: module-0 の「APIキーを安全に管理」スライド（slideId=api-key-management）
  - URL パス例: `/ja/course/module-0?slideId=api-key-management`（`ja` は `en` / `es` に置き換え可）
  - ローカルでブラウザを開く（macOS、開発サーバーがポート 3000 の場合）:
    ```bash
    open "http://localhost:3000/ja/course/module-0?slideId=api-key-management"
    ```
  - module-0 は `slideId` なしで開くとセットアップハブへリダイレクトされる。該当スライドへ直接入るときは必ず `slideId` を付ける。

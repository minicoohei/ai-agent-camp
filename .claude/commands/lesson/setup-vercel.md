---
description: "Vercel CLI セットアップ（完全ガイド付き）"
duration: "約10分"
prerequisites: ["Node.js 18以上がインストールされている", "ブラウザが使える"]
level: "beginner"
tags: ["setup", "vercel", "deploy", "hosting"]
---

# Vercel CLI セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-vercel` を実行して進捗を表示
2. 既存のインストール状態を自動検出:
   - `vercel --version` を実行してCLIがインストール済みか確認
   - `vercel whoami` を実行してログイン済みか確認
   - 両方成功した場合、Step 4（テスト）へスキップ
3. **このセットアップは任意です。** Vercel CLIはLesson 15-5（LP制作 - Vercelデプロイ）で使用します。すぐに必要でなければスキップしても構いません。

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Vercel CLIをインストールし、ログインしてWebサイトのデプロイ・公開ができる状態にする |
| 所要時間 | 約10分 |
| 前提条件 | Node.js 18以上がインストールされていること、ブラウザが使えること |
| 操作レベル | CLIコマンド入力あり（インストールはAIが自動実行 + ブラウザ認証） |
| 料金 | 無料プラン（Hobby）で個人プロジェクト無制限。研修では無料枠で十分 |

**このセッションの流れ:**
1. Vercelアカウントを作成する（ブラウザでサインアップ）
2. Vercel CLIをインストールする（AIが自動実行）
3. Vercelにログインする（ブラウザ認証またはトークン認証）
4. 動作テスト（AIが自動実行）

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？（このセットアップは任意です。Lesson 15-5 で使用します）",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "skip", "label": "今は必要ないのでスキップする"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 「Node.js 18以上が必要です。`node --version` で確認できます」と案内)
(skip → 「スキップしました。必要になったら `/setup-vercel` で再度セットアップできます」と案内して終了)
(different_lesson → モジュール一覧を表示)

---

## Step 1: Vercel アカウント作成

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://vercel.com/signup
# Windows:
start https://vercel.com/signup
# Linux:
xdg-open https://vercel.com/signup
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 1: Vercel アカウント作成",
  "questions": [{
    "id": "account_status",
    "prompt": "ブラウザが開きましたか？以下の手順でアカウントを作成してください:\n\n1. 「Continue with GitHub」をクリック（推奨）\n   - GitHubアカウントでそのままサインアップできます\n   - または「Continue with GitLab」「Continue with Email」も選択可能\n2. 認証・メール確認を済ませる\n3. アカウント作成が完了する\n\nアカウントの状態を教えてください:",
    "options": [
      {"id": "created", "label": "アカウント作成しました！"},
      {"id": "already_have", "label": "既にアカウントを持っている"},
      {"id": "no_github", "label": "GitHubアカウントがない"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"}
    ]
  }]
}
```

(created → Step 2へ)
(already_have → Step 2へ)
(no_github → 「Emailでもサインアップできます。サインアップページで『Continue with Email』を選択してください。または先に `/setup-github` でGitHubアカウントを作成することもおすすめです」と案内)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://vercel.com/signup」と案内)

---

## Step 2: Vercel CLI インストール

**AIが自動で実行すること:**
1. Node.jsのバージョンを確認する:
   ```bash
   node --version
   ```
   - Node.js 18未満の場合: 「Node.js 18以上が必要です。 `/start-0-1` でセットアップしてください」と案内して中断
2. Vercel CLIをインストールする:
   ```bash
   npm i -g vercel
   ```
   - 権限エラー（`EACCES`）の場合: `sudo npm i -g vercel` を案内
3. インストール確認:
   ```bash
   vercel --version
   ```

**インストール成功時:**
```text
Vercel CLI がインストールされました！（バージョン: XX.X.X）
次はVercelアカウントにログインします。
```

**インストール失敗時のAskQuestion:**
```json
{
  "title": "インストールでエラーが発生しました",
  "questions": [{
    "id": "install_error",
    "prompt": "Vercel CLIのインストールでエラーが発生しました。",
    "options": [
      {"id": "retry", "label": "もう一度試す"},
      {"id": "sudo", "label": "管理者権限で試す（sudo）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip", "label": "スキップして後で試す"}
    ]
  }]
}
```

(retry → `npm i -g vercel` を再実行)
(sudo → `sudo npm i -g vercel` を実行)
(show_error → エラーメッセージを表示して原因と解決方法を案内)
(skip → 「スキップしました。後で `/setup-vercel` で再度セットアップできます」と案内)

---

## Step 3: Vercel ログイン

**方法A（対話環境・推奨）と方法B（非対話環境・トークン認証）の2つがあることを案内する。**

**AIが実行すること:**
1. まず方法Aを試みる: `vercel login` を実行
2. ブラウザが自動で開き、Vercelアカウントで認証する
3. ターミナルに「Congratulations!」と表示されればログイン完了

**ユーザーに案内するメッセージ:**

```text
Vercelへのログインを行います。

┌─────────────────────────────────────────────────────────────┐
│ 方法A（推奨）: ブラウザ認証                                │
│                                                             │
│ `vercel login` を実行するとブラウザが開きます。             │
│ Vercelアカウントで認証すれば完了です。                       │
│                                                             │
│ 方法B（非対話環境）: トークン認証                           │
│                                                             │
│ CI/CD環境やブラウザが使えない場合:                          │
│ 1. https://vercel.com/account/tokens でトークンを作成       │
│ 2. 別ターミナルで以下を実行:                                │
│    uv run python tools/credential_manager.py store VERCEL_TOKEN    │
│ 3. デプロイ時に --token オプションで使用                    │
└─────────────────────────────────────────────────────────────┘
```

**AskQuestionの設定:**
```json
{
  "title": "Step 3: Vercel ログイン",
  "questions": [{
    "id": "login_status",
    "prompt": "`vercel login` を実行しました。結果を教えてください:",
    "options": [
      {"id": "done", "label": "ログインできた（Congratulations! が表示された）"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "non_interactive", "label": "非対話環境を使っている（トークン認証したい）"}
    ]
  }]
}
```

(done → Step 4へ)
(browser_not_open → 「ブラウザが開かない場合は、ターミナルに表示されたURLを手動でブラウザにコピー＆ペーストしてください。それでも解決しない場合は、方法B（トークン認証）をお試しください」と案内)
(non_interactive → 以下のトークン認証フローを案内)

### 方法B: トークン認証（非対話環境用）

**AIが実行すること:**
1. ブラウザでトークン発行ページを開く:
   ```bash
   # Mac:
   open https://vercel.com/account/tokens
   # Windows:
   start https://vercel.com/account/tokens
   # Linux:
   xdg-open https://vercel.com/account/tokens
   ```

**ユーザーに案内するメッセージ:**

```text
トークン認証でセットアップします。

┌─────────────────────────────────────────────────────────────┐
│ 別のターミナルウィンドウで以下の手順を実行してください:     │
│                                                             │
│ 1. ブラウザで https://vercel.com/account/tokens を開く      │
│ 2. 「Create」ボタンでトークンを作成                        │
│ 3. トークンをコピー                                        │
│ 4. 別ターミナルで以下のコマンドを実行:                      │
│                                                             │
│    uv run python tools/credential_manager.py store VERCEL_TOKEN    │
│                                                             │
│ → 「Enter value for VERCEL_TOKEN:」と表示されます           │
│ → コピーしたトークンを貼り付けてEnterを押してください       │
│   （入力した文字は画面に表示されません。これは正常です）    │
│ → 「Stored VERCEL_TOKEN」と表示されたら保存完了です         │
└─────────────────────────────────────────────────────────────┘

保存が完了したら、こちらのチャットに戻って「完了」と教えてください。
```

**トークン保存後のAskQuestion:**
```json
{
  "title": "トークン認証",
  "questions": [{
    "id": "token_status",
    "prompt": "別のターミナルでトークンを保存できましたか？",
    "options": [
      {"id": "done", "label": "保存しました！"},
      {"id": "terminal_help", "label": "ターミナルの開き方がわからない"},
      {"id": "command_error", "label": "コマンドでエラーが出た"}
    ]
  }]
}
```

(done → Step 4へ)
(terminal_help → 「Cursorの場合: 画面上部のメニュー > Terminal > New Terminal、またはキーボードの Ctrl+バッククォート (Macの場合は Cmd+バッククォート) を押してください。Claude Codeの場合: 別のターミナルウィンドウ/タブを開いてください。Mac: Cmd+T (新しいタブ) または Cmd+N (新しいウィンドウ)。Windows: PowerShell や Windows Terminal を スタートメニュー から開くか、Ctrl+Shift+T で新しいタブを追加してください。開いたら cd でプロジェクトのディレクトリに移動してください」と案内)
(command_error → AIが `uv run python tools/credential_manager.py status` を実行して状況を確認し、原因を特定。keyring 未インストールの場合は `pip install keyring` を自動実行)

---

## Step 4: テスト

**AIが自動で実行すること:**

1. ログイン方法に応じてテストを実行する:
   - **方法A（ブラウザ認証）の場合**: `vercel whoami` を実行し、ユーザー名が表示されれば成功
   - **方法B（トークン認証）の場合**: まず `uv run python tools/credential_manager.py status` で `VERCEL_TOKEN` が保存されているか確認し、保存済みなら credential_manager からトークンを取得して `vercel whoami --token <TOKEN>` で確認する

**テスト成功時:**
```text
Vercel CLIのセットアップが完了しました！

テスト結果: ログインユーザー名「xxxxx」を確認しました。
これでWebサイトのデプロイ・公開ができるようになりました。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "`vercel whoami` でエラーが発生しました。考えられる原因を確認しましょう。",
    "options": [
      {"id": "retry", "label": "もう一度テストする"},
      {"id": "relogin", "label": "ログインし直す（Step 3に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行)
(relogin → Step 3に戻る)
(show_error → エラーメッセージを表示して原因と解決方法を案内)
(skip_test → 「テストはスキップしました。後で `/check-setup` で確認できます」と案内)

---

## よくあるトラブルと解決方法

**AskQuestionの設定:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_permission", "label": "npm権限エラー（EACCES）が出る"},
      {"id": "trouble_notfound", "label": "「vercel: command not found」が出る"},
      {"id": "trouble_browser", "label": "ブラウザ認証が失敗する"},
      {"id": "trouble_node", "label": "Node.jsのバージョンが古い"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: npm権限エラー（EACCES）
**原因**: グローバルインストールに管理者権限が必要
**AIが行うこと**:
1. `sudo npm i -g vercel` を案内
2. それでも解決しない場合は `npm config set prefix ~/.npm-global` でユーザーディレクトリにインストール先を変更し、PATHに `~/.npm-global/bin` を追加する方法を案内

### トラブル2: 「vercel: command not found」
**原因**: PATHが通っていない、またはインストールが不完全
**AIが行うこと**:
1. `which vercel` や `npm list -g vercel` でインストール場所を確認
2. PATHに追加が必要な場合はシェル設定ファイル（`.zshrc` / `.bashrc`）への追加を案内
3. ターミナルを再起動するか `source ~/.zshrc` を実行

### トラブル3: ブラウザ認証が失敗する
**原因**: ブラウザとCLI間の通信エラー、またはファイアウォール
**AIの案内**: 「`vercel login` を再度実行してみてください。ブラウザが開かない場合は、ターミナルに表示されるURLを手動でブラウザにコピー＆ペーストしてください。それでも解決しない場合は、方法B（トークン認証）をお試しください」

### トラブル4: Node.jsのバージョンが古い
**原因**: Node.js 18未満がインストールされている
**AIが行うこと**:
1. `node --version` で現在のバージョンを確認
2. Node.js 18以上へのアップグレードを案内（`nvm install 18` または公式サイトからダウンロード）

### トラブル5: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] Vercel アカウントを作成した
- [ ] Vercel CLI がインストールされている（vercel --version）
- [ ] Vercel にログインしている（vercel whoami）
- [ ] テスト成功（ユーザー名が表示された）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "Vercel CLIのセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "try_deploy", "label": "LP制作・デプロイを試す（/start-15-5）"},
      {"id": "back_to_setup", "label": "セットアップ一覧に戻る（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- try_deploy → /start-15-5 を案内
- back_to_setup → /start-0-1 を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-vercel` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/start-15-5` でLP制作・Vercelデプロイに挑戦しましょう」

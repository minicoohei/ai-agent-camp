---
description: "GitHub アカウント設定とリポジトリ作成"
duration: "約10分"
prerequisites: ["/setup-start 完了"]
level: "beginner"
tags: ["setup", "github"]
---

# GitHub アカウント設定とリポジトリ作成

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-github` を実行して進捗を表示
2. `gh auth status` で既にログイン済みか確認。ログイン済みなら「GitHub認証は完了しています」と表示
3. `git remote -v` で自分用リポが既にあるか確認。あれば「リポジトリも設定済みです。スキップしますか？」と確認

## このセッションでやること

**GitHub アカウント設定** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GitHub にログインし、自分専用の private リポジトリを作成する |
| 所要時間 | 約10分（アカウント作成が必要な場合は15分） |
| 使うスキル | なし（AIが全て自動で実行します） |
| 前提条件 | `/setup-start` 完了済み（Python / Node.js / Git / GitHub CLI がインストール済み） |
| 次のコマンド | `/start-0-1`（環境セットアップ確認） |

**このセッションの流れ:**
1. GitHub アカウントの確認
2. GitHub 認証（ブラウザで「許可」ボタンを押すだけ）
3. 自分専用リポジトリの作成

> **重要**: あなたがターミナルにコマンドを入力する必要は一切ありません。全てAIが裏側で自動実行します。ブラウザが開いたら画面の指示に従うだけでOKです。
> **セキュリティ注意**: パスワードやトークンをチャットに貼り付けないでください。認証は全てブラウザ経由で安全に行います。
> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。
>
> **Codex向けメモ**: Codex では `/setup-github` をそのまま実行するのではなく、このドキュメント内の確認手順と `gh auth` の実処理を順番に進めます。ブラウザ上のログインや認可ボタンのクリックだけユーザーが担当します。

---

## セッション開始前の確認

**AskQuestionの設定:**
```json
{
  "title": "セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "chrome", "label": "/chrome でブラウザ操作を自動化する"},
      {"id": "check_prereq", "label": "/setup-start をまだやっていない"},
      {"id": "what_is_github", "label": "GitHub って何？"}
    ]
  }]
}
```

(ready → Step 1へ)
(chrome → Step 1 でアカウント作成が必要な場合、ブラウザを開いた後に「Chrome 統合で自動化する場合」セクションの手順で自動実行する)
(check_prereq → 「先に /setup-start を実行してください。必要なソフトウェアのインストールを確認します。」と案内)
(what_is_github → 以下を案内:「GitHub は、プログラムやファイルを安全に保存・管理できるクラウドサービスです。Google ドライブのプログラマー版のようなものです。この研修では、あなたの作業内容を保存するために使います。無料で使えます。」→ Step 1へ)

---

## Step 1: GitHub アカウントの確認

**AskQuestionの設定:**
```json
{
  "title": "Step 1: GitHub アカウントの確認",
  "questions": [{
    "id": "has_account",
    "prompt": "GitHub のアカウントを持っていますか？",
    "options": [
      {"id": "yes", "label": "持っている"},
      {"id": "no", "label": "持っていない（作りたい）"},
      {"id": "not_sure", "label": "わからない"}
    ]
  }]
}
```

### アカウントを持っている場合 (yes)

→ Step 2 へ進む

### アカウントを持っていない場合 (no)

**AIが自動実行する内容:**
まず `uname -s` を実行して OS を判定する（Step 1 で判定済みの場合はその結果を使用）。

表示:
```text
GitHub のアカウントを作成しましょう。
AIがブラウザを自動で開きます。少しお待ちください...
```

```bash
# AIが実行:
# Mac:
open https://github.com/signup
# Windows:
start https://github.com/signup
```

**アカウント作成手順の案内:**
```text
ブラウザが開いたら、以下の手順で進めてください:

1. メールアドレスを入力して「Continue」をクリック
2. パスワードを設定して「Continue」をクリック
   （8文字以上、数字または記号を含むパスワードにしてください）
3. ユーザー名を決めて「Continue」をクリック
   （半角英数字とハイフンのみ。例: taro-yamada）
4. メール通知の設定を選んで「Continue」をクリック
5. パズル認証を解いて「Create account」をクリック
6. 登録したメールアドレスに確認コードが届きます
7. メールに記載された 6桁のコードを入力

アカウント作成が完了したら、ここに「できた」と入力してください。
```

### Chrome 統合で自動化する場合（`/chrome` モード、新規アカウント作成時のみ）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://github.com/signup を開く
2. Chrome 統合を使って以下の操作を順番に実行する:
   - メールアドレス入力欄にフォーカスし、ユーザーに入力を促す
   - 「Continue」ボタンをクリック
   - パスワード入力後に「Continue」をクリック
   - ユーザー名入力後に「Continue」をクリック
   - メール通知設定後に「Continue」をクリック
   - パズル認証はユーザーに操作を任せる
   - 「Create account」をクリック
3. メール確認コードの入力はユーザーが手動で行う
4. アカウント作成完了後、Step 2 に進む

**注意:** パスワードやメールアドレスの値はブラウザ画面から読み取らないこと。

Chrome 統合が利用できない場合は、上記の手順を手動で実行してください。

**AskQuestionの設定（完了確認）:**
```json
{
  "title": "アカウント作成の確認",
  "questions": [{
    "id": "account_created",
    "prompt": "GitHub アカウントの作成は完了しましたか？",
    "options": [
      {"id": "done", "label": "完了した！"},
      {"id": "stuck", "label": "途中でつまった"},
      {"id": "browser_not_open", "label": "ブラウザが開かなかった"}
    ]
  }]
}
```

(done → Step 2 へ)
(stuck → 「どの画面で止まっていますか？画面に表示されている内容を教えてください。」と聞いて対応)
(browser_not_open → 「ブラウザを開いて、アドレスバーに https://github.com/signup と入力してください」と案内)

### わからない場合 (not_sure)

表示:
```text
確認してみましょう。以下のどちらかに心当たりはありますか？
- GitHub から登録確認メールを受け取ったことがある
- https://github.com にログインできる

わからない場合は、新しく作成しても問題ありません。
```

**AskQuestionの設定:**
```json
{
  "title": "アカウントの確認",
  "questions": [{
    "id": "account_check",
    "prompt": "どうしますか？",
    "options": [
      {"id": "try_login", "label": "ログインを試してみる（ブラウザを開いて）"},
      {"id": "create_new", "label": "新しく作成する"}
    ]
  }]
}
```

(try_login → AIが `open https://github.com/login` / `start https://github.com/login` を実行してブラウザを開く → ログインできたら Step 2 へ、できなかったら新規作成フローへ)
(create_new → 上記「アカウントを持っていない場合」のフローへ)

---

## Step 2: GitHub 認証

**AIが自動実行する内容:**

### 2-1. 既存の認証状態を確認

まず `gh auth status` を実行して、既にログイン済みか確認する。

**既にログイン済みの場合:**
```text
GitHub に {ユーザー名} としてログイン済みです。
```
→ Step 3 へ進む

**未ログインの場合:**

### 2-2. ブラウザ認証を開始

表示:
```text
GitHub にログインします。
AIがブラウザを自動で開きます。以下の手順に従ってください:
```

```bash
AIが実行: gh auth login --web -p https
```

このコマンドの結果に応じて2つのパターンがある:

**パターンA: ブラウザが自動で開く場合**
```text
ブラウザが自動で開きました。
画面に表示される「Authorize GitHub CLI」の緑色のボタンをクリックしてください。
完了すると、このチャットに自動で結果が表示されます。
```

**パターンB: 8桁のコードが表示される場合**

コマンド出力から表示された 8桁のコード（例: `XXXX-XXXX`）を読み取り、以下を案内:
```text
ブラウザに認証ページが開いています。
以下のコードを画面に入力してください:

    XXXX-XXXX

（上のコードをそのまま入力してください）

手順:
1. ブラウザの画面に 8桁の入力欄が表示されています
2. 上記のコードを入力して「Continue」をクリック
3. 「Authorize GitHub CLI」の緑色のボタンをクリック
4. 完了すると、このチャットに自動で結果が表示されます
```

もしブラウザが開かない場合:
```text
ブラウザが開かなかった場合は、以下のURLをブラウザで開いてください:
https://github.com/login/device

開いたら、上記のコードを入力してください。
```

### 2-3. 認証結果の確認

AIが `gh auth status` を実行して結果を確認する。

**認証成功の場合:**
```text
認証成功です！ {ユーザー名} として GitHub にログインしました。
```
→ Step 3 へ進む

**認証失敗の場合:**

**AskQuestionの設定:**
```json
{
  "title": "認証に問題が発生しました",
  "questions": [{
    "id": "auth_trouble",
    "prompt": "認証がうまくいかなかったようです。状況を教えてください。",
    "options": [
      {"id": "retry", "label": "もう一度やり直す"},
      {"id": "browser_issue", "label": "ブラウザが開かなかった"},
      {"id": "code_expired", "label": "コードの入力画面が消えてしまった"},
      {"id": "other_error", "label": "エラーメッセージが表示された"}
    ]
  }]
}
```

(retry → `gh auth login --web -p https` を再実行)
(browser_issue → 「ブラウザを開いて https://github.com/login/device にアクセスしてください」と案内し、コードを再表示)
(code_expired → 「コードの有効期限が切れた可能性があります。もう一度実行します。」→ `gh auth login --web -p https` を再実行)
(other_error → 「表示されているエラーメッセージを教えてください」と聞いて対応)

---

## Step 3: 自分専用リポジトリの作成

**AIが自動実行する内容:**

### 3-1. 現在の状態を確認

AIが以下を順番に実行:
1. `gh auth status` からログインユーザー名を取得
2. `git remote -v` で現在の remote 設定を確認

### 3-2. 状態に応じた処理

**ケースA: 既に自分用リポジトリが設定されている場合**
（`git remote -v` の origin URL にログインユーザー名が含まれている場合）

表示:
```text
あなた専用のリポジトリは既に設定されています。
  リポジトリ: https://github.com/{username}/ai-agent-camp

問題ありません。次のステップへ進みましょう。
```
→ 完了セクションへ

**ケースB: origin が TokenPocket/ai-agent-camp（教材配布元）のままの場合**

表示:
```text
現在の設定は教材の配布元リポジトリを指しています。
あなた専用の private リポジトリを作成します。
```

**AskQuestionの設定:**
```json
{
  "title": "自分専用リポジトリの作成",
  "questions": [{
    "id": "create_repo",
    "prompt": "{username}/ai-agent-camp という名前で、あなた専用の private リポジトリを作成します。よろしいですか？",
    "options": [
      {"id": "yes", "label": "作成する"},
      {"id": "different_name", "label": "別の名前にしたい"},
      {"id": "explain", "label": "リポジトリって何？"}
    ]
  }]
}
```

(yes → リポジトリ作成を実行)
(different_name → 「どのような名前にしますか？半角英数字とハイフンが使えます。」と聞いて入力を受け取る)
(explain → 「リポジトリとは、ファイルの保存場所です。Google ドライブのフォルダのようなものと考えてください。private に設定するので、あなただけがアクセスできます。」と案内 → 再度 AskQuestion を表示)

**リポジトリ作成の実行:**

AIが以下を順番に実行:

1. 既存の origin を upstream にリネーム（教材配布元として保持）:
   ```bash
   git remote rename origin upstream
   ```
   （既に upstream がある場合はスキップ）

2. 自分用リポジトリを作成して origin に設定:
   ```bash
   gh repo create {username}/ai-agent-camp --private --source . --remote origin --push
   ```

3. 結果を確認:
   ```bash
   git remote -v
   ```

**作成成功の場合:**
```text
あなた専用の private リポジトリが作成されました！

  リポジトリURL: https://github.com/{username}/ai-agent-camp
  公開設定: private（あなただけがアクセスできます）

これで研修の成果物が安全に保存されるようになりました。
```
→ 完了セクションへ

**作成失敗の場合:**

AIがエラーメッセージを解析して原因を特定:

- 「already exists」→ 同名リポジトリが既にある場合:
  ```text
  同じ名前のリポジトリが既に存在しています。
  ```
  **AskQuestionの設定:**
  ```json
  {
    "title": "リポジトリが既に存在しています",
    "questions": [{
      "id": "repo_exists",
      "prompt": "同名のリポジトリが見つかりました。どうしますか？",
      "options": [
        {"id": "use_existing", "label": "既存のリポジトリを使う"},
        {"id": "different_name", "label": "別の名前で作成する"}
      ]
    }]
  }
  ```
  (use_existing → AIが `git remote add origin https://github.com/{username}/ai-agent-camp.git` と `git push -u origin main` を実行)
  (different_name → 「どのような名前にしますか？」と聞いて入力を受け取り、その名前で再実行)

- 「permission denied」→ 認証に問題がある場合:
  → Step 2 の認証フローへ戻る

- その他のエラー → エラー内容を表示し、「画面に表示されている内容を教えてください」と聞いて対応

**ケースC: origin がない場合**
（`git remote -v` で何も表示されない場合）

表示:
```text
リモートリポジトリが設定されていません。
あなた専用の private リポジトリを新規作成します。
```
→ ケースB の「リポジトリ作成の実行」と同じ手順を実行（ただし手順1のリネームはスキップ）

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
      {"id": "trouble_1", "label": "ブラウザが開かない"},
      {"id": "trouble_2", "label": "認証コードを入力する画面がない"},
      {"id": "trouble_3", "label": "リポジトリ作成でエラーが出る"},
      {"id": "trouble_4", "label": "GitHub のパスワードを忘れた"},
      {"id": "trouble_5", "label": "その他のトラブル"}
    ]
  }]
}
```

### トラブル1: 「ブラウザが開かない」
**原因**: デフォルトブラウザの設定、またはセキュリティソフトのブロック
**解決方法**:
```text
ブラウザを手動で開いて、以下のURLにアクセスしてください:
- アカウント作成: https://github.com/signup
- ログイン: https://github.com/login
- デバイス認証: https://github.com/login/device
```

### トラブル2: 「認証コードを入力する画面がない」
**原因**: ブラウザの別タブで開かれている、またはポップアップブロック
**解決方法**:
```text
1. ブラウザのタブを確認してください（新しいタブが開いているかもしれません）
2. 見つからない場合は、ブラウザで https://github.com/login/device を開いてください
3. 表示されたコードを入力してください
```

### トラブル3: 「リポジトリ作成でエラーが出る」
**原因**: 認証切れ、ネットワーク問題、または権限不足
**解決方法**:
AIが `gh auth status` を実行して認証状態を確認。
- 認証切れ → Step 2 の認証フローへ戻る
- ネットワーク問題 → インターネット接続を確認するよう案内
- 権限不足 → `gh auth refresh -s repo` を実行して権限を更新

### トラブル4: 「GitHub のパスワードを忘れた」
**解決方法**:
```text
AIがパスワードリセットページを開きます。
```
```bash
# AIが実行:
# Mac:
open https://github.com/password_reset
# Windows:
start https://github.com/password_reset
```

```text
1. メールアドレスを入力して「Send password reset email」をクリック
2. メールに届いたリンクをクリック
3. 新しいパスワードを設定
4. 完了したら、ここに「できた」と入力してください
```

### トラブル5: 「その他のトラブル」
**解決方法**:
```text
どのような問題が起きていますか？画面に表示されているエラーメッセージや状況を教えてください。
AIが原因を診断して解決策を提示します。
```

---

## チェックポイント

AIが全項目を自動で確認し、結果を一覧表示する:

| 項目 | 確認コマンド | 期待される結果 |
|------|-------------|---------------|
| GitHub 認証 | `gh auth status` | ログインユーザー名が表示される |
| リモートリポジトリ | `git remote -v` | origin が自分のリポジトリを指している |
| Push 状態 | `git log --oneline -1` | 最新のコミットが存在する |

---

## 完了

```text
おめでとうございます！GitHub の設定が全て完了しました！

  GitHubユーザー名: {username}
  リポジトリURL: https://github.com/{username}/ai-agent-camp
  公開設定: private（あなただけがアクセスできます）

これで研修を始める準備が整いました。
```

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_lesson", "label": "研修を開始する（/start-0-1）"},
      {"id": "view_repo", "label": "作成したリポジトリをブラウザで見る"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(next_lesson → 「新しいチャットを開いて /start-0-1 と入力してください」と案内)
(view_repo → AIが `open https://github.com/{username}/ai-agent-camp` / `start https://github.com/{username}/ai-agent-camp` を実行してブラウザで表示 → その後「研修を開始するには、新しいチャットを開いて /start-0-1 と入力してください」と案内)
(finish → 「お疲れさまでした！研修を始めるときは /start-0-1 と入力してください。」と案内)

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-github` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/setup-gemini` でGemini APIを設定しましょう」

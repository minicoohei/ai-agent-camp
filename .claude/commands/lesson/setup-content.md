---
description: "Firebase 認証 + GitHub 連携 + 教材コンテンツのセットアップ"
duration: "約5分"
prerequisites: ["/setup-start 完了"]
level: "beginner"
tags: ["setup", "firebase", "github", "content"]
---

# 教材コンテンツのセットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/firebase_onboarding.py cleanup-token` で残存する一時ファイルを削除
2. `uv run python tools/firebase_onboarding.py status` を実行してオンボーディング状態を表示
3. 全ステップ完了済みなら「教材セットアップは完了しています」と表示し、更新のみ案内
4. 途中まで完了している場合は、未完了のステップから再開

## このセッションでやること

**教材コンテンツのセットアップ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Firebase アカウントと GitHub を連携し、教材リポジトリへのアクセス権を取得する |
| 所要時間 | 約5分（GitHub アカウント作成が必要な場合は10分） |
| 使うスキル | なし（AIが全て自動で実行します） |
| 前提条件 | `/setup-start` 完了済み |
| 次のコマンド | `/start-0-1`（環境セットアップ確認） |

**このセッションの流れ:**
1. Firebase 認証（ブラウザで Google ログインボタンをクリック）
2. GitHub アカウント確認（未所持なら作成案内）
3. Firebase ↔ GitHub 自動連携
4. 教材リポジトリへのアクセス権取得
5. 教材コンテンツの初回ダウンロード

> **重要**: あなたがターミナルにコマンドを入力する必要は一切ありません。全てAIが裏側で自動実行します。ブラウザが開いたら画面の指示に従うだけでOKです。
> **セキュリティ注意**: パスワードやトークンをチャットに貼り付けないでください。認証は全てブラウザ経由で安全に行います。
> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

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
      {"id": "check_prereq", "label": "/setup-start をまだやっていない"},
      {"id": "what_is_this", "label": "これは何をするの？"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 「先に /setup-start を実行してください。必要なソフトウェアのインストールを確認します。」と案内)
(what_is_this → 以下を案内:「教材コンテンツは GitHub のプライベートリポジトリで配信しています。このセットアップでは、あなたの Firebase アカウント（Google ログイン）と GitHub アカウントを連携して、教材にアクセスできるようにします。全てAIが自動で行います。」→ Step 1へ)

---

## Step 1: Firebase 認証（Google ログイン）

**AIが自動実行する内容:**

### 1-1. オンボーディング状態の確認

AIが `uv run python tools/firebase_onboarding.py status` の出力から `firebase_auth` が ✅ か確認。

**既に完了済みの場合:**
```text
Firebase 認証は完了しています。
```
→ Step 2 へ進む

**未完了の場合:**

### 1-2. ブラウザで Firebase 認証を開始

表示:
```text
Firebase の Google 認証を行います。
ブラウザが自動で開きます。少しお待ちください...
```

AIが以下を実行:
```bash
uv run python tools/firebase_onboarding.py auth-only
```

出力が `AUTH_OK:/tmp/.firebase_token_xxxxx.tmp` の場合 → 認証成功。トークンファイルパスを記憶しておく（Step 3 で使用）。
出力が `AUTH_FAILED` の場合 → 認証失敗。

**認証成功の場合:**
```text
Firebase 認証が完了しました！ Google アカウントで正常にログインできました。
```
→ Step 2 へ進む

**認証失敗（タイムアウト）の場合:**

**AskQuestionの設定:**
```json
{
  "title": "Firebase 認証に問題が発生しました",
  "questions": [{
    "id": "firebase_trouble",
    "prompt": "ブラウザでの Google ログインがうまくいかなかったようです。",
    "options": [
      {"id": "retry", "label": "もう一度やり直す"},
      {"id": "browser_issue", "label": "ブラウザが開かなかった"},
      {"id": "popup_blocked", "label": "ポップアップがブロックされた"},
      {"id": "other", "label": "その他のエラー"}
    ]
  }]
}
```

(retry → `uv run python tools/firebase_onboarding.py auth-only` を再実行)
(browser_issue → 「ブラウザを手動で開いてください。AIがもう一度認証を開始します。」→ 再実行)
(popup_blocked → 「ブラウザの設定でポップアップを許可してください。Safari: 設定→Webサイト→ポップアップウインドウ→許可、Chrome: 設定→プライバシーとセキュリティ→サイトの設定→ポップアップとリダイレクト→許可」と案内 → 再実行)
(other → 「どのような画面が表示されていますか？状況を教えてください。」と聞いて対応)

---

## Step 2: GitHub アカウントの確認

**AIが自動実行する内容:**

### 2-1. GitHub CLI の認証状態を確認

```bash
gh api user -q .login
```

**既にログイン済みの場合:**
```text
GitHub に {username} としてログイン済みです。
```

AIが `uv run python tools/firebase_onboarding.py status` で `github_auth` が未完了なら:
```bash
python -c "
import sys; sys.path.insert(0, 'tools')
from firebase_onboarding import mark_step_completed
mark_step_completed('github_auth')
"
```
→ Step 3 へ進む

**未ログインの場合:**

**AskQuestionの設定:**
```json
{
  "title": "Step 2: GitHub アカウントの確認",
  "questions": [{
    "id": "has_github",
    "prompt": "GitHub のアカウントを持っていますか？",
    "options": [
      {"id": "yes", "label": "持っている（ログインしたい）"},
      {"id": "no", "label": "持っていない（作りたい）"},
      {"id": "not_sure", "label": "わからない"}
    ]
  }]
}
```

### 持っている場合 (yes)

表示:
```text
GitHub にログインします。ブラウザが自動で開きます。
```

```bash
gh auth login --web -p https
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

### 認証結果の確認

AIが `gh api user -q .login` を実行して結果を確認。

**認証成功の場合:**
```text
認証成功です！ {ユーザー名} として GitHub にログインしました。
```

AIが `mark_step_completed("github_auth")` を実行。
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
(code_expired → 「コードの有効期限が切れた可能性があります。もう一度実行します。」→ 再実行)
(other_error → 「表示されているエラーメッセージを教えてください」と聞いて対応)

### 持っていない場合 (no)

**AIが自動実行する内容:**
```bash
# Mac:
open https://github.com/signup
# Windows:
start https://github.com/signup
```

```text
ブラウザが開きました。以下の手順で GitHub アカウントを作成してください:

1. メールアドレスを入力して「Continue」をクリック
2. パスワードを設定して「Continue」をクリック
   （8文字以上、数字または記号を含むパスワード）
3. ユーザー名を決めて「Continue」をクリック
   （半角英数字とハイフンのみ。例: taro-yamada）
4. メール通知の設定を選んで「Continue」をクリック
5. パズル認証を解いて「Create account」をクリック
6. メールに届いた 6桁のコードを入力

アカウント作成が完了したら「できた」と教えてください。
```

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

(done → `gh auth login --web -p https` を実行して GitHub CLI にログイン → 認証成功後に `mark_step_completed("github_auth")` → Step 3 へ)
(stuck → 「どの画面で止まっていますか？画面に表示されている内容を教えてください。」と聞いて対応)
(browser_not_open → 「ブラウザで https://github.com/signup にアクセスしてください」と案内)

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

(try_login → AIが `open https://github.com/login` を実行 → ログインできたら `gh auth login --web -p https` を実行 → Step 3 へ。できなかったら新規作成フローへ)
(create_new → 上記「持っていない場合」のフローへ)

---

## Step 3: Firebase ↔ GitHub 連携

**AIが自動実行する内容:**

### 3-1. GitHub ユーザー名を取得

```bash
gh api user -q .login
```

ユーザー名を取得して表示:
```text
GitHub ユーザー名: {username}
Firebase と GitHub を連携します...
```

### 3-2. Cloud Function を呼び出し

AIが以下を実行（Step 1 で取得したトークンファイルパスを使用）:
```bash
uv run python tools/firebase_onboarding.py call-function {token_file_path}
```

出力が `OK:{username}` の場合 → 成功。
出力が `ERROR:...` の場合 → 失敗。

**NOTE:** Step 1 で `firebase_auth` が完了済みだった場合（再開時）はトークンファイルがないため、先に `uv run python tools/firebase_onboarding.py auth-only` を実行してトークンを再取得してから `call-function` を実行する。

**成功の場合:**
```text
コラボレーター招待を送信しました！
リポジトリ: minicoohei/aiagent-base-content
```
→ Step 4 へ進む

**失敗の場合:**

**AskQuestionの設定:**
```json
{
  "title": "連携に問題が発生しました",
  "questions": [{
    "id": "cf_trouble",
    "prompt": "Firebase と GitHub の連携でエラーが発生しました。",
    "options": [
      {"id": "retry", "label": "もう一度やり直す"},
      {"id": "rate_limited", "label": "「1時間待ってください」と表示された"},
      {"id": "token_expired", "label": "「Firebase token」のエラーが出た"},
      {"id": "other", "label": "その他のエラー"}
    ]
  }]
}
```

(retry → `auth-only` でトークン再取得 → `call-function` を再実行)
(rate_limited → 「レートリミットに引っかかっています。1時間後に再実行してください。」と案内)
(token_expired → 「Firebase の認証トークンが期限切れです。再認証します。」→ `auth-only` を実行して Step 3 を再開)
(other → 「表示されたエラーメッセージを教えてください」と聞いて対応)

---

## Step 4: 招待の受諾

**AIが自動実行する内容:**

### 4-1. 招待を確認・自動受諾

```bash
uv run python tools/firebase_onboarding.py check-invitation
```

出力が `ACCEPTED:{id}` の場合 → 成功。
出力が `NOT_FOUND` の場合 → 招待がまだ届いていない。

**受諾成功の場合:**
```text
招待を受諾しました！ 教材リポジトリにアクセスできるようになりました。
```
→ Step 5 へ進む

**招待が見つからない場合:**

AIが 5秒待ってから `uv run python tools/firebase_onboarding.py check-invitation` を再実行（最大3回リトライ）。

それでも見つからない場合:

**AskQuestionの設定:**
```json
{
  "title": "招待が見つかりません",
  "questions": [{
    "id": "invitation_trouble",
    "prompt": "コラボレーター招待がまだ届いていないようです。",
    "options": [
      {"id": "check_email", "label": "メールで確認する"},
      {"id": "check_github", "label": "GitHub の通知を確認する"},
      {"id": "retry_later", "label": "少し待ってからもう一度"},
      {"id": "skip", "label": "手動で受諾済み（スキップ）"}
    ]
  }]
}
```

(check_email → 「GitHub に登録したメールアドレスの受信箱を確認してください。件名に「invitation」を含むメールがあるはずです。受諾したら教えてください。」と案内)
(check_github → AIが `open https://github.com/notifications` を実行してブラウザで GitHub 通知を表示)
(retry_later → 10秒後に `check-invitation` を再実行)
(skip → AIが `git ls-remote upstream HEAD` で実際にアクセスできるか検証。成功なら `mark_step_completed("invitation_accepted")` を実行。失敗なら「まだアクセスできないようです。招待を受諾してから再実行してください。」と案内)

---

## Step 5: 教材コンテンツのセットアップ

**AIが自動実行する内容:**

### 5-1. upstream リモートの確認

```bash
git remote -v
```

**upstream が未設定の場合:**
```text
教材配布元リポジトリを upstream として設定します...
```

```bash
uv run python tools/content_updater.py --setup
```

**upstream が設定済みの場合:**
```text
教材を最新版に更新します...
```

### 5-2. コンテンツ更新の確認

```bash
uv run python tools/content_updater.py --dry-run
```

AIがドライラン結果を確認し、更新内容をユーザーに表示:
```text
更新可能なファイル: {N} 件
  変更: {M} 件
  新規: {A} 件
```

更新がない場合は「最新の状態です」と表示して完了セクションへ。

**AskQuestionの設定:**
```json
{
  "title": "教材の更新",
  "questions": [{
    "id": "update_confirm",
    "prompt": "{N} 件のファイルが更新可能です。更新しますか？",
    "options": [
      {"id": "update", "label": "更新する"},
      {"id": "skip", "label": "今はスキップする"}
    ]
  }]
}
```

(update → 以下を実行)
(skip → 完了セクションへ)

### 5-3. コンテンツ更新の実行

AIが以下を実行:
```bash
uv run python tools/content_updater.py
```

スキルコンフリクトが発生した場合（stdout に「コンフリクト検出」が表示された場合）、`content_updater.py` の `resolve_skill_conflicts()` が stdin で待機する。

**コンフリクトが発生した場合の Agent 対応:**

AIは `content_updater.py` の stdout に表示されるコンフリクト情報を読み取り、ユーザーに AskQuestion で確認する。ただし、stdin 対話が必要な `--skill-strategy ask` モード（デフォルト）では Agent との相性が悪いため、**事前にスキルの状態を確認して戦略を決定してから実行する**方式を使う。

1. まず `uv run python tools/content_updater.py --dry-run` の出力でスキルコンフリクトの有無を確認
2. コンフリクトがあるスキルごとに AskQuestion で確認:

```json
{
  "title": "スキルのコンフリクト: {skill_name}",
  "questions": [{
    "id": "skill_conflict",
    "prompt": "「{skill_name}」スキルがローカルと upstream の両方で変更されています。どうしますか？",
    "options": [
      {"id": "keep_mine", "label": "自分のバージョンを維持する"},
      {"id": "take_upstream", "label": "最新版に更新する（自分のはバックアップ）"},
      {"id": "keep_both", "label": "両方残す（自分のを -custom にリネーム）"},
      {"id": "show_diff", "label": "差分を確認してから決める"}
    ]
  }]
}
```

(keep_mine → `uv run python tools/content_updater.py --skill-strategy keep-mine` で実行)
(take_upstream → `uv run python tools/content_updater.py --skill-strategy take-upstream` で実行)
(keep_both → `uv run python tools/content_updater.py --skill-strategy keep-both` で実行)
(show_diff → AIが `git diff HEAD..upstream/main -- {skill_path}` の結果を表示 → 再度同じ AskQuestion を表示して選択を求める)

**NOTE:** 全スキルに同じ戦略を適用する場合は `--skill-strategy` で一括実行。スキルごとに異なる戦略が必要な場合は、個別のスキルパスに対して `git checkout` を手動で実行する。

**更新完了:**
```text
教材の更新が完了しました！
```

AIが `mark_step_completed("content_setup")` を実行。

---

## チェックポイント

AIが全項目を自動で確認し、結果を一覧表示する:

| 項目 | 確認コマンド | 期待される結果 |
|------|-------------|---------------|
| Firebase 認証 | `uv run python tools/firebase_onboarding.py status` | firebase_auth ✅ |
| GitHub 認証 | `gh api user -q .login` | ユーザー名が表示される |
| Firebase ↔ GitHub 連携 | `uv run python tools/firebase_onboarding.py status` | cloud_function ✅ |
| 招待受諾 | `git ls-remote upstream HEAD` | upstream にアクセスできる |
| コンテンツ | `uv run python tools/content_updater.py --status` | 最新の状態 |

---

## 完了

```text
おめでとうございます！教材コンテンツのセットアップが完了しました！

  GitHubユーザー名: {username}
  教材リポジトリ: minicoohei/aiagent-base-content
  アクセス権限: read（読み取り専用）

教材を更新するには:
  /update-content を実行してください

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
      {"id": "update_later", "label": "教材を更新する方法を確認"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(next_lesson → 「新しいチャットを開いて /start-0-1 と入力してください」と案内)
(update_later → 「教材の更新は `/update-content` コマンドで行えます。月1〜2回の更新があります。」と案内)
(finish → 「お疲れさまでした！研修を始めるときは /start-0-1 と入力してください。」と案内)

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
      {"id": "trouble_2", "label": "Firebase の認証がタイムアウトする"},
      {"id": "trouble_3", "label": "GitHub の招待が届かない"},
      {"id": "trouble_4", "label": "コンテンツの更新でエラーが出る"},
      {"id": "trouble_5", "label": "その他のトラブル"}
    ]
  }]
}
```

### トラブル1: 「ブラウザが開かない」
**原因**: デフォルトブラウザの設定、またはセキュリティソフトのブロック
**解決方法**: AIが再度 `uv run python tools/firebase_onboarding.py auth-only` を実行します。ブラウザが開かない場合は表示された URL を手動でブラウザにコピーしてください。

### トラブル2: 「Firebase の認証がタイムアウトする」
**解決方法**: 認証は120秒以内に完了する必要があります。ブラウザで Google ログイン画面が表示されたら、すぐにログインしてください。再実行すれば何度でもやり直せます。

### トラブル3: 「GitHub の招待が届かない」
**解決方法**: GitHub の通知（https://github.com/notifications）を確認してください。メールフィルタで「GitHub」からのメールが迷惑メールに振り分けられている場合もあります。

### トラブル4: 「コンテンツの更新でエラーが出る」
**解決方法**: AIが `uv run python tools/content_updater.py --status` でエラーの原因を診断します。ネットワーク接続を確認し、`gh auth status` で GitHub 認証が有効か確認してください。

### トラブル5: 「その他のトラブル」
**解決方法**: 画面に表示されているエラーメッセージや状況を教えてください。AIが原因を診断して解決策を提示します。

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/firebase_onboarding.py cleanup-token` で一時ファイルをクリーンアップ
2. `uv run python tools/firebase_onboarding.py status` で全ステップの完了を確認
3. ユーザーに次のステップを案内: 「次は `/start-0-1` で研修を開始しましょう」

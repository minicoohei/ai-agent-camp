---
description: "Lesson command"
duration: "約10分"
prerequisites: ["Node.js 18以上がインストール済み", "Googleアカウントを持っている", "ブラウザが使える"]
level: "beginner"
tags: ["setup", "gas", "clasp", "google"]
---

# Google Apps Script CLI (clasp) セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-clasp` を実行して進捗を表示
2. 既存のインストール状態を自動検出:
   - `npx -y @google/clasp --version` を実行
   - clasp が既に利用可能で `npx -y @google/clasp list` が動作する場合、Step 5（テスト）のみ実行して完了にできる
   - 未インストールの場合は Step 1 から開始

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | clasp (Google Apps Script CLI) をインストールし、OAuth認証を完了して、GASプロジェクトをローカルから作成・編集・デプロイできるようにする |
| 所要時間 | 約10分 |
| 前提条件 | Node.js 18以上がインストール済み、Googleアカウントを持っていること、ブラウザが使えること |
| 操作レベル | CLIコマンド入力あり（npx で clasp 実行 + clasp login） |
| 料金 | 無料 |

**このセッションの流れ:**
1. Node.js のバージョンを確認する
2. clasp を npx 経由で利用可能にする（グローバルインストール不要、AIが自動確認）
3. ブラウザで Apps Script API を有効化する（AIがブラウザを自動起動）
4. clasp login でOAuth認証を行う
5. 動作テスト（AIが自動実行）

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## 準備チェック

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
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(chrome → Step 3 でブラウザを開いた後、「Chrome 統合で自動化する場合」セクションの手順で自動実行する)
(check_prereq → 「Node.js 18以上がインストール済みで、Googleアカウントでブラウザにログインできれば準備OKです。Node.jsの確認は次のステップで行います」と案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: Node.js の確認

**AIが実行すること:**
1. `node --version` を実行してNode.jsのバージョンを確認する
2. バージョンが18以上であることを確認する

**Node.jsが18以上の場合:**
「Node.js v{バージョン} を確認しました。Step 2 に進みます」と案内して Step 2 へ

**Node.jsが未インストールまたは18未満の場合のAskQuestion:**

```json
{
  "title": "Step 1: Node.js のインストールが必要です",
  "questions": [{
    "id": "node_status",
    "prompt": "claspの実行にはNode.js 18以上が必要です。以下のURLからインストールしてください:\n\nhttps://nodejs.org/\n\n「LTS」バージョンのダウンロードボタンをクリックし、インストーラーの指示に従ってください。\n\nインストールが完了したら、ターミナルを再起動してください。",
    "options": [
      {"id": "installed", "label": "Node.js をインストールしました"},
      {"id": "help", "label": "インストール方法がわからない"},
      {"id": "skip", "label": "後で設定する（スキップ）"}
    ]
  }]
}
```

(installed → `node --version` を再実行して確認。18以上ならStep 2へ)
(help → 「https://nodejs.org/ にアクセスして、緑色の "LTS" ボタンをクリックしてダウンロードしてください。ダウンロードしたファイルを開いて、画面の指示に従って進めるだけでインストールできます」と案内)
(skip → 「claspのセットアップには Node.js が必要です。後で /setup-clasp を再実行してください」と案内して終了)

---

## Step 2: clasp の利用確認

**AIが自動で実行すること:**
1. `npx -y @google/clasp --version` を実行して clasp が npx 経由で利用できることを確認する
2. 実行結果を確認する

> **補足**: グローバルインストール（`npm install -g`）は不要です。`npx @google/clasp` を使えば、常に最新版の clasp をインストールなしで実行できます。

**確認成功時:**
「clasp が npx 経由で利用可能です。Step 3 に進みます」と案内して Step 3 へ

**npx の実行でエラーが発生した場合のAskQuestion:**

```json
{
  "title": "Step 2: npx の実行エラー",
  "questions": [{
    "id": "npx_error",
    "prompt": "npx @google/clasp の実行でエラーが発生しました。以下を確認してください:\n\n1. Node.js と npm が正しくインストールされているか\n2. ネットワーク接続が有効か（npx は初回実行時にパッケージをダウンロードします）",
    "options": [
      {"id": "retry", "label": "もう一度試す"},
      {"id": "check_node", "label": "Node.js の確認に戻る（Step 1）"},
      {"id": "help", "label": "他の方法を知りたい"}
    ]
  }]
}
```

(retry → `npx -y @google/clasp --version` を再実行。成功したらStep 3へ)
(check_node → Step 1 に戻る)
(help → 「ネットワーク接続を確認してください。プロキシ環境の場合は npm のプロキシ設定が必要な場合があります」と案内)

---

## Step 3: Apps Script API の有効化

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://script.google.com/home/usersettings
# Windows:
start https://script.google.com/home/usersettings
# Linux:
xdg-open https://script.google.com/home/usersettings
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 3: Apps Script API を有効化",
  "questions": [{
    "id": "api_status",
    "prompt": "ブラウザが開きましたか？以下の手順で Apps Script API を有効化してください:\n\n1. Googleアカウントでログインする\n2. 「Google Apps Script API」のトグルスイッチを探す\n3. トグルを「オン」に切り替える\n\n※ 既にオンになっている場合はそのままでOKです。\n\n完了しましたか？",
    "options": [
      {"id": "done", "label": "APIを有効化しました！（または既にオンでした）"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "no_toggle", "label": "トグルスイッチが見つからない"},
      {"id": "org_restriction", "label": "組織の管理者によって制限されていると表示される"}
    ]
  }]
}
```

(done → Step 4へ)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://script.google.com/home/usersettings」と案内)
(no_toggle → 「ページ中央付近に "Google Apps Script API" という項目と、オン/オフのトグルスイッチがあります。ページを下にスクロールしてみてください。見つからない場合は、Googleアカウントでログインしているか確認してください」と案内)
(org_restriction → 「Google Workspaceの組織管理者がApps Script APIを無効にしている可能性があります。個人のGmailアカウント（xxx@gmail.com）でログインし直してみてください。組織アカウントで使う必要がある場合は、IT管理者にApps Script APIの有効化を依頼してください」と案内)

---

## Chrome 統合で自動化する場合（`/chrome` モード）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://script.google.com/home/usersettings を開く
2. Chrome 統合を使って以下の操作を実行する:
   - 「Google Apps Script API」のトグルを見つける
   - トグルが OFF の場合は、クリックして ON に切り替える
3. トグルが ON になったことを確認し、Step 4 に進む

Chrome 統合が利用できない場合は、Step 3 の手順を手動で実行してください。

---

## Step 4: clasp login（OAuth認証）

**AIが自動で実行すること:**
1. `npx -y @google/clasp login` を実行する
2. ブラウザが自動で開き、Googleアカウントの認証画面が表示される

**AskQuestionの設定:**

```json
{
  "title": "Step 4: Googleアカウントで認証",
  "questions": [{
    "id": "login_status",
    "prompt": "clasp login を実行しました。ブラウザでGoogleアカウントの認証画面が表示されます:\n\n1. 使用するGoogleアカウントを選択する\n2. 「許可」をクリックしてclaspにアクセス権限を付与する\n3. ターミナルに「Authorization successful.」と表示されたら完了\n\n認証は完了しましたか？",
    "options": [
      {"id": "done", "label": "「Authorization successful.」と表示されました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "permission_denied", "label": "「このアプリはブロックされています」と表示される"},
      {"id": "timeout", "label": "認証画面が表示されたが、ターミナルが反応しない"}
    ]
  }]
}
```

(done → Step 5へ)
(browser_not_open → 「ターミナルにURLが表示されている場合は、それをコピーしてブラウザに貼り付けてください。SSHなどリモート環境の場合は `npx -y @google/clasp login --no-localhost` を試してください」と案内)
(permission_denied → 「Google Workspaceの組織ポリシーでサードパーティアプリがブロックされている可能性があります。個人のGmailアカウント（xxx@gmail.com）でログインし直してみてください」と案内)
(timeout → 「認証後にブラウザに "Logged in!" と表示されていれば、ターミナルに戻って確認してください。反応がない場合は Ctrl+C で中断して `npx -y @google/clasp login` を再実行してください」と案内)

---

## Step 5: 設定テスト

**AIが自動で実行すること:**

1. `npx -y @google/clasp --version` を実行してバージョンを確認する
2. `npx -y @google/clasp list` を実行してプロジェクト一覧を取得する
   - 初回は「No script files found.」や空の一覧でもOK。エラーが出なければ認証は成功

3. テスト結果に応じてAskQuestionを表示:

**テスト成功時:**
```text
clasp のセットアップが完了しました！

テスト結果:
- clasp バージョン: {バージョン}
- OAuth認証: 成功
- プロジェクト一覧取得: 成功（{件数}件のプロジェクト）

これでGoogle Apps Scriptのプロジェクトをローカルから作成・編集・デプロイできるようになりました。
Google Sheets, Forms, Docsの自動化にお使いいただけます。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "claspのテストでエラーが発生しました。考えられる原因を確認しましょう。",
    "options": [
      {"id": "retry", "label": "もう一度テストする"},
      {"id": "relogin", "label": "clasp login をやり直す（Step 4に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行)
(relogin → Step 4に戻る)
(show_error → エラーメッセージを表示して原因と解決方法を案内)
(skip_test → 「テストはスキップしました。後で /check-setup で確認できます」と案内)

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
      {"id": "trouble_npm", "label": "npx @google/clasp の実行でエラーが出る"},
      {"id": "trouble_api_disabled", "label": "「Apps Script API has not been used」エラーが出る"},
      {"id": "trouble_browser", "label": "clasp login でブラウザが開かない"},
      {"id": "trouble_org", "label": "組織のGoogleアカウントで制限されている"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: npx @google/clasp の実行でエラーが出る
**原因**: ネットワーク接続の問題、または Node.js/npm のインストール不備
**AIが行うこと**:
1. `node --version` と `npm --version` で環境を確認
2. ネットワーク接続の確認を案内。プロキシ環境の場合は npm のプロキシ設定を案内

### トラブル2: 「Apps Script API has not been used」エラー
**原因**: Apps Script API が有効化されていない
**AIが行うこと**:
1. ブラウザで https://script.google.com/home/usersettings を開く
2. 「Google Apps Script API」のトグルがオンになっているか確認を案内
3. オンにした後、`npx -y @google/clasp list` を再実行して確認

### トラブル3: clasp login でブラウザが開かない
**原因**: リモート環境・SSH接続・WSLなどでブラウザが起動できない
**AIの案内**: 「`npx -y @google/clasp login --no-localhost` を試してください。ターミナルに表示されるURLをコピーして、手動でブラウザに貼り付けて認証してください」

### トラブル4: 組織のGoogleアカウントで制限されている
**原因**: Google Workspaceの組織管理者がサードパーティアプリやApps Script APIを制限している
**AIの案内**: 「個人のGmailアカウント（xxx@gmail.com）で `npx -y @google/clasp login` を試してください。組織アカウントで使う必要がある場合は、IT管理者に以下を依頼してください: (1) Apps Script API の有効化、(2) clasp（OAuth クライアント）の許可」

### トラブル5: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] Node.js 18以上がインストールされている
- [ ] `npx -y @google/clasp --version` で clasp が利用可能であることを確認した
- [ ] Apps Script API を有効化した（https://script.google.com/home/usersettings）
- [ ] `npx -y @google/clasp login` でOAuth認証が完了した（「Authorization successful.」が表示された）
- [ ] `npx -y @google/clasp --version` でバージョンが表示された
- [ ] `npx -y @google/clasp list` がエラーなく実行できた

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "clasp のセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "start_gas", "label": "GASの基本を学ぶ（/start-10-1）"},
      {"id": "setup_other", "label": "他のセットアップに進む（/start-0-1）"},
      {"id": "check_setup", "label": "環境全体をチェックする（/check-setup）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- start_gas → /start-10-1 を案内（Clasp基本・GASプロジェクト管理）
- setup_other → /start-0-1 を案内
- check_setup → /check-setup を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-clasp` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/start-10-1` でGASの基本を学びましょう（Clasp基本・GASプロジェクト管理）」

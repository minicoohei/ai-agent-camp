---
description: "gogcli (Google Workspace CLI) セットアップ（完全ガイド付き）"
duration: "約15分"
prerequisites: ["Googleアカウントを持っている", "ブラウザが使える"]
level: "beginner"
tags: ["setup", "gogcli", "google", "gmail", "calendar", "oauth"]
---

# gogcli (Google Workspace CLI) セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-gogcli` を実行して進捗を表示
2. 既存のインストール・認証を自動検出:
   - `which gog` または `gog --version` を実行
   - gogcli がインストール済みの場合、`gog auth list` で認証状態を確認
   - インストール済み＆認証済みの場合、Step 4（動作テスト）へスキップ

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | gogcli をインストールし、Google OAuth 認証を完了して、Gmail/Calendar/Drive/Sheets にCLIからアクセスできるようにする |
| 所要時間 | 約15分 |
| 前提条件 | Googleアカウントを持っていること、ブラウザが使えること |
| 操作レベル | CLIコマンド入力なし（すべてAIが自動実行 + ブラウザでのOAuth認証のみ） |

**このセッションの流れ:**
1. gogcli をインストールする（AIが自動でOS判定・インストール）
2. Google OAuth 認証を行う（AIがコマンド実行 → ブラウザでGoogleログイン）
3. 認証済みアカウントを確認する（AIが自動実行）
4. Gmail/Calendarの動作テスト（AIが自動実行）

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
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 「Googleアカウントでブラウザにログインできれば準備OKです。gogcli は無料で利用でき、Google Workspace API の無料枠内で動作します」と案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: gogcli のインストール

**AIが実行すること:**
1. OSを自動判定する（Mac / Linux）
2. 既にインストール済みか確認する: `which gog`
3. 未インストールの場合、以下のコマンドを実行:

```bash
# Mac (Homebrew推奨):
brew install nicholasgasior/tools/gog

# Mac代替 (Goがインストール済みの場合):
go install github.com/nicholasgasior/gog@latest

# Linux (Goが必要):
go install github.com/nicholasgasior/gog@latest
```

4. インストール後、`gog --version` で確認する

**インストール方法の判定ロジック:**
- `which brew` が成功 → Homebrew でインストール
- `which go` が成功 → `go install` でインストール
- 両方ない場合 → Homebrew のインストールから案内

**AskQuestionの設定:**
```json
{
  "title": "Step 1: gogcli のインストール",
  "questions": [{
    "id": "install_status",
    "prompt": "gogcli のインストールを実行しました。結果を確認してください。",
    "options": [
      {"id": "installed", "label": "インストールできました！"},
      {"id": "brew_error", "label": "brew install でエラーが出た"},
      {"id": "go_error", "label": "go install でエラーが出た"},
      {"id": "no_brew_no_go", "label": "Homebrew も Go もインストールされていない"},
      {"id": "command_not_found", "label": "gog コマンドが見つからない"}
    ]
  }]
}
```

(installed → Step 2へ)
(brew_error → `brew update && brew tap nicholasgasior/tools` を実行後リトライ。それでも失敗する場合は `go install` を案内)
(go_error → Goのバージョン確認 `go version`。Go 1.21以上が必要。未インストールの場合は `brew install go` を案内)
(no_brew_no_go → 「まずHomebrewをインストールしましょう。ブラウザで https://brew.sh を開いてインストールコマンドをコピー・実行してください」と案内)
(command_not_found → `export PATH=$PATH:$(go env GOPATH)/bin` をシェル設定に追加する手順を案内。Homebrew の場合は `brew link gog` を実行)

---

## Step 2: Google OAuth 認証

**AIが実行すること:**
1. `gog auth add` を実行する
2. ブラウザが自動で開き、Google OAuth 認証画面が表示される

**ユーザーに案内するメッセージ:**

```text
Google OAuth 認証を開始します。

┌─────────────────────────────────────────────────────────────┐
│ ブラウザが自動で開きます。以下の手順で認証してください:     │
│                                                             │
│ 1. ブラウザでGoogleアカウントを選択（またはログイン）       │
│ 2. 「このアプリを許可しますか？」の画面で「許可」をクリック │
│ 3. 「Authorization successful」と表示されたら認証完了       │
│ 4. ターミナルに戻ってください                               │
│                                                             │
│ ※ 認証情報は ~/.config/gogcli/ に安全に保存されます        │
│ ※ APIキーの手動入力は不要です（OAuth認証で自動管理）       │
└─────────────────────────────────────────────────────────────┘
```

**AskQuestionの設定:**
```json
{
  "title": "Step 2: Google OAuth 認証",
  "questions": [{
    "id": "auth_status",
    "prompt": "ブラウザでGoogleアカウントの認証を行ってください。認証できましたか？",
    "options": [
      {"id": "authenticated", "label": "認証できました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "auth_error", "label": "認証エラーが出た"},
      {"id": "account_help", "label": "Googleアカウントの選び方がわからない"},
      {"id": "access_denied", "label": "「access denied」と表示された"}
    ]
  }]
}
```

(authenticated → Step 3へ)
(browser_not_open → 「ターミナルに表示されたURLをコピーして、手動でブラウザに貼り付けてください」と案内)
(auth_error → `gog auth add` を再実行。エラーメッセージを確認して原因を特定)
(account_help → 「普段Gmailで使用しているGoogleアカウントを選択してください。会社のGoogle Workspaceアカウントでも個人のGmailアカウントでもOKです。後から別のアカウントを追加することもできます」と案内)
(access_denied → 「組織のGoogle Workspaceで外部アプリへのアクセスが制限されている可能性があります。IT管理者に確認するか、個人のGmailアカウントでお試しください」と案内)

---

## Step 3: アカウント確認

**AIが自動で実行すること:**
1. `gog auth list` を実行して認証済みアカウント一覧を表示
2. 正しいGoogleアカウントが表示されることを確認

**確認のAskQuestion:**
```json
{
  "title": "Step 3: アカウント確認",
  "questions": [{
    "id": "account_check",
    "prompt": "認証済みアカウントが表示されました。正しいアカウントですか？",
    "options": [
      {"id": "correct", "label": "正しいアカウントです！"},
      {"id": "wrong_account", "label": "別のアカウントを使いたい"},
      {"id": "no_account", "label": "アカウントが表示されない"}
    ]
  }]
}
```

(correct → Step 4へ)
(wrong_account → `gog auth add` で別のアカウントを追加する手順を案内)
(no_account → Step 2に戻り、OAuth認証をやり直す)

---

## Step 4: 動作テスト

**AIが自動で実行すること:**

1. `gog auth list` で認証済みアカウントのメールアドレスを取得する
2. Gmail検索テストを実行:
   ```bash
   gog gmail search "newer_than:1d" --account <email>
   ```
3. Calendar取得テストを実行:
   ```bash
   gog calendar list --account <email> --days 1
   ```

**テスト成功時:**
```text
gogcli のセットアップが完了しました！

テスト結果:
- Gmail検索: 正常に動作しています
- Calendar取得: 正常に動作しています

これでGmail/Calendar/Drive/SheetsにCLIからアクセスできるようになりました。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "動作テストでエラーが発生しました。考えられる原因を確認しましょう。",
    "options": [
      {"id": "retry", "label": "もう一度テストする"},
      {"id": "reauth", "label": "OAuth認証をやり直す（Step 2に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行)
(reauth → Step 2に戻る)
(show_error → エラーメッセージを表示して原因と解決方法を案内)
(skip_test → 「動作テストはスキップしました。後で /check-setup で確認できます」と案内)

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
      {"id": "trouble_brew", "label": "brew install でエラーが出る"},
      {"id": "trouble_auth", "label": "OAuth認証が失敗する"},
      {"id": "trouble_org", "label": "組織のGoogleアカウントで制限がかかる"},
      {"id": "trouble_access", "label": "「access denied」エラーが出る"},
      {"id": "trouble_not_found", "label": "gog コマンドが見つからない"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: brew install でエラーが出る
**原因**: Homebrew のtapが登録されていない、またはHomebrewが古い
**AIが行うこと**:
1. `brew update` を実行
2. `brew tap nicholasgasior/tools` を実行
3. 再度 `brew install nicholasgasior/tools/gog` を実行
4. それでも失敗する場合は `go install` での代替手順を案内

### トラブル2: OAuth認証が失敗する
**原因**: ブラウザのポップアップブロック、またはネットワーク問題
**AIが行うこと**:
1. ターミナルに表示されたURLを手動でブラウザに貼り付ける方法を案内
2. `gog auth add` を再実行
3. ブラウザのポップアップブロック設定の確認を案内

### トラブル3: 組織のGoogleアカウントで制限がかかる
**原因**: Google Workspace 管理者が外部アプリへのアクセスを制限している
**AIの案内**: 「組織のIT管理者にgogcliの利用許可を確認してください。それが難しい場合は、個人のGmailアカウント（@gmail.com）で認証をお試しください。`gog auth add` で別のアカウントを追加できます」

### トラブル4: 「access denied」エラー
**原因**: OAuth スコープの権限不足、またはアカウントのセキュリティ設定
**AIが行うこと**:
1. `gog auth list` で認証状態を確認
2. 認証を削除して再認証を案内: `gog auth remove <email>` → `gog auth add`
3. Google アカウントのセキュリティ設定（https://myaccount.google.com/security）を確認する手順を案内

### トラブル5: gog コマンドが見つからない
**原因**: PATH が通っていない
**AIが行うこと**:
1. Homebrew でインストールした場合: `brew link gog` を実行
2. `go install` でインストールした場合: `export PATH=$PATH:$(go env GOPATH)/bin` を `.zshrc` / `.bashrc` に追加する手順を案内
3. `source ~/.zshrc` または新しいターミナルを開く手順を案内

### トラブル6: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] gogcli がインストールされている
- [ ] Google OAuth 認証が完了している
- [ ] gog auth list でアカウントが表示される
- [ ] Gmail検索テストが成功した
- [ ] Calendar取得テストが成功した

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "gogcli のセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "try_gmail", "label": "Gmail検索・閲覧を試す（/start-15-1）"},
      {"id": "try_calendar", "label": "Google Calendar操作を試す"},
      {"id": "try_article", "label": "記事作成を始める（/start-16-1）"},
      {"id": "back_to_setup", "label": "セットアップ一覧に戻る（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- try_gmail → /start-15-1 を案内
- try_calendar → Google Calendar操作の使い方を案内
- try_article → /start-16-1 を案内
- back_to_setup → /start-0-1 を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-gogcli` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/start-15-1` でGmail検索・閲覧を試しましょう」

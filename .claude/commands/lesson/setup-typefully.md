---
description: "Lesson command"
duration: "約10分"
prerequisites: ["X (Twitter) アカウントを持っている", "ブラウザが使える"]
level: "beginner"
tags: ["setup", "typefully", "api", "sns"]
nonInteractiveMode: incompatible
---
# Typefully API セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-typefully` を実行して進捗を表示
2. 既存のAPIキーを自動検出:
   - `uv run python tools/credential_manager.py status` を実行
   - TYPEFULLY_API_KEY が設定済みの場合、Step 4（APIテスト）のみ実行して完了にできる
   - `.env` に平文で存在する場合、credential store への移行を提案

> **このセットアップは任意です。** Typefully APIはマーケティング系レッスン（モジュール12）でSNS投稿のスケジューリングに使用します。マーケティング系レッスンを受講しない場合はスキップして構いません。

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Typefully で API キーを取得し、Credential Store に保存してSNS投稿のスケジューリング・管理機能を使えるようにする |
| 所要時間 | 約10分 |
| 前提条件 | X (Twitter) アカウントを持っていること、ブラウザが使えること |
| 操作レベル | 基本はAI自動実行（APIキー保存時のみ、別ターミナルで手動1コマンド） |

**Typefully とは:**
X (Twitter)、LinkedIn等のSNS投稿をスケジューリング・管理するサービスです。AIで生成したコンテンツを直接投稿できます。無料プランあり。有料プランは$12.5/月〜。

**このセッションの流れ:**
1. ブラウザでTypefullyを開く（AIが自動でブラウザを起動）
2. X (Twitter) アカウントでサインアップ・ログインする
3. APIキーを取得する（設定画面からコピーするだけ）
4. credential_manager.py でAPIキーを安全に保存する（別ターミナルで実行）
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
      {"id": "skip", "label": "このセットアップをスキップしたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(chrome → Step 1 でブラウザを開いた後、「Chrome 統合で自動化する場合」セクションの手順で自動実行する)
(check_prereq → 「X (Twitter) アカウントでブラウザにログインできれば準備OKです。Typefullyは無料プランがあるので、費用はかかりません」と案内)
(skip → 「Typefully APIのセットアップをスキップしました。後で必要になったら /setup-typefully で設定できます」と案内して終了)
(different_lesson → モジュール一覧を表示)

---

## Step 1: ブラウザでTypefullyを開く

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://typefully.com
# Windows:
start https://typefully.com
# Linux:
xdg-open https://typefully.com
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 1: Typefullyにサインアップ / ログイン",
  "questions": [{
    "id": "browser_status",
    "prompt": "ブラウザが開きましたか？以下の手順でサインアップしてください:\n\n1. Typefully のトップページで「Get started free」をクリック\n2. 「Sign up with X (Twitter)」を選択してXアカウントで認証する\n3. Typefullyのダッシュボードが表示されたらサインアップ完了です\n\nサインアップできましたか？",
    "options": [
      {"id": "signed_up", "label": "サインアップ / ログインできました！"},
      {"id": "already_account", "label": "すでにアカウントを持っています"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "x_auth_issue", "label": "Xアカウントでの認証がうまくいかない"}
    ]
  }]
}
```

(signed_up → Step 2へ)
(already_account → Step 2へ)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://typefully.com」と案内)
(x_auth_issue → 「Xアカウントでの認証がブロックされる場合は、X側のプライバシー設定でサードパーティアプリの連携を許可してください。X → 設定 → セキュリティとアカウントアクセス → アプリとセッション で確認できます」と案内)

---

## Chrome 統合で自動化する場合（`/chrome` モード）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://typefully.com を開く
2. Chrome 統合を使って以下の操作を順番に実行する:
   - 「Get started free」をクリック
   - 「Sign up with X (Twitter)」で認証（ユーザーの操作を待つ）
   - ログイン後、https://typefully.com/settings/api に移動
   - 「Generate API Key」または「Create API Key」をクリック
3. APIキーが表示されたことを確認したら、ユーザーに「APIキーをコピーしてください」と案内する
4. Step 3 に進む

**注意:** APIキーの値はブラウザ画面から読み取らないこと。ユーザーが手動でコピーする。

Chrome 統合が利用できない場合は、以下の手順を手動で実行してください。

---

## Step 2: APIキーを取得する

**AIが実行すること:**
1. 以下のコマンドを実行してブラウザでAPI設定ページを開く:

```bash
# Mac:
open https://typefully.com/settings/api
# Windows:
start https://typefully.com/settings/api
# Linux:
xdg-open https://typefully.com/settings/api
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 2: APIキーを取得",
  "questions": [{
    "id": "api_key_status",
    "prompt": "API設定ページが開きましたか？以下の手順でAPIキーを取得してください:\n\n1. Typefully の Settings > API ページを確認\n2. APIキーが表示されている場合はそのままコピー\n3. 新規作成が必要な場合は「Generate API Key」をクリック\n4. 表示されたAPIキーをコピーしてください\n\nAPIキーをコピーできましたか？",
    "options": [
      {"id": "copied", "label": "APIキーをコピーしました！"},
      {"id": "page_not_found", "label": "API設定ページが見つからない"},
      {"id": "no_api_key", "label": "APIキーが表示されない"},
      {"id": "paid_plan_required", "label": "有料プランが必要と表示される"}
    ]
  }]
}
```

(copied → Step 3へ)
(page_not_found → 「ブラウザで直接このURLを開いてください: https://typefully.com/settings/api　ログイン状態であれば設定ページが表示されます」と案内)
(no_api_key → 「ページ内に「Generate API Key」や「Create API Key」ボタンがないか確認してください。見つからない場合はページをリロードしてみてください」と案内)
(paid_plan_required → 「APIアクセスには有料プランが必要な場合があります。無料プランでAPIが利用できない場合はこのセットアップをスキップしても問題ありません」と案内)

---

## Step 3: APIキーを安全に保存する

**セキュリティに関する重要な注意:**
APIキーはこのチャットに貼り付けないでください。別のターミナルウィンドウで安全に保存します。

**AIが自動で実行すること:**
1. `keyring` パッケージがインストール済みか確認する
   - 未インストールの場合: `uv add keyring` を自動実行する
2. `uv run python tools/credential_manager.py status` を実行して現在の状態を確認する

**ユーザーに案内するメッセージ:**

```text
APIキーをコピーしたら、以下の手順で安全に保存してください:

┌─────────────────────────────────────────────────────────────┐
│ 別のターミナルウィンドウで以下のコマンドを実行してください: │
│                                                             │
│ Cursor: Ctrl+` (バッククォート) で新しいターミナルを開く    │
│ Claude Code: 別のターミナルウィンドウを開く                 │
│                                                             │
│ uv run python tools/credential_manager.py store TYPEFULLY_API_KEY  │
│                                                             │
│ → 「Enter value for TYPEFULLY_API_KEY:」と表示されます      │
│ → コピーしたAPIキーを貼り付けてEnterを押してください        │
│   （入力した文字は画面に表示されません。これは正常です）    │
│ → 「✅ Stored TYPEFULLY_API_KEY」と表示されたら保存完了です │
└─────────────────────────────────────────────────────────────┘

保存が完了したら、こちらのチャットに戻って「完了」と教えてください。
```

**⚠️ なぜ別ウィンドウで実行するのか:**
AIのチャットでAPIキーを扱うと、会話ログに値が残ってしまいます。
別ウィンドウで `credential_manager.py` を実行すれば、キーの値はOSの
暗号化ストレージ（macOS Keychain / Windows Credential Locker / Linux SecretService）に
直接保存され、平文ファイルやチャットログに一切残りません。

**AskQuestionの設定:**
```json
{
  "title": "Step 3: APIキーの保存",
  "questions": [{
    "id": "store_status",
    "prompt": "別のターミナルでコマンドを実行できましたか？",
    "options": [
      {"id": "done", "label": "保存しました！"},
      {"id": "terminal_help", "label": "ターミナルの開き方がわからない"},
      {"id": "command_error", "label": "コマンドでエラーが出た"},
      {"id": "security_question", "label": "セキュリティについて質問がある"}
    ]
  }]
}
```

(done → Step 4へ)
(terminal_help → 「Cursorの場合: 画面上部のメニュー > Terminal > New Terminal、またはキーボードの Ctrl+バッククォート (Macの場合は Cmd+バッククォート) を押してください。Claude Codeの場合: 別のターミナルウィンドウ/タブを開いてください。Mac: Cmd+T (新しいタブ) または Cmd+N (新しいウィンドウ)。Windows: WSL ターミナル（Ubuntu）を開くか、Windows Terminal で Ubuntu タブを追加してください。開いたら cd でプロジェクトのディレクトリに移動してください」と案内)
(command_error → AIが `uv run python tools/credential_manager.py status` を実行して状況を確認し、原因を特定。keyring 未インストールの場合は `uv add keyring` を自動実行)
(security_question → 「このツールはOS標準の暗号化ストレージを使います。macOSではKeychain、WindowsではCredential Locker、LinuxではSecretService (GNOME Keyring等) に保存されます。平文のファイル(.env)は一切作成しません。画面ロック中はストレージもロックされるため、物理的なアクセスからも保護されます」と説明)

---

## Step 4: 設定テスト

**AIが自動で実行すること:**

1. まず `credential_manager.py status` を実行して、`TYPEFULLY_API_KEY` が Credential Store に保存されているか確認する:
   - **注意**: APIキーの値そのものをチャットに表示しないこと。「APIキーが設定されていることを確認しました（先頭4文字: xxxx...）」のようにマスク表示のみ
   - ステータス確認コマンド: `uv run python tools/credential_manager.py status`

2. 簡易チェックに通ったら、実際にTypefully APIにテストリクエストを送信する:
   - Credential Store から環境変数に注入してAPI呼び出しを実行する
   - テストコード例:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("TYPEFULLY_API_KEY")
     if not key:
         print("エラー: TYPEFULLY_API_KEY が設定されていません。")
         sys.exit(1)
     resp = requests.get("https://api.typefully.com/v2/me",
         headers={"Authorization": f"Bearer {key}"})
     if resp.status_code == 200:
         print("接続成功！ Typefully APIにアクセスできました。")
     else:
         print(f"エラー: {resp.status_code}")
         print("詳細は再認証・APIキー再生成・権限設定を確認してください。")
     ```
   - 必要なパッケージ（`requests`, `keyring`）がインストールされていない場合は自動でインストールする

3. テスト結果に応じてAskQuestionを表示:

**テスト成功時:**
```text
Typefully APIの設定が完了しました！

テスト結果: APIからの応答を正常に受信しました。
これでSNS投稿のスケジューリング・管理機能が使えるようになりました。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "APIテストでエラーが発生しました。考えられる原因を確認しましょう。",
    "options": [
      {"id": "retry", "label": "もう一度テストする"},
      {"id": "recheck_key", "label": "APIキーを確認し直す（Step 2に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行)
(recheck_key → Step 2に戻る)
(show_error → エラーメッセージを表示して原因と解決方法を案内)
(skip_test → 「APIテストはスキップしました。後で /check-setup で確認できます」と案内)

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
      {"id": "trouble_x_auth", "label": "Xアカウントでの連携がうまくいかない"},
      {"id": "trouble_invalid", "label": "「Invalid API key」や「Unauthorized」エラーが出る"},
      {"id": "trouble_not_found", "label": "APIキーの取得ページが見つからない"},
      {"id": "trouble_cost", "label": "料金が心配"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: Xアカウントでの連携がうまくいかない
**原因**: X側のプライバシー設定でサードパーティアプリの連携がブロックされている
**AIが行うこと**:
1. 「X (Twitter) → 設定 → セキュリティとアカウントアクセス → アプリとセッション でサードパーティアプリの連携を許可してください」と案内
2. それでも解決しない場合は「ブラウザのCookieをクリアしてから再度試してください」と案内
3. Xアカウントが凍結・制限されていないか確認を促す

### トラブル2: 「Invalid API key」や「Unauthorized」エラー
**原因**: APIキーが正しくコピーされていない、またはキーが無効
**AIが行うこと**:
1. `credential_manager.py status` で `TYPEFULLY_API_KEY` の保存状態を確認（値はマスク表示のみ）
2. Credential Store に保存されていない場合は再登録を案内
3. 保存済みの場合はAPIテストを再実行。失敗すれば「Typefullyの設定ページ (https://typefully.com/settings/api) でキーを再作成してください」と案内

### トラブル3: APIキーの取得ページが見つからない
**原因**: ログインしていない、またはURLが変更された
**AIの案内**: 「まずTypefullyにログインしてから https://typefully.com/settings/api にアクセスしてください。ページが見つからない場合は、ダッシュボード右上のアイコン → Settings → API の順にアクセスしてください」

### トラブル4: 料金が心配
**AIの案内**: 「Typefullyには無料プランがあります。無料プランでも基本的なAPIアクセスが可能です。有料プランは$12.5/月〜で、より多くの機能（スケジューリング、分析など）が使えます。研修レベルの利用であれば無料プランで十分です」

### トラブル5: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] Typefully にX (Twitter) アカウントでサインアップした
- [ ] API設定ページ (Settings > API) でAPIキーを取得した
- [ ] credential_manager.py store で Credential Store に保存した
- [ ] credential_manager.py status で保存を確認した
- [ ] APIテストが成功した（Typefully APIからの応答を受信できた）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "Typefully APIのセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "try_marketing", "label": "マーケティング系レッスンを始める（/start-12-1）"},
      {"id": "setup_other", "label": "他のAPIもセットアップする（/start-0-1）"},
      {"id": "try_banner", "label": "バナーを作ってみる（/start-1-1）"},
      {"id": "back_to_setup", "label": "セットアップ一覧に戻る（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- try_marketing → /start-12-1 を案内
- setup_other → /start-0-1 を案内
- try_banner → /start-1-1 を案内
- back_to_setup → /start-0-1 を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-typefully` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「マーケティング系レッスン（/start-12-1）でSNS投稿の作成・スケジューリングを実践できます」

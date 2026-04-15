---
description: "Lesson command"
duration: "約15分"
prerequisites: ["Slack ワークスペースの管理者権限"]
level: "beginner"
tags: ["setup", "slack", "api"]
---

# Slack API セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-slack` を実行して進捗を表示
2. **このステップは任意です。** Slack連携を使わない場合はスキップできます
3. 既存トークンを自動検出:
   - `.env` や credential store に `SLACK_USER_TOKEN` が存在するか確認
   - 存在する場合、Slack API `auth.test` で有効性を確認。有効なら「Slack設定は完了しています。スキップしますか？」と確認
4. スキップする場合: `uv run python tools/setup_progress.py skip setup-slack --reason 'ユーザーがスキップ'` を実行

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Slack Appを作成し、User Tokenを取得して安全に保存し、Slack検索・メッセージ取得機能を使えるようにする |
| 所要時間 | 約15分 |
| 前提条件 | Slackワークスペースの管理者権限（またはApp追加の許可）、ブラウザが使えること |
| 操作レベル | CLIコマンド入力なし（すべてAIが自動実行 + GUI操作のみ） |

**このセッションの流れ:**
1. Slack App管理画面を開く（AIが自動でブラウザを起動）
2. 新しいSlack Appを作成する（画面上のボタンをクリック）
3. User Token Scopesを設定する（必要な権限を追加）
4. ワークスペースにインストールする（許可ボタンをクリック）
5. User Tokenを安全に保存する（credential_managerを使用）
6. 動作テスト（AIが自動実行）

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
      {"id": "no_slack", "label": "Slackワークスペースを持っていない"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(chrome → Step 1 でブラウザを開いた後、「Chrome 統合で自動化する場合」セクションの手順で自動実行する)
(check_prereq → 「Slackワークスペースにログイン済みで、App追加の権限があれば準備OKです。権限がない場合はワークスペース管理者に確認してください」と案内)
(no_slack → 「Slackは無料で作成できます。https://slack.com/create からテスト用ワークスペースを作成してから、このセットアップを再開してください」と案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: Slack App管理画面を開く

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://api.slack.com/apps
# Windows:
start https://api.slack.com/apps
# Linux:
xdg-open https://api.slack.com/apps
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 1: Slack App を作成する",
  "questions": [{
    "id": "app_create",
    "prompt": "ブラウザでSlack App管理画面が開きました。以下の手順で新しいAppを作成してください:\n\n1. 右上の「Create New App」ボタンをクリック\n2. 「From scratch」を選択\n3. App Name に「AIAgent Bootcamp」と入力\n4. Pick a workspace で自分のワークスペースを選択\n5. 「Create App」ボタンをクリック\n\nAppを作成できましたか？",
    "options": [
      {"id": "created", "label": "Appを作成しました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "no_create_button", "label": "「Create New App」ボタンが見つからない"},
      {"id": "no_workspace", "label": "ワークスペースが表示されない"},
      {"id": "permission_error", "label": "権限エラーが表示された"}
    ]
  }]
}
```

(created → Step 2へ)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://api.slack.com/apps」と案内)
(no_create_button → 「Slackにログインしていない可能性があります。まず右上の 'Sign in' からSlackアカウントでログインしてください」と案内)
(no_workspace → 「ワークスペースにログインした状態でページを再読み込みしてください。それでも表示されない場合は、新しいワークスペースを作成する必要があるかもしれません」と案内)
(permission_error → 「ワークスペースの管理者がApp追加を制限している可能性があります。管理者に『AIAgent Bootcamp という Slack App を追加したい』と依頼してください。または、テスト用の無料ワークスペースを https://slack.com/create から作成してください」と案内)

---

## Chrome 統合で自動化する場合（`/chrome` モード）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://api.slack.com/apps を開く
2. Chrome 統合を使って以下の操作を順番に実行する:
   - 「Create New App」ボタンをクリック
   - 「From scratch」を選択
   - App Name に「AIAgent Bootcamp」と入力
   - 「Pick a workspace」でワークスペースを選択
   - 「Create App」をクリック
   - 左メニューの「OAuth & Permissions」をクリック
   - 「User Token Scopes」セクションで「Add an OAuth Scope」をクリックし、以下の4つを1つずつ追加: channels:history, channels:read, chat:write, users:read
   - ページ上部の「Install to Workspace」をクリック
   - 権限確認画面で「Allow」をクリック
3. User OAuth Token（xoxp-...）が表示されたことを確認したら、ユーザーに「トークンの横のCopyボタンをクリックしてコピーしてください」と案内する
4. Step 4 に進む

**注意:** トークンの値はブラウザ画面から読み取らないこと。ユーザーが手動でコピーする。

Chrome 統合が利用できない場合は、以下の Step 2〜3 の手順を手動で実行してください。

---

## Step 2: User Token Scopes を設定する

**AskQuestionの設定:**
```json
{
  "title": "Step 2: User Token Scopes を設定する",
  "questions": [{
    "id": "scope_setup",
    "prompt": "Appの設定画面が表示されています。以下の手順でUser Token Scopesを設定してください:\n\n1. 左メニューの「OAuth & Permissions」をクリック\n2. 下にスクロールして「Scopes」セクションを見つける\n3. 「User Token Scopes」の「Add an OAuth Scope」をクリック\n4. 以下の4つのスコープを1つずつ追加する:\n\n   - channels:history（チャンネルのメッセージを読み取る）\n   - channels:read（チャンネル情報を読み取る）\n   - chat:write（メッセージを送信する）\n   - users:read（ユーザー情報を読み取る）\n\n4つのスコープを追加できましたか？",
    "options": [
      {"id": "scopes_added", "label": "4つのスコープを追加しました！"},
      {"id": "cant_find_oauth", "label": "「OAuth & Permissions」が見つからない"},
      {"id": "cant_find_scopes", "label": "「User Token Scopes」が見つからない"},
      {"id": "scope_not_found", "label": "追加したいスコープが候補に出てこない"},
      {"id": "what_are_scopes", "label": "スコープって何？"}
    ]
  }]
}
```

(scopes_added → Step 3へ)
(cant_find_oauth → 「左側のサイドバーメニューを確認してください。「Features」セクションの下に「OAuth & Permissions」があります。サイドバーが見えない場合は、ブラウザの画面を横に広げてみてください」と案内)
(cant_find_scopes → 「ページを下にスクロールしてください。「OAuth Tokens for Your Workspace」セクションの下に「Scopes」セクションがあります。その中の「User Token Scopes」が対象です。※「Bot Token Scopes」ではないので注意してください」と案内)
(scope_not_found → 「スコープ名を正確に入力してください。入力欄にテキストを打つと候補がフィルタされます。例えば 'channels' と入力すると channels:history や channels:read が候補に表示されます」と案内)
(what_are_scopes → 「スコープとは、Appに許可する操作範囲のことです。今回追加する4つは:\n- channels:history = チャンネルの過去メッセージを読む権限\n- channels:read = チャンネル一覧を見る権限\n- chat:write = Appとしてメッセージを投稿する権限\n- users:read = ワークスペースのメンバー情報を見る権限\nこれらはSlack検索やタスク管理機能に必要な最小限の権限です」と説明)

---

## Step 3: ワークスペースにインストールする

**AskQuestionの設定:**
```json
{
  "title": "Step 3: ワークスペースにインストール",
  "questions": [{
    "id": "install_app",
    "prompt": "スコープの設定が完了したら、Appをワークスペースにインストールします:\n\n1. ページを上にスクロールして「OAuth Tokens for Your Workspace」セクションを見つける\n2. 「Install to Workspace」ボタンをクリック\n   （ボタンが「Reinstall to Workspace」の場合もクリックしてOK）\n3. 権限の確認画面で「Allow」（許可）をクリック\n4. 「User OAuth Token」が表示される（xoxp- で始まる文字列）\n5. トークンの右にある「Copy」ボタンをクリックしてコピー\n\nUser OAuth Token をコピーできましたか？",
    "options": [
      {"id": "token_copied", "label": "トークンをコピーしました！"},
      {"id": "no_install_button", "label": "「Install to Workspace」ボタンがない"},
      {"id": "allow_denied", "label": "「Allow」画面で拒否された"},
      {"id": "no_token", "label": "トークンが表示されない"}
    ]
  }]
}
```

(token_copied → Step 4へ)
(no_install_button → 「User Token Scopes が1つも追加されていないと Install ボタンが表示されません。Step 2 に戻って、少なくとも1つのスコープを追加してください」と案内)
(allow_denied → 「ワークスペースの管理者がApp追加を制限している可能性があります。管理者に承認を依頼するか、テスト用の自分専用ワークスペースを作成してください」と案内)
(no_token → 「インストールが正常に完了していれば、『OAuth & Permissions』ページの上部に『User OAuth Token』が表示されます。ページを再読み込みして、上部を確認してください」と案内)

---

## Step 4: トークンを安全に保存

**セキュリティに関する重要な注意:**
トークンはこのチャットに貼り付けないでください。別のターミナルウィンドウで安全に保存します。

**AIが自動で実行すること:**
1. `keyring` パッケージがインストール済みか確認する
   - 未インストールの場合: `pip install keyring` を自動実行する
2. `uv run python tools/credential_manager.py status` を実行して現在の状態を確認する

**ユーザーに案内するメッセージ:**

```text
トークンをコピーしたら、以下の手順で安全に保存してください:

┌─────────────────────────────────────────────────────────────┐
│ 別のターミナルウィンドウで以下のコマンドを実行してください: │
│                                                             │
│ Cursor: Ctrl+` (バッククォート) で新しいターミナルを開く    │
│ Claude Code: 別のターミナルウィンドウを開く                 │
│                                                             │
│ uv run python tools/credential_manager.py store SLACK_USER_TOKEN    │
│                                                             │
│ → 「Enter value for SLACK_USER_TOKEN:」と表示されます        │
│ → コピーしたUser Tokenを貼り付けてEnterを押してください      │
│   （入力した文字は画面に表示されません。これは正常です）    │
│ → 「Stored SLACK_USER_TOKEN」と表示されたら保存完了です      │
└─────────────────────────────────────────────────────────────┘

保存が完了したら、こちらのチャットに戻って「完了」と教えてください。
```

**なぜ別ウィンドウで実行するのか:**
AIのチャットでトークンを扱うと、会話ログに値が残ってしまいます。
別ウィンドウで `credential_manager.py` を実行すれば、トークンの値はOSの
暗号化ストレージ（macOS Keychain / Windows Credential Locker / Linux SecretService）に
直接保存され、平文ファイルやチャットログに一切残りません。

**AskQuestionの設定:**
```json
{
  "title": "Step 4: トークンの保存",
  "questions": [{
    "id": "store_status",
    "prompt": "別のターミナルでコマンドを実行できましたか？",
    "options": [
      {"id": "done", "label": "保存しました！"},
      {"id": "terminal_help", "label": "ターミナルの開き方がわからない"},
      {"id": "command_error", "label": "コマンドでエラーが出た"},
      {"id": "credential_store_unavailable", "label": "Credential Storeが利用できない（例外対応）"},
      {"id": "security_question", "label": "セキュリティについて質問がある"}
    ]
  }]
}
```

(done → Step 5へ)
(terminal_help → 「Cursorの場合: 画面上部のメニュー > Terminal > New Terminal、またはキーボードの Ctrl+\` (Macの場合は Cmd+\`) を押してください。Claude Codeの場合: 別のターミナルウィンドウ/タブを開いてください。Mac: Cmd+T (新しいタブ) または Cmd+N (新しいウィンドウ)。Windows: WSL ターミナル（Ubuntu）を開くか、Windows Terminal で Ubuntu タブを追加してください。開いたら cd でプロジェクトのディレクトリに移動してください」と案内)
(command_error → AIが `uv run python tools/credential_manager.py status` を実行して状況を確認し、原因を特定。keyring 未インストールの場合は `pip install keyring` を自動実行)
(credential_store_unavailable → 「まず `uv run python tools/credential_manager.py status` でストアの状態を確認します」と案内し、本当に利用不可の場合のみ例外対応として .env フォールバックを案内。その際、別ターミナルで .env ファイルにトークンを直接入力する手順を案内し、「.envファイルが.gitignoreに含まれていることを確認してください。Credential Store が利用可能になったら `uv run python tools/credential_manager.py migrate` で移行し、`uv run python tools/credential_manager.py cleanup` で .env の平文トークンを削除してください」と注意喚起)
(security_question → 「このツールはOS標準の暗号化ストレージを使います。macOSではKeychain、WindowsではCredential Locker、LinuxではSecretService (GNOME Keyring等) に保存されます。平文のファイル(.env)は一切作成しません。画面ロック中はストレージもロックされるため、物理的なアクセスからも保護されます」と説明)

---

## Step 5: 設定テスト

**AIが自動で実行すること:**

1. まず `credential_manager.py status` を実行して、`SLACK_USER_TOKEN` が Credential Store に保存されているか確認する:
   - **注意**: トークンの値そのものをチャットに表示しないこと。「トークンが設定されていることを確認しました（xoxp-****...）」のようにマスク表示のみ
   - ステータス確認コマンド: `uv run python tools/credential_manager.py status`

2. 簡易チェックに通ったら、実際にSlack APIにテストリクエストを送信する:
   - Credential Store から環境変数に注入してAPI呼び出しを実行する
   - テストコード例:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     token = os.getenv("SLACK_USER_TOKEN")
     if not token or token == "xoxp-your-user-token":
         print("エラー: SLACK_USER_TOKEN が設定されていません。")
         sys.exit(1)
     resp = requests.post(
         "https://slack.com/api/auth.test",
         headers={"Authorization": f"Bearer {token}"}
     ).json()
     if resp.get("ok"):
         print(f"接続成功！ ワークスペース: {resp['team']} / Bot名: {resp['user']}")
     else:
         print(f"エラー: {resp.get('error', '不明なエラー')}")
     ```
   - 必要なパッケージ（`requests`, `keyring`）がインストールされていない場合は自動でインストールする

3. テスト結果に応じてメッセージを表示:

**テスト成功時:**
```text
Slack APIの設定が完了しました！

テスト結果:
  ワークスペース: [ワークスペース名]
  Bot名: [Bot名]
  接続: 正常

これでSlack検索（/start-9-1）やSlackタスク管理（/start-9-2）が使えるようになりました。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "Slack APIテストでエラーが発生しました。考えられる原因を確認しましょう。",
    "options": [
      {"id": "retry", "label": "もう一度テストする"},
      {"id": "recheck_token", "label": "トークンを確認し直す（Step 3に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行)
(recheck_token → Step 3に戻る)
(show_error → エラーメッセージを表示して原因と解決方法を案内。よくあるエラー: `invalid_auth` = トークンが無効、`token_revoked` = トークンが取り消された、`not_authed` = トークンが未設定)
(skip_test → 「APIテストはスキップしました。後で /check-setup で確認できます」と案内)

---

## 補足: Botをチャンネルに招待する

**テスト成功後、AIが以下を案内する:**

Slack Appがメッセージを読み取るには、対象チャンネルにBotを招待する必要があります。

**手順（Slackアプリ上で操作）:**
1. Slackアプリを開く
2. メッセージを読み取りたいチャンネルに移動する
3. チャンネル名をクリックして設定を開く
4. 「インテグレーション」タブをクリック
5. 「アプリを追加する」をクリック
6. 「AIAgent Bootcamp」を選択して追加する

または、チャンネル内で `/invite @AIAgent Bootcamp` とメッセージを送信してもOKです。

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
      {"id": "trouble_invalid", "label": "「invalid_auth」エラーが出る"},
      {"id": "trouble_missing_scope", "label": "「missing_scope」エラーが出る"},
      {"id": "trouble_not_in_channel", "label": "「not_in_channel」エラーが出る"},
      {"id": "trouble_admin", "label": "管理者の承認が必要と言われた"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: 「invalid_auth」エラー
**原因**: User Tokenが正しくコピーされていない、または無効
**AIが行うこと**:
1. `uv run python tools/credential_manager.py status` で Credential Store の状態を確認（値は表示せず、`xoxp-` で始まっているかのみ報告）
2. 余分なスペース・改行・クォーテーションが含まれていないか自動チェック
3. 問題が見つかれば再保存を提案。見つからなければ「Slack App設定画面でトークンを再生成してください」と案内

### トラブル2: 「missing_scope」エラー
**原因**: 必要なUser Token Scopeが追加されていない
**AIの案内**: 「Slack App設定画面の『OAuth & Permissions』→『User Token Scopes』で、以下のスコープが全て追加されているか確認してください: channels:history, channels:read, chat:write, users:read。スコープを追加したら『Reinstall to Workspace』をクリックして再インストールが必要です」

### トラブル3: 「not_in_channel」エラー
**原因**: Botが対象チャンネルに招待されていない
**AIの案内**: 「Slackアプリで対象チャンネルを開き、チャンネル名をクリック → 『インテグレーション』→『アプリを追加する』で『AIAgent Bootcamp』を追加してください」

### トラブル4: 管理者の承認が必要
**原因**: ワークスペースの設定でApp追加が制限されている
**AIの案内**: 「ワークスペースの管理者にSlack App追加の承認を依頼してください。急ぎの場合は、テスト用の無料ワークスペースを https://slack.com/create から作成して練習できます」

### トラブル5: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、Slack API のエラーコード一覧と照合して原因と解決方法を案内する

---

## チェックポイント
- [ ] Slack App「AIAgent Bootcamp」を作成した
- [ ] User Token Scopes に4つのスコープ（channels:history, channels:read, chat:write, users:read）を追加した
- [ ] ワークスペースにAppをインストールした
- [ ] SLACK_USER_TOKEN が Credential Store に保存されている（`uv run python tools/credential_manager.py status` で確認）
- [ ] APIテストが成功した（ワークスペース名とBot名が表示された）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "Slack APIのセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "setup_gemini", "label": "Gemini APIもセットアップする（/setup-gemini）"},
      {"id": "try_slack_search", "label": "Slack検索を試してみる（/start-9-1）"},
      {"id": "try_slack_task", "label": "Slackタスク管理を試してみる（/start-9-2）"},
      {"id": "back_to_setup", "label": "セットアップ一覧に戻る"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- setup_gemini → /setup-gemini を案内
- try_slack_search → /start-9-1 を案内
- try_slack_task → /start-9-2 を案内
- back_to_setup → セットアップ系レッスン一覧を表示
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-slack` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/setup-extensions` で拡張機能をインストールしましょう」

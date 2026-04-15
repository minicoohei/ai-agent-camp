---
description: "Lesson command"
duration: "約10分"
prerequisites: ["Googleアカウントを持っている", "ブラウザが使える"]
level: "beginner"
tags: ["setup", "gemini", "api"]
---

# Gemini API セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-gemini` を実行して進捗を表示
2. 既存のAPIキーを自動検出:
   - `uv run python tools/credential_manager.py status` を実行
   - GEMINI_API_KEY が設定済みの場合、Step 3（APIテスト）のみ実行して完了にできる
   - `.env` に平文で存在する場合、credential store への移行を提案

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Google AI Studio で Gemini API キーを取得し、.env に設定して画像生成などのAI機能を使えるようにする |
| 所要時間 | 約10分 |
| 前提条件 | Googleアカウントを持っていること、ブラウザが使えること |
| 操作レベル | CLIコマンド入力なし（すべてAIが自動実行 + GUI操作のみ） |

**このセッションの流れ:**
1. ブラウザでGoogle AI Studioを開く（AIが自動でブラウザを起動）
2. APIキーを取得する（画面上のボタンをクリックするだけ）
3. .envファイルを準備する（AIが自動作成）
4. APIキーを.envファイルに入力する（ファイルを開いて貼り付け）
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
(chrome → Step 1 でブラウザを開いた後、「Chrome 統合で自動化する場合」セクションの手順で自動実行する)
(check_prereq → 「Googleアカウントでブラウザにログインできれば準備OKです」と案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: ブラウザでGoogle AI Studioを開く

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://aistudio.google.com/apikey
# Windows:
start https://aistudio.google.com/apikey
# Linux:
xdg-open https://aistudio.google.com/apikey
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 1: ブラウザでAPIキーを取得",
  "questions": [{
    "id": "browser_status",
    "prompt": "ブラウザが開きましたか？以下の手順でAPIキーを取得してください:\n\n1. Googleアカウントでログインする\n2. 「Get API key」ボタンをクリック\n3. 「Create API key」をクリック\n4. 表示されたAPIキーの右にある「コピーボタン」をクリック\n\nAPIキーをコピーできましたか？",
    "options": [
      {"id": "copied", "label": "APIキーをコピーしました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "no_button", "label": "「Get API key」ボタンが見つからない"},
      {"id": "login_issue", "label": "Googleアカウントにログインできない"}
    ]
  }]
}
```

(copied → Step 2へ)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://aistudio.google.com/apikey」と案内)
(no_button → 「ページが完全に読み込まれるまで待ってください。それでも表示されない場合は、ページ上部の "Get API key" タブをクリックしてください」と案内)
(login_issue → 「Google AI Studioにはgmail.comまたはGoogle Workspaceのアカウントが必要です。会社のアカウントでログインしてみてください」と案内)

---

## Chrome 統合で自動化する場合（`/chrome` モード）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://aistudio.google.com/apikey を開く
2. Chrome 統合を使って以下の操作を順番に実行する:
   - Googleアカウントへのログインが必要な場合はユーザーの操作を待つ
   - 「Get API key」または「APIキーを取得」ボタンをクリック
   - 「Create API key」または「APIキーを作成」ボタンをクリック
   - プロジェクト選択画面が出たら、デフォルトのプロジェクトを選んで「Create API key in existing project」をクリック
3. APIキーが画面に表示されたことを確認したら、ユーザーに「コピーボタンをクリックしてAPIキーをコピーしてください」と案内する
4. Step 2 に進む

**注意:** APIキーの値はブラウザ画面から読み取らないこと。ユーザーが手動でコピーする。

Chrome 統合が利用できない場合は、Step 1 の手順を手動で実行してください。

---

## Step 2: APIキーを安全に保存する

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
│ uv run python tools/credential_manager.py store GEMINI_API_KEY     │
│                                                             │
│ → 「Enter value for GEMINI_API_KEY:」と表示されます         │
│ → コピーしたAPIキーを貼り付けてEnterを押してください        │
│   （入力した文字は画面に表示されません。これは正常です）    │
│ → 「✅ Stored GEMINI_API_KEY」と表示されたら保存完了です    │
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
  "title": "Step 2: APIキーの保存",
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

(done → Step 3へ)
(terminal_help → 「Cursorの場合: 画面上部のメニュー > Terminal > New Terminal、またはキーボードの Ctrl+` (Macの場合は ⌘+`) を押してください。Claude Codeの場合: 別のターミナルウィンドウ/タブを開いてください。Mac: Cmd+T (新しいタブ) または Cmd+N (新しいウィンドウ)。Windows: WSL ターミナル（Ubuntu）を開くか、Windows Terminal で Ubuntu タブを追加してください。開いたら cd でプロジェクトのディレクトリに移動してください」と案内)
(command_error → AIが `uv run python tools/credential_manager.py status` を実行して状況を確認し、原因を特定。keyring 未インストールの場合は `uv add keyring` を自動実行)
(security_question → 「このツールはOS標準の暗号化ストレージを使います。macOSではKeychain、WindowsではCredential Locker、LinuxではSecretService (GNOME Keyring等) に保存されます。平文のファイル(.env)は一切作成しません。画面ロック中はストレージもロックされるため、物理的なアクセスからも保護されます」と説明)

---

## Step 3: 設定テスト

**AIが自動で実行すること:**

1. まず `credential_manager.py status` を実行して、`GEMINI_API_KEY` が Credential Store に保存されているか確認する:
   - **注意**: APIキーの値そのものをチャットに表示しないこと。「APIキーが設定されていることを確認しました（先頭4文字: AIza...）」のようにマスク表示のみ
   - ステータス確認コマンド: `uv run python tools/credential_manager.py status`

2. 簡易チェックに通ったら、実際にGemini APIにテストリクエストを送信する:
   - Credential Store から環境変数に注入してAPI呼び出しを実行する
   - テストコード例:
     ```python
     import os
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     from dotenv import load_dotenv
     load_dotenv()
     from google import genai
     client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
     response = client.models.generate_content(
         model="gemini-2.5-flash",
         contents="こんにちは！一言で挨拶してください。"
     )
     print("API応答:", response.text)
     ```
   - 必要なパッケージ（`google-genai`, `keyring`）がインストールされていない場合は自動でインストールする

3. テスト結果に応じてAskQuestionを表示:

**テスト成功時:**
```text
Gemini APIの設定が完了しました！

テスト結果: APIからの応答を正常に受信しました。
これで画像生成（/banner）、図表作成（/diagram）などのAI機能が使えるようになりました。
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
      {"id": "recheck_key", "label": "APIキーを確認し直す（Step 1に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行)
(recheck_key → Step 1に戻る)
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
      {"id": "trouble_invalid", "label": "「Invalid API key」エラーが出る"},
      {"id": "trouble_quota", "label": "「Quota exceeded」エラーが出る"},
      {"id": "trouble_package", "label": "Pythonパッケージのエラーが出る"},
      {"id": "trouble_cost", "label": "料金が心配"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: 「Invalid API key」エラー
**原因**: APIキーが正しくコピーされていない、またはキーが無効
**AIが行うこと**:
1. `credential_manager.py status` で `GEMINI_API_KEY` の保存状態を確認（値はマスク表示のみ）
2. Credential Store に保存されていない場合は再登録を案内
3. 保存済みの場合はAPIテストを再実行。失敗すれば「Google AI Studioでキーを再作成してください」と案内

### トラブル2: 「Quota exceeded」エラー
**原因**: 無料枠の制限に達した
**AIの案内**: 「Gemini APIの無料枠は1分あたり15リクエスト、1日あたり1,500リクエストです。数分待ってから再度お試しください。研修での利用であれば無料枠で十分です」

### トラブル3: Pythonパッケージのエラー
**原因**: 必要なパッケージがインストールされていない
**AIが行うこと**: 不足パッケージを自動でインストールする（`uv add google-genai python-dotenv`）

### トラブル4: 料金が心配
**AIの案内**: 「Gemini APIには無料枠があります。無料枠の範囲内であれば費用は一切かかりません。研修レベルの利用（1日数十回の生成）であれば無料枠で十分です。有料になる前にGoogleから通知が届きます」

### トラブル5: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] Google AI StudioでAPIキーを取得した
- [ ] credential_manager.py store で Credential Store に保存した
- [ ] credential_manager.py status で保存を確認した
- [ ] APIテストが成功した（Gemini APIからの応答を受信できた）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "Gemini APIのセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "setup_slack", "label": "Slack APIもセットアップする（/setup-slack）"},
      {"id": "try_banner", "label": "さっそくバナーを作ってみる（/start-1-1）"},
      {"id": "try_diagram", "label": "図表を作ってみる（/start-2-1）"},
      {"id": "back_to_setup", "label": "セットアップ一覧に戻る（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- setup_slack → /setup-slack を案内
- try_banner → /start-1-1 を案内
- try_diagram → /start-2-1 を案内
- back_to_setup → /start-0-1 を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-gemini` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/setup-slack` でSlack APIを設定しましょう（スキップ可能）」

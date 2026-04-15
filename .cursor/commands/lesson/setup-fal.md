---
description: "Lesson command"
duration: "約10分"
prerequisites: ["ブラウザが使える", "GitHub または Google アカウントを持っている"]
level: "beginner"
tags: ["setup", "fal", "api", "video", "image"]
---

# fal.ai API セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-fal` を実行して進捗を表示
2. 既存のAPIキーを自動検出:
   - `uv run python tools/credential_manager.py status` を実行
   - FAL_KEY が設定済みの場合、Step 4（テスト）のみ実行して完了にできる
   - `.env` に平文で存在する場合、credential store への移行を提案

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | fal.ai でAPIキーを取得し、Credential Store に保存して動画・画像生成などのAI機能を使えるようにする |
| 所要時間 | 約10分 |
| 前提条件 | GitHub または Google アカウントを持っていること、ブラウザが使えること |
| 操作レベル | 基本はAI自動実行（APIキー保存時のみ、別ターミナルで手動1コマンド） |

**fal.ai とは:**
動画生成(Kling, Veo等)、画像生成、リップシンク(Fabric)、音楽生成(Suno)などのAIエンジンを統合的に利用できるプラットフォームです。1つのAPIキーで複数のAIモデルにアクセスできます。

**このセッションの流れ:**
1. ブラウザで fal.ai を開く（AIが自動でブラウザを起動）
2. アカウントを作成してAPIキーを取得する（画面上のボタンをクリックするだけ）
3. APIキーを Credential Store に安全に保存する（別ターミナルでコマンド実行）
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
(check_prereq → 「GitHubアカウントまたはGoogleアカウントがあればサインアップできます。ブラウザでログインできれば準備OKです」と案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: ブラウザで fal.ai を開いてアカウントを作成する

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://fal.ai
# Windows:
start https://fal.ai
# Linux:
xdg-open https://fal.ai
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 1: fal.ai アカウントの作成",
  "questions": [{
    "id": "account_status",
    "prompt": "ブラウザが開きましたか？以下の手順でアカウントを作成してください:\n\n1. 右上の「Sign Up」または「Login」をクリック\n2. GitHub または Google アカウントで認証する\n3. ダッシュボードが表示されたら完了\n\nアカウントにログインできましたか？",
    "options": [
      {"id": "logged_in", "label": "ログインできました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "signup_issue", "label": "サインアップできない"},
      {"id": "already_have_account", "label": "既にアカウントを持っている"}
    ]
  }]
}
```

(logged_in → Step 2へ)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://fal.ai」と案内)
(signup_issue → 「GitHubアカウントでの認証をお試しください。それでもうまくいかない場合は、Googleアカウントでの認証を試してみてください」と案内)
(already_have_account → Step 2へ)

---

## Chrome 統合で自動化する場合（`/chrome` モード）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://fal.ai を開く
2. Chrome 統合を使って以下の操作を順番に実行する:
   - 「Sign Up」または「Login」ボタンをクリック
   - GitHub または Google アカウントで認証（ユーザーの操作を待つ）
   - ログイン後、https://fal.ai/dashboard/keys に移動
   - 「Create Key」または「Add Key」ボタンをクリック
3. APIキーが表示されたことを確認したら、ユーザーに「APIキーをコピーしてください」と案内する
4. Step 3 に進む

**注意:** APIキーの値はブラウザ画面から読み取らないこと。ユーザーが手動でコピーする。

Chrome 統合が利用できない場合は、以下の手順を手動で実行してください。

---

## Step 2: APIキーを取得する

**AIが実行すること:**
1. APIキー管理ページをブラウザで開く:

```bash
# Mac:
open https://fal.ai/dashboard/keys
# Windows:
start https://fal.ai/dashboard/keys
# Linux:
xdg-open https://fal.ai/dashboard/keys
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 2: APIキーの取得",
  "questions": [{
    "id": "key_status",
    "prompt": "APIキー管理ページが開きましたか？以下の手順でAPIキーを取得してください:\n\n1. 「Create Key」または「Add Key」ボタンをクリック\n2. 表示されたAPIキーをコピーする\n   （キーは一度しか表示されない場合があります。必ずコピーしてください）\n\nAPIキーをコピーできましたか？",
    "options": [
      {"id": "copied", "label": "APIキーをコピーしました！"},
      {"id": "page_not_found", "label": "キー管理ページが見つからない"},
      {"id": "no_create_button", "label": "「Create Key」ボタンが見つからない"},
      {"id": "key_already_exists", "label": "既存のキーがある"}
    ]
  }]
}
```

(copied → Step 3へ)
(page_not_found → 「ブラウザで直接このURLを開いてください: https://fal.ai/dashboard/keys ログイン済みであることを確認してください」と案内)
(no_create_button → 「ページが完全に読み込まれるまで待ってください。ダッシュボード左側のメニューから「Keys」や「API Keys」を探してみてください」と案内)
(key_already_exists → 「既存のキーを使うこともできます。キーの値をコピーできればStep 3に進めます。新しいキーを作成しても構いません」と案内してStep 3へ)

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
│ uv run python tools/credential_manager.py store FAL_KEY            │
│                                                             │
│ → 「Enter value for FAL_KEY:」と表示されます               │
│ → コピーしたAPIキーを貼り付けてEnterを押してください        │
│   （入力した文字は画面に表示されません。これは正常です）    │
│ → 「✅ Stored FAL_KEY」と表示されたら保存完了です           │
└─────────────────────────────────────────────────────────────┘

保存が完了したら、こちらのチャットに戻って「完了」と教えてください。
```

**なぜ別ウィンドウで実行するのか:**
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
(terminal_help → 「Cursorの場合: 画面上部のメニュー > Terminal > New Terminal、またはキーボードの Ctrl+` (Macの場合は ⌘+`) を押してください。Claude Codeの場合: 別のターミナルウィンドウ/タブを開いてください。Mac: Cmd+T (新しいタブ) または Cmd+N (新しいウィンドウ)。Windows: WSL ターミナル（Ubuntu）を開くか、Windows Terminal で Ubuntu タブを追加してください。開いたら cd でプロジェクトのディレクトリに移動してください」と案内)
(command_error → AIが `uv run python tools/credential_manager.py status` を実行して状況を確認し、原因を特定。keyring 未インストールの場合は `uv add keyring` を自動実行)
(security_question → 「このツールはOS標準の暗号化ストレージを使います。macOSではKeychain、WindowsではCredential Locker、LinuxではSecretService (GNOME Keyring等) に保存されます。平文のファイル(.env)は一切作成しません。画面ロック中はストレージもロックされるため、物理的なアクセスからも保護されます」と説明)

---

## Step 4: 設定テスト

**AIが自動で実行すること:**

1. まず `credential_manager.py status` を実行して、`FAL_KEY` が Credential Store に保存されているか確認する:
   - **注意**: APIキーの値そのものをチャットに表示しないこと。「APIキーが設定されていることを確認しました（先頭8文字: xxxxxxxx...）」のようにマスク表示のみ
   - ステータス確認コマンド: `uv run python tools/credential_manager.py status`

2. `fal-client` パッケージがインストールされているか確認する:
   - 未インストールの場合: `uv add fal-client` を自動実行する

3. パッケージのインポートと FAL_KEY の設定確認テストを実行する:
   - **注意**: fal.ai の実際のAPI呼び出しはコストがかかるため、パッケージのインポートとキーの設定確認のみ行う
   - テストコード:
     ```python
     import os
     import sys
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("FAL_KEY")
     if not key:
         print("エラー: FAL_KEY が設定されていません。")
         sys.exit(1)
     try:
         import fal_client
         print(f"fal-client インストール済み: {fal_client.__version__ if hasattr(fal_client, '__version__') else 'OK'}")
         print(f"FAL_KEY 設定済み（先頭8文字: {key[:8]}...）")
         print("fal.ai APIの設定が完了しました！")
     except ImportError:
         print("fal-client が未インストールです。uv add fal-client を実行してください。")
     ```

4. テスト結果に応じてAskQuestionを表示:

**テスト成功時:**
```text
fal.ai APIの設定が完了しました！

テスト結果: fal-client パッケージのインポートと FAL_KEY の設定を確認しました。
これで動画生成（Kling, Veo等）、画像生成、リップシンク（Fabric）、音楽生成（Suno）などの
AIエンジンが利用可能です。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "テストでエラーが発生しました。考えられる原因を確認しましょう。",
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
      {"id": "trouble_signup", "label": "アカウントの作成・ログインができない"},
      {"id": "trouble_invalid", "label": "APIキーが無効（認証エラー）"},
      {"id": "trouble_package", "label": "fal-client のインストールでエラーが出る"},
      {"id": "trouble_python", "label": "Python バージョンの問題が出る"},
      {"id": "trouble_cost", "label": "料金が心配"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: アカウントの作成・ログインができない
**原因**: 認証プロバイダ（GitHub/Google）との連携に問題がある
**AIが行うこと**:
1. 「別の認証方法を試してください。GitHubで失敗した場合はGoogleアカウント、またはその逆をお試しください」と案内
2. 「ブラウザのシークレットモード（プライベートブラウジング）で https://fal.ai にアクセスし直してみてください」と案内
3. それでも解決しない場合は「fal.ai のサポート（https://fal.ai）に問い合わせてください」と案内

### トラブル2: APIキーが無効（認証エラー）
**原因**: APIキーが正しくコピーされていない、またはキーが無効
**AIが行うこと**:
1. `credential_manager.py status` で `FAL_KEY` の保存状態を確認（値はマスク表示のみ）
2. Credential Store に保存されていない場合は再登録を案内
3. 保存済みの場合は「fal.ai のダッシュボード（https://fal.ai/dashboard/keys）でキーが有効か確認してください。必要に応じて新しいキーを作成してください」と案内

### トラブル3: fal-client のインストールでエラーが出る
**原因**: pip の問題、または依存パッケージの競合
**AIが行うこと**:
1. `uv add fal-client` を再実行する
2. エラーが続く場合は `uv sync` を実行してから再試行
3. 環境が壊れている場合は `bash tools/scripts/setup.sh` で環境を再セットアップする

### トラブル4: Python バージョンの問題
**原因**: fal-client は Python 3.10 以上が必要
**AIが行うこと**:
1. `python --version` で現在のバージョンを確認
2. 3.10未満の場合は「fal-client は Python 3.10 以上が必要です。Python をアップグレードしてください」と案内
3. pyenv がインストール済みの場合は `pyenv install 3.10` を案内

### トラブル5: 料金が心配
**AIの案内**: 「fal.ai は従量課金制です。研修レベルの利用（数回の画像・動画生成テスト）であれば数ドル程度です。ダッシュボード（https://fal.ai/dashboard）で利用状況と残高をいつでも確認できます。課金上限を設定することも可能です」

### トラブル6: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] fal.ai でアカウントを作成した
- [ ] fal.ai ダッシュボードでAPIキーを取得した
- [ ] credential_manager.py store で Credential Store に FAL_KEY を保存した
- [ ] credential_manager.py status で保存を確認した
- [ ] fal-client パッケージがインストールされている
- [ ] テストが成功した（fal-client のインポートと FAL_KEY の設定確認）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "fal.ai APIのセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "video_overview", "label": "動画AIエンジンの概要を学ぶ（/start-13-2）"},
      {"id": "setup_elevenlabs", "label": "ElevenLabs APIもセットアップする（/setup-elevenlabs）"},
      {"id": "back_to_setup", "label": "セットアップ一覧に戻る（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- video_overview → /start-13-2 を案内
- setup_elevenlabs → /setup-elevenlabs を案内
- back_to_setup → /start-0-1 を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-fal` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/start-13-2` で動画AIエンジンの概要を学びましょう。または `/setup-elevenlabs` でElevenLabs APIを設定できます」

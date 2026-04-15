---
description: "Lesson command"
duration: "約10分"
prerequisites: ["ブラウザが使える", "メールアドレスまたはGoogle/GitHubアカウントを持っている"]
level: "beginner"
tags: ["setup", "elevenlabs", "api", "tts", "voice"]
---

# ElevenLabs API セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-elevenlabs` を実行して進捗を表示
2. 既存のAPIキーを自動検出:
   - `uv run python tools/credential_manager.py status` を実行
   - ELEVENLABS_API_KEY（または ELEVEN_API_KEY）が設定済みの場合、Step 4（APIテスト）のみ実行して完了にできる
   - `.env` に平文で存在する場合、credential store への移行を提案

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | ElevenLabs でAPIキーを取得し、Credential Store に保存してテキスト読み上げ(TTS)・音声合成機能を使えるようにする |
| 所要時間 | 約10分 |
| 前提条件 | メールアドレスまたはGoogle/GitHubアカウントを持っていること、ブラウザが使えること |
| 操作レベル | CLIコマンド入力なし（すべてAIが自動実行 + GUI操作のみ） |

**用途:**
ElevenLabs はAI音声合成（TTS）サービスです。テキスト読み上げ、音声クローニング、多言語音声合成が可能で、動画のナレーション生成などに使用します。

**料金について:**
無料プランで月1万文字まで利用可能です。研修レベルでは無料枠で十分です。

**このセッションの流れ:**
1. ブラウザでElevenLabsを開く（AIが自動でブラウザを起動）
2. アカウント作成・ログイン（Google/GitHub認証でサインアップ可）
3. APIキーを取得する（設定画面からコピーするだけ）
4. Credential Store に保存する（別ターミナルでコマンド実行）
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
(check_prereq → 「メールアドレスまたはGoogle/GitHubアカウントがあればOKです。無料プランで月1万文字まで使えます」と案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: ブラウザでElevenLabsを開く

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://elevenlabs.io
# Windows:
start https://elevenlabs.io
# Linux:
xdg-open https://elevenlabs.io
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 1: ElevenLabsにサインアップ / ログイン",
  "questions": [{
    "id": "signup_status",
    "prompt": "ブラウザが開きましたか？以下の手順でアカウントを作成してください:\n\n1. 右上の「Sign up」をクリック（既にアカウントがあれば「Log in」）\n2. Google / GitHub 認証、またはメールアドレスでサインアップ\n3. ログインできたら次に進みます\n\nログインできましたか？",
    "options": [
      {"id": "logged_in", "label": "ログインできました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "signup_issue", "label": "サインアップがうまくいかない"},
      {"id": "already_have_key", "label": "すでにAPIキーを持っている"}
    ]
  }]
}
```

(logged_in → Step 2へ)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://elevenlabs.io」と案内)
(signup_issue → 「Google認証が最も簡単です。右上の Sign up → Continue with Google をクリックしてください。それでもダメな場合はメールアドレスで登録してみてください」と案内)
(already_have_key → Step 3へスキップ)

---

## Chrome 統合で自動化する場合（`/chrome` モード）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://elevenlabs.io を開く
2. Chrome 統合を使って以下の操作を順番に実行する:
   - 「Sign up」または「Log in」をクリック
   - Google、GitHub、またはメールで認証（ユーザーの操作を待つ）
   - ログイン後、https://elevenlabs.io/app/settings/api-keys に移動
   - 既存のキーがあればそのまま、なければ「Create API Key」をクリック
3. APIキーが表示されたことを確認したら、ユーザーに「APIキーのコピーボタンをクリックしてコピーしてください」と案内する
4. Step 3 に進む

**注意:** APIキーの値はブラウザ画面から読み取らないこと。ユーザーが手動でコピーする。

Chrome 統合が利用できない場合は、以下の手順を手動で実行してください。

---

## Step 2: APIキーを取得する

**AIが実行すること:**
1. APIキー取得ページをブラウザで開く:

```bash
# Mac:
open https://elevenlabs.io/app/settings/api-keys
# Windows:
start https://elevenlabs.io/app/settings/api-keys
# Linux:
xdg-open https://elevenlabs.io/app/settings/api-keys
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 2: APIキーを取得",
  "questions": [{
    "id": "key_status",
    "prompt": "APIキーの設定画面が開きましたか？以下の手順でAPIキーを取得してください:\n\n1. API Keys ページが表示されていることを確認\n2. 既存のキーがあればコピーアイコンをクリック\n3. なければ「Create API Key」をクリックして新規作成\n4. 表示されたAPIキーをコピー\n\nAPIキーをコピーできましたか？",
    "options": [
      {"id": "copied", "label": "APIキーをコピーしました！"},
      {"id": "page_not_found", "label": "設定ページが見つからない"},
      {"id": "no_create_button", "label": "「Create API Key」ボタンが見つからない"},
      {"id": "need_help", "label": "その他のヘルプが必要"}
    ]
  }]
}
```

(copied → Step 3へ)
(page_not_found → 「ログイン後、左下のプロフィールアイコン → Profile + API key をクリックしてください。または直接このURLを開いてください: https://elevenlabs.io/app/settings/api-keys」と案内)
(no_create_button → 「ページが完全に読み込まれるまで待ってください。API Keys セクションに既存のキーが表示されている場合は、そのキーの横にあるコピーアイコンをクリックしてください」と案内)
(need_help → エラー状況をヒアリングして個別に対応)

---

## Step 3: APIキーを安全に保存する

**セキュリティに関する重要な注意:**
APIキーはこのチャットに貼り付けないでください。別のターミナルウィンドウで安全に保存します。

**AIが自動で実行すること:**
1. `keyring` パッケージがインストール済みか確認する
   - 未インストールの場合: `pip install keyring` を自動実行する
2. `uv run python tools/credential_manager.py status` を実行して現在の状態を確認する

**ユーザーに案内するメッセージ:**

```text
APIキーをコピーしたら、以下の手順で安全に保存してください:

┌──────────────────────────────────────────────────────────────────┐
│ 別のターミナルウィンドウで以下のコマンドを順番に実行してください:│
│                                                                  │
│ Cursor: Ctrl+` (バッククォート) で新しいターミナルを開く         │
│ Claude Code: 別のターミナルウィンドウを開く                      │
│                                                                  │
│ ① メインのキー名で保存:                                         │
│ uv run python tools/credential_manager.py store ELEVENLABS_API_KEY      │
│                                                                  │
│ → 「Enter value for ELEVENLABS_API_KEY:」と表示されます          │
│ → コピーしたAPIキーを貼り付けてEnterを押してください             │
│   （入力した文字は画面に表示されません。これは正常です）         │
│ → 「✅ Stored ELEVENLABS_API_KEY」と表示されたら保存完了です     │
│                                                                  │
│ ② エイリアスでも保存（一部のコードがこちらを参照します）:       │
│ uv run python tools/credential_manager.py store ELEVEN_API_KEY           │
│                                                                  │
│ → 同じAPIキーを貼り付けてEnterを押してください                   │
│ → 「✅ Stored ELEVEN_API_KEY」と表示されたら完了です             │
└──────────────────────────────────────────────────────────────────┘

2つとも保存が完了したら、こちらのチャットに戻って「完了」と教えてください。
```

**⚠️ なぜ別ウィンドウで実行するのか:**
AIのチャットでAPIキーを扱うと、会話ログに値が残ってしまいます。
別ウィンドウで `credential_manager.py` を実行すれば、キーの値はOSの
暗号化ストレージ（macOS Keychain / Windows Credential Locker / Linux SecretService）に
直接保存され、平文ファイルやチャットログに一切残りません。

**⚠️ なぜ2つのキー名で保存するのか:**
ElevenLabs の公式SDKやサンプルコードでは `ELEVEN_API_KEY` が使われることがあります。
`ELEVENLABS_API_KEY` と `ELEVEN_API_KEY` の両方に同じ値を保存しておくことで、
どちらのキー名を参照するコードでも正しく動作します。

**AskQuestionの設定:**
```json
{
  "title": "Step 3: APIキーの保存",
  "questions": [{
    "id": "store_status",
    "prompt": "別のターミナルで2つのコマンドを実行できましたか？",
    "options": [
      {"id": "done", "label": "2つとも保存しました！"},
      {"id": "one_done", "label": "1つ目だけ保存した"},
      {"id": "terminal_help", "label": "ターミナルの開き方がわからない"},
      {"id": "command_error", "label": "コマンドでエラーが出た"},
      {"id": "security_question", "label": "セキュリティについて質問がある"}
    ]
  }]
}
```

(done → Step 4へ)
(one_done → 「2つ目も同様に実行してください: `uv run python tools/credential_manager.py store ELEVEN_API_KEY` → 同じAPIキーを貼り付けてください」と案内)
(terminal_help → 「Cursorの場合: 画面上部のメニュー > Terminal > New Terminal、またはキーボードの Ctrl+バッククォート (Macの場合は Cmd+バッククォート) を押してください。Claude Codeの場合: 別のターミナルウィンドウ/タブを開いてください。Mac: Cmd+T (新しいタブ) または Cmd+N (新しいウィンドウ)。Windows: WSL ターミナル（Ubuntu）を開くか、Windows Terminal で Ubuntu タブを追加してください。開いたら cd でプロジェクトのディレクトリに移動してください」と案内)
(command_error → AIが `uv run python tools/credential_manager.py status` を実行して状況を確認し、原因を特定。keyring 未インストールの場合は `pip install keyring` を自動実行)
(security_question → 「このツールはOS標準の暗号化ストレージを使います。macOSではKeychain、WindowsではCredential Locker、LinuxではSecretService (GNOME Keyring等) に保存されます。平文のファイル(.env)は一切作成しません。画面ロック中はストレージもロックされるため、物理的なアクセスからも保護されます」と説明)

---

## Step 4: 設定テスト

**AIが自動で実行すること:**

1. まず `credential_manager.py status` を実行して、`ELEVENLABS_API_KEY` が Credential Store に保存されているか確認する:
   - **注意**: APIキーの値は一切表示しないこと。結果は「APIキーが設定されていることを確認しました」のみ表示する
   - ステータス確認コマンド: `uv run python tools/credential_manager.py status`

2. 簡易チェックに通ったら、実際にElevenLabs APIにテストリクエストを送信する:
   - Credential Store から環境変数に注入してAPI呼び出しを実行する
   - テストコード例:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_API_KEY")
     if not key:
         print("エラー: ELEVENLABS_API_KEY が設定されていません。")
         sys.exit(1)
     resp = requests.get("https://api.elevenlabs.io/v1/models",
         headers={"xi-api-key": key})
     if resp.status_code == 200:
         models = resp.json()
         print(f"接続成功！ 利用可能モデル数: {len(models)}")
         for m in models[:3]:
             print(f"  - {m.get('name', 'N/A')}")
     else:
         print(f"エラー: {resp.status_code}")
         print("詳細は再認証・APIキー再生成・権限設定を確認してください。")
     ```
   - 必要なパッケージ（`requests`, `keyring`）がインストールされていない場合は自動でインストールする

3. テスト結果に応じてAskQuestionを表示:

**テスト成功時:**
```text
ElevenLabs APIの設定が完了しました！

テスト結果: APIからモデル一覧を正常に取得できました。
これでテキスト読み上げ(TTS)、音声合成、ナレーション生成などの機能が使えるようになりました。
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
      {"id": "trouble_invalid", "label": "「Invalid API key」エラーが出る"},
      {"id": "trouble_quota", "label": "「Quota exceeded」エラーが出る"},
      {"id": "trouble_package", "label": "Pythonパッケージのエラーが出る"},
      {"id": "trouble_voice", "label": "日本語ボイスの選び方がわからない"},
      {"id": "trouble_cost", "label": "料金が心配"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: 「Invalid API key」エラー
**原因**: APIキーが正しくコピーされていない、またはキーが無効
**AIが行うこと**:
1. `credential_manager.py status` で `ELEVENLABS_API_KEY` の保存状態を確認（値はマスク表示のみ）
2. Credential Store に保存されていない場合は再登録を案内
3. 保存済みの場合はAPIテストを再実行。失敗すれば「ElevenLabsの設定画面でキーを再作成してください: https://elevenlabs.io/app/settings/api-keys」と案内

### トラブル2: 「Quota exceeded」エラー
**原因**: 無料枠の月間文字数制限（1万文字）に達した
**AIの案内**: 「ElevenLabsの無料プランは月1万文字までです。月初にリセットされるので、翌月まで待つか、有料プラン（Starter: $5/月、30,000文字）へのアップグレードを検討してください。現在の使用量は https://elevenlabs.io/app/subscription で確認できます」

### トラブル3: Pythonパッケージのエラー
**原因**: 必要なパッケージがインストールされていない
**AIが行うこと**: 不足パッケージを自動でインストールする（`pip install requests keyring`）

### トラブル4: 日本語ボイスの選び方
**AIの案内**: 「ElevenLabsでは多言語対応ボイスが利用可能です。日本語に対応しているボイスを探すには、https://elevenlabs.io/app/voice-library で 'Japanese' でフィルタリングしてください。Multilingual v2 モデルを使用すると、ほとんどのボイスで日本語テキストを自然に読み上げられます」

### トラブル5: 料金が心配
**AIの案内**: 「ElevenLabsには無料プランがあり、月1万文字まで利用できます。研修レベルの利用（テスト生成を数回程度）であれば無料枠で十分です。使用量は https://elevenlabs.io/app/subscription でいつでも確認できます。有料プランへの自動切り替えはないので、意図せず課金されることはありません」

### トラブル6: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] ElevenLabsアカウントを作成した（またはログインした）
- [ ] APIキー設定画面でAPIキーを取得・コピーした
- [ ] credential_manager.py store ELEVENLABS_API_KEY で Credential Store に保存した
- [ ] credential_manager.py store ELEVEN_API_KEY でエイリアスも保存した
- [ ] credential_manager.py status で保存を確認した
- [ ] APIテストが成功した（モデル一覧を取得できた）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "ElevenLabs APIのセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "try_video_narration", "label": "プロダクト紹介動画を作ってみる（/start-13-3）"},
      {"id": "try_slide_video", "label": "スライド解説動画を作ってみる（/start-13-5）"},
      {"id": "setup_other", "label": "他のAPIもセットアップする（/start-0-1）"},
      {"id": "back_to_setup", "label": "セットアップ一覧に戻る（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- try_video_narration → /start-13-3 を案内
- try_slide_video → /start-13-5 を案内
- setup_other → /start-0-1 を案内
- back_to_setup → /start-0-1 を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-elevenlabs` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「ElevenLabs APIの設定が完了しました。`/start-13-3` でプロダクト紹介動画の作成、`/start-13-5` でスライド解説動画の作成に進めます」

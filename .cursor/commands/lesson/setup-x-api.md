---
description: "Lesson command"
duration: "約15分"
prerequisites: ["Xアカウントを持っている", "ブラウザが使える"]
level: "beginner"
tags: ["setup", "x", "twitter", "api"]
---

# X (Twitter) API セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-x-api` を実行して進捗を表示
2. 既存のAPIキーを自動検出:
   - `uv run python tools/credential_manager.py status` を実行
   - X_BEARER_TOKEN が設定済みの場合、Step 4（APIテスト）のみ実行して完了にできる
   - `.env` に平文で存在する場合、credential store への移行を提案

**重要な警告をユーザーに表示:**

```text
⚠️ X (Twitter) API は有料プランが必要です

- Free tier: Recent Search API は利用できません
- Basic plan: $100/月 が必要です
- このセットアップは任意です。x-research スキルを使わない場合はスキップできます

研修の他のレッスン（バナー生成、図表作成、データ分析など）は
X API がなくても問題なく受講できます。
```

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | X Developer Portal で Bearer Token を取得し、Credential Store に保存して X のリアルタイム検索・トレンド分析機能を使えるようにする |
| 所要時間 | 約15分 |
| 前提条件 | Xアカウントを持っていること、ブラウザが使えること |
| 操作レベル | CLIコマンド入力なし（すべてAIが自動実行 + GUI操作のみ） |
| 料金 | **Basic plan ($100/月) 以上が必要**。Free tier では Recent Search API が使えません |
| 用途 | X (Twitter) のリアルタイム検索・トレンド分析。x-research スキルで使用 |

**このセッションの流れ:**
1. ブラウザで X Developer Portal を開く（AIが自動でブラウザを起動）
2. Developer アカウントを申請し、プロジェクト・Appを作成する
3. Bearer Token を取得する
4. 別ターミナルで credential_manager.py を使って安全に保存する
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
    "prompt": "X API のセットアップには Basic plan ($100/月) が必要です。準備はできていますか？",
    "options": [
      {"id": "ready", "label": "有料プランに加入済み / 加入する予定です。始めましょう"},
      {"id": "chrome", "label": "/chrome でブラウザ操作を自動化する"},
      {"id": "check_cost", "label": "料金について詳しく知りたい"},
      {"id": "skip", "label": "スキップする（X APIは使わない）"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready -> Step 1へ)
(chrome → Step 1 でブラウザを開いた後、「Chrome 統合で自動化する場合」セクションの手順で自動実行する)
(check_cost -> 「X API の料金体系: Free tier は投稿のみ（検索API不可）。Basic plan ($100/月) で Recent Search API が使えます。Pro plan ($5,000/月) は Full-Archive Search が使えますが、研修では Basic で十分です。コストに見合わない場合はスキップを推奨します」と案内)
(skip -> 「X APIセットアップをスキップしました。他のレッスンに影響はありません。後から /setup-x-api で再開できます」と案内して完了処理へ)
(different_lesson -> モジュール一覧を表示)

---

## Step 1: ブラウザで X Developer Portal を開く

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://developer.x.com/en/portal/dashboard
# Windows:
start https://developer.x.com/en/portal/dashboard
# Linux:
xdg-open https://developer.x.com/en/portal/dashboard
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 1: X Developer Portal にアクセス",
  "questions": [{
    "id": "portal_status",
    "prompt": "ブラウザが開きましたか？以下の手順で Developer アカウントを申請してください:\n\n1. Xアカウントでログインする\n2. 「Sign up for Free Account」または「Subscribe to Basic」を選択\n   （Recent Search API を使うには Basic plan が必要です）\n3. 利用目的を記入する（例: 'Academic research and AI agent training'）\n4. 開発者契約に同意する\n\nDeveloper Portal のダッシュボードが表示されましたか？",
    "options": [
      {"id": "dashboard_ready", "label": "ダッシュボードが表示されました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "signup_issue", "label": "Developer アカウントの申請がうまくいかない"},
      {"id": "already_have_account", "label": "すでに Developer アカウントを持っている"}
    ]
  }]
}
```

(dashboard_ready -> Step 2へ)
(browser_not_open -> 「ブラウザで直接このURLを開いてください: https://developer.x.com/en/portal/dashboard」と案内)
(signup_issue -> 「Developer Portal の申請には審査が必要な場合があります。利用目的は具体的に記入してください（例: 'Building an AI-powered social media research tool for corporate training'）。審査に数日かかる場合があります。承認メールが届いてから再度このセットアップを実行してください」と案内)
(already_have_account -> Step 2へ)

---

## Chrome 統合で自動化する場合（`/chrome` モード）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://developer.x.com/en/portal/dashboard を開く
2. Chrome 統合を使って以下の操作を順番に実行する:
   - 「Subscribe to Basic」を選択（Recent Search API を使うには Basic plan が必要。Free Account では検索APIが使えません）
   - 支払い情報の入力はユーザーに任せる（ユーザーの操作を待つ）
   - Use case に「AI agent training and educational purposes」と入力
   - Developer Agreement に同意して Submit（ユーザーの操作を待つ）
   - Dashboard で「Projects & Apps」に移動
   - 「+ Add Project」をクリック → Project name に「AIAgent Bootcamp」、Use case で「Exploring the API」を選択
   - 「+ Add App」をクリック → App name に「AIAgent Bootcamp」、Environment で「Development」を選択
   - 「Keys and tokens」タブを開く
   - Bearer Token の横にある「Regenerate」をクリック
   - 確認ダイアログで「Yes, regenerate」をクリック
3. Bearer Token が表示されたことを確認したら、ユーザーに「トークンをコピーしてください。ページを離れると再表示できません」と案内する
4. Step 3 に進む

**注意:** Bearer Token の値はブラウザ画面から読み取らないこと。ユーザーが手動でコピーする。

Chrome 統合が利用できない場合は、以下の手順を手動で実行してください。

---

## Step 2: プロジェクト作成と Bearer Token の取得

**AskQuestionの設定:**
```json
{
  "title": "Step 2: Bearer Token を取得",
  "questions": [{
    "id": "token_status",
    "prompt": "以下の手順で Bearer Token を取得してください:\n\n1. Dashboard > 「Projects & Apps」セクションを確認\n2. プロジェクトがない場合は「+ Add Project」をクリック\n   - プロジェクト名を入力（例: 'AIAgent Bootcamp'）\n   - Use case を選択（例: 'Exploring the API'）\n3. プロジェクト内の「+ Add App」をクリック\n   - App名を入力（例: 'AIAgent Bootcamp'）\n   - App environment は「Development」を選択\n4. 「Keys and tokens」タブを開く\n5. 「Bearer Token」セクションの「Regenerate」をクリック\n6. 表示された Bearer Token をコピーする\n\nBearer Token をコピーできましたか？",
    "options": [
      {"id": "copied", "label": "Bearer Token をコピーしました！"},
      {"id": "no_project", "label": "プロジェクトの作成方法がわからない"},
      {"id": "no_bearer", "label": "Bearer Token が見つからない"},
      {"id": "plan_issue", "label": "Free tier なので Basic にアップグレードしたい"}
    ]
  }]
}
```

(copied -> Step 3へ)
(no_project -> 「Dashboard の左メニューから 'Projects & Apps' を選択してください。'+ Add Project' ボタンが表示されます。プロジェクト名は自由に設定できます（例: 'AIAgent Bootcamp'）。作成後、プロジェクト内で '+ Add App' をクリックしてアプリを追加してください」と案内)
(no_bearer -> 「App を選択 > 'Keys and tokens' タブを開いてください。ページ中段に 'Bearer Token' セクションがあります。'Regenerate' ボタンをクリックすると新しいトークンが生成されます。表示されたトークンをすぐにコピーしてください（ページを離れると再表示できません）」と案内)
(plan_issue -> 「Dashboard の左メニューから 'Products' > 'Twitter API v2' を選択し、'Basic' プランの 'Subscribe' をクリックしてください。クレジットカード情報の入力が必要です。アップグレード完了後、Step 2 の手順に戻ってください」と案内)

---

## Step 3: Bearer Token を安全に保存する

**セキュリティに関する重要な注意:**
Bearer Token はこのチャットに貼り付けないでください。別のターミナルウィンドウで安全に保存します。

**AIが自動で実行すること:**
1. `keyring` パッケージがインストール済みか確認する
   - 未インストールの場合: `pip install keyring` を自動実行する
2. `uv run python tools/credential_manager.py status` を実行して現在の状態を確認する

**ユーザーに案内するメッセージ:**

```text
Bearer Token をコピーしたら、以下の手順で安全に保存してください:

┌─────────────────────────────────────────────────────────────┐
│ 別のターミナルウィンドウで以下のコマンドを実行してください: │
│                                                             │
│ Cursor: Ctrl+` (バッククォート) で新しいターミナルを開く    │
│ Claude Code: 別のターミナルウィンドウを開く                 │
│                                                             │
│ uv run python tools/credential_manager.py store X_BEARER_TOKEN     │
│                                                             │
│ → 「Enter value for X_BEARER_TOKEN:」と表示されます         │
│ → コピーした Bearer Token を貼り付けてEnterを押してください │
│   （入力した文字は画面に表示されません。これは正常です）    │
│ → 「✅ Stored X_BEARER_TOKEN」と表示されたら保存完了です    │
└─────────────────────────────────────────────────────────────┘

保存が完了したら、こちらのチャットに戻って「完了」と教えてください。
```

**なぜ別ウィンドウで実行するのか:**
AIのチャットで Bearer Token を扱うと、会話ログに値が残ってしまいます。
別ウィンドウで `credential_manager.py` を実行すれば、トークンの値はOSの
暗号化ストレージ（macOS Keychain / Windows Credential Locker / Linux SecretService）に
直接保存され、平文ファイルやチャットログに一切残りません。

**AskQuestionの設定:**
```json
{
  "title": "Step 3: Bearer Token の保存",
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

(done -> Step 4へ)
(terminal_help -> 「Cursorの場合: 画面上部のメニュー > Terminal > New Terminal、またはキーボードの Ctrl+バッククォート (Macの場合は Cmd+バッククォート) を押してください。Claude Codeの場合: 別のターミナルウィンドウ/タブを開いてください。Mac: Cmd+T (新しいタブ) または Cmd+N (新しいウィンドウ)。Windows: WSL ターミナル（Ubuntu）を開くか、Windows Terminal で Ubuntu タブを追加してください。開いたら cd でプロジェクトのディレクトリに移動してください」と案内)
(command_error -> AIが `uv run python tools/credential_manager.py status` を実行して状況を確認し、原因を特定。keyring 未インストールの場合は `pip install keyring` を自動実行)
(security_question -> 「このツールはOS標準の暗号化ストレージを使います。macOSではKeychain、WindowsではCredential Locker、LinuxではSecretService (GNOME Keyring等) に保存されます。平文のファイル(.env)は一切作成しません。画面ロック中はストレージもロックされるため、物理的なアクセスからも保護されます」と説明)

---

## Step 4: 設定テスト

**AIが自動で実行すること:**

1. まず `credential_manager.py status` を実行して、`X_BEARER_TOKEN` が Credential Store に保存されているか確認する:
   - **注意**: Bearer Token の値そのものをチャットに表示しないこと。「Bearer Token が設定されていることを確認しました（先頭4文字: AAAA...）」のようにマスク表示のみ
   - ステータス確認コマンド: `uv run python tools/credential_manager.py status`

2. 簡易チェックに通ったら、実際に X API にテストリクエストを送信する:
   - Credential Store から環境変数に注入してAPI呼び出しを実行する
   - テストコード:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     token = os.getenv("X_BEARER_TOKEN")
     if not token:
         print("エラー: X_BEARER_TOKEN が設定されていません。")
         sys.exit(1)
     resp = requests.get("https://api.x.com/2/tweets/search/recent",
         params={"query": "hello", "max_results": 10},
         headers={"Authorization": f"Bearer {token}"})
     if resp.status_code == 200:
         data = resp.json()
         count = data.get("meta", {}).get("result_count", 0)
         print(f"接続成功！ 検索結果: {count}件")
     elif resp.status_code == 403:
         print("エラー: アクセス権限がありません。Basic plan ($100/月) 以上が必要です。")
     else:
         print(f"エラー: {resp.status_code}")
         print("詳細は再認証・APIキー再生成・権限設定を確認してください。")
     ```
   - 必要なパッケージ（`requests`, `keyring`）がインストールされていない場合は自動でインストールする

3. テスト結果に応じてAskQuestionを表示:

**テスト成功時:**
```text
X API の設定が完了しました！

テスト結果: Recent Search API からの応答を正常に受信しました。
これで X (Twitter) のリアルタイム検索・トレンド分析機能が使えるようになりました。
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
      {"id": "recheck_token", "label": "Bearer Token を確認し直す（Step 1に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry -> テストを再実行)
(recheck_token -> Step 1に戻る)
(show_error -> エラーメッセージを表示して原因と解決方法を案内)
(skip_test -> 「APIテストはスキップしました。後で /check-setup で確認できます」と案内)

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
      {"id": "trouble_403", "label": "「403 Forbidden」エラーが出る"},
      {"id": "trouble_429", "label": "「429 Too Many Requests」エラーが出る"},
      {"id": "trouble_401", "label": "「401 Unauthorized」エラーが出る"},
      {"id": "trouble_approval", "label": "Developer Portal の申請が承認されない"},
      {"id": "trouble_package", "label": "Pythonパッケージのエラーが出る"},
      {"id": "trouble_cost", "label": "料金が心配"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: 「403 Forbidden」エラー
**原因**: Free tier では Recent Search API が利用できない
**AIの案内**: 「X API の Free tier では Recent Search API（/2/tweets/search/recent）が利用できません。Basic plan ($100/月) 以上へのアップグレードが必要です。Dashboard > Products > Twitter API v2 から Basic プランに Subscribe してください。アップグレード後、Bearer Token の再生成は不要です（同じトークンで利用できます）」

### トラブル2: 「429 Too Many Requests」エラー
**原因**: Rate limit に達した
**AIの案内**: 「X API にはレート制限があります。Basic plan の Recent Search API は15分あたり60リクエストが上限です。数分待ってから再度お試しください。連続で大量のリクエストを送らないようにしてください」

### トラブル3: 「401 Unauthorized」エラー
**原因**: Bearer Token が無効または正しくコピーされていない
**AIが行うこと**:
1. `credential_manager.py status` で `X_BEARER_TOKEN` の保存状態を確認（値はマスク表示のみ）
2. Credential Store に保存されていない場合は再登録を案内
3. 保存済みの場合はAPIテストを再実行。失敗すれば「Developer Portal > App > Keys and tokens で Bearer Token を Regenerate してください」と案内

### トラブル4: Developer Portal の申請が承認されない
**AIの案内**: 「Developer Portal の申請には審査が必要な場合があります。以下のポイントを確認してください: (1) 利用目的を具体的かつ英語で記入する (2) 'Academic research and AI agent training for corporate education programs' のように教育目的を強調する (3) データの利用方法を明記する（例: 'Analyzing public tweet trends for training purposes only'）。通常1〜3営業日で承認されます。再申請も可能です」

### トラブル5: Pythonパッケージのエラー
**原因**: 必要なパッケージがインストールされていない
**AIが行うこと**: 不足パッケージを自動でインストールする（`pip install requests keyring`）

### トラブル6: 料金が心配
**AIの案内**: 「X API の料金体系は以下の通りです: Free ($0) = 投稿のみ、検索API不可。Basic ($100/月) = Recent Search API（過去7日間）が利用可能。Pro ($5,000/月) = Full-Archive Search（全履歴）が利用可能。研修では Basic で十分です。X API を使わないレッスン（バナー生成、図表作成など）は影響ありません。コストに見合わないと感じた場合はスキップしてください」

### トラブル7: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] X Developer Portal で Developer アカウントを申請した
- [ ] プロジェクトと App を作成した
- [ ] Bearer Token を取得した
- [ ] credential_manager.py store で Credential Store に保存した
- [ ] credential_manager.py status で保存を確認した
- [ ] APIテストが成功した（Recent Search API からの応答を受信できた）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "X API のセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "try_x_research", "label": "X リサーチを試してみる（x-research スキル）"},
      {"id": "try_marketing", "label": "マーケティングレッスンを始める（/start-12-1）"},
      {"id": "setup_other", "label": "他のAPIもセットアップする（/start-0-1）"},
      {"id": "back_to_setup", "label": "セットアップ一覧に戻る（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- try_x_research -> x-research スキルの使い方を案内
- try_marketing -> /start-12-1 を案内
- setup_other -> /start-0-1 を案内
- back_to_setup -> /start-0-1 を案内
- finish -> 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-x-api` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「x-research スキルやマーケティングレッスン（/start-12-1）で X API を活用できます」

---
description: "Lesson command"
duration: "約15分"
prerequisites: ["Notionアカウントを持っている（無料プランでOK）", "ブラウザが使える", "Node.js 18以上"]
level: "beginner"
tags: ["setup", "notion", "ncli", "mcp", "api"]
nonInteractiveMode: incompatible
---
# Notion CLI (ncli) + MCP セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-notion` を実行して進捗を表示
2. 既存の設定を自動検出:
   - `which ncli` で ncli がインストール済みか確認
   - Claude Code の場合: `~/.claude/mcp_settings.json` に `notion` サーバーが定義されているか確認
   - Cursor の場合: `.cursor/mcp.json` に `notion` サーバーが定義されているか確認
   - ncli インストール済み＆MCP設定済みの場合、Step 6（接続テスト）のみ実行して完了にできる

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | ncli（Notion CLI）をインストールし、Notion インテグレーションを作成して、ターミナル＋MCP 経由で Notion を操作できるようにする |
| 所要時間 | 約15分 |
| 前提条件 | Notionアカウント（無料プランでOK）、Node.js 18以上、ブラウザ |
| 操作レベル | CLIコマンド入力なし（すべてAIが自動実行 + GUI操作のみ） |

**このセッションの流れ:**
1. ncli（@sakasegawa/ncli）をインストールする（AIが自動実行）
2. ブラウザでNotion Integrationsページを開く（AIが自動でブラウザを起動）
3. インテグレーションを作成してAPIキーを取得する（画面上のボタンをクリックするだけ）
4. MCP設定ファイルを作成する（AIが自動作成）
5. Notionページへのインテグレーション共有設定
6. ncli + MCP 接続テスト

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
      {"id": "which_tool", "label": "Claude Code と Cursor のどちらを使っているか確認したい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(chrome → Step 1 でブラウザを開いた後、「Chrome 統合で自動化する場合」セクションの手順で自動実行する)
(check_prereq → 「Notionアカウント（無料プランでOK）があり、ブラウザでログインできれば準備OKです」と案内)
(which_tool → 「Claude Code を使っている場合と Cursor を使っている場合で設定ファイルの場所が異なります。Step 4 でそれぞれの手順を案内します」と説明)
(different_lesson → モジュール一覧を表示)

---

## Step 1: ncli（Notion CLI）のインストール

**AIが実行すること:**
1. Node.js のバージョンを確認: `node --version`（18以上が必要）
2. ncli がインストール済みか確認: `which ncli`
3. 未インストールの場合、以下のコマンドを実行:

```bash
npm install -g @sakasegawa/ncli
```

4. インストール後、`ncli --version` で確認する

**AskQuestionの設定:**
```json
{
  "title": "Step 1: ncli のインストール",
  "questions": [{
    "id": "ncli_status",
    "prompt": "ncli のインストールを実行しました。結果を確認してください。",
    "options": [
      {"id": "installed", "label": "インストールできました！"},
      {"id": "npm_error", "label": "npm install でエラーが出た"},
      {"id": "no_node", "label": "Node.js がインストールされていない"},
      {"id": "command_not_found", "label": "ncli コマンドが見つからない"}
    ]
  }]
}
```

(installed → Step 2へ)
(npm_error → `npm cache clean --force` を実行後リトライ。権限エラーの場合は `sudo npm install -g @sakasegawa/ncli` を案内)
(no_node → 「https://nodejs.org/ から LTS 版（18以上）をインストールしてください」と案内)
(command_not_found → `npm list -g @sakasegawa/ncli` でインストール確認。PATH の問題なら `npm bin -g` で確認してPATHに追加する手順を案内)

---

## Step 2: ブラウザでNotion Integrationsページを開く

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. 以下のコマンドを実行してブラウザを自動起動する:

```bash
# Mac:
open https://www.notion.so/my-integrations
# Windows:
start https://www.notion.so/my-integrations
# Linux:
xdg-open https://www.notion.so/my-integrations
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 2: インテグレーションを作成",
  "questions": [{
    "id": "browser_status",
    "prompt": "ブラウザが開きましたか？以下の手順でインテグレーションを作成してください:\n\n1. Notionにログインする\n2. 「New integration」（新しいインテグレーション）ボタンをクリック\n3. 名前を「AIAgent Bootcamp」にする\n4. タイプは「Internal」を選択\n5. Capabilities で「Read content」「Update content」「Insert content」にチェック\n6. 「Submit」（送信）をクリック\n\nインテグレーションを作成できましたか？",
    "options": [
      {"id": "created", "label": "インテグレーションを作成しました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "no_button", "label": "「New integration」ボタンが見つからない"},
      {"id": "login_issue", "label": "Notionにログインできない"}
    ]
  }]
}
```

(created → Step 3へ)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://www.notion.so/my-integrations」と案内)
(no_button → 「ページが完全に読み込まれるまで待ってください。Notionにログインした状態で https://www.notion.so/my-integrations にアクセスすると、右上付近に「New integration」ボタンが表示されます」と案内)
(login_issue → 「Notionアカウントをお持ちでない場合は https://www.notion.so/signup から無料で作成できます。既にアカウントがある場合は、メールアドレスまたはGoogleアカウントでログインしてください」と案内)

---

## Chrome 統合で自動化する場合（`/chrome` モード）

**前提条件:** Chrome に「Claude in Chrome」拡張機能（v1.0.36+）がインストール済みで、`claude --chrome` で起動しているか、セッション内で `/chrome` を実行済みであること。

**AIが Chrome 統合で自動実行する内容:**
1. ブラウザで https://www.notion.so/my-integrations を開く
2. Chrome 統合を使って以下の操作を順番に実行する:
   - 「New integration」ボタンをクリック
   - Name に「AIAgent Bootcamp」と入力
   - Associated workspace でデフォルトのワークスペースを選択
   - Type で「Internal」を選択
   - Capabilities で Read content、Update content、Insert content にチェック
   - 「Submit」をクリック
3. Internal Integration Secret が表示されたことを確認したら、ユーザーに「シークレットの横のCopyボタンをクリックしてコピーしてください」と案内する
4. Step 3 に進む

**注意:** シークレットの値はブラウザ画面から読み取らないこと。ユーザーが手動でコピーする。

Chrome 統合が利用できない場合は、以下の手順を手動で実行してください。

---

## Step 3: APIキーをコピーする

**ユーザーに案内するメッセージ:**

```text
インテグレーション作成後、以下の手順でAPIキーをコピーしてください:

1. 作成したインテグレーションの設定ページが表示されます
2. 「Internal Integration Secret」セクションにトークンが表示されます
   （secret_xxx で始まる文字列です）
3. 「Copy」ボタンをクリックしてトークンをコピーしてください

⚠️ コピーしたトークンはこのチャットに貼り付けないでください。
   次のステップでAIが安全に設定ファイルに書き込みます。
```

**AskQuestionの設定:**
```json
{
  "title": "Step 3: APIキーのコピー",
  "questions": [{
    "id": "copy_status",
    "prompt": "Internal Integration Secret（secret_xxx で始まる文字列）をコピーできましたか？",
    "options": [
      {"id": "copied", "label": "APIキーをコピーしました！"},
      {"id": "no_secret", "label": "トークンが見つからない"},
      {"id": "help_capabilities", "label": "Capabilitiesの設定がわからない"}
    ]
  }]
}
```

(copied → Step 4へ)
(no_secret → 「インテグレーション一覧（https://www.notion.so/my-integrations）から作成したインテグレーション名をクリックすると、設定ページに移動できます。「Internal Integration Secret」セクションに secret_ で始まるトークンが表示されます」と案内)
(help_capabilities → 「インテグレーション設定ページの「Capabilities」タブで、「Read content」「Update content」「Insert content」にチェックを入れてください。これでAPIからページの読み書きが可能になります」と案内)

---

## Step 4: MCP設定ファイルを作成する

**AIが自動で実行すること:**

1. 使用ツールを判定する（Claude Code or Cursor）
2. 対応するMCP設定ファイルにプレースホルダー付きの設定を作成する
3. ユーザーにプレースホルダーをAPIキーで置換してもらう

**AIが作成するMCP設定ファイル:**

**Claude Code の場合:** `~/.claude/mcp_settings.json`
**Cursor の場合:** `~/.cursor/mcp.json`（ホームディレクトリ。リポジトリ内の `.cursor/mcp.json` には書き込まないこと）

設定内容（既存の `mcpServers` がある場合は `notion` エントリを追記）:
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "YOUR_NOTION_TOKEN_HERE"
      }
    }
  }
}
```

3. AIがファイルを作成した後、ユーザーに案内する:

```text
MCP設定ファイルを作成しました。APIキーを設定してください:

┌─────────────────────────────────────────────────────────────┐
│ 以下のファイルをテキストエディタで開いてください:           │
│                                                             │
│ Claude Code: ~/.claude/mcp_settings.json                    │
│ Cursor:      ~/.cursor/mcp.json                             │
│                                                             │
│ ファイル内の YOUR_NOTION_TOKEN_HERE を                       │
│ コピーしたAPIキー（secret_xxx...）で置き換えてください。     │
│ 保存したら、こちらのチャットに戻ってください。              │
└─────────────────────────────────────────────────────────────┘

⚠️ APIキーはこのチャットに貼り付けないでください。
   エディタで直接ファイルを編集すれば、チャットログに残りません。
```

**AskQuestionの設定:**
```json
{
  "title": "Step 4: MCP設定ファイルの作成",
  "questions": [{
    "id": "config_status",
    "prompt": "MCP設定ファイルのAPIキーを置換できましたか？",
    "options": [
      {"id": "done", "label": "APIキーを設定しました！"},
      {"id": "editor_help", "label": "ファイルの開き方がわからない"},
      {"id": "existing_config", "label": "既に設定ファイルがあるので追記方法を知りたい"},
      {"id": "security_question", "label": "セキュリティについて質問がある"}
    ]
  }]
}
```

(done → AIが設定ファイルを読み取り、`YOUR_NOTION_TOKEN_HERE` が残っていないか確認（キーの値は表示しない）。OKなら Step 5 へ)
(editor_help → 「ターミナルで以下を実行するとエディタで開けます: Mac: `open ~/.claude/mcp_settings.json` / Cursor: `code ~/.cursor/mcp.json`。または Finder/エクスプローラーで隠しファイルを表示してファイルを開いてください」と案内)
(existing_config → 既存ファイルの内容を読み取り、`mcpServers` に `notion` エントリを追記する方法を案内。既存の他のMCPサーバー設定は保持する)
(security_question → 「MCP設定ファイルはホームディレクトリ内にあり、Gitリポジトリには含まれません。APIキーはこのファイルにのみ保存され、MCPサーバー起動時に環境変数として渡されます」と説明)

---

## Step 5: ページへのインテグレーション共有

**重要: この手順を行わないと、MCPからNotionのページにアクセスできません。**

**ユーザーに案内するメッセージ:**

```text
Notion APIでは、インテグレーションがアクセスできるページを明示的に指定する必要があります。
以下の手順で、アクセスしたいページにインテグレーションを共有してください:

┌─────────────────────────────────────────────────────────────┐
│ 1. Notionでアクセスしたいページを開く                       │
│ 2. ページ右上の「...」（三点メニュー）をクリック            │
│ 3. 「Add connections」（接続を追加）を選択                  │
│ 4. 検索欄に「AIAgent Bootcamp」と入力                       │
│ 5. 表示されたインテグレーション名をクリックして選択         │
│ 6. 確認ダイアログで「Confirm」をクリック                    │
│                                                             │
│ ※ 親ページに共有設定すると、子ページにも自動で適用されます │
│ ※ 複数のページにアクセスしたい場合は、各ページで同じ操作   │
│   を行うか、共通の親ページに設定してください                │
└─────────────────────────────────────────────────────────────┘
```

**AskQuestionの設定:**
```json
{
  "title": "Step 5: ページへのインテグレーション共有",
  "questions": [{
    "id": "share_status",
    "prompt": "Notionページにインテグレーションを共有できましたか？",
    "options": [
      {"id": "shared", "label": "共有設定しました！"},
      {"id": "no_connection", "label": "「Add connections」が見つからない"},
      {"id": "no_integration", "label": "インテグレーション名が表示されない"},
      {"id": "skip_share", "label": "後で設定する（スキップ）"}
    ]
  }]
}
```

(shared → Step 6へ)
(no_connection → 「ページ右上の「...」メニューを開くと、下の方に「Add connections」があります。見つからない場合は、ページのオーナー権限があるか確認してください。ゲスト権限では表示されません」と案内)
(no_integration → 「インテグレーション作成直後は表示に少し時間がかかる場合があります。ページをリロードしてから再度お試しください。それでも表示されない場合は、https://www.notion.so/my-integrations でインテグレーションが正しく作成されているか確認してください」と案内)
(skip_share → 「後で設定できます。MCPからページにアクセスする際にこの設定が必要になります。/start-12-1 で Notion を使う前に設定してください」と案内してStep 6へ)

---

## Step 6: MCP接続テスト

**AIが実行すること:**

1. Claude Code / Cursor の再起動を案内:

```text
MCP設定を反映するには、ツールの再起動が必要です。

Claude Code の場合:
  → 一度 exit で終了し、再度 claude を起動してください

Cursor の場合:
  → Cmd+Shift+P (Mac) / Ctrl+Shift+P (Windows) で
    コマンドパレットを開き「Reload Window」を実行してください
```

**AskQuestionの設定:**
```json
{
  "title": "Step 6: MCP接続テスト",
  "questions": [{
    "id": "restart_status",
    "prompt": "ツールを再起動しましたか？",
    "options": [
      {"id": "restarted", "label": "再起動しました！テストしてください"},
      {"id": "how_restart", "label": "再起動の方法がわからない"},
      {"id": "skip_test", "label": "テストをスキップする"}
    ]
  }]
}
```

(restarted → MCP接続テスト実行)

2. MCP接続テスト:
   - Notion MCPツールが利用可能か確認
   - 利用可能な場合: Notionのページ一覧を取得して接続成功を確認
   - 「Notionから X 件のページが取得できました。MCP接続は正常です」と表示

**テスト成功時:**
```text
Notion MCP の設定が完了しました！

テスト結果: MCPサーバー経由でNotionに正常に接続できました。
これで Claude Code/Cursor から直接 Notion のページ・データベースを操作できます。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "MCP接続テストでエラーが発生しました。考えられる原因を確認しましょう。",
    "options": [
      {"id": "retry", "label": "もう一度テストする"},
      {"id": "check_config", "label": "MCP設定ファイルを確認する"},
      {"id": "recheck_key", "label": "APIキーを確認し直す（Step 2に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行)
(check_config → MCP設定ファイルの内容を確認。NOTION_TOKEN がプレースホルダーのままでないか、JSONの構文が正しいか確認)
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
      {"id": "trouble_mcp_start", "label": "MCPサーバーが起動しない"},
      {"id": "trouble_invalid", "label": "「token_invalid」エラーが出る"},
      {"id": "trouble_permissions", "label": "「insufficient_permissions」エラーが出る"},
      {"id": "trouble_not_found", "label": "「object_not_found」エラーが出る"},
      {"id": "trouble_npx", "label": "npx コマンドが見つからない"},
      {"id": "trouble_cost", "label": "料金が心配"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: MCPサーバーが起動しない
**原因**: Node.js が未インストール、npx が使えない、MCP設定ファイルのJSONが壊れている
**AIが行うこと**:
1. `node --version` で Node.js の存在とバージョン（18以上必要）を確認
2. `npx --version` で npx が使えるか確認
3. MCP設定ファイルのJSONバリデーション（`python -m json.tool` で構文チェック）
4. Node.js 未インストールの場合: 「https://nodejs.org/ から LTS 版をインストールしてください」と案内

### トラブル2: 「token_invalid」エラー
**原因**: APIキーが正しくコピーされていない、またはキーが無効
**AIが行うこと**:
1. MCP設定ファイルを確認（キーの値は表示せず、`secret_` で始まっているかのみ確認）
2. プレースホルダー（`secret_your_token_here`）のままでないか確認
3. 問題がある場合: 「https://www.notion.so/my-integrations でトークンを再生成（Regenerate）してから、MCP設定ファイルを更新してください」と案内

### トラブル3: 「insufficient_permissions」エラー
**原因**: インテグレーションのCapabilities設定が不足、またはページに共有されていない
**AIが行うこと**:
1. 「https://www.notion.so/my-integrations でインテグレーションの Capabilities を確認してください。Read content / Update content / Insert content にチェックが入っていますか？」と案内
2. 「対象のNotionページにインテグレーションが共有されていますか？ Step 5の手順を再確認してください」と案内

### トラブル4: 「object_not_found」エラー
**原因**: 対象のページにインテグレーションが共有されていない
**AIの案内**: 「APIからアクセスしたいNotionページに、インテグレーションが共有されていません。Step 5の手順でページの「Add connections」からインテグレーションを追加してください。親ページに追加すると子ページにも適用されます」

### トラブル5: npx コマンドが見つからない
**原因**: Node.js がインストールされていない、または PATH が通っていない
**AIが行うこと**:
1. `node --version` で確認。未インストールなら https://nodejs.org/ を案内
2. インストール済みで PATH の問題なら、フルパス（`/usr/local/bin/npx`）を設定ファイルに記載する方法を案内

### トラブル6: 料金が心配
**AIの案内**: 「Notion自体は無料プランで利用可能です。API利用に追加費用はかかりません。無料プランでもAPIの全機能が使えます。Notion MCP サーバー（@notionhq/notion-mcp-server）も無料のオープンソースです」

### トラブル7: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] ncli（@sakasegawa/ncli）がインストールされている
- [ ] Notion Integrationsページでインテグレーション（AIAgent Bootcamp）を作成した
- [ ] Internal Integration Secret（secret_xxx）をコピーした
- [ ] MCP設定ファイルにNotionサーバーの設定を追加した
- [ ] アクセスしたいNotionページにインテグレーションを共有した
- [ ] Claude Code / Cursor を再起動した
- [ ] MCP接続テストが成功した（Notionページにアクセスできた）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "Notion MCPのセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "try_notion_mcp", "label": "Notion MCP操作を試す（/start-12-1）"},
      {"id": "try_notion_db", "label": "Notionデータベースを操作する（/start-12-2）"},
      {"id": "setup_other", "label": "他のAPIもセットアップする（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- try_notion_mcp → /start-12-1 を案内
- try_notion_db → /start-12-2 を案内
- setup_other → /start-0-1 を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-notion` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/start-12-1` でNotion MCP操作を試しましょう」

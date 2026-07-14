---
description: "Lesson command"
duration: "約10分"
prerequisites: ["Notionアカウントを持っている（無料プランでOK）", "ブラウザが使える", "Node.js 18以上"]
level: "beginner"
tags: ["setup", "notion", "ncli", "mcp", "oauth"]
nonInteractiveMode: incompatible
---

# Notion CLI (ncli) + Hosted MCP セットアップ（OAuth 統一）

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-notion` を実行して進捗を表示
2. 既存の設定を自動検出:
   - `which ncli` で ncli がインストール済みか確認
   - Claude Code の場合: `~/.claude/mcp_settings.json` に `notion` サーバーが定義されているか確認
   - Cursor の場合: `~/.cursor/mcp.json` に `notion` サーバーが定義されているか確認
   - ncli インストール済み＆MCP設定済みの場合、Step 6（接続テスト）のみ実行して完了にできる

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | ncli（Notion CLI）と Notion 公式の Hosted MCP を **OAuth 認証** で接続し、ターミナル＋MCP 経由で Notion を操作できるようにする |
| 所要時間 | 約10分 |
| 前提条件 | Notionアカウント（無料プランでOK）、Node.js 18以上、ブラウザ |
| 操作レベル | CLIコマンド入力なし（すべてAIが自動実行 + ブラウザでの OAuth 承認のみ） |
| 認証方式 | **このセットアップ手順では OAuth のみ**を使います（APIキー不要）。<br>※ 一部のレガシースクリプト（`tools/run_lesson_14_11.py` 等）は引き続き `NOTION_API_KEY` を要求します。詳細は `.env.example` を参照 |

**このセッションの流れ:**
1. ncli（@sakasegawa/ncli）をインストールする（AIが自動実行）
2. `ncli login` を実行してブラウザで Notion OAuth を承認する
3. `ncli whoami` / `ncli search` で動作確認する
4. MCP設定ファイルに Notion Hosted MCP（OAuth）を追加する（AIが自動作成）
5. Claude Code / Cursor を再起動 → 初回利用時に OAuth ダイアログを承認する
6. MCP接続テスト

> **Hosted MCP + OAuth に統一した理由**: 旧方式の Internal Integration Token は、Notion 上でインテグレーションを作成し、各ページに「Add connections」で個別に共有する必要がありました。OAuth ではブラウザでログインするだけで、ワークスペース全体への権限を一度に付与できるため、**この Hosted MCP 手順では**ページ単位の共有設定は **不要** です。なお、`NOTION_API_KEY` を直接読む旧スクリプト（`tools/run_lesson_14_11.py` 等）を実行する場合は、従来通り Internal Integration Token も併用してください。

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
      {"id": "which_tool", "label": "Claude Code と Cursor のどちらを使っているか確認したい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 「Notionアカウント（無料プランでOK）があり、ブラウザでログインできれば準備OKです。Node.js 18 以上もインストール済みであることを確認してください」と案内)
(which_tool → 「Claude Code を使っている場合と Cursor を使っている場合で MCP 設定ファイルの場所が異なります。Step 4 でそれぞれの手順を案内します」と説明)
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

## Step 2: ncli で Notion に OAuth ログインする

**AIが実行すること:**
1. ターミナルで以下を実行:

```bash
ncli login
```

2. ncli が自動でブラウザを開き、Notion の OAuth 認証画面が表示される
3. ユーザーは画面の案内に従って:
   - Notion にログイン（未ログインの場合）
   - 連携先のワークスペースを選択
   - 「Allow access」（アクセスを許可）をクリック
4. 承認が成功するとターミナルに「Logged in as ...」のような表示が出る

**ユーザーに案内するメッセージ:**

```text
ブラウザで Notion の OAuth 画面が開きました。

1. Notion にログインしていない場合はログインしてください
2. アクセスを許可するワークスペースを選択してください
3. 「Allow access」をクリックして承認してください

承認が完了するとブラウザのタブが自動で閉じ、ターミナルにログイン成功のメッセージが表示されます。

⚠️ APIキー（secret_xxx）の入力は不要です。すべてブラウザ上の OAuth で完了します。
```

**AskQuestionの設定:**
```json
{
  "title": "Step 2: Notion へ OAuth ログイン",
  "questions": [{
    "id": "login_status",
    "prompt": "ncli login の OAuth 認証は完了しましたか？",
    "options": [
      {"id": "logged_in", "label": "ログインできました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "login_denied", "label": "Notion にログインできない／承認に失敗した"},
      {"id": "wrong_workspace", "label": "別のワークスペースで承認してしまった"}
    ]
  }]
}
```

(logged_in → Step 3へ)
(browser_not_open → 「ターミナルに OAuth 用の URL が表示されているはずです。その URL を手動でブラウザにコピー＆ペーストしてアクセスしてください」と案内)
(login_denied → 「Notion アカウントをお持ちでない場合は https://www.notion.so/signup から無料で作成できます。承認後にエラーが出る場合は、もう一度 `ncli login` を実行してやり直してください」と案内)
(wrong_workspace → 「`ncli logout` でいったんログアウトしてから `ncli login` をやり直し、正しいワークスペースを選択してください」と案内)

---

## Step 3: ncli の動作確認（whoami / search）

**AIが実行すること:**
1. 現在のログイン状態を確認:

```bash
ncli whoami
```

2. ワークスペース内検索のスモークテスト（1〜2件取得できれば成功）:

```bash
ncli search ""
```

または検索キーワードを指定:

```bash
ncli search "test"
```

3. 結果が表示されればワークスペース全体への OAuth 権限が正しく付与されている

**AskQuestionの設定:**
```json
{
  "title": "Step 3: ncli の動作確認",
  "questions": [{
    "id": "smoke_test",
    "prompt": "whoami / search コマンドの結果は正常でしたか？",
    "options": [
      {"id": "ok", "label": "ユーザー名が表示され、検索結果も返ってきた"},
      {"id": "whoami_fail", "label": "whoami で「not logged in」のように表示される"},
      {"id": "search_empty", "label": "検索結果が0件だった"},
      {"id": "other_error", "label": "別のエラーが出た"}
    ]
  }]
}
```

(ok → Step 4へ)
(whoami_fail → 「`ncli login` をもう一度実行してください。複数アカウントを使い分けている場合は、`ncli logout` してからやり直すと確実です」と案内)
(search_empty → 「ワークスペース内にページがない場合は当然0件です。テスト用に Notion で1ページ作成してから再度 `ncli search` を試してください」と案内)
(other_error → エラーメッセージを確認し、原因を特定して案内)

---

## Step 4: MCP設定ファイルに Notion Hosted MCP（OAuth）を追加する

Notion 公式の Hosted MCP は `https://mcp.notion.com/mcp` でホストされており、Streamable HTTP + OAuth で認証します。設定ファイルにはトークンや環境変数を一切記載しません。

**AIが自動で実行すること:**

1. 使用ツールを判定する（Claude Code or Cursor）
2. 対応するMCP設定ファイルに `notion` エントリを追記する（既存の `mcpServers` は保持）

**AIが書き込むMCP設定ファイル:**

**Claude Code の場合:** `~/.claude/mcp_settings.json`
**Cursor の場合:** `~/.cursor/mcp.json`（ホームディレクトリ。リポジトリ内の `.cursor/mcp.json` には書き込まないこと）

設定内容（既存の `mcpServers` がある場合は `notion` エントリを追記）:
```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

**重要:**
- `command` / `args` / `env` は **不要**（Hosted MCP なのでローカル起動しない）
- `NOTION_TOKEN` などのシークレットは **設定しない**（OAuth で認証する）
- `type` は必ず `http`（Streamable HTTP）を指定する

**AskQuestionの設定:**
```json
{
  "title": "Step 4: MCP設定ファイルの作成",
  "questions": [{
    "id": "config_status",
    "prompt": "MCP設定ファイルに Notion エントリを追加できましたか？",
    "options": [
      {"id": "done", "label": "追加できました！"},
      {"id": "editor_help", "label": "ファイルの場所がわからない"},
      {"id": "existing_config", "label": "既に他のMCPサーバー設定があるので追記方法を知りたい"},
      {"id": "security_question", "label": "OAuth のセキュリティについて質問がある"}
    ]
  }]
}
```

(done → AI が設定ファイルを読み取り、`notion` エントリの `type` が `http`、`url` が `https://mcp.notion.com/mcp` になっていることを確認。`NOTION_TOKEN` や `command` が混入していないことも確認。OK なら Step 5 へ)
(editor_help → 「Mac: `open ~/.claude/mcp_settings.json` または `open ~/.cursor/mcp.json` で開けます。ファイルが存在しない場合は新規作成してください」と案内)
(existing_config → 既存ファイルの内容を読み取り、`mcpServers` オブジェクトに `notion` エントリを追記する。他のサーバー設定は保持する)
(security_question → 「Hosted MCP は Notion 公式が運用するサーバーで、認証はブラウザ OAuth で行います。トークンは設定ファイルに保存されず、各ツール（Claude Code / Cursor）の認証ストアで安全に管理されます」と説明)

---

## Step 5: ツールを再起動して OAuth ダイアログを承認する

**AIが案内するメッセージ:**

```text
MCP設定を反映するには、ツールの再起動が必要です。

Claude Code の場合:
  → 一度 exit で終了し、再度 claude を起動してください

Cursor の場合:
  → Cmd+Shift+P (Mac) / Ctrl+Shift+P (Windows) で
    コマンドパレットを開き「Reload Window」を実行してください

再起動後、初めて Notion MCP のツールを呼び出すタイミングで
ブラウザに Notion の OAuth 承認ダイアログが開きます。
「Allow access」をクリックして承認してください。
（一度承認すれば、以後は自動でログイン状態が保持されます）
```

**AskQuestionの設定:**
```json
{
  "title": "Step 5: 再起動と OAuth 承認",
  "questions": [{
    "id": "restart_status",
    "prompt": "ツールを再起動しましたか？",
    "options": [
      {"id": "restarted", "label": "再起動しました！次のテストへ"},
      {"id": "how_restart", "label": "再起動の方法がわからない"},
      {"id": "no_oauth_dialog", "label": "OAuth ダイアログが出てこない"}
    ]
  }]
}
```

(restarted → Step 6へ)
(how_restart → ツール別の再起動手順を再度案内)
(no_oauth_dialog → 「ダイアログは MCP ツールを **初めて呼び出したとき** に開きます。Step 6 のテストを実行すれば自動で表示されます。それでも開かない場合は、ツール側のログ（Claude Code: `claude --debug`、Cursor: 出力パネルの MCP）を確認してください」と案内)

---

## Step 6: MCP接続テスト

**AIが実行すること:**

1. Notion MCP ツール（例: `notion-search`、`notion-fetch` 等）が利用可能か確認
2. 簡単なリクエストを発行してワークスペースから情報を取得
3. 初回実行時はブラウザに OAuth 承認ダイアログが開くので承認してもらう
4. 結果として「Notion から N 件のページを取得しました。MCP 接続は正常です」と表示

**テスト成功時:**
```text
Notion Hosted MCP の設定が完了しました！

テスト結果: MCPサーバー経由で Notion に正常に接続できました。
これで Claude Code / Cursor から直接 Notion のページ・データベースを操作できます。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "MCP接続テストでエラーが発生しました。原因を確認しましょう。",
    "options": [
      {"id": "retry", "label": "もう一度テストする"},
      {"id": "check_config", "label": "MCP設定ファイルを確認する"},
      {"id": "reauth", "label": "OAuth を再承認する"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行。OAuth ダイアログが開いた場合は承認してもらう)
(check_config → MCP設定ファイルを確認。`type: "http"`、`url: "https://mcp.notion.com/mcp"` になっているか、JSON 構文が正しいか確認)
(reauth → ツールの認証ストアから Notion の認証情報をクリアして再起動するよう案内。Claude Code: `claude mcp logout notion` などツール側のコマンドを案内)
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
      {"id": "trouble_oauth_fail", "label": "OAuth 認証が失敗する"},
      {"id": "trouble_mcp_no_response", "label": "MCP サーバーから応答がない"},
      {"id": "trouble_no_pages", "label": "ページが取得できない（ワークスペース選択ミス）"},
      {"id": "trouble_ncli_login", "label": "ncli login がうまくいかない"},
      {"id": "trouble_cost", "label": "料金が心配"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: OAuth 認証が失敗する
**原因**: ブラウザ側でポップアップがブロックされている、または Notion 側で承認をキャンセルした
**AIが行うこと**:
1. ブラウザでポップアップ／リダイレクトが許可されているか確認するよう案内
2. もう一度 `ncli login` または MCP のツール呼び出しを実行して OAuth をやり直す
3. それでも失敗する場合は、ブラウザの Notion セッションを一度ログアウトしてから再試行する

### トラブル2: MCP サーバーから応答がない
**原因**: MCP 設定ファイルの記述ミス、ツールの再起動忘れ、ネットワーク経路で `https://mcp.notion.com` がブロックされている
**AIが行うこと**:
1. MCP 設定ファイルを確認（`type: "http"`、`url: "https://mcp.notion.com/mcp"` か）
2. JSON の構文を検証（Claude Code: `python -m json.tool ~/.claude/mcp_settings.json` / Cursor: `python -m json.tool ~/.cursor/mcp.json`）
3. ツール（Claude Code / Cursor）を完全に再起動する
4. `curl -I https://mcp.notion.com/mcp` でネットワーク到達性を確認

### トラブル3: ページが取得できない
**原因**: OAuth 承認時に意図しないワークスペースを選んだ
**AIが行うこと**:
1. `ncli logout` → `ncli login` で正しいワークスペースを選び直すよう案内
2. MCP 側でも同様に、ツールの認証ストアから Notion をログアウトしてから再認証する

### トラブル4: ncli login がうまくいかない
**原因**: Node.js のバージョン不足、ncli が古い、または OAuth 用のリスナーポートが他プロセスで使用中
**AIが行うこと**:
1. `node --version` で 18 以上を確認
2. `npm install -g @sakasegawa/ncli@latest` で最新版に更新
3. ポート競合の場合は他のローカルサーバー（特に開発サーバー）を停止してから再試行

### トラブル5: 料金が心配
**AIの案内**: 「Notion 自体は無料プランで利用可能です。OAuth 経由の API 利用にも追加費用はかかりません。Notion 公式 Hosted MCP（`mcp.notion.com`）も**現時点では**無料で利用できますが、ツールごとの利用可否は Notion のプラン（Free / Plus / Business / Enterprise）や Notion AI の有効化状況によって変わる場合があります。最新の対応範囲は公式の [MCP supported tools ドキュメント](https://developers.notion.com/docs/mcp-supported-tools) と [Notion 料金ページ](https://www.notion.com/pricing) を確認してください。ncli（@sakasegawa/ncli）はオープンソースで無料です」

### トラブル6: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] ncli（@sakasegawa/ncli）がインストールされている
- [ ] `ncli login` でブラウザ OAuth 認証が完了している
- [ ] `ncli whoami` でログインユーザーが表示される
- [ ] `ncli search` でワークスペース内のページが取得できる
- [ ] MCP 設定ファイルに `notion`（`type: http`、`url: https://mcp.notion.com/mcp`）が追加されている
- [ ] Claude Code / Cursor を再起動した
- [ ] MCP 接続テストが成功した（OAuth 承認後に Notion ページにアクセスできた）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "Notion MCP のセットアップが完了しました！次はどうしますか？",
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
3. ユーザーに次のステップを案内: 「次は `/start-12-1` で Notion MCP 操作を試しましょう」

---
description: "Pencil MCP セットアップ（ダウンロード・設定ガイド）"
duration: "約15分"
prerequisites: ["ブラウザが使える", "Claude Code または Cursor が導入済み"]
level: "beginner"
tags: ["setup", "pencil", "mcp", "design"]
---

# Pencil MCP セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-pencil` を実行して進捗を表示
2. 既存の設定を自動検出:
   - Claude Code の場合: `~/.claude/mcp_settings.json` に `pencil` サーバーが定義されているか確認
   - Cursor の場合: `.cursor/mcp.json` に `pencil` サーバーが定義されているか確認
   - 設定済みの場合、Step 4（接続テスト）のみ実行して完了にできる

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Pencil デスクトップアプリをインストールし、MCP サーバー経由で Claude Code/Cursor からデザインファイル（.pen）を操作できるようにする |
| 所要時間 | 約15分 |
| 前提条件 | ブラウザが使えること、Claude Code または Cursor が導入済みであること |
| 操作レベル | アプリインストール + MCP設定（AIが自動支援） |

**このセッションの流れ:**
1. Pencil デスクトップアプリをダウンロード・インストール
2. Pencil アプリを起動して初期設定
3. MCP設定ファイルに Pencil サーバーを追加
4. MCP接続テスト

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
      {"id": "already_installed", "label": "Pencilは既にインストール済み"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 「Claude Code または Cursor が導入済みであれば準備OKです」と案内)
(already_installed → Step 3（MCP設定）へスキップ)
(different_lesson → モジュール一覧を表示)

---

## Step 1: Pencil デスクトップアプリのダウンロード

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. ブラウザで Pencil ダウンロードページを開く:

```bash
# Mac:
open https://pencil.evolves.dev/download
# Windows:
start https://pencil.evolves.dev/download
# Linux:
xdg-open https://pencil.evolves.dev/download
```

**ブラウザが開いたら、以下のAskQuestionを表示:**

```json
{
  "title": "Step 1: Pencil アプリのダウンロード",
  "questions": [{
    "id": "download_status",
    "prompt": "ブラウザで Pencil のダウンロードページが開きましたか？\n\n手順:\n1. お使いのOS（Mac / Windows）に合ったインストーラーをダウンロード\n2. ダウンロードしたファイルを実行してインストール\n   - Mac: .dmg を開いてアプリケーションフォルダにドラッグ\n   - Windows: .exe を実行してウィザードに従う\n\nインストールできましたか？",
    "options": [
      {"id": "installed", "label": "インストールしました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "download_issue", "label": "ダウンロードできない"},
      {"id": "mac_security", "label": "Macのセキュリティ警告が出る"}
    ]
  }]
}
```

(installed → Step 2へ)
(browser_not_open → 「ブラウザで直接このURLを開いてください: https://pencil.evolves.dev/download」と案内)
(download_issue → 「インターネット接続を確認してください。ダウンロードが遅い場合は少しお待ちください」と案内)
(mac_security → 「システム設定 → プライバシーとセキュリティ → 「このまま開く」をクリックしてください。または、Finderでアプリを右クリック→「開く」を選択してください」と案内)

---

## Step 2: Pencil アプリの起動と初期設定

**ユーザーに案内するメッセージ:**

```text
Pencil アプリを起動してください:

┌─────────────────────────────────────────────────────────────┐
│ 1. アプリケーションから「Pencil」を起動                      │
│ 2. 初回起動時にアカウント作成またはログインが必要な場合は    │
│    画面の指示に従ってください                                │
│ 3. エディター画面が表示されたらOKです                        │
│                                                             │
│ ※ Pencil は .pen 形式のデザインファイルを作成・編集する     │
│   デスクトップアプリです                                    │
└─────────────────────────────────────────────────────────────┘
```

**AskQuestionの設定:**
```json
{
  "title": "Step 2: Pencil アプリの起動",
  "questions": [{
    "id": "app_status",
    "prompt": "Pencil アプリを起動できましたか？",
    "options": [
      {"id": "running", "label": "Pencilが起動しています！"},
      {"id": "cant_find", "label": "アプリが見つからない"},
      {"id": "crash", "label": "起動するとクラッシュする"},
      {"id": "login_issue", "label": "ログイン/アカウント作成で困っている"}
    ]
  }]
}
```

(running → Step 3へ)
(cant_find → Mac: 「アプリケーション」フォルダ / Windows: スタートメニューを確認。インストールが完了していなければ Step 1 に戻る)
(crash → 「OSが最新か確認してください。問題が続く場合は、一度アンインストールして再インストールしてください」と案内)
(login_issue → 「Pencil の公式サイト（https://pencil.evolves.dev）でアカウントを作成できます。メールアドレスで登録できます」と案内)

---

## Step 3: MCP設定ファイルに Pencil サーバーを追加

**AIが自動で実行すること:**

1. 使用ツールを判定する（Claude Code or Cursor）
2. Pencil MCP サーバーの設定方法を案内する

**Pencil MCP の接続方式:**

Pencil MCP は Pencil デスクトップアプリに内蔵されています。アプリが起動していれば、MCP サーバーとして自動的に利用可能になります。

**Claude Code の場合:** `~/.claude/mcp_settings.json` に以下を追加:
```json
{
  "mcpServers": {
    "pencil": {
      "url": "http://localhost:13742/sse"
    }
  }
}
```

**Cursor の場合:** `~/.cursor/mcp.json` に以下を追加:
```json
{
  "mcpServers": {
    "pencil": {
      "url": "http://localhost:13742/sse"
    }
  }
}
```

> **注意**: 既存の MCP 設定ファイルがある場合は、`mcpServers` 内に `pencil` エントリを追記してください。他のサーバー設定は削除しないでください。

**AskQuestionの設定:**
```json
{
  "title": "Step 3: MCP設定",
  "questions": [{
    "id": "config_status",
    "prompt": "MCP設定ファイルに Pencil サーバーの設定を追加しましたか？",
    "options": [
      {"id": "done", "label": "設定を追加しました！"},
      {"id": "auto_setup", "label": "AIに自動で設定してほしい"},
      {"id": "existing_config", "label": "既に設定ファイルがあるので追記方法を知りたい"},
      {"id": "help", "label": "設定方法がわからない"}
    ]
  }]
}
```

(done → Step 4へ)
(auto_setup → AIが自動で設定ファイルを作成/更新する。既存のサーバー設定は保持する)
(existing_config → 既存ファイルの内容を読み取り、`mcpServers` に `pencil` エントリを追記する方法を案内)
(help → ツール別の詳細手順を案内)

---

## Step 4: MCP接続テスト

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
  "title": "Step 4: MCP接続テスト",
  "questions": [{
    "id": "restart_status",
    "prompt": "ツールを再起動しましたか？（Pencil アプリも起動中であることを確認してください）",
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
   - `get_editor_state()` を実行してPencilの状態を取得
   - 接続成功: 「Pencil MCP に正常に接続できました」と表示
   - 接続失敗: トラブルシューティングへ

**テスト成功時:**
```text
Pencil MCP の設定が完了しました！

テスト結果: Pencil MCP サーバーに正常に接続できました。
これで Claude Code/Cursor から直接 .pen ファイルを作成・編集できます。

利用可能なツール:
- get_editor_state(): エディター状態の取得
- open_document(): ドキュメントの作成/オープン
- batch_design(): デザイン要素の挿入・更新・削除
- get_screenshot(): スクリーンショットの取得
- get_guidelines(): デザインガイドラインの取得
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
      {"id": "check_app", "label": "Pencilアプリが起動しているか確認"},
      {"id": "check_config", "label": "MCP設定ファイルを確認する"},
      {"id": "check_port", "label": "ポート13742が使えるか確認"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry → テストを再実行)
(check_app → 「Pencilアプリが起動していないとMCPサーバーに接続できません。Pencilアプリを起動してから再度テストしてください」と案内)
(check_config → MCP設定ファイルの内容を確認。URLが正しいか、JSONの構文が正しいか確認)
(check_port → `lsof -i :13742` でポートの使用状況を確認)
(skip_test → 「テストはスキップしました。Lesson 13-3 で Pencil MCP を使う際に接続を確認します」と案内)

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
      {"id": "trouble_connect", "label": "MCPサーバーに接続できない"},
      {"id": "trouble_app", "label": "Pencilアプリが起動しない"},
      {"id": "trouble_port", "label": "ポートが既に使われている"},
      {"id": "trouble_cost", "label": "料金が心配"}
    ]
  }]
}
```

### トラブル1: MCPサーバーに接続できない
**原因**: Pencilアプリが起動していない、またはMCP設定のURLが間違っている
**AIが行うこと**:
1. Pencilアプリが起動しているか確認を案内
2. MCP設定ファイルのURLが `http://localhost:13742/sse` になっているか確認
3. `lsof -i :13742` でポートのリスニング状態を確認

### トラブル2: Pencilアプリが起動しない
**原因**: インストールが不完全、またはOSの互換性
**AIが行うこと**:
1. OSバージョンの確認
2. 再インストールを案内
3. Macのセキュリティ設定を確認（Gatekeeper）

### トラブル3: ポートが既に使われている
**原因**: 別のプロセスがポート13742を使用している
**AIが行うこと**:
1. `lsof -i :13742` で使用中のプロセスを確認
2. 競合するプロセスの停止を案内

### トラブル4: 料金が心配
**AIの案内**: 「Pencilアプリには無料プランがあります。MCP連携を含む基本機能は無料で利用可能です。詳細は https://pencil.evolves.dev を確認してください」

---

## チェックポイント
- [ ] Pencil デスクトップアプリをダウンロード・インストールした
- [ ] Pencil アプリが正常に起動する
- [ ] MCP設定ファイルに Pencil サーバーの設定を追加した
- [ ] Claude Code / Cursor を再起動した
- [ ] MCP接続テストが成功した（get_editor_state が動作した）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "Pencil MCPのセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "start_design", "label": "LP デザインを開始する（/start-13-3）"},
      {"id": "try_pencil", "label": "Pencilの基本操作を試してみる"},
      {"id": "setup_other", "label": "他のAPIもセットアップする（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- start_design → /start-13-3 を案内
- try_pencil → get_editor_state, open_document, batch_design の基本操作を案内
- setup_other → /start-0-1 を案内
- finish → 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-pencil` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/start-13-3` でPencilを使ったLPデザインを始めましょう」

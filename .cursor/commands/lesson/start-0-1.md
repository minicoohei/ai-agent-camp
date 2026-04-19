---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "約15分"
prerequisites: ["Codex Desktop または Cursor をインストール済み", "ai-agent-camp フォルダを開いている"]
level: "beginner"
tags: ["setup", "environment"]
---

# Lesson 0-1: 環境セットアップ確認

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Codex で学習を始められるよう、Node.js / Python / GitHub CLI を含む環境が整っているかチェックする |
| 所要時間 | 約15分 |
| 前提条件 | Codex Desktop または Cursor をインストール済み、ai-agent-camp フォルダを開いている |
| 教材ページ | [コース教材トップ](https://ai-agent.camp/ja/course/module-0) を並行参照 |

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## セットアップ方法

このレッスンでは、以下の2つのコマンドを使って環境を整えます。
**ターミナルの操作は一切不要です。全てAIが自動で実行します。**
もしAIが「ターミナルで実行してください」と案内した場合は [ターミナル入門ガイド](../../../docs/terminal-guide.md) を参照してください。

> **Codex向けメモ**: Codex では `/setup-start` や `/check-setup` を Cursor の slash command として直接実行するのではなく、このファイルに書かれた確認内容を順番に実行します。ブラウザ認証など GUI 操作が必要になったら、その時点でユーザー操作に切り替えます。

### Step 1: セットアップ開始

まず `/setup-start` を実行してください。このコマンドは以下を**AIが全自動で**行います:

- OS の判定（Mac / Windows）
- Python / Node.js / Git / GitHub CLI の有無とバージョン確認
- 不足しているツールがあればGUIインストーラーのURLを案内

**AskQuestionの設定:**
```json
{
  "title": "Step 1: セットアップ開始",
  "questions": [{
    "id": "action",
    "prompt": "環境のセットアップを始めましょう。何をしますか？",
    "options": [
      {"id": "run_setup", "label": "セットアップを始める（/setup-start を実行）"},
      {"id": "run_check", "label": "環境チェックだけ行う（/check-setup を実行）"},
      {"id": "already_done", "label": "既にセットアップ済み"},
      {"id": "view_html", "label": "先に教材ページを見たい"}
    ]
  }]
}
```

(run_setup → `/setup-start` の内容を実行する)
(run_check → `/check-setup` の内容を実行する)
(already_done → Step 2 へ)
(view_html → 教材ページのパス `https://ai-agent.camp/ja/course/module-0` を案内)

---

### Step 2: GitHub設定と自分用リポジトリの作成

`/setup-github` を実行してください。このコマンドは以下を**AIが全自動で**行います:

- GitHub アカウントの有無確認
- ブラウザを自動起動して GitHub ログイン（`gh auth login --web`）
- 自分用の private リポジトリを自動作成

**AskQuestionの設定:**
```json
{
  "title": "Step 2: GitHub設定",
  "questions": [{
    "id": "github_action",
    "prompt": "GitHub の設定を行います。何をしますか？",
    "options": [
      {"id": "run_github", "label": "GitHub設定を始める（/setup-github を実行）"},
      {"id": "already_done", "label": "既に GitHub にログイン済み＆自分用リポあり"},
      {"id": "skip", "label": "スキップして次のレッスンへ"}
    ]
  }]
}
```

(run_github → `/setup-github` の内容を実行する)
(already_done → 完了チェックへ)
(skip → 次のステップへ)

---

### Step 3: 環境の総合チェック

全てのセットアップが完了したら、`/check-setup` で環境の状態を確認します。
AIが以下を全て自動でチェックし、レポートを表示します:

- 基本ツール（Python, Node.js, Git, GitHub CLI）
- 認証・API（GitHub認証, Gemini API, Slack API）
- プロジェクト設定（.env, .gitignore, セキュリティフック）
- 拡張機能

問題がある項目は、AIが自動修復するか、対応するセットアップコマンドへ誘導します。

---

## 実行コマンド

```text
/setup-start
/setup-github
/check-setup
```

## 期待される出力例

```text
環境チェックレポート
| 項目       | 状態 | 詳細          |
|-----------|------|--------------|
| Python    | OK   | 3.12.x       |
| Node.js   | OK   | 24.x         |
| Git       | OK   | 2.x          |
| GitHub CLI | OK  | ログイン済み   |
```

## よくあるトラブル
- AIの応答が止まる → 「続きを表示して」と入力
- GitHub認証が失敗する → `/setup-github` を再実行
- ツールが見つからない → AIが案内するインストーラーURLからインストール

---

## チェックポイント
- [ ] Codex Desktop または Cursor が起動する
- [ ] Python 3.9 以上がインストールされている
- [ ] Node.js 18 以上がインストールされている
- [ ] Git がインストールされている
- [ ] GitHub CLI にログインしている
- [ ] 自分の private リポジトリに push 済み

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next", "label": "拡張機能をインストールする（/start-0-2）"},
      {"id": "gemini", "label": "Gemini APIを設定する（/start-0-3）"},
      {"id": "check", "label": "環境チェックをする（/check-setup）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(next → /start-0-2 を案内)
(gemini → /start-0-3 を案内)
(check → /check-setup の内容を実行する)
(finish → 終了)

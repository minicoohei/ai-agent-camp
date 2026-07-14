---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "約15分"
prerequisites: ["Node.js 18以上がインストール済み", "[ターミナル操作に慣れている](../../../docs/terminal-guide.md)"]
level: "beginner"
tags: ["setup", "claude-code", "cli"]
nonInteractiveMode: incompatible
---
# Lesson 0-7: Claude Code セットアップ

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Claude Code をインストールし、認証・プロジェクト初期化を完了する。スラッシュコマンドとスキルの使い方を理解する |
| 所要時間 | 約15分 |
| 前提条件 | Node.js 18以上がインストール済み、ターミナル操作に慣れている |
| 教材ページ | [コース教材トップ](https://ai-agent.camp/ja/course/module-0) を並行参照 |

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## Claude Code とは

Claude Code は Anthropic 公式の CLI ツールです。ターミナルから直接 Claude を呼び出し、コード編集・ファイル操作・コマンド実行を自然言語で行えます。

Cursor との違い:
- **Cursor**: GUI エディタ内で AI を利用（チャット・インライン編集）
- **Claude Code**: ターミナルから AI を利用（CLI ベース・自動化向き）

どちらのツールでもこのカリキュラムのレッスンを受講できます。

---

## Step 1: インストール

Claude Code を npm でグローバルインストールします。

```bash
npm install -g @anthropic-ai/claude-code
```

インストール後、バージョンを確認します:

```bash
claude --version
```

**AskQuestionの設定:**
```json
{
  "title": "Step 1: インストール",
  "questions": [{
    "id": "install_status",
    "prompt": "Claude Code のインストール状況を教えてください",
    "options": [
      {"id": "not_installed", "label": "今からインストールする（上記コマンドを実行）"},
      {"id": "already_installed", "label": "既にインストール済み"},
      {"id": "error", "label": "インストールでエラーが出た"}
    ]
  }]
}
```

(not_installed → `npm install -g @anthropic-ai/claude-code` を実行し、結果を確認)
(already_installed → Step 2 へ)
(error → `node --version` で Node.js 18以上か確認。npm キャッシュクリア `npm cache clean --force` を案内)

---

## Step 2: 認証（OAuth ログイン）

Claude Code は初回起動時に自動で認証フローが開始されます。以下のコマンドを実行するとブラウザが開きます:

```bash
claude
```

ブラウザで Anthropic アカウントにログインし、認証を完了してください。

> **注意**: Claude Pro / Max / Team / Enterprise プランが必要です。無料プランでは利用できません。
>
> **API キーで認証する場合**: 先に `source ./.env`（`.env` に `ANTHROPIC_API_KEY` を設定済みの場合）を実行してから `claude` を起動してください。
>
> **セッション内で再認証が必要な場合**: Claude Code のチャット内で `/login` と入力してください。

**AskQuestionの設定:**
```json
{
  "title": "Step 2: 認証",
  "questions": [{
    "id": "auth_status",
    "prompt": "認証の状況を教えてください",
    "options": [
      {"id": "run_auth", "label": "認証を始める（claude を実行）"},
      {"id": "already_authed", "label": "既に認証済み"},
      {"id": "api_key", "label": "API キーで認証したい"},
      {"id": "error", "label": "認証でエラーが出た"}
    ]
  }]
}
```

(run_auth → `claude` を実行。初回起動時にブラウザが開き認証フローが始まる)
(already_authed → Step 3 へ)
(api_key → `.env` に `ANTHROPIC_API_KEY=sk-ant-...` を設定し、`source ./.env` を実行してから `claude` を起動する手順を案内)
(error → `claude auth status` で状態を確認し、トラブルシュートを案内。セッション内では `/login` で再認証可能)

---

## Step 3: プロジェクト初期化

ai-agent-camp リポジトリのルートで `claude` を起動します:

```bash
cd /path/to/ai-agent-camp
claude
```

初回起動時、Claude Code は以下を自動的に行います:

1. `CLAUDE.md` を読み込んでプロジェクト設定を理解
2. `.claude/commands/` 配下のコマンドを認識
3. `skills/` 配下のスキルを認識

---

## Step 4: スラッシュコマンドの使い方

Claude Code では **`/コマンド名`** でレッスンやユーティリティを呼び出せます。

### レッスンの開始方法

```text
/start-0-1    → 環境セットアップ確認
/start-0-7    → このレッスン（Claude Code セットアップ）
/start-1-1    → バナー生成入門
```

### ユーティリティコマンド

```text
/check-setup  → 環境の総合チェック
/overview     → プロジェクト全体の概要
```

> **ポイント**: Cursor の場合は Cmd+Shift+P → コマンドパレットから実行しますが、Claude Code ではチャット内で直接 `/コマンド名` を入力するだけです。

**AskQuestionの設定:**
```json
{
  "title": "Step 4: コマンドの確認",
  "questions": [{
    "id": "command_check",
    "prompt": "スラッシュコマンドを試してみましょう",
    "options": [
      {"id": "try_check", "label": "/check-setup を試す"},
      {"id": "understood", "label": "理解した、次へ進む"},
      {"id": "more_info", "label": "もっと詳しく知りたい"}
    ]
  }]
}
```

(try_check → `/check-setup` の内容を実行する)
(understood → Step 5 へ)
(more_info → `.claude/commands/lesson/` 配下のファイル一覧を表示し、各コマンドの説明を案内)

---

## Step 5: スキルシステムの理解

Claude Code の **スキル** は、特定のタスクを実行するための専門モジュールです。`skills/` 配下に格納されています。

### スキルとスラッシュコマンドの違い

| 機能 | 仕組み | 例 |
|------|--------|-----|
| **スラッシュコマンド** (`/command`) | `.claude/commands/` 内のファイルを実行 | `/start-0-1`, `/check-setup` |
| **スキル** | 自然言語のトリガーフレーズで自動選択 | 「バナーを作って」→ banner-creator |

> **重要**: スキルは `/skill-name` のようなスラッシュコマンドでは呼び出せません。スラッシュコマンドは `.claude/commands/` 内のファイル専用です。

### スキルの呼び出し方

スキルは **自然言語でタスクを依頼** すると、各スキルの `SKILL.md` に定義されたトリガーフレーズに基づいて自動的に選択されます:

```text
「バナーを作って」       → banner-creator が自動選択される
「データを分析して」     → data-analyst が自動選択される
「スクショに注釈をつけて」→ screenshot-annotator が自動選択される
```

> **ポイント**: 特定のスキルを確実に使いたい場合は、そのスキルのトリガーフレーズ（例: 「バナー作成」「データ分析」）を含めて依頼してください。

### 利用可能なスキルの確認

```text
「どのスキルが使えるか教えて」と入力
```

---

## Step 6: CLAUDE.md の役割

`CLAUDE.md` はプロジェクトのルートに配置される設定ファイルです。Claude Code が最初に読み込み、以下を理解します:

- プロジェクトのルール・規約
- 利用可能なスキルの一覧
- コマンドの実行方法
- セキュリティポリシー

> **重要**: CLAUDE.md を編集することで、Claude Code の動作をカスタマイズできます。これは Module 6（Agent Development）で詳しく学びます。

---

## 推奨ワークフロー

Claude Code でこのカリキュラムを進める際の推奨手順:

1. **CLAUDE.md を確認**: プロジェクトのルールとスキル一覧を把握
2. **環境チェック**: `/check-setup` で環境が整っているか確認
3. **レッスン開始**: `/start-{module}-{lesson}` でレッスンを開始
4. **スキルを活用**: レッスン内で必要なスキルは自動的に呼び出される

---

## 権限モードの設定（推奨: Auto Mode）

Claude Code にはツール実行時の権限確認モードがあります。このカリキュラムでは **Auto Mode** の使用を推奨します。

### モード一覧

| モード | 起動方法 | 動作 |
|--------|---------|------|
| **Default** | `claude` | ファイル編集・コマンド実行のたびに確認を求める |
| **Auto-accept edits** | チャット内で `/permissions` → acceptEdits | ファイル編集は自動承認、コマンド実行は確認あり |
| **Auto Mode (推奨)** | チャット内で `/permissions` → auto | 許可ルールに基づいて自動承認 |
| **Full auto** | `claude --dangerously-skip-permissions` | 全操作を確認なしで実行 |

### Auto Mode の設定手順

Claude Code 起動後、チャット内で以下を入力します:

```text
/permissions
```

表示されるメニューから **auto** を選択してください。

> **リスクについて**: Auto Mode では、許可ルールに合致する操作（ファイル編集、シェルコマンド実行など）が確認なしで実行されます。意図しないファイルの変更やコマンド実行が行われる可能性があります。このカリキュラムはローカル環境の学習用リポジトリで使用する前提のため Auto Mode を推奨していますが、**本番環境や機密データを含むリポジトリでは Default モードを使用してください**。
>
> `--dangerously-skip-permissions`（Full auto）はすべての安全確認をスキップするため、学習目的であっても通常は不要です。

---

## 実行コマンド

```text
npm install -g @anthropic-ai/claude-code
claude
/check-setup
```

## 期待される出力例

```text
$ claude --version
2.x.x (Claude Code)

$ claude auth status
{
  "loggedIn": true,
  "authMethod": "claude.ai",
  "apiProvider": "firstParty",
  "email": "your-email@example.com",
  ...
}

$ claude
╭─────────────────────────────────────╮
│ ✻ Welcome to Claude Code!          │
│                                     │
│   /help for available commands      │
╰─────────────────────────────────────╯
```

## よくあるトラブル
- `npm install` が失敗する → Node.js 18以上か `node --version` で確認
- 認証できない → Pro / Max / Team / Enterprise プランか確認
- コマンドが認識されない → リポジトリルートで `claude` を起動しているか確認。`.claude/commands/` にファイルを追加・変更した場合は、Claude Code を一度終了（`/exit` または Ctrl+C）して再起動してください
- スキルが見つからない → `skills/` ディレクトリが存在するか確認

---

## チェックポイント
- [ ] Claude Code がインストールされている（`claude --version` が動作する）
- [ ] OAuth 認証が完了している（`claude auth status` でログイン済み）
- [ ] ai-agent-camp リポジトリで `claude` が起動できる
- [ ] `/check-setup` が実行できる
- [ ] スラッシュコマンドの使い方を理解している
- [ ] スキルシステムの概要を理解している
- [ ] 権限モード（Auto Mode）を設定した

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "Claude Code のセットアップが完了しました。次に何をしますか？",
    "options": [
      {"id": "check", "label": "環境チェックをする（/check-setup）"},
      {"id": "start_lesson", "label": "最初のレッスンを始める（/start-1-1: バナー生成）"},
      {"id": "overview", "label": "プロジェクト全体を確認する（/overview）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(check → /check-setup の内容を実行する)
(start_lesson → /start-1-1 を案内)
(overview → /overview を案内)
(finish → 「お疲れさまでした。いつでも /start-1-1 で最初のレッスンを始められます」と表示)

---

## 補足: Claude for Chrome の活用

Claude Code を使うには Claude Pro / Team / Enterprise プランが必要です。つまり、**あなたは既に Claude を利用できます！**

ブラウザでの作業効率を上げるために「Claude for Chrome」拡張機能の導入をおすすめします。

### インストール方法
1. Chrome ウェブストアで「Claude」を検索
2. 「Claude」（Anthropic公式）をインストール
3. ブラウザ右上の拡張機能アイコンからClaudeにアクセス

### 主な使い方
- **Webページの要約**: 長い記事やドキュメントの要約
- **コード理解**: GitHub 上のコードの説明
- **翻訳**: 英語ドキュメントの日本語化
- **リサーチ**: 技術調査やAPI仕様の確認

### Claude Code との使い分け
| シーン | 推奨ツール |
|--------|----------|
| ターミナルでコード編集・実行 | Claude Code |
| ブラウザでドキュメント読解 | Claude for Chrome |
| API仕様書の確認・理解 | Claude for Chrome |
| ファイル操作・Git操作 | Claude Code |
| Webページの情報抽出 | Claude for Chrome |

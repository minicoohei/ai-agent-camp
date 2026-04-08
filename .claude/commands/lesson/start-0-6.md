---
description: "When the user says /start-0-6 — Module 0 Lesson 0-6: Codex CLI セットアップ"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "約15分"
prerequisites: ["Node.js 18以上がインストールされている", "OpenAI APIキーを取得済み"]
level: "beginner"
tags: ["setup", "codex", "cli"]
---

# Lesson 0-6: Codex CLI セットアップ

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Codex CLI をインストール・認証し、ai-agent-camp でレッスンを実行できる状態にする |
| 所要時間 | 約15分 |
| 前提条件 | Node.js 18以上、OpenAI APIキーを取得済み |
| 教材ページ | [コース教材トップ](https://ai-agent.camp/ja/course/module-0) を並行参照 |

> **ヒント**: このレッスンは Codex CLI ユーザー向けです。Cursor ユーザーは Lesson 0-1 から始めてください。

---

## Step 1: Codex CLI のインストール

Codex CLI は npm でインストールします。ターミナルで以下を実行してください:

**推奨: npx で直接実行（インストール不要）**

```bash
npx @openai/codex --version
```

npx を使えばグローバルインストールなしで最新版を実行できます。

**代替: グローバルインストール**

nvm や fnm を使っている場合は sudo 不要です:

```bash
npm install -g @openai/codex
codex --version
```

> **注意**: Node.js 18以上が必要です。`node --version` で確認してください。
> 権限エラーが出る場合は、[npm 公式ガイド](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally) を参照して prefix を変更してください。`sudo npm install -g` は推奨されません。

---

## Step 2: 認証（OpenAI API キー）

Codex CLI は OpenAI API キーで認証します。以下のいずれかの方法で設定してください:

### 方法A: credential_manager を使用（推奨）

`tools/credential_manager.py` を使うと、APIキーを安全に管理できます:

```bash
uv run python tools/credential_manager.py store OPENAI_API_KEY
```

プロンプトに従ってキーを入力すると、暗号化されたキーストアに保存されます。

### 方法B: 環境変数で設定

```bash
export OPENAI_API_KEY="your-api-key-here"
```

`.bashrc` や `.zshrc` に追記すると永続化できます。

### 方法C: .env ファイルで設定（fallback）

上記の方法が使えない場合のみ、ai-agent-camp リポジトリの `.env` に以下を追加:

```dotenv
OPENAI_API_KEY=your-api-key-here
```

> **セキュリティ警告**: `.env` ファイルには秘密情報が含まれます。**絶対に Git にコミットしないでください。** `.gitignore` に `.env` が含まれていることを必ず確認してください。誤ってコミットすると、APIキーが漏洩するリスクがあります。

---

## Step 3: ランタイム設定

Codex CLI の推奨設定は以下の通りです:

Codex CLI の承認モードは `-a`（`--ask-for-approval`）で指定します:

| 承認モード | 説明 |
|-----------|------|
| `on-request` | モデルがユーザー承認を求めるタイミングを自動判断する（学習時の推奨） |
| `never` | 確認なしで自動実行（上級者向け、非推奨） |

起動コマンド例:

```bash
codex -a on-request
```

> **重要**: サンドボックスは Codex が自動管理します。詳細な設定は `AGENTS.md` の推奨設定に従ってください。`never` モードは通常の学習フローでは使用しないでください。詳しくは `docs/codex-safety.md` を参照。

---

## Step 4: Codex でのレッスン実行方法

Cursor では `/start-0-1` のようなスラッシュコマンドでレッスンを開始しますが、Codex CLI では代わりに **スキル** を使います。

### スラッシュコマンドとスキルの対応表

| Cursor コマンド | Codex での方法 |
|----------------|---------------|
| `/overview` | `aiagent-guide` スキルを使用 |
| `/check-setup` | `aiagent-check-setup` スキルを使用 |
| `/start-0-1` | `aiagent-lesson-runner` スキルで `start-0-1` を指定 |
| `/setup-security` | `aiagent-tooling-setup` スキルを使用 |

### 使い方

Codex CLI を起動し、以下のように依頼してください:

```text
aiagent-lesson-runner スキルを使って start-0-1 レッスンを開始してください
```

または:

```text
start-0-1 のレッスンを始めたい
```

Codex は `AGENTS.md` と `skills/` ディレクトリを自動的に認識し、適切なスキルを使用します。

---

## Step 5: 動作確認

以下の手順で Codex CLI が正しく動作するか確認します:

1. **ai-agent-camp ディレクトリで Codex を起動**:
   ```bash
   cd /path/to/ai-agent-camp
   codex
   ```

2. **リポジトリのフック設定を確認**:
   ```text
   bash scripts/install_hooks.sh を実行してください
   ```

3. **セットアップ確認スキルを実行**:
   ```text
   aiagent-check-setup スキルで環境を確認してください
   ```

---

## 期待される出力例

```text
環境チェックレポート
| 項目        | 状態 | 詳細            |
|------------|------|----------------|
| Node.js    | OK   | 22.x           |
| Codex CLI  | OK   | 1.x.x          |
| OpenAI API | OK   | 認証済み         |
| Git        | OK   | 2.x            |
| Hooks      | OK   | pre-commit 設定済み |
```

## よくあるトラブル

- `codex: command not found` → `npx @openai/codex` で直接実行するか、`npm install -g @openai/codex` を再実行
- API認証エラー → `OPENAI_API_KEY` が正しく設定されているか確認
- パーミッションエラー → nvm/fnm を使用するか、[npm prefix の変更](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally) で対処
- スキルが見つからない → ai-agent-camp のルートディレクトリで Codex を起動しているか確認

---

## チェックポイント
- [ ] Codex CLI がインストールされている（`codex --version` が動作する）
- [ ] OpenAI API キーが設定されている
- [ ] 承認モードを `on-request` に設定している（AGENTS.md の推奨設定を参照）
- [ ] `bash scripts/install_hooks.sh` でフックが設定されている
- [ ] `aiagent-check-setup` スキルが正常に動作する

---

## 次のステップ

Codex CLI のセットアップが完了したら、レッスンを開始できます。

**Codex ユーザーの推奨フロー:**

1. セットアップ確認: `aiagent-lesson-runner` スキルで `start-0-1`（環境セットアップ確認）を実行
2. 本格レッスン開始: `aiagent-lesson-runner` スキルで `start-1-1`（Module 1 バナー生成入門）を開始
3. 各レッスンのスラッシュコマンドはスキル経由で実行
4. 困ったら `aiagent-guide` スキルで全体像を確認

> **補足**: `.cursor/commands/lesson/` 内のレッスンファイルは Codex でも参照資料として利用できます。ただし、スラッシュコマンドとして直接実行することはできません。

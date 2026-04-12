---
description: "環境セットアップ状態の自動チェック"
duration: "約2分"
prerequisites: ["ai-agent-camp フォルダを Codex または Cursor で開いている"]
level: "beginner"
tags: ["setup", "check"]
---

# /check-setup -- 環境の自動チェック

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current check-setup` を実行して全体の進捗を表示
2. 未完了のステップがある場合は警告: 「以下のステップが未完了です: {ステップ名}。先に完了することを推奨しますが、チェックは実行可能です」

---

## このコマンドの役割

あなたの開発環境の状態を**AIが全自動でチェック**し、結果をレポートとして表示します。
問題がある項目は、対応するセットアップコマンドへの誘導や自動修復を提案します。

**ターミナルにコマンドを打つ必要は一切ありません。全てAIが裏側で実行します。**

| 項目 | 内容 |
|------|------|
| ゴール | 環境の健全性を確認し、問題があれば修正方法を案内する |
| 所要時間 | 約2分（自動実行） |
| 前提条件 | ai-agent-camp フォルダを Codex または Cursor で開いている |
| ユーザー操作 | 結果を確認するだけ（CLIコマンドの入力は不要） |

> **Codex向けメモ**: Codex では `/check-setup` という slash command は存在しないため、このドキュメントに列挙された確認コマンドを AI が順に実行して同じレポートを組み立てます。

---

## AIが自動実行するチェック手順

このコマンドが実行されたら、AIは以下を**全て裏側で自動実行**し、結果を一覧レポートとして表示する。ユーザーにコマンドの入力を求めてはならない。

### チェック1: 基本ツール

以下のコマンドを**AIが裏側で**実行し、各ツールの有無とバージョンを確認する:

| チェック対象 | 実行するコマンド | 判定基準 |
|-------------|-----------------|---------|
| OS種別 | `uname -s` (Mac/Linux), PowerShell `$env:OS` (Windows) | 表示のみ |
| Python | `python3 --version 2>/dev/null \|\| python --version 2>/dev/null` | バージョン 3.9 以上で合格 |
| Node.js | `node --version 2>/dev/null` | バージョン 18 以上で合格 |
| Git | `git --version 2>/dev/null` | 存在すれば合格 |
| GitHub CLI | `gh --version 2>/dev/null` | 存在すれば合格 |

### チェック2: 認証・API

以下のコマンドを**AIが裏側で**実行し、認証状態とAPI設定を確認する:

| チェック対象 | 実行するコマンド | 判定基準 |
|-------------|-----------------|---------|
| GitHub認証 | `gh auth status 2>&1` | 「Logged in」が含まれれば合格 |
| Gemini API | `.env` ファイルを読み取り、`GEMINI_API_KEY` の有無を確認 | キーが設定されていれば合格（値は表示しない） |
| Slack API | `.env` ファイルを読み取り、`SLACK_BOT_TOKEN` の有無を確認 | 設定済み or 「後で設定可」 |
| fal.ai API | `uv run python tools/credential_manager.py status` で `FAL_KEY` 確認 | 設定済み or 「後で設定可」 |
| ElevenLabs API | `uv run python tools/credential_manager.py status` で `ELEVENLABS_API_KEY` 確認 | 設定済み or 「後で設定可」 |
| Notion API | MCP設定ファイル（`~/.claude/mcp_settings.json` or `.cursor/mcp.json`）に `notion` エントリがあるか確認 | 設定済み or 「後で設定可」 |
| Clasp (GAS) | `clasp --version 2>/dev/null` | 存在すれば合格 or 「後で設定可」 |
| Typefully API | `uv run python tools/credential_manager.py status` で `TYPEFULLY_API_KEY` 確認 | 設定済み or 「後で設定可」 |
| X API | `uv run python tools/credential_manager.py status` で `X_BEARER_TOKEN` 確認 | 設定済み or 「後で設定可」 |
| gogcli (Google) | `gog version 2>/dev/null` | 存在すれば合格 or 「後で設定可」 |
| BigQuery/GCP | `gcloud --version 2>/dev/null` + `gcloud auth application-default print-access-token 2>/dev/null` | gcloud存在 + ADC設定済み or 「後で設定可」 |
| Vercel CLI | `vercel --version 2>/dev/null` + `vercel whoami 2>/dev/null` | 存在 + ログイン済み or 「後で設定可」 |

**重要: APIキーの値は絶対に画面に表示しない。「設定済み」「未設定」のみ表示する。**

### チェック3: プロジェクト設定

以下を**AIが裏側で**確認する:

| チェック対象 | 確認方法 | 判定基準 |
|-------------|---------|---------|
| プロジェクトフォルダ | カレントディレクトリが ai-agent-camp であるか | ディレクトリ名に `ai-agent-camp` が含まれれば合格 |
| 自分用リポジトリ | `git remote -v` を実行し origin の URL を確認 | origin が `TokenPocket/ai-agent-camp` または自分用 fork を指していれば合格 |
| .env ファイル | `.env` ファイルの存在を確認 | ファイルが存在すれば合格 |
| .gitignore | `.gitignore` を読み取り `.env` が除外設定されているか | `.env` のエントリがあれば合格 |
| セキュリティフック | `.git/hooks/pre-commit` の存在と実行権限を確認 | ファイルが存在し実行可能であれば合格 |

### チェック4: 拡張機能

以下のコマンドを**AIが裏側で**実行する:
```bash
cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null
```

確認対象の拡張機能:

| 拡張機能 | ID |
|---------|----|
| Python | `ms-python.python` |
| Marp | `marp-team.marp-vscode` |
| Draw.io | `hediet.vscode-drawio` |
| PlantUML | `jebbs.plantuml` |
| AIDE Pro | `nicepkg.aide-pro` |
| Pylance | `ms-python.vscode-pylance` |
| Prettier | `esbenp.prettier-vscode` |

---

## レポートの出力形式

チェック完了後、以下の形式で結果をユーザーに表示する:

```markdown
## 環境チェックレポート

### 基本ツール
| 項目 | 状態 | 詳細 |
|------|------|------|
| OS | (値) | macOS 14.x / Windows 11 / Linux |
| Python | (合否) | 3.12.x / 未インストール |
| Node.js | (合否) | 20.x / 未インストール |
| Git | (合否) | 2.x / 未インストール |
| GitHub CLI | (合否) | 2.x / 未インストール |

### 認証・API
| 項目 | 状態 | 詳細 |
|------|------|------|
| GitHub認証 | (合否) | ログイン済み(ユーザー名) / 未認証 |
| Gemini API | (合否) | .envに設定済み / 未設定 |
| Slack API | (合否またはスキップ可) | .envに設定済み / 未設定（後で設定可） |

### プロジェクト設定
| 項目 | 状態 | 詳細 |
|------|------|------|
| プロジェクトフォルダ | (合否) | ai-agent-camp を開いている / 別フォルダ |
| 自分用リポジトリ | (合否) | origin が自分のリポ / upstream のまま |
| .env ファイル | (合否) | 存在する / 未作成 |
| .gitignore | (合否) | .env が除外設定済み / 未設定 |
| セキュリティフック | (合否) | pre-commit 設定済み / 未設定 |

### 拡張機能
| 項目 | 状態 |
|------|------|
| Python | (合否) |
| Marp | (合否) |
| Draw.io | (合否) |
| PlantUML | (合否) |
```

**状態の表記ルール:**
- 合格: 項目名の右に「OK」と表示（例: `Python | OK | 3.12.1`）
- 不合格: 項目名の右に「要対応」と表示（例: `Python | 要対応 | 未インストール`）
- スキップ可能: 項目名の右に「任意」と表示（例: `Slack API | 任意 | 未設定（後で設定可）`）

---

## 推奨アクションの表示

レポートの後に、「要対応」の項目がある場合は推奨アクションを表示する。

### 「要対応」がある場合

```markdown
### 推奨アクション

以下の項目に対応が必要です:

1. Python が未インストール
   → Mac: https://www.python.org/downloads/ からインストーラーをダウンロード
   → Windows: Microsoft Store で「Python」を検索してインストール

2. .gitignore が未設定
   → /setup-security を実行すると自動で設定します

3. 拡張機能が不足
   → /setup-extensions を実行すると自動でインストールします
```

**AskQuestionの設定:**
```json
{
  "title": "問題を修正しますか？",
  "questions": [{
    "id": "fix_action",
    "prompt": "「要対応」の項目があります。どうしますか？",
    "options": [
      {"id": "auto_fix", "label": "AIが自動で修正できるものを全て修正する"},
      {"id": "guide_fix", "label": "1つずつ修正方法を案内してほしい"},
      {"id": "extensions_only", "label": "拡張機能だけ先にセットアップする（/setup-extensions）"},
      {"id": "security_only", "label": "セキュリティだけ先に設定する（/setup-security）"},
      {"id": "skip", "label": "今はスキップする"}
    ]
  }]
}
```

(auto_fix -> AIが自動修正できる項目を全て実行)

AIが自動修正できる項目:
- .gitignore の設定 -> `.gitignore` に不足エントリを自動追加
- セキュリティフック -> `.git/hooks/pre-commit` を自動作成
- 拡張機能のインストール -> `cursor --install-extension` を自動実行
- .env ファイルの作成 -> `.env.example` をコピーして `.env` を作成

AIが自動修正できない項目（ユーザーの操作が必要）:
- Python / Node.js / Git のインストール -> ダウンロードページのURLを案内
- GitHub CLI のインストールとログイン -> インストール手順とGUI操作を案内
- Gemini APIキーの取得 -> `/start-0-3` を案内
- 自分用リポジトリの作成 -> `/start-0-1` の Step 1.5 を案内

(guide_fix -> 「要対応」の項目を1つずつ AskQuestion で案内)
(extensions_only -> /setup-extensions を案内)
(security_only -> /setup-security を案内)
(skip -> 終了)

### 全て合格の場合

```markdown
### セットアップ完了

全てのチェック項目に合格しました。環境は正常に設定されています。

💡 **より効果的に学習するには**: Web版コース (https://ai-agent.camp) では、24/7 AIチューター、専用デスクトップアプリ、インタラクティブな演習環境を利用できます。まだご利用でなければ、ぜひお試しください。

/start-1-1 で最初のレッスン（バナー生成入門）を始めましょう！
```

**AskQuestionの設定:**
```json
{
  "title": "セットアップ完了！次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "全てのチェックに合格しました。次に何をしますか？",
    "options": [
      {"id": "start_lesson", "label": "最初のレッスンを始める（/start-1-1）"},
      {"id": "web_course", "label": "Web版コースを見る（ai-agent.camp）"},
      {"id": "overview", "label": "プロジェクトの全体像を確認する（/overview）"},
      {"id": "guide", "label": "使い方ガイドを見る（/guide）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(web_course -> 「https://ai-agent.camp でWeb版コースを確認できます。28モジュール、100以上のレッスン、70以上の実務スキルに加え、AIチューターと専用デスクトップアプリが利用可能です。」と案内)

(start_lesson -> /start-1-1 を案内)
(overview -> /overview を案内)
(guide -> /guide を案内)
(finish -> 「お疲れさまでした」と表示)

---

## よくあるトラブルと解決方法

**AskQuestionの設定:**
```json
{
  "title": "トラブルがありますか？",
  "questions": [{
    "id": "trouble",
    "prompt": "何か問題がありますか？",
    "options": [
      {"id": "trouble_1", "label": "Pythonのインストール方法がわからない"},
      {"id": "trouble_2", "label": "Node.jsのインストール方法がわからない"},
      {"id": "trouble_3", "label": "GitHubにログインできない"},
      {"id": "trouble_4", "label": "Gemini APIキーの取得方法がわからない"},
      {"id": "trouble_5", "label": "「ai-agent-campフォルダを開いている」が不合格になる"},
      {"id": "no_trouble", "label": "問題なし"}
    ]
  }]
}
```

### トラブル1: Pythonのインストール方法がわからない
**AIが行う対処（GUI手順を案内）**:
- **Mac の場合**: 「ブラウザで https://www.python.org/downloads/ にアクセスし、"Download Python 3.x" ボタンをクリックしてインストーラーをダウンロード。ダウンロードしたファイルをダブルクリックして、画面の指示に従ってインストールしてください」
- **Windows の場合**: 「Microsoft Store を開き、検索バーに "Python" と入力。"Python 3.x" を選択して "入手" ボタンをクリックしてインストールしてください。または、ブラウザで https://www.python.org/downloads/ からインストーラーをダウンロードしてください。インストール時に "Add Python to PATH" にチェックを入れることを忘れずに」
- インストール後: 「Cursorを再起動してから、もう一度 /check-setup を実行してください」

### トラブル2: Node.jsのインストール方法がわからない
**AIが行う対処（GUI手順を案内）**:
- **Mac の場合**: 「ブラウザで https://nodejs.org/ にアクセスし、"LTS" と書かれた緑色のボタンをクリックしてインストーラーをダウンロード。ダウンロードしたファイルをダブルクリックして、画面の指示に従ってインストールしてください」
- **Windows の場合**: 「ブラウザで https://nodejs.org/ にアクセスし、"LTS" と書かれた緑色のボタンをクリックしてインストーラーをダウンロード。ダウンロードした .msi ファイルをダブルクリックして、画面の指示に従ってインストールしてください」
- インストール後: 「Cursorを再起動してから、もう一度 /check-setup を実行してください」

### トラブル3: GitHubにログインできない
**AIが行う対処**:
1. AIが裏側で `gh auth status` を実行して現在の状態を確認
2. 未認証の場合:
   - 「ブラウザで https://github.com/ にアクセスし、アカウントにログインしてください」
   - 「その後、Cursorのチャットに "GitHubにログインして" と入力してください。AIがログイン手順をガイドします」

### トラブル4: Gemini APIキーの取得方法がわからない
**AIが行う対処**:
- 「/start-0-3 を実行すると、APIキーの取得手順を1ステップずつガイドします」と案内

### トラブル5: 「ai-agent-campフォルダを開いている」が不合格になる
**AIが行う対処（GUI手順を案内）**:
- 「Cursorのメニューから "ファイル" > "フォルダーを開く"（Mac: Cmd+O / Windows: Ctrl+O）を選択し、ai-agent-camp フォルダを選んで開いてください」
- 「フォルダを開いたら、もう一度 /check-setup を実行してください」

---

## 完了処理

**AIが自動実行する内容:**
1. 全チェックが OK の場合: `uv run python tools/setup_progress.py complete check-setup` で進捗を更新
2. 更新後の進捗サマリーを表示
3. 全ステップ完了なら: 「🎉 セットアップが全て完了しました！ `/start-1-1` で最初のレッスンを始めましょう！」
4. 未完了ステップがあれば: 「以下のステップを完了してください: {ステップ名}」と案内

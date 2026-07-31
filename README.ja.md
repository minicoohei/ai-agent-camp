[English](README.md) | **日本語** | [Español](README.es.md)

# ai-agent-camp

**非エンジニア向けAIエージェント研修 - Claude Code / Cursor / Codex 活用完全ガイド**

[![GitHub](https://img.shields.io/badge/GitHub-minicoohei%2Faiagent--base-181717?style=flat&logo=github)](https://github.com/minicoohei/ai-agent-camp)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)](https://github.com/minicoohei/ai-agent-camp/releases)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776ab.svg?style=flat&logo=python)](https://www.python.org/)

> ### ⚠️ クローンする前に
>
> **公式リポジトリ**（メンテナンス主体）:
> - `https://github.com/minicoohei/ai-agent-camp`
>
> このリポジトリのレッスンを実行すると、AI エージェントにシェル・ファイル書き込み・外部 API への権限を与えることになります。**fork やミラーは、レッスンやスキルの中身を静かに書き換えている可能性があります。** レッスンを始める前に、クローンしたリポが公式かを検証してください:
>
> ```bash
> python3 tools/scripts/verify_integrity.py
> ```
>
> fork や欠落ファイルが検出された場合は、`git diff upstream/main -- .claude/ skills/ tools/ scripts/` で差分を確認してから進めてください。詳細は [`docs/security-guardrails.md`](docs/security-guardrails.md)。

<!-- AGENT-META v1
schema: https://github.com/minicoohei/ai-agent-camp/blob/main/docs/release-process.md#agent-meta-v1
repo: minicoohei/ai-agent-camp
primary_branch: main
languages: [ja, en, es]
default_language: ja
latest_tag_api: https://api.github.com/repos/minicoohei/ai-agent-camp/releases/latest
release_asset_pattern: https://github.com/minicoohei/ai-agent-camp/releases/download/{tag}/ai-agent-camp-{lang}-{tag}.zip
manifest_raw_pattern: https://raw.githubusercontent.com/minicoohei/ai-agent-camp/{ref}/courses/lessons.manifest{lang_suffix}.yaml
lang_suffix: {ja: "", en: ".en", es: ".es"}
integrity_cli: python3 tools/scripts/verify_integrity.py
-->

## リリースとダウンロード

リリースは `main` が安定したタイミングでメンテナが `v*` タグ（semver）を切ることで発火します。1 つのタグから 3 言語分の zip が生成され、同一の GitHub Release に添付されます。

**ダウンロード URL のパターン**（一度 publish されたら同じ内容を返す固定 URL）:

```
https://github.com/minicoohei/ai-agent-camp/releases/download/{tag}/ai-agent-camp-{lang}-{tag}.zip
```

| 言語 | アセット | チェックサム |
|------|---------|-------------|
| 日本語 | `ai-agent-camp-ja-{tag}.zip` | `ai-agent-camp-ja-{tag}.zip.sha256` |
| English | `ai-agent-camp-en-{tag}.zip` | `ai-agent-camp-en-{tag}.zip.sha256` |
| Español | `ai-agent-camp-es-{tag}.zip` | `ai-agent-camp-es-{tag}.zip.sha256` |

各 zip には言語 suffix を除去済みの `courses/` / `skills/` / `.claude/` / `.cursor/` / `docs/` と、全ファイルの sha256 を記録した `CHECKSUMS.txt` が含まれます。

### 人間向け

```bash
# 最新リリース・任意の言語
gh release download --repo minicoohei/ai-agent-camp --pattern 'ai-agent-camp-ja-*.zip'

# 特定バージョン
gh release download v0.1.0 --repo minicoohei/ai-agent-camp \
  --pattern 'ai-agent-camp-ja-v0.1.0.zip'
```

### AI エージェント向け

上記の `<!-- AGENT-META v1 -->` ブロックを parse したうえで:

1. （任意）`latest_tag_api` を叩いて現在のタグを取得
2. `release_asset_pattern` の `{tag}` と `{lang}` を埋める
3. ダウンロード後、対応する `.sha256` と照合してから unzip

レッスンマニフェストだけが必要な場合は `manifest_raw_pattern` と `lang_suffix` を使って `courses/lessons.manifest[.en|.es].yaml` を任意の ref（ブランチ・タグ・commit SHA）から直接取得できます。

仕様の全文・バージョニング方針・ロールバック手順・Python parse サンプルは [`docs/release-process.md`](docs/release-process.md) を参照してください。

> **初回タグ前の注意**: まだ Release アセットが存在しないため、上記 URL パターンは `v0.1.0` がリリースされるまで 404 を返します。それまでは `git clone https://github.com/minicoohei/ai-agent-camp.git` でリポを取得するか、`raw.githubusercontent.com/.../main/...` で個別ファイルを参照してください。

## 目次

- [プロジェクト概要](#プロジェクト概要)
- [主な特徴](#主な特徴)
- [クイックスタート](#クイックスタート)
- [Webコース（推奨）](#webコース推奨)
- [ツール別の違い](#ツール別の違い)
- [学習パス](#学習パス)
- [ディレクトリ構造](#ディレクトリ構造)
- [スキルマトリックス](#スキルマトリックス)
- [必要なAPI](#必要なapi)
- [リリースとダウンロード](#リリースとダウンロード)
- [ドキュメント](#ドキュメント)
- [よくある質問](#よくある質問)
- [コントリビューション](#コントリビューション)
- [サポート](#サポート)

---

## プロジェクト概要

**ai-agent-camp** は、マーケティング、営業、企画、事務などの**非エンジニア職**が、Claude Code、Cursor、Codex などのAIエージェントを使って業務を自動化・効率化するための包括的な研修教材です。

### 対象者

- プログラミング経験がない方
- AIツールを業務で活用したい方
- 自動化やデータ分析に興味がある方
- チーム全体のAIリテラシー向上を目指す方

### プロジェクトの目指す未来

AIエージェントを「専門家向けのツール」から「すべての職種が活用できるツール」へと民主化し、組織全体の生産性向上を実現します。

---

## 主な特徴

✅ **非エンジニア向けに最適化**
- プログラミング知識不要
- ステップバイステップのチュートリアル
- 実際の業務シナリオに基づいた教材

🚀 **実践的なスキルセット**
- [Commands リファレンス](docs/commands-reference.md)に掲載された業務用コマンド
- [Skills リファレンス](docs/skills-reference.md)に掲載された実装済みスキル
- 業務別のワークフローサンプル

📚 **包括的なカリキュラム**
- AI基礎（Foundation）26チャプター
- 環境セットアップ（Setup）6チャプター
- 提供中の26個のコアモジュール（Google Workspace・動画制作・要件定義・マーケティング等を含む）
- CursorBootcamp YAML メタデータ対応（全62チャプター）
- 総学習時間：約24時間（演習込みで約30時間以上）

🔒 **セキュリティとベストプラクティス**
- API キー管理のガイドライン
- 安全なデータ処理の手法
- 企業内での導入方針

🎯 **業務別ワークフロー**
- カスタマーサポート
- セールスプロセス
- コンテンツマーケティング
- オンボーディング自動化
- 承認フロー最適化

---

## クイックスタート

### 前提条件

- Git がインストール済み
- Python 3.9 以上
- インターネット接続
- Cursor、Claude Code、または Codex が利用可能
- **Windows ユーザーは WSL2 + Ubuntu が必須です。** Windows ネイティブ（PowerShell / cmd）はサポート対象外です。WSL2 のセットアップは [docs/terminal-guide.md](docs/terminal-guide.md) を参照してください。

> **どのツールを選べばいい？** `/start-0-8`（ツール選択ガイド）で Cursor / Claude Code / Codex の比較と選び方を確認できます。

### 最短の始め方

1. この repo を clone する
2. 自分の使うツールの入口を読む
   - Codex: `AGENTS.md`
   - Claude Code: `CLAUDE.md`
   - Cursor: `.cursor/commands/lesson/start-0-1.md` を含む `.cursor/commands/*`（Google Workspace 教材 Module 4 用は `/module-18-google-auth` など `module-18-*.md`）
3. 安全ルールを確認する
   - Codex: `docs/codex-safety.md`
   - Claude / Cursor: `docs/security-guardrails.md`
4. セットアップ確認を行う
   - Codex: `aiagent-check-setup`
   - Cursor: `/check-setup`
5. `start-0-1` から最初の lesson を始める

### 自分専用のリポジトリを作成する

このリポジトリを自分専用のプライベートリポジトリとしてコピーする方法です。以下のいずれかの方法を選択してください。

#### 方法1: Import repository（GUI操作・簡単）

GitHub の画面操作だけで完結します。

1. GitHub にログインし、右上の「+」→「Import repository」を選択
2. 以下を入力:
   - **Your old repository's clone URL**: `https://github.com/minicoohei/ai-agent-camp.git`
   - **Repository name**: 任意の名前（例: `my-aiagent`）
   - **Privacy**: **Private** を選択
3. 「Begin import」をクリック
4. インポート完了後、自分のリポジトリを clone:
   ```bash
   git clone https://github.com/{あなたのユーザ名}/my-aiagent.git
   cd my-aiagent
   ```

#### 方法2: Clone & Push（コマンドライン）

ターミナル操作に慣れている方向けです。

```bash
# 1. GitHub で空の Private リポジトリを作成

# 2. ミラー clone を作成
git clone --bare https://github.com/minicoohei/ai-agent-camp.git my-aiagent.git
cd my-aiagent.git

# 3. 新しい origin を設定して push
git push --mirror https://github.com/{あなたのユーザ名}/my-aiagent.git

# 4. 通常の作業用 clone を取り直す
cd ..
git clone https://github.com/{あなたのユーザ名}/my-aiagent.git
```

### 元リポジトリの更新を取り込む

配布元の教材が更新された場合、以下の方法で変更を取り込めます。

```bash
# 初回のみ: 元リポジトリを upstream として追加
git remote add upstream https://github.com/minicoohei/ai-agent-camp.git

# 更新を取り込む
git fetch upstream
git merge upstream/main
```

Cursor を使っている場合は、チャットで **`/update-material`** を実行すると同様の操作ができます。

> **注意**: 自分で変更を加えている場合、コンフリクトが発生する可能性があります。その場合は手動で解決してください。

### インストール手順

#### 1. リポジトリをクローン

```bash
git clone https://github.com/minicoohei/ai-agent-camp.git ~/ai-agent-camp
cd ~/ai-agent-camp
```

#### 2. 環境変数を設定

```bash
# まず .env.local に必要なキーの行を用意
uv run python tools/credential_manager.py prepare-dotenv GEMINI_API_KEY

# 保存後、必要に応じて Credential Store に移行
# uv run python tools/credential_manager.py import-dotenv GEMINI_API_KEY --delete
```

> API キーはチャットに貼らず、`.env.local` に保存してください。

#### 3. Python 依存パッケージをインストール

```bash
# uv で依存パッケージをインストール
uv sync
```

#### 4. コースを開始

```bash
# ブラウザで教材を開く
# macOS: open https://ai-agent.camp/ja/course/module-0
# WSL2:  wslview https://ai-agent.camp/ja/course/module-0   (または Windows 側ブラウザで直接開く)

# Cursor でワークスペースを開く
cursor .

# Claude Code / Codex でも同じリポジトリを開けます
claude
codex
```

### ツール別の開始方法

#### Cursor

```bash
/check-setup
/overview
/start-0-1
```

#### Claude Code

- `CLAUDE.md` を読む
- `docs/security-guardrails.md` を確認する
- setup 確認後に lesson 導線へ進む

#### Codex

- `AGENTS.md` を読む
- `docs/codex-guide.md` を開く
- `aiagent-check-setup` skill で環境確認を行う
- `aiagent-lesson-runner` skill に `start-0-1` を渡して最初のレッスンを開始する

---

## Webコース（推奨）

> **体系的に学びたい方へ**
>
> [AI Agent Camp](https://ai-agent.camp) では、28モジュール、100以上のレッスン、70以上の実務スキルを備えたWeb版コースを提供しています。24/7 AIチューターや環境構築を自動化する専用デスクトップアプリも利用可能です。
>
> このリポジトリと同じカリキュラムに加え、非エンジニア向けのインタラクティブな機能や追加コンテンツが含まれています。
>
> 👉 **[ai-agent.camp で学習を始める](https://ai-agent.camp)**

<p align="center">
  <a href="https://ai-agent.camp">
    <img src="docs/images/ai-agent-camp-preview.png" alt="AI Agent Camp Webコース" width="600">
  </a>
</p>

---

## ツール別の違い

教材そのものは共通です。違うのは「どこから入るか」と「どう操作するか」です。

| 項目 | Codex | Claude Code | Cursor |
| --- | --- | --- | --- |
| 入口 | `AGENTS.md` | `CLAUDE.md` | `.cursor/commands/*` |
| lesson 開始 | `aiagent-lesson-runner` | Claude 側の lesson 導線 | `/start-*` |
| setup 確認 | `aiagent-check-setup` | Claude 側で確認 | `/check-setup` |
| 安全モデル | sandbox + approval | Claude hooks + permissions | Cursor rules + commands |
| lesson id | `start-*` | `start-*` | `start-*` |

共通点:
- 同じリポジトリを使います
- 同じ lesson id を使います
- 秘密情報と Git の安全原則は同じです

受講者向けの基本ルール:
- 小さい作業は軽く進める
- 大きい作業は短い計画を書いてから進める
- Git、MCP、秘密情報を触る前に対応する safety ガイドを読む

---

## 学習パス

### フェーズ1: Foundation（AI基礎）- 5時間

AI エージェントの基本を学びます。下記の学習パスは最初の11チャプター（約5時間）を扱います。Foundation レッスン全体では26チャプターあります。

| チャプター | 内容 | 学習時間 |
|-----------|------|---------|
| 0-1 | LLM の基本原理と仕組み | 30分 |
| 0-2 | Token 概念と計算方法 | 30分 |
| 0-3 | AI エージェントとは | 30分 |
| 0-4 | Context Engineering と Prompt | 30分 |
| 0-5 | Cursor の使い方 | 25分 |
| 0-6 | MCP（Model Context Protocol） | 25分 |
| 0-7 | マルチモーダル AI | 25分 |
| 0-8 | RAG（検索拡張生成） | 25分 |
| 0-9 | Skill / SubAgent / Agent Team | 25分 |
| 0-10 | ハルシネーション対策 | 25分 |
| 0-11 | AI セキュリティ | 25分 |

**学習目標**
- LLM の基本を理解する
- トークンが何か知る
- AIエージェントの概念を把握する
- より良いプロンプトを書く
- MCP・RAG・マルチモーダルの仕組みを理解する
- AI利用時のセキュリティリスクを把握する

---

### フェーズ2: Setup（環境構築）- 1.5時間

AIエージェントを実際に使うための準備です。

| モジュール | 内容 | 学習時間 |
|-----------|------|---------|
| 0 | Claude Code / Cursor のセットアップ | 30分 |
| 0.5 | 拡張機能とカスタマイズ | 15分 |
| 0.9 | API キー設定と認証 | 45分 |

**学習目標**
- Claude Code / Cursor を導入する
- API キーを安全に管理する
- 基本的な設定を完了する

---

### フェーズ3: Core Modules（コアスキル）- 17.5時間

実際の業務で使えるスキルを習得します。

| # | モジュール | 主な Skills | レッスン数 | 難易度 |
|---|-----------|-----------|---------|--------|
| **1** | **バナー・画像生成** | banner-creator, nanobanana | 3 | ⭐ |
| **2** | **図表・フロー作成** | diagram-generator, PlantUML | 3 | ⭐⭐ |
| **3** | **チュートリアル** | screenshot-analyzer, tutorial-generator | 6 | ⭐⭐ |
| **4** | **Google Workspace** | gogcli, Gmail, Calendar, Drive, Sheets | 7 | ⭐⭐⭐ |
| **5** | **PPTX 解析・編集** | pptx-analyzer, pptx-creator, pptx-converter | 2 | ⭐⭐ |
| **6** | **エージェント開発** | Commands/Skills 作成、カスタマイズ | 5 | ⭐⭐⭐⭐ |
| **7** | **Skill/Commands** | Skill設計、SKILL.md実装、テスト、デザインパターン | 8 | ⭐⭐⭐⭐ |
| **8** | **データ分析・EDA** | data-analyst, BigQuery, Marimo | 4 | ⭐⭐⭐ |
| **9** | **Slack 連携** | slack-search, check-inbox, task-manager | 2 | ⭐ |
| **10** | **GAS 自動化** | gas-clasp-ops, Calendar, Sheets | 3 | ⭐⭐⭐ |
| **11** | **GitHub Actions** | Workflow, Secrets, CI/CD | 2 | ⭐⭐⭐ |
| **12** | **Notion 連携** | Notion MCP, DB操作, ncli | 6 | ⭐⭐ |
| **13** | **LP/HP 制作** | 訴求整理、WF作成、Pencilデザイン、HTML実装、Vercelデプロイ | 5 | ⭐⭐⭐ |
| **14** | **記事制作** | article-writer, copy-editing, fact-checker | 7 | ⭐⭐⭐ |
| **15** | **動画制作** | Kling, HeyGen, Veo, Remotion, MV | 8 | ⭐⭐⭐ |
| **16** | **メール/LINE 自動化** | email-sequence, Resend, LINE API | 8 | ⭐⭐⭐ |
| **17** | **マーケティング** | X投稿、SEO調査、コピーライティング、デザインモック | 4 | ⭐⭐⭐ |
| **18** | **要件定義/システム開発** | pm-toolkit, test-planner, Notion連携 | 20 | ⭐⭐⭐⭐⭐ |
| **19** | **Microsoft Office (Outlook)** | Outlook MCP 連携 | 1 | ⭐⭐ |
| **20** | **Freee/MoneyForward** | Freee MCP 会計データ操作 | 1 | ⭐⭐ |

**総学習時間: 約 24 時間（演習・実践課題を含めると約 30 時間以上）**

### 学習オプション

**推奨順序（初心者向け）**
```text
Module 1 → Module 2 → Module 3 → Module 5 → Module 6 → Module 8
```

**推奨順序（実務効率化重視）**
```text
Module 4 → Module 9 → Module 10 → Module 11 → Module 12 → Module 8
```

**推奨順序（クリエイティブ重視）**
```text
Module 1 → Module 2 → Module 3 → Module 15 → Module 13 → Module 14
```

**推奨順序（マーケティング重視）**
```text
Module 1 → Module 17 → Module 13 → Module 15 → Module 14 → Module 16
```

---

### CursorBootcamp YAML メタデータ

`courses/aiagent/` に、CursorBootcamp プラットフォーム向けの YAML メタデータを配備しています。一部のチャプターには `practice/`（演習）と `final/`（最終課題）が含まれます（web 教材へリンクするチャプターにはありません）。

| レッスン | チャプター数 | 内容 |
|---------|-----------|------|
| **Lesson 01: Foundation** | 26 | LLM基礎、Token、Agent、Context Engineering、MCP、マルチモーダル、RAG、SubAgent、ハルシネーション、セキュリティ、計測、実現可能性 |
| **Lesson 02: Setup** | 6 | 環境構築、拡張機能、API設定、セキュリティ確認、リモート環境、ナレッジベース |
| **Lesson 03: Core** | 26 | Banner ～ slide-forge（全コアモジュール対応） |
| **Lesson 04: Practice** | 4 | 図解演習、並列セッション、調査→提案デッキ、PMO定例運用（`practice/` / `final/` ディレクトリなし） |

合計 **62 チャプター**。

---

## ディレクトリ構造

```
ai-agent-camp/
│
├── 📚 courses/                         # カリキュラム source of truth
│   ├── lessons.manifest.yaml           # レッスンマニフェスト
│   └── aiagent/
│       ├── course.yaml                 # コース全体定義（日本語）
│       ├── course.en.yaml              # コース全体定義（英語）
│       ├── course.es.yaml              # コース全体定義（スペイン語）
│       ├── cover.png                   # コースカバー画像
│       ├── lesson01-foundation/        # 基礎知識（26 チャプター）
│       │   └── ch00 ~ ch24/           # LLM, Token, Agent, MCP, RAG, Security, 計測, 実現可能性 等
│       ├── lesson02-setup/             # 環境構築（6 チャプター）
│       │   └── ch01 ~ ch06/           # 環境, 拡張機能, API設定, セキュリティ確認, リモート環境, ナレッジベース
│       ├── lesson03-core/              # コアスキル（提供中 26 モジュール）
│       │   └── module01 ~ module25, module29/ # Banner ～ slide-forge
│       └── lesson04-practice/          # 実践演習（4 チャプター）
│           └── ex01 ~ ex04/           # 図解演習, 並列セッション, 提案デッキ, PMO定例
│
├── 💻 .cursor/commands/                # docs/commands-reference.md を参照
│   ├── lesson/                         # 学習用コマンド
│   │   ├── /start-0-1 ~ /start-0-8    # Module 0: Setup
│   │   ├── /start-1-1 ~ /start-1-3    # Module 1: バナー
│   │   ├── /start-2-1 ~ /start-2-3    # Module 2: 図解
│   │   ├── /start-3-1 ~ /start-3-6    # Module 3: チュートリアル
│   │   ├── /start-4-1 ~ /start-4-7    # Module 4: Google Workspace
│   │   ├── /start-5-1 ~ /start-5-2    # Module 5: PPTX
│   │   ├── /start-6-1 ~ /start-6-9    # Module 6: エージェント開発
│   │   ├── /start-7-1 ~ /start-7-8    # Module 7: Skill/Commands
│   │   ├── /start-8-1 ~ /start-8-4    # Module 8: データ分析
│   │   ├── /start-9-1 ~ /start-9-3    # Module 9: Slack連携
│   │   ├── /start-10-1 ~ /start-10-4  # Module 10: GAS
│   │   ├── /start-11-1 ~ /start-11-5  # Module 11: GitHub Actions
│   │   ├── /start-12-1 ~ /start-12-6  # Module 12: Notion
│   │   ├── /start-13-1 ~ /start-13-5  # Module 13: LP制作
│   │   ├── /start-14-1 ~ /start-14-7  # Module 14: 記事制作
│   │   ├── /start-15-1 ~ /start-15-13 # Module 15: 動画制作（7a-7d を含む）
│   │   ├── /start-16-1 ~ /start-16-8  # Module 16: メール/LINE自動化
│   │   ├── /start-17-1 ~ /start-17-5  # Module 17: マーケティング
│   │   ├── /start-18-1 ~ /start-18-20 # Module 18: 要件定義/システム開発
│   │   ├── /setup-m365cli + /start-19-1 ~ /start-19-2 # Module 19: Outlook
│   │   ├── /setup-freee + /start-20-1  # Module 20: Freee/MoneyForward
│   │   ├── /setup-figma + /start-21-1  # Module 21: Figma
│   │   ├── /setup-discord + /start-22-1 # Module 22: Discord
│   │   ├── /setup-line-harness + /start-23-1 # Module 23: LINE
│   │   ├── /setup-salesforce + /start-24-1 # Module 24: Salesforce
│   │   ├── /setup-google-ads + /start-25-1 # Module 25: Google Ads
│   │   └── /start-29-1 ~ /start-29-4  # Module 29: slide-forge
│   │
│   └── utility/                        # ユーティリティコマンド
│       ├── /check-setup                # セットアップ確認
│       ├── /overview                   # プロジェクト概要
│       ├── /guide                      # 使い方ガイド
│       ├── /tutor                      # 対話型ヘルプ
│       ├── /update-material            # 教材を最新版に更新
│       └── ... その他のヘルパー
│
├── 🛠️ skills/                            # docs/skills-reference.md を参照
│   │
│   │  ── 画像・バナー生成 ──
│   ├── banner-creator/                 # SNS バナー生成
│   ├── nanobanana/                     # 汎用画像生成・編集
│   ├── diagram-generator/              # インフォグラフィック生成
│   │
│   │  ── スクリーンショット・チュートリアル ──
│   ├── screenshot-analyzer/            # スクリーンショット分析
│   ├── screenshot-annotator/           # スクリーンショット注釈
│   ├── tutorial-generator/             # チュートリアル自動生成
│   │
│   │  ── ドキュメント処理 ──
│   ├── pptx-analyzer/                  # PPTX 構造分析
│   ├── pptx-converter/                 # PPTX テンプレート変換（NEW）
│   ├── pptx-creator/                   # トピック → PPTX 自動生成（NEW）
│   ├── document-processor/             # PDF/Word 処理
│   ├── pdf-compressor/                 # PDF 圧縮
│   │
│   │  ── 動画・メディア ──
│   ├── storyboard-generator/           # 絵コンテ + Kling 動画生成
│   ├── video-frame-reader/             # 動画キーフレーム抽出
│   ├── media-generator/                # メディアファイル生成
│   │
│   │  ── データ分析・認証 ──
│   ├── data-analyst/                   # データ分析・EDA
│   ├── bigquery-auth/                  # BigQuery 認証
│   ├── gcp-auth/                       # GCP 認証・設定
│   │
│   │  ── Slack・通信 ──
│   ├── check-inbox/                    # メール/Slack TODO 抽出
│   ├── slack-search/                   # Slack セマンティック検索
│   ├── slack-task-manager/             # Slack タスク管理
│   ├── slack-unanswered/               # 未返信メッセージ検出
│   │
│   │  ── GAS・その他 ──
│   ├── gas-clasp-ops/                  # Google Apps Script 操作
│   ├── lp-designer/                    # LP/HP 制作ワークフロー（NEW）
│   │
│   │  ── マーケティング（20 スキル・NEW）──
│   ├── ab-test-setup/                  # A/B テスト設計・実装
│   ├── analytics-tracking/             # GA4・GTM トラッキング
│   ├── competitor-alternatives/         # 競合比較ページ
│   ├── content-strategy/               # コンテンツ戦略
│   ├── copy-editing/                   # コピー編集・レビュー
│   ├── copywriting/                    # マーケティングコピー
│   ├── email-sequence/                 # メールシーケンス
│   ├── free-tool-strategy/             # 無料ツール戦略
│   ├── launch-strategy/                # ローンチ戦略
│   ├── marketing-ideas/                # マーケティングアイデア
│   ├── marketing-psychology/           # マーケティング心理学
│   ├── paid-ads/                       # 有料広告キャンペーン
│   ├── pricing-strategy/               # 価格戦略
│   ├── product-marketing-context/      # プロダクトマーケティング
│   ├── programmatic-seo/               # プログラマティック SEO
│   ├── referral-program/               # リファラルプログラム
│   ├── schema-markup/                  # 構造化データ
│   ├── seo-audit/                      # SEO 監査
│   └── social-content/                 # SNS コンテンツ
│
├── mv-composer/                        # 運営・制作専用の Remotion 動画制作（受講には不要）
├── gas-example/                        # 運営・制作専用の GAS サンプル（受講には不要）
├── ops/                                # 運営・制作専用スクリプト（受講には不要）
│
├── 🗂️ data/                            # lesson / Codex 実行に必要な最小データ
│   ├── codex-command-manifest.json     # Codex ルーティング定義
│   ├── google-sync/                    # Google 同期用スクリプトとテンプレート
│   ├── slack-sync/                     # Slack 同期用スクリプトとデータ置き場
│   └── videos/                         # 動画レッスン用サンプル
│
├── 🧪 tests/                            # テストスイート
│   ├── e2e/                            # エンドツーエンドテスト
│   ├── security/                       # セキュリティテスト
│   ├── skills/                         # スキルテスト
│   ├── tools/                          # ツールテスト
│   └── knowledge_base/                 # ナレッジベーステスト
│
├── 🎬 tools/                            # Python スクリプト・ツール
│   ├── ugc/                            # 動画生成エンジン
│   │   ├── remotion/                   # Remotion (React 動画)
│   │   └── ... その他の動画ツール
│   └── ... その他のユーティリティ
│
├── 📚 docs/                            # ドキュメント
│   ├── commands-reference.md           # Commands 全体リファレンス
│   ├── skills-reference.md             # Skills 全体リファレンス
│   ├── troubleshoot.md                 # トラブルシューティング
│   ├── codex-guide.md                  # Codex 向けガイド
│   ├── codex-safety.md                 # Codex 安全ガイド
│   ├── codex-mcp.md                    # Codex MCP ガイド
│   ├── security-guardrails.md          # セキュリティガードレール
│   ├── i18n-glossary.md                # 国際化用語集
│   ├── images/                         # ドキュメント用画像
│   ├── bootcamp/                       # Bootcamp 関連資料
│   │   ├── screenshots/               # スクリーンショット
│   │   └── tutorials/                 # チュートリアル
│   ├── generated/                      # 自動生成ドキュメント
│   └── setup-guides/                   # API 設定ガイド
│       └── docs/
│           ├── GEMINI_API_SETUP.md
│           ├── GOOGLE_OAUTH_SETUP.md
│           ├── BIGQUERY_SETUP.md
│           ├── SLACK_TOKEN_SETUP.md
│           ├── NOTION_API_SETUP.md
│           └── GITHUB_SECRETS_SETUP.md
│
├── .cursor/                            # Cursor ルール
│   └── rules/                          # カスタムルール
│
├── .github/                            # GitHub Actions
│   └── workflows/                      # CI/CD ワークフロー
│
├── .githooks/                          # Git フック
│   └── pre-commit                      # Pre-commit ルール
│
├── .env.example                        # 環境変数テンプレート
├── .gitignore                          # Git 除外ルール
├── AGENTS.md                           # Codex ガイド
├── CLAUDE.md                           # Claude Code ガイド
├── PROGRESS_CHECKLIST.md               # 学習進捗チェックリスト
├── package.json                        # NPM パッケージ設定
├── pyproject.toml                      # Python プロジェクト設定
├── requirements.txt                    # Python 依存パッケージ
├── requirements-test.txt               # テスト用パッケージ
└── README.md                           # メイン README（英語）
```

---

## スキルマトリックス

### 学習結果マップ

完了後に習得できるスキル一覧です。

#### タイプ別スキル分類

**📊 データ処理・分析**
- BigQuery を使用したデータ分析
- Python による EDA（探索的データ分析）
- CSV/Excel ファイル処理
- データビジュアライゼーション

**🎨 コンテンツ生成**
- AI による画像生成
- SNS バナー・サムネイル作成
- インフォグラフィック・図表生成
- スクリーンショット自動注釈

**📹 動画・メディア**
- AI 動画生成（Kling, HeyGen）
- ショート動画の自動作成
- キーフレーム抽出・分析
- 絵コンテの自動生成

**📄 ドキュメント処理**
- PPTX スライド自動生成・編集
- PDF 処理・圧縮
- Word ドキュメント操作
- ドキュメント内容分析

**💬 コミュニケーション自動化**
- Slack ワークフロー自動化
- メール TODO 自動抽出
- チャットボット開発
- メッセージルーティング

**🔄 業務オートメーション**
- Google Sheets/Calendar 自動操作
- GAS（Google Apps Script）開発
- GitHub Actions による CI/CD
- Notion データベース操作

**🤖 AI エージェント開発**
- カスタム Command の作成
- カスタム Skill の開発
- LLM プロンプト最適化
- ワークフロー設計

**📣 マーケティング・CRO**
- A/B テスト設計・実装
- SEO 監査・プログラマティック SEO
- コピーライティング・コピー編集
- メールシーケンス・SNS コンテンツ
- 広告キャンペーン・価格戦略
- GA4 / GTM トラッキング実装

**🌐 LP/HP 制作**
- 訴求整理・コピーライティング
- ワイヤーフレーム作成
- Pencil MCP デザイン
- HTML/CSS/JS 実装
- Vercel デプロイ

#### モジュール別習得スキル

| モジュール | 習得スキル | 応用例 |
|-----------|-----------|--------|
| **1** | 画像生成、バナー作成 | SNS マーケティング、プレゼン資料 |
| **2** | フロー図、ダイアグラム | プロセス設計、システム設計 |
| **3** | スクショ分析、チュートリアル | マニュアル作成、UI/UX 改善報告 |
| **4** | Google Workspace 統合 | Gmail分析、Calendar管理、Drive操作、AI秘書 |
| **5** | PowerPoint 自動化 | プレゼン資料作成、定期レポート |
| **6** | エージェント開発 | Commands/Skills 作成、カスタムツール |
| **7** | Skill/Commands 設計 | 業務特化スキル、デザインパターン |
| **8** | データ分析、可視化 | ビジネス分析、レポート自動化 |
| **9** | Slack 統合、タスク管理 | 通知自動化、チーム運営効率化 |
| **10** | GAS 自動化 | スケジュール管理、データ連携 |
| **11** | GitHub Actions | CI/CD パイプライン、自動テスト |
| **12** | Notion 連携 | ナレッジ管理、プロジェクト管理 |
| **13** | LP/HP 制作 | 訴求整理、WF、デザイン、実装、デプロイ |
| **14** | 記事制作 | テーマ設定、スタイル適用、校閲、ファクトチェック |
| **15** | AI 動画生成 | プロダクト紹介、MV、スライド動画 |
| **16** | メール/LINE 自動化 | メールシーケンス、LINE Bot |
| **17** | マーケティング | X投稿、SEO、コピーライティング |
| **18** | 要件定義/システム開発 | PRD、設計、テスト、Notionエクスポート |
| **19** | Outlook連携 | Microsoft Office統合 |
| **20** | Freee/MoneyForward | 会計データ操作 |
| **21** | Figma連携 | デザインシステム・UI共同作業 |
| **22** | Discord連携 | Bot・チャンネル運用 |
| **23** | LINE公式アカウント | メッセージ・アカウント運用 |
| **24** | Salesforce CLI連携 | CRMクエリ・メタデータ操作 |
| **25** | Google Ads連携 | 広告データ操作 |
| **29** | slide-forge | スライド生成・修正ワークフロー |

---

## 必要なAPI

### 必須

| API | 説明 | 取得先 | 用途 |
|-----|------|--------|------|
| **Gemini API** | Google の生成 AI API | [Google AI Studio](https://aistudio.google.com/) | 画像生成、テキスト分析、コンテンツ作成 |

### 強く推奨（Module 4, 8, 9, 12 で必要）

| API | 説明 | 取得先 | 用途 | 必要なモジュール |
|-----|------|--------|------|-----------------|
| **Google OAuth** | Google アカウント連携 | [Google Cloud Console](https://console.cloud.google.com/) | Gmail、Calendar、Drive 操作 | 4, 10 |
| **BigQuery** | Google の SQL データウェアハウス | [Google Cloud Console](https://console.cloud.google.com/) | 大規模データ分析 | 8 |
| **Slack API** | Slack ワークスペース連携 | [Slack App Directory](https://api.slack.com/apps) | メッセージ取得、自動返信 | 9 |
| **Notion (OAuth)** | Notion ワークスペース連携 | `ncli login`（ブラウザ OAuth）+ Notion 公式 Hosted MCP（`https://mcp.notion.com/mcp`） | データベース操作 | 12 |

### オプション（Module 15 で推奨）

| API | 説明 | 取得先 | 用途 |
|-----|------|--------|------|
| **FAL.ai** | AI 画像・動画生成 | [fal.ai](https://fal.ai) | 高速画像生成 |
| **Kling AI** | テキスト → 動画生成 | [Kling](https://klingai.com/) | ショート動画自動生成 |
| **HeyGen** | アバター動画生成 | [HeyGen](https://www.heygen.com/) | 自動解説動画作成 |
| **Google Veo** | AI 動画生成モデル | [Google AI Studio](https://aistudio.google.com/) | 高品質動画生成 |
| **GitHub Token** | GitHub 連携 | [GitHub Settings](https://github.com/settings/tokens) | CI/CD 操作 |

### API キー取得ステップ

詳細は以下のドキュメントを参照してください：

- [Gemini API セットアップ](docs/setup-guides/docs/GEMINI_API_SETUP.md)
- [Google OAuth セットアップ](docs/setup-guides/docs/GOOGLE_OAUTH_SETUP.md)
- [BigQuery セットアップ](docs/setup-guides/docs/BIGQUERY_SETUP.md)
- [Slack API セットアップ](docs/setup-guides/docs/SLACK_TOKEN_SETUP.md)
- [Notion API セットアップ](docs/setup-guides/docs/NOTION_API_SETUP.md)

---

## ドキュメント

### 学習教材

| ドキュメント | 説明 |
|------------|------|
| [courses/aiagent](courses/aiagent) | カリキュラム source of truth |
| [docs/codex-guide.md](docs/codex-guide.md) | Codex 向け開始ガイド |
| [学習チェックリスト](PROGRESS_CHECKLIST.md) | 進捗追跡用チェックリスト |

### リファレンス

| ドキュメント | 説明 |
|------------|------|
| [Commands リファレンス](docs/commands-reference.md) | 全コマンドの自動生成一覧 |
| [Skills リファレンス](docs/skills-reference.md) | 全スキルの自動生成一覧 |
| [Claude Code ガイド](CLAUDE.md) | Claude Code 特有の機能解説 |

### API 設定ガイド

すべてのガイドは `docs/setup-guides/docs/` ディレクトリにあります：

```
docs/setup-guides/docs/
├── GEMINI_API_SETUP.md      # Gemini API
├── GOOGLE_OAUTH_SETUP.md    # Google OAuth
├── BIGQUERY_SETUP.md        # BigQuery
├── SLACK_TOKEN_SETUP.md     # Slack
├── NOTION_API_SETUP.md      # Notion
└── GITHUB_SECRETS_SETUP.md  # GitHub Secrets
```

### トラブルシューティング

よくある問題の解決方法は [トラブルシューティングガイド](docs/troubleshoot.md) を参照してください。

---

## よくある質問（FAQ）

### セットアップについて

**Q: Python がインストールされていない場合は？**

A: 以下からダウンロード・インストールしてください：
- [Python 公式](https://www.python.org/downloads/)
- インストール時に「Add Python to PATH」にチェック

**Q: macOS でパッケージがインストールできません**

A: Homebrew を使用してください：
```bash
brew install python3
```

**Q: 特定の API キーがない場合、進められないか？**

A: いいえ。必須は Gemini API のみです。他は必要なモジュール時に取得できます。

### 学習について

**Q: プログラミング経験がなくても大丈夫？**

A: はい。すべてのコマンドとスキルはプログラミング知識不要で設計されています。

**Q: モジュールの順序は固定か？**

A: いいえ。興味のある順に学習できます。ただし、Foundation モジュール（0-1～0-4）は最初に受講を推奨します。

**Q: 学習にかかる時間は？**

A: 講義部分で約 24 時間、演習・実践課題を含めると約 30 時間以上です。1 日 2-3 時間で 2 週間程度で完了できます。

**Q: 修了証はもらえるか？**

A: リポジトリ内の進捗チェックリスト ([PROGRESS_CHECKLIST.md](PROGRESS_CHECKLIST.md)) で進捗を追跡できます。

### 実務応用について

**Q: 自分たちの業務に合わせてカスタマイズできるか？**

A: はい。Module 6（エージェント開発）と Module 7（Skill/Commands）で、カスタム Command や Skill を作成できます。

**Q: 組織全体での導入を考えているが？**

A: ライセンスガイドと企業向けカスタマイズについて Issue で相談してください。

**Q: セキュリティを厳しくする必要があるが？**

A: [セキュリティガードレール](docs/security-guardrails.md) を参照し、エンタープライズ向けの設定も可能です。

---

## コントリビューション

皆さんのフィードバックや改善提案を歓迎します！

### バグ報告・機能リクエスト

1. [Issues](https://github.com/minicoohei/ai-agent-camp/issues) で既出かどうか確認
2. 新しい Issue がある場合は作成
3. テンプレートに従って詳細情報を記入

### Pull Request

1. このリポジトリを Fork
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. コミット (`git commit -m 'Add amazing feature'`)
4. ブランチに Push (`git push origin feature/amazing-feature`)
5. Pull Request を作成

### ドキュメント改善

誤字修正や説明の改善も大歓迎です。下記の形式で PR をお送りください：

- 対象ファイルを明記
- 改善理由を記載
- 可能なら修正案を提示

### 日本語での質問・相談

Issue は日本語での記載で OK です。日本語コミュニティとして運営しています。

---

## サポート

### ドキュメント

- 📖 [ドキュメント一覧](#ドキュメント)
- 🎓 [コースサイト](https://ai-agent.camp/ja/course/module-0)
- 🔧 [トラブルシューティング](docs/troubleshoot.md)

### 質問・相談

| 方法 | 用途 |
|------|------|
| [GitHub Issues](https://github.com/minicoohei/ai-agent-camp/issues) | バグ報告、機能リクエスト、技術的な質問 |
| [Discussions](https://github.com/minicoohei/ai-agent-camp/discussions) | 一般的な質問、情報交換、アイデア提案 |

### コマンドでのヘルプ

```bash
# セットアップ確認
Cursor: /check-setup
Codex: aiagent-check-setup

# 使い方ガイド
/guide

# プロジェクト概要
/overview

# 対話型ヘルプ
/tutor

# 特定のモジュールについて
/help-module-1
```

### その他のリソース

- **公式リポジトリ**: [github.com/minicoohei/ai-agent-camp](https://github.com/minicoohei/ai-agent-camp)
- **Issue トラッカー**: [Issues](https://github.com/minicoohei/ai-agent-camp/issues)
- **Release ノート**: [Releases](https://github.com/minicoohei/ai-agent-camp/releases)

---

## 関連リソース

### 公式ドキュメント

- [Claude AI Documentation](https://claude.ai/docs)
- [Cursor Official Docs](https://cursor.com/docs)
- [Google Gemini API Docs](https://ai.google.dev/docs)

### コミュニティ

- [Claude Community Discord](https://discord.gg/claude)
- [Cursor Community](https://community.cursor.sh)

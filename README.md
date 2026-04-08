# ai-agent-camp

**非エンジニア向けAIエージェント研修 - Claude Code / Cursor / Codex 活用完全ガイド**

[![GitHub](https://img.shields.io/badge/GitHub-minicoohei%2Faiagent--base-181717?style=flat&logo=github)](https://github.com/TokenPocket/ai-agent-camp)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)](https://github.com/TokenPocket/ai-agent-camp/releases)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776ab.svg?style=flat&logo=python)](https://www.python.org/)

## 目次

- [プロジェクト概要](#プロジェクト概要)
- [主な特徴](#主な特徴)
- [クイックスタート](#クイックスタート)
- [ツール別の違い](#ツール別の違い)
- [学習パス](#学習パス)
- [ディレクトリ構造](#ディレクトリ構造)
- [スキルマトリックス](#スキルマトリックス)
- [必要なAPI](#必要なapi)
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
- すぐに業務で使える80個のコマンド
- 実装済みの42個のスキル（マーケティング・LP/HP制作を含む）
- 業務別のワークフローサンプル

📚 **包括的なカリキュラム**
- AI基礎（Foundation）11チャプター
- 環境セットアップ（Setup）3チャプター
- 20個のコアモジュール（Google Workspace・動画制作・要件定義・マーケティング等を含む）
- CursorBootcamp YAML メタデータ対応（全25チャプター）
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
   - **Your old repository's clone URL**: `https://github.com/TokenPocket/ai-agent-camp.git`
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
git clone --bare https://github.com/TokenPocket/ai-agent-camp.git my-aiagent.git
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
git remote add upstream https://github.com/TokenPocket/ai-agent-camp.git

# 更新を取り込む
git fetch upstream
git merge upstream/main
```

Cursor を使っている場合は、チャットで **`/update-material`** を実行すると同様の操作ができます。

> **注意**: 自分で変更を加えている場合、コンフリクトが発生する可能性があります。その場合は手動で解決してください。

### インストール手順

#### 1. リポジトリをクローン

```bash
git clone https://github.com/TokenPocket/ai-agent-camp.git ~/ai-agent-camp
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
# 推奨: venv を使用
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows

# パッケージのインストール
pip install -r requirements.txt
```

#### 4. コースを開始

```bash
# ブラウザで教材を開く
open https://ai-agent.camp/ja/course/module-0

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

AI エージェントの基本を学びます。11チャプターで幅広く理解します。

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

`courses/aiagent/` に、CursorBootcamp プラットフォーム向けの YAML メタデータを配備しています。各チャプターには `practice/`（演習）と `final/`（最終課題）が含まれます。

| レッスン | チャプター数 | 内容 |
|---------|-----------|------|
| **Lesson 01: Foundation** | 11 | LLM基礎、Token、Agent、Context Engineering、MCP、マルチモーダル、RAG、SubAgent、ハルシネーション、セキュリティ |
| **Lesson 02: Setup** | 3 | 環境構築、拡張機能、API設定 |
| **Lesson 03: Core** | 12 | Banner ～ Marketing（全コアモジュール対応） |

合計 **26 チャプター**、全チャプターに practice/final コンテンツ付き。

---

## ディレクトリ構造

```
ai-agent-camp/
│
├── 📚 courses/                         # カリキュラム source of truth
│   ├── index.html                      # ポータルページ
│   ├── CURRICULUM.md                   # カリキュラム全体
│   ├── MODULES_GUIDE.md                # モジュールガイド
│   │
│   ├── foundation/                     # AI 基礎 (4 セクション)
│   │   ├── 0-1-llm-basics.html         # LLM 基本原理
│   │   ├── 0-2-tokens.html             # Token 概念
│   │   ├── 0-3-ai-agents.html          # AI エージェント入門
│   │   └── 0-4-context.html            # Context Engineering
│   │
│   ├── setup/                          # セットアップガイド (3 セクション)
│   │   ├── 0-setup.html                # 環境構築
│   │   ├── 0-5-extensions.html         # 拡張機能
│   │   └── 0-9-api-setup.html          # API 設定
│   │
│   ├── modules/                        # 13 個のコアモジュール
│   │   ├── 1-banner/                   # バナー・画像生成
│   │   ├── 2-diagram/                  # 図表・フロー作成
│   │   ├── 3-screenshot/               # スクリーンショット分析
│   │   ├── 4-data/                     # データ分析
│   │   ├── 5-pptx/                     # PPTX 解析・編集
│   │   ├── 6-search/                   # Slack 検索・分析
│   │   ├── 7-video/                    # AI 動画生成
│   │   ├── 8-gas/                      # GAS 自動化
│   │   ├── 9-actions/                  # GitHub Actions
│   │   ├── 10-notion/                  # Notion 連携
│   │   ├── 11-agent/                   # AI エージェント開発
│   │   ├── 12-marketing/              # マーケティング（NEW）
│   │   └── 13-lp/                     # LP/HP 制作（NEW）
│   │
│   ├── exercises/                      # 実践演習
│   │   ├── basic/                      # 基本演習
│   │   │   ├── workflow-support.md     # カスタマーサポート
│   │   │   ├── workflow-sales.md       # セールスプロセス
│   │   │   ├── workflow-content.md     # コンテンツ作成
│   │   │   └── workflow-onboarding.md  # オンボーディング
│   │   │
│   │   ├── samples/                    # サンプルコード
│   │   │   ├── workflows/              # ワークフローサンプル
│   │   │   ├── slack/                  # Slack 連携サンプル
│   │   │   └── screenshots/            # スクリーンショット例
│   │   │
│   │   └── advanced/                   # 高度な演習（将来拡張）
│   │
│   ├── assets/                         # 画像・スタイルシート (style.css 共有)
│   └── images/                         # 教材用画像
│
├── 📚 courses/                         # CursorBootcamp YAML メタデータ（NEW）
│   └── aiagent/
│       ├── course.yaml                 # コース全体定義
│       ├── cover.png                   # コースカバー画像
│       ├── lesson01-foundation/        # 基礎知識（11 チャプター）
│       │   └── ch01 ~ ch11/           # LLM, Token, Agent, MCP, RAG, Security 等
│       ├── lesson02-setup/             # 環境構築（3 チャプター）
│       │   └── ch01 ~ ch03/           # 環境, 拡張機能, API設定
│       └── lesson03-core/              # コアスキル（12 チャプター）
│           └── ch01 ~ ch12/           # Banner ～ Marketing（practice/final 付き）
│
├── 💻 .cursor/commands/                # 80 個のコマンド
│   ├── lesson/                         # 学習用コマンド (52 個)
│   │   ├── /start-0-1 ~ /start-0-8    # Module 0: Setup
│   │   ├── /start-1-1 ~ /start-1-3    # Module 1: バナー
│   │   ├── /start-2-1 ~ /start-2-3    # Module 2: 図解
│   │   ├── /start-3-1 ~ /start-3-6    # Module 3: チュートリアル
│   │   ├── /start-4-1 ~ /start-4-7    # Module 4: Google Workspace
│   │   ├── /start-5-1 ~ /start-5-2    # Module 5: PPTX
│   │   ├── /start-6-1 ~ /start-6-5    # Module 6: エージェント開発
│   │   ├── /start-7-1 ~ /start-7-8    # Module 7: Skill/Commands
│   │   ├── /start-8-1 ~ /start-8-4    # Module 8: データ分析
│   │   ├── /start-9-1 ~ /start-9-2    # Module 9: Slack連携
│   │   ├── /start-10-1 ~ /start-10-3  # Module 10: GAS
│   │   ├── /start-11-1 ~ /start-11-2  # Module 11: GitHub Actions
│   │   ├── /start-12-1 ~ /start-12-6  # Module 12: Notion
│   │   ├── /start-13-1 ~ /start-13-5  # Module 13: LP制作
│   │   ├── /start-14-1 ~ /start-14-7  # Module 14: 記事制作
│   │   ├── /start-15-1 ~ /start-15-8  # Module 15: 動画制作
│   │   ├── /start-16-1 ~ /start-16-8  # Module 16: メール/LINE自動化
│   │   ├── /start-17-1 ~ /start-17-4  # Module 17: マーケティング
│   │   ├── /start-18-1 ~ /start-18-20 # Module 18: 要件定義/システム開発
│   │   ├── /start-19-1               # Module 19: Outlook（準備中）
│   │   └── /start-20-1               # Module 20: Freee/MoneyForward（準備中）
│   │
│   └── utility/                        # ユーティリティコマンド (28 個)
│       ├── /check-setup                # セットアップ確認
│       ├── /overview                   # プロジェクト概要
│       ├── /guide                      # 使い方ガイド
│       ├── /tutor                      # 対話型ヘルプ
│       ├── /update-material            # 教材を最新版に更新
│       └── ... その他のヘルパー
│
├── 🛠️ skills/                            # 42 個の再利用可能スキル
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
├── 🗂️ data/                            # lesson / Codex 実行に必要な最小データ
│   ├── codex-command-manifest.json     # Codex ルーティング定義
│   ├── google-sync/                    # Google 同期用スクリプトとテンプレート
│   ├── slack-sync/                     # Slack 同期用スクリプトとデータ置き場
│   └── videos/                         # 動画レッスン用サンプル
│
├── 🧪 tests/                            # テストスイート
│   ├── unit/                           # ユニットテスト
│   ├── integration/                    # 統合テスト
│   └── e2e/                            # エンドツーエンドテスト
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
│   ├── setup-guides/                   # API 設定ガイド
│   │   ├── GEMINI_API_SETUP.md
│   │   ├── SLACK_TOKEN_SETUP.md
│   │   ├── GOOGLE_OAUTH_SETUP.md
│   │   ├── BIGQUERY_SETUP.md
│   │   ├── NOTION_API_SETUP.md
│   │   └── ... その他
│   │
│   └── best-practices/                 # ベストプラクティス
│       ├── security.md                 # セキュリティガイド
│       ├── performance.md              # パフォーマンス最適化
│       └── workflows.md                # ワークフロー設計
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
├── CLAUDE.md                           # Claude Code ガイド
├── PROGRESS_CHECKLIST.md               # 学習進捗チェックリスト
├── package.json                        # NPM パッケージ設定
├── requirements.txt                    # Python 依存パッケージ
├── requirements-test.txt               # テスト用パッケージ
└── README.md                           # このファイル
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
| **19** | Outlook連携 | Microsoft Office統合（準備中） |
| **20** | Freee/MoneyForward | 会計データ操作（準備中） |

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
| **Notion API** | Notion ワークスペース連携 | [Notion Integrations](https://www.notion.so/my-integrations) | データベース操作 | 12 |

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

- [Gemini API セットアップ](docs/setup-guides/GEMINI_API_SETUP.md)
- [Google OAuth セットアップ](docs/setup-guides/GOOGLE_OAUTH_SETUP.md)
- [BigQuery セットアップ](docs/setup-guides/BIGQUERY_SETUP.md)
- [Slack API セットアップ](docs/setup-guides/SLACK_TOKEN_SETUP.md)
- [Notion API セットアップ](docs/setup-guides/NOTION_API_SETUP.md)

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
| [Commands リファレンス](docs/commands-reference.md) | 80 個のコマンド全体説明 |
| [Skills リファレンス](docs/skills-reference.md) | 42 個のスキル詳細情報 |
| [Claude Code ガイド](CLAUDE.md) | Claude Code 特有の機能解説 |

### API 設定ガイド

すべてのガイドは `docs/setup-guides/` ディレクトリにあります：

```
docs/setup-guides/
├── GEMINI_API_SETUP.md      # Gemini API
├── GOOGLE_OAUTH_SETUP.md    # Google OAuth
├── BIGQUERY_SETUP.md        # BigQuery
├── SLACK_TOKEN_SETUP.md     # Slack
├── NOTION_API_SETUP.md      # Notion
└── ...
```

### ベストプラクティス

| ドキュメント | トピック |
|------------|---------|
| [セキュリティガイド](docs/best-practices/security.md) | API キー管理、データ保護 |
| [パフォーマンス最適化](docs/best-practices/performance.md) | API 利用最適化、バッチ処理 |
| [ワークフロー設計](docs/best-practices/workflows.md) | 効率的な業務フロー |

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

A: [セキュリティガイド](docs/best-practices/security.md) を参照し、エンタープライズ向けの設定も可能です。

---

## コントリビューション

皆さんのフィードバックや改善提案を歓迎します！

### バグ報告・機能リクエスト

1. [Issues](https://github.com/TokenPocket/ai-agent-camp/issues) で既出かどうか確認
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
| [GitHub Issues](https://github.com/TokenPocket/ai-agent-camp/issues) | バグ報告、機能リクエスト、技術的な質問 |
| [Discussions](https://github.com/TokenPocket/ai-agent-camp/discussions) | 一般的な質問、情報交換、アイデア提案 |

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

- **公式リポジトリ**: [github.com/TokenPocket/ai-agent-camp](https://github.com/TokenPocket/ai-agent-camp)
- **Issue トラッカー**: [Issues](https://github.com/TokenPocket/ai-agent-camp/issues)
- **Release ノート**: [Releases](https://github.com/TokenPocket/ai-agent-camp/releases)

---

## 関連リソース

### 公式ドキュメント

- [Claude AI Documentation](https://claude.ai/docs)
- [Cursor Official Docs](https://cursor.com/docs)
- [Google Gemini API Docs](https://ai.google.dev/docs)

### コミュニティ

- [Claude Community Discord](https://discord.gg/claude)
- [Cursor Community](https://community.cursor.sh)

---

## 更新履歴

### v3.0.0（2026-03-29）

- **モジュール大幅拡充**: 13 → 20 モジュールへ拡大
- **モジュール番号リナンバリング**: aiagent-course の表示順序と完全一致するよう全モジュール番号を再編成
- **新規モジュール追加**: Module 4（Google Workspace）、Module 7（Skill/Commands）、Module 14（記事制作）、Module 15（動画制作）、Module 16（メール/LINE自動化）、Module 18（要件定義/システム開発）、Module 19（Outlook）、Module 20（Freee/MoneyForward）
- **レッスン数**: 119 レッスン（start-0-1 〜 start-20-1）
- **Trigger Word 導入**: 全レッスンの description に `When the user says /start-N-M` 形式を適用し、Skill 発動率を向上
- **3ツール完全同期**: .claude/commands/lesson/ と .cursor/commands/lesson/ が完全同一

### v2.0.0（2026-02-10）

- **モジュール追加**: Module 12（マーケティング）、Module 13（LP/HP 制作）
- **スキル大幅拡充**: 20 → 42 個（マーケティング系 20 スキル、PPTX Converter/Creator、LP Designer 追加）
- **CursorBootcamp 対応**: `courses/aiagent/` に YAML メタデータレイヤー追加（3 レッスン・26 チャプター）
- **教材全面リニューアル**: Foundation/Setup/Index 全 22 ページを新フォーマットに統一
- **practice/final コンテンツ**: 全 25 チャプターに演習・最終課題を配備
- **品質改善**: CodeRabbit レビュー対応、共有スタイルシート (style.css) 導入、Clipboard API エラーハンドリング追加
- **コマンド追加**: 77 → 80 個（Module 12/13 のレッスンコマンド、ユーティリティ追加）

### v1.0.0（2025-02-02）

- 初回リリース
- Foundation（4 セクション）
- Setup（3 セクション）
- Core Modules（11 モジュール）
- 20 個のスキル、77 個のコマンド

詳細は [CHANGELOG.md](CHANGELOG.md) を参照してください。

---

## 最後に

このプロジェクトは、**AI を「専門家だけのツール」から「すべての職種が活用できるツール」へ民主化する**という目標の下で開発されています。

AIの力を活用して、あなたの仕事をより効率的に、より創造的に。

Happy Learning! 🚀

---

<div align="center">

**Made with ❤️ for non-engineers who want to master AI agents**

[Star us on GitHub](https://github.com/TokenPocket/ai-agent-camp) | [Report a Bug](https://github.com/TokenPocket/ai-agent-camp/issues) | [Request a Feature](https://github.com/TokenPocket/ai-agent-camp/issues)

</div>

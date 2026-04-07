# AIエージェント研修 カリキュラム

## コース概要

- **対象**: 非エンジニア（マーケ、営業、企画等）
- **形式**: セルフペース学習
- **総時間**: 約51時間（Foundation 5時間 + Setup 1時間 + Core 45時間）
- **モジュール数**: 32（Foundation 12 + Setup 3 + Core 17）

## 学習目標

このコースを修了すると、以下のスキルを習得できます：

1. AIエージェントの基本概念と仕組みの理解
2. Claude Code / Cursor を使った実務タスクの自動化
3. 各種API連携による業務効率化
4. 社内ツールとの統合による生産性向上

---

## 学習パス

### Phase 1: 基礎知識（Foundation）

AIエージェントを使いこなすための基礎知識を学びます。

| モジュール | 内容 | 時間 | コマンド |
|-----------|------|------|---------|
| 0-1 | LLM基礎 | 30分 | 教材ページ参照 |
| 0-2 | Token概念 | 30分 | 教材ページ参照 |
| 0-3 | AIエージェント | 30分 | 教材ページ参照 |
| 0-4 | Context Engineering | 30分 | 教材ページ参照 |
| 0-5 | Cursorの使い方 | 25分 | 教材ページ参照 |
| 0-5.5 | Claude Code概要 | 25分 | 教材ページ参照 |
| 0-6 | MCP（Model Context Protocol） | 25分 | 教材ページ参照 |
| 0-7 | マルチモーダルAI | 25分 | 教材ページ参照 |
| 0-8 | RAG | 25分 | 教材ページ参照 |
| 0-9 | Skill / SubAgent / Agent Team | 25分 | 教材ページ参照 |
| 0-10 | ハルシネーション | 25分 | 教材ページ参照 |
| 0-11 | AIセキュリティ | 25分 | 教材ページ参照 |
| 0-12 | Extended Thinking | 15分 | 教材ページ参照 |

**学習内容**:
- LLM（大規模言語モデル）の動作原理
- トークンとコンテキストウィンドウの理解
- エージェントとアシスタントの違い
- 効果的なプロンプト設計
- Cursorの画面・モード・安全設定の基礎
- Claude Codeの概要・インストール・基本操作
- MCPプロトコルによるAIとツール連携
- マルチモーダルAI（画像・テキスト・音声統合）
- RAG（検索拡張生成）の仕組みと活用
- Skill/SubAgent/Agent Teamの活用と使い分け
- ハルシネーションの理解と対策
- AIセキュリティの基礎知識
- Extended Thinking（拡張思考）の仕組みと活用

### Phase 2: 環境構築（Setup）

学習に必要な環境を整えます。全てAIが対話形式で自動実行するため、CLIコマンドの入力は不要です。

| ステップ | 内容 | 時間 | コマンド |
|---------|------|------|---------|
| 1 | 基本ツール確認 | 10分 | `/setup-start` |
| 1.5 | Claude Code インストール | 15分 | 教材ページ参照 |
| 2 | GitHub設定 | 10分 | `/setup-github` |
| 3 | 拡張機能 | 5分 | `/setup-extensions` |
| 4 | Gemini API設定 | 10分 | `/setup-gemini` |
| 5 | Slack API設定 | 15分 | `/setup-slack` |
| 6 | セキュリティ設定 | 5分 | `/setup-security` |
| 7 | 総合チェック | 5分 | `/check-setup` |

**レッスンラッパーコマンド**（上記 setup-* への誘導）:

| コマンド | 内容 |
|---------|------|
| `/start-0-1` | 環境セットアップ確認（/setup-start + /setup-github） |
| `/start-0-2` | 拡張機能インストール（/setup-extensions） |
| `/start-0-3` | Gemini API設定（/setup-gemini） |
| `/start-0-4` | Slack API設定（/setup-slack） |
| `/start-0-5` | セキュリティ設定（/setup-security） |

**セットアップ内容**:
- Python / Node.js / Git / GitHub CLI のインストール確認
- Claude Code のインストールと初期設定
- VS Code拡張機能の自動インストール
- 必要なAPIキーの取得と設定（.envファイル直接編集方式）
- セキュリティ設定（.gitignore + pre-commitフック）

### Phase 3: コアスキル（Core Modules）

実践的なスキルを身につけます。

| モジュール | 内容 | 時間 | レッスン数 | コマンド |
|-----------|------|------|-----------|---------|
| 1 | バナー・画像生成 | 90分 | 3 | `/start-1-1` ~ `/start-1-3` |
| 2 | 図表・フロー作成 | 80分 | 3 | `/start-2-1` ~ `/start-2-3` |
| 3 | スクリーンショット注釈 | 170分 | 6 | `/start-3-1` ~ `/start-3-6` |
| 4 | データ分析・抽出 | 130分 | 4 | `/start-8-1` ~ `/start-8-4` |
| 5 | PowerPoint/スライド作成 | 55分 | 2 | `/start-5-1`, `/start-5-2` |
| 6 | セマンティック検索 | 50分 | 2 | `/start-9-1`, `/start-9-2` |
| 7 | 動画生成 | 285分 | 8 | `/start-13-1` ~ `/start-13-8` |
| 8 | GAS自動化 | 85分 | 3 | `/start-10-1` ~ `/start-10-3` |
| 9 | GitHub Actions | 70分 | 2 | `/start-11-1`, `/start-11-2` |
| 10 | Notion連携 | 60分 | 2 | `/start-12-1`, `/start-12-2` |
| 11 | エージェント開発 | 275分 | 9 | `/start-6-1` ~ `/start-6-9` |
| 12 | マーケティング | 140分 | 4 | `/start-17-1` ~ `/start-17-4` |
| 13 | LP/HP制作 | 120分 | 5 | `/start-15-1` ~ `/start-15-5` |
| 14 | PM & システム要件定義 | 550分 | 20 | `/start-18-1` ~ `/start-18-20` |
| 15 | メール自動化 | 150分 | 5 | `/start-16-1` ~ `/start-16-5` |
| 16 | 記事作成 | 230分 | 7 | `/start-14-1` ~ `/start-14-7` |
| 18 | AI秘書 — Google Workspace 統合活用 | 180分 | 6 | `/start-18-1` ~ `/start-18-6` |

---

## モジュール詳細

### Module 1: バナー・画像生成
SNS投稿やプレスリリース用のバナーを自動生成します。

**学習内容**:
- Gemini Image Generation APIの活用
- プラットフォーム別サイズ設定（X, Instagram, Facebook等）
- トーン・配色の指定方法
- コピーテキストの同時生成

**使用スキル**: `banner-creator`, `nanobanana`

### Module 2: 図表・フロー作成
テキストから図解やフローチャートを自動生成します。

**学習内容**:
- インフォグラフィック生成
- PlantUML図の作成
- フロー図・組織図の作成
- Mermaid記法の活用

**使用スキル**: `diagram-generator`

### Module 3: スクショ分析
スクリーンショットの解析とチュートリアル作成を行います。

**学習内容**:
- エラー画面の自動診断
- 操作手順のステップ化
- 注釈付きスクリーンショットの作成
- マニュアル自動生成

**使用スキル**: `screenshot-analyzer`, `screenshot-annotator`, `tutorial-generator`

### Module 4: データ分析
BigQuery/Snowflakeに接続してデータ分析を行います。

**学習内容**:
- GCP認証とBigQuery接続
- 探索的データ分析（EDA）
- 可視化グラフの作成
- Marimoノートブック活用

**使用スキル**: `data-analyst`, `bigquery-auth`

### Module 5: PPTX解析・編集
PowerPointファイルの解析と自動編集を行います。

**学習内容**:
- スライド構造の解析
- テンプレート抽出
- テキスト差し替え
- 新規スライド生成

**使用スキル**: `pptx-analyzer`, `document-processor`

### Module 6: Slack検索・分析
Slackデータのセマンティック検索と分析を行います。

**学習内容**:
- チャンネル検索・詳細取得
- 人物・イベント検索
- タイムライン分析
- TODO抽出

**使用スキル**: `slack-search.skill`, `slack-task-manager`

### Module 7: 動画生成
AI UGC動画の絵コンテ作成と動画生成を行います。

**学習内容**:
- 絵コンテ（ストーリーボード）生成
- キャラクター一貫性の維持
- Kling APIによる動画生成
- 縦型/横型フォーマット対応

**使用スキル**: `storyboard-generator`, `video-frame-reader`

### Module 8: GAS自動化
Google Apps Scriptの自動デプロイと実行を行います。

**学習内容**:
- clasp CLIの活用
- 複数プロジェクト管理
- 関数のテスト実行
- 自動デプロイ設定

**使用スキル**: `gas-clasp-ops`

### Module 9: GitHub Actions
CI/CD自動化とワークフロー作成を行います。

**学習内容**:
- GitHub Actionsの基礎
- ワークフロー定義
- 定期実行の設定
- Secrets管理

### Module 10: Notion連携
NotionデータベースとAIの連携を行います。

**学習内容**:
- Notion API設定
- データベース操作
- ページ作成・更新
- 自動連携フロー

### Module 11: エージェント開発
カスタムAIエージェントの開発方法を学びます。

**学習内容**:
- Skillファイルの作成
- Commandの定義
- SubAgent/Agent Teamの設計と並列実行
- カスタムSubAgentの作成（.claude/agents/）
- TeamAgentによるプロジェクト管理

**スキル作成マスタートラック**（Lesson 11-6〜11-9）:
- Anthropic公式ガイドに基づくスキル設計（3カテゴリ、Progressive Disclosure）
- SKILL.mdの実装（YAMLフロントマター、ディレクトリ構造）
- テストとイテレーション（トリガー/機能/パフォーマンステスト）
- 5つの設計パターン（Sequential Workflow、Multi-MCP等）

**参考資料**: [スキルエコシステム戦略](https://ai-agent.camp/ja/course/module-6) — 外部プラグインの統合戦略とSkillsBench論文に基づくエビデンス

### Module 12: マーケティング
AIスキルを活用したマーケティングコンテンツの作成と運用を学びます。

**学習内容**:
- SNS投稿コンテンツ作成（social-content + banner-creator）
- SEO監査とキーワード戦略（seo-audit + programmatic-seo）
- マーケティングコピー作成（copywriting）
- Pencil MCPによるデザインモックアップ

### Module 13: LP/HP制作
ランディングページ・ホームページを一気通貫で制作します。

**学習内容**:
- AskQuestionによるヒアリングと訴求整理
- ASCII / ビジュアルワイヤーフレーム作成
- Pencil MCPによるプロ品質のデザイン
- HTML/CSS(Tailwind)/JSによるLP実装
- Vercel CLIによるデプロイ・公開

**使用スキル**: `lp-designer`, `diagram-generator`, `nanobanana`

**3段階の体験**:
1. テキストベースでシンプルLP作成
2. 複数セクション構成のHP制作
3. Pencilデザイン → コード変換 → Vercelデプロイ

### Module 14: PM & システム要件定義
タスク管理アプリ「TaskFlow」を題材に、企画から設計・実装・テスト・運用まで、AI活用でプロダクト開発の全工程を体験します。

**学習内容**:
- Phase A（企画）: 顧客インタビュー、要求資料、PRD作成、3種レビュー
- Phase B（要件定義・設計）: 要件定義書、ユースケース・シーケンス図、画面遷移図、DB設計、API設計、WBS、Notion連携
- Phase C（デザイン・実装）: UIデザイン（Pencil MCP）、HTML+Tailwindプロトタイプ、Playwright E2Eテスト
- Phase D（テスト・運用）: テスト計画書、単体テスト、結合テスト、会議体設計・議事録分析、marimoダッシュボード、総合演習

**使用スキル**: `pm-toolkit`, `test-planner`, `monitoring-dashboard`, `diagram-generator`, `notion-db`

### Module 15: メール自動化
gogcli（gog コマンド）を使って Gmail の認証・検索・送信を行い、AIエージェントでメール業務を自動化します。

**学習内容**:
- gogcli セットアップと Gmail 認証
- check-inbox によるメール分析・タスク抽出・優先度判定
- gog gmail send によるメール送信・スレッド返信・添付ファイル
- email-sequence によるドリップキャンペーン・シーケンス設計
- GitHub Actions によるメール自動化ワークフロー構築

**使用ツール/スキル**: `gogcli (gog)`, `check-inbox`, `email-sequence`, `google-sync`

### Module 16: 記事作成
AIエージェントを活用した記事執筆の全工程（企画→文体学習→執筆→挿絵→校閲→ファクトチェック→公開）を学びます。

**学習内容**:
- テーマ決定とアウトライン自動生成
- ユーザーの文章を読み込ませた文体プロファイル作成
- スタイル適用による記事ドラフト生成
- nanobanana / PlantUMLによる挿絵自動生成
- 校閲エージェントによるレビュー（5 Sweeps）
- ファクトチェックエージェントによる事実検証
- 複数テーマの並列実行

**使用スキル**: `article-writer`, `style-analyzer`, `proofreading-agent`, `fact-checker`, `nanobanana`, `diagram-generator`

### Module 18: AI秘書 — Google Workspace 統合活用

gogcli を使って Google Calendar / Gmail / Drive / Sheets を AI から操作する統合モジュール。
「来週の空きで1on1入れといて」を一言で実現する AI秘書ワークフローを構築します。

| レッスン | 内容 | 時間 |
|---------|------|------|
| 18-1 | 秘書を雇う — Google認証 & 環境構築 | 25分 |
| 18-2 | スケジュール調整 — Calendar を AI で管理 | 35分 |
| 18-3 | 朝のブリーフィング — 返信漏れ & メール下書き | 30分 |
| 18-4 | ファイル管理 — Google Drive 操作 | 30分 |
| 18-5 | データ連携 — Sheets / Excel 操作 | 30分 |
| 18-6 | 定型業務の自動化 — GAS × gogcli 統合 | 30分 |

**学習内容**:
- gogcli による Google Calendar の検索・作成・更新・削除
- Gmail の受信分析・タスク抽出・返信下書き生成
- Google Drive のファイル検索・アップロード・フォルダ操作
- Google Sheets の読み書き・データ変換
- GAS と gogcli を組み合わせた定型業務の自動化ワークフロー

**使用ツール/スキル**: `gogcli (gog)`, `check-inbox`, `gas-clasp-ops`, `google-sync`

---

## 推奨学習順序

### 必須パス（全員）
```
Foundation (0-1 ~ 0-5) → Setup (0, 0.5, 0.9)
```

### 役職別推奨パス

**マーケティング担当**:
```
必須パス → Module 1 (バナー) → Module 2 (図表) → Module 7 (動画)
```

**営業担当**:
```
必須パス → Module 5 (PPTX) → Module 6 (Slack) → Module 10 (Notion)
```

**企画・分析担当**:
```
必須パス → Module 4 (データ分析) → Module 3 (スクショ) → Module 6 (Slack)
```

**業務効率化担当**:
```
必須パス → Module 8 (GAS) → Module 9 (Actions) → Module 11 (エージェント)
```

---

## 必要なAPI

| API | 必須/任意 | 使用モジュール | 取得方法 |
|-----|----------|---------------|---------|
| Gemini API | 必須 | 全モジュール | [GEMINI_API_SETUP.md](../docs/setup-guides/GEMINI_API_SETUP.md) |
| Slack API | Module 6 | Slack検索 | [SLACK_TOKEN_SETUP.md](../docs/setup-guides/SLACK_TOKEN_SETUP.md) |
| Google OAuth | Module 4, 8 | データ分析, GAS | [GOOGLE_OAUTH_SETUP.md](../docs/setup-guides/GOOGLE_OAUTH_SETUP.md) |
| BigQuery | Module 4 | データ分析 | [BIGQUERY_SETUP.md](../docs/setup-guides/BIGQUERY_SETUP.md) |
| FAL/Kling | Module 7 | 動画生成 | 別途案内 |
| Notion API | Module 10 | Notion連携 | [NOTION_API_SETUP.md](../docs/setup-guides/NOTION_API_SETUP.md) |

---

## 学習の進め方

### 1. モジュールの開始
```bash
/start-{モジュール番号}
```
例: `/start-1-1`

### 2. 演習の実行
各モジュールの指示に従って演習を実行します。

### 3. 進捗確認
```bash
/check-setup    # 環境確認
/exercise-review # 演習レビュー
```

### 4. 質問・サポート
- Slackの#ai-agent-helpチャンネルで質問
- よくある問題は[troubleshoot.md](../docs/troubleshoot.md)を参照

---

## 修了条件

1. **Foundation**: 全12モジュール完了
2. **Setup**: 環境構築完了（`/check-setup` でPASS）
3. **Core**: 11モジュール以上の演習完了（`/exercise-review` で進捗確認）

修了後は修了証を発行します。

---

## YAML メタデータ構造（CursorBootcamp 対応）

本コースは `courses/aiagent/` 配下に YAML メタデータを持ちます：

```
courses/aiagent/
├── course.yaml                  # コース全体定義
├── lesson01-foundation/         # Foundation（11チャプター）
│   ├── lesson.yaml
│   └── ch01-llm-basics/ ~ ch11-security/
│       ├── chapter.yaml
│       ├── practice/
│       └── final/
├── lesson02-setup/              # Setup（3チャプター）
│   ├── lesson.yaml
│   └── ch01-environment/ ~ ch03-api-settings/
└── lesson03-core/               # Core（13チャプター）
    ├── lesson.yaml
    └── module01-banner/ ~ module18-pm-sysdef/
```

各 `chapter.yaml` は `externalContent` で既存 HTML 教材を参照します。

> **Note**: Module 13 (LP/HP制作)、15 (メール自動化)、16 (記事作成) は HTML 教材として存在しますが、YAML チャプターは未登録です。そのため YAML 上の `module18-pm-sysdef` はモジュール番号 14（PM & システム要件定義）に対応します。

---

## 更新履歴

- 2026-02-10: Foundation 0.8をSkill/SubAgent/Agent Teamに変更。Module 2-8の演習を充実（各4演習）。Module 3をリネーム。Module 12（マーケティング）を新規追加。Module 11にSubAgent並列実行演習を追加。CRO系6スキルを削除。
- 2026-02-10: Foundation に6チャプター追加（MCP, マルチモーダル, RAG, Skill/SubAgent/Agent Team, ハルシネーション, セキュリティ）。CursorBootcamp YAML メタデータ追加。
- 2026-02-02: 初版作成
- Module 11 (エージェント開発) を追加

---
最終更新: 2026-02-24 JST

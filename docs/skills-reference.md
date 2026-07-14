# スキルリファレンス完全ガイド

**対応スキル数**: 102個

最終更新: 2026-07-14

---

## 目次

1. [クイックスタート](#クイックスタート)
2. [スキル一覧](#スキル一覧)
3. [インストール方法](#インストール方法)
4. [スキルの実行方法](#スキルの実行方法)
5. [トラブルシューティング](#トラブルシューティング)
6. [FAQ](#faq)
7. [参考リンク](#参考リンク)

---

## クイックスタート

### スキルとは

スキルは、この repo で再利用するための機能単位です。  
Codex では `skills/` の SKILL.md を入口に使い、Claude Code でも同じスキル定義を参照します。

### スキルの使用方法

```text
Codex:
- SKILL.md を読む
- 必要なら python script を直接実行する

Claude Code:
- 同じ SKILL.md を参照して Claude 側の実行フローに載せる

共通:
- scripts があれば `python skills/スキル名/scripts/...` で直接実行できる
```

### よく使うスキル TOP 5

| # | スキル | 用途 | 難易度 |
|---|--------|------|--------|
| 1 | `banner-creator` | SNSバナー生成 | 初心者 |
| 2 | `nanobanana` | 画像生成・編集 | 初心者 |
| 3 | `screenshot-analyzer` | エラー診断・チュートリアル生成 | 初級 |
| 4 | `data-analyst` | BigQuery・EDA・可視化 | 中級 |
| 5 | `document-processor` | PDF・PPTX・Excel処理 | 中級 |

---

<!-- AUTO-GENERATED:skills START -->
## スキル一覧

既存カテゴリを引き継ぎ、新しく検出したスキルは「未分類」に追加します。

### 画像生成・編集系スキル（4個）

| スキル | 説明 | 定義 |
|---|---|---|
| `banner-creator` | 各種SNS・広告プラットフォーム向けのバナー/クリエイティブを生成するスキル。 X, Facebook, Instagram, PRTimes, YouTube, LINE, Web広告に対応。 「バナーを作って」「広告画像を生成」「SNS用の画像」「クリエイティブ制作」等のリクエストで発動。 | [`skills/banner-creator/SKILL.md`](../skills/banner-creator/SKILL.md) |
| `diagram-generator` | Gemini Image Generation API でテキストから図解・インフォグラフィック・ダイアグラムを生成するスキル。 「図を作って」「インフォグラフィック生成」「プロセスを図解して」等のリクエストで発動。 | [`skills/diagram-generator/SKILL.md`](../skills/diagram-generator/SKILL.md) |
| `nanobanana` | Gemini画像生成APIでテキストから画像生成、既存画像の編集を行うスキル。 「画像を生成して」「イラストを作って」「写真を編集して」等のリクエストで発動。 | [`skills/nanobanana/SKILL.md`](../skills/nanobanana/SKILL.md) |
| `screenshot-annotator` | スクリーンショットに赤枠・矢印・吹き出し等の注釈を自動追加するスキル。 「スクショに注釈を付けて」「画面に矢印を追加」「マニュアル用の注釈」等のリクエストで発動。 | [`skills/screenshot-annotator/SKILL.md`](../skills/screenshot-annotator/SKILL.md) |

### データ分析・処理系スキル（4個）

| スキル | 説明 | 定義 |
|---|---|---|
| `bigquery-auth` | GCPプロジェクト単位でBigQuery認証を設定するスキル。 gcloud設定プロファイルで複数プロジェクトを安全に分離管理。 「BigQueryに繋ぎたい」「BQ認証」「gcloud認証」「データ分析の認証設定」等のリクエストで発動。 | [`skills/bigquery-auth/SKILL.md`](../skills/bigquery-auth/SKILL.md) |
| `data-analyst` | BigQuery/Snowflake接続、EDA、可視化、Marimoノートブック作成を行うサブエージェント。 データ分析関連の4つのルール（data_analysis, visualization, notebook, marimo_variable_naming）を統合。 「データ分析して」「BigQueryに接続」「EDAを実行」「Marimoで分析」等のリクエストで発動。 | [`skills/data-analyst/SKILL.md`](../skills/data-analyst/SKILL.md) |
| `gcp-auth` | Google Cloud Platform (GCP) の Application Default Credentials 認証を実行するスキル。 「GCP認証して」「Google Cloud認証」「gcloud login」等のリクエストで発動。 BigQuery や Cloud Storage 等の GCP サービス利用前の認証手順をガイド。 | [`skills/gcp-auth/SKILL.md`](../skills/gcp-auth/SKILL.md) |
| `pptx-analyzer` | PowerPointファイル（.pptx）の構造を解析し、スライド・図形・テキスト情報を出力するスキル。 「PPTXを解析」「テンプレート構造を確認」「スライドの要素を調べて」等のリクエストで発動。 | [`skills/pptx-analyzer/SKILL.md`](../skills/pptx-analyzer/SKILL.md) |

### ドキュメント処理系スキル（3個）

| スキル | 説明 | 定義 |
|---|---|---|
| `document-processor` | PDF/PPTX/Excelファイルの読み取り・編集・分析を行うサブエージェント。 大きなドキュメントの処理をメインコンテキストから分離し、コンテキスト消費を最適化する。 「PDFを分析」「PPTXの内容を読んで」「Excelを解析」「スライドを編集」等のリクエストで発動。 | [`skills/document-processor/SKILL.md`](../skills/document-processor/SKILL.md) |
| `pdf-compressor` | 大きなPDFファイルを圧縮するスキル。ファイルサイズを最大98%削減。 「PDFを圧縮して」「PDFを軽くして」「ファイルサイズを小さくして」等のリクエストで発動。 | [`skills/pdf-compressor/SKILL.md`](../skills/pdf-compressor/SKILL.md) |
| `tutorial-generator` | スクリーンショットからGemini Vision APIで操作チュートリアルを自動生成する。 「操作マニュアルを作って」「スクショから手順書を生成」「使い方ガイドを作成」等で発動。 | [`skills/tutorial-generator/SKILL.md`](../skills/tutorial-generator/SKILL.md) |

### 動画・メディア系スキル（3個）

| スキル | 説明 | 定義 |
|---|---|---|
| `media-generator` | バナー/図表/スライド/画像の生成・編集を行うサブエージェント。 Gemini Image Generation APIを使用して各種メディアを生成する。 「バナーを作って」「図表を生成」「スライドを作成」「画像を生成」等のリクエストで発動。 | [`skills/media-generator/SKILL.md`](../skills/media-generator/SKILL.md) |
| `storyboard-generator` | AI UGC動画用の絵コンテを自動生成するスキル。1枚シート生成→切り出しでキャラクター一貫性を保証。 「絵コンテを作って」「ストーリーボード生成」「UGC動画の流れを作って」等のリクエストで発動。 | [`skills/storyboard-generator/SKILL.md`](../skills/storyboard-generator/SKILL.md) |
| `video-frame-reader` | 動画ファイルからキーフレームを抽出し、重複除去・最適化した上で内容を分析するスキル。 「動画の中身を見て」「キーフレームを抽出」「この動画を分析して」等で発動。 | [`skills/video-frame-reader/SKILL.md`](../skills/video-frame-reader/SKILL.md) |

### API・認証系スキル（2個）

| スキル | 説明 | 定義 |
|---|---|---|
| `gas-clasp-ops` | Google Apps Script (GAS) プロジェクトを clasp 経由で操作するスキル。 「GASをデプロイして」「claspでpush」「GAS関数をテスト」等のリクエストで発動。 push / deploy / run を一括または個別に実行。複数プロジェクト管理に対応。 | [`skills/gas-clasp-ops/SKILL.md`](../skills/gas-clasp-ops/SKILL.md) |
| `slack-search` | Slackチャンネルやメッセージをセマンティック検索するスキル。 「Slackで検索して」「チャンネルを探して」「発言を探して」等のリクエストで発動。 | [`skills/slack-search/SKILL.md`](../skills/slack-search/SKILL.md) |

### Slack・通信系スキル（3個）

| スキル | 説明 | 定義 |
|---|---|---|
| `check-inbox` | メールとSlackから返信すべき項目・タスクを抽出する統合型スキル。 Gemini 3.0 Flashで文脈判定し、優先度と返信ドラフトを生成。 「受信箱チェック」「TODO確認」「返信すべきメッセージ」「メール確認」等のリクエストで発動。 | [`skills/check-inbox/SKILL.md`](../skills/check-inbox/SKILL.md) |
| `slack-task-manager` | Slack検索・TODO抽出・タスク管理を行うサブエージェント。 複数データソースからタスクを抽出し、優先順位付けを行う。 「Slackを検索」「タスクを抽出」「TODO確認」「メンション確認」等のリクエストで発動。 | [`skills/slack-task-manager/SKILL.md`](../skills/slack-task-manager/SKILL.md) |
| `slack-unanswered` | Slackの未返信メッセージを検出し、返信ドラフトを生成するスキル。 「未返信メッセージ」「返信してないメッセージ」「Slack確認」等のリクエストで発動。 | [`skills/slack-unanswered/SKILL.md`](../skills/slack-unanswered/SKILL.md) |

### その他のスキル（1個）

| スキル | 説明 | 定義 |
|---|---|---|
| `screenshot-analyzer` | スクリーンショットからエラー診断や操作チュートリアルを自動生成するスキル。 「スクショを分析して」「画面のエラーを調べて」「操作手順を作って」等のリクエストで発動。 | [`skills/screenshot-analyzer/SKILL.md`](../skills/screenshot-analyzer/SKILL.md) |

### 未分類（82個）

| スキル | 説明 | 定義 |
|---|---|---|
| `ab-test-setup` | A/Bテストや実験の設計・実装を支援するスキル。 「A/Bテストを設計して」「スプリットテストしたい」「仮説を立ててテストしたい」「バリアントを比較」等のリクエストで発動。 トラッキング実装は analytics-tracking を参照。 | [`skills/ab-test-setup/SKILL.md`](../skills/ab-test-setup/SKILL.md) |
| `agent-designer` | マルチエージェントシステムのアーキテクチャ設計ツールキット。 「エージェントを設計して」「マルチエージェント構成」「エージェントのアーキテクチャ」「オーケストレーション設計」等のリクエストで発動。 | [`skills/agent-designer/SKILL.md`](../skills/agent-designer/SKILL.md) |
| `aiagent-check-setup` | ai-agent-campのローカル環境セットアップを確認するスキル。 「セットアップ確認」「環境チェック」「初期設定できてる？」「インストール確認」「依存関係チェック」等のリクエストで発動。 | [`skills/aiagent-check-setup/SKILL.md`](../skills/aiagent-check-setup/SKILL.md) |
| `aiagent-command-router` | ai-agent-campのスラッシュコマンドをCodexでルーティングするスキル。 「/start-0-1を実行」「スラッシュコマンドを使いたい」「コマンドルーティング」「Cursorのコマンドを使いたい」等のリクエストで発動。 | [`skills/aiagent-command-router/SKILL.md`](../skills/aiagent-command-router/SKILL.md) |
| `aiagent-env-manager` | ai-agent-campの環境変数・認証情報を安全に管理するスキル。 「APIキーを設定」「.envを管理」「環境変数の設定」「credential managerを使いたい」「秘密情報の管理」等のリクエストで発動。 | [`skills/aiagent-env-manager/SKILL.md`](../skills/aiagent-env-manager/SKILL.md) |
| `aiagent-guide` | ai-agent-campリポジトリの案内・オリエンテーションスキル。 「リポジトリ案内」「次のレッスンは？」「どこから始める」「ツールの違い」「aiagent概要」等のリクエストで発動。 | [`skills/aiagent-guide/SKILL.md`](../skills/aiagent-guide/SKILL.md) |
| `aiagent-lesson-runner` | ai-agent-campのレッスンをCodexで開始・進行するスキル。 「レッスン開始」「次のレッスン」「start-0-1を始めたい」「Codexでレッスン」「スラッシュコマンドのレッスン」等のリクエストで発動。 | [`skills/aiagent-lesson-runner/SKILL.md`](../skills/aiagent-lesson-runner/SKILL.md) |
| `aiagent-material-sync` | ai-agent-campの教材をupstreamから安全に同期するスキル。 「教材を最新にしたい」「upstreamから更新」「コースを同期」「git pullしたい」「教材アップデート」等のリクエストで発動。 | [`skills/aiagent-material-sync/SKILL.md`](../skills/aiagent-material-sync/SKILL.md) |
| `aiagent-tooling-setup` | ai-agent-camp用のCodexツーリングを設定するスキル。 「MCPサーバーを設定」「フックをインストール」「Codexの設定」「ツールセットアップ」「Codex CLIのインストール」等のリクエストで発動。 | [`skills/aiagent-tooling-setup/SKILL.md`](../skills/aiagent-tooling-setup/SKILL.md) |
| `aiagent-utility-runner` | ai-agent-campのユーティリティ・セットアップコマンドをCodexで実行するスキル。 「/guideを実行」「/setup-api-key」「ユーティリティコマンド」「Cursorのユーティリティを使いたい」等のリクエストで発動。 | [`skills/aiagent-utility-runner/SKILL.md`](../skills/aiagent-utility-runner/SKILL.md) |
| `aiagent-verify-module` | モジュールの完了状況をAI評価で検証するスキル。 「モジュール確認」「モジュール1の達成度」「レッスンの完了チェック」「進捗を検証」「verify module」等のリクエストで発動。 | [`skills/aiagent-verify-module/SKILL.md`](../skills/aiagent-verify-module/SKILL.md) |
| `analytics-tracking` | アナリティクスのトラッキング設定・改善・監査を支援するスキル。 「トラッキングを設定」「GA4を導入」「コンバージョン計測」「イベントトラッキング」「UTMパラメータ」「GTMの設定」等のリクエストで発動。 A/Bテスト計測は ab-test-setup を参照。 | [`skills/analytics-tracking/SKILL.md`](../skills/analytics-tracking/SKILL.md) |
| `article-writer` | テーマからアウトライン生成→文体プロファイル適用→Markdown記事出力を行う記事執筆スキル。 挿絵マーカーの自動挿入、style-analyzerプロファイル参照による文体統一に対応。 「記事を書いて」「ブログ作成」「テーマで記事生成」等のリクエストで発動。 | [`skills/article-writer/SKILL.md`](../skills/article-writer/SKILL.md) |
| `code-reviewer` | TypeScript, JavaScript, Python, Go, Swift, Kotlin対応のコードレビュー自動化スキル。 PRの複雑度・リスク分析、SOLID違反・コードスメルの検出、レビューレポート生成。 「コードレビューして」「PRを分析」「コード品質チェック」「レビューレポート」等のリクエストで発動。 | [`skills/code-reviewer/SKILL.md`](../skills/code-reviewer/SKILL.md) |
| `competitor-alternatives` | 競合比較ページ・代替製品ページをSEO・営業資料向けに作成するスキル。 「競合比較ページを作って」「代替ツールのページ」「vs ページ」「〇〇 vs △△」「alternative page」等のリクエストで発動。 単数alternative、複数alternatives、自社vs競合、競合同士比較の4フォーマットに対応。 | [`skills/competitor-alternatives/SKILL.md`](../skills/competitor-alternatives/SKILL.md) |
| `content-creator` | マーケティングコンテンツ制作スキル。X/Instagram投稿、Note/Medium記事、 バナー画像、動画スクリプト等を作成する。 「投稿作って」「バナー作成」「記事書いて」「コピー作成」等で発動。 product-context.mdを参照してブランド一貫性を保つ。 | [`skills/content-creator/SKILL.md`](../skills/content-creator/SKILL.md) |
| `content-optimizer` | コンテンツのA/Bテスト・自己改善ループを支援するプランナースキル。 市場トレンド調査 → 仮説生成 → 実験設計 → メトリクス収集 → 分析改善の全サイクルをカバー。 「コンテンツを最適化」「投稿を改善したい」「トレンド分析して投稿案を作って」「エンゲージメント改善」等のリクエストで発動。 | [`skills/content-optimizer/SKILL.md`](../skills/content-optimizer/SKILL.md) |
| `content-strategy` | コンテンツ戦略の立案、トピック選定、記事テーマ決めを行うスキル。 「コンテンツ戦略を立てて」「何を書けばいい？」「ブログのテーマを考えて」等のリクエストで発動。 For writing individual pieces, see copywriting. For SEO-specific audits, see seo-audit. | [`skills/content-strategy/SKILL.md`](../skills/content-strategy/SKILL.md) |
| `copy-editing` | マーケティングコピーの編集・レビュー・改善を行うスキル。 「コピーを編集して」「文章を校正して」「コピーのフィードバック」等のリクエストで発動。 Multiple focused passes による体系的な編集アプローチ。 | [`skills/copy-editing/SKILL.md`](../skills/copy-editing/SKILL.md) |
| `copywriting` | ランディングページ、ホームページ、料金ページ等のマーケティングコピーを作成・改善するスキル。 「コピーを書いて」「LPのコピー作成」「ヘッドライン考えて」等のリクエストで発動。 For email copy, see email-sequence. For popup copy, see popup-cro. | [`skills/copywriting/SKILL.md`](../skills/copywriting/SKILL.md) |
| `create-cowork-plugin` | Cowork セッションでプラグインをゼロから作成するスキル。 「プラグインを作って」「プラグイン開発」「plugin作成」等のリクエストで発動。 Cowork モードで .plugin ファイルを生成。 | [`skills/create-cowork-plugin/SKILL.md`](../skills/create-cowork-plugin/SKILL.md) |
| `csv-analyzer` | CSVファイルの行数・列数の取得、データ型推定、欠損値検出、数値列の統計情報を出力するスキル。 「CSVを分析して」「CSVの中身を確認」「データの概要を見せて」等のリクエストで発動。 | [`skills/csv-analyzer/SKILL.md`](../skills/csv-analyzer/SKILL.md) |
| `data-visualization` | Python (matplotlib, seaborn, plotly) でデータ可視化を行うスキル。 「グラフを作って」「チャート作成」「データを可視化して」等のリクエストで発動。 チャート選定、デザイン原則、アクセシビリティ対応も含む。 | [`skills/data-visualization/SKILL.md`](../skills/data-visualization/SKILL.md) |
| `email-sequence` | メールシーケンス、ステップメール、ドリップキャンペーンの設計・最適化を行うスキル。 「メール設計」「ステップメール作成」「ウェルカムメール」等のリクエストで発動。 For in-app onboarding, see onboarding-cro. | [`skills/email-sequence/SKILL.md`](../skills/email-sequence/SKILL.md) |
| `exploratory-data-analysis` | 200以上のファイル形式に対応した探索的データ分析（EDA）スキル。 「データを分析して」「EDAして」「ファイルの中身を調べて」等のリクエストで発動。 ファイル自動検出、品質評価、統計サマリー、可視化推奨を含むレポート生成。 | [`skills/exploratory-data-analysis/SKILL.md`](../skills/exploratory-data-analysis/SKILL.md) |
| `fact-checker` | 記事内の事実主張（数値、日付、固有名詞、統計）を自動抽出し、Web検索で裏付け確認するスキル。 「ファクトチェックして」「事実確認して」「裏付けを取って」等のリクエストで発動。 信頼度スコア付きレポートを出力。 | [`skills/fact-checker/SKILL.md`](../skills/fact-checker/SKILL.md) |
| `feature-spec` | PRD（プロダクト要件定義書）の作成、機能仕様の策定、受け入れ基準の定義を行うスキル。 「PRDを書いて」「機能仕様を作って」「要件定義して」等のリクエストで発動。 | [`skills/feature-spec/SKILL.md`](../skills/feature-spec/SKILL.md) |
| `free-tool-strategy` | マーケティング目的の無料ツール戦略（リード獲得、SEO、ブランド認知）を立案するスキル。 「無料ツールを作りたい」「リード獲得ツール」「engineering as marketing」等のリクエストで発動。 | [`skills/free-tool-strategy/SKILL.md`](../skills/free-tool-strategy/SKILL.md) |
| `gslides-creator` | テンプレートから Google Slides を作成するスキル。 「Google Slidesを作って」「スライド生成」「プレゼン作成」等のリクエストで発動。 GAS + clasp CLI でテンプレートコピー・コンテンツ書き換え・ゼロからのデッキ生成を行う。 | [`skills/gslides-creator/SKILL.md`](../skills/gslides-creator/SKILL.md) |
| `gslides-parser` | Google Slides の構造を GAS 経由でパースし、YAML マッピングを出力するスキル。 「スライドをパースして」「スライドの構造を解析」「YAMLマッピング作成」等のリクエストで発動。 pptx-converter 互換のセマンティック解析 + プレースホルダー付与。 | [`skills/gslides-parser/SKILL.md`](../skills/gslides-parser/SKILL.md) |
| `interactive-dashboard-builder` | Chart.js を使ったインタラクティブなHTMLダッシュボードを構築するスキル。 「ダッシュボードを作って」「インタラクティブなレポート」「HTMLチャート作成」等のリクエストで発動。 フィルター・グラフ・プロフェッショナルなスタイリング付きのスタンドアロンHTMLを生成。 | [`skills/interactive-dashboard-builder/SKILL.md`](../skills/interactive-dashboard-builder/SKILL.md) |
| `jupyter-to-marimo` | Jupyter ノートブック (.ipynb) を marimo ノートブック (.py) に変換するスキル。 「Jupyterを変換して」「ipynbをmarimoに」「ノートブック変換」等のリクエストで発動。 | [`skills/jupyter-to-marimo/SKILL.md`](../skills/jupyter-to-marimo/SKILL.md) |
| `launch-strategy` | プロダクトローンチ、機能リリース、Go-to-Market 戦略を立案するスキル。 「ローンチ戦略を立てて」「リリース計画」「Product Hunt準備」等のリクエストで発動。 フェーズドローンチ、チャネル戦略、モメンタム構築をカバー。 | [`skills/launch-strategy/SKILL.md`](../skills/launch-strategy/SKILL.md) |
| `lp-designer` | LP/HP作成ワークフロー。ヒアリング→訴求整理→WF→Pencilデザイン→HTML実装→Vercelデプロイの全フローをガイド。 「LPを作って」「ランディングページ作成」「HPデザイン」「Webページ制作」等のリクエストで発動。 | [`skills/lp-designer/SKILL.md`](../skills/lp-designer/SKILL.md) |
| `marimo-notebook` | marimo ノートブックを正しいフォーマットでPythonファイルに作成するスキル。 「marimoノートブック作成」「インタラクティブノートブック」「Pythonノートブック」等のリクエストで発動。 | [`skills/marimo-notebook/SKILL.md`](../skills/marimo-notebook/SKILL.md) |
| `marketing-ideas` | SaaSやソフトウェア製品のマーケティングアイデア・戦略を139のアプローチから提案するスキル。 「マーケティングアイデア」「集客方法を教えて」「成長戦略」等のリクエストで発動。 | [`skills/marketing-ideas/SKILL.md`](../skills/marketing-ideas/SKILL.md) |
| `marketing-planner` | マーケティング計画策定・プロダクトマーケティングコンテキスト作成スキル。 「マーケ計画」「ポジショニング」「ペルソナ作成」「競合分析」「コンテンツ戦略」等で発動。 product-marketing-context.mdを生成し、他のマーケティングスキルの土台を作る。 | [`skills/marketing-planner/SKILL.md`](../skills/marketing-planner/SKILL.md) |
| `marketing-psychology` | 心理学・メンタルモデル・行動科学をマーケティングに応用するスキル。70以上のメンタルモデルを提供。 「購買心理」「認知バイアス」「説得テクニック」「なぜ買うのか」等のリクエストで発動。 | [`skills/marketing-psychology/SKILL.md`](../skills/marketing-psychology/SKILL.md) |
| `matplotlib` | Pythonのmatplotlibでグラフ・チャートを作成するスキル。PNG/PDF/SVG出力対応。 「グラフを作って」「チャートを描いて」「可視化して」「matplotlib」等のリクエストで発動。 | [`skills/matplotlib/SKILL.md`](../skills/matplotlib/SKILL.md) |
| `meeting-notes-summarizer` | 会議テキストやメモから構造化された議事録を自動生成するスキル。 「議事録をまとめて」「会議メモを整理して」「アクション項目を抽出して」等のリクエストで発動。 | [`skills/meeting-notes-summarizer/SKILL.md`](../skills/meeting-notes-summarizer/SKILL.md) |
| `monitoring-dashboard` | marimoダッシュボード・プロジェクト進捗可視化に使用。 「ダッシュボードを作って」「進捗を可視化して」「テスト結果を表示して」等のリクエストで発動。 | [`skills/monitoring-dashboard/SKILL.md`](../skills/monitoring-dashboard/SKILL.md) |
| `motion-review` | Remotionコンポジションを20項目チェックリストで品質レビューする。 「動画レビュー」「motion review」「Remotion品質チェック」等のリクエストで発動。 | [`skills/motion-review/SKILL.md`](../skills/motion-review/SKILL.md) |
| `mv-composer` | Remotion + Kling i2v でプロモーションMV動画・バイラルショート動画を生成するスキル。 「MV作成」「動画を作って」「プロモーション動画」「TikTok動画」等のリクエストで発動。 | [`skills/mv-composer/SKILL.md`](../skills/mv-composer/SKILL.md) |
| `narration-qa` | ElevenLabsで生成したナレーション音声の品質を自動検証するスキル。 「ナレーションチェック」「音声確認」「発音チェック」等のリクエストで発動。 | [`skills/narration-qa/SKILL.md`](../skills/narration-qa/SKILL.md) |
| `paid-ads` | Google Ads・Meta・LinkedIn等の有料広告キャンペーンを設計・最適化するスキル。 「広告を出したい」「広告キャンペーンを作って」「リターゲティング」等のリクエストで発動。 | [`skills/paid-ads/SKILL.md`](../skills/paid-ads/SKILL.md) |
| `planning-with-files` | 複雑なタスクをファイルベースで計画管理するスキル。task_plan.md、findings.md、progress.mdを作成。 「計画を立てて」「タスクを整理して」「プランニング」等のリクエストで発動。 | [`skills/planning-with-files/SKILL.md`](../skills/planning-with-files/SKILL.md) |
| `plotly` | Plotlyでインタラクティブなグラフ・ダッシュボードを作成するスキル。ホバー、ズーム、パン対応。 「インタラクティブグラフ」「plotlyでチャート」「操作できるグラフ」等のリクエストで発動。 | [`skills/plotly/SKILL.md`](../skills/plotly/SKILL.md) |
| `pm-toolkit` | PRD・要件定義書・要求資料・レビューの生成に使用。 「PRDを作って」「要件定義書を書いて」「レビューして」「議事録を分析して」等のリクエストで発動。 | [`skills/pm-toolkit/SKILL.md`](../skills/pm-toolkit/SKILL.md) |
| `post-publisher` | コンテンツの投稿・配信実行スキル。Typefully経由のX投稿、画像アップロード、 投稿スケジューリングを行う。 「投稿して」「スケジュール設定」「Typefullyに下書き」等で発動。 | [`skills/post-publisher/SKILL.md`](../skills/post-publisher/SKILL.md) |
| `pptx-converter` | PPTXテンプレート変換 & ゼロからデッキ生成。テーマ・アニメーション・SmartArtを保持してコンテンツを書き換え。 「PPTX変換」「スライド作成」「パワポ書き換え」「デッキ生成」等のリクエストで発動。 | [`skills/pptx-converter/SKILL.md`](../skills/pptx-converter/SKILL.md) |
| `pptx-creator` | トピックを入力するだけで、テンプレートのデザインを維持した .pptx を自動生成するスキル。 「プレゼンを作って」「スライド生成」「PPTX作成」「提案資料を作成」等のリクエストで発動。 | [`skills/pptx-creator/SKILL.md`](../skills/pptx-creator/SKILL.md) |
| `pricing-strategy` | 料金設計・パッケージング・マネタイズ戦略を支援するスキル。 「料金を決めたい」「プランを設計して」「pricing を見直したい」等のリクエストで発動。 | [`skills/pricing-strategy/SKILL.md`](../skills/pricing-strategy/SKILL.md) |
| `product-marketing-context` | プロダクトマーケティングのコンテキスト文書を作成・更新するスキル。 「マーケティングコンテキストを作成」「ポジショニングを整理」「製品情報をまとめて」等のリクエストで発動。 | [`skills/product-marketing-context/SKILL.md`](../skills/product-marketing-context/SKILL.md) |
| `programmatic-seo` | テンプレートとデータを使ってSEOページを大量生成するスキル。 「SEOページを量産したい」「テンプレートページを作って」「地域別ページを作りたい」等のリクエストで発動。 | [`skills/programmatic-seo/SKILL.md`](../skills/programmatic-seo/SKILL.md) |
| `proofreading-agent` | 日本語記事の校閲エージェント。誤字脱字、文法、表現の一貫性、読みやすさをチェックし、修正提案をインライン注釈で出力する。 「校閲して」「文章をチェック」「誤字脱字を確認」「記事をレビュー」等のリクエストで発動。 | [`skills/proofreading-agent/SKILL.md`](../skills/proofreading-agent/SKILL.md) |
| `referral-program` | 紹介プログラム・アフィリエイト・口コミ戦略を設計・最適化するスキル。 「紹介プログラムを作りたい」「アフィリエイト設計」「口コミ施策を考えて」等のリクエストで発動。 | [`skills/referral-program/SKILL.md`](../skills/referral-program/SKILL.md) |
| `remotion-trace` | 参考動画からプロ品質の Remotion 動画を再現するワークフロースキル。 「参考動画から再現したい」「動画トレース」「PVを作りたい」「Remotion動画を参考動画ベースで作りたい」で発動。 | [`skills/remotion-trace/SKILL.md`](../skills/remotion-trace/SKILL.md) |
| `schema-markup` | 構造化データ・スキーママークアップの追加・修正・最適化を行うスキル。 「構造化データを追加して」「JSON-LDを作って」「リッチスニペットを設定」等のリクエストで発動。 | [`skills/schema-markup/SKILL.md`](../skills/schema-markup/SKILL.md) |
| `scientific-visualization` | 論文投稿用の出版品質グラフ・図表を作成するメタスキル。 「論文用のグラフを作って」「Nature用の図を作成」「出版品質の可視化」等のリクエストで発動。 | [`skills/scientific-visualization/SKILL.md`](../skills/scientific-visualization/SKILL.md) |
| `seo-audit` | サイトのSEO問題を監査・診断し、改善提案を行うスキル。 「SEOを監査して」「検索順位が上がらない原因を調べて」「技術SEOをチェック」等のリクエストで発動。 | [`skills/seo-audit/SKILL.md`](../skills/seo-audit/SKILL.md) |
| `session-retrospective` | セッション終了時に自己改善Issueを自動生成するスキル。 「振り返りIssue出して」「レトロスペクティブ」「改善点をIssueにして」等のリクエストで発動。 | [`skills/session-retrospective/SKILL.md`](../skills/session-retrospective/SKILL.md) |
| `skill-name` | 1行の説明文 | [`skills/_template/SKILL.md`](../skills/_template/SKILL.md) |
| `slack-todo-extractor` | Slackの同期データからメンションを検索しTODO/タスクを抽出・ステータス判定するスキル。 「Slackからタスク抽出」「TODO確認」「メンション確認」等のリクエストで発動。 | [`skills/slack-todo-extractor/SKILL.md`](../skills/slack-todo-extractor/SKILL.md) |
| `slide-forge` | アウトラインやリサーチ結果から、体裁の揃った提案スライド（自己完結HTML・16:9）を組み立てるスキル。「スライドにして」「提案デッキを作って」「スライド化」「slide forge」などのリクエストで使用する。 | [`skills/slide-forge/SKILL.md`](../skills/slide-forge/SKILL.md) |
| `social-content` | SNS投稿の作成・スケジュール・最適化を支援するスキル。 「SNS投稿を作って」「LinkedInの投稿を書いて」「コンテンツカレンダーを作成」等のリクエストで発動。 | [`skills/social-content/SKILL.md`](../skills/social-content/SKILL.md) |
| `sql-queries` | 主要データウェアハウス方言で正確かつ高性能なSQLを記述するスキル。 「SQLを書いて」「クエリを最適化して」「BigQueryで集計」等のリクエストで発動。 | [`skills/sql-queries/SKILL.md`](../skills/sql-queries/SKILL.md) |
| `statistical-analysis` | 統計検定の選択・仮定チェック・検出力分析・APA形式レポートを支援するスキル。 「統計分析をして」「t検定を実行」「適切な検定を選んで」等のリクエストで発動。 | [`skills/statistical-analysis/SKILL.md`](../skills/statistical-analysis/SKILL.md) |
| `style-analyzer` | ユーザーの既存文章を複数読み込み、文体特徴（語尾パターン、文の長さ、漢字/ひらがな比率、口調、接続詞傾向）を抽出してスタイルプロファイルを生成する。 「文体を分析して」「書き方を真似て」「文章のスタイルを学習」等のリクエストで発動。 | [`skills/style-analyzer/SKILL.md`](../skills/style-analyzer/SKILL.md) |
| `tdd-guide` | Test-driven development workflow with test generation, coverage analysis, and multi-framework support | [`skills/tdd-guide/SKILL.md`](../skills/tdd-guide/SKILL.md) |
| `test-planner` | テスト計画書・テストケース・テストレポートの生成に使用。 「テスト計画を作って」「テストケースを生成して」「E2Eテストを書いて」等で発動。 | [`skills/test-planner/SKILL.md`](../skills/test-planner/SKILL.md) |
| `tmux-session-manager` | Lightsail上のClaude Code tmuxセッションをSSH経由で管理。 「セッション確認」「PR同期」「tmuxの状態」等のリクエストで発動。 | [`skills/tmux-session-manager/SKILL.md`](../skills/tmux-session-manager/SKILL.md) |
| `ui-ux-pro-max` | UI/UX デザインガイド。50スタイル・97パレット・57フォント組み合わせ・9スタック対応。 「UI設計して」「デザインシステムを作って」「画面レビュー」等のリクエストで発動。 | [`skills/ui-ux-pro-max/SKILL.md`](../skills/ui-ux-pro-max/SKILL.md) |
| `video-analyzer` | TikTok/YouTube動画を分析してテンプレート化するスキル。 動画ダウンロード→フレーム抽出→STT→構成分析→テンプレートJSON生成。 競合分析、人気動画の構成学習に使用。 「TikTok分析」「YouTube分析」「動画テンプレート化」「競合動画分析」等で発動。 | [`skills/video-analyzer/SKILL.md`](../skills/video-analyzer/SKILL.md) |
| `video-audio` | 動画用音声生成スキル。ElevenLabs TTS APIでscenes.jsonのナレーションから 音声ファイルを生成し、動画と同期可能な形式で出力する。 「ナレーション生成」「TTS」「音声追加」等で発動。 | [`skills/video-audio/SKILL.md`](../skills/video-audio/SKILL.md) |
| `video-editor` | TikTok/YouTube向け動画編集スキル。ffmpegでキャプション焼き込み、 Ken Burnsエフェクト、シーン結合、音声合成を行う。 scenes.jsonから自動的に編集指示を読み取り最終動画を出力する。 Remotionコンポーネントも同梱（ローカル環境用）。 「動画編集」「キャプション追加」「テロップ付き動画」等で発動。 | [`skills/video-editor/SKILL.md`](../skills/video-editor/SKILL.md) |
| `video-playbook` | 動画分析結果からタイプ別Playbookに知見を蓄積・活用するスキル。 video-analyzerの出力template.jsonを入力として使う。 「Playbook更新」「動画タイプ別知見」「Playbook確認」等で発動。 | [`skills/video-playbook/SKILL.md`](../skills/video-playbook/SKILL.md) |
| `video-scriptwriter` | TikTok/YouTube向け動画スクリプト自動生成スキル。 テーマ+フォーマット+尺を指定すると、scenes.json（storyboard/audio/editor互換）を生成。 Playbookの知見を自動参照して最適な構成を適用。 「スクリプト作成」「台本生成」「企画作って」等で発動。 | [`skills/video-scriptwriter/SKILL.md`](../skills/video-scriptwriter/SKILL.md) |
| `video-storyboard` | 動画スクリプトからAI画像生成で絵コンテ（ストーリーボード）を作成するスキル。 「絵コンテを作って」「ストーリーボード生成」「スクリプトから画像を作成」等で発動。 | [`skills/video-storyboard/SKILL.md`](../skills/video-storyboard/SKILL.md) |
| `viral-short-video` | TikTok/YouTube Shorts向けのバイラル動画スクリプト&ストーリーボード生成スキル。 調査済みのバイラルテクニック（3秒フック、モジュラー構造、ループブリッジ、フラッシュテキスト、 スプリットスクリーン等）をスクリプティングとストーリーボード作成に自動組み込み。 「TikTok動画のスクリプト」「バイラル動画を作りたい」「Short動画の台本」等で発動。 | [`skills/viral-short-video/SKILL.md`](../skills/viral-short-video/SKILL.md) |
| `x-research` | X (Twitter) のリアルタイム検索を行い、トピックに関するツイートを収集・分析する。 検索結果を構造化レポート（Markdown + JSON + TXT）として出力。 「Xで検索して」「Twitterで調べて」「ツイートを分析」等で発動。 | [`skills/x-research/SKILL.md`](../skills/x-research/SKILL.md) |
| `youtube-clipper` | YouTube/マルチプラットフォーム動画からAIでハイライトを抽出し、 バイリンガル字幕付きクリップを自動生成するスキル。 「動画からクリップを切り出して」「ハイライトを抽出」「字幕付きクリップ」等で発動。 | [`skills/youtube-clipper/SKILL.md`](../skills/youtube-clipper/SKILL.md) |
| `youtube-uploader` | YouTube Data API v3 を使用した動画アップロードスキル。 Shorts自動検出、UTMリンク自動挿入、予約投稿に対応。 「YouTube投稿」「動画アップロード」「Shorts投稿」等で発動。 | [`skills/youtube-uploader/SKILL.md`](../skills/youtube-uploader/SKILL.md) |
<!-- AUTO-GENERATED:skills END -->

## インストール方法

### 方法 1: SKILL.md を入口に使う

Codex / Claude Code ともに、まず `skills/スキル名/SKILL.md` を読みます。

### 方法 2: 手動インストール

```bash
# スキルディレクトリに移動
cd skills/スキル名

# 依存関係インストール
uv sync

# (オプション) セットアップスクリプト実行
python scripts/install.py
```

### 方法 3: 一括インストール

```bash
# すべてのスキルをインストール
python scripts/setup.py --install skills

# 特定のカテゴリのスキル
python scripts/setup.py --install skills --category data-analysis
```

### 依存関係確認

```bash
# 各スキルの requirements.txt を確認
cat skills/スキル名/requirements.txt

# 一般的な依存関係
# - google-genai (画像生成スキル向け)
# - google-cloud-bigquery (BigQuery スキル向け)
# - python-pptx (PPTX 処理スキル向け)
# - pillow (画像処理)
# - requests (HTTP通信)
```

---

## スキルの実行方法

### 基本的な実行

```bash
# Python スクリプト直接実行
python skills/スキル名/scripts/main.py --param value

# Codex / Claude Code ともに SKILL.md の usage に従う
cat skills/スキル名/SKILL.md
```

### パラメータ指定

```bash
# 基本
python skills/スキル名/scripts/main.py --param1 value1 --param2 value2

# JSON 設定ファイル
python skills/スキル名/scripts/main.py --config config.json

# 環境変数
export SKILL_PARAM="value"
python skills/スキル名/scripts/main.py
```

### 出力確認

```bash
# 標準出力で確認
python skills/スキル名/scripts/main.py > output.log

# JSON 形式で出力
python skills/スキル名/scripts/main.py --output-format json

# ファイルに保存
python skills/スキル名/scripts/main.py --output result.json
```

---

## トラブルシューティング

### インストール関連エラー

#### "uv: command not found"

```bash
# Python 3 を確認
python3 --version

# pip3 を使用
uv add -r requirements.txt

# または poetry
poetry install
```

---

#### "Module not found"

```bash
# 依存関係確認
uv pip list | grep モジュール名

# インストール
uv add モジュール名

# 要件ファイルから一括インストール
uv sync
```

---

### 実行時エラー

#### "API キー未設定"

```bash
# まず .env.local に入力欄を用意
uv run python tools/credential_manager.py prepare-dotenv GEMINI_API_KEY

# 保存後に Credential Store へ移行
uv run python tools/credential_manager.py import-dotenv GEMINI_API_KEY --delete

# 状態確認
uv run python tools/credential_manager.py status
```

> API キーは chat に貼らず、`.env.local` に保存してください。

---

#### "認証エラー"

```bash
# gcloud 認証
gcloud auth application-default login

# Clasp 認証
clasp login

# GitHub 認証
gh auth login
```

---

#### "レート制限エラー"

```bash
# リトライ設定
python skills/スキル名/scripts/main.py \
  --retry-delay 5 \
  --max-retries 3

# キューイング
python skills/スキル名/scripts/main.py \
  --queue \
  --batch-size 10
```

---

### パフォーマンス問題

#### "メモリ不足"

```bash
# バッチサイズを削減
python skills/スキル名/scripts/main.py --batch-size 5

# 不要なプロセス終了
killall python

# メモリ確認
top -l 1 | grep "PhysMem"
```

---

#### "実行が遅い"

```bash
# 並列処理設定
python skills/スキル名/scripts/main.py --workers 4

# キャッシュ活用
python skills/スキル名/scripts/main.py --cache

# デバッグ情報確認
python skills/スキル名/scripts/main.py --debug
```

---

### デバッグ方法

#### 詳細ログ出力

```bash
# ログレベル指定
python skills/スキル名/scripts/main.py --log-level DEBUG

# ファイルに保存
python skills/スキル名/scripts/main.py --log-file debug.log

# 標準出力に出力
python skills/スキル名/scripts/main.py -v -v -v
```

---

#### 実行内容確認

```bash
# Dry-run (実行しない)
python skills/スキル名/scripts/main.py --dry-run

# 実行前に確認
python skills/スキル名/scripts/main.py --confirm

# 実行内容を表示
python skills/スキル名/scripts/main.py --trace
```

---

## FAQ

### Q1: 複数のスキルを組み合わせたい

**A**: パイプまたはスクリプトを使用

```bash
# スキル1の出力をスキル2に渡す
python skills/skill1/scripts/main.py | \
  python skills/skill2/scripts/main.py --input -

# または中間ファイル経由
python skills/skill1/scripts/main.py --output temp.json
python skills/skill2/scripts/main.py --input temp.json
```

---

### Q2: 独自の設定でスキルを実行したい

**A**: 設定ファイルを使用

```bash
# 設定ファイル作成
cat > config.json << EOF
{
  "platform": "x_post",
  "tone": "professional",
  "custom_colors": true
}
EOF

# スキル実行
python skills/banner-creator/scripts/main.py --config config.json
```

---

### Q3: スキルの出力をカスタマイズしたい

**A**: パラメータで制御

```bash
# JSON 形式
python skills/スキル名/scripts/main.py --output-format json

# CSV 形式
python skills/スキル名/scripts/main.py --output-format csv

# Markdown 形式
python skills/スキル名/scripts/main.py --output-format markdown
```

---

### Q4: スキルを定期実行したい

**A**: cron または GitHub Actions

```bash
# cron で定期実行
0 9 * * * python /path/to/skills/skill/scripts/main.py >> /var/log/skill.log

# GitHub Actions ワークフロー
name: Daily Skill Execution
on:
  schedule:
    - cron: '0 9 * * *'
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: python skills/skill/scripts/main.py
```

---

### Q5: スキル開発・カスタマイズしたい

**A**: スキルテンプレートを使用

```bash
# 新規スキル作成
python scripts/create_skill.py --name my-skill --template basic

# スキルのテストコード
python -m pytest skills/my-skill/tests/

# スキルのデプロイ
python scripts/deploy_skill.py --name my-skill
```

---

## 参考リンク

- [Claude Code 公式ドキュメント](https://claude.com/claude-code)
- [Codex Guide](./codex-guide.md)
- [Gemini API ドキュメント](https://ai.google.dev/gemini-api)
- [Google Cloud ドキュメント](https://cloud.google.com/docs)
- [Slack API ドキュメント](https://api.slack.com)
- [コマンドリファレンス](./commands-reference.md)
- [トラブルシューティング](./troubleshoot.md)

---

**ドキュメント更新履歴**

| 日付 | バージョン | 変更内容 |
|------|-----------|---------|
| 2026-03-20 | 1.2.0 | コース使用43スキル全網羅（23スキル追加、6カテゴリ新設） |
| 2026-03-20 | 1.1.0 | 3ツール共通のスキル入口説明に更新 |
| 2026-02-02 | 1.0.0 | 初版作成（20スキル網羅） |

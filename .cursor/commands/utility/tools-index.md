# Tools Index - ツール一覧

このプロジェクトで使用できるツールの一覧と概要です。

## カテゴリ別ツール一覧

### プロジェクト分析
- **project_overview**: プロジェクト構造をPlantUML/Mermaid/WBSで可視化し、モジュール・機能・不足点を要約します。

### スクリーンショット解析・加工
- **screenshot_analyzer**: スクリーンショット解析統合ツール。
  - `analyze`モード: エラー検出・原因特定・NextStep提案
  - `tutorial`モード: 操作手順の解析・ステップ注釈付きチュートリアル生成
- **annotate_screenshot**: スクリーンショットに赤枠・矢印・吹き出しなどの注釈を追加します（元画像は変更せずオーバーレイ）。
- **video_frame_reader**: 動画からキーフレーム抽出 + Gemini解析を行います。

### 広告・バナー生成
- **banner_creator**: 各種SNS・広告プラットフォーム向けのバナー/クリエイティブを生成します。
  - X, Facebook, Instagram, PRタイムズ, YouTube, LINE, Web広告に対応
  - トーン・色味・フォントスタイル・優先度を細かく設定可能
  - 投稿用コピーテキスト（投稿文・ハッシュタグ・CTA）の同時生成
  - 参考画像の指定やWeb検索からの取得に対応

### スライド・図解生成
- **generate_aitutor_slide**: 17種類のリファレンススライドをベースに、AI BRAIN PARTNERS仕様の研修スライド画像を生成します。
- **generate_slide**: トピックから講義用スライド画像を生成します（白背景/青メイン/黄アクセントのシンプルデザイン）。
- **generate_diagram**: トピックやテキストからインフォグラフィック/図解画像を生成します。
- **generate_plantuml_diagram**: PlantUMLファイルからVisio風のモダンなフローチャート画像を生成します。
- **pptx_template**: PPTXからフォーマットを抽出してYAMLテンプレート化し、テキストだけを差し替えた新しいスライドを生成します。

### 学習支援・ガイド
- **guide_action**: SpecStory履歴から現在の状況を分析し、背景説明と次のアクションを提示します。
- **tutor_generate**: SpecStory履歴から学習ギャップを抽出し、初学者向け学習コンテンツ（HTML）を生成します。

### セットアップ・ユーティリティ
- **google_api_setup**: MCP用Google API OAuth認証をセットアップします（Gmail, Calendar, Drive, Sheets対応）。
- **gmail_account_setup**: 複数GmailアカウントのOAuth認証を設定し、GitHub Secretsに自動登録します。
- **google_account_setup**: 複数GoogleアカウントのCalendar/Drive用OAuth認証を設定し、GitHub Secretsに自動登録します。Gmail用と同じクライアントIDを流用可能。
- **bigquery_auth**: GCPプロジェクト単位でBigQuery認証を設定。gcloud設定プロファイルで複数プロジェクトを安全に管理。
- **notebooklm_cli**: NotebookLM Enterprise APIでノートブック作成/取得/最近閲覧一覧を取得します。
- **bootcamp_utils**: 共通ユーティリティ（Gemini APIクライアント取得、HTMLテンプレート生成など）。内部的に使用されます。

## コマンド一覧

| コマンド | 対応ツール | 説明 |
|----------|------------|------|
| `/overview` | project_overview | プロジェクト構造を可視化 |
| `/screenshot-analyzer` | screenshot_analyzer | スクリーンショット解析（エラー/チュートリアル） |
| `/annotate-screenshot` | annotate_screenshot | 画像への注釈追加 |
| `/video-frame-reader` | video_frame_reader | 動画キーフレーム抽出 + Gemini解析 |
| `/create-banner` | banner_creator | 広告バナー/クリエイティブ生成 |
| `/generate-aitutor-slide` | generate_aitutor_slide | 研修スライド生成 |
| `/generate-slide` | generate_slide | 汎用スライド生成 |
| `/generate-diagram` | generate_diagram | 図解生成 |
| `/generate-plantuml-diagram` | generate_plantuml_diagram | PlantUML図生成 |
| `/pptx-template` | pptx_template | PPTXテンプレート抽出・生成 |
| `/guide` | guide_action | 次のアクション提示 |
| `/tutor` | tutor_generate | 学習コンテンツ生成 |
| `/setup-google-api` | google_api_setup | Google API認証設定 |
| `/gmail-account-setup` | gmail_account_setup | Gmail OAuth認証・Secrets登録 |
| `/google-account-setup` | google_account_setup | Calendar/Drive OAuth認証・Secrets登録 |
| `/bigquery-auth` | bigquery_auth | BigQuery認証（プロジェクト単位） |
| `/notebooklm` | notebooklm_cli | NotebookLMノートブック作成/取得/一覧 |
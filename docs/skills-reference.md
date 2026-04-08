# スキルリファレンス完全ガイド

**対応スキル数**: 46個（コース使用: 43個 + 参考収録: 3個）

最終更新: 2026年3月20日

---

## 目次

1. [クイックスタート](#クイックスタート)
2. [画像生成・編集系スキル (4個)](#画像生成編集系スキル-4個)
3. [データ分析・処理系スキル (8個)](#データ分析処理系スキル-8個)
4. [ドキュメント処理系スキル (3個)](#ドキュメント処理系スキル-3個)
5. [動画・メディア系スキル (4個)](#動画メディア系スキル-4個)
6. [API・認証系スキル (2個)](#api認証系スキル-2個)
7. [Slack・通信系スキル (3個)](#slack通信系スキル-3個)
8. [コンテンツ制作・ライティング系スキル (7個)](#コンテンツ制作ライティング系スキル-7個)
9. [SEO・マーケティング系スキル (4個)](#seoマーケティング系スキル-4個)
10. [プロジェクト管理系スキル (4個)](#プロジェクト管理系スキル-4個)
11. [SNSリサーチ系スキル (1個)](#snsリサーチ系スキル-1個)
12. [教材・セットアップ系スキル (5個)](#教材セットアップ系スキル-5個)
13. [その他のスキル (1個)](#その他のスキル-1個)
14. [インストール方法](#インストール方法)
15. [トラブルシューティング](#トラブルシューティング)

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

## 画像生成・編集系スキル (4個)

### 1. `banner-creator` - 広告バナー/クリエイティブ生成

**目的**: 各種SNS・広告プラットフォーム向けのバナー/クリエイティブを自動生成

**説明**: 
Generate advertising banners and creatives for various platforms (X, Facebook, Instagram, PRTimes, YouTube, LINE, Web ads). Supports platform-specific presets, reference image search, and copy text generation.

**インストール**:
```bash
python skills/banner-creator/scripts/install.py
```

**必要な依存関係**:
- Python 3.10+
- google-genai
- Pillow
- python-dotenv
- requests

**必須 API キー**:
- GEMINI_API_KEY または GOOGLE_API_KEY

**機能一覧**:
1. **プラットフォーム別プリセット**: X, Facebook, Instagram, PRタイムズ, YouTube, LINE, Web広告
2. **トーン・スタイル設定**: プロフェッショナル、ポップ、エレガントなど
3. **参考画像検索**: キーワードからWeb検索で参考画像を取得
4. **コピーテキスト生成**: 投稿文・ハッシュタグ・CTAを同時生成
5. **バリエーション生成**: 複数パターン一括生成

**プラットフォーム別サイズ**:

| Platform | Size | Aspect Ratio | 用途 |
|----------|------|--------------|------|
| x_post | 1200x675 | 16:9 | X タイムライン投稿 |
| x_card | 800x418 | 1.91:1 | X カード表示 |
| facebook | 1200x630 | 1.91:1 | Facebook リンク投稿 |
| facebook_story | 1080x1920 | 9:16 | Facebook ストーリーズ |
| instagram_feed | 1080x1080 | 1:1 | Instagram フィード投稿 |
| instagram_story | 1080x1920 | 9:16 | Instagram ストーリーズ |
| prtimes | 1200x630 | 1.91:1 | PRタイムズ |
| youtube | 1280x720 | 16:9 | YouTube サムネイル |
| line | 1040x1040 | 1:1 | LINE リッチメッセージ |
| web_horizontal | 1200x628 | 1.91:1 | Web広告（横） |
| web_vertical | 300x600 | 1:2 | Web広告（縦） |

**パラメータ一覧**:

```
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --platform | Yes | - | ターゲットプラットフォーム |
| --message | Yes | - | メインメッセージ/キャッチコピー |
| --sub-copy | No | - | サブコピー（詳細情報） |
| --cta | No | - | Call to Action テキスト |
| --tone | No | professional | トーン: professional, casual, pop, elegant, urgent, minimal, tech, natural |
| --color-scheme | No | auto | 色味: warm, cool, mono, pastel, vivid, dark, auto, または HEXコード（例: #FF5733） |
| --font-style | No | auto | フォント: gothic, mincho, handwritten, bold, script, geometric, auto |
| --priority | No | ctr | 優先順位: ctr, brand, info, emotion, product, event |
| --brand-name | No | - | ブランド/企業名 |
| --reference | No | - | 参考画像ローカルパスまたはURL |
| --search-ref | No | - | 参考画像検索キーワード |
| --session | No | - | セッション名（出力フォルダ整理用） |
| --with-copy | No | false | 投稿用コピーテキストも生成するか |
| --variants | No | 1 | 生成バリエーション数 |
| --output | No | auto | 出力ファイルパス |
```

**使用例**:

```bash
# 基本的な使用
python skills/banner-creator/scripts/main.py \
  --platform x_post \
  --message "AI時代の働き方改革"

# コピーテキスト付き
python skills/banner-creator/scripts/main.py \
  --platform instagram_feed \
  --message "新商品発売" \
  --sub-copy "限定先行販売中" \
  --tone pop \
  --color-scheme vivid \
  --with-copy

# 参考画像検索付き
python skills/banner-creator/scripts/main.py \
  --platform facebook \
  --message "セール開催" \
  --search-ref "EC セール バナー" \
  --tone urgent

# 複数バリエーション生成
python skills/banner-creator/scripts/main.py \
  --platform youtube \
  --message "チュートリアル動画" \
  --variants 3 \
  --tone professional \
  --session "tutorial_series"

# ブランドカラー指定
python skills/banner-creator/scripts/main.py \
  --platform prtimes \
  --message "新サービスリリース" \
  --brand-name "〇〇株式会社" \
  --color-scheme "#1E40AF" \
  --font-style bold \
  --priority info
```

**出力形式**:
- 画像ファイル: `docs/generated/banners/{日付}_{セッション}/{filename}.png`
- コピーテキスト（--with-copy時）: `{セッション}_copy.md`
  - 投稿文案 × 3パターン
  - ハッシュタグ提案
  - CTAフレーズ例

**トラブルシューティング**:
- API キー未設定: `.env.local` に保存してから Credential Store に移行
- メモリ不足: `--variants` を削減
- 画像品質が低い: `--priority ctr` を使用

---

### 2. `nanobanana` - AI画像生成・編集

**目的**: テキストプロンプトから画像を生成・編集

**説明**: 
Generate images from text prompts or edit existing images using Gemini Image Generation API. Supports realistic photos, anime, illustrations, and various editing effects.

**インストール**:
```bash
python skills/nanobanana/scripts/install.py
```

**必須 API キー**:
- GEMINI_API_KEY または GOOGLE_API_KEY

**機能**:
1. テキストから画像生成
2. 既存画像の編集・加工
3. スタイル変換
4. 高品質出力

**パラメータ**:
```
--prompt         生成・編集内容（必須）
--input          編集対象の画像ファイル（オプション）
--style          リアル, アニメ, イラスト, アート, 写真, スケッチ
--size           256x256, 512x512, 1024x1024, 1024x768, 768x1024
--quality        draft, normal, high
--session        セッション名
--output         出力ファイルパス
```

**使用例**:
```bash
# テキストから画像生成
python skills/nanobanana/scripts/main.py \
  --prompt "青い空を背景にした商品写真" \
  --style realistic \
  --size 1024x768

# 既存画像を編集
python skills/nanobanana/scripts/main.py \
  --input photo.jpg \
  --prompt "明度を上げて、暖色系に変更" \
  --style photo

# アニメスタイルで生成
python skills/nanobanana/scripts/main.py \
  --prompt "未来的なシティスケープ、ネオンライト" \
  --style anime \
  --size 1024x1024 \
  --quality high
```

---

### 3. `diagram-generator` - 図表・インフォグラフィック生成

**目的**: テキストトピックから図表・インフォグラフィックを自動生成

**説明**: 
Generate infographics, diagrams, and visualizations from text topics using Gemini Image Generation API. Creates professional diagrams in PlantUML format.

**対応図表種類**:
- インフォグラフィック
- フロー図
- 比較図
- 階層図
- タイムライン
- ネットワーク図

**使用例**:
```bash
python skills/diagram-generator/scripts/main.py \
  --topic "ユーザー登録フロー" \
  --type flow \
  --style professional

python skills/diagram-generator/scripts/main.py \
  --topic "売上成長推移" \
  --type timeline \
  --style colorful \
  --size large
```

---

### 4. `screenshot-annotator` - スクショに注釈追加

**目的**: スクリーンショットに手書き風の注釈を追加

**説明**: 
Add manual-style annotations (red boxes, arrows, callouts, highlights) to screenshots for technical documentation and tutorials.

**機能**:
- 赤枠追加
- 矢印・吹き出し
- テキスト注釈
- ハイライト

---

## データ分析・処理系スキル (8個)

### 5. `data-analyst` - BigQuery・EDA・可視化

**目的**: データ分析・探索的データ分析（EDA）・可視化

**説明**: 
Perform exploratory data analysis, generate visualizations, and create interactive analysis reports.

**機能**:
1. BigQuery データの読み込み
2. 自動EDA（記述統計、分布分析）
3. グラフ・チャート生成
4. 異常検知
5. 予測分析

---

### 6. `bigquery-auth` - BigQuery認証設定

**目的**: GCPプロジェクト単位でBigQuery認証を設定

**説明**: 
GCPプロジェクト単位でBigQuery認証を設定。gcloud設定プロファイルで複数プロジェクトを安全に分離管理。

**パラメータ**:
```
--project        GCPプロジェクトID（必須）
--account        Google アカウント（オプション）
--override       既存設定を上書きするか
```

---

### 7. `gcp-auth` - Google Cloud Platform認証

**目的**: GCP Application Default Credentials 認証

**説明**: 
Google Cloud Platform (GCP) の Application Default Credentials 認証を実行。BigQuery や Cloud Storage 等の GCP サービス利用を有効化。

**必須**:
- gcloud CLI インストール

---

### 8. `pptx-analyzer` - PowerPointファイル解析

**目的**: PPTX ファイルの構造解析

**説明**: 
PowerPointファイル（.pptx）の構造を解析し、スライド・図形・プレースホルダー・テキスト情報をJSON/テキスト形式で出力。

**機能**:
- スライド構造の抽出
- テンプレート分析
- テキスト内容の抽出
- プレースホルダー検出

---

### `csv-analyzer` - CSV ファイル分析

**目的**: CSV ファイルの統計情報・データ型推定・欠損値検出

**説明**:
CSVファイルを分析し、行数・列数の取得、データ型推定、数値列の基本統計量算出、欠損値検出、エンコーディング判定を行うスキル。

**機能**:
- 行数・列数の取得
- データ型推定（各列のデータ型を自動判定）
- 統計情報（数値列の基本統計量）
- 欠損値検出（NULLやNA値の検出）
- エンコーディング判定

---

### `matplotlib` - データ可視化（静的グラフ）

**目的**: 静的・アニメーション・インタラクティブな高品質グラフを作成

**説明**:
Low-level plotting library for full customization. Use when you need fine-grained control over every plot element, creating novel plot types, or integrating with specific scientific workflows. Export to PNG/PDF/SVG for publication.

**機能**:
- 折れ線・散布図・棒グラフ・ヒストグラム・ヒートマップなど多数の図表タイプ
- pyplot インターフェースとオブジェクト指向 API の両方をサポート
- 出版品質のグラフ出力（PNG/PDF/SVG）

---

### `plotly` - インタラクティブ可視化

**目的**: ホバー・ズーム・パン対応のインタラクティブなチャートを作成

**説明**:
Interactive visualization library. Use when you need hover info, zoom, pan, or web-embeddable charts. Best for dashboards, exploratory analysis, and presentations.

**機能**:
- 40 種類以上のチャートタイプ
- ホバー情報・ズーム・パン操作
- Web 埋め込み対応のインタラクティブグラフ
- ダッシュボード・プレゼンテーション向け

---

### `monitoring-dashboard` - プロジェクトモニタリングダッシュボード

**目的**: marimo Run Mode でプロジェクト進捗・テスト結果を可視化

**説明**:
marimo Run Mode を使って、プロジェクト進捗・テスト結果・要件トレーサビリティを可視化するダッシュボードを生成。

**機能**:
- プロジェクト進捗ダッシュボード
- テスト結果ダッシュボード
- 統合ダッシュボード
- JSON/CSV データソース対応

---

## ドキュメント処理系スキル (3個)

### 9. `document-processor` - PDF・PPTX・Excel処理

**目的**: ドキュメント処理の統合ツール

**説明**: 
Process and manipulate various document formats including PDF, PPTX, and Excel files.

**対応形式**:
- PDF: 結合、分割、ページ削除、テキスト抽出
- PPTX: スライド操作、テンプレート適用
- Excel: 読み込み、編集、出力

---

### 10. `pdf-compressor` - PDF 圧縮

**目的**: 大容量 PDF ファイル圧縮

**説明**: 
Compress large PDF files by resizing pages and optimizing images. Use when PDF file size is too large for email or web sharing.

**機能**:
- ページサイズ最適化
- 画像解像度調整
- テキスト圧縮

---

### 11. `tutorial-generator` - チュートリアル生成

**目的**: スクリーンショットから操作チュートリアル自動生成

**説明**: 
Generate step-by-step operation tutorials from screenshots using Gemini Vision API. Analyzes UI elements and creates detailed instructions.

---

## 動画・メディア系スキル (4個)

### 12. `video-frame-reader` - 動画フレーム抽出

**目的**: 動画からキーフレーム抽出・分析

**説明**: 
Extract and analyze key frames from video files for creating storyboards and tutorials.

---

### 13. `storyboard-generator` - 絵コンテ生成

**目的**: AI UGC用の絵コンテ生成・動画制作

**説明**: 
AI UGC用の16コマ絵コンテを生成し、キャラクター一貫性を保ちながらKlingで動画生成まで対応。

**機能**:
1. 16コマ絵コンテ自動生成
2. キャラクター一貫性維持
3. Kling動画生成との連携

---

### 14. `media-generator` - メディア生成

**目的**: 各種メディア（画像、動画、音声）生成

**説明**:
Generate various media formats including images, videos, and audio content.

---

### `youtube-clipper` - 動画ハイライト抽出・クリップ生成

**目的**: YouTube/マルチプラットフォーム動画からハイライトを抽出しクリップを自動生成

**説明**:
YouTube/マルチプラットフォーム動画からAIでハイライトを抽出し、バイリンガル字幕付きクリップを自動生成。動画の文字起こし、マーケティング素材の作成にも対応。

**機能**:
- 動画ハイライト自動抽出
- バイリンガル字幕生成
- マーケティング素材への変換
- 文字起こし（字幕なし動画にも対応）

---

### `narration-qa` - ナレーション品質検証

**目的**: ElevenLabsで生成したナレーション音声の品質を自動検証

**説明**:
ElevenLabs TTS で生成したナレーション音声を Whisper STT + Gemini で書き起こし、期待テキストと比較して発音精度を自動検証する。英語IT用語の日本語化ルール、漢字ひらがな化ルール等のベストプラクティスを集積。

**機能**:
- TTS入力テキストの事前ルール適用（英語→カタカナ、漢字誤読対策）
- Whisper STT による書き起こし検証
- 不一致クリップの自動再生成
- atempo調整（ナレーション尺 > シーン尺の場合）

---

### `youtube-uploader` - YouTube動画アップロード

**目的**: YouTube Data API v3 を使用した動画アップロード

**説明**:
YouTube動画のアップロード、Shorts自動検出、UTMリンク自動挿入、予約投稿に対応。dry-runモードで安全に検証可能。

**機能**:
- 動画アップロード（通常・Shorts）
- 予約投稿
- UTMリンク自動挿入
- タグ・カテゴリ設定

---

## API・認証系スキル (2個)

### 15. `gas-clasp-ops` - GAS・Clasp操作

**目的**: Google Apps Script・Clasp プロジェクト管理

**説明**: 
Manage and deploy Google Apps Script projects using Clasp CLI.

**機能**:
- プロジェクト作成・削除
- スクリプトデプロイ
- バージョン管理

---

### 16. `slack-search` - Slack検索

**目的**: Slack メッセージ・ファイル検索

**説明**: 
Search Slack messages, files, and threads with advanced filtering options.

**必要な API キー**:
- SLACK_BOT_TOKEN
- SLACK_CHANNEL_IDS

---

## Slack・通信系スキル (3個)

### 17. `check-inbox` - メール・Slack TODO抽出

**目的**: メール・Slack から TODO 自動抽出

**説明**: 
Extract actionable TODOs from email and Slack messages automatically.

**機能**:
- メール内 TODO 検出
- Slack スレッド分析
- 優先度判定
- 自動タスク化

---

### 18. `slack-task-manager` - Slack タスク管理

**目的**: Slack タスク統合管理

**説明**: 
Manage tasks and projects directly from Slack with automated workflows.

---

### 19. `slack-unanswered` - 未答スレッド検出

**目的**: 未回答 Slack メッセージ検出

**説明**: 
Find unanswered Slack messages where you are mentioned or threads you created.

---

## コンテンツ制作・ライティング系スキル (7個)

### `article-writer` - AI 記事執筆エンジン

**目的**: テーマからアウトライン生成、文体プロファイル適用、Markdown 記事出力

**説明**:
テーマを入力するだけで、構造化されたMarkdown記事を自動生成。文体プロファイルによるトーン統一、挿絵マーカーの自動挿入に対応し、一貫性のある高品質な記事を出力。

**機能**:
1. テーマ分析とアウトライン生成
2. スタイルプロファイル読み込み（YAML）
3. セクションごとのドラフト執筆
4. 挿絵マーカーの自動挿入
5. 全体の一貫性チェック

---

### `copywriting` - マーケティングコピー作成

**目的**: LP・HP・広告など各種ページ向けのコンバージョンコピーを作成

**説明**:
When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature pages, about pages, or product pages.

**機能**:
- ページ種別に応じたコピーライティング
- CTA コピー最適化
- ヘッドライン・サブコピー生成

---

### `style-analyzer` - 文体分析・プロファイル生成

**目的**: ユーザーの既存文章から文体特徴を抽出しスタイルプロファイルを生成

**説明**:
ユーザーが書いた複数の文章ファイルを読み込み、文体の特徴を定量的に抽出してスタイルプロファイル（YAML形式）を生成。文体再現や一貫性チェックに活用。

**機能**:
- 語尾パターン分析（です/ます調、だ/である調）
- 文長・文字種比率・接続詞分析
- 体言止め検出・句読点パターン判定
- 口語/文語バランス推定

---

### `proofreading-agent` - 日本語記事校閲エージェント

**目的**: 日本語記事の誤字脱字・文法・表現一貫性・読みやすさをチェック

**説明**:
日本語記事を体系的に校閲するエージェント。Five Sweeps（正確性・一貫性・構造・読みやすさ・スタイル）で記事を多角的にレビューし、修正提案をインライン注釈で出力。

**機能**:
1. 正確性チェック（誤字脱字、送り仮名、同音異義語）
2. 一貫性チェック（用語統一、文体統一）
3. 構造チェック（見出し階層、段落構成）
4. 読みやすさチェック（文長、難読語）
5. スタイルチェック（トーン、ブランドガイドライン準拠）

---

### `fact-checker` - ファクトチェックエージェント

**目的**: 記事内の事実主張を自動抽出し Web 検索で裏付け確認

**説明**:
記事やドキュメント内の事実主張（数値、日付、固有名詞、統計）を自動的に抽出し、Web検索を使って裏付け確認。信頼度スコア付きの Markdown レポートを出力。

**必須 API キー**:
- GEMINI_API_KEY または GOOGLE_API_KEY

---

### `social-content` - ソーシャルメディアコンテンツ作成

**目的**: SNS 各プラットフォーム向けのコンテンツ作成・最適化

**説明**:
LinkedIn, Twitter/X, Instagram, TikTok, Facebook 等のプラットフォーム向けコンテンツ作成を支援。コンテンツカレンダー、エンゲージメント最適化にも対応。

**機能**:
- プラットフォーム別投稿作成
- コンテンツカレンダー設計
- エンゲージメント最適化
- コンテンツリパーパス

---

### `email-sequence` - メールシーケンス設計

**目的**: ドリップキャンペーン・ライフサイクルメール・自動化フローの設計

**説明**:
When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. ウェルカム・ナーチャリング・リエンゲージメント等のシーケンス設計に対応。

**機能**:
- Welcome/オンボーディングシーケンス
- リードナーチャリングシーケンス
- リエンゲージメントメール
- メール自動化フロー設計

---

## SEO・マーケティング系スキル (4個)

### `seo-audit` - SEO 監査・診断

**目的**: サイトの SEO 問題を診断し改善提案を行う

**説明**:
When the user wants to audit, review, or diagnose SEO issues on their site. テクニカル SEO、オンページ SEO、メタタグレビュー等の SEO ヘルスチェックに対応。

**機能**:
- テクニカル SEO 監査
- オンページ SEO 分析
- メタタグ・構造化データレビュー
- アクション可能な改善提案

---

### `programmatic-seo` - プログラマティック SEO

**目的**: テンプレートとデータを使って SEO ページを大量生成

**説明**:
When the user wants to create SEO-driven pages at scale using templates and data. ディレクトリページ、地域別ページ、比較ページ等のテンプレート生成に対応。

**機能**:
- テンプレートベースの大量ページ生成
- 薄いコンテンツペナルティ回避の品質担保
- キーワード＋地域の組み合わせページ

---

### `ab-test-setup` - A/B テスト設計

**目的**: A/B テスト・スプリットテスト・実験の設計と計画

**説明**:
When the user wants to plan, design, or implement an A/B test or experiment. 統計的に有効でアクション可能なテスト設計を支援。

**機能**:
- テスト仮説の構造化
- サンプルサイズ計算
- バリエーション設計
- 結果分析フレームワーク

---

### `lp-designer` - LP/HP 制作ワークフロー

**目的**: ランディングページ/ホームページをゼロから制作

**説明**:
ヒアリング → 訴求整理 → ワイヤーフレーム → Pencil デザイン → HTML 実装 → Vercel デプロイの全フローをガイド。6つのフェーズで LP/HP 制作を完結。

**機能**:
1. ヒアリングによる訴求整理
2. ワイヤーフレーム作成
3. Pencil MCP デザイン
4. HTML + Tailwind CSS 実装
5. Vercel デプロイ

---

## プロジェクト管理系スキル (4個)

### `pm-toolkit` - プロダクトマネジメントツールキット

**目的**: PRD・要件定義書・要求資料・レビューの生成

**説明**:
プロダクト開発の企画・要件定義フェーズで使うテンプレートとプロンプトを提供。Working Backwards 方式の PRD、IPA 準拠の要件定義書、Devil's Advocate レビュー等に対応。

**機能**:
- PRD テンプレート（Working Backwards 方式）
- 要件定義書生成
- レビュー（Devil's Advocate / セキュリティ / 技術）
- 議事録分析

---

### `test-planner` - テスト計画・実行支援

**目的**: テスト計画書・テストケース・テストコードの自動生成

**説明**:
ユースケースからテスト計画書、テストケース、テストコードを自動生成。正常系/異常系/境界値/セキュリティの観点を網羅。

**機能**:
- テスト計画書生成
- テストケース生成（正常系/異常系/境界値）
- Playwright E2E テストコード生成

---

### `meeting-notes-summarizer` - 議事録自動生成

**目的**: 会議テキストやメモから構造化された議事録を自動生成

**説明**:
会議メモ、文字起こし、チャットログを読み取り、構造化されたMarkdown議事録へ整形。参加者、議題、決定事項、アクション項目、次回予定を整理。

**機能**:
- 会議メモの構造化
- 決定事項・アクション項目の抽出
- 優先度・期限の整理
- Markdown 議事録出力

---

### `course-editor` - HTML 教材エディター

**目的**: HTML 教材（course/）の編集・新規作成を効率化

**説明**:
テンプレート構造、CSSフレームワーク、セクション単位編集の手順を提供し、並列エージェントによるリライト時のコンテキスト消費を最小化するガイドラインスキル。

**機能**:
- テンプレート構造に沿った教材作成
- セクション単位の効率的な編集
- CSS フレームワーク準拠

---

## SNSリサーチ系スキル (1個)

### `x-research` - X (Twitter) リアルタイム検索・分析

**目的**: X (Twitter) のリアルタイム検索を行いトピックに関するツイートを収集・分析

**説明**:
X (Twitter) のリアルタイム検索を行い、トピックに関するツイートを収集・分析。検索結果を構造化レポート（Markdown + JSON + TXT）として出力。

**必要な API キー**:
- X_BEARER_TOKEN

**機能**:
- キーワード検索・トレンド調査
- ツイート分析・構造化レポート出力
- 複数出力形式（Markdown/JSON/TXT）

---

## 教材・セットアップ系スキル (5個)

### `aiagent-guide` - リポジトリオリエンテーション

**目的**: ai-agent-camp リポジトリの全体像を案内し次のステップを推薦

**説明**:
Codex / Claude Code 内で ai-agent-camp のリポジトリ概要、ツール間の違い、推奨レッスンとワークフローを案内。

---

### `aiagent-lesson-runner` - レッスン実行ランナー

**目的**: Codex で `start-*` レッスンを実行するワークフローを再現

**説明**:
レッスン ID（例: start-0-1）を入力として受け取り、対応するレッスンファイルを読み込んで目標・前提条件・チェックポイントを抽出し、学習を進行。

---

### `aiagent-check-setup` - 環境セットアップ確認

**目的**: ai-agent-camp のローカル環境が正しくセットアップされているか確認

**説明**:
Git、Node.js、npm、Python3 のバージョン確認、環境変数・Credential Store のセットアップ状況、Git フックのインストール状態をチェック。

---

### `aiagent-tooling-setup` - ツーリング設定

**目的**: Codex 向けのツーリング（MCP サーバー、リポフック等）を設定

**説明**:
MCP サーバーの有効化、リポフックのインストール、ツール固有のセットアップ手順を案内。既存のリポスクリプトを優先的に活用。

---

### `_template` - スキルテンプレート

**目的**: 新規スキル作成時のテンプレート

**説明**:
新しいスキルを作成する際の SKILL.md テンプレート。メタデータ（名前、説明、バージョン）、分類（ロール、難易度、タグ）、実行情報の定義フォーマットを提供。

---

## その他のスキル (1個)

### 20. `screenshot-analyzer` - スクリーンショット解析

**目的**: エラー診断・マニュアル生成

**説明**: 
Analyze screenshots for error diagnosis and tutorial generation using Gemini Vision API. Detects errors and UI elements automatically.

**機能**:
- エラー画面診断
- UI コンポーネント認識
- テキスト抽出（OCR）
- チュートリアル生成

---

## インストール方法

### 方法 1: SKILL.md を入口に使う

Codex / Claude Code ともに、まず `skills/スキル名/SKILL.md` を読みます。

### 方法 2: 手動インストール

```bash
# スキルディレクトリに移動
cd skills/スキル名

# 依存関係インストール
pip install -r requirements.txt

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

#### "pip: command not found"

```bash
# Python 3 を確認
python3 --version

# pip3 を使用
pip3 install -r requirements.txt

# または poetry
poetry install
```

---

#### "Module not found"

```bash
# 依存関係確認
pip list | grep モジュール名

# インストール
pip install モジュール名

# 要件ファイルから一括インストール
pip install -r skills/スキル名/requirements.txt
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

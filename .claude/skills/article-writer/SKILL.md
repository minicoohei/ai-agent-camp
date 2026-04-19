---
name: article-writer
description: "テーマからアウトライン生成→文体プロファイル適用→Markdown記事出力を行う記事執筆スキル。 挿絵マーカーの自動挿入、style-analyzerプロファイル参照による文体統一に対応。 「記事を書いて」「ブログ作成」「テーマで記事生成」等のリクエストで発動。"
triggers:
  - article-writer
  - 記事を書いて
  - ブログ作成
  - テーマで記事生成
  - 記事執筆
  - アウトライン作成
  - Markdown記事
---

# Article Writer - AI記事執筆エンジン

テーマを入力するだけで、構造化されたMarkdown記事を自動生成します。文体プロファイルによるトーン統一、挿絵マーカーの自動挿入に対応し、一貫性のある高品質な記事を出力します。

## ワークフロー

```
テーマ入力 → アウトライン生成 → スタイル適用 → セクション執筆 → 挿絵マーカー挿入 → 一貫性チェック → Markdown出力
```

1. **テーマ分析とアウトライン生成**: テーマからセクション構成・見出し・キーポイントを自動設計
2. **スタイルプロファイル読み込み**: YAMLファイルで文体（トーン、語尾、語彙レベル等）を指定可能
3. **セクションごとのドラフト執筆**: アウトラインに沿ってGemini APIで各セクションを生成
4. **挿絵マーカーの自動挿入**: 図表・画像の挿入位置をHTMLコメントとして自動配置
5. **全体の一貫性チェック**: 文体・用語の統一性を確認し最終Markdownを出力

## Usage

```bash
# Basic article generation
python scripts/article_writer.py --theme "AIエージェントの活用法" --output output/article.md

# With style profile
python scripts/article_writer.py --theme "AIエージェントの活用法" --style style_profile.yaml --output output/article.md

# With target audience
python scripts/article_writer.py --theme "AIエージェントの活用法" --audience "非エンジニアのビジネスパーソン" --style style_profile.yaml

# Specify word count and section count
python scripts/article_writer.py --theme "データ分析入門" --word-count 5000 --sections 7

# Disable illustration markers
python scripts/article_writer.py --theme "プロジェクト管理" --illustrations none

# Test mode (no API call)
python scripts/article_writer.py --test
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --theme | Yes | - | 記事のテーマ・トピック |
| --style | No | - | 文体プロファイルYAMLファイルのパス |
| --audience | No | - | 想定読者（例: "非エンジニアのビジネスパーソン"） |
| --output | No | auto | 出力ファイルパス（デフォルト: output/article_{timestamp}.md） |
| --word-count | No | 3000 | 目標文字数 |
| --sections | No | auto | セクション数（autoの場合テーマから自動決定） |
| --illustrations | No | auto | 挿絵マーカー: auto（自動挿入）/ manual（位置のみ）/ none（なし） |
| --test | No | false | テストモード（API呼び出しなしでサンプル記事を生成） |

## 挿絵マーカー形式

記事中に以下のHTMLコメント形式で挿絵の挿入位置を示します。後続のスキル（nanobanana, diagram-generator等）で実際の画像を生成できます。

```html
<!-- illustration: type=diagram description="フロー図: AIエージェントの処理手順" -->

<!-- illustration: type=image description="モダンなオフィスでAIを使う人" -->
```

| type | 説明 | 推奨スキル |
|------|------|-----------|
| diagram | フローチャート、構成図、UML図 | diagram-generator |
| image | 写真風、イラスト、概念図 | nanobanana |
| chart | グラフ、データ可視化 | data-analyst |
| screenshot | UI画面キャプチャ | screenshot-annotator |

## スタイルプロファイル形式

YAMLファイルで文体を指定します（style-analyzerスキルで自動生成可能）。

```yaml
tone: professional        # professional / casual / academic / friendly
formality: high            # high / medium / low
sentence_ending: です・ます  # です・ます / だ・である / 混合
vocabulary_level: general   # general / technical / simple
paragraph_length: medium    # short / medium / long
use_examples: true
use_metaphors: false
target_audience: "ビジネスパーソン"
brand_voice: "信頼感があり、分かりやすい"
avoid_words:
  - "要するに"
  - "ぶっちゃけ"
preferred_expressions:
  - "具体的には"
  - "例えば"
```

## 出力形式

Markdown形式の記事ファイル。以下の構成で出力されます。

```markdown
# 記事タイトル

> リード文（記事の要約・導入）

## 目次

- [セクション1](#セクション1)
- [セクション2](#セクション2)
- ...

## セクション1

本文テキスト...

<!-- illustration: type=diagram description="..." -->

## セクション2

本文テキスト...

<!-- illustration: type=image description="..." -->

## まとめ

結論テキスト...
```

## 並列実行

複数テーマの記事を同時に生成する場合、エージェントを複数起動して並列処理できます。

```bash
# 複数テーマを並列実行
python scripts/article_writer.py --theme "AI活用法" --output output/ai.md &
python scripts/article_writer.py --theme "DX推進" --output output/dx.md &
wait
```

## Requirements

- **API Key**: GEMINI_API_KEY または GOOGLE_API_KEY を環境変数に設定
- **Python packages**: google-genai, pyyaml, python-dotenv

## Related Skills

| スキル | 連携内容 |
|--------|---------|
| **style-analyzer** | 参考文章から文体プロファイルを自動生成 → --style に渡す |
| **proofreading-agent** | 生成記事の校正・推敲 |
| **fact-checker** | 記事内の事実関係を検証 |
| **nanobanana** | 挿絵マーカー（type=image）から実際の画像を生成 |
| **diagram-generator** | 挿絵マーカー（type=diagram）からフロー図等を生成 |

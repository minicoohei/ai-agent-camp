---
name: fact-checker
description: |
  記事内の事実主張（数値、日付、固有名詞、統計）を自動抽出し、Web検索で裏付け確認するスキル。
  「ファクトチェックして」「事実確認して」「裏付けを取って」等のリクエストで発動。
  信頼度スコア付きレポートを出力。
version: 1.0.0
author: ai-agent-camp
dependencies:
  - google-genai>=1.0.0
  - pyyaml>=6.0
  - python-dotenv>=0.19.0
triggers:
  - fact-checker
  - ファクトチェック
  - 事実確認
  - 裏付け確認
  - 情報の真偽
  - fact check
---

## トリガーワード
「ファクトチェック」「事実確認」「裏付け」「情報の真偽」

# Fact Checker - ファクトチェックエージェント

## 概要

記事やドキュメント内の事実主張（Factual Claims）を自動的に抽出し、Web検索を使って裏付け確認を行うスキルです。
Gemini API を使って主張を構造化抽出し、各主張に対してグラウンディング検索で検証を実施します。
最終的に、信頼度スコア付きの Markdown レポートを出力します。

## 主張カテゴリ

| カテゴリ | 識別キー | 説明 | 例 |
|---------|---------|------|-----|
| **数値・統計** | `numbers` | 数字を含む主張 | 「市場規模は500億ドル」「成長率15%」 |
| **日付・時系列** | `dates` | 日付や時系列に関する記述 | 「2024年に発表された」「設立から10年」 |
| **固有名詞** | `names` | 人名、組織名、製品名 | 「OpenAIのCEOサム・アルトマン」 |
| **因果関係** | `causation` | 「〜により〜が起きた」型の主張 | 「AIの普及により雇用構造が変化」 |
| **引用・出典** | `citations` | 既存の引用や出典の正確性 | 「Gartnerの調査によると〜」 |

## 検証レベル

| 判定 | 意味 | 基準 |
|------|------|------|
| ✅ **確認済** (Verified) | 複数の信頼できるソースで裏付け | 2つ以上の独立した情報源が一致 |
| ⚠️ **要確認** (Needs Review) | 部分的に一致、または情報が古い可能性 | ソースが1つ、または数値に軽微な差異 |
| ❌ **不一致** (Discrepancy) | ソースと矛盾する情報を発見 | 信頼できるソースと明確に矛盾 |
| ℹ️ **検証不能** (Unverifiable) | 検索で裏付けが見つからない | 公開情報として確認できない |

## クイックスタート

```bash
# 記事全体をファクトチェック
python skills/fact-checker/scripts/fact_checker.py --input article.md

# 数値・統計のみをチェック
python skills/fact-checker/scripts/fact_checker.py --input article.md --category numbers

# 詳細モードで出力先を指定
python skills/fact-checker/scripts/fact_checker.py --input article.md --output report.md --depth thorough

# テストモード（API不要、サンプル記事で動作確認）
python skills/fact-checker/scripts/fact_checker.py --test
```

## パラメータ

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --input, -i | Yes* | - | 入力ファイルパス（Markdown/テキスト） |
| --output, -o | No | `output/fact_report_{timestamp}.md` | 出力レポートのパス |
| --category, -c | No | `all` | チェック対象カテゴリ: `all`, `numbers`, `dates`, `names`, `causation`, `citations` |
| --depth, -d | No | `quick` | 検証深度: `quick`（高速、主要な主張のみ）, `thorough`（全主張を詳細検証） |
| --test | No | false | テストモード（API不要、サンプル記事で動作確認） |

*`--test` 使用時は `--input` は不要

## 出力フォーマット

Markdown レポートが生成されます:

```markdown
# ファクトチェックレポート

**対象ファイル**: article.md
**検証日時**: 2026-02-12 15:30:00
**検証深度**: quick

## サマリー
- 検出した主張: 12件
- ✅ 確認済: 7件
- ⚠️ 要確認: 3件
- ❌ 不一致: 1件
- ℹ️ 検証不能: 1件

## 詳細

### 主張1: 「AIの市場規模は2025年に1900億ドルに達する」
- **カテゴリ**: 数値・統計
- **判定**: ⚠️ 要確認
- **信頼度**: 65%
- **理由**: 数値が最新データと若干異なる。複数ソースで1840〜2000億ドルの範囲
- **出典**:
  - [Statista - AI Market Size](https://example.com/source1)
  - [Grand View Research](https://example.com/source2)

### 主張2: 「OpenAIは2015年にサンフランシスコで設立された」
- **カテゴリ**: 固有名詞 / 日付・時系列
- **判定**: ✅ 確認済
- **信頼度**: 95%
- **理由**: 複数の公式ソースで確認済み
- **出典**:
  - [Wikipedia - OpenAI](https://example.com/source3)
  - [OpenAI公式サイト](https://example.com/source4)
```

## 処理フロー

1. **記事読み込み**: 入力ファイル（Markdown/テキスト）を読み込む
2. **主張抽出**: Gemini API で事実主張を構造化 JSON として抽出
3. **検索クエリ生成**: 各主張に対して最適な検索クエリを生成
4. **検証実行**: Gemini のグラウンディング検索で各主張を検証
5. **レポート生成**: 検証結果を Markdown レポートとして出力

## 環境設定

### 必須: Gemini API Key

```bash
# .env に追加
GEMINI_API_KEY=your_api_key_here
# または
GOOGLE_API_KEY=your_api_key_here
```

### 依存パッケージ

```txt
google-genai>=1.0.0
pyyaml>=6.0
python-dotenv>=0.19.0
```

## 使用例

```bash
# ブログ記事のファクトチェック
python skills/fact-checker/scripts/fact_checker.py \
  --input docs/blog-post.md --depth thorough

# ニュース記事の数値のみチェック
python skills/fact-checker/scripts/fact_checker.py \
  --input news_article.txt --category numbers

# プレスリリースの固有名詞と日付をチェック
python skills/fact-checker/scripts/fact_checker.py \
  --input press_release.md --category names --output output/press_check.md

# テスト実行（API キー不要）
python skills/fact-checker/scripts/fact_checker.py --test
```

## 関連スキル

- **article-writer**: 記事作成スキル（作成後のファクトチェックに連携可能）
- **proofreading-agent**: 校正エージェント（文法・表現チェック）
- **seo-audit**: SEO監査（コンテンツの正確性確認に補完的）

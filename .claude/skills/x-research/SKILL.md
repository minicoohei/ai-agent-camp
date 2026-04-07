---
name: x-research
version: 1.0.0
author: ai-agent-camp
description: |
  X (Twitter) のリアルタイム検索を行い、トピックに関するツイートを収集・分析する。
  検索結果を構造化レポート（Markdown + JSON + TXT）として出力。
  以下のリクエストで使用:
  - 「Xで○○を検索して」「Twitterで○○を調べて」
  - 「○○についてのツイートを分析」「X上での反応を調べて」
  - 「SNSリサーチ: ○○」「○○のトレンドを調査」
  - 「○○に関するX上の意見を集めて」
  - "search X for ○○" "analyze tweets about ○○"
dependencies:
  - requests>=2.28.0
  - python-dotenv>=0.19.0
---

# X Research - X (Twitter) リアルタイム検索・分析

## Description

X API v2 Recent Search エンドポイントを使用して、指定トピックに関するリアルタイムのツイートを検索・収集・分析します。
取得したツイートをエンゲージメント順にランキングし、ハッシュタグ分析・時系列分布・共有URL一覧を含む構造化レポートを
Markdown + JSON + プレーンテキストの3形式で出力します。

## クイックスタート

```bash
# 基本的な検索
python skills/x-research/scripts/x_research.py --topic "生成AI"

# 英語で検索、リツイート除外
python skills/x-research/scripts/x_research.py --topic "Claude AI" --lang en --no-retweets

# 直近3日間、関連度順
python skills/x-research/scripts/x_research.py --topic "OpenAI" --days 3 --sort relevancy
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --topic, -t | Yes | - | 検索トピック・キーワード |
| --query, -q | No | auto | カスタム検索クエリ（topicの代わりに直接指定） |
| --lang, -l | No | ja | 言語フィルタ: ja, en, all |
| --days, -d | No | 7 | 検索期間（日数、最大7） |
| --sort, -s | No | relevancy | ソート: relevancy, recency |
| --no-retweets | No | false | リツイートを除外 |
| --no-replies | No | false | リプライを除外 |
| --media-only | No | false | メディア付きツイートのみ |
| --from-user | No | - | 特定ユーザーのツイートのみ |
| --min-likes | No | 0 | 最小いいね数（取得後フィルタ） |
| --max-results, -m | No | 50 | 1ページあたりの最大取得数（最大100） |
| --max-pages | No | 3 | 最大ページ数 |
| --top-n | No | 10 | トップツイート表示数 |
| --output, -o | No | output/x-research/ | 出力ディレクトリ |
| --session | No | auto | セッション名（出力フォルダ名に使用） |
| --dry-run | No | false | クエリを表示するだけで実行しない |
| --raw-json | No | false | 生APIレスポンスをstderrに出力 |

## クエリ構文ガイド

`--query` で直接指定する場合、X API v2 の検索演算子が使えます:

| 演算子 | 例 | 説明 |
|--------|-----|------|
| キーワード | `生成AI` | 基本キーワード検索 |
| "フレーズ" | `"Claude Code"` | 完全一致フレーズ |
| from: | `from:OpenAI` | 特定ユーザーの投稿 |
| to: | `to:username` | 特定ユーザーへのメンション |
| -is:retweet | `-is:retweet` | リツイート除外 |
| -is:reply | `-is:reply` | リプライ除外 |
| has:media | `has:media` | メディア付きのみ |
| has:links | `has:links` | リンク付きのみ |
| lang: | `lang:ja` | 言語指定 |
| #ハッシュタグ | `#AI` | ハッシュタグ検索 |
| OR | `AI OR 人工知能` | OR 検索 |
| -keyword | `-広告` | キーワード除外 |

## 出力フォーマット

3つのファイルが `output/x-research/YYYYMMDD_HHMMSS_{topic}/` に生成されます:

1. **`{topic}_report.md`** - Markdown レポート
   - サマリー統計（ツイート数、ユニークユーザー数、いいね合計等）
   - トップツイート（エンゲージメント順）
   - ハッシュタグ分析
   - 時系列分布
   - 共有URL一覧

2. **`{topic}_data.json`** - 構造化 JSON
   - メタデータ（クエリ、パラメータ、生成日時）
   - 統計情報
   - 全ツイートデータ（テキスト、メトリクス、著者情報）

3. **`{topic}_raw.txt`** - プレーンテキスト要約

## 使用例

```bash
# 日本語で「生成AI」を検索（デフォルト設定）
python skills/x-research/scripts/x_research.py --topic "生成AI"

# 英語で「Claude」を検索、リツイート・リプライ除外
python skills/x-research/scripts/x_research.py \
  --topic "Claude AI" --lang en --no-retweets --no-replies

# 特定ユーザーの投稿を検索
python skills/x-research/scripts/x_research.py \
  --topic "AI" --from-user AnthropicAI --lang en

# メディア付きツイートのみ、直近3日間
python skills/x-research/scripts/x_research.py \
  --topic "AI art" --media-only --days 3 --lang en

# カスタムクエリで高度な検索
python skills/x-research/scripts/x_research.py \
  --query '"Claude Code" OR "Cursor AI" -is:retweet lang:en' --topic "AI IDE"

# dry-run でクエリを確認
python skills/x-research/scripts/x_research.py \
  --topic "テスト" --no-retweets --lang ja --dry-run
```

## 環境設定

### 必須: X Bearer Token

```bash
# .env に追加
X_BEARER_TOKEN=your_bearer_token_here
```

取得方法:
1. [X Developer Portal](https://developer.x.com/en/portal/dashboard) にアクセス
2. プロジェクト/アプリを作成
3. Bearer Token を取得
4. `.env` ファイルに `X_BEARER_TOKEN=...` を追加

### API制限

| プラン | 検索上限 | 期間 |
|--------|----------|------|
| Free | 使用不可 | - |
| Basic ($100/月) | 60リクエスト/15分 | 直近7日 |
| Pro ($5,000/月) | 300リクエスト/15分 | 直近7日 |

## 出力例

```
=== 出力完了 ===
  Markdown: output/x-research/20260210_053000_生成AI/生成AI_report.md
  JSON:     output/x-research/20260210_053000_生成AI/生成AI_data.json
  Text:     output/x-research/20260210_053000_生成AI/生成AI_raw.txt

--- サマリー ---
  ツイート数:     30
  ユニーク著者:   28
  いいね合計:     1,234
  リツイート合計: 56
  リプライ合計:   12
  期間:           2026-02-03 ~ 2026-02-10
```

## 依存関係

```text
requests>=2.28.0
python-dotenv>=0.19.0
```

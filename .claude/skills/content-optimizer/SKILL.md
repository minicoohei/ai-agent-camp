---
name: content-optimizer
version: 1.0.0
author: ai-agent-camp
description: "コンテンツのA/Bテスト・自己改善ループを支援するプランナースキル。 市場トレンド調査 → 仮説生成 → 実験設計 → メトリクス収集 → 分析改善の全サイクルをカバー。 「コンテンツを最適化」「投稿を改善したい」「トレンド分析して投稿案を作って」「エンゲージメント改善」等のリクエストで発動。"
triggers:
  - content-optimizer
  - コンテンツを最適化
  - 投稿を改善
  - トレンド分析
  - エンゲージメント改善
  - コンテンツ改善ループ
  - Typefully
  - content optimization
dependencies:
  - requests>=2.28.0
  - python-dotenv>=0.19.0
  - pyyaml>=6.0
  - google-genai>=0.5.0
---

# Content Performance Optimizer - コンテンツ自己改善ループ

## Description

5ソース（X, Google検索, Google Trends, Reddit/HN, 競合アカウント）から市場データを収集し、
LLMで統合分析して仮説とA/Bバリアントを自動生成します。
生成した投稿バリアントをTypefullyにドラフト登録し、投稿後のパフォーマンスを測定・学習することで、
コンテンツの継続的な自己改善サイクルを実現します。

## ワークフロー概要

```
① 市場調査 → ② 仮説生成 → ③ バリアント作成 → ④ 投稿（Typefully） → ⑤ メトリクス収集 → ⑥ 分析・学習 → ①に戻る
```

## クイックスタート

```bash
# 仮説生成（トレンド調査→仮説→バリアント一気通貫）
python skills/content-optimizer/scripts/hypothesis_generator.py --topic "AIエージェント" --channel x_twitter

# メトリクス収集（投稿後のパフォーマンス測定）
python skills/content-optimizer/scripts/collect_metrics.py --tweet-ids "123,456" --experiment-id exp-001

# ドライラン（API呼び出しなし）
python skills/content-optimizer/scripts/hypothesis_generator.py --topic "SaaS" --dry-run
```

## スクリプト一覧

| スクリプト | 用途 |
|-----------|------|
| hypothesis_generator.py | 市場調査→仮説生成→バリアント作成 |
| collect_metrics.py | ツイートメトリクス収集・バリアント比較 |
| typefully_client.py | Typefully API v2 クライアント |

## hypothesis_generator.py Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --topic, -t | Yes | - | 調査トピック |
| --channel, -c | No | x_twitter | チャネル: x_twitter, email, linkedin |
| --competitors | No | - | 競合アカウント（カンマ区切り） |
| --lang, -l | No | ja | 言語: ja, en, all |
| --days, -d | No | 7 | 調査期間 |
| --num-hypotheses | No | 5 | 生成する仮説数 |
| --auto-draft | No | false | Typefullyにドラフト自動作成 |
| --output, -o | No | output/content-optimizer/ | 出力先 |
| --dry-run | No | false | API呼び出しなしでプレビュー |
| --test | No | false | セルフテスト |

## collect_metrics.py Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --tweet-ids | No | - | メトリクス取得対象ツイートID（カンマ区切り） |
| --username | No | - | ユーザーの直近投稿を取得 |
| --experiment-id | No | - | 実験IDで紐付けて比較 |
| --days-after | No | 3 | 投稿後何日分のメトリクスを取得 |
| --output, -o | No | output/content-optimizer/ | 出力先 |
| --test | No | false | セルフテスト |

## データソース

| ソース | API | 取得データ | 環境変数 |
|--------|-----|----------|---------|
| X (Twitter) | X API v2 Recent Search | バズ投稿（エンゲージメント上位） | X_BEARER_TOKEN |
| Google 検索 | Gemini Google Search grounding | トレンド記事・ベストプラクティス | GEMINI_API_KEY |
| Google Trends | Gemini grounding経由 | 検索ボリューム推移・急上昇トピック | GEMINI_API_KEY |
| Reddit / HN | Reddit JSON API + HN Algolia API | コミュニティ議論・センチメント | 不要 |
| 競合アカウント | X API v2 User Tweets | 競合の高パフォーマンス投稿 | X_BEARER_TOKEN |

## 出力フォーマット

```
output/content-optimizer/hypotheses/YYYYMMDD_HHMMSS_{topic}/
├── market_report.md       # トレンドレポート
├── hypotheses.yaml        # 仮説リスト（優先度付き）
├── experiment_design.yaml # 実験設計書
├── raw_data.json          # 全ソースの生データ
└── drafts/                # A/Bバリアント投稿案
    ├── variant_a.md
    └── variant_b.md
```

## 環境設定

### 必須環境変数

```bash
# .env に追加
X_BEARER_TOKEN=your_x_bearer_token_here   # X API v2 検索・ユーザー取得
GEMINI_API_KEY=your_gemini_api_key_here   # Google Search grounding + LLM分析
```

### オプション環境変数

```bash
TYPEFULLY_API_KEY=your_typefully_key_here  # --auto-draft オプション使用時
```

### 取得方法

- **X_BEARER_TOKEN**: [X Developer Portal](https://developer.x.com/en/portal/dashboard) でプロジェクト作成後に取得（Basic プラン以上）
- **GEMINI_API_KEY**: [Google AI Studio](https://aistudio.google.com/apikey) で取得（無料）
- **TYPEFULLY_API_KEY**: [Typefully Settings](https://typefully.com/settings/integrations) の API セクションで取得

## 自己改善ループの使い方

1. `hypothesis_generator.py` でトレンド分析 → 仮説 → バリアント生成
2. Typefully で A/B バリアントを投稿（手動 or `--auto-draft` フラグ）
3. 2-3日後に `collect_metrics.py` でパフォーマンス測定
4. 結果を踏まえて次の仮説を生成（学習が蓄積される）

## 使用例

```bash
# AIエージェントについてX向けに仮説生成（日本語）
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "AIエージェント" --channel x_twitter --lang ja

# 競合アカウントも調査してバリアントをTypefullyに自動登録
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "SaaS" --competitors "user_a,user_b" --auto-draft

# 英語でLinkedIn向けコンテンツを5仮説生成
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "productivity" --channel linkedin --lang en --num-hypotheses 5

# ツイートID指定でメトリクス収集
python skills/content-optimizer/scripts/collect_metrics.py \
  --tweet-ids "1234567890,0987654321" --experiment-id exp-001

# ユーザーの直近投稿を取得して分析
python skills/content-optimizer/scripts/collect_metrics.py \
  --username myaccount --days-after 7

# dry-run でどんなデータが取れるか確認
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "生成AI" --dry-run
```

## 依存関係

```text
requests>=2.28.0
python-dotenv>=0.19.0
pyyaml>=6.0
google-genai>=0.5.0
```

## Related Skills

- `x-research` — X検索データの収集
- `ab-test-setup` — 実験設計の詳細フレームワーク
- `social-content` — SNSコンテンツ戦略
- `content-strategy` — コンテンツ計画
- `analytics-tracking` — メトリクス計測

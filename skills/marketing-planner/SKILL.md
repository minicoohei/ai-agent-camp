---
name: marketing-planner
description: "マーケティング計画策定・プロダクトマーケティングコンテキスト作成スキル。 「マーケ計画」「ポジショニング」「ペルソナ作成」「競合分析」「コンテンツ戦略」等で発動。 product-marketing-context.mdを生成し、他のマーケティングスキルの土台を作る。"
triggers:
  - マーケ計画
  - マーケティング計画
  - ポジショニング
  - ペルソナ
  - 競合分析
  - コンテンツ戦略
  - ターゲット設定
  - product marketing context
---

# Marketing Planner

プロダクトのマーケティング基礎文書を作成し、全マーケティング施策の土台を構築する。

## 出力ファイル

`marketing/product-context.md` — 他スキル（content-creator, post-publisher等）が参照する共通コンテキスト。

## ワークフロー

### Step 1: 既存コンテキスト確認

`marketing/product-context.md` が存在するか確認。
- **存在する場合**: 読み込んで更新箇所を確認
- **存在しない場合**: 新規作成フローへ

### Step 2: 情報収集

以下のセクションを会話形式で埋める。一度に全部聞かない。

1. **プロダクト概要** — 一言説明、カテゴリ、ビジネスモデル、価格
2. **ターゲット** — ユーザー層、ペルソナ、主要ユースケース
3. **課題・ペイン** — ユーザーが抱える問題、既存ソリューションの不足
4. **競合** — 直接/間接競合、差別化ポイント
5. **ブランドボイス** — トーン、スタイル、使う言葉/避ける言葉
6. **目標** — ビジネスゴール、KPI、コンバージョンアクション

詳細フレームワーク → `references/context-template.md`

### Step 3: コンテキスト文書生成

収集した情報から `marketing/product-context.md` を生成。

### Step 4: チャネル戦略（オプション）

コンテキストに基づいて最適チャネルミックスを提案。
詳細 → `references/channel-strategy.md`

### Step 5: コンテンツカレンダー（オプション）

月次/週次のコンテンツ投稿計画を `marketing/content-calendar.md` に出力。

## 関連スキル

- `content-creator` — コンテキストを参照してコンテンツ制作
- `post-publisher` — 制作コンテンツを各プラットフォームに投稿
- 元スキル: `product-marketing-context`, `content-strategy`, `marketing-ideas`, `launch-strategy`

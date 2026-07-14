# マーケティングスキル基盤

## 概要

OpenClaw / Claude Code 対応のマーケティングスキルセット。
[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) をベースに、
日本市場向けにカスタマイズ・拡張したOpenClaw対応スキル3種を追加。

## スキル構成

### OpenClaw対応スキル（自作）

| スキル | 説明 | パス |
|-------|------|------|
| **marketing-planner** | 計画策定・プロダクトコンテキスト作成 | `skills/marketing-planner/` |
| **content-creator** | コンテンツ制作（SNS/記事/バナー/動画/メール） | `skills/content-creator/` |
| **post-publisher** | 投稿実行（Typefully API連携） | `skills/post-publisher/` |

### ベーススキル（marketingskills由来 × 19）

| カテゴリ | スキル |
|---------|--------|
| **戦略** | product-marketing-context, content-strategy, marketing-ideas, launch-strategy, marketing-psychology, pricing-strategy |
| **コピー** | copywriting, copy-editing, email-sequence, social-content |
| **SEO** | seo-audit, programmatic-seo, schema-markup, competitor-alternatives |
| **広告** | paid-ads, ab-test-setup, analytics-tracking |
| **成長** | referral-program, free-tool-strategy |

## フロー

```text
marketing-planner（計画）
  → product-context.md 生成
    → content-creator（制作）
      → drafts/ にコンテンツ保存
        → post-publisher（投稿）
          → Typefully API → X/LinkedIn
          → post-log.md に記録
```

## セットアップ

1. `TYPEFULLY_API_KEY` を環境変数/secretsに設定
2. `marketing/product-context.md` を `marketing-planner` で作成
3. `content-creator` でコンテンツ制作
4. `post-publisher` で投稿

## Issue管理

[marketing ラベルのIssue一覧](../../issues?q=is%3Aissue+label%3Amarketing)

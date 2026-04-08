---
name: content-creator
description: |
  マーケティングコンテンツ制作スキル。X/Instagram投稿、Note/Medium記事、
  バナー画像、動画スクリプト等を作成する。
  「投稿作って」「バナー作成」「記事書いて」「コピー作成」等で発動。
  product-context.mdを参照してブランド一貫性を保つ。
triggers:
  - 投稿作って
  - コンテンツ作成
  - バナー作成
  - 記事書いて
  - コピー作成
  - SNS投稿
  - ツイート作成
  - Instagram投稿
  - Note記事
  - Medium記事
---

# Content Creator

マーケティングコンテンツを制作するスキル。プロダクトコンテキストに基づいてブランド一貫性のあるコンテンツを生成する。

## 前提

`marketing/product-context.md` が存在すること。なければ `marketing-planner` スキルで先に作成を促す。

## コンテンツタイプ

### 1. SNS投稿（X / Instagram）

**入力**: テーマ or プロンプト
**出力**: 投稿テキスト + ハッシュタグ + （必要なら）画像プロンプト

フォーマット → `references/post-formats.md`

#### X (Twitter)
- 280文字以内（日本語は140文字目安）
- スレッド形式も対応（3-7ツイート）
- CTA明確に

#### Instagram
- キャプション: 2200文字以内、最初の125文字が勝負
- ハッシュタグ: 20-30個（関連性順）
- Reels/Stories用スクリプトも対応

### 2. 記事（Note / Medium / ブログ）

**入力**: テーマ、ターゲット、目的
**出力**: 構成案 → 本文 → メタ情報

プロセス:
1. アウトライン提案（H2/H3構成）
2. 承認後に本文執筆
3. SEOメタ（タイトル、description、OGP）生成

### 3. バナー画像

**入力**: 用途、テキスト、スタイル
**出力**: Gemini画像生成プロンプト → 生成 → 確認

サイズガイド:
- X: 1200×675px
- Instagram Feed: 1080×1080px
- Instagram Stories: 1080×1920px
- Note/Medium OGP: 1200×630px

### 4. 動画スクリプト

**入力**: テーマ、尺、プラットフォーム
**出力**: スクリプト（セリフ + 画面指示）

- Short (15-60秒): フック→本題→CTA
- Long (5-15分): イントロ→セクション→まとめ→CTA

### 5. メール

**入力**: 目的、ターゲット、シーケンス位置
**出力**: 件名 + 本文 + CTA

詳細 → `references/email-templates.md`

## コンテンツ品質チェック

生成後に必ず確認:
- [ ] product-context.mdのブランドボイスに合致
- [ ] ターゲットペルソナに適切
- [ ] CTAが明確
- [ ] プラットフォーム制約を満たす（文字数、画像サイズ等）
- [ ] 避けるべき言葉を使っていない

## バッチ生成

「1週間分の投稿作って」等のリクエストに対応:
1. content-calendar.md参照（あれば）
2. テーマバリエーション生成
3. 曜日・時間帯に最適化
4. 一括出力 → `marketing/drafts/` に保存

## 関連スキル

- `marketing-planner` — コンテキスト文書作成
- `post-publisher` — 制作コンテンツの投稿実行
- 元スキル: `copywriting`, `copy-editing`, `social-content`, `email-sequence`

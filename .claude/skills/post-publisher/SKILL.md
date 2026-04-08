---
name: post-publisher
description: |
  コンテンツの投稿・配信実行スキル。Typefully経由のX投稿、画像アップロード、
  投稿スケジューリングを行う。
  「投稿して」「スケジュール設定」「Typefullyに下書き」等で発動。
triggers:
  - 投稿して
  - 投稿する
  - スケジュール投稿
  - Typefully
  - 下書き作成
  - 配信
  - publish
  - schedule post
---

# Post Publisher

制作済みコンテンツを各プラットフォームに投稿・スケジューリングする。

## 対応プラットフォーム

| プラットフォーム | 方法 | ステータス |
|----------------|------|-----------|
| X (Twitter) | Typefully API | ✅ 対応 |
| X スレッド | Typefully API | ✅ 対応 |
| LinkedIn | Typefully API | ✅ 対応 |
| Instagram | 手動 / Meta API（要実装） | 🔧 計画中 |
| TikTok | 手動 / TikTok API（要実装） | 🔧 計画中 |
| Note | 手動 / API（要調査） | 🔧 計画中 |
| Medium | Medium API | 🔧 計画中 |

## Typefully API

### 認証
環境変数: `TYPEFULLY_API_KEY`

### エンドポイント

#### 下書き作成
```bash
curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "投稿テキスト",
    "threadify": false,
    "schedule-date": "2025-01-15T09:00:00Z",
    "auto_retweet_enabled": false,
    "auto_plug_enabled": false
  }'
```

#### スレッド投稿
`content` 内で `\n\n\n\n` （改行4つ）でツイートを区切る。
```json
{
  "content": "1/🧵 フック\n\n\n\n2/ 本題\n\n\n\n3/ CTA",
  "threadify": true
}
```

#### スケジュール投稿
- `schedule-date`: ISO 8601形式（UTC）
- `schedule-date: "next-free-slot"` で次の空きスロットに自動配置

#### 即時投稿（下書きなし）
```json
{
  "content": "テキスト",
  "schedule-date": "next-free-slot"
}
```

### 画像付き投稿

Typefully APIは画像直接アップロード非対応。ワークフロー:
1. 画像をcatbox.moeにアップロード
2. Typefully下書きにテキストのみ投稿
3. 画像URLをコメントで付記（手動添付が必要な場合あり）

## 投稿ワークフロー

### 単発投稿
1. `marketing/drafts/` からコンテンツ読み込み（またはcontent-creatorで生成）
2. プラットフォーム確認
3. Typefully APIで下書き or スケジュール作成
4. 確認メッセージ送信

### バッチ投稿
1. `marketing/drafts/` 内の複数コンテンツ読み込み
2. スケジュール配分（時間帯最適化）
3. 一括API呼び出し
4. 結果サマリー送信

### 最適投稿時間（日本市場）
| 曜日 | X | Instagram | TikTok |
|------|---|-----------|--------|
| 平日 | 7-8時, 12時, 18-21時 | 12時, 18-21時 | 18-22時 |
| 土日 | 9-11時, 14-16時 | 10-12時, 15-17時 | 12-22時 |

## ログ

投稿結果を `marketing/post-log.md` に記録:
```markdown
| 日時 | プラットフォーム | コンテンツ要約 | URL | ステータス |
```

## 関連スキル

- `marketing-planner` — 計画策定
- `content-creator` — コンテンツ制作

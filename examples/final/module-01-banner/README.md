# Module 1: バナー生成 - 成果物（Final）

SNS投稿用バナー画像の生成例です。

## 学習目標
- banner-creatorスキルを使ってSNSバナーを作成できる
- 各プラットフォームの推奨サイズを理解する
- 効果的なバナーデザインの要素を把握する

## 成果物一覧

| ファイル | サイズ | 用途 |
|---------|--------|------|
| `banner-x-post.png` | 1200x675px | X（Twitter）投稿用 |
| `banner-youtube-thumbnail.png` | 1280x720px | YouTubeサムネイル |
| `banner-instagram-square.png` | 1080x1080px | Instagram正方形 |
| `banner-linkedin-cover.png` | 1584x396px | LinkedInカバー |

## 各プラットフォームの推奨サイズ

```
┌─────────────────────────────────────────────────────────┐
│  プラットフォーム別 推奨バナーサイズ                      │
├─────────────────────────────────────────────────────────┤
│  X (Twitter)                                            │
│    ├─ 投稿画像: 1200 x 675px (16:9)                     │
│    ├─ ヘッダー: 1500 x 500px (3:1)                      │
│    └─ プロフィール: 400 x 400px (1:1)                   │
├─────────────────────────────────────────────────────────┤
│  YouTube                                                │
│    ├─ サムネイル: 1280 x 720px (16:9)                   │
│    └─ チャンネルアート: 2560 x 1440px                   │
├─────────────────────────────────────────────────────────┤
│  Instagram                                              │
│    ├─ 正方形: 1080 x 1080px (1:1)                       │
│    ├─ 縦長: 1080 x 1350px (4:5)                         │
│    └─ ストーリー: 1080 x 1920px (9:16)                  │
├─────────────────────────────────────────────────────────┤
│  LinkedIn                                               │
│    ├─ 投稿画像: 1200 x 627px                            │
│    └─ カバー: 1584 x 396px                              │
└─────────────────────────────────────────────────────────┘
```

## 実行コマンド例

### X投稿用バナー
```bash
uv run python tools/banner_creator.py \
  --platform x_post \
  --topic "AIで業務効率化" \
  --style "modern, business" \
  --output examples/final/module-01-banner/banner-x-post.png
```

### YouTubeサムネイル
```bash
uv run python tools/banner_creator.py \
  --platform youtube_thumbnail \
  --topic "【保存版】ChatGPT活用術10選" \
  --style "bold, eye-catching, thumbnail" \
  --output examples/final/module-01-banner/banner-youtube-thumbnail.png
```

### Instagram正方形
```bash
uv run python tools/banner_creator.py \
  --platform instagram_square \
  --topic "週末限定セール開催中" \
  --style "clean, minimal, japanese" \
  --output examples/final/module-01-banner/banner-instagram-square.png
```

## バナーデザインのポイント

### 1. テキストの視認性
- **コントラスト**: 背景と文字のコントラストを確保
- **フォントサイズ**: 小さいデバイスでも読めるサイズ
- **文字数**: 簡潔に（X投稿なら10文字以内推奨）

### 2. 配色
- **ブランドカラー**: 一貫性のある色使い
- **アクセントカラー**: CTAボタンや重要要素に
- **背景**: シンプルで邪魔にならない

### 3. レイアウト
- **余白**: 適度な余白で見やすく
- **整列**: 要素を揃えて整然と
- **視線誘導**: 重要な情報に視線を誘導

## プロンプトのコツ

```markdown
# 効果的なプロンプト例

## 良い例 ✅
「青と白を基調とした、ビジネス向けの洗練されたデザイン。
テキスト『AIで業務効率化』を中央に配置。
背景にはグラデーションと抽象的なテクノロジーパターン」

## 悪い例 ❌
「かっこいいバナー」
「おしゃれな画像」
```

## チェックリスト

- [ ] 推奨サイズで作成されている
- [ ] テキストが読みやすい
- [ ] ブランドカラーが適切に使われている
- [ ] プラットフォームに適したデザイン
- [ ] 高解像度で出力されている

## 関連レッスン

- `/start-1-1`: バナー生成入門
- `/start-1-2`: 応用バナー作成
- `/start-1-3`: バッチ生成

## 参考リンク

- [Twitter画像サイズガイド](https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/uploading-media/media-best-practices)
- [YouTube サムネイル ベストプラクティス](https://support.google.com/youtube/answer/72431)
- [Instagram 画像サイズ](https://help.instagram.com/1631821640426723)

# 演習: SNSバナー生成

![SNSバナー生成ワークフロー](images/exercise-hero.png)

## 概要

複数のSNSプラットフォーム向けにバナー画像を自動生成する演習です。
`banner-creator` スキルを使い、X（旧Twitter）、Instagram、Facebookの3プラットフォーム向けにそれぞれ最適化されたバナーを作成します。

## 前提条件

- Gemini API キーが設定済みであること（`GEMINI_API_KEY` または `GOOGLE_API_KEY`）
- Python 3.8 以上がインストール済み
- 必要パッケージ: `google-genai`, `Pillow`, `python-dotenv`, `requests`

```bash
# 環境確認
echo $GEMINI_API_KEY
python --version
uv add google-genai Pillow python-dotenv requests
```

## タスク

### タスク1: X投稿用バナー生成（1200x675）

X（旧Twitter）向けの投稿バナーを生成してください。

```bash
uv run python tools/banner_creator.py \
  --platform x_post \
  --message "AIエージェント研修 - Claude Code で業務効率化" \
  --tone professional \
  --color-scheme cool \
  --output output/x-post-banner.png
```

**要件:**
- テーマ: AI研修・業務効率化
- トーン: プロフェッショナル
- CTAやサブコピーの追加は任意

### タスク2: Instagram投稿用バナー生成（1080x1080）

Instagram フィード向けの正方形バナーを生成してください。

```bash
uv run python tools/banner_creator.py \
  --platform instagram_feed \
  --message "非エンジニアでもできるAI活用" \
  --sub-copy "AIエージェント研修プログラム" \
  --tone pop \
  --color-scheme vivid \
  --output output/instagram-feed.png
```

**要件:**
- テーマ: AI活用の敷居の低さ
- トーン: ポップで親しみやすい
- 視覚的にインパクトがある配色

### タスク3: Facebook広告用バナー生成（1200x630）

Facebook 広告向けのバナーを生成してください。

```bash
uv run python tools/banner_creator.py \
  --platform facebook \
  --message "業務効率3倍 - AIエージェント活用ブートキャンプ" \
  --cta "今すぐ申し込む" \
  --tone urgent \
  --priority ctr \
  --output output/facebook-ad.png
```

**要件:**
- テーマ: 業務効率化の具体的な数値訴求
- CTAボタンのテキストを含める
- クリック率（CTR）を重視した構成

## 完了条件

- [ ] X投稿用バナー（1200x675）が正常に生成されている
- [ ] Instagram投稿用バナー（1080x1080）が正常に生成されている
- [ ] Facebook広告用バナー（1200x630）が正常に生成されている
- [ ] 各画像が指定のプラットフォームサイズに合致している
- [ ] 生成コマンドと結果をメモしている

## ヒント

- 詳しいプロンプトのコツは `hints.md` を参照してください
- `data/sample-copy.json` にバナー用コピーのサンプルがあります
- `data/brand-guidelines.md` にブランドカラーとトーンの指定例があります
- `--with-copy` オプションでコピーテキストも同時生成できます
- `--variants 3` で複数バリエーションを一度に生成できます

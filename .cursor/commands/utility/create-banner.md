# Create Banner - 広告バナー/クリエイティブ生成

このコマンドは、`tools/banner_creator.py` を使用して、各種SNS・広告プラットフォーム向けのバナー/クリエイティブを生成します。

## 重要：実行前の確認事項

**このコマンドを実行する前に、必ず `ask_question` ツールを使用して以下の情報を確認してください。**

## Step 1: ask_question で情報収集

以下の質問を `ask_question` ツールで確認してください：

```json
{
  "title": "広告バナー/クリエイティブ作成",
  "questions": [
    {
      "id": "platform",
      "prompt": "どのプラットフォーム向けのバナーを作成しますか？",
      "options": [
        {"id": "x_post", "label": "X (Twitter) - タイムライン投稿 (1200x675)"},
        {"id": "x_card", "label": "X (Twitter) - カード表示 (800x418)"},
        {"id": "facebook", "label": "Facebook - リンク投稿 (1200x630)"},
        {"id": "facebook_story", "label": "Facebook - ストーリーズ (1080x1920)"},
        {"id": "instagram_feed", "label": "Instagram - フィード投稿 (1080x1080)"},
        {"id": "instagram_story", "label": "Instagram - ストーリーズ (1080x1920)"},
        {"id": "prtimes", "label": "PRタイムズ - プレスリリース (1200x630)"},
        {"id": "youtube", "label": "YouTube - サムネイル (1280x720)"},
        {"id": "line", "label": "LINE - リッチメッセージ (1040x1040)"},
        {"id": "web_horizontal", "label": "Web広告 - 横長 (1200x628)"},
        {"id": "web_vertical", "label": "Web広告 - 縦長 (300x600)"},
        {"id": "custom", "label": "カスタムサイズ"}
      ],
      "allow_multiple": false
    },
    {
      "id": "tone",
      "prompt": "バナーのトーン/雰囲気を選択してください",
      "options": [
        {"id": "professional", "label": "プロフェッショナル - ビジネス向け、信頼感"},
        {"id": "casual", "label": "カジュアル - 親しみやすい、フレンドリー"},
        {"id": "pop", "label": "ポップ - 明るい、楽しい、若者向け"},
        {"id": "elegant", "label": "エレガント - 高級感、洗練された"},
        {"id": "urgent", "label": "緊急感 - セール、期間限定、今すぐ"},
        {"id": "minimal", "label": "ミニマル - シンプル、余白を活かす"},
        {"id": "tech", "label": "テック - 先進的、デジタル感"},
        {"id": "natural", "label": "ナチュラル - 自然、オーガニック"}
      ],
      "allow_multiple": false
    },
    {
      "id": "color_scheme",
      "prompt": "色味の方向性を選択してください",
      "options": [
        {"id": "brand", "label": "ブランドカラー指定（後で入力）"},
        {"id": "warm", "label": "暖色系 - 赤、オレンジ、黄色"},
        {"id": "cool", "label": "寒色系 - 青、緑、紫"},
        {"id": "mono", "label": "モノトーン - 白黒、グレー"},
        {"id": "pastel", "label": "パステル - 淡い色合い"},
        {"id": "vivid", "label": "ビビッド - 鮮やかな原色"},
        {"id": "dark", "label": "ダーク - 黒ベース、高級感"},
        {"id": "auto", "label": "AIにおまかせ"}
      ],
      "allow_multiple": false
    },
    {
      "id": "font_style",
      "prompt": "フォントスタイルを選択してください",
      "options": [
        {"id": "gothic", "label": "ゴシック体 - 読みやすい、モダン"},
        {"id": "mincho", "label": "明朝体 - 伝統的、高級感"},
        {"id": "handwritten", "label": "手書き風 - 親しみやすい、個性的"},
        {"id": "bold", "label": "太字・インパクト - 力強い、目立つ"},
        {"id": "script", "label": "スクリプト体 - エレガント、女性向け"},
        {"id": "geometric", "label": "ジオメトリック - 未来的、テック"},
        {"id": "auto", "label": "AIにおまかせ"}
      ],
      "allow_multiple": false
    },
    {
      "id": "priority",
      "prompt": "このバナーで最も重要視することは？",
      "options": [
        {"id": "ctr", "label": "クリック率 (CTR) - 目立つ、行動喚起"},
        {"id": "brand", "label": "ブランド認知 - ロゴ・企業名を強調"},
        {"id": "info", "label": "情報伝達 - 内容を正確に伝える"},
        {"id": "emotion", "label": "感情訴求 - 共感、感動を呼ぶ"},
        {"id": "product", "label": "商品訴求 - 商品を魅力的に見せる"},
        {"id": "event", "label": "イベント告知 - 日時・場所を明確に"}
      ],
      "allow_multiple": false
    },
    {
      "id": "reference_type",
      "prompt": "参考画像をどのように指定しますか？",
      "options": [
        {"id": "search", "label": "キーワードでWeb検索（競合・類似クリエイティブを参考）"},
        {"id": "url", "label": "画像URLを直接指定"},
        {"id": "local", "label": "ローカルファイルを指定"},
        {"id": "none", "label": "参考画像なし（テキストから生成）"}
      ],
      "allow_multiple": false
    }
  ]
}
```

## Step 2: 追加情報の取得

上記の回答に基づいて、以下の追加情報をテキスト入力で確認してください：

1. **メインメッセージ/キャッチコピー**: バナーに表示するテキスト
2. **サブコピー（任意）**: 補足情報、詳細
3. **CTA（行動喚起）**: 「今すぐ登録」「詳細はこちら」など
4. **ブランド名/ロゴ（任意）**: 表示する企業・サービス名
5. **ブランドカラー（color_schemeでbrand選択時）**: HEXコード例: #FF5733
6. **カスタムサイズ（custom選択時）**: 幅x高さ 例: 1200x800
7. **参考画像の検索キーワード/URL/パス（reference_typeの選択に応じて）**
8. **セッション名**: 出力フォルダの名前（例: summer_sale_campaign）

## Step 3: ツールの実行

収集した情報を元に、以下のコマンドを実行します（media-generator サブエージェントに委譲も可能）：

```bash
uv run python tools/banner_creator.py \
  --platform "{platform}" \
  --message "{メインメッセージ}" \
  --tone "{tone}" \
  --color-scheme "{color_scheme}" \
  --font-style "{font_style}" \
  --priority "{priority}" \
  --session "{セッション名}" \
  --with-copy
```

### オプション引数

| 引数 | 説明 | 例 |
|------|------|-----|
| `--platform` | プラットフォーム（必須） | `x_post`, `instagram_feed` |
| `--message` | メインメッセージ（必須） | `"夏のセール開催中"` |
| `--tone` | トーン | `professional`, `pop` |
| `--color-scheme` | 色味 | `warm`, `cool`, `#FF5733` |
| `--font-style` | フォント | `gothic`, `bold` |
| `--priority` | 重要視する点 | `ctr`, `brand` |
| `--sub-copy` | サブコピー | `"最大50%OFF"` |
| `--cta` | CTAテキスト | `"今すぐチェック"` |
| `--brand-name` | ブランド名 | `"MyCompany"` |
| `--reference` | 参考画像パス/URL | `./ref.png` or URL |
| `--search-ref` | 参考画像を検索 | `"SaaS広告 バナー"` |
| `--session` | セッション名 | `"summer_campaign"` |
| `--with-copy` | 投稿用コピーも生成 | フラグ |
| `--variants` | バリエーション数 | `3` |
| `--output` | 出力先 | `./output/banner.png` |

## Step 4: 結果の報告

生成完了後、以下を報告してください：

1. **生成されたバナー画像のパス**
2. **生成されたコピーテキスト**（--with-copy指定時）
   - 投稿文案 × 3パターン
   - ハッシュタグ提案
   - CTAフレーズ
3. **バリエーション**（--variants指定時）

## 使用例

### X投稿用バナー
```bash
uv run python tools/banner_creator.py \
  --platform x_post \
  --message "AI時代の働き方改革" \
  --sub-copy "無料ウェビナー開催" \
  --cta "今すぐ登録" \
  --tone professional \
  --color-scheme cool \
  --font-style bold \
  --priority ctr \
  --session "webinar_promotion" \
  --with-copy
```

### Instagramフィード用（参考画像検索）
```bash
uv run python tools/banner_creator.py \
  --platform instagram_feed \
  --message "新商品発売" \
  --tone pop \
  --color-scheme vivid \
  --search-ref "コスメ 新商品 Instagram広告" \
  --with-copy
```

### PRタイムズ用プレスリリース画像
```bash
uv run python tools/banner_creator.py \
  --platform prtimes \
  --message "〇〇株式会社、新サービスを発表" \
  --brand-name "〇〇株式会社" \
  --tone professional \
  --color-scheme "#1E40AF" \
  --font-style gothic \
  --priority info
```

## 注意事項

- 実行には `GEMINI_API_KEY` または `GOOGLE_API_KEY` が環境変数に設定されている必要があります
- 生成された画像は `docs/generated/banners/{日付}_{セッション名}/` に保存されます
- `--with-copy` オプションで投稿用テキストも同時に生成されます
- Web検索での参考画像取得にはブラウザツールが使用されます

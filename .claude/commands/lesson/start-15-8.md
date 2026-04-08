---
description: "When the user says /start-15-8 — Module 15 Lesson 15-8: Clipper × Remotion でマーケ素材を自動生成"
duration: 45分
prerequisites: ["start-15-7"]
level: intermediate
tags: ["video", "remotion", "marketing", "sns"]
---

# Lesson 15-8: Clipper × Remotion — マーケ素材自動生成

## 学習目標

Lesson 15-7 で抽出したクリップを、Remotion を使って
SNS用マーケティング素材に変換する方法を学びます。

1. Remotion の基本概念（React + 動画 = プログラマブル動画）
2. テンプレートの理解（ShortClip, QuoteClip, SummaryVideo）
3. クリップ → SNS投稿用動画への変換
4. 複数フォーマットの同時出力
5. CursorBootcampブランドのカスタマイズ

---

## Remotionとは？

Remotion は **React でプログラマブルに動画を作る** フレームワークです。

- HTMLとCSSで動画のレイアウトを定義
- React コンポーネントでアニメーションを制御
- FFmpeg でローカルレンダリング（API不要、コスト$0）
- テンプレートを一度作れば、データを変えるだけで量産可能

---

## Step 1: 統合パイプラインの実行

Lesson 15-7 のClipperと組み合わせて、一気通貫で実行:

```bash
uv run python tools/ugc/clipper_marketing_pipeline.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --auto-select "score>0.8" \
  --batch-render short,quote
```

これにより:
1. 動画DL → AI分析 → ハイライト抽出
2. 各クリップを「ショート(9:16)」「引用(16:9)」でレンダリング
3. SNS投稿ドラフト（テキスト + ハッシュタグ）を自動生成

---

## Step 2: テンプレートの種類を理解する

利用可能なテンプレート一覧:

```bash
uv run python tools/ugc/remotion_render.py --list-templates
```

| テンプレート | サイズ | 用途 |
|-------------|--------|------|
| `short` | 1080x1920 (9:16) | TikTok / Reels / Shorts |
| `quote` | 1920x1080 (16:9) | Twitter/X / LinkedIn |
| `summary` | 1920x1080 (16:9) | YouTube / ブログ |
| `blog` | 1920x1080 (16:9) | ブログ埋め込み |
| `training` | 1920x1080 (16:9) | 研修素材 |
| `square` | 1080x1080 (1:1) | Instagram Feed |

---

## Step 3: 個別レンダリング

特定のクリップを特定のテンプレートでレンダリング:

```bash
# Lesson 15-7 で生成されたremotion_input.jsonを指定
uv run python tools/ugc/remotion_render.py \
  --input output/clips/SESSION_DIR/remotion_input.json \
  --template short \
  --clip-id clip_01
```

---

## Step 4: バッチレンダリング

1つのクリップから全フォーマットを一括生成:

```bash
uv run python tools/ugc/remotion_render.py \
  --input output/clips/SESSION_DIR/remotion_input.json \
  --batch short,quote,summary,square
```

---

## Step 5: SNS投稿ドラフトの確認

パイプライン実行後に生成される `post_drafts.json` を確認:

```bash
cat output/clips/SESSION_DIR/post_drafts.json | python3 -m json.tool
```

各プラットフォーム向けのテキスト、ハッシュタグ、動画パスが含まれています。

---

## 演習課題

1. **基本**: 好きな動画のハイライトを3つ選び、ショート動画(9:16)を生成してください
2. **応用**: 同じクリップから3種類（short, quote, square）を同時生成してください
3. **発展**: 生成されたpost_drafts.jsonを元に、実際にSNS投稿文を完成させてください

---

## コスト参考

| 処理 | コスト |
|------|--------|
| Clipper（DL + 分析 + 翻訳） | ~$0.035/動画 |
| Remotion レンダリング | $0（ローカル） |
| **合計** | **~$0.035/動画** |

---

## まとめ

- YouTube Clipper でAIが動画の「おいしいところ」を自動検出
- Remotion でテンプレートに流し込み → SNS素材を量産
- 1本の動画から複数プラットフォーム用の素材を同時生成
- コストはほぼゼロ（Gemini API ~$0.035 + ローカルレンダリング）


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/ugc/
├── *.mp4           (動画ファイル)
├── metadata.json   (メタデータ)
└── thumbnails/     (サムネイル)
```

### 確認コマンド
```bash
# 出力ファイルの一覧とサイズ
ls -lh output/ugc/

# メタデータを確認
cat output/ugc/*metadata*.json 2>/dev/null | head -20

# 動画を再生（macOS: open / Linux: xdg-open）
open output/ugc/*.mp4
```

---

## ➡️ 次のステップ

これでModule 15（動画制作）は完了です。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-16-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-16-1
- finish → 終了

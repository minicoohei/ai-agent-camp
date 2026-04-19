---
name: video-editor
description: "TikTok/YouTube向け動画編集スキル。ffmpegでキャプション焼き込み、 Ken Burnsエフェクト、シーン結合、音声合成を行う。 scenes.jsonから自動的に編集指示を読み取り最終動画を出力する。 Remotionコンポーネントも同梱（ローカル環境用）。 「動画編集」「キャプション追加」「テロップ付き動画」等で発動。"
triggers:
  - 動画を編集
  - キャプションを追加
  - テロップ付き動画を作成
  - シーンを結合
  - 動画を書き出し
  - video-editor
  - ffmpeg 編集
---

# Video Editor

scenes.json + フレーム画像/動画クリップから最終動画を生成する。

## 2つの実行モード

### 🟢 ffmpegモード（サンドボックス対応・推奨）
Chromium不要。サンドボックスでも動作する。

```bash
python skills/video-editor/scripts/compose_video.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --captions \
  --output output/final_tiktok.mp4
```

### 🔵 Remotionモード（ローカル環境用）
Chromium + Node.js必要。より高度なアニメーション。

```bash
npx remotion render TikTokVideo --output=out/tiktok_video.mp4 --root=remotion-editor/src/Root.tsx
```

## ffmpegパイプライン

### 1. 素材準備
```
scenes.json → 各フレームのmotion_type確認
  i2v        → video/{frame}_i2v.mp4 を使用
  ken_burns  → ffmpeg zoompan フィルターで画像→動画
  static     → ffmpeg loop で画像→動画
  motion_graphics → ffmpeg で画像→動画（将来テキストアニメ追加）
```

### 2. 正規化
全クリップを統一仕様に:
- 解像度: 1080×1920 (9:16) or 1920×1080 (16:9)
- FPS: 30
- コーデック: h264 / yuv420p
- 横向きi2V動画 → ぼかし背景付き縦型に変換

### 3. キャプション焼き込み（drawtext）
```bash
ffmpeg -i clip.mp4 -vf "drawtext=text='テキスト':fontfile=/path/to/NotoSansJP-Bold.otf:\
  fontsize=64:fontcolor=white:borderw=3:bordercolor=black:\
  x=(w-text_w)/2:y=h*0.58" output.mp4
```

キャプション仕様:
| 項目 | TikTok推奨 |
|------|-----------|
| フォントサイズ | 54-76px (画面幅の5-7%) |
| 文字数/行 | 日本語5-8文字 / 英語2-3語 |
| 最大行数 | 2行 |
| フォント | Noto Sans JP Bold |
| 色 | 白 + 黒ストローク(3px) + シャドウ |
| 位置 | Y: 55-65% (TikTokセーフゾーン内) |

### 4. 結合
```bash
ffmpeg -f concat -safe 0 -i concat.txt -c:v libx264 -pix_fmt yuv420p final.mp4
```

### 5. 音声合成（オプション）
```bash
ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac -shortest final_with_audio.mp4
```

## TikTokセーフゾーン
```
┌─────────────────────┐
│  ⚠️ 上15% 避ける     │ ← ユーザー名/フォローボタン
├─────────────────────┤
│   メインコンテンツ    │
│  ┌───────────────┐  │
│  │ キャプション    │  │ ← Y: 55-65%
│  └───────────────┘  │
├─────────────────────┤
│  ⚠️ 下20% 避ける     │ ← いいね/コメント/シェア
└─────────────────────┘
```

## scenes.json フォーマット
```json
{
  "title": "動画タイトル",
  "scenes": [
    {
      "frame_number": 1,
      "timestamp": "0:00-0:02",
      "motion_type": "i2v | ken_burns | static | motion_graphics",
      "narration": "ナレーション台本",
      "text_overlay": {
        "main_text": "メインテロップ",
        "sub_text": "サブテロップ",
        "position": "top | center | bottom",
        "style": "bold | subtitle | minimal"
      }
    }
  ]
}
```

## 依存
- ffmpeg (静的バイナリ: `.bin/ffmpeg`)
- Python 3.11+ (compose_video.py)
- Noto Sans JP フォント（キャプション用）

## Remotionコンポーネント（ローカル用）
```
remotion-editor/src/
  components/
    Caption.tsx    # TikTok最適キャプション（日本語改行、pop-inアニメ）
    KenBurns.tsx   # Ken Burns zoom/pan エフェクト
  compositions/
    TikTokVideo.tsx # 9:16 メインコンポジション
  Root.tsx         # エントリポイント
```

## 関連スキル
- `storyboard-generator` — 入力素材（frames + scenes.json）
- `content-creator` — コンテンツ企画
- `post-publisher` — 投稿・配信

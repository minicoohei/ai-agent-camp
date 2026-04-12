---
name: video-analyzer
description: |
  TikTok/YouTube動画を分析してテンプレート化するスキル。
  動画ダウンロード→フレーム抽出→STT→構成分析→テンプレートJSON生成。
  競合分析、人気動画の構成学習に使用。
  「TikTok分析」「YouTube分析」「動画テンプレート化」「競合動画分析」等で発動。
triggers:
  - 動画を分析
  - TikTok分析
  - YouTube動画を分析
  - 競合動画を分析
  - 動画テンプレート化
  - video-analyzer
  - 動画の構成を学習
---

# Video Analyzer

TikTok/YouTube/Instagram動画をダウンロード→分析→テンプレート化する。

## 対応プラットフォーム

- **TikTok** — `https://www.tiktok.com/@user/video/...` / `https://vt.tiktok.com/...`
- **YouTube** — `https://www.youtube.com/watch?v=...` / `https://youtu.be/...`
- **YouTube Shorts** — `https://youtube.com/shorts/...`
- **Instagram Reels** — `https://www.instagram.com/reel/...`
- その他 yt-dlp が対応するプラットフォーム

## クイックスタート

```bash
# TikTok動画を分析
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://www.tiktok.com/@user/video/123456" \
  --output output/templates/

# YouTube動画を分析
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://www.youtube.com/watch?v=XXXXX" \
  --output output/templates/

# YouTube Shortsを分析
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://youtube.com/shorts/XXXXX" \
  --output output/templates/
```

## パイプライン

```
URL → yt-dlp → 動画ファイル（TikTok/YouTube/Instagram等対応）
  → ffmpeg → フレーム抽出 (1fps)
  → Whisper API → STT (テキスト + タイムスタンプ)
  → Vision AI → フレーム分析 (テロップ位置、デザイン、構図)
  → テンプレート JSON (scenes.json互換)
```

## 出力: template.json

```json
{
  "source_url": "https://...",
  "duration": 32.5,
  "resolution": "1080x1920",
  "scenes": [
    {
      "frame_number": 1,
      "timestamp": "0:00-0:03",
      "duration": 3.0,
      "narration": "STTから抽出したテキスト",
      "text_overlay": {
        "text": "画面上のテロップ",
        "position": "center",
        "style": "bold",
        "color": "#FFFFFF",
        "has_stroke": true
      },
      "visual": {
        "shot_type": "close_up | medium | wide | overhead",
        "subject": "人物が商品を持っている",
        "transition_to_next": "cut | fade | swipe"
      },
      "motion_type": "i2v",
      "energy": "high | medium | low"
    }
  ],
  "summary": {
    "total_scenes": 8,
    "avg_scene_duration": 4.1,
    "full_transcript": "...",
    "category": "tutorial",
    "caption_style": "太字白テキスト、黒ストローク、画面中央下",
    "structure": "hook → problem → solution → demo → CTA",
    "pacing": "fast | medium | slow",
    "key_techniques": ["technique1", "technique2"]
  }
}
```

## 使い方

### 1. 単体分析
```bash
python analyze_video.py --url "URL"
```

### 2. バッチ分析（複数URL）
```bash
python analyze_video.py --urls-file urls.txt --output output/templates/
```

### 3. Playbook蓄積（別スキル）
分析結果のtemplate.jsonを `video-playbook` スキルに渡して、タイプ別知見を蓄積：
```bash
python skills/video-playbook/scripts/manage_playbook.py --add -t output/templates/template.json
```

### 4. テンプレートを使って新動画生成
分析結果のtemplate.jsonをstoryboard-generatorに渡して、自社コンテンツでリメイク：
```bash
python generate_storyboard.py --template output/templates/template.json --topic "自社プロダクト名"
```

## 依存
- yt-dlp (`.bin/yt-dlp`)
- ffmpeg (`.bin/ffmpeg`)
- OpenAI Whisper API (STT)
- Gemini Vision API (フレーム分析)

## 環境変数
- `OPENAI_API_KEY` — Whisper STT用
- `GEMINI_API_KEY` — Vision分析用

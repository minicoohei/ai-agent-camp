---
name: video-editor
description: "Video editing skill for TikTok/YouTube. Burns captions with ffmpeg, applies Ken Burns effects, combines scenes, and synthesizes audio. Reads edit instructions from scenes.json and outputs the final video. Also includes Remotion components (for local environments). Triggered by 'Edit video', 'Add captions', 'Create captioned video', etc."
triggers:
  - Edit video
  - Add captions
  - Create captioned video
  - Combine scenes
  - Export video
  - video-editor
  - ffmpeg edit
---

# Video Editor

Generates final video from scenes.json + frame images/video clips.

## Two Execution Modes

### ffmpeg Mode (Sandbox-compatible / Recommended)
No Chromium required. Works in sandboxed environments.

```bash
python skills/video-editor/scripts/compose_video.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --captions \
  --output output/final_tiktok.mp4
```

### Remotion Mode (Local environment)
Requires Chromium + Node.js. More advanced animations.

```bash
npx remotion render TikTokVideo --output=out/tiktok_video.mp4 --root=remotion-editor/src/Root.tsx
```

## ffmpeg Pipeline

### 1. Asset Preparation
```
scenes.json -> Check motion_type for each frame
  i2v        -> Use video/{frame}_i2v.mp4
  ken_burns  -> ffmpeg zoompan filter: image -> video
  static     -> ffmpeg loop: image -> video
  motion_graphics -> ffmpeg: image -> video (future text animation support)
```

### 2. Normalization
Normalize all clips to unified specifications:
- Resolution: 1080x1920 (9:16) or 1920x1080 (16:9)
- FPS: 30
- Codec: h264 / yuv420p
- Landscape i2V video -> Convert to portrait with blurred background

### 3. Caption Burn-in (drawtext)
```bash
ffmpeg -i clip.mp4 -vf "drawtext=text='Text':fontfile=/path/to/NotoSansJP-Bold.otf:\
  fontsize=64:fontcolor=white:borderw=3:bordercolor=black:\
  x=(w-text_w)/2:y=h*0.58" output.mp4
```

Caption specifications:
| Item | TikTok Recommended |
|------|-------------------|
| Font size | 54-76px (5-7% of screen width) |
| Characters/line | Japanese 5-8 chars / English 2-3 words |
| Max lines | 2 |
| Font | Noto Sans JP Bold |
| Color | White + black stroke (3px) + shadow |
| Position | Y: 55-65% (within TikTok safe zone) |

### 4. Concatenation
```bash
ffmpeg -f concat -safe 0 -i concat.txt -c:v libx264 -pix_fmt yuv420p final.mp4
```

### 5. Audio Synthesis (Optional)
```bash
ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac -shortest final_with_audio.mp4
```

## TikTok Safe Zone
```
+---------------------+
|  Avoid top 15%      | <- Username/Follow button
+---------------------+
|   Main content      |
|  +---------------+  |
|  | Captions      |  | <- Y: 55-65%
|  +---------------+  |
+---------------------+
|  Avoid bottom 20%   | <- Like/Comment/Share
+---------------------+
```

## scenes.json Format
```json
{
  "title": "Video title",
  "scenes": [
    {
      "frame_number": 1,
      "timestamp": "0:00-0:02",
      "motion_type": "i2v | ken_burns | static | motion_graphics",
      "narration": "Narration script",
      "text_overlay": {
        "main_text": "Main caption",
        "sub_text": "Sub caption",
        "position": "top | center | bottom",
        "style": "bold | subtitle | minimal"
      }
    }
  ]
}
```

## Dependencies
- ffmpeg (static binary: `.bin/ffmpeg`)
- Python 3.11+ (compose_video.py)
- Noto Sans JP font (for captions)

## Remotion Components (Local Use)
```
remotion-editor/src/
  components/
    Caption.tsx    # TikTok-optimized captions (Japanese line breaks, pop-in animation)
    KenBurns.tsx   # Ken Burns zoom/pan effects
  compositions/
    TikTokVideo.tsx # 9:16 main composition
  Root.tsx         # Entry point
```

## Related Skills
- `storyboard-generator` -- Input assets (frames + scenes.json)
- `content-creator` -- Content planning
- `post-publisher` -- Publishing & distribution

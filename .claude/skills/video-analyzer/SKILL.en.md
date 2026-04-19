---
name: video-analyzer
description: "Skill for analyzing TikTok/YouTube videos and converting them into templates. Downloads video, extracts frames, runs STT, analyzes composition, and generates template JSON. Used for competitor analysis and learning popular video structures. Triggered by 'Analyze video', 'TikTok analysis', 'YouTube analysis', etc."
triggers:
  - Analyze video
  - TikTok analysis
  - Analyze YouTube video
  - Analyze competitor video
  - Convert video to template
  - video-analyzer
  - Learn video composition
---

# Video Analyzer

Downloads, analyzes, and converts TikTok/YouTube/Instagram videos into templates.

## Supported Platforms

- **TikTok** -- `https://www.tiktok.com/@user/video/...` / `https://vt.tiktok.com/...`
- **YouTube** -- `https://www.youtube.com/watch?v=...` / `https://youtu.be/...`
- **YouTube Shorts** -- `https://youtube.com/shorts/...`
- **Instagram Reels** -- `https://www.instagram.com/reel/...`
- Other platforms supported by yt-dlp

## Quick Start

```bash
# Analyze a TikTok video
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://www.tiktok.com/@user/video/123456" \
  --output output/templates/

# Analyze a YouTube video
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://www.youtube.com/watch?v=XXXXX" \
  --output output/templates/

# Analyze YouTube Shorts
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://youtube.com/shorts/XXXXX" \
  --output output/templates/
```

## Pipeline

```
URL -> yt-dlp -> Video file (supports TikTok/YouTube/Instagram, etc.)
  -> ffmpeg -> Frame extraction (1fps)
  -> Whisper API -> STT (text + timestamps)
  -> Vision AI -> Frame analysis (caption position, design, composition)
  -> Template JSON (scenes.json compatible)
```

## Output: template.json

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
      "narration": "Text extracted from STT",
      "text_overlay": {
        "text": "On-screen caption",
        "position": "center",
        "style": "bold",
        "color": "#FFFFFF",
        "has_stroke": true
      },
      "visual": {
        "shot_type": "close_up | medium | wide | overhead",
        "subject": "Person holding a product",
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
    "caption_style": "Bold white text, black stroke, lower center of screen",
    "structure": "hook -> problem -> solution -> demo -> CTA",
    "pacing": "fast | medium | slow",
    "key_techniques": ["technique1", "technique2"]
  }
}
```

## Usage

### 1. Single Analysis
```bash
python analyze_video.py --url "URL"
```

### 2. Batch Analysis (Multiple URLs)
```bash
python analyze_video.py --urls-file urls.txt --output output/templates/
```

### 3. Playbook Accumulation (Separate Skill)
Pass template.json analysis results to the `video-playbook` skill to accumulate insights by type:
```bash
python skills/video-playbook/scripts/manage_playbook.py --add -t output/templates/template.json
```

### 4. Generate New Video from Template
Pass template.json analysis results to storyboard-generator to remake with your own content:
```bash
python generate_storyboard.py --template output/templates/template.json --topic "Your product name"
```

## Dependencies
- yt-dlp (`.bin/yt-dlp`)
- ffmpeg (`.bin/ffmpeg`)
- OpenAI Whisper API (STT)
- Gemini Vision API (Frame analysis)

## Environment Variables
- `OPENAI_API_KEY` -- For Whisper STT
- `GEMINI_API_KEY` -- For Vision analysis

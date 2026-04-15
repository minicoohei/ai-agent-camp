---
name: youtube-clipper
description: "Skill for extracting AI-powered highlights from YouTube/multi-platform videos and generating clips with bilingual subtitles. Triggered by 'Clip from video', 'Extract highlights', 'Subtitled clips', etc."
triggers:
  - Clip from video
  - Extract highlights
  - Create subtitled clips
  - Clip from YouTube
  - Cut best moments from video
  - youtube-clipper
  - clip highlight
---

# /youtube-clipper - Video Highlight Extraction & Clip Generation

## Entry Point

```bash
python skills/youtube-clipper/scripts/main.py --url "https://..."
```

## Overview

Semantically analyzes highlights from YouTube/Vimeo/X videos using AI,
and automatically generates clips with bilingual subtitles.

## Quick Start

```bash
# Extract clips from YouTube video
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=xxxxx"

# Also supports local videos
python skills/youtube-clipper/scripts/clipper.py \
  --file /path/to/local.mp4

# Auto-select mode (auto-extract chapters with score > 0.8)
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://..." --auto-select "score>0.8"
```

## Workflow

```text
Input (URL or local file)
  |
Step 1: Video DL + subtitle retrieval (no subtitles -> Gemini speech recognition)
  |
Step 2: AI chapter analysis (semantic segmentation + summary + score)
  |
Step 3: User selects highlights (number/natural language/score filter)
  |
Step 4: Clip extraction + subtitle translation + burn-in
  |
Output: clips/ + chapters.json + SNS summary
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--url` | - | YouTube/Vimeo/X URL, etc. |
| `--file` | - | Local video file |
| `--output` | `output/clips/` | Output directory |
| `--resolution` | `1080` | Video quality (720/1080/best) |
| `--target-lang` | `ja` | Translation target language |
| `--burn-subtitles` | false | Burn subtitles into video |
| `--auto-select` | - | Auto-selection criteria (`score>0.8`, `all`) |
| `--chapters-only` | false | Chapter analysis only (no clip extraction) |

## Output Structure

```text
output/clips/YYYYMMDD_HHMMSS_{video_id}/
+-- metadata.json
+-- chapters.json
+-- subtitles/
|   +-- original.srt
|   +-- translated_ja.srt
+-- clips/
|   +-- clip_01/
|   |   +-- clip_01.mp4
|   |   +-- clip_01_subtitled.mp4
|   |   +-- original.srt
|   |   +-- translated_ja.srt
|   |   +-- bilingual.srt
|   |   +-- summary.json
|   +-- ...
+-- remotion_input.json
```

## Supported Platforms

YouTube, Vimeo, X/Twitter, Niconico, Dailymotion, etc. (yt-dlp supported range)

## Videos Without Subtitles

When subtitles are not available, audio is extracted with FFmpeg,
and Gemini 3.0 Flash Preview performs transcription + timestamp generation.

## Cost Estimate

| Process | Cost |
|---------|------|
| Video DL | $0 |
| Gemini transcription (10-min video) | ~$0.02 |
| Chapter analysis | ~$0.01 |
| Subtitle translation | ~$0.005 |
| **Total** | **~$0.035/video** |

## Troubleshooting

### YouTube Download Fails

Headless servers may be blocked by YouTube's bot detection.
Configure a cookie file:

```bash
# Method 1: Specify cookie file
export YTDLP_COOKIES=/path/to/cookies.txt    # Mac/Linux/WSL

# Method 2: Get cookies from browser (for local PC)
export YTDLP_COOKIES_FROM_BROWSER=chrome    # Mac/Linux/WSL
```

How to get cookie file:
1. Export YouTube cookies using browser extension "Get cookies.txt LOCALLY" or similar
2. Upload the Netscape-format cookies.txt to server
3. Set the path in `YTDLP_COOKIES` environment variable

### yt-dlp Not Found

```bash
uv pip install yt-dlp
```

### FFmpeg Not Found

```bash
sudo apt-get install -y ffmpeg    # Ubuntu/Debian
# macOS: brew install ffmpeg
# Windows: winget install ffmpeg
```

### deno (JS runtime) Required

yt-dlp's YouTube extractor may require deno JS runtime:

```bash
curl -fsSL https://deno.land/install.sh | sh    # Mac/Linux/WSL
export PATH="$HOME/.deno/bin:$PATH"    # Mac/Linux/WSL
```

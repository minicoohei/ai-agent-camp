---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video/chapter.yaml"
duration: "~40 min"
prerequisites: ["start-15-2"]
level: intermediate
tags: ["video", "clipper", "subtitles", "ai-analysis"]
---

# Lesson 15-3: YouTube Clipper -- Video Highlight Extraction

## Learning Objectives

In this lesson, you will learn how to automatically extract highlights from YouTube (and other platform) videos using AI.

1. Download videos and retrieve subtitles
2. AI-powered semantic chapter segmentation
3. Natural language highlight selection
4. Clip extraction + bilingual subtitle generation
5. Gemini speech recognition for videos without subtitles

---

## Step 1: Verify Environment

First, verify that the required tools are installed.

```bash
yt-dlp --version
ffmpeg -version | head -1
python3 -c "import pysrt; print('pysrt OK')"    # On Windows, replace python3 with python
```

If not installed:
```bash
uv add yt-dlp pysrt
apt-get install ffmpeg    # Ubuntu/Debian
# macOS: brew install ffmpeg
# Windows: winget install ffmpeg or download from https://ffmpeg.org/download.html
```

---

## Step 2: Check Video Information

Prepare a YouTube video URL of your choice.
First, check the video information:

```bash
python skills/youtube-clipper/scripts/downloader.py \
  "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --subs-only
```

Check the output for:
- `subtitles_available`: Manual subtitle languages
- `auto_subtitles_available`: Auto subtitle languages
- `duration`: Video length

---

## Step 3: Chapter Analysis with Clipper

Run chapter analysis only:

```bash
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --chapters-only
```

The AI semantically segments the video into chapters, assigning a title, summary, and highlight_score to each.

---

## Step 4: Extract Highlight Clips

Extract chapters with high scores as clips:

```bash
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --auto-select "score>0.7" \
  --burn-subtitles
```

The following are generated in the `output/clips/` directory:
- MP4 for each clip
- Original subtitles + Japanese translation subtitles
- Bilingual SRT
- Social media post summary (JSON)

---

## Step 5: Transcription for Videos Without Subtitles (Advanced)

Even videos without subtitles can be handled with Gemini speech recognition:

```bash
# Try with a local video file
python skills/youtube-clipper/scripts/clipper.py \
  --file /path/to/video_without_subs.mp4
```

Internally, FFmpeg extracts audio -> Gemini 3.0 Flash Preview performs transcription.

---

## Exercises

1. **Basic**: Choose a YouTube video (5-15 minutes) and extract 3 or more clips
2. **Intermediate**: Burn bilingual subtitles (English-Japanese) onto clips from an English video
3. **Advanced**: Try Gemini speech recognition on a video without subtitles and check the accuracy

---

## Next Steps

In Lesson 15-4, you will learn how to convert extracted clips into social media marketing materials using Remotion.

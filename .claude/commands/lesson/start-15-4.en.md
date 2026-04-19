---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video/chapter.yaml"
duration: "~45 min"
prerequisites: ["start-15-3"]
level: intermediate
tags: ["video", "remotion", "marketing", "sns"]
---

# Lesson 15-4: Clipper x Remotion -- Auto-Generate Marketing Materials

## Learning Objectives

Learn how to convert clips extracted in Lesson 15-3 into social media marketing materials using Remotion.

1. Basic Remotion concepts (React + video = programmable video)
2. Understanding templates (ShortClip, QuoteClip, SummaryVideo)
3. Converting clips to social media post videos
4. Simultaneous multi-format output
5. CursorBootcamp brand customization

---

## What is Remotion?

Remotion is a framework for **creating programmable videos with React**.

- Define video layout with HTML and CSS
- Control animations with React components
- Local rendering with FFmpeg (no API required, $0 cost)
- Once a template is created, mass-produce by just changing the data

---

## Step 1: Run the Integrated Pipeline

Combine with Lesson 15-3's Clipper for end-to-end execution:

```bash
uv run python tools/ugc/clipper_marketing_pipeline.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --auto-select "score>0.8" \
  --batch-render short,quote
```

This performs:
1. Video DL -> AI analysis -> highlight extraction
2. Render each clip as "short (9:16)" and "quote (16:9)"
3. Auto-generate social media post drafts (text + hashtags)

---

## Step 2: Understand Template Types

List available templates:

```bash
uv run python tools/ugc/remotion_render.py --list-templates
```

| Template | Size | Use case |
|----------|------|----------|
| `short` | 1080x1920 (9:16) | TikTok / Reels / Shorts |
| `quote` | 1920x1080 (16:9) | Twitter/X / LinkedIn |
| `summary` | 1920x1080 (16:9) | YouTube / Blog |
| `blog` | 1920x1080 (16:9) | Blog embed |
| `training` | 1920x1080 (16:9) | Training materials |
| `square` | 1080x1080 (1:1) | Instagram Feed |

---

## Step 3: Individual Rendering

Render a specific clip with a specific template:

```bash
# Specify the remotion_input.json generated in Lesson 15-3
uv run python tools/ugc/remotion_render.py \
  --input output/clips/SESSION_DIR/remotion_input.json \
  --template short \
  --clip-id clip_01
```

---

## Step 4: Batch Rendering

Generate all formats from a single clip at once:

```bash
uv run python tools/ugc/remotion_render.py \
  --input output/clips/SESSION_DIR/remotion_input.json \
  --batch short,quote,summary,square
```

---

## Step 5: Review Social Media Post Drafts

Check the `post_drafts.json` generated after pipeline execution:

```bash
cat output/clips/SESSION_DIR/post_drafts.json | python3 -m json.tool
```

It contains text, hashtags, and video paths for each platform.

---

## Exercises

1. **Basic**: Select 3 highlights from a video of your choice and generate short videos (9:16)
2. **Intermediate**: Generate 3 formats (short, quote, square) simultaneously from the same clips
3. **Advanced**: Based on the generated post_drafts.json, finalize actual social media post text

---

## Cost Reference

| Process | Cost |
|---------|------|
| Clipper (DL + analysis + translation) | ~$0.035/video |
| Remotion rendering | $0 (local) |
| **Total** | **~$0.035/video** |

---

## Summary

- YouTube Clipper auto-detects the "best parts" of a video with AI
- Remotion pours them into templates -> mass-produce social media materials
- Generate materials for multiple platforms simultaneously from a single video
- Cost is nearly zero (Gemini API ~$0.035 + local rendering)

---

## Deliverables Preview

### Expected output
```text
output/ugc/
  *.mp4           (video files)
  metadata.json   (metadata)
  thumbnails/     (thumbnails)
```

### Verification commands
```bash
# List and size of output files
ls -lh output/ugc/

# Check metadata
cat output/ugc/*metadata*.json 2>/dev/null | head -20

# Play video (macOS: open / Linux: xdg-open)
open output/ugc/*.mp4
```

---

## Next Steps

This completes Module 15 (Video Production).

In Codex, you can typically choose from options in the chat.

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Open in new window (/start-15-5)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection guide (example)**:
- next_auto -> /next_lesson
- next_window -> Open /start-15-5 in a new window
- finish -> End

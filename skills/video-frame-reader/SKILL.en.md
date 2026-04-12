---
name: video-frame-reader
description: "Skill for extracting keyframes from video files, deduplicating and optimizing them, then analyzing their content. Triggered by 'Show me the video contents', 'Extract keyframes', 'Analyze this video', etc."
triggers:
  - Show me the video contents
  - Extract keyframes
  - Analyze this video
  - Check the video
  - View screen recording
  - video-frame-reader
  - keyframe extraction
---

# Video Frame Reader

Extract keyframes from video, present token cost, then analyze.

## Requirements

- ffmpeg (for frame extraction)
- Python 3 + Pillow + numpy

## Workflow

### 1. Capture User Intent

Clearly understand why the user wants the video analyzed:
- Example: "The screen transition behavior looks wrong"
- Example: "I want to check the response after button click"
- Example: "Help me identify performance issues"

This intent becomes important context for the analysis.

### 2. Create venv (First Time Only)

```bash
python3 -m venv skills/video-frame-reader/scripts/venv
source skills/video-frame-reader/scripts/venv/bin/activate    # Mac/Linux
# Windows: skills\video-frame-reader\scripts\venv\Scripts\activate
pip install Pillow numpy --quiet
```

### 3. Extract Keyframes

```bash
source skills/video-frame-reader/scripts/venv/bin/activate    # Mac/Linux
# Windows: skills\video-frame-reader\scripts\venv\Scripts\activate
python3 skills/video-frame-reader/scripts/extract_keyframes.py "<video_path>"
```

Output example (JSON):
```json
{
  "keyframe_count": 52,
  "image_size": "266x576",
  "total_tokens": 10400,
  "cost_usd_opus": 0.156,
  "cost_usd_sonnet": 0.031,
  "cost_usd_haiku": 0.0104,
  "files": ["/.../key_0001.jpg", ...]
}
```

### 4. Present Cost

After extraction, present the following to the user:

```
Keyframe extraction complete:
- Frames extracted: {keyframe_count}
- Image size: {image_size}
- Estimated tokens: {total_tokens}
- Cost estimate: Haiku ${cost_usd_haiku} / Sonnet ${cost_usd_sonnet} / Opus ${cost_usd_opus}

Proceed with frame analysis?
```

### 5. Invoke Subagent After Approval

After user approval, invoke subagent using Task tool:

```
Task(
  subagent_type="general-purpose",
  model="haiku",
  description="Frame analysis",
  prompt="""
[User Intent]
{Intent captured in Step 1}

[Frame Image Files]
{List of paths from files array}

Analyze the above frame images and identify issues/behaviors according to the user's intent.
"""
)
```

Benefits of this approach:
- User intent is included in analysis context
- Subagent can focus on intent-specific efficient analysis
- Processed in independent context for better token efficiency

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-t, --threshold` | 0.85 | Similarity threshold (higher = more frames kept) |
| `-q, --quality` | 30 | JPEG quality (1-100) |
| `-s, --scale` | 0.3 | Resize scale |
| `-o, --output` | `<video_name>_keyframes/` | Output directory |

### Token Reduction Example

```bash
# More aggressive reduction (lower threshold, quality, and size)
python3 extract_keyframes.py video.mp4 -t 0.75 -q 20 -s 0.2
```

## Overview

A skill for automatically extracting keyframes from video files, deduplicating and optimizing them, then analyzing their content. Presents token cost upfront and executes analysis via subagent after user approval.

## Troubleshooting

| Error | Solution |
|-------|---------|
| ffmpeg not found | `brew install ffmpeg` (Mac) or `apt install ffmpeg` (Linux) to install |
| No keyframes extracted | Lower `--threshold` (e.g., 0.75) to extract more frames |

## Success Criteria

- [ ] Keyframe images are saved in the output directory
- [ ] Token cost estimate is displayed in JSON format
- [ ] Results aligned with the user's analysis intent are returned

## Usage

See the "Workflow" section above. Basic examples:

```bash
# Extract keyframes
python3 skills/video-frame-reader/scripts/extract_keyframes.py "video.mp4"

# With token reduction options
python3 skills/video-frame-reader/scripts/extract_keyframes.py "video.mp4" -t 0.75 -q 20 -s 0.2
```

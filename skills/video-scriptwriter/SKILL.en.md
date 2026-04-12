---
name: video-scriptwriter
description: "Automatic video script generation skill for TikTok/YouTube. Specify a theme + format + duration to generate scenes.json (compatible with storyboard/audio/editor). Automatically references Playbook insights for optimal structure. Triggered by 'Create a script', 'Generate script', 'Create a plan', etc."
triggers:
  - Create a video script
  - Generate script
  - Create a video plan
  - TikTok script
  - Generate scenes.json
  - video-scriptwriter
  - Video structure proposal
---

# Video Scriptwriter

Automatically generates theme -> plan -> scenes.json.

## 6 Formats

| Format | Description | Mass Production Suitability |
|--------|-------------|---------------------------|
| `split_screen_teaching` | Top half text+TTS / bottom half gameplay footage | 5/5 |
| `ranking_list` | Ranking TOP 5 format | 4/5 |
| `reddit_story` | Reddit/2ch read-aloud + background video | 5/5 |
| `dark_facts` | "Scary things you didn't know about X" trivia format | 4/5 |
| `standard_teaching` | Standard educational/explanatory format | 4/5 |
| `product_intro` | Product introduction/review format | 3/5 |

## Quick Start

```bash
# Basic
python3 skills/video-scriptwriter/scripts/generate_script.py \
  --topic "5 ways to improve sleep quality" \
  --format ranking_list \
  --duration 30s

# Split-screen educational
python3 skills/video-scriptwriter/scripts/generate_script.py \
  --topic "What is quantum computing" \
  --format split_screen_teaching \
  --duration 30s \
  --hook shocking

# List formats
python3 skills/video-scriptwriter/scripts/generate_script.py --list-formats
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--topic` | (required) | Video topic/theme |
| `--format` | standard_teaching | Format |
| `--duration` | 30s | Video duration (15s/30s/60s) |
| `--language` | ja | Language |
| `--hook` | question | Hook style (question/shocking/pov/wait/ranking/dark/nobody/comparison) |
| `--output` | auto | Output directory |
| `--instructions` | - | Additional instruction text |

## Output: scenes.json

Compatible format with storyboard-generator / video-audio / video-editor:

```json
{
  "title": "Video title",
  "format": "split_screen_teaching",
  "scenes": [
    {
      "frame_number": 1,
      "timestamp": "0:00-0:03",
      "duration": 3.0,
      "scene_type": "hook",
      "narration": "Narration",
      "text_overlay": { "main_text": "Caption" },
      "visual_prompt": "English prompt for image gen...",
      "motion_type": "i2v"
    }
  ],
  "metadata": {
    "target_audience": "...",
    "estimated_retention_hooks": ["hook technique", "progressive information disclosure"]
  }
}
```

## Pipeline Integration

```
scriptwriter (theme -> scenes.json)
  |
storyboard-generator (scenes.json -> AI images)
  |
video-audio (scenes.json -> TTS audio)
  |
video-editor (images + audio -> final video)
```

## Playbook Integration

Automatically references insights accumulated in `video-playbook`:
- Average scene duration, pacing
- Structure patterns
- Caption style
- Effective techniques

## Dependencies
- Gemini API (`GEMINI_API_KEY`)
- video-playbook (optional, for insight reference)

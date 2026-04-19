---
name: video-playbook
description: "Skill for accumulating and utilizing insights in type-specific Playbooks from video analysis results. Uses template.json output from video-analyzer as input. Triggered by 'Update Playbook', 'Type-specific video insights', 'Check Playbook', etc."
triggers:
  - Update Playbook
  - Type-specific video insights
  - Check Playbook
  - Video production guidelines
  - Accumulate analysis results
  - video-playbook
---

# Video Playbook

Determines video type from analysis results (template.json) and accumulates production insights in type-specific Playbooks.

## Video Types (7 types)

| Type | Description |
|------|-------------|
| `intro` | Introduction/Review (product intro, service intro, person intro) |
| `teaching` | Teaching/Explanation (how-to, knowledge sharing, tips, know-how) |
| `template` | Template/Trend (trending formats, sound sync, challenges) |
| `meme` | Meme/Comedy (punchline-focused, humor, parody) |
| `dance` | Dance/Performance (choreography, BPM sync, covers) |
| `mv` | MV/Cinematic (music video, effects-heavy, cinematic production) |
| `clip` | Clip/Highlight (long-to-short, best moments, stream clips) |

## Quick Start

```bash
# Add insights to Playbook after analyzing with video-analyzer
python skills/video-playbook/scripts/manage_playbook.py \
  --add -t output/templates/video_001/template.json

# List Playbooks by type
python skills/video-playbook/scripts/manage_playbook.py --list

# Show Playbook for specific type
python skills/video-playbook/scripts/manage_playbook.py --show teaching

# Export in Markdown format
python skills/video-playbook/scripts/manage_playbook.py --export teaching
```

## Workflow

```
1. Analyze video with video-analyzer -> template.json
2. manage_playbook.py --add -t template.json
   -> Auto-detect video type
   -> Extract insights on timing, structure, captions, etc.
   -> Add to type-specific playbook JSON
   -> Auto-update aggregated data
3. manage_playbook.py --show TYPE to review accumulated insights
4. Reference Playbook when creating new videos
```

## How Playbook Accumulation Works

The following insights are extracted from each analysis result and accumulated by type:

- **Timing**: Average scene duration, pacing, hook length
- **Structure**: Composition patterns (hook->problem->solution, etc.), techniques used
- **Captions**: Style, placement, color, density
- **Visual**: Shot types, variety, resolution
- **Audio**: Narration presence, density, characters per scene

As more samples accumulate, the aggregated data becomes more precise, and production guidelines for "how to make this type of video" are automatically generated.

## Leveraging for Content Creation

When creating new videos using Playbook insights:

1. Use `--show TYPE` to review insights for the target type
2. Use `--export TYPE` to generate a Markdown summary
3. Include the summary in LLM prompts to generate scripts and structure proposals
4. Reflect Playbook insights in storyboard-generator

## Data Storage Location

```
skills/video-playbook/playbooks/
  +-- teaching.json    # Teaching insights
  +-- intro.json       # Introduction insights
  +-- meme.json        # Meme insights
  +-- ...
```

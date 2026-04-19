---
name: storyboard-generator
description: "Skill for automatically generating storyboards for AI UGC videos. Guarantees character consistency by generating a single sheet and then cropping individual frames. Triggered by requests like 'Create a storyboard', 'Generate storyboard', 'Create UGC video flow', etc."
triggers:
  - Create a storyboard
  - Generate storyboard
  - Create UGC video flow
  - Video storyboard
  - Create scene composition
  - storyboard-generator
  - storyboard
---

# Storyboard Generator (UGC Storyboard Generation)

A storyboard creation tool for AI UGC video production. **Generates all frames as a single sheet image, then crops them** to guarantee character consistency.

## Generation Modes

### Sheet Mode (Default / Recommended)
- Generates all frames as **a single storyboard sheet**
- One API call for all frames -> **Excellent character consistency**
- Grid is cropped into individual frames after generation
- Superior in speed, cost, and consistency

### Individual Mode (Legacy)
- Generates one frame at a time
- Attempts to maintain consistency via character reference images, but has limitations
- For fallback use

## Features

### 1. Character Design
- Generate reference images from detailed character prompts
- Use existing character images as reference
- In sheet mode, reference images are passed during sheet generation to enhance consistency

### 2. Storyboard Generation
- Automatically generates 4/8/16-panel scene descriptions from scenarios (Gemini Flash)
- Sheet mode: Generates as a single grid image, then auto-crops
- Individual mode: Generates one frame at a time, then composites into grid
- Auto-resize (default 540px width, JPG compression)

### 3. Narration & Text Overlay Instructions
- Automatically generates narration scripts (Japanese) for each frame
- Specifies text overlay content, position, and style
- Outputs narration and text_overlay fields in scenes.json

### 4. Automatic Motion Type Detection (motion_type)
- **static**: Text-focused -> Keep as still image
- **ken_burns**: Landscape/static composition -> Zoom/pan is sufficient (no i2V needed)
- **motion_graphics**: UI transitions/text animation -> Remotion is sufficient (no i2V needed)
- **i2v**: Character movement/facial expressions -> Requires i2V conversion (e.g., fal.ai wan-i2v)
- Cost optimization: Only scenes that truly need i2V are designated as i2V

### 5. Video Generation Integration
- Select any StartFrame/EndFrame from the storyboard
- Image-to-Video generation via fal.ai (wan-i2v)
- Camera motion specification supported

## Usage

```bash
# Recommended: Sheet mode (generate single sheet -> crop)
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "UGC video explaining how to use the app" \
    --character "Japanese woman in her 20s, casual clothing, bright expression" \
    --aspect-ratio 9:16 \
    --num-frames 8 \
    --mode sheet \
    --session "app_promo"

# Individual mode (fallback)
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "Product review video" \
    --character "..." \
    --mode individual \
    --session "product_review"

# Using existing character image
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "..." \
    --character-image "path/to/character.png" \
    --mode sheet \
    --session "with_ref"

# Video generation (from existing storyboard)
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --storyboard-dir "output/storyboard/YYYYMMDD_session" \
    --start-frame 1 \
    --end-frame 8 \
    --video-duration 10
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --scenario | Yes | - | Video scenario/topic |
| --character | No* | - | Detailed character prompt |
| --character-image | No* | - | Path to existing character reference image |
| --mode | No | sheet | Generation mode: sheet / individual |
| --aspect-ratio | No | 9:16 | Aspect ratio (9:16, 16:9, 1:1, 4:3, 3:4) |
| --num-frames | No | 16 | Number of frames (4, 8, 16) |
| --output-width | No | 540 | Max output image width in px (0 for unlimited) |
| --layout | No | auto | Grid layout (individual mode only) |
| --session | No | - | Session name (output folder name) |
| --style | No | modern_clean | Visual style |
| --start-frame | No | - | Start frame number for video generation |
| --end-frame | No | - | End frame number for video generation |
| --video-duration | No | 5 | Video duration (seconds): 5 or 10 |
| --camera-motion | No | - | Camera motion |

*Either --character or --character-image is required

## Output Structure

```
output/storyboard/
+-- YYYYMMDD_HHMMSS_session/
    +-- character_reference.png    # Character reference image
    +-- storyboard_sheet.png       # Original sheet (sheet mode)
    +-- storyboard_grid.jpg        # Resized grid
    +-- frames/
    |   +-- frame_01.jpg           # Cropped frames (JPG compressed)
    |   +-- frame_02.jpg
    |   +-- ...
    +-- scenes.json                # Scene info (narration, text_overlay, motion_type)
    +-- video/                     # When generating video
        +-- output.mp4
```

## Performance Comparison

| | Sheet (Recommended) | Individual |
|---|---|---|
| API calls | 3 | N+2 |
| Generation time (8 frames) | ~1 min | ~5 min |
| File size | ~325KB | ~800KB |
| Character consistency | Excellent | Fair |

## Visual Styles

- `modern_clean` - Modern & clean (default)
- `animal_crossing` - Animal Crossing style
- `vibrant_ugc` - Vivid UGC
- `anime` - Anime style

## Requirements

- `GEMINI_API_KEY`: For Gemini Flash/Image Generation
- `FAL_KEY`: For i2V video generation (only when generating video)
- Python packages: google-genai, Pillow, python-dotenv

## Environment Setup

```bash
export GEMINI_API_KEY="your-key"    # Mac/Linux/WSL
export PYTHONPATH="/path/to/.pip/local/local/lib/python3.11/dist-packages:$PYTHONPATH"    # Mac/Linux/WSL
```

## Trigger Phrases

- "Create a storyboard"
- "Generate storyboard"
- "UGC video storyboard"
- "Create video flow"

## Overview

A skill for automatically generating storyboards for AI UGC video production. Guarantees character consistency by generating all frames as a single sheet image and then cropping. Also supports narration scripts and automatic motion type detection.

## Troubleshooting

| Error | Solution |
|-------|---------|
| API key not found | Set `GEMINI_API_KEY` as an environment variable |
| Character consistency issues | Use `--mode sheet` (recommended). Individual mode has lower consistency |
| FAL_KEY not set | Only required for video generation (i2V). Not needed for storyboard generation alone |

## Success Criteria

- [ ] Storyboard images for the specified number of frames are generated in `output/storyboard/`
- [ ] `scenes.json` contains narration and motion_type
- [ ] Character appearance is consistent across frames

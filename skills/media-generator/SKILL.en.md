---
name: media-generator
description: "Sub-agent for generating and editing banners, diagrams, slides, and images. Uses Gemini Image Generation API to generate various media. Triggered by requests like 'create a banner', 'generate a diagram', 'create slides', 'generate an image', etc."
triggers:
  - create a banner
  - banner generation
  - create a diagram
  - infographic
  - diagram
  - generate slides
  - generate an image
  - edit an image
  - image for X
  - for Instagram
  - for Facebook
---

# Media Generator Sub-agent

Sub-agent that executes banner/diagram/slide/image generation and editing in a dedicated context.

## Purpose

Separates media generation processing from the main agent's context to:
- Optimize processing that includes multiple reference images
- Apply platform-specific presets
- Return only the generated file path information

## Feature List

| Feature | Script | Description |
|---------|--------|-------------|
| Banner generation | `banner_creator.py` | SNS/ad banner generation |
| Diagram generation | `generate_diagram.py` | Infographic/diagram generation |
| Slide generation | `generate_slide.py` | Lecture slide image generation |
| General image generation | `nanobanana.py` | Text-to-image, image editing |

## 1. Banner Generation (`tools/banner_creator.py`)

### Platform Presets

| Preset | Size | Aspect Ratio | Use Case |
|--------|------|--------------|----------|
| `x_post` | 1200x675 | 16:9 | X timeline post |
| `x_card` | 800x418 | 16:9 | X link card |
| `facebook` | 1200x630 | 16:9 | Facebook link post |
| `facebook_story` | 1080x1920 | 9:16 | Facebook Stories |
| `instagram_feed` | 1080x1080 | 1:1 | Instagram feed |
| `instagram_story` | 1080x1920 | 9:16 | Instagram Stories |
| `prtimes` | 1200x630 | 16:9 | PRTimes press release |
| `youtube_thumbnail` | 1280x720 | 16:9 | YouTube thumbnail |
| `line` | 1200x628 | 16:9 | LINE official account |
| `web_banner` | 1200x628 | 16:9 | Web ad banner |

### Usage

```bash
# Generate X banner
uv run python tools/banner_creator.py \
  --platform x_post \
  --topic "New service release announcement" \
  --tone professional \
  --output-dir docs/generated/banners

# Use reference images
uv run python tools/banner_creator.py \
  --platform instagram_feed \
  --topic "Summer campaign" \
  --reference-images image1.png image2.png \
  --output-dir docs/generated/banners

# Generate with copy text
uv run python tools/banner_creator.py \
  --platform prtimes \
  --topic "For press release" \
  --with-copy \
  --output-dir docs/generated/banners
```

## 2. Diagram/Infographic Generation (`tools/generate_diagram.py`)

### Styles

| Style | Description |
|-------|-------------|
| `colorful_infographic` | Bright colors, icons, readable layout |
| `sketch` | Hand-drawn style, pencil/charcoal texture |
| `photorealistic` | Photo-like realistic quality |
| `minimalist` | Simple, whitespace-focused, limited colors |
| `claymation` | 3D clay style, soft lighting |
| `pixel_art` | Retro game style, blocky design |

### Usage

```bash
# Generate diagram from topic
uv run python tools/generate_diagram.py \
  --topic "Marketing funnel" \
  --style colorful_infographic \
  --aspect-ratio 16:9 \
  --output-dir reports/visualizations

# Infographic from long text
uv run python tools/generate_diagram.py \
  --topic "$(cat article.txt)" \
  --style minimalist \
  --output-dir reports/visualizations
```

## 3. General Image Generation/Editing (`tools/nanobanana.py`)

### Usage

```bash
# Text-to-image generation
uv run python tools/nanobanana.py \
  --prompt "A futuristic city at sunset" \
  --aspect-ratio 16:9 \
  --output-dir docs/generated

# Image editing (reference image + instructions)
uv run python tools/nanobanana.py \
  --prompt "Make the background blue" \
  --reference reference.png \
  --output-dir docs/generated

# Using multiple reference images
uv run python tools/nanobanana.py \
  --prompt "Combine these styles" \
  --reference image1.png image2.png \
  --output-dir docs/generated
```

### Aspect Ratios

| Aspect Ratio | Use Case |
|--------------|----------|
| `1:1` | Instagram, profile images |
| `4:3` | General landscape |
| `3:4` | General portrait |
| `16:9` | YouTube, presentations |
| `9:16` | Stories, Reels |
| `21:9` | Ultra-wide |

## Sub-agent Call Pattern

The main agent calls this sub-agent using the following pattern:

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Banner generation",
    prompt="""
    Read and execute this skill: skills/media-generator/SKILL.md
    
    Task: {user instructions}
    Platform: {x_post / instagram_feed / etc.}
    Topic: {content to generate}
    
    Return the path of the generated image.
    """
)
```

## Return Format

Processing results are returned in the following format:

```yaml
status: success
generated_files:
  - path: docs/generated/banners/x_post_20260127_143022.png
    platform: x_post
    size: 1200x675
    aspect_ratio: 16:9
copy_text: |
  [New Service Release]
  An AI-powered business efficiency tool has arrived!
  #AI #BusinessEfficiency
```

## Dependencies

```txt
google-generativeai>=0.3.0
Pillow>=9.0.0
python-dotenv>=1.0.0
```

## Environment Variables

```bash
# Required
GEMINI_API_KEY=your_api_key
# or
GOOGLE_API_KEY=your_api_key
```

## Notes

- Generated images are automatically saved under `docs/generated/`
- Specifying a session name organizes files into subfolders
- Explicitly instruct when including Japanese text
- Up to 5 reference images

---
name: diagram-generator
description: "Skill for generating diagrams, infographics, and visual illustrations from text using the Gemini Image Generation API. Triggered by requests like 'create a diagram,' 'generate an infographic,' 'illustrate this process,' etc."
triggers:
  - diagram-generator
  - 図を作って
  - ダイアグラム生成
  - インフォグラフィック
  - 図解して
  - diagram
  - フローチャート作成
---

# Diagram Generator

Generate visual diagrams and infographics from text descriptions.

## Workflow

1. Provide topic/text to visualize
2. Gemini Flash optimizes the image generation prompt
3. Gemini Image generates the visualization
4. Outputs PNG image

## Usage

```bash
python scripts/generate_diagram.py "{topic}" --style "{style}" --aspect_ratio "{ratio}"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| topic | Yes | - | Topic or text to visualize |
| --style | No | colorful_infographic | Visual style |
| --aspect_ratio | No | 16:9 | Output ratio |
| --output | No | auto | Output path |

## Styles

| Style | Description |
|-------|-------------|
| colorful_infographic | Vibrant icons, organized layout (default) |
| sketch | Hand-drawn, pencil texture |
| minimalist | Clean, simple geometric shapes |
| photorealistic | High-quality photo look |
| claymation | 3D clay texture, playful |
| pixel_art | Retro game style |

## Aspect Ratios

`16:9`, `1:1`, `4:3`, `3:4`, `9:16`, `21:9`

## Examples

```bash
# Basic diagram
python scripts/generate_diagram.py "How photosynthesis works"

# Minimalist style
python scripts/generate_diagram.py "Machine learning pipeline" --style minimalist

# Portrait format
python scripts/generate_diagram.py "Company org chart" --aspect_ratio 9:16

# From long text
python scripts/generate_diagram.py "Gemini is a multimodal AI model that can understand text, images, and code..." --style colorful_infographic
```

## Requirements

- GEMINI_API_KEY or GOOGLE_API_KEY in environment
- Python packages: google-genai, Pillow, python-dotenv

## Overview

A skill that automatically generates infographics, diagrams, and visuals from text topics or descriptions using the Gemini Image Generation API. Ideal for visual aids in presentations and documentation.

## Troubleshooting

| Error | Solution |
|-------|----------|
| API key not found | Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` in environment variables |
| Image generation returned empty | The topic may be too short. Provide a more detailed description |

## Success Criteria

- [ ] PNG image generated with the correct aspect ratio
- [ ] Generated image visually represents the topic content
- [ ] Completed without errors

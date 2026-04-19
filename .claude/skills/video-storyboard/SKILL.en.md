---
name: video-storyboard
description: "Skill for creating storyboards (visual boards) from video scripts using AI image generation. Triggered by 'Create a storyboard', 'Generate storyboard', 'Create images from script', etc."
triggers:
  - Create a storyboard
  - Generate storyboard
  - Create images from script
  - Generate video frame images
  - Create scene images
  - video-storyboard
  - storyboard
---

## Trigger Words
"Storyboard", "Visual board", "Generate images from video script", "Video planning"

# Video Storyboard Skill

## Purpose
Convert video scripts into visual storyboards with AI-generated images.

## Prerequisites
- Gemini API key setup (set environment variable `GEMINI_API_KEY` or pass as `$KEY`)
- Output directory `frames/` exists in the project (created automatically if not present)

## Usage
Input: A script from `video-scriptwriter` with scene descriptions.

## Process
1. Extract visual descriptions from each scene
2. Generate image prompts (English, detailed, cinematic)
3. Call Gemini API with `responseModalities: ["TEXT", "IMAGE"]`
4. Save frames as `scene_XX.png`

## Image Prompt Guidelines
- Describe composition, lighting, color palette
- Specify style: "cinematic", "anime", "flat illustration", etc.
- Include camera angle and framing
- Keep consistent visual style across scenes

## API
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Generate an image: ..."}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}'
```

## Output
- `frames/scene_01.png` ... `scene_NN.png`
- Each image: 1024x1024 or native aspect ratio

## Integration
Output feeds into fal.ai i2V for video clip generation.

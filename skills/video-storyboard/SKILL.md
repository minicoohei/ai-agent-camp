---
name: video-storyboard
description: "動画スクリプトからAI画像生成で絵コンテ（ストーリーボード）を作成するスキル。 「絵コンテを作って」「ストーリーボード生成」「スクリプトから画像を作成」等で発動。"
triggers:
  - 絵コンテを作って
  - ストーリーボード生成
  - スクリプトから画像を作成
  - 動画のフレーム画像を生成
  - シーン画像を作って
  - video-storyboard
  - storyboard
---

## トリガーワード
「絵コンテ」「ストーリーボード」「動画スクリプトから画像生成」「動画企画」

# Video Storyboard Skill

## Purpose
Convert video scripts into visual storyboards with AI-generated images.

## 前提条件
- Gemini API キーの設定（環境変数 `GEMINI_API_KEY` を設定するか、`$KEY` として渡す）
- 出力先ディレクトリ `frames/` がプロジェクト内に存在すること（なければ自動作成）

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

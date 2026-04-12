---
name: diagram-generator
description: "Gemini Image Generation API でテキストから図解・インフォグラフィック・ダイアグラムを生成するスキル。 「図を作って」「インフォグラフィック生成」「プロセスを図解して」等のリクエストで発動。"
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

テキストのトピックや説明文から、Gemini Image Generation APIを使ってインフォグラフィック・図解・ビジュアルを自動生成するスキルです。プレゼン資料やドキュメントの視覚的補助に最適。

## Troubleshooting

| エラー | 解決方法 |
|--------|---------|
| API key not found | `GEMINI_API_KEY` または `GOOGLE_API_KEY` を環境変数に設定 |
| Image generation returned empty | トピックが短すぎる可能性。より詳しい説明を指定 |

## Success Criteria

- [ ] PNG画像が正しいアスペクト比で生成されている
- [ ] 生成画像がトピックの内容を視覚的に表現している
- [ ] エラーなく完了している

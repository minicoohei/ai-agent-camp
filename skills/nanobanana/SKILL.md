---
name: nanobanana
description: |
  Gemini画像生成APIでテキストから画像生成、既存画像の編集を行うスキル。
  「画像を生成して」「イラストを作って」「写真を編集して」等のリクエストで発動。
triggers:
  - 画像を生成して
  - イラストを作って
  - 写真を編集して
  - 画像を作成
  - nanobanana
  - image generation
  - ロゴをデザインして
---

# Nano Banana Pro - Image Generation & Editing

Generate or edit images using Gemini Image Generation API.

## Modes

1. **Text-to-Image**: Generate new images from text prompts
2. **Image Editing**: Edit existing images with instructions

## Usage

```bash
# Text-to-image
python scripts/nanobanana.py "{prompt}" --aspect-ratio "{ratio}"

# Image editing
python scripts/nanobanana.py "{prompt}" --input "{image_path}"

# Multiple reference images
python scripts/nanobanana.py "{prompt}" --input "{image1}" --input "{image2}"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| prompt | Yes | - | Generation/edit instruction |
| --input, -i | No | - | Input image(s) for editing |
| --output, -o | No | auto | Output path |
| --aspect-ratio, -ar | No | 16:9 | Output ratio |
| --session, -s | No | - | Session name for organizing output |
| --force-ar | No | false | Force aspect ratio in edit mode |

## Aspect Ratios

`1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9`

## Examples

```bash
# Generate landscape
python scripts/nanobanana.py "Mt. Fuji at sunset, photorealistic"

# Edit image
python scripts/nanobanana.py "Remove the background" --input photo.jpg

# Combine images
python scripts/nanobanana.py "Merge these into one composition" --input img1.png --input img2.png

# With session organization
python scripts/nanobanana.py "Company logo design" --session "brand_assets" --aspect-ratio 1:1
```

## Requirements

- GEMINI_API_KEY or GOOGLE_API_KEY in environment
- Python packages: google-genai, Pillow, python-dotenv

## Overview

Gemini Image Generation APIを使って、テキストプロンプトからの画像生成や、既存画像の編集を行う汎用画像生成スキルです。複数参照画像の合成にも対応。

## Troubleshooting

| エラー | 解決方法 |
|--------|---------|
| API key not found | `GEMINI_API_KEY` または `GOOGLE_API_KEY` を環境変数に設定 |
| Input image not found | `--input` に正しいファイルパスを指定。相対パスは実行ディレクトリ基準 |

## Success Criteria

- [ ] 指定アスペクト比で画像が生成されている
- [ ] 編集モード時に元画像への変更が正しく反映されている
- [ ] エラーなく完了している

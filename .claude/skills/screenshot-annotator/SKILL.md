---
name: screenshot-annotator
description: |
  スクリーンショットに赤枠・矢印・吹き出し等の注釈を自動追加するスキル。
  「スクショに注釈を付けて」「画面に矢印を追加」「マニュアル用の注釈」等のリクエストで発動。
triggers:
  - スクショに注釈を付けて
  - 画面に矢印を追加
  - マニュアル用の注釈
  - 赤枠を付けて
  - 吹き出しを追加
  - screenshot-annotator
  - annotate screenshot
---

# Screenshot Annotator

Add annotations to screenshots without modifying the original image. Annotations are overlaid on top.

## Workflow

1. Analyze the screenshot to identify the target element
2. Generate annotation overlay using Gemini Vision API
3. Output annotated image as a separate file

## Usage

```bash
python scripts/annotate.py "{image_path}" "{instruction}" --style "{style}" --text "{label}" --output "{output_path}"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| image_path | Yes | - | Path to screenshot |
| instruction | Yes | - | What to annotate (e.g., "the Login button") |
| --style | No | red_box | Annotation style |
| --text | No | - | Text label to add |
| --output | No | auto | Output path |

## Styles

| Style | Description |
|-------|-------------|
| red_box | Red rectangle + arrow (default) |
| arrow | Red arrow pointing to element |
| callout | Speech bubble with text |
| highlight | Semi-transparent yellow overlay |
| circle | Red circle around element |
| number | Numbered marker for steps |

## Examples

```bash
# Basic annotation
python scripts/annotate.py "login.png" "the Login button"

# With text label
python scripts/annotate.py "settings.png" "the gear icon" --text "Click here"

# Callout style
python scripts/annotate.py "form.png" "email field" --style callout --text "Enter your email"
```

## Requirements

- GEMINI_API_KEY or GOOGLE_API_KEY in environment
- Python packages: google-genai, Pillow, python-dotenv

## Overview

スクリーンショットに赤枠・矢印・吹き出し・ハイライト等の注釈を自動で追加するスキルです。技術ドキュメント、ユーザーマニュアル、チュートリアル作成に最適。

## Troubleshooting

| エラー | 解決方法 |
|--------|---------|
| API key not found | `GEMINI_API_KEY` または `GOOGLE_API_KEY` を環境変数に設定 |
| Element not found in screenshot | `instruction` をより具体的に記述（例: "左上の歯車アイコン"） |

## Success Criteria

- [ ] 元画像を変更せず、注釈付きの別ファイルが出力されている
- [ ] 指定したUI要素に正しく注釈が付けられている
- [ ] エラーなく完了している

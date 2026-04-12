---
name: screenshot-annotator
description: "A skill that automatically adds annotations such as red boxes, arrows, and callouts to screenshots. Triggered by requests like 'Add annotations to screenshot', 'Add arrows to the screen', 'Annotations for manual'."
triggers:
  - Add annotations to screenshot
  - Add arrows to the screen
  - Annotations for manual
  - Add red box
  - Add callout
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

A skill that automatically adds annotations such as red boxes, arrows, callouts, and highlights to screenshots. Ideal for creating technical documentation, user manuals, and tutorials.

## Troubleshooting

| Error | Solution |
|-------|----------|
| API key not found | Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` as an environment variable |
| Element not found in screenshot | Describe the `instruction` more specifically (e.g., "the gear icon in the top left") |

## Success Criteria

- [ ] An annotated file is output without modifying the original image
- [ ] Annotations are correctly applied to the specified UI element
- [ ] Completed without errors

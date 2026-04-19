---
name: tutorial-generator
description: "Automatically generates operation tutorials from screenshots using Gemini Vision API. Triggered by requests like 'Create an operation manual', 'Generate instructions from screenshots', 'Create a usage guide', etc."
triggers:
  - Create an operation manual
  - Generate instructions from screenshots
  - Create a usage guide
  - Create a tutorial
  - Explain from screen capture
  - tutorial-generator
  - how-to guide
---

# Tutorial Generator

Analyze screenshots and generate step-by-step operation instructions.

## Workflow

1. Provide screenshot of the UI/screen
2. Gemini Vision analyzes visible elements (buttons, forms, menus)
3. Generates structured tutorial with actionable steps
4. Outputs HTML tutorial with embedded image

## Usage

```bash
python scripts/generate_tutorial.py "{screenshot_path}" --output "{output_path}"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| screenshot_path | Yes | - | Path to screenshot |
| --output | No | auto | Output HTML path |
| --context | No | - | Additional context about the screen |

## Output Format

Generated HTML includes:
- Screen overview (what this screen is for)
- Original screenshot
- Numbered operation steps
- Element locations and descriptions
- Tips and warnings

## Example

```bash
# Basic usage
python scripts/generate_tutorial.py "login_screen.png"

# With context
python scripts/generate_tutorial.py "settings.png" --context "User settings page for changing password"

# Specify output
python scripts/generate_tutorial.py "dashboard.png" --output "docs/tutorials/dashboard_guide.html"
```

## Requirements

- GEMINI_API_KEY or GOOGLE_API_KEY in environment
- Python packages: google-genai, Pillow, python-dotenv

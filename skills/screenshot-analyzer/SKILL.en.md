---
name: screenshot-analyzer
description: "A skill that automatically generates error diagnoses or operation tutorials from screenshots. Triggered by requests like 'Analyze this screenshot', 'Check the screen error', 'Create operation steps'."
triggers:
  - Analyze this screenshot
  - Check the screen error
  - Create operation steps
  - Screenshot analysis
  - Diagnose error screen
  - screenshot-analyzer
  - screenshot analysis
---

# Screenshot Analyzer

Analyze screenshots for error diagnosis or operation tutorial generation.

## Modes

1. **Analyze**: Detect errors, identify causes, suggest solutions
2. **Tutorial**: Generate step-by-step operation guides with annotations

## Usage

```bash
# Error analysis (default)
python scripts/analyze.py "{screenshot}" --mode analyze

# Tutorial generation
python scripts/analyze.py "{screenshot}" --mode tutorial
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| screenshot | Yes | - | Path to screenshot |
| --mode, -m | No | analyze | Mode: analyze or tutorial |
| --output, -o | No | auto | Output HTML path |
| --no-annotate | No | false | Skip annotation generation |

## Output

### Analyze Mode
- Screen description
- Error detection (message, type, location)
- Root cause analysis
- Solution suggestions (NextStep)

### Tutorial Mode
- Screen overview
- Numbered operation steps
- Annotated screenshots per step
- Tips and warnings

## Examples

```bash
# Analyze error screenshot
python scripts/analyze.py "error_console.png"

# Generate tutorial
python scripts/analyze.py "settings_menu.png" --mode tutorial

# Specify output
python scripts/analyze.py "login.png" --mode tutorial --output "docs/login_guide.html"

# Skip annotations
python scripts/analyze.py "error.png" --no-annotate
```

## Requirements

- GEMINI_API_KEY or GOOGLE_API_KEY in environment
- Python packages: google-genai, Pillow, python-dotenv

## Overview

A skill that automatically generates error diagnoses or operation tutorials from screenshots. It recognizes UI elements with Gemini Vision API and outputs root cause analysis, solution suggestions, or step-by-step operation guides.

## Troubleshooting

| Error | Solution |
|-------|----------|
| API key not found | Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` as an environment variable |
| Analysis returned empty results | Screenshot may be unclear. Use a higher resolution image |

## Success Criteria

- [ ] Analyze mode: Error content and solutions are output
- [ ] Tutorial mode: Step-numbered operation guide is output
- [ ] Output HTML file is generated correctly

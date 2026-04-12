---
name: pptx-creator
description: "A skill that automatically generates .pptx files maintaining template design, just by entering a topic. Triggered by requests like 'Create a presentation', 'Generate slides', 'Create PPTX', 'Create a proposal deck'."
triggers:
  - Create a presentation
  - Generate slides
  - Create PPTX
  - Create a proposal deck
  - pptx-creator
  - Create PowerPoint
  - Make a deck
---

# /pptx-creator — PPTX Presentation Auto-Generation v2

Automatically generates editable .pptx files that maintain template design, just by entering a topic.
After generation, image export + Gemini Vision quality verification is available.

## Triggers

Activated by requests such as:
- "Create a presentation", "Generate slides", "Create PPTX", "Generate deck"
- "Create a presentation about ~"
- "Create a proposal deck", "Generate report slides"

## How It Works

1. **Gemini Flash** generates a structured outline (YAML) from the topic
2. Maintains the template PPTX design (master/theme/fonts)
3. Hybrid approach of **Layout PH injection** + **Rich element code generation** for high-quality slide generation
4. **Image export** + **Gemini Vision quality review** (`--verify`)

## Templates

| Template | Size | Font | Features |
|----------|------|------|----------|
| `simple` | 13.333" x 7.5" | Yu Gothic | Simple, versatile, PH injection method |
| `standard` | 20.0" x 11.25" | Noto Sans JP + Futura | Professional design, code_gen method |

## Slide Types (11 types)

| Type | Description |
|------|-------------|
| `title` | Cover slide (centered title + subtitle + accent line) |
| `section` | Section divider (number + title + accent bar) |
| `content` | Bulleted content (title bar + bullet points) |
| `key_message` | One key message displayed large and centered |
| `two_column` | Two-column layout (left/right content in rounded cards) |
| `comparison` | Left/right comparison (header bar + bullet points) |
| `agenda` | Numbered agenda (circle numbers + divider lines) |
| `closing` | Closing slide (Thank you + accent line) |
| `kpi_dashboard` | KPI card display (3-4 cards, rounded cards + change rate) |
| `process_flow` | Process flow (numbered circles + arrows + descriptions) |
| `table` | Table display (header row accent + alternating backgrounds) |

## Usage

### Generate PPTX from Topic

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "AI Utilization Proposal" \
  --template simple \
  -o output/slides/proposal.pptx
```

### Generate + Quality Verification (Recommended)

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "Q1 Performance Report" \
  --template standard \
  --slides 10 \
  --verify \
  -o output/slides/q1_report.pptx
```

### Generate Outline Only (Dry Run)

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "New Business Plan" \
  --dry-run \
  --save-outline /tmp/outline.yaml
```

### Image Export Only

```bash
python skills/pptx-creator/scripts/export_to_images.py \
  output/slides/proposal.pptx \
  -o output/slides/proposal_images/
```

### Quality Review Only

```bash
python skills/pptx-creator/scripts/quality_reviewer.py \
  output/slides/proposal_images/ \
  --threshold 7.0
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--topic` | *1 | - | Presentation topic |
| `--outline` | *1 | - | Existing outline YAML path |
| `--template` | No | simple | Template name (simple/standard) |
| `--output` / `-o` | No | auto-generated | Output PPTX path |
| `--slides` / `-n` | No | 8 | Number of slides |
| `--audience` | No | business | Target audience |
| `--language` / `-l` | No | ja | Output language (ja/en) |
| `--save-outline` | No | - | Outline YAML save destination |
| `--dry-run` | No | false | Generate outline only |
| `--verify` | No | false | Image export + quality verification after generation |
| `--verify-threshold` | No | 7.0 | Quality verification pass score threshold |

*1: `--topic` and `--outline` are mutually exclusive required parameters

## Template Placement

```text
skills/pptx-creator/templates/
├── simple/template.pptx      ← Simple Yu Gothic template
└── standard/template.pptx    ← Standard basic template
```

## Dependencies

- Python 3.8+
- `python-pptx` — PPTX manipulation
- `google-genai` — Gemini API
- `pyyaml` — YAML processing
- `python-dotenv` — Environment variables
- `libreoffice` — Image export (when using --verify)
- `poppler-utils` — PDF to PNG conversion (when using --verify)
- Environment variables: `GEMINI_API_KEY` or `GOOGLE_API_KEY`

## Agent Execution Steps

When a user requests "Create a presentation" or similar:

1. Gather topic and requirements
2. Execute the following command:

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "<user's topic>" \
  --template simple \
  --slides <count> \
  --verify \
  -o output/slides/<filename>.pptx
```

3. Check quality verification results
4. If failed, modify outline and regenerate
5. Communicate the output file path to the user

## Overview

A skill that automatically generates editable .pptx files maintaining template design, just by entering a topic. Generates outlines (YAML) with Gemini Flash, supporting 11 slide types.

## Troubleshooting

| Error | Solution |
|-------|----------|
| API key not found | Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` as an environment variable |
| Template not found | Verify template files are placed in `skills/pptx-creator/templates/` |
| LibreOffice not found | `libreoffice` installation is required when using `--verify` |

## Success Criteria

- [ ] A .pptx file containing the specified number of slides has been generated
- [ ] When `--verify` is specified, the quality score is above the threshold
- [ ] Template fonts and color scheme are maintained

## Usage

See the "Usage" section above. Basic example:

```bash
python skills/pptx-creator/scripts/pptx_creator.py --topic "AI Utilization Proposal" --template simple --verify -o output/slides/proposal.pptx
```

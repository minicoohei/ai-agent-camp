---
name: pptx-converter
description: "PPTX template conversion & deck generation from scratch. Rewrites content while preserving themes, animations, and SmartArt. Triggered by requests like 'Convert PPTX', 'Create slides', 'Rewrite PowerPoint', 'Generate deck'."
triggers:
  - Convert PPTX
  - Create slides
  - Rewrite PowerPoint
  - Generate deck
  - pptx-converter
  - PowerPoint conversion
  - Create slides using template
version: 1.0.0
author: CursorBootcamp
dependencies:
  - python: 3.8+
  - packages: ["python-pptx", "pyyaml", "lxml", "google-generativeai", "python-dotenv", "Pillow"]
---

## Trigger Words
"Convert PPTX", "Create slides", "Rewrite PowerPoint", "Generate deck", "PowerPoint"

# PPTX Converter

A tool for PowerPoint file template conversion and deck generation from scratch.

## Features

### 1. convert - Template Conversion (single command)
Copies the source PPTX, semantically analyzes all elements with Gemini, and automatically rewrites content for a new topic.

```bash
python skills/pptx-converter/scripts/pptx_converter.py convert \
    source.pptx \
    --topic "2026 Q1 Sales Report" \
    -o output/slides/q1_report.pptx
```

**Preserved:** Slide masters, theme colors, font definitions, animations, transitions, SmartArt structure, layout positioning

### 2. extract - Generate Mapping YAML
Extracts and semantically analyzes all elements from the source PPTX, generating a coordinate-element mapping YAML for manual review and editing.

```bash
python skills/pptx-converter/scripts/pptx_converter.py extract \
    source.pptx \
    -o mapping.yaml
```

### 3. build - Mapping + Data → PPTX
Rewrites elements using a manually edited data YAML.

```bash
python skills/pptx-converter/scripts/pptx_converter.py build \
    source.pptx \
    mapping.yaml \
    --data data.yaml \
    -o output.pptx
```

### 4. deck - Generate Deck from Scratch
Generates an outline with Gemini from a topic → automatically creates PPTX.

```bash
python skills/pptx-converter/scripts/pptx_converter.py deck \
    --topic "AI Agent Utilization Proposal" \
    --type proposal \
    --style corporate \
    -o output/slides/proposal.pptx
```

**deck options:**
- `--type`: auto / presentation / proposal / report / educational / pitch
- `--style`: corporate / creative / minimal / academic
- `--slides N`: Number of slides (0=AI decides)
- `--audience`: Target audience
- `--outline-only`: Output outline YAML only

## Supported Element Types

| Type | Extract | Rewrite | Notes |
|------|:-------:|:-------:|-------|
| Text | o | o | Full style preservation (font, color, bold, etc.) |
| Chart | o | o | Data-only replacement via chart.replace_data() |
| Table | o | o | Cell style preserved, content only replaced |
| Image | o | o | Preserved by default, individual replacement available |
| Shape | o | o | Text within shapes replaced |
| Group | o | o | Child elements processed recursively (up to depth 3) |
| SmartArt | o | partial | Text nodes only, replaced via direct XML manipulation |

## Mapping YAML Structure

```yaml
source: "source.pptx"
generated_at: "2026-02-09T15:30:00"
slide_width: 12192000
slide_height: 6858000

slides:
  - slide_number: 1
    layout: "Title Slide"
    elements:
      - id: 2
        name: "Title 1"
        type: text
        role: title
        hint: "Main title. 15-25 characters."
        position: { left: 457200, top: 274638, width: 8229600, height: 1143000 }
        style: { font: "Meiryo UI", size: 36, bold: true, color: "2563EB" }
        value: "2025 Sales Strategy"
        placeholder: "{{slide_1_title}}"

placeholders:
  - key: "{{slide_1_title}}"
    type: text
    role: title
    current: "2025 Sales Strategy"
```

## Workflow Decision

- **Have a template PPTX** → `convert` (single command)
- **Want to manually review mapping** → `extract` → edit YAML → `build`
- **Create from scratch** → `deck`

## Environment Variables

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Gemini API key (required)
- `GEMINI_FLASH_MODEL`: Text processing model (default: gemini-2.5-flash)

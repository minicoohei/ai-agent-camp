---
name: gslides-creator
description: "Skill for creating Google Slides from templates. Triggered by requests like 'create Google Slides,' 'generate slides,' 'create a presentation,' etc. Uses GAS + clasp CLI to copy templates, rewrite content, and generate decks from scratch."
triggers:
  - gslides-creator
  - Google Slides作成
  - スライド生成
  - プレゼン作成
  - テンプレートからスライド
  - gslides
---

# /gslides-creator - Google Slides Creator

Create Google Slides from templates, or generate decks from scratch.

## Prerequisites

```bash
# clasp logged in
clasp login

# GAS API enabled
# https://script.google.com/home/usersettings

# gslides-parser configured (used by convert command)
python skills/gslides-parser/scripts/gslides_parser.py setup
```

## Quick Start

```bash
# 1. Initial GAS project setup (first time only)
python skills/gslides-creator/scripts/gslides_creator.py setup

# 2. Create from template with new topic
python skills/gslides-creator/scripts/gslides_creator.py convert \
  1ZVAI8Cjts1N44lYXgoCoZXfb0gz7BAx7A1A5-bhapvQ \
  --topic "Claude Code Practical Course for Engineers" \
  --title "Claude Code Practical Course"

# 3. Generate deck from scratch
python skills/gslides-creator/scripts/gslides_creator.py deck \
  --topic "2026 Q1 Sales Report" --slides 10 --style corporate
```

## Subcommands

| Command | Description |
|---------|-------------|
| `setup` | Initial GAS project setup |
| `convert <template_id> --topic "..."` | Template copy -> Gemini rewrite |
| `build <template_id> --data data.yaml` | Template copy -> Precise YAML data rewrite |
| `deck --topic "..."` | Generate deck from scratch (Gemini outline) |

## convert - Template Rewrite

Copy a template and generate content adapted to a new topic using Gemini, then batch replace with `replaceAllText`.

```bash
python gslides_creator.py convert TEMPLATE_ID \
  --topic "New topic" \
  --title "New title"
```

Processing flow:
1. Parse template structure with gslides-parser
2. Generate new content for placeholders with Gemini Flash
3. Copy template + replaceAllText with GAS `convertPresentation()`
4. Output new Google Slides URL

## build - Precise Rewrite

Rewrite text, style, and position per element based on a mapping YAML.

```bash
# 1. Get mapping with gslides-parser
python gslides_parser.py analyze TEMPLATE_ID -o mapping.yaml

# 2. Create data YAML (manual or Gemini)
# 3. Build
python gslides_creator.py build TEMPLATE_ID \
  --data data.yaml --title "New Presentation"
```

Data YAML format:
```yaml
slides:
  - slide_number: 1
    elements:
      - id: "g123abc"
        value: "New title text"
        style:
          font: "Noto Sans JP"
          size: 36
          bold: true
      - id: "g456def"
        value: "New body text"
```

## deck - Generate Deck from Scratch

Generate an outline with Gemini and build slides with GAS.

```bash
python gslides_creator.py deck \
  --topic "AI Utilization Proposal" \
  --slides 10 \
  --style corporate \
  --save-outline outline.yaml

# To inherit a template's theme
python gslides_creator.py deck \
  --topic "Q1 Report" \
  --template TEMPLATE_ID \
  --style minimal
```

### Styles

| Style | Description |
|-------|-------------|
| `corporate` | Blue-toned business (default) |
| `minimal` | Monochrome + red accent |

### Slide Types (Auto-selected)

| Type | Description |
|------|-------------|
| title | Title slide |
| section | Section divider |
| content | Bullet points |
| key_message | Key message |
| two_column | Two-column layout |
| comparison | Comparison (left/right) |
| agenda | Agenda |
| closing | Closing slide |
| kpi_dashboard | KPI cards |
| process_flow | Process flow |
| table | Table |

## GAS Function List

| Function | File | Description |
|----------|------|-------------|
| `convertPresentation()` | convertSlides.js | Template copy + replaceAllText |
| `listPlaceholders()` | convertSlides.js | Get placeholder list |
| `buildPresentation()` | buildSlides.js | Detailed element-level rewrite |
| `createDeck()` | deckSlides.js | Generate deck from scratch |
| `createDeckFromTemplate()` | deckSlides.js | Template-based deck generation |

## Related Skills

- **gslides-parser**: Parse Google Slides structure and generate mapping YAML
- **pptx-creator**: PPTX version of equivalent functionality (Gemini -> YAML -> PPTX)
- **pptx-converter**: PPTX template conversion
- **gas-clasp-ops**: clasp project management

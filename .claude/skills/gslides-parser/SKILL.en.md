---
name: gslides-parser
description: "Skill for parsing Google Slides structure via GAS and outputting YAML mapping. Triggered by requests like 'parse the slides,' 'analyze slide structure,' 'create YAML mapping,' etc. Performs pptx-converter compatible semantic analysis + placeholder assignment."
triggers:
  - gslides-parser
  - スライドパース
  - スライド構造解析
  - YAMLマッピング
  - Google Slides解析
  - gslides
---

# /gslides-parser - Google Slides Parser

Parse the structure of a Google Slides presentation via GAS and output pptx-converter compatible mapping YAML.

## Prerequisites

```bash
# Install clasp (if not already installed)
npm install -g @google/clasp

# Log in with Google account
clasp login

# Enable Google Apps Script API
# https://script.google.com/home/usersettings
```

## Quick Start

```bash
# 1. Initial GAS project setup (first time only)
python skills/gslides-parser/scripts/gslides_parser.py setup

# 2. Manually run once in GAS editor to grant permissions
npx @google/clasp open --cwd skills/gslides-parser/gas/

# 3. Run parse
python skills/gslides-parser/scripts/gslides_parser.py analyze \
  1ZVAI8Cjts1N44lYXgoCoZXfb0gz7BAx7A1A5-bhapvQ \
  -o output/slides/mapping.yaml
```

## Subcommands

| Command | Description |
|---------|-------------|
| `setup` | Initial GAS project setup (clasp create + push) |
| `analyze <id>` | Parse presentation -> YAML output |
| `json <id>` | Output only GAS parse result JSON |

## Options

### analyze

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output YAML path | `output/slides/gslides_<id>_<timestamp>.yaml` |
| `--no-gemini` | Disable Gemini semantic analysis | false |
| `--skip-push` | Skip clasp push | false |

### json

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output JSON path | stdout |
| `--skip-push` | Skip clasp push | false |

## Output YAML Schema (pptx-converter compatible)

```yaml
source: "Google Slides: Presentation Name"
presentation_id: "1ZVAI8..."
presentation_url: "https://docs.google.com/presentation/d/1ZVAI8.../edit"
generated_at: "2026-02-10T12:00:00"
slide_width_pt: 720
slide_height_pt: 405

slides:
  - slide_number: 1
    object_id: "p6"
    layout: "TITLE"
    elements:
      - id: "g1234abcd"
        type: text
        role: title
        hint: "Main title."
        position: { left: 36, top: 150, width: 648, height: 80 }
        style: { font: "Noto Sans JP", size: 36, bold: true, color: "333333" }
        value: "Title Text"
        placeholder: "{{slide_1_title}}"

placeholders:
  - key: "{{slide_1_title}}"
    type: text
    role: title
    current: "Title Text"
```

## Processing Flow

```
[User] -> python gslides_parser.py analyze <id>
                    |
        +-----------+-----------+
        |  1. clasp push        |  Push GAS code
        |     (gas/ -> GAS)     |
        +-----------+-----------+
                    |
        +-----------+-----------+
        |  2. clasp run         |  Run parsePresentation()
        |     parsePresentation |  -> Returns JSON structure
        +-----------+-----------+
                    |
        +-----------+-----------+
        |  3. gas_to_yaml.py    |  Semantic analysis
        |     JSON -> YAML      |  + placeholder assignment
        +-----------+-----------+
                    |
        +-----------+-----------+
        |  4. YAML output       |  pptx-converter compatible
        +-----------+
```

## Elements Parsed by GAS Parser

| Element Type | Extracted Information |
|-------------|---------------------|
| **Shape (Text)** | Text, style (font/size/bold/color), placeholder detection, fill color |
| **Image** | Source URL, content URL, link |
| **Table** | All cell text, row/column count, header detection, cell style |
| **Group** | Recursive parsing of child elements |
| **SheetsChart** | Spreadsheet ID, chart ID |
| **Line** | Line type, thickness, color |
| **WordArt** | Rendered text |
| **Video** | Source, URL, video ID |

## Semantic Analysis

Heuristics automatically detect the following roles:

- **Text**: title, subtitle, heading, body, caption, label, footnote, page_number, bullet_list
- **Image**: hero_image, logo, icon, photo, decorative, background
- **Table**: data_table, comparison_table, schedule_table
- **Chart**: revenue_chart, trend_chart, comparison_chart
- **Shape**: accent_decoration, callout, divider, background_shape
- **Group**: process_flow, feature_cards, step_diagram

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Not logged in` | clasp not logged in | `npx @google/clasp login` |
| `Script API disabled` | GAS API disabled | Enable at [GAS API settings](https://script.google.com/home/usersettings) |
| `PERMISSION_DENIED` | OAuth scope not approved | Manually run once in GAS editor to grant permissions |
| `Function not found` | Push not completed | `npx @google/clasp push --force` |
| Timeout | Large presentation | Run directly from GAS editor |

## Related Skills

- **gslides-creator**: Create new slides from templates using the parsed YAML
- **pptx-converter**: Equivalent functionality for PPTX files (extract -> build -> convert)
- **gas-clasp-ops**: clasp project management

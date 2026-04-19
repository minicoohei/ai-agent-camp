# PowerPoint Operations - PPTX Operations

Read, write, and analyze PowerPoint files using python-pptx.

## Features

- Read slides and convert to Markdown
- Analyze presentation structure
- Extract templates
- Create new PPTX files

## Execution Steps

### Step 1: Extract Parameters

Extract the following from the user's input:
- **Command**: read / to-markdown / analyze / extract-template / create
- **File path**: Path to the PPTX file
- **Slide number**: When specifying a particular slide
- **Output destination**: File path (displayed on screen if omitted)

### Step 2: Run the Tool

```bash
# Read
uv run python tools/pptx_ops.py read <file.pptx>

# Convert to Markdown
uv run python tools/pptx_ops.py to-markdown <file.pptx>

# Analyze structure
uv run python tools/pptx_ops.py analyze <file.pptx>

# Extract template
uv run python tools/pptx_ops.py extract-template <file.pptx> --output template.json

# Create
uv run python tools/pptx_ops.py create template.json --output new.pptx
```

### Step 3: Display Results

Present the output data to the user.

## Options

### read command

| Option | Description |
|--------|-------------|
| `--slide INT` / `-s` | Specific slide number (1-indexed) |
| `--format TEXT` / `-f` | Output format: text / json |

### to-markdown command

| Option | Description |
|--------|-------------|
| `--output PATH` / `-o` | Output file path |

### extract-template command

| Option | Description |
|--------|-------------|
| `--output PATH` / `-o` | Output JSON file path |

### create command

| Option | Description |
|--------|-------------|
| `--output PATH` / `-o` | Output PPTX file path (required) |

## Usage Examples

### Read a file

```
/pptx-ops read presentation.pptx
```

### Read a specific slide

```
/pptx-ops read presentation.pptx --slide 3
```

### Convert to Markdown

```
/pptx-ops to-markdown presentation.pptx -o slides.md
```

### Analyze a presentation

```
/pptx-ops analyze presentation.pptx --format json
```

### Extract a template

```
/pptx-ops extract-template template.pptx --output my_template.json
```

### Create from a template

```
/pptx-ops create my_template.json --output new_presentation.pptx
```

## Output Format

### read (text format)

```
=== Slide 1 ===
Shapes: 5

Text content:
  - Presentation Title
  - Subtitle
  - Author: Taro Tanaka

Notes: Speaker notes appear here...
```

### to-markdown

```markdown
# presentation.pptx

**Slides**: 10

---

## Table of Contents

1. [Presentation Title](#slide-1)
2. [Overview](#slide-2)
...

---

## Slide 1 {#slide-1}

### Presentation Title

Subtitle

> **Speaker Notes:**
> Speaker notes appear here
```

### analyze

```
📊 Analysis Report: presentation.pptx
==================================================
Slides: 10
Total text length: 2500 characters
Layouts used: ['Title Slide', 'Title and Content', 'Blank']

Shape types:
  MSO_SHAPE_TYPE.PLACEHOLDER (14): 28
  MSO_SHAPE_TYPE.TEXT_BOX (17): 5
  MSO_SHAPE_TYPE.PICTURE (13): 3

Slides overview:
  1. Title Slide (3 shapes)
  2. Title and Content (5 shapes)
  3. Title and Content (4 shapes)
```

### extract-template

```json
{
  "source_file": "presentation.pptx",
  "slide_width": 9144000,
  "slide_height": 6858000,
  "layouts": [
    {
      "name": "Title Slide",
      "placeholders": [...]
    }
  ],
  "slides": [
    {
      "index": 1,
      "layout_name": "Title Slide",
      "content_structure": [...]
    }
  ]
}
```

## Template JSON Format (for create)

```json
{
  "slides": [
    {
      "title": "Slide Title",
      "content": [
        "Bullet point 1",
        "Bullet point 2",
        "Bullet point 3"
      ],
      "notes": "Speaker notes"
    }
  ]
}
```

## Prerequisites

The python-pptx library is required:

```bash
uv add python-pptx
```

## Related Commands

- `/excel-ops` - Excel operations
- `/fetch-slides` - Fetch Google Slides
- `/generate-slide` - Generate slide images

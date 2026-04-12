# PPTX Template Operations

A tool that extracts the format from PowerPoint files into YAML templates and generates new slides with only the text replaced.

## Overview

This tool consists of two scripts:

1. **pptx_ops.py extract-template** - Extract a template from a PPTX
2. **pptx_ops.py create** - Generate a new PPTX from a template

## Workflow

```text
[Original PPTX] -> [Extractor] -> [template.yaml] + [screenshots/]
                                      |
                                 [data.yaml]
                                      |
[template.yaml] + [data.yaml] -> [Generator] -> [New PPTX]
```

## Usage

### 1. Extract Template

Extract format information from an existing PPTX file.

```bash
# Basic template extraction
uv run python tools/pptx_ops.py extract-template sample.pptx --output template.yaml

# Extract specific slides only
uv run python tools/pptx_ops.py extract-template sample.pptx --slide 1 --output slide1_template.yaml

# Generate screenshots as well (requires LibreOffice)
uv run python tools/pptx_ops.py extract-template sample.pptx \
    --output template.yaml \
    --screenshot-dir ./screenshots

# Skip placeholder conversion (keep original text as-is)
uv run python tools/pptx_ops.py extract-template sample.pptx \
    --output template.yaml \
    --no-placeholder
```

### 2. Check File Information

Inspect the structure of a PPTX file.

```bash
uv run python tools/pptx_ops.py analyze sample.pptx
```

### 3. List Placeholders

View the placeholders (replaceable variables) in a template.

```bash
uv run python tools/pptx_ops.py placeholders template.yaml
```

### 4. Create Data Template

Generate an empty data file corresponding to the template.

```bash
uv run python tools/pptx_ops.py create-data template.yaml --output data.yaml
```

### 5. Generate New PPTX

Generate a new PPTX from a template and data.

```bash
uv run python tools/pptx_ops.py generate template.yaml data.yaml --output output.pptx
```

## Template YAML Structure

```yaml
source_file: sample.pptx
slide_width: 12192000  # EMU (914400 EMU = 1 inch)
slide_height: 6858000
slides:
  - index: 1
    layout_name: Blank
    screenshot: slide_1.png
    shapes:
      - id: shape_1
        name: "Title 1"
        type: text_box
        position:
          left: 457200
          top: 274638
          width: 8229600
          height: 1143000
        content:
          word_wrap: true
          paragraphs:
            - text: "{{title}}"
              original_text: "Original Title"
              style:
                font_name: "Meiryo UI"
                font_size: 44
                font_bold: true
                font_color: "000000"
                alignment: center
        fill:
          type: solid
          color: "FFFFFF"
```

## Data YAML Example

```yaml
# Define values corresponding to {{placeholder}} in template.yaml
title: "New Title"
subtitle: "Subtitle"
image_path: "./images/new_image.png"
cell_0_1: "Table cell value"
```

## Supported Shape Types

| Type | Description | Extracted Information |
|------|-------------|---------------------|
| text_box | Text box | Position, size, text, font style, alignment |
| picture | Image | Position, size, image path (converted to placeholder) |
| table | Table | Position, size, row/column count, cell content, cell style |
| auto_shape | Shape | Position, size, fill color, line color, text |
| placeholder | Placeholder | Position, size, type, text |
| group | Group | Recursive extraction of child shapes |

## Screenshot Generation

The following are required for automatic screenshot generation:

```bash
# macOS
brew install poppler
pip install pdf2image
brew install --cask libreoffice

# Windows
# poppler: Download from https://github.com/oschwartz10612/poppler-windows and add to PATH
pip install pdf2image
# LibreOffice: winget install --id TheDocumentFoundation.LibreOffice
```

Use the `--no-generate-screenshot` option to use existing screenshots.

## Example: Mass-Producing Formatted Slides

1. Prepare a formatted PPTX as the source

2. Extract the template
   ```bash
   uv run python tools/pptx_ops.py extract-template format_sample.pptx \
       --output my_template.yaml
   ```

3. Check placeholders
   ```bash
   uv run python tools/pptx_ops.py placeholders my_template.yaml
   ```

4. Create a data file
   ```bash
   uv run python tools/pptx_ops.py create-data my_template.yaml \
       --output my_data.yaml
   ```

5. Edit the data and enter values
   ```yaml
   # my_data.yaml
   title: "Q1 2026 Report"
   author: "Sales Department"
   date: "2026-01-16"
   ```

6. Generate a new PPTX
   ```bash
   uv run python tools/pptx_ops.py generate my_template.yaml my_data.yaml \
       --output Q1_report.pptx
   ```

## Prerequisites

- Python 3.8 or higher
- Required libraries: `python-pptx`, `pyyaml`
- Optional: `pdf2image`, `Pillow` (for screenshot generation)
- Optional: LibreOffice (for PDF conversion)

```bash
pip install python-pptx pyyaml pdf2image Pillow
```

## Notes

- EMU (English Metric Units): 914,400 EMU = 1 inch
- Theme colors cannot be directly converted to RGB and are output as `theme:XXX`
- Grouped shapes are extracted individually as child shapes
- Complex animations and transition effects are not preserved

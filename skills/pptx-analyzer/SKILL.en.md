---
name: pptx-analyzer
description: "A skill that analyzes the structure of PowerPoint files (.pptx), outputting slide, shape, and text information. Triggered by requests like 'Analyze PPTX', 'Check template structure', 'Inspect slide elements'."
triggers:
  - Analyze PPTX
  - Check template structure
  - Inspect slide elements
  - pptx-analyzer
  - PowerPoint analysis
  - Show me the contents of the PowerPoint
---

# PPTX Analyzer

A skill for analyzing the structure of PowerPoint files.

## Features

1. **Structure Extraction**: Extract slides, shapes, placeholders, and text
2. **Image Generation**: Convert slides to PNG images (optional)
3. **Semantic Analysis**: Determine slide roles and element purposes using Gemini (optional)

## Usage

```bash
# Basic analysis (JSON + TXT output)
python scripts/analyze_pptx.py template.pptx

# Analysis with images
python scripts/analyze_pptx.py template.pptx --with-images

# With Gemini semantic analysis
python scripts/analyze_pptx.py template.pptx --with-gemini

# Specify output directory
python scripts/analyze_pptx.py template.pptx --output-dir ./output
```

## Output Formats

### JSON (`{filename}_structure.json`)

```json
{
  "source_file": "template",
  "total_slides": 5,
  "slides": [
    {
      "slide_index": 0,
      "layout_name": "Title Slide",
      "shapes": [
        {
          "shape_id": 2,
          "name": "Title 1",
          "shape_type": "Shape",
          "left": 838200,
          "top": 2130425,
          "width": 10515600,
          "height": 1325563,
          "text": "Presentation Title",
          "has_text_frame": true,
          "is_placeholder": true,
          "placeholder_type": "TITLE (1)"
        }
      ]
    }
  ]
}
```

### Text (`{filename}_structure.txt`)

```
=== Slide 1 (Layout: Title Slide) ===
  [2] Title 1
      Type: Shape, Pos: (0.9", 2.3"), Size: 11.5" x 1.5"
      Placeholder: TITLE (1)
      Text: "Presentation Title"
```

## Dependencies

- `python-pptx`: Required
- `Pillow`: Image processing (when using `--with-images`)
- `pdf2image` + LibreOffice: Image conversion via PDF
- `google-generativeai`: Gemini analysis (when using `--with-gemini`)

## Use Cases

1. **Template Analysis**: Understand template structure before automated slide generation
2. **Placeholder Identification**: Identify text boxes and chart positions for replacement
3. **Layout Verification**: Check layout types and element positioning for each slide

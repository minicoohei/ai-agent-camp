---
name: document-processor
description: "Sub-agent for reading, editing, and analyzing PDF/PPTX/Excel files. Separates large document processing from the main context to optimize context consumption. Triggered by requests like 'analyze the PDF,' 'read the PPTX contents,' 'parse the Excel,' 'edit the slides,' etc."
triggers:
  - PDFを分析
  - PDFを編集
  - PPTXを分析
  - PPTXを読んで
  - スライドの内容
  - Excelを分析
  - Excelを読んで
  - ドキュメントを処理
---

# Document Processor Sub-Agent

A sub-agent for reading, editing, and analyzing PDF/PPTX/Excel files in a dedicated context.

## Purpose

Separate large document processing from the main agent's context to:
- Reduce context consumption (2000-10000 token reduction effect)
- Return only processing result summaries
- Enable parallel processing of multiple files

## Supported Formats

| Format | Read | Edit | Analyze |
|--------|:----:|:----:|:-------:|
| PDF (.pdf) | Yes | Yes | Yes |
| PowerPoint (.pptx) | Yes | Yes | Yes |
| Excel (.xlsx) | Yes | Yes | Yes |

## Available Scripts

### 1. PowerPoint Operations (`tools/pptx_ops.py`)

```bash
# Read
uv run python tools/pptx_ops.py read <file.pptx>

# Markdown conversion
uv run python tools/pptx_ops.py to-markdown <file.pptx>

# Structure analysis
uv run python tools/pptx_ops.py analyze <file.pptx>

# Template extraction
uv run python tools/pptx_ops.py extract-template <file.pptx> --output template.json

# Create new
uv run python tools/pptx_ops.py create <template.json> --output new.pptx
```

### 2. Excel Operations (`tools/excel_ops.py`)

```bash
# Read
uv run python tools/excel_ops.py read <file.xlsx>

# Read specific sheet
uv run python tools/excel_ops.py read <file.xlsx> --sheet "Sheet1"

# Markdown conversion
uv run python tools/excel_ops.py to-markdown <file.xlsx>

# Analysis report
uv run python tools/excel_ops.py analyze <file.xlsx>

# Write
uv run python tools/excel_ops.py write <file.xlsx> --data '{"sheet": "Sheet1", "cell": "A1", "value": "Hello"}'
```

### 3. PDF Operations (`tools/pdf_page_editor.py`)

```bash
# Text extraction and analysis
uv run python tools/pdf_page_editor.py analyze <file.pdf>

# Page editing
uv run python tools/pdf_page_editor.py edit <file.pdf> --page 1 --changes <changes.yaml>

# Compression
uv run python tools/pdf_page_editor.py compress <file.pdf> --output compressed.pdf
```

## Sub-Agent Invocation Pattern

The main agent invokes this sub-agent using the following pattern:

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Document analysis",
    prompt="""
    Read and execute this skill: skills/document-processor/SKILL.md
    
    Task: {user's instructions}
    Target file: {file path}
    
    Return the result in summary format.
    """
)
```

## Return Format

Processing results are returned in the following summary format:

```yaml
status: success
file: example.pptx
summary:
  total_slides: 10
  key_content:
    - slide_1: "Title slide - Project overview"
    - slide_2: "Table of contents - 5 items"
  findings:
    - "Template is 16:9 aspect ratio"
    - "Color scheme: blue/white/black"
output_files:
  - example_structure.json
  - example_structure.txt
```

## Dependencies

```txt
python-pptx>=0.6.21
openpyxl>=3.1.0
pdf2image>=1.16.0
Pillow>=9.0.0
PyMuPDF>=1.21.0
google-generativeai>=0.3.0
```

## Use Cases

1. **PPTX analysis**: Understanding template structure, identifying placeholders
2. **Excel analysis**: Understanding data structure, grasping inter-sheet relationships
3. **PDF editing**: Text correction, page reconstruction
4. **Batch processing**: Bulk processing of multiple documents

## Notes

- Large files (>50MB) may take time to process
- PDF editing does not modify the original file; it generates a new file
- Image-heavy PPTX files can have images extracted with the `--with-images` option

## Overview

A sub-agent skill that reads, edits, and analyzes PDF/PPTX/Excel files in a dedicated context. Separates large document processing from the main context and returns only processing result summaries.

## Troubleshooting

| Error | Solution |
|-------|----------|
| python-pptx not installed | Install with `uv add python-pptx` |
| PDF parsing error | Verify PyMuPDF is installed: `uv add PyMuPDF` |
| File too large (>50MB) | Processing may take time. Consider pre-compressing with the PDF compression skill |

## Success Criteria

- [ ] Document content has been returned in summary format (YAML)
- [ ] During edit operations, the original file is not modified and a new file is generated
- [ ] Completed without errors

## Usage

See the "Available Scripts" section above. Basic examples:

```bash
# Read PPTX
uv run python tools/pptx_ops.py read presentation.pptx

# Analyze Excel
uv run python tools/excel_ops.py analyze data.xlsx

# Analyze PDF
uv run python tools/pdf_page_editor.py analyze document.pdf
```

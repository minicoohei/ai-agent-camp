---
nonInteractiveMode: compliant
---

# Excel Operations - Excel File Operations

Read, write, and analyze Excel files using openpyxl.

## Features

- Sheet reading and Markdown conversion
- Workbook structure analysis
- New Excel file creation
- Cell updates

## Steps

### Step 1: Extract Parameters

Extract the following from the user's input:
- **Command**: read / to-markdown / analyze / write / list-sheets
- **File path**: Path to the Excel file
- **Sheet name**: If specifying a particular sheet
- **Output destination**: File path (defaults to screen display if omitted)

### Step 2: Run the Tool

```bash
# Read
uv run python tools/excel_ops.py read <file.xlsx>

# Convert to Markdown
uv run python tools/excel_ops.py to-markdown <file.xlsx>

# Analyze
uv run python tools/excel_ops.py analyze <file.xlsx>

# List sheets
uv run python tools/excel_ops.py list-sheets <file.xlsx>
```

### Step 3: Display Results

Present the output data to the user.

## Options

### read command

| Option | Description |
|--------|-------------|
| `--sheet TEXT` / `-s` | Read a specific sheet |
| `--max-rows INT` / `-n` | Maximum rows (default: 100) |
| `--format TEXT` / `-f` | Output format: text / json |

### to-markdown command

| Option | Description |
|--------|-------------|
| `--sheet TEXT` / `-s` | Convert a specific sheet |
| `--max-rows INT` / `-n` | Maximum rows |
| `--output PATH` / `-o` | Output file path |

### write command

| Option | Description |
|--------|-------------|
| `--data JSON` / `-d` | Data in JSON format (required) |
| `--output PATH` / `-o` | Output to a separate file |

## Usage Examples

### Read a file

```
/excel-ops read report.xlsx
```

### Convert a specific sheet to Markdown

```
/excel-ops to-markdown data.xlsx --sheet "Sales Data" -o sales.md
```

### Analyze a workbook

```
/excel-ops analyze financial_report.xlsx --format json
```

### Create a new file

```
/excel-ops write new.xlsx --data '{"headers":["Name","Age"],"rows":[["Tanaka",30],["Sato",25]]}'
```

## Output Formats

### read (text format)

```
Sheet: Sheet1
Dimensions: A1:D100
Rows: 99

Headers: ['Name', 'Department', 'Sales', 'Achievement Rate']

Sample rows (first 5):
  1: ['Taro Tanaka', 'Sales Dept', '1500000', '120%']
  2: ['Hanako Sato', 'Planning Dept', '980000', '98%']
```

### to-markdown

```markdown
# report.xlsx

**Sheet**: Sheet1
**Dimensions**: A1:D100
**Rows**: 99 (max 100)

| Name | Department | Sales | Achievement Rate |
|------|-----------|-------|-----------------|
| Taro Tanaka | Sales Dept | 1500000 | 120% |
| Hanako Sato | Planning Dept | 980000 | 98% |
```

### analyze

```
Analysis Report: report.xlsx
==================================================
Sheets: 3
Total rows: 150
Estimated cells: 600

Sheet1
   Dimensions: A1:D50
   Rows: 50, Columns: 4
   Headers: ['Name', 'Department', 'Sales', 'Achievement Rate']
```

## Prerequisites

The openpyxl library is required:

```bash
uv add openpyxl
```

## Related Commands

- `/pptx-ops` - PowerPoint operations
- `/fetch-slides` - Google Slides retrieval

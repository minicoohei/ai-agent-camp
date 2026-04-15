---
name: csv-analyzer
description: "Skill for retrieving row/column counts, estimating data types, detecting missing values, and outputting statistical information for numeric columns from CSV files. Triggered by requests like 'analyze the CSV,' 'check the CSV contents,' 'show me a data overview,' etc."
triggers:
  - csv-analyzer
  - CSV分析
  - CSVファイル解析
  - データ概要
  - 欠損値チェック
  - CSV統計
  - CSVプロファイリング
---

## Trigger Words
"CSV analysis," "CSV file parsing," "data overview," "missing value check," "CSV statistics"

# CSV Analyzer Skill

## Overview
A skill that analyzes CSV files and performs statistical information and data type estimation.

## Features
- Row and column count retrieval
- Data type estimation (automatic type detection for each column)
- Statistical information (basic statistics for numeric columns)
- Missing value detection (NULL and NA value detection)
- Encoding detection

## Usage

### Command Line Execution
```bash
python skills/csv-analyzer/scripts/analyzer.py --input data.csv
```

### Using in Python
```python
from scripts.analyzer import CSVAnalyzer

analyzer = CSVAnalyzer("data.csv")
result = analyzer.analyze()
print(result)
```

## Output Format
```json
{
  "filename": "data.csv",
  "rows": 1000,
  "columns": 5,
  "encoding": "utf-8",
  "file_size_mb": 2.5,
  "columns_info": []
}
```

## Dependencies
- pandas >= 2.0
- chardet >= 5.0

## Installation
```bash
uv sync
```

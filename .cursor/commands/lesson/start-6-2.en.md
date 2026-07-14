---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1"]
duration: "~35 min"
level: "intermediate"
tags: ["agent", "skill", "skills"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 6-2: Skill Creation Basics

## 📍 What You'll Do

**Lesson 6-2: Skill Creation Basics** !

| Item | Details |
|------|---------|
| Goal | Create reusable Skills in `skills/` in a format that can be referenced from Codex / Claude Code / Cursor |
| Duration | ~35 min |
| Skills Used | SKILL.md, Python |
| Prerequisites | Lesson 6-1 completed, Python environment set up |
| Course Page | [Module 6: Agent Development](https://ai-agent.camp/en/course/module-6) in parallel |

**Session flow:**
1. Create the Skill directory structure
2. Implement SKILL.md and scripts
3. Verify operation and reflect in usage guide

By the end of this session, you will be able to manage custom Skills in the shared `skills/` directory.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Create Skill Directory Structure

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Create the Skill directory structure",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the skills/csv-analyzer directory and prepare the following structure:

mkdir -p skills/csv-analyzer/scripts
mkdir -p skills/csv-analyzer/tests
mkdir -p skills/csv-analyzer/examples

touch skills/csv-analyzer/SKILL.md
touch skills/csv-analyzer/requirements.txt

Verify the directory structure.
```

**Expected result**: The Skill directory structure is created.

---

## 🚀 Step 2: Create SKILL.md Document

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Create SKILL.md document",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the file skills/csv-analyzer/SKILL.md with the following content:

---
name: csv-analyzer
description: A Skill that analyzes CSV files and provides statistics and data type inference
version: 1.0.0
author: your-username
dependencies:
  - python: "3.8+"
  - packages: ["pandas", "chardet"]
---

# CSV Analyzer Skill

## Overview
A Skill that analyzes CSV files and provides statistics and data type inference.

## Features
- Get row and column counts
- Data type inference (auto-detect each column's data type)
- Statistics (basic stats for numeric columns)
- Missing value detection (detect NULL and NA values)
- Encoding detection

## Usage

### Command-Line Execution
```bash
python skills/csv-analyzer/scripts/analyzer.py --input data.csv
```

### Using in Python
```python
from scripts.analyzer import CSVAnalyzer

analyzer = CSVAnalyzer('data.csv')
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
```

**Expected result**: The SKILL.md document is created.

---

## 🚀 Step 3: Create Python Implementation

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Create Python implementation",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the file skills/csv-analyzer/scripts/analyzer.py with the following content:

import pandas as pd
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

class CSVAnalyzer:
    """Class for analyzing CSV files"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def analyze(self) -> Dict[str, Any]:
        """Analyze CSV file"""
        df = pd.read_csv(self.file_path)
        file_size_mb = self.file_path.stat().st_size / (1024 * 1024)

        return {
            "filename": self.file_path.name,
            "rows": len(df),
            "columns": len(df.columns),
            "file_size_mb": round(file_size_mb, 2),
            "columns_info": self._analyze_columns(df)
        }

    def _analyze_columns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze each column"""
        columns_info = []
        for col in df.columns:
            col_data = df[col]
            col_info = {
                "name": col,
                "type": str(col_data.dtype),
                "null_count": int(col_data.isna().sum()),
                "unique_values": int(col_data.nunique())
            }

            # Add statistics for numeric columns
            if pd.api.types.is_numeric_dtype(col_data):
                col_info["stats"] = {
                    "min": float(col_data.min()) if not col_data.isna().all() else None,
                    "max": float(col_data.max()) if not col_data.isna().all() else None,
                    "mean": float(col_data.mean()) if not col_data.isna().all() else None
                }

            columns_info.append(col_info)
        return columns_info

    def to_json(self, output_path: str = None) -> str:
        """Output analysis results in JSON format"""
        result = self.analyze()
        json_str = json.dumps(result, indent=2, ensure_ascii=False)

        if output_path:
            Path(output_path).write_text(json_str, encoding='utf-8')

        return json_str

def main():
    parser = argparse.ArgumentParser(description="Analyze CSV files")
    parser.add_argument("--input", required=True, help="Input CSV file path")
    parser.add_argument("--output", help="Output JSON file path (prints to stdout if omitted)")
    args = parser.parse_args()

    analyzer = CSVAnalyzer(args.input)
    result = analyzer.to_json(args.output)

    if not args.output:
        print(result)

if __name__ == "__main__":
    main()
```

**Expected result**: The CSVAnalyzer class is implemented.

---

## 🚀 Step 4: Create requirements.txt

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Create requirements.txt",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the file skills/csv-analyzer/requirements.txt with the following content:

pandas>=2.0.0
chardet>=5.0.0
pytest>=7.4.0
```

**Expected result**: The dependency file is created.

---

## 🚀 Step 5: Create and Run Tests

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Create and run tests",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create the file skills/csv-analyzer/tests/test_analyzer.py with the following content:

import pytest
import pandas as pd
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.analyzer import CSVAnalyzer

@pytest.fixture
def sample_csv():
    """Create a sample CSV file for testing"""
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, None, 28],
        'score': [85.5, 90.0, 78.5, 82.0, 88.5]
    })
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.csv', delete=False, encoding='utf-8'
    ) as f:
        df.to_csv(f, index=False)
        return f.name

def test_analyze_basic(sample_csv):
    """Basic analysis test"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    assert result['rows'] == 5
    assert result['columns'] == 4
    assert 'columns_info' in result

def test_column_types(sample_csv):
    """Column type analysis test"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    col_names = [col['name'] for col in result['columns_info']]
    assert 'id' in col_names
    assert 'name' in col_names

def test_null_detection(sample_csv):
    """Missing value detection test"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    age_col = next(col for col in result['columns_info'] if col['name'] == 'age')
    assert age_col['null_count'] == 1

def test_file_not_found():
    """File not found error test"""
    with pytest.raises(FileNotFoundError):
        CSVAnalyzer('nonexistent.csv')

Then run the tests with the following command:
cd skills/csv-analyzer && uv sync && pytest tests/ -v
```

**Expected result**: Tests are created and all tests pass.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "Cannot import module"},
      {"id": "trouble_2", "label": "pandas is not installed"},
      {"id": "trouble_3", "label": "Tests fail"},
      {"id": "trouble_4", "label": "JSON output has character encoding issues"}
    ]
  }]
}
```


### Issue 1: "Cannot import module"
**Cause**: Python path is not configured
**Solution prompt**:
```
Add the script directory to sys.path:
sys.path.insert(0, str(Path(__file__).parent.parent))
Or set the PYTHONPATH environment variable.
```

### Issue 2: "pandas is not installed"
**Cause**: Dependency packages not installed
**Solution prompt**:
```
Run `uv add -r requirements`.txt.
If using a virtual environment, verify the correct environment is active.
```

### Issue 3: "Tests fail"
**Cause**: Test file path is incorrect
**Solution prompt**:
```
Verify the directory from which you are running pytest.
Check that test files are in the tests/ directory.
```

### Issue 4: "JSON output has character encoding issues"
**Cause**: Encoding is not UTF-8
**Solution prompt**:
```
Specify ensure_ascii=False in json.dumps().
Specify encoding='utf-8' when writing to files.
```

---

## ✅ Checkpoint
- [ ] Directory structure is created
- [ ] Documented with SKILL.md
- [ ] analyzer.py is implemented
- [ ] requirements.txt is created
- [ ] All tests pass


---

## 📋 Output Preview

### Expected Output
```
📁 output/
└── {project-name}/  (agent/code artifacts)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/{project-name}/

# Check the beginning (first 30 lines)
head -30 output/{project-name}/
```

> 💡 View full text: `cat output/{project-name}/` to display the full text

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that skills/csv-analyzer/ directory was correctly created and pytest All tests pass.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-6-3)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-6-3
- finish → End

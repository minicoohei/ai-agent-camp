---
name: monitoring-dashboard
description: "Used for marimo dashboards and project progress visualization. Triggered by requests like 'create a dashboard', 'visualize progress', 'display test results', etc."
triggers:
  - create a dashboard
  - visualize progress
  - display test results
  - monitoring-dashboard
  - project progress dashboard
  - monitoring
---

# Monitoring Dashboard - Project Monitoring Dashboard

Generates dashboards to visualize project progress, test results, and requirements traceability using marimo Run Mode.

## Workflow

1. Specify the data source (JSON/CSV)
2. Select the dashboard layout (progress/test/integrated)
3. Auto-generate a marimo notebook (.py)
4. Launch with `marimo run` and check in the browser

## Dashboard Types

### 1. Project Progress Dashboard

Visualizes the following from WBS progress data:
- Task completion rate (overall/by phase)
- Burndown chart
- Workload by assignee
- Delayed task alerts

**Data format:** `dummy-wbs-progress.json`
```json
{
  "tasks": [
    {
      "id": "WBS-001",
      "name": "Task name",
      "phase": "Phase A",
      "assignee": "Assignee",
      "progress": 75,
      "start_date": "2025-01-01",
      "due_date": "2025-01-15",
      "status": "in_progress"
    }
  ]
}
```

### 2. Test Results Dashboard

Visualizes the following from test execution results:
- Pass/fail/skip rate by test suite
- Test coverage trend
- Failed test list (by severity)
- Test execution time analysis

**Data format:** `dummy-test-results.json`
```json
{
  "suites": [
    {
      "name": "Suite name",
      "tests": [
        {
          "id": "TC-001",
          "name": "Test name",
          "status": "passed",
          "duration_ms": 150,
          "severity": "high"
        }
      ]
    }
  ]
}
```

### 3. Requirements Traceability Dashboard

Tracking from requirements to design to tests:
- Requirements coverage matrix
- Highlighting of untested requirements
- Requirements status distribution (pie chart)

## marimo Notebook Structure

```python
import marimo as mo
import pandas as pd
import plotly.express as px
import json

app = mo.App()

@app.cell
def load_data():
    """Load data"""
    with open("path/to/data.json") as f:
        data = json.load(f)
    return pd.DataFrame(data["tasks"])

@app.cell
def progress_chart(df):
    """Progress chart"""
    fig = px.bar(df, x="name", y="progress", color="phase",
                 title="Task Progress Rate")
    mo.ui.plotly(fig)

@app.cell
def summary_metrics(df):
    """Summary metrics"""
    total = len(df)
    completed = len(df[df["progress"] == 100])
    mo.md(f"""
    ## Project Summary
    - Total tasks: **{total}**
    - Completed: **{completed}**
    - Completion rate: **{completed/total*100:.1f}%**
    """)
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| data_source | Yes | - | Path to data file (JSON/CSV) |
| dashboard_type | No | integrated | Dashboard type (progress/test/traceability/integrated) |
| output | No | output/pm/dashboard.py | Output file path |
| title | No | Project Dashboard | Dashboard title |

## Output Format

Generates a marimo notebook (.py):
- `output/pm/dashboard.py` -- Launch with `marimo run output/pm/dashboard.py`

## Requirements

- Python 3.10+
- marimo (`uv add marimo`)
- pandas (`uv add pandas`)
- plotly (`uv add plotly`)

## Example

```
Use the monitoring-dashboard skill to create an integrated project dashboard from dummy data.
Data: Any progress JSON or CSV
-> output/pm/dashboard.py is generated -> Launch with marimo run
```

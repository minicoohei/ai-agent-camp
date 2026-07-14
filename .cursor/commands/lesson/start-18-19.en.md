---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-18"]
level: "intermediate"
tags: ["pm", "dashboard", "marimo", "monitoring"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-19: marimo Dashboard

| Item | Details |
|------|------|
| Goal | Create an integrated dashboard for the TaskFlow project using marimo Run Mode (with dummy data) |
| Duration | ~30 min |
| Skills Used | monitoring-dashboard skill, data-analyst skill |
| Prerequisites | Lesson 18-18 completed |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

## 📍 Step 1: Verifying marimo Environment

marimo is a reactive notebook environment built on Python. Unlike Jupyter, cells automatically track dependencies and recalculate on changes. In this lesson, you will build an integrated project dashboard using marimo.

```json
{
  "type": "AskQuestion",
  "question": "Do you have experience with marimo?",
  "options": [
    "First time using it",
    "Have Jupyter experience",
    "Have marimo experience",
    "Just help me with setup"
  ],
  "multiple": false
}
```

### marimo Setup

Based on your selection, prepare the environment with the following commands:

```bash
# Verify Python 3.10 or higher
python3 --version    # On Windows: python --version

# Install marimo
uv add marimo pandas plotly numpy

# Check installation
marimo --version
```

**Quick tutorial for first-time users:**
- marimo cells are text fields containing Python code
- Variable changes within a cell automatically update other dependent cells
- `marimo run` mode: Read-only (for dashboard distribution)
- `marimo edit` mode: Interactive editing (for development)

Optionally, run the official tutorial with the `marimo tutorial` command.

## 📍 Step 2: Loading Dummy Data

Check the TaskFlow project dummy data and prepare data to display on the dashboard.

```json
{
  "type": "AskQuestion",
  "question": "Which data do you want to use?",
  "options": [
    "WBS progress data",
    "Test result data",
    "Both",
    "Add custom data too"
  ],
  "multiple": false
}
```

### Data File Verification

Use the following dummy data for the dashboard (data structure embedded within the lesson):

**dummy-wbs-progress.json** structure:
```json
{
  "project_id": "taskflow-v1",
  "phases": [
    {
      "phase_name": "Planning",
      "start_date": "2024-01-01",
      "planned_end": "2024-02-28",
      "actual_end": "2024-02-25",
      "status": "completed",
      "completion_rate": 100,
      "tasks": 5,
      "completed_tasks": 5
    }
  ],
  "current_phase": "Implementation",
  "overall_progress": 65,
  "requirements": [
    {"req_id": "REQ-001", "title": "User Auth", "status": "Done", "test_cases": 12},
    {"req_id": "REQ-002", "title": "Task CRUD", "status": "Done", "test_cases": 20},
    {"req_id": "REQ-003", "title": "Notifications", "status": "Done", "test_cases": 8},
    {"req_id": "REQ-004", "title": "Search/Filter", "status": "In Progress", "test_cases": 5},
    {"req_id": "REQ-005", "title": "Dashboard Display", "status": "In Progress", "test_cases": 3},
    {"req_id": "REQ-006", "title": "Report Output", "status": "On Hold", "test_cases": 0},
    {"req_id": "REQ-007", "title": "External API Integration", "status": "Rejected", "test_cases": 0}
  ]
}
```

**dummy-test-results.json** structure:
```json
{
  "test_execution_date": "2024-07-15",
  "test_suites": [
    {
      "suite_name": "User Auth Test",
      "total_cases": 12,
      "passed": 11,
      "failed": 1,
      "skipped": 0,
      "success_rate": 91.67
    }
  ],
  "overall_pass_rate": 87.5,
  "failed_tests": [
    {
      "test_id": "TC-AUTH-007",
      "name": "Password Reset - Invalid Token Handling",
      "error": "Expected status 400, got 500"
    }
  ]
}
```

### Data Loading Code Example

Define and use dummy data directly within the dashboard (refer to the JSON structure above).

```python
import json
import pandas as pd

# Define dummy data directly (using the structure above)
wbs_data = {
    "project_id": "taskflow-v1",
    "phases": [
        {"phase_name": "Planning", "start_date": "2024-01-01", "planned_end": "2024-02-28",
         "actual_end": "2024-02-25", "status": "completed", "completion_rate": 100,
         "tasks": 5, "completed_tasks": 5},
        # ... Define other phases similarly
    ],
    "current_phase": "Implementation",
    "overall_progress": 65,
    "requirements": [
        {"req_id": "REQ-001", "title": "User Auth", "status": "Done", "test_cases": 12},
        {"req_id": "REQ-002", "title": "Task CRUD", "status": "Done", "test_cases": 20},
        {"req_id": "REQ-003", "title": "Notifications", "status": "Done", "test_cases": 8},
        {"req_id": "REQ-004", "title": "Search/Filter", "status": "In Progress", "test_cases": 5},
        {"req_id": "REQ-005", "title": "Dashboard Display", "status": "In Progress", "test_cases": 3},
        {"req_id": "REQ-006", "title": "Report Output", "status": "On Hold", "test_cases": 0},
        {"req_id": "REQ-007", "title": "External API Integration", "status": "Rejected", "test_cases": 0}
    ]
}

test_data = {
    "test_execution_date": "2024-07-15",
    "test_suites": [
        {"suite_name": "User Auth Test", "total_cases": 12, "passed": 11,
         "failed": 1, "skipped": 0, "success_rate": 91.67},
        # ... Define other suites similarly
    ],
    "overall_pass_rate": 87.5,
    "failed_tests": [
        {"test_id": "TC-AUTH-007", "name": "Password Reset - Invalid Token Handling",
         "error": "Expected status 400, got 500"}
    ]
}

# Convert to DataFrame
phases_df = pd.DataFrame(wbs_data["phases"])
test_suites_df = pd.DataFrame(test_data["test_suites"])

print("WBS Progress Data:")
print(phases_df.head())
print("\nTest Results Data:")
print(test_suites_df.head())
```

## 📍 Step 3: 3-Panel Dashboard Configuration

Display the key metrics of the TaskFlow project in 3 panels. Each panel visualizes a different aspect of project management.

```json
{
  "type": "AskQuestion",
  "question": "Select the dashboard layout",
  "options": [
    "3 panels side by side",
    "Tab switching",
    "Scroll type",
    "Let AI suggest optimal layout"
  ],
  "multiple": false
}
```

### Panel 1: Project Progress

Display overall project progress from multiple perspectives:

**Display content:**
- Overall progress bar (currently 65%)
- Phase-by-phase progress table (Planning 100%, Design 92%, Implementation 65%, Testing 20%)
- Progress trend chart (weekly progress rates)
- Delay alert (implementation phase is -3 days vs. schedule)

**Plotly code example:**
```python
import plotly.graph_objects as go
import plotly.express as px

# Progress bar by phase
fig_phase = go.Figure(data=[
    go.Bar(y=['Planning', 'Design', 'Implementation', 'Testing', 'Operations'],
           x=[100, 92, 65, 20, 0],
           orientation='h',
           marker=dict(color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6']))
])
fig_phase.update_layout(title="Progress by Phase",
                        xaxis_title="Progress Rate (%)",
                        height=300)

# Overall progress gauge
fig_gauge = go.Figure(data=[
    go.Indicator(mode="gauge+number",
                 value=65,
                 title={'text': "Overall Progress"},
                 domain={'x': [0, 1], 'y': [0, 1]},
                 gauge={'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffcccc"},
                            {'range': [50, 80], 'color': "#ffffcc"},
                            {'range': [80, 100], 'color': "#ccffcc"}]})
])
```

### Panel 2: Test Results

Test execution results and quality metrics:

**Display content:**
- Pie chart of overall test success rate (87.5%)
- Test suite results list (success rate, test count)
- Failed test list (test ID, failure reason, severity)
- Quality trend (success rate trend over past 4 weeks)

**Plotly code example:**
```python
# Test success rate pie chart
success_rate = test_data["overall_pass_rate"]
failure_rate = 100 - success_rate

fig_pie = go.Figure(data=[
    go.Pie(labels=['Passed', 'Failed'],
           values=[success_rate, failure_rate],
           marker=dict(colors=['#2ecc71', '#e74c3c']),
           hole=0.3)
])
fig_pie.update_layout(title="Overall Test Success Rate")

# Bar chart by test suite
fig_suites = px.bar(test_suites_df,
                    x='suite_name',
                    y='success_rate',
                    color='success_rate',
                    color_continuous_scale='RdYlGn',
                    range_color=[70, 100],
                    title="Success Rate by Test Suite")

# Failed test list table
failed_df = pd.DataFrame(test_data["failed_tests"])
```

### Panel 3: Requirements Tracker

Requirements coverage and status tracking:

**Display content:**
- Requirements status distribution (implemented, in progress, on hold, rejected)
- Test coverage rate (92% of all requirements implemented and tested)
- Requirement-level test mapping (number of test cases linked to each requirement)
- High-risk requirement flags (requirements with 0 test cases)

**Plotly code example:**
```python
# Requirements status distribution
status_counts = {
    'Implemented': 42,
    'In Progress': 8,
    'On Hold': 2,
    'Rejected': 1
}

fig_status = go.Figure(data=[
    go.Bar(x=list(status_counts.keys()),
           y=list(status_counts.values()),
           marker=dict(color=['#2ecc71', '#f39c12', '#3498db', '#95a5a6']))
])
fig_status.update_layout(title="Requirements Status Distribution",
                        yaxis_title="Number of Requirements")

# Test coverage rate
coverage = 92
fig_coverage = go.Figure(data=[
    go.Indicator(mode="gauge+number+delta",
                 value=coverage,
                 title={'text': "Test Coverage"},
                 gauge={'axis': {'range': [0, 100]},
                        'threshold': {'line': {'color': "red"}, 'thickness': 4, 'value': 80}})
])
```

## 📍 Step 4: Launch and Verify with marimo run

Run the completed dashboard in marimo and verify that all panels render correctly.

```json
{
  "type": "AskQuestion",
  "question": "Select the launch method",
  "options": [
    "marimo run (read-only)",
    "marimo edit (edit mode)",
    "Verify with screenshots"
  ],
  "multiple": false
}
```

### Dashboard Python File Structure

Create with the following structure as `output/pm/dashboard.py`:

```python
import marimo as mo
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

app = mo.App()

# ============= Cell 1: Environment and Dependencies =============
@app.cell
def environment():
    import sys
    print(f"Python {sys.version}")
    print(f"marimo version: {mo.__version__}")
    return

# ============= Cell 2: Data Definition =============
@app.cell
def load_data():
    # Define dummy data directly
    wbs_data = {
        "project_id": "taskflow-v1",
        "phases": [
            {"phase_name": "Planning", "start_date": "2024-01-01", "planned_end": "2024-02-28",
             "actual_end": "2024-02-25", "status": "completed", "completion_rate": 100,
             "tasks": 5, "completed_tasks": 5},
            {"phase_name": "Design", "start_date": "2024-03-01", "planned_end": "2024-04-30",
             "actual_end": "2024-04-28", "status": "completed", "completion_rate": 92,
             "tasks": 8, "completed_tasks": 7},
            {"phase_name": "Implementation", "start_date": "2024-05-01", "planned_end": "2024-07-31",
             "actual_end": None, "status": "in_progress", "completion_rate": 65,
             "tasks": 12, "completed_tasks": 8},
            {"phase_name": "Testing", "start_date": "2024-08-01", "planned_end": "2024-09-15",
             "actual_end": None, "status": "planned", "completion_rate": 20,
             "tasks": 6, "completed_tasks": 1},
            {"phase_name": "Operations", "start_date": "2024-09-16", "planned_end": "2024-10-31",
             "actual_end": None, "status": "planned", "completion_rate": 0,
             "tasks": 4, "completed_tasks": 0}
        ],
        "current_phase": "Implementation",
        "overall_progress": 65,
        "requirements": [
            {"req_id": "REQ-001", "title": "User Auth", "status": "Done", "test_cases": 12},
            {"req_id": "REQ-002", "title": "Task CRUD", "status": "Done", "test_cases": 20},
            {"req_id": "REQ-003", "title": "Notifications", "status": "Done", "test_cases": 8},
            {"req_id": "REQ-004", "title": "Search/Filter", "status": "In Progress", "test_cases": 5},
            {"req_id": "REQ-005", "title": "Dashboard Display", "status": "In Progress", "test_cases": 3},
            {"req_id": "REQ-006", "title": "Report Output", "status": "On Hold", "test_cases": 0},
            {"req_id": "REQ-007", "title": "External API Integration", "status": "Rejected", "test_cases": 0}
        ]
    }

    test_data = {
        "test_execution_date": "2024-07-15",
        "test_suites": [
            {"suite_name": "User Auth Test", "total_cases": 12, "passed": 11,
             "failed": 1, "skipped": 0, "success_rate": 91.67},
            {"suite_name": "Task Management Test", "total_cases": 20, "passed": 17,
             "failed": 2, "skipped": 1, "success_rate": 85.0},
            {"suite_name": "Notification Test", "total_cases": 8, "passed": 7,
             "failed": 1, "skipped": 0, "success_rate": 87.5}
        ],
        "overall_pass_rate": 87.5,
        "failed_tests": [
            {"test_id": "TC-AUTH-007", "name": "Password Reset - Invalid Token Handling",
             "error": "Expected status 400, got 500"}
        ]
    }

    phases_df = pd.DataFrame(wbs_data["phases"])
    test_suites_df = pd.DataFrame(test_data["test_suites"])

    return wbs_data, test_data, phases_df, test_suites_df

# ============= Cell 3: Panel 1 - Project Progress =============
@app.cell
def panel_progress(wbs_data):
    mo.md(f"""
    # 📊 Panel 1: Project Progress

    **Overall Progress: {wbs_data['overall_progress']}%**

    Current Phase: {wbs_data['current_phase']}
    """)

# ============= Cell 4: Panel 2 - Test Results =============
@app.cell
def panel_tests(test_data):
    mo.md(f"""
    # ✅ Panel 2: Test Results

    **Overall Success Rate: {test_data['overall_pass_rate']}%**

    Failed Tests: {len(test_data['failed_tests'])}
    """)

# ============= Cell 5: Panel 3 - Requirements Tracker =============
@app.cell
def panel_requirements(wbs_data):
    total = len(wbs_data.get("requirements", []))
    done = sum(1 for r in wbs_data.get("requirements", []) if r.get("status") == "Done")
    in_progress = sum(1 for r in wbs_data.get("requirements", []) if r.get("status") == "In Progress")
    coverage = round(done / total * 100) if total > 0 else 0
    mo.md(f"""
    # 📋 Panel 3: Requirements Tracker

    **Test Coverage: {coverage}%**

    Implemented Requirements: {done}
    In-Progress Requirements: {in_progress}
    """)

# ============= Cell 6: Dashboard Integration =============
@app.cell
def dashboard(wbs_data):
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M JST")
    mo.md(f"""
    # 🎯 TaskFlow Project Integrated Dashboard

    Each panel (Panel 1-3) is displayed individually in the cells above.

    ---

    **Last Updated**: {now}

    **Data Source**: Dummy data (samples/)
    """)

if __name__ == "__main__":
    app.run()
```

### Execution commands

```bash
# Launch in read-only mode (for dashboard distribution)
marimo run output/pm/dashboard.py

# Or launch in edit mode (for development and fine-tuning)
marimo edit output/pm/dashboard.py
```

### Verification Checklist

```json
{
  "type": "AskQuestion",
  "question": "Did the dashboard launch successfully?",
  "options": [
    "Success - All panels are displayed",
    "Partial error - Fixes needed",
    "Launch failed - Debug support needed",
    "Screenshot verification is sufficient"
  ],
  "multiple": false
}
```

**Expected display:**
- Panel 1 (Project Progress): Phase-by-phase bars, overall progress gauge
- Panel 2 (Test Results): Success rate pie chart, failed test list
- Panel 3 (Requirements Tracker): Status distribution, coverage rate

If everything displays correctly, this lesson is complete.

---

## ✅ Deliverables

- `output/pm/dashboard.py` - Integrated dashboard in marimo notebook format

## 🚀 Troubleshooting

| Problem | Solution |
|------|--------|
| Cannot install marimo | Verify Python 3.10+. Retry after `uv sync` |
| Data is missing | Refer to the embedded dummy data structure within the lesson to supplement definitions |
| Plotly charts not displaying | Install the latest version with `uv add plotly` |
| marimo run does not start | Check for syntax errors with `marimo edit` |


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── presentation.md  (presentation materials)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/presentation.md

# Check the beginning (first 30 lines)
head -30 output/pm/presentation.md
```

> 💡 Full text: Run `cat output/pm/presentation.md` to display the full text

## ➡️ Next Steps

→ [Lesson 18-20: Comprehensive Exercise (Capstone)](start-18-20.md)

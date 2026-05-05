---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1", "start-8-2"]
duration: "~40 min"
level: "intermediate"
tags: ["data", "marimo", "dashboard", "visualization"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 8-3: Interactive Analysis with Marimo Notebooks

## 📍 What You'll Do

**Lesson 8-3: Interactive Dashboard with Marimo** !

| Item | Details |
|------|------|
| Goal | Build a reactive dashboard for BigQuery data with Marimo |
| Duration | ~40 min |
| Skills used | data-analyst, Marimo |
| Prerequisites | Lesson 8-1 and 8-2 completed, BigQuery connected |
| Course page | [Module 8: Data Analysis](https://ai-agent.camp/en/course/module-8) alongside this lesson |

**Session flow:**
1. Set up the Marimo environment
2. Load and visualize BigQuery data
3. Dynamic filter and chart updates

By the end of this session, you will be able to create interactive analysis notebooks.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite verification)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Install and Launch Marimo

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Install and Launch Marimo",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please set up the Marimo environment.

1. Check if Marimo is installed
2. Also check required packages (altair, pandas)
3. Install if not already installed

After installation, display the version to verify it works.
```

**Expected result:** Marimo and related packages are installed and version is displayed.

---

## 🚀 Step 2: Create a New Marimo Notebook

Create a notebook for GA4 analysis:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Create a New Marimo Notebook",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please create a Marimo notebook for GA4 data analysis.

File: ~/ai-agent-camp/notebooks/ga4_analysis_dashboard.py

Initial cell contents:
1. Import libraries (marimo, pandas, altair, bigquery)
2. Initialize BigQuery client
3. Title and dashboard description

Please also show me how to launch Marimo and open it in the browser.
```

**Expected result:** The notebook file is created and the startup command is provided.

---

## 🚀 Step 3: Add Interactive UI Components

Add UI components for filtering:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Add Interactive UI Components",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please add interactive filters to the Marimo notebook.

UI components to add:
1. Date range selection (start date, end date text boxes)
2. Event type dropdown (ALL, view_item, add_to_cart, purchase)
3. Display count slider (5-50 items)

Please generate the code for each component.
```

**Expected result:** Marimo code for each UI component is generated.

---

## 🚀 Step 4: Reactive Data Fetching

Create cells that fetch data based on UI component values:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Reactive Data Fetching",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please create a cell that uses Marimo's cache feature
to fetch GA4 data for the selected date range.

Requirements:
- Enable caching with @mo.cache decorator
- Accept date range (date_start, date_end) as parameters
- Get daily event count and unique user count
- Return results as DataFrame

Please generate the code.
```

**Expected result:** A data retrieval function with caching is generated.

---

## 🚀 Step 5: Create Charts with Altair

Add charts to visualize data:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Create Charts with Altair",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please generate Marimo cells that create the following charts with Altair.

1. Daily event count line chart
   - X-axis: Date
   - Y-axis: Event count
   - Tooltip: Date, event count, user count

2. Event type bar chart
   - X-axis: Event count
   - Y-axis: Event name (descending)
   - Color: Gradient based on percentage

Please wrap each chart with mo.ui.altair_chart().
```

**Expected result:** Interactive Altair chart code is generated.

---

## ⚠️ Common Issues and Solutions

Use AskQuestion to select the issue, then follow the guidance.

**AskQuestion configuration:**
```json
{
  "title": "Select the issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "Marimo won't start"},
      {"id": "trouble_2", "label": "Cells not updating (reactivity issue)"},
      {"id": "trouble_3", "label": "BigQuery query is slow"},
      {"id": "trouble_4", "label": "Charts not displaying"}
    ]
  }]
}
```


### Issue 1: "Marimo won't start"
**Cause:** Incomplete installation
**Solution prompt:**
```
Please reinstall Marimo.
uv add --upgrade marimo

After installation, verify with marimo --version.
```

### Issue 2: "Cells don't update (reactivity issue)"
**Cause:** Duplicate variable names
**Solution prompt:**
```
Please explain Marimo's variable naming rules.
Please describe how to use different suffixes per cell
(_fetch, _prep, _dyn, etc.).
```

### Issue 3: "BigQuery query is slow"
**Cause:** Cache is not working
**Solution prompt:**
```
Please show me the correct way to use Marimo's @mo.cache decorator.
Also, please show me how to clear the cache.
```

### Issue 4: "Charts don't display"
**Cause:** Altair encoding error
**Solution prompt:**
```
Please diagnose the error where Altair charts are not displaying.
Please check if the DataFrame types and chart encoding
are consistent.
```

---

## ✅ Checkpoint
- [ ] Marimo launched successfully
- [ ] BigQuery client initialized
- [ ] Date input field works
- [ ] Dropdown filter works
- [ ] Slider works
- [ ] Cache function (@mo.cache) works
- [ ] Altair charts update dynamically
- [ ] Verified that multiple cells update in coordination

---

## 📚 Important Marimo Features

### Variable Naming Rules
| Purpose | Suffix | Example |
|------|------|----|
| Data fetch | `_fetch` | `df_daily_fetch` |
| Preprocessing | `_prep` | `df_events_prep` |
| Dynamic filter | `_dyn` | `chart_events_dyn` |
| Statistical calc | `_calc` | `total_events_calc` |

### Commonly Used UI Components
```python
mo.ui.text(...)       # Text input
mo.ui.dropdown(...)   # Dropdown
mo.ui.slider(...)     # Slider
mo.ui.table(...)      # Table display
mo.ui.altair_chart()  # Chart display
```


---

## 📋 Deliverable Preview

The deliverables for this lesson are terminal outputs.

### Expected Output Example
```
┌─────────────────────────────────────┐
│  Command execution result               │
│  Status: ✅ Success                      │
│  Records processed: N                    │
└─────────────────────────────────────┘
```

> 💡 To save output to a file, add ` > output/result.txt` at the end of the command

---

## ✅ Completion Check
Paste the following into chat to verify completion:

```
# Completion check: Please verify that the expected output files have been generated in the output/ folder.
```

**Expected result:** A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin a new section.

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-8-4)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-8-4
- finish → End

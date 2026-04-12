---
description: "When the user says /start-8-4 — Module 8 Lesson 8-4: Data Visualization and Dashboard Creation"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1", "start-8-2", "start-8-3"]
duration: "~35 min"
level: "intermediate"
tags: ["data", "visualization", "dashboard", "matplotlib"]
---

# 🎓 Lesson 8-4: Data Visualization and Dashboard Creation

## 📍 What You'll Do

**Lesson 8-4: Visualization and Dashboards** !

| Item | Details |
|------|------|
| Goal | Create charts with matplotlib/seaborn and build dashboards |
| Duration | ~35 min |
| Skills used | data-analyst, visualization libraries |
| Prerequisites | Lesson 8-1 through 8-3 completed, BigQuery connected |
| Course page | [Module 8: Data Analysis](https://ai-agent.camp/en/course/module-8) alongside this lesson |

**Session flow:**
1. Create various charts
2. Combine multiple charts
3. Complete the dashboard and output reports

By the end of this session, you will be able to create analysis reports and dashboards.

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

## 🔧 Step 0: Environment Setup (Japanese Font Settings & Data Preparation)

To display Japanese correctly in charts, first configure the fonts. Add the following code at the beginning of your script:

```python
import matplotlib
import matplotlib.pyplot as plt

# Japanese font settings (auto-detect OS)
import platform
_system = platform.system()
if _system == "Darwin":
    matplotlib.rcParams['font.family'] = 'Hiragino Sans'
elif _system == "Windows":
    matplotlib.rcParams['font.family'] = 'MS Gothic'
else:
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
```

### Fallback When BigQuery Connection Fails

Even if GCP authentication doesn't work, you can proceed with the lesson using sample data. Create a local DataFrame as follows:

```python
import pandas as pd

# Shakespeare-style sample data (no BigQuery required)
sample_data = pd.DataFrame({
    'corpus': ['hamlet', 'macbeth', 'othello', 'kinglear', 'tempest',
               'juliuscaesar', 'romeoand', 'midsummer', 'merchantof', 'twelfthnight'],
    'unique_words': [4828, 3896, 3885, 3766, 3309, 3032, 3000, 2930, 2892, 2780],
    'total_words': [32446, 18314, 27602, 27619, 17780, 20876, 25689, 17121, 22152, 20890]
})

# Time series sample data (GA4-style)
import numpy as np
dates = pd.date_range('2021-01-01', periods=10, freq='D')
sample_timeseries = pd.DataFrame({
    'date': dates,
    'event_count': np.random.randint(500, 2000, size=10)
})
```

> **💡 Hint**: If you already have a BigQuery connection, run queries directly. If you cannot connect, use the sample data above as an alternative.

---

## 🚀 Step 1: Create a Basic Bar Chart

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Create a Basic Bar Chart",
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
```text
Using the BigQuery Shakespeare dataset,
please visualize the unique word count by work as a horizontal bar chart.

Query:
SELECT corpus, COUNT(DISTINCT word) as unique_words
FROM bigquery-public-data.samples.shakespeare
GROUP BY corpus
ORDER BY unique_words DESC
LIMIT 10

Chart requirements:
- Horizontal bar chart (barh)
- Title: "Unique Word Count by Shakespeare Work"
- X-axis label: "Unique Word Count"
- Save at high resolution (dpi=150)

Output: ~/ai-agent-camp/output/chart-4-4-bar.png
```

**Expected result:** A horizontal bar chart is generated and saved to file.

---

## 🚀 Step 2: Time Series Line Chart

Visualize time series trends:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Time Series Line Chart",
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
```text
Please visualize the daily event count from GA4 data as a line chart.

Period: 2021-01-01 to 2021-01-10

Chart requirements:
- Line chart + markers
- X-axis: Date
- Y-axis: Event count
- Add grid lines
- Title: "Daily Event Count Trend"
- Save at high resolution (dpi=150)

Output: ~/ai-agent-camp/output/chart-4-4-line.png
```

**Expected result:** A time series line chart is generated.

---

## 🚀 Step 3: Distribution Histogram

Create a histogram to check the data distribution:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Distribution Histogram",
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
```text
Please visualize the word occurrence distribution in the Shakespeare dataset
as a histogram.

Conditions:
- Words with occurrence count greater than 0 and less than 100
- Number of bins: 50

Chart requirements:
- Histogram
- X-axis: "Word Occurrence Count"
- Y-axis: "Frequency"
- Title: "Word Occurrence Distribution"
- Grid lines on vertical axis
- Save at high resolution (dpi=150)

Output: ~/ai-agent-camp/output/chart-4-4-hist.png
```

**Expected result:** A histogram showing the distribution of occurrences is generated.

---

## 🚀 Step 4: Scatter Plot and Correlation Analysis

Visualize the relationship between 2 variables with a scatter plot:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Scatter Plot and Correlation Analysis",
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
```text
Please visualize the relationship between "Unique Word Count" and "Total Word Count"
of Shakespeare works as a scatter plot.

Chart requirements:
- Scatter plot
- X-axis: Unique word count
- Y-axis: Total word count
- Add labels with work names at each point
- Grid lines
- Save at high resolution (dpi=150)

Output: ~/ai-agent-camp/output/chart-4-4-scatter.png
```

**Expected result:** A scatter plot showing correlations is generated.

---

## 🚀 Step 5: Create a Dashboard

Combine multiple charts into a single image:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Create a Dashboard",
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
```text
Please combine the charts created in Module 8
into a 4-panel dashboard.

Layout:
┌────────────────┬────────────────┐
│  Bar Chart     │  Line Chart    │
│ (Category agg) │ (Time series)  │
├────────────────┼────────────────┤
│  Scatter Plot  │  Histogram     │
│ (Correlation)  │ (Distribution) │
└────────────────┴────────────────┘

Size: 16x12 inches
Overall title: "GA4 & Shakespeare Data Analysis Dashboard"
Save at high resolution (dpi=150)

Output: ~/ai-agent-camp/output/dashboard-4-4.png
```

**Expected result:** A dashboard image with 4 charts is generated.

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
      {"id": "trouble_1", "label": "Charts not displaying"},
      {"id": "trouble_2", "label": "Japanese characters are garbled"},
      {"id": "trouble_3", "label": "Memory error occurs"},
      {"id": "trouble_4", "label": "Chart appearance is poor"}
    ]
  }]
}
```


### Issue 1: "Charts don't display"
**Cause:** matplotlib backend settings
**Solution prompt:**
```text
Please check the matplotlib backend.
Please show me how to switch to the 'Agg' backend for file saving.
```

### Issue 2: "Japanese characters are garbled"
**Cause:** Japanese font is not configured
**Solution prompt:**
```text
Please show me how to configure fonts for displaying
Japanese correctly in matplotlib.
Please provide the settings for macOS.
```

### Issue 3: "Memory error occurs"
**Cause:** Too much data
**Solution prompt:**
```text
Please show me how to optimize memory when plotting large amounts of data.
Please explain approaches using sampling and aggregation.
```

### Issue 4: "Charts don't look good"
**Cause:** Default style settings
**Solution prompt:**
```text
Please show me how to improve chart style with seaborn.
Please provide easy-to-read style settings for presentations.
```

---

## ✅ Checkpoint
- [ ] Created basic bar chart
- [ ] Expressed time series data as line chart
- [ ] Visualized distribution with histogram
- [ ] Analyzed 2-variable relationship with scatter plot
- [ ] Combined multiple charts into dashboard
- [ ] Saved at high resolution (dpi=150+)

---

## 🛠️ Troubleshooting

- Charts don't display
- Japanese fonts are broken
- Memory error occurs

### Charts Not Displaying
Check the matplotlib backend and switch to `Agg` for saving if needed.

### Japanese Font Rendering Issues
Add Japanese font settings and adjust font name priority.

### Memory Error Occurs
Sample the data or pre-aggregate before visualization.

### Choosing Between seaborn and matplotlib
- **matplotlib**: Best for fine-grained customization or placing multiple charts in dashboards using `subplot`
- **seaborn**: Best for creating statistical visualizations (heatmaps, pair plots, box plots, etc.) cleanly with less code. Use `sns.set_theme(style='whitegrid')` to improve appearance globally
- You can combine both. A common pattern is to draw with seaborn and adjust axis labels and titles with matplotlib

---

## 📚 How to Choose Chart Types

| Chart Type | Use Case | Example |
|-------------|------|-----|
| Bar chart | Comparison between categories | Sales by country, headcount by dept |
| Line chart | Time series trends | Daily sales trends |
| Scatter plot | 2-variable relationship | Price vs. sales volume |
| Histogram | Distribution check | Age distribution |
| Pie chart | Composition ratio | Market share |
| Heatmap | 2D data density | Correlation matrix |

---

## 🎉 Module 8 Complete!

Congratulations! You have acquired the following skills:
- BigQuery connection and authentication
- Running exploratory data analysis (EDA)
- Interactive analysis with Marimo
- Creating various chart types
- Building dashboards


---

## 📋 Deliverable Preview

The deliverables for this lesson are terminal outputs.

### Expected Output Example
```text
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

```text
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
      {"id": "next_window", "label": "Start in new window (/start-9-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-9-1
- finish → End

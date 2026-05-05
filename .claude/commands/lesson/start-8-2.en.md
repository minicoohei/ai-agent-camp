---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1"]
duration: "~30 min"
level: "intermediate"
tags: ["data", "bigquery", "eda", "analysis"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 8-2: Running EDA (Exploratory Data Analysis)

## 📍 What You'll Do

**Lesson 8-2: EDA with BigQuery** !

| Item | Details |
|------|------|
| Goal | Perform EDA on GA4 sample data to understand basic statistics, missing values, and distributions |
| Duration | ~30 min |
| Skills used | data-analyst, BigQuery |
| Prerequisites | Lesson 8-1 completed, BigQuery connected |
| Course page | [Module 8: Data Analysis](https://ai-agent.camp/en/course/module-8) alongside this lesson |

**Session flow:**
1. Understand the dataset overview
2. Check basic statistics and missing values
3. Visualize distributions

By the end of this session, you will be able to explore BigQuery data.

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

## 🚀 Step 1: Verify Table Schema

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Verify Table Schema",
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
Please check the GA4 table structure in the BigQuery public dataset.

Table: bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20210101

Information to display:
- Number of rows in the table
- Number of columns
- Name, data type, and description of each column

Please explain the key columns (event_timestamp, event_name, user_pseudo_id,
geo.country, device.browser, ecommerce) in detail.
```

**Expected result:** Table schema information is organized and displayed.

---

## 🚀 Step 2: Calculate Basic Statistics

Calculate basic statistics of the data:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Calculate Basic Statistics",
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
Please calculate basic statistics for the GA4 sample data.

Period: 2021-01-01 to 2021-01-03

Statistics to calculate:
- Total number of events
- Number of unique users
- Number of sessions
- Most common events
- First and last event timestamps

Please display the results clearly.
```

**Expected result:** Basic statistics are displayed in table format.

---

## 🚀 Step 3: Check Missing Values

Check for missing values to verify data quality:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Check Missing Values",
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
Please check for missing values in the GA4 data.

Target date: 2021-01-01

Columns to check:
- user_pseudo_id
- event_name
- geo.country
- device.browser
- ecommerce.purchase_revenue

Please calculate the missing count and missing rate for each column,
and provide insights on data quality.
```

**Expected result:** The missing rate for each column and data quality considerations are displayed.

---

## 🚀 Step 4: Check Categorical Data Distribution

Check the distribution of events and regions:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Check Categorical Data Distribution",
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
Please analyze the distribution of categorical variables in the GA4 data.

1. Event type distribution (TOP 15)
   - Event name, count, unique users, percentage

2. User distribution by country (TOP 10)
   - Country name, event count, unique users, average revenue

3. Browser usage breakdown (TOP 10)
   - Browser name, event count, percentage

Please display each analysis result in table format.
```

**Expected result:** The distribution of each category is displayed in an organized table.

---

## 🚀 Step 5: Time Series Analysis

Analyze daily and hourly trends:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Time Series Analysis",
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
Please perform a time series analysis on the GA4 data.

Period: 2021-01-01 to 2021-01-10

Analysis contents:
1. Daily aggregation
   - Date, total events, unique users, sessions, revenue

2. Hourly trends
   - Event count and user count per time slot (0-23h)

Please display the results and provide insights on trends.
```

**Expected result:** Time series data and trend analysis are displayed.

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
      {"id": "trouble_1", "label": "Query times out"},
      {"id": "trouble_2", "label": "Quota exceeded error"},
      {"id": "trouble_3", "label": "Don't know how to handle NULL"},
      {"id": "trouble_4", "label": "Cannot access nested columns"}
    ]
  }]
}
```


### Issue 1: "Query times out"
**Cause:** Data volume is too large
**Solution prompt:**
```text
Please improve query performance.
Consider the following methods:
- Narrow the date range
- Add a LIMIT clause
- Use sampling
```

### Issue 2: "Quota exceeded error"
**Cause:** BigQuery quota exceeded
**Solution prompt:**
```text
A BigQuery quota error occurred.
Please show me how to reduce query costs.
Also, please show me how to check current quota usage.
```

### Issue 3: "Don't know how to handle NULLs"
**Cause:** Unknown how to aggregate NULL values
**Solution prompt:**
```text
Please show me how to handle NULL values in BigQuery.
- Count NULLs with COUNTIF
- Replace NULLs with COALESCE
- Convert to NULL with NULLIF
```

### Issue 4: "Cannot access nested columns"
**Cause:** Don't know STRUCT/ARRAY type syntax
**Solution prompt:**
```text
Please show me how to access nested columns (STRUCT type)
in BigQuery.
Example: geo.country, device.browser, ecommerce.purchase_revenue
```

---

## ✅ Checkpoint
- [ ] Verified table schema
- [ ] Calculated basic statistics
- [ ] Checked missing values
- [ ] Checked categorical data distribution
- [ ] Analyzed time series data
- [ ] Understood e-commerce data characteristics

---

## 📚 Common EDA Patterns

### Check Distribution
```sql
SELECT column_name, COUNT(*) as count
FROM table
GROUP BY column_name
ORDER BY count DESC
```

### Time Series Trends
```sql
SELECT DATE(timestamp) as date, COUNT(*) as count
FROM table
GROUP BY date
ORDER BY date
```

### Preparation for Correlation Analysis
```sql
SELECT column_a, column_b, COUNT(*) as count
FROM table
GROUP BY column_a, column_b
```


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
      {"id": "next_window", "label": "Start in new window (/start-8-3)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-8-3
- finish → End

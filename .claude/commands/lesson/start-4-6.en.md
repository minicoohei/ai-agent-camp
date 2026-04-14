---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "sheets"]
---

# 🎓 Lesson 4-6: Google Sheets Operations

## 📍 What You'll Do

**Lesson 4-6: Google Sheets Operations** !

| Item | Details |
|------|---------|
| Goal | Read and write spreadsheets using gogcli |
| Duration | ~30 min |
| Skills Used | gogcli sheets |
| Prerequisites | gogcli authentication setup completed (start-4-1 done) |

**Session flow:**
1. Search for spreadsheets from Drive
2. Retrieve sheet data (CSV output)
3. Analyze retrieved data with AI

By the end of this session, you will be able to read and analyze Google Sheets data using gogcli.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. The response may pause depending on the tool, but this is not a malfunction.

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
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → `gog auth list`  to check auth status)
(different_lesson → Show module list)

---

## 🚀 Step 1: Search Spreadsheets from Drive

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Search spreadsheets",
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

First, let's identify the target spreadsheet:

```bash
# Search for spreadsheets from Drive
gog drive ls --query "mimeType='application/vnd.google-apps.spreadsheet'" --account your-email@gmail.com

# Note: gogcli v0.9.0 does not have a `gog sheets list` command.
# Check sheet (tab) names in the Google Sheets UI, or
# specify the sheet name when retrieving data with gog sheets get.
```

**How to get the spreadsheet ID:**
- Google Sheets URL: `https://docs.google.com/spreadsheets/d/<this-is-the-spreadsheet-ID>/edit`
- Or use the file ID from `gog drive ls` results

**Expected result**: A list of spreadsheet files in Drive (file names and IDs) is displayed.

> **💡 Hint**: If you don't have a practice spreadsheet, create a new spreadsheet in Google Sheets and enter a few rows of sample data (names, sales, dates, etc.).

---

## 🚀 Step 2: Get Sheet Data (CSV Output)

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Data retrieval",
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

Retrieve spreadsheet data:

```bash
# Get all sheet data
gog sheets get <spreadsheet-ID> "Sheet1" --account your-email@gmail.com

# Get a specific range (A1:D10)
gog sheets get <spreadsheet-ID> "Sheet1!A1:D10" --account your-email@gmail.com

# Save as CSV file
gog sheets get <spreadsheet-ID> "Sheet1" --account your-email@gmail.com > /tmp/sheet_data.csv

# Alternative: Download CSV via Drive
gog drive download <spreadsheet-ID> --format csv --out ./downloads/sheet_data.csv --account your-email@gmail.com
```

**Range specification format:**

| Format | Description | Example |
|------|------|-----|
| `Sheet1` | Entire sheet | `"Sheet1"` |
| `Sheet1!A1:D10` | Specific range | `"Sheet1!A1:D10"` |
| `Sheet1!A:A` | Entire column | `"Sheet1!A:A"` |
| `Sheet1!1:5` | Row range | `"Sheet1!1:5"` |
| `'Sales Data'!A1:Z` | Japanese sheet name | Wrap sheet name in single quotes |

**Expected result**: Spreadsheet data is displayed in the terminal. If redirected to CSV, it is saved to a file.

> **⚠️ Warning**: When using Japanese sheet names, wrap them in single quotes (e.g., `'Sales Data'!A1:D10`).

---

## 🚀 Step 3: Analyze Retrieved Data with AI

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: AI-powered data analysis",
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

Let's have the AI analyze the retrieved spreadsheet data:

```bash
# Get data and save to file
gog sheets get <spreadsheet-ID> "Sheet1" --account your-email@gmail.com > /tmp/sheet_data.csv
```

Load the saved CSV file in Cursor and request analysis:

```text
Analyze the data in /tmp/sheet_data.csv:
1. Data overview (row count, column count, data types)
2. Basic statistics (mean, max, min for numeric columns)
3. Any trends or patterns noticed
4. Point out any data quality issues (missing values, outliers)
```

**Advanced: Report generation**
```text
Create a monthly report summary from the spreadsheet data above:
- Key KPI highlights
- Month-over-month changes
- Notable trends
- Improvement suggestions
Save in Markdown format in output/reports/.
```

**Advanced: Data visualization**
```text
Visualize the data above with Python matplotlib:
- Monthly sales trend graph
- Pie chart by category
- Top 10 bar chart
Save graphs in output/images/.
```

**Expected result**: The AI generates analysis results, statistics, and trend explanations for the data.

---

## ⚠️ Common Issues and Solutions

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "Do not know the spreadsheet ID"},
      {"id": "trouble_2", "label": "Range specification results in error"},
      {"id": "trouble_3", "label": "Data has character encoding issues"},
      {"id": "trouble_4", "label": "No practice data available"}
    ]
  }]
}
```

### Issue 1: "Do not know the spreadsheet ID"
**Cause**: Does not know how to get the ID
**Solution prompt**:
```text
Open Google Sheets and check the URL:
https://docs.google.com/spreadsheets/d/<this-part-is-the-ID>/edit
Or search for spreadsheets with gog drive ls and use the file ID.
```

### Issue 2: "Range specification results in error"
**Cause**: Sheet name is wrong, or the range does not exist
**Solution prompt**:
```text
gogcli does not have a `gog sheets list` command.
Check the sheet name (tab name) in the Google Sheets UI.
Japanese sheet names must be enclosed in single quotes: 'Sales Data'!A1:D10
```

### Issue 3: "Data has character encoding issues"
**Cause**: Encoding issue
**Solution prompt**:
```text
Redirect output to a file and check the encoding:
gog sheets get ... > /tmp/data.csv
file /tmp/data.csv
If not UTF-8, convert with iconv: iconv -f SHIFT_JIS -t UTF-8 /tmp/data.csv
```

### Issue 4: "No practice data available"
**Cause**: No spreadsheet available for testing
**Solution prompt**:
```text
Create a new spreadsheet in Google Sheets and enter the following sample data:
A1: Name, B1: Department, C1: Sales, D1: Month
A2: Tanaka, B2: Sales, C2: 500000, D2: January
A3: Suzuki, B3: Marketing, C3: 350000, D3: January
(5-10 rows is sufficient)
```

---

## ✅ Checkpoint
- [ ] Was able to search for spreadsheets from Drive
- [ ] Was able to retrieve data from a specific range
- [ ] Was able to save data as a CSV file
- [ ] Was able to have AI analyze data and confirm results


---

## 📋 Output Preview

The deliverable for this lesson is terminal output.

### Expected Output
```text
┌─────────────────────────────────────┐
│  Command execution result              │
│  Status: ✅ Success                     │
│  Items processed: N                     │
└─────────────────────────────────────┘
```

> Tip: To save output to a file, append ` > output/result.txt` to the end of the command

---

## ✅ Completion Check
Paste the following into Codex chat to verify completion:

```text
Run the following gogcli commands to verify that Sheets operations work correctly:
1. gog drive ls --query "mimeType='application/vnd.google-apps.spreadsheet'" --account <email-address>
2. Pick one from the list above, then retrieve data with gog sheets get <spreadsheet-ID> "Sheet1" --account <email-address>
3. Verify the retrieved data displays correctly
Please confirm everything works correctly.
```

**Expected result**: Sheet listing and data retrieval complete without errors.

---

## 🎉 Next Steps

Google Sheets operations are now complete! In the next lesson, you will build an AI secretary workflow integrating Gmail, Calendar, Drive, and Sheets.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/start-4-7)"},
      {"id": "next_window", "label": "Start in new window (/start-4-7)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /start-4-7（AI Secretary Workflow Integration)
- next_window → Open new window with /start-4-7
- finish → End

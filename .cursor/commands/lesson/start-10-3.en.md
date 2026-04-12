---
description: "When the user says /start-10-3 — Module 10 Lesson 10-3: Scheduled Execution and Trigger Setup"
chapter: "courses/aiagent/lesson03-core/module10-gas"
prerequisites: ["start-10-1", "start-10-2"]
duration: "~30 min"
level: "intermediate"
tags: ["gas", "sheets", "google", "automation"]
---

# 🎓 Lesson 10-3: Scheduled Execution and Trigger Setup

## 📍 What You'll Do

**Lesson 10-3: GAS and Google Sheets Integration**!

| Item | Details |
|------|------|
| Goal | Automate spreadsheet reading/writing, data processing, and report generation from GAS |
| Duration | ~30 min |
| Skills used | gas-clasp-ops, Google Sheets API, gogcli |
| Prerequisites | Lesson 10-1 and Lesson 10-2 completed, GAS project created |
| Course page | [Module 10: GAS](https://ai-agent.camp/en/course/module-10)  alongside this lesson |

**Session flow:**
1. Spreadsheet access
2. Data reading functionality
3. Data writing functionality
4. Report generation functionality
5. Automation workflow

By the end of this session, you will be able to automate Sheets integration.

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

## 🚀 Step 1: Spreadsheet Access

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Spreadsheet Access",
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
Please create a Sheets.gs file in the gas-example directory with the following content:

function getActiveSpreadsheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    Logger.log("No active spreadsheet. Please create a new one.");
    return null;
  }
  Logger.log("Spreadsheet: " + ss.getName());
  Logger.log("Spreadsheet ID: " + ss.getId());
  return ss;
}

function getAllSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) return [];

  const sheets = ss.getSheets();
  Logger.log("Total sheets: " + sheets.length);

  sheets.forEach(sheet => {
    Logger.log("- " + sheet.getName() + " (" + sheet.getLastRow() + " rows)");
  });

  return sheets;
}

Please sync with clasp push.
```

**Expected result:** Sheets.gs is synced to Google Drive.

---

## 🚀 Step 2: Data Reading Functions

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Data Reading Functions",
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
Please add the following data reading functions to Sheets.gs:

function getDataRange(sheetName, range) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("Sheet not found: " + sheetName);
    return [];
  }

  const data = sheet.getRange(range).getValues();
  Logger.log("Data retrieved: " + range + " (" + data.length + " rows)");
  return data;
}

function getAllData(sheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return [];

  const lastRow = sheet.getLastRow();
  const lastColumn = sheet.getLastColumn();

  if (lastRow < 1) {
    Logger.log("No data available");
    return [];
  }

  return sheet.getRange(1, 1, lastRow, lastColumn).getValues();
}

Please sync with clasp push.
```

**Expected result:** A function to read data from the spreadsheet is added.

---

## 🚀 Step 3: Data Writing Functions

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Data Writing Functions",
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
Please add the following data writing functions to Sheets.gs:

function writeSingleCell(sheetName, cell, value) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("Sheet not found: " + sheetName);
    return false;
  }

  sheet.getRange(cell).setValue(value);
  Logger.log("Cell write: " + cell + " = " + value);
  return true;
}

function appendRow(sheetName, rowData) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("Sheet not found: " + sheetName);
    return false;
  }

  sheet.appendRow(rowData);
  Logger.log("Row added: " + rowData.join(", "));
  return true;
}

function writeDataRange(sheetName, startCell, data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return false;

  const rows = data.length;
  const cols = data[0].length;
  const range = sheet.getRange(startCell).offset(0, 0, rows, cols);
  range.setValues(data);

  Logger.log("Range write complete: " + rows + " rows x " + cols + " cols");
  return true;
}

Please sync with clasp push.
```

**Expected result:** A function to write data to the spreadsheet is added.

---

## 🚀 Step 4: Report Generation Function

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Report Generation Function",
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
Please add the following report generation functions to Sheets.gs:

function generateSummaryReport(sourceSheetName, reportSheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sourceSheet = ss.getSheetByName(sourceSheetName);
  let reportSheet = ss.getSheetByName(reportSheetName);

  // Create report sheet if it does not exist
  if (!reportSheet) {
    reportSheet = ss.insertSheet(reportSheetName);
  }

  // Clear the report sheet
  reportSheet.clearContents();

  // Report header
  reportSheet.getRange("A1").setValue("=== Summary Report ===");
  reportSheet.getRange("A1").setFontSize(14).setFontWeight("bold");
  reportSheet.getRange("A2").setValue("Generated: " + new Date().toLocaleString("en-US"));

  // Data statistics
  const lastRow = sourceSheet.getLastRow();
  const lastCol = sourceSheet.getLastColumn();

  reportSheet.getRange("A4").setValue("Total records:");
  reportSheet.getRange("B4").setValue(lastRow - 1); // Excluding header

  reportSheet.getRange("A5").setValue("Total columns:");
  reportSheet.getRange("B5").setValue(lastCol);

  Logger.log("Summary report generation complete");
}

function createTestData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("TestData");

  if (!sheet) {
    sheet = ss.insertSheet("TestData");
  }

  // Header
  sheet.getRange("A1:D1").setValues([["Date", "Product", "Quantity", "Amount"]]);

  // Sample data
  const testData = [
    ["2024-01-01", "Product A", 10, 1000],
    ["2024-01-02", "Product B", 5, 500],
    ["2024-01-03", "Product A", 15, 1500],
    ["2024-01-04", "Product C", 8, 800],
    ["2024-01-05", "Product B", 12, 1200]
  ];

  sheet.getRange(2, 1, testData.length, 4).setValues(testData);
  Logger.log("Test data creation complete");
}

Please clasp push, first run createTestData, then run generateSummaryReport("TestData", "Report").
```

**Expected result:** Test data and a summary report are automatically generated.

---

## 🚀 Step 5: Automation Workflow

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Automation Workflow",
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
Please add the following automation workflow functions to Sheets.gs:

function dailyReportTask() {
  Logger.log("===== Daily report generation started =====");

  try {
    // Generate report
    generateSummaryReport("TestData", "DailyReport");

    // Completion notification (send email)
    const userEmail = Session.getActiveUser().getEmail();
    if (userEmail) {
      GmailApp.sendEmail(
        userEmail,
        "Daily report complete " + new Date().toLocaleDateString("en-US"),
        "The daily report has been generated. Please check the DailyReport sheet in the spreadsheet."
      );
    }

    Logger.log("Daily report complete");
  } catch (error) {
    Logger.log("Error: " + error);
  }
}

function setDailyReportTrigger() {
  // Delete existing triggers with the same name
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === "dailyReportTask") {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Create a trigger to run daily at 10:00
  ScriptApp.newTrigger("dailyReportTask")
    .timeBased()
    .everyDays(1)
    .atHour(10)
    .create();

  Logger.log("Daily 10:00 report generation trigger has been set");
}

Please sync with clasp push.
```

**Expected result:** Daily report auto-generation and trigger configuration are set up.

---

## 🚀 Step 6: gogcli x GAS x clasp deploy - Email Aggregation Pipeline

> **Key point**: Build an E2E pipeline: retrieve emails with gogcli -> aggregate with GAS -> output to Sheets -> deploy to production with clasp deploy. This is a practical workflow combining a local CLI (gogcli) with a cloud execution environment (GAS).

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 6: gogcli x GAS x clasp deploy",
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
Build a pipeline to retrieve emails with gogcli, aggregate in GAS, and output to a spreadsheet.

### Step 6-1: Retrieve unread emails with gogcli

gog gmail search "is:unread" --json > ~/ai-agent-camp/gas-example/unread_emails.json

Please check the JSON contents (sender, subject, date, etc.).

### Step 6-2: Create email aggregation script in GAS

Please add the following function to Sheets.gs:

function aggregateEmailStats() {
  // Aggregate email statistics with GmailApp and output to sheet
  const threads = GmailApp.search("is:unread", 0, 50);
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Email Summary");

  if (!sheet) {
    sheet = ss.insertSheet("Email Summary");
  }

  sheet.clearContents();

  // Header
  sheet.getRange("A1:E1").setValues([["Sender", "Subject", "Received", "Label", "Thread Count"]]);
  sheet.getRange("A1:E1").setFontWeight("bold");

  // Email data
  const data = threads.map(thread => {
    const msg = thread.getMessages()[0];
    return [
      msg.getFrom(),
      msg.getSubject(),
      msg.getDate().toLocaleString("ja-JP"),
      thread.getLabels().map(l => l.getName()).join(", "),
      thread.getMessageCount()
    ];
  });

  if (data.length > 0) {
    sheet.getRange(2, 1, data.length, 5).setValues(data);
  }

  // Aggregation summary
  const summaryRow = data.length + 3;
  sheet.getRange("A" + summaryRow).setValue("Aggregation date:");
  sheet.getRange("B" + summaryRow).setValue(new Date().toLocaleString("ja-JP"));
  sheet.getRange("A" + (summaryRow + 1)).setValue("Unread email count:");
  sheet.getRange("B" + (summaryRow + 1)).setValue(data.length);

  Logger.log("Email aggregation complete: " + data.length + " items");
}

Please sync with clasp push.

### Step 6-3: Production deploy with clasp deploy

cd ~/ai-agent-camp/gas-example
clasp push
clasp deploy --description "Email aggregation v1"

Verify that the deploy ID is displayed.
Run aggregateEmailStats in the GAS editor and verify it outputs to the spreadsheet.
```

**Expected result:** You can check email data locally with gogcli, GAS aggregates the same email data into a spreadsheet, and clasp deploy completes the production deployment.

**Practical exercise: Retrieve emails with gogcli -> Aggregate with GAS -> Output to Sheets -> clasp deploy**

Let's practice the following workflow:
1. Retrieve the unread email list locally with `gog gmail search "is:unread" --json`
2. Run GAS `aggregateEmailStats()` to aggregate in the spreadsheet
3. Compare gogcli output with GAS output to verify data consistency
4. Deploy to production with `clasp push && clasp deploy --description "email-aggregation-v1"`
5. Set up a trigger on the deployed script for automatic daily morning execution

> **Hint**: This pipeline is a very commonly used pattern in practice.
> - **gogcli**: Quickly check and debug data locally
> - **GAS**: Scheduled execution and automation in the cloud
> - **clasp**: Local development -> cloud deployment CI/CD flow

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
      {"id": "trouble_1", "label": "Sheet not found"},
      {"id": "trouble_2", "label": "Invalid range"},
      {"id": "trouble_3", "label": "Permission denied for Gmail"},
      {"id": "trouble_4", "label": "Cannot write data"},
      {"id": "trouble_5", "label": "clasp deploy fails"},
      {"id": "trouble_6", "label": "gogcli authentication error (gog gmail search fails)"}
    ]
  }]
}
```


### Issue 1: "Sheet not found"
**Cause:** Sheet name does not exist
**Solution prompt:**
```
Please run getAllSheets() to check existing sheet names.
Verify that the sheet name spelling is correct.
```

### Issue 2: "Invalid range"
**Cause:** Range specification format is invalid
**Solution prompt:**
```
Please verify the range specification in A1:C10 format.
Check the valid range with getLastRow() and getLastColumn().
```

### Issue 3: "Permission denied for Gmail"
**Cause:** Gmail API permissions are missing
**Solution prompt:**
```
Please enable the Gmail API in the GAS editor.
Show how to add Gmail scopes to appsscript.json.
```

### Issue 4: Cannot write data
**Cause:** Sheet is protected or array sizes do not match
**Solution prompt:**
```
Please check the sheet protection settings.
Verify that the row and column counts of the data array to write are correct.
```

### Issue 5: clasp deploy fails
**Cause:** Missing deploy permissions or appsscript.json is misconfigured
**Solution prompt:**
```
Please check existing deployments with clasp deployments.
Verify that the required oauthScopes are set in appsscript.json.
Check the authentication status with clasp login --status.
```

### Issue 6: gogcli authentication error
**Cause:** gogcli authentication is incomplete or token has expired
**Solution prompt:**
```
Please check the authentication status with gog auth status.
If authentication has expired, re-authenticate with gog auth login.
Refer to 4-1 to complete the gogcli setup.
```

---

## ✅ Checkpoint
- [ ] Can access the spreadsheet
- [ ] Can read data
- [ ] Can write data
- [ ] Report generation is working
- [ ] Automation trigger can be configured
- [ ] Email notifications are sent
- [ ] Can retrieve email data with gogcli (`gog gmail search "is:unread" --json`)
- [ ] GAS email aggregation is output to the spreadsheet
- [ ] Production deployment succeeds with `clasp deploy`


---

## 📋 Deliverable Preview

### Expected Output
```
📁 output/gas/
└── Code.gs  (GAS script)
```

### Verification Commands
```bash
# Check local script files
ls -la output/gas/

# Check the beginning of script contents
head -30 output/gas/Code.gs

# Verify in GAS editor
clasp open
```

---

## ✅ Completion Check
Paste the following into chat to verify completion:

```
# Completion check: Verify that test data and report sheets have been created in Google Sheets, GAS functions (after clasp push) work correctly, and clasp deploy has succeeded.
```

**Expected result:** Completion/incomplete status and missing items are displayed.

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
      {"id": "next_window", "label": "Start in new window (/start-11-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-11-1
- finish → End

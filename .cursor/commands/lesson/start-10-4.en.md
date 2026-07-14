---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module10-gas"
duration: "~25 min"
prerequisites: ["start-10-1"]
level: "intermediate"
tags: ["gas", "gmail", "sheets", "automation", "clasp"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 10-4: GmailApp Email Search/Extraction → Sheet Organization

## 📍 What You'll Do

**Lesson 10-4: GmailApp Email Search/Extraction → Sheet Organization**!

| Item | Details |
|------|------|
| Goal | Search and extract emails with GAS GmailApp, then automatically organize them in a spreadsheet |
| Duration | ~25 min |
| Skills used | GAS (GmailApp, SpreadsheetApp), clasp |
| Prerequisites | Lesson 10-1 completed (clasp authenticated) |

**Session flow:**
1. Add Gmail scope to appsscript.json
2. Search emails with GmailApp.search()
3. Extract info from threads/messages
4. Write data to a sheet with SpreadsheetApp
5. Set up a scheduled trigger

By the end of this session, you'll have a complete GAS script that automatically searches, extracts, and organizes emails in a spreadsheet.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume.

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
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Verify Lesson 10-1 completion. Check auth status with `clasp login --status`)
(different_lesson → Display module list)

---

## 🚀 Step 1: Add Gmail Scope to appsscript.json

```json
{
  "title": "🚀 Step 1: Add Gmail Scope",
  "questions": [{
    "id": "step_action",
    "prompt": "Add the Gmail read scope to appsscript.json.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review current appsscript.json"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Add the following to `oauthScopes` in `gas-example/appsscript.json`:

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/script.scriptapp"
  ]
}
```

After adding, deploy with `clasp push`:

```bash
cd gas-example && npx -y @google/clasp push
```

**Expected result:** The `gmail.readonly` scope is added to `appsscript.json` and the push succeeds.

---

## 🚀 Step 2: Search Emails with GmailApp.search()

```json
{
  "title": "🚀 Step 2: Email Search",
  "questions": [{
    "id": "step_action",
    "prompt": "Create a function that searches emails using GmailApp.search().",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review Gmail search query syntax"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Create the `searchEmails` function in `gas-example/Gmail.gs`:

```javascript
function searchEmails(query, maxResults) {
  query = query || "is:unread newer_than:7d";
  maxResults = maxResults || 50;
  var threads = GmailApp.search(query, 0, maxResults);
  Logger.log("Search results: " + threads.length + " threads");
  return threads;
}
```

**Gmail search query examples:**

| Query | Meaning |
|--------|------|
| `is:unread` | Unread emails |
| `newer_than:7d` | Within the last 7 days |
| `from:example@company.com` | From a specific sender |
| `subject:meeting` | Subject contains "meeting" |
| `has:attachment` | Has attachments |
| `is:unread newer_than:3d` | Combined conditions |

Run `clasp push` → `clasp open` to open the GAS editor, then execute `searchEmails` and check the logs.

**Expected result:** The number of matching threads is displayed in the logs.

---

## 🚀 Step 3: Extract Email Information

```json
{
  "title": "🚀 Step 3: Extract Email Info",
  "questions": [{
    "id": "step_action",
    "prompt": "Extract email information (sender, subject, date, body) from threads.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review the GmailMessage API"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Add the `extractEmailData` function:

```javascript
function extractEmailData(threads) {
  var data = [];
  threads.forEach(function(thread) {
    var messages = thread.getMessages();
    var lastMessage = messages[messages.length - 1];
    data.push({
      subject: lastMessage.getSubject(),
      from: lastMessage.getFrom(),
      date: lastMessage.getDate(),
      body: lastMessage.getPlainBody().substring(0, 200),
      isUnread: lastMessage.isUnread(),
      messageCount: messages.length
    });
  });
  return data;
}
```

**Key methods:**

| Method | Returns |
|---------|---------|
| `getSubject()` | Subject |
| `getFrom()` | Sender |
| `getDate()` | Date/time |
| `getPlainBody()` | Body (plain text) |
| `isUnread()` | Whether the email is unread |
| `getMessages().length` | Number of messages in the thread |

**Expected result:** Email information is extracted as an array of objects.

---

## 🚀 Step 4: Write Data to a Spreadsheet

```json
{
  "title": "🚀 Step 4: Write to Sheet",
  "questions": [{
    "id": "step_action",
    "prompt": "Write the extracted email data to a spreadsheet.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review the SpreadsheetApp API"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Add the `writeToSheet` function and the main function `extractAndOrganizeEmails`:

```javascript
function writeToSheet(data, sheetName) {
  sheetName = sheetName || "Email_List_" + Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyy-MM-dd");
  var ss = SpreadsheetApp.create(sheetName);
  var sheet = ss.getActiveSheet();

  // Header row
  var headers = ["Subject", "From", "Date", "Body (first 200 chars)", "Status", "Message Count"];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");

  // Data rows
  if (data.length > 0) {
    var rows = data.map(function(item) {
      return [
        item.subject, item.from,
        Utilities.formatDate(item.date, "Asia/Tokyo", "yyyy-MM-dd HH:mm"),
        item.body, item.isUnread ? "Unread" : "Read", item.messageCount
      ];
    });
    sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
  }

  Logger.log("Sheet created: " + ss.getUrl());
  return ss.getUrl();
}

function extractAndOrganizeEmails() {
  var threads = searchEmails("is:unread newer_than:7d", 50);
  var data = extractEmailData(threads);
  var url = writeToSheet(data);
  Logger.log("Complete: " + data.length + " emails organized into a sheet");
}
```

Run `clasp push` → `clasp open` and execute `extractAndOrganizeEmails`.

**Expected result:** A spreadsheet named "Email_List_YYYY-MM-DD" is created in Google Drive, containing the organized email information.

---

## 🚀 Step 5: Set Up a Scheduled Trigger

```json
{
  "title": "🚀 Step 5: Trigger Setup",
  "questions": [{
    "id": "step_action",
    "prompt": "Set up a trigger to automatically run email organization daily at 9 AM.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review the ScriptApp.newTrigger specification"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

```javascript
function setEmailExtractTrigger() {
  // Delete existing triggers
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    if (trigger.getHandlerFunction() === "extractAndOrganizeEmails") {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Create a new trigger
  ScriptApp.newTrigger("extractAndOrganizeEmails")
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();

  Logger.log("Daily 9 AM trigger has been set");
}
```

Run `clasp push` → `clasp open` and execute `setEmailExtractTrigger`.

**Expected result:** A time-driven trigger set for daily at 9 AM appears in the GAS editor's "Triggers" screen.

---

## ⚠️ Common Issues and Solutions

```json
{
  "title": "⚠️ Troubleshooting",
  "questions": [{
    "id": "trouble",
    "prompt": "Are you experiencing any issues?",
    "options": [
      {"id": "trouble_1", "label": "Gmail permission error"},
      {"id": "trouble_2", "label": "Spreadsheet not created"},
      {"id": "trouble_3", "label": "Characters are garbled"},
      {"id": "trouble_4", "label": "Trigger not working"}
    ]
  }]
}
```

### Issue 1: "Gmail permission error"
**Cause**: The `gmail.readonly` scope has not been added to `appsscript.json`, or the initial authorization was not completed.
**Solution prompt:**
```text
Check whether "https://www.googleapis.com/auth/gmail.readonly" is included in oauthScopes in appsscript.json. If not, add it and run clasp push. On the first run, execute the function in the GAS editor and complete the authorization dialog.
```

### Issue 2: "Spreadsheet not created"
**Cause**: Missing `spreadsheets` scope, or the email search returned 0 results.
**Solution prompt:**
```text
Check whether "https://www.googleapis.com/auth/spreadsheets" is in oauthScopes. Also try broadening the search query to "newer_than:30d" and re-run.
```

### Issue 3: "Characters are garbled"
**Cause**: Encoding issue with `getPlainBody()`.
**Solution prompt:**
```text
Try using getBody() instead of getPlainBody(), and add a helper function to strip HTML tags.
```

### Issue 4: "Trigger not working"
**Cause**: Insufficient trigger permissions, or the script has errors.
**Solution prompt:**
```text
Check the error logs in the GAS editor's "Executions" screen. Also verify that the ScriptApp scope is included in appsscript.json.
```

---

## ✅ Checkpoint

- [ ] Gmail scope has been added to `appsscript.json`
- [ ] `searchEmails` function can search emails
- [ ] `extractEmailData` function can extract sender, subject, date, and body
- [ ] `extractAndOrganizeEmails` generates a spreadsheet
- [ ] A scheduled trigger has been set up

---

## 📋 Deliverable Preview

**Files created:**
```text
gas-example/
├── appsscript.json   # Gmail scope added
├── Calendar.gs       # Lesson 10-2 deliverable
├── Sheets.gs         # Lesson 10-3 deliverable
└── Gmail.gs          # This lesson's deliverable (5 functions)
```

**Generated spreadsheet:**

| Subject | From | Date | Body (first 200 chars) | Status | Message Count |
|------|--------|------|---------------------|------|-------------|
| Weekly Report | alice@co.com | 2026-04-14 10:30 | Hello. This week's... | Unread | 3 |
| Meeting Minutes | bob@co.com | 2026-04-13 15:00 | Today's meeting... | Read | 1 |

---

## ➡️ Next Steps

```json
{
  "title": "➡️ Next Steps",
  "questions": [{
    "id": "next_step",
    "prompt": "What would you like to do next?",
    "options": [
      {"id": "next_auto", "label": "Move on to Module 11 (GitHub Actions) → /start-11-1"},
      {"id": "review_module", "label": "Review Module 10 deliverables"},
      {"id": "finish", "label": "Finish for today"}
    ]
  }]
}
```

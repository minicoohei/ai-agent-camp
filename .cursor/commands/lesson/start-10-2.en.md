---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module10-gas"
prerequisites: ["start-10-1"]
duration: "~30 min"
level: "intermediate"
tags: ["gas", "calendar", "google", "automation"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 10-2: Spreadsheet Automation with GAS

## 📍 What You'll Do

**Lesson 10-2: GAS and Google Calendar Integration**!

| Item | Details |
|------|------|
| Goal | Automate event operations from GAS using the Google Calendar API |
| Duration | ~30 min |
| Skills used | gas-clasp-ops, Google Calendar API, gogcli |
| Prerequisites | Lesson 10-1 completed, GAS project created, Apps Script API enabled |
| Course page | [Module 10: GAS](https://ai-agent.camp/en/course/module-10)  alongside this lesson |

**Session flow:**
1. Create a calendar retrieval script
2. Create, update, and delete events
3. Configure triggers and notifications

By the end of this session, you will be able to automate calendar integration.

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

## 🚀 Step 1: Calendar Retrieval Script

**Prerequisite check (auto-run):**
Verify the following before proceeding:

1. **Check for `.clasp.json`**: Verify that `gas-example/.clasp.json` exists. If not, complete 4-1 first.
2. **Verify Apps Script API is enabled**: Check that "Google Apps Script API" is ON at https://script.google.com/home/usersettings.
3. **`appsscript.json` oauthScopes configuration**: Add the following scopes to `gas-example/appsscript.json` to use the Calendar API:

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/script.external_request"
  ]
}
```

> **Important**: If oauthScopes are not configured, a "Permission denied" error will occur when calling the Calendar API.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Calendar Retrieval Script",
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
Please create a Calendar.gs file in the gas-example directory with the following content:

function getDefaultCalendar() {
  const calendar = CalendarApp.getDefaultCalendar();
  Logger.log("Calendar name: " + calendar.getName());
  Logger.log("Calendar ID: " + calendar.getId());
  return calendar;
}

function getAllCalendars() {
  const calendars = CalendarApp.getAllCalendars();
  Logger.log("Total calendars: " + calendars.length);
  calendars.forEach(calendar => {
    Logger.log("- " + calendar.getName());
  });
  return calendars;
}

Please sync with clasp push.
```

**Expected result:** Calendar.gs is synced to Google Drive, and you can retrieve the calendar list.

---

## 🚀 Step 2: Event Creation Function

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Event Creation Function",
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
Please add the following event creation function to Calendar.gs:

function createSimpleEvent(title, startTime, endTime) {
  const calendar = CalendarApp.getDefaultCalendar();
  const event = calendar.createEvent(title, startTime, endTime);
  Logger.log("Event created: " + title);
  Logger.log("Event ID: " + event.getId());
  return event.getId();
}

function createTomorrowEvent() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  const startTime = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 14, 0, 0);
  const endTime = new Date(startTime.getTime() + 60 * 60 * 1000);

  return createSimpleEvent("Test Event", startTime, endTime);
}

Please clasp push and run createTomorrowEvent in the GAS editor.
```

**Expected result:** A one-hour "Test Event" starting at 14:00 tomorrow is added to the calendar.

---

## 🚀 Step 3: Get Event List

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Get Event List",
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
Please add the following event retrieval function to Calendar.gs:

function getTodayEvents() {
  const calendar = CalendarApp.getDefaultCalendar();
  const today = new Date();
  const dayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 0, 0, 0);
  const dayEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59, 59);

  const events = calendar.getEvents(dayStart, dayEnd);
  Logger.log("Today's event count: " + events.length);

  events.forEach(event => {
    Logger.log("- " + event.getTitle() + " (" + event.getStartTime().toLocaleString() + ")");
  });

  return events;
}

Please clasp push and run.
```

**Expected result:** Today's calendar event list is displayed in the log.

---

## 🚀 Step 4: Scheduled Trigger Setup

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Scheduled Trigger Setup",
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
Please add the following trigger setup function to Calendar.gs:

function dailyMorningTask() {
  const events = getTodayEvents();
  Logger.log("Today's events: " + events.length + " items");
  // Add email notification processing here
}

function createDailyTrigger() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));

  // Create a trigger to run daily at 9:00
  ScriptApp.newTrigger("dailyMorningTask")
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();

  Logger.log("Daily 9:00 trigger has been set");
}

Please clasp push and run createDailyTrigger.
```

**Expected result:** A trigger that runs automatically at 9 AM daily is configured.

---

## 🚀 Step 5: gogcli x GAS Integration - Calendar Data Retrieval and Transcription

> **Key point**: Using gogcli configured in 4-1, you will experience a workflow of retrieving calendar data locally and auto-transferring it to a spreadsheet with GAS. By combining gogcli (local CLI) and GAS (cloud execution), you can build flexible data pipelines.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: gogcli x GAS Integration",
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
Integrate gogcli with GAS to automatically transfer calendar information to a spreadsheet.

### Step 5-1: Retrieve calendar data with gogcli

gog calendar list --days 7 --json > ~/ai-agent-camp/gas-example/calendar_data.json

Please check the contents of the retrieved JSON file.

### Step 5-2: Load calendar data in GAS and transfer to sheet

Please add the following function to Calendar.gs:

function importCalendarDataToSheet() {
  // Image of transferring JSON data obtained via gogcli to a spreadsheet
  // In practice, there are two patterns: directly retrieving via CalendarApp from GAS linked to a spreadsheet,
  // or manually/automatically pasting gogcli output to the sheet

  const calendar = CalendarApp.getDefaultCalendar();
  const now = new Date();
  const weekLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  const events = calendar.getEvents(now, weekLater);

  // Write to spreadsheet
  const ss = SpreadsheetApp.create("Calendar Weekly Report");
  const sheet = ss.getActiveSheet();

  // Header
  sheet.getRange("A1:E1").setValues([["Title", "Start Time", "End Time", "Location", "Description"]]);

  // Event data
  const data = events.map(event => [
    event.getTitle(),
    event.getStartTime().toLocaleString("ja-JP"),
    event.getEndTime().toLocaleString("ja-JP"),
    event.getLocation() || "",
    event.getDescription() || ""
  ]);

  if (data.length > 0) {
    sheet.getRange(2, 1, data.length, 5).setValues(data);
  }

  Logger.log("Calendar data transfer complete: " + data.length + " items");
  Logger.log("Spreadsheet URL: " + ss.getUrl());
  return ss.getUrl();
}

Please clasp push and run importCalendarDataToSheet in the GAS editor.
```

**Expected result:** You can retrieve calendar JSON locally with gogcli, and GAS can also transfer the same calendar data to a spreadsheet.

**Practical exercise: Auto-transfer calendar data retrieved with gogcli to a spreadsheet using GAS**

Let's practice the following workflow:
1. Retrieve this week's schedule with `gog calendar list --days 7 --json`
2. Check the structure of the output JSON (title, date/time, location, etc.)
3. Run GAS `importCalendarDataToSheet()` to transfer the same data to the spreadsheet
4. Compare gogcli output with GAS output to verify data consistency

> **Hint**: gogcli is a local CLI, making it easy to integrate with CI/CD and scripts. On the other hand, GAS can run periodically (via triggers) in the cloud. By combining both, you can achieve a development flow of local verification -> cloud automation.

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
      {"id": "trouble_1", "label": "Calendar not found"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Event not found"},
      {"id": "trouble_4", "label": "Triggers do not work"},
      {"id": "trouble_5", "label": "Apps Script API has not been used / is not enabled"},
      {"id": "trouble_6", "label": "gogcli authentication error (gog calendar list fails)"}
    ]
  }]
}
```


### Issue 1: "Calendar not found"
**Cause:** Calendar ID is invalid or access permissions are missing
**Solution prompt:**
```
Please run getAllCalendars() and check the list of accessible calendars.
Verify that the calendar ID is correct.
```

### Issue 2: "Permission denied"
**Cause:** Calendar API permissions have not been granted
**Solution prompt:**
```
Please add the Google Calendar API from "Services" in the GAS editor.
Also show how to add oauthScopes to appsscript.json.
```

### Issue 3: "Event not found"
**Cause:** Event ID does not exist or has been deleted
**Solution prompt:**
```
Please add a null check before getEventById and implement error handling for when the event does not exist.
```

### Issue 4: Triggers do not work
**Cause:** Trigger does not have execution permissions
**Solution prompt:**
```
Please check the trigger status from the "Triggers" menu in the GAS editor.
If there are error logs, provide the details.
```

### Issue 5: "Apps Script API has not been used in project / User has not enabled the Apps Script API"
**Cause:** Google Apps Script API is disabled
**Resolution steps**:
1. Go to https://script.google.com/home/usersettings
2. Switch the "Google Apps Script API" toggle to **ON**
3. After the change, redo from `clasp login`

> This setting is per Google account. Once enabled, it can be used for all subsequent GAS projects.

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
- [ ] Calendar retrieval is working
- [ ] Event creation is working
- [ ] Event list retrieval is working
- [ ] Trigger has been configured
- [ ] Scheduled execution is working
- [ ] Can retrieve calendar data with gogcli (`gog calendar list --days 7 --json`)
- [ ] GAS can transfer calendar data to a spreadsheet


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
# Completion check: Please verify the following.
# 1. gas-example/Calendar.gs exists
# 2. appsscript.json has oauthScopes (calendar, script.external_request) configured
# 3. clasp push succeeds (run in gas-example directory)
# 4. Running getDefaultCalendar() in the GAS editor displays the calendar name
# 5. createTomorrowEvent() creates an event in the calendar
```

**Expected result:** All checklist items pass, and you can operate events using the Google Calendar API from GAS.

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
      {"id": "next_window", "label": "Start in new window (/start-10-3)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-10-3
- finish → End

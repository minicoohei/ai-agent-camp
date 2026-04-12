---
description: "When the user says /start-4-3 — Module 4 Lesson 4-3: Google Calendar Operations"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~25 min"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "calendar"]
---

# 🎓 Lesson 4-3: Google Calendar Operations

## 📍 What You'll Do

**Lesson 4-3: Google Calendar Operations** !

| Item | Details |
|------|---------|
| Goal | List, create, and update calendar events using gogcli |
| Duration | ~25 min |
| Skills Used | gogcli calendar |
| Prerequisites | gogcli authentication setup completed (start-4-1 done) |

**Session flow:**
1. List today's and this week's events
2. Create new events
3. Set up recurring meetings automatically

By the end of this session, you will be able to view and create calendar events using gogcli.

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

## 🚀 Step 1: List Today's and This Week's Events

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Display event list",
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

Let's check the calendar events:

```bash
# Today's events
gog calendar list --account your-email@gmail.com --days 1

# This week's events (7 days)
gog calendar list --account your-email@gmail.com --days 7

# Get calendar list (check available calendar IDs)
gog calendar calendars --account your-email@gmail.com
```

**Expected result**: Event titles, start times, end times, and locations (if set) are listed.

> **💡 Hint**: `--days` retrieves events for the specified number of days. The default calendar is `primary`.

**Advanced: AI-powered schedule analysis**

Pass the retrieved event list to the AI for analysis:
```text
Analyze this week's schedule above:
1. Identify available time slots
2. Identify days with concentrated meetings
3. Calculate meeting time per day
```

---

## 🚀 Step 2: Create New Events

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Create events",
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

Create new calendar events:

```bash
# Basic event creation
gog calendar create primary --account your-email@gmail.com \
  --summary "AI Study Session" \
  --from "2026-03-15T14:00:00+09:00" \
  --to "2026-03-15T15:00:00+09:00"

# Event creation with location and description
gog calendar create primary --account your-email@gmail.com \
  --summary "Team Meeting" \
  --from "2026-03-16T10:00:00+09:00" \
  --to "2026-03-16T11:00:00+09:00" \
  --location "Meeting Room A" \
  --description "Weekly progress update"
```

**Expected result**: Events are created and reflected in Google Calendar. Event IDs are returned.

> **⚠️ Warning**: Specify dates and times in ISO 8601 format (`YYYY-MM-DDTHH:MM:SS+09:00`). Including the timezone offset (e.g., `+09:00`) is recommended.

---

## 🚀 Step 3: Automated Setup of Recurring Meetings

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Automatic Setup of Recurring Meetings",
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

Let's use AI to create multiple events in batch. Enter the following prompt in Cursor:

```text
Use the gog calendar create command to create the following recurring meetings:

1. Every Monday 10:00-10:30 "Weekly Team Standup" (4 weeks starting next week)
2. Every Wednesday 14:00-15:00 "Project Progress Meeting" (4 weeks starting next week)
3. Every Friday 17:00-17:30 "Weekly Retrospective" (4 weeks starting next week)

Account: your-email@gmail.com
Also add an appropriate description to each event.
```

**Example of AI-generated commands:**
```bash
# Monday morning meeting (4 weeks)
gog calendar create primary --account your-email@gmail.com --summary "Weekly Team Standup" --from "2026-03-16T10:00:00+09:00" --to "2026-03-16T10:30:00+09:00" --description "Weekly team kickoff"
gog calendar create primary --account your-email@gmail.com --summary "Weekly Team Standup" --from "2026-03-23T10:00:00+09:00" --to "2026-03-23T10:30:00+09:00" --description "Weekly team kickoff"
# ... and so on
```

**Expected result**: 12 events (3 types x 4 weeks) are registered in the calendar. Check them in Google Calendar.

> **💡 Hint**: By delegating to AI, you can automate repetitive manual tasks. This is the true power of using AI assistants.

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
      {"id": "trouble_1", "label": "Events are not displayed"},
      {"id": "trouble_2", "label": "Date/time format error"},
      {"id": "trouble_3", "label": "Do not know the calendar ID"},
      {"id": "trouble_4", "label": "Created events are not reflected"}
    ]
  }]
}
```

### Issue 1: "Events are not displayed"
**Cause**: No events in the target period, or the calendar ID is different
**Solution prompt**:
```text
Try a larger --days value (e.g., --days 30).
Also check available calendars with gog calendar calendars.
```

### Issue 2: "Date/time format error"
**Cause**: Not in ISO 8601 format
**Solution prompt**:
```text
Specify date/time in "YYYY-MM-DDTHH:MM:SS+09:00" format.
Example: "2026-03-15T14:00:00+09:00"
Put "T" between date and time, and include the timezone offset.
```

### Issue 3: "Do not know the calendar ID"
**Cause**: When there are multiple calendars
**Solution prompt**:
```text
List with gog calendar calendars --account your-email@gmail.com
and check the target calendar ID.
The main calendar is usually "primary".
```

### Issue 4: "Created events are not reflected"
**Cause**: API response delay, or calendar cache
**Solution prompt**:
```text
Check with gog calendar list. Reload the browser on the Google Calendar web page.
There may be a delay of a few seconds.
```

---

## ✅ Checkpoint
- [ ] Was able to retrieve today's and this week's event listings
- [ ] Was able to confirm the calendar list (calendar IDs)
- [ ] Was able to create new events (with location and description)
- [ ] Was able to batch create recurring meetings using AI


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
Run the following commands to verify Calendar operations work correctly:
1. gog calendar list --account <your-email> --days 7
2. Verify the results include events created in this lesson
Verify that all commands work correctly.
```

**Expected result**: Created events are displayed in the listing.

---

## 🎉 Next Steps

Google Calendar operations are now complete! In the next lesson, you will learn Google Drive operations.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/start-4-4)"},
      {"id": "next_window", "label": "Start in new window (/start-4-4)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /start-4-4（Google Drive Operations)
- next_window → Open new window with /start-4-4
- finish → End

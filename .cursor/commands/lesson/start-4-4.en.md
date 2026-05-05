---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-4-3"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "calendar", "event-management"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 4-4: Google Calendar Event Registration and Management

## 📍 What You'll Do

**Lesson 4-4: Google Calendar Event Registration and Management** !

| Item | Details |
|------|---------|
| Goal | Create, manage attendees, set recurrence, and delete calendar events using gogcli |
| Duration | ~30 min |
| Skills Used | gogcli calendar create / delete |
| Prerequisites | Google Calendar basics completed (start-4-3 done) |

**Session flow:**
1. Create a simple event
2. Create events with attendees and Google Meet
3. Set up recurring events (recurrence rules)
4. Delete and manage events
5. Practical exercise: batch register a weekly schedule

By the end of this session, you will be able to freely create and manage calendar events using gogcli.

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
(check_prereq → `gog auth list`  to check auth status、start-4-3 completion)
(different_lesson → Show module list)

---

## 🚀 Step 1: Simple Event Creation

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Simple event creation",
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

Let's create a basic event:

```bash
# Simple event creation (title, start, and end only)
gog calendar create primary --account your-email@gmail.com \
  --summary "AI Study Session" \
  --from "2026-03-20T14:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00"

# Event creation with description and location
gog calendar create primary --account your-email@gmail.com \
  --summary "AI Study Session" \
  --from "2026-03-20T14:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00" \
  --description "Study session on Claude Code usage. Materials shared in advance." \
  --location "Conference Room B"
```

**Expected result**: Events are created and reflected in Google Calendar. Event IDs are returned.

> **⚠️ Warning**: Specify dates and times in RFC3339 format (`YYYY-MM-DDTHH:MM:SS+09:00`). Always include the timezone offset (e.g., `+09:00`).

---

## 🚀 Step 2: Events with Attendees and Google Meet

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Events with attendees and Google Meet",
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

Create events that invite attendees and auto-generate Google Meet links:

```bash
# Event with attendees and Google Meet
gog calendar create primary --account your-email@gmail.com \
  --summary "Team Meeting" \
  --from "2026-03-20T10:00:00+09:00" \
  --to "2026-03-20T11:00:00+09:00" \
  --attendees "colleague@company.com" \
  --with-meet

# Specify multiple attendees separated by commas
gog calendar create primary --account your-email@gmail.com \
  --summary "Project Kickoff" \
  --from "2026-03-21T13:00:00+09:00" \
  --to "2026-03-21T14:30:00+09:00" \
  --attendees "member1@company.com,member2@company.com,member3@company.com" \
  --with-meet \
  --description "New project kickoff meeting" \
  --location "Online"

# With visibility settings and notification options
gog calendar create primary --account your-email@gmail.com \
  --summary "All-hands Meeting" \
  --from "2026-03-22T15:00:00+09:00" \
  --to "2026-03-22T16:00:00+09:00" \
  --attendees "team@company.com" \
  --with-meet \
  --visibility public \
  --send-updates all
```

**Expected result**: Events are created, invitation emails are sent to attendees, and Google Meet links are auto-generated.

> **💡 Hint**: The `--send-updates` option controls who receives invitation notifications (`all`=everyone, `externalOnly`=external only, `none`=no notifications).

---

## 🚀 Step 3: Recurring Events (Recurrence Rules)

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Recurring events (recurrence rules)",
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

Use the `--rrule` option to specify recurrence rules (RFC 5545 RRULE):

```bash
# Weekly Monday recurring event (12 times)
gog calendar create primary --account your-email@gmail.com \
  --summary "Weekly Standup" \
  --from "2026-03-23T10:00:00+09:00" \
  --to "2026-03-23T11:00:00+09:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=12"

# Monthly first Monday review (6 times)
gog calendar create primary --account your-email@gmail.com \
  --summary "Monthly Review" \
  --from "2026-04-06T14:00:00+09:00" \
  --to "2026-04-06T15:30:00+09:00" \
  --rrule "RRULE:FREQ=MONTHLY;BYDAY=1MO;COUNT=6" \
  --attendees "manager@company.com" \
  --with-meet

# All-day event (--all-day option)
gog calendar create primary --account your-email@gmail.com \
  --summary "Team Offsite" \
  --from "2026-04-10" \
  --to "2026-04-11" \
  --all-day \
  --description "Q2 Team Offsite (2 days / 1 night)"
```

**Common RRULE patterns:**

| Pattern | RRULE | Description |
|---------|-------|------|
| Every Monday | `FREQ=WEEKLY;BYDAY=MO;COUNT=12` | 12 weeks |
| Every Tue/Thu | `FREQ=WEEKLY;BYDAY=TU,TH;COUNT=24` | 12 weeks (twice/week) |
| 1st of each month | `FREQ=MONTHLY;BYMONTHDAY=1;COUNT=6` | 6 months |
| 2nd Wed of each month | `FREQ=MONTHLY;BYDAY=2WE;COUNT=6` | 6 months |
| Every weekday | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=20` | 4 weeks |

> **💡 Hint**: `COUNT` specifies the number of repetitions, and `UNTIL` specifies the end date. If `COUNT` is omitted, the event repeats indefinitely, so be careful.

---

## 🚀 Step 4: Event Deletion and Management

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Event deletion and management",
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

Manage and delete created events:

```bash
# Delete event (eventId returned during creation)
gog calendar delete primary <eventId> --account your-email@gmail.com --force

# Check ID from event list and delete
gog calendar list --account your-email@gmail.com --days 7
# Delete using the event ID shown above
```

**Useful options when creating events:**

```bash
# Specify event color (number 1-11)
gog calendar create primary --account your-email@gmail.com \
  --summary "Important Task" \
  --from "2026-03-20T09:00:00+09:00" \
  --to "2026-03-20T10:00:00+09:00" \
  --event-color 11

# Focus time (deep work time)
gog calendar create primary --account your-email@gmail.com \
  --summary "Focus Time" \
  --from "2026-03-20T13:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00" \
  --event-type focus-time

# Out of Office setting
gog calendar create primary --account your-email@gmail.com \
  --summary "Vacation" \
  --from "2026-03-25T00:00:00+09:00" \
  --to "2026-03-26T00:00:00+09:00" \
  --event-type out-of-office
```

**Event color number reference:**

| Number | Color | Example use |
|------|-----|-------|
| 1 | Lavender | Personal |
| 2 | Sage | Learning |
| 4 | Flamingo | Important |
| 5 | Banana | Caution |
| 9 | Blueberry | Meeting |
| 11 | Tomato | Urgent |

> **💡 Hint**: The `--force` flag deletes without confirmation. Note that deleting a recurring event deletes the entire series.

---

## 🚀 Step 5: Hands-on Exercise (Batch Register a Week's Schedule)

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Hands-on exercise",
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

Let's combine the features you've learned to batch register a weekly schedule. Enter the following prompt in Cursor:

```text
Use the gog calendar create command to create the following weekly schedule:

1. Every morning 9:00-9:15 "Morning Standup" (Mon-Fri, with --with-meet, using --rrule)
2. Monday 10:00-12:00 "Focus Time" (--event-type focus-time)
3. Tuesday 14:00-15:00 "1-on-1 Meeting" (attendee: manager@company.com, with --with-meet)
4. Wednesday 15:00-16:00 "Team Study Session" (--description "AI use case sharing", --event-color 2)
5. Friday 17:00-17:30 "Weekly Retrospective" (--attendees "team@company.com", with --with-meet)

Account: your-email@gmail.com
Start date: next Monday
Please also add appropriate descriptions to each event.
```

**Example of AI-generated commands:**
```bash
# 1. Morning standup (recurring)
gog calendar create primary --account your-email@gmail.com \
  --summary "Morning Standup" \
  --from "2026-03-23T09:00:00+09:00" \
  --to "2026-03-23T09:15:00+09:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=5" \
  --with-meet \
  --description "Daily progress sharing (15 min)"

# 2. Focus time
gog calendar create primary --account your-email@gmail.com \
  --summary "Focus Time" \
  --from "2026-03-23T10:00:00+09:00" \
  --to "2026-03-23T12:00:00+09:00" \
  --event-type focus-time \
  --description "Focus work time. Set Slack to DND."

# 3. 1-on-1 meeting
gog calendar create primary --account your-email@gmail.com \
  --summary "1-on-1 Meeting" \
  --from "2026-03-24T14:00:00+09:00" \
  --to "2026-03-24T15:00:00+09:00" \
  --attendees "manager@company.com" \
  --with-meet \
  --description "1-on-1 with manager"

# 4. Team study session
gog calendar create primary --account your-email@gmail.com \
  --summary "Team Study Session" \
  --from "2026-03-25T15:00:00+09:00" \
  --to "2026-03-25T16:00:00+09:00" \
  --event-color 2 \
  --description "AI use case sharing"

# 5. Weekly retrospective
gog calendar create primary --account your-email@gmail.com \
  --summary "Weekly Retrospective" \
  --from "2026-03-27T17:00:00+09:00" \
  --to "2026-03-27T17:30:00+09:00" \
  --attendees "team@company.com" \
  --with-meet \
  --description "Share this week's results and next week's plans"
```

**Expected result**: 5 types of events are registered in the calendar. Check them in Google Calendar.

> **💡 Hint**: By delegating to AI, even complex schedule settings can be easily automated.

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
      {"id": "trouble_1", "label": "Events are not created"},
      {"id": "trouble_2", "label": "Notifications not reaching attendees"},
      {"id": "trouble_3", "label": "Recurrence rules not working correctly"},
      {"id": "trouble_4", "label": "Google Meet link not generated"}
    ]
  }]
}
```

### Issue 1: "Events are not created"
**Cause**: Incorrect calendarId specification, or date/time format error
**Solution prompt**:
```text
Verify that calendarId is correct (usually "primary").
Specify dates/times in RFC3339 format ("YYYY-MM-DDTHH:MM:SS+09:00").
You can check calendar IDs with gog calendar calendars --account your-email@gmail.com
```

### Issue 2: "Notifications not reaching attendees"
**Cause**: --send-updates option is not specified
**Solution prompt**:
```text
Add --send-updates all.
By default, notifications may not be sent.
Example: gog calendar create primary --account ... --attendees "..." --send-updates all
```

### Issue 3: "Recurrence rules not working correctly"
**Cause**: RRULE syntax error
**Solution prompt**:
```text
Check the RRULE syntax:
- The "RRULE:" prefix is required
- FREQ is mandatory (WEEKLY, MONTHLY, DAILY, etc.)
- BYDAY uses 2-letter day codes (MO, TU, WE, TH, FR, SA, SU)
- Specify end conditions with COUNT or UNTIL
Correct example: "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=12"
```

### Issue 4: "Google Meet link not generated"
**Cause**: --with-meet flag is not specified
**Solution prompt**:
```text
Add the --with-meet flag.
Example: gog calendar create primary --account ... --summary "Meeting" --with-meet
If you are not using a Google Workspace account, Meet link generation may be restricted.
```

---

## ✅ Checkpoint
- [ ] Successfully created a simple event
- [ ] Successfully created events with attendees and Meet
- [ ] Successfully set up recurring events
- [ ] Successfully deleted events
- [ ] Completed batch registration of a weekly schedule


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
Run the following commands to verify that Calendar event registration and management works correctly:
1. gog calendar list --account <your-email> --days 7
2. Verify that events created in this lesson appear in the results above
3. Verify that recurring events are set up correctly
Confirm that everything works correctly.
```

**Expected result**: Created events (simple, with attendees, recurring, focus time, etc.) are displayed in the listing.

---

## 🎉 Next Steps

Google Calendar event registration and management is now complete! In the next lesson, you will learn Google Drive operations.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/start-4-5)"},
      {"id": "next_window", "label": "Start in new window (/start-4-5)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /start-4-5（Google Drive Operations)
- next_window → Open new window with /start-4-5
- finish → End

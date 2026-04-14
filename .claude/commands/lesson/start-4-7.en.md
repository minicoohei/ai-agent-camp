---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-4-1", "start-4-2", "start-4-3", "start-4-4", "start-4-5", "start-4-6"]
level: "intermediate"
tags: ["google", "workspace", "gogcli", "workflow", "automation"]
---

# 🎓 Lesson 4-7: AI Secretary Workflow Integration

## 📍 What You'll Do

**Lesson 4-7: AI Secretary Workflow Integration** !

| Item | Details |
|------|---------|
| Goal | Build an AI secretary workflow combining Gmail+Calendar+Drive |
| Duration | ~30 min |
| Skills Used | gogcli, check-inbox, google-sync |
| Prerequisites | All Lessons 4-1 through 4-6 completed |

**Session flow:**
1. Batch sync data with google-sync
2. Extract tasks from emails with check-inbox
3. Determine priority by cross-referencing with calendar
4. Auto-generate daily reports

By the end of this session, an AI secretary workflow spanning Gmail, Calendar, and Drive will be operational.

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
      {"id": "check_prereq", "label": "I want to check prerequisites (4-1 to 4-6 completion status)"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → 4-1〜4-6 completion status)
(different_lesson → Show module list)

---

## 🚀 Step 1: Bulk Data Sync with google-sync

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Bulk data sync",
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

Use the google-sync script to batch sync Gmail, Calendar, and Drive data:

```bash
# Install google-sync dependencies
pip install -r data/google-sync/requirements.txt

# Execute data sync
python data/google-sync/scripts/sync_google.py --account your-email@gmail.com
```

**What sync_google.py does:**
1. **Gmail**: Retrieve recent emails and save in Markdown format to `data/google-sync/data/gmail/`
2. **Calendar**: Retrieve upcoming events and save to `data/google-sync/data/calendar/`
3. **Drive**: Save metadata of recently updated documents to `data/google-sync/data/docs/`

```bash
# Check sync results
ls -la data/google-sync/data/

# Check Gmail sync data
ls data/google-sync/data/gmail/ | head -10

# Check Calendar sync data
ls data/google-sync/data/calendar/
```

**Expected result**: Gmail, Calendar, and Drive data is saved in the `data/` directory.

> **💡 Hint**: If sync_google.py does not exist, you can also manually sync by combining gogcli commands. Ask the AI for alternative steps from Step 1.

**Alternative steps (direct gogcli execution):**
```bash
# Gmail: Get unread emails
mkdir -p /tmp/google-sync/gmail
gog gmail search "is:unread newer_than:7d" --account your-email@gmail.com > /tmp/google-sync/gmail/unread.txt

# Calendar: This week's events
mkdir -p /tmp/google-sync/calendar
gog calendar list --account your-email@gmail.com --days 7 > /tmp/google-sync/calendar/this_week.txt

# Drive: Recently updated files
mkdir -p /tmp/google-sync/drive
gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-07'" --max 20 > /tmp/google-sync/drive/recent.txt
```

---

## 🚀 Step 2: Extract Tasks from Email with check-inbox

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Extract tasks from email",
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

Use the check-inbox skill to automatically extract action items from emails:

```bash
# Run check-inbox script
python skills/check-inbox/scripts/check_inbox.py --account your-email@gmail.com
```

**What check-inbox does:**
1. Retrieve recent emails
2. AI analyzes email content and extracts the following:
   - **Emails requiring a reply** (priority: High/Medium/Low)
   - **Emails containing requests/tasks** (with deadlines)
   - **FYI (information sharing only)**
   - **Emails requiring follow-up**

**Alternative steps (request AI directly):**

You can also have the AI analyze email data retrieved with gogcli:

```bash
# Get unread emails
gog gmail search "is:unread newer_than:3d" --account your-email@gmail.com
```

Paste the results into Cursor chat:
```text
From the email list above, extract tasks using the following categories:

## 🔴 Urgent (within 24 hours)
- Email subject / Sender / Required action

## 🟡 Respond this week
- Email subject / Sender / Required action

## 🟢 Information only (FYI)
- Email subject / Sender / Summary

## 📋 Follow-up
- Email subject / Sender / Follow-up deadline
```

**Expected result**: Emails are classified by category and a prioritized task list is generated.

---

## 🚀 Step 3: Cross-reference with Calendar to Determine Priority

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Calendar cross-reference and priority determination",
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

Cross-reference tasks extracted in Step 2 with calendar events to determine priority:

```bash
# Get this week's calendar
gog calendar list --account your-email@gmail.com --days 7
```

Combine the retrieved calendar data with the Step 2 task list and request AI analysis:

```text
Cross-reference the following two datasets and perform an integrated priority assessment:

[Tasks extracted from email]
(Paste the Step 2 results here)

[This week's calendar]
(Paste the calendar list here)

Analyze from the following perspectives:
1. Are there tasks that need preparation right before a meeting?
2. Avoid assigning tasks on days with many meetings
3. Suggest assigning tasks to free time slots
4. Warn about tasks with approaching deadlines
5. List of things to do today in preparation for tomorrow

Output results in the following format:

## 📅 Today's To-Do (prioritized)
1. [High] Task name - Reason
2. [Med] Task name - Reason
3. [Low] Task name - Reason

## 📋 This week's To-Do (by day)
### Monday
- Task (free: recommended for 10:00-12:00)
### Tuesday
- ...

## ⚠️ Notes
- Pre-meeting preparation reminders
- Deadline warnings
```

**Expected result**: Email tasks and calendar events are integrated, and an actionable To-Do list with priorities is generated.

---

## 🚀 Step 4: Auto-generate Daily Report

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Daily report generation",
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

Integrate all data to generate a daily report. Enter the following prompt in Cursor:

```text
Run the following gogcli commands, integrate the results, and generate a daily report:

1. gog gmail search "newer_than:1d" --account your-email@gmail.com
2. gog calendar list --account your-email@gmail.com --days 1
3. gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-13'" --max 10

Create a report in the following format and save to output/reports/daily_report_2026-03-14.md:

# 📊 Daily Report: 2026-03-14

## 📧 Email Summary
- Received: X (Unread: X)
- Require reply: X
- Key emails:
  1. [Subject] from [Sender] - [One-line summary]

## 📅 Today's Schedule
| Time | Event | Location |
|------|-------|----------|
| 10:00-11:00 | xxx | xxx |

## 📁 Recently Updated Files
- [File name] - [Last modified]

## ✅ Today's To-Do (prioritized)
1. [High] xxx
2. [Med] xxx

## 📝 Notes
- Points of interest
```

**Advanced: Setting up scheduled execution**

To auto-generate daily reports every morning, use the following method:

```bash
# Combine into a shell script
cat > tools/daily_report.sh << 'SCRIPT'
#!/bin/bash
ACCOUNT="your-email@gmail.com"
DATE=$(date +%Y-%m-%d)

echo "=== Gmail ===" > /tmp/daily_data.txt
gog gmail search "newer_than:1d" --account $ACCOUNT >> /tmp/daily_data.txt

echo "=== Calendar ===" >> /tmp/daily_data.txt
gog calendar list --account $ACCOUNT --days 1 >> /tmp/daily_data.txt

echo "=== Drive ===" >> /tmp/daily_data.txt
gog drive ls --account $ACCOUNT --query "modifiedTime > '$(date -v-1d +%Y-%m-%d)'" --max 10 >> /tmp/daily_data.txt

echo "Data collection complete: /tmp/daily_data.txt"
echo "In Cursor, enter: Please read /tmp/daily_data.txt and generate a daily report"
SCRIPT
chmod +x tools/daily_report.sh
```

**Expected result**: The daily report is saved in Markdown format in `output/reports/`.

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
      {"id": "trouble_1", "label": "google-sync script does not work"},
      {"id": "trouble_2", "label": "check-inbox results in error"},
      {"id": "trouble_3", "label": "Too much data, processing takes too long"},
      {"id": "trouble_4", "label": "Want to improve report quality"}
    ]
  }]
}
```

### Issue 1: "google-sync script does not work"
**Cause**: Missing dependency packages, or script configuration
**Solution prompt**:
```text
As an alternative, collect data directly using gogcli commands.
Run the commands in the "Alternative steps" section of Step 1.
```

### Issue 2: "check-inbox results in error"
**Cause**: Insufficient skill configuration, or email data retrieval failure
**Solution prompt**:
```text
Instead of check-inbox, retrieve emails with gogcli gmail search
and ask the AI to extract tasks directly (see "Alternative steps" in Step 2).
```

### Issue 3: "Too much data, processing takes too long"
**Cause**: --max parameter is too large
**Solution prompt**:
```text
Reduce the --max value (recommended: 10-20).
Shortening the period with --query "newer_than:1d" can also speed things up.
```

### Issue 4: "Want to improve report quality"
**Cause**: Prompt improvement is needed
**Solution prompt**:
```text
Try adding the following to your prompt:
- "Business email importance criteria: Prioritize emails from managers/clients"
- "Append preparation items to each meeting event"
- "Carry over incomplete To-Do items from the previous day"
```

---

## ✅ Checkpoint
- [ ] Was able to batch collect data with google-sync (or manual gogcli commands)
- [ ] Was able to extract tasks from emails and classify by priority
- [ ] Was able to cross-reference calendar and tasks to create an integrated To-Do
- [ ] Was able to generate and save daily reports in Markdown format


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
Perform the Module 4 comprehensive check:
1. Verify Google account authentication status with gog auth list
2. Verify that daily reports have been generated in output/reports/
3. Verify that all the following gogcli commands work:
   - gog gmail search "newer_than:1d" --account <email>
   - gog calendar list --account <email> --days 1
   - gog drive ls --account <email> --max 3
```

**Expected result**: All commands work without errors and daily reports are generated.

---

## 🎉 Module 4 Complete！

Congratulations! Module 4 'Google Workspace Utilization' is now complete.

**Skills acquired:**
- gogcli installation and authentication setup
- Gmail email search, viewing, and AI analysis
- Google Calendar event management
- Google Drive file operations
- Google Sheets data retrieval and analysis
- AI secretary workflow integrating Gmail+Calendar+Drive

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_module", "label": "Proceed to Module 5 (/start-5-1)"},
      {"id": "review", "label": "Review Module 4 (/start-4-1)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_module → /start-5-1（to the next module)
- review → /start-4-1（Review Module 4 from the beginning)
- finish → End

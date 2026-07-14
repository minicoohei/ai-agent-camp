---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
prerequisites: ["start-9-1"]
duration: "~25 min"
level: "intermediate"
tags: ["slack", "task", "todo", "extraction"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 9-2: Slack Channel Summary and Report

## 📍 What You'll Do

**Lesson 9-2: Slack Task Extraction** !

| Item | Details |
|------|------|
| Goal | Extract TODOs/tasks from Slack, determine priorities, and generate task reports |
| Duration | ~25 min |
| Skills used | slack-task-manager, check-inbox |
| Prerequisites | Lesson 9-1 completed, Slack API configured |
| Course page | [Module 9: Slack Search](https://ai-agent.camp/en/course/module-9) alongside this lesson |

**Session flow:**
1. Detect mentions and action items
2. Determine priority and generate task list
3. Output and utilize task reports

By the end of this session, you will be able to automatically track pending replies and TODOs from Slack.

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

## 🚀 Step 1: Check Mentions to Yourself

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Check Mentions to Yourself",
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
Please search for mentions directed to you in Slack.
Search using the following username patterns:
- @YourName (replace with your username)
- @YourDisplayName

Summarize the mentions from the last week by channel.
```

**Expected result:** A list of mentions directed to you is displayed.

---

## 🚀 Step 2: Extract Action Items

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Extract Action Items",
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
Please extract TODOs from Slack messages using the following patterns:

Search patterns:
- "please do ~" "I request ~"
- "please confirm" "please review"
- "please handle" "urgent"
- Request messages with mentions to you

Target those within the last 2 weeks.
```

**Expected result:** Messages containing action items are extracted.

---

## 🚀 Step 3: Priority Assessment

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Priority Assessment",
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
Please assess the priority of extracted TODOs using the following criteria:

High priority:
- Contains "urgent" "today" "ASAP" "emergency"
- Mentions from executives or supervisors

Medium priority:
- Deadline is explicitly stated
- Contains "this week" "by next week"

Low priority:
- No deadline
- Information sharing only

Display the count and content for each priority level.
```

**Expected result:** TODOs are categorized by priority.

---

## 🚀 Step 4: Check Thread Replies

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Check Thread Replies",
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
Please check the thread for each extracted TODO:

Items to check:
- Whether it has been addressed (replies with "completed" "handled" etc.)
- Whether there are additional requests
- Whether it has been left without a reply

Classify TODOs by response status:
- Addressed
- In progress
- Not addressed
```

**Expected result:** The status of TODOs is determined.

---

## 🚀 Step 5: Generate Task Report

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Generate Task Report",
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
Please compile the extracted TODOs into a Markdown report in the following format:

# Slack TODO Report
Generated: (current date/time)

## Summary
- High priority: X items
- Medium priority: X items
- Low priority: X items
- Not addressed: X items

## High Priority (Details)
### 1. (Task name)
- Channel: #...
- Requester: @...
- Date/time: ...
- Content: ...
- Status: Not addressed/In progress/Completed

(continued below)

Output: ~/ai-agent-camp/output/slack_todo_report.md
```

**Expected result:** The TODO list is saved as a Markdown report.

---

## 🚀 Step 6: Automate Periodic Reports

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 6: Automate Periodic Reports",
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
Please create a Python script to automatically generate
a TODO report every Monday.

Features:
- Extract TODOs from Slack sync data
- Priority assessment and status checking
- Markdown report generation
- Diff display from previous reports

Output: ~/ai-agent-camp/tools/slack_todo_extractor.py
```

**Expected result:** A Python script for automation is created.

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
      {"id": "trouble_1", "label": "Mentions not detected"},
      {"id": "trouble_2", "label": "Japanese pattern not working"},
      {"id": "trouble_3", "label": "Cannot retrieve thread information"},
      {"id": "trouble_4", "label": "There are many TODOs"}
    ]
  }]
}
```


### Issue 1: "Mentions not detected"
**Cause:** Slack User ID format differs
**Solution prompt:**
```
Please check the Slack mention format.
Please show how to search both the User ID format like <@U12345678>
and the @DisplayName format.
```

### Issue 2: "Japanese patterns don't work"
**Cause:** Regular expression encoding issue
**Solution prompt:**
```
Japanese regular expression patterns are not working.
Please show how to search using the re.UNICODE flag.
```

### Issue 3: "Cannot retrieve thread information"
**Cause:** Thread sync is disabled
**Solution prompt:**
```
Please show how to retrieve Slack thread information.
Also show how to enable threads in the slack-sync settings.
```

### Issue 4: "Too many TODOs"
**Cause:** Insufficient filtering
**Solution prompt:**
```
There are too many TODOs to manage.
Please add the following filters:
- Narrow the date range (last 3 days)
- Show high priority only
- Target specific channels only
```

---

## ✅ Checkpoint
- [ ] Detected mentions directed to me
- [ ] Extracted messages with TODO patterns
- [ ] Determined priorities
- [ ] Confirmed thread reply status
- [ ] Generated Markdown report
- [ ] Identified unresolved tasks


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
      {"id": "next_window", "label": "Start in new window (/start-10-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-10-1
- finish → End

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
prerequisites: ["start-0-4"]
duration: "~25 min"
level: "intermediate"
tags: ["slack", "search", "bookrag"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 9-1: Slack Search

## 📍 What You'll Do

**Lesson 9-1: Slack Keyword Extended Search** !

| Item | Details |
|------|------|
| Goal | Perform keyword extended search on channels and messages with slack-search |
| Duration | ~25 min |
| Skills used | slack-search (BookRAG) |
| Prerequisites | Slack API configured (Lesson 0-4), data should exist in data/slack-sync |
| Course page | [Module 9: Slack Search](https://ai-agent.camp/en/course/module-9) alongside this lesson |

**Session flow:**
1. Slack search basics and index verification
2. Execute keyword and semantic searches
3. Utilize search results

By the end of this session, you will be able to search Slack conversations using keyword extended search (SequenceMatcher-based similarity search).

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

## 🚀 Step 1: Verify Slack Sync Data

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Verify Slack Sync Data",
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
Please check the ~/ai-agent-camp/data/slack-sync/data/ folder.
Please provide the following information:
- List of synced channels
- Total number of message files
- Last sync date/time
```

**Expected result:** The Slack data sync status is displayed. If not synced, setup is required.

---

## 🚀 Step 2: Run Keyword Search

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Run Keyword Search",
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
Please search for messages containing the keyword "project progress" in Slack.
Display those from the last week in the following format:
- Channel name
- Date/time
- Speaker
- Message content (up to 100 characters)
```

**Expected result:** A list of matching messages is displayed.

---

## 🚀 Step 3: Channel-Specific Search

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Channel-Specific Search",
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
Please search a specific Slack channel:
- Channel: #general (or an existing channel name)
- Keywords: meeting OR conference
- Period: Last 2 weeks

Organize the found messages chronologically.
```

**Expected result:** Search results from the specified channel are displayed.

---

## 🚀 Step 4: User-Specific Search

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: User-Specific Search",
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
Please search for messages from a specific user in Slack:
- Target user: @YourName (replace with your username)
- Search keywords: review OR confirm
- Period: Last 1 month

Sort the results by importance.
```

**Expected result:** Messages from the specified user are extracted.

---

## 🚀 Step 5: Using Extended Keyword Search

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Using Extended Keyword Search",
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
Please perform an extended keyword search for messages related to "customer feedback" in Slack.

Also include the following synonyms in the search:
- feedback, opinions, requests, complaints, impressions
- customers, clients

Categorize the search results (positive/negative/neutral).
```

**Expected result:** Semantically related messages are categorized and displayed.

---

## 🚀 Step 6: Convert Search Results to Report

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 6: Convert Search Results to Report",
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
Please compile the previous search results into a Markdown report.

Please use the following format:
# Slack Search Report
Generated: (current date/time)

## Search Criteria
- Keywords: ...
- Period: ...

## Search Results Summary
- Total count: ...
- Breakdown by channel: ...

## Details
(Message list)

Output: ~/ai-agent-camp/output/slack_search_report.md
```

**Expected result:** Search results are compiled into a Markdown report.

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
      {"id": "trouble_1", "label": "Sync data not found"},
      {"id": "trouble_2", "label": "Search results are few"},
      {"id": "trouble_3", "label": "Japanese search not working well"},
      {"id": "trouble_4", "label": "Don't know the specific user's ID"}
    ]
  }]
}
```


### Issue 1: "Sync data not found"
**Cause:** slack-sync setup not completed
**Solution prompt:**
```
Please check the slack-sync setup status.
Please explain the structure and required files in the ~/ai-agent-camp/data/slack-sync/ folder.
```

### Issue 2: "Too few search results"
**Cause:** Search criteria too strict
**Solution prompt:**
```
To increase search results, try the following:
- Extend the search period to 1 month
- Change keywords to more general ones
- Remove channel specification
```

### Issue 3: "Japanese search doesn't work well"
**Cause:** Encoding or tokenization issue
**Solution prompt:**
```
Searching with Japanese keywords is not working well.
Please try the following:
- Search using both hiragana and katakana
- Split keywords into shorter segments
- Use partial match search
```

### Issue 4: "Don't know the specific user's ID"
**Cause:** Need to identify the Slack User ID
**Solution prompt:**
```
Please show how to check the Slack User ID.
Search for your User ID from the users.json file.
```

---

## ✅ Checkpoint
- [ ] Confirmed the location of Slack sync data
- [ ] Successfully executed keyword search
- [ ] Successfully searched by specified channel
- [ ] Successfully searched by user
- [ ] Successfully used expanded keyword search
- [ ] Successfully compiled search results into a report


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
      {"id": "next_window", "label": "Start in new window (/start-9-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-9-2
- finish → End

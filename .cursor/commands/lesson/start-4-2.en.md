---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~25 min"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "gmail"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 4-2: Gmail Search and Browse

## 📍 What You'll Do

**Lesson 4-2: Gmail Search and Browse** !

| Item | Details |
|------|---------|
| Goal | Search, view, and analyze Gmail emails using gogcli |
| Duration | ~25 min |
| Skills Used | gogcli gmail |
| Prerequisites | gogcli authentication setup completed (start-4-1 done) |

**Session flow:**
1. Learn Gmail search query syntax
2. View email thread details
3. Analyze and summarize search results with AI

By the end of this session, you will be able to freely search and analyze Gmail emails using gogcli.

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

## 🚀 Step 1: Learn Gmail Search Query Syntax

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Learn Gmail search query syntax",
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

Let's try the main query syntax available in gogcli Gmail search:

```bash
# Search unread emails
gog gmail search "is:unread" --account your-email@gmail.com

# Search emails from a specific sender
gog gmail search "from:example@company.com" --account your-email@gmail.com

# Search emails from the last 7 days
gog gmail search "newer_than:7d" --account your-email@gmail.com

# Search emails containing keywords in subject
gog gmail search "subject:meeting" --account your-email@gmail.com

# Search emails with attachments
gog gmail search "has:attachment newer_than:30d" --account your-email@gmail.com

# Compound conditions: unread and within last 3 days
gog gmail search "is:unread newer_than:3d" --account your-email@gmail.com
```

**Main search operators:**

| Operator | Description | Example |
|--------|------|-----|
| `is:unread` | Unread emails | `is:unread` |
| `from:` | Specify sender | `from:boss@company.com` |
| `to:` | Specify recipient | `to:team@company.com` |
| `subject:` | Subject search | `subject:meeting-notes` |
| `newer_than:` | Period specification | `newer_than:7d` / `newer_than:1m` |
| `has:attachment` | Has attachment | `has:attachment` |
| `label:` | Label specification | `label:important` |
| `in:` | Folder specification | `in:inbox` / `in:sent` |

**Expected result**: A list of emails matching each query (email ID, subject, sender, date/time) is displayed.

---

## 🚀 Step 2: Browse Email Thread Details

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: View email thread details",
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

Use the thread IDs obtained in Step 1 to check the details:

```bash
# Get thread ID via email search
gog gmail search "newer_than:1d" --account your-email@gmail.com

# Get thread details (use the thread ID shown above)
gog gmail thread get <thread-ID> --account your-email@gmail.com

# Get message body
gog gmail message get <message-ID> --account your-email@gmail.com
```

**Steps:**
1. `gog gmail search` to search for emails and note the thread ID of emails of interest
2. `gog gmail thread get` to view the entire thread (including replies)
3. `gog gmail message get` to get the body of individual messages

**Expected result**: The email subject, sender, date/time, and body are displayed. Thread view also shows the reply chain.

---

## 🚀 Step 3: Analyze and Summarize Search Results with AI

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Analyze and summarize search results with AI",
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

Have the AI analyze emails retrieved with gogcli:

```bash
# Get unread emails from the last week
gog gmail search "is:unread newer_than:7d" --account your-email@gmail.com
```

Paste the retrieved email list into Cursor chat and request analysis with a prompt like the following:

```text
Analyze the email list above and summarize from the following perspectives:
1. Emails requiring a reply (priority: High/Medium/Low)
2. Information-sharing-only emails (FYI)
3. Emails containing tasks
4. One-line summary for each email
```

**Advanced example:**
```bash
# Summarize interactions with a specific person chronologically
gog gmail search "from:boss@company.com newer_than:30d" --account your-email@gmail.com

# -> Ask AI: "Summarize the above emails chronologically and extract pending requests"
```

**Expected result**: The AI classifies emails and generates a prioritized task list and summary.

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
      {"id": "trouble_1", "label": "Search returns 0 results"},
      {"id": "trouble_2", "label": "Email body has garbled characters"},
      {"id": "trouble_3", "label": "Authentication error occurs"},
      {"id": "trouble_4", "label": "Error from forgetting --account"}
    ]
  }]
}
```

### Issue 1: "Search results return 0 items"
**Cause**: Query syntax error, or no matching emails exist
**Solution prompt**:
```text
Try a looser query. First check if there are emails from the last 30 days with "newer_than:30d".
If searching by Japanese subject doesn't work well, try filtering by sender or date.
```

### Issue 2: "Email body has character encoding issues"
**Cause**: Encoding issue
**Solution prompt**:
```text
Try redirecting gogcli output to a file:
gog gmail message get <id> --account <email> > /tmp/mail.txt
Check the file encoding: file /tmp/mail.txt
```

### Issue 3: "Authentication error occurs"
**Cause**: Token has expired
**Solution prompt**:
```text
Remove authentication with gog auth remove your-email@gmail.com,
then re-authenticate with gog auth add your-email@gmail.com.
```

### Issue 4: "Error from forgetting --account"
**Cause**: gogcli requires --account for all commands
**Solution prompt**:
```text
In gogcli, --account <email-address> is required for all commands.
Setting up an alias is convenient:
alias gogg="gog --account your-email@gmail.com"
```

---

## ✅ Checkpoint
- [ ] Understood Gmail search query syntax (is:unread, from:, newer_than:, etc.)
- [ ] Was able to view email thread details
- [ ] Was able to have AI analyze search results and generate summaries
- [ ] Was able to search with compound conditions


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
Run the following gogcli commands to verify Gmail search and viewing works correctly:
1. gog gmail search "is:unread newer_than:7d" --account <your-email>
2. Select one result from above and display thread details with gog gmail thread get
Verify that all commands work correctly.
```

**Expected result**: Search results and thread details are displayed without errors.

---

## 🎉 Next Steps

Gmail search and viewing is now complete! In the next lesson, you will learn Google Calendar operations.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/start-4-3)"},
      {"id": "next_window", "label": "Start in new window (/start-4-3)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /start-4-3（Google Calendar Operations)
- next_window → Open new window with /start-4-3
- finish → End

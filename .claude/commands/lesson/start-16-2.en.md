---
description: "When the user says /start-16-2 — Module 16 Lesson 16-2: Incoming email analysis & task extraction - check-inbox"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-16-1"]
level: "beginner"
tags: ["email", "gmail", "check-inbox", "task-extraction"]
---

# Lesson 16-2: Incoming Email Analysis & Task Extraction

## What You Will Do in This Session

Welcome to **Lesson 16-2: Incoming Email Analysis & Task Extraction**!

| Item | Details |
|------|---------|
| Goal | Use the check-inbox skill to extract TODOs from emails, determine priority, and generate reply drafts |
| Duration | ~30 min |
| Skills used | check-inbox |
| Prerequisites | Lesson 16-1 complete (gogcli authenticated), Gemini API key configured |
| Course page | Refer to [Module 16: Email Automation](https://ai-agent.camp/en/course/module-16) in parallel |

**Session flow:**
1. Understand how check-inbox works
2. Prepare email data (google-sync)
3. Run email analysis with check-inbox
4. Review prioritized task list and reply drafts

By the end of this session, you will be able to auto-extract TODOs from incoming emails, determine priority, and generate reply drafts.

> **Tip**: If the AI response stops midway, type "please continue" or "it stopped" to resume.

---

## Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "previous_lesson", "label": "I want to do 13-1 first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

---

## Step 1: Understand How check-inbox Works

The check-inbox skill operates as follows:

```text
Sync emails with google-sync -> Save as Markdown files
    |
check-inbox reads local files
    |
Analyze content with Gemini API
    |
Priority determination + reply draft generation
```

**Key points:**
- It does not call the Gmail API in real time; it analyzes pre-synced local data
- Fast context determination with Gemini 3.0 Flash

---

## Step 2: Prepare Email Data

check-inbox reads local Markdown files.

**Check for existing data:**
```bash
ls output/gmail/ 2>/dev/null && echo "Data exists" || echo "No data"
```

If no data, export directly with gogcli:

```bash
# Get latest emails and save in JSON format
gog gmail search "is:inbox newer_than:7d" --account <your-email@gmail.com> --max 20 --format json
```

**AskQuestion:**
```json
{
  "title": "Email data status",
  "questions": [{
    "id": "data_status",
    "prompt": "Do you have email data?",
    "options": [
      {"id": "exists", "label": "Data exists in output/gmail/ -> Proceed"},
      {"id": "export_needed", "label": "No data -> Help me export"},
      {"id": "use_sample", "label": "I want to try with sample data"}
    ]
  }]
}
```

---

## Step 3: Run Email Analysis with check-inbox

**Run the following prompt in Cursor / Claude Code:**

```text
Check my inbox and list emails that need replies.
Assign priorities and create reply drafts.
```

Or call the `skills/check-inbox` skill directly:

```text
/check-inbox
```

**Expected output:**
- List of emails requiring replies (with priority)
- Summary of each email
- Suggested reply drafts

---

## Step 4: Review Results and Apply

Review check-inbox results and consider how to use them in practice.

**AskQuestion:**
```json
{
  "title": "Using analysis results",
  "questions": [{
    "id": "usage",
    "prompt": "How do you want to use the analysis results?",
    "options": [
      {"id": "reply", "label": "I want to reply using drafts -> Go to 13-3"},
      {"id": "review", "label": "I want to review/organize the task list"},
      {"id": "retry", "label": "I want to re-analyze with a different filter"},
      {"id": "next", "label": "I want to go to the next lesson"}
    ]
  }]
}
```

---

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| `GEMINI_API_KEY` error | Set the Gemini API key in `.env`, or run `/setup-gemini` |
| Email data not found | Check if the `output/gmail/` directory exists |
| Analysis results are empty | Check the email data format (Markdown + YAML front matter) |

---

## Checkpoint

- [ ] Email analysis was executed with check-inbox
- [ ] A prioritized task list was generated
- [ ] Reply drafts were suggested


---

## Deliverables Preview

### Expected output
```text
output/email/
  index.html  (HTML email)
  style.css
  assets/
```

### Verification commands
```bash
# File list
ls -lh output/email/

# Open in browser (macOS: open / Linux: xdg-open)
open output/email/index.html
```

> View HTML structure: `head -30 output/email/index.html`

---

## Completion Check

```bash
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

---

## Next Steps

**AskQuestion:**
```json
{
  "title": "Lesson 16-2 Complete!",
  "questions": [{
    "id": "next_action",
    "prompt": "What do you want to do next?",
    "options": [
      {"id": "next_lesson", "label": "Go to 13-3 -> Send email with gogcli"},
      {"id": "practice", "label": "I want to try more analysis"},
      {"id": "review", "label": "Review Module 16 overview"},
      {"id": "end", "label": "That's all for today"}
    ]
  }]
}
```

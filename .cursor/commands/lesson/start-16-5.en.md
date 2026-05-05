---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-16-1", "start-16-2", "start-16-3"]
level: "advanced"
tags: ["email", "gmail", "gogcli", "github-actions", "automation"]
nonInteractiveMode: deferred
---
# Lesson 16-5: Email Automation Workflow

## What You Will Do in This Session

Welcome to **Lesson 16-5: Email Automation Workflow**!

| Item | Details |
|------|---------|
| Goal | Automate scheduled email sending with GitHub Actions and set up Slack notification integration |
| Duration | ~30 min |
| Tools used | gogcli (gog), check-inbox, GitHub Actions |
| Prerequisites | Lessons 16-1 through 16-3 complete |
| Course page | Refer to [Module 16: Email Automation](https://ai-agent.camp/en/course/module-16) in parallel |

**Session flow:**
1. Design the overall email automation architecture
2. Create a GitHub Actions workflow
3. Set up Slack notification integration
4. Comprehensive exercise (all skills integrated)

By the end of this session, an email workflow automation pipeline will be built.

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
      {"id": "previous_lesson", "label": "I want to do a previous lesson first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

---

## Step 1: Overall Email Automation Architecture

Automation pipeline built with GitHub Actions + gogcli:

```text
+------------------------------------------+
|         GitHub Actions (cron)            |
|  +--------------+  +------------------+ |
|  | google-sync  |->|  check-inbox     | |
|  | Email sync   |  |  Task extraction | |
|  +--------------+  +--------+---------+ |
|                             |            |
|  +--------------+  +--------v---------+ |
|  | gog send     |<-|  Reply draft     | |
|  | Email send   |  |  Review/approve  | |
|  +------+-------+  +------------------+ |
|         |                                |
|  +------v----------------------------+  |
|  | Slack notification (result summary)|  |
|  +------------------------------------+  |
+------------------------------------------+
```

---

## Step 2: Design GitHub Actions Workflow

**Design a workflow example:**

```text
Design a GitHub Actions workflow with these requirements:

1. Trigger: Run daily at 9 AM (JST)
2. Steps:
   a. Sync emails with google-sync
   b. Extract tasks with check-inbox
   c. Output results as a summary
   d. Notify via Slack
3. Environment variables: GOOGLE_CREDENTIALS (Secret)
```

**AskQuestion:**
```json
{
  "title": "Workflow customization",
  "questions": [{
    "id": "workflow_type",
    "prompt": "What type of automation do you want to build?",
    "options": [
      {"id": "daily_check", "label": "Daily morning email check & task extraction"},
      {"id": "auto_reply", "label": "Auto-reply under specific conditions"},
      {"id": "report", "label": "Weekly email report auto-send"},
      {"id": "custom", "label": "Custom workflow (specify conditions)"}
    ]
  }]
}
```

---

## Step 3: Set Up Slack Notification Integration

Send email processing results to Slack.

**Slack Webhook setup:**
1. Set up Incoming Webhook in Slack App
2. Save the Webhook URL to GitHub Secrets
3. Send notifications with `curl` in the workflow

**Notification message example:**
```json
{
  "text": "Email daily report\n- Unread: 5\n- Need reply: 2\n- Tasks: 3\n\nDetails: <URL>"
}
```

---

## Step 4: Comprehensive Exercise

An exercise integrating all skills learned in Module 16.

**Exercise:**

```text
Build the following email workflow automation pipeline:

1. Get incoming emails with gogcli
2. Extract tasks with check-inbox and determine priority
3. Generate reply drafts for high-priority emails
4. Review send content with --dry-run
5. After confirmation, send replies with gogcli
6. Notify Slack with processing results
```

**AskQuestion:**
```json
{
  "title": "Comprehensive exercise approach",
  "questions": [{
    "id": "exercise_approach",
    "prompt": "How do you want to approach the exercise?",
    "options": [
      {"id": "guided", "label": "Work through it together with guidance"},
      {"id": "independent", "label": "Try it on my own"},
      {"id": "skip", "label": "Skip the exercise and go to review"},
      {"id": "partial", "label": "I want to try just part of it"}
    ]
  }]
}
```

---

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Credential error in GitHub Actions | Verify correct values are set in Secrets |
| Cron doesn't execute | Check cron syntax (UTC note: JST 9:00 = UTC 0:00) |
| Slack notification doesn't arrive | Verify the Webhook URL is correct |
| gogcli doesn't work in CI environment | Verify `gog` binary is in PATH |

---

## Checkpoint

- [ ] Designed an email automation workflow
- [ ] Created a GitHub Actions YAML file
- [ ] Understood the Slack notification mechanism
- [ ] Used all skills integratively in the comprehensive exercise


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
  "title": "All Module 16 Lessons Complete!",
  "questions": [{
    "id": "next_action",
    "prompt": "Congratulations! What do you want to do next?",
    "options": [
      {"id": "next_module", "label": "Go to Module 14 -> Article writing"},
      {"id": "review_all", "label": "I want to review Module 16"},
      {"id": "home", "label": "Go to home"},
      {"id": "end", "label": "That's all for today"}
    ]
  }]
}
```

---
description: "When the user says /start-16-1 — Module 16 Lesson 16-1: Gmail setup - gogcli authentication and email sync"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "~25 min"
prerequisites: []
level: "beginner"
tags: ["email", "gmail", "gogcli", "setup"]
---

# Lesson 16-1: Gmail Setup - gogcli Authentication and Email Sync

## What You Will Do in This Session

Welcome to **Lesson 16-1: Gmail Setup**!

| Item | Details |
|------|---------|
| Goal | Authenticate with Gmail using gogcli and get email search/reading working |
| Duration | ~25 min |
| Tools used | gogcli (gog) |
| Prerequisites | Google account (Gmail) |
| Course page | Refer to [Module 16: Email Automation](https://ai-agent.camp/en/course/module-16) in parallel |

**Session flow:**
1. Verify gogcli installation
2. Set up Gmail authentication with `gog auth add`
3. Test email search with `gog gmail search`
4. Verify email sync with google-sync

By the end of this session, you will be able to access Gmail via gogcli and search/read emails.

> **Tip**: If the AI response stops midway, type "please continue" or "it stopped" to resume. Responses may pause depending on the tool, but this is not an error.

---

## Readiness Check

First, confirm that everything is ready.

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
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Go to Step 1)
(check_prereq -> Run prerequisite check)
(view_html -> Show the course page path)
(different_lesson -> Show module list)

---

## Step 1: Verify gogcli Installation

First, verify that gogcli is installed.

**Command to run:**
```bash
gog --version
```

**Expected result:**
- If a version number is displayed, you're good (v0.9.0 or later recommended)
- If the command is not found, install with `brew install gogcli` (or run `/setup-gogcli`)

> **Note**: All Gmail API calls in the following commands require `--account <your-email@gmail.com>`. Specify explicitly if you have multiple accounts registered.

**AskQuestion:**
```json
{
  "title": "gogcli installation status",
  "questions": [{
    "id": "gog_installed",
    "prompt": "What was the result of the gogcli installation check?",
    "options": [
      {"id": "installed", "label": "Version was displayed -> Proceed"},
      {"id": "not_installed", "label": "Command not found -> Help me install"},
      {"id": "error", "label": "Got an error -> Troubleshoot"}
    ]
  }]
}
```

---

## Step 2: Set Up Gmail Authentication

Authenticate your Gmail account with gogcli.

**Command to run:**
```bash
gog auth add <your-email@gmail.com>
```

A browser will open and display the Google OAuth authentication screen.
Grant access and the token will be saved locally.

**Verify authentication:**
```bash
gog auth list
```

**Expected result:**
```text
ACCOUNT                    DEFAULT
your-email@gmail.com       *
```

**Check scopes:**
```bash
gog auth services
```

Confirm that the Gmail send scope (`gmail.send`) is included.

---

## Step 3: Test Email Search

Once authentication is complete, test email search.

**Search for unread emails:**
```bash
gog gmail search "is:unread" --account <your-email@gmail.com> --max 5
```

**Search for emails from a specific sender:**
```bash
gog gmail search "from:noreply@github.com" --account <your-email@gmail.com> --max 5
```

**View thread details:**
```bash
gog gmail thread get <thread-id> --account <your-email@gmail.com>
```

**AskQuestion:**
```json
{
  "title": "Email search test results",
  "questions": [{
    "id": "search_result",
    "prompt": "Was the email search successful?",
    "options": [
      {"id": "success", "label": "Emails were displayed -> Proceed"},
      {"id": "empty", "label": "Results were empty -> Retry with different query"},
      {"id": "auth_error", "label": "Authentication error -> Troubleshoot"}
    ]
  }]
}
```

---

## Step 4: Email Sync with google-sync (Optional)

The check-inbox skill reads local Markdown files.
Syncing emails locally with google-sync will make 13-2 smoother.

**Check sync status:**
```bash
ls data/google-sync/data/*/gmail/ 2>/dev/null || echo "No sync data"
```

If there is no sync data, it will be configured when using check-inbox in 13-2.

---

## Common Issues and Solutions

**AskQuestion:**
```json
{
  "title": "Did you have any issues?",
  "questions": [{
    "id": "trouble",
    "prompt": "Did you encounter any problems?",
    "options": [
      {"id": "none", "label": "No problems -> Go to checkpoint"},
      {"id": "auth_fail", "label": "Authentication failed"},
      {"id": "no_results", "label": "No search results"},
      {"id": "other", "label": "Other error"}
    ]
  }]
}
```

| Issue | Solution |
|-------|----------|
| `gog` command not found | Run `brew install gogcli` (or `/setup-gogcli`) |
| Browser doesn't open for auth | Use `gog auth add --no-browser <email>` to manually copy the URL (required in non-interactive environments) |
| OAuth scope insufficient | `gog auth remove <email>` -> re-run `gog auth add <email>` |
| Search results are empty | Change query to `is:inbox` and retry |

---

## Checkpoint

Verify the following:

- [ ] `gog --version` displays a version number
- [ ] `gog auth list` shows your account
- [ ] `gog gmail search "is:inbox" --account <your-email@gmail.com> --max 3` retrieves emails


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
  "title": "Lesson 16-1 Complete!",
  "questions": [{
    "id": "next_action",
    "prompt": "What do you want to do next?",
    "options": [
      {"id": "next_lesson", "label": "Go to 13-2 -> Incoming email analysis & task extraction"},
      {"id": "practice", "label": "I want to practice searching more"},
      {"id": "review", "label": "Review Module 16 overview"},
      {"id": "end", "label": "That's all for today"}
    ]
  }]
}
```

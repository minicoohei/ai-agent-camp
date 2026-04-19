---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "~35 min"
prerequisites: ["start-16-1"]
level: "intermediate"
tags: ["email", "gmail", "gogcli", "send"]
---

# Lesson 16-3: Send Email with gogcli

## What You Will Do in This Session

Welcome to **Lesson 16-3: Send Email with gogcli**!

| Item | Details |
|------|---------|
| Goal | Practice composing, sending, thread replying, and attaching files with `gog gmail send` |
| Duration | ~35 min |
| Tools used | gogcli (gog) |
| Prerequisites | Lesson 16-1 complete (gogcli authenticated) |
| Course page | Refer to [Module 16: Email Automation](https://ai-agent.camp/en/course/module-16) in parallel |

**Session flow:**
1. Version check and learn `--account` usage
2. Send a test email to yourself
3. Practice thread replies (`--thread-id`)
4. Practice attachments (`--attach`)

By the end of this session, you will be able to safely send, reply, and attach files with gogcli.

> **Warning**: Email sending is an irreversible operation. Always review the content carefully before sending.
> **Note**: In v0.9.0, the `--dry-run` flag has been deprecated. Review content visually before sending.

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

## Step 1: Version Check and Preparation

First, check the gogcli version and understand `--account` usage.

```bash
gog --version
```

Confirm it is v0.9.0 or later.

> **Important**: In v0.9.0, the `--dry-run` flag has been deprecated. Visually confirm the arguments (to, subject, body) before sending.
> All `gog gmail` commands require `--account <your-email@gmail.com>`.

**AskQuestion:**
```json
{
  "title": "Version check",
  "questions": [{
    "id": "version_result",
    "prompt": "Is the gogcli version v0.9.0 or later?",
    "options": [
      {"id": "correct", "label": "v0.9.0 or later -> Proceed"},
      {"id": "old_version", "label": "Old version -> Help me update"},
      {"id": "error", "label": "Got an error -> Troubleshoot"}
    ]
  }]
}
```

---

## Step 2: Send a Test Email

**Always use your own email address as the recipient.**

```bash
gog gmail send \
  --account <your-email@gmail.com> \
  --to <your-email@gmail.com> \
  --subject "gogcli test send" \
  --body "This is a test email sent from gogcli (gog gmail send)."
```

**Expected result:**
- A success message is displayed
- The email arrives in your inbox

**Load body from a file:**
```bash
echo "This is the body loaded from a file." > /tmp/test-email.txt
gog gmail send \
  --account <your-email@gmail.com> \
  --to <your-email@gmail.com> \
  --subject "File body send test" \
  --body-file /tmp/test-email.txt
```

---

## Step 3: Thread Reply

Reply to the thread of the email you just sent.

**Step 3-1: Get the thread ID**
```bash
gog gmail search "subject:gogcli test send" --account <your-email@gmail.com> --max 1
```

Check the thread ID from the output.

**Step 3-2: Reply to the thread**
```bash
gog gmail send \
  --account <your-email@gmail.com> \
  --thread-id <thread-id> \
  --subject "Re: gogcli test send" \
  --body "This is a thread reply test from gogcli."
```

> **Note**: In v0.9.0, `--subject` is required. It cannot be omitted even for replies.

**Reply-all:**
```bash
gog gmail send \
  --account <your-email@gmail.com> \
  --reply-to-message-id <message-id> \
  --reply-all \
  --subject "Re: original subject" \
  --body "This is a reply-all test."
```

---

## Step 4: Send with Attachment

Send an email with a file attachment.

**Create a test file:**
```bash
echo "Attachment test content." > /tmp/test-attachment.txt
```

**Send email with attachment:**
```bash
gog gmail send \
  --account <your-email@gmail.com> \
  --to <your-email@gmail.com> \
  --subject "Attachment test" \
  --body "This is a test email with an attachment." \
  --attach /tmp/test-attachment.txt
```

> **Note**: Visually confirm `--to`, `--subject`, `--body`, and `--attach` content before sending.

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
      {"id": "send_fail", "label": "Send failed"},
      {"id": "scope_error", "label": "Permission error"},
      {"id": "other", "label": "Other error"}
    ]
  }]
}
```

| Issue | Solution |
|-------|----------|
| `insufficient permission` | `gog auth remove <email>` -> `gog auth add <email>` to re-authenticate |
| Sent but not received | Check spam folder |
| `thread not found` | Re-check thread ID with `gog gmail search` |
| Attachment error | Confirm file path is correct (absolute path recommended) |

---

## Checkpoint

- [ ] Confirmed `gog --version` is v0.9.0 or later
- [ ] Sent a test email to yourself and confirmed receipt
- [ ] Replied to a thread with `--thread-id`
- [ ] Sent an attachment with `--attach`


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
  "title": "Lesson 16-3 Complete!",
  "questions": [{
    "id": "next_action",
    "prompt": "What do you want to do next?",
    "options": [
      {"id": "next_lesson", "label": "Go to 13-4 -> Email sequence design"},
      {"id": "practice", "label": "I want to practice sending more"},
      {"id": "review", "label": "Review Module 16 overview"},
      {"id": "end", "label": "That's all for today"}
    ]
  }]
}
```

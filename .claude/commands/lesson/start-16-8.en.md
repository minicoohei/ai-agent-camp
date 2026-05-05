---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-16-6", "start-16-7"]
level: "intermediate"
tags: ["email", "resend", "resend-cli", "sequences", "drip-campaign", "automation"]
nonInteractiveMode: deferred
---
# Lesson 16-8: Resend Sequence & CLI Drip Campaign

## What You Will Do in This Session

Welcome to **Lesson 16-8: Resend Sequence Drip Campaign**!

| Item | Details |
|------|---------|
| Goal | Create a welcome sequence with Resend Sequences and automate contact management with CLI |
| Duration | ~30 min |
| Tools used | Resend CLI (`resend-cli`), Resend Dashboard, email-sequence skill |
| Prerequisites | Lessons 16-6 & 16-7 complete (domain verified & API key created) |
| Course page | Refer to [Module 16: Email Automation](https://ai-agent.camp/en/course/module-16) in parallel |

**Session flow:**
1. Sequence concepts and design patterns
2. Create a sequence in Resend Dashboard
3. Manage contacts and Audiences with Resend CLI
4. Generate templates with email-sequence skill

By the end of this session, an automated email sequence will be built.

> **Tip**: By automating contact management with Resend CLI, you can automatically add new users to sequences.

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
      {"id": "previous_lesson", "label": "I want to do Lesson 16-7 first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

---

## Step 1: Basic Sequence Concepts

**What is a sequence?**
A mechanism that automatically sends emails at preset intervals triggered by a specific event.

**Welcome sequence example:**
| Email | Timing | Subject | Purpose |
|-------|--------|---------|---------|
| 1st | Day 0 (immediate) | Welcome! Getting started guide | First impression, service overview |
| 2nd | Day 3 | 3 tips for getting the most out of it | Key feature introduction |
| 3rd | Day 7 | How [name] uses it | Social proof |
| 4th | Day 14 | We'd love your feedback | Engagement |

**AskQuestion:**
```json
{
  "title": "Select sequence type",
  "questions": [{
    "id": "sequence_type",
    "prompt": "What type of sequence do you want to create?",
    "options": [
      {"id": "welcome", "label": "Welcome sequence (for new signups)"},
      {"id": "onboarding", "label": "Onboarding (getting started support)"},
      {"id": "nurture", "label": "Lead nurturing (prospect development)"},
      {"id": "custom", "label": "Custom (specify your own conditions)"}
    ]
  }]
}
```

---

## Step 2: Create a Sequence in Resend Dashboard

1. Resend dashboard -> **Sequences** -> Create Sequence
2. Enter sequence name (e.g., "Welcome Series")
3. Set trigger condition (e.g., when added to Audience)
4. Add email steps (subject, body, send interval)

**Generate template with email-sequence skill:**
```text
Use the email-sequence skill to design a SaaS welcome sequence.

Conditions:
- Target: New free-tier users
- Number of emails: 4
- Period: 14 days
- Goal: Product adoption and paid plan conversion
- Tone: Friendly and approachable
```

---

## Step 3: Manage Contacts and Audiences with Resend CLI

**Create an Audience:**
```bash
resend audiences create --name "Welcome Series"
```

**Add a contact:**
```bash
resend contacts create \
  --audience-id <audience-id> \
  --email "user@example.com" \
  --first-name "Taro"
```

**List contacts:**
```bash
resend contacts list --audience-id <audience-id>
```

**JSON output (for automation/scripting):**
```bash
resend contacts list --audience-id <audience-id> --json
```

> **Automation tip**: If you auto-add contacts via Webhook -> Resend CLI when a new user signs up, the sequence starts automatically.

---

## Step 4: Test Send and Monitoring

**Run the sequence with a test contact:**
1. Add your email address as a contact
2. Confirm the first sequence email arrives
3. Monitor delivery status in the Resend dashboard

**Delivery metrics to check:**
- Delivery Rate
- Open Rate
- Click Rate
- Unsubscribe Rate

---

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Sequence doesn't start | Verify contacts are correctly added to the Audience |
| Emails not delivered | Re-check domain verification. Check SPF/DKIM settings |
| CLI can't find Audience | Check ID with `resend audiences list` |
| Template not as expected | Add more detailed conditions and regenerate with email-sequence skill |

---

## Checkpoint

- [ ] Understood sequence design patterns
- [ ] Created a sequence in Resend Dashboard
- [ ] Managed Audiences and contacts with Resend CLI
- [ ] Verified sequence operation with a test send


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
uv run python tools/lesson_progress.py --check start-16-8
```

---

## Next Steps

**AskQuestion:**
```json
{
  "title": "Lesson 16-8 Complete!",
  "questions": [{
    "id": "next_action",
    "prompt": "What do you want to do next?",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Open in new window (/start-17-1)"},
      {"id": "practice", "label": "I want to create another sequence"},
      {"id": "review", "label": "Review Module 16 overview"},
      {"id": "end", "label": "That's all for today"}
    ]
  }]
}
```

**Post-selection guide (example)**:
- next_auto -> /next_lesson
- next_window -> Open /start-17-1 in a new window
- practice -> Practice with another sequence
- review -> Review Module 16
- end -> End

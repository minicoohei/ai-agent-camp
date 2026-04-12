---
description: "When the user says /start-16-4 — Module 16 Lesson 16-4: Email sequence design - drip campaigns"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-16-1"]
level: "intermediate"
tags: ["email", "sequence", "drip-campaign", "marketing"]
---

# Lesson 16-4: Email Sequence Design

## What You Will Do in This Session

Welcome to **Lesson 16-4: Email Sequence Design**!

| Item | Details |
|------|---------|
| Goal | Design drip campaigns and welcome sequences with the email-sequence skill |
| Duration | ~30 min |
| Skills used | email-sequence |
| Prerequisites | Lesson 16-1 complete (gogcli authenticated) |
| Course page | Refer to [Module 16: Email Automation](https://ai-agent.camp/en/course/module-16) in parallel |

**Session flow:**
1. Understand basic email sequence concepts
2. Design a welcome sequence
3. Create email templates
4. Optimize send timing and subject line strategy

By the end of this session, you will be able to design practical email sequences.

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
      {"id": "previous_lesson", "label": "I want to do 13-3 first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

---

## Step 1: Basic Email Sequence Concepts

An email sequence is a series of emails automatically sent in response to specific triggers.

**Main sequence types:**
| Type | Purpose | Example |
|------|---------|---------|
| Welcome | Greet new subscribers | Service intro -> Usage guide -> Tips |
| Onboarding | Support getting started | Setup -> First action -> Advanced |
| Lead nurturing | Nurture prospects | Problem statement -> Solution -> Case study -> CTA |
| Re-engagement | Win back churned users | Update -> New features -> Special offer |

---

## Step 2: Design a Welcome Sequence

Use the email-sequence skill to design a welcome sequence.

**Run the following prompt in Cursor / Claude Code:**

```text
Use the email-sequence skill to design a welcome email sequence for a SaaS product.

Conditions:
- Target: New free-tier users
- Number of emails: 5
- Period: 14 days from registration
- Goal: Upgrade to paid plan
```

**AskQuestion:**
```json
{
  "title": "Sequence customization",
  "questions": [{
    "id": "sequence_type",
    "prompt": "What type of sequence do you want to design?",
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

## Step 3: Create Email Templates

Create templates for each email in the designed sequence.

**Template components:**
- **Subject**: The most critical element affecting open rate
- **Preheader**: Subject supplement (shown in email client preview)
- **Body**: Main content
- **CTA**: Call-to-action button/link

**Prompt example:**
```text
Create an email template for the first email of the welcome sequence designed earlier.
Suggest 3 subject line patterns and output the body in HTML format.
```

---

## Step 4: Send Timing and Subject Line Strategy

**Send timing best practices:**
| Email | Timing | Reason |
|-------|--------|--------|
| 1st | Immediately after signup | Highest interest moment |
| 2nd | Next day | First action follow-up |
| 3rd | 3 days later | Habit formation support |
| 4th | 7 days later | Value reconfirmation |
| 5th | 14 days later | Upgrade proposal |

**Subject line A/B test strategy:**
- Personalization: Include "{name}," or not
- Urgency: "Limited time", "3 days left"
- Question form: "Are you struggling with...?"
- Numbers: "In 3 steps"

---

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Can't decide on sequence structure | Start with a template and customize gradually |
| Too many/few emails | Design with the minimum steps needed for the goal |
| Can't come up with subject ideas | Reference competitor emails or have AI suggest multiple options |

---

## Checkpoint

- [ ] Completed email sequence design (5+ emails)
- [ ] Created subject line and body template for each email
- [ ] Set send timing


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
  "title": "Lesson 16-4 Complete!",
  "questions": [{
    "id": "next_action",
    "prompt": "What do you want to do next?",
    "options": [
      {"id": "next_lesson", "label": "Go to 13-5 -> Email automation workflow"},
      {"id": "practice", "label": "I want to design another sequence type"},
      {"id": "review", "label": "Review Module 16 overview"},
      {"id": "end", "label": "That's all for today"}
    ]
  }]
}
```

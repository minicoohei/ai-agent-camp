---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "~25 min"
prerequisites: ["start-16-6"]
level: "beginner"
tags: ["email", "resend", "api-key", "resend-cli", "send"]
---

# Lesson 16-7: API Key Creation & First Email Send

## What You Will Do in This Session

Welcome to **Lesson 16-7: API Key Creation & First Email Send**!

| Item | Details |
|------|---------|
| Goal | Create a Resend API key and send email using both CLI and SDK |
| Duration | ~25 min |
| Tools used | Resend CLI (`resend-cli`), Resend SDK (TypeScript) |
| Prerequisites | Lesson 16-6 complete (domain verified) |
| Course page | Refer to [Module 16: Email Automation](https://ai-agent.camp/en/course/module-16) in parallel |

**Session flow:**
1. Create API key and set permissions
2. Send email with Resend CLI
3. Send email with Resend SDK (TypeScript)
4. Manage API key securely with .env

By the end of this session, you will be able to send email via Resend.

> **Warning**: The API key is only displayed once. Always save it in .env and never commit to Git.

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
      {"id": "previous_lesson", "label": "I want to do 13-4 first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

---

## Step 1: Create API Key

**Create in Resend dashboard:**
1. Settings -> API Keys -> Create API Key
2. Name: anything (e.g., `dev-key`)
3. Permission: `Full access` (for development) or `Sending access` (for production)
4. Domain: Select verified domain

**Permission differences:**
| Permission | Capabilities | Recommended use |
|------------|-------------|-----------------|
| Full access | Email send + domain management + Audience management | Development/testing |
| Sending access | Email send only | Production (principle of least privilege) |

**Save API key to .env:**
```bash
echo "RESEND_API_KEY=re_xxxxxxxx" >> .env
```

---

## Step 2: Send Email with Resend CLI

**Test send with CLI:**
```bash
resend emails send \
  --from "noreply@your-domain.com" \
  --to "your-email@gmail.com" \
  --subject "Resend CLI test send" \
  --html "<p>Test email sent from Resend CLI!</p>"
```

**Check send results:**
```bash
resend emails list
```

**Scheduled send (natural language support):**
```bash
resend emails send \
  --from "noreply@your-domain.com" \
  --to "your-email@gmail.com" \
  --subject "Scheduled send test" \
  --html "<p>This email arrives in 1 hour</p>" \
  --scheduled-at "in 1 hour"
```

**AskQuestion:**
```json
{
  "title": "CLI send result",
  "questions": [{
    "id": "cli_result",
    "prompt": "Was the CLI email send successful?",
    "options": [
      {"id": "success", "label": "Send succeeded -> Proceed to SDK send"},
      {"id": "auth_error", "label": "Authentication error"},
      {"id": "domain_error", "label": "Domain error"},
      {"id": "other", "label": "Other error"}
    ]
  }]
}
```

---

## Step 3: Send with Resend SDK

**Install SDK:**
```bash
npm install resend
```

**Send email with TypeScript:**
```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send({
  from: 'noreply@your-domain.com',
  to: 'your-email@gmail.com',
  subject: 'Resend SDK test send',
  html: '<p>Test email sent from Resend SDK!</p>',
});

if (error) {
  console.error('Send error:', error);
} else {
  console.log('Send success:', data);
}
```

---

## Step 4: Manage API Key Securely with .env

**Add .env to .gitignore:**
```bash
echo ".env" >> .gitignore
```

**Verify:**
```bash
cat .gitignore | grep .env
```

---

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| `API key is invalid` | Verify the API key was copied correctly. May need to recreate |
| `Domain not verified` | Return to 13-4 and complete domain verification |
| `The from address is not verified` | Verify the from address domain is verified |
| Email not received | Check spam folder. Re-check SPF/DKIM settings |

---

## Checkpoint

- [ ] Created API key and saved to .env
- [ ] Sent a test email with Resend CLI
- [ ] Sent email with Resend SDK (TypeScript)
- [ ] .gitignore includes .env


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
uv run python tools/lesson_progress.py --check start-16-7
```

---

## Next Steps

**AskQuestion:**
```json
{
  "title": "Lesson 16-7 Complete!",
  "questions": [{
    "id": "next_action",
    "prompt": "What do you want to do next?",
    "options": [
      {"id": "next_lesson", "label": "Go to Lesson 16-8 -> Resend Sequence drip campaign"},
      {"id": "practice", "label": "I want to try more email sending"},
      {"id": "review", "label": "Review Module 16 overview"},
      {"id": "end", "label": "That's all for today"}
    ]
  }]
}
```

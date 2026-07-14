---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-13-1"]
level: "beginner"
tags: ["email", "resend", "domain", "dns", "vercel", "spf", "dkim"]
nonInteractiveMode: deferred
---
# Lesson 16-6: Resend Registration & Domain Setup

## What You Will Do in This Session

Welcome to **Lesson 16-6: Resend Registration & Domain Setup**!

| Item | Details |
|------|---------|
| Goal | Create a Resend account and complete Vercel domain DNS configuration (SPF, DKIM) |
| Duration | ~30 min |
| Tools used | Resend CLI (`resend-cli`), Vercel Dashboard |
| Prerequisites | Domain managed in Vercel |
| Course page | Refer to [Module 16: Email Automation](https://ai-agent.camp/en/course/module-16) in parallel |

**Session flow:**
1. Register a Resend account
2. Install and authenticate Resend CLI
3. Add domain and auto-configure Vercel DNS
4. Verify domain

By the end of this session, a domain configured for sending email via Resend will be ready.

> **Tip**: If you've already deployed a Landing Page or website on Vercel, you can use that same domain with Resend.

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

## Step 1: Register a Resend Account

1. Go to [resend.com](https://resend.com) and create an account
2. Enter organization information (company name, address, etc.)
3. Complete email verification

**Once complete, proceed to the next step.**

---

## Step 2: Install and Authenticate Resend CLI

**Install Resend CLI:**

```bash
# Install with npm
npm install -g resend-cli

# Or with Homebrew (Mac)
brew install resend/cli/resend
```

**Verify installation:**
```bash
resend --version
```

**Authentication (API key setup):**
Create an API Key in the Resend dashboard and configure it for the CLI.
(Detailed API key creation steps are covered in 13-5. Use the default key for now.)

---

## Step 3: Add Domain and Auto-configure Vercel DNS

**Add a domain with Resend CLI:**
```bash
resend domains create --name your-domain.com --region ap-northeast-1
```

**Auto-configure with Vercel Dashboard:**
1. Resend dashboard -> Domains -> Added domain -> Records tab
2. Click the "Auto configure" button
3. MX, SPF, DKIM records are auto-added to Vercel DNS

**Check domain list with CLI:**
```bash
resend domains list
```

**AskQuestion:**
```json
{
  "title": "Domain setup check",
  "questions": [{
    "id": "domain_status",
    "prompt": "What is the domain setup status?",
    "options": [
      {"id": "auto_done", "label": "Auto configure completed -> Go to verification"},
      {"id": "manual", "label": "I want to set DNS records manually"},
      {"id": "no_vercel", "label": "I'm using DNS other than Vercel"},
      {"id": "error", "label": "Got an error -> Troubleshoot"}
    ]
  }]
}
```

---

## Step 4: Domain Verification

**Run domain verification with CLI:**
```bash
resend domains verify --domain-id <domain-id>
```

**Check verification status:**
```bash
resend domains list
```

DNS record propagation may take a few minutes to hours. Once the status shows `verified`, you're done.

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
      {"id": "dns_pending", "label": "DNS verification not completing"},
      {"id": "auto_config_fail", "label": "Auto configure doesn't work"},
      {"id": "other", "label": "Other error"}
    ]
  }]
}
```

| Issue | Solution |
|-------|----------|
| DNS verification not completing | DNS propagation may take hours. Re-check with `resend domains verify` |
| Auto configure doesn't work | Verify domain is correctly set up in Vercel. Manually add TXT/MX records |
| resend CLI not found | Re-install with `npm install -g resend-cli` |

---

## Checkpoint

- [ ] Created a Resend account
- [ ] Installed and authenticated Resend CLI
- [ ] Added domain and configured DNS records (SPF, DKIM)
- [ ] Domain verification completed (`verified` status)


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
uv run python tools/lesson_progress.py --check start-16-6
```

---

## Next Steps

**AskQuestion:**
```json
{
  "title": "Lesson 16-6 Complete!",
  "questions": [{
    "id": "next_action",
    "prompt": "What do you want to do next?",
    "options": [
      {"id": "next_lesson", "label": "Go to Lesson 16-7 -> API key creation & first send"},
      {"id": "practice", "label": "I want to review DNS settings more"},
      {"id": "review", "label": "Review Module 16 overview"},
      {"id": "end", "label": "That's all for today"}
    ]
  }]
}
```

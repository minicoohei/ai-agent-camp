---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "~15 min"
prerequisites: ["start-0-1", "start-0-2", "start-0-3"]
level: "beginner"
tags: ["setup", "slack", "api"]
---

# Lesson 0-4: Slack API Setup

## Check Setup Progress

**Auto-run by AI:** Run `uv run python tools/setup_progress.py show` to display the current setup progress.

---

## What You'll Do

| Item | Details |
|------|---------|
| Goal | Create a Slack App, obtain a Bot Token, configure it in .env, and enable Slack integration features |
| Duration | ~15 min |
| Prerequisites | Lesson 0-1 through Lesson 0-3 completed; admin access (or App creation permission) for a Slack workspace |
| Course Page | Refer to [Course Materials Top](https://ai-agent.camp/en/course/module-0) in parallel |

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

---

## Slack API Auto-Setup

In this lesson, just run `/setup-slack` and you're done.
**No terminal operations required. The AI handles everything automatically.**

### What the AI Does Automatically

1. Auto-launch the Slack App management page in the browser
2. Guide you step by step through creating a Slack App
3. Guide you through setting Bot Token Scopes (channels:history, channels:read, chat:write, users:read)
4. Guide you through installing to the workspace and obtaining the token
5. Auto-add the token line to the `.env` file
6. You enter the token directly in the `.env` file
7. Auto-run a test request to the Slack API to verify it works

**Important**: Do not paste the token in the chat. You can securely save it with the following command:

```bash
uv run python tools/credential_manager.py store SLACK_BOT_TOKEN
```

When run, a password input prompt will appear. The entered value is not displayed on screen and is securely stored in the OS Credential Store (macOS Keychain, etc.).

> **Note**: You can also write directly to the `.env` file, but in Claude Code this may be blocked by the security guard (write_guard). Using `credential_manager.py` is the safest and most reliable method.

**AskQuestion settings:**
```json
{
  "title": "Slack API Setup",
  "questions": [{
    "id": "action",
    "prompt": "Would you like to start the Slack API setup?",
    "options": [
      {"id": "run", "label": "Start setup (run /setup-slack)"},
      {"id": "already_done", "label": "Slack API already configured"},
      {"id": "no_slack", "label": "I don't have a Slack workspace"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(run -> Run the contents of `/setup-slack`)
(already_done -> Go to checkpoint)
(no_slack -> Guide: "You can create a Slack workspace for free. Create a test workspace at https://slack.com/create, then restart this setup.")
(different_lesson -> Show module list)

---

## Commands to Run

```text
/setup-slack
```

## Expected Output Example

```text
Slack API Test Result:
Connection: OK
Workspace: your-workspace
Bot name: AIAgent Bootcamp
```

## Common Troubleshooting
- Browser doesn't open -> Manually open `https://api.slack.com/apps`
- `not_authed` error -> Check .env to ensure the token was copied correctly
- `missing_scope` error -> Add scopes in the Slack admin page, then click "Reinstall to Workspace"

---

## Checkpoint
- [ ] Created a Slack App named "AIAgent Bootcamp"
- [ ] Configured the required Bot Token Scopes
- [ ] Installed the App to the workspace
- [ ] SLACK_BOT_TOKEN is set in .env
- [ ] API test succeeded

---

## Next Steps

**AskQuestion settings:**
```json
{
  "title": "Choose Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "What would you like to do next?",
    "options": [
      {"id": "next", "label": "Configure security settings (/start-0-5)"},
      {"id": "try_slack", "label": "Try Slack search (/start-6-1)"},
      {"id": "check", "label": "Run environment check (/check-setup)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(next -> Guide to /start-0-5)
(try_slack -> Guide to /start-6-1)
(check -> Run the contents of /check-setup)
(finish -> End)

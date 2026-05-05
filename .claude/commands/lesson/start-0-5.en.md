---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "~5 min"
prerequisites: ["start-0-1", "start-0-2", "start-0-3", "start-0-4"]
level: "beginner"
tags: ["setup", "security"]
nonInteractiveMode: deferred
---
# Lesson 0-5: Security Settings Verification

## Check Setup Progress

**Auto-run by AI:** Run `uv run python tools/setup_progress.py show` to display the current setup progress.

---

## What You'll Do

| Item | Details |
|------|---------|
| Goal | Configure .gitignore and pre-commit hooks to prevent API key leaks. Safely complete Module 0 |
| Duration | ~5 min |
| Prerequisites | Lesson 0-1 through Lesson 0-4 completed; API keys configured in .env |
| Course Page | Refer to [Course Materials Top](https://ai-agent.camp/en/course/module-0) in parallel |

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

---

## Security Settings Auto-Setup

In this lesson, just run `/setup-security` and you're done.
**No terminal operations required. The AI handles everything automatically.**

### What the AI Does Automatically

1. Check `.gitignore` and auto-add missing entries (.env, credentials/, *.key, *.pem, etc.)
2. Auto-configure `pre-commit` hooks (block accidental commits of .env files)
3. Run a current safety check (verify .env is not tracked by Git, not committed in the past)
4. If issues are found, suggest auto-fixes

**AskQuestion settings:**
```json
{
  "title": "Security Settings",
  "questions": [{
    "id": "action",
    "prompt": "Would you like to start the security setup?",
    "options": [
      {"id": "run", "label": "Start auto-setup (run /setup-security)"},
      {"id": "already_done", "label": "Security already configured"},
      {"id": "more_info", "label": "Why are security settings necessary?"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(run -> Run the contents of `/setup-security`)
(already_done -> Go to completion check)
(more_info -> Explain: "If API keys are exposed on GitHub, there is a risk of unauthorized use and high charges. This command automatically sets up preventive measures." Then prompt again.)
(different_lesson -> Show module list)

---

## Commands to Run

```text
/setup-security
```

## Expected Output Example

```text
Security Setup Complete:
- .gitignore: Added .env, credentials/, *.key, *.pem ✓
- pre-commit hook: Configured ✓
- .env file: Not tracked by Git ✓
```

## Common Troubleshooting
- pre-commit hook blocks a commit -> Ask the AI to "check the commit contents"
- .env is tracked by Git -> Ask the AI to "remove .env from Git tracking"

---

## Checkpoint
- [ ] .gitignore includes .env
- [ ] .gitignore includes credentials/
- [ ] pre-commit hook is configured
- [ ] .env file is not tracked by Git
- [ ] Git history does not contain sensitive information

---

## Module 0 Complete!

Once security settings are complete, Module 0 is fully done.

As a final check, run `/check-setup` to display a report of all items.

---

## Next Steps

**AskQuestion settings:**
```json
{
  "title": "Module 0 Complete! Choose Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Congratulations! Module 0 is complete. What would you like to do next?",
    "options": [
      {"id": "start_lesson", "label": "Start the first lesson (/start-1-1: Banner Generation)"},
      {"id": "final_check", "label": "Run final check (/check-setup)"},
      {"id": "overview", "label": "Review the project overview (/overview)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(start_lesson -> Guide to /start-1-1)
(final_check -> Run the contents of /check-setup)
(overview -> Guide to /overview)
(finish -> Display "Great work! You can start the first lesson anytime with /start-1-1")

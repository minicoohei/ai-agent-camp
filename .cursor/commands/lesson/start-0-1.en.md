---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "~15 min"
prerequisites: ["Codex Desktop or Cursor installed", "ai-agent-camp folder is open"]
level: "beginner"
tags: ["setup", "environment"]
nonInteractiveMode: incompatible
---
# Lesson 0-1: Environment Setup Verification

## Check Setup Progress

**Auto-run by AI:** Run `uv run python tools/setup_progress.py show` to display the current setup progress.

---

## What You'll Do

| Item | Details |
|------|---------|
| Goal | Verify that your environment — including Node.js, Python, and GitHub CLI — is ready so you can start learning with Codex |
| Duration | ~15 min |
| Prerequisites | Codex Desktop or Cursor installed; ai-agent-camp folder is open |
| Course Page | Refer to [Course Materials Top](https://ai-agent.camp/en/course/module-0) in parallel |

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

---

## How to Set Up

In this lesson, you will use the following two commands to set up your environment.
**No terminal operations required. The AI handles everything automatically.**

> **Note for Codex**: In Codex, instead of running `/setup-start` or `/check-setup` directly as Cursor slash commands, follow the verification steps written in this file in order. When GUI operations like browser authentication are needed, switch to manual user operation at that point.

### Step 1: Start Setup

Run `/setup-start` first. This command **automatically** performs the following:

- Detect your OS (Mac / Windows)
- Check for Python / Node.js / Git / GitHub CLI and their versions
- Provide GUI installer URLs for any missing tools

**AskQuestion settings:**
```json
{
  "title": "Step 1: Start Setup",
  "questions": [{
    "id": "action",
    "prompt": "Let's start setting up your environment. What would you like to do?",
    "options": [
      {"id": "run_setup", "label": "Start setup (run /setup-start)"},
      {"id": "run_check", "label": "Run environment check only (run /check-setup)"},
      {"id": "already_done", "label": "Already set up"},
      {"id": "view_html", "label": "View the course page first"}
    ]
  }]
}
```

(run_setup -> Run the contents of `/setup-start`)
(run_check -> Run the contents of `/check-setup`)
(already_done -> Go to Step 2)
(view_html -> Provide the course page URL `https://ai-agent.camp/en/course/module-0`)

---

### Step 2: GitHub Settings and Personal Repository Creation

Run `/setup-github`. This command **automatically** performs the following:

- Check for a GitHub account
- Auto-launch the browser for GitHub login (`gh auth login --web`)
- Auto-create your personal private repository

**AskQuestion settings:**
```json
{
  "title": "Step 2: GitHub Settings",
  "questions": [{
    "id": "github_action",
    "prompt": "We'll configure GitHub. What would you like to do?",
    "options": [
      {"id": "run_github", "label": "Start GitHub setup (run /setup-github)"},
      {"id": "already_done", "label": "Already logged in to GitHub & have my own repo"},
      {"id": "skip", "label": "Skip and go to the next lesson"}
    ]
  }]
}
```

(run_github -> Run the contents of `/setup-github`)
(already_done -> Go to completion check)
(skip -> Go to the next step)

---

### Step 3: Comprehensive Environment Check

Once all setup is complete, run `/check-setup` to verify the state of your environment.
The AI will automatically check all of the following and display a report:

- Basic tools (Python, Node.js, Git, GitHub CLI)
- Authentication & APIs (GitHub auth, Gemini API, Slack API)
- Project settings (.env, .gitignore, security hooks)
- Extensions

If any items have issues, the AI will auto-fix them or guide you to the appropriate setup command.

---

## Commands to Run

```text
/setup-start
/setup-github
/check-setup
```

## Expected Output Example

```text
Environment Check Report
| Item       | Status | Details        |
|-----------|--------|---------------|
| Python    | OK     | 3.12.x        |
| Node.js   | OK     | 24.x          |
| Git       | OK     | 2.x           |
| GitHub CLI | OK    | Logged in      |
```

## Common Troubleshooting
- AI response stops -> Type "please continue"
- GitHub authentication fails -> Re-run `/setup-github`
- Tool not found -> Install from the installer URL provided by the AI

---

## Checkpoint
- [ ] Codex Desktop or Cursor launches successfully
- [ ] Python 3.9 or higher is installed
- [ ] Node.js 18 or higher is installed
- [ ] Git is installed
- [ ] Logged in to GitHub CLI
- [ ] Pushed to your own private repository

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
      {"id": "next", "label": "Install extensions (/start-0-2)"},
      {"id": "gemini", "label": "Set up Gemini API (/start-0-3)"},
      {"id": "check", "label": "Run environment check (/check-setup)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(next -> Guide to /start-0-2)
(gemini -> Guide to /start-0-3)
(check -> Run the contents of /check-setup)
(finish -> End)

---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch02-extensions"
duration: "~5 min"
prerequisites: ["Lesson 0-1 completed"]
level: "beginner"
tags: ["setup", "extensions"]
---

# Lesson 0-2: Extension Installation

## Check Setup Progress

**Auto-run by AI:** Run `uv run python tools/setup_progress.py show` to display the current setup progress.

---

## What You'll Do

| Item | Details |
|------|---------|
| Goal | Verify and install the extensions needed for AI agent development to boost development efficiency |
| Duration | ~5 min |
| Prerequisites | Lesson 0-1 completed (Cursor is working) |
| Course Page | Refer to [Course Materials Top](https://ai-agent.camp/en/course/module-0) in parallel |

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

---

## Auto-Install Extensions

In this lesson, just run `/setup-extensions` and you're done.
**No terminal operations required. The AI handles everything automatically.**

### What the AI Does Automatically

1. Check currently installed extensions
2. Identify missing required extensions (Python, Marp, Draw.io, PlantUML, etc.)
3. Auto-install the missing ones
4. Display an installation results report

**AskQuestion settings:**
```json
{
  "title": "Extension Setup",
  "questions": [{
    "id": "action",
    "prompt": "Would you like to start the automatic extension installation?",
    "options": [
      {"id": "run", "label": "Start auto-install (run /setup-extensions)"},
      {"id": "already_done", "label": "Already installed"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(run -> Run the contents of `/setup-extensions`)
(already_done -> Go to checkpoint)
(view_html -> Provide the course page URL)
(different_lesson -> Show module list)

---

## Commands to Run

```text
/setup-extensions
```

## Expected Output Example

```text
Extension Check Results:
- Marp for VS Code: Already installed ✓
- Draw.io Integration: Newly installed ✓
- PlantUML: Newly installed ✓
All required extensions are ready!
```

## Common Troubleshooting
- Installation doesn't proceed -> Restart Cursor and re-run
- `cursor --list-extensions` not found -> Install manually from the Command Palette

---

## Extension ID List

| Extension | Extension ID | Required/Recommended |
|-----------|-------------|---------------------|
| Python | ms-python.python | Required |
| Marp | marp-team.marp-vscode | Recommended |
| Draw.io | hediet.vscode-drawio | Recommended |
| PlantUML | jebbs.plantuml | Recommended |

## Checkpoint
- [ ] Python extension is installed
- [ ] Marp extension is installed
- [ ] Draw.io extension is installed
- [ ] PlantUML extension is installed
- [ ] Syntax highlighting is working

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
      {"id": "next", "label": "Set up Gemini API (/start-0-3)"},
      {"id": "check", "label": "Run environment check (/check-setup)"},
      {"id": "back", "label": "Go back to environment verification (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(next -> Guide to /start-0-3)
(check -> Run the contents of /check-setup)
(back -> Guide to /start-0-1)
(finish -> End)

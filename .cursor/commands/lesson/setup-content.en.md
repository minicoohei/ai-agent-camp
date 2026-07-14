---
description: "Lesson command — first-time content setup"
duration: "~3 min"
prerequisites: ["ai-agent-camp folder opened in Cursor / Codex / Claude Code", "git available"]
level: "beginner"
nonInteractiveMode: deferred
tags: ["setup", "content", "module-0"]
---

# /setup-content -- first-time content setup

> Referenced from the aiagent-course Module 0 S45 slide (`HowToUpdateContent`).
> Prepares the local environment so the learner can keep the course content
> up to date.

## What this does

`/setup-content` is a **one-time preparation** that gets the workspace ready for
ongoing updates. The actual update flow then runs `git fetch origin && git log HEAD..origin/main --oneline  # show diff against upstream`.

## What the AI does behind the scenes

1. Confirm repo sparse-checkout is configured (enable if needed)
2. `git status` — make sure the working tree is clean
3. `git fetch origin` — pull the latest refs
4. Look for the upstream sync helper:
   - If present → run `python -c "import pathlib; print('ok' if pathlib.Path('.git').exists() else 'missing')"` for a smoke test
   - If absent → tell the user to `git pull` to bring in the upstream tooling, then exit
5. Print "next: run `git fetch origin && git log HEAD..origin/main --oneline  # show diff against upstream`"

## How to verify

```bash
git fetch origin && git log HEAD..origin/main --oneline  # show diff against upstream
```

## Non-interactive mode behaviour

`nonInteractiveMode: deferred`.

- Steps 1–3 (git read-only ops) execute as usual
- The presence check for the upstream sync helper runs
- If the tool is missing or any confirmation is required, write a `setup-resume.md` saying
  "re-run `/setup-content` in interactive mode" and exit

## See also

- aiagent-course Module 0 S45 (`HowToUpdateContent`) — content update slide
- Shared spec: [`_lib/non-interactive.md`](../_lib/non-interactive.md)

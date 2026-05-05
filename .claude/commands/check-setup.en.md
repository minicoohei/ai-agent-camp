---
description: "Top-level alias — see lesson/check-setup.en.md for the full body."
duration: "~2 min"
level: "beginner"
nonInteractiveMode: deferred
tags: ["setup", "check", "alias"]
---

# /check-setup -- automated environment check (top-level alias)

## Purpose

A thin wrapper so users can invoke `/check-setup` without remembering the
sub-directory namespace (`/lesson:check-setup`). All real logic lives in
[`lesson/check-setup.en.md`](./lesson/check-setup.en.md).

## Instructions to the AI

1. When this command is invoked, **Read** `.claude/commands/lesson/check-setup.en.md`
   and follow it as if it were the original.
2. If the runtime is non-interactive (`claude -p`, `cursor-agent --print`, no TTY,
   or env vars `CLAUDE_CODE_NON_INTERACTIVE=1` / `CURSOR_AGENT_PRINT=1`), use
   **deferred mode**:
   - Execute the read-only checks normally.
   - Print the report.
   - Replace any `AskQuestion` block with a single line: *"Re-run `/check-setup`
     in interactive mode to choose the next step."* Then exit.
3. In interactive mode, surface the `AskQuestion` blocks from the source file as-is.

## See also

- Shared non-interactive mode spec: [`_lib/non-interactive.md`](./_lib/non-interactive.md)
- Locale variants: [`check-setup.md`](./check-setup.md), [`check-setup.es.md`](./check-setup.es.md)

---
name: aiagent-lesson-runner
description: "A skill for starting and progressing through ai-agent-camp lessons in Codex. Triggered by requests like 'start lesson', 'next lesson', 'I want to start start-0-1', 'lesson in Codex', 'slash command lesson', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-lesson-runner
  - start lesson
  - next lesson
  - run lesson
  - Codex lesson
  - start-0-1
  - lesson runner
  - レッスン開始
  - 次のレッスン
  - レッスン実行
---

## Trigger Words
"start lesson", "next lesson", "run lesson", "slash command", "Codex lesson"

# AI Agent Lesson Runner

Use this skill to reproduce the `start-*` workflow in Codex.

## Inputs
- A lesson id such as `start-0-1`

## Workflow
1. Validate that the lesson id matches `^start-\d+-\d+$`. Reject any other value.
2. Check that `.cursor/commands/lesson/<lesson-id>.md` exists before reading it.
3. Open `.cursor/commands/lesson/<lesson-id>.md`.
4. Extract the lesson goal, prerequisites, checkpoints, command references, and referenced files.
5. Resolve the curriculum source in this order:
   - frontmatter `chapter` when it points to a `courses/aiagent/**/chapter*.yaml`
   - sibling `practice/` and `final/` docs next to that chapter
   - if `chapter` is missing, infer the best source from `courses/lessons.manifest.yaml`, the lesson URL, and the `start-X-Y` module number
6. Treat embedded `AskQuestion` / `AskUserQuestion` JSON as a conversation blueprint. In Codex, convert it into concise numbered or bulleted options in normal chat instead of pretending the Cursor UI exists.
7. For `/setup-start`, `/setup-github`, `/check-setup`, and similar setup flows, do not tell the user to run the Cursor slash command literally. Execute or describe the underlying checks and split GUI-required steps from AI-executable steps.
8. If the lesson touches Git, secrets, MCP, or external APIs, tell the user which safety doc to read first and verify prerequisites before attempting the task.
9. Guide the user through:
   - prerequisite check
   - files to read
   - actions to perform
   - completion criteria
   - next recommended lesson

## Required References
- `.cursor/commands/lesson/start-*.md`
- matching `courses/aiagent/**/chapter*.yaml` when available
- sibling `practice/` or `final/` docs for the resolved chapter
- `courses/lessons.manifest.yaml` as the fallback lookup table when a lesson markdown is missing `chapter`

## Safety
- If the lesson implies Git or environment changes, also consult `docs/codex-safety.md`.
- Never pretend the user can run the Cursor markdown command file directly in Codex.
- Never ask the user to paste secret values into chat. Reuse the repo credential workflow instead.

## Expected Output
- Lesson summary
- Ordered next actions
- Relevant files
- Done criteria
- Suggested follow-up lesson
- When the lesson contains structured choices, present the Codex-friendly options inline in the response

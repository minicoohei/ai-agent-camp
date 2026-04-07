---
name: aiagent-lesson-runner
description: Start and guide ai-agent-camp lessons in Codex（OpenAIが提供するターミナルベースのAIコーディングアシスタント） by lesson id such as start-0-1 or start-1-1. Use when the user wants the Codex equivalent of the existing slash-command lesson flow.
version: 1.0.0
author: AI Brain Partners
dependencies: []
---

## トリガーワード
「レッスン開始」「次のレッスン」「レッスン実行」「スラッシュコマンド」「Codexレッスン」

# AI Agent Lesson Runner

Use this skill to reproduce the `start-*` workflow in Codex.

## Inputs
- A lesson id such as `start-0-1`

## Workflow
1. Validate that the lesson id matches `^start-\d+-\d+$`. Reject any other value.
2. Check that `.cursor/commands/lesson/<lesson-id>.md` exists before reading it.
3. Open `.cursor/commands/lesson/<lesson-id>.md`.
4. Extract the lesson goal, prerequisites, checkpoints, and referenced files.
5. Map the lesson id to the underlying `courses/aiagent/...` files.
6. If the lesson touches Git, secrets, or MCP, tell the user which safety doc to read first.
7. Guide the user through:
   - prerequisite check
   - files to read
   - actions to perform
   - completion criteria
   - next recommended lesson

## Required References
- `.cursor/commands/lesson/start-*.md`
- `course/index.html`
- matching `courses/aiagent/**/chapter*.yaml`
- matching `practice/` or `final/` docs

## Safety
- If the lesson implies Git or environment changes, also consult `docs/codex-safety.md`.
- Never pretend the user can run the Cursor markdown command file directly in Codex.

## Expected Output
- Lesson summary
- Ordered next actions
- Relevant files
- Done criteria
- Suggested follow-up lesson

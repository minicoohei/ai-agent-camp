---
name: aiagent-command-router
description: "A skill for routing ai-agent-camp slash commands in Codex. Triggered by requests like 'run /start-0-1', 'I want to use slash commands', 'command routing', 'use Cursor commands', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-command-router
  - command routing
  - slash command
  - /start-
  - Cursor commands
  - コマンドルーティング
  - スラッシュコマンド
  - Cursorのコマンド
---

# AI Agent Command Router

Use this skill when a user types an existing ai-agent-camp command string in Codex.

## Workflow
1. Resolve the command via `data/codex-command-manifest.json`.
2. If the command is a lesson route, delegate to `aiagent-lesson-runner` with the resolved lesson id.
3. If the command is a utility route, delegate to `aiagent-utility-runner` with the resolved utility id.
4. If the command is not mapped, say it is not yet supported in Codex and show the closest source file path.

## Required References
- `data/codex-command-manifest.json`
- `tools/codex_command_router.py`
- `skills/aiagent-lesson-runner/SKILL.md`
- `skills/aiagent-utility-runner/SKILL.md`

## Output
- The resolved handler and canonical id
- The next action taken in Codex
- A clear unmapped message when no route exists

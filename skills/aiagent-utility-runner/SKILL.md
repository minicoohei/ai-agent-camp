---
name: aiagent-utility-runner
description: Run existing ai-agent-camp utility and setup commands in Codex. Use when the user invokes /guide, /tutor, /setup-api-key, /generate-slide, /utility/*, or non-start command files that originally lived in Cursor or Claude command folders.
version: 1.0.0
author: AI Brain Partners
dependencies: []
---

# AI Agent Utility Runner

Use this skill to reproduce utility and setup command workflows in Codex.

## Workflow
1. Resolve the canonical command id from `data/codex-command-manifest.json`.
2. Open the source markdown command file listed in the manifest.
3. Reuse an existing Codex skill if one already matches the task.
4. Otherwise, follow the source command instructions directly, using local scripts and files rather than pretending a slash runtime exists.
5. When useful for testing or debugging, surface the handler trace from `tools/codex_command_router.py --trace`.

## Required References
- `data/codex-command-manifest.json`
- `tools/codex_command_router.py`
- `.cursor/commands/utility/*.md`
- `.cursor/commands/*.md`

## Output
- The resolved utility id
- The source file being followed
- The local steps or scripts executed in Codex

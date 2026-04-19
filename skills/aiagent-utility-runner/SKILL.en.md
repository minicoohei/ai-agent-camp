---
name: aiagent-utility-runner
description: "A skill for executing ai-agent-camp utility and setup commands in Codex. Triggered by requests like 'run /guide', '/setup-api-key', 'utility command', 'use Cursor utility', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-utility-runner
  - utility command
  - /guide
  - /setup-api-key
  - run utility
  - utility runner
  - ユーティリティコマンド
  - ユーティリティ実行
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

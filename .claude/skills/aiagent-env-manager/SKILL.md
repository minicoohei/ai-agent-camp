---
name: aiagent-env-manager
description: Manage environment variables and credentials for ai-agent-camp. Use when setting up API keys, .env handling, or the credential manager safely.
version: 1.0.0
author: AI Brain Partners
dependencies: []
---

# AI Agent Env Manager

Use this skill for safe environment setup.

## Quickstart
- Check expected keys in `.env.example`.
- Prefer `uv run python tools/credential_manager.py store <KEY>` over editing secrets into markdown.
- Use `uv run python tools/credential_manager.py status` to verify setup without printing values.

## Primary Files
- `.env.example`
- `tools/credential_manager.py`
- `docs/codex-safety.md`

## Workflow
1. Check whether the user wants plain `.env` management or OS credential storage.
2. Prefer `uv run python tools/credential_manager.py store <KEY>` when possible.
3. If `.env` is required, limit guidance to key names and file locations.
4. Verify setup with `uv run python tools/credential_manager.py status` or masked file checks.

## Safety
- Never echo raw secret values.
- Remind the user that `.env` is local-only and must stay out of git.
- If a lesson depends on a missing key, tell the user which key name is required.

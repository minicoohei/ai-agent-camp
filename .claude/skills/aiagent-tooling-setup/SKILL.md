---
name: aiagent-tooling-setup
description: Configure Codex tooling for ai-agent-camp. Use when enabling MCP servers, installing repo hooks, or explaining tool-specific setup.
version: 1.0.0
author: AI Brain Partners
dependencies: []
---

# AI Agent Tooling Setup

Codex CLI は OpenAI が提供するターミナルベースの AI コーディングアシスタントです。

Use this skill when the user needs Codex-specific tooling guidance.

## Workflow
1. Read `docs/codex-mcp.md`.
2. Identify whether the request is about repo tools, repo hooks, or MCP servers.
3. Prefer existing repo scripts over ad hoc shell instructions.
4. Keep the final answer focused on the exact tooling path the learner needs.

## Repo Commands
- `bash scripts/install_hooks.sh`
- `uv run python tools/check_command_paths.py`
- `uv run python tools/credential_manager.py status`

## Codex CLI Installation & Authentication

### Installation
```bash
npm install -g @openai/codex
codex --version   # verify installation
```
Requires Node.js 18+.

### Authentication
Set the OpenAI API key via environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```
Or add `OPENAI_API_KEY=...` to the repo `.env` file (never commit this file).

### Recommended Runtime
| Setting | Value | Reason |
|---------|-------|--------|
| Sandbox | `workspace-write` | Restricts writes to the repo directory |
| Approval | `on-request` | Asks before external commands |

Launch with:
```bash
codex -a on-request
```

Avoid `danger-full-access` for normal learning flows. See `docs/codex-safety.md`.

### First-Time Flow
1. Install Codex CLI (`npm install -g @openai/codex`)
2. Set `OPENAI_API_KEY`
3. Open ai-agent-camp and run `bash scripts/install_hooks.sh`
4. Use `aiagent-check-setup` skill to verify environment
5. Start lessons via `aiagent-lesson-runner` skill

## Reminders
- Keep project rules in `AGENTS.md`.
- Keep machine-specific settings in the Codex config layer.
- Avoid implying that Cursor command files are executable in Codex.

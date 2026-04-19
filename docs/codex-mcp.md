# Codex MCP And Tooling Guide

## Goal
Use external tools in a way that stays explicit, reviewable, and beginner-safe.

## Tool Layers
- Repo-local tools: scripts in `tools/`
- Repo hooks: scripts in `.githooks/`
- MCP servers: machine-specific integrations added in the Codex MCP config layer

## Before Adding MCP
1. Decide whether the lesson really needs an MCP server or whether a local script is enough.
2. Confirm how credentials will be stored.
3. Read `docs/codex-safety.md` if the tool touches secrets, Git, or remote systems.

## MCP Workflow
1. Add only the servers needed for the lesson.
2. Verify the configured server list before use.
3. Keep secrets in environment variables or Credential Store, not in markdown files.
4. Do not auto-approve project MCP settings you have not reviewed.

## Useful Repo Tools
- `uv run python tools/check_command_paths.py`
- `uv run python tools/credential_manager.py status`
- `bash scripts/install_hooks.sh`

## Lessons That Commonly Need Tools
- Setup: local environment checks and credentials
- MCP: external server connections and tool discovery
- GitHub Actions / Slack / Notion / GAS: service-specific setup and API keys

## Notes
- `AGENTS.md` and Codex skills hold project-specific workflow guidance.
- The Codex config layer should hold machine-specific MCP settings.
- Tool differences should stay aligned with `aiagent-course-data` and `aiagent-course` learner-facing copy.

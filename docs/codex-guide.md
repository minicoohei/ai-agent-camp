# Codex Guide

## What Codex Uses In This Repo
- `AGENTS.md` for the Codex entry path
- `skills/` for Codex-facing workflows
- `tools/` for local helper scripts
- `.githooks/pre-commit` for repo-local safety checks

## Recommended Runtime
- Sandbox: `workspace-write`
- Approval: `on-request`
- Read `AGENTS.md` and `docs/codex-safety.md` before making changes

## First Run
1. Read `AGENTS.md`.
2. Run the setup flow through `aiagent-check-setup`.
3. Install hooks with `bash scripts/install_hooks.sh`.
4. Review `docs/codex-safety.md` and `docs/codex-mcp.md`.

## Tool Differences At A Glance

| Topic | Codex | Claude Code | Cursor |
| --- | --- | --- | --- |
| Main entry | `AGENTS.md` | `CLAUDE.md` | slash commands and `.cursor/commands/*` |
| Lesson start | `aiagent-lesson-runner` | Claude lesson flow | `/start-*` |
| Setup check | `aiagent-check-setup` | Claude workflow | `/check-setup` |
| Safety model | explicit sandbox + approval | Claude permissions + hooks | Cursor rules + commands |
| Lesson ids | `start-*` | `start-*` | `start-*` |

## Recommended Workflow
- Small task: inspect files, answer briefly, avoid over-structuring.
- Larger task: write a short plan first and keep notes as you go.
- Git, MCP, or secrets task: read the relevant safety doc before acting.

## Mapping From Existing Flows

| Existing flow | Codex entry |
| --- | --- |
| `/overview` | `aiagent-guide` |
| `/check-setup` | `aiagent-check-setup` |
| `/start-0-1` | `aiagent-lesson-runner start-0-1` |
| `/update-material` | `aiagent-material-sync` |

## Files Codex Should Read For A Lesson
1. `.cursor/commands/lesson/<lesson-id>.md`
2. Matching `courses/aiagent/.../chapter*.yaml`
3. Related `practice/`, `final/`, and supporting docs
4. Safety or tooling docs if the lesson touches Git, MCP, or secrets

## Skill Roles
- `aiagent-guide`: repo orientation, tool differences, next step
- `aiagent-check-setup`: environment readiness and safe starting checks
- `aiagent-env-manager`: `.env.local` and credential-store workflow
- `aiagent-tooling-setup`: MCP servers, hooks, and local tooling
- `aiagent-lesson-runner`: launch a lesson by `start-*` id
- `aiagent-material-sync`: update from upstream without unsafe Git shortcuts

## Important Notes
- Treat `.cursor/commands/*` as lesson reference documents, not executable Codex commands.
- Codex uses the shared curriculum but a different entry path from Cursor and Claude Code.
- `ai-agent-camp` is the wording source of truth; learner-facing UI in `aiagent-course-data` and `aiagent-course` should mirror these tool differences.

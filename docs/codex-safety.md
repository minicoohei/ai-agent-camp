# Codex Safety Guide

## Safety Rules Learners Should Remember
1. Do not run destructive commands such as `rm -rf`, `git reset --hard`, `git clean -fd`, or `git push --force`.
2. Do not paste API keys or tokens into chat.
3. Put secrets in `.env.local` first, then import them into Credential Store.
4. Do not auto-approve MCP or project config you do not understand.
5. Ask before broad deletion, broad overwrite, or history-rewriting Git work.

## Baseline Runtime
- Default runtime: `workspace-write + on-request`
- Avoid `danger-full-access` for normal lessons
- Review safety guidance before editing learner repos or handling external tools

## Secret Handling
- Keep `.env` and `.env.local` out of commits.
- Use `uv run python tools/credential_manager.py prepare-dotenv KEY_NAME` before asking the user to save a secret.
- After the user saves the value, use `uv run python tools/credential_manager.py import-dotenv KEY_NAME --delete`.
- Use `uv run python tools/credential_manager.py status` to verify presence without printing secret values.

## Safe Git Workflow
1. Check `git status` before edits, before pulls, and before commits.
2. Install repo hooks with `bash scripts/install_hooks.sh`.
3. Prefer `git fetch` + `git merge` over history rewrites.
4. Preserve local work before resolving upstream drift.

## Important Files
- `README.md`
- `CLAUDE.md`
- `AGENTS.md`
- `.env.example`
- `.githooks/pre-commit`
- `scripts/install_hooks.sh`
- `courses/`
- `skills/`

## Hooks And Guardrails
- `.githooks/pre-commit` is the repo-local baseline.
- Claude Code also uses `.claude/settings.json` and `.claude/hooks/`.
- Learners do not need to understand every hook implementation, but they should understand why dangerous actions are blocked.

## Recovery Posture
- Stop when a task might delete or overwrite large areas.
- Prefer additive changes and explicit patches.
- If sync conflicts appear, preserve local work before trying to resolve them.

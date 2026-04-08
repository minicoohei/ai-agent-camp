# ai-agent-camp Codex Guide

## Purpose
- This repository is a training repo for non-engineers learning AI agents.
- Codex is supported alongside Claude Code and Cursor.
- The curriculum is shared. Tool differences affect only entry, setup, and workflow.

## Start Here
1. Read `README.md` for the course overview.
2. Read `docs/codex-guide.md` for the Codex path.
3. Read `docs/codex-safety.md` before handling Git, secrets, or external tools.
4. Use `skills/aiagent-check-setup/SKILL.md` to confirm your local setup.
5. Use `skills/aiagent-lesson-runner/SKILL.md` with `start-0-1` to begin.

## Tool Differences
- Shared across all tools: same repo, same lessons, same safety baseline, same lesson ids.
- Codex: use `AGENTS.md`, skills in `skills/`, and explicit approval/sandbox settings.
- Claude Code: use `CLAUDE.md`, Claude commands, and Claude hooks.
- Cursor: use `.cursor/commands/*` and `.cursor/rules/*`.
- In Codex, treat `.cursor/commands/lesson/start-*.md` as reference files, not runnable commands.

## Working Rules
- Start with a short plan before edits.
- Prefer non-destructive inspection before changes.
- Reuse repo docs, tools, and skills before inventing new workflow text.
- Keep explanations short and tied to real files in this repo.
- For larger tasks, write down a lightweight plan before implementing.

## Safety Rules
- Do not run destructive commands such as `rm -rf`, `git reset --hard`, `git clean -fd`, or `git push --force`.
- Do not heavily rewrite important files without explicit confirmation.
- Treat these paths as confirmation-required: `README.md`, `CLAUDE.md`, `AGENTS.md`, `.env.example`, `.githooks/`, `scripts/install_hooks.sh`, `courses/`, `skills/`.
- Never print secret values from `.env`, Keychain, or any credential store.
- Never ask the user to paste API keys or tokens into chat.

## Secret Handling Workflow
- **Guided flow**: Run `/setup-api-key` in Cursor or Claude Code chat; the command file walks through the credential_manager steps.
- Use `uv run python tools/credential_manager.py prepare-dotenv KEY_NAME` to create a `KEY_NAME=` line in `.env.local`.
- Tell the user to paste the key on the right side of that line and save the file.
- After the user says `保存した`, run `uv run python tools/credential_manager.py import-dotenv KEY_NAME --delete`.
- Do not delete all of `.env.local`; remove only imported private keys and keep public values such as `NEXT_PUBLIC_*`.
- Keep the repo runtime precedence as `env -> credential store -> .env.local -> .env`.

## Recommended Runtime
- Sandbox: `workspace-write`
- Approval: `on-request`
- Install repo hooks with `bash scripts/install_hooks.sh`.
- Avoid `danger-full-access` for normal lessons.

## Directory Map
- `courses/aiagent/`: source curriculum and lesson metadata
- `docs/codex-guide.md`: Codex onboarding and entry flow
- `skills/`: Codex workflow skills for this repo
- `tools/`: helper and validation scripts
- `.cursor/`: Cursor-only commands and rules
- `.claude/`: Claude Code-only commands, hooks, and skills

## Complex Tasks
- For quick questions or one-file work, stay lightweight.
- For larger tasks, create a short plan and keep findings written down.
- If a lesson touches Git, secrets, or MCP, read the relevant safety docs first.

## Network Restrictions
- Codex CLI sandbox blocks many external API calls by default.
- For lessons that require live API access, the safer default is to run the relevant local script outside the sandbox with reviewable inputs.
- `codex --full-auto` is intentionally not the default for this course because it removes approval prompts and weakens the learning-time safety posture.

## Multi-Repo Note
- `ai-agent-camp` is the learner-facing repo for this training distribution.
- `aiagent-course-data` and `aiagent-course` should mirror learner-facing tool differences and onboarding copy from this repo.

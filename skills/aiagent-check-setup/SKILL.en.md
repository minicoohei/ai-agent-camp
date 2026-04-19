---
name: aiagent-check-setup
description: "A skill to verify the local environment setup for ai-agent-camp. Triggered by requests like 'check setup', 'environment check', 'is the initial setup done?', 'verify installation', 'dependency check', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-check-setup
  - check setup
  - environment check
  - initial setup
  - verify installation
  - dependency check
  - セットアップ確認
  - 環境チェック
  - インストール確認
---

## Trigger Words
"check setup", "environment check", "initial setup", "verify installation"

# AI Agent Check Setup

Use this skill to confirm the learner can safely start the course with Codex.

## Checks
- `git --version`
- `node --version`
- `npm --version`
- `python3 --version`
- `claude --version` and `cursor --version` only if the user wants cross-tool parity
- presence of `.env` or credential-store setup without printing secrets
- presence of `.git/hooks/pre-commit` after `bash scripts/install_hooks.sh`
- whether the learner has read the Codex safety path for secrets and Git

## Workflow
1. Read `docs/codex-safety.md`.
2. Review `courses/aiagent/lesson02-setup/ch01-environment/practice/checklist.md` (skip if this path does not exist).
3. Run only non-destructive checks.
4. Report missing prerequisites as a short ordered list.
5. If setup is complete, point the learner to `aiagent-lesson-runner` with the next lesson id.

## Do Not
- Print secret values.
- "Fix" setup by using destructive shell commands.
- Assume Cursor-only slash commands exist in Codex.

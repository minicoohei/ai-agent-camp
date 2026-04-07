---
name: aiagent-check-setup
description: Verify local setup for ai-agent-camp with Codex. Use for install checks, dependency checks, hook checks, and initial readiness review.
version: 1.0.0
author: AI Brain Partners
dependencies: []
---
## トリガーワード
「セットアップ確認」「環境チェック」「初期設定」「インストール確認」


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
2. Review `courses/aiagent/lesson02-setup/ch01-environment/practice/checklist.md`（このパスが存在しない場合はスキップ）.
3. Run only non-destructive checks.
4. Report missing prerequisites as a short ordered list.
5. If setup is complete, point the learner to `aiagent-lesson-runner` with the next lesson id.

## Do Not
- Print secret values.
- “Fix” setup by using destructive shell commands.
- Assume Cursor-only slash commands exist in Codex.

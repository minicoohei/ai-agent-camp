---
name: aiagent-guide
description: Orient Codex inside ai-agent-camp. Use when the user wants repo overview, tool differences, or the next recommended lesson and workflow.
version: 1.0.0
author: AI Brain Partners
dependencies: []
---

## トリガーワード
「リポジトリ案内」「次のレッスン」「どこから始める」「ツールの違い」「aiagent概要」

# AI Agent Guide

Use this skill to orient the user inside `ai-agent-camp`.

## Workflow
1. Read `AGENTS.md`.
2. Read `README.md` if a broader overview is needed.
3. If the user asks where to start, recommend:
   - `aiagent-check-setup` for environment readiness
   - `aiagent-lesson-runner` for any `start-*` lesson id
4. Explain the shared lesson model and the differences between Codex, Claude Code, and Cursor only at the level learners need.
5. For larger tasks, tell the user to make a short plan before implementation.
6. Keep explanations short and tie them to real files.

## Required References
- `AGENTS.md`
- `CLAUDE.md` — Claude Code project instructions
- `docs/codex-guide.md`

## Output
- A short orientation summary
- The relevant tool differences when needed
- The next file or skill to use
- Any safety warning that matters for the requested task

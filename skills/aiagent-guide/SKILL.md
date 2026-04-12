---
name: aiagent-guide
description: |
  ai-agent-campリポジトリの案内・オリエンテーションスキル。
  「リポジトリ案内」「次のレッスンは？」「どこから始める」「ツールの違い」「aiagent概要」等のリクエストで発動。
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-guide
  - リポジトリ案内
  - 次のレッスン
  - どこから始める
  - ツールの違い
  - aiagent概要
  - guide
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

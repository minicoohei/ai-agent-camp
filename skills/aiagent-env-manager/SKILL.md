---
name: aiagent-env-manager
description: "ai-agent-campの環境変数・認証情報を安全に管理するスキル。 「APIキーを設定」「.envを管理」「環境変数の設定」「credential managerを使いたい」「秘密情報の管理」等のリクエストで発動。"
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-env-manager
  - APIキーを設定
  - 環境変数の設定
  - .env管理
  - credential manager
  - 秘密情報の管理
  - 認証情報の設定
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

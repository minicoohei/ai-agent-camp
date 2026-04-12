---
name: aiagent-material-sync
description: "ai-agent-campの教材をupstreamから安全に同期するスキル。 「教材を最新にしたい」「upstreamから更新」「コースを同期」「git pullしたい」「教材アップデート」等のリクエストで発動。"
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-material-sync
  - 教材を最新に
  - upstreamから更新
  - コースを同期
  - 教材アップデート
  - material sync
---

# AI Agent Material Sync

Use this skill for safe curriculum updates.

## Workflow
1. Check `git status`.
2. Warn about local changes and untracked files before sync.
3. Check `git remote -v` and choose a valid remote.
4. If `upstream` exists, prefer `git fetch upstream` and `git merge upstream/main`.
5. If `upstream` does not exist, fall back to the tracked default remote, usually `origin/main`.
6. If neither remote is usable, stop and tell the user which remote name is missing.
7. Explain conflicts and recovery without using force push or destructive cleanup.

## Example Failure Message
- `upstream` is not configured in this clone. Use `origin` instead or add `upstream` before syncing.

## References
- `README.md`
- `docs/codex-safety.md`

## Safety
- Do not use `git reset --hard`.
- Do not use `git clean -fd`.
- Do not force push as a “fix”.

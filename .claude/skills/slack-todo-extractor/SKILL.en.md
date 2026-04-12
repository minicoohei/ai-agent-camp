---
name: slack-todo-extractor
description: "A skill that searches Slack synced data for mentions and extracts TODOs/tasks with status determination. Triggered by requests like 'Extract tasks from Slack', 'Check TODOs', 'Check mentions'."
triggers:
  - Extract tasks from Slack
  - Check TODOs
  - Check mentions
  - Tasks for me
  - Unhandled Slack tasks
  - slack-todo-extractor
  - Slack TODO
---

# Slack TODO Extraction Skill

## Overview

A skill that searches Slack synced data (`slack-sync/data/`) for mentions addressed to a specific user, and extracts TODOs/tasks with status determination including thread replies.

## Quick Start

```bash
# Basic (keyword-based)
uv run python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "YourName,your-username" \
  --period "2026-01-06:2026-01-08"

# LLM-based (high accuracy, requires GEMINI_API_KEY)
uv run python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "YourName,your-username" \
  --period "1/6:8" \
  --use-llm
```

## Input Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--users`, `-u` | Yes | Target user names (comma-separated) | `YourName, your-username` |
| `--period`, `-p` | Yes | Search period | `2026-01-06:2026-01-08` or `1/6:8` |
| `--workspace`, `-w` | No | Workspace (all if omitted) | `my-workspace`, `my-workspace-2` |
| `--use-llm` | No | Use LLM (Gemini 2.0 Flash) for determination | - |
| `--output`, `-o` | No | Output format | `markdown` (default) or `json` |

## Processing Flow

### Step 1: Mention Search
Search `slack-sync/data/{workspace}/*.md` for messages containing `@username`

### Step 2: Thread Reply Check
For each mention:
- Extract thread replies (`> ####` format)
- Check subsequent channel messages on the same day

### Step 3: Status Determination

#### Keyword-based (without `--use-llm`)
| Condition | Status |
|-----------|--------|
| Target user replied "done", "completed" etc. | completed |
| Requester replied "thank you", "I'll check" etc. | completed |
| Target user replied "understood", "will do" etc. | in_progress |
| No reply | pending |

#### LLM-based (with `--use-llm`)
Gemini 2.0 Flash understands context:
- "Understood" is acceptance, not completion
- If a deadline is set, status is in_progress before that deadline
- Requester's confirmation reply determines completion

## Environment Setup

### GEMINI_API_KEY (when using LLM mode)

Store in Credential Store:
```bash
uv run python tools/credential_manager.py store GEMINI_API_KEY
```

## Prerequisites

- `slack-sync/` Slack sync must be completed (see `data/slack-sync/`)

## Related Skills

- `slack-search`: Full-text search of Slack messages
- `slack-task-manager`: Integrated task management

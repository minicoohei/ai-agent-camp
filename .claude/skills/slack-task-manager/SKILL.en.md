---
name: slack-task-manager
description: "A sub-agent for Slack search, TODO extraction, and task management. Extracts tasks from multiple data sources and prioritizes them. Triggered by requests like 'Search Slack', 'Extract tasks', 'Check TODOs', 'Check mentions'."
triggers:
  - Search Slack
  - Slack search
  - Find channels
  - Check mentions
  - Extract TODOs
  - Extract tasks
  - Task list
  - Unhandled tasks
  - Requested items
---

# Slack/Task Manager Sub-Agent

A sub-agent that executes Slack search, TODO extraction, and task management in a dedicated context.

## Purpose

Separates Slack data and task management from the main agent's context to:
- Efficiently search large volumes of Slack messages
- Integrate task extraction from multiple data sources
- Return only summarized search results

## Feature List

| Feature | Script | Description |
|---------|--------|-------------|
| Slack Search | `slack_search.py` | BookRAG-based semantic search |
| TODO Extraction | `extract_todos.py` | TODO extraction from mentions with status determination |
| Task Extraction | `extract_tasks.py` | Task extraction from multiple sources |

## 1. Slack Search (`tools/slack_search.py`)

Semantic search utilizing BookRAG-based hierarchical indexing.

### Features

| Method | Description |
|--------|-------------|
| `get_workspace_overview()` | Workspace overview |
| `find_channels(query)` | Channel search |
| `get_channel_detail(channel_id)` | Channel details |
| `find_related_channels(channel_id)` | Related channel search |
| `find_person(name)` | Person search |

## 2. TODO Extraction (`skills/slack-todo-extractor/scripts/extract_todos.py`)

Extracts tasks from Slack mentions and determines their status.

### Usage

```bash
# Basic (keyword-based)
python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "YourName,your-username" \
  --period "2026-01-06:2026-01-08"

# LLM-based (high accuracy, requires GEMINI_API_KEY)
python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "YourName,your-username" \
  --period "1/6:8" \
  --use-llm

# JSON output
python skills/slack-todo-extractor/scripts/extract_todos.py \
  -u "YourName" -p "1/6:8" --use-llm -o json
```

### Status Determination

| Status | Condition |
|--------|-----------|
| Completed | Target user replied "done" etc. / Requester replied "thank you" etc. |
| In progress | Target user replied "understood", "will do" etc. |
| Pending | No reply |

## 3. Task Extraction (`tools/extract_tasks.py`)

Automatically extracts and prioritizes tasks from multiple data sources.

### Data Sources

| Source | Description |
|--------|-------------|
| Git | Changed files, uncommitted work |
| Activity Logger | Recent activity |
| SpecStory | In-progress tasks |
| Slack-sync | Requests, mentions |
| Output | Calendar, Gmail, voice memos |
| Notion | Databases/pages |

### Usage

```bash
# Extract tasks from all sources
uv run python tools/extract_tasks.py

# Specific sources only
uv run python tools/extract_tasks.py --sources git,slack

# With HowToDo generation
uv run python tools/extract_tasks.py --with-howtodo

# HTML output
uv run python tools/extract_tasks.py --format html --output tasks.html
```

## Prerequisites

- `slack-sync/` Slack sync must be completed
- Thread replies require pre-synchronization if needed

```bash
# Slack sync
python slack-sync/scripts/fetch_slack.py --workspace my-workspace

# Also fetch thread replies
python slack-sync/scripts/fetch_slack.py --workspace my-workspace --refresh-threads
```

## Dependencies

```txt
python-dotenv>=1.0.0
google-generativeai>=0.3.0  # When using LLM mode
```

## Environment Variables

```bash
# When using LLM mode
GEMINI_API_KEY=your_api_key

# When using Notion integration
NOTION_TOKEN=your_token
```

## Use Cases

1. **Channel search**: Find project-related channels
2. **TODO check**: Extract tasks from mentions addressed to you
3. **Task integration**: List tasks from multiple sources
4. **Prioritization**: Organize tasks by deadline and importance

---
name: slack-search
description: "A skill for semantic searching of Slack channels and messages. Triggered by requests like 'Search Slack', 'Find channels', 'Find messages'."
triggers:
  - Search Slack
  - Find channels
  - Find messages
  - Related channels
  - Search events
  - slack-search
  - Slack search
---

# Slack Search Skill

Slack semantic search utilizing BookRAG-based hierarchical indexing.

## Quick Start

```python
import sys
from pathlib import Path
# Add project root tools/ directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools"))
from slack_search import SlackSearch

search = SlackSearch()

# Workspace overview
overview = search.get_workspace_overview()

# Channel search (semantic search)
results = search.find_channels("DX exhibition")

# Channel details
detail = search.get_channel_detail("my-workspace/example-channel")

# Related channel exploration
related = search.find_related_channels("my-workspace/example-channel")

# Person search
persons = search.find_person("Shimizu")

# Event search
events = search.find_events("DX")

# Timeline search
timeline = search.get_timeline("2025-12-01", "2025-12-31")
```

## Available Search Functions

### 1. Workspace Overview (`get_workspace_overview`)
Get overall statistics and category structure.

### 2. Channel Search (`find_channels`)
Semantic search across channel names, topics, and summaries.

### 3. Channel Details (`get_channel_detail`)
Get detailed information for a specific channel including overview, topics, participants, activity period, file paths, and related channels.

### 4. Related Channel Exploration (`find_related_channels`)
Explore related channels based on graph structure. Supports depth parameter for indirect relationships.

### 5. Person Search (`find_person`)
Search for people by speaker name or mentions. Returns name, aliases, channel count, and channel list.

### 6. Event Search (`find_events`)
Search for exhibitions, meetings, and other events.

### 7. Category Listing (`list_channels_by_category`)
List channels by category (cafe, project, product, sales, notify, partner, event, external).

### 8. Timeline Search (`get_timeline`)
Search activity by date range.

### 9. Output Sources (`get_output_sources`)
Statistics for calendar, gmail, drive, and voicememo outputs.

## CLI Commands

```bash
# Workspace overview
uv run python tools/slack_search.py overview [workspace]

# Channel search
uv run python tools/slack_search.py find "query"

# Channel details
uv run python tools/slack_search.py detail "channel_id"

# Related channels
uv run python tools/slack_search.py related "channel_id"

# Person search
uv run python tools/slack_search.py person "name"

# Event search
uv run python tools/slack_search.py events [query]

# By category
uv run python tools/slack_search.py category "category_name"

# Timeline
uv run python tools/slack_search.py timeline "start_date" "end_date"
```

## Index Update

The index is automatically updated daily via GitHub Actions.
Manual update:

```bash
python3 slack-sync/scripts/build_book_index.py
```

## Overview

A skill that uses BookRAG-based hierarchical indexing for semantic search of Slack channels and messages. Supports channel search, person search, event search, and timeline search.

## Troubleshooting

| Error | Solution |
|-------|----------|
| Index file not found | Rebuild the index with `python3 slack-sync/scripts/build_book_index.py` |
| No results found | Change query keywords or check available categories with `get_workspace_overview()` |

## Success Criteria

- [ ] Related channels or messages are returned for the search query
- [ ] Search results include channel name, summary, and relevance
- [ ] Completed without errors

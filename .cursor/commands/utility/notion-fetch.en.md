# Notion Fetch - Notion Integration

Fetches Notion pages and databases and outputs them in Markdown format.

## Features

- Fetch and convert single pages to Markdown
- Output databases in table format
- Search within Notion
- Convert rich text (bold, italic, code, etc.)
- Support for various block types (headings, lists, code, quotes, etc.)

## Execution Steps

### Step 1: Extract Parameters

Extract the following from the user's input:
- **Command**: page / database / search
- **ID/URL**: Notion page ID or URL
- **Output destination**: File path (displayed on screen if omitted)

### Step 2: Run the Tool

```bash
# Fetch a page
python src/notion_fetcher.py page <page_id_or_url>

# Fetch a database
python src/notion_fetcher.py database <database_id_or_url>

# Search
python src/notion_fetcher.py search "keyword"
```

### Step 3: Display Results

Present the output Markdown to the user.

## Options

### page command

| Option | Description |
|--------|-------------|
| `--output PATH` / `-o` | Output file path |

### database command

| Option | Description |
|--------|-------------|
| `--output PATH` / `-o` | Output file path |
| `--include-content` / `-c` | Include the content of each page |

### search command

| Option | Description |
|--------|-------------|
| `--type TEXT` / `-t` | Filter: page / database |

## Usage Examples

### Fetch a page

```
/notion-fetch https://www.notion.so/myworkspace/Page-Name-abc123
```

### Fetch a database

```
/notion-fetch database abc123def456 --output tasks.md
```

### Search

```
/notion-fetch search "project plan"
```

### Detailed database output

```
/notion-fetch database abc123 --include-content
```

## Output Format

### Page

```markdown
---
id: abc123...
created: 2026-01-15T10:00:00.000Z
modified: 2026-01-16T14:30:00.000Z
title: Page Title
url: https://www.notion.so/...
---

# Page Title

## Section 1

Body text...

- List item 1
- List item 2

> Quoted text

```python
code block
```
```

### Database

```markdown
---
id: def456...
type: database
title: Task Management
total_items: 25
---

# Task Management

| Task Name | Status | Assignee | Due Date |
|-----------|--------|----------|----------|
| Task A | In Progress | Tanaka | 2026-01-20 |
| Task B | Complete | Sato | 2026-01-18 |
```

## Prerequisites

Notion authentication is **OAuth-only**. Either of the following completed setups will work:

- You're already logged in via `ncli login` (browser OAuth approved)
- Or your Claude Code / Cursor is connected to the **Notion Hosted MCP** (`https://mcp.notion.com/mcp`, Streamable HTTP + OAuth)

See `/setup-notion` for the full setup walkthrough.

> No API key (`secret_xxx`) or `NOTION_TOKEN` is required. Per-page "Add connections" sharing in Notion is also unnecessary (OAuth grants workspace-wide access).

## Supported Block Types

| Type | Support Status |
|------|---------------|
| paragraph | ✅ |
| heading_1/2/3 | ✅ |
| bulleted_list_item | ✅ |
| numbered_list_item | ✅ |
| to_do | ✅ |
| toggle | ✅ |
| code | ✅ |
| quote | ✅ |
| callout | ✅ |
| divider | ✅ |
| image | ✅ |
| bookmark | ✅ |
| child_page | ✅ (title only) |
| child_database | ✅ (title only) |
| table | ⚠️ (basic support) |

## Related Commands

- `/api-setup-wizard` - Notion API setup
- `/extract-tasks` - Task extraction (Notion integration planned)

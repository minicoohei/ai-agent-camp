---
nonInteractiveMode: compliant
---

# Extract Tasks - Task Extraction

Extract tasks from multiple data sources and list them with priority rankings.

## Data Sources

1. **Git** - Latest commit information, run git pull
2. **Activity Logger** - Recent work log summary
3. **SpecStory** - In-progress tasks (with remaining TODOs)
4. **Slack-sync** - Requests from each workspace
5. **Output** - Calendar, Gmail, voice memos
6. **Notion** - Task database (when NOTION_API_KEY is configured)

## Steps

### Step 1: Extract Parameters

Extract the following from the user's input:
- **Days**: Number of days for SpecStory scope (default: 3)
- **Workspace**: Slack target (default: all)
- **git pull**: Whether to execute (default: yes)

### Step 2: Run the Tool

```bash
uv run python tools/extract_tasks.py --days {days} --workspaces {workspace}
```

### Step 3: Display Results

Present the output Markdown to the user.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--days INT` | Number of days for SpecStory scope | 3 |
| `--workspaces TEXT` | Slack targets (comma-separated) | all |
| `--output PATH` | Output file path | stdout |
| `--format TEXT` | Output format: markdown / json / html | markdown |
| `--git-pull` | Execute git pull | True |
| `--no-git-pull` | Skip git pull | - |
| `--notion-db TEXT` | Notion database ID | Environment variable |
| `--no-notion` | Skip Notion retrieval | - |
| `--howtodo` | Generate HowToDo procedures | - |

## Usage Examples

### Basic execution

```
/extract-tasks
```

Runs with default settings (3 days, all workspaces).

### Specify number of days

```
/extract-tasks 7 days
```

Runs with `--days 7`.

### Specific workspaces only

```
/extract-tasks workspace-1 and workspace-2 only
```

Runs with `--workspaces workspace-1,workspace-2`.

### Without git pull

```
/extract-tasks without git pull
```

Runs with `--no-git-pull`.

### Output in JSON format

```
/extract-tasks in json format
```

Runs with `--format json`.

## Output Format

### Priority A: In-progress tasks
- Sessions from SpecStory with remaining TODOs

### Priority B: Slack requests
- Recent messages from each workspace
- Messages with mentions are displayed with higher priority

### Priority C: Recurring tasks
- Today's calendar events
- Recent emails
- Voice memos

## Notes

- git pull is automatically executed unless `--no-git-pull` is specified
- Activity Logger shows the last 2 days
- When there is a large amount of data, results are limited to approximately the top 5 items

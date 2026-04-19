# Guide - Suggest Next Actions

This command uses `tools/guide_action.py` to analyze the current situation from SpecStory history and present background context and next actions.

## Features

- Analyze the current situation from SpecStory history
- Provide **background and context explanations**
- Clearly present **next actions**
- Generate **example prompts for use with the next Agent**
- **Explicitly list referenced files**

## Steps

### Step 1: Get the SpecStory File List

First, retrieve the file list in JSON format with the following command:

```bash
uv run python tools/guide_action.py --list --json
```

### Step 2: Display the File Selection UI

Based on the retrieved JSON, use the AskQuestion tool to display a file selection UI to the user.

**AskQuestion configuration:**
- `title`: "Select SpecStory files to analyze"
- `questions`: Present each file from the retrieved JSON as a selection option
- `allow_multiple`: true (allow multiple selections)

Example:
```json
{
  "title": "Select SpecStory files to analyze",
  "questions": [{
    "id": "specstory_files",
    "prompt": "Select the files to analyze (multiple selections allowed)",
    "options": [
      {"id": "2025-12-18_10-00Z-example.md", "label": "2025-12-18 10:00Z - Example Title"},
      ...
    ],
    "allow_multiple": true
  }]
}
```

### Step 3: Run Analysis with Selected Files

Using the file names selected by the user, execute the following command:

```bash
uv run python tools/guide_action.py --names "{selected_filenames_comma_separated}" --output "{output_path}"
```

Example:
```bash
uv run python tools/guide_action.py --names "2025-12-18_10-00Z-example.md,2025-12-17_09-30Z-another.md"
```

### Step 4: Verify Results

- Check the path of the generated HTML file and report it to the user.
- Guide the user on how to open it with Live Server.

## Options

| Option | Description |
|--------|-------------|
| `--list`, `-l` | Display SpecStory file list |
| `--json`, `-j` | Output in JSON format (use with --list) |
| `--names`, `-n` | Specify by filename (comma-separated) |
| `--select`, `-s` | Specify by number (e.g., 1,2,3) |
| `--files`, `-f` | Analyze the latest N files (default: 3) |
| `--output`, `-o` | Output file path |

## Output Content

- **Referenced SpecStory file list**: Which files were analyzed
- **Current situation summary**: What is currently being worked on
- **Background explanation**: Why this work is necessary
- **Next actions**: Specific things to do
- **Prompt examples**: Prompts to input into a new Agent
- **Expected results**: What will be achieved

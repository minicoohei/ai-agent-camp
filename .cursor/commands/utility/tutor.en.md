---
nonInteractiveMode: deferred
---

# Tutor - Learning Content Generation

This command uses `tools/tutor_generate.py` to automatically generate beginner-friendly learning HTML from various input sources.

## Features

- **Multiple input sources**: Topic / File / Text / SpecStory
- Automatically generates **tutorial-format HTML** for beginners
- **Displays referenced files**
- **Shows PlantUML processing flow diagrams**

## Execution Steps

### Step 1: Select Input Source

Use the AskQuestion tool to have the user select an input source:

```json
{
  "title": "Select learning content input source",
  "questions": [{
    "id": "input_source",
    "prompt": "Which method would you like to use to create the tutorial?",
    "options": [
      {"id": "topic", "label": "Specify topic - Generate a tutorial on any topic"},
      {"id": "file", "label": "Specify file - Generate a usage manual for a code file"},
      {"id": "text", "label": "Specify text - Generate an explanation for pasted code/text"},
      {"id": "specstory", "label": "SpecStory analysis - Analyze learning gaps from conversation history"}
    ]
  }]
}
```

### Step 2: Process According to Input Source

#### For topic specification

Ask the user to enter a topic, then execute:

```bash
uv run python tools/tutor_generate.py --topic "topic name"
```

Examples:
```bash
uv run python tools/tutor_generate.py --topic "Git Basics"
uv run python tools/tutor_generate.py --topic "Introduction to GitHub Actions"
uv run python tools/tutor_generate.py --topic "Python Decorators"
```

#### For file specification

Ask the user to select/enter a file, then execute:

```bash
uv run python tools/tutor_generate.py --file "file_path"
```

Examples:
```bash
uv run python tools/tutor_generate.py --file "src/auth.py"
uv run python tools/tutor_generate.py --file "tools/guide_action.py"
```

#### For text specification

Ask the user to input text/code, then execute:

```bash
uv run python tools/tutor_generate.py --text "input text"
```

#### For SpecStory analysis

1. First, get the file list:
```bash
uv run python tools/tutor_generate.py --list --json
```

2. Display file selection UI with AskQuestion:
```json
{
  "title": "Select SpecStory files to analyze",
  "questions": [{
    "id": "specstory_files",
    "prompt": "Select the files to analyze (multiple selection allowed)",
    "options": [...],
    "allow_multiple": true
  }]
}
```

3. Execute with the selected files:
```bash
uv run python tools/tutor_generate.py --names "file1.md,file2.md"
```

### Step 3: Verify Results

- Confirm the path of the generated HTML file and report it to the user.
- Provide instructions on how to open it with Live Server.

## Option List

| Option | Description |
|--------|-------------|
| `--topic`, `-t` | Specify a topic to generate a tutorial |
| `--file` | Specify a file path to generate a manual |
| `--text` | Specify text to generate an explanation |
| `--specstory` | Analyze learning gaps from SpecStory history |
| `--list`, `-l` | Display SpecStory file list |
| `--json`, `-j` | Output in JSON format (use with --list) |
| `--names`, `-n` | Specify by file name (comma-separated) |
| `--select`, `-s` | Specify by number (e.g., 1,2,3) |
| `--files`, `-f` | Number of files to analyze (default: 1) |
| `--output`, `-o` | Output file path |

## Output Contents (Tutorial Format)

- **Input source information**: Which source the content was generated from
- **Processing flow diagram**: PlantUML visualization of the process
- **Overview**: Introduction to the topic and significance of learning it
- **Prerequisites**: Required foundational knowledge
- **Sections**: Step-by-step explanations
  - Detailed descriptions
  - Code examples
  - Key points & tips
- **Common mistakes and cautions**: Points beginners tend to trip on
- **Summary**: Review of learned content
- **Next steps**: What to learn next

## Usage Examples

### Generate tutorial from a topic
```
/tutor
-> Select "Specify topic"
-> Enter "Docker Basics"
```

### Generate manual from a file
```
/tutor
-> Select "Specify file"
-> Select or enter a file
```

### Analyze learning gaps from SpecStory
```
/tutor
-> Select "SpecStory analysis"
-> Select multiple files to analyze
```

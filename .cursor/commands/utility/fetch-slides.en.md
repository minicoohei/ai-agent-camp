# Fetch Slides - Google Slides Retrieval

Retrieve Google Slides presentation content in Markdown/JSON format.

## Features

- Text extraction from slides
- Table conversion to Markdown
- Speaker notes retrieval
- Metadata annotation (creation date, last editor, etc.)

## Steps

### Step 1: Extract Parameters

Extract the following from the user's input:
- **URL/ID**: Google Slides URL or presentation ID
- **Output format**: markdown / json (default: markdown)
- **Output destination**: File path (defaults to screen display if omitted)

### Step 2: Run the Tool

Use the Google Slides API to retrieve content. After setting up authentication with `/setup-google-api`, follow these steps:

```bash
# Check/configure Google API authentication
uv run python tools/api_setup_wizard.py guide google
```

Use Claude Code / Cursor's interactive features to specify the URL or ID, retrieve slide content, and format it.

### Step 3: Display Results

Present the output Markdown or JSON to the user.

## Usage Examples

### Retrieve from URL

```
/fetch-slides https://docs.google.com/presentation/d/1abc123xyz/edit
```

### Retrieve from ID

```
/fetch-slides 1abc123xyz
```

### Save in JSON format

```
/fetch-slides 1abc123xyz --output slides.json --format json
```

### Save to Markdown file

```
/fetch-slides https://docs.google.com/presentation/d/1abc123xyz/edit -o output/slides.md
```

## Output Formats

### Markdown

```markdown
---
id: 1abc123xyz
title: Presentation Title
created: 2026-01-15T10:00:00Z
modified: 2026-01-16T14:30:00Z
authors: user@example.com
total_slides: 10
---

# Presentation Title

## Table of Contents

1. [Introduction](#slide-1)
2. [Overview](#slide-2)
...

---

## Slide 1 {#slide-1}

Slide content...

> **Speaker Notes:**
> Speaker notes are displayed here

---

## Slide 2 {#slide-2}

...
```

### JSON

```json
{
  "id": "1abc123xyz",
  "title": "Presentation Title",
  "total_slides": 10,
  "slides": [
    {
      "number": 1,
      "content": ["Slide text..."],
      "speaker_notes": "Speaker notes..."
    }
  ]
}
```

## Prerequisites

Google API authentication is required. Set up one of the following:

1. **Service account**: `GCP_SA_KEY` environment variable
2. **OAuth**: `token.json` file

Setup method:

```bash
uv run python tools/api_setup_wizard.py guide google
```

## Related Commands

- `/api-setup-wizard` - Google API setup
- `/generate-slide` - Slide image generation

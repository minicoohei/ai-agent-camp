---
name: check-inbox
description: "An integrated skill for extracting actionable items and tasks from email and Slack. Uses Gemini 3.0 Flash for context analysis, generating priorities and reply drafts. Triggered by requests like 'check inbox', 'check TODOs', 'messages to reply', 'check email', etc."
triggers:
  - check-inbox
  - check inbox
  - check TODOs
  - messages to reply
  - check email
  - check Slack
  - inbox
  - 受信箱チェック
  - TODO確認
  - メール確認
---

## Trigger Words
"check inbox", "check TODOs", "messages to reply", "check email", "check Slack"

# /check-inbox - Inbox Task Extraction

Extracts items requiring replies from email (Gmail) and Slack, and lists them with priority levels.

## Quick Start

```bash
# Basic execution (past 3 days)
python skills/check-inbox/scripts/check_inbox.py

# Check past 7 days
python skills/check-inbox/scripts/check_inbox.py --days 7

# Email only
python skills/check-inbox/scripts/check_inbox.py --email-only

# Slack only
python skills/check-inbox/scripts/check_inbox.py --slack-only
```

## Features

- **Email analysis**: Extracts emails from Markdown files in `/output/gmail/`
  - Automatically excludes marketing and automated notification emails
  - Only analyzes emails from real people via LLM

- **Slack analysis**: Extracts mentions from `slack-sync/data/`
  - Searches identifiers from `--users` option or default settings
  - Considers thread replies in analysis

- **LLM analysis** (Gemini 3.0 Flash)
  - Determines whether a reply is needed
  - Sets priority (high/medium/low)
  - Generates reply drafts

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--days, -d` | How many past days to check | 3 |
| `--email-only` | Check email only | - |
| `--slack-only` | Check Slack only | - |
| `--output, -o` | Output file path | `inbox-{date}.md` |
| `--gmail-dir` | Gmail data directory | Auto-detect |
| `--slack-dir` | Slack data directory | Auto-detect |
| `--workspace, -w` | Slack workspace | All |
| `--users, -u` | Target users to search (comma-separated) | Default list |
| `--no-llm` | Skip LLM analysis | - |
| `--quiet, -q` | Suppress progress display | - |
| `--notify-line` | Send results to LINE notification | - |

## Output Example

```markdown
# Inbox Tasks - 2026-01-28

## High Priority

### Email
- **[Re: Project Progress]** from: Taro Tanaka (2026-01-27)
  - Reason: Deadline-bound confirmation request
  - Draft reply: "Thank you for your message. I will review and report back by tomorrow."

### Slack
- **[#pj_xxx]** @{YOUR_NAME} (2026-01-27 14:30)
  - Content: Question about API specifications
  - Reason: Direct question, requires answer
  - Draft reply: "I've reviewed the API specifications..."

## Medium Priority
...

---
Generated: 2026-01-28 10:00:00
Period: Past 3 days
Emails: 15 -> Actionable: 3
Slack: 42 -> Actionable: 8
```

## Environment Setup

### Required Environment Variables

Set the following in `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
# or
GOOGLE_API_KEY=your_api_key_here

# LINE notification (when using --notify-line)
LINE_CHANNEL_ACCESS_TOKEN=your_line_access_token
LINE_USER_ID=your_line_user_id
```

### Dependencies

```bash
uv add google-generativeai python-dateutil
```

## Data Directories

The following paths are auto-detected:

**Email**:
- `./output/gmail/`
- `~/output/gmail/`

**Slack**:
- `./slack-sync/data/`
- `~/githubactions_fordata/slack-sync/data/`

## Related Skills

- `/email-tasks` - Email-specific task extraction
- `/slack-tasks` - Slack-specific task extraction

## Overview

A skill that automatically extracts messages and tasks requiring replies from Gmail and Slack. Uses Gemini 3.0 Flash for context analysis, generating prioritized reply drafts.

## Troubleshooting

| Error | Solution |
|-------|----------|
| API key not found | Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` in `.env` |
| No Gmail data found | Check if email data exists in `output/gmail/` directory |
| No Slack data found | Check if `slack-sync/data/` directory is synced |

## Success Criteria

- [ ] Tasks are listed by priority (high/medium/low)
- [ ] Reply drafts are generated for each task
- [ ] Output Markdown file is saved correctly

## Usage

See the "Quick Start" section above. Basic example:

```bash
# Check inbox for past 3 days
python skills/check-inbox/scripts/check_inbox.py

# Slack only, past 7 days
python skills/check-inbox/scripts/check_inbox.py --slack-only --days 7
```

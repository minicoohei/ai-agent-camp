---
nonInteractiveMode: incompatible
---

# Gmail Pending Replies - Extract Unreplied Emails

Extract emails that need a reply from Gmail and **automatically generate reply drafts**.

## Target Categories

1. **Unreplied emails**: Emails addressed to you (TO/CC) that you haven't replied to
2. **Thread replies**: Threads you started where the last reply is from someone else

## Data Sources

### Method 1: Use Synced Data (Recommended)

Analyze Markdown files synced to `output/gmail/{account_name}/`.

| Account | Path | Your Address |
|---------|------|-------------|
| default | `output/gmail/default/` | `user@example.com` |
| work | `output/gmail/work/` | Corresponding address |

### Method 2: Via API (When GMAIL_ACCOUNTS_CONFIG Is Set)

```bash
python src/get_gmail_pending_replies.py --days {days}
```

## Steps

### Step 1: Extract Parameters

Extract the following from the user's input:
- **Days**: Number of target days (default: 7)
- **Account**: Specific account only (default: all)
- **Output format**: markdown / json (default: screen display)

### Step 2: Scan Emails

Analyze synced data at `output/gmail/{account}/YYYY-MM-DD/*.md` and extract:
- Received emails from people other than yourself
- Exclude notification emails (noreply, bank, peatix, etc.)
- Exclude meeting invitations (.ics attachments)
- Exclude emails with the same subject where you've already replied

### Step 3: Display Results + Auto-Generate Reply Drafts

1. Display the list of unreplied emails
2. **Analyze the content of each email and determine its type**:
   - **Request/Task**: Something requiring a specific action
   - **Question**: Something requiring an answer
   - **Information sharing**: No reply needed (shared via CC, etc.)

3. **Automatically generate reply drafts for request and question emails**:
   - Read the email body
   - Reference related project information if available
   - Create an appropriate reply draft

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--days INT` / `-d` | Number of target days | 7 |
| `--account TEXT` / `-a` | Specific account only (label name) | all |
| `--output PATH` / `-o` | Output file path (.json / .md) | stdout |

## Usage Examples

### Basic execution

```
/gmail-pending-replies
```

Runs with default settings (7 days, all accounts).

### Specify number of days

```
/gmail-pending-replies 3 days
```

Runs with `--days 3`.

### Specific account only

```
/gmail-pending-replies personal account only
```

Runs with `--account personal`.

### Save as Markdown

```
/gmail-pending-replies save to output/pending.md
```

Runs with `--output output/pending.md`.

## Prerequisites

### When Using Synced Data (Recommended)

Emails must be synced to `output/gmail/{account_name}/`.

```
output/gmail/
├── my-account/
│   ├── 2026-01-27/
│   │   ├── index.md          # Daily index
│   │   ├── 19bfd03adcbf0235.md  # Individual email
│   │   └── ...
│   └── ...
└── work/
    └── ...
```

Format of each email file:
```yaml
---
id: 19bfd03adcbf0235
subject: Subject
from: Sender <email@example.com>
date: 2026-01-27 10:13:51
attachments: file1.pdf, file2.xlsx  # Optional
---

# Subject

Email body...
```

### When Using API (Optional)

The `GMAIL_ACCOUNTS_CONFIG` environment variable must be set with multi-account configuration:

```json
{
  "accounts": [
    {
      "label": "work",
      "type": "service_account",
      "subject": "user@company.com"
    },
    {
      "label": "personal",
      "type": "oauth",
      "client_id_env": "GMAIL_PERSONAL_CLIENT_ID",
      "client_secret_env": "GMAIL_PERSONAL_CLIENT_SECRET",
      "refresh_token_env": "GMAIL_PERSONAL_REFRESH_TOKEN"
    }
  ]
}
```

## Output Format

### 1. Unreplied Email List

```
Emails requiring a reply (default): 2 items
Target period: Past 7 days

======================================================================

1. About the project progress report - Action required
   Date: 2026-01-27 10:13
   From: Taro Yamada <taro.yamada@example.com>
   Type: Request/Task
   Summary: Report review request
   Link: https://mail.google.com/mail/u/0/#inbox/xxx

2. About the monthly meeting agenda
   Date: 2026-01-23 13:53
   From: Hanako Sato <hanako.sato@example.com>
   Type: Information sharing (CC)
   Summary: Agenda draft sharing
   Link: https://mail.google.com/mail/u/0/#inbox/yyy

======================================================================
```

### 2. Auto-Generated Reply Drafts (for request/question emails only)

Reply drafts are automatically generated for emails containing requests or questions:

```
---
## Reply Draft: About the project progress report

Subject: Re: About the project progress report

Dear Mr. Yamada,

Thank you for reaching out.
I acknowledge your request for the report.

I'm planning to prepare the report in the following categories:

[1. Information gathering/search]
- Cross-search and summary generation for Slack/Gmail/Calendar

[2. Document/material creation]
- Automatic generation of workflow diagrams

[3. Formatting/transcription]
- Data cleansing and format conversion

I will send the materials by the end of this week.
---
```

## Exclusion Patterns

The following emails are automatically excluded:

| Category | Example Patterns |
|----------|-----------------|
| Notifications | noreply, no-reply, notification |
| Banks | @bank.gmo-aozora.com |
| Events | @peatix.com, @morningpitch.com |
| Auto-sent | spamdigest, Moderator |
| Meeting invitations | .ics attachments, teams.microsoft.com |

## Related Commands

- `/extract-tasks` - Task extraction from multiple sources (includes Gmail)
- `/slack-pending-replies` - Slack version of unreplied message extraction

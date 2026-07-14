---
name: slack-unanswered
description: "A skill that detects unanswered Slack messages and generates reply drafts. Triggered by requests like 'Unanswered messages', 'Messages I haven't replied to', 'Check Slack'."
triggers:
  - Unanswered messages
  - Messages I haven't replied to
  - Check Slack
  - Unread mentions
  - Messages needing reply
  - slack-unanswered
  - unanswered messages
---

## Trigger Words
"Unanswered messages", "Messages I haven't replied to", "Check Slack", "Unread mentions"

# Slack Unanswered Messages Finder

This skill finds Slack messages that need your attention and helps you reply to them.

## Target Directory

All searches are performed in: `slack-sync/data/`

## Your Identifiers

> Replace the following with your own Slack display name and username.

Search for these names (case-insensitive):
- `@{YOUR_DISPLAY_NAME}`
- `@{YOUR_FULL_NAME}`
- `@{YOUR_SLACK_USERNAME}`
- Messages posted by: `{YOUR_FULL_NAME}`, `{YOUR_SLACK_USERNAME}`

Setup: Replace the placeholders above with your information, or specify via the `--users` option.

---

## Workflow

### Step 1: Find Unanswered Messages

Search for messages containing your identifiers:

```bash
grep -rn -B2 -A10 -E "@{YOUR_DISPLAY_NAME}|@{YOUR_SLACK_USERNAME}|{YOUR_FULL_NAME}" slack-sync/data/
```

### Step 2: Identify Unanswered Messages

A message is **unanswered** if:
1. It contains a mention of your name (or you posted it)
2. It ends with a question (`?`) or contains a request
3. There are NO lines starting with `> ####` immediately after it (before the next `###` or `---`)

Focus on recent messages (last 7 days). Exclude bot messages (Sentry, Vercel, etc.).

### Step 3: Present Findings

For each unanswered message, provide:
- Channel name
- Date/Time
- Sender
- Content summary
- Slack link
- Whether it needs a reply or is a follow-up

### Step 4: Generate Reply Draft

For messages that need replies, generate a draft reply in Japanese. Ask the user to review and edit.

### Step 5: Send Reply (with confirmation)

**IMPORTANT: Always get user confirmation before sending!**

The reply flow is:
1. Show the draft reply to the user
2. Ask: "Is it OK to send with this content? (Let me know if you have edits)"
3. Wait for user confirmation or edits
4. Only after explicit approval, use the reply script

---

## Replying to Messages

### Reply Script Location

```
data/slack-sync/scripts/reply_slack.py
```

### Usage

```bash
# Dry run (preview without sending)
python data/slack-sync/scripts/reply_slack.py \
  --url "https://xxx.slack.com/archives/CHANNEL/pTIMESTAMP" \
  --message "Reply content" \
  --dry-run

# Actually send (only after user confirms!)
python data/slack-sync/scripts/reply_slack.py \
  --url "https://xxx.slack.com/archives/CHANNEL/pTIMESTAMP" \
  --message "Reply content"
```

### Environment Variable Required

```
SLACK_USER_TOKEN=xoxp-...
```

This token needs the `chat:write` scope. See setup instructions below.

---

## Setup: Adding chat:write Scope

To enable reply functionality:

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Select your app (e.g., "Message Archiver")
3. Navigate to **OAuth & Permissions**
4. Under **User Token Scopes**, add:
   - `chat:write` - Post messages
5. Click **Reinstall to Workspace**
6. Copy the new `xoxp-...` token
7. Update `SLACK_USER_TOKEN` in your environment/GitHub Secrets

---

## Message Format Reference

Messages in markdown files:
- **Main message**: `### HH:MM - Sender Name [[Slack]](url)`
- **Reply**: Lines starting with `> ####`

---

## TODO File Management

### TODO File Location

```
slack-sync/TODO.md
```

### Workflow with TODO

1. **During search**: Add unanswered messages found to TODO.md
2. **When replying**: Change checkbox to `[x]`
3. **When done**: Move to "Completed messages" section

---

## Quick Commands

### Find mentions in recent files:
```bash
grep -rn -B2 -A10 "@{YOUR_DISPLAY_NAME}" slack-sync/data/ | head -200
```

### Find your posts:
```bash
grep -rn "### [0-9:]* - {YOUR_DISPLAY_NAME}" slack-sync/data/ | head -100
```

### Find questions to you:
```bash
grep -rn -A5 "@{YOUR_DISPLAY_NAME}" slack-sync/data/ | grep -E "\?$|please|could you|can you"
```

### View current TODO:
```bash
cat slack-sync/TODO.md
```

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
duration: "~25 min"
prerequisites: ["start-9-2"]
level: "intermediate"
tags: ["slack", "api", "message", "reply", "post"]
---

# 🎓 Lesson 9-3: Sending Replies

## 📍 What You'll Do

**Lesson 9-3: Slack API — Sending Messages and Retrieving User Info**!

| Item | Details |
|------|------|
| Goal | Send messages and thread replies with chat.postMessage, and retrieve user info with users.list / users.info |
| Duration | ~25 min |
| Skills used | curl, Slack Web API, AI text generation |
| Prerequisites | Lesson 9-2 completed (able to retrieve messages and threads) |
| Course page | [Module 9: Slack](https://ai-agent.camp/en/course/module-9) alongside this lesson |

**Session flow:**
1. Send a message to a channel with `chat.postMessage` (dry-run confirmation flow)
2. Send a thread reply by specifying `thread_ts`
3. Send a message with mentions
4. Retrieve user info with `users.list` / `users.info` (resolve user IDs for mentions)
5. Hands-on exercise: Summarize a thread and create/send a reply

By the end of this session, you'll be able to send messages and thread replies via the Slack API, and retrieve user information.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Set the token as an environment variable and go to Step 1)
(check_prereq → Run `auth.test` to verify the connection. Also check for the `chat:write` scope. If it fails, direct to Lesson 9-1)
(view_html → Show course page path)
(different_lesson → Display module list)

**What the AI runs automatically at session start:**
```bash
export SLACK_USER_TOKEN=$(uv run python tools/credential_manager.py get SLACK_USER_TOKEN)
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" "https://slack.com/api/auth.test" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Connection OK: {d[\"team\"]} / {d[\"user\"]} (user_id: {d[\"user_id\"]})')" 2>/dev/null || echo "Connection failed: Please complete Lesson 9-1 first"
```

---

## 🚀 Step 1: Send a Message with chat.postMessage (Dry-Run Confirmation Flow)

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Send a Message (with dry-run)",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selecting practice:**

**Important**: Sending a message is an irreversible action, so always include a dry-run (preview) step.

1. Check the destination channel:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=20" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    print(f'{ch[\"id\"]} : #{ch[\"name\"]}')"
```

2. **dry-run**: Confirm the message content with the user:
```text
The following message will be sent. Type "OK to send" if everything looks good.

Destination: #channel-name (CHANNEL_ID)
Message: Test post (learning Slack API)
```

3. Send after user confirmation:
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"Test post (learning Slack API)"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**Expected result:**
```json
{
    "ok": true,
    "channel": "C0XXXXXXX",
    "ts": "1713075000.123456",
    "message": {
        "text": "Test post (learning Slack API)",
        "user": "U0XXXXXXX",
        "ts": "1713075000.123456"
    }
}
```

**Required OAuth scope**: `chat:write`

---

## 🚀 Step 2: Send a Thread Reply Using thread_ts

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Send a Thread Reply",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selecting practice:**

1. Check the target thread (use the ts from the message posted in Step 1):
```bash
# Retrieve existing messages with threads
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=5" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for msg in data.get('messages', []):
    has_thread = '(has thread)' if msg.get('reply_count', 0) > 0 else ''
    print(f'ts={msg[\"ts\"]} {has_thread}: {msg.get(\"text\", \"\")[:60]}')"
```

2. **dry-run** → Send a thread reply after user confirmation:
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"Thread reply test","thread_ts":"PARENT_TS"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**Key points:**
- Specifying the parent message's `ts` in `thread_ts` makes it a thread reply
- Adding `reply_broadcast: true` also posts the thread reply to the channel (same as "Also send to channel")

---

## 🚀 Step 3: Send a Message with Mentions

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Send a Message with Mentions",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selecting practice:**

Mentions are embedded using the user ID in `<@USER_ID>` format:
```bash
# Get your own user ID
MY_USER_ID=$(curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/auth.test" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['user_id'])")
echo "My user ID: $MY_USER_ID"
```

```bash
# Send a message with a mention (to yourself — for testing)
# Execute after dry-run confirmation
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"channel\":\"CHANNEL_ID\",\"text\":\"<@${MY_USER_ID}> Mention test\"}" \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**Mention syntax reference:**
| Syntax | Target |
|------|------|
| `<@U0XXXXXXX>` | Specific user |
| `<!channel>` | Everyone in the channel |
| `<!here>` | All online members |
| `<!subteam^S0XXXXXXX>` | User group |

**Note**: Avoid using `<!channel>` or `<!here>` for testing purposes, as they send notifications to many people.

---

## 🚀 Step 4: Retrieve User Info with users.list / users.info

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Retrieve User Info",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selecting practice:**

1. Retrieve the workspace user list with `users.list`:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.list?limit=50" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for u in data.get('members', []):
    if u.get('deleted') or u.get('is_bot'):
        continue
    print(f'{u[\"id\"]} : {u.get(\"real_name\", \"Unknown\")} (@{u[\"name\"]}')"
```

2. Retrieve details for a specific user with `users.info`:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.info?user=U0XXXXXXX" \
  | python3 -c "
import sys, json
u = json.load(sys.stdin)['user']
print(f'Name: {u.get(\"real_name\", \"Unknown\")}')
print(f'Display name: {u.get(\"profile\", {}).get(\"display_name\", \"Not set\")}')
print(f'Email: {u.get(\"profile\", {}).get(\"email\", \"Not public\")}')
print(f'Status: {u.get(\"profile\", {}).get(\"status_text\", \"None\")}')
print(f'Timezone: {u.get(\"tz\", \"Unknown\")}')"
```

**Key fields:**
| Field | Description |
|-----------|------|
| `id` | User ID (used for mentions) |
| `name` | Username (the name after @) |
| `real_name` | Real name |
| `profile.display_name` | Display name |
| `profile.email` | Email address (requires `users:read.email` scope) |
| `tz` | Timezone |
| `is_bot` | Whether the user is a bot |

**Required OAuth scope**: `users:read`

---

## 🚀 Step 5: Hands-On Exercise — Summarize a Thread and Send as a Reply

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Hands-On Exercise — Thread Summary Reply",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selecting practice — execute the following workflow:**

This exercise combines the message retrieval learned in Lesson 9-2 with the sending covered in this lesson.

1. **Retrieve the thread**: Get the thread using `conversations.replies`
2. **Resolve user IDs**: Convert user IDs to names using `users.info`
3. **AI summary**: Have the AI summarize the thread content
4. **dry-run**: Display the summary text and get user confirmation
5. **Thread reply**: Send the summary as a reply using `chat.postMessage`

```bash
# 1. Retrieve the thread and save to a file
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.replies?channel=CHANNEL_ID&ts=THREAD_TS" \
  | python3 -c "
import sys, json, datetime
data = json.load(sys.stdin)
for msg in data.get('messages', []):
    ts = datetime.datetime.fromtimestamp(float(msg['ts']))
    print(f'[{ts.strftime(\"%m/%d %H:%M\")}] {msg.get(\"user\",\"?\")} : {msg.get(\"text\",\"\")}')" \
  > ~/ai-agent-camp/data/slack_thread_for_summary.txt
```

```text
# 2. Ask the AI to summarize
Read ~/ai-agent-camp/data/slack_thread_for_summary.txt and
summarize this thread in 3-5 lines.
Start the summary with "Thread summary:"
```

```bash
# 3. After dry-run confirmation, send the summary as a thread reply
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"Thread summary:\n(AI-generated summary text)","thread_ts":"THREAD_TS"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**Expected result**: The summary is posted as a reply in the thread.

---

## ⚠️ Common Issues and Solutions

**AskQuestion configuration:**
```json
{
  "title": "Select the issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "chat.postMessage returns not_authed / missing_scope"},
      {"id": "trouble_2", "label": "Message was sent but doesn't appear"},
      {"id": "trouble_3", "label": "Mentions don't work (displayed as plain text)"},
      {"id": "trouble_4", "label": "Japanese characters are garbled"}
    ]
  }]
}
```

### Issue 1: "not_authed / missing_scope"
**Cause**: The `chat:write` scope is not configured
**Solution**:
1. Open your app at https://api.slack.com/apps
2. Go to OAuth & Permissions → Add `chat:write` to User Token Scopes
3. Reinstall to the workspace
4. Save the new token using `credential_manager.py store SLACK_USER_TOKEN`

### Issue 2: "Message was sent but doesn't appear"
**Cause**: The message was sent to a different channel, or was posted inside a thread
**Solution**:
```bash
# Check the channel and ts in the response
# Verify the channel matches what you expected
# Check whether thread_ts is included (unintentional thread reply)
```

### Issue 3: "Mentions displayed as plain text"
**Cause**: Written as `@username` in text form
**Solution**: Mentions must use the `<@U0XXXXXXX>` format with the user ID. Writing `@name` will not create a mention.
```bash
# Look up user IDs
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.list?limit=100" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for u in data.get('members', []):
    if not u.get('deleted') and not u.get('is_bot'):
        print(f'<@{u[\"id\"]}> → {u.get(\"real_name\", u[\"name\"])}')"
```

### Issue 4: "Japanese characters are garbled"
**Cause**: JSON encoding issue
**Solution**: Set `Content-Type: application/json; charset=utf-8` and send via a JSON body. When using `application/x-www-form-urlencoded`, Japanese characters must be URL-encoded.

---

## ✅ Checkpoint
- [ ] Sent a message to a channel with `chat.postMessage`
- [ ] Sent a thread reply using `thread_ts`
- [ ] Sent a message with mentions
- [ ] Retrieved user info with `users.list` / `users.info`
- [ ] Created a thread summary and sent it as a reply

---

## 📋 Deliverable Preview

The deliverables for this lesson are terminal output and posts on Slack.

### Expected Output
```text
# chat.postMessage result
ok: true
channel: C0XXXXXXX
ts: 1713075000.123456

# users.list result
U0ABC1234 : Taro Yamada (@taro.yamada)
U0DEF5678 : Hanako Sato (@hanako.sato)
U0GHI9012 : Ichiro Tanaka (@ichiro.tanaka)

# What appears on Slack
"Test post (learning Slack API)" is posted to #general
The summary is posted as a reply in the thread
```

---

## ➡️ Next Steps

You have now completed all the basic Slack API operations (channel retrieval, message retrieval, message sending, and user info retrieval). Let's move on to the next module.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-10-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-10-1
- finish → End

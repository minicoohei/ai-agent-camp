---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "About 30 min"
prerequisites: ["start-17-4"]
level: "intermediate"
tags: ["marketing", "typefully", "x", "threads", "sns", "api"]
---

# 🎓 Lesson 17-5: Automate X/Threads Posting with Typefully

## 📍 What You'll Do in This Session

Welcome to **Lesson 17-5: Automate X/Threads Posting with Typefully**!

| Item | Details |
|------|---------|
| Goal | Automate posting to X (Twitter) and Threads using the Typefully API v2 |
| Duration | About 30 min |
| Skills Used | Typefully API v2 (social set retrieval, draft creation, scheduling, thread posting) |
| Prerequisites | Typefully account created, API key obtained |
| Course Page | Refer to [Module 17: Marketing](https://ai-agent.camp/en/course/module-17) in parallel |

> **💡 Tool Info**: This lesson uses the Typefully API v2. It works with Cursor IDE and Claude Code (CLI/Desktop). In some environments like Codex CLI, you may see a `request_user_input is not supported` error. If so, refer to the "Alternative Workflow" section.

> **⚠️ API Version**: As of 2025, Typefully API has migrated to v2. The v1 `x-api-key` header and `/v1/drafts/` endpoint are deprecated. This lesson uses v2 (`Authorization: Bearer` header + `/v2/social-sets/{id}/drafts` endpoint).

**Session Flow:**
1. Understand the Typefully API overview and set up account/API key/social_set_id
2. Create drafts and configure scheduled posting
3. Try simultaneous posting to X (Twitter) and Threads
4. Automate thread-style sequential posting
5. Verify results and save records to output/typefully/

By the end of this session, you'll be able to create drafts, schedule posts, and automate thread posting via the Typefully API v2.

> **💡 Hint**: If the AI response stops midway, type "continue" or "please go on" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first confirm everything is set up.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session Check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's go"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Check prerequisites)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Typefully API v2 Overview and Account Setup

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Typefully API v2 Overview and Account Setup",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please explain the Typefully API v2 overview. Cover the following:

1. What is Typefully — a post management and scheduling tool for X (Twitter) / Threads
2. What the API v2 can do — social set retrieval, draft creation, scheduling, thread posting, platform-specific posts
3. Account setup steps:
   a. Create an account at https://typefully.com
   b. Connect your X (Twitter) account
   c. Connect your Threads account (if supported)
4. Getting the API key:
   a. Go to Typefully Settings → Integrations → API & Integrations
   b. Generate and copy the API Key
5. Set the API key as an environment variable:
   export TYPEFULLY_API_KEY="your-api-key-here"
6. Retrieve the social_set_id (required for v2):

curl -X GET "https://api.typefully.com/v2/social-sets" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY"

   Copy the id of the social set you want to use from the response:
   export TYPEFULLY_SOCIAL_SET_ID="the-id-you-got"
```

**Expected result**: You understand the Typefully overview and have completed API key and social_set_id setup.

---

## 🚀 Step 2: Creating Drafts and Scheduling

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Creating Drafts and Scheduling",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Use the Typefully API v2 to create a draft and set up a scheduled post.

Steps:
1. mkdir -p output/typefully
2. Create a draft with the following curl command (v2 endpoint):

curl -X POST "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/drafts" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "x": {
        "enabled": true,
        "posts": [
          {"text": "AI agents are dramatically changing work efficiency!\n\nPractical techniques anyone can use — no engineering background needed.\n\n#AIAgent #Productivity"}
        ]
      }
    },
    "publish_at": "next-free-slot"
  }'

3. Record the draft ID from the response
4. Verify scheduling options (publish_at: "next-free-slot" / ISO8601 datetime)
5. Save the result to output/typefully/draft-result.json
```

**Expected result**: A draft is created in Typefully with scheduling configured.

---

## 🚀 Step 3: Simultaneous Posting to X (Twitter) and Threads

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Simultaneous Posting to X and Threads",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Create a draft using the Typefully API v2 that posts to both X (Twitter) and Threads simultaneously.

Steps:
1. Enable both platforms.x and platforms.threads to specify posting destinations:

curl -X POST "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/drafts" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "x": {
        "enabled": true,
        "posts": [
          {"text": "Automated posting test from Typefully API v2!\n\nSimultaneously distributing to X and Threads.\n\n#AutoPost #TypefullyAPI"}
        ]
      },
      "threads": {
        "enabled": true,
        "posts": [
          {"text": "Automated posting test from Typefully API v2!\n\nSimultaneously distributing to X and Threads.\n\n#AutoPost #TypefullyAPI"}
        ]
      }
    },
    "publish_at": "next-free-slot"
  }'

2. Verify the posting destinations (X / Threads) in the Typefully dashboard
3. Save results to output/typefully/multi-post-result.json
4. Check character limits and format differences between platforms (X: 280 chars, Threads: 500 chars)
```

**Expected result**: A draft for simultaneous posting to X and Threads is created.

---

## 🚀 Step 4: Automating Thread-Style Sequential Posts

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Automating Thread-Style Sequential Posts",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Create a thread-style sequential post using the Typefully API v2.

Steps:
1. In v2, threads are formed by placing multiple entries in the posts array (the v1 threadify + four-newline separator approach is deprecated):

curl -X POST "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/drafts" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "x": {
        "enabled": true,
        "posts": [
          {"text": "[AI Agent Guide 1/3]\n\nAn AI agent is an AI that autonomously executes tasks based on instructions."},
          {"text": "[2/3]\n\nPractical use cases:\n- Automated email replies\n- Schedule management\n- Data analysis report generation"},
          {"text": "[3/3]\n\nGetting started is easy!\nTry automating one task first.\n\nLearn more at the link in bio 👇"}
        ]
      }
    },
    "publish_at": "next-free-slot"
  }'

2. Verify the thread is split in order based on the posts array
3. Save results to output/typefully/thread-result.json
```

**Expected result**: A thread consisting of 3 tweets is created as a draft.

---

## 🚀 Step 5: Verifying Results and Record Keeping

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Verifying Results and Record Keeping",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review examples only"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Verify the posting results so far and create a summary.

Steps:
1. Check the list of created drafts in the Typefully dashboard
2. Verify the status of each draft (Draft / Scheduled / Posted)
3. Create a summary in output/typefully/summary.md covering:
   - Number of drafts created
   - Scheduling details (publish_at)
   - Posting destinations (platforms.x / platforms.threads)
   - Thread post structure (number of elements in posts array)
4. Suggest 3 improvement points for future automation
```

**Expected result**: A posting results summary is saved in output/typefully/.

---

## ⚠️ Common Troubleshooting

AskUserQuestion (AskQuestion) lets you select the issue for guidance.

**AskQuestion configuration:**
```json
{
  "title": "Select Your Issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "API key authentication error"},
      {"id": "trouble_2", "label": "Don't know social_set_id"},
      {"id": "trouble_3", "label": "Draft creation error"},
      {"id": "trouble_4", "label": "Thread not splitting correctly"},
      {"id": "trouble_5", "label": "Threads posts not appearing"}
    ]
  }]
}
```


### Trouble 1: "API key authentication error"
**Cause**: Invalid API key, or v2 requires the `Authorization: Bearer` header (the v1 `x-api-key` is deprecated)
**Solution prompt**:
```
Verify the TYPEFULLY_API_KEY environment variable is set correctly.
Run [[ -n "$TYPEFULLY_API_KEY" ]] && echo "set" || echo "not set" to check existence,
and verify the key is valid in Typefully Settings → API & Integrations.
For v2, always use the "Authorization: Bearer $TYPEFULLY_API_KEY" format.
```

### Trouble 2: "Don't know social_set_id"
**Cause**: v2 endpoints require social_set_id in the URL path
**Solution prompt**:
```
Retrieve the list of available social sets with:

curl -X GET "https://api.typefully.com/v2/social-sets" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY"

Copy the id of the social set you want from the response and set
export TYPEFULLY_SOCIAL_SET_ID="the-id-you-got" as an environment variable.
```

### Trouble 3: "Draft creation error"
**Cause**: Invalid JSON format in request body, or missing v2 required fields (platforms)
**Solution prompt**:
```
Check the JSON body in your curl command.
In v2, platforms.{x|threads}.{enabled, posts} is required.
The posts field must be an array, and each element needs a text field.
Verify the Content-Type: application/json header is included.
Use jq to format the response for easier debugging.
```

### Trouble 4: "Thread not splitting correctly"
**Cause**: In v2 threads are split via the posts array (the v1 four-newline separator / threadify are deprecated)
**Solution prompt**:
```
In v2, threads are determined by the number of elements in the posts array.
Arrange them like {"posts": [{"text": "first"}, {"text": "second"}]}.
The v1 threadify parameter and four-newline separator (\n\n\n\n) do not work in v2.
```

### Trouble 5: "Threads posts not appearing"
**Cause**: Threads account not connected to Typefully, or platforms.threads.enabled is false
**Solution prompt**:
```
Check if your Threads account is connected in
Typefully Settings → Accounts.
Verify that platforms.threads.enabled: true is set in the request body
and that platforms.threads.posts contains at least one post.
Also check Typefully's latest documentation for Threads API support status.
```

---

## ✅ Checkpoint
- [ ] Understood the Typefully API v2 overview and configured the API key and social_set_id
- [ ] Created a draft and set up scheduled posting
- [ ] Tried simultaneous posting to X (Twitter) and Threads
- [ ] Automated thread-style sequential posting (posts array)
- [ ] Posting results saved in output/typefully/


---

## 📋 Deliverables Preview

### Expected Output
```
📁 output/typefully/
├── draft-result.json          ← Single draft creation result
├── multi-post-result.json     ← X/Threads simultaneous posting result
├── thread-result.json         ← Thread posting result
└── summary.md                 ← Posting results summary
```
> Format: JSON / Markdown

### Verification Commands
```bash
# Check output files
ls -lh output/typefully/

# Check draft result
cat output/typefully/draft-result.json | jq .

# Check summary
cat output/typefully/summary.md
```

> 💡 **Claude Code**: `Read output/typefully/summary.md` for in-chat preview
> 💡 **Cursor**: Click the file in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor's chat to check completion status:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## ➡️ Next Steps

You've completed all lessons in Module 17: Marketing!

AskUserQuestion (AskQuestion) lets you choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose your next action",
    "options": [
      {"id": "next_module", "label": "Start next module (/start-18-1)"},
      {"id": "review_module", "label": "Review Module 17"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_module → /start-18-1 to go to the Requirements/System Development module
- review_module → Review each lesson in Module 17
- finish → End session

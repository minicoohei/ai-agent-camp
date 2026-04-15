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
| Goal | Automate posting to X (Twitter) and Threads using the Typefully API |
| Duration | About 30 min |
| Skills Used | Typefully API (draft creation, scheduling, thread posting) |
| Prerequisites | Typefully account created, API key obtained |
| Course Page | Refer to [Module 17: Marketing](https://ai-agent.camp/en/course/module-17) in parallel |

> **💡 Tool Info**: This lesson uses the Typefully API. It works with Cursor IDE and Claude Code (CLI/Desktop). In some environments like Codex CLI, you may see a `request_user_input is not supported` error. If so, refer to the "Alternative Workflow" section.

**Session Flow:**
1. Understand the Typefully API overview and set up account/API key
2. Create drafts and configure scheduled posting
3. Try simultaneous posting to X (Twitter) and Threads
4. Automate thread-style sequential posting
5. Verify results and save records to output/typefully/

By the end of this session, you'll be able to create drafts, schedule posts, and automate thread posting via the Typefully API.

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

## 🚀 Step 1: Typefully API Overview and Account Setup

AskUserQuestion (AskQuestion) lets you choose "Proceed / Review examples / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Typefully API Overview and Account Setup",
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
Please explain the Typefully API overview. Cover the following:

1. What is Typefully — a post management and scheduling tool for X (Twitter) / Threads
2. What the API can do — draft creation, scheduling, thread posting
3. Account setup steps:
   a. Create an account at https://typefully.com
   b. Connect your X (Twitter) account
   c. Connect your Threads account (if supported)
4. Getting the API key:
   a. Go to Typefully Settings → Integrations → API & Integrations
   b. Generate and copy the API Key
5. Set the API key as an environment variable:
   export TYPEFULLY_API_KEY="your-api-key-here"
```

**Expected result**: You understand the Typefully overview and have completed API key setup.

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
Use the Typefully API to create a draft and set up a scheduled post.

Steps:
1. mkdir -p output/typefully
2. Create a draft with the following curl command:

curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI agents are dramatically changing work efficiency!\n\nPractical techniques anyone can use — no engineering background needed.\n\n#AIAgent #Productivity",
    "schedule-date": "next-free-slot"
  }'

3. Record the draft ID from the response
4. Verify scheduling options (next-free-slot / specific datetime)
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
Create a draft using the Typefully API that posts to both X (Twitter) and Threads simultaneously.

Steps:
1. Specify the posting destinations with the share parameter:

curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Automated posting test from Typefully API!\n\nSimultaneously distributing to X and Threads.\n\n#AutoPost #TypefullyAPI",
    "schedule-date": "next-free-slot",
    "share": true
  }'

2. Verify the posting destinations (X / Threads) in the Typefully dashboard
3. Save results to output/typefully/multi-post-result.json
4. Check character limits and format differences between platforms
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
Create a thread-style sequential post using the Typefully API.

Steps:
1. Use four newlines (\n\n\n\n) as the thread separator in the content field:

curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "[AI Agent Guide 1/3]\n\nAn AI agent is an AI that autonomously executes tasks based on instructions.\n\n\n\n[2/3]\n\nPractical use cases:\n- Automated email replies\n- Schedule management\n- Data analysis report generation\n\n\n\n[3/3]\n\nGetting started is easy!\nTry automating one task first.\n\nLearn more at the link in bio 👇",
    "schedule-date": "next-free-slot",
    "threadify": true
  }'

2. Verify the thread is correctly split into individual tweets
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
   - Scheduling details
   - Posting destinations (X / Threads)
   - Thread post structure
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
      {"id": "trouble_2", "label": "Draft creation error"},
      {"id": "trouble_3", "label": "Thread not splitting correctly"},
      {"id": "trouble_4", "label": "Threads posts not appearing"}
    ]
  }]
}
```


### Trouble 1: "API key authentication error"
**Cause**: Invalid API key or environment variable not set correctly
**Solution prompt**:
```
Verify the TYPEFULLY_API_KEY environment variable is set correctly.
Run echo $TYPEFULLY_API_KEY to check the value,
and verify the key is valid in Typefully Settings → API & Integrations.
```

### Trouble 2: "Draft creation error"
**Cause**: Invalid JSON format in request body or missing required fields
**Solution prompt**:
```
Check the JSON body in your curl command.
The content field is required.
Verify the Content-Type: application/json header is included.
Use jq to format the response for easier debugging.
```

### Trouble 3: "Thread not splitting correctly"
**Cause**: Thread separator (four newlines) not correct
**Solution prompt**:
```
Thread separators use \n\n\n\n (four newlines).
Verify the newlines are correct in the content field.
Also check that the threadify parameter is set to true.
```

### Trouble 4: "Threads posts not appearing"
**Cause**: Threads account not connected to Typefully
**Solution prompt**:
```
Check if your Threads account is connected in
Typefully Settings → Accounts.
Also check Typefully's latest documentation for Threads API support status.
```

---

## ✅ Checkpoint
- [ ] Understood the Typefully API overview and configured the API key
- [ ] Created a draft and set up scheduled posting
- [ ] Tried simultaneous posting to X (Twitter) and Threads
- [ ] Automated thread-style sequential posting
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

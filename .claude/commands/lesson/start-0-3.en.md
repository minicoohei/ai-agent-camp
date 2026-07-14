---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "~10 min"
prerequisites: ["start-0-1", "start-0-2"]
level: "beginner"
tags: ["setup", "gemini", "api"]
nonInteractiveMode: deferred
---
# Lesson 0-3: Gemini API Setup

## Check Setup Progress

**Auto-run by AI:** Run `uv run python tools/setup_progress.py show` to display the current setup progress.

---

## What You'll Do

| Item | Details |
|------|---------|
| Goal | Obtain a Gemini API key from Google AI Studio and configure it in .env so you can use AI features like image generation |
| Duration | ~10 min |
| Prerequisites | Lesson 0-1 and Lesson 0-2 completed; able to log in to a Google account via browser |
| Course Page | Refer to [Course Materials Top](https://ai-agent.camp/en/course/module-0) in parallel |

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

---

## Gemini API Auto-Setup

In this lesson, just run `/setup-gemini` and you're done.
**No terminal operations required. The AI handles everything automatically.**

### What the AI Does Automatically

1. Auto-launch Google AI Studio in the browser (AI runs `open` / `start` depending on your OS)
2. Guide you step by step through the API key acquisition process in the browser
3. Auto-create the `.env` file (copy from `.env.example` + verify `.gitignore`)
4. You enter the API key directly in the `.env` file (edit in the Cursor editor)
5. Auto-run a test request to the Gemini API to verify it works

**Important**: Do not paste the API key in the chat. This process uses direct entry in the `.env` file.

**AskQuestion settings:**
```json
{
  "title": "Gemini API Setup",
  "questions": [{
    "id": "action",
    "prompt": "Would you like to start the Gemini API setup?",
    "options": [
      {"id": "run", "label": "Start setup (run /setup-gemini)"},
      {"id": "already_done", "label": "Gemini API already configured"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(run -> Run the contents of `/setup-gemini`)
(already_done -> Go to checkpoint)
(view_html -> Provide the course page URL)
(different_lesson -> Show module list)

---

## Commands to Run

```text
/setup-gemini
```

## Expected Output Example

```text
Gemini API Test Result:
API response: Hello! How can I help you?
```

> **Note**: The response text varies by model. If no error occurs, the connection was successful.

## Common Troubleshooting
- Browser doesn't open -> Ask the AI to "open Google AI Studio"
- API test fails -> Check the key in .env and re-run `/setup-gemini`

---

## Checkpoint
- [ ] Obtained an API key from Google AI Studio
- [ ] GEMINI_API_KEY is set in .env
- [ ] .env file is excluded by .gitignore
- [ ] API test succeeded (received a response from Gemini API)

---

## Next Steps

**AskQuestion settings:**
```json
{
  "title": "Choose Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "What would you like to do next?",
    "options": [
      {"id": "next", "label": "Set up Slack API (/start-0-4)"},
      {"id": "try_banner", "label": "Try creating a banner right away (/start-1-1)"},
      {"id": "check", "label": "Run environment check (/check-setup)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(next -> Guide to /start-0-4)
(try_banner -> Guide to /start-1-1)
(check -> Run the contents of /check-setup)
(finish -> End)

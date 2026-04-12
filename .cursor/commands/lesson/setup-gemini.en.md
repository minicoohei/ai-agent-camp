---
description: "Gemini API Setup (Complete Guide)"
duration: "~10 min"
prerequisites: ["Have a Google account", "Browser available"]
level: "beginner"
tags: ["setup", "gemini", "api"]
---

# Gemini API Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-gemini` to display progress
2. Auto-detect existing API key:
   - Run `uv run python tools/credential_manager.py status`
   - If GEMINI_API_KEY is already set, you can just run Step 3 (API test) and mark it as complete
   - If a plaintext key exists in `.env`, suggest migrating it to the credential store

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Get a Gemini API key from Google AI Studio and save it to the Credential Store so you can use AI features like image generation |
| Duration | ~10 minutes |
| Prerequisites | Have a Google account and a browser available |
| Skill Level | No CLI commands needed (everything is auto-run by AI + GUI operations only) |

**Session flow:**
1. Open Google AI Studio in the browser (AI opens the browser automatically)
2. Get your API key (just click buttons on screen)
3. Save the API key securely (AI creates the file automatically)
4. Enter the API key (open the file and paste)
5. Functionality test (AI runs automatically)

> **Hint**: If the AI's response stops midway, type "please continue" or "it stopped" to resume.

---

## Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "chrome", "label": "Automate browser operations with /chrome"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(chrome -> After opening the browser in Step 1, follow the "Automating with Chrome integration" section for automatic execution)
(check_prereq -> Guide: "You're ready if you can log in to a browser with a Google account.")
(different_lesson -> Display module list)

---

## Step 1: Open Google AI Studio in the Browser

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to open the browser automatically:

```bash
# Mac:
open https://aistudio.google.com/apikey
# Windows:
start https://aistudio.google.com/apikey
# Linux:
xdg-open https://aistudio.google.com/apikey
```

**After the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Get your API key in the browser",
  "questions": [{
    "id": "browser_status",
    "prompt": "Did the browser open? Follow these steps to get your API key:\n\n1. Log in with your Google account\n2. Click the 'Get API key' button\n3. Click 'Create API key'\n4. Click the 'Copy' button next to the displayed API key\n\nDid you copy the API key?",
    "options": [
      {"id": "copied", "label": "I copied the API key!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "no_button", "label": "I can't find the 'Get API key' button"},
      {"id": "login_issue", "label": "I can't log in to my Google account"}
    ]
  }]
}
```

(copied -> Proceed to Step 2)
(browser_not_open -> Guide: "Open this URL directly in your browser: https://aistudio.google.com/apikey")
(no_button -> Guide: "Wait for the page to fully load. If it still doesn't appear, click the 'Get API key' tab at the top of the page.")
(login_issue -> Guide: "Google AI Studio requires a gmail.com or Google Workspace account. Try logging in with your company account.")

---

## Automating with Chrome Integration (`/chrome` mode)

**Prerequisite:** The "Claude in Chrome" extension (v1.0.36+) must be installed in Chrome, and you must have launched with `claude --chrome` or run `/chrome` in the session.

**What the AI auto-runs with Chrome integration:**
1. Open https://aistudio.google.com/apikey in the browser
2. Use Chrome integration to perform the following operations in order:
   - If Google account login is needed, wait for user's action
   - Click the "Get API key" or "Get API key" button
   - Click the "Create API key" or "Create API key" button
   - If a project selection screen appears, select the default project and click "Create API key in existing project"
3. Once the API key appears on screen, tell the user "Click the copy button to copy the API key"
4. Proceed to Step 2

**Note:** Do not read the API key value from the browser screen. The user copies it manually.

If Chrome integration is not available, follow the Step 1 instructions manually.

---

## Step 2: Save the API Key Securely

**Important security note:**
Do not paste the API key in this chat. We'll save it securely in a separate terminal window.

**What the AI auto-runs:**
1. Check if the `keyring` package is installed
   - If not installed: auto-run `pip install keyring`
2. Run `uv run python tools/credential_manager.py status` to check the current state

**Message to display to the user:**

```text
Once you've copied the API key, follow these steps to save it securely:

┌─────────────────────────────────────────────────────────────┐
│ Run the following command in a separate terminal window:     │
│                                                             │
│ Cursor: Ctrl+` (backtick) to open a new terminal           │
│ Claude Code: Open a separate terminal window                │
│                                                             │
│ uv run python tools/credential_manager.py store GEMINI_API_KEY     │
│                                                             │
│ → "Enter value for GEMINI_API_KEY:" will be displayed       │
│ → Paste the copied API key and press Enter                  │
│   (The characters you type won't be shown on screen.        │
│    This is normal.)                                         │
│ → "Stored GEMINI_API_KEY" means it was saved successfully   │
└─────────────────────────────────────────────────────────────┘

Once saved, come back to this chat and let me know "done".
```

**Why run in a separate window:**
If you handle API keys in the AI chat, the values will remain in the conversation log.
By running `credential_manager.py` in a separate window, the key values are stored directly
in the OS's encrypted storage (macOS Keychain / Windows Credential Locker / Linux SecretService),
and never stored in plaintext files or chat logs.

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Save the API key",
  "questions": [{
    "id": "store_status",
    "prompt": "Did you run the command in a separate terminal?",
    "options": [
      {"id": "done", "label": "Saved!"},
      {"id": "terminal_help", "label": "I don't know how to open a terminal"},
      {"id": "command_error", "label": "I got an error with the command"},
      {"id": "security_question", "label": "I have a question about security"}
    ]
  }]
}
```

(done -> Proceed to Step 3)
(terminal_help -> Guide: "For Cursor: Menu at the top > Terminal > New Terminal, or press Ctrl+` (Cmd+` on Mac). For Claude Code: Open a separate terminal window/tab. Mac: Cmd+T (new tab) or Cmd+N (new window). Windows: Open PowerShell or Windows Terminal from the Start menu, or press Ctrl+Shift+T for a new tab. Then cd to the project directory.")
(command_error -> AI runs `uv run python tools/credential_manager.py status` to check the situation and identify the cause. If keyring is not installed, auto-run `pip install keyring`)
(security_question -> Explain: "This tool uses the OS's standard encrypted storage. On macOS it uses Keychain, on Windows it uses Credential Locker, and on Linux it uses SecretService (GNOME Keyring, etc.). No plaintext files (.env) are created. The storage is also locked when the screen is locked, providing protection from physical access.")

---

## Step 3: Setup Test

**What the AI auto-runs:**

1. First, run `credential_manager.py status` to check if `GEMINI_API_KEY` is saved in the Credential Store:
   - **Note**: Do not display the API key value itself in the chat. Only show masked output like "API key is set (first 4 characters: AIza...)"
   - Status check command: `uv run python tools/credential_manager.py status`

2. If the basic check passes, send a test request to the Gemini API:
   - Inject environment variables from the Credential Store and make the API call
   - Test code example:
     ```python
     import os
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     from dotenv import load_dotenv
     load_dotenv()
     from google import genai
     client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
     response = client.models.generate_content(
         model="gemini-2.5-flash",
         contents="Hello! Please give a one-line greeting."
     )
     print("API response:", response.text)
     ```
   - Auto-install required packages (`google-genai`, `keyring`) if not installed

3. Display an AskQuestion based on the test result:

**On success:**
```text
Gemini API setup is complete!

Test result: Successfully received a response from the API.
You can now use AI features like image generation (/banner), diagram creation (/diagram), and more.
```

**On failure — AskQuestion:**
```json
{
  "title": "Test Result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the API test. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Run the test again"},
      {"id": "recheck_key", "label": "Recheck the API key (go back to Step 1)"},
      {"id": "show_error", "label": "I want to see the error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(recheck_key -> Go back to Step 1)
(show_error -> Display the error message and guide on the cause and solution)
(skip_test -> Guide: "The API test was skipped. You can check later with /check-setup.")

---

## Common Troubles and Solutions

**AskQuestion configuration:**
```json
{
  "title": "Select the trouble type",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the one that applies to you",
    "options": [
      {"id": "trouble_invalid", "label": "I get an 'Invalid API key' error"},
      {"id": "trouble_quota", "label": "I get a 'Quota exceeded' error"},
      {"id": "trouble_package", "label": "I get a Python package error"},
      {"id": "trouble_cost", "label": "I'm worried about costs"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Trouble 1: "Invalid API key" Error
**Cause**: API key was not copied correctly, or the key is invalid
**What the AI does**:
1. Check `GEMINI_API_KEY` save status with `credential_manager.py status` (only show masked value)
2. If not saved in Credential Store, guide to re-register
3. If saved, re-run the API test. If it fails, guide: "Please recreate the key in Google AI Studio."

### Trouble 2: "Quota exceeded" Error
**Cause**: Free tier limit reached
**AI guidance**: "The Gemini API free tier allows 15 requests per minute and 1,500 requests per day. Wait a few minutes and try again. The free tier is more than enough for training usage."

### Trouble 3: Python Package Error
**Cause**: Required packages are not installed
**What the AI does**: Auto-install missing packages (`pip install google-genai python-dotenv`)

### Trouble 4: Cost Concerns
**AI guidance**: "The Gemini API has a free tier. There is no cost within the free tier limits. For training-level usage (a few dozen generations per day), the free tier is more than sufficient. Google will notify you before any charges would apply."

### Trouble 5: Other Errors
**What the AI does**: Check the error message content, identify the cause, and guide the user to a solution

---

## Checkpoint
- [ ] Got an API key from Google AI Studio
- [ ] Saved to the Credential Store with credential_manager.py store
- [ ] Confirmed the save with credential_manager.py status
- [ ] API test succeeded (received a response from the Gemini API)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Gemini API setup is complete! What would you like to do next?",
    "options": [
      {"id": "setup_slack", "label": "Also set up Slack API (/setup-slack)"},
      {"id": "try_banner", "label": "Try creating a banner right away (/start-1-1)"},
      {"id": "try_diagram", "label": "Try creating a diagram (/start-2-1)"},
      {"id": "back_to_setup", "label": "Go back to the setup list (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- setup_slack -> Guide to /setup-slack
- try_banner -> Guide to /start-1-1
- try_diagram -> Guide to /start-2-1
- back_to_setup -> Guide to /start-0-1
- finish -> End

---

## Completion

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-gemini` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "Next, set up the Slack API with `/setup-slack` (can be skipped)"

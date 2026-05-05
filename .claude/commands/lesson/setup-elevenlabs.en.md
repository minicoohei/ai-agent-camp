---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Browser available", "Have an email or Google/GitHub account"]
level: "beginner"
tags: ["setup", "elevenlabs", "api", "tts", "voice"]
nonInteractiveMode: incompatible
---
# ElevenLabs API Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-elevenlabs` to display progress
2. Auto-detect existing API key:
   - Run `uv run python tools/credential_manager.py status`
   - If ELEVENLABS_API_KEY (or ELEVEN_API_KEY) is already set, you can just run Step 4 (API test) and mark it as complete
   - If a plaintext key exists in `.env`, suggest migrating it to the credential store

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Get an API key from ElevenLabs and save it to the Credential Store so you can use text-to-speech (TTS) and voice synthesis features |
| Duration | ~10 minutes |
| Prerequisites | An email address or Google/GitHub account, and a browser available |
| Skill Level | No CLI commands needed (everything is auto-run by AI + GUI operations only) |

**Use cases:**
ElevenLabs is an AI voice synthesis (TTS) service. It supports text-to-speech, voice cloning, and multilingual voice synthesis, used for generating video narration and more.

**About costs:**
The free plan allows up to 10,000 characters per month. This is more than enough for training-level usage.

**Session flow:**
1. Open ElevenLabs in the browser (AI opens the browser automatically)
2. Create an account / log in (sign up via Google/GitHub authentication)
3. Get your API key (just copy it from the settings page)
4. Save to the Credential Store (run a command in a separate terminal)
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
(check_prereq -> Guide: "You're good to go if you have an email address or a Google/GitHub account. The free plan allows up to 10,000 characters per month.")
(different_lesson -> Display module list)

---

## Step 1: Open ElevenLabs in the Browser

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to open the browser automatically:

```bash
# Mac:
open https://elevenlabs.io
# Windows:
start https://elevenlabs.io
# Linux:
xdg-open https://elevenlabs.io
```

**After the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Sign up / Log in to ElevenLabs",
  "questions": [{
    "id": "signup_status",
    "prompt": "Did the browser open? Follow these steps to create your account:\n\n1. Click 'Sign up' in the top right (or 'Log in' if you already have an account)\n2. Sign up with Google / GitHub authentication, or with your email address\n3. Once logged in, proceed to the next step\n\nAre you logged in?",
    "options": [
      {"id": "logged_in", "label": "I'm logged in!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "signup_issue", "label": "I'm having trouble signing up"},
      {"id": "already_have_key", "label": "I already have an API key"}
    ]
  }]
}
```

(logged_in -> Proceed to Step 2)
(browser_not_open -> Guide: "Open this URL directly in your browser: https://elevenlabs.io")
(signup_issue -> Guide: "Google authentication is the easiest. Click Sign up in the top right -> Continue with Google. If that doesn't work, try signing up with your email address.")
(already_have_key -> Skip to Step 3)

---

## Automating with Chrome Integration (`/chrome` mode)

**Prerequisite:** The "Claude in Chrome" extension (v1.0.36+) must be installed in Chrome, and you must have launched with `claude --chrome` or run `/chrome` in the session.

**What the AI auto-runs with Chrome integration:**
1. Open https://elevenlabs.io in the browser
2. Use Chrome integration to perform the following operations in order:
   - Click "Sign up" or "Log in"
   - Authenticate with Google, GitHub, or email (wait for user's action)
   - After login, navigate to https://elevenlabs.io/app/settings/api-keys
   - If there's an existing key, leave it as is; otherwise click "Create API Key"
3. Once the API key is displayed, tell the user "Click the copy button next to the API key to copy it"
4. Proceed to Step 3

**Note:** Do not read the API key value from the browser screen. The user copies it manually.

If Chrome integration is not available, follow the steps below manually.

---

## Step 2: Get Your API Key

**What the AI does:**
1. Open the API key page in the browser:

```bash
# Mac:
open https://elevenlabs.io/app/settings/api-keys
# Windows:
start https://elevenlabs.io/app/settings/api-keys
# Linux:
xdg-open https://elevenlabs.io/app/settings/api-keys
```

**After the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 2: Get your API key",
  "questions": [{
    "id": "key_status",
    "prompt": "Did the API key settings page open? Follow these steps to get your API key:\n\n1. Confirm the API Keys page is displayed\n2. If there's an existing key, click the copy icon\n3. If not, click 'Create API Key' to create a new one\n4. Copy the displayed API key\n\nDid you copy the API key?",
    "options": [
      {"id": "copied", "label": "I copied the API key!"},
      {"id": "page_not_found", "label": "I can't find the settings page"},
      {"id": "no_create_button", "label": "I can't find the 'Create API Key' button"},
      {"id": "need_help", "label": "I need other help"}
    ]
  }]
}
```

(copied -> Proceed to Step 3)
(page_not_found -> Guide: "After logging in, click the profile icon in the bottom left -> Profile + API key. Or open this URL directly: https://elevenlabs.io/app/settings/api-keys")
(no_create_button -> Guide: "Wait for the page to fully load. If existing keys are displayed in the API Keys section, click the copy icon next to the key.")
(need_help -> Gather error details and assist individually)

---

## Step 3: Save the API Key Securely

**Important security note:**
Do not paste the API key in this chat. We'll save it securely in a separate terminal window.

**What the AI auto-runs:**
1. Check if the `keyring` package is installed
   - If not installed: auto-run `uv add keyring`
2. Run `uv run python tools/credential_manager.py status` to check the current state

**Message to display to the user:**

```text
Once you've copied the API key, follow these steps to save it securely:

┌──────────────────────────────────────────────────────────────────┐
│ Run the following commands in a separate terminal window:        │
│                                                                  │
│ Cursor: Ctrl+` (backtick) to open a new terminal                │
│ Claude Code: Open a separate terminal window                     │
│                                                                  │
│ (1) Save with the main key name:                                 │
│ uv run python tools/credential_manager.py store ELEVENLABS_API_KEY      │
│                                                                  │
│ → "Enter value for ELEVENLABS_API_KEY:" will be displayed        │
│ → Paste the copied API key and press Enter                       │
│   (The characters you type won't be shown on screen. This is     │
│    normal.)                                                      │
│ → "Stored ELEVENLABS_API_KEY" means it was saved successfully    │
│                                                                  │
│ (2) Also save with the alias (some code references this name):   │
│ uv run python tools/credential_manager.py store ELEVEN_API_KEY          │
│                                                                  │
│ → Paste the same API key and press Enter                         │
│ → "Stored ELEVEN_API_KEY" means it's done                        │
└──────────────────────────────────────────────────────────────────┘

Once both saves are complete, come back to this chat and let me know "done".
```

**Why run in a separate window:**
If you handle API keys in the AI chat, the values will remain in the conversation log.
By running `credential_manager.py` in a separate window, the key values are stored directly
in the OS's encrypted storage (macOS Keychain / Windows Credential Locker / Linux SecretService),
and never stored in plaintext files or chat logs.

**Why save under two key names:**
The official ElevenLabs SDK and sample code sometimes use `ELEVEN_API_KEY`.
By saving the same value under both `ELEVENLABS_API_KEY` and `ELEVEN_API_KEY`,
any code referencing either name will work correctly.

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Save the API key",
  "questions": [{
    "id": "store_status",
    "prompt": "Did you run both commands in a separate terminal?",
    "options": [
      {"id": "done", "label": "I saved both!"},
      {"id": "one_done", "label": "I only saved the first one"},
      {"id": "terminal_help", "label": "I don't know how to open a terminal"},
      {"id": "command_error", "label": "I got an error with the command"},
      {"id": "security_question", "label": "I have a question about security"}
    ]
  }]
}
```

(done -> Proceed to Step 4)
(one_done -> Guide: "Please also run the second one: `uv run python tools/credential_manager.py store ELEVEN_API_KEY` -> Paste the same API key.")
(terminal_help -> Guide: "For Cursor: Menu at the top > Terminal > New Terminal, or press Ctrl+backtick (Cmd+backtick on Mac). For Claude Code: Open a separate terminal window/tab. Mac: Cmd+T (new tab) or Cmd+N (new window). Windows: Open your WSL terminal (Ubuntu), or add an Ubuntu tab in Windows Terminal. Then cd to the project directory.")
(command_error -> AI runs `uv run python tools/credential_manager.py status` to check the situation and identify the cause. If keyring is not installed, auto-run `uv add keyring`)
(security_question -> Explain: "This tool uses the OS's standard encrypted storage. On macOS it uses Keychain, on Windows it uses Credential Locker, and on Linux it uses SecretService (GNOME Keyring, etc.). No plaintext files (.env) are created. The storage is also locked when the screen is locked, providing protection from physical access.")

---

## Step 4: Setup Test

**What the AI auto-runs:**

1. First, run `credential_manager.py status` to check if `ELEVENLABS_API_KEY` is saved in the Credential Store:
   - **Note**: Do not display the API key value at all. Only show "Confirmed that the API key is set."
   - Status check command: `uv run python tools/credential_manager.py status`

2. If the basic check passes, send a test request to the ElevenLabs API:
   - Inject environment variables from the Credential Store and make the API call
   - Test code example:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_API_KEY")
     if not key:
         print("Error: ELEVENLABS_API_KEY is not set.")
         sys.exit(1)
     resp = requests.get("https://api.elevenlabs.io/v1/models",
         headers={"xi-api-key": key})
     if resp.status_code == 200:
         models = resp.json()
         print(f"Connection successful! Available models: {len(models)}")
         for m in models[:3]:
             print(f"  - {m.get('name', 'N/A')}")
     else:
         print(f"Error: {resp.status_code}")
         print("Please check re-authentication, API key regeneration, or permission settings.")
     ```
   - Auto-install required packages (`requests`, `keyring`) if not installed

3. Display an AskQuestion based on the test result:

**On success:**
```text
ElevenLabs API setup is complete!

Test result: Successfully retrieved the model list from the API.
You can now use text-to-speech (TTS), voice synthesis, narration generation, and more.
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
      {"id": "recheck_key", "label": "Recheck the API key (go back to Step 2)"},
      {"id": "show_error", "label": "I want to see the error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(recheck_key -> Go back to Step 2)
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
      {"id": "trouble_voice", "label": "I don't know how to choose a Japanese voice"},
      {"id": "trouble_cost", "label": "I'm worried about costs"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Trouble 1: "Invalid API key" Error
**Cause**: API key was not copied correctly, or the key is invalid
**What the AI does**:
1. Check `ELEVENLABS_API_KEY` save status with `credential_manager.py status` (only show masked value)
2. If not saved in Credential Store, guide to re-register
3. If saved, re-run the API test. If it fails, guide: "Please recreate the key on the ElevenLabs settings page: https://elevenlabs.io/app/settings/api-keys"

### Trouble 2: "Quota exceeded" Error
**Cause**: Reached the free plan's monthly character limit (10,000 characters)
**AI guidance**: "The ElevenLabs free plan allows up to 10,000 characters per month. It resets at the beginning of each month, so you can wait until the next month or consider upgrading to a paid plan (Starter: $5/month, 30,000 characters). You can check current usage at https://elevenlabs.io/app/subscription."

### Trouble 3: Python Package Error
**Cause**: Required packages are not installed
**What the AI does**: Auto-install missing packages (`uv add requests keyring`)

### Trouble 4: Choosing Japanese Voices
**AI guidance**: "ElevenLabs offers multilingual voices. To find voices that support Japanese, filter by 'Japanese' at https://elevenlabs.io/app/voice-library. Using the Multilingual v2 model allows most voices to naturally read Japanese text."

### Trouble 5: Cost Concerns
**AI guidance**: "ElevenLabs has a free plan that allows up to 10,000 characters per month. For training-level usage (a few test generations), the free tier is more than enough. You can check your usage at https://elevenlabs.io/app/subscription anytime. There's no automatic upgrade to a paid plan, so you won't be charged unexpectedly."

### Trouble 6: Other Errors
**What the AI does**: Check the error message content, identify the cause, and guide the user to a solution

---

## Checkpoint
- [ ] Created an ElevenLabs account (or logged in)
- [ ] Got and copied the API key from the API key settings page
- [ ] Saved to Credential Store with credential_manager.py store ELEVENLABS_API_KEY
- [ ] Also saved the alias with credential_manager.py store ELEVEN_API_KEY
- [ ] Confirmed the save with credential_manager.py status
- [ ] API test succeeded (retrieved the model list)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "ElevenLabs API setup is complete! What would you like to do next?",
    "options": [
      {"id": "try_video_narration", "label": "Try creating a product intro video (/start-13-3)"},
      {"id": "try_slide_video", "label": "Try creating a slide narration video (/start-13-5)"},
      {"id": "setup_other", "label": "Set up another API (/start-0-1)"},
      {"id": "back_to_setup", "label": "Go back to the setup list (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- try_video_narration -> Guide to /start-13-3
- try_slide_video -> Guide to /start-13-5
- setup_other -> Guide to /start-0-1
- back_to_setup -> Guide to /start-0-1
- finish -> End

---

## Completion

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-elevenlabs` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "ElevenLabs API setup is complete. You can proceed to create a product intro video with `/start-13-3` or a slide narration video with `/start-13-5`."

## Reference links (mirrors aiagent-course Module 15 slides)

Five resources you can use to find templates or inspiration.

- [Dribbble (motion design portfolios)](https://dribbble.com/)
- [Envato Elements — video templates / logo animation](https://elements.envato.com/video-templates/logo+animation)
- [Placeit — minimalist motion-graphics intro maker](https://placeit.net/c/videos/stages/intro-maker-with-minimalist-motion-graphics-988)
- [YouTube — After Effects templates project channel](https://www.youtube.com/@paftereffectstemplatesproj6705)
- [YouTube — motion-graphics templates playlist](https://www.youtube.com/playlist?list=PLCWRuswMLN-huRtRNjplBjZGuIknrhckj)


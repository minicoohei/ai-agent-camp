---
description: "fal.ai API Setup (Complete Guide)"
duration: "~10 min"
prerequisites: ["Browser available", "Have a GitHub or Google account"]
level: "beginner"
tags: ["setup", "fal", "api", "video", "image"]
---

# fal.ai API Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-fal` to display progress
2. Auto-detect existing API key:
   - Run `uv run python tools/credential_manager.py status`
   - If FAL_KEY is already set, you can just run Step 4 (test) and mark it as complete
   - If a plaintext key exists in `.env`, suggest migrating it to the credential store

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Get an API key from fal.ai and save it to the Credential Store so you can use AI features like video and image generation |
| Duration | ~10 minutes |
| Prerequisites | A GitHub or Google account, and a browser available |
| Skill Level | Mostly AI auto-run (only one manual command in a separate terminal for API key storage) |

**What is fal.ai:**
A platform that provides unified access to AI engines for video generation (Kling, Veo, etc.), image generation, lip sync (Fabric), music generation (Suno), and more. One API key gives you access to multiple AI models.

**Session flow:**
1. Open fal.ai in the browser (AI opens the browser automatically)
2. Create an account and get your API key (just click buttons on screen)
3. Save the API key securely to the Credential Store (run a command in a separate terminal)
4. Functionality test (AI runs automatically)

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
(check_prereq -> Guide: "You can sign up with a GitHub or Google account. If you can log in via browser, you're ready.")
(different_lesson -> Display module list)

---

## Step 1: Open fal.ai in the Browser and Create an Account

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to open the browser automatically:

```bash
# Mac:
open https://fal.ai
# Windows:
start https://fal.ai
# Linux:
xdg-open https://fal.ai
```

**After the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Create a fal.ai account",
  "questions": [{
    "id": "account_status",
    "prompt": "Did the browser open? Follow these steps to create your account:\n\n1. Click 'Sign Up' or 'Login' in the top right\n2. Authenticate with GitHub or Google account\n3. Once the dashboard is displayed, you're done\n\nAre you logged in?",
    "options": [
      {"id": "logged_in", "label": "I'm logged in!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "signup_issue", "label": "I can't sign up"},
      {"id": "already_have_account", "label": "I already have an account"}
    ]
  }]
}
```

(logged_in -> Proceed to Step 2)
(browser_not_open -> Guide: "Open this URL directly in your browser: https://fal.ai")
(signup_issue -> Guide: "Try authenticating with your GitHub account. If that fails, try with your Google account.")
(already_have_account -> Proceed to Step 2)

---

## Automating with Chrome Integration (`/chrome` mode)

**Prerequisite:** The "Claude in Chrome" extension (v1.0.36+) must be installed in Chrome, and you must have launched with `claude --chrome` or run `/chrome` in the session.

**What the AI auto-runs with Chrome integration:**
1. Open https://fal.ai in the browser
2. Use Chrome integration to perform the following operations in order:
   - Click the "Sign Up" or "Login" button
   - Authenticate with GitHub or Google account (wait for user's action)
   - After login, navigate to https://fal.ai/dashboard/keys
   - Click the "Create Key" or "Add Key" button
3. Once the API key is displayed, tell the user "Please copy the API key"
4. Proceed to Step 3

**Note:** Do not read the API key value from the browser screen. The user copies it manually.

If Chrome integration is not available, follow the steps below manually.

---

## Step 2: Get Your API Key

**What the AI does:**
1. Open the API key management page in the browser:

```bash
# Mac:
open https://fal.ai/dashboard/keys
# Windows:
start https://fal.ai/dashboard/keys
# Linux:
xdg-open https://fal.ai/dashboard/keys
```

**After the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 2: Get your API key",
  "questions": [{
    "id": "key_status",
    "prompt": "Did the API key management page open? Follow these steps to get your API key:\n\n1. Click the 'Create Key' or 'Add Key' button\n2. Copy the displayed API key\n   (The key may only be shown once. Make sure to copy it.)\n\nDid you copy the API key?",
    "options": [
      {"id": "copied", "label": "I copied the API key!"},
      {"id": "page_not_found", "label": "I can't find the key management page"},
      {"id": "no_create_button", "label": "I can't find the 'Create Key' button"},
      {"id": "key_already_exists", "label": "I already have an existing key"}
    ]
  }]
}
```

(copied -> Proceed to Step 3)
(page_not_found -> Guide: "Open this URL directly in your browser: https://fal.ai/dashboard/keys Make sure you're logged in.")
(no_create_button -> Guide: "Wait for the page to fully load. Look for 'Keys' or 'API Keys' in the left sidebar menu of the dashboard.")
(key_already_exists -> Guide: "You can also use an existing key. If you can copy the key value, proceed to Step 3. You can also create a new key if you prefer." and proceed to Step 3)

---

## Step 3: Save the API Key Securely

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
│ uv run python tools/credential_manager.py store FAL_KEY            │
│                                                             │
│ → "Enter value for FAL_KEY:" will be displayed              │
│ → Paste the copied API key and press Enter                  │
│   (The characters you type won't be shown on screen.        │
│    This is normal.)                                         │
│ → "Stored FAL_KEY" means it was saved successfully          │
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
  "title": "Step 3: Save the API key",
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

(done -> Proceed to Step 4)
(terminal_help -> Guide: "For Cursor: Menu at the top > Terminal > New Terminal, or press Ctrl+` (Cmd+` on Mac). For Claude Code: Open a separate terminal window/tab. Mac: Cmd+T (new tab) or Cmd+N (new window). Windows: Open PowerShell or Windows Terminal from the Start menu, or press Ctrl+Shift+T for a new tab. Then cd to the project directory.")
(command_error -> AI runs `uv run python tools/credential_manager.py status` to check the situation and identify the cause. If keyring is not installed, auto-run `pip install keyring`)
(security_question -> Explain: "This tool uses the OS's standard encrypted storage. On macOS it uses Keychain, on Windows it uses Credential Locker, and on Linux it uses SecretService (GNOME Keyring, etc.). No plaintext files (.env) are created. The storage is also locked when the screen is locked, providing protection from physical access.")

---

## Step 4: Setup Test

**What the AI auto-runs:**

1. First, run `credential_manager.py status` to check if `FAL_KEY` is saved in the Credential Store:
   - **Note**: Do not display the API key value itself in the chat. Only show masked output like "API key is set (first 8 characters: xxxxxxxx...)"
   - Status check command: `uv run python tools/credential_manager.py status`

2. Check if the `fal-client` package is installed:
   - If not installed: auto-run `pip install fal-client`

3. Run a package import and FAL_KEY configuration check test:
   - **Note**: Actual fal.ai API calls incur costs, so only check the package import and key configuration
   - Test code:
     ```python
     import os
     import sys
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("FAL_KEY")
     if not key:
         print("Error: FAL_KEY is not set.")
         sys.exit(1)
     try:
         import fal_client
         print(f"fal-client installed: {fal_client.__version__ if hasattr(fal_client, '__version__') else 'OK'}")
         print(f"FAL_KEY set (first 8 characters: {key[:8]}...)")
         print("fal.ai API setup is complete!")
     except ImportError:
         print("fal-client is not installed. Please run pip install fal-client.")
     ```

4. Display an AskQuestion based on the test result:

**On success:**
```text
fal.ai API setup is complete!

Test result: Confirmed fal-client package import and FAL_KEY configuration.
You can now use AI engines for video generation (Kling, Veo, etc.), image generation,
lip sync (Fabric), music generation (Suno), and more.
```

**On failure — AskQuestion:**
```json
{
  "title": "Test Result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the test. Let's check possible causes.",
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
(skip_test -> Guide: "The test was skipped. You can check later with /check-setup.")

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
      {"id": "trouble_signup", "label": "I can't create an account / log in"},
      {"id": "trouble_invalid", "label": "API key is invalid (authentication error)"},
      {"id": "trouble_package", "label": "I get an error installing fal-client"},
      {"id": "trouble_python", "label": "I have a Python version issue"},
      {"id": "trouble_cost", "label": "I'm worried about costs"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Trouble 1: Can't Create Account / Log In
**Cause**: Issues with the authentication provider (GitHub/Google)
**What the AI does**:
1. Guide: "Try a different authentication method. If GitHub failed, try Google account, or vice versa."
2. Guide: "Try accessing https://fal.ai again in your browser's incognito/private browsing mode."
3. If still unresolved: "Please contact fal.ai support (https://fal.ai)."

### Trouble 2: Invalid API Key (Authentication Error)
**Cause**: API key was not copied correctly, or the key is invalid
**What the AI does**:
1. Check `FAL_KEY` save status with `credential_manager.py status` (only show masked value)
2. If not saved in Credential Store, guide to re-register
3. If saved: "Check on the fal.ai dashboard (https://fal.ai/dashboard/keys) that the key is valid. Create a new key if needed."

### Trouble 3: Error Installing fal-client
**Cause**: pip issues or dependency conflicts
**What the AI does**:
1. Re-run `pip install fal-client`
2. If errors persist, run `pip install --upgrade pip` and retry
3. If the venv is broken, recreate it with `bash tools/scripts/setup.sh`

### Trouble 4: Python Version Issue
**Cause**: fal-client requires Python 3.10 or higher
**What the AI does**:
1. Check current version with `python --version`
2. If below 3.10: "fal-client requires Python 3.10 or higher. Please upgrade Python."
3. If pyenv is installed, guide to `pyenv install 3.10`

### Trouble 5: Cost Concerns
**AI guidance**: "fal.ai uses a pay-as-you-go pricing model. For training-level usage (a few image/video generation tests), costs are around a few dollars. You can check usage and balance on the dashboard (https://fal.ai/dashboard) anytime. You can also set a billing cap."

### Trouble 6: Other Errors
**What the AI does**: Check the error message content, identify the cause, and guide the user to a solution

---

## Checkpoint
- [ ] Created a fal.ai account
- [ ] Got an API key from the fal.ai dashboard
- [ ] Saved FAL_KEY to the Credential Store with credential_manager.py store
- [ ] Confirmed the save with credential_manager.py status
- [ ] fal-client package is installed
- [ ] Test succeeded (fal-client import and FAL_KEY configuration confirmed)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "fal.ai API setup is complete! What would you like to do next?",
    "options": [
      {"id": "video_overview", "label": "Learn about video AI engines (/start-13-2)"},
      {"id": "setup_elevenlabs", "label": "Also set up ElevenLabs API (/setup-elevenlabs)"},
      {"id": "back_to_setup", "label": "Go back to the setup list (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- video_overview -> Guide to /start-13-2
- setup_elevenlabs -> Guide to /setup-elevenlabs
- back_to_setup -> Guide to /start-0-1
- finish -> End

---

## Completion

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-fal` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "Next, learn about video AI engines with `/start-13-2`. Or set up the ElevenLabs API with `/setup-elevenlabs`."

---
description: "Typefully API Setup (with complete guide)"
duration: "~10 min"
prerequisites: ["Have an X (Twitter) account", "Browser available"]
level: "beginner"
tags: ["setup", "typefully", "api", "sns"]
---

# Typefully API Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-typefully` to display progress
2. Auto-detect existing API key:
   - Run `uv run python tools/credential_manager.py status`
   - If TYPEFULLY_API_KEY is already set, only run Step 4 (API test) and mark as complete
   - If it exists in plaintext in `.env`, suggest migration to the credential store

> **This setup is optional.** The Typefully API is used in marketing lessons (Module 12) for scheduling SNS posts. You can skip it if you're not taking marketing lessons.

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Obtain a Typefully API key, save it to the Credential Store, and enable SNS post scheduling and management features |
| Duration | ~10 minutes |
| Prerequisites | Have an X (Twitter) account, browser available |
| Skill Level | Mostly AI auto-run (only one manual command in a separate terminal for API key storage) |

**What is Typefully:**
Typefully is a service for scheduling and managing SNS posts on X (Twitter), LinkedIn, and more. You can post AI-generated content directly. Free plan available. Paid plans start at $12.5/month.

**Session flow:**
1. Open Typefully in the browser (AI auto-launches browser)
2. Sign up / log in with X (Twitter) account
3. Obtain the API key (just copy from the settings page)
4. Securely save the API key with credential_manager.py (run in separate terminal)
5. Operation test (AI auto-runs)

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

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
      {"id": "skip", "label": "I want to skip this setup"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(chrome -> After opening the browser in Step 1, follow the "Chrome integration automation" section)
(check_prereq -> Guide: "You're good to go if you can log in to your X (Twitter) account in a browser. Typefully has a free plan so there's no cost")
(skip -> Guide: "Typefully API setup skipped. You can set it up later with /setup-typefully when needed" and end)
(different_lesson -> Show module list)

---

## Step 1: Open Typefully in the Browser

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to auto-launch the browser:

```bash
# Mac:
open https://typefully.com
# Windows:
start https://typefully.com
# Linux:
xdg-open https://typefully.com
```

**Once the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Sign Up / Log In to Typefully",
  "questions": [{
    "id": "browser_status",
    "prompt": "Did the browser open? Follow these steps to sign up:\n\n1. Click 'Get started free' on the Typefully top page\n2. Select 'Sign up with X (Twitter)' to authenticate with your X account\n3. Once the Typefully dashboard appears, sign-up is complete\n\nWere you able to sign up?",
    "options": [
      {"id": "signed_up", "label": "Signed up / logged in!"},
      {"id": "already_account", "label": "I already have an account"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "x_auth_issue", "label": "Authentication with X account isn't working"}
    ]
  }]
}
```

(signed_up -> Proceed to Step 2)
(already_account -> Proceed to Step 2)
(browser_not_open -> Guide: "Please open this URL directly in your browser: https://typefully.com")
(x_auth_issue -> Guide: "If authentication with your X account is blocked, enable third-party app access in X's privacy settings. Go to X -> Settings -> Security and account access -> Apps and sessions to check")

---

## Chrome Integration Automation (`/chrome` mode)

**Prerequisites:** The "Claude in Chrome" extension (v1.0.36+) is installed in Chrome, and you launched with `claude --chrome` or ran `/chrome` within the session.

**What the AI auto-runs via Chrome integration:**
1. Open https://typefully.com in the browser
2. Use Chrome integration to sequentially perform:
   - Click "Get started free"
   - Authenticate with "Sign up with X (Twitter)" (wait for user action)
   - After login, navigate to https://typefully.com/settings/api
   - Click "Generate API Key" or "Create API Key"
3. Once the API key is displayed, prompt the user: "Please copy the API key"
4. Proceed to Step 3

**Note:** Do not read the API key value from the browser screen. The user copies it manually.

If Chrome integration is not available, follow the manual steps below.

---

## Step 2: Obtain the API Key

**What the AI does:**
1. Run the following command to open the API settings page in the browser:

```bash
# Mac:
open https://typefully.com/settings/api
# Windows:
start https://typefully.com/settings/api
# Linux:
xdg-open https://typefully.com/settings/api
```

**Once the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 2: Obtain API Key",
  "questions": [{
    "id": "api_key_status",
    "prompt": "Did the API settings page open? Follow these steps to obtain the API key:\n\n1. Go to the Typefully Settings > API page\n2. If an API key is displayed, copy it as-is\n3. If you need to create a new one, click 'Generate API Key'\n4. Copy the displayed API key\n\nWere you able to copy the API key?",
    "options": [
      {"id": "copied", "label": "API key copied!"},
      {"id": "page_not_found", "label": "Can't find the API settings page"},
      {"id": "no_api_key", "label": "No API key is displayed"},
      {"id": "paid_plan_required", "label": "It says a paid plan is required"}
    ]
  }]
}
```

(copied -> Proceed to Step 3)
(page_not_found -> Guide: "Please open this URL directly in your browser: https://typefully.com/settings/api -- The settings page will appear if you're logged in")
(no_api_key -> Guide: "Check if there's a 'Generate API Key' or 'Create API Key' button on the page. If you can't find it, try reloading the page")
(paid_plan_required -> Guide: "A paid plan may be required for API access. If the free plan doesn't support API access, you can skip this setup without any issues")

---

## Step 3: Save the API Key Securely

**Important security note:**
Do not paste the API key in this chat. We'll save it securely in a separate terminal window.

**What the AI auto-runs:**
1. Check whether the `keyring` package is installed
   - If not installed: Auto-run `pip install keyring`
2. Run `uv run python tools/credential_manager.py status` to check the current state

**Message to show the user:**

```text
After copying the API key, follow these steps to save it securely:

┌─────────────────────────────────────────────────────────────┐
│ Run the following command in a separate terminal window:    │
│                                                             │
│ Cursor: Ctrl+` (backtick) to open a new terminal           │
│ Claude Code: Open a separate terminal window                │
│                                                             │
│ uv run python tools/credential_manager.py store TYPEFULLY_API_KEY  │
│                                                             │
│ -> "Enter value for TYPEFULLY_API_KEY:" will appear         │
│ -> Paste the copied API key and press Enter                 │
│   (The text you type won't be shown on screen. This is      │
│    normal)                                                  │
│ -> "Stored TYPEFULLY_API_KEY" means it's saved!             │
└─────────────────────────────────────────────────────────────┘

Once saved, come back to this chat and let me know you're "done".
```

**Why run it in a separate window:**
If you handle the API key in this AI chat, the value remains in the conversation log.
By running `credential_manager.py` in a separate window, the key value is saved directly to the OS's
encrypted storage (macOS Keychain / Windows Credential Locker / Linux SecretService),
and never appears in plaintext files or chat logs.

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Save the API Key",
  "questions": [{
    "id": "store_status",
    "prompt": "Were you able to run the command in a separate terminal?",
    "options": [
      {"id": "done", "label": "Saved!"},
      {"id": "terminal_help", "label": "I don't know how to open a terminal"},
      {"id": "command_error", "label": "The command gave an error"},
      {"id": "security_question", "label": "I have a question about security"}
    ]
  }]
}
```

(done -> Proceed to Step 4)
(terminal_help -> Guide: "For Cursor: Menu > Terminal > New Terminal, or press Ctrl+` (Mac: Cmd+`). For Claude Code: Open a separate terminal window/tab. Mac: Cmd+T (new tab) or Cmd+N (new window). Windows: Open PowerShell or Windows Terminal from the Start Menu, or Ctrl+Shift+T for a new tab. Then cd to the project directory")
(command_error -> AI runs `uv run python tools/credential_manager.py status` to check the situation and identify the cause. If keyring is not installed, auto-run `pip install keyring`)
(security_question -> Explain: "This tool uses your OS's built-in encrypted storage. On macOS it uses Keychain, on Windows it uses Credential Locker, and on Linux it uses SecretService (GNOME Keyring, etc.). No plaintext files (.env) are created. The storage is also locked when your screen is locked, providing protection against physical access")

---

## Step 4: Configuration Test

**What the AI auto-runs:**

1. First run `credential_manager.py status` to check if `TYPEFULLY_API_KEY` is saved in the Credential Store:
   - **Note**: Do not display the API key value itself in chat. Only show masked output like "Confirmed API key is set (first 4 characters: xxxx...)"
   - Status check command: `uv run python tools/credential_manager.py status`

2. If the basic check passes, send an actual test request to the Typefully API:
   - Inject from Credential Store to environment variables and execute the API call
   - Test code example:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     key = os.getenv("TYPEFULLY_API_KEY")
     if not key:
         print("Error: TYPEFULLY_API_KEY is not set.")
         sys.exit(1)
     resp = requests.get("https://api.typefully.com/v1/drafts/recently-created",
         headers={"X-API-KEY": key})
     if resp.status_code == 200:
         print("Connection successful! Typefully API is accessible.")
     else:
         print(f"Error: {resp.status_code}")
         print("Please check re-authentication, API key regeneration, or permission settings.")
     ```
   - Auto-install any missing packages (`requests`, `keyring`)

3. Display AskQuestion based on test results:

**On test success:**
```text
Typefully API setup is complete!

Test result: Response successfully received from the API.
You can now use SNS post scheduling and management features.
```

**AskQuestion on test failure:**
```json
{
  "title": "Test result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the API test. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Try the test again"},
      {"id": "recheck_key", "label": "Re-check the API key (go back to Step 2)"},
      {"id": "show_error", "label": "I want to see error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(recheck_key -> Go back to Step 2)
(show_error -> Display error message with cause and solution)
(skip_test -> Guide: "API test skipped. You can check later with /check-setup")

---

## Common Troubleshooting

**AskQuestion configuration:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_x_auth", "label": "X account authentication isn't working"},
      {"id": "trouble_invalid", "label": "Getting 'Invalid API key' or 'Unauthorized' error"},
      {"id": "trouble_not_found", "label": "Can't find the API key page"},
      {"id": "trouble_cost", "label": "Concerned about pricing"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Issue 1: X account authentication isn't working
**Cause**: Third-party app access is blocked in X's privacy settings
**What the AI does**:
1. Guide: "Go to X (Twitter) -> Settings -> Security and account access -> Apps and sessions to enable third-party app access"
2. If that doesn't help: "Try clearing your browser cookies and trying again"
3. Check whether the X account is suspended or restricted

### Issue 2: "Invalid API key" or "Unauthorized" error
**Cause**: API key was not copied correctly, or the key is invalid
**What the AI does**:
1. Check `TYPEFULLY_API_KEY` storage state with `credential_manager.py status` (only masked display of value)
2. If not saved in Credential Store, guide re-registration
3. If saved, re-run API test. On failure, guide: "Please recreate the key on the Typefully settings page (https://typefully.com/settings/api)"

### Issue 3: Can't find the API key page
**Cause**: Not logged in, or URL has changed
**AI guidance**: "First log in to Typefully, then access https://typefully.com/settings/api. If the page isn't found, navigate from the top-right icon on the dashboard -> Settings -> API"

### Issue 4: Concerned about pricing
**AI guidance**: "Typefully has a free plan. Basic API access is available on the free plan. Paid plans start at $12.5/month with more features (scheduling, analytics, etc.). The free plan is sufficient for training-level usage"

### Issue 5: Other errors
**What the AI does**: Check the error message content, identify the cause, and guide the solution

---

## Checkpoint
- [ ] Signed up for Typefully with X (Twitter) account
- [ ] Obtained API key from the API settings page (Settings > API)
- [ ] Saved to Credential Store with credential_manager.py store
- [ ] Confirmed storage with credential_manager.py status
- [ ] API test succeeded (received response from Typefully API)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Typefully API setup is complete! What would you like to do next?",
    "options": [
      {"id": "try_marketing", "label": "Start marketing lessons (/start-12-1)"},
      {"id": "setup_other", "label": "Set up other APIs (/start-0-1)"},
      {"id": "try_banner", "label": "Try creating a banner (/start-1-1)"},
      {"id": "back_to_setup", "label": "Back to setup list (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- try_marketing -> Guide to /start-12-1
- setup_other -> Guide to /start-0-1
- try_banner -> Guide to /start-1-1
- back_to_setup -> Guide to /start-0-1
- finish -> End

---

## Completion Processing

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-typefully` to update progress
2. Updated progress summary is automatically displayed
3. Guide the user to the next step: "You can now create and schedule SNS posts in the marketing lessons (/start-12-1)"

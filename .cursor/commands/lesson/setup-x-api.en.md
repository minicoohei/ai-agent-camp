---
description: "X (Twitter) API Setup (with complete guide)"
duration: "~15 min"
prerequisites: ["Have an X account", "Browser available"]
level: "beginner"
tags: ["setup", "x", "twitter", "api"]
---

# X (Twitter) API Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-x-api` to display progress
2. Auto-detect existing API key:
   - Run `uv run python tools/credential_manager.py status`
   - If X_BEARER_TOKEN is already set, only run Step 4 (API test) and mark as complete
   - If it exists in plaintext in `.env`, suggest migration to the credential store

**Display important warning to the user:**

```text
WARNING: X (Twitter) API requires a paid plan

- Free tier: Recent Search API is NOT available
- Basic plan: $100/month required
- This setup is optional. You can skip it if you won't use the x-research skill

Other training lessons (banner creation, chart generation, data analysis, etc.)
work perfectly fine without the X API.
```

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Obtain a Bearer Token from the X Developer Portal, save it to the Credential Store, and enable real-time X search and trend analysis features |
| Duration | ~15 minutes |
| Prerequisites | Have an X account, browser available |
| Skill Level | No CLI commands needed (all auto-run by AI + GUI-only operations) |
| Pricing | **Basic plan ($100/month) or higher required**. Free tier does not support Recent Search API |
| Use case | Real-time X (Twitter) search and trend analysis. Used by the x-research skill |

**Session flow:**
1. Open X Developer Portal in browser (AI auto-launches browser)
2. Apply for a Developer account, create a project and app
3. Obtain the Bearer Token
4. Securely save with credential_manager.py in a separate terminal
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
    "prompt": "X API setup requires the Basic plan ($100/month). Are you ready?",
    "options": [
      {"id": "ready", "label": "I have a paid plan / plan to subscribe. Let's start"},
      {"id": "chrome", "label": "Automate browser operations with /chrome"},
      {"id": "check_cost", "label": "I want to know more about pricing"},
      {"id": "skip", "label": "Skip (I won't use X API)"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(chrome -> After opening the browser in Step 1, follow the "Chrome integration automation" section)
(check_cost -> Guide: "X API pricing: Free tier is post-only (no search API). Basic plan ($100/month) enables Recent Search API. Pro plan ($5,000/month) enables Full-Archive Search, but Basic is sufficient for training. If the cost doesn't justify it, we recommend skipping")
(skip -> Guide: "X API setup skipped. No impact on other lessons. You can restart with /setup-x-api later" and proceed to completion)
(different_lesson -> Show module list)

---

## Step 1: Open X Developer Portal in Browser

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to auto-launch the browser:

```bash
# Mac:
open https://developer.x.com/en/portal/dashboard
# Windows:
start https://developer.x.com/en/portal/dashboard
# Linux:
xdg-open https://developer.x.com/en/portal/dashboard
```

**Once the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Access X Developer Portal",
  "questions": [{
    "id": "portal_status",
    "prompt": "Did the browser open? Follow these steps to apply for a Developer account:\n\n1. Log in with your X account\n2. Select 'Sign up for Free Account' or 'Subscribe to Basic'\n   (Basic plan is required to use Recent Search API)\n3. Fill in the use case (e.g., 'Academic research and AI agent training')\n4. Agree to the developer agreement\n\nDid the Developer Portal dashboard appear?",
    "options": [
      {"id": "dashboard_ready", "label": "The dashboard appeared!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "signup_issue", "label": "Having trouble with the Developer account application"},
      {"id": "already_have_account", "label": "I already have a Developer account"}
    ]
  }]
}
```

(dashboard_ready -> Proceed to Step 2)
(browser_not_open -> Guide: "Please open this URL directly in your browser: https://developer.x.com/en/portal/dashboard")
(signup_issue -> Guide: "Developer Portal applications may require review. Fill in the use case specifically (e.g., 'Building an AI-powered social media research tool for corporate training'). Review may take a few days. Please re-run this setup after receiving the approval email")
(already_have_account -> Proceed to Step 2)

---

## Chrome Integration Automation (`/chrome` mode)

**Prerequisites:** The "Claude in Chrome" extension (v1.0.36+) is installed in Chrome, and you launched with `claude --chrome` or ran `/chrome` within the session.

**What the AI auto-runs via Chrome integration:**
1. Open https://developer.x.com/en/portal/dashboard in the browser
2. Use Chrome integration to sequentially perform:
   - Select "Subscribe to Basic" (Basic plan is required for Recent Search API. Free Account does not support search API)
   - Leave payment information entry to the user (wait for user action)
   - Enter "AI agent training and educational purposes" as the use case
   - Agree to the Developer Agreement and Submit (wait for user action)
   - Navigate to "Projects & Apps" on the Dashboard
   - Click "+ Add Project" -> Enter "AIAgent Bootcamp" as Project name, select "Exploring the API" as use case
   - Click "+ Add App" -> Enter "AIAgent Bootcamp" as App name, select "Development" as environment
   - Open the "Keys and tokens" tab
   - Click "Regenerate" next to Bearer Token
   - Click "Yes, regenerate" in the confirmation dialog
3. Once the Bearer Token is displayed, prompt the user: "Please copy the token. It cannot be shown again once you leave the page"
4. Proceed to Step 3

**Note:** Do not read the Bearer Token value from the browser screen. The user copies it manually.

If Chrome integration is not available, follow the manual steps below.

---

## Step 2: Create Project and Obtain Bearer Token

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Obtain Bearer Token",
  "questions": [{
    "id": "token_status",
    "prompt": "Follow these steps to obtain the Bearer Token:\n\n1. Check the Dashboard > 'Projects & Apps' section\n2. If there's no project, click '+ Add Project'\n   - Enter a project name (e.g., 'AIAgent Bootcamp')\n   - Select a use case (e.g., 'Exploring the API')\n3. Click '+ Add App' within the project\n   - Enter an App name (e.g., 'AIAgent Bootcamp')\n   - Select 'Development' for App environment\n4. Open the 'Keys and tokens' tab\n5. Click 'Regenerate' in the 'Bearer Token' section\n6. Copy the displayed Bearer Token\n\nWere you able to copy the Bearer Token?",
    "options": [
      {"id": "copied", "label": "Bearer Token copied!"},
      {"id": "no_project", "label": "I don't know how to create a project"},
      {"id": "no_bearer", "label": "I can't find the Bearer Token"},
      {"id": "plan_issue", "label": "I'm on the Free tier and want to upgrade to Basic"}
    ]
  }]
}
```

(copied -> Proceed to Step 3)
(no_project -> Guide: "Select 'Projects & Apps' from the left menu in the Dashboard. You'll see the '+ Add Project' button. The project name can be anything (e.g., 'AIAgent Bootcamp'). After creating it, click '+ Add App' within the project to add an app")
(no_bearer -> Guide: "Select the App > open the 'Keys and tokens' tab. The 'Bearer Token' section is in the middle of the page. Click the 'Regenerate' button to generate a new token. Copy the displayed token immediately (it cannot be shown again once you leave the page)")
(plan_issue -> Guide: "Select 'Products' > 'Twitter API v2' from the left menu in the Dashboard, and click 'Subscribe' under the 'Basic' plan. Credit card information is required. After the upgrade is complete, return to the Step 2 instructions")

---

## Step 3: Save Bearer Token Securely

**Important security note:**
Do not paste the Bearer Token in this chat. We'll save it securely in a separate terminal window.

**What the AI auto-runs:**
1. Check whether the `keyring` package is installed
   - If not installed: Auto-run `pip install keyring`
2. Run `uv run python tools/credential_manager.py status` to check the current state

**Message to show the user:**

```text
After copying the Bearer Token, follow these steps to save it securely:

┌─────────────────────────────────────────────────────────────┐
│ Run the following command in a separate terminal window:    │
│                                                             │
│ Cursor: Ctrl+` (backtick) to open a new terminal           │
│ Claude Code: Open a separate terminal window                │
│                                                             │
│ uv run python tools/credential_manager.py store X_BEARER_TOKEN     │
│                                                             │
│ -> "Enter value for X_BEARER_TOKEN:" will appear            │
│ -> Paste the copied Bearer Token and press Enter            │
│   (The text you type won't be shown on screen. This is      │
│    normal)                                                  │
│ -> "Stored X_BEARER_TOKEN" means it's saved!                │
└─────────────────────────────────────────────────────────────┘

Once saved, come back to this chat and let me know you're "done".
```

**Why run it in a separate window:**
If you handle the Bearer Token in this AI chat, the value remains in the conversation log.
By running `credential_manager.py` in a separate window, the token value is saved directly to the OS's
encrypted storage (macOS Keychain / Windows Credential Locker / Linux SecretService),
and never appears in plaintext files or chat logs.

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Save the Bearer Token",
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

1. First run `credential_manager.py status` to check if `X_BEARER_TOKEN` is saved in the Credential Store:
   - **Note**: Do not display the Bearer Token value itself in chat. Only show masked output like "Confirmed Bearer Token is set (first 4 characters: AAAA...)"
   - Status check command: `uv run python tools/credential_manager.py status`

2. If the basic check passes, send an actual test request to the X API:
   - Inject from Credential Store to environment variables and execute the API call
   - Test code:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     token = os.getenv("X_BEARER_TOKEN")
     if not token:
         print("Error: X_BEARER_TOKEN is not set.")
         sys.exit(1)
     resp = requests.get("https://api.x.com/2/tweets/search/recent",
         params={"query": "hello", "max_results": 10},
         headers={"Authorization": f"Bearer {token}"})
     if resp.status_code == 200:
         data = resp.json()
         count = data.get("meta", {}).get("result_count", 0)
         print(f"Connection successful! Search results: {count} items")
     elif resp.status_code == 403:
         print("Error: Access denied. Basic plan ($100/month) or higher is required.")
     else:
         print(f"Error: {resp.status_code}")
         print("Please check re-authentication, API key regeneration, or permission settings.")
     ```
   - Auto-install any missing packages (`requests`, `keyring`)

3. Display AskQuestion based on test results:

**On test success:**
```text
X API setup is complete!

Test result: Response successfully received from Recent Search API.
You can now use X (Twitter) real-time search and trend analysis features.
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
      {"id": "recheck_token", "label": "Re-check the Bearer Token (go back to Step 1)"},
      {"id": "show_error", "label": "I want to see error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(recheck_token -> Go back to Step 1)
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
      {"id": "trouble_403", "label": "Getting a '403 Forbidden' error"},
      {"id": "trouble_429", "label": "Getting a '429 Too Many Requests' error"},
      {"id": "trouble_401", "label": "Getting a '401 Unauthorized' error"},
      {"id": "trouble_approval", "label": "Developer Portal application isn't being approved"},
      {"id": "trouble_package", "label": "Python package errors"},
      {"id": "trouble_cost", "label": "Concerned about pricing"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Issue 1: "403 Forbidden" error
**Cause**: Recent Search API is not available on the Free tier
**AI guidance**: "The X API Free tier does not support Recent Search API (/2/tweets/search/recent). An upgrade to Basic plan ($100/month) or higher is required. Go to Dashboard > Products > Twitter API v2 and Subscribe to the Basic plan. After upgrading, Bearer Token regeneration is not needed (the same token will work)"

### Issue 2: "429 Too Many Requests" error
**Cause**: Rate limit reached
**AI guidance**: "The X API has rate limits. The Basic plan's Recent Search API allows 60 requests per 15 minutes. Please wait a few minutes and try again. Avoid sending a large number of requests in rapid succession"

### Issue 3: "401 Unauthorized" error
**Cause**: Bearer Token is invalid or was not copied correctly
**What the AI does**:
1. Check `X_BEARER_TOKEN` storage state with `credential_manager.py status` (only masked display of value)
2. If not saved in Credential Store, guide re-registration
3. If saved, re-run API test. On failure, guide: "Go to Developer Portal > App > Keys and tokens and Regenerate the Bearer Token"

### Issue 4: Developer Portal application isn't being approved
**AI guidance**: "Developer Portal applications may require review. Check the following: (1) Fill in the use case specifically and in English (2) Emphasize the educational purpose, such as 'Academic research and AI agent training for corporate education programs' (3) Clearly state how data will be used (e.g., 'Analyzing public tweet trends for training purposes only'). Approval typically takes 1-3 business days. Re-applications are also possible"

### Issue 5: Python package errors
**Cause**: Required packages are not installed
**What the AI does**: Auto-install missing packages (`pip install requests keyring`)

### Issue 6: Concerned about pricing
**AI guidance**: "X API pricing is as follows: Free ($0) = post only, no search API. Basic ($100/month) = Recent Search API (past 7 days) available. Pro ($5,000/month) = Full-Archive Search (entire history) available. Basic is sufficient for training. Lessons that don't use X API (banner creation, chart generation, etc.) are unaffected. If the cost doesn't justify it, feel free to skip"

### Issue 7: Other errors
**What the AI does**: Check the error message content, identify the cause, and guide the solution

---

## Checkpoint
- [ ] Applied for a Developer account on X Developer Portal
- [ ] Created a project and app
- [ ] Obtained the Bearer Token
- [ ] Saved to Credential Store with credential_manager.py store
- [ ] Confirmed storage with credential_manager.py status
- [ ] API test succeeded (received response from Recent Search API)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "X API setup is complete! What would you like to do next?",
    "options": [
      {"id": "try_x_research", "label": "Try X research (x-research skill)"},
      {"id": "try_marketing", "label": "Start marketing lessons (/start-12-1)"},
      {"id": "setup_other", "label": "Set up other APIs (/start-0-1)"},
      {"id": "back_to_setup", "label": "Back to setup list (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- try_x_research -> Guide how to use the x-research skill
- try_marketing -> Guide to /start-12-1
- setup_other -> Guide to /start-0-1
- back_to_setup -> Guide to /start-0-1
- finish -> End

---

## Completion Processing

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-x-api` to update progress
2. Updated progress summary is automatically displayed
3. Guide the user to the next step: "You can now use the X API with the x-research skill and marketing lessons (/start-12-1)"

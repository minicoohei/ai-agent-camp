---
description: "Lesson command"
duration: "~15 min"
prerequisites: ["Admin access to a Slack workspace"]
level: "beginner"
tags: ["setup", "slack", "api"]
---

# Slack API Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-slack` to display progress
2. **This step is optional.** You can skip it if you won't be using Slack integration
3. Auto-detect existing token:
   - Check whether `SLACK_USER_TOKEN` exists in `.env` or credential store
   - If it exists, verify validity with Slack API `auth.test`. If valid, ask "Slack is already configured. Would you like to skip?"
4. If skipping: Run `uv run python tools/setup_progress.py skip setup-slack --reason 'User skipped'`

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Create a Slack App, obtain a User Token, save it securely, and enable Slack search and message retrieval features |
| Duration | ~15 minutes |
| Prerequisites | Admin access to a Slack workspace (or permission to add Apps), browser available |
| Skill Level | No CLI commands needed (all auto-run by AI + GUI-only operations) |

**Session flow:**
1. Open the Slack App management page (AI auto-launches browser)
2. Create a new Slack App (click buttons on screen)
3. Set up User Token Scopes (add required permissions)
4. Install to workspace (click the allow button)
5. Save the User Token securely (using credential_manager)
6. Operation test (AI auto-runs)

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
      {"id": "no_slack", "label": "I don't have a Slack workspace"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(chrome -> After opening the browser in Step 1, follow the "Chrome integration automation" section)
(check_prereq -> Guide: "You're good to go if you're logged into a Slack workspace and have permission to add Apps. If you don't have permission, check with your workspace admin")
(no_slack -> Guide: "You can create a Slack workspace for free. Create a test workspace at https://slack.com/create, then restart this setup")
(different_lesson -> Show module list)

---

## Step 1: Open Slack App Management Page

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to auto-launch the browser:

```bash
# Mac:
open https://api.slack.com/apps
# Windows:
start https://api.slack.com/apps
# Linux:
xdg-open https://api.slack.com/apps
```

**Once the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Create a Slack App",
  "questions": [{
    "id": "app_create",
    "prompt": "The Slack App management page has opened in your browser. Follow these steps to create a new App:\n\n1. Click the 'Create New App' button in the top right\n2. Select 'From scratch'\n3. Enter 'AIAgent Bootcamp' as the App Name\n4. Select your workspace under 'Pick a workspace'\n5. Click the 'Create App' button\n\nWere you able to create the App?",
    "options": [
      {"id": "created", "label": "App created!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "no_create_button", "label": "Can't find the 'Create New App' button"},
      {"id": "no_workspace", "label": "My workspace doesn't appear"},
      {"id": "permission_error", "label": "I got a permissions error"}
    ]
  }]
}
```

(created -> Proceed to Step 2)
(browser_not_open -> Guide: "Please open this URL directly in your browser: https://api.slack.com/apps")
(no_create_button -> Guide: "You may not be logged in to Slack. First, click 'Sign in' in the top right to log in with your Slack account")
(no_workspace -> Guide: "Reload the page while logged into your workspace. If it still doesn't appear, you may need to create a new workspace")
(permission_error -> Guide: "Your workspace admin may have restricted App additions. Ask the admin to allow adding a Slack App called 'AIAgent Bootcamp'. Alternatively, create a free test workspace at https://slack.com/create")

---

## Chrome Integration Automation (`/chrome` mode)

**Prerequisites:** The "Claude in Chrome" extension (v1.0.36+) is installed in Chrome, and you launched with `claude --chrome` or ran `/chrome` within the session.

**What the AI auto-runs via Chrome integration:**
1. Open https://api.slack.com/apps in the browser
2. Use Chrome integration to sequentially perform:
   - Click "Create New App"
   - Select "From scratch"
   - Enter "AIAgent Bootcamp" as the App Name
   - Select a workspace under "Pick a workspace"
   - Click "Create App"
   - Click "OAuth & Permissions" in the left menu
   - In the "User Token Scopes" section, click "Add an OAuth Scope" and add these 4 scopes one by one: channels:history, channels:read, chat:write, users:read
   - Click "Install to Workspace" at the top of the page
   - Click "Allow" on the permission confirmation screen
3. Once the User OAuth Token (xoxp-...) appears, prompt the user: "Click the Copy button next to the token to copy it"
4. Proceed to Step 4

**Note:** Do not read the token value from the browser screen. The user copies it manually.

If Chrome integration is not available, follow the manual steps in Steps 2-3 below.

---

## Step 2: Set Up User Token Scopes

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Set Up User Token Scopes",
  "questions": [{
    "id": "scope_setup",
    "prompt": "The App settings page is displayed. Follow these steps to set up User Token Scopes:\n\n1. Click 'OAuth & Permissions' in the left menu\n2. Scroll down to find the 'Scopes' section\n3. Click 'Add an OAuth Scope' under 'User Token Scopes'\n4. Add the following 4 scopes one by one:\n\n   - channels:history (read channel messages)\n   - channels:read (read channel information)\n   - chat:write (send messages)\n   - users:read (read user information)\n\nHave you added all 4 scopes?",
    "options": [
      {"id": "scopes_added", "label": "Added all 4 scopes!"},
      {"id": "cant_find_oauth", "label": "Can't find 'OAuth & Permissions'"},
      {"id": "cant_find_scopes", "label": "Can't find 'User Token Scopes'"},
      {"id": "scope_not_found", "label": "The scope I want to add doesn't appear as an option"},
      {"id": "what_are_scopes", "label": "What are scopes?"}
    ]
  }]
}
```

(scopes_added -> Proceed to Step 3)
(cant_find_oauth -> Guide: "Check the left sidebar menu. 'OAuth & Permissions' is under the 'Features' section. If you can't see the sidebar, try widening your browser window")
(cant_find_scopes -> Guide: "Scroll down the page. The 'Scopes' section is below the 'OAuth Tokens for Your Workspace' section. Look for 'User Token Scopes' within it. Note: this is NOT 'Bot Token Scopes'")
(scope_not_found -> Guide: "Enter the scope name exactly. Typing in the input field filters the suggestions. For example, typing 'channels' will show channels:history and channels:read as options")
(what_are_scopes -> Explain: "Scopes define the range of operations your App is allowed to perform. The 4 we're adding are:\n- channels:history = Permission to read past messages in channels\n- channels:read = Permission to view the channel list\n- chat:write = Permission to post messages as the App\n- users:read = Permission to view workspace member information\nThese are the minimum permissions needed for Slack search and task management features")

---

## Step 3: Install to Workspace

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Install to Workspace",
  "questions": [{
    "id": "install_app",
    "prompt": "Once scope setup is complete, install the App to your workspace:\n\n1. Scroll up to find the 'OAuth Tokens for Your Workspace' section\n2. Click the 'Install to Workspace' button\n   (It's also OK if the button says 'Reinstall to Workspace')\n3. Click 'Allow' on the permission confirmation screen\n4. The 'User OAuth Token' will appear (a string starting with xoxp-)\n5. Click the 'Copy' button to the right of the token\n\nWere you able to copy the User OAuth Token?",
    "options": [
      {"id": "token_copied", "label": "Token copied!"},
      {"id": "no_install_button", "label": "There's no 'Install to Workspace' button"},
      {"id": "allow_denied", "label": "Was denied on the 'Allow' screen"},
      {"id": "no_token", "label": "No token is displayed"}
    ]
  }]
}
```

(token_copied -> Proceed to Step 4)
(no_install_button -> Guide: "The Install button won't appear if no User Token Scopes have been added. Go back to Step 2 and add at least one scope")
(allow_denied -> Guide: "Your workspace admin may have restricted App additions. Ask the admin for approval, or create a test workspace of your own")
(no_token -> Guide: "If installation completed successfully, the 'User OAuth Token' should appear at the top of the 'OAuth & Permissions' page. Reload the page and check the top section")

---

## Step 4: Save Token Securely

**Important security note:**
Do not paste the token in this chat. We'll save it securely in a separate terminal window.

**What the AI auto-runs:**
1. Check whether the `keyring` package is installed
   - If not installed: Auto-run `pip install keyring`
2. Run `uv run python tools/credential_manager.py status` to check the current state

**Message to show the user:**

```text
After copying the token, follow these steps to save it securely:

┌─────────────────────────────────────────────────────────────┐
│ Run the following command in a separate terminal window:    │
│                                                             │
│ Cursor: Ctrl+` (backtick) to open a new terminal           │
│ Claude Code: Open a separate terminal window                │
│                                                             │
│ uv run python tools/credential_manager.py store SLACK_USER_TOKEN    │
│                                                             │
│ -> "Enter value for SLACK_USER_TOKEN:" will appear           │
│ -> Paste the copied User Token and press Enter               │
│   (The text you type won't be shown on screen. This is      │
│    normal)                                                  │
│ -> "Stored SLACK_USER_TOKEN" means it's saved!               │
└─────────────────────────────────────────────────────────────┘

Once saved, come back to this chat and let me know you're "done".
```

**Why run it in a separate window:**
If you handle the token in this AI chat, the value remains in the conversation log.
By running `credential_manager.py` in a separate window, the token value is saved directly to the OS's
encrypted storage (macOS Keychain / Windows Credential Locker / Linux SecretService),
and never appears in plaintext files or chat logs.

**AskQuestion configuration:**
```json
{
  "title": "Step 4: Save the Token",
  "questions": [{
    "id": "store_status",
    "prompt": "Were you able to run the command in a separate terminal?",
    "options": [
      {"id": "done", "label": "Saved!"},
      {"id": "terminal_help", "label": "I don't know how to open a terminal"},
      {"id": "command_error", "label": "The command gave an error"},
      {"id": "credential_store_unavailable", "label": "Credential Store is unavailable (fallback)"},
      {"id": "security_question", "label": "I have a question about security"}
    ]
  }]
}
```

(done -> Proceed to Step 5)
(terminal_help -> Guide: "For Cursor: Menu > Terminal > New Terminal, or press Ctrl+` (Mac: Cmd+`). For Claude Code: Open a separate terminal window/tab. Mac: Cmd+T (new tab) or Cmd+N (new window). Windows: Open your WSL terminal (Ubuntu), or add an Ubuntu tab in Windows Terminal. Then cd to the project directory")
(command_error -> AI runs `uv run python tools/credential_manager.py status` to check the situation and identify the cause. If keyring is not installed, auto-run `pip install keyring`)
(credential_store_unavailable -> Guide: "First, let's check store status with `uv run python tools/credential_manager.py status`". If truly unavailable, provide .env fallback as an exception: guide to enter the token directly into the .env file in a separate terminal, with the note: "Make sure .env is included in .gitignore. Once Credential Store becomes available, migrate with `uv run python tools/credential_manager.py migrate` and clean up with `uv run python tools/credential_manager.py cleanup` to remove the plaintext token from .env")
(security_question -> Explain: "This tool uses your OS's built-in encrypted storage. On macOS it uses Keychain, on Windows it uses Credential Locker, and on Linux it uses SecretService (GNOME Keyring, etc.). No plaintext files (.env) are created. The storage is also locked when your screen is locked, providing protection against physical access")

---

## Step 5: Configuration Test

**What the AI auto-runs:**

1. First run `credential_manager.py status` to check if `SLACK_USER_TOKEN` is saved in the Credential Store:
   - **Note**: Do not display the token value itself in chat. Only show masked output like "Confirmed token is set (xoxp-****...)"
   - Status check command: `uv run python tools/credential_manager.py status`

2. If the basic check passes, send an actual test request to the Slack API:
   - Inject from Credential Store to environment variables and execute the API call
   - Test code example:
     ```python
     import os, sys, requests
     try:
         from tools.credential_manager import inject_to_environ
         inject_to_environ()
     except ImportError:
         pass
     token = os.getenv("SLACK_USER_TOKEN")
     if not token or token == "xoxp-your-user-token":
         print("Error: SLACK_USER_TOKEN is not set.")
         sys.exit(1)
     resp = requests.post(
         "https://slack.com/api/auth.test",
         headers={"Authorization": f"Bearer {token}"}
     ).json()
     if resp.get("ok"):
         print(f"Connection successful! Workspace: {resp['team']} / Bot name: {resp['user']}")
     else:
         print(f"Error: {resp.get('error', 'Unknown error')}")
     ```
   - Auto-install any missing packages (`requests`, `keyring`)

3. Display messages based on test results:

**On test success:**
```text
Slack API setup is complete!

Test results:
  Workspace: [workspace name]
  Bot name: [bot name]
  Connection: Normal

You can now use Slack search (/start-9-1) and Slack task management (/start-9-2).
```

**AskQuestion on test failure:**
```json
{
  "title": "Test result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the Slack API test. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Try the test again"},
      {"id": "recheck_token", "label": "Re-check the token (go back to Step 3)"},
      {"id": "show_error", "label": "I want to see error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(recheck_token -> Go back to Step 3)
(show_error -> Display error message with cause and solution. Common errors: `invalid_auth` = token is invalid, `token_revoked` = token was revoked, `not_authed` = token not set)
(skip_test -> Guide: "API test skipped. You can check later with /check-setup")

---

## Supplementary: Invite Bot to a Channel

**After a successful test, AI provides the following guidance:**

For the Slack App to read messages, the Bot must be invited to the target channel.

**Steps (performed in the Slack app):**
1. Open the Slack app
2. Navigate to the channel where you want to read messages
3. Click the channel name to open settings
4. Click the "Integrations" tab
5. Click "Add an App"
6. Select "AIAgent Bootcamp" and add it

Alternatively, you can also send the message `/invite @AIAgent Bootcamp` in the channel.

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
      {"id": "trouble_invalid", "label": "Getting an 'invalid_auth' error"},
      {"id": "trouble_missing_scope", "label": "Getting a 'missing_scope' error"},
      {"id": "trouble_not_in_channel", "label": "Getting a 'not_in_channel' error"},
      {"id": "trouble_admin", "label": "Told admin approval is needed"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Issue 1: "invalid_auth" error
**Cause**: User Token was not copied correctly, or is invalid
**What the AI does**:
1. Check Credential Store state with `uv run python tools/credential_manager.py status` (only report whether it starts with `xoxp-`, do not display the value)
2. Auto-check for extra spaces, newlines, or quotation marks
3. If an issue is found, suggest re-saving. If not, guide: "Please regenerate the token from the Slack App settings page"

### Issue 2: "missing_scope" error
**Cause**: Required User Token Scope has not been added
**AI guidance**: "In the Slack App settings page, go to 'OAuth & Permissions' -> 'User Token Scopes' and verify all these scopes are added: channels:history, channels:read, chat:write, users:read. After adding scopes, you need to click 'Reinstall to Workspace' to reinstall"

### Issue 3: "not_in_channel" error
**Cause**: Bot has not been invited to the target channel
**AI guidance**: "Open the target channel in the Slack app, click the channel name -> 'Integrations' -> 'Add an App' and add 'AIAgent Bootcamp'"

### Issue 4: Admin approval required
**Cause**: Workspace settings restrict App additions
**AI guidance**: "Ask your workspace admin to approve the Slack App addition. If you need it urgently, you can create a free test workspace at https://slack.com/create to practice"

### Issue 5: Other errors
**What the AI does**: Check the error message content and cross-reference with Slack API error codes to provide the cause and solution

---

## Checkpoint
- [ ] Created the "AIAgent Bootcamp" Slack App
- [ ] Added 4 scopes to User Token Scopes (channels:history, channels:read, chat:write, users:read)
- [ ] Installed the App to the workspace
- [ ] SLACK_USER_TOKEN is saved in the Credential Store (check with `uv run python tools/credential_manager.py status`)
- [ ] API test succeeded (workspace name and bot name displayed)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Slack API setup is complete! What would you like to do next?",
    "options": [
      {"id": "setup_gemini", "label": "Set up Gemini API too (/setup-gemini)"},
      {"id": "try_slack_search", "label": "Try Slack search (/start-9-1)"},
      {"id": "try_slack_task", "label": "Try Slack task management (/start-9-2)"},
      {"id": "back_to_setup", "label": "Back to setup list"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- setup_gemini -> Guide to /setup-gemini
- try_slack_search -> Guide to /start-9-1
- try_slack_task -> Guide to /start-9-2
- back_to_setup -> Show setup lesson list
- finish -> End

---

## Completion Processing

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-slack` to update progress
2. Updated progress summary is automatically displayed
3. Guide the user to the next step: "Next, let's install extensions with `/setup-extensions`"

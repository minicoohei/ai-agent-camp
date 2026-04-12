---
description: "Vercel CLI Setup (with complete guide)"
duration: "~10 min"
prerequisites: ["Node.js 18 or higher installed", "Browser available"]
level: "beginner"
tags: ["setup", "vercel", "deploy", "hosting"]
---

# Vercel CLI Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-vercel` to display progress
2. Auto-detect existing installation state:
   - Run `vercel --version` to check if the CLI is installed
   - Run `vercel whoami` to check if already logged in
   - If both succeed, skip to Step 4 (test)
3. **This setup is optional.** Vercel CLI is used in Lesson 15-5 (LP Production - Vercel Deploy). You can skip it if you don't need it right away.

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Install Vercel CLI, log in, and get ready to deploy and publish websites |
| Duration | ~10 minutes |
| Prerequisites | Node.js 18 or higher installed, browser available |
| Skill Level | CLI command input required (installation is AI auto-run + browser authentication) |
| Pricing | Free plan (Hobby) with unlimited personal projects. The free tier is sufficient for training |

**Session flow:**
1. Create a Vercel account (sign up in browser)
2. Install Vercel CLI (AI auto-runs)
3. Log in to Vercel (browser authentication or token authentication)
4. Operation test (AI auto-runs)

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

---

## Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready? (This setup is optional. Used in Lesson 15-5)",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "chrome", "label": "Automate browser operations with /chrome"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "skip", "label": "I don't need this now, skip"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(chrome -> After opening the browser in Step 1, follow the "Chrome integration automation" section)
(check_prereq -> Guide: "Node.js 18 or higher is required. You can check with `node --version`")
(skip -> Guide: "Skipped. You can set it up again later with `/setup-vercel` when needed" and end)
(different_lesson -> Show module list)

---

## Step 1: Create Vercel Account

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to auto-launch the browser:

```bash
# Mac:
open https://vercel.com/signup
# Windows:
start https://vercel.com/signup
# Linux:
xdg-open https://vercel.com/signup
```

**Once the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Create Vercel Account",
  "questions": [{
    "id": "account_status",
    "prompt": "Did the browser open? Follow these steps to create an account:\n\n1. Click 'Continue with GitHub' (recommended)\n   - You can sign up directly with your GitHub account\n   - Or choose 'Continue with GitLab' or 'Continue with Email'\n2. Complete authentication / email verification\n3. Account creation is complete\n\nPlease tell me your account status:",
    "options": [
      {"id": "created", "label": "Account created!"},
      {"id": "already_have", "label": "I already have an account"},
      {"id": "no_github", "label": "I don't have a GitHub account"},
      {"id": "browser_not_open", "label": "The browser didn't open"}
    ]
  }]
}
```

(created -> Proceed to Step 2)
(already_have -> Proceed to Step 2)
(no_github -> Guide: "You can also sign up with Email. Select 'Continue with Email' on the signup page. Or you can also first create a GitHub account with `/setup-github`")
(browser_not_open -> Guide: "Please open this URL directly in your browser: https://vercel.com/signup")

---

## Chrome Integration Automation (`/chrome` mode)

**Prerequisites:** The "Claude in Chrome" extension (v1.0.36+) is installed in Chrome, and you launched with `claude --chrome` or ran `/chrome` within the session.

**What the AI auto-runs via Chrome integration:**
1. Open https://vercel.com/signup in the browser
2. Use Chrome integration to perform:
   - Click "Continue with GitHub"
   - If the GitHub authentication screen appears, prompt the user to approve
3. After signup is confirmed, proceed to Step 2

If Chrome integration is not available, follow the manual steps in Step 1.

---

## Step 2: Install Vercel CLI

**What the AI auto-runs:**
1. Check the Node.js version:
   ```bash
   node --version
   ```
   - If below Node.js 18: Guide "Node.js 18 or higher is required. Please set up with `/start-0-1`" and stop
2. Install the Vercel CLI:
   ```bash
   npm i -g vercel
   ```
   - On permission error (`EACCES`): Guide `sudo npm i -g vercel`
3. Verify installation:
   ```bash
   vercel --version
   ```

**On installation success:**
```text
Vercel CLI has been installed! (Version: XX.X.X)
Next, we'll log in to your Vercel account.
```

**AskQuestion on installation failure:**
```json
{
  "title": "Installation error occurred",
  "questions": [{
    "id": "install_error",
    "prompt": "An error occurred while installing Vercel CLI.",
    "options": [
      {"id": "retry", "label": "Try again"},
      {"id": "sudo", "label": "Try with admin privileges (sudo)"},
      {"id": "show_error", "label": "I want to see error details"},
      {"id": "skip", "label": "Skip and try later"}
    ]
  }]
}
```

(retry -> Re-run `npm i -g vercel`)
(sudo -> Run `sudo npm i -g vercel`)
(show_error -> Display error message with cause and solution)
(skip -> Guide: "Skipped. You can set it up again later with `/setup-vercel`")

---

## Step 3: Vercel Login

**Guide that there are two methods: Method A (interactive environment, recommended) and Method B (non-interactive environment, token authentication).**

**What the AI does:**
1. First try Method A: Run `vercel login`
2. The browser opens automatically and authenticate with Vercel account
3. If "Congratulations!" appears in the terminal, login is complete

**Message to show the user:**

```text
We'll log in to Vercel.

┌─────────────────────────────────────────────────────────────┐
│ Method A (recommended): Browser authentication              │
│                                                             │
│ Running `vercel login` will open your browser.              │
│ Authenticate with your Vercel account to complete.          │
│                                                             │
│ Method B (non-interactive environments): Token auth         │
│                                                             │
│ For CI/CD or when a browser isn't available:                │
│ 1. Create a token at https://vercel.com/account/tokens      │
│ 2. In a separate terminal, run:                             │
│    uv run python tools/credential_manager.py store VERCEL_TOKEN    │
│ 3. Use the --token option when deploying                    │
└─────────────────────────────────────────────────────────────┘
```

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Vercel Login",
  "questions": [{
    "id": "login_status",
    "prompt": "`vercel login` has been run. What's the result?",
    "options": [
      {"id": "done", "label": "Logged in (Congratulations! appeared)"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "non_interactive", "label": "I'm in a non-interactive environment (want token auth)"}
    ]
  }]
}
```

(done -> Proceed to Step 4)
(browser_not_open -> Guide: "If the browser doesn't open, copy the URL displayed in the terminal and paste it into your browser manually. If that still doesn't work, try Method B (token authentication)")
(non_interactive -> Guide through the token authentication flow below)

### Method B: Token Authentication (for non-interactive environments)

**What the AI does:**
1. Open the token creation page in the browser:
   ```bash
   # Mac:
   open https://vercel.com/account/tokens
   # Windows:
   start https://vercel.com/account/tokens
   # Linux:
   xdg-open https://vercel.com/account/tokens
   ```

**Message to show the user:**

```text
We'll set up with token authentication.

┌─────────────────────────────────────────────────────────────┐
│ Follow these steps in a separate terminal window:           │
│                                                             │
│ 1. Open https://vercel.com/account/tokens in browser        │
│ 2. Click the "Create" button to create a token              │
│ 3. Copy the token                                           │
│ 4. In a separate terminal, run:                             │
│                                                             │
│    uv run python tools/credential_manager.py store VERCEL_TOKEN    │
│                                                             │
│ -> "Enter value for VERCEL_TOKEN:" will appear              │
│ -> Paste the copied token and press Enter                   │
│   (The text you type won't be shown on screen. This is      │
│    normal)                                                  │
│ -> "Stored VERCEL_TOKEN" means it's saved!                  │
└─────────────────────────────────────────────────────────────┘

Once saved, come back to this chat and let me know you're "done".
```

**AskQuestion for token storage:**
```json
{
  "title": "Token Authentication",
  "questions": [{
    "id": "token_status",
    "prompt": "Were you able to save the token in a separate terminal?",
    "options": [
      {"id": "done", "label": "Saved!"},
      {"id": "terminal_help", "label": "I don't know how to open a terminal"},
      {"id": "command_error", "label": "The command gave an error"}
    ]
  }]
}
```

(done -> Proceed to Step 4)
(terminal_help -> Guide: "For Cursor: Menu > Terminal > New Terminal, or press Ctrl+` (Mac: Cmd+`). For Claude Code: Open a separate terminal window/tab. Mac: Cmd+T (new tab) or Cmd+N (new window). Windows: Open PowerShell or Windows Terminal from the Start Menu, or Ctrl+Shift+T for a new tab. Then cd to the project directory")
(command_error -> AI runs `uv run python tools/credential_manager.py status` to check the situation and identify the cause. If keyring is not installed, auto-run `pip install keyring`)

---

## Step 4: Test

**What the AI auto-runs:**

1. Run tests based on the login method:
   - **Method A (browser auth)**: Run `vercel whoami` -- success if username appears
   - **Method B (token auth)**: First check if `VERCEL_TOKEN` is saved with `uv run python tools/credential_manager.py status`, then retrieve the token from credential_manager and verify with `vercel whoami --token <TOKEN>`

**On test success:**
```text
Vercel CLI setup is complete!

Test result: Confirmed login username "xxxxx".
You can now deploy and publish websites.
```

**AskQuestion on test failure:**
```json
{
  "title": "Test result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred with `vercel whoami`. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Try the test again"},
      {"id": "relogin", "label": "Log in again (go back to Step 3)"},
      {"id": "show_error", "label": "I want to see error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(relogin -> Go back to Step 3)
(show_error -> Display error message with cause and solution)
(skip_test -> Guide: "Test skipped. You can check later with `/check-setup`")

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
      {"id": "trouble_permission", "label": "npm permission error (EACCES)"},
      {"id": "trouble_notfound", "label": "'vercel: command not found'"},
      {"id": "trouble_browser", "label": "Browser authentication fails"},
      {"id": "trouble_node", "label": "Node.js version is too old"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Issue 1: npm permission error (EACCES)
**Cause**: Admin privileges needed for global installation
**What the AI does**:
1. Guide `sudo npm i -g vercel`
2. If that doesn't work, guide changing the install directory with `npm config set prefix ~/.npm-global` and adding `~/.npm-global/bin` to PATH

### Issue 2: "vercel: command not found"
**Cause**: PATH not set, or incomplete installation
**What the AI does**:
1. Check installation location with `which vercel` or `npm list -g vercel`
2. If PATH needs to be added, guide adding to shell config (`.zshrc` / `.bashrc`)
3. Restart the terminal or run `source ~/.zshrc`

### Issue 3: Browser authentication fails
**Cause**: Communication error between browser and CLI, or firewall
**AI guidance**: "Try running `vercel login` again. If the browser doesn't open, copy the URL displayed in the terminal and paste it into your browser manually. If that still doesn't work, try Method B (token authentication)"

### Issue 4: Node.js version is too old
**Cause**: Node.js below version 18 is installed
**What the AI does**:
1. Check current version with `node --version`
2. Guide upgrading to Node.js 18 or higher (`nvm install 18` or download from the official site)

### Issue 5: Other errors
**What the AI does**: Check the error message content, identify the cause, and guide the solution

---

## Checkpoint
- [ ] Created a Vercel account
- [ ] Vercel CLI is installed (vercel --version)
- [ ] Logged in to Vercel (vercel whoami)
- [ ] Test succeeded (username displayed)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Vercel CLI setup is complete! What would you like to do next?",
    "options": [
      {"id": "try_deploy", "label": "Try LP production and deploy (/start-15-5)"},
      {"id": "back_to_setup", "label": "Back to setup list (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- try_deploy -> Guide to /start-15-5
- back_to_setup -> Guide to /start-0-1
- finish -> End

---

## Completion Processing

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-vercel` to update progress
2. Updated progress summary is automatically displayed
3. Guide the user to the next step: "Next, let's try LP production and Vercel deploy with `/start-15-5`"

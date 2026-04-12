---
description: "GitHub Account Setup and Repository Creation"
duration: "~10 min"
prerequisites: ["/setup-start completed"]
level: "beginner"
tags: ["setup", "github"]
---

# GitHub Account Setup and Repository Creation

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-github` to display progress
2. Check if already logged in with `gh auth status`. If logged in, display "GitHub authentication is complete."
3. Check if a personal repo already exists with `git remote -v`. If it exists, confirm "Repository is also configured. Do you want to skip?"

## What You'll Do in This Session

**Welcome to GitHub Account Setup!**

| Item | Details |
|------|---------|
| Goal | Log in to GitHub and create your own private repository |
| Duration | ~10 minutes (15 minutes if account creation is needed) |
| Skills Used | None (the AI handles everything automatically) |
| Prerequisites | `/setup-start` completed (Python / Node.js / Git / GitHub CLI are installed) |
| Next Command | `/start-0-1` (Environment setup check) |

**Session flow:**
1. Verify your GitHub account
2. GitHub authentication (just click "Allow" in the browser)
3. Create your personal repository

> **Important**: You don't need to type any commands in the terminal. The AI handles everything behind the scenes. When the browser opens, just follow the on-screen instructions.
> **Security note**: Do not paste passwords or tokens in the chat. All authentication is done securely through the browser.
> **Hint**: If the AI's response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a bug.
>
> **Note for Codex**: In Codex, rather than running `/setup-github` directly, follow the verification steps in this document and proceed through `gh auth` sequentially. Only the browser login and authorization button clicks are done by the user.

---

## Pre-session Confirmation

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
      {"id": "check_prereq", "label": "I haven't done /setup-start yet"},
      {"id": "what_is_github", "label": "What is GitHub?"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(chrome -> When account creation is needed in Step 1, after opening the browser, follow the "Automating with Chrome integration" section for automatic execution)
(check_prereq -> Guide: "Please run /setup-start first. It will check that the required software is installed.")
(what_is_github -> Guide: "GitHub is a cloud service for safely storing and managing programs and files. Think of it as the programmer's version of Google Drive. In this training, we'll use it to save your work. It's free to use." -> Proceed to Step 1)

---

## Step 1: Verify Your GitHub Account

**AskQuestion configuration:**
```json
{
  "title": "Step 1: GitHub Account Verification",
  "questions": [{
    "id": "has_account",
    "prompt": "Do you have a GitHub account?",
    "options": [
      {"id": "yes", "label": "Yes, I have one"},
      {"id": "no", "label": "No (I want to create one)"},
      {"id": "not_sure", "label": "I'm not sure"}
    ]
  }]
}
```

### If you have an account (yes)

-> Proceed to Step 2

### If you don't have an account (no)

**What the AI auto-runs:**
First, run `uname -s` to detect the OS (if already detected in Step 1, use that result).

Display:
```text
Let's create a GitHub account.
The AI will open the browser automatically. Please wait a moment...
```

```bash
# AI runs:
# Mac:
open https://github.com/signup
# Windows:
start https://github.com/signup
```

**Account creation instructions:**
```text
Once the browser opens, follow these steps:

1. Enter your email address and click "Continue"
2. Set a password and click "Continue"
   (Use a password with 8+ characters, including numbers or symbols)
3. Choose a username and click "Continue"
   (Only half-width alphanumeric characters and hyphens. Example: taro-yamada)
4. Choose your email notification preference and click "Continue"
5. Solve the puzzle verification and click "Create account"
6. A confirmation code will be sent to your registered email
7. Enter the 6-digit code from the email

Once account creation is complete, type "done" here.
```

### Automating with Chrome Integration (`/chrome` mode, for new account creation only)

**Prerequisite:** The "Claude in Chrome" extension (v1.0.36+) must be installed in Chrome, and you must have launched with `claude --chrome` or run `/chrome` in the session.

**What the AI auto-runs with Chrome integration:**
1. Open https://github.com/signup in the browser
2. Use Chrome integration to perform the following operations in order:
   - Focus on the email input field and prompt the user to enter their email
   - Click "Continue"
   - Click "Continue" after password entry
   - Click "Continue" after username entry
   - Click "Continue" after email notification settings
   - Leave the puzzle verification to the user
   - Click "Create account"
3. Email confirmation code entry is done manually by the user
4. After account creation is complete, proceed to Step 2

**Note:** Do not read password or email values from the browser screen.

If Chrome integration is not available, follow the steps above manually.

**AskQuestion configuration (completion check):**
```json
{
  "title": "Account creation confirmation",
  "questions": [{
    "id": "account_created",
    "prompt": "Is the GitHub account creation complete?",
    "options": [
      {"id": "done", "label": "Done!"},
      {"id": "stuck", "label": "I got stuck partway"},
      {"id": "browser_not_open", "label": "The browser didn't open"}
    ]
  }]
}
```

(done -> Proceed to Step 2)
(stuck -> "Which screen are you on? Please tell me what's displayed on your screen." and assist)
(browser_not_open -> Guide: "Open your browser and type https://github.com/signup in the address bar.")

### If not sure (not_sure)

Display:
```text
Let's check. Do either of the following ring a bell?
- You received a registration confirmation email from GitHub
- You can log in at https://github.com

If you're not sure, it's fine to create a new one.
```

**AskQuestion configuration:**
```json
{
  "title": "Account verification",
  "questions": [{
    "id": "account_check",
    "prompt": "What would you like to do?",
    "options": [
      {"id": "try_login", "label": "Try logging in (open browser)"},
      {"id": "create_new", "label": "Create a new one"}
    ]
  }]
}
```

(try_login -> AI runs `open https://github.com/login` / `start https://github.com/login` to open browser -> If login succeeds, proceed to Step 2; if not, go to the new account creation flow)
(create_new -> Go to "If you don't have an account" flow above)

---

## Step 2: GitHub Authentication

**What the AI auto-runs:**

### 2-1. Check Existing Authentication

First, run `gh auth status` to check if already logged in.

**If already logged in:**
```text
You are logged in to GitHub as {username}.
```
-> Proceed to Step 3

**If not logged in:**

### 2-2. Start Browser Authentication

Display:
```text
Logging in to GitHub.
The AI will open the browser automatically. Follow these steps:
```

```bash
AI runs: gh auth login --web -p https
```

This command has two possible results:

**Pattern A: Browser opens automatically**
```text
The browser opened automatically.
Click the green "Authorize GitHub CLI" button on the screen.
The result will automatically appear in this chat when done.
```

**Pattern B: An 8-digit code is displayed**

Read the 8-digit code (e.g., `XXXX-XXXX`) from the command output and guide:
```text
An authentication page has opened in the browser.
Enter the following code on the screen:

    XXXX-XXXX

(Enter this code exactly as shown)

Steps:
1. An 8-digit input field is displayed in the browser
2. Enter the code above and click "Continue"
3. Click the green "Authorize GitHub CLI" button
4. The result will automatically appear in this chat when done
```

If the browser doesn't open:
```text
If the browser didn't open, open the following URL in your browser:
https://github.com/login/device

Then enter the code above.
```

### 2-3. Verify Authentication Result

AI runs `gh auth status` to check the result.

**If authentication succeeded:**
```text
Authentication successful! You are now logged in to GitHub as {username}.
```
-> Proceed to Step 3

**If authentication failed:**

**AskQuestion configuration:**
```json
{
  "title": "Authentication problem occurred",
  "questions": [{
    "id": "auth_trouble",
    "prompt": "Authentication didn't seem to work. Please tell me your situation.",
    "options": [
      {"id": "retry", "label": "Try again"},
      {"id": "browser_issue", "label": "The browser didn't open"},
      {"id": "code_expired", "label": "The code entry screen disappeared"},
      {"id": "other_error", "label": "An error message was displayed"}
    ]
  }]
}
```

(retry -> Re-run `gh auth login --web -p https`)
(browser_issue -> Guide: "Open your browser and go to https://github.com/login/device" and re-display the code)
(code_expired -> "The code may have expired. Running again." -> Re-run `gh auth login --web -p https`)
(other_error -> "Please tell me the error message displayed." and assist)

---

## Step 3: Create Your Personal Repository

**What the AI auto-runs:**

### 3-1. Check Current State

AI runs the following in order:
1. Get the login username from `gh auth status`
2. Check current remote settings with `git remote -v`

### 3-2. Actions Based on State

**Case A: Personal repository is already configured**
(The origin URL in `git remote -v` contains the login username)

Display:
```text
Your personal repository is already configured.
  Repository: https://github.com/{username}/ai-agent-camp

No issues. Let's proceed to the next step.
```
-> Go to Completion section

**Case B: origin is still set to minicoohei/ai-agent-camp (the course distribution source)**

Display:
```text
The current settings point to the course distribution repository.
We'll create your personal private repository.
```

**AskQuestion configuration:**
```json
{
  "title": "Create personal repository",
  "questions": [{
    "id": "create_repo",
    "prompt": "We'll create a private repository named {username}/ai-agent-camp for you. Is that OK?",
    "options": [
      {"id": "yes", "label": "Create it"},
      {"id": "different_name", "label": "I want a different name"},
      {"id": "explain", "label": "What is a repository?"}
    ]
  }]
}
```

(yes -> Execute repository creation)
(different_name -> "What name would you like? You can use half-width alphanumeric characters and hyphens." and accept input)
(explain -> "A repository is a storage location for files. Think of it like a Google Drive folder. It will be set to private, so only you can access it." -> Re-display the AskQuestion)

**Execute repository creation:**

AI runs the following in order:

1. Rename existing origin to upstream (keep as the course distribution source):
   ```bash
   git remote rename origin upstream
   ```
   (Skip if upstream already exists)

2. Create personal repository and set as origin:
   ```bash
   gh repo create {username}/ai-agent-camp --private --source . --remote origin --push
   ```

3. Verify the result:
   ```bash
   git remote -v
   ```

**On success:**
```text
Your personal private repository has been created!

  Repository URL: https://github.com/{username}/ai-agent-camp
  Visibility: private (only you can access it)

Your training deliverables will now be safely saved.
```
-> Go to Completion section

**On failure:**

AI analyzes the error message and identifies the cause:

- "already exists" -> A repository with the same name already exists:
  ```text
  A repository with the same name already exists.
  ```
  **AskQuestion configuration:**
  ```json
  {
    "title": "Repository already exists",
    "questions": [{
      "id": "repo_exists",
      "prompt": "A repository with the same name was found. What would you like to do?",
      "options": [
        {"id": "use_existing", "label": "Use the existing repository"},
        {"id": "different_name", "label": "Create with a different name"}
      ]
    }]
  }
  ```
  (use_existing -> AI runs `git remote add origin https://github.com/{username}/ai-agent-camp.git` and `git push -u origin main`)
  (different_name -> "What name would you like?" and accept input, then re-run with that name)

- "permission denied" -> Authentication issue:
  -> Go back to Step 2 authentication flow

- Other errors -> Display error content and ask "Please tell me what's displayed on your screen." to assist

**Case C: No origin exists**
(Nothing is displayed by `git remote -v`)

Display:
```text
No remote repository is configured.
We'll create a new private repository for you.
```
-> Execute the same "Execute repository creation" steps as Case B (but skip step 1 rename)

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
      {"id": "trouble_1", "label": "The browser doesn't open"},
      {"id": "trouble_2", "label": "There's no screen to enter the authentication code"},
      {"id": "trouble_3", "label": "I get an error creating the repository"},
      {"id": "trouble_4", "label": "I forgot my GitHub password"},
      {"id": "trouble_5", "label": "Other trouble"}
    ]
  }]
}
```

### Trouble 1: "Browser Doesn't Open"
**Cause**: Default browser settings, or security software blocking
**Solution**:
```text
Open the browser manually and go to one of these URLs:
- Account creation: https://github.com/signup
- Login: https://github.com/login
- Device authentication: https://github.com/login/device
```

### Trouble 2: "No Screen to Enter Authentication Code"
**Cause**: Opened in another browser tab, or popup blocker
**Solution**:
```text
1. Check your browser tabs (a new tab may have been opened)
2. If not found, open https://github.com/login/device in your browser
3. Enter the displayed code
```

### Trouble 3: "Error Creating Repository"
**Cause**: Expired authentication, network issues, or insufficient permissions
**Solution**:
AI runs `gh auth status` to check authentication state.
- Expired authentication -> Go back to Step 2 authentication flow
- Network issue -> Guide to check internet connection
- Insufficient permissions -> Run `gh auth refresh -s repo` to update permissions

### Trouble 4: "Forgot GitHub Password"
**Solution**:
```text
The AI will open the password reset page.
```
```bash
# AI runs:
# Mac:
open https://github.com/password_reset
# Windows:
start https://github.com/password_reset
```

```text
1. Enter your email address and click "Send password reset email"
2. Click the link in the email that arrives
3. Set a new password
4. Once done, type "done" here
```

### Trouble 5: "Other Trouble"
**Solution**:
```text
What kind of problem are you experiencing? Please tell me the error message or the situation on your screen.
The AI will diagnose the cause and suggest a solution.
```

---

## Checkpoint

AI auto-checks all items and displays results:

| Item | Check Command | Expected Result |
|------|--------------|----------------|
| GitHub authentication | `gh auth status` | Login username is displayed |
| Remote repository | `git remote -v` | origin points to your repository |
| Push state | `git log --oneline -1` | Latest commit exists |

---

## Completion

```text
Congratulations! GitHub setup is complete!

  GitHub username: {username}
  Repository URL: https://github.com/{username}/ai-agent-camp
  Visibility: private (only you can access it)

You're now ready to start the training.
```

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_lesson", "label": "Start the training (/start-0-1)"},
      {"id": "view_repo", "label": "View the created repository in the browser"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(next_lesson -> Guide: "Open a new chat and type /start-0-1")
(view_repo -> AI runs `open https://github.com/{username}/ai-agent-camp` / `start https://github.com/{username}/ai-agent-camp` to show in browser -> Then guide: "To start the training, open a new chat and type /start-0-1")
(finish -> Guide: "Great work! When you're ready to start the training, type /start-0-1.")

---

## Completion Processing

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-github` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "Next, set up the Gemini API with `/setup-gemini`"

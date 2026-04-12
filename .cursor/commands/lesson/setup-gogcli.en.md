---
description: "gogcli (Google Workspace CLI) Setup (Complete Guide)"
duration: "~15 min"
prerequisites: ["Have a Google account", "Browser available"]
level: "beginner"
tags: ["setup", "gogcli", "google", "gmail", "calendar", "oauth"]
---

# gogcli (Google Workspace CLI) Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-gogcli` to display progress
2. Auto-detect existing installation and authentication:
   - Run `which gog` or `gog --version`
   - If gogcli is already installed, check authentication status with `gog auth list`
   - If installed and authenticated, skip to Step 4 (functionality test)

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Install gogcli and complete Google OAuth authentication so you can access Gmail/Calendar/Drive/Sheets from the CLI |
| Duration | ~15 minutes |
| Prerequisites | Have a Google account, browser available |
| Skill Level | No CLI commands needed (everything is auto-run by AI + browser OAuth authentication only) |

**Session flow:**
1. Install gogcli (AI auto-detects OS and installs)
2. Perform Google OAuth authentication (AI runs the command, you log in via browser)
3. Verify the authenticated account (AI auto-runs)
4. Gmail/Calendar functionality test (AI auto-runs)

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
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(check_prereq -> Guide: "You're ready if you can log in to a browser with a Google account. gogcli is free to use and operates within Google Workspace API free tier limits.")
(different_lesson -> Display module list)

---

## Step 1: Install gogcli

**What the AI does:**
1. Auto-detect the OS (Mac / Linux)
2. Check if already installed: `which gog`
3. If not installed, run the following commands:

```bash
# Mac (Homebrew recommended):
brew install nicholasgasior/tools/gog

# Mac alternative (if Go is installed):
go install github.com/nicholasgasior/gog@latest

# Linux (Go required):
go install github.com/nicholasgasior/gog@latest
```

4. After installation, verify with `gog --version`

**Installation method decision logic:**
- `which brew` succeeds -> Install via Homebrew
- `which go` succeeds -> Install via `go install`
- Neither available -> Guide through Homebrew installation first

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Install gogcli",
  "questions": [{
    "id": "install_status",
    "prompt": "The gogcli installation has been run. Please check the result.",
    "options": [
      {"id": "installed", "label": "Installed successfully!"},
      {"id": "brew_error", "label": "I got an error with brew install"},
      {"id": "go_error", "label": "I got an error with go install"},
      {"id": "no_brew_no_go", "label": "Neither Homebrew nor Go is installed"},
      {"id": "command_not_found", "label": "The gog command is not found"}
    ]
  }]
}
```

(installed -> Proceed to Step 2)
(brew_error -> Run `brew update && brew tap nicholasgasior/tools` then retry. If it still fails, guide to `go install`)
(go_error -> Check Go version with `go version`. Go 1.21 or higher is required. If not installed, guide to `brew install go`)
(no_brew_no_go -> Guide: "Let's install Homebrew first. Open https://brew.sh in your browser and copy/run the installation command.")
(command_not_found -> Guide through adding `export PATH=$PATH:$(go env GOPATH)/bin` to shell configuration. For Homebrew, run `brew link gog`)

---

## Step 2: Google OAuth Authentication

**What the AI does:**
1. Run `gog auth add`
2. The browser opens automatically and displays the Google OAuth authentication screen

**Message to display to the user:**

```text
Starting Google OAuth authentication.

+-------------------------------------------------------------+
| The browser will open automatically. Follow these steps to   |
| authenticate:                                                |
|                                                              |
| 1. Select your Google account in the browser (or log in)     |
| 2. On the "Allow this app?" screen, click "Allow"            |
| 3. When "Authorization successful" appears, auth is complete |
| 4. Return to the terminal                                    |
|                                                              |
| * Credentials are securely stored in ~/.config/gogcli/       |
| * No manual API key entry needed (managed via OAuth)         |
+-------------------------------------------------------------+
```

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Google OAuth Authentication",
  "questions": [{
    "id": "auth_status",
    "prompt": "Please authenticate your Google account in the browser. Were you able to authenticate?",
    "options": [
      {"id": "authenticated", "label": "Authenticated!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "auth_error", "label": "I got an authentication error"},
      {"id": "account_help", "label": "I don't know which Google account to choose"},
      {"id": "access_denied", "label": "I see 'access denied'"}
    ]
  }]
}
```

(authenticated -> Proceed to Step 3)
(browser_not_open -> Guide: "Copy the URL displayed in the terminal and paste it manually into your browser.")
(auth_error -> Re-run `gog auth add`. Check the error message to identify the cause)
(account_help -> Guide: "Select the Google account you normally use with Gmail. A company Google Workspace account or a personal Gmail account both work. You can add another account later.")
(access_denied -> Guide: "Your organization's Google Workspace may restrict access to external apps. Check with your IT administrator, or try using a personal Gmail account.")

---

## Step 3: Account Verification

**What the AI auto-runs:**
1. Run `gog auth list` to display the list of authenticated accounts
2. Verify that the correct Google account is shown

**Verification AskQuestion:**
```json
{
  "title": "Step 3: Account Verification",
  "questions": [{
    "id": "account_check",
    "prompt": "The authenticated account is displayed. Is it the correct account?",
    "options": [
      {"id": "correct", "label": "That's the correct account!"},
      {"id": "wrong_account", "label": "I want to use a different account"},
      {"id": "no_account", "label": "No account is displayed"}
    ]
  }]
}
```

(correct -> Proceed to Step 4)
(wrong_account -> Guide through adding a different account with `gog auth add`)
(no_account -> Go back to Step 2 and redo OAuth authentication)

---

## Step 4: Functionality Test

**What the AI auto-runs:**

1. Get the authenticated account email address with `gog auth list`
2. Run a Gmail search test:
   ```bash
   gog gmail search "newer_than:1d" --account <email>
   ```
3. Run a Calendar retrieval test:
   ```bash
   gog calendar list --account <email> --days 1
   ```

**On success:**
```text
gogcli setup is complete!

Test results:
- Gmail search: Working correctly
- Calendar retrieval: Working correctly

You can now access Gmail/Calendar/Drive/Sheets from the CLI.
```

**On failure - AskQuestion:**
```json
{
  "title": "Test Result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the functionality test. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Run the test again"},
      {"id": "reauth", "label": "Redo OAuth authentication (go back to Step 2)"},
      {"id": "show_error", "label": "I want to see the error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(reauth -> Go back to Step 2)
(show_error -> Display the error message and guide on the cause and solution)
(skip_test -> Guide: "The functionality test was skipped. You can check later with /check-setup.")

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
      {"id": "trouble_brew", "label": "I get an error with brew install"},
      {"id": "trouble_auth", "label": "OAuth authentication fails"},
      {"id": "trouble_org", "label": "My organization's Google account has restrictions"},
      {"id": "trouble_access", "label": "I get an 'access denied' error"},
      {"id": "trouble_not_found", "label": "The gog command is not found"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Trouble 1: Error with brew install
**Cause**: The Homebrew tap is not registered, or Homebrew is outdated
**What the AI does**:
1. Run `brew update`
2. Run `brew tap nicholasgasior/tools`
3. Retry `brew install nicholasgasior/tools/gog`
4. If it still fails, guide to the `go install` alternative

### Trouble 2: OAuth Authentication Fails
**Cause**: Browser popup blocker, or network issues
**What the AI does**:
1. Guide on manually pasting the URL displayed in the terminal into the browser
2. Re-run `gog auth add`
3. Guide on checking browser popup blocker settings

### Trouble 3: Organization's Google Account Has Restrictions
**Cause**: The Google Workspace admin has restricted access to external apps
**AI guidance**: "Check with your organization's IT administrator about permission to use gogcli. If that's not possible, try authenticating with a personal Gmail account (@gmail.com). You can add another account with `gog auth add`."

### Trouble 4: "access denied" Error
**Cause**: Insufficient OAuth scope permissions, or account security settings
**What the AI does**:
1. Check authentication status with `gog auth list`
2. Guide to remove and re-authenticate: `gog auth remove <email>` then `gog auth add`
3. Guide on checking Google account security settings (https://myaccount.google.com/security)

### Trouble 5: gog Command Not Found
**Cause**: PATH is not configured
**What the AI does**:
1. If installed via Homebrew: run `brew link gog`
2. If installed via `go install`: guide through adding `export PATH=$PATH:$(go env GOPATH)/bin` to `.zshrc` / `.bashrc`
3. Guide to run `source ~/.zshrc` or open a new terminal

### Trouble 6: Other Errors
**What the AI does**: Check the error message content, identify the cause, and guide to a solution

---

## Checkpoint
- [ ] gogcli is installed
- [ ] Google OAuth authentication is complete
- [ ] `gog auth list` shows the account
- [ ] Gmail search test succeeded
- [ ] Calendar retrieval test succeeded

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "gogcli setup is complete! What would you like to do next?",
    "options": [
      {"id": "try_gmail", "label": "Try Gmail search and browsing (/start-15-1)"},
      {"id": "try_calendar", "label": "Try Google Calendar operations"},
      {"id": "try_article", "label": "Start writing an article (/start-16-1)"},
      {"id": "back_to_setup", "label": "Go back to the setup list (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- try_gmail -> Guide to /start-15-1
- try_calendar -> Guide on how to use Google Calendar operations
- try_article -> Guide to /start-16-1
- back_to_setup -> Guide to /start-0-1
- finish -> End

---

## Completion

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-gogcli` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "Next, try Gmail search and browsing with `/start-15-1`"

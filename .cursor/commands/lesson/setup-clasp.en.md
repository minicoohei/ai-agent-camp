---
description: "Google Apps Script CLI (clasp) Setup (Complete Guide)"
duration: "~10 min"
prerequisites: ["Node.js 18 or higher installed", "Have a Google account", "Browser available"]
level: "beginner"
tags: ["setup", "gas", "clasp", "google"]
---

# Google Apps Script CLI (clasp) Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-clasp` to display progress
2. Auto-detect existing installation status:
   - Run `clasp --version`
   - If clasp is already installed and `clasp list` works, you can just run Step 5 (test) and mark it as complete
   - If not installed, start from Step 1

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Install clasp (Google Apps Script CLI), complete OAuth authentication, and be able to create, edit, and deploy GAS projects from your local machine |
| Duration | ~10 minutes |
| Prerequisites | Node.js 18+ installed, a Google account, and a browser available |
| Skill Level | CLI command entry required (npm install + clasp login) |
| Cost | Free |

**Session flow:**
1. Check your Node.js version
2. Install clasp globally via npm (AI runs automatically)
3. Enable the Apps Script API in the browser (AI opens the browser automatically)
4. Perform OAuth authentication with clasp login
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
(chrome -> After opening the browser in Step 3, follow the "Automating with Chrome integration" section for automatic execution)
(check_prereq -> Guide: "You're ready if you have Node.js 18+ installed and can log into a browser with a Google account. Node.js will be checked in the next step.")
(different_lesson -> Display module list)

---

## Step 1: Check Node.js

**What the AI does:**
1. Run `node --version` to check the Node.js version
2. Verify that the version is 18 or higher

**If Node.js is 18 or higher:**
Display "Confirmed Node.js v{version}. Moving to Step 2." and proceed to Step 2

**If Node.js is not installed or below 18 — AskQuestion:**

```json
{
  "title": "Step 1: Node.js installation required",
  "questions": [{
    "id": "node_status",
    "prompt": "clasp requires Node.js 18 or higher. Please install it from the following URL:\n\nhttps://nodejs.org/\n\nClick the 'LTS' version download button and follow the installer instructions.\n\nAfter installation, restart your terminal.",
    "options": [
      {"id": "installed", "label": "I installed Node.js"},
      {"id": "help", "label": "I don't know how to install it"},
      {"id": "skip", "label": "Set up later (skip)"}
    ]
  }]
}
```

(installed -> Re-run `node --version` to verify. If 18+, proceed to Step 2)
(help -> Guide: "Go to https://nodejs.org/ and click the green 'LTS' button to download. Open the downloaded file and follow the on-screen instructions to complete the installation.")
(skip -> Guide: "clasp setup requires Node.js. Please re-run /setup-clasp later." and end)

---

## Step 2: Install clasp

**What the AI auto-runs:**
1. Run `npm install -g @google/clasp` to install clasp globally
2. Verify the installation result

**On successful installation:**
Display "clasp installation complete. Moving to Step 3." and proceed to Step 3

**If a permission error (EACCES) occurs — AskQuestion:**

```json
{
  "title": "Step 2: npm permission error",
  "questions": [{
    "id": "npm_permission",
    "prompt": "A permission error occurred during npm global installation. You can resolve it with one of these methods:\n\n[Method 1] Use sudo (Mac/Linux):\nsudo npm install -g @google/clasp\n→ You will be prompted for your password\n\n[Method 2] Use npx instead (no installation needed):\nnpx @google/clasp login\n→ You need to add npx each time, but it avoids the permission issue",
    "options": [
      {"id": "sudo", "label": "Retry with sudo"},
      {"id": "npx", "label": "Use npx instead"},
      {"id": "help", "label": "I want to know other methods"}
    ]
  }]
}
```

(sudo -> Run `sudo npm install -g @google/clasp`. If successful, proceed to Step 3)
(npx -> Guide: "In the following steps, use `npx @google/clasp` instead of `clasp`." and proceed to Step 3)
(help -> Guide: "You can change npm's default directory permissions: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally")

---

## Step 3: Enable the Apps Script API

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to open the browser automatically:

```bash
# Mac:
open https://script.google.com/home/usersettings
# Windows:
start https://script.google.com/home/usersettings
# Linux:
xdg-open https://script.google.com/home/usersettings
```

**After the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 3: Enable the Apps Script API",
  "questions": [{
    "id": "api_status",
    "prompt": "Did the browser open? Follow these steps to enable the Apps Script API:\n\n1. Log in with your Google account\n2. Find the 'Google Apps Script API' toggle switch\n3. Turn the toggle to 'On'\n\n* If it's already on, leave it as is.\n\nDone?",
    "options": [
      {"id": "done", "label": "I enabled the API! (or it was already on)"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "no_toggle", "label": "I can't find the toggle switch"},
      {"id": "org_restriction", "label": "It says it's restricted by my organization's admin"}
    ]
  }]
}
```

(done -> Proceed to Step 4)
(browser_not_open -> Guide: "Open this URL directly in your browser: https://script.google.com/home/usersettings")
(no_toggle -> Guide: "Near the center of the page, there should be a 'Google Apps Script API' item with an on/off toggle switch. Try scrolling down. If you can't find it, make sure you're logged in with your Google account.")
(org_restriction -> Guide: "Your Google Workspace organization admin may have disabled the Apps Script API. Try logging in with a personal Gmail account (xxx@gmail.com). If you need to use an organization account, ask your IT admin to enable the Apps Script API.")

---

## Automating with Chrome Integration (`/chrome` mode)

**Prerequisite:** The "Claude in Chrome" extension (v1.0.36+) must be installed in Chrome, and you must have launched with `claude --chrome` or run `/chrome` in the session.

**What the AI auto-runs with Chrome integration:**
1. Open https://script.google.com/home/usersettings in the browser
2. Use Chrome integration to perform the following:
   - Find the "Google Apps Script API" toggle
   - If the toggle is OFF, click to turn it ON
3. Confirm the toggle is ON, then proceed to Step 4

If Chrome integration is not available, follow the Step 3 instructions manually.

---

## Step 4: clasp login (OAuth Authentication)

**What the AI auto-runs:**
1. Run `clasp login`
2. The browser opens automatically, displaying the Google account authentication screen

**AskQuestion configuration:**

```json
{
  "title": "Step 4: Authenticate with Google account",
  "questions": [{
    "id": "login_status",
    "prompt": "clasp login has been executed. The Google account authentication screen will appear in the browser:\n\n1. Select the Google account you want to use\n2. Click 'Allow' to grant clasp access permissions\n3. When 'Authorization successful.' appears in the terminal, you're done\n\nIs the authentication complete?",
    "options": [
      {"id": "done", "label": "'Authorization successful.' was displayed!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "permission_denied", "label": "'This app is blocked' is displayed"},
      {"id": "timeout", "label": "The auth screen appeared but the terminal isn't responding"}
    ]
  }]
}
```

(done -> Proceed to Step 5)
(browser_not_open -> Guide: "If a URL is displayed in the terminal, copy it and paste it into your browser. If you're in a remote environment like SSH, try `clasp login --no-localhost`.")
(permission_denied -> Guide: "Your Google Workspace organization policy may be blocking third-party apps. Try logging in with a personal Gmail account (xxx@gmail.com).")
(timeout -> Guide: "If 'Logged in!' is displayed in the browser after authentication, go back to the terminal and check. If there's no response, press Ctrl+C to cancel and re-run `clasp login`.")

---

## Step 5: Setup Test

**What the AI auto-runs:**

1. Run `clasp --version` to check the version
2. Run `clasp list` to get the project list
   - On first use, "No script files found." or an empty list is fine. If there's no error, authentication succeeded

3. Display an AskQuestion based on the test result:

**On success:**
```text
clasp setup is complete!

Test results:
- clasp version: {version}
- OAuth authentication: Successful
- Project list retrieval: Successful ({count} projects)

You can now create, edit, and deploy Google Apps Script projects from your local machine.
This can be used for automating Google Sheets, Forms, and Docs.
```

**On failure — AskQuestion:**
```json
{
  "title": "Test Result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the clasp test. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Run the test again"},
      {"id": "relogin", "label": "Redo clasp login (go back to Step 4)"},
      {"id": "show_error", "label": "I want to see the error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(relogin -> Go back to Step 4)
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
      {"id": "trouble_npm", "label": "I get a permission error (EACCES) with npm install"},
      {"id": "trouble_api_disabled", "label": "I get an 'Apps Script API has not been used' error"},
      {"id": "trouble_browser", "label": "The browser doesn't open with clasp login"},
      {"id": "trouble_org", "label": "I'm restricted with an organization Google account"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Trouble 1: Permission Error (EACCES) with npm install
**Cause**: No write permission to the global installation directory
**What the AI does**:
1. Suggest retrying with `sudo npm install -g @google/clasp`
2. If still unresolved, guide to changing npm's default directory: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally

### Trouble 2: "Apps Script API has not been used" Error
**Cause**: The Apps Script API is not enabled
**What the AI does**:
1. Open https://script.google.com/home/usersettings in the browser
2. Guide user to check if the "Google Apps Script API" toggle is on
3. After turning it on, re-run `clasp list` to verify

### Trouble 3: Browser Doesn't Open with clasp login
**Cause**: Remote environment, SSH connection, WSL, etc. where a browser can't launch
**AI guidance**: "Try `clasp login --no-localhost`. Copy the URL displayed in the terminal and paste it into your browser manually for authentication."

### Trouble 4: Restricted with Organization Google Account
**Cause**: Google Workspace organization admin has restricted third-party apps or the Apps Script API
**AI guidance**: "Try `clasp login` with a personal Gmail account (xxx@gmail.com). If you need to use an organization account, ask your IT admin for: (1) Enable the Apps Script API, (2) Allow clasp (OAuth client)."

### Trouble 5: Other Errors
**What the AI does**: Check the error message content, identify the cause, and guide the user to a solution

---

## Checkpoint
- [ ] Node.js 18 or higher is installed
- [ ] clasp was installed with `npm install -g @google/clasp`
- [ ] The Apps Script API was enabled (https://script.google.com/home/usersettings)
- [ ] OAuth authentication was completed with `clasp login` ("Authorization successful." displayed)
- [ ] `clasp --version` displays the version
- [ ] `clasp list` runs without errors

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "clasp setup is complete! What would you like to do next?",
    "options": [
      {"id": "start_gas", "label": "Learn GAS basics (/start-10-1)"},
      {"id": "setup_other", "label": "Proceed to another setup (/start-0-1)"},
      {"id": "check_setup", "label": "Run a full environment check (/check-setup)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- start_gas -> Guide to /start-10-1 (Clasp basics / GAS project management)
- setup_other -> Guide to /start-0-1
- check_setup -> Guide to /check-setup
- finish -> End

---

## Completion

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-clasp` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "Next, learn GAS basics with `/start-10-1` (Clasp basics / GAS project management)"

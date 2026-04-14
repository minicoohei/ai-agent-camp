---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~25 min"
prerequisites: ["start-0-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "auth"]
---

# 🎓 Lesson 4-1: gogcli Authentication Setup

## 📍 What You'll Do

**Lesson 4-1: gogcli Authentication Setup** !

| Item | Details |
|------|---------|
| Goal | Authenticate with a Google account using gogcli to enable Gmail/Calendar/Drive |
| Duration | ~25 min |
| Skills Used | gogcli (gog) |
| Prerequisites | Environment setup completed (start-0-1 done) |

**Session flow:**
1. Verify gogcli Installation
2. Add a Google Account via OAuth Authentication
3. Verify authentication status and basic operation test

By the end of this session, gogcli will have access to Gmail, Calendar, and Drive.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. The response may pause depending on the tool, but this is not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite check)
(different_lesson → Show module list)

---

## 🚀 Step 1: Verify gogcli Installation

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Verify gogcli Installation",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:

Verify that gogcli is installed. Run the following commands:

```bash
# Check version
gog --version

# If not installed
brew install gogcli
# If Homebrew is not available, download from GitHub Releases:
# https://github.com/steipete/gogcli/releases
```

**Expected result**: The gogcli version number is displayed (e.g., `gog version 0.x.x`).

> **📝 Note**: gogcli does not require creating an OAuth client in the GCP console. It uses built-in OAuth credentials for authentication, making setup very simple.

---

## 🚀 Step 2: Add Google Account via OAuth

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Add a Google Account via OAuth Authentication",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:

Authenticate your Google account. Run the following command:

```bash
# Add Google account (browser will open)
gog auth add your-email@gmail.com
```

**Steps:**
1. Running the command will automatically open the browser
2. Log in with your Google account
3. Approve access permissions for gogcli (Gmail, Calendar, Drive, Sheets, etc.)
4. Once "Authentication complete" is displayed, you can close the browser

```bash
# Check list of authenticated accounts
gog auth list

# Check available subcommands
gog --help
```

**Expected result**: `gog auth list` displays your email address.

> **⚠️ Warning**: Authentication credentials are stored securely on your local machine. Tokens are stored in the `.gog/` directory.

---

## 🚀 Step 3: Basic Operation Test

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Basic Operation Test",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:

Verify that each service is working correctly:

```bash
# Gmail: Search for the latest 5 emails
gog gmail search "newer_than:1d" --account your-email@gmail.com

# Calendar: List today's events
gog calendar list --account your-email@gmail.com --days 1

# Drive: List files in root folder
gog drive ls --account your-email@gmail.com --max 5
```

**Expected result**: Data from Gmail/Calendar/Drive is displayed with each command. If no errors appear, authentication has completed successfully.

> **💡 Hint**: The `--account` flag is required for all gogcli commands. You must specify your email address each time.

---

## ⚠️ Common Issues and Solutions

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "Cannot install gogcli"},
      {"id": "trouble_2", "label": "Browser does not open"},
      {"id": "trouble_3", "label": "Cannot access after authentication"},
      {"id": "trouble_4", "label": "Permission denied error"}
    ]
  }]
}
```

### Issue 1: "Cannot install gogcli"
**Cause**: Homebrew is not installed or PATH is not set
**Solution prompt**:
```text
Check the installation method for gogcli.
If Homebrew is available, try brew install gogcli.
If Homebrew is not available, download the binary from https://github.com/steipete/gogcli/releases.
```

### Issue 2: "Browser does not open"
**Cause**: Running in a remote or headless environment
**Solution prompt**:
```text
Copy the URL displayed when running gog auth add and paste it into your browser manually.
Enter the authentication code in the terminal when it is issued.
```

### Issue 3: "Cannot access after authentication"
**Cause**: Token storage failed, or insufficient scope
**Solution prompt**:
```text
Remove the authentication with gog auth remove your-email@gmail.com,
then re-authenticate with gog auth add your-email@gmail.com.
```

### Issue 4: "Permission denied error"
**Cause**: Access permissions are insufficient on the Google account side
**Solution prompt**:
```text
Check that "Less secure apps" are not blocked in your Google account security settings.
If a Google Workspace administrator has set API restrictions, consult the administrator.
```

---

## ✅ Checkpoint
- [ ] gogcli is installed (`gog --version` works)
- [ ] Google account authentication is complete (`gog auth list` displays it)
- [ ] Gmail search works (`gog gmail search` displays emails)
- [ ] Calendar listing works (`gog calendar list` displays events)
- [ ] Drive file listing works (`gog drive ls` displays files)


---

## 📋 Output Preview

The deliverable for this lesson is terminal output.

### Expected Output
```text
┌─────────────────────────────────────┐
│  Command execution result              │
│  Status: ✅ Success                     │
│  Items processed: N                     │
└─────────────────────────────────────┘
```

> Tip: To save output to a file, append ` > output/result.txt` to the end of the command

---

## ✅ Completion Check
Paste the following into Codex chat to verify completion:

```text
Run the following commands to verify gogcli authentication status:
1. gog auth list
2. gog gmail search "newer_than:1d" --account <your-email>
3. gog calendar list --account <your-email> --days 1
Verify that all commands work correctly.
```

**Expected result**: All three commands execute without errors.

---

## 🎉 Next Steps

gogcli authentication setup is now complete! In the next lesson, you will learn Gmail search and viewing.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/start-4-2)"},
      {"id": "next_window", "label": "Start in new window (/start-4-2)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /start-4-2（Gmail Search & Viewing)
- next_window → Open new window with /start-4-2
- finish → End

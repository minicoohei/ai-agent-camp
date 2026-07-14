---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Codex Desktop or Cursor installed"]
level: "beginner"
tags: ["setup", "environment"]
nonInteractiveMode: incompatible
---
# Training Environment Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-start` to display current progress
2. Auto-check the following; if all succeed, ask "Basic tools are already installed. Would you like to skip?":
   - `python3 --version`
   - `node --version`
   - `git --version`
   - `gh --version`
3. On Mac, check if Homebrew is available with `which brew`. If available, offer the option to auto-install missing tools with `brew install`

## What You'll Do in This Session

**Welcome to Training Environment Setup!**

| Item | Details |
|------|---------|
| Goal | Verify that Python / Node.js / Git / GitHub CLI are installed, and guide installation if anything is missing |
| Duration | ~10 minutes (3 minutes if everything is already installed) |
| Skills used | None (AI checks everything automatically) |
| Prerequisites | Codex Desktop or Cursor installed, ai-agent-camp folder open |
| Next command | `/setup-github` (GitHub account setup) |

**Session flow:**
1. Auto-detect OS (Mac / Windows)
2. Check Python
3. Check Node.js
4. Check Git
5. Check GitHub CLI

> **Important**: You do not need to type any commands in the terminal. The AI runs everything automatically behind the scenes. Just review the results displayed on screen.
>
> **Note for Codex**: In Codex, instead of calling `/setup-start` as a slash command, follow the check items in this document in order. The AI will hand off to you only for steps that require downloads or browser authentication.
>
> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

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
      {"id": "what_is_this", "label": "What does this command do?"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(what_is_this -> Guide: "This command has the AI automatically check whether the software needed for the training is installed on your computer. If something is missing, you just follow the on-screen instructions to install it. No command input needed." -> Proceed to Step 1)
(different_lesson -> Show module list)

---

## Step 1: Auto-detect OS

**What the AI auto-runs:**
The AI runs the following behind the scenes to detect the OS:

```bash
uname -s
```

Mac returns `Darwin`, Linux/WSL returns `Linux`. If `Linux` is returned, further check whether it is WSL:

```bash
grep -qi microsoft /proc/version 2>/dev/null && echo "WSL" || echo "Native Linux"
```

**Display the detection result:**
- Mac: "Your computer is a **Mac**. We'll proceed with Mac-specific steps."
- WSL: "Your computer is running **Windows (WSL)**. We'll proceed with Linux-based steps."
- Linux: "Your computer is running **Linux**. We'll proceed with Linux-specific steps."

**The detected OS information is used in all subsequent steps.**

> User action required: None (AI auto-detects everything)

---

## Step 2: Check Python

**What the AI auto-runs:**

1. Run the following to check the version:

```bash
# Mac / Linux
python3 --version

# Windows
python --version
```

2. Evaluate the result:
   - If a version is displayed -> Installed
   - If command not found -> Not installed

### If Python is installed

Display example:
```text
Python 3.12.x found. No issues.
```
-> Automatically proceed to Step 3

### If Python is not installed

**AskQuestion configuration:**
```json
{
  "title": "Python installation required",
  "questions": [{
    "id": "python_install",
    "prompt": "Python 3 is not installed. We'll guide you through installation.",
    "options": [
      {"id": "guide_me", "label": "Show me the installation steps"},
      {"id": "already_done", "label": "I installed it another way (re-check)"}
    ]
  }]
}
```

(guide_me -> Show OS-specific instructions)
(already_done -> Re-run `python3 --version` / `python --version` to check)

**Mac instructions:**
```text
Follow these steps to install:

1. The AI will automatically open your browser (please wait a moment)
2. Click the yellow "Download Python 3.12.x" button on the page
3. Double-click the downloaded .pkg file
4. Follow the installer: click "Continue" -> "Install"
5. When done, type "finished" here
```

```bash
AI runs: open https://www.python.org/downloads/
```

**Windows instructions:**
```text
Follow these steps to install:

1. The AI will automatically open your browser (please wait a moment)
   * If the browser doesn't open, open the Microsoft Store app and search for "Python 3.12"
2. Click the "Get" button for "Python 3.12" in the Microsoft Store
3. When installation is complete, type "finished" here
```

```bash
AI runs: start https://apps.microsoft.com/search?query=Python+3.12
# Falls back to start https://www.python.org/downloads/ on failure
```

**After installation:**
AI re-runs `python3 --version` / `python --version` to verify.
- Success -> Display "Python installation complete!" and proceed to Step 3
- Failure -> Guide to the troubleshooting section

---

## Step 3: Check Node.js

**What the AI auto-runs:**

1. Run the following to check the version:

```bash
node --version
```

2. Evaluate the result:
   - Version 18.x or higher displayed -> Installed
   - Version is old -> Guide upgrade
   - Command not found -> Not installed

### If Node.js is installed (18.x or higher)

Display example:
```text
Node.js v20.x.x found. No issues.
```
-> Automatically proceed to Step 4

### If Node.js is not installed / version is old

**AskQuestion configuration:**
```json
{
  "title": "Node.js installation required",
  "questions": [{
    "id": "node_install",
    "prompt": "Node.js 18 or higher is required. We'll guide you through installation.",
    "options": [
      {"id": "guide_me", "label": "Show me the installation steps"},
      {"id": "already_done", "label": "I installed it another way (re-check)"}
    ]
  }]
}
```

(guide_me -> Show OS-specific instructions)
(already_done -> Re-run `node --version` to check)

**Mac / Windows common instructions:**
```text
Follow these steps to install:

1. The AI will automatically open your browser (please wait a moment)
2. Click the green "LTS" button on the page (this is the recommended version)
3. Open the downloaded file to launch the installer
4. Follow the installer: click "Next" -> "Install"
5. When done, type "finished" here
```

```bash
# AI runs:
# Mac:
open https://nodejs.org/
# Windows:
start https://nodejs.org/
```

**After installation:**
AI re-runs `node --version` to verify.
- Success -> Display "Node.js installation complete!" and proceed to Step 4
- Failure -> Guide: "Close Cursor completely and reopen it, then run this command (/setup-start) again"

---

## Step 4: Check Git

**What the AI auto-runs:**

1. Run the following to check the version:

```bash
git --version
```

2. Evaluate the result:
   - If a version is displayed -> Installed
   - If command not found -> Not installed

### If Git is installed

Display example:
```text
Git 2.x.x found. No issues.
```
-> Automatically proceed to Step 5

### If Git is not installed

**Mac instructions:**
```text
We'll install Git.
The AI will automatically run the install command.
If a popup appears, click "Install".
```

```bash
AI runs: xcode-select --install
# The Xcode Command Line Tools installer launches. User just clicks "Install" in the popup
```

After installation, AI re-runs `git --version` to verify.

**Windows instructions:**
```text
Follow these steps to install:

1. The AI will automatically open your browser (please wait a moment)
2. The download will start automatically (if not, click "Click here to download")
3. Open the downloaded .exe file to launch the installer
4. Keep all default settings and click "Next" -> "Install"
5. When done, type "finished" here
```

```bash
AI runs: start https://git-scm.com/download/win
```

**After installation:**
AI re-runs `git --version` to verify.
- Success -> Display "Git installation complete!" and proceed to Step 5
- Failure -> Guide: "Close Cursor completely and reopen it, then run this command (/setup-start) again"

---

## Step 5: Check GitHub CLI

**What the AI auto-runs:**

1. Run the following to check the version:

```bash
gh --version
```

2. Evaluate the result:
   - If a version is displayed -> Installed
   - If command not found -> Not installed

### If GitHub CLI is installed

Display example:
```text
GitHub CLI 2.x.x found. No issues.
```
-> Proceed to completion section

### If GitHub CLI is not installed

**AskQuestion configuration:**
```json
{
  "title": "GitHub CLI installation required",
  "questions": [{
    "id": "gh_install",
    "prompt": "GitHub CLI is not installed. We'll guide you through installation.",
    "options": [
      {"id": "guide_me", "label": "Show me the installation steps"},
      {"id": "already_done", "label": "I installed it another way (re-check)"}
    ]
  }]
}
```

(guide_me -> Show OS-specific instructions)
(already_done -> Re-run `gh --version` to check)

**Mac instructions:**

First check if Homebrew is installed:

```bash
brew --version
```

If Homebrew is available:
```text
The AI will automatically run the installation. Please wait...
```

```bash
AI runs: brew install gh
```

If Homebrew is not available:
```text
Follow these steps to install:

1. The AI will automatically open your browser (please wait a moment)
2. Click "Download for macOS" on the page
3. Double-click the downloaded .pkg file
4. Follow the installer: click "Continue" -> "Install"
5. When done, type "finished" here
```

```bash
AI runs: open https://cli.github.com/
```

**Windows instructions:**
```text
Follow these steps to install:

1. The AI will automatically open your browser (please wait a moment)
2. Click "Download for Windows" on the page
3. Open the downloaded .msi file to launch the installer
4. Keep all default settings and click "Next" -> "Install"
5. When done, type "finished" here
```

```bash
AI runs: start https://cli.github.com/
```

**After installation:**
AI re-runs `gh --version` to verify.
- Success -> Display "GitHub CLI installation complete!" and proceed to completion section
- Failure -> Guide: "Close Cursor completely and reopen it, then run this command (/setup-start) again"

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
      {"id": "trouble_1", "label": "The browser didn't open automatically"},
      {"id": "trouble_2", "label": "It says 'not found' even though I installed it"},
      {"id": "trouble_3", "label": "The installer gives an error"},
      {"id": "trouble_4", "label": "No popup on Mac (Git)"},
      {"id": "trouble_5", "label": "Other issue"}
    ]
  }]
}
```

### Issue 1: "The browser didn't open automatically"
**Cause**: Default browser settings, or security software blocking
**Solution**:
```text
If the browser doesn't open, copy and paste the following URLs directly into your browser's address bar:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Git (Windows): https://git-scm.com/download/win
- GitHub CLI: https://cli.github.com/
```

### Issue 2: "It says 'not found' even though I installed it"
**Cause**: Cursor (terminal) hasn't recognized the installation
**Solution**:
```text
Close Cursor completely (click the X button in the top right), then reopen it.
After that, run /setup-start again.
This resolves the issue in most cases.
```

### Issue 3: "The installer gives an error"
**Cause**: Insufficient permissions, insufficient disk space, or network issues
**Solution**:
AI auto-diagnoses:

```bash
# 1. Check free disk space
df -h /                          # Mac / Linux
wmic logicaldisk get freespace   # Windows

# 2. Check network connection
ping -c 1 google.com             # Mac / Linux
ping -n 1 google.com             # Windows
```

3. Provide specific solutions based on the results

### Issue 4: "No Git popup on Mac"
**Cause**: Xcode Command Line Tools already installed, or another issue
**Solution**:
AI runs `xcode-select -p` to check the path.
If a path is displayed, it's already installed. Re-check `git --version`.

### Issue 5: "Other issue"
**Solution**:
```text
What problem are you experiencing? Please tell me the error message or situation shown on screen.
The AI will diagnose the cause and suggest a solution.
```

---

## Checkpoint

AI auto-checks all items and displays results:

| Item | Status | Version |
|------|--------|---------|
| OS | (auto-displayed) | Mac / Windows |
| Python | (auto-displayed) | 3.x.x |
| Node.js | (auto-displayed) | 20.x.x |
| Git | (auto-displayed) | 2.x.x |
| GitHub CLI | (auto-displayed) | 2.x.x |

Only proceed to the next step if all items are OK.

---

## Next Steps

**If everything is installed:**

```text
Congratulations! All required software is ready!

Next, we'll set up GitHub.
Enter the following in Cursor's chat:

/setup-github
```

**If some items are not installed:**

```text
The following items are not yet installed:
- (list missing items)

Please complete the above installations, then run /setup-start again.
```

---

## Completion Processing

**What the AI auto-runs:**
1. Update progress with the following command:
   ```bash
   uv run python tools/setup_progress.py complete setup-start --details "{\"python\":\"$(python3 --version 2>&1 | awk '{print $2}')\",\"node\":\"$(node --version 2>&1)\",\"git\":\"$(git --version 2>&1 | awk '{print $3}')\"}"
   ```
2. Updated progress summary is automatically displayed
3. Guide the user to the next step: "Next, let's set up GitHub with `/setup-github`"

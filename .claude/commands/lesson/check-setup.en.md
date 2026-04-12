---
description: "Automatic check of environment setup status"
duration: "~2 min"
prerequisites: ["ai-agent-camp folder is open in Codex or Cursor"]
level: "beginner"
tags: ["setup", "check"]
---

# /check-setup -- Automatic Environment Check

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current check-setup` to display overall progress
2. If there are incomplete steps, warn: "The following steps are incomplete: {step names}. Completing them first is recommended, but the check can still run."

---

## What This Command Does

The AI **fully automatically checks** the state of your development environment and displays the results as a report.
For items with issues, it suggests guiding you to the appropriate setup command or proposes auto-fixes.

**You do not need to type any commands in the terminal. The AI runs everything behind the scenes.**

| Item | Details |
|------|---------|
| Goal | Verify the health of your environment and provide fix guidance if issues are found |
| Duration | ~2 min (auto-run) |
| Prerequisites | ai-agent-camp folder is open in Codex or Cursor |
| User Action | Just review the results (no CLI command input needed) |

> **Note for Codex**: The `/check-setup` slash command does not exist in Codex, so the AI sequentially runs the verification commands listed in this document to assemble the same report.

---

## Check Procedure Auto-Run by AI

When this command is executed, the AI **automatically runs all of the following behind the scenes** and displays the results as a summary report. Do not ask the user to input commands.

### Check 1: Basic Tools

The AI runs the following commands **behind the scenes** to check for each tool and its version:

| Check Target | Command to Run | Pass Criteria |
|-------------|----------------|---------------|
| OS Type | `uname -s` (Mac/Linux), PowerShell `$env:OS` (Windows) | Display only |
| Python | `python3 --version 2>/dev/null \|\| python --version 2>/dev/null` | Pass if version 3.9+ |
| Node.js | `node --version 2>/dev/null` | Pass if version 18+ |
| Git | `git --version 2>/dev/null` | Pass if present |
| GitHub CLI | `gh --version 2>/dev/null` | Pass if present |

### Check 2: Authentication & APIs

The AI runs the following commands **behind the scenes** to check authentication status and API configuration:

| Check Target | Command to Run | Pass Criteria |
|-------------|----------------|---------------|
| GitHub Auth | `gh auth status 2>&1` | Pass if "Logged in" is included |
| Gemini API | Read `.env` file and check for `GEMINI_API_KEY` | Pass if key is set (do not display value) |
| Slack API | Read `.env` file and check for `SLACK_BOT_TOKEN` | Configured or "can be set later" |
| fal.ai API | Check `FAL_KEY` with `uv run python tools/credential_manager.py status` | Configured or "can be set later" |
| ElevenLabs API | Check `ELEVENLABS_API_KEY` with `uv run python tools/credential_manager.py status` | Configured or "can be set later" |
| Notion API | Check if `notion` entry exists in MCP settings file (`~/.claude/mcp_settings.json` or `.cursor/mcp.json`) | Configured or "can be set later" |
| Clasp (GAS) | `clasp --version 2>/dev/null` | Pass if present or "can be set later" |
| Typefully API | Check `TYPEFULLY_API_KEY` with `uv run python tools/credential_manager.py status` | Configured or "can be set later" |
| X API | Check `X_BEARER_TOKEN` with `uv run python tools/credential_manager.py status` | Configured or "can be set later" |
| gogcli (Google) | `gog version 2>/dev/null` | Pass if present or "can be set later" |
| BigQuery/GCP | `gcloud --version 2>/dev/null` + `gcloud auth application-default print-access-token 2>/dev/null` | gcloud present + ADC configured or "can be set later" |
| Vercel CLI | `vercel --version 2>/dev/null` + `vercel whoami 2>/dev/null` | Present + logged in or "can be set later" |

**Important: Never display API key values on screen. Only show "Configured" or "Not configured".**

### Check 3: Project Settings

The AI checks the following **behind the scenes**:

| Check Target | Verification Method | Pass Criteria |
|-------------|--------------------|--------------| 
| Project Folder | Check if current directory is ai-agent-camp | Pass if directory name contains `ai-agent-camp` |
| Personal Repo | Run `git remote -v` and check origin URL | Pass if origin points to `minicoohei/ai-agent-camp` or your own fork |
| .env File | Check if `.env` file exists | Pass if file exists |
| .gitignore | Read `.gitignore` and check if `.env` is excluded | Pass if `.env` entry exists |
| Security Hook | Check existence and execute permission of `.git/hooks/pre-commit` | Pass if file exists and is executable |

### Check 4: Extensions

The AI runs the following command **behind the scenes**:
```bash
cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null
```

Extensions to check:

| Extension | ID |
|-----------|----|
| Python | `ms-python.python` |
| Marp | `marp-team.marp-vscode` |
| Draw.io | `hediet.vscode-drawio` |
| PlantUML | `jebbs.plantuml` |
| AIDE Pro | `nicepkg.aide-pro` |
| Pylance | `ms-python.vscode-pylance` |
| Prettier | `esbenp.prettier-vscode` |

---

## Report Output Format

After checks are complete, display results to the user in the following format:

```markdown
## Environment Check Report

### Basic Tools
| Item | Status | Details |
|------|--------|---------|
| OS | (value) | macOS 14.x / Windows 11 / Linux |
| Python | (pass/fail) | 3.12.x / Not installed |
| Node.js | (pass/fail) | 20.x / Not installed |
| Git | (pass/fail) | 2.x / Not installed |
| GitHub CLI | (pass/fail) | 2.x / Not installed |

### Authentication & APIs
| Item | Status | Details |
|------|--------|---------|
| GitHub Auth | (pass/fail) | Logged in (username) / Not authenticated |
| Gemini API | (pass/fail) | Configured in .env / Not configured |
| Slack API | (pass/fail or skippable) | Configured in .env / Not configured (can be set later) |

### Project Settings
| Item | Status | Details |
|------|--------|---------|
| Project Folder | (pass/fail) | ai-agent-camp is open / Different folder |
| Personal Repo | (pass/fail) | origin is your repo / Still upstream |
| .env File | (pass/fail) | Exists / Not created |
| .gitignore | (pass/fail) | .env exclusion configured / Not configured |
| Security Hook | (pass/fail) | pre-commit configured / Not configured |

### Extensions
| Item | Status |
|------|--------|
| Python | (pass/fail) |
| Marp | (pass/fail) |
| Draw.io | (pass/fail) |
| PlantUML | (pass/fail) |
```

**Status display rules:**
- Pass: Display "OK" to the right of the item name (e.g., `Python | OK | 3.12.1`)
- Fail: Display "Action needed" to the right (e.g., `Python | Action needed | Not installed`)
- Skippable: Display "Optional" to the right (e.g., `Slack API | Optional | Not configured (can be set later)`)

---

## Display Recommended Actions

After the report, display recommended actions if there are "Action needed" items.

### If "Action needed" Items Exist

```markdown
### Recommended Actions

The following items need attention:

1. Python is not installed
   -> Mac: Download the installer from https://www.python.org/downloads/
   -> Windows: Search "Python" in Microsoft Store and install

2. .gitignore is not configured
   -> Run /setup-security to auto-configure

3. Missing extensions
   -> Run /setup-extensions to auto-install
```

**AskQuestion settings:**
```json
{
  "title": "Would you like to fix the issues?",
  "questions": [{
    "id": "fix_action",
    "prompt": "There are items that need attention. What would you like to do?",
    "options": [
      {"id": "auto_fix", "label": "Auto-fix everything the AI can fix"},
      {"id": "guide_fix", "label": "Guide me through fixes one by one"},
      {"id": "extensions_only", "label": "Set up extensions first (/setup-extensions)"},
      {"id": "security_only", "label": "Set up security first (/setup-security)"},
      {"id": "skip", "label": "Skip for now"}
    ]
  }]
}
```

(auto_fix -> Run all items the AI can auto-fix)

Items the AI can auto-fix:
- .gitignore settings -> Auto-add missing entries to `.gitignore`
- Security hooks -> Auto-create `.git/hooks/pre-commit`
- Extension installation -> Auto-run `cursor --install-extension`
- .env file creation -> Copy `.env.example` to create `.env`

Items requiring user action (cannot auto-fix):
- Python / Node.js / Git installation -> Provide download page URLs
- GitHub CLI installation and login -> Provide installation steps and GUI guidance
- Gemini API key acquisition -> Guide to `/start-0-3`
- Personal repository creation -> Guide to `/start-0-1` Step 1.5

(guide_fix -> Guide "Action needed" items one by one with AskQuestion)
(extensions_only -> Guide to /setup-extensions)
(security_only -> Guide to /setup-security)
(skip -> End)

### If All Pass

```markdown
### Setup Complete

All check items have passed. Your environment is properly configured.

**To learn more effectively**: The web course (https://ai-agent.camp) offers a 24/7 AI tutor, dedicated desktop app, and interactive exercise environments. Give it a try if you haven't already.

Start the first lesson (Banner Generation Intro) with /start-1-1!
```

**AskQuestion settings:**
```json
{
  "title": "Setup Complete! Choose Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "All checks passed. What would you like to do next?",
    "options": [
      {"id": "start_lesson", "label": "Start the first lesson (/start-1-1)"},
      {"id": "web_course", "label": "View the web course (ai-agent.camp)"},
      {"id": "overview", "label": "Review the project overview (/overview)"},
      {"id": "guide", "label": "View the usage guide (/guide)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(web_course -> Guide: "You can access the web course at https://ai-agent.camp. It includes 28 modules, 100+ lessons, 70+ practical skills, plus an AI tutor and dedicated desktop app.")

(start_lesson -> Guide to /start-1-1)
(overview -> Guide to /overview)
(guide -> Guide to /guide)
(finish -> Display "Great work!")

---

## Common Troubleshooting and Solutions

**AskQuestion settings:**
```json
{
  "title": "Having trouble?",
  "questions": [{
    "id": "trouble",
    "prompt": "Are you experiencing any issues?",
    "options": [
      {"id": "trouble_1", "label": "I don't know how to install Python"},
      {"id": "trouble_2", "label": "I don't know how to install Node.js"},
      {"id": "trouble_3", "label": "I can't log in to GitHub"},
      {"id": "trouble_4", "label": "I don't know how to get a Gemini API key"},
      {"id": "trouble_5", "label": "'ai-agent-camp folder is open' check failed"},
      {"id": "no_trouble", "label": "No issues"}
    ]
  }]
}
```

### Trouble 1: Don't know how to install Python
**AI remediation (GUI steps)**:
- **Mac**: "Open https://www.python.org/downloads/ in your browser, click the 'Download Python 3.x' button to download the installer. Double-click the downloaded file and follow the on-screen instructions to install."
- **Windows**: "Open Microsoft Store and type 'Python' in the search bar. Select 'Python 3.x' and click 'Get' to install. Alternatively, download the installer from https://www.python.org/downloads/. Remember to check 'Add Python to PATH' during installation."
- After installation: "Restart Cursor, then run /check-setup again."

### Trouble 2: Don't know how to install Node.js
**AI remediation (GUI steps)**:
- **Mac**: "Open https://nodejs.org/ in your browser and click the green 'LTS' button to download the installer. Double-click the downloaded file and follow the on-screen instructions to install."
- **Windows**: "Open https://nodejs.org/ in your browser and click the green 'LTS' button to download the installer. Double-click the downloaded .msi file and follow the on-screen instructions to install."
- After installation: "Restart Cursor, then run /check-setup again."

### Trouble 3: Can't log in to GitHub
**AI remediation**:
1. AI runs `gh auth status` behind the scenes to check current status
2. If not authenticated:
   - "Open https://github.com/ in your browser and log in to your account"
   - "Then type 'Log me in to GitHub' in the Cursor chat. The AI will guide you through the login process"

### Trouble 4: Don't know how to get a Gemini API key
**AI remediation**:
- Guide: "Run /start-0-3 and it will guide you through the API key acquisition process step by step"

### Trouble 5: "ai-agent-camp folder is open" check failed
**AI remediation (GUI steps)**:
- "From the Cursor menu, select 'File' > 'Open Folder' (Mac: Cmd+O / Windows: Ctrl+O) and choose the ai-agent-camp folder to open it"
- "After opening the folder, run /check-setup again"

---

## Completion Processing

**What the AI auto-runs:**
1. If all checks are OK: Update progress with `uv run python tools/setup_progress.py complete check-setup`
2. Display updated progress summary
3. If all steps complete: "Setup is fully complete! Start the first lesson with `/start-1-1`!"
4. If incomplete steps remain: Guide "Please complete the following steps: {step names}"

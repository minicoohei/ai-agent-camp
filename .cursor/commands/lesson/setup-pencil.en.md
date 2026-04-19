---
description: "Lesson command"
duration: "~15 min"
prerequisites: ["Browser available", "Claude Code or Cursor installed"]
level: "beginner"
tags: ["setup", "pencil", "mcp", "design"]
---

# Pencil MCP Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-pencil` to display progress
2. Auto-detect existing settings:
   - For Claude Code: Check whether a `pencil` server is defined in `~/.claude/mcp_settings.json`
   - For Cursor: Check whether a `pencil` server is defined in `.cursor/mcp.json`
   - If already configured, only run Step 4 (connection test) and mark as complete

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Install the Pencil desktop app and enable design file (.pen) operations from Claude Code/Cursor via the MCP server |
| Duration | ~15 minutes |
| Prerequisites | Browser available, Claude Code or Cursor already installed |
| Skill Level | App installation + MCP configuration (AI-assisted) |

**Session flow:**
1. Download and install the Pencil desktop app
2. Launch Pencil and complete initial setup
3. Add the Pencil server to the MCP configuration file
4. MCP connection test

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
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "already_installed", "label": "Pencil is already installed"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(check_prereq -> Guide: "You're good to go if Claude Code or Cursor is already installed")
(already_installed -> Skip to Step 3 (MCP configuration))
(different_lesson -> Show module list)

---

## Step 1: Download the Pencil Desktop App

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Open the Pencil download page in the browser:

```bash
# Mac:
open https://pencil.evolves.dev/download
# Windows:
start https://pencil.evolves.dev/download
# Linux:
xdg-open https://pencil.evolves.dev/download
```

**Once the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Download the Pencil App",
  "questions": [{
    "id": "download_status",
    "prompt": "Did the Pencil download page open in your browser?\n\nSteps:\n1. Download the installer for your OS (Mac / Windows)\n2. Run the downloaded file to install\n   - Mac: Open the .dmg and drag to the Applications folder\n   - Windows: Run the .exe and follow the wizard\n\nWere you able to install it?",
    "options": [
      {"id": "installed", "label": "Installed!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "download_issue", "label": "Can't download"},
      {"id": "mac_security", "label": "I'm getting a Mac security warning"}
    ]
  }]
}
```

(installed -> Proceed to Step 2)
(browser_not_open -> Guide: "Please open this URL directly in your browser: https://pencil.evolves.dev/download")
(download_issue -> Guide: "Please check your internet connection. If the download is slow, please wait a moment")
(mac_security -> Guide: "Go to System Settings -> Privacy & Security -> click 'Open Anyway'. Alternatively, right-click the app in Finder and select 'Open'")

---

## Step 2: Launch and Initial Setup of the Pencil App

**Message to show the user:**

```text
Please launch the Pencil app:

┌─────────────────────────────────────────────────────────────┐
│ 1. Launch "Pencil" from your Applications                   │
│ 2. If account creation or login is required on first        │
│    launch, follow the on-screen instructions                │
│ 3. You're good once the editor screen appears               │
│                                                             │
│ * Pencil is a desktop app for creating and editing          │
│   design files in .pen format                               │
└─────────────────────────────────────────────────────────────┘
```

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Launch the Pencil App",
  "questions": [{
    "id": "app_status",
    "prompt": "Were you able to launch the Pencil app?",
    "options": [
      {"id": "running", "label": "Pencil is running!"},
      {"id": "cant_find", "label": "I can't find the app"},
      {"id": "crash", "label": "It crashes on launch"},
      {"id": "login_issue", "label": "I'm having trouble with login/account creation"}
    ]
  }]
}
```

(running -> Proceed to Step 3)
(cant_find -> Mac: Check the "Applications" folder / Windows: Check the Start Menu. If installation isn't complete, go back to Step 1)
(crash -> Guide: "Make sure your OS is up to date. If the problem persists, try uninstalling and reinstalling")
(login_issue -> Guide: "You can create an account on the Pencil website (https://pencil.evolves.dev). You can register with your email address")

---

## Step 3: Add Pencil Server to MCP Configuration File

**What the AI auto-runs:**

1. Determine the tool being used (Claude Code or Cursor)
2. Guide the Pencil MCP server configuration

**Pencil MCP connection method:**

Pencil MCP is built into the Pencil desktop app. When the app is running, it automatically becomes available as an MCP server.

**For Claude Code:** Add the following to `~/.claude/mcp_settings.json`:
```json
{
  "mcpServers": {
    "pencil": {
      "url": "http://localhost:13742/sse"
    }
  }
}
```

**For Cursor:** Add the following to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "pencil": {
      "url": "http://localhost:13742/sse"
    }
  }
}
```

> **Note**: If you already have an MCP configuration file, add the `pencil` entry inside `mcpServers`. Do not delete other server configurations.

**AskQuestion configuration:**
```json
{
  "title": "Step 3: MCP Configuration",
  "questions": [{
    "id": "config_status",
    "prompt": "Have you added the Pencil server configuration to the MCP config file?",
    "options": [
      {"id": "done", "label": "Configuration added!"},
      {"id": "auto_setup", "label": "I want the AI to configure it automatically"},
      {"id": "existing_config", "label": "I already have a config file and want to know how to append"},
      {"id": "help", "label": "I don't know how to configure it"}
    ]
  }]
}
```

(done -> Proceed to Step 4)
(auto_setup -> AI automatically creates/updates the configuration file. Existing server configurations are preserved)
(existing_config -> Read the existing file contents and guide how to append the `pencil` entry to `mcpServers`)
(help -> Guide with detailed steps for each tool)

---

## Step 4: MCP Connection Test

**What the AI does:**

1. Guide restarting Claude Code / Cursor:

```text
You need to restart your tool to apply MCP settings.

For Claude Code:
  -> Exit with 'exit' and restart claude

For Cursor:
  -> Press Cmd+Shift+P (Mac) / Ctrl+Shift+P (Windows) to
    open the Command Palette and run "Reload Window"
```

**AskQuestion configuration:**
```json
{
  "title": "Step 4: MCP Connection Test",
  "questions": [{
    "id": "restart_status",
    "prompt": "Have you restarted your tool? (Please also confirm that the Pencil app is running)",
    "options": [
      {"id": "restarted", "label": "Restarted! Please run the test"},
      {"id": "how_restart", "label": "I don't know how to restart"},
      {"id": "skip_test", "label": "Skip the test"}
    ]
  }]
}
```

(restarted -> Run MCP connection test)

2. MCP connection test:
   - Run `get_editor_state()` to get Pencil's state
   - Connection success: Display "Successfully connected to Pencil MCP"
   - Connection failure: Go to troubleshooting

**On test success:**
```text
Pencil MCP setup is complete!

Test result: Successfully connected to the Pencil MCP server.
You can now create and edit .pen files directly from Claude Code/Cursor.

Available tools:
- get_editor_state(): Get editor state
- open_document(): Create/open documents
- batch_design(): Insert, update, and delete design elements
- get_screenshot(): Take screenshots
- get_guidelines(): Get design guidelines
```

**AskQuestion on test failure:**
```json
{
  "title": "Test result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the MCP connection test. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Try the test again"},
      {"id": "check_app", "label": "Check if the Pencil app is running"},
      {"id": "check_config", "label": "Check the MCP config file"},
      {"id": "check_port", "label": "Check if port 13742 is available"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(check_app -> Guide: "The MCP server cannot be reached if the Pencil app is not running. Please launch the Pencil app and try the test again")
(check_config -> Check the MCP config file contents. Verify the URL is correct and JSON syntax is valid)
(check_port -> Check port usage with `lsof -i :13742`)
(skip_test -> Guide: "Test skipped. You can verify the connection when you use Pencil MCP in Lesson 13-3")

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
      {"id": "trouble_connect", "label": "Can't connect to the MCP server"},
      {"id": "trouble_app", "label": "Pencil app won't launch"},
      {"id": "trouble_port", "label": "The port is already in use"},
      {"id": "trouble_cost", "label": "Concerned about pricing"}
    ]
  }]
}
```

### Issue 1: Can't connect to the MCP server
**Cause**: Pencil app is not running, or the MCP config URL is incorrect
**What the AI does**:
1. Guide checking whether the Pencil app is running
2. Verify the MCP config file URL is `http://localhost:13742/sse`
3. Check port listening status with `lsof -i :13742`

### Issue 2: Pencil app won't launch
**Cause**: Incomplete installation or OS compatibility issue
**What the AI does**:
1. Check OS version
2. Guide reinstallation
3. Check Mac security settings (Gatekeeper)

### Issue 3: Port is already in use
**Cause**: Another process is using port 13742
**What the AI does**:
1. Check the process using the port with `lsof -i :13742`
2. Guide stopping the conflicting process

### Issue 4: Concerned about pricing
**AI guidance**: "The Pencil app has a free plan. Basic features including MCP integration are available for free. Check https://pencil.evolves.dev for details"

---

## Checkpoint
- [ ] Downloaded and installed the Pencil desktop app
- [ ] Pencil app launches successfully
- [ ] Added Pencil server configuration to the MCP config file
- [ ] Restarted Claude Code / Cursor
- [ ] MCP connection test succeeded (get_editor_state works)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Pencil MCP setup is complete! What would you like to do next?",
    "options": [
      {"id": "start_design", "label": "Start LP design (/start-13-3)"},
      {"id": "try_pencil", "label": "Try basic Pencil operations"},
      {"id": "setup_other", "label": "Set up other APIs (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- start_design -> Guide to /start-13-3
- try_pencil -> Guide basic operations: get_editor_state, open_document, batch_design
- setup_other -> Guide to /start-0-1
- finish -> End

---

## Completion Processing

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-pencil` to update progress
2. Updated progress summary is automatically displayed
3. Guide the user to the next step: "Next, let's start LP design with Pencil using `/start-13-3`"

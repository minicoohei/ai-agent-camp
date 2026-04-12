---
description: "Notion MCP Setup (Complete Guide)"
duration: "~15 min"
prerequisites: ["Have a Notion account (free plan OK)", "Browser available"]
level: "beginner"
tags: ["setup", "notion", "mcp", "api"]
---

# Notion MCP Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-notion` to display progress
2. Auto-detect existing configuration:
   - For Claude Code: check if a `notion` server is defined in `~/.claude/mcp_settings.json`
   - For Cursor: check if a `notion` server is defined in `.cursor/mcp.json`
   - If already configured, you can just run Step 5 (connection test) and mark it as complete

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Create a Notion integration and enable Claude Code/Cursor to operate Notion pages and databases via the MCP server |
| Duration | ~15 minutes |
| Prerequisites | Have a Notion account (free plan OK), browser available |
| Skill Level | No CLI commands needed (everything is auto-run by AI + GUI operations only) |

**Session flow:**
1. Open the Notion Integrations page in the browser (AI opens the browser automatically)
2. Create an integration and get the API key (just click buttons on screen)
3. Create the MCP configuration file (AI creates it automatically)
4. Share the integration with Notion pages
5. MCP connection test

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
      {"id": "which_tool", "label": "I want to confirm whether I'm using Claude Code or Cursor"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(chrome -> After opening the browser in Step 1, follow the "Automating with Chrome Integration" section for automatic execution)
(check_prereq -> Guide: "You're ready if you have a Notion account (free plan OK) and can log in via your browser.")
(which_tool -> Explain: "The configuration file location differs between Claude Code and Cursor. Step 3 will guide you through the steps for each.")
(different_lesson -> Display module list)

---

## Step 1: Open the Notion Integrations Page in the Browser

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run the following command to open the browser automatically:

```bash
# Mac:
open https://www.notion.so/my-integrations
# Windows:
start https://www.notion.so/my-integrations
# Linux:
xdg-open https://www.notion.so/my-integrations
```

**After the browser opens, display the following AskQuestion:**

```json
{
  "title": "Step 1: Create an integration",
  "questions": [{
    "id": "browser_status",
    "prompt": "Did the browser open? Follow these steps to create an integration:\n\n1. Log in to Notion\n2. Click the 'New integration' button\n3. Set the name to 'AIAgent Bootcamp'\n4. Select 'Internal' for the type\n5. Under Capabilities, check 'Read content', 'Update content', and 'Insert content'\n6. Click 'Submit'\n\nDid you create the integration?",
    "options": [
      {"id": "created", "label": "I created the integration!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "no_button", "label": "I can't find the 'New integration' button"},
      {"id": "login_issue", "label": "I can't log in to Notion"}
    ]
  }]
}
```

(created -> Proceed to Step 2)
(browser_not_open -> Guide: "Open this URL directly in your browser: https://www.notion.so/my-integrations")
(no_button -> Guide: "Wait for the page to fully load. When you visit https://www.notion.so/my-integrations while logged in to Notion, you'll see the 'New integration' button near the top right.")
(login_issue -> Guide: "If you don't have a Notion account, you can create one for free at https://www.notion.so/signup. If you already have an account, log in with your email address or Google account.")

---

## Automating with Chrome Integration (`/chrome` mode)

**Prerequisite:** The "Claude in Chrome" extension (v1.0.36+) must be installed in Chrome, and you must have launched with `claude --chrome` or run `/chrome` in the session.

**What the AI auto-runs with Chrome integration:**
1. Open https://www.notion.so/my-integrations in the browser
2. Use Chrome integration to perform the following operations in order:
   - Click the "New integration" button
   - Enter "AIAgent Bootcamp" in the Name field
   - Select the default workspace under Associated workspace
   - Select "Internal" for the Type
   - Check Read content, Update content, and Insert content under Capabilities
   - Click "Submit"
3. Once the Internal Integration Secret appears, tell the user "Click the Copy button next to the secret to copy it"
4. Proceed to Step 3

**Note:** Do not read the secret value from the browser screen. The user copies it manually.

If Chrome integration is not available, follow the instructions below manually.

---

## Step 2: Copy the API Key

**Message to display to the user:**

```text
After creating the integration, follow these steps to copy the API key:

1. The settings page for the created integration will be displayed
2. A token is shown in the "Internal Integration Secret" section
   (a string starting with secret_xxx)
3. Click the "Copy" button to copy the token

Do not paste the copied token in this chat.
In the next step, the AI will securely write it to the configuration file.
```

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Copy the API key",
  "questions": [{
    "id": "copy_status",
    "prompt": "Did you copy the Internal Integration Secret (the string starting with secret_xxx)?",
    "options": [
      {"id": "copied", "label": "I copied the API key!"},
      {"id": "no_secret", "label": "I can't find the token"},
      {"id": "help_capabilities", "label": "I don't understand the Capabilities settings"}
    ]
  }]
}
```

(copied -> Proceed to Step 3)
(no_secret -> Guide: "Click on the name of the integration you created from the integration list (https://www.notion.so/my-integrations) to go to its settings page. You'll find a token starting with secret_ in the 'Internal Integration Secret' section.")
(help_capabilities -> Guide: "On the integration settings page, go to the 'Capabilities' tab and check 'Read content', 'Update content', and 'Insert content'. This enables reading and writing pages via the API.")

---

## Step 3: Create the MCP Configuration File

**What the AI auto-runs:**

1. Determine the tool being used (Claude Code or Cursor)
2. Create the corresponding MCP configuration file with a placeholder
3. Have the user replace the placeholder with the API key

**MCP configuration file the AI creates:**

**For Claude Code:** `~/.claude/mcp_settings.json`
**For Cursor:** `~/.cursor/mcp.json` (home directory; do NOT write to `.cursor/mcp.json` inside the repository)

Configuration content (if `mcpServers` already exists, add the `notion` entry):
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "YOUR_NOTION_API_KEY_HERE"
      }
    }
  }
}
```

3. After the AI creates the file, display this message to the user:

```text
The MCP configuration file has been created. Please set the API key:

+-------------------------------------------------------------+
| Open the following file in a text editor:                    |
|                                                              |
| Claude Code: ~/.claude/mcp_settings.json                     |
| Cursor:      ~/.cursor/mcp.json                              |
|                                                              |
| Replace YOUR_NOTION_API_KEY_HERE in the file with            |
| the API key you copied (secret_xxx...).                      |
| After saving, come back to this chat.                        |
+-------------------------------------------------------------+

Do not paste the API key in this chat.
Editing the file directly in an editor keeps it out of chat logs.
```

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Create the MCP configuration file",
  "questions": [{
    "id": "config_status",
    "prompt": "Did you replace the API key in the MCP configuration file?",
    "options": [
      {"id": "done", "label": "I set the API key!"},
      {"id": "editor_help", "label": "I don't know how to open the file"},
      {"id": "existing_config", "label": "I already have a config file and want to know how to add to it"},
      {"id": "security_question", "label": "I have a question about security"}
    ]
  }]
}
```

(done -> AI reads the config file and checks that `YOUR_NOTION_API_KEY_HERE` is no longer present (without displaying the key value). If OK, proceed to Step 4)
(editor_help -> Guide: "Run the following in your terminal to open it in an editor: Mac: `open ~/.claude/mcp_settings.json` / Cursor: `code ~/.cursor/mcp.json`. Or show hidden files in Finder/Explorer and open the file.")
(existing_config -> Read the existing file content and guide on adding the `notion` entry to `mcpServers`. Preserve other existing MCP server configurations)
(security_question -> Explain: "The MCP configuration file is in your home directory and is not included in the Git repository. The API key is stored only in this file and is passed as an environment variable when the MCP server starts.")

---

## Step 4: Share the Integration with Pages

**Important: If you skip this step, the MCP will not be able to access your Notion pages.**

**Message to display to the user:**

```text
The Notion API requires you to explicitly specify which pages the integration can access.
Follow these steps to share the integration with the pages you want to access:

+-------------------------------------------------------------+
| 1. Open the Notion page you want to access                   |
| 2. Click the "..." (three-dot menu) at the top right         |
| 3. Select "Add connections"                                  |
| 4. Type "AIAgent Bootcamp" in the search field               |
| 5. Click on the integration name that appears                |
| 6. Click "Confirm" in the confirmation dialog                |
|                                                              |
| * Sharing a parent page automatically applies to child pages |
| * To access multiple pages, either repeat this for each page |
|   or set it on a common parent page                          |
+-------------------------------------------------------------+
```

**AskQuestion configuration:**
```json
{
  "title": "Step 4: Share the integration with pages",
  "questions": [{
    "id": "share_status",
    "prompt": "Did you share the integration with your Notion page?",
    "options": [
      {"id": "shared", "label": "I set up sharing!"},
      {"id": "no_connection", "label": "I can't find 'Add connections'"},
      {"id": "no_integration", "label": "The integration name doesn't appear"},
      {"id": "skip_share", "label": "I'll set it up later (skip)"}
    ]
  }]
}
```

(shared -> Proceed to Step 5)
(no_connection -> Guide: "Open the '...' menu at the top right of the page, and you'll find 'Add connections' near the bottom. If you can't find it, check that you have owner permissions for the page. It doesn't appear with guest permissions.")
(no_integration -> Guide: "It may take a moment for the integration to appear right after creation. Reload the page and try again. If it still doesn't appear, check that the integration was correctly created at https://www.notion.so/my-integrations.")
(skip_share -> Guide: "You can set this up later. This setting is needed when accessing pages via MCP. Please configure it before using Notion in /start-12-1." then proceed to Step 5)

---

## Step 5: MCP Connection Test

**What the AI does:**

1. Guide the user to restart Claude Code / Cursor:

```text
You need to restart the tool to apply the MCP settings.

For Claude Code:
  -> Exit with exit, then start claude again

For Cursor:
  -> Press Cmd+Shift+P (Mac) / Ctrl+Shift+P (Windows) to open
    the Command Palette and run "Reload Window"
```

**AskQuestion configuration:**
```json
{
  "title": "Step 5: MCP Connection Test",
  "questions": [{
    "id": "restart_status",
    "prompt": "Did you restart the tool?",
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
   - Check if the Notion MCP tool is available
   - If available: retrieve the Notion page list to confirm a successful connection
   - Display "Retrieved X pages from Notion. The MCP connection is working."

**On success:**
```text
Notion MCP setup is complete!

Test result: Successfully connected to Notion via the MCP server.
You can now operate Notion pages and databases directly from Claude Code/Cursor.
```

**On failure - AskQuestion:**
```json
{
  "title": "Test Result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the MCP connection test. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Run the test again"},
      {"id": "check_config", "label": "Check the MCP configuration file"},
      {"id": "recheck_key", "label": "Recheck the API key (go back to Step 1)"},
      {"id": "show_error", "label": "I want to see the error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(check_config -> Check the MCP configuration file content. Verify that NOTION_API_KEY is not still the placeholder and that the JSON syntax is correct)
(recheck_key -> Go back to Step 1)
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
      {"id": "trouble_mcp_start", "label": "The MCP server won't start"},
      {"id": "trouble_invalid", "label": "I get a 'token_invalid' error"},
      {"id": "trouble_permissions", "label": "I get an 'insufficient_permissions' error"},
      {"id": "trouble_not_found", "label": "I get an 'object_not_found' error"},
      {"id": "trouble_npx", "label": "The npx command is not found"},
      {"id": "trouble_cost", "label": "I'm worried about costs"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Trouble 1: MCP Server Won't Start
**Cause**: Node.js is not installed, npx is unavailable, or the MCP config file JSON is malformed
**What the AI does**:
1. Check Node.js existence and version (18 or higher required) with `node --version`
2. Check if npx is available with `npx --version`
3. Validate the MCP config file JSON (syntax check with `python -m json.tool`)
4. If Node.js is not installed: guide "Please install the LTS version from https://nodejs.org/"

### Trouble 2: "token_invalid" Error
**Cause**: The API key was not copied correctly, or the key is invalid
**What the AI does**:
1. Check the MCP config file (only verify it starts with `secret_`, without displaying the key value)
2. Check if it's still the placeholder (`secret_your_token_here`)
3. If there's an issue: guide "Regenerate the token at https://www.notion.so/my-integrations, then update the MCP config file"

### Trouble 3: "insufficient_permissions" Error
**Cause**: Integration Capabilities settings are insufficient, or the page is not shared
**What the AI does**:
1. Guide: "Check the integration's Capabilities at https://www.notion.so/my-integrations. Are Read content / Update content / Insert content checked?"
2. Guide: "Is the integration shared with the target Notion page? Please re-check the Step 4 instructions."

### Trouble 4: "object_not_found" Error
**Cause**: The target page does not have the integration shared
**AI guidance**: "The integration is not shared with the Notion page you want to access via the API. Follow the Step 4 instructions to add the integration from the page's 'Add connections'. Adding it to a parent page also applies to child pages."

### Trouble 5: npx Command Not Found
**Cause**: Node.js is not installed, or PATH is not configured
**What the AI does**:
1. Check with `node --version`. If not installed, guide to https://nodejs.org/
2. If installed but a PATH issue, guide on specifying the full path (`/usr/local/bin/npx`) in the config file

### Trouble 6: Cost Concerns
**AI guidance**: "Notion itself is available on a free plan. There are no additional costs for API usage. All API features are available on the free plan. The Notion MCP server (@notionhq/notion-mcp-server) is also free and open source."

### Trouble 7: Other Errors
**What the AI does**: Check the error message content, identify the cause, and guide to a solution

---

## Checkpoint
- [ ] Created an integration (AIAgent Bootcamp) on the Notion Integrations page
- [ ] Copied the Internal Integration Secret (secret_xxx)
- [ ] Added the Notion server configuration to the MCP configuration file
- [ ] Shared the integration with the Notion pages you want to access
- [ ] Restarted Claude Code / Cursor
- [ ] MCP connection test succeeded (was able to access Notion pages)

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Notion MCP setup is complete! What would you like to do next?",
    "options": [
      {"id": "try_notion_mcp", "label": "Try Notion MCP operations (/start-12-1)"},
      {"id": "try_notion_db", "label": "Operate Notion databases (/start-12-2)"},
      {"id": "setup_other", "label": "Set up other APIs too (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- try_notion_mcp -> Guide to /start-12-1
- try_notion_db -> Guide to /start-12-2
- setup_other -> Guide to /start-0-1
- finish -> End

---

## Completion

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-notion` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "Next, try Notion MCP operations with `/start-12-1`"

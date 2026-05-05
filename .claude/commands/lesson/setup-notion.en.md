---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Have a Notion account (free plan OK)", "Browser available", "Node.js 18 or higher"]
level: "beginner"
tags: ["setup", "notion", "ncli", "mcp", "oauth"]
---

# Notion CLI (ncli) + Hosted MCP Setup (OAuth-only)

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-notion` to display progress
2. Auto-detect existing configuration:
   - Run `which ncli` to check if ncli is already installed
   - For Claude Code: check if a `notion` server is defined in `~/.claude/mcp_settings.json`
   - For Cursor: check if a `notion` server is defined in `~/.cursor/mcp.json`
   - If ncli is installed and MCP is configured, you can just run Step 6 (connection test) and mark it complete

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Connect ncli (Notion CLI) and Notion's official Hosted MCP via **OAuth**, so you can operate Notion from the terminal and from MCP-aware tools |
| Duration | ~10 minutes |
| Prerequisites | Notion account (free plan OK), Node.js 18 or higher, browser |
| Skill Level | No CLI commands needed (everything is auto-run by AI + a single browser-based OAuth approval) |
| Auth Method | **This setup uses OAuth only** (no API keys required).<br>Note: a few legacy scripts (e.g. `tools/run_lesson_14_11.py`) still require `NOTION_API_KEY`. See `.env.example` for details. |

**Session flow:**
1. Install ncli (@sakasegawa/ncli) (AI auto-runs)
2. Run `ncli login` and approve Notion's OAuth in the browser
3. Verify with `ncli whoami` / `ncli search`
4. Add Notion Hosted MCP (OAuth) to your MCP configuration file (AI writes it automatically)
5. Restart Claude Code / Cursor and approve the OAuth dialog on first use
6. MCP connection test

> **Why Hosted MCP + OAuth?** The legacy Internal Integration Token flow forced you to create an integration in Notion and individually share each page via "Add connections". With OAuth, a single browser login grants workspace-wide access, so **for this Hosted MCP flow** per-page sharing is **not required**. If you still need to run legacy scripts that read `NOTION_API_KEY` directly (e.g. `tools/run_lesson_14_11.py`), keep using an Internal Integration Token alongside this OAuth setup.

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
      {"id": "which_tool", "label": "I want to confirm whether I'm using Claude Code or Cursor"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(check_prereq -> Guide: "You're ready if you have a Notion account (free plan OK), can log in via your browser, and have Node.js 18 or higher installed.")
(which_tool -> Explain: "The MCP configuration file location differs between Claude Code and Cursor. Step 4 will guide you through the steps for each.")
(different_lesson -> Display module list)

---

## Step 1: Install ncli (Notion CLI)

**What the AI does:**
1. Check Node.js version: `node --version` (18 or higher required)
2. Check if ncli is already installed: `which ncli`
3. If not installed, run the following command:

```bash
npm install -g @sakasegawa/ncli
```

4. After installation, verify with `ncli --version`

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Install ncli",
  "questions": [{
    "id": "ncli_status",
    "prompt": "ncli installation has been executed. Please check the result.",
    "options": [
      {"id": "installed", "label": "Installed successfully!"},
      {"id": "npm_error", "label": "Got an error with npm install"},
      {"id": "no_node", "label": "Node.js is not installed"},
      {"id": "command_not_found", "label": "ncli command not found"}
    ]
  }]
}
```

(installed -> Proceed to Step 2)
(npm_error -> Run `npm cache clean --force` and retry. If it's a permissions error, guide to `sudo npm install -g @sakasegawa/ncli`)
(no_node -> Guide: "Please install the LTS version (18 or higher) from https://nodejs.org/")
(command_not_found -> Check installation with `npm list -g @sakasegawa/ncli`. If it's a PATH issue, check with `npm bin -g` and guide on adding it to PATH)

---

## Step 2: Log in to Notion via OAuth using ncli

**What the AI does:**
1. Run the following in the terminal:

```bash
ncli login
```

2. ncli automatically opens the browser to Notion's OAuth screen
3. The user follows the on-screen flow:
   - Log in to Notion (if not already)
   - Select the workspace to grant access to
   - Click "Allow access"
4. On success, the terminal shows a message like "Logged in as ..."

**Message to display to the user:**

```text
The Notion OAuth screen has opened in your browser.

1. If you're not logged in to Notion, log in
2. Select the workspace you want to grant access to
3. Click "Allow access" to approve

After approval, the browser tab closes automatically and the terminal shows a successful login message.

No API key (secret_xxx) input is needed. Everything is completed via the browser-based OAuth flow.
```

**AskQuestion configuration:**
```json
{
  "title": "Step 2: OAuth login to Notion",
  "questions": [{
    "id": "login_status",
    "prompt": "Is the OAuth flow for ncli login complete?",
    "options": [
      {"id": "logged_in", "label": "Logged in successfully!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "login_denied", "label": "I can't log in to Notion / approval failed"},
      {"id": "wrong_workspace", "label": "I approved the wrong workspace"}
    ]
  }]
}
```

(logged_in -> Proceed to Step 3)
(browser_not_open -> Guide: "Look for an OAuth URL printed in the terminal. Copy and paste it into your browser manually.")
(login_denied -> Guide: "If you don't have a Notion account, you can create one for free at https://www.notion.so/signup. If approval errors out, run `ncli login` again to retry.")
(wrong_workspace -> Guide: "Run `ncli logout` first, then `ncli login` again and select the correct workspace.")

---

## Step 3: Verify ncli (whoami / search)

**What the AI does:**
1. Verify the current login state:

```bash
ncli whoami
```

2. Smoke-test workspace search (success means at least one or two results come back):

```bash
ncli search ""
```

Or specify a keyword:

```bash
ncli search "test"
```

3. If results show up, OAuth has correctly granted workspace-wide access

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Verify ncli",
  "questions": [{
    "id": "smoke_test",
    "prompt": "Did the whoami / search commands return expected results?",
    "options": [
      {"id": "ok", "label": "My user shows up and search returns results"},
      {"id": "whoami_fail", "label": "whoami says I'm not logged in"},
      {"id": "search_empty", "label": "Search returned 0 results"},
      {"id": "other_error", "label": "Some other error appeared"}
    ]
  }]
}
```

(ok -> Proceed to Step 4)
(whoami_fail -> Guide: "Run `ncli login` again. If you switch between multiple Notion accounts, run `ncli logout` first to be safe.")
(search_empty -> Guide: "Zero results just means there are no pages in the workspace. Create one test page in Notion and try `ncli search` again.")
(other_error -> Inspect the error message and guide on the cause)

---

## Step 4: Add Notion Hosted MCP (OAuth) to your MCP configuration file

Notion's official Hosted MCP is hosted at `https://mcp.notion.com/mcp` and uses Streamable HTTP + OAuth. You do **not** put any tokens or env vars in the configuration.

**What the AI auto-runs:**

1. Determine the tool being used (Claude Code or Cursor)
2. Add a `notion` entry to the MCP configuration file (preserve any existing `mcpServers`)

**MCP configuration file the AI writes to:**

**For Claude Code:** `~/.claude/mcp_settings.json`
**For Cursor:** `~/.cursor/mcp.json` (home directory; do NOT write to `.cursor/mcp.json` inside the repository)

Configuration content (if `mcpServers` already exists, add the `notion` entry):
```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

**Important:**
- Do **not** include `command` / `args` / `env` (this is a Hosted MCP; it doesn't run locally)
- Do **not** set `NOTION_TOKEN` or any other secret (OAuth handles auth)
- `type` must be `http` (Streamable HTTP)

**AskQuestion configuration:**
```json
{
  "title": "Step 4: Create the MCP configuration file",
  "questions": [{
    "id": "config_status",
    "prompt": "Did you add the Notion entry to the MCP configuration file?",
    "options": [
      {"id": "done", "label": "Added it!"},
      {"id": "editor_help", "label": "I don't know where the file is"},
      {"id": "existing_config", "label": "I already have other MCP servers configured and want to know how to add this one"},
      {"id": "security_question", "label": "I have a question about OAuth security"}
    ]
  }]
}
```

(done -> AI reads the configuration file and verifies the `notion` entry has `type: "http"` and `url: "https://mcp.notion.com/mcp"`, with no `NOTION_TOKEN` or `command` mixed in. If OK, proceed to Step 5)
(editor_help -> Guide: "On macOS, run `open ~/.claude/mcp_settings.json` or `open ~/.cursor/mcp.json`. If the file doesn't exist yet, create it.")
(existing_config -> Read the existing file content and add the `notion` entry to the `mcpServers` object, preserving other server configurations)
(security_question -> Explain: "The Hosted MCP is operated by Notion themselves and authentication uses browser-based OAuth. Tokens are never stored in your configuration file - they're managed in your tool's secure auth store (Claude Code / Cursor).")

---

## Step 5: Restart the tool and approve the OAuth dialog

**Message the AI displays:**

```text
You need to restart the tool to apply the MCP settings.

For Claude Code:
  -> Exit with exit, then start claude again

For Cursor:
  -> Press Cmd+Shift+P (Mac) / Ctrl+Shift+P (Windows) to open
    the Command Palette and run "Reload Window"

After restarting, the first time a Notion MCP tool is invoked,
your browser will open Notion's OAuth approval dialog.
Click "Allow access" to approve.
(Once approved, the session is kept logged in automatically.)
```

**AskQuestion configuration:**
```json
{
  "title": "Step 5: Restart and OAuth approval",
  "questions": [{
    "id": "restart_status",
    "prompt": "Did you restart the tool?",
    "options": [
      {"id": "restarted", "label": "Restarted! On to the test"},
      {"id": "how_restart", "label": "I don't know how to restart"},
      {"id": "no_oauth_dialog", "label": "The OAuth dialog isn't appearing"}
    ]
  }]
}
```

(restarted -> Proceed to Step 6)
(how_restart -> Re-explain the per-tool restart steps)
(no_oauth_dialog -> Guide: "The dialog opens the **first time** you invoke an MCP tool. Run the Step 6 test and it should appear automatically. If still nothing, check the tool's logs (Claude Code: `claude --debug`; Cursor: the MCP section of the Output panel).")

---

## Step 6: MCP Connection Test

**What the AI does:**

1. Check that Notion MCP tools (e.g., `notion-search`, `notion-fetch`) are available
2. Issue a simple request to fetch information from the workspace
3. On first run, the browser opens an OAuth approval dialog - have the user approve it
4. Display "Retrieved N pages from Notion. The MCP connection is working."

**On success:**
```text
Notion Hosted MCP setup is complete!

Test result: Successfully connected to Notion via the MCP server.
You can now operate Notion pages and databases directly from Claude Code/Cursor.
```

**On failure - AskQuestion:**
```json
{
  "title": "Test Result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the MCP connection test. Let's check the cause.",
    "options": [
      {"id": "retry", "label": "Run the test again"},
      {"id": "check_config", "label": "Check the MCP configuration file"},
      {"id": "reauth", "label": "Re-approve OAuth"},
      {"id": "show_error", "label": "I want to see the error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test. If the OAuth dialog appears, have the user approve it)
(check_config -> Verify the config file: `type: "http"` and `url: "https://mcp.notion.com/mcp"`, and that the JSON is valid)
(reauth -> Guide the user to clear the Notion auth state from the tool's auth store and restart. Claude Code: e.g., `claude mcp logout notion`)
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
      {"id": "trouble_oauth_fail", "label": "OAuth approval fails"},
      {"id": "trouble_mcp_no_response", "label": "No response from the MCP server"},
      {"id": "trouble_no_pages", "label": "Can't fetch pages (wrong workspace selected)"},
      {"id": "trouble_ncli_login", "label": "ncli login isn't working"},
      {"id": "trouble_cost", "label": "I'm worried about costs"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Trouble 1: OAuth approval fails
**Cause**: Pop-ups are blocked in the browser, or the user cancelled the Notion approval
**What the AI does**:
1. Ask the user to allow pop-ups / redirects in the browser
2. Run `ncli login` again, or re-invoke the MCP tool to retry OAuth
3. If it still fails, log out of Notion in the browser and try again

### Trouble 2: No response from the MCP server
**Cause**: Misconfigured MCP file, tool not restarted, or `https://mcp.notion.com` blocked on the network
**What the AI does**:
1. Verify the MCP config (`type: "http"`, `url: "https://mcp.notion.com/mcp"`)
2. Validate JSON syntax (Claude Code: `python -m json.tool ~/.claude/mcp_settings.json` / Cursor: `python -m json.tool ~/.cursor/mcp.json`)
3. Fully restart the tool (Claude Code / Cursor)
4. Check reachability with `curl -I https://mcp.notion.com/mcp`

### Trouble 3: Can't fetch pages
**Cause**: Wrong workspace selected during OAuth approval
**What the AI does**:
1. Run `ncli logout` -> `ncli login` and pick the correct workspace
2. On the MCP side, log out of Notion in the tool's auth store and re-authenticate

### Trouble 4: ncli login isn't working
**Cause**: Node.js too old, ncli outdated, or the local OAuth listener port is in use
**What the AI does**:
1. Verify Node.js >= 18 with `node --version`
2. Update with `npm install -g @sakasegawa/ncli@latest`
3. If a port conflict, stop other local servers (especially dev servers) and retry

### Trouble 5: Cost concerns
**AI guidance**: "Notion itself is available on the free plan, and there are no additional costs for OAuth-based API usage. Notion's official Hosted MCP (`mcp.notion.com`) is **also free as of now**, but per-tool availability can depend on your Notion plan (Free / Plus / Business / Enterprise) and whether Notion AI is enabled. Always check the official [MCP supported tools docs](https://developers.notion.com/docs/mcp-supported-tools) and the [Notion pricing page](https://www.notion.com/pricing) for the latest scope. ncli (@sakasegawa/ncli) is open-source and free."

### Trouble 6: Other errors
**What the AI does**: Inspect the error message, identify the cause, and guide on a solution

---

## Checkpoint
- [ ] ncli (@sakasegawa/ncli) is installed
- [ ] `ncli login` browser OAuth is complete
- [ ] `ncli whoami` shows the logged-in user
- [ ] `ncli search` returns pages from the workspace
- [ ] MCP configuration file has a `notion` entry (`type: http`, `url: https://mcp.notion.com/mcp`)
- [ ] Restarted Claude Code / Cursor
- [ ] MCP connection test succeeded (after OAuth approval, can access Notion pages)

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

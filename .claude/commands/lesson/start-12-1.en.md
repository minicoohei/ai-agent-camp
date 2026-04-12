---
description: "When the user says /start-12-1 — Module 12 Lesson 12-1: Notion API Connection and Authentication"
chapter: "courses/aiagent/lesson03-core/module12-notion"
duration: "~30 min"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["notion", "mcp", "api"]
---

# 🎓 Lesson 12-1: Notion API Connection

## 📍 What You'll Do

**Lesson 12-1: Notion API Fundamentals**!

| Item | Details |
|------|------|
| Goal | Operate Notion pages and databases from Claude Code using MCP/Notion API |
| Duration | ~30 min |
| Skills used | Notion API, MCP (Model Context Protocol) |
| Prerequisites | Notion account, integration creation permissions |
| Course page | [Module 12: Notion](https://ai-agent.camp/en/course/module-12)  alongside this lesson |

**Session flow:**
1. Create a Notion integration
2. Obtain the API key and database ID
3. Read and write pages and databases

By the end of this session, you will be able to operate Notion from Claude Code.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite verification)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Create Notion Integration

**Prerequisite:** The Notion MCP server must be configured.
If not configured, run `/setup-notion` first.

**What the AI automatically verifies:**
1. Verify that the `notion` server is defined in the MCP config file:
   - Claude Code: Read `~/.claude/mcp_settings.json` and verify `mcpServers.notion` exists
   - Cursor: Read `.cursor/mcp.json` and verify `mcpServers.notion` exists
2. If already configured -> proceed to Step 2 (MCP config file creation)
3. If not configured -> guide to run `/setup-notion`

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Verify Notion Integration",
  "questions": [{
    "id": "step_action",
    "prompt": "Check NOTION_API_KEY configuration status.",
    "options": [
      {"id": "check", "label": "Check configuration status"},
      {"id": "setup_notion", "label": "Set up with /setup-notion"},
      {"id": "skip", "label": "Skip (if already configured)"}
    ]
  }]
}
```

(check → Verify the notion entry in the MCP config file. If configured, proceed to Step 2)
(setup_notion → Guide to run /setup-notion)
(skip → Proceed to Step 2)

---

## 🚀 Step 2: Create MCP Configuration File

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Create MCP Configuration File",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please create the MCP configuration file for Claude Code.

File: ~/.claude/mcp_settings.json

Content (replace NOTION_API_KEY with your actual token):
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": [
        "-y",
        "@notionhq/notion-mcp-server"
      ],
      "env": {
        "NOTION_API_KEY": "secret_your_token_here"
      }
    }
  }
}

Please create the file.
```

**Expected result:** The MCP config file is created. Replace the actual token manually.

---

## 🚀 Step 3: Grant Workspace Access Permission

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Grant Workspace Access Permission",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please explain how to grant access permissions to the integration in Notion.

Steps:
1. Open a page in Notion
2. Top-right "..." menu > Connections
3. Add the created integration "Claude MCP Integration"

Note: Only pages under the page where the integration is added will be accessible.
```

**Expected result:** The procedure for configuring access permissions to Notion pages is explained.

---

## 🚀 Step 4: Connection Test

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Connection Test",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
We will perform a Notion MCP connection test.

Please verify the following:
1. The MCP configuration file (~/.claude/mcp_settings.json) exists
2. NOTION_API_KEY is configured
3. Restart Claude Code and verify MCP is loaded

As a connection test, connect to Notion and list the accessible pages.
```

**Expected result:** If MCP is configured correctly, a list of Notion pages is displayed.

---

## 🚀 Step 5: Basic Operations Test

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Basic Operations Test",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Please test the following operations in Notion:

1. Page creation test:
   - Create a page named "MCP Connection Test"
   - Write "MCP connection test from Claude Code successful!" as content
   - Also add the current time

2. Page read test:
   - Read and display the content of the created page

3. Page update test:
   - Append "Updated: [current time]" to the page

Please report the results of each operation.
```

**Expected result:** Creating, reading, and updating Notion pages can be done from Claude Code.

---

## ⚠️ Common Issues and Solutions

Use AskQuestion to select the issue, then follow the guidance.

**AskQuestion configuration:**
```json
{
  "title": "Select the issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "Could not connect to Notion"},
      {"id": "trouble_2", "label": "Insufficient permissions"},
      {"id": "trouble_3", "label": "MCP server does not start"},
      {"id": "trouble_4", "label": "Page not found"}
    ]
  }]
}
```


### Issue 1: "Could not connect to Notion"
**Cause:** API key is incorrect or the MCP config file path is wrong
**Solution prompt:**
```
Please verify the following:
1. The path ~/.claude/mcp_settings.json is correct
2. The NOTION_API_KEY value starts with "secret_"
3. The JSON syntax is correct (commas, brackets, etc.)
```

### Issue 2: "Insufficient permissions"
**Cause:** Integration has not been added to the page
**Solution prompt:**
```
Open the target page in Notion, and check from the top-right "..." > Connections
whether "Claude MCP Integration" has been added.
Adding the integration to a parent page also grants access to child pages.
```

### Issue 3: MCP server does not start
**Cause:** Node.js version is outdated or npx is unavailable
**Solution prompt:**
```
Please verify the following:
1. Check that node --version is v18 or higher
2. Check that npx is available with npx --version
3. Install npx with npm install -g npx
```

### Issue 4: Page not found
**Cause:** Integration does not have access permissions
**Solution prompt:**
```
In the Notion workspace, add the integration to the page
or parent page you want to access.
To grant access to the entire workspace, add it to the top-level page.
```

---

## ✅ Checkpoint
- [ ] Notion integration has been created
- [ ] Secret token has been obtained
- [ ] MCP config file has been created
- [ ] Integration has been added to the Notion page
- [ ] Can create, read, and update pages

---

## ✅ Completion Check
Paste the following into chat to verify completion:

```
# Completion check: Please verify that the expected output files have been generated in the output/ folder.
```

**Expected result:** Completion/incomplete status and missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin a new section.

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-12-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-12-2
- finish → End

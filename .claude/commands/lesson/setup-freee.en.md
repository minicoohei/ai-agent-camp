---
description: "Lesson command — Freee MCP setup"
duration: "~30 min"
prerequisites: ["Freee MCP account"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-20"]
---

# /setup-freee -- Freee MCP setup

> Connect to freee Accounting via MCP. Requires browser OAuth + Client ID/Secret.

**Highlight**: Freee Developer App + browser OAuth login required

## Setup steps

1. Create an app in the freee Developer Portal

   ```bash
   https://app.secure.freee.co.jp/developers/applications
   ```

2. Save Client ID / Client Secret — `(browser only)`

3. Install freee-mcp (pinned) — `npm install -g freee-mcp@0.26.0`

4. Register the MCP — `claude mcp add --transport stdio freee -- npx freee-mcp@0.26.0`

5. Authorise via the OAuth browser flow — `follow the MCP prompts`

## Gotchas

- Get your company ID via `freee_get_companies` → save to `~/.config/freee-mcp/config.json`
- Sandbox vs production apps are separate. Test in sandbox first, then swap to a production app

## Non-interactive mode

Browser OAuth is mandatory — cannot complete under `claude -p` / `cursor-agent --print`. Re-run in interactive mode.

## Related slides

- aiagent-course Module 20: see slide deck for the full visual walkthrough

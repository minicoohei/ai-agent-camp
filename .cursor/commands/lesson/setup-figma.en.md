---
description: "Lesson command — Figma + Serendie design-system MCP setup"
duration: "~20 min"
prerequisites: ["Figma + Serendie MCP account"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-21"]
---

# /setup-figma -- Figma + Serendie design-system MCP setup

> Wire the official Figma plugin (the writer) and Serendie MCP (the knowledge source).

**Highlight**: No PAT needed — OAuth browser login does it all

## Setup steps

1. Install the Figma plugin into Claude Code — `/plugin install figma@claude-plugins-official`

2. Sign in to Figma via OAuth — `/mcp → figma → Authenticate → 'Allow Access' in the browser`

3. Add the Serendie MCP — `claude mcp add --transport http serendie-mcp https://serendie.design/mcp`

4. Verify — `claude mcp list`

5. Bring the Serendie UI Kit into your Figma team

   ```bash
   https://www.figma.com/community/file/1433690846108785966
   ```

## Gotchas

- You can't 'Publish library' until you move the Serendie UI Kit from Community into your team
- On enterprise Figma accounts, an admin has to approve the app first

## Non-interactive mode

Browser OAuth is mandatory — cannot complete under `claude -p` / `cursor-agent --print`. Re-run in interactive mode.

## Related slides

- aiagent-course Module 21: see slide deck for the full visual walkthrough

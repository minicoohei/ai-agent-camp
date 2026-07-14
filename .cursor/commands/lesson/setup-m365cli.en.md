---
description: "Lesson command — M365 CLI setup"
duration: "~20 min"
prerequisites: ["Microsoft 365 CLI (PnP CLI) account"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "module-19"]
---

# /setup-m365cli -- M365 CLI setup

> Drive Microsoft 365 (Outlook / SharePoint / Teams) from one CLI: `@pnp/cli-microsoft365`. Device-code auth, nothing else.

**Highlight**: No PAT required — OAuth device code only

## Setup steps

1. Confirm Node.js 18+ — `node -v`

2. Install @pnp/cli-microsoft365 (pinned) — `npm install -g @pnp/cli-microsoft365@7.x`

3. Sign in via device code

   ```bash
   m365 login
# Open the printed URL in your browser and enter the code
   ```

4. Verify — `m365 status`

## Gotchas

- Avoid running `m365 logout` if you want to stay signed in — the token persists until it expires
- On WSL, open the URL in your Windows browser (the CLI doesn't auto-launch a browser there)

## Non-interactive mode

Browser interaction is required, so `-p` mode runs only the read-only checks then writes a `setup-resume.md` and exits.

## Related slides

- aiagent-course Module 19: see slide deck for the full visual walkthrough

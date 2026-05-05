---
description: "Lesson command — Discord Bot + claude-channel-discord MCP setup"
duration: "~30 min"
prerequisites: ["Discord account", "Bun or Node.js 18+"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "discord", "mcp", "module-22"]
---

# /setup-discord -- Discord Bot + claude-channel-discord MCP setup

## Goal

Create a Discord Bot in the Developer Portal and connect Claude Code to it
through the `claude-channel-discord` MCP. Mirrors aiagent-course Module 22.

> **Non-interactive note**: This command requires browser actions and a token
> paste. Under `claude -p` / `cursor-agent --print` it cannot finish — the
> `nonInteractiveMode: deferred` declaration tells the AI to emit a
> `setup-resume.md` checklist and stop.

---

## Step 0: detect existing setup

The AI should:

1. Check `~/.claude/mcp_settings.json` and `<project>/.mcp.json` for a `discord` entry.
2. Verify `bunx claude-channel-discord@0.0.4 --version` (or `npx ...`) is reachable.
3. Confirm Keychain has `DISCORD_BOT_TOKEN` via `security find-generic-password
   -s DISCORD_BOT_TOKEN 2>&1 | head -3` (do NOT print the value).

If everything is set, jump to **Step 5 (smoke test)**.

---

## Step 1: create the bot in Developer Portal

Open <https://discord.com/developers/applications>.

1. **New Application** → name it (e.g. `AI Agent Camp Demo`) → **Create**.
2. Sidebar **Bot** → **Reset Token** → copy the token immediately into a password manager.
3. Enable both **Privileged Gateway Intents**: `SERVER MEMBERS INTENT` and `MESSAGE CONTENT INTENT`.

---

## Step 2: invite the bot

OAuth2 → URL Generator → scopes `bot` + `applications.commands` → bot permissions
(Read / Send Messages, Add Reactions, Manage Messages) → open the URL → choose
your server.

---

## Step 3: store the token in Keychain

```bash
security add-generic-password -a "$USER" -s DISCORD_BOT_TOKEN -w '<paste-token>'
echo 'export DISCORD_BOT_TOKEN="$(security find-generic-password -s DISCORD_BOT_TOKEN -w 2>/dev/null)"' >> ~/.zshrc
```

---

## Step 4: register the MCP

```bash
bun install -g claude-channel-discord@0.0.4
claude mcp add --transport stdio discord -- bun x claude-channel-discord@0.0.4
claude mcp list
```

Expected: `discord (stdio): ... ✓ connected`.

---

## Step 5: lock down access policy

```bash
/discord:access set --dm-policy allowlist
/discord:access approve <your-discord-user-id>
/discord:access list
```

---

## Step 6: smoke test

In Claude Code: `Send "Hello from MCP" as a DM to me on Discord`. If the DM
arrives, you're done.

---

## Common gotchas (mirrors Module 22 slide)

| Symptom | Cause | Fix |
|---|---|---|
| Token stops working | Old token after `Reset Token` | Reset again, update Keychain |
| Messages can't be read | `MESSAGE CONTENT INTENT` off | Toggle on, restart MCP |
| Cross-user DMs not visible | Discord API limit | Use private ticket channels |
| Cannot DM cold prospects | No DM channel exists | They must DM the bot first |

---

## Non-interactive behavior

`nonInteractiveMode: deferred` — under `-p` only Step 0 runs; everything else
is written to `setup-resume.md` for an interactive resume. See
`_lib/non-interactive.md` for the shared spec.

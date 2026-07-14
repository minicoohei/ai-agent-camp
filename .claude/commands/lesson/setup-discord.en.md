---
description: "Lesson command — Discord Bot + official Claude Code Channels plugin setup"
duration: "~30 min"
prerequisites: ["Discord account", "Claude Code", "Bun"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "discord", "plugin", "module-22"]
---

# /setup-discord -- Discord Bot + official Claude Code Channels plugin setup

## Goal

Create a Discord Bot in the Developer Portal and launch it as a Claude Code
Channel through the official `discord@claude-plugins-official` plugin. Mirrors
aiagent-course Module 22.

> **Non-interactive note**: This command requires browser actions, a token
> paste, and Claude Code plugin commands. Under `claude -p` /
> `cursor-agent --print` it cannot finish; `nonInteractiveMode: deferred`
> tells the AI to emit a `setup-resume.md` checklist and stop.

---

## Step 0: detect existing setup

The AI should:

1. Guide the learner to check whether `discord@claude-plugins-official` is installed in Claude Code.
2. Confirm `~/.claude/channels/discord/.env` contains `DISCORD_BOT_TOKEN` without printing the value.
3. Ask the learner to run `/discord:access` inside Claude Code to inspect access state.

If everything is set, jump to **Step 6 (smoke test)**.

---

## Step 1: create the bot in Developer Portal

Open <https://discord.com/developers/applications>.

1. **New Application** → name it (for example, `AI Agent Camp Demo`) → **Create**.
2. Sidebar **Bot** → **Reset Token** → copy the token immediately into a password manager.
3. Under **Privileged Gateway Intents**, enable only `MESSAGE CONTENT INTENT`.

MESSAGE CONTENT INTENT is required so the bot can read message text.

---

## Step 2: invite the bot

1. Open **OAuth2** → **URL Generator**.
2. Select the `bot` scope.
3. Under **Bot Permissions**, select the minimum permissions:
   - `View Channels`
   - `Send Messages`
   - `Send Messages in Threads`
   - `Read Message History`
   - `Attach Files`
4. Set **Integration type** to **Guild Install**.
5. Open the generated URL and add the bot to your server.

---

## Step 3: install the official Discord plugin

Start Claude Code and run these commands inside Claude Code:

```text
/plugin install discord@claude-plugins-official
/reload-plugins
```

After reloading plugins, configure the bot token in the same Claude Code session:

```text
/discord:configure <paste-bot-token>
```

This writes `DISCORD_BOT_TOKEN` to `~/.claude/channels/discord/.env`. Do not paste
the token into normal chat or logs.

---

## Step 4: launch Claude Code with Channels

Exit Claude Code, then start it from the terminal:

```bash
claude --channels plugin:discord@claude-plugins-official
```

The Discord channel does not run from normal server registration. Always launch
with `--channels plugin:discord@claude-plugins-official`.

---

## Step 5: configure access control

Pairing captures your Discord user ID. Keep Claude Code running with the Step 4
launch command, then DM the bot from Discord. When the bot replies with a
6-character pairing code, run this inside Claude Code:

```text
/discord:access pair <code>
/discord:access policy allowlist
/discord:access
```

If you already know a user's Discord snowflake, add it manually:

```text
/discord:access allow <snowflake>
/discord:access
```

For production use, switch to `allowlist` after adding the needed users so
unknown DM senders do not receive pairing-code replies.

---

## Step 6: smoke test

With Claude Code running as:

```bash
claude --channels plugin:discord@claude-plugins-official
```

DM the bot from Discord and confirm the notification reaches Claude Code and the
bot can reply. If nothing happens, run `/discord:access` to inspect the allowlist
and pending pairings.

---

## Common gotchas (mirrors Module 22 slide)

| Symptom | Cause | Fix |
|---|---|---|
| Token stops working | Old token after `Reset Token` | Reset again, then run `/discord:configure <paste-bot-token>` |
| Messages can't be read | `MESSAGE CONTENT INTENT` off | Toggle it on and relaunch with `--channels` |
| Bot does not react to DMs | Claude Code was launched without `--channels` | Start with `claude --channels plugin:discord@claude-plugins-official` |
| Unknown sender behavior is unclear | Access policy / allowlist not checked | Run `/discord:access`, then use `pair` or `allow` as needed |

---

## Non-interactive behavior

`nonInteractiveMode: deferred` — under `-p`, only Step 0 can run. Browser
actions, token paste, and Claude Code plugin commands are written to
`setup-resume.md` for an interactive resume. See `_lib/non-interactive.md`.

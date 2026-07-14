---
description: "Lesson command"
category: "lesson"
chapter: "courses/aiagent/lesson03-core/module22-discord"
duration: "~60 min"
prerequisites: ["start-21-1", "setup-discord"]
level: "intermediate"
tags: ["discord", "bot", "channels", "plugin"]
nonInteractiveMode: incompatible
---
# Lesson 22-1: Discord Integration Introduction

## What You'll Do

Learn how to combine a **Discord Bot** with the **official Claude Code Channels discord plugin** so Claude Code can safely read and write Discord channels and DMs.

## Prerequisites

- Have a Discord account and a server where you can invite a bot
- Be able to launch Claude Code in interactive mode
- Run `/setup-discord` first to confirm the official plugin installation and `--channels` launch flow

## Goals

1. Explain how to create a bot in the Discord Developer Portal and enable MESSAGE CONTENT INTENT
2. Confirm the official flow from `/plugin install discord@claude-plugins-official` to `claude --channels plugin:discord@claude-plugins-official`
3. Handle tokens and access control safely with `/discord:configure`, local environment variables, and allowlist
4. Understand what the bot can and cannot do, then choose between private client channels and a bot-as-hub pattern

## Related Page

- Lesson Page: [Module 22](https://ai-agent.camp/en/course/module-22?slideId=module-overview)

## Next Steps

Next, run `/start-23-1` to continue to LINE official account operations.

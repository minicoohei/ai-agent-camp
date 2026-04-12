---
description: "Unified API setup guide (list of service configurations)"
aliases: ["api-setup", "setup-api"]
category: "setup"
duration: "About 5 minutes"
prerequisites: ["Cursor is installed", "ai-agent-camp folder is open"]
level: "beginner"
tags: ["setup", "api", "guide"]
---

# API Setup Wizard - Unified Setup Guide

Centrally manage the setup of various APIs (Google, Notion, Slack, Fal.AI, Gemini, etc.).

## Quick Setup (Recommended)

Simply enter the following commands in Cursor's chat field, and the AI will guide you through setup interactively.

| Command | Target Service | Description |
|---------|---------------|-------------|
| `/setup-gemini` | Gemini API | Required for image/text generation (required) |
| `/setup-github` | GitHub | Required for repository operations and Actions (recommended) |
| `/setup-slack` | Slack API | Required for Slack search and task management |
| `/check-setup` | Overall Check | Check all API configurations at once |

## Supported Services

| Service | Description | Setup Method |
|---------|-------------|--------------|
| `gemini` | Google Gemini generative AI | Run `/setup-gemini` |
| `google` | Gmail, Calendar, Drive, Sheets, Slides | Run `/setup-google-api` |
| `notion` | Notion pages and databases | Enter `NOTION_API_KEY` directly in `.env` |
| `slack` | Slack workspace | Run `/setup-slack` |
| `fal` | Fal.AI image/video generation | Enter `FAL_KEY` directly in `.env` |
| `heygen` | HeyGen AI avatar videos | Enter `HEYGEN_API_KEY` directly in `.env` |
| `elevenlabs` | ElevenLabs TTS (text-to-speech) | Enter `ELEVENLABS_API_KEY` directly in `.env` |
| `typefully` | Typefully X (formerly Twitter) post management | Enter `TYPEFULLY_API_KEY` directly in `.env` |

## Checking Configuration Status

To check all API configurations, enter the following in Cursor's chat field:

```text
/check-setup
```

The AI will automatically check all items and display a report showing which APIs are configured and which are not.

## Related Commands

- `/setup-gemini` - Gemini API setup (AI opens browser to guide you)
- `/setup-slack` - Slack API setup (AI opens browser to guide you)
- `/setup-github` - GitHub authentication setup
- `/check-setup` - Comprehensive environment check
- `/setup-google-api` - Google API dedicated setup (OAuth authentication flow)
- `/gmail-account-setup` - Gmail multiple account configuration

---
description: "Lesson command — Salesforce CLI (sf) setup"
duration: "~15 min"
prerequisites: ["Salesforce CLI (sf) account"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-24"]
---

# /setup-salesforce -- Salesforce CLI (sf) setup

> Drive Salesforce orgs from the `sf` CLI. No Connected App — browser OAuth is enough.

**Highlight**: No Connected App — browser OAuth only

## Setup steps

1. Install Salesforce CLI (pinned, npm preferred) — `npm install -g @salesforce/cli@2.x`

2. Sign in to Production — `sf org login web --alias prod`

3. For Sandbox — `sf org login web --alias dev --instance-url https://test.salesforce.com`

4. Verify — `sf org list`

## Gotchas

- `sf` v1 (`sfdx`) and v2 (`sf`) have different commands — use v2
- Always pass `--instance-url https://test.salesforce.com` for Sandbox

## Non-interactive mode

Browser OAuth is mandatory — cannot complete under `claude -p` / `cursor-agent --print`. Re-run in interactive mode.

## Related slides

- aiagent-course Module 24: see slide deck for the full visual walkthrough

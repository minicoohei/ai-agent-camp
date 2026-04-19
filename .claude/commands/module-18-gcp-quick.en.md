---
description: Slash /module-18-gcp-quick — Module 18 Lesson 4-1 — Authenticate gog using bundled OAuth (no terminal input required)
---

## Start here (quickest)

**The learner only needs to run `/module-18-gcp-quick` in chat.** The bash commands below are for the agent (or for those who want to troubleshoot manually).

Run **`/module-18-gcp-quick`** in chat to load all instructions for this lesson into context at once.

# Module 18 — Google Auth Quick (Lesson 4-1 GCP Main)

The user is working on the course material "Module 18 - Google Auth Quick (`slideId=lesson-18-1-gcp`)." **The user does not need to type commands directly in the terminal.** The agent should run `gog` (gogcli) and report the results.

## Prerequisites

- The working directory should be the **ai-agent-camp repository root** (already cloned).
- OAuth client JSON path (per course material): `credentials/google-workspace-desktop-oauth.json`

## Steps

### For the agent: Verify gog availability and auth status

Run the following commands **in this order** and summarize the results for the user (do not ask the learner to type in the terminal).

```bash
# Check if gog is in PATH (if not found, installation is needed)
command -v gog || echo "gog: not found in PATH"

gog --version

gog auth --help

gog auth list
```

- If `gog` is not found → Guide the user to install gogcli (gog) via **Module 15-1** or similar, then continue.
- If `gog auth list` already shows an account, avoid duplicate additions and only run `gog auth add` when necessary.

### OAuth Setup

1. Verify that `credentials/google-workspace-desktop-oauth.json` exists. If not, guide the user to proceed to the course material's Appendix (`slideId=lesson-18-1-gcp-appendix`) or obtain the JSON from the course administrators.
2. Run `gog auth credentials set credentials/google-workspace-desktop-oauth.json` **from the repository root** to register the shared client.
3. Ask the user for the **Google account email they want to use for login**, then run `gog auth add <email>`. When the browser opens, guide them through the **4 OAuth screen captures** in the course slide `lesson-18-1-gcp` (Google Auth Quick) (order may vary):
   - **Unverified app**: Click "Advanced" → click the **Continue to Cursor Bootcamp** link at the bottom (developer display showing `user@example.com` etc. is expected).
   - **Basic consent**: Confirm profile and email, then proceed with "Next" or similar.
   - **Scopes**: Select all if needed and grant/continue.
   - **Gog Account UI** (if shown): Verify connection and permissions via DEFAULT and per-service badges.
4. Run `gog auth list` to confirm the account has been registered (optionally also use Gog's local management UI).
5. On success, proceed to **`/module-18-google-auth`** (auth test) to verify Gmail/Calendar connectivity.

## References

- Course: `slideId=lesson-18-1-gcp` (main), `slideId=lesson-18-1-gcp-appendix` (self-managed GCP)
- Example: `/en/course/module-18?slideId=lesson-18-1-gcp`

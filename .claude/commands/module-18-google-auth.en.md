---
description: Slash /module-18-google-auth — Module 18 Lesson 4-1 — Assist Google authentication (gog auth) and Gmail/Calendar verification
---

## Start here (quickest)

Run **`/module-18-google-auth`** in chat to load all instructions for this lesson into context at once. **This is faster and more reliable than manually typing long prompts.**

# Module 18 — Google Authentication Test (Lesson 4-1 Auth)

The user is working on the course material "Module 18 - Authentication Test." **Via this command,** **the user does not need to type anything directly in the terminal.** The agent should run `gog` (gogcli) and report the results.

## Steps

1. If not authenticated, first complete **`/module-18-gcp-quick`** (bundled OAuth registration and `gog auth add`).
2. Run `gog gmail search --query "is:inbox" --max 5` to verify inbox retrieval.
3. Run `gog calendar events --days 7` to verify event retrieval.
4. On failure, cross-reference with the course material's `slideId=lesson-18-1-gcp-appendix` (self-managed GCP) OAuth settings.

## References

- Course: `slideId=lesson-18-1-auth` (e.g., `/en/course/module-18?slideId=lesson-18-1-auth`)

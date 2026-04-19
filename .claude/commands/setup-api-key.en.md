---
description: "Guide the procedure for safely setting up API keys and tokens (for beginners)"
---

# API Key Setup Guide

When the user requests "I want to set up an API key" or "I want to enter a Gemini key," guide them using **only this procedure**. Do not let them paste secrets in chat.

## Top Priority Rule

- **Do not let users paste API keys or tokens in chat.** If they do, simply say "That approach is risky. Please paste it in `.env.local` instead, not in chat."

## Procedure (follow this order)

1. **Prepare**  
   Run the following at the project root to add the key entry to `.env.local`:
   ```bash
   uv run python tools/credential_manager.py prepare-dotenv KEY_NAME
   ```
   (`KEY_NAME` examples: `GEMINI_API_KEY`, `GITHUB_TOKEN`. For multiple keys, list them: `KEY_NAME1 KEY_NAME2`.)

2. **Paste**  
   Tell the user: "Open [`.env.local`](.env.local) and paste the value **only to the right of** `KEY_NAME=`, then save. Once saved, type 'saved' to continue."  
   Do not let them paste the value or the entire file in chat.

3. **Migrate**  
   Once the user says "saved," run:
   ```bash
   uv run python tools/credential_manager.py import-dotenv --delete KEY_NAME
   ```
   This moves the value to the OS Credential Store and deletes the line from `.env.local`.

4. **Verify**  
   ```bash
   uv run python tools/credential_manager.py status
   ```
   Confirm the target key shows as `stored`.

5. **Run scripts that use secrets**  
   Follow each lesson or project's instructions. To inject from Credential Store to environment variables, use `inject_to_environ` (see lesson commands like `setup-fal.md`).

## Notes

- `NEXT_PUBLIC_*` and Firebase public configs can remain in `.env.local`. Only delete imported key lines.
- For terminal-only setup, `uv run python tools/credential_manager.py store KEY_NAME` also works (input is hidden from screen).

## References

- Course: Module 0 "Manage API Keys Safely" slide (slideId=api-key-management)
  - URL path example: `/en/course/module-0?slideId=api-key-management` (replace `en` with `ja` / `es`)
  - Open in browser locally (macOS, dev server on port 3000):
    ```bash
    open "http://localhost:3000/en/course/module-0?slideId=api-key-management"
    ```
  - Opening module-0 without `slideId` redirects to the setup hub. Always include `slideId` to go directly to the slide.

---
description: Slash /module-18-gcp-appendix — Module 18 — Self-managed GCP (Console procedure checklist)
---

## Start here (quickest)

Run **`/module-18-gcp-appendix`** in chat to load the GCP console procedure support context.

# Module 18 — Self-Managed GCP (Appendix)

The user is working on the course material "Module 18 - For those who want to manage GCP themselves (`slideId=lesson-18-1-gcp-appendix`)." Google Cloud Console operations are done **manually in the user's browser**; the agent should provide **checklists for each step, troubleshooting tips, and brief explanations of terminology.**

## Steps (corresponding to the course's 4 steps)

1. **Project and APIs**: Verify that a project has been created and Gmail / Calendar / Drive / Sheets / Google Docs APIs have been enabled.
2. **Billing**: Verify that a billing account has been linked to the project.
3. **OAuth Client**: Verify that "Create credentials" → OAuth client ID → **External** → **Desktop app** → JSON has been downloaded.
4. **OAuth Consent Screen**: Verify that required fields have been entered in Branding and the user's own Google account has been added as a **Test user**.

## Troubleshooting

- If the wizard requires filling in the consent screen first, guide the user to complete Step 4 (Branding) before returning to Step 3.
- The downloaded JSON should **not be committed to Git**. Reference it via `.env` or Credential Manager.

## References

- Course: `/en/course/module-18?slideId=lesson-18-1-gcp-appendix` (adjust locale as needed)

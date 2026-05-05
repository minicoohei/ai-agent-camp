---
description: "Lesson command — Google Ads API setup"
duration: "~180 min (API Center approval is most of it)"
prerequisites: ["Google Ads API account"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-25"]
---

# /setup-google-ads -- Google Ads API setup

> The 3-day journey to actually call Google Ads API v21 (Python SDK). You need MCC + Basic Access + OAuth refresh_token.

**Highlight**: Basic Access approval can take a business day. OAuth must use the web flow

## Setup steps

1. Create a Google Ads Manager Account (MCC)

   ```bash
   https://ads.google.com/aw/signup/manager
   ```

2. Request a Developer Token in the API Center — `MCC → Tools → API Center → Apply for Basic Access`

3. Create a GCP project and an OAuth Client (web)

   ```bash
   https://console.cloud.google.com/apis/credentials
   ```

4. Mint a refresh_token via the web flow (local listener) — `# Use Google OAuth Playground or `gcloud auth application-default login` to mint a refresh_token (or your own OAuth helper)`

5. Save the 5 secrets in Keychain + GitHub Secrets — `GOOGLE_ADS_DEVELOPER_TOKEN / CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN / LOGIN_CUSTOMER_ID`

6. Smoke-test from the Python SDK (validate_only=True dry-run) — `python -c "from google.ads.googleads.client import GoogleAdsClient; print('SDK loaded ok')"  # dry-run details in the next lesson`

## Gotchas

- Test Accounts can't run paid ads. Switch to a production account once Basic Access is granted
- Always set EU political advertising status on campaign_operation (`DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`) — it's required
- Even with validate_only=True you must use a `mutate` atomic batch (budget + campaign with temp resource_name `-1`); otherwise the resource_name existence check fails

## Non-interactive mode

Browser OAuth is mandatory — cannot complete under `claude -p` / `cursor-agent --print`. Re-run in interactive mode.

## Related slides

- aiagent-course Module 25: see slide deck for the full visual walkthrough

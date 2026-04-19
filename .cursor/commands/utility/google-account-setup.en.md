# Google Account Setup (for Calendar/Drive)

Assists with setting up personal Google account Calendar/Drive integration.
**You can reuse the same OAuth Client ID used for Gmail.**

## Why a Separate Setup Is Needed

Gmail/Calendar/Drive each require different scopes (permissions).
This script authenticates all three scopes together.

---

## Prerequisite Checks

### 1. Verify GitHub CLI

```bash
gh auth status
```

If not authenticated:
```bash
gh auth login
```

### 2. Verify OAuth Client ID

Ask the user:
"Have you already created an OAuth Client ID in Google Cloud Console?"

**If not, guide them as follows:**

Refer to `docs/GMAIL_OAUTH_SETUP.md`, or go to https://console.cloud.google.com/ and:

1. Create a project (first time only)
2. **Enable Gmail API / Calendar API / Drive API**
3. Configure OAuth consent screen (external, required fields only)
4. Credentials -> Create OAuth Client ID (**Desktop app**)
5. Copy the Client ID and Secret

---

## Run Setup

> **Important**: Since browser authentication is required, **run this directly in the terminal.**
> Pipe execution from Cursor's chat will time out.

```bash
python scripts/setup_google_account.py --label <account_name>
```

### Examples

```bash
python scripts/setup_google_account.py --label my-account
python scripts/setup_google_account.py --label work
python scripts/setup_google_account.py --label work
```

### Input During Execution

1. Client ID (copy from Google Cloud Console)
2. Client Secret (same)
3. Log in to Google via browser -> Grant permission

---

## Post-Setup Configuration

### 1. Verify Secrets

```bash
gh secret list --repo <owner/repo> | grep GOOGLE
```

The following Secrets will be registered:
- `GOOGLE_<LABEL>_CLIENT_ID`
- `GOOGLE_<LABEL>_CLIENT_SECRET`
- `GOOGLE_<LABEL>_REFRESH_TOKEN`

### 2. Update GOOGLE_ACCOUNTS_CONFIG

**This must be updated each time you add an account:**

```bash
# Example: 2 accounts - my-account and work
gh secret set GOOGLE_ACCOUNTS_CONFIG \
  --body '{"accounts":[{"label":"my-account","type":"oauth"},{"label":"work","type":"oauth"}]}' \
  --repo <owner/repo>
```

### 3. Set Drive Folder ID (Optional)

If retrieving files from Drive, set the target folder ID:

```bash
gh secret set GOOGLE_MYACCOUNT_DRIVE_FOLDER_ID \
  --body '<Google Drive folder ID>' \
  --repo <owner/repo>
```

Alternatively, you can include the folder ID in GOOGLE_ACCOUNTS_CONFIG:

```json
{
  "accounts": [
    {
      "label": "my-account",
      "type": "oauth",
      "drive_folder_id": "1234567890abcdef"
    }
  ]
}
```

### 4. Add Environment Variables to Workflow

Add environment variables for the new account in `.github/workflows/fetch_data.yml`:

```yaml
env:
  # For Calendar/Drive
  GOOGLE_<LABEL>_CLIENT_ID: ${{ secrets.GOOGLE_<LABEL>_CLIENT_ID }}
  GOOGLE_<LABEL>_CLIENT_SECRET: ${{ secrets.GOOGLE_<LABEL>_CLIENT_SECRET }}
  GOOGLE_<LABEL>_REFRESH_TOKEN: ${{ secrets.GOOGLE_<LABEL>_REFRESH_TOKEN }}
  GOOGLE_<LABEL>_DRIVE_FOLDER_ID: ${{ secrets.GOOGLE_<LABEL>_DRIVE_FOLDER_ID }}
```

### 5. Commit and Push Changes

```bash
git add .github/workflows/fetch_data.yml
git commit -m "feat: Add Google account <label> for Calendar/Drive"
git push
```

---

## Verification

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```

Check logs:
```
Starting Multi-Calendar fetch (OAuth mode)...
Processing Calendar for account: my-account
[my-account] OAuth authentication successful for Calendar
[my-account] Fetched 5 calendar events
Starting Multi-Drive fetch (OAuth mode)...
Processing Drive for account: my-account
[my-account] OAuth authentication successful for Drive
[my-account] Fetched 10 Drive files
```

---

## Output Directory Structure

```
output/
├── calendar/
│   ├── my-account/
│   │   ├── 2026-01-16_events.md
│   │   └── 2026-01-17_events.md
│   └── work/
│       └── 2026-01-16_events.md
└── drive/
    ├── my-account/
    │   ├── docs/
    │   ├── sheets/
    │   └── slides/
    └── work/
        └── docs/
```

---

## Troubleshooting

### "This app isn't verified" message appears

This is normal. Click "Advanced" -> "Go to [app name]" to continue.

### Authentication error occurs

Check the following:
1. Are Gmail API / Calendar API / Drive API enabled?
2. Is the OAuth consent screen configured?
3. Are the Client ID/Secret correct?

### GitHub Secrets registration fails

```bash
gh auth status
```
Check authentication status. If not authenticated, run `gh auth login`.

### Drive files are not retrieved

- Verify that `drive_folder_id` or `GOOGLE_<LABEL>_DRIVE_FOLDER_ID` is set
- Verify that you have read permissions for the target folder

### "multiple remotes detected" error

```bash
python scripts/setup_google_account.py --label my-account --repo owner/repo
```
Explicitly specify the repository.

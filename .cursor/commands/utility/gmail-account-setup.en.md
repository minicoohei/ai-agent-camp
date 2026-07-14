---
nonInteractiveMode: incompatible
---

# Gmail Account Setup

Assists with setting up personal Gmail account integration.

## Why an OAuth Client ID Is Needed

Personal Gmail (@gmail.com) requires **the user to log in and grant permission via browser** for security reasons. The OAuth Client ID serves as identification for "which application is requesting access."

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
2. Enable Gmail API
3. Configure OAuth consent screen (external, required fields only)
4. Credentials -> Create OAuth Client ID (**Desktop app**)
5. Copy the Client ID and Secret

---

## Run Setup

> **Important**: Since browser authentication is required, **run this directly in the terminal.**
> Pipe execution from Cursor's chat will time out.

```bash
python scripts/setup_gmail_account.py --label <account_name>
```

### Examples

```bash
python scripts/setup_gmail_account.py --label my-account
python scripts/setup_gmail_account.py --label work
python scripts/setup_gmail_account.py --label work
```

### Input During Execution

1. Client ID (copy from Google Cloud Console)
2. Client Secret (same)
3. Log in to Google via browser -> Grant permission

---

## Post-Setup Configuration

### 1. Verify Secrets

```bash
gh secret list --repo <owner/repo> | grep GMAIL
```

### 2. Update GMAIL_ACCOUNTS_CONFIG

**This must be updated each time you add an account:**

```bash
# Example: 2 accounts - my-account and work
gh secret set GMAIL_ACCOUNTS_CONFIG \
  --body '{"accounts":[{"label":"my-account","type":"oauth"},{"label":"work","type":"oauth"}]}' \
  --repo <owner/repo>
```

### 3. Add Environment Variables to Workflow

Add environment variables for the new account in `.github/workflows/fetch_data.yml`:

```yaml
env:
  GMAIL_<LABEL>_CLIENT_ID: ${{ secrets.GMAIL_<LABEL>_CLIENT_ID }}
  GMAIL_<LABEL>_CLIENT_SECRET: ${{ secrets.GMAIL_<LABEL>_CLIENT_SECRET }}
  GMAIL_<LABEL>_REFRESH_TOKEN: ${{ secrets.GMAIL_<LABEL>_REFRESH_TOKEN }}
```

### 4. Commit and Push Changes

```bash
git add .github/workflows/fetch_data.yml
git commit -m "feat: Add Gmail account <label>"
git push
```

---

## Verification

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```

Check logs:
```
Starting Multi-Gmail fetch...
Processing account: my-account
[my-account] OAuth authentication successful
Processing account: work
[work] OAuth authentication successful
```

---

## Troubleshooting

### "This app isn't verified" message appears

This is normal. Click "Advanced" -> "Go to [app name]" to continue.

### Authentication error occurs

Check the following:
1. Is the Gmail API enabled?
2. Is the OAuth consent screen configured?
3. Are the Client ID/Secret correct?

### GitHub Secrets registration fails

```bash
gh auth status
```
Check authentication status. If not authenticated, run `gh auth login`.

### "multiple remotes detected" error

```bash
python scripts/setup_gmail_account.py --label my-account --repo owner/repo
```
Explicitly specify the repository.

### Git push conflict error

This occurs when multiple workflows run simultaneously. Running again will resolve it.

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```

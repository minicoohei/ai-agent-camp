---
description: "Lesson command"
duration: "~15 min"
prerequisites: ["Have a Google account", "Browser available"]
level: "beginner"
tags: ["setup", "bigquery", "gcp", "gcloud"]
nonInteractiveMode: incompatible
---
# BigQuery / GCP Authentication Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-bigquery` to display progress
2. Auto-detect existing gcloud CLI installation:
   - Run `gcloud --version`
   - If gcloud CLI is already installed and authenticated, skip to Step 4 (connection test)
   - If not installed, start from Step 1

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Install gcloud CLI, authenticate with Application Default Credentials (ADC), and run SQL queries in BigQuery |
| Duration | ~15 minutes |
| Prerequisites | Have a Google account and a browser available |
| Skill Level | A few CLI commands + browser authentication (AI guides you through the steps) |

**Session flow:**
1. Install gcloud CLI (AI guides you through the steps)
2. Log in with your Google account (browser opens automatically)
3. Set up a GCP project (AI guides you)
4. Set up Application Default Credentials (one command)
5. BigQuery connection test (AI runs automatically)

> **About costs**: BigQuery offers up to 1 TB of free queries per month. The training uses public datasets, so costs are virtually zero. Google will notify you before exceeding the free tier.
>
> **Hint**: If the AI's response stops midway, type "please continue" or "it stopped" to resume.

---

## Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(check_prereq -> Guide: "If you can log in to a browser with a Google account, you're ready. BigQuery is free for up to 1 TB of queries per month, so usage during the training is virtually free.")
(different_lesson -> Display module list)

---

## Step 1: Install gcloud CLI

**What the AI does:**
1. Auto-detect the OS (Mac / Windows / Linux)
2. Run `gcloud --version` to check if it's already installed
3. If already installed, skip to Step 2
4. If not installed, guide the user through OS-specific installation steps

**Mac (Homebrew recommended):**
```bash
brew install google-cloud-sdk
```

**Mac (if Homebrew is unavailable) / Windows:**
Download the installer via browser:
```bash
# Mac:
open https://cloud.google.com/sdk/docs/install
# Windows:
start https://cloud.google.com/sdk/docs/install
```

**Post-installation verification:**
```bash
gcloud --version
```

**AskQuestion configuration:**
```json
{
  "title": "Step 1: gcloud CLI Installation",
  "questions": [{
    "id": "install_status",
    "prompt": "Please tell us the status of your gcloud CLI installation:",
    "options": [
      {"id": "installed", "label": "Installed (or already had it installed)"},
      {"id": "homebrew_issue", "label": "Can't use Homebrew (Mac)"},
      {"id": "windows_help", "label": "I need help with Windows instructions"},
      {"id": "install_error", "label": "I got an error during installation"}
    ]
  }]
}
```

(installed -> Verify with `gcloud --version`, then proceed to Step 2)
(homebrew_issue -> Guide: "Open https://cloud.google.com/sdk/docs/install in your browser and download the macOS installer. Extract the downloaded file and run ./install.sh to install.")
(windows_help -> Guide: "Open https://cloud.google.com/sdk/docs/install in your browser and download the Windows installer (.exe). Double-click the downloaded file and follow the on-screen instructions. After installation, open a new WSL terminal (Ubuntu).")
(install_error -> Check the error message and identify the cause. If PATH is not configured, guide user to run `source ~/.zshrc` or open a new terminal)

---

## Step 2: GCP Project Setup

**What the AI does:**
1. Run `gcloud auth login` to start Google authentication in the browser
2. The browser opens automatically, prompting you to log in with your Google account

```bash
gcloud auth login
```

**Browser authentication instructions for the user:**

```text
The browser will open automatically. Follow these steps to authenticate:

┌─────────────────────────────────────────────────────────────┐
│ 1. Select your Google account and log in via browser        │
│ 2. "Google Cloud SDK is requesting access"                  │
│    → Click "Allow"                                          │
│ 3. When "Authentication complete" appears, close the browser│
│ 4. Return to the terminal to see the success message        │
└─────────────────────────────────────────────────────────────┘
```

**After authentication, set up the project:**
```bash
# List existing projects
gcloud projects list

# Set the project (replace PROJECT_ID with your actual ID)
gcloud config set project PROJECT_ID
```

**AskQuestion configuration:**
```json
{
  "title": "Step 2: GCP Project Setup",
  "questions": [{
    "id": "auth_status",
    "prompt": "Did you complete the Google account authentication in the browser?",
    "options": [
      {"id": "auth_done", "label": "Authentication complete!"},
      {"id": "browser_not_open", "label": "The browser didn't open"},
      {"id": "auth_denied", "label": "I got an error on the authentication screen"},
      {"id": "no_project", "label": "I don't have a GCP project (I want to create one)"}
    ]
  }]
}
```

(auth_done -> Display the project list with `gcloud projects list`. If an existing project is available, guide user to run `gcloud config set project PROJECT_ID` and proceed to Step 3)
(browser_not_open -> Guide: "Copy the URL displayed in the terminal and paste it into your browser's address bar.")
(auth_denied -> Guide: "Try using your browser's incognito/private browsing mode. If blocked by your company account, try using a personal Google account.")
(no_project -> Guide: "Let's create a new GCP project. Run the following command: `gcloud projects create PROJECT_ID --name='Project Name'` (PROJECT_ID can be any name using alphanumeric characters and hyphens, e.g., `my-bigquery-lab`). Alternatively, you can create a new project at https://console.cloud.google.com.")

---

## Step 3: Application Default Credentials (ADC) Setup

**What the AI does:**

1. Run the ADC setup command:
```bash
gcloud auth application-default login
```

2. The browser will open again to create ADC credentials (same browser authentication as Step 2)

**Message to display to the user:**
```text
The browser will open once more. This is to create authentication credentials (ADC)
for applications like Python to connect to BigQuery.

┌─────────────────────────────────────────────────────────────┐
│ 1. Select your Google account and log in via browser        │
│ 2. Click "Allow"                                            │
│ 3. If "Credentials saved to file: ..." appears in the       │
│    terminal, it was successful                               │
└─────────────────────────────────────────────────────────────┘
```

3. After ADC setup, enable the BigQuery API:
```bash
gcloud services enable bigquery.googleapis.com
```

**AskQuestion configuration:**
```json
{
  "title": "Step 3: ADC Setup",
  "questions": [{
    "id": "adc_status",
    "prompt": "Did you complete the ADC authentication and BigQuery API activation?",
    "options": [
      {"id": "adc_done", "label": "'Credentials saved to file' was displayed!"},
      {"id": "adc_browser_issue", "label": "Browser authentication isn't working"},
      {"id": "api_enable_error", "label": "I got an error enabling the BigQuery API"},
      {"id": "adc_what", "label": "What is ADC?"}
    ]
  }]
}
```

(adc_done -> Proceed to Step 4)
(adc_browser_issue -> Guide: "Follow the same browser authentication steps as Step 2. If it doesn't work, copy the URL displayed in the terminal and paste it into your browser.")
(api_enable_error -> Guide: "Let me check the error message. If it says 'permission denied', you need project owner permissions. You can also enable it manually at https://console.cloud.google.com/apis/library/bigquery.googleapis.com.")
(adc_what -> Explain: "ADC (Application Default Credentials) is a mechanism for applications like Python scripts to automatically find GCP authentication credentials. Once configured, you can connect to BigQuery securely without specifying API keys in your code.")

---

## Step 4: BigQuery Connection Test

**What the AI auto-runs:**

1. Check that required packages are installed:
```bash
uv add google-cloud-bigquery
```

2. Run the BigQuery connection test:
```python
from google.cloud import bigquery

client = bigquery.Client()
query = "SELECT COUNT(*) as cnt FROM `bigquery-public-data.samples.shakespeare`"
result = client.query(query).result()
for row in result:
    print(f"Connection successful! Shakespeare dataset: {row.cnt} rows")
```

3. Display an AskQuestion based on the test result:

**On success:**
```text
BigQuery connection test succeeded!

Test result: The query on the public dataset (Shakespeare) executed successfully.
You can now use BigQuery for SQL execution, data analysis, and EDA.
```

**On failure — AskQuestion:**
```json
{
  "title": "Test Result: An error occurred",
  "questions": [{
    "id": "test_error",
    "prompt": "An error occurred during the BigQuery connection test. Let's check possible causes.",
    "options": [
      {"id": "retry", "label": "Run the test again"},
      {"id": "reauth", "label": "Redo authentication (go back to Step 2)"},
      {"id": "show_error", "label": "I want to see the error details"},
      {"id": "skip_test", "label": "Skip the test and move on"}
    ]
  }]
}
```

(retry -> Re-run the test)
(reauth -> Go back to Step 2)
(show_error -> Display the error message and guide on the cause and solution)
(skip_test -> Guide: "The connection test was skipped. You can check later with /check-setup.")

---

## Common Troubles and Solutions

**AskQuestion configuration:**
```json
{
  "title": "Select the trouble type",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the one that applies to you",
    "options": [
      {"id": "trouble_install", "label": "I get errors installing gcloud CLI"},
      {"id": "trouble_auth", "label": "Browser authentication fails"},
      {"id": "trouble_project", "label": "I don't have a GCP project / can't select one"},
      {"id": "trouble_api", "label": "Can't enable the BigQuery API"},
      {"id": "trouble_permission", "label": "I get a 'permission denied' error"},
      {"id": "trouble_package", "label": "google-cloud-bigquery package error"},
      {"id": "trouble_cost", "label": "I'm worried about costs"},
      {"id": "trouble_other", "label": "Other error"}
    ]
  }]
}
```

### Trouble 1: gcloud CLI Installation Error
**Cause**: Homebrew issues, PATH not configured, insufficient permissions
**What the AI does**:
1. Check installation status with `which gcloud`
2. If Homebrew errors, run `brew doctor` to identify the issue
3. If PATH is not configured, guide user to run `source ~/.zshrc` or open a new terminal
4. If still unresolved, guide user through manual installation via browser

### Trouble 2: Browser Authentication Fails
**Cause**: Browser doesn't open, company security policies, account permissions
**What the AI does**:
1. Guide user to manually paste the URL from the terminal into the browser
2. Suggest authentication in incognito mode
3. Guide user through `gcloud auth login --no-launch-browser` for manual URL entry

### Trouble 3: No GCP Project
**Cause**: First time using GCP
**AI guidance**: "You can create a project with `gcloud projects create my-bigquery-lab --name='BigQuery Lab'`. Alternatively, go to https://console.cloud.google.com and create a new project via 'Select a project' > 'New Project' at the top of the page."

### Trouble 4: Can't Enable BigQuery API
**Cause**: Missing project owner permissions, billing not enabled
**What the AI does**:
1. Re-run `gcloud services enable bigquery.googleapis.com`
2. Check error message; if billing needs to be enabled, guide to https://console.cloud.google.com/billing
3. If it's a permissions issue, advise asking the project owner to grant permissions

### Trouble 5: "Permission Denied" Error
**Cause**: ADC not properly configured, BigQuery API disabled, insufficient project permissions
**What the AI does**:
1. Check ADC status with `gcloud auth application-default print-access-token`
2. If ADC is not set up, re-run `gcloud auth application-default login`
3. Check if BigQuery API is enabled with `gcloud services list --enabled`

### Trouble 6: google-cloud-bigquery Package Error
**Cause**: Package not installed, version mismatch
**What the AI does**: Auto-run `uv add google-cloud-bigquery`. If the environment is broken, guide user to recreate it with `bash tools/scripts/setup.sh`

### Trouble 7: Cost Concerns
**AI guidance**: "BigQuery offers up to 1 TB of free queries per month. Access to public datasets used in the training is also free. Google will notify you before exceeding the free tier. For training-level usage, the free tier is more than sufficient."

### Trouble 8: Other Errors
**What the AI does**: Check the error message content, identify the cause, and guide the user to a solution

---

## Checkpoint
- [ ] gcloud CLI is installed
- [ ] Google account authentication is complete
- [ ] GCP project is configured
- [ ] Application Default Credentials are set up
- [ ] BigQuery API is enabled
- [ ] BigQuery connection test passed

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "BigQuery / GCP authentication setup is complete! What would you like to do next?",
    "options": [
      {"id": "try_bigquery", "label": "Learn BigQuery connection and auth setup (/start-8-1)"},
      {"id": "try_eda", "label": "Try running EDA (/start-8-2)"},
      {"id": "setup_other", "label": "Proceed to another setup (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- try_bigquery -> Guide to /start-8-1
- try_eda -> Guide to /start-8-2
- setup_other -> Guide to /start-0-1
- finish -> End

---

## Completion

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-bigquery` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "Next, learn BigQuery connection and auth setup with `/start-8-1`"

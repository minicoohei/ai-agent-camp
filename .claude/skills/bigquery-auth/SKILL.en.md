---
name: bigquery-auth
description: "A skill for setting up BigQuery authentication on a per-GCP-project basis. Safely isolates and manages multiple projects using gcloud configuration profiles. Triggered by requests like 'connect to BigQuery', 'BQ authentication', 'gcloud authentication', 'data analysis auth setup', etc."
triggers:
  - bigquery-auth
  - BigQuery authentication
  - connect to BQ
  - gcloud authentication
  - data analysis auth
  - BigQuery connection
  - GCP authentication
  - BigQuery認証
  - gcloud認証
---

## Trigger Words
"BigQuery authentication", "connect to BQ", "data analysis auth", "gcloud authentication"

# BigQuery Authentication (Project-based)

A skill for creating gcloud configuration profiles on a per-GCP-project basis and performing BigQuery authentication.

## Workflow

1. User says "I want to use BigQuery" or "I want to see data from {project}"
2. **Confirm GCP project ID** (required)
3. Check existing configuration profiles
4. Create a new profile if needed
5. Guide through browser authentication
6. Run connection test

## Authentication Steps

### Step 1: Check Configuration Profiles

```bash
gcloud config configurations list
```

Display existing profiles and check if there is one for the target project.

### Step 2: Create Profile (if new)

```bash
# Create profile
gcloud config configurations create {PROFILE_NAME}

# Set project
gcloud config set project {PROJECT_ID}
```

### Step 3: gcloud Authentication

```bash
# Main authentication (opens browser)
gcloud auth login

# Python SDK authentication (opens browser)
gcloud auth application-default login --quiet
```

**Note**: Both commands require browser authentication.

### Step 4: Verify Authentication

```bash
# Check current profile
gcloud config configurations list

# Check project
gcloud config get-value project

# Check ADC token
gcloud auth application-default print-access-token
```

### Step 5: BigQuery Connection Test

```python
import os
# Avoid environment variable conflicts
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

from google.cloud import bigquery
client = bigquery.Client(project="{PROJECT_ID}")
datasets = list(client.list_datasets())
print(f"Connection successful! {len(datasets)} datasets found")
```

## Profile Switching

```bash
# List profiles
gcloud config configurations list

# Switch
gcloud config configurations activate {PROFILE_NAME}
```

## Registered Profiles (Template)

### ADC Authentication (gcloud login)

| Profile | Project ID | Account | Purpose |
|---------|-----------|---------|---------|
| `default` | {YOUR_PROJECT_ID} | {YOUR_EMAIL} | Default |
| `{PROFILE_2}` | {PROJECT_ID_2} | {EMAIL_2} | Analysis |

> Replace with your own project information.

### Service Account Authentication (External Projects)

| Profile | Project ID | Key File | Purpose |
|---------|-----------|----------|---------|
| `{SA_PROFILE}` | {SA_PROJECT_ID} | `~/.gcp/{SA_KEY_FILE}.json` | External project analysis |

## How to Use Service Account Authentication

When connecting to external projects with a service account:

```python
import os
from google.cloud import bigquery
from google.oauth2 import service_account

# Authenticate with service account key
credentials = service_account.Credentials.from_service_account_file(
    os.path.expanduser("~/.gcp/{SA_KEY_FILE}.json")
)

# Create BigQuery client
client = bigquery.Client(
    project="{SA_PROJECT_ID}",
    credentials=credentials
)

# Connection test
datasets = list(client.list_datasets())
print(f"Connection successful! {len(datasets)} datasets found")
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| File xxx was not found | GOOGLE_APPLICATION_CREDENTIALS is invalid | `unset GOOGLE_APPLICATION_CREDENTIALS` |
| Reauthentication needed | Authentication expired | Re-run authentication |
| Permission denied | No BigQuery permissions | Check IAM settings |

## Important Notes

### Environment Variable Conflicts

If the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set, it takes priority over ADC.
Run the following in Python code to avoid this:

```python
import os
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
```

### When Using marimo Notebook

Follow the rules in `.cursor/rules/notebook.mdc`:
1. Before starting work, ask "Which GCP project will you work with?"
2. Display profile list with `gcloud config configurations list`
3. Switch profiles as needed

## Requirements

- Google Cloud SDK (`gcloud`) installed
- Ability to log in to Google account via browser
- BigQuery viewing permissions on the target project

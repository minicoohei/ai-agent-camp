# BigQuery Auth - Project-Level BigQuery Authentication

This command uses Cursor Browser to set up BigQuery authentication on a per-GCP-project basis. It leverages gcloud configuration profiles to safely manage multiple projects.

## Features

- **Project isolation**: Safely manage multiple GCP projects with gcloud configuration profiles
- **Browser authentication**: Guide authentication through Google Cloud Console
- **Application-default credentials**: Obtain credentials usable from the Python SDK
- **Environment variable support**: Avoid conflicts with existing `GOOGLE_APPLICATION_CREDENTIALS`

## Steps

### Phase 1: Confirm Parameters

Confirm the following information from the user's input:

1. **GCP Project ID** (required):
   - Example: `my-project-123`, `my-gcp-project`

2. **Profile name** (optional, default: auto-generated from Project ID):
   - Example: `my-profile`, `my-dev`, `default`

3. **Google account** (optional, selected by user)

### Phase 2: Check Existing Configuration Profiles

```bash
gcloud config configurations list
```

Display existing profiles and confirm:
- Whether a profile for the target project already exists
- What the currently active profile is

**Guide the user:**
```
[Existing Configuration Profiles]
NAME     IS_ACTIVE  ACCOUNT                     PROJECT
default  True       user@example.com            my-project
...

Do you have a profile for the target project?
- "Create new": Create a new profile
- "{profile_name}": Use an existing profile
```

### Phase 3: Create Configuration Profile (if new)

```bash
# Create a new profile
gcloud config configurations create {PROFILE_NAME}

# Set the project ID
gcloud config set project {PROJECT_ID}
```

### Phase 4: Browser Authentication (Cursor Browser)

#### Step 1: gcloud auth login

```bash
gcloud auth login
```

When the browser opens, check the page state with `browser_snapshot`.

**Guide the user:**
```
[Google Account Authentication]
The browser has opened.
1. Select the Google account you want to use
2. Grant access to "Google Cloud SDK"
3. It's complete when "You can close this window" is displayed

Enter "done" when authentication is complete.
```

#### Step 2: application-default credentials

```bash
gcloud auth application-default login --quiet
```

When the browser opens again, guide the authentication.

**Guide the user:**
```
[Application Default Credentials Authentication]
The browser has opened.
1. Select the same Google account
2. Grant access to "Google Auth Library"
3. Authentication is successful when a completion message is displayed

Enter "done" when authentication is complete.
```

### Phase 5: Verify Authentication

```bash
# Check authentication status
gcloud auth list

# Check project
gcloud config get-value project

# Check ADC token (OK if no error)
gcloud auth application-default print-access-token 2>/dev/null && echo "ADC authentication OK" || echo "ADC authentication failed"
```

### Phase 6: BigQuery Connection Test

```python
# Clear environment variables before testing
import os
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

from google.cloud import bigquery
client = bigquery.Client(project="{PROJECT_ID}")
datasets = list(client.list_datasets())
print(f"Connection successful! {len(datasets)} datasets found")
```

### Phase 7: Completion Report

**Report to the user:**
```
[BigQuery Authentication Complete]

Profile: {PROFILE_NAME}
Project: {PROJECT_ID}
Account: {ACCOUNT}
BigQuery connection: Successful

Profile switch command:
   gcloud config configurations activate {PROFILE_NAME}

Note: If the environment variable GOOGLE_APPLICATION_CREDENTIALS is set,
   run `del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]` in Python code
   or unset it before use.
```

## Usage Examples

### Basic usage
```
/bigquery-auth my-gcp-project
```

### Specify profile name
```
/bigquery-auth my-dev-project --profile my-dev
```

### Switch profiles
```
/bigquery-auth --switch my-profile
```

## Available GCP Profiles (Reference)

| Profile Name | Project ID | Purpose |
|-------------|------------|---------|
| `default` | - | Default environment |
| `my-profile` | my-gcp-project | Production data analysis |
| `my-dev` | my-dev-project | Development analysis |

## Troubleshooting

### Error: "File xxx was not found"
- The environment variable `GOOGLE_APPLICATION_CREDENTIALS` points to an invalid path
- Solution: `unset GOOGLE_APPLICATION_CREDENTIALS` or delete it in Python

### Error: "Reauthentication is needed"
- Authentication has expired
- Solution: Run `/bigquery-auth {PROJECT_ID}` again

### Error: "User does not have permission"
- No access permissions for BigQuery
- Solution: Check IAM permissions in the GCP Console

## Notes

- **Prevent forgetting to switch profiles**: Check the current profile with `gcloud config configurations list` before starting work
- **Environment variable conflicts**: If `GOOGLE_APPLICATION_CREDENTIALS` is set, it takes priority over ADC
- **When using marimo notebook**: Follow the rules in notebook.mdc and always verify the GCP environment before starting work

---
name: gcp-auth
description: "Skill for executing Google Cloud Platform (GCP) Application Default Credentials authentication. Triggered by requests like 'authenticate GCP,' 'Google Cloud auth,' 'gcloud login,' etc. Guides authentication procedures before using GCP services like BigQuery or Cloud Storage."
triggers:
  - gcp-auth
  - GCP認証
  - Google Cloud認証
  - gcloud login
  - サービスアカウント
  - ADC認証
---

## Trigger Words
"GCP auth," "Google Cloud auth," "gcloud login," "service account"

# GCP Authentication

A skill for executing Google Cloud Application Default Credentials (ADC) authentication.

## Workflow

1. User says "authenticate GCP," "I want to use BigQuery," etc.
2. Guide the user to run the authentication command in their terminal
3. Authenticate Google account in browser
4. Confirm authentication completion

## Usage

### Authentication Command (run directly in terminal)

```bash
gcloud auth application-default login
```

**Note**: This command requires browser-based authentication, so please run it directly in your terminal.

## Authentication Flow

1. **Run command** -> Browser opens automatically
2. **Select Google account** -> Choose the account to use
3. **Grant permissions** -> Click "Allow" on "Allow access to Google Auth Library"
4. **Confirm completion** -> Terminal displays "Credentials saved to file"

## Troubleshooting

| Error | Solution |
|-------|----------|
| Reauthentication is needed | Authentication expired. Run `gcloud auth application-default login` again |
| GOOGLE_APPLICATION_CREDENTIALS warning | Remove the relevant line from `.env`, or use ADC |
| Project not set | Set project with `gcloud config set project PROJECT_ID` |

## Checking Authentication Status

```bash
# If a token is displayed, authentication is complete
gcloud auth application-default print-access-token

# Check current project
gcloud config get-value project
```

## Requirements

- Google Cloud SDK (`gcloud`) is installed
- Able to log in to a Google account in browser

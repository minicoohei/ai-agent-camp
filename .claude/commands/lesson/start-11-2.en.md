---
description: "When the user says /start-11-2 — Module 11 Lesson 11-2: Automated Testing and Deployment Pipeline"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
prerequisites: ["start-11-1"]
duration: "~35 min"
level: "intermediate"
tags: ["github-actions", "secrets", "google-api"]
---

# 🎓 Lesson 11-2: Automated Testing and Deployment

## 📍 What You'll Do

**Lesson 11-2: GitHub Actions and API Integration**!

| Item | Details |
|------|------|
| Goal | Build automated data retrieval and processing pipelines using Secrets in GitHub Actions for Google API integration |
| Duration | ~35 min |
| Skills used | GitHub Actions, Repository Secrets, Google API |
| Prerequisites | Lesson 11-1 completed, GitHub repository |
| Course page | [Module 11: GitHub Actions](https://ai-agent.camp/en/course/module-11)  alongside this lesson |

**Session flow:**
1. Configure Repository Secrets
2. Call APIs from workflows
3. Execute automated data retrieval and processing

By the end of this session, you will have a secure API integration pipeline using Secrets.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite verification)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Configure Repository Secrets

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Configure Repository Secrets",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```text
Please explain the GitHub Repository Secrets configuration procedure.
Configuration location: Repository > Settings > Secrets and variables > Actions
The following Secrets are to be configured:
- GOOGLE_CREDENTIALS (service account key)
- SLACK_WEBHOOK (for notifications)
```

**Expected result:** The Secrets configuration procedure is explained. Actual configuration is done via the GitHub Web UI.

---

## 🚀 Step 2: Google Authentication Workflow

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Google Authentication Workflow",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:

> **Recommendation**: If possible, prioritize Workload Identity Federation (OIDC).  
> When using service account keys, minifying the JSON to a single line before saving to Secrets makes it less likely to break.

```yaml
Please create the .github/workflows/google-auth.yml file with the following content:

name: Google API Integration

on:
  workflow_dispatch:
    inputs:
      operation:
        description: 'Operation to execute'
        required: true
        default: 'test'
        type: choice
        options:
          - test
          - fetch_data
          - update_sheet

jobs:
  google-operation:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install google-auth google-auth-oauthlib google-api-python-client

      - name: Create credentials file
        run: |
          printf '%s' '${{ secrets.GOOGLE_CREDENTIALS }}' > credentials.json
          chmod 600 credentials.json

      - name: Test Google auth
        if: github.event.inputs.operation == 'test'
        run: |
          python -c "
          from google.oauth2 import service_account
          import json

          try:
              creds = service_account.Credentials.from_service_account_file('credentials.json')
              print('Google authentication successful!')
              print(f'Service account: {creds.service_account_email}')
          except Exception as e:
              print(f'Authentication error: {e}')
              exit(1)
          "

      - name: Cleanup credentials
        if: always()
        run: rm -f credentials.json
```

**Expected result:** A workflow for secure Google authentication is created.

---

## 🚀 Step 3: Data Retrieval Pipeline

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Data Retrieval Pipeline",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```text
Please create the .github/workflows/data-pipeline.yml file with the following content:

name: Data Pipeline

on:
  schedule:
    - cron: '0 1 * * *'  # Daily at 01:00 UTC
  workflow_dispatch:

jobs:
  data-pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pandas requests

      - name: Step 1 - Fetch data
        run: |
          python -c "
          import json
          from datetime import datetime

          # Generate sample data (actually fetched from API)
          data = {
              'timestamp': datetime.now().isoformat(),
              'records': [
                  {'id': 1, 'value': 100},
                  {'id': 2, 'value': 200},
                  {'id': 3, 'value': 300}
              ]
          }

          with open('data.json', 'w') as f:
              json.dump(data, f)

          print('Data retrieval complete')
          "

      - name: Step 2 - Process data
        run: |
          python -c "
          import json
          import pandas as pd

          with open('data.json', 'r') as f:
              data = json.load(f)

          df = pd.DataFrame(data['records'])
          df['processed_at'] = data['timestamp']

          summary = {
              'total_records': len(df),
              'sum_value': int(df['value'].sum()),
              'avg_value': float(df['value'].mean())
          }

          with open('summary.json', 'w') as f:
              json.dump(summary, f)

          print(f'Processing complete: {summary}')
          "

      - name: Step 3 - Save results
        run: |
          mkdir -p output
          mv data.json output/
          mv summary.json output/
          echo "Results saved to output/"
          ls -la output/

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: pipeline-results-${{ github.run_number }}
          path: output/
          retention-days: 7
```

**Expected result:** A data retrieval, processing, and storage pipeline is created.

---

## 🚀 Step 4: Workflow with Notifications

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Workflow with Notifications",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```text
Please create the .github/workflows/notify.yml file with the following content:

name: Pipeline with Notification

on:
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  build-and-notify:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run build
        id: build
        run: |
          echo "Building project..."
          echo "status=success" >> $GITHUB_OUTPUT
          echo "Build completed!"

      - name: Run tests
        id: test
        run: |
          echo "Running tests..."
          echo "Tests passed!"

      - name: Send success notification
        if: success()
        run: |
          echo "Sending success notification..."
          # If Slack Webhook is configured
          # curl -X POST -H 'Content-type: application/json' \
          #   --data '{"text":"Pipeline success: ${{ github.repository }}"}' \
          #   ${{ secrets.SLACK_WEBHOOK }}
          echo "Notification: Pipeline completed successfully!"

      - name: Send failure notification
        if: failure()
        run: |
          echo "Sending failure notification..."
          echo "Notification: Pipeline failed!"

      - name: Summary
        if: always()
        run: |
          echo "## Workflow Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Repository**: ${{ github.repository }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Branch**: ${{ github.ref_name }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Actor**: ${{ github.actor }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Status**: ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

**Expected result:** A workflow that sends notifications after build completion is created.

---

## 🚀 Step 5: Matrix Build

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Matrix Build",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```text
Please create the .github/workflows/matrix.yml file with the following content:

name: Matrix Build

on:
  workflow_dispatch:
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
      fail-fast: false

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Display Python version
        run: |
          python --version
          echo "OS: ${{ matrix.os }}"
          echo "Python: ${{ matrix.python-version }}"

      - name: Run tests
        run: |
          python -c "print('Test passed on ${{ matrix.os }} with Python ${{ matrix.python-version }}')"
```

**Expected result:** A workflow for simultaneous testing across multiple OS and Python versions is created.

---

## ⚠️ Common Issues and Solutions

Use AskQuestion to select the issue, then follow the guidance.

**AskQuestion configuration:**
```json
{
  "title": "Select the issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "Invalid credentials"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Secrets cannot be referenced"},
      {"id": "trouble_4", "label": "Artifacts are not uploaded"}
    ]
  }]
}
```


### Issue 1: "Invalid credentials"
**Cause:** Secret value is incorrect or JSON format is invalid
**Solution prompt:**
```text
Please check the GOOGLE_CREDENTIALS Secret value.
Copy the entire JSON file content and set it.
Verify that line breaks and spaces are correctly included.
```

### Issue 2: "Permission denied"
**Cause:** Insufficient service account permissions
**Solution prompt:**
```text
Please check the service account permissions in the Google Cloud Console.
Verify that the required APIs are enabled.
Verify that IAM roles are properly configured.
```

### Issue 3: Secrets cannot be referenced
**Cause:** Typo in Secret name or Secret is not configured
**Solution prompt:**
```text
Please check the Secret name in the GitHub repository Settings > Secrets and variables > Actions.
Verify that it is referenced in the format secrets.SECRET_NAME.
```

### Issue 4: Artifacts are not uploaded
**Cause:** Path does not exist or file size is exceeded
**Solution prompt:**
```text
Please verify that the directory specified in path exists.
Verify that the file size does not exceed the limit (500MB).
```

---

## ✅ Checkpoint
- [ ] Understand the Repository Secrets configuration procedure
- [ ] google-auth.yml has been created
- [ ] data-pipeline.yml has been created
- [ ] notify.yml has been created
- [ ] matrix.yml has been created
- [ ] Understand how to handle Secrets securely


---

## 📋 Deliverable Preview

### Expected Output
```text
📁 .github/workflows/
└── {workflow}.yml  (GitHub Actions workflow)
```

### Verification Commands
```bash
# List workflow files
ls -la .github/workflows/

# Check file contents
cat .github/workflows/{workflow}.yml

# Check execution status on GitHub
gh run list --limit 5
```

---

## ✅ Completion Check
Paste the following into chat to verify completion:

```text
# Completion check: Please verify that the expected output files have been generated in the output/ folder.
```

**Expected result:** Completion/incomplete status and missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin a new section.

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-12-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-12-1
- finish → End

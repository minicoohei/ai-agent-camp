---
description: "When the user says /start-8-1 — Module 8 Lesson 8-1: BigQuery Connection and Authentication Setup"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
duration: "~25 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["data", "bigquery", "gcp", "authentication"]
---

# 🎓 Lesson 8-1: BigQuery Connection and Authentication Setup

## 📍 What You'll Do

**Lesson 8-1: BigQuery Connection and Authentication Setup** !

| Item | Details |
|------|------|
| Goal | Configure GCP authentication, connect to BigQuery, and access public datasets |
| Duration | ~25 min |
| Skills used | bigquery-auth, gcloud CLI |
| Prerequisites | Access to a Google Cloud project, Python 3.8+, gcloud CLI installed |
| Course page | [Module 8: Data Analysis](https://ai-agent.camp/en/course/module-8) alongside this lesson |

**Session flow:**
1. Verify GCP authentication
2. Execute authentication (if not configured)
3. BigQuery connection test
4. Access public datasets

By the end of this session, you will be able to execute queries in BigQuery.

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

## 🚀 Step 1: Verify GCP Authentication

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Verify GCP Authentication",
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
```
Please check the GCP (Google Cloud Platform) authentication status.

Items to check:
1. Whether gcloud CLI is installed
2. Current authenticated account
3. Current project ID
4. Application Default Credentials (ADC) status

If there are any issues, please provide solutions.
```

**Expected result:** The authentication status is displayed, and setup steps are provided as needed.

---

## 🚀 Step 2: Run Authentication (If Not Configured)

If authentication is not configured, set it up with the following prompt:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Run Authentication (If Not Configured)",
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
```
Please configure authentication to access BigQuery.

Authentication to run:
1. gcloud auth login (main authentication)
2. gcloud auth application-default login (for Python SDK)

Please execute each command and
confirm whether they succeeded.
```

**Expected result:** The browser opens and authentication with your Google account is completed.

---

## 🚀 Step 3: BigQuery Connection Test

After authentication is complete, test the BigQuery connection:

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: BigQuery Connection Test",
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
```
Please run a BigQuery connection test.

Test contents:
1. Initialize BigQuery Python client
2. Get current project ID
3. Execute a simple test query

Test query:
SELECT CURRENT_TIMESTAMP() as current_time,
       @@project_id as project_id,
       "connection_success" as status
```

**Expected result:** A connection success message and the project ID are displayed.

---

## 🚀 Step 4: Access Public Datasets

Access the Google public dataset (GA4 E-commerce sample):

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Access Public Datasets",
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
```
Please verify access to the BigQuery public dataset
(GA4 E-commerce sample).

Test query:
SELECT
    COUNT(*) as event_count,
    COUNT(DISTINCT user_pseudo_id) as unique_users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20210101`

Please display the results.
```

**Expected result:** Event count and user count from the GA4 sample dataset are displayed.

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
      {"id": "trouble_1", "label": "gcloud: command not found"},
      {"id": "trouble_2", "label": "File xxx was not found"},
      {"id": "trouble_3", "label": "403 Forbidden / Permission denied"},
      {"id": "trouble_4", "label": "Reauthentication needed"}
    ]
  }]
}
```


### Issue 1: "gcloud: command not found"
**Cause:** gcloud CLI is not installed
**Solution prompt:**
```
Please show me how to install gcloud CLI (Google Cloud SDK).
Please provide the steps for macOS.
```

### Issue 2: "File xxx was not found"
**Cause:** The GOOGLE_APPLICATION_CREDENTIALS environment variable points to an invalid path
**Solution prompt:**
```
Please check the GOOGLE_APPLICATION_CREDENTIALS environment variable.
If an invalid value is set, please show me how to clear it.
```

### Issue 3: "403 Forbidden / Permission denied"
**Cause:** No BigQuery permissions
**Solution prompt:**
```
Please tell me the IAM permissions required to access BigQuery.
Also, please show me how to check the permissions set on the current account.
```

### Issue 4: "Reauthentication needed"
**Cause:** Authentication token expired
**Solution prompt:**
```
The BigQuery authentication token has expired.
Please re-authenticate.
```

### Resetting ADC Authentication
If `GOOGLE_APPLICATION_CREDENTIALS` points to an old path:
```bash
unset GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login
```

---

## ✅ Checkpoint
- [ ] gcloud CLI is installed
- [ ] Authentication completed with gcloud auth login
- [ ] ADC configured with gcloud auth application-default login
- [ ] BigQuery client initialized
- [ ] Test query executed successfully
- [ ] Accessed public dataset (GA4 Sample)

---

## 📚 Supplementary: Multi-Project Environment

When managing multiple GCP projects:

```
Please show me how to create gcloud configuration profiles
for managing multiple GCP projects.

Example:
- project-a: development environment
- project-b: production environment

Please also show me how to switch between profiles.
```


---

## 📋 Deliverable Preview

The deliverables for this lesson are terminal outputs.

### Expected Output Example
```
┌─────────────────────────────────────┐
│  Command execution result               │
│  Status: ✅ Success                      │
│  Records processed: N                    │
└─────────────────────────────────────┘
```

> 💡 To save output to a file, add ` > output/result.txt` at the end of the command

---

## ✅ Completion Check
Paste the following into chat to verify completion:

```
# Completion check: Please verify that the expected output files have been generated in the output/ folder.
```

**Expected result:** A pass/fail judgment and any missing items are displayed.

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
      {"id": "next_window", "label": "Start in new window (/start-8-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-8-2
- finish → End

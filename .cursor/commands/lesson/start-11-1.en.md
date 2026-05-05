---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
prerequisites: ["start-0-1"]
duration: "~35 min"
level: "intermediate"
tags: ["github-actions", "ci-cd", "automation"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 11-1: GitHub Actions Basics

## 📍 What You'll Do

**Lesson 11-1: Introduction to GitHub Actions**!

| Item | Details |
|------|------|
| Goal | Build CI/CD pipelines with GitHub Actions (automated testing and deployment) |
| Duration | ~35 min |
| Skills used | GitHub Actions, YAML workflows |
| Prerequisites | GitHub repository, Lesson 0-1 (gh CLI) completion recommended |
| Course page | [Module 11: GitHub Actions](https://ai-agent.camp/en/course/module-11)  alongside this lesson |

**Session flow:**
1. Create the workflow directory
2. Hello World workflow
3. Python environment setup workflow
4. Scheduled execution workflow
5. Multi-job workflow

By the end of this session, tests and deployments will run automatically on push.

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

## 🚀 Step 1: Create Workflow Directory

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Create Workflow Directory",
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
Please create the GitHub Actions workflow directory in the ai-agent-camp project.

mkdir -p .github/workflows

Verify that the directory has been created.
```

**Expected result:** The `.github/workflows/` directory is created.

---

## 🚀 Step 2: Hello World Workflow

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Hello World Workflow",
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
Please create the .github/workflows/hello.yml file with the following content:

name: Hello World

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest

    steps:
      - name: Say Hello
        run: echo "Hello, GitHub Actions!"

      - name: Print Date
        run: date

      - name: Print Environment
        run: |
          echo "GitHub Actor: ${{ github.actor }}"
          echo "GitHub Repository: ${{ github.repository }}"
          echo "GitHub Event: ${{ github.event_name }}"
```

**Expected result:** A YAML file is created. It runs automatically when pushed to GitHub.

---

## 🚀 Step 3: Python Environment Setup Workflow

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Python Environment Setup Workflow",
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
Please create the .github/workflows/python-ci.yml file with the following content:

name: Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
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
          # uv は自動で最新のパッケージを管理します
          uv add pytest
          if [ -f pyproject.toml ]; then uv sync; fi

      - name: Run simple test
        run: |
          python -c "print('Python CI is working!')"
          python --version
```

**Expected result:** A workflow for Python environment setup and test execution is created.

---

## 🚀 Step 4: Scheduled Execution Workflow

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Scheduled Execution Workflow",
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
Please create the .github/workflows/scheduled.yml file with the following content:

name: Scheduled Task

on:
  schedule:
    # Execute daily at 09:00 UTC (18:00 JST)
    - cron: '0 9 * * *'
  workflow_dispatch:
    inputs:
      task_name:
        description: 'Task name'
        required: true
        default: 'daily_check'
        type: choice
        options:
          - daily_check
          - weekly_report

jobs:
  scheduled-task:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run scheduled task
        run: |
          echo "Running scheduled task at $(date)"
          echo "Task: ${{ github.event.inputs.task_name || 'daily_check' }}"

      - name: Check files
        run: |
          echo "Repository files:"
          ls -la
```

**Expected result:** A workflow supporting both scheduled and manual triggers is created.

---

## 🚀 Step 5: Multi-Job Workflow

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Multi-Job Workflow",
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
Please create the .github/workflows/multi-job.yml file with the following content:

name: Multi-Job Workflow

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      build_status: ${{ steps.build.outputs.status }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build
        id: build
        run: |
          echo "Building project..."
          echo "status=success" >> $GITHUB_OUTPUT
          echo "Build completed!"

  test:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Test
        run: |
          echo "Build status: ${{ needs.build.outputs.build_status }}"
          echo "Running tests..."
          echo "Tests passed!"

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy
        run: |
          echo "Deploying to production..."
          echo "Deployment completed!"
```

**Expected result:** A multi-job workflow that runs in the order build -> test -> deploy is created.

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
      {"id": "trouble_1", "label": "Workflow file invalid"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Command not found"},
      {"id": "trouble_4", "label": "Scheduled execution does not work"}
    ]
  }]
}
```


### Issue 1: "Workflow file invalid"
**Cause:** YAML syntax error
**Solution prompt:**
```
Please check the YAML file syntax.
Verify that indentation uses 2 spaces consistently.
Verify that there is a space after colons.
```

### Issue 2: "Permission denied"
**Cause:** Script does not have execution permissions
**Solution prompt:**
```
Please add a step to run chmod +x script.sh within the workflow.
```

### Issue 3: "Command not found"
**Cause:** Required programs are not installed
**Solution prompt:**
```
Please add setup actions such as actions/setup-python and actions/setup-node.
Add a step to install the required packages.
```

### Issue 4: Scheduled execution does not work
**Cause:** Cron configuration error or not running on the default branch
**Solution prompt:**
```
Please verify that the cron expression is correct (specified in UTC time).
Verify that the workflow exists on the default branch (main).
Manually trigger with workflow_dispatch to verify operation.
```

---

## ✅ Checkpoint
- [ ] The .github/workflows/ directory exists
- [ ] hello.yml has been created
- [ ] python-ci.yml has been created
- [ ] scheduled.yml has been created
- [ ] multi-job.yml has been created
- [ ] Workflows are displayed on GitHub


---

## 📋 Deliverable Preview

### Expected Output
```
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

```
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
      {"id": "next_window", "label": "Start in new window (/start-11-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-11-2
- finish → End

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
duration: "~25 min"
prerequisites: ["start-11-2"]
level: "intermediate"
tags: ["github-actions", "claude-code", "codex", "ai", "automation", "code-review"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 11-4: Running Claude Code / Codex / Cursor in GitHub Actions

## 📍 What You'll Do

**Lesson 11-4: Running AI CLI in GitHub Actions**!

| Item | Details |
|------|------|
| Goal | Run Claude Code CLI / Codex CLI within GitHub Actions workflows for automated code review and PR generation |
| Duration | ~25 min |
| Skills used | GitHub Actions, Claude Code CLI, Codex CLI, gh CLI |
| Prerequisites | Lesson 11-2 completed (understanding of Secrets configuration) |

**Session flow:**
1. Overview of AI CLI tools and usage patterns
2. Run Claude Code in a workflow
3. Create a PR auto-review workflow
4. Run Codex CLI in a workflow
5. Hands-on exercise: Issue → AI implementation → auto-PR pipeline

By the end of this session, you'll have workflows built that leverage AI CLI tools in GitHub Actions.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume.

---

## 🎯 Readiness Check

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
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Verify Lesson 11-2 completion. Check API key availability)
(different_lesson → Display module list)

---

## 🚀 Step 1: Overview of AI CLI Tools

```json
{
  "title": "🚀 Step 1: AI CLI Tools Overview",
  "questions": [{
    "id": "step_action",
    "prompt": "Review the AI CLI tools available for use in GitHub Actions.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review the differences between each tool"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

| Tool | Command | API Key | Primary Use |
|--------|---------|---------|---------|
| Claude Code | `claude -p "prompt"` | `ANTHROPIC_API_KEY` | Code review, implementation, analysis |
| Codex CLI | `codex -q "prompt"` | `OPENAI_API_KEY` | Code generation, fixes, Q&A |

**Common pattern for GitHub Actions:**
```yaml
# Always pass API keys via Secrets
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**API keys to set in Secrets:**
- `ANTHROPIC_API_KEY`: For Claude Code (obtain from Anthropic console)
- `OPENAI_API_KEY`: For Codex (obtain from OpenAI console)

**Expected result:** Understand the differences between each tool and the required configuration.

---

## 🚀 Step 2: Run Claude Code in a Workflow

```json
{
  "title": "🚀 Step 2: Claude Code Workflow",
  "questions": [{
    "id": "step_action",
    "prompt": "Create a workflow that runs Claude Code CLI in GitHub Actions.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review claude CLI options"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Create `.github/workflows/claude-review.yml`:

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]
  workflow_dispatch:
    inputs:
      prompt:
        description: 'Prompt to send to Claude'
        type: string
        default: 'Analyze the code quality of this repository'

jobs:
  claude-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Claude Code review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            DIFF=$(git diff ${{ github.event.pull_request.base.sha }}..HEAD)
            PROMPT="Please review the following diff. Summarize issues, improvement suggestions, and good points:\n\n$DIFF"
          else
            PROMPT="${{ inputs.prompt }}"
          fi
          claude -p "$PROMPT" --output-format text > review_result.txt

      - name: Post review comment
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review_result.txt', 'utf8');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## 🤖 Claude Code Review\n\n${review}`
            });
```

**Key points:**
- Use `claude -p` to pass a prompt directly (non-interactive mode)
- On PR trigger, pass `git diff` for review
- Use `actions/github-script` to post the review result as a PR comment

**Expected result:** When a PR is created, Claude Code automatically reviews it and posts a comment.

---

## 🚀 Step 3: PR Auto-Review Workflow

```json
{
  "title": "🚀 Step 3: PR Auto-Review",
  "questions": [{
    "id": "step_action",
    "prompt": "Enhance the workflow to analyze PR changes and post structured review comments.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review the review criteria"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Enhance the review prompt:

```yaml
      - name: Run structured review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          DIFF=$(git diff ${{ github.event.pull_request.base.sha }}..HEAD)
          cat <<'PROMPT' > /tmp/review_prompt.txt
          Please review the following diff.

          ## Review Criteria
          1. **Bug Risk**: Potential bugs and edge cases
          2. **Security**: Vulnerabilities and hardcoded secrets
          3. **Performance**: Inefficient processing and N+1 issues
          4. **Readability**: Naming, structure, and comment quality
          5. **Testing**: Insufficient test coverage

          ## Output Format
          For each criterion, respond with either "✅ No issues" or "⚠️ Needs attention: specific finding".

          ## Diff
          PROMPT
          echo "$DIFF" >> /tmp/review_prompt.txt
          claude -p "$(cat /tmp/review_prompt.txt)" --output-format text > review_result.txt
```

**Expected result:** Structured review comments are posted on the PR.

---

## 🚀 Step 4: Run Codex CLI in a Workflow

```json
{
  "title": "🚀 Step 4: Codex CLI",
  "questions": [{
    "id": "step_action",
    "prompt": "Create a workflow that runs Codex CLI in GitHub Actions.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review Codex CLI options"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Create `.github/workflows/codex-task.yml`:

```yaml
name: Codex Task Runner
on:
  workflow_dispatch:
    inputs:
      task:
        description: 'Task for Codex to execute'
        type: string
        required: true

jobs:
  codex-run:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Install Codex CLI
        run: npm install -g @openai/codex

      - name: Run Codex
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex -q "${{ inputs.task }}" --approval-mode full-auto
          
      - name: Check for changes
        id: changes
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
          fi

      - name: Create PR with changes
        if: steps.changes.outputs.has_changes == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          BRANCH="codex/auto-$(date +%Y%m%d-%H%M%S)"
          git checkout -b "$BRANCH"
          git add -A
          git commit -m "feat: Auto-implementation by Codex — ${{ inputs.task }}"
          git push origin "$BRANCH"
          gh pr create \
            --title "🤖 Codex: ${{ inputs.task }}" \
            --body "Auto-implementation by Codex CLI.\n\nTask: ${{ inputs.task }}" \
            --base main
```

**Key points:**
- `--approval-mode full-auto` enables fully automatic execution
- A PR is automatically created if there are changes
- `GITHUB_TOKEN` is automatically provided by GitHub

**Expected result:** Specifying a task via `gh workflow run` causes Codex to implement it and create a PR.

---

## 🚀 Step 5: Hands-On Exercise — Issue → AI Implementation → PR Pipeline

```json
{
  "title": "🚀 Step 5: Hands-On Exercise",
  "questions": [{
    "id": "step_action",
    "prompt": "Build a pipeline that automatically implements when an Issue is created and creates a PR.",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Review how Issue triggers work"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Create `.github/workflows/ai-implement.yml`:

```yaml
name: AI Auto-Implement
on:
  issues:
    types: [labeled]

jobs:
  implement:
    if: contains(github.event.issue.labels.*.name, 'ai-implement')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Implement from issue
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          TITLE="${{ github.event.issue.title }}"
          BODY="${{ github.event.issue.body }}"
          claude -p "Please implement the following Issue:\n\nTitle: $TITLE\n\nBody:\n$BODY" \
            --output-format text > implementation_log.txt

      - name: Create PR
        if: ${{ success() }}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            BRANCH="ai/issue-${{ github.event.issue.number }}"
            git checkout -b "$BRANCH"
            git add -A
            git commit -m "feat: AI implementation for #${{ github.event.issue.number }}"
            git push origin "$BRANCH"
            gh pr create \
              --title "🤖 AI Implementation: ${{ github.event.issue.title }}" \
              --body "Closes #${{ github.event.issue.number }}\n\nAuto-implementation by Claude Code." \
              --base main
          fi
```

**Test procedure:**
1. Create an Issue (e.g., "Add a Contributing section to the README")
2. Add the `ai-implement` label
3. The workflow runs automatically → a PR is created

**Expected result:** A PR is automatically generated from a labeled Issue.

---

## ⚠️ Common Issues and Solutions

```json
{
  "title": "⚠️ Troubleshooting",
  "questions": [{
    "id": "trouble",
    "prompt": "Are you experiencing any issues?",
    "options": [
      {"id": "trouble_1", "label": "API key error"},
      {"id": "trouble_2", "label": "claude / codex command not found"},
      {"id": "trouble_3", "label": "PR creation permission error"},
      {"id": "trouble_4", "label": "Review comment not posted"}
    ]
  }]
}
```

### Issue 1: "API key error"
**Cause**: API key is not set in Secrets, or the key is invalid.
**Solution prompt:**
```text
Check that ANTHROPIC_API_KEY is set in the repository's Settings → Secrets and variables → Actions. The key is a string that starts with sk-ant-.
```

### Issue 2: "claude / codex command not found"
**Cause**: The npm install step failed.
**Solution prompt:**
```text
Check the error in the npm install step in the workflow logs. Verify that the Node.js version is 18 or higher.
```

### Issue 3: "PR creation permission error"
**Cause**: Missing `permissions` configuration.
**Solution prompt:**
```text
Verify that the workflow permissions include contents: write and pull-requests: write. Also check that "Read and write permissions" is enabled in the repository's Settings → Actions → General → Workflow permissions.
```

### Issue 4: "Review comment not posted"
**Cause**: The `actions/github-script` script has an error, or pull-requests: write permission is missing.
**Solution prompt:**
```text
Check the error in the actions/github-script step in the workflow logs. If review_result.txt is empty, check the Claude Code execution result.
```

---

## ✅ Checkpoint

- [ ] Claude Code CLI can run within a workflow
- [ ] Review comments are posted on PR trigger
- [ ] Codex CLI can run within a workflow
- [ ] The Issue → AI implementation → PR pipeline works
- [ ] API keys are securely stored in Secrets

---

## 📋 Deliverable Preview

**Workflows created:**
```text
.github/workflows/
├── claude-review.yml      # PR auto-review
├── codex-task.yml         # Codex task runner
└── ai-implement.yml       # Issue → AI implementation → PR
```

---

## ➡️ Next Steps

```json
{
  "title": "➡️ Next Steps",
  "questions": [{
    "id": "next_step",
    "prompt": "What would you like to do next?",
    "options": [
      {"id": "next_auto", "label": "Move on to Lesson 11-5 (Deploy & File Generation) → /start-11-5"},
      {"id": "review_module", "label": "Review this lesson's deliverables"},
      {"id": "finish", "label": "Finish for today"}
    ]
  }]
}
```

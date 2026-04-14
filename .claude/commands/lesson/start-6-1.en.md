---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
duration: "~30 min"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["agent", "command", "cursor"]
---

# 🎓 Lesson 6-1: Custom Command Creation Basics

## 📍 What You'll Do

**Lesson 6-1: Custom Command Creation Basics** !

| Item | Details |
|------|---------|
| Goal | Create custom commands (.cursor/commands/) in Cursor for team reuse |
| Duration | ~30 min |
| Skills Used | Cursor Commands, Markdown（YAML frontmatter） |
| Prerequisites | Using Cursor, ai-agent-camp is open |
| Course Page | [Module 6: Agent Development](https://ai-agent.camp/en/course/module-6) in parallel |

**Session flow:**
1. Check the command directory structure
2. Create simple commands (project-info, env-check, run-tests)
3. Verify operation

By the end of this session, you will be able to use commands for yourself and your team.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Check Command Directory Structure

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Check the command directory structure",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```text
Check the command directory structure of the ai-agent-camp project.

Verify that the following directories exist:
- .cursor/commands/
- .cursor/commands/lesson/
- .cursor/commands/utility/

Create them if they do not exist.
```

**Expected result**: The command directory structure is confirmed and created.

---

## 🚀 Step 2: Create Simple Commands

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Create simple commands",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
````text
Create the file .cursor/commands/project-info.md with the following content:

---
description: "Display project information"
---

# Project Information

## Overview
This project is a base platform for AI agent development.

## Directory Structure
```
ai-agent-camp/
├── .claude/         # Claude Code configuration
│   └── skills/      # Reusable skills
├── .cursor/         # Cursor IDE configuration
│   └── commands/    # Custom commands
│   └── commands/    # Custom commands for Cursor
├── skills/          # Master copy of common skills
├── course/          # HTML course materials
└── tools/           # Python scripts
```

## Technology Stack
- AI Framework: Claude 3.5 Sonnet
- Protocol: MCP (Model Context Protocol)
- IDE: Cursor / Claude Code
````

**Expected result**: `/project-info` command is created.

---

## 🚀 Step 3: Environment Check Command

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Environment check command",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
````text
Create the file .cursor/commands/env-check.md with the following content:

---
description: "Check development environment status"
---

# Environment Check

A command to check the status of your development environment.

## Checklist

Run the following commands to verify your environment:

### 1. Check Node.js Version
```bash
node --version
```
Expected: v18.x or later

### 2. Check Python Version
```bash
python3 --version    # On Windows, python --version
```
Expected: Python 3.9 or later

### 3. Check Git Settings
```bash
git config user.name
git config user.email
```

### 4. Check npm Packages
```bash
npm list -g --depth=0
```

### 5. Check pip Packages
```bash
pip list | head -20
```

## Troubleshooting
If you encounter any issues, verify your setup with `/start-0-1`.
````

**Expected result**: `/env-check` command is created.

---

## 🚀 Step 4: Test Execution Command

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Test execution command",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
````text
Create the file .cursor/commands/run-tests.md with the following content:

---
description: "Run project tests"
---

# Test Execution

A command to run project tests.

## Python Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Tests with Coverage
```bash
pytest tests/ -v --cov=src/ --cov-report=term-missing
```

### Run Specific Test File
```bash
pytest tests/test_specific.py -v
```

## JavaScript Tests (Node.js)

### npm Tests
```bash
npm test
```

### Specific Test File
```bash
npx jest tests/specific.test.js
```

## Interpreting Test Results

- ✅ PASSED: Test passed
- ❌ FAILED: Test failed (check error details)
- ⚠️ SKIPPED: Skipped test
- 📊 Coverage: Coverage rate (target: 80% or higher)
````

**Expected result**: `/run-tests` command is created.

---

## 🚀 Step 5: Verify Command Operation

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Verify command operation",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```text
Check the list and operation of the created commands:

1. List the files in the .cursor/commands/ directory
2. Extract the description from each command file
3. Verify that the naming convention is consistent

Created commands:
- /project-info
- /env-check
- /run-tests

Verify that each command is recognized by Cursor.
```

**Expected result**: You can confirm that the created commands are correctly recognized.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "Command is not recognized"},
      {"id": "trouble_2", "label": "description is not displayed"},
      {"id": "trouble_3", "label": "Code inside command is not executed"},
      {"id": "trouble_4", "label": "Japanese text has character encoding issues"}
    ]
  }]
}
```


### Issue 1: "Command is not recognized"
**Cause**: File path is incorrect, or Markdown format is invalid
**Solution prompt**:
```text
Check the following:
1. Is the file in the .cursor/commands/ directory?
2. Is the file extension .md?
3. Is the frontmatter (section enclosed by ---) formatted correctly?
```

### Issue 2: "description is not displayed"
**Cause**: YAML frontmatter syntax error
**Solution prompt**:
```text
Check the frontmatter format:
---
description: "description text"
---

Note: A space is required after the colon.
```

### Issue 3: "Code inside command is not executed"
**Cause**: Commands are instructions and are not auto-executed
**Solution prompt**:
```text
Cursor commands function as "templates".
Code blocks within commands need to be copied & pasted by the user,
or you need to instruct the AI with "execute this command".
```

### Issue 4: "Japanese text has character encoding issues"
**Cause**: File encoding is not UTF-8
**Solution prompt**:
```text
Verify that the file is saved in UTF-8.
Set the default encoding to UTF-8 in Cursor settings.
```

---

## ✅ Checkpoint
- [ ] .cursor/commands/ directory exists
- [ ] project-info.md is created
- [ ] env-check.md is created
- [ ] run-tests.md is created
- [ ] Commands are recognized in Cursor


---

## 📋 Output Preview

### Expected Output
```text
📁 output/
└── {project-name}/  (agent/code artifacts)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/{project-name}/

# Check the beginning (first 30 lines)
head -30 output/{project-name}/
```

> 💡 View full text: `cat output/{project-name}/` to display the full text

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```text
# Completion check: Verify that expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-6-2)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-6-2
- finish → End

---
description: "When the user says /start-6-3 — Module 6 Lesson 6-3: Cursor Rules Configuration"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1"]
duration: "~25 min"
level: "intermediate"
tags: ["agent", "rules", "cursor"]
---

# 🎓 Lesson 6-3: Cursor Rules Configuration

## 📍 What You'll Do

**Lesson 6-3: Cursor Rules Configuration** !

| Item | Details |
|------|---------|
| Goal | Control AI behavior, context, and constraints with Cursor Rules (.cursor/rules/) |
| Duration | ~25 min |
| Skills Used | Cursor Rules, .mdc files |
| Prerequisites | Lesson 6-1 completed, using Cursor |
| Course Page | [Module 6: Agent Development](https://ai-agent.camp/en/course/module-6) in parallel |

**Session flow:**
1. Create the Rules directory
2. Define project rules (coding standards, security)
3. Verify operation

By the end of this session, the AI will respond according to project rules.

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

## 🚀 Step 1: Create Rules Directory

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Create the Rules directory",
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
```
Create the .cursor/rules/ directory and prepare the structure for Cursor Rules.

mkdir -p .cursor/rules

Verify the directory has been created.
```

**Expected result**: The `.cursor/rules/` directory is created.

---

## 🚀 Step 2: Create Basic Rules

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Create basic Rules",
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
```
Create the file .cursor/rules/rules.md with the following content:

# Cursor Rules - AI Agent Development Project

## Project Overview
Base platform for AI agent development
- Python 3.11+
- REST API with FastAPI
- Claude AI API integration
- GitHub Actions CI/CD

---

## Coding Conventions

### Python Style
- **PEP 8 compliant**: All code
- **Line length**: 100 characters or fewer
- **Indentation**: 4 spaces
- **Naming**:
  - Functions/variables: snake_case
  - Classes: PascalCase
  - Constants: UPPER_CASE

### Code Sample
```python
# Good example
def calculate_user_score(user_id: int) -> float:
    """Calculate user score"""
    user = get_user(user_id)
    return user.points * user.multiplier

# Avoid this
def calc(u):
    return get_user(u).pts * get_user(u).m
```

---

## Security Rules

### Required Check Items
- Input validation: All endpoints
- SQL injection prevention: Use ORM
- Authentication: Use JWT tokens
- Logging: Do not include sensitive information
- Environment variables: Managed via .env

### Prohibited
- Hard-coded passwords
- Sensitive information in log output
- Direct SQL statement execution

---

## AI (Claude) Guidelines

### Do
- Conciseness: Implement features with minimal code
- Readability: Implementation easy for others to understand
- Error handling: Handle foreseeable errors
- Test code: Provide alongside implementation

### Avoid
- Long functions: Keep to 30 lines or fewer per function
- Global variables: Avoid whenever possible
- Magic numbers: Define as constants
```

**Expected result**: A basic Rules file is created.

---

## 🚀 Step 3: Create Security Rules

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Create security Rules",
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
```
Create the file .cursor/rules/security.md with the following content:

# Security-Focused Rules

## Authentication & Authorization

### JWT Tokens
JWT verification required for all API endpoints

```python
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/data")
async def get_data(token = Depends(security)):
    user = verify_token(token.credentials)
    return fetch_user_data(user.id)
```

### Input Validation
Automatic validation using Pydantic models

```python
from pydantic import BaseModel, EmailStr

class UserInput(BaseModel):
    email: EmailStr
    age: int  # Automatic type checking
```

## Logging Security

```python
# Avoid
logger.info(f"User {user.password} logged in")

# Recommended
logger.info(f"User {user.id} logged in")
```

## Environment Variable Management

```python
# Managed in .env file
DATABASE_URL=postgresql://...
API_KEY=secret_xxx

# Load in code
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")
```
```

**Expected result**: A security-specific Rules file is created.

---

## 🚀 Step 4: Create Testing Rules

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Create testing Rules",
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
```
Create the file .cursor/rules/testing.md with the following content:

# Testing Conventions

## Test Coverage Targets
- Overall: 80% or higher
- Business logic: 90% or higher
- API endpoints: 85% or higher

## Types of Tests

### Unit Tests
Verify function inputs and outputs

```python
def test_calculate_score():
    result = calculate_score(points=100)
    assert result > 0
    assert result <= 100
```

### Integration Tests
Tests combining multiple modules

```python
def test_user_registration_flow():
    user = create_user(email="test@example.com")
    assert user.id > 0
    assert db.query(User).filter(User.id == user.id).first()
```

## Test Execution Commands

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/ --cov-report=term-missing

# Specific marker
pytest tests/ -m "unit"
```

## Test Naming Conventions
- File name: test_<module_name>.py
- Function name: test_<feature>_<condition>_<expected_result>

Example: test_login_with_invalid_password_returns_401
```

**Expected result**: A testing-specific Rules file is created.

---

## 🚀 Step 5: Verify Rules Application

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Verify Rules application",
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
```
Please verify the list and contents of the Rules files you created:

1. List the files in the .cursor/rules/ directory
2. Summarize the key points of each Rules file
3. Verify that the Rules apply to the entire project

After verification, write a simple Python function and verify it follows the Rules.
Example: An API endpoint to retrieve user information
```

**Expected result**: Rules files are recognized by Cursor and referenced during code generation.

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
      {"id": "trouble_1", "label": "Rules are not applied"},
      {"id": "trouble_2", "label": "Rules are too long to load"},
      {"id": "trouble_3", "label": "AI ignores Rules"},
      {"id": "trouble_4", "label": "Rules conflict"}
    ]
  }]
}
```


### Issue 1: "Rules are not applied"
**Cause**: File path is incorrect, or Cursor has not reloaded
**Solution prompt**:
```
Check the following:
1. Is the file in .cursor/rules/?
2. Restart Cursor to reload Rules
3. Verify the file extension is .md
```

### Issue 2: "Rules are too long to load"
**Cause**: File size is too large
**Solution prompt**:
```
Split your Rules files:
- rules.md (basic rules)
- security.md (security)
- testing.md (testing)
Keep each file at a reasonable size.
```

### Issue 3: "AI ignores Rules"
**Cause**: Rules description is ambiguous, or priority is too low
**Solution prompt**:
```
Write Rules more clearly:
- Use "must" instead of "recommended"
- Include specific code examples
- Clearly state prohibited actions
```

### Issue 4: "Rules conflict"
**Cause**: Multiple Rules files have contradictory instructions
**Solution prompt**:
```
Check for contradictions between Rules files.
Prioritize the basic rules (rules.md) and use specialized rules as supplements.
```

---

## ✅ Checkpoint
- [ ] .cursor/rules/ directory exists
- [ ] rules.md has been created
- [ ] security.md has been created
- [ ] testing.md has been created
- [ ] Code is generated in accordance with Rules


---

## 📋 Output Preview

### Expected Output
```
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

```
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
      {"id": "next_window", "label": "Start in new window (/start-6-4)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-6-4
- finish → End

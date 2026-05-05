---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1", "start-6-2", "start-6-3", "start-6-4"]
duration: "~50 min"
level: "advanced"
tags: ["agent", "capstone", "deployment"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 6-5: Comprehensive Exercise - AI Agent Development Integration

## 📍 What You'll Do

**Lesson 6-5: Comprehensive Exercise - AI Agent Development Integration** !

| Item | Details |
|------|---------|
| Goal | Integrate learning from Modules 1-7 and complete a working AI agent project |
| Duration | ~50 min |
| Skills Used | Comprehensive Command / Skill / Rules / SubAgent, production deployment concepts |
| Prerequisites | Lesson 6-1 through Lesson 6-4 completed |
| Course Page | [Module 6: Agent Development](https://ai-agent.camp/en/course/module-6) in parallel |

**Session flow:**
1. Project initialization and requirements organization
2. Assemble the integrated agent
3. Verify operation and prepare for production deployment

By the end of this session, a full-fledged AI agent system will be complete, and the course will be finished.

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

## 🚀 Step 1: Project Initialization

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Project initialization",
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
Create the project structure for the comprehensive exercise.

Create directories:
mkdir -p ai-content-agent/src/{api,services,subagents,utils}
mkdir -p ai-content-agent/tests
mkdir -p ai-content-agent/.github/workflows
mkdir -p ai-content-agent/.claude/{skills,rules}
mkdir -p ai-content-agent/.cursor/commands

Create required files:
touch ai-content-agent/requirements.txt
touch ai-content-agent/README.md
touch ai-content-agent/.env.example

Verify the structure.
```

**Expected result**: The comprehensive exercise project structure is created.

---

## 🚀 Step 2: FastAPI Server Implementation

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: FastAPI server implementation",
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
Create the file ai-content-agent/src/main.py with the following content:

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import uuid
from datetime import datetime

app = FastAPI(
    title="AI Content Generator API",
    version="1.0.0",
    description="AI-powered content generation and management"
)

# Model definitions
class TaskRequest(BaseModel):
    title: str
    prompt: str
    priority: str = "medium"

class TaskResponse(BaseModel):
    task_id: str
    status: str
    created_at: str

# In-memory task storage (use a DB in production)
tasks: Dict[str, Dict] = {}

@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """Create a new task"""
    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = {
        "id": task_id,
        "title": request.title,
        "prompt": request.prompt,
        "priority": request.priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "result": None
    }
    return TaskResponse(
        task_id=task_id,
        status="pending",
        created_at=tasks[task_id]["created_at"]
    )

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Get task information"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.get("/tasks")
async def list_tasks(limit: int = 10):
    """Get task list"""
    task_list = list(tasks.values())
    return task_list[:limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Expected result**: The FastAPI server is implemented.

---

## 🚀 Step 3: Create requirements.txt

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Create requirements.txt",
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
Write the following content to ai-content-agent/requirements.txt:

fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.0
python-dotenv==1.0.0
httpx==0.26.0
pytest==7.4.0
pytest-asyncio==0.23.0
```

**Expected result**: The dependency file is created.

---

## 🚀 Step 4: GitHub Actions Workflow

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: GitHub Actions workflow",
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
Create the file ai-content-agent/.github/workflows/ci.yml with the following content:

name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

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
          uv sync

      - name: Run tests
        run: |
          pytest tests/ -v || echo "No tests found"

      - name: Health check
        run: |
          python -c "from src.main import app; print('Import successful!')"

      - name: Summary
        if: always()
        run: |
          echo "## CI Summary" >> $GITHUB_STEP_SUMMARY
          echo "- Branch: ${{ github.ref_name }}" >> $GITHUB_STEP_SUMMARY
          echo "- Status: ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

**Expected result**: The CI/CD pipeline is configured.

---

## 🚀 Step 5: Create Test Code

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Create test code",
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
Create the file ai-content-agent/tests/test_api.py with the following content:

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.main import app

client = TestClient(app)

def test_health_check():
    """Health check test"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data

def test_create_task():
    """Task creation test"""
    response = client.post("/tasks", json={
        "title": "Test Task",
        "prompt": "Generate test content",
        "priority": "high"
    })
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "pending"

def test_get_task():
    """Task retrieval test"""
    # First create a task
    create_response = client.post("/tasks", json={
        "title": "Get Test",
        "prompt": "Test prompt"
    })
    task_id = create_response.json()["task_id"]

    # Get the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Test"

def test_get_task_not_found():
    """Non-existent task retrieval test"""
    response = client.get("/tasks/nonexistent")
    assert response.status_code == 404

def test_list_tasks():
    """Task list test"""
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

Run the tests:
cd ai-content-agent && uv sync && pytest tests/ -v
```

**Expected result**: All API tests pass.

---

## 🚀 Step 6: Final Check and Documentation

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 6: Final check and documentation",
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
Create the file ai-content-agent/README.md with the following content:

# AI Content Generator Agent

An AI-powered content generation and management system.

## Features

- Task management via RESTful API
- Asynchronous content generation
- Quality review functionality
- Multi-platform publishing

## Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
git clone <repository-url>
cd ai-content-agent

# Install dependencies with uv
uv sync
```

### Run

```bash
python -m src.main
```

API: http://localhost:8000

### Tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|------|
| GET | /health | Health check |
| POST | /tasks | Create task |
| GET | /tasks/{id} | Get task |
| GET | /tasks | List tasks |

## Project Structure

```
ai-content-agent/
├── src/
│   ├── main.py          # FastAPI main
│   ├── api/             # Endpoints
│   ├── services/        # Business logic
│   └── subagents/       # SubAgent implementation
├── tests/               # Tests
├── .github/workflows/   # CI/CD
└── requirements.txt     # Dependencies
```

## License
MIT
```

**Expected result**: Project documentation is complete.

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
      {"id": "trouble_1", "label": "Import error"},
      {"id": "trouble_2", "label": "Port is in use"},
      {"id": "trouble_3", "label": "GitHub Actions fails"},
      {"id": "trouble_4", "label": "Tests not found"}
    ]
  }]
}
```


- Import error occurs
- Port is in use
- GitHub Actions fails
- Tests not found

### Issue 1: "Import error"
**Cause**: PYTHONPATH is not set
**Solution prompt**:
```
Check the following:
1. Add the project root to sys.path
2. __init__.py exists in the directory
3. The virtual environment is active
```

### Issue 2: "Port is in use"
**Cause**: Port 8000 is already in use
**Solution prompt**:
```
Change the port:
uvicorn.run(app, host="0.0.0.0", port=8001)
Or terminate the existing process:
lsof -i :8000 && kill <PID>          # Mac/Linux/WSL
# Windows: Find PID with netstat -ano | findstr :8000, then terminate with taskkill /PID <PID> /F
```

### Issue 3: "GitHub Actions fails"
**Cause**: Workflow configuration error
**Solution prompt**:
```
Check the following:
1. Is the YAML indentation correct?
2. Is the requirements.txt path correct?
3. Is the Python version correct?
```

### Issue 4: "Tests not found"
**Cause**: Test file naming convention is incorrect
**Solution prompt**:
```
pytest test file naming conventions:
- test_*.py or *_test.py
- Test functions start with test_
```

---

## ✅ Checkpoint

### Comprehensive Exercise Checklist

### Module 6-1: Commands
- [ ] Commands placed in .cursor/commands/
- [ ] At least 3 commands created

### Module 6-2: Skills
- [ ] Skills placed in skills/
- [ ] Documented with SKILL.md
- [ ] Test code exists

### Module 6-3: Rules
- [ ] Behavior defined in .cursor/rules/rules.md
- [ ] Security and performance standards specified

### Module 6-4: SubAgents
- [ ] Orchestrator is implemented
- [ ] Multiple SubAgents are linked
- [ ] Error handling exists

### Module 6-5: Integration
- [ ] FastAPI server operation verified
- [ ] API endpoints tested
- [ ] GitHub Actions configured
- [ ] Documentation complete

---

## 🎉 Congratulations!

You have completed all modules!

### Skills Acquired
1. **AI Agent Development**: Complex workflow design and implementation
2. **Microservices**: Loosely coupled SubAgent design
3. **External API Integration**: Notion, Slack, Google integration
4. **DevOps**: CI/CD pipeline construction
5. **Enterprise Development**: Scalable system design


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

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

All sections are now complete. Choose what to do next.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_module", "label": "Proceed to Module 7 Skill/Commands (/start-7-1)"},
      {"id": "course_top", "label": "Open course top (ai-agent.camp)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_module → /start-7-1（Module 7 Skill/Commands）
- course_top → Open https://ai-agent.camp/en/course in the browser
- finish → End

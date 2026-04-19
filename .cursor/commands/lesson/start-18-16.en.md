---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-15", "output/pm/test-cases.md"]
level: "intermediate"
tags: ["pm", "test", "unit-test", "pytest"]
---

# 🎓 Lesson 18-16: Unit Testing

| Item | Details |
|------|------|
| Goal | Run unit tests on TaskFlow backend logic with pytest and collect evidence |
| Duration | ~25 min |
| Skills Used | test-planner skill |
| Prerequisites | Lesson 18-15 completed、output/pm/test-cases.md exists |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

## 📍 Step 1: Identifying Functions to Test

### TaskFlow Backend Main Modules

The TaskFlow backend consists of the following functional modules:

1. **Authentication/Authorization module** (`auth.py`)
   - User authentication, token generation, permission checking

2. **Task CRUD module** (`tasks.py`)
   - Task creation, reading, updating, and deletion

3. **Validation module** (`validators.py`)
   - Input validation, business logic verification

4. **Notification module** (`notifications.py`)
   - Email sending, Slack notifications

5. **DB access module** (`database.py`)
   - Database operations, transaction management

### Which module do you want to test?

```json
{
  "type": "AskQuestion",
  "question": "Select the functional module(s) to test. Multiple selections are possible.",
  "options": [
    {
      "id": "auth_logic",
      "label": "Authentication logic (auth.py)",
      "value": "auth_logic",
      "description": "Test user authentication, token generation, and permission checking"
    },
    {
      "id": "task_crud",
      "label": "Task CRUD (tasks.py)",
      "value": "task_crud",
      "description": "Test task creation, update, deletion, and search"
    },
    {
      "id": "validation",
      "label": "Validation (validators.py)",
      "value": "validation",
      "description": "Test input validation and business logic verification"
    },
    {
      "id": "notifications",
      "label": "Notification module (notifications.py)",
      "value": "notifications",
      "description": "Test email and Slack notification features (using mocks)"
    },
    {
      "id": "all_modules",
      "label": "All modules",
      "value": "all_modules",
      "description": "Comprehensive testing of all modules above"
    }
  ],
  "required": true,
  "helpText": "Starting with 'Task CRUD' or 'Validation' is recommended for easier testing."
}
```

### Extracting Target Functions

Based on the selected module, the following information is analyzed:

- Each function's signature (input/output)
- Dependencies (on other functions or libraries)
- Side effects (DB operations, external API calls, etc.)
- Existing test code (if any)
- Lines not yet covered

Example extracted functions:

```python
# auth.py
def authenticate_user(email: str, password: str) -> Dict[str, Any]
def verify_token(token: str) -> Dict[str, Any]
def check_permission(user_id: int, resource_id: int) -> bool

# tasks.py
def create_task(user_id: int, title: str, description: str) -> Task
def update_task(task_id: int, updates: Dict) -> Task
def delete_task(task_id: int) -> bool
def get_tasks_by_user(user_id: int, filters: Dict) -> List[Task]

# validators.py
def validate_email(email: str) -> bool
def validate_password(password: str) -> bool
def validate_task_input(title: str, description: str) -> bool
```

---

## 🚀 Step 2: Generating pytest Test Code

### pytest Test Styles

In pytest, there are multiple test code writing styles:

1. **Function-style tests** - Simple and readable (for beginners)
   ```python
   def test_authenticate_user_success():
       result = authenticate_user("user@example.com", "Pass1234!")
       assert result["success"] is True
   ```

2. **Class-style tests** - Organize related tests (for medium projects)
   ```python
   class TestAuthentication:
       def test_authenticate_user_success(self):
           ...
   ```

3. **Fixture usage** - Pre/post processing and mock management (for large projects)
   ```python
   @pytest.fixture
   def test_user():
       return create_test_user()

   def test_authenticate_user(test_user):
       result = authenticate_user(test_user.email, "Pass1234!")
       assert result["success"] is True
   ```

4. **AI-recommended style** - Optimal style based on project scale and complexity

### Which test style do you want to use?

```json
{
  "type": "AskQuestion",
  "question": "Select a pytest test code writing style. Choose based on project scale and complexity.",
  "options": [
    {
      "id": "function_style",
      "label": "Function-style tests",
      "value": "function_style",
      "description": "Simple and readable. Ideal for beginners and small-scale tests"
    },
    {
      "id": "class_style",
      "label": "Class-style tests",
      "value": "class_style",
      "description": "Group related tests. For medium-scale projects"
    },
    {
      "id": "fixture_style",
      "label": "Fixture usage",
      "value": "fixture_style",
      "description": "Streamline pre/post test setup. For large-scale projects"
    },
    {
      "id": "ai_recommended",
      "label": "AI-recommended style",
      "value": "ai_recommended",
      "description": "AI selects the optimal style based on project scale and complexity"
    }
  ],
  "required": true,
  "helpText": "Starting with 'Function-style tests' is recommended for simplicity. Select 'Fixture usage' for complex setups."
}
```

### Test Code Generation Process

Based on the selected style, the following is executed:

1. **Load test cases generated in Lesson 18-15**
   - Extract test cases from output/pm/test-cases.md

2. **Generate test function templates**
   ```python
   # test_tasks.py
   import pytest
   from app.tasks import create_task, update_task, delete_task
   from app.models import Task

   # Happy path test
   def test_create_task_success():
       """TC-004: Happy path - Task creation success"""
       task = create_task(
           user_id=1,
           title="New Task",
           description="Task description"
       )
       assert task.title == "New Task"
       assert task.user_id == 1

   # Error path test
   def test_create_task_empty_title():
       """TC-005: Error path - Empty title string"""
       with pytest.raises(ValueError, match="Title cannot be empty"):
           create_task(user_id=1, title="", description="desc")

   # Boundary value test
   def test_create_task_max_title_length():
       """TC-006: Boundary value - Maximum title length"""
       long_title = "x" * 255
       task = create_task(user_id=1, title=long_title, description="desc")
       assert len(task.title) == 255
   ```

3. **Create mocks and fixtures**
   ```python
   @pytest.fixture
   def test_user():
       return User(id=1, email="test@example.com")

   @pytest.fixture
   def test_db(monkeypatch):
       # Set up test DB
       monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
   ```

4. **Generate test code files**
   - output/pm/unit-test-code/test_auth.py
   - output/pm/unit-test-code/test_tasks.py
   - output/pm/unit-test-code/test_validators.py
   - output/pm/unit-test-code/conftest.py (shared Fixtures)

---

## ⚠️ Step 3: Test Execution and Evidence Capture

### Selecting pytest Execution Method

There are several patterns for test execution:

1. **Run all tests** - Execute all tests at once
2. **Run by category** - Execute by module (auth tests, tasks tests, etc.)
3. **Run one by one** - Execute individual tests for debugging

### Select test execution method

```json
{
  "type": "AskQuestion",
  "question": "Select the pytest test execution method. Detailed evidence capture is required.",
  "options": [
    {
      "id": "run_all",
      "label": "Run all tests",
      "value": "run_all",
      "description": "Execute all tests at once. Short execution time (recommended)"
    },
    {
      "id": "run_by_category",
      "label": "Run by category",
      "value": "run_by_category",
      "description": "Execute by module (auth, tasks, validators). Provides detailed results"
    },
    {
      "id": "run_individually",
      "label": "Run one by one",
      "value": "run_individually",
      "description": "Execute individual tests for verification. Convenient for debugging (takes more time)"
    }
  ],
  "required": true,
  "helpText": "Start with 'Run all tests' to get the big picture, then use 'Run by category' for detailed review of failed tests."
}
```

### Test Execution and Evidence Capture

Based on the selected method, the following is executed:

1. **Prepare test execution environment**
   ```bash
   # Install dependencies with uv
   uv add pytest pytest-cov pytest-html pydantic
   ```

2. **Execute tests and capture results**
   ```bash
   # Run all tests (with HTML report and coverage report)
   pytest output/pm/unit-test-code/ \
     --html=output/pm/unit-test-evidence/report.html \
     --self-contained-html \
     --cov=app \
     --cov-report=html:output/pm/unit-test-evidence/coverage \
     --cov-report=term \
     -v --tb=short > output/pm/unit-test-evidence/test-output.log 2>&1
   ```

3. **Generate evidence files**
   ```
   output/pm/unit-test-evidence/
   ├── report.html              # pytest HTML report
   ├── coverage/                # Coverage report (HTML)
   │   └── index.html
   ├── test-output.log          # Test execution log
   ├── summary.md               # Test result summary
   └── failed-tests.txt         # Failed test details
   ```

4. **Auto-generate test result summary**
   ```
   # Summary example
   Test Execution Result Summary
   =======================

   Tests executed: 42
   Passed: 40
   Failed: 2
   Skipped: 0
   Execution time: 12.34 sec

   Coverage: 87.5%

   Failed tests:
   - test_create_task_with_null_user() - ValueError
   - test_update_nonexistent_task() - KeyError
   ```

---

## ✅ Step 4: Generating Test Result Reports

### Generated Reports

**output/pm/unit-test-evidence/report.html**
- Execution results of all test cases (pass/fail)
- Execution time for each test
- Stack trace (on failure)
- Coverage map

**output/pm/unit-test-evidence/summary.md**
```markdown
# Unit Test Execution Report

## Overview
- Execution date/time: 2026-02-10 15:30:45
- Target modules: auth.py, tasks.py, validators.py
- Test style: Function-style tests
- Test execution method: Run all tests

## Test Results
| Item | Result |
|------|------|
| Tests executed | 42 |
| Passed | 40 (95.2%) |
| Failed | 2 (4.8%) |
| Skipped | 0 |
| Execution time | 12.34 sec |

## Coverage
| Module | Coverage |
|-----------|-----------|
| auth.py | 92% |
| tasks.py | 85% |
| validators.py | 88% |
| **Overall** | **87.5%** |

## Failed Test Details
### test_create_task_with_null_user()
- **Error**: ValueError: user_id cannot be null
- **Expected**: Error should occur when user ID is null during task creation
- **Actual**: Error message does not match

### test_update_nonexistent_task()
- **Error**: KeyError: task not found
- **Expected**: Appropriate error message returned when updating a non-existent task
- **Actual**: KeyError is raised (error handling not implemented)

## Improvement Proposals
1. Standardize error messages
2. Strengthen null checks
3. Unify exception handling
```

### Report Execution Commands

```bash
# Run the test-planner skill (answer Step 1-3 choices interactively)
/test-planner --mode execute
```

Or execute manually:

```bash
# Run tests and capture results
pytest output/pm/unit-test-code/ \
  --html=output/pm/unit-test-evidence/report.html \
  --self-contained-html \
  --cov=app \
  --cov-report=term \
  -v

# Generate summary
uv run python tools/test_report_generator.py \
  --input output/pm/unit-test-evidence/report.html \
  --output output/pm/unit-test-evidence/summary.md
```

### File Verification

```bash
# Verify generated files
ls -la output/pm/unit-test-evidence/
cat output/pm/unit-test-evidence/summary.md
```


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/unit-test-code/
└──   (unit test code)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/unit-test-code/

# Check the beginning (first 30 lines)
head -30 output/pm/unit-test-code/
```

> 💡 Full text: Run `cat output/pm/unit-test-code/` to display the full text

---

## ➡️ Next Step

Unit testing is complete. You are ready to proceed to the next step:

**[Lesson 18-17: Integration Testing & E2E Testing](./start-18-17.md)**

In the next lesson, you will perform integration tests across multiple modules and end-to-end testing.

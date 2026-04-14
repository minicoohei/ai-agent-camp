---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-16", "output/pm/unit-test-code/"]
level: "intermediate"
tags: ["pm", "test", "integration", "api-test"]
---

# 🎓 Lesson 18-17: Integration Testing

| Item | Details |
|------|------|
| Goal | Run integration tests on TaskFlow's API interactions and collect evidence |
| Duration | ~25 min |
| Skills Used | test-planner skill |
| Prerequisites | Lesson 18-16 completed |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

## 📍 Step 1: Designing Integration Test Scenarios

Integration testing is a critical process for verifying coordination between multiple APIs. In the TaskFlow system, the following coordination patterns are tested.

- **API to DB coordination**: The complete flow from API task creation to database storage to search
- **Auth to task operations**: Permission verification for task creation, editing, and deletion after user authentication
- **Notification pipeline**: Completeness verification of internal notifications to Webhook delivery on task updates
- **Full integration**: Complete operation verification across multiple systems

```json
{
  "type": "AskQuestion",
  "question": "Which test scope do you want to prioritize?",
  "options": [
    {
      "id": "api_db",
      "label": "API to DB coordination (from task creation to search)",
      "nextStep": "start-test-api-db"
    },
    {
      "id": "auth_task",
      "label": "Auth to task operations (including permission verification)",
      "nextStep": "start-test-auth-task"
    },
    {
      "id": "notification",
      "label": "Notification pipeline (internal notifications to Webhook)",
      "nextStep": "start-test-notification"
    },
    {
      "id": "all",
      "label": "Run all tests",
      "nextStep": "start-test-all"
    }
  ],
  "context": "The integration test scope selection is based on project risk assessment and time constraints. Refer to stakeholder feedback."
}
```

## 🚀 Step 2: Test Code Generation (pytest + requests)

Generate API integration test code using the pytest framework and requests library. The test code should follow this structure.

- Import section: Import pytest, requests, and unittest.mock
- Fixture setup: Initialize test base URL, auth tokens, and test data
- Test cases: Functions corresponding to each API coordination scenario
- Assertions: Verify HTTP status codes, response bodies, and database state
- Cleanup: Post-test environment restoration

```json
{
  "type": "AskQuestion",
  "question": "How do you want to configure your mock strategy?",
  "options": [
    {
      "id": "real_db",
      "label": "Use test DB (verification close to production)",
      "config": {
        "strategy": "integration_testing",
        "database": "test_database",
        "external_apis": "mocked"
      }
    },
    {
      "id": "mock_db",
      "label": "Use mock DB (fast, isolated testing) (recommended)",
      "config": {
        "strategy": "unit_testing",
        "database": "in_memory_mock",
        "external_apis": "mocked"
      }
    },
    {
      "id": "hybrid",
      "label": "Hybrid strategy (test DB for core features, mock for external APIs)",
      "config": {
        "strategy": "hybrid_testing",
        "database": "test_database",
        "external_apis": "mocked"
      }
    }
  ],
  "context": "The mock strategy is chosen by balancing test reliability and execution speed. Real DB testing offers higher verification accuracy but adds complexity to test environment setup and management."
}
```

Test code example:

```python
import pytest
import requests
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

class TestTaskFlowIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = "http://localhost:8000/api"
        self.auth_token = "test-token-xyz123"
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        yield
        # Cleanup processing
        self._cleanup_test_data()

    def test_create_task_and_retrieve(self):
        """Integration test: Task creation -> Search"""
        payload = {
            "title": "Integration Test Task",
            "description": "Testing API→DB coordination",
            "priority": "high"
        }
        response = requests.post(
            f"{self.base_url}/tasks",
            json=payload,
            headers=self.headers
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # Verify DB search
        get_response = requests.get(
            f"{self.base_url}/tasks/{task_id}",
            headers=self.headers
        )
        assert get_response.status_code == 200
        assert get_response.json()["title"] == payload["title"]

    def test_auth_required_for_task_operations(self):
        """Reject task operations without authentication"""
        response = requests.get(f"{self.base_url}/tasks")
        assert response.status_code == 401

    def _cleanup_test_data(self):
        """Clean up test data"""
        pass
```

## ⚠️ Step 3: Test Execution and Evidence Capture

Test execution and result recording serve as the basis for project quality assurance.

Execute tests using the following procedure.

1. Verify the test environment
   - Is the test DB running independently?
   - Are the test API endpoints running correctly?
   - Are external dependencies properly mocked?

2. Test execution command
   ```bash
   pytest tests/integration/ -v --tb=short --html=report.html --cov=src
   ```

3. Evidence collection
   - Test execution log (JSON format)
   - Screenshots (screen state on failure)
   - Performance metrics (response time, memory usage)
   - Database verification log (INSERT/UPDATE/DELETE records)

Evidence file structure:

```text
output/pm/integration-test-evidence/
├── test-execution-log.json
├── test-results.html
├── failed-cases/              # Generated only on test failure
│   └── case-XXX-description.md
├── performance-metrics.csv
└── summary.md
```

## ✅ Step 4: Creating Bug Reports

Defects found during test execution must be documented in an appropriate format.

```json
{
  "type": "AskQuestion",
  "question": "Which bug report format do you want to use?",
  "options": [
    {
      "id": "simple",
      "label": "Simple format (title, cause, and solution only)",
      "template": "simple-defect-report.md"
    },
    {
      "id": "detailed",
      "label": "Detailed format (includes reproduction steps, expected values, actual values, and screenshots)",
      "template": "detailed-defect-report.md"
    },
    {
      "id": "jira",
      "label": "Jira format (fields: priority, assignee, sprint)",
      "template": "jira-defect-format.json"
    }
  ],
  "context": "The bug report format is chosen based on your organization's processes and tracking system. The detailed format improves the development team's fix efficiency."
}
```

Bug report template (detailed format):

```markdown
# Bug Report #001

## Overview
- **Title**: DB write error on task creation after user authentication
- **Severity**: High
- **Discovery Date**: 2024-02-10
- **Assignee**: Dev Team A

## Reproduction Steps
1. Log in with test user
2. Call task creation API (POST /api/tasks)
3. 500 error is returned

## Expected Values
- Status code: 201 Created
- Response: JSON of the created task

## Actual Values
- Status code: 500 Internal Server Error
- Error message: "Database constraint violation on tasks.user_id"

## Root Cause
User ID validation logic during task creation is inconsistent with DB constraints

## Proposed Solutions
- Fix user ID validation logic
- Execute DB migration
- Add regression tests

## Evidence
- Screenshot: error-500-screenshot.png
- Log extract: output/pm/logs/api-error.log
- API response: response-dump.json
```


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── operation-manual.md  (operation manual)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/operation-manual.md

# Check the beginning (first 30 lines)
head -30 output/pm/operation-manual.md
```

> 💡 Full text: Run `cat output/pm/operation-manual.md` to display the full text

## ➡️ Completion and Next Steps

Verify that the following deliverables are ready in output/pm/integration-test-evidence/.

- test-execution-log.json: Complete test execution records
- test-results.html: Browser-viewable test results report
- failed-cases/*.md: Detailed reports of discovered defects
- performance-metrics.csv: Performance data such as API response times

**Next Lesson**: → Lesson 18-18 Meeting Design & Minutes Analysis

The integration testing skills acquired in this lesson are a critical part of the quality assurance process in system development. The collected evidence is used for reliability reporting to stakeholders and final verification before production.

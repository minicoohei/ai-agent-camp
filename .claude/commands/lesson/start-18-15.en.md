---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-14", "output/pm/usecases.md"]
level: "intermediate"
tags: ["pm", "test", "test-plan", "test-cases"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-15: Test Plan & Test Case Generation

| Item | Details |
|------|------|
| Goal | Auto-generate test plans and test cases from TaskFlow use cases |
| Duration | ~25 min |
| Skills Used | test-planner skill |
| Prerequisites | output/pm/usecases.md exists |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

## 📍 Step 1: Test Plan Structure Explanation

### Basic Elements of a Test Plan

A test plan consists of the following elements:

- **Test scope**: Which parts of the system to test
- **Test strategy**: What and how to verify
- **Test environment**: Environment configuration for testing
- **Schedule**: Test execution period and timing of each phase
- **Resources**: Tools and personnel required for test execution
- **Success criteria**: Test pass criteria

Test cases are specific procedures and expected values for testing individual features and scenarios.

### What is your testing experience level?

```json
{
  "type": "AskQuestion",
  "question": "Select your testing experience level. This will adjust the detail and complexity of the test plan.",
  "options": [
    {
      "id": "beginner",
      "label": "Beginner - Limited testing experience or unclear test perspectives",
      "value": "beginner",
      "description": "AI will suggest more test perspectives and include detailed explanations"
    },
    {
      "id": "intermediate",
      "label": "Intermediate - Understands basic test perspectives",
      "value": "intermediate",
      "description": "Generates standard test plans and test cases"
    },
    {
      "id": "advanced",
      "label": "Advanced - Considers test strategy and optimization",
      "value": "advanced",
      "description": "Proposes plans including risk analysis, coverage optimization, and efficiency improvements"
    }
  ],
  "required": true,
  "helpText": "Generates test plans and test cases at the appropriate detail level based on your selection."
}
```

---

## 🚀 Step 2: Generating Test Cases from Use Cases

### Test Perspective Classification

To generate test cases effectively, testing from multiple perspectives is required:

1. **Happy path tests**: Test the normal flow of use cases
2. **Error path tests**: Test errors and unexpected inputs
3. **Boundary value tests**: Test minimum, maximum, and surrounding input values
4. **Security tests**: Test authorization, authentication, and input validation

### To what extent do you want to generate test cases?

```json
{
  "type": "AskQuestion",
  "question": "How much coverage do you want for test case generation? Detail increases progressively.",
  "options": [
    {
      "id": "normal_only",
      "label": "Happy path only",
      "value": "normal_only",
      "description": "Generate test cases for normal use case flows only (minimal)"
    },
    {
      "id": "normal_abnormal",
      "label": "Happy path + Error path",
      "value": "normal_abnormal",
      "description": "Covers normal flows and common error patterns (standard)"
    },
    {
      "id": "normal_abnormal_boundary",
      "label": "Happy path + Error path + Boundary values",
      "value": "normal_abnormal_boundary",
      "description": "Includes boundary value tests in addition to the above (more detailed)"
    },
    {
      "id": "comprehensive",
      "label": "Happy path + Error path + Boundary values + Security",
      "value": "comprehensive",
      "description": "Complete test coverage including security tests (most detailed)"
    }
  ],
  "required": true,
  "helpText": "The number of test cases and detail level are determined based on the selected perspectives. Start with 'Happy path + Error path' for a balanced approach."
}
```

### Test Case Generation Process

Based on your selection, the following processes are executed:

1. Load output/pm/usecases.md
2. Auto-generate test cases from each use case based on selected perspectives
3. Assign ID, description, preconditions, steps, and expected values to each test case
4. Group test cases (by use case, by feature, etc.)
5. Save to output/pm/test-cases.md

Test cases are generated in the following format:

```text
### Test Case ID: TC-001
**Use Case**: UC-001 - User Registration
**Perspective**: Happy path
**Description**: User registration succeeds with email and password

**Preconditions**:
- System is accessible
- User is not yet registered

**Test Steps**:
1. Open the registration screen
2. Enter email address (e.g.: user@example.com)
3. Enter password (e.g.: Pass1234!)
4. Click the register button

**Expected Values**:
- Registration succeeds
- Confirmation email is sent
- User becomes able to log in
```

---

## ⚠️ Step 3: Prioritizing Test Cases

### Prioritization Approach

When there are many test cases, it may be difficult to execute all of them.
When resources are limited, prioritize and execute important tests first.

Main prioritization methods:

1. **Risk-based**: Prioritize tests for features with high business risk
2. **Coverage-based**: Prioritize tests that cover more features and branches
3. **AI-suggested**: AI proposes priorities based on past data and best practices

### Select a test case prioritization method

```json
{
  "type": "AskQuestion",
  "question": "Select a prioritization method for the generated test cases. This is effective when the testing period is limited.",
  "options": [
    {
      "id": "risk_based",
      "label": "Risk-based prioritization",
      "value": "risk_based",
      "description": "Place test cases for high business risk features (authentication, payments, etc.) at the top"
    },
    {
      "id": "coverage_based",
      "label": "Coverage-based prioritization",
      "value": "coverage_based",
      "description": "Place test cases with high feature/branch coverage at the top (achieve maximum coverage with limited budget)"
    },
    {
      "id": "ai_suggested",
      "label": "AI-recommended prioritization",
      "value": "ai_suggested",
      "description": "AI proposes priorities combining best practices and feature complexity"
    },
    {
      "id": "priority_all",
      "label": "Prioritize all (recommended)",
      "value": "priority_all",
      "description": "Adopt all 3 perspectives above and display multiple priority ranks (most flexible)"
    }
  ],
  "required": true,
  "helpText": "Risk-based is the most common. If multiple perspectives are needed, select 'AI-recommended' or 'Prioritize all'."
}
```

### Executing Prioritization

Based on the selected method:

1. Calculate a priority score for each test case
2. Generate risk matrices, coverage maps, etc.
3. Determine execution order by priority
4. Append priority information to output/pm/test-cases.md

---

## ✅ Step 4: Executing Test Plan and Test Case Generation

### Generated Files

**output/pm/test-plan.md**
```text
# Test Plan

## 1. Test Scope
- TaskFlow Backend API
- Frontend UI
- Authentication/Authorization features
- Task management features
- Notification features

## 2. Test Strategy
- Unit Test
- Integration Test
- E2E Test (End-to-End Test)

## 3. Test Environment
- Development environment: localhost:3000
- Test DB: SQLite (test-only)

## 4. Schedule
- Phase 1: Unit tests (5 business days)
- Phase 2: Integration tests (3 business days)
- Phase 3: E2E tests (2 business days)

## 5. Success Criteria
- Test case execution rate: 100%
- Test case success rate: 95% or higher
- Critical bugs: 0
```

**output/pm/test-cases.md**
```text
# Test Case List

## Use Case UC-001: User Registration

### TC-001 Happy Path - Normal user registration
**Priority**: High (Risk-based)
**Priority**: High (Coverage-based)
**Expected Value**: Registration success

### TC-002 Error Path - Duplicate email address
**Priority**: High
**Expected Value**: Error message displayed

### TC-003 Error Path - Insufficient password
**Priority**: Medium
**Expected Value**: Validation error displayed

## Use Case UC-002: Task Creation
...
```

### Execution commands

```bash
# Run the test-planner skill (answer Step 1-3 choices interactively)
/test-planner
```

Alternatively, the skill automatically executes the following:

1. **Test plan generation**
   ```bash
   uv run python tools/test_planner.py \
     --input output/pm/usecases.md \
     --output output/pm/test-plan.md \
     --experience-level <selected_value> \
     --test-scope <selected_value>
   # On Windows, replace python3 with python
   ```

2. **Test case generation**
   ```bash
   uv run python tools/test_case_generator.py \
     --input output/pm/usecases.md \
     --output output/pm/test-cases.md \
     --coverage <selected_value> \
     --prioritize <selected_value>
   # On Windows, replace python3 with python
   ```

3. **File generation verification**
   ```bash
   ls -la output/pm/test-plan.md output/pm/test-cases.md
   ```


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── test-cases.md  (test cases)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/test-cases.md

# Check the beginning (first 30 lines)
head -30 output/pm/test-cases.md
```

> 💡 Full text: Run `cat output/pm/test-cases.md` to display the full text

---

## ➡️ Next Step

You are ready to proceed to the next lesson:

**[start-18-16: Unit Testing (pytest)](./start-18-16.md)**

In Lesson 18-16, you will execute unit tests on backend logic using pytest based on the generated test cases.

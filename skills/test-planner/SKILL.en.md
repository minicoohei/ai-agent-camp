---
name: test-planner
description: "Used for generating test plans, test cases, and test reports. Triggered by requests like 'Create a test plan', 'Generate test cases', 'Write E2E tests', etc."
triggers:
  - Create a test plan
  - Generate test cases
  - Write E2E tests
  - Test results summary
  - Analyze test perspectives
  - test-planner
  - Playwright test
---

# Test Planner - Test Planning & Execution Support Tool

Automatically generates test plans, test cases, and test code from use case descriptions.

## Workflow

1. Receive use case description (usecases.md) as input
2. Analyze test perspectives (normal/abnormal/boundary/security)
3. Output structured test plan and test cases
4. Generate Playwright E2E test code as needed

## Templates

### Test Plan Template

```markdown
# Test Plan: {System Name}

## 1. Test Overview
### 1.1 Test Objective
### 1.2 Test Scope
### 1.3 Test Environment

## 2. Test Strategy
### 2.1 Test Levels
| Level | Target | Method | Tool |
|-------|--------|--------|------|
| Unit Test | Individual functions/methods | White-box | pytest |
| Integration Test | Inter-API coordination | Gray-box | pytest + requests |
| E2E Test | Screen operation flows | Black-box | Playwright |

### 2.2 Test Perspectives
- Functional testing (normal/abnormal cases)
- Boundary value testing
- Security testing (authentication/authorization)
- Performance testing (response time)
- Usability testing

## 3. Test Schedule
| Phase | Duration | Owner | Deliverables |
|-------|----------|-------|-------------|

## 4. Pass/Fail Criteria
- Test case execution rate: 100%
- Critical bugs (Severity: Critical/High): 0
- Test coverage: 80% or above
```

### Test Case Template

```markdown
# Test Case List

## TC-{Number}: {Test Name}
- **Test Level:** Unit / Integration / E2E
- **Related Use Case:** UC-{Number}
- **Preconditions:**
- **Test Steps:**
  1. {Step 1}
  2. {Step 2}
  3. {Step 3}
- **Expected Result:**
- **Test Data:**
- **Priority:** High / Medium / Low
- **Result:** Not executed / Pass / Fail
```

### Playwright E2E Test Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('{Feature Name}', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('{Test Name}', async ({ page }) => {
    // Arrange
    // Act
    // Assert
    await expect(page.locator('{selector}')).toBeVisible();
  });
});
```

### Test Evidence Template

```markdown
# Test Evidence: {Test Case ID}

## Execution Information
- Execution Date: {datetime}
- Executor: {name}
- Environment: {environment}

## Result
- Status: Pass / Fail
- Screenshot: {path}
- Log: {path}

## Notes
```

### Test Results Summary Template

```markdown
# Test Results Summary

## Overview
| Item | Value |
|------|-------|
| Total Test Cases | {total} |
| Executed | {executed} |
| Passed | {passed} |
| Failed | {failed} |
| Skipped | {skipped} |
| Pass Rate | {rate}% |

## Failed Tests List
| TC-ID | Test Name | Failure Reason | Severity | Status |
|-------|-----------|---------------|----------|--------|

## Quality Assessment
- [ ] Pass/fail criteria are met
- [ ] Critical bugs are at 0
- [ ] Test coverage is 80% or above
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| input | Yes | - | Path to use case description file |
| type | No | all | Test type (unit/integration/e2e/all) |
| output_dir | No | output/pm/ | Output directory |
| format | No | markdown | Output format (markdown/playwright) |

## Output Format

- Test plan -> `output/pm/test-plan.md`
- Test cases -> `output/pm/test-cases.md`
- E2E test code -> `output/pm/e2e-tests/*.spec.ts`
- Test evidence -> `output/pm/unit-test-evidence/`, `output/pm/integration-test-evidence/`
- Test results summary -> `output/pm/test-summary.md`

## Example

```
Use the test-planner skill to generate a test plan and test cases from usecases.md.
-> output/pm/test-plan.md and output/pm/test-cases.md are generated
```

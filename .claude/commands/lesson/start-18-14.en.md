---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-13", "output/pm/prototype/"]
level: "intermediate"
tags: ["pm", "test", "e2e", "playwright"]
---

# 🎓 Lesson 18-14: Playwright E2E Testing

| Item | Details |
|------|------|
| Goal | Generate and run Playwright E2E test code for the TaskFlow prototype |
| Duration | ~25 min |
| Skills Used | test-planner skill |
| Prerequisites | Lesson 18-13 completed, HTML prototype exists in output/pm/prototype/ |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

---

## 📍 Step 1: Playwright Environment Setup

Playwright is a tool for running automated browser tests. In this step, prepare the environment for testing the TaskFlow prototype.

### Environment Setup Flow

1. Initialize a new project with npm init playwright@latest
2. Configure basic settings in playwright.config.ts
3. Install browser drivers
4. Verify the test execution environment

```json
{
  "type": "AskQuestion",
  "question": "Do you have experience with Playwright?",
  "options": [
    {
      "id": "beginner",
      "label": "First time using it",
      "value": "beginner",
      "description": "Provides detailed setup guidance"
    },
    {
      "id": "intermediate",
      "label": "I know the basics",
      "value": "intermediate",
      "description": "Provides standard setup steps"
    },
    {
      "id": "advanced",
      "label": "Practical experience",
      "value": "advanced",
      "description": "Proceed with minimal guidance"
    },
    {
      "id": "setup_only",
      "label": "Just help me with setup",
      "value": "setup_only",
      "description": "Run setup script"
    }
  ],
  "required": true,
  "helpText": "The level of setup guidance detail changes according to experience level"
}
```

### Setup Commands

**Options: First time using / Already know the basics**

```bash
# Move to project directory (directory with prototype)
cd output/pm

# Initialize Playwright (interactive)
npm init playwright@latest

# Or explicit setup
npm install -D @playwright/test
npx playwright install
```

**Basic settings for playwright.config.ts**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e-tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npx serve . -l 8080',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
  },
});
```

✅ **Checkpoint: Playwright environment setup complete**

```bash
npx playwright --version  # Verify v1.40.0 or higher
ls -la playwright.config.ts  # Verify config file
```

---

## 📍 Step 2: Designing E2E Test Scenarios

Design test scenarios for the TaskFlow prototype. Select scenarios that cover key user flows based on the use cases defined in Lesson 18-6.

### Test Scenario Selection

```json
{
  "type": "AskQuestion",
  "question": "Select the scope of test scenarios",
  "options": [
    {
      "id": "minimal",
      "label": "Basic 3 scenarios (minimum)",
      "value": "minimal",
      "description": "Minimum tests covering only main flows"
    },
    {
      "id": "standard",
      "label": "Standard 5 scenarios (recommended)",
      "value": "standard",
      "description": "Covers main flows + edge cases"
    },
    {
      "id": "comprehensive",
      "label": "Comprehensive (8+ scenarios)",
      "value": "comprehensive",
      "description": "Comprehensive testing of all use cases"
    },
    {
      "id": "ai_suggest",
      "label": "Get AI suggestions",
      "value": "ai_suggest",
      "description": "AI analyzes the prototype and suggests optimal scenarios"
    }
  ],
  "required": true,
  "helpText": "Select based on the quality assurance scope of your prototype. Standard 5 scenarios is recommended"
}
```

### Scenario Definition

**Basic 3 Scenarios (Minimum)**

| # | Scenario | Test Target | Verification Item |
|----|----------|----------|--------|
| 1 | Page load verification | Top page display | Title display, header rendering, initial form display |
| 2 | Task creation flow | Main use case | Form input, submit button, completed screen display |
| 3 | Navigation verification | Menu/page transitions | Menu click, page URL change, back button behavior |

**Standard 5 Scenarios (Recommended)**

| # | Scenario | Test Target | Verification Item |
|----|----------|----------|--------|
| 1 | Page load verification | Top page display | Title display, header rendering, initial form display |
| 2 | Task creation flow | Main use case | Form input, submit button, completed screen display |
| 3 | Navigation verification | Menu/page transitions | Menu click, page URL change, back button behavior |
| 4 | Responsive display verification | Mobile/Tablet | Layout on screen size change, touch operations |
| 5 | Error handling verification | Input validation | Error display when required items are blank, error message confirmation |

**Comprehensive (8+ Scenarios)**

In addition to the 5 scenarios above:

| # | Scenario | Test Target | Verification Item |
|----|----------|----------|--------|
| 6 | Local storage verification | Data persistence | Input data saving, restoration after page reload |
| 7 | Multiple task management | List functionality | Task addition/deletion/editing, task list display |
| 8 | API integration verification | Backend communication | API calls, response processing, network error handling |
| 9 | Performance verification | Loading speed | LCP (Largest Contentful Paint) measurement, scroll performance |

### Scenario Mapping

Each scenario maps to use cases defined in Lesson 18-6:

```text
UC-1: Task Creation → Scenario #2 (Standard)
UC-2: Task List Display → Scenario #7 (Comprehensive)
UC-3: Task Update → Scenario #7 (Comprehensive)
UC-4: Navigation → Scenario #3 (Basic)
UC-5: Error Handling → Scenario #5 (Standard)
```

✅ **Checkpoint: 3 or more test scenarios designed**

```bash
# Create test scenario document
cat > output/pm/e2e-tests/SCENARIOS.md << 'EOF'
# E2E Test Scenarios

## Selected Scenarios
- [x] Page load verification
- [x] Task creation flow
- [x] Navigation verification
- [x] (Optional) Responsive display verification
- [x] (Optional) Error handling verification
EOF
```

---

## 📍 Step 3: Auto-generating Test Code

Use the test-planner skill to auto-generate test code based on the designed scenarios.

### Select Test Code Generation Method

```json
{
  "type": "AskQuestion",
  "question": "Select how to generate test code",
  "options": [
    {
      "id": "auto_generate",
      "label": "Auto-generate with test-planner skill",
      "value": "auto_generate",
      "description": "AI batch-generates test code based on scenarios"
    },
    {
      "id": "from_template",
      "label": "Modify from template",
      "value": "from_template",
      "description": "Customize based on template"
    },
    {
      "id": "interactive",
      "label": "Create one by one interactively",
      "value": "interactive",
      "description": "Create one test at a time in conversation with AI"
    },
    {
      "id": "import_existing",
      "label": "Import existing test files",
      "value": "import_existing",
      "description": "Load and extend existing test files"
    }
  ],
  "required": true,
  "helpText": "Select auto-generation for efficiency, or interactive creation for customization"
}
```

### Auto-generation (Recommended)

```bash
# Run test-planner skill
# AI generates .spec.ts files based on scenarios
```

### Test File Structure

The generated test files have the following structure:

**01-page-load.spec.ts - Page Load Verification**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Page Load Verification', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Title is displayed correctly', async ({ page }) => {
    const title = page.locator('h1');
    await expect(title).toContainText('TaskFlow');
  });

  test('Header is rendered', async ({ page }) => {
    const header = page.locator('header');
    await expect(header).toBeVisible();
  });

  test('Initial form is displayed', async ({ page }) => {
    const form = page.locator('form');
    await expect(form).toBeVisible();
  });
});
```

**02-task-creation.spec.ts - Task Creation Flow**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Task Creation Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Can create a task', async ({ page }) => {
    // Form input
    await page.locator('input[name="taskName"]').fill('Test Task');
    await page.locator('input[name="dueDate"]').fill('2025-12-31');

    // Submit
    await page.locator('button[type="submit"]').click();

    // Verify completion
    const successMessage = page.locator('.success-message');
    await expect(successMessage).toContainText('Created successfully');
  });

  test('Redirects after form submission', async ({ page }) => {
    await page.locator('input[name="taskName"]').fill('Test Task');
    await page.locator('button[type="submit"]').click();

    // Verify page redirect
    await page.waitForURL('/tasks');
    expect(page.url()).toContain('/tasks');
  });
});
```

**03-navigation.spec.ts - Navigation Verification**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Navigation Verification', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Navigate by clicking menu', async ({ page }) => {
    await page.locator('a[href="/tasks"]').click();
    await expect(page).toHaveURL('/tasks');
  });

  test('Go back to previous page with back button', async ({ page }) => {
    await page.goto('/tasks');
    await page.goBack();
    await expect(page).toHaveURL('/');
  });
});
```

**04-responsive.spec.ts - Responsive Display (Optional)**

```typescript
import { test, expect, devices } from '@playwright/test';

test.describe('Responsive Display Verification', () => {
  test('Layout does not break on mobile display', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 12'],
    });
    const page = await context.newPage();
    await page.goto('/');

    const header = page.locator('header');
    await expect(header).toBeVisible();

    await context.close();
  });
});
```

**05-error-handling.spec.ts - Error Handling (Optional)**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Error Handling Verification', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Error is displayed when required fields are empty', async ({ page }) => {
    await page.locator('button[type="submit"]').click();

    const errorMessage = page.locator('.error-message');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('Required field');
  });

  test('Error is displayed for invalid date format', async ({ page }) => {
    await page.locator('input[name="dueDate"]').fill('invalid-date');
    await page.locator('button[type="submit"]').click();

    const errorMessage = page.locator('.error-message');
    await expect(errorMessage).toContainText('Invalid date format');
  });
});
```

### File Placement

The generated test files are placed in the following structure:

```text
output/pm/
├── e2e-tests/
│   ├── 01-page-load.spec.ts
│   ├── 02-task-creation.spec.ts
│   ├── 03-navigation.spec.ts
│   ├── 04-responsive.spec.ts (Optional)
│   ├── 05-error-handling.spec.ts (Optional)
│   ├── SCENARIOS.md
│   └── fixtures/ (as needed)
├── playwright.config.ts
└── package.json
```

✅ **Checkpoint: Test code (.spec.ts) generated**

```bash
# Check test files
ls -la output/pm/e2e-tests/*.spec.ts

# Test code syntax check
npx tsc --noEmit e2e-tests/*.spec.ts
```

---

## 🚀 Step 4: Test Execution & Report Review

Execute the generated test code and review the results.

### Select Test Execution Method

```json
{
  "type": "AskQuestion",
  "question": "Select how to run the tests",
  "options": [
    {
      "id": "run_all",
      "label": "Run all tests (recommended)",
      "value": "run_all",
      "description": "Run all test suites at once and generate report"
    },
    {
      "id": "headless",
      "label": "Headless mode (fast)",
      "value": "headless",
      "description": "Fast execution without browser display"
    },
    {
      "id": "ui_mode",
      "label": "UI mode (with browser)",
      "value": "ui_mode",
      "description": "Display browser for visual verification"
    },
    {
      "id": "one_by_one",
      "label": "Verify one test at a time",
      "value": "one_by_one",
      "description": "Run tests one at a time and check results"
    }
  ],
  "required": true,
  "helpText": "We recommend UI mode for initial verification, then headless mode for fast execution afterward"
}
```

### Run All Tests

```bash
# Verify the prototype server is running
# (Auto-started by webServer setting in playwright.config.ts)

# Run tests
npx playwright test

# Or run individually
npx playwright test 01-page-load.spec.ts
npx playwright test 02-task-creation.spec.ts
```

### Headless Mode Execution (Fast)

```bash
npx playwright test --headed=false

# For CI environment
CI=true npx playwright test
```

### UI Mode Execution (Browser Display)

```bash
npx playwright test --ui

# Or run specific tests in UI mode
npx playwright test 02-task-creation.spec.ts --ui
```

### Verify One Test at a Time

```bash
# Run in debug mode
npx playwright test --debug

# Or use Playwright Inspector
PWDEBUG=1 npx playwright test 02-task-creation.spec.ts
```

### Report Review

```bash
# Generate and display HTML report
npx playwright show-report

# Generate report only (no display)
npx playwright test --reporter=html
```

The generated report includes the following information:

- ✅ **Passed tests**: Check mark, execution time
- ❌ **Failed tests**: Stack trace, screenshot
- ⚠️ **Skipped tests**: Skip reason
- 📊 **Statistics**: Total runs, passes, failures, skips
- 📸 **Screenshots**: Auto-captured on failure-on-error

### Troubleshooting

| Issue | Cause and Solution |
|------|----------|
| **Playwright installation error** | Run `npx playwright install` after `npm install` |
| **Browser does not start** | Reinstall browser driver with `npx playwright install chromium` |
| **Selector not found** | Check DOM structure with `npx playwright test --debug` and fix selectors |
| **Test timeout** | Specify `timeout: 30000` in playwright.config.ts, or use `test.setTimeout(30000)` |
| **webServer does not start** | Check the `dev` script in package.json, check for port conflicts |

✅ **Checkpoint: Test execution successful**

```bash
# Check test results
# Verify execution result ends with "X passed"
npx playwright test

# Check report
npx playwright show-report
```

---

## ✅ Completion Verification

Verify that the following items are complete:

- ✅ Playwright environment setup complete
  - v1.40.0 or later with `npx playwright --version`
  - playwright.config.ts is configured

- ✅ 3 or more test scenarios designed
  - Documented in output/pm/e2e-tests/SCENARIOS.md
  - Mapping with Lesson 18-6 use cases complete

- ✅ Test code (.spec.ts) generated
  - *.spec.ts files exist in output/pm/e2e-tests/
  - Each file contains test.describe, test.beforeEach, and multiple test()

- ✅ Test execution successful
  - Confirmed "X passed" with `npx playwright test`
  - No failures (or only known failures)

- ✅ Report reviewed
  - HTML report displayed with `npx playwright show-report`
  - Details of each test can be confirmed

---

## ⚠️ Important Notes

- **Browser drivers**: On first setup, install each browser with `npx playwright install` (approximately 500MB)
- **Local server**: If WebServer settings are not configured, run `npm run dev` in a separate terminal
- **Selector maintenance**: When the prototype UI changes, test code selectors also need to be updated
- **CI/CD integration**: When using GitHub Actions or GitLab CI, add a Playwright dependencies installation step to the runner


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── deployment-plan.md  (Deployment Plan)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/deployment-plan.md

# Check the beginning (first 30 lines)
head -30 output/pm/deployment-plan.md
```

> 💡 Full text: Run `cat output/pm/deployment-plan.md` to display the full text

---

## ➡️ Next Steps

**→ Lesson 18-15: Test Plan & Test Case Generation**

In the next lesson, you will:

- Create a test plan
- Generate detailed test cases
- Auto-create test result reports

**Note**: Phase C (Design & Implementation) is complete!
Starting from Lesson 18-15, proceed to Phase D (Testing & Operations).

---

## 📚 Related Resources

- [Playwright Official Documentation](https://playwright.dev/)
- [Playwright Test API Reference](https://playwright.dev/docs/api/class-test)
- [Best Practices for E2E Testing](https://playwright.dev/docs/best-practices)
- [Previous lesson: Lesson 18-13](./start-18-13.md)
- [Module Top: Module 18 PM System Definition](https://ai-agent.camp/en/course/module-18)

---

**Created**: February 2025
**Course**: TaskFlow PM Training Course
**Phase**: Phase C - Design & Implementation (Final Stage)

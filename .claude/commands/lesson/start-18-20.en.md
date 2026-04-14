---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-1", "start-18-2", "start-18-3", "start-18-4", "start-18-5", "start-18-6", "start-18-7", "start-18-8", "start-18-9", "start-18-10", "start-18-11", "start-18-12", "start-18-13", "start-18-14", "start-18-15", "start-18-16", "start-18-17", "start-18-18", "start-18-19"]
level: "intermediate"
tags: ["pm", "capstone", "review", "traceability"]
---

# 🎓 Lesson 18-20: Comprehensive Exercise (Capstone)

| Item | Details |
|------|------|
| Goal | Conduct an integrated review of all 20 lesson deliverables from Module 18 and review the entire product development process |
| Duration | ~30 min |
| Skills Used | pm-toolkit, test-planner, monitoring-dashboard skills |
| Prerequisites | Lesson 18-1〜Lesson 18-19 completed |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

## 📍 Step 1: Reviewing All Deliverables

Review all 20 lesson deliverables created throughout Module 18 and assess completion and progress.

```json
{
  "type": "AskQuestion",
  "question": "Select how to verify deliverables",
  "options": [
    "Auto-scan (all files in output/pm/)",
    "Verify by phase",
    "Check only missing items",
    "Skip"
  ],
  "multiple": false
}
```

### Expected Deliverables List

The following are the deliverables to be generated across all 20 lessons of Module 18:

**Planning phase (18-1 to 18-3):**
- Lesson 18-1: customer-needs.md (customer needs analysis document)
- Lesson 18-2: requirements-brief.md (requirements brief)
- Lesson 18-3: prd.md (PRD - Working Backwards method)

**Requirements phase (18-4 to 18-7):**
- Lesson 18-4: review-summary.md (integrated results of 3 review types)
- Lesson 18-5: requirements-spec.md (requirements specification)
- Lesson 18-6: usecases.md (use case descriptions and sequence diagrams)
- Lesson 18-7: wireframes.md (screen transition diagrams and wireframes)

**Design phase (Lesson 18-8 to 18-12):**
- Lesson 18-8: er-diagram.puml (ER diagram and entity specifications)
- Lesson 18-9: system-architecture.puml (system architecture diagram and API design)
- Lesson 18-10: wbs.md (WBS and Gantt chart)
- Lesson 18-11: notion-export.md (Notion integration export)
- Lesson 18-12: design-system.md (design system specification)

**Implementation/Testing phase (Lesson 18-13 to 18-18):**
- Lesson 18-13: prototype/ (HTML prototype)
- Lesson 18-14: e2e-tests/ (Playwright E2E tests)
- Lesson 18-15: test-plan.md (test plan and test cases)
- Lesson 18-16: unit-test-evidence/ (unit test execution results)
- Lesson 18-17: integration-test-evidence/ (integration test execution results)
- Lesson 18-18: spec-changes.md (meeting design and minutes analysis)

**Integration/Summary (Lesson 18-19 to 18-20):**
- Lesson 18-19: dashboard.py (marimo dashboard)
- Lesson 18-20: capstone-review-summary.html (capstone summary review)

### Automatic Deliverable Scan

```python
import os
from pathlib import Path

output_dir = Path("output/pm")

# Get file list
deliverables = {
    "planning": [],
    "requirements": [],
    "design": [],
    "implementation": [],
    "integration": []
}

if output_dir.exists():
    for file in sorted(output_dir.glob("*")):
        if file.is_file():
            print(f"✓ {file.name} ({file.stat().st_size} bytes)")
else:
    print(f"output/pm/ directory not found")

# Calculate completion rate
total_expected = 20
total_found = len(list(output_dir.glob("*"))) if output_dir.exists() else 0
completion_rate = (total_found / total_expected) * 100

print(f"\nCompletion: {completion_rate:.1f}% ({total_found}/{total_expected} files)")
```

### Completion by Phase

```json
{
  "type": "AskQuestion",
  "question": "Which phase details do you want to review?",
  "options": [
    "Planning phase (1-3)",
    "Requirements phase (4-7)",
    "Design phase (8-12)",
    "Implementation/Testing phase (13-18)",
    "All phases summary"
  ],
  "multiple": false
}
```

## 📍 Step 2: Traceability Verification (Requirements → Design → Testing)

Important verification in product development: confirm that "all requirements are implemented in the design, and all designs are covered by tests."

```json
{
  "type": "AskQuestion",
  "question": "Select the scope of traceability verification",
  "options": [
    "Top 5 requirements",
    "All requirements",
    "Let AI select important ones",
    "Check dashboard only"
  ],
  "multiple": false
}
```

### Traceability Matrix Structure

Perform the following tracking for each requirement:

```text
Requirement (Req-001)
├── Design Document Reference (Design-Section-2.3)
│   ├── UI Wireframe (WF-005)
│   ├── API Endpoint (POST /api/users)
│   └── DB Table (users table)
├── Test Cases (TC-USER-001, TC-USER-002, TC-USER-003)
│   ├── Unit Test: UserModel
│   ├── Integration Test: Auth Flow
│   └── UI Test: Registration Form
└── Test Execution Results
    ├── TC-USER-001: PASS
    ├── TC-USER-002: PASS
    └── TC-USER-003: PASS
```

### Traceability Verification Script

```python
import json
import csv
from pathlib import Path

# Load requirements file
req_file = Path("output/pm/requirements-spec.md")
test_file = Path("output/pm/test-plan.md")

traceability_matrix = {
    "total_requirements": 53,
    "requirements_with_tests": 49,
    "requirements_without_tests": 4,
    "tests_without_requirements": 2,
    "coverage_percentage": 92.45
}

# Generate traceability matrix
with open("output/pm/traceability-matrix.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Requirement ID",
        "Requirement",
        "Design Reference",
        "Test Cases",
        "Status",
        "Coverage"
    ])
    writer.writeheader()

    # Sample requirements
    requirements = [
        {
            "id": "REQ-001",
            "name": "User Registration",
            "design_ref": "Section 3.1, API-001",
            "tests": "TC-AUTH-001, TC-AUTH-002",
            "status": "Covered",
            "coverage": "✓"
        },
        {
            "id": "REQ-002",
            "name": "User Login",
            "design_ref": "Section 3.2, API-002",
            "tests": "TC-AUTH-003, TC-AUTH-004, TC-AUTH-005",
            "status": "Covered",
            "coverage": "✓"
        },
        {
            "id": "REQ-003",
            "name": "Password Reset",
            "design_ref": "Section 3.3, API-003",
            "tests": "TC-AUTH-006, TC-AUTH-007",
            "status": "Partially Covered",
            "coverage": "⚠"
        }
    ]

    for req in requirements:
        writer.writerow(req)

print("Traceability matrix generation complete")
print(f"Total requirements: {traceability_matrix['total_requirements']}")
print(f"Requirements with tests: {traceability_matrix['requirements_with_tests']}")
print(f"Coverage rate: {traceability_matrix['coverage_percentage']:.1f}%")
```

### Gap Analysis

```json
{
  "type": "AskQuestion",
  "question": "How do you want to address the gap analysis results?",
  "options": [
    "Fix all found gaps",
    "Fix high-priority gaps only",
    "Document gaps and defer",
    "Decide after impact assessment"
  ],
  "multiple": false
}
```

**Example detected gaps:**
- Req-045 (API rate limiting): No test cases defined
- Req-051 (monitoring logs): Details unclear in design documents
- TC-PERF-012 (performance test): Corresponding requirement not identified

## 📍 Step 3: Calculating Quality Metrics

Quantify the overall project quality status and evaluate objectively.

```json
{
  "type": "AskQuestion",
  "question": "Select the level of metrics detail",
  "options": [
    "Summary only",
    "Detailed analysis",
    "With benchmark comparison",
    "AI analysis recommended"
  ],
  "multiple": false
}
```

### Key Metrics

```python
import json
from datetime import datetime

quality_metrics = {
    "timestamp": datetime.now().isoformat(),
    "project_name": "TaskFlow v1",
    "evaluation_date": "2024-07-15",

    # 1. Requirements Coverage
    "requirements": {
        "total": 53,
        "specified": 53,
        "coverage_rate": 100,
        "status": "✓ Excellent"
    },

    # 2. Test Coverage
    "test_coverage": {
        "total_requirements": 53,
        "tested_requirements": 49,
        "coverage_rate": 92.45,
        "status": "✓ Good"
    },

    # 3. Test Execution Results
    "test_results": {
        "total_test_cases": 156,
        "passed": 136,
        "failed": 12,
        "skipped": 8,
        "pass_rate": 87.18,
        "status": "⚠ Need Improvement"
    },

    # 4. Documentation Completion
    "documentation": {
        "required_docs": 9,
        "completed_docs": 8,
        "draft_docs": 1,
        "completion_rate": 88.89,
        "status": "✓ Good"
    },

    # 5. Code Quality Metrics
    "code_quality": {
        "lines_of_code": 12450,
        "code_duplication": 8.5,
        "cyclomatic_complexity_avg": 3.2,
        "test_code_ratio": 0.45,
        "status": "✓ Good"
    },

    # 6. Schedule Progress
    "schedule": {
        "planned_duration_days": 180,
        "actual_elapsed_days": 173,
        "progress_percentage": 96.1,
        "status": "✓ On Track"
    },

    # 7. Risk Management
    "risk_management": {
        "identified_risks": 24,
        "mitigated_risks": 22,
        "active_risks": 2,
        "mitigation_rate": 91.67,
        "status": "✓ Good"
    },

    # 8. Overall Score
    "overall_health": {
        "score": 88.5,
        "level": "GREEN",
        "status": "✓ Project Health: Excellent"
    }
}

# Save as JSON
with open("output/pm/quality-metrics.json", "w") as f:
    json.dump(quality_metrics, f, indent=2, ensure_ascii=False)

# Display in table format
print("=" * 70)
print("TASKFLOW V1 - Quality Metrics Summary")
print("=" * 70)
print(f"Evaluation Date: {quality_metrics['evaluation_date']}")
print()

print("📊 Metrics List")
print("-" * 70)
print(f"Requirements Coverage: {quality_metrics['requirements']['coverage_rate']}%")
print(f"Test Coverage:         {quality_metrics['test_coverage']['coverage_rate']:.2f}%")
print(f"Test Pass Rate:        {quality_metrics['test_results']['pass_rate']:.2f}%")
print(f"Documentation:         {quality_metrics['documentation']['completion_rate']:.2f}%")
print(f"Schedule Progress:     {quality_metrics['schedule']['progress_percentage']:.1f}%")
print(f"Risk Mitigation:       {quality_metrics['risk_management']['mitigation_rate']:.2f}%")
print()
print(f"🎯 Overall Project Score: {quality_metrics['overall_health']['score']}/100")
print(f"Status: {quality_metrics['overall_health']['status']}")
print("=" * 70)
```

### Benchmark Comparison

```text
Industry Standard vs TaskFlow v1
┌──────────────────────────┬──────────────┬────────────┬────────────────┐
│ Metric                   │ Industry Std │ TaskFlow   │ Rating         │
├──────────────────────────┼──────────────┼────────────┼────────────────┤
│ Requirements Coverage    │ 85-95%       │ 100%       │ Excellent      │
│ Test Coverage            │ 80-90%       │ 92.45%     │ Excellent      │
│ Test Pass Rate           │ 90%+         │ 87.18%     │ Needs Improve  │
│ Documentation            │ 85%+         │ 88.89%     │ Excellent      │
│ Schedule Achievement     │ 95%+         │ 96.1%      │ Excellent      │
│ Risk Mitigation Rate     │ 85%+         │ 91.67%     │ Excellent      │
└──────────────────────────┴──────────────┴────────────┴────────────────┘
```

## 📍 Step 4: Generating Improvement Proposals

Develop specific improvement proposals for issues detected in each phase.

```json
{
  "type": "AskQuestion",
  "question": "Select the scope of improvement proposals",
  "options": [
    "Planning phase",
    "Design phase",
    "Implementation phase",
    "Testing/Operations phase",
    "All"
  ],
  "multiple": true
}
```

### Improvement Proposal Template

```python
improvement_plan = {
    "planning_phase": {
        "issues": [
            {
                "id": "IMP-P-001",
                "title": "Additional market analysis research",
                "description": "Feature comparison analysis with competitors is insufficient",
                "priority": "Medium",
                "effort": "3 days",
                "recommendation": "Conduct detailed benchmark of competitor products in Q4"
            }
        ]
    },

    "requirements_phase": {
        "issues": [
            {
                "id": "IMP-R-001",
                "title": "Refine non-functional requirements",
                "description": "Performance requirements are not quantitative",
                "priority": "High",
                "effort": "2 days",
                "recommendation": "Define specific values for API response time and DB processing time"
            },
            {
                "id": "IMP-R-002",
                "title": "Expand use cases",
                "description": "Error handling scenarios are insufficient",
                "priority": "Medium",
                "effort": "3 days",
                "recommendation": "Add exception flows to each use case"
            }
        ]
    },

    "design_phase": {
        "issues": [
            {
                "id": "IMP-D-001",
                "title": "Unify API design",
                "description": "Error response format is inconsistent",
                "priority": "High",
                "effort": "2 days",
                "recommendation": "Define a standard error response schema and apply to all APIs"
            }
        ]
    },

    "implementation_phase": {
        "issues": [
            {
                "id": "IMP-I-001",
                "title": "Test execution failure",
                "description": "Test failure in password reset feature (TC-AUTH-007)",
                "priority": "High",
                "effort": "1 day",
                "recommendation": "Fix error handling logic and re-run tests"
            }
        ]
    },

    "testing_phase": {
        "issues": [
            {
                "id": "IMP-T-001",
                "title": "Improve test coverage",
                "description": "Edge case testing is insufficient (4 requirements uncovered)",
                "priority": "Medium",
                "effort": "5 days",
                "recommendation": "Add boundary value analysis and error branch testing"
            }
        ]
    }
}

# Save as JSON
with open("output/pm/improvement-plan.json", "w") as f:
    json.dump(improvement_plan, f, indent=2, ensure_ascii=False)
```

### Lessons Learned Document

```markdown
# Lessons Learned - TaskFlow v1 Project

## Successful Practices

### 1. Requirements Traceability Matrix
**Impact**: Successfully detected design gaps and duplications
**Continue**: Adopt the same approach in the next project

### 2. Early Security Review
**Impact**: Risk detection became possible at the design stage
**Continue**: Make Lesson 18-12 security design a standard for all projects

### 3. Use Case Driven Design
**Impact**: Successfully created UI wireframes from the user's perspective
**Continue**: Generate test cases directly from use cases

## Areas for Improvement

### 1. Test Execution Timing
**Issue**: Test pass rate 87.2% (target 90%)
**Cause**: Tests run immediately after implementation completion, with incomplete implementation
**Action**: Ensure a buffer period of at least 2 days after sprint end

### 2. Documentation Maintenance
**Issue**: Delay in API specification updates
**Cause**: Asynchronous code implementation and documentation updates
**Action**: Introduce automatic OpenAPI specification generation in CI/CD pipeline

### 3. Continuity of Risk Management
**Issue**: Weekly risk reviews regressed to monthly
**Cause**: Meeting reduction due to schedule pressure
**Action**: Fix risk review schedule, never subject to reduction

## Recommendations for Next Project (TaskFlow v2)

1. **Scale up**: Basic design is reusable
2. **Test automation**: Introduce UI test automation tools
3. **DevOps expansion**: Build continuous monitoring in production environment
4. **Team expansion**: Hire dedicated test engineers
```

### NextSteps Roadmap

```json
{
  "type": "AskQuestion",
  "question": "What are the priority issues for TaskFlow v2?",
  "options": [
    "Strengthen test automation",
    "Automate API specification management",
    "Performance optimization",
    "Security hardening",
    "Operations automation"
  ],
  "multiple": true
}
```

## ✅ Deliverables

Deliverables generated in this capstone exercise:

```text
output/pm/
├── traceability-matrix.csv        # Requirements → Design → Test tracking matrix
├── quality-metrics.json           # Quality metrics summary
├── improvement-plan.json          # Improvement proposals list
├── lessons-learned.md             # Lessons learned
└── capstone-review-summary.html   # HTML capstone summary
```

## 🚀 Checklist

```text
□ Verified all deliverables in output/pm/ (20+ files)
□ Created traceability matrix (53 requirements)
□ Calculated quality metrics (8 metrics)
□ Completed gap analysis (4 gaps detected)
□ Generated improvement proposals (for each phase)
□ Created lessons learned document
□ Reviewed all of Module 18 (18-1 through 18-20)
□ Organized recommendations for next project
```

## 📍 Final Verification

```json
{
  "type": "AskQuestion",
  "question": "What is the capstone exercise completion status?",
  "options": [
    "All complete - Module 18 mastered",
    "Almost complete - Fixing details",
    "Partially complete - Some areas need review",
    "Need support - Have questions"
  ],
  "multiple": false
}
```

---

## 🎯 Key Points Upon Completing Module 18

By completing this module, you have acquired the following skills:

✅ **Planning skills**: Market analysis, business requirements definition
✅ **Requirements skills**: System requirements specifications, use cases, user stories
✅ **Design skills**: System architecture, DB design, API design, security design
✅ **Implementation skills**: Code structure, CI/CD pipelines
✅ **Testing skills**: Test plans, test cases, test automation
✅ **Integration skills**: Traceability management, quality metrics, risk management


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── project-summary.md  (project summary)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/project-summary.md

# Check the beginning (first 30 lines)
head -30 output/pm/project-summary.md
```

> 💡 Full text: Run `cat output/pm/project-summary.md` to display the full text

## ➡️ Next Steps

```json
{
  "type": "AskQuestion",
  "question": "Great work! Select your next action",
  "options": [
    "Take on the capstone exercise (course/exercises/18-pm-sysdef/capstone/README.md)",
    "Move to another module",
    "Commit deliverables to Git",
    "End here"
  ],
  "multiple": false
}
```

### How to Proceed to the Capstone Exercise (Optional)

In the advanced **practical capstone exercise**, based on actual project definitions rather than dummy data, you will perform:

1. **Create actual project specifications** (applying methods from 18-1 through 18-20)
2. **Team exercise**: Role distribution among multiple members
3. **Feedback loop**: Stakeholder review
4. **Deliverable quality verification**: Evaluate with all Module 18 checklists

See `course/exercises/18-pm-sysdef/capstone/README.md` for details.

### Committing to Git

```bash
# Commit deliverables to Git
git add output/pm/
git commit -m "Lesson 18-20: TaskFlow PM project integrated review complete

- Traceability matrix: 53 requirements, coverage 92.45%
- Quality metrics summary: overall score 88.5/100
- Gap analysis: 4 improvement proposals
- Lessons learned: documented successes and areas for improvement

Module 18 (PM System Definition) complete
"

git push
```

---

## 🎓 Learning Path Summary

| Item | Lesson | Deliverable |
|------|--------|--------|
| Customer needs analysis | 18-1 | customer-needs.md |
| Requirements brief | 18-2 | requirements-brief.md |
| PRD | 18-3 | prd.md |
| 3-type review | 18-4 | review-summary.md |
| Requirements spec | 18-5 | requirements-spec.md |
| Use cases | 18-6 | usecases.md |
| Screen transitions/WF | 18-7 | wireframes.md |
| DB design | 18-8 | er-diagram.puml |
| System architecture/API | 18-9 | system-architecture.puml |
| WBS/Gantt chart | 18-10 | wbs.md |
| Notion integration | 18-11 | notion-export.md |
| UI design | 18-12 | design-system.md |
| Prototype | 18-13 | prototype/ |
| E2E tests | 18-14 | e2e-tests/ |
| Test plan | 18-15 | test-plan.md |
| Unit tests | 18-16 | unit-test-evidence/ |
| Integration tests | 18-17 | integration-test-evidence/ |
| Meetings/Minutes | 18-18 | spec-changes.md |
| Dashboard | 18-19 | dashboard.py |
| Integrated review | 18-20 | capstone-review-summary.html |

---

**You have completed Module 18 and mastered the entire product development process. Great work!**

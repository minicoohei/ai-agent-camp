---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-1", "output/pm/customer-needs.md"]
level: "intermediate"
tags: ["pm", "requirements", "moscow"]
---

# 🎓 Lesson 18-2: Creating Requirements Document

## 📍 What You'll Do

**Lesson 18-2: Creating Requirements Document** — Welcome!

| Item | Details |
|------|------|
| Goal | Organize TaskFlow's functional/non-functional requirements and create a requirements document (MoSCoW method) |
| Duration | ~25 min |
| Skills Used | pm-toolkit skill |
| Prerequisites | Lesson 18-1 completed, output/pm/customer-needs.md exists |
| Lesson Page | [Module 18: PM & System Requirements Definition](https://ai-agent.camp/en/course/module-18) for parallel reference |

**Session flow:**
1. Load customer-needs.md and extract requirements
2. List functional requirements (prioritize with MoSCoW method)
3. Define non-functional requirements (performance, security, availability)
4. Generate requirements-brief.md

By the end of this session, the TaskFlow requirements document will be completed.

> **💡 Tip**: If the AI response stops midway, type "continue" or "keep going" to resume. Responses may pause due to tool processing, but this is not a malfunction.

---

## 🎯 Readiness Check

Have you finished 18-1 and are ready to create the requirements document? Let's verify.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check if Lesson 18-1 is completed"},
      {"id": "view_html", "label": "View the lesson page first"},
      {"id": "different_lesson", "label": "Move to a different lesson"}
    ]
  }]
}
```

(ready → Proceed to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show the lesson page path)
(different_lesson → Display the module list)

---

## 🚀 Step 1: Loading Customer Needs

Let's prepare to extract requirement types from the customer-needs.md created in the previous lesson.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Verify Customer Needs",
  "questions": [{
    "id": "needs_status",
    "prompt": "Is customer-needs.md ready?",
    "options": [
      {"id": "ready", "label": "File exists, proceed"},
      {"id": "missing", "label": "File is missing"},
      {"id": "show_me", "label": "I want to check the file contents"}
    ]
  }]
}
```

(ready → Proceed to Step 2)
(missing → Redirect to Lesson 18-1)
(show_me → Display file contents)

**Expected result**: customer-needs.md is verified and its contents are organized.

---

## 🚀 Step 2: Listing Functional Requirements

Based on the needs from customer-needs.md, list TaskFlow's functional requirements and prioritize them using the MoSCoW method.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Select Functional Requirement Category",
  "questions": [{
    "id": "functional_category",
    "prompt": "Select a functional requirement category to explore in detail",
    "options": [
      {"id": "task_basics", "label": "Basic Task Management Features"},
      {"id": "team_collab", "label": "Team Collaboration"},
      {"id": "analytics", "label": "Analytics & Reporting"},
      {"id": "notification", "label": "Notifications & Alerts"},
      {"id": "all_categories", "label": "Organize all categories at once (let AI handle)"}
    ]
  }]
}
```

**Example functional requirements per category (AI-suggested):**

```text
[Basic Task Management]
- Create, edit, and delete tasks
- Set task priority
- Set deadlines and reminders
- Status management (Not Started → In Progress → Done)
- Task search and filters

[Team Collaboration]
- Task assignment
- Comments and discussions between team members
- File attachment feature
- Change/delegate assignees
- Team permission management

[Analytics & Reporting]
- Project progress dashboard
- Individual/team productivity analysis
- Overdue task visualization
- Weekly/monthly report generation

[Notifications & Alerts]
- Pre-deadline notifications
- Task assignment notifications
- Comment notifications
- Email/Slack integration
```

**AskQuestion configuration example (MoSCoW classification):**
```json
{
  "title": "🚀 Step 2-2: Classify Features Using MoSCoW Method",
  "questions": [{
    "id": "moscow_classification",
    "prompt": "Classify the extracted features into the following categories",
    "options": [
      {"id": "must_have", "label": "Must Have (essential): Required for MVP"},
      {"id": "should_have", "label": "Should Have (important): Needed in 1-2 months"},
      {"id": "could_have", "label": "Could Have (nice-to-have): Consider for the future"},
      {"id": "wont_have", "label": "Won't Have (not needed): Not implementing this time"},
      {"id": "auto_classify", "label": "Let AI auto-classify"}
    ]
  }]
}
```

**MoSCoW classification guidelines:**
```text
Must Have criteria:
  ✓ Feature used by 80% of users
  ✓ Multiple customers mentioned "we can't work without this"
  ✓ Standard feature of competitors
  → Example: Task creation, priority, deadline setting

Should Have criteria:
  ✓ Feature used by 50%+ of users
  ✓ "It would be nice to have" feedback
  ✓ Can be implemented in the next phase after MVP
  → Example: Productivity dashboard, Slack integration

Could Have criteria:
  ✓ Niche use case
  ✓ High implementation cost
  ✓ Can be added later
  → Example: AI-based priority suggestions, advanced analytics

Won't Have criteria:
  ✓ Out of scope
  ✓ Difficult to operate
  ✓ Unclear demand
  → Example: Mobile native app (web only), advanced customization
```

**Expected result**: Functional requirements are classified from Must Have to Won't Have.

---

## 🚀 Step 3: Defining Non-Functional Requirements

Define requirements beyond features, such as quality, performance, and security.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Select Non-Functional Requirement Aspect",
  "questions": [{
    "id": "nonfunctional_aspect",
    "prompt": "Select a non-functional requirement aspect to define specific target values",
    "options": [
      {"id": "performance", "label": "Performance requirements (response time, processing speed)"},
      {"id": "security", "label": "Security requirements"},
      {"id": "availability", "label": "Availability requirements (uptime, redundancy)"},
      {"id": "usability", "label": "Usability requirements"},
      {"id": "all_aspects", "label": "All aspects at once (let AI handle)"}
    ]
  }]
}
```

**Specific examples per aspect:**

```text
[Performance Requirements]
- Page load time: < 3 seconds
- API response time: < 500ms
- Concurrent users: 1,000
- Database query: < 1 second

[Security Requirements]
- Communication encrypted with SSL/TLS
- Authentication: Email + password (two-factor authentication optional)
- Permission management: Role-based (Admin, Manager, Member)
- Password policy: Minimum 8 characters, including uppercase and numbers
- Audit log: Record all operations

[Availability Requirements]
- Service uptime: 99.5% or higher
- Monthly maintenance: Maximum 4 hours (once per month)
- Backup: Daily automatic backup
- Disaster recovery: RPO = 1 day, RTO = 4 hours

[Usability Requirements]
- Supported browsers: Latest versions of Chrome, Firefox, Safari
- Responsive: Mobile and tablet compatible
- Accessibility: WCAG 2.1 AA compliant
- Supported languages: Japanese (English in the future)
- Help and tutorials: Complete guide for first-time users
```

**AskQuestion configuration example (setting numerical targets):**
```json
{
  "title": "🚀 Step 3-2: Non-Functional Requirement Targets",
  "questions": [
    {
      "id": "perf_targets",
      "prompt": "Select or enter performance targets",
      "options": [
        {"id": "fast", "label": "Fast (page load <2s, API <300ms)"},
        {"id": "normal", "label": "Standard (page load <3s, API <500ms)"},
        {"id": "custom", "label": "Custom input"}
      ]
    },
    {
      "id": "security_level",
      "prompt": "Select the security level",
      "options": [
        {"id": "standard", "label": "Standard (password auth, HTTPS)"},
        {"id": "high", "label": "High (two-factor auth, audit logs)"},
        {"id": "custom", "label": "Custom"}
      ]
    }
  ]
}
```

**Expected result**: Numerical targets for each non-functional requirement are set.

---

## 🚀 Step 4: Generating requirements-brief.md

Document the functional and non-functional requirements organized in Steps 2 and 3.

**Document to generate:**
```text
Generate output/pm/requirements-brief.md with the following content:

# TaskFlow Requirements Document

## 1. Document Information
- Project name: TaskFlow
- Version: 1.0
- Created: {Today's date}
- Target version: MVP (Minimum Viable Product)

## 2. Overview
TaskFlow is a task management web application for small and medium businesses with 10 to 100 employees.
It lets you see at a glance what everyone on the team needs to do today, with AI suggesting priorities to prevent tasks from being overlooked.

## 3. Functional Requirements (MoSCoW Classification)

### 3.1 Must Have (Essential for MVP)
| # | Feature | Description | Priority |
|---|---------|-------------|----------|
| 1 | Task creation | Create tasks with text and deadlines | P0 |
| 2 | Task list view | List your own tasks and team tasks | P0 |
| ... | ... | ... | ... |

### 3.2 Should Have (Phase 2 Implementation)
| # | Feature | Description | Priority |
|---|---------|-------------|----------|
| 1 | Project-based management | Support for multiple projects | P1 |
| ... | ... | ... | ... |

### 3.3 Could Have (Under Consideration)
| # | Feature | Description |
|---|---------|-------------|
| 1 | AI priority suggestions | Auto-determine priority from natural language |
| ... | ... | ... |

### 3.4 Won't Have (Out of Scope)
- Mobile native app (to be considered in the future)
- Advanced customization features (operationally difficult)

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- Page load time: < 3 seconds
- API response time: < 500ms
- Concurrent users: Maximum 1,000

### 4.2 Security Requirements
- Authentication: Email + password (initial version)
- Communication: Encrypted with TLS 1.2 or higher
- Permission management: Role-based (Admin, Manager, Member)
- Audit log: Record and retain all operations

### 4.3 Availability & Reliability
- Service uptime: 99.5% or higher (monthly downtime < 3.6 hours)
- Backup: Daily automatic backup (30-day retention)
- Disaster recovery: RTO 4 hours, RPO 1 day

### 4.4 Usability
- Supported browsers: Latest versions of Chrome, Firefox, Safari
- Responsive design: Mobile and tablet compatible
- Supported languages: Japanese
- Help: Complete tutorials + FAQ

## 5. Constraints
- Development period: 8 weeks (MVP)
- Team size: 3 engineers, 1 PM, 1 designer
- Budget: {Budget range from customer interview}
- Tech stack: Frontend (React), Backend (Node.js + PostgreSQL)

## 6. Assumptions & Risks

### Assumptions
- Customer can provide regular feedback
- Design and brand guidelines are prepared in advance

### Risks
1. Frequent API spec changes → Mitigate with weekly design reviews
2. Scalability → Conduct load testing (Phase 2)

## 7. Next Steps
- Lesson 18-3: Create PRD (Product Requirements Document)

mkdir -p output/pm && save the file to output/pm/requirements-brief.md
```

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Confirm Generated Content",
  "questions": [{
    "id": "doc_generation",
    "prompt": "Ready to generate requirements-brief.md?",
    "options": [
      {"id": "generate", "label": "Generate it"},
      {"id": "review", "label": "Review the content before generating"},
      {"id": "custom", "label": "Customize and generate"}
    ]
  }]
}
```

(generate → Generate the document)
(review → Preview the content)
(custom → Show customization options)

**Expected result**: `output/pm/requirements-brief.md` will be generated.

---

## ⚠️ Common Issues and Solutions

**AskQuestion configuration example:**
```json
{
  "title": "Select issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "Can't determine feature priority in MoSCoW classification"},
      {"id": "trouble_2", "label": "Don't know numerical targets for non-functional requirements"},
      {"id": "trouble_3", "label": "customer-needs.md is missing"},
      {"id": "trouble_4", "label": "Output file is not generated"}
    ]
  }]
}
```

### Issue 1: Can't determine priority in MoSCoW classification
**Solution**: Ask yourself the following questions:
- "Is this feature used by 80% of users?" → If yes, it's Must Have
- "Did multiple customers mention 'we can't work without this'?" → If yes, it's Must Have
- "Is this a standard feature of competitors (Trello, Asana)?" → If yes, it's Should Have
- "Is this needed in 1-2 months?" → If yes, it's Should Have
- "Is this a feature to try and see the response?" → If yes, it's Could Have
- "Is this out of scope for this time?" → If yes, it's Won't Have

### Issue 2: Don't know numerical targets for non-functional requirements
**Solution**: Refer to industry standard values:

| Item | Standard | Fast |
|------|----------|------|
| Page load time | < 3s | < 2s |
| API response | < 500ms | < 300ms |
| Site uptime | 99.5% | 99.99% |
| Backup frequency | Daily | Hourly |

If unsure, choose "Standard" and improve after operations begin.

### Issue 3: customer-needs.md is missing
**Solution**: Start from Lesson 18-1. Alternatively, create a simplified version:
```markdown
# Customer Needs Analysis (Simplified)

## Persona
- Name: Taro (alias)
- Job title: Project Manager
- Challenge: Task management with Excel is cumbersome

## Needs
1. See all team members' tasks
2. Auto-alert when deadlines are overdue
3. Want Slack integration for notifications
```

### Issue 4: Output file is not generated
**Solution**: Check if the `output/pm/` directory exists:
```bash
mkdir -p output/pm
# Then re-run the document generation
```

---

## ✅ Checkpoint
- [ ] Lesson 18-1 is completed
- [ ] customer-needs.md is loaded
- [ ] Functional requirements are classified from Must Have to Won't Have
- [ ] Must Have is narrowed to 5-10 items (check it's not too many)
- [ ] Non-functional requirements have specific numerical targets
- [ ] output/pm/requirements-brief.md is generated
- [ ] Document content is accurate (no typos or contradictions)


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── customer-needs.md  (Customer Needs Analysis)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/customer-needs.md

# Check the beginning (first 30 lines)
head -30 output/pm/customer-needs.md
```

> 💡 Full text: Run `cat output/pm/customer-needs.md` to display the full text

---

## ✅ Completion Check
Enter the following in the Codex chat to check the completion status:

```text
Check the content of output/pm/requirements-brief.md:

1. Are functional requirements classified into Must Have / Should Have / Could Have / Won't Have?
2. Is at least one feature defined in each category?
3. Do non-functional requirements (performance, security, availability) have specific numerical values?
4. Are constraints and assumptions clearly stated?

After verification, reply "Done".
```

**Expected result**: The completeness of the document will be verified.

---

## ➡️ Next Steps

Lesson 18-2 is now complete. Next, you will create the PRD (Product Requirements Document) based on the requirements document.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select how to proceed",
    "options": [
      {"id": "next_auto", "label": "Start next lesson (PRD Creation)"},
      {"id": "next_window", "label": "Start /start-18-3 in a new window"},
      {"id": "review", "label": "Review the requirements document again"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- next_auto → Run /start-18-3
- next_window → Open /start-18-3 in a new window
- review → Re-display requirements-brief.md
- finish → End

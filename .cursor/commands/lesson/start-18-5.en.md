---
description: "When the user says /start-18-5 — Module 18 Lesson 18-5: PM - Requirements Specification Creation (IPA Compliant)"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-4", "output/pm/prd.md", "output/pm/requirements-brief.md"]
level: "intermediate"
tags: ["pm", "requirements-spec", "ipa"]
---

# 🎓 Lesson 18-5: Requirements Specification Creation

Topic: Create a requirements specification for TaskFlow based on the IPA (Information-technology Promotion Agency) format.

## 📍 What You'll Do

| Item | Details |
|------|------|
| Goal | Create a TaskFlow requirements definition document based on IPA format |
| Duration | ~25 min |
| Skills Used | pm-toolkit skill |
| Prerequisites | Lesson 18-4 completed, output/pm/prd.md and output/pm/requirements-brief.md exist |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

## 🎯 Readiness Check

```json
{
  "type": "AskQuestion",
  "question": "Before starting this session, please verify the following. Which items are completed?",
  "options": [
    {
      "label": "✓ All completed (proceed)",
      "value": "ready",
      "next": "step1"
    },
    {
      "label": "⚠️ 16-4 is not yet completed",
      "value": "missing_14_4",
      "next": "abort_14_4"
    },
    {
      "label": "⚠️ output/pm/ directory not found",
      "value": "missing_output",
      "next": "abort_output"
    }
  ],
  "hint": "You need the PRD and requirements summary documents. Check the files created in 16-4."
}
```

**Readiness Check Points:**
- [ ] Lesson 18-4 is completed
- [ ] `output/pm/prd.md` file exists
- [ ] `output/pm/requirements-brief.md` file exists
- [ ] pm-toolkit skill is available

---

## 🚀 Step 1: Loading PRD/Requirements Documents and Explaining Conversion Methods

In this step, learn the methodology for converting the PRD and requirements documents created so far into an IPA-format requirements specification.

```json
{
  "type": "AskQuestion",
  "question": "Do you have experience with requirements definition?",
  "options": [
    {
      "label": "This is my first time",
      "value": "beginner",
      "detail": "We will explain carefully from the basics"
    },
    {
      "label": "I know the concepts",
      "value": "intermediate",
      "detail": "We will focus on key points of the IPA format"
    },
    {
      "label": "I have practical experience",
      "value": "experienced",
      "detail": "We will suggest an efficient approach"
    }
  ],
  "hint": "The explanation level will be adjusted according to your selected experience."
}
```

**Step 1 Explanation:**

The requirements specification is a critical document that clarifies "what to build." The IPA format is Japan's official standard, with the following characteristics:

1. **Structured description method**
   - Clearly separate functional and non-functional requirements
   - Assign unique IDs (e.g., REQ-001) to each requirement
   - Ensure traceability

2. **Conversion process from PRD to requirements**
   ```text
   PRD (Product Specification)
   → User scenario extraction
   → Feature decomposition
   → Requirements description
   → Review & finalize
   ```

3. **Main sections of the IPA format**
   - System overview
   - Functional requirements (by screen/use case)
   - Non-functional requirements (performance, security, availability, etc.)
   - Constraints and dependencies
   - Terminology definitions and prerequisites

**Expected result:**
- Understand PRD contents and extract requirement elements
- IPA format structure is understood
- Ready to proceed to the next step (functional requirements detailing)

---

## 🚀 Step 2: Detailing Functional Requirements

In this step, expand the features described in the PRD on a per-screen basis and define input, processing, output, and constraints for each screen.

```json
{
  "type": "AskQuestion",
  "question": "How would you like to organize functional requirements?",
  "options": [
    {
      "label": "Define by screen",
      "value": "screen_based",
      "detail": "UI/screen-centered requirements definition. Easy to collaborate with UI designers"
    },
    {
      "label": "Define by use case",
      "value": "usecase_based",
      "detail": "Business flow centered. More abstract and flexible"
    },
    {
      "label": "Get AI suggestions",
      "value": "ai_suggest",
      "detail": "Automatically generate optimal classification from PRD"
    }
  ],
  "hint": "TaskFlow is a UI-centered tool, so defining by screen is recommended."
}
```

**Step 2 Details:**

**Functional Requirements Description Format:**

```text
REQ-F-001: Task Creation Screen
  Description: Screen for users to create new tasks

  Input:
    - Task name (text, required, max 100 characters)
    - Priority (dropdown: High/Medium/Low)
    - Due date (date picker, optional)
    - Description (text area, optional, max 500 characters)

  Processing:
    - Input value validation check
    - Save task to DB
    - Redirect to task list screen

  Output:
    - Save success message
    - Add new task to list

  Constraints:
    - User must be authenticated
    - Multiple tasks with the same name can be created
```

**Main Features in TaskFlow Requirements Definition (Examples):**

1. **REQ-F-001: Workspace Creation**
   - Input: Workspace name, description, member settings
   - Processing: Member permission initialization, initial task generation
   - Output: Added to workspace list

2. **REQ-F-002: Task Creation**
   - Input: Title, description, priority, due date, assignee
   - Processing: Task ID generation, status initialization
   - Output: Navigate to task detail screen

3. **REQ-F-003: Task Status Update**
   - Input: Task ID, new status
   - Processing: State transition rule verification, timestamp recording
   - Output: Update confirmation message

4. **REQ-F-004: Task Search/Filter**
   - Input: Keywords, priority, status, assignee
   - Processing: Multi-condition search, sorting
   - Output: Matched task list

5. **REQ-F-005: Add Comment**
   - Input: Task ID, comment text
   - Processing: Comment saving, mention notification
   - Output: Added to comment display area

Similarly, detail 10 or more features below.

**Expected result:**
- At least 10 functional requirements are defined
- Input, processing, output, and constraints are documented for each function
- The functional requirements section of requirements-spec.md is filled in

---

## 🚀 Step 3: Quantifying Non-functional Requirements

Non-functional requirements are system quality attributes. It is important to set specific numerical values rather than vague terms like "fast" or "secure."

```json
{
  "type": "AskQuestion",
  "question": "Select the level of non-functional requirements",
  "options": [
    {
      "label": "For startups (relaxed)",
      "value": "startup",
      "detail": "Requirements at MVP stage. Minimum quality standards"
    },
    {
      "label": "For enterprises (standard)",
      "value": "enterprise",
      "detail": "General SaaS standard. Balanced criteria"
    },
    {
      "label": "For finance/healthcare (strict)",
      "value": "strict",
      "detail": "Compliance focused. High availability and security"
    }
  ],
  "hint": "If TaskFlow aims to be a B2B SaaS, the enterprise (standard) level is recommended."
}
```

**Step 3 Details:**

**Performance Requirements (Startup Standard Examples):**

| Item | Requirement | Rationale |
|------|------|------|
| Response time (page display) | Under 2 seconds | User bounce rate increases at 3 seconds |
| Response time (API) | Under 500ms | Under 2 seconds including frontend processing |
| Concurrent connections (initial) | 100 | Assumed user count at MVP stage |
| DB query execution time | Under 100ms | Multiple queries within API response |

**Performance Requirements (Enterprise Standard Examples):**

| Item | Requirement | Rationale |
|------|------|------|
| Response time (page display) | Under 1 second | Enterprise user productivity standard |
| Response time (API) | Under 200ms | SLA 99.5% requirement |
| Concurrent connections | 1000+ | Assumed demand at growth stage |
| DB query execution time | Under 50ms | Stricter index design |

**Availability Requirements:**

| Item | Requirement (Enterprise) | Rationale |
|------|------|------|
| Uptime | 99.5% | Monthly downtime 3.6 hours |
| Planned maintenance | Once per month, max 4 hours | Avoid Japanese holidays |
| Emergency response time | Within 15 minutes | From fault detection to response start |
| Recovery time (RTO) | Within 1 hour | Recovery from DB backup |

**Security Requirements:**

| Item | Requirement | Implementation Method |
|------|------|------|
| Authentication | OAuth 2.0 + MFA support | Google/GitHub login, TOTP |
| Communication | HTTPS (TLS 1.2+) | All endpoint encryption |
| Password | SHA-256 hash with salt | Using bcrypt library |
| API Authentication | JWT (24-hour expiration) | Tamper detection via token signing |
| Log retention | 12 months | Audit compliance |

**Scalability Requirements:**

| Item | Requirement | Planned Implementation |
|------|------|------|
| Storage | 1TB/year growth assumption | S3 + CloudFront cache |
| User count | Support up to 10,000 users | Horizontal scaling design |
| Database | Read replica support | Master-slave configuration |

**Expected result:**
- Performance requirements are quantified (e.g., "under 2 seconds")
- Availability, security, and scalability requirements are defined
- Each requirement has rationale (business goals or best practices) documented
- The non-functional requirements section of requirements-spec.md is filled in

---

## 🚀 Step 4: Generating requirements-spec.md

In this step, output the functional and non-functional requirements defined so far as an integrated requirements-spec.md file.

```json
{
  "type": "AskQuestion",
  "question": "Select the output format",
  "options": [
    {
      "label": "Full document version",
      "value": "full",
      "detail": "Complete version covering all requirements (15-20 pages equivalent)"
    },
    {
      "label": "Summary version",
      "value": "summary",
      "detail": "Concise version with main requirements only (5-8 pages equivalent)"
    },
    {
      "label": "AI-reviewed version",
      "value": "with_review",
      "detail": "Version where AI checks for missing or contradictory requirements"
    }
  ],
  "hint": "For first-timers, the full document version is recommended. You can reorganize later."
}
```

**Step 4 Details:**

Generate requirements-spec.md using the pm-toolkit skill:

```bash
pm-toolkit generate-requirements-spec \
  --prd output/pm/prd.md \
  --brief output/pm/requirements-brief.md \
  --format full \
  --include-nfr true \
  --output output/pm/requirements-spec.md
```

**Generated File Structure:**

1. **Document Header**
   - Title: TaskFlow Requirements Specification
   - Version: 1.0
   - Created: [today's date]
   - Last updated: [today's date]

2. **Table of Contents**
   - Auto-generated

3. **1. Introduction**
   - System overview
   - Scope
   - Stakeholders

4. **2. Reference Documents**
   - Link to PRD (prd.md)
   - Link to requirements brief (requirements-brief.md)

5. **3. Functional Requirements**
   - REQ-F-001〜REQ-F-XXX
   - Input, processing, output, and constraints for each requirement

6. **4. Non-functional Requirements**
   - 4.1 Performance requirements (REQ-NFR-P-001, etc.)
   - 4.2 Availability/reliability (REQ-NFR-A-001, etc.)
   - 4.3 Security requirements (REQ-NFR-S-001, etc.)
   - 4.4 Scalability (REQ-NFR-SC-001, etc.)

7. **5. External Interface Requirements**
   - API endpoint list
   - Data integration specifications

8. **6. Constraints and Preconditions**
   - Technical constraints
   - Business constraints

9. **7. Terminology Definitions**
   - Important terms used within the system

10. **8. Traceability Matrix**
    - Mapping of PRD requirements ↔ requirements specification requirements

**Post-generation Verification Checks:**

- [ ] File has been generated at output/pm/requirements-spec.md
- [ ] File size is 10KB or more (content is substantial)
- [ ] 10 or more functional requirements are defined
- [ ] Non-functional requirements include numerical values
- [ ] Traceability matrix has been created

**Expected result:**
- output/pm/requirements-spec.md file has been generated
- All requirements are organized in IPA format
- Traceability is ensured
- The document that serves as input for the next step (use case description) is complete

---

## ⚠️ Common Issues and Solutions

```json
{
  "type": "AskQuestion",
  "question": "Which issue are you experiencing?",
  "options": [
    {
      "label": "PRD/requirements files not found",
      "value": "missing_files"
    },
    {
      "label": "Too many features to organize",
      "value": "too_many_features"
    },
    {
      "label": "Unsure about non-functional requirement values",
      "value": "nfr_numbers"
    },
    {
      "label": "requirements-spec.md generation error",
      "value": "generation_error"
    },
    {
      "label": "Traceability matrix is blank",
      "value": "traceability_blank"
    }
  ],
  "hint": "Select the applicable issue and the solution will be displayed."
}
```

**Solutions by Trouble Type:**

### PRD/Requirements Files Not Found

**Cause:** Lesson 18-4 was skipped, or the file was saved in a different location

**Verification commands:**
```bash
ls -la output/pm/
find . -name "prd.md"
find . -name "requirements-brief.md"
```

**Solution:**
1. Go back to Lesson 18-4 and create the PRD
2. Once the file is generated, copy it to the output/pm/ directory
```bash
cp ~/prd.md output/pm/prd.md
```

### Too Many Features to Organize

**Cause:** Trying to include all features described in the PRD as requirements

**Use the MoSCoW Method:**
- **Must have**: Required at the MVP stage
- **Should have**: Implement in the next phase
- **Could have**: In a future phase
- **Won't have**: Out of scope

**Response:**
1. Classify PRD features into 3 categories
2. Limit requirements specification to Must have only (approximately 10-15)
3. Document Should/Could in a separate document (backlog.md)

### Unsure About Non-functional Requirement Values

**General Best Practice Reference Values:**

**For Startups:**
- Response time: 2-3 seconds
- Concurrent connections: 100-500
- Uptime: 99%
- Multi-factor authentication: Optional

**For Enterprise SaaS:**
- Response time: Under 1 second
- Concurrent connections: 1000+
- Uptime: 99.5%
- Multi-factor authentication: Required

**Solution:**
1. Calculate backwards from business goals (revenue, user count projections)
2. Reference competitor product SLAs
3. If uncertain, mark as "TBD" (to be revised later)

### requirements-spec.md Generation Error

**Common Errors:**

```text
Error: prd.md not found
```
→ Check the file path. Specify the full path.

```text
Error: Invalid YAML header
```
→ Check the YAML front matter of requirements-brief.md.

**Solution:**
```bash
# Check file existence
test -f output/pm/prd.md && echo "OK" || echo "NOT FOUND"

# JSON validation (including YAML)
python3 -c "import yaml; yaml.safe_load(open('output/pm/requirements-brief.md'))"  # On Windows, use python instead of python3

# Check pm-toolkit version
pm-toolkit version
```

### Traceability Matrix Is Blank

**Cause:** Requirement ID mapping between PRD and requirements-spec.md has not been done

**Solution:**
1. Add IDs to each PRD requirement (e.g., PR-001, PR-002)
2. In requirements-spec.md, document each requirement to reference PR-XXX
3. Manually create the traceability matrix

**Template:**

| PRD ID | PRD Requirement | Requirement Spec ID | Status |
|--------|--------|---------|----------|
| PR-001 | Workspace management | REQ-F-001 | ✓ |
| PR-002 | Task management | REQ-F-002 to REQ-F-005 | ✓ |

---

## ✅ Checkpoint

When this session is complete, verify that all of the following are checked:

- [ ] **Step 1: PRD Loading**
  - [ ] PRD (prd.md) contents are understood
  - [ ] Purpose of requirements definition is clear
  - [ ] IPA format structure is understood

- [ ] **Step 2: Functional Requirements Definition**
  - [ ] 10 or more functional requirements are defined
  - [ ] Input, processing, and output are documented for each function
  - [ ] Sequentially numbered as REQ-F-001 through REQ-F-XXX
  - [ ] Constraints are documented

- [ ] **Step 3: Non-functional Requirements Quantification**
  - [ ] Performance requirements have specific numerical values
  - [ ] Availability requirements (uptime, RTO, etc.) are defined
  - [ ] Security requirements are documented
  - [ ] Scalability requirements are defined

- [ ] **Step 4: File Generation**
  - [ ] output/pm/requirements-spec.md file exists
  - [ ] File size is 10KB or more
  - [ ] Table of contents is auto-generated in the document
  - [ ] Traceability matrix is included

- [ ] **General**
  - [ ] No issues have occurred
  - [ ] Generated file has been previewed and content verified
  - [ ] Ready to start Lesson 18-6


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── requirements-spec.md  (Requirements Specification)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/requirements-spec.md

# Check the beginning (first 30 lines)
head -30 output/pm/requirements-spec.md
```

> 💡 Full text: Run `cat output/pm/requirements-spec.md` to display the full text

---

## ➡️ Next Steps

```json
{
  "type": "AskQuestion",
  "question": "Select the next action for this session",
  "options": [
    {
      "label": "✓ All checkpoints completed → Proceed to 18-6",
      "value": "proceed_14_6",
      "next": "start-18-6"
    },
    {
      "label": "⚠️ I want to review the requirements again",
      "value": "review_requirements",
      "detail": "Re-edit requirements-spec.md"
    },
    {
      "label": "❓ The issue has not been resolved",
      "value": "troubleshoot",
      "detail": "Return to troubleshooting"
    },
    {
      "label": "📚 I want to refer to the course material",
      "value": "reference",
      "detail": "Display detailed explanation of Module 18"
    }
  ],
  "hint": "If all checkpoints are completed, proceed to Lesson 18-6 (Use Case Description & Sequence Diagrams)."
}
```

**What to do in 18-6:**

In the next session "Lesson 18-6: Use Case Description and Sequence Diagrams":

1. **Creating Use Case Diagrams (UML)**
   - Actor definition (users, administrators, external systems)
   - Use case relationships (include, extend)

2. **Detailed Use Case Descriptions**
   - Pre-conditions and post-conditions
   - Main flow and exception flow
   - Exception handling

3. **Creating Sequence Diagrams**
   - Chronological depiction of major business processes
   - Interactions between systems

4. **Output Files**
   - usecase-diagram.md (use case diagram)
   - usecases-detail.md (detailed use cases)
   - sequence-diagrams.md (sequence diagrams)

---

**You have completed this session. Congratulations! 🎉**

If you have questions or issues, refer to the "Troubleshooting" section above.

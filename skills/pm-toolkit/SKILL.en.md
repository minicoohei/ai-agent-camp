---
name: pm-toolkit
description: "Used for generating PRDs, requirements specifications, request documents, and reviews. Triggered by requests like 'create a PRD', 'write requirements specs', 'review this', 'analyze meeting minutes', etc."
triggers:
  - create a PRD
  - write requirements specs
  - review this
  - analyze meeting minutes
  - pm-toolkit
  - PRD
  - create request document
---

# PM Toolkit - Product Management Toolkit

Provides templates and prompts for use in the planning and requirements definition phases of product development.

## Workflow

1. User specifies the deliverable to create (PRD / requirements spec / review, etc.)
2. Apply the corresponding template and interactively gather information
3. Generate a structured document in `output/pm/`

## Templates

### PRD Template (Working Backwards Method)

```markdown
# PRD: {Product Name}

## 1. Press Release
### Headline
{One-line title that conveys the value}

### Subheadline
{Target users and primary benefit}

### Problem
{3 user pain points}

### Solution
{How the product solves them}

### Customer Testimonial (Hypothetical)
{Ideal user reaction}

### How It Works
{Explain in 3 steps}

### CTA
{Next action}

## 2. FAQ
### User FAQ (5 questions)
### Stakeholder FAQ (5 questions)

## 3. User Stories
| ID | Persona | As a... | I want to... | So that... | Priority |
|----|---------|---------|-------------|-----------|----------|

## 4. Scope
### In Scope (MVP)
### Out of Scope (v2+)

## 5. Success Metrics (KPIs)
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
```

### Requirements Specification Template (IPA-Compliant)

```markdown
# Requirements Specification: {System Name}

## 1. Overview
### 1.1 Purpose
### 1.2 Scope
### 1.3 Glossary

## 2. Functional Requirements
### 2.1 Feature List
| ID | Feature Name | Summary | Priority | Screen |
|----|-------------|---------|----------|--------|

### 2.2 Feature Details
#### FR-001: {Feature Name}
- Input:
- Processing:
- Output:
- Constraints:

## 3. Non-Functional Requirements
### 3.1 Performance Requirements
| Item | Requirement | Rationale |
|------|-------------|-----------|
| Response Time | Page transition within 3 seconds | UX standard |
| Concurrent Users | 100 users | Expected user base |

### 3.2 Security Requirements
### 3.3 Availability Requirements
### 3.4 Migration Requirements

## 4. External Interfaces
### 4.1 User Interface
### 4.2 External System Integration

## 5. Constraints & Assumptions
```

### Request Document Template

```markdown
# Request Document: {Project Name}

## Functional Requirements (MoSCoW Method)
### Must Have
### Should Have
### Could Have
### Won't Have (Out of Scope)

## Non-Functional Requirements
| Category | Requirement | Priority | Notes |
|----------|-------------|----------|-------|
```

### Review Prompts

#### Devil's Advocate Review
AI provides counterarguments and critiques from the following perspectives:
- Is this feature truly necessary? What is the evidence?
- Is there a simpler alternative?
- What is the worst-case scenario? Is the risk acceptable?
- Does the target user actually want this?
- Is it technically feasible? Is the cost reasonable?

#### Security Review (STRIDE)
| Threat | Description | Applicable Area | Countermeasure |
|--------|-------------|----------------|----------------|
| Spoofing | Identity spoofing | Authentication | |
| Tampering | Data tampering | Task data | |
| Repudiation | Denial of actions | Operation logs | |
| Information Disclosure | Data leaks | User data | |
| Denial of Service | Service disruption | API | |
| Elevation of Privilege | Privilege escalation | Admin functions | |

#### Business Case Review
```markdown
## Business Case
### Market Size (TAM/SAM/SOM)
### Competitive Analysis (3C Analysis)
### Revenue Model
### P&L Forecast (3 Years)
| Item | Year 1 | Year 2 | Year 3 |
|------|--------|--------|--------|
```

### Meeting Templates

#### Agenda Template
```markdown
# {Meeting Name} Agenda
- Date/Time:
- Attendees:
- Purpose:

## Topics
1. {Topic 1} (10 min)
2. {Topic 2} (15 min)
3. Next Action Items Review (5 min)
```

#### Meeting Minutes Template
```markdown
# Meeting Minutes: {Meeting Name}
- Date/Time:
- Attendees:
- Note Taker:

## Decisions
1.

## Discussion

## Action Items
| # | Item | Owner | Deadline | Status |
|---|------|-------|----------|--------|
```

#### Meeting Minutes to Spec Change Extraction Prompt
Analyze the following meeting minutes and extract sections that constitute specification changes:
- Change details
- Impact scope (related requirement IDs)
- Reason for change
- Response priority

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| template | Yes | - | Template to use (prd/requirements/review/meeting) |
| product_name | No | TaskFlow | Product name |
| output_dir | No | output/pm/ | Output directory |

## Output Format

Outputs Markdown documents to the specified directory:
- PRD -> `output/pm/prd.md`
- Requirements Spec -> `output/pm/requirements-spec.md`
- Request Document -> `output/pm/requirements-brief.md`
- Review -> `output/pm/review-{type}.md`
- Meeting Minutes -> `output/pm/meeting-minutes.md`

## Example

```
Use the pm-toolkit skill to create a PRD for TaskFlow using the Working Backwards method.
-> output/pm/prd.md will be generated
```

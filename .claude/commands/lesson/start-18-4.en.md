---
description: "When the user says /start-18-4 — Module 18 Lesson 18-4: PM - Three Reviews (Devil's Advocate / Security / Business Planning)"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~40 min"
category: "lesson"
prerequisites: ["start-18-3", "output/pm/prd.md"]
level: "intermediate"
tags: ["pm", "review", "devils-advocate", "security", "business"]
---

# 🎓 Lesson 18-4: Three Reviews

## 📍 What You'll Do

**Lesson 18-4: Three Reviews**  — Welcome!

| Item | Details |
|------|------|
| Goal | Review the PRD from 3 different perspectives (Devil's Advocate, Security, Business Planning) |
| Duration | ~40 min |
| Skills Used | pm-toolkit skill |
| Prerequisites | Lesson 18-3 completed、output/pm/prd.md exists |
| Lesson Page | [Module 18: PM & System Requirements Definition](https://ai-agent.camp/en/course/module-18) for parallel reference |

**Session flow:**
1. Devil's Advocate Review (AI plays the contrarian role)
2. Security Review (STRIDE + data flow analysis)
3. Business Planning Review (business case, market size, P&L)
4. Integrating review results and reflecting improvements

By the end of this session, the three review result documents for TaskFlow will be complete.

Deliverables:
- `output/pm/review-devils-advocate.md`
- `output/pm/review-security.md`
- `output/pm/review-business-case.md`

> **💡 Tip**: If the AI response stops midway, type "continue" or "keep going" to resume. Responses may pause due to tool processing, but this is not a malfunction.

---

## 🎯 Readiness Check

Have you finished Lesson 18-3 and are ready for the three reviews? Let's verify.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check if Lesson 18-3 is completed"},
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

## 🚀 Step 1: Devil's Advocate Review

Rigorously review the prd.md created in the previous lesson from the perspective of investors and skeptics.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Devil's Advocate Review Severity",
  "questions": [{
    "id": "review_severity",
    "prompt": "Select the review severity level",
    "options": [
      {"id": "soft", "label": "Gentle (constructive feedback focused)"},
      {"id": "balanced", "label": "Standard (balanced)"},
      {"id": "harsh", "label": "Harsh (investor perspective)"},
      {"id": "ultra_harsh", "label": "Ultra harsh (counter every point)"}
    ]
  }]
}
```

(soft → Start constructive review)
(balanced → Start balanced review)
(harsh → Start investor perspective review)
(ultra_harsh → Start ultra-strict review)

**After selection (example)**:
Input:
```text
Based on output/pm/prd.md, act as a Devil's Advocate and
rigorously review the TaskFlow proposal.

Key review items:

[Business Validity]
1. Is this feature truly necessary? What is the basis?
   - Is the evidence for user needs sufficient?
   - Has it been mentioned by multiple users?
   - Why are existing tools (Asana, Trello) not sufficient?

2. Does the target market truly want this?
   - What is the basis for TAM/SAM/SOM estimates?
   - What are the differentiation points from competitors?
   - Why is this company size (10-100 employees) optimal?

3. Is the MVP scope appropriate?
   - Are there features that can be cut?
   - Are there simpler alternatives?
   - Is everything truly needed for MVP?

[Technical Validity]
4. Is it technically feasible?
   - What is the basis for estimates?
   - What are the technical risks?
   - Is scalability ensured?

5. Is the cost/ROI reasonable?
   - Development cost: Is it accurate? Any hidden costs?
   - Monetization: What is the revenue per user?
   - What is the payback period?
   - Can the return on investment be justified?

[Risk / Worst-Case Scenarios]
6. What is the worst-case scenario?
   - What if users don't adopt it?
   - What if there are technical failures in key features?
   - What if competitors release the same features?
   - Are these risks acceptable?

[Overall Proposal]
7. Is the product strategy convincing?
   - Why this solution?
   - Have other approaches been considered?
   - Is the long-term vision clear?

Provide specific criticisms and questions for each item.
Summarize improvement proposals at the end.
```

**Expected result**: Rigorous review results from the Devil's Advocate perspective are output.

---

## 🚀 Step 2: Security Review (STRIDE)

Analyze TaskFlow's security risks using the STRIDE framework.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Security Review Scope",
  "questions": [{
    "id": "security_scope",
    "prompt": "Select the security review scope",
    "options": [
      {"id": "stride_only", "label": "STRIDE analysis only"},
      {"id": "stride_dataflow", "label": "STRIDE + data flow diagram"},
      {"id": "stride_full", "label": "STRIDE + data flow + countermeasure proposals"},
      {"id": "comprehensive", "label": "Full security assessment"}
    ]
  }]
}
```

(stride_only → Analyze all 6 STRIDE categories)
(stride_dataflow → Additional data flow diagram analysis)
(stride_full → Include countermeasure proposals)
(comprehensive → Include risk assessment and prioritization)

**After selection (example)**:
Input:
```text
For TaskFlow in output/pm/prd.md,
conduct a STRIDE security analysis.

[STRIDE 6-Category Analysis]

1. **Spoofing (Identity Spoofing)**
   Target: User authentication
   Questions:
   - What is the user authentication method? (email/password, OAuth, SSO)
   - What is the risk of spoofing attacks?
   - Countermeasures: Strong password policy, MFA, session management

2. **Tampering (Data Tampering)**
   Target: Task data
   Questions:
   - Is the integrity of task data guaranteed?
   - What is the risk of unauthorized data modification?
   - Countermeasures: Digital signatures, audit logs, transaction management

3. **Repudiation (Non-Repudiation)**
   Target: Operation logs and audit trails
   Questions:
   - Can you track who did what?
   - Is there a possibility users deny their actions?
   - Countermeasures: Complete operation logs, timestamps, tamper prevention

4. **Information Disclosure (Data Leakage)**
   Target: User data (tasks, messages, etc.)
   Questions:
   - What is the risk of accessing other users' data?
   - Is the database encrypted?
   - Is communication encrypted?
   - Countermeasures: TLS/SSL, encrypted storage, access control

5. **Denial of Service (DoS)**
   Target: API, web servers
   Questions:
   - What is the resilience against intentional overload attacks?
   - Are DDoS countermeasures implemented?
   - What about rate limiting?
   - Countermeasures: WAF, rate limiting, capacity planning

6. **Elevation of Privilege (Privilege Escalation)**
   Target: Admin functions, team permissions
   Questions:
   - What is the risk of regular users gaining admin privileges?
   - Is the role-based access control (RBAC) design appropriate?
   - Countermeasures: Strict privilege verification, audit logs, periodic privilege review

[Data Flow Diagram]
Illustrate the data flow between the following components:
- User browser <-> Web server
- Web server <-> API server
- API server <-> Database
- API server <-> Notification service (email/Slack)

Verify security at each connection point.

[Threat/Countermeasure Table Format]
| Threat Category | Threat | Impact | Risk | Countermeasure | Implemented |
|------------|-----|--------|--------|------|---------|
| Spoofing | Credential leakage | High | User data leakage | MFA | ✗ |
| Tampering | Task tampering | Medium | Data corruption | Audit logs | ✓ |

Output the completed analysis in markdown.
```

**Expected result**: The security review based on STRIDE analysis is completed.

---

## 🚀 Step 3: Business Planning Review (Business Case)

Analyze TaskFlow's business case in detail.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Business Case Depth",
  "questions": [{
    "id": "business_depth",
    "prompt": "Select the business case depth",
    "options": [
      {"id": "simple", "label": "Simple (market size + competitors only)"},
      {"id": "standard", "label": "Standard (+ revenue model)"},
      {"id": "detailed", "label": "Detailed (+ 3-year P&L forecast)"},
      {"id": "full", "label": "Full (+ investor pitch)"}
    ]
  }]
}
```

(simple → Market size and competitive analysis)
(standard → Also add revenue model)
(detailed → Include 3-year P&L forecast)
(full → Full version for investor pitch)

**After selection (example)**:
Input:
```text
Based on output/pm/prd.md and output/pm/customer-needs.md,
conduct a business case analysis for TaskFlow.

[1. Market Sizing]

TAM (Total Addressable Market):
- Target: Project management software market for Japanese companies with 10-100 employees
- Market size estimation method (top-down):
  * Number of companies in Japan: approx. 3.8 million
  * Companies with 10-100 employees: approx. 100,000 (from existing data)
  * Task management tool adoption rate: currently 15% (estimated)
  * Average purchase amount: 500K JPY/year/company (5 users x 100K JPY/user)
  * TAM = 100K x 500K = 5 billion JPY/year

SAM (Serviceable Addressable Market):
- Market that TaskFlow targets
- Target: Companies with 10-100 employees dissatisfied with Asana/Trello
- Estimate: 30% of TAM = 1.5 billion JPY/year

SOM (Serviceable Obtainable Market):
- Achievable market share within 5 years
- Target: 1% = 150 million JPY/year
- This equals 300 companies x 500K JPY per year

[2. 3C Analysis]

**Customer**
- Primary: PM/leaders at mid-size companies with 10-100 employees
- Secondary: Sales managers, production/development team leaders
- Needs:
  * Want to solve inefficiencies in task management with Excel/email
  * Visibility of tasks across the entire team
  * Automation of deadline management

**Competitor**
- Direct competitors: Asana, Trello, Notion, Monday.com
  * Asana: Feature-rich but expensive (1,350 JPY/user/month), complex
  * Trello: Simple but weak in team analytics features
  * Notion: General-purpose with a steep learning curve
  * Monday.com: Modern but insufficient Japanese language support
- Indirect competitors: Excel, Google Sheets, Slack
  * Already present in companies, zero adoption cost
  * Inferior in functionality but very strong substitutes

**Company**
- TaskFlow strengths:
  * Simple and intuitive UI (optimized for Japanese companies)
  * AI-powered priority suggestions
  * Notifications via Slack integration
  * Affordable pricing (estimated 500 JPY/user/month)
- Weaknesses:
  * Zero brand recognition
  * Time needed for initial market building
  * Many startups competing

[3. Revenue Model]

B2B SaaS model:
- Price: 500-1,000 JPY/user/month
- Minimum contract unit: 5 users = 2,500-5,000 JPY/month
- Support: Email/chat (free in the first year)
- Upsell: Premium plan (API, SSO, advanced analytics)

LTV (Life Time Value) and CAC (Customer Acquisition Cost):
- Average contract period: 2 years (24 months)
- Average churn rate: 5%/month (initial stage)
- LTV = 3,000 JPY/month x 24 months = 72,000 JPY
- CAC target: 18,000 JPY (25% of LTV)

[4. 3-Year P&L Forecast]

**Year 1:**
- Start: Monthly recurring revenue 1M JPY (400 initial customers)
- Growth rate: 10%/month (typical SaaS value)
- Annual recurring revenue: 18M JPY
- Development cost: 15M JPY (personnel costs)
- Marketing: 5M JPY
- Infrastructure/other: 3M JPY
- **EBITDA: -13M JPY (loss)**

**Year 2:**
- Monthly recurring revenue: 2M JPY (800 customers)
- Annual recurring revenue: 36M JPY
- Development cost: 20M JPY
- Marketing: 10M JPY
- Infrastructure/other: 5M JPY
- **EBITDA: -9M JPY (improving)**

**Year 3:**
- Monthly recurring revenue: 4M JPY (1,600 customers)
- Annual recurring revenue: 72M JPY
- Development cost: 25M JPY (organization expansion)
- Marketing: 15M JPY
- Infrastructure/other: 8M JPY
- **EBITDA: 4M JPY (break-even)**

[5. Risks & Opportunities]

**Downside risks:**
1. Competitor price drops
   - Asana drops to 100 JPY/user/year
   - Countermeasure: Continue differentiating with AI features

2. Churn rate higher than expected (10%/month)
   - Impact: Break-even delayed to Year 2
   - Countermeasure: Improve onboarding, build success stories

3. Regulatory tightening (GDPR, etc.)
   - Countermeasure: Implement compliance proactively

**Upside opportunities:**
1. Acquiring large contracts with 50 companies
   - Additional revenue of 1.5M JPY/month
   - Reduce Year 1 losses by 20%

2. Indirect sales through API/integration partners
   - Integration with existing SaaS (HR, ERP)

3. International expansion (Southeast Asia)
   - Full-scale from Year 3, new market development

Output the completed analysis in markdown.
```

**Expected result**: The business case analysis (market size, 3C, revenue model, P&L forecast) is completed.

---

## 🚀 Step 4: Integrating Review Results

Consolidate the three review results and create an improvement action plan.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Incorporating Review Results",
  "questions": [{
    "id": "integration_method",
    "prompt": "How would you like to incorporate the review results?",
    "options": [
      {"id": "auto_update", "label": "Auto-update the PRD"},
      {"id": "action_list", "label": "Create only an improvement list"},
      {"id": "important_only", "label": "Incorporate only critical findings"},
      {"id": "review_first", "label": "Review everything before deciding"}
    ]
  }]
}
```

(auto_update → Execute automatic PRD update)
(action_list → Create improvement list)
(important_only → Create prioritized list)
(review_first → Create integrated report for review)

**After selection (example)**:
Input:
```text
Consolidate the three review results (Devil's Advocate, Security, Business Case)
and create output/pm/review-summary.md.

Format:

# TaskFlow Integrated Review Report

## Executive Summary
- Overall rating: (on a 5-point scale)
- Key findings: 3-5 items
- Recommended actions: by priority

## 1. Devil's Advocate Review Results
### Critical Findings
- [ ] Finding 1
- [ ] Finding 2
- [ ] Finding 3

### Improvement Proposals
- Proposal 1: Implementation difficulty (Low/Medium/High), Priority (P0/P1/P2)
- Proposal 2: ...

## 2. Security Review Results
### High-Risk Threats (Implementation Required)
- Threat 1 → Countermeasure and implementation timeline

### Medium-Risk Threats (Early Implementation Recommended)
- Threat 2 → Countermeasure and implementation timeline

### Low-Risk Threats (Can Be Addressed Later)
- Threat 3 → Countermeasure and implementation timeline

## 3. Business Case Review Results
### Management Decision
- Is the market size sufficient: Yes / No / Basis for judgment
- ROI expectation: Appropriate / Room for improvement
- Competitive advantage: Is it secured?

### Actions
- Marketing investment: Increase/maintain/decrease decision
- Development scope: Need for adjustment

## 4. Integrated Judgment & Next Steps

### Go/No-Go Decision
- Current: Go → With the following conditions
  * Condition 1: Clear XXX
  * Condition 2: Implement XXX

Or in case of No-Go:
- Proposal: Reconsider after improving XXX

### Action Plan by Priority

**Phase 0 (Go/No-Go Decision):**
- Action 1: XXX (responsible, duration)
- Action 2: XXX (responsible, duration)

**Phase 1 (Before MVP Development):**
- Action 1: Create security design document (Security Engineer, 1 week)
- Action 2: Market validation (PM, 2 weeks)

**Phase 2 (During MVP Development):**
- Action 1: Security testing (QA, ongoing)
- Action 2: Customer feedback collection (CS, ongoing)

**Phase 3 (Post-MVP):**
- Action 1: Security audit (external, 1 month)
- Action 2: Marketing acceleration (Sales & Marketing)

## 5. Risks & Concerns
| Risk | Impact | Countermeasure |
|--------|------|------|
| R1 | High | ... |
| R2 | Medium | ... |

Save this report after completion.
```

**Expected result**: The improvement plan integrating the three reviews is completed.

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
      {"id": "trouble_1", "label": "Devil's Advocate is too harsh"},
      {"id": "trouble_2", "label": "I don't understand STRIDE analysis"},
      {"id": "trouble_3", "label": "I don't know how to estimate market size"},
      {"id": "trouble_4", "label": "prd.md does not exist"}
    ]
  }]
}
```

### Trouble 1: Devil's Advocate is too harsh
**Solution**: Change the review severity to "gentle." By instructing "focus on constructive feedback" in the prompt, you can get more actionable advice.

Debug:
```text
Tell the AI "try again at a gentle level," or
re-run with severity="soft" in the new input
```

### Trouble 2: Do not understand STRIDE analysis
**Solution**: Review the definition of each STRIDE category:

| Threat | Description | Example |
|------|------|-----|
| Spoofing | Impersonation of user authentication | Password eavesdropping, session hijacking |
| Tampering | Data falsification | Unauthorized task data modification, direct DB manipulation |
| Repudiation | Denial of actions | Claiming "I did not perform that operation" |
| Information Disclosure | Information leakage | User data breach, eavesdropping |
| Denial of Service | Service disruption | DDoS, overload attacks |
| Elevation of Privilege | Privilege escalation | Regular user obtaining admin privileges |

Request the AI to "also show specific STRIDE examples."

### Trouble 3: Do not know how to estimate market size
**Solution**: There are two approaches to market size estimation:

**Top-down method:**
```text
1. Number of domestic companies (statistics) -> Target companies -> Adoption rate -> Average purchase amount
2. Example: 3.8M companies x 3% x 50% x 500K JPY = 28.5B JPY
```

**Bottom-up method:**
```text
1. Existing customers (track record) -> Reachable market -> Growth rate
2. Example: 100 companies x 100 x 20% growth = 2,000 company market size
```

If unsure, explicitly state multiple assumptions and show a sensitivity analysis of "what happens when assumptions change."

### Trouble 4: prd.md does not exist
**Solution**: Start from Lesson 18-3. Alternatively, create a simplified PRD:

```markdown
# TaskFlow - PRD (Simplified Version)

## Overview
Task management web app for companies with 10-100 employees

## Key Features
- Task creation and management
- Team sharing
- AI priority suggestions
- Slack integration

## Target
PM/leaders at mid-size companies with 10-100 employees

## Pricing
500 JPY/user/month
```

Proceed using this simplified version as a base.

### Trouble 5: Generated files are not output
**Solution**: Check if the `output/pm/` directory exists:

```bash
mkdir -p output/pm
# Then re-run review generation
```

---

## ✅ Checkpoint
- [ ] Received 3 or more points from the Devil's Advocate review
- [ ] Analyzed all 6 STRIDE categories
- [ ] Created business case (market size or revenue model)
- [ ] output/pm/review-devils-advocate.md has been generated
- [ ] output/pm/review-security.md has been generated
- [ ] output/pm/review-business-case.md has been generated
- [ ] Extracted key improvement actions from the three reviews
- [ ] Made a Go/No-Go decision


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── review-*.md  (review document collection)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/review-*.md

# Check the beginning (first 30 lines)
head -30 output/pm/review-*.md
```

> 💡 Full text: Run `cat output/pm/review-*.md` to display the full text

---

## ✅ Completion Check
Enter the following in the Codex chat to check the completion status:

```text
Display a list of review-related files in output/pm/:

1. Number of findings in review-devils-advocate.md
2. Number of high-risk threats in review-security.md
3. 3-year P&L estimate in review-business-case.md

Verify that these three files are all present.
```

**Expected result**: The completeness of review documents is verified.

---

## ➡️ Next Steps

Lesson 18-4 (Phase A "Planning") is now complete. Next, proceed to Phase B "Requirements Definition & Design."

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select how to proceed",
    "options": [
      {"id": "next_auto", "label": "Start the next lesson (Requirements Specification)"},
      {"id": "next_window", "label": "Start /start-18-5 in a new window"},
      {"id": "review", "label": "Review the results once more"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- next_auto → Run /start-18-5
- next_window → Open /start-18-5 in a new window
- review → Re-display review documents
- finish → End

**Note**: Phase A (Planning) complete! Next, in Phase B (Requirements Definition & Design), create more detailed requirements specifications.


---
description: "When the user says /start-18-3 — Module 18 Lesson 18-3: PM - PRD Creation (Working Backwards Method)"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-2", "output/pm/requirements-brief.md"]
level: "intermediate"
tags: ["pm", "prd", "working-backwards"]
---

# 🎓 Lesson 18-3: PRD Creation (Working Backwards Method)

## 📍 What You'll Do

| Item | Details |
|------|------|
| Goal | Create TaskFlow's PRD using the Amazon Working Backwards method |
| Duration | ~30 min |
| Skills Used | pm-toolkit skill |
| Prerequisites | Lesson 18-2 completed、output/pm/requirements-brief.md exists |
| Lesson Page | [Module 18: PM & System Requirements Definition](https://ai-agent.camp/en/course/module-18) for parallel reference |

**Session flow:**
1. Explanation of the Working Backwards method
2. Drafting a PRD in press release format
3. Adding FAQ and user stories
4. Generating and formatting prd.md

Deliverable: `output/pm/prd.md`

---

## 🎯 Readiness Check - readiness check

```json
{
  "type": "AskQuestion",
  "question": "Pre-lesson readiness check",
  "description": "Check the required conditions before starting Lesson 18-3.",
  "options": [
    {
      "label": "Ready. Lesson 18-2 completed, requirements-brief.md exists",
      "value": "ready",
      "next_action": "continue"
    },
    {
      "label": "I want to review Lesson 18-2",
      "value": "review_previous",
      "next_action": "view_html",
      "url": "../../start-18-2"
    },
    {
      "label": "I want to check the current file structure",
      "value": "check_structure",
      "next_action": "bash",
      "command": "ls -la output/pm/ 2>/dev/null || echo 'Directory not found'"
    },
    {
      "label": "I want to learn Module 18 from the beginning",
      "value": "start_module",
      "next_action": "view_html",
      "url": "https://ai-agent.camp/en/course/module-18"
    }
  ]
}
```

**Confirmation items:**
- ✓ Lesson 18-2 (Requirements Definition Brief) is completed
- ✓ `output/pm/requirements-brief.md` exists
- ✓ Project background is understood

---

## 🚀 Step 1: Understanding and Preparing the Working Backwards Method

```json
{
  "type": "AskQuestion",
  "question": "How familiar are you with the Amazon Working Backwards method?",
  "description": "The Working Backwards method is an innovative product development approach adopted by Amazon. We will check your proficiency with this method and adjust the explanation level accordingly.",
  "options": [
    {
      "label": "I know it well (learned from Amazon case studies and books)",
      "value": "expert",
      "next_action": "continue"
    },
    {
      "label": "I only know the overview (developing from customer perspective)",
      "value": "intermediate",
      "next_action": "continue"
    },
    {
      "label": "First time hearing about it, or 'what is that?'",
      "value": "beginner",
      "next_action": "continue"
    }
  ]
}
```

### What is the Working Backwards Method

The Working Backwards method is an Amazon development approach that **"defines the product by working backwards from the customer's perspective."**

**Differences from traditional development methods:**

| Traditional Method | Working Backwards |
|--------|-----------------|
| Start from technical specifications | **Start from customer experience** |
| Think about usage after completion | **Write the press release first** |
| Requirements definition from internal perspective | **Write customer questions (FAQ) first** |

**The 5 Steps of Working Backwards:**

1. **Press Release** - Write the product announcement for customers
2. **FAQ (Frequently Asked Questions)** - Answer questions from customers and stakeholders
3. **User Stories** - Define specific usage scenarios
4. **Scope Definition** - Distinguish between MVP and future versions
5. **Success Metrics** - Define KPIs

**When applying to TaskFlow:**
- Clarify who is "struggling with task management"
- Express "what changes would make users happy" in the press release
- Explain "why it is needed" in the FAQ

### Preparation: Review Previous Documents

```json
{
  "type": "AskQuestion",
  "question": "Would you like to review the contents of requirements-brief.md?",
  "description": "The previous Requirements Brief will serve as reference material when creating the press release in Step 2. We recommend reviewing the contents in advance.",
  "options": [
    {
      "label": "Check the content (display the file)",
      "value": "view",
      "next_action": "bash",
      "command": "cat output/pm/requirements-brief.md || echo 'File not found'"
    },
    {
      "label": "Already checked, proceed to next step",
      "value": "skip",
      "next_action": "continue"
    },
    {
      "label": "File not found, I need help",
      "value": "help",
      "next_action": "bash",
      "command": "find . -name 'requirements-brief.md' -o -name '*requirement*' 2>/dev/null | head -10"
    }
  ]
}
```

---

## 🚀 Step 2: Drafting PRD in Press Release Format

By writing the PRD in press release format, you create a document where **customer benefits are clear** and that is **easy for internal engineers to understand**.

```json
{
  "type": "AskQuestion",
  "question": "How would you like to set the tone and target audience for the press release?",
  "description": "In the Working Backwards method, how you write the press release matters. Adjust the tone and content based on the target audience.",
  "options": [
    {
      "label": "Business-oriented (formal, assuming shareholders/investors)",
      "value": "formal",
      "next_action": "continue"
    },
    {
      "label": "Startup-oriented (casual, assuming user community)",
      "value": "casual",
      "next_action": "continue"
    },
    {
      "label": "Internal (practical, for engineers)",
      "value": "internal",
      "next_action": "continue"
    },
    {
      "label": "Investor-oriented (numbers-focused, emphasizing growth)",
      "value": "investor",
      "next_action": "continue"
    }
  ]
}
```

### Press Release Template

The Working Backwards press release requires the following sections:

**Required sections:**

```text
# [HEADLINE: Concise and powerful title]

## Summary
[Describe the essence of the product in one paragraph]

## Problem
[What challenges do target customers face]

## Solution
[How TaskFlow solves this, 3-5 bullet points]

## Customer Benefits
[Specific advantages for the customer]

## Availability / Pricing
[Availability and pricing strategy]

## More Information
[Website, documentation, contact information]

---

## Customer Testimonials
"[Express expected benefits in the customer's own words]" - [Company Name, Title]
```

### Executing Step 2

```json
{
  "type": "AskQuestion",
  "question": "Would you like the AI to generate the press release draft, or create it manually?",
  "description": "In Step 2, you can choose to have the AI automatically generate a press release draft by reading requirements-brief.md, or create it manually yourself.",
  "options": [
    {
      "label": "Have AI generate it (auto-generate with pm-toolkit)",
      "value": "ai_generate",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-pressrelease --tone-mode {tone_option} --input-file output/pm/requirements-brief.md"
    },
    {
      "label": "Create manually (AI assists with review only)",
      "value": "manual",
      "next_action": "continue"
    },
    {
      "label": "I want to see AI's draft then adjust",
      "value": "hybrid",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-pressrelease-draft --tone-mode {tone_option} --input-file output/pm/requirements-brief.md"
    }
  ]
}
```

**Steps for manual creation:**

1. Open the editor: `output/pm/prd-draft.md`
2. Paste the template above
3. Refer to the requirements-brief and fill in each section
4. Before submitting for internal review, verify that "customer benefits" are clearly stated

**Press release quality checklist:**
- [ ] The headline expresses "what changes" at a glance
- [ ] The problem section describes customer pain points realistically
- [ ] The solution section focuses on "What/Why" rather than "How"
- [ ] Customer testimonials specifically express business value
- [ ] Technical jargon is minimized, using words anyone can understand

---

## 🚀 Step 3: Adding FAQ and User Stories

Once the press release is complete, add **FAQ (Frequently Asked Questions)** and **User Stories** to make the PRD more detailed.

### 3-1: Creating FAQ (Frequently Asked Questions)

```json
{
  "type": "AskQuestion",
  "question": "Select which perspectives to cover in the FAQ",
  "description": "FAQs require two types of questions: (1) questions from end users, and (2) questions from stakeholders (executives and engineers). Which would you like to prioritize?",
  "options": [
    {
      "label": "User FAQ (usage, features, support)",
      "value": "user_faq",
      "next_action": "continue"
    },
    {
      "label": "Stakeholder FAQ (business value, technology, scalability)",
      "value": "stakeholder_faq",
      "next_action": "continue"
    },
    {
      "label": "User stories (specific usage scenarios)",
      "value": "user_stories",
      "next_action": "continue"
    },
    {
      "label": "All (User FAQ + Stakeholder FAQ + User Stories)",
      "value": "all",
      "next_action": "continue"
    }
  ]
}
```

**Example user FAQ:**

```markdown
## FAQ - For Users

### Q1: How many tasks can TaskFlow manage?
A: TaskFlow supports managing thousands of tasks simultaneously. ...

### Q2: Can I migrate from existing tools (Notion, Asana, etc.)?
A: Yes, you can bulk migrate using the CSV/JSON import feature. ...

### Q3: Is there a mobile app?
A: The MVP version provides a web app. A mobile app is planned for v2. ...

### Q4: Can I use it offline?
A: Yes, basic features are available in offline mode. ...

### Q5: How granular can team permission management be configured?
A: We provide three levels of permissions: Owner, Member, and Viewer. ...
```

**Example stakeholder FAQ:**

```markdown
## FAQ - For Stakeholders

### Q1: How large is TaskFlow's target market?
A: The global project management market is $XX billion annually, with a growth rate of Y%. ...

### Q2: What differentiates TaskFlow from competitors (Jira, Monday.com, etc.)?
A: TaskFlow specializes in "simplicity" and "team collaboration." ...

### Q3: What is the revenue model?
A: We adopt a SaaS subscription model (freemium + paid plans). ...

### Q4: Is technical scalability adequate?
A: With cloud-native architecture, we anticipate scaling to millions of users. ...

### Q5: What about security and compliance?
A: We have obtained SOC 2 Type II certification and comply with GDPR/data protection laws. ...
```

### 3-2: Defining User Stories

```json
{
  "type": "AskQuestion",
  "question": "How would you like to prioritize user stories?",
  "description": "User stories are classified into Must/Should/Could by implementation priority. How many stories would you like to write for each level?",
  "options": [
    {
      "label": "Focus on Must (MVP essential) only: 3-5 stories",
      "value": "must_only",
      "next_action": "continue"
    },
    {
      "label": "Must + Should: 8-10 total",
      "value": "must_should",
      "next_action": "continue"
    },
    {
      "label": "Full set (Must/Should/Could): 15+",
      "value": "full_set",
      "next_action": "continue"
    },
    {
      "label": "Let AI auto-generate",
      "value": "ai_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-user-stories --input-file output/pm/requirements-brief.md --count 10"
    }
  ]
}
```

**User story template:**

```text
As a [role], I want [feature/action], so that [business value/benefit]

Example 1) As a busy project manager, I want to set recurring tasks, so that I don't have to manually recreate them every week.

Example 2) As a team lead, I want to see real-time progress on all projects, so that I can identify blockers immediately.

Example 3) As a new user, I want a guided onboarding tutorial, so that I can set up my first project in under 5 minutes.
```

**MoSCoW Priority:**

```text
## User Stories (Prioritized)

### MUST (MVP Essential)
- [ ] US-1: As a user, I want to create tasks with title and description
- [ ] US-2: As a team lead, I want to assign tasks to team members
- [ ] US-3: As a user, I want to mark tasks as complete/incomplete

### SHOULD (Want to implement in v1)
- [ ] US-4: As a user, I want to set due dates and reminders
- [ ] US-5: As a user, I want to organize tasks into projects/folders

### COULD (Implementation in future versions)
- [ ] US-6: As a user, I want to integrate with Slack notifications
- [ ] US-7: As a user, I want to generate reports on productivity metrics
```

---

## 🚀 Step 4: Scope Definition and Success Metrics

Finally, clarify **what to do and what not to do**, and define **how to measure success**.

### 4-1: In Scope (MVP) vs Out of Scope (Future Versions)

```json
{
  "type": "AskQuestion",
  "question": "How would you like to proceed with scope definition?",
  "description": "Deciding what to include and exclude significantly impacts development effort and timeline. Choose from the methods below.",
  "options": [
    {
      "label": "Let AI suggest (auto-extract from requirements-brief)",
      "value": "ai_suggest",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-scope-definition --input-file output/pm/requirements-brief.md"
    },
    {
      "label": "Decide manually (manual input using template)",
      "value": "manual",
      "next_action": "continue"
    },
    {
      "label": "Hybrid (review and adjust AI suggestions)",
      "value": "hybrid",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-scope-definition-draft --input-file output/pm/requirements-brief.md"
    }
  ]
}
```

**Scope definition template:**

```text
## In Scope (MVP v1.0)

### Core Features
- Task creation, editing, deletion
- Task assignment to team members
- Due date and priority setting
- Project/folder organization
- Basic filtering and search
- Team collaboration (comments on tasks)
- Email notifications

### Technical
- Web application (responsive design for desktop, tablet)
- SQLite/PostgreSQL database
- REST API for future mobile app
- Basic authentication

## Out of Scope (v2+)

### Future Features
- Mobile native apps (iOS/Android)
- Advanced reporting and analytics
- Integration with Slack/Teams
- Time tracking and estimation
- Resource allocation algorithms
- Advanced permission management

### Not Planned
- Desktop client (will use web)
- Complex workflow automation
- AI-powered task recommendations (future AI phase)
```

### 4-2: Defining Success Metrics / KPIs

```json
{
  "type": "AskQuestion",
  "question": "Which framework would you like to use to define success metrics (KPIs)?",
  "description": "Product Success Metrics are measurable indicators directly tied to business goals. The AARRR framework (Acquisition, Activation, Retention, Revenue, Referral) is commonly used.",
  "options": [
    {
      "label": "Define using AARRR (Pirate Metrics)",
      "value": "aarrr",
      "next_action": "continue"
    },
    {
      "label": "Define using OKR (Objectives & Key Results)",
      "value": "okr",
      "next_action": "continue"
    },
    {
      "label": "Define using general SaaS KPIs",
      "value": "saas_kpi",
      "next_action": "continue"
    },
    {
      "label": "Let AI generate everything",
      "value": "ai_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-success-metrics --input-file output/pm/requirements-brief.md --framework aarrr"
    }
  ]
}
```

**KPI Definition Examples Using the AARRR Framework:**

```text
## Success Metrics (KPIs)

### Acquisition
- Monthly signup rate: Target 500 users/month (by end of v1)
- Organic traffic rate: Target 30% (vs paid marketing)
- Sign-up conversion rate: Target 3% (from landing page)

### Activation
- First project creation rate: Target 70% (within 7 days of signup)
- First task creation rate: Target 85% (within 24 hours)
- Tutorial completion rate: Target 60%

### Retention
- Monthly active users (MAU): Target 80% of signups
- Weekly active users (WAU): Target 50% of signups
- Churn rate: Target < 5% per month (for paid users)

### Revenue
- Conversion to paid: Target 10% of free users
- Average revenue per account (ARPA): Target $50/month
- Customer lifetime value (LTV): Target $2,400

### Referral
- Viral coefficient: Target 1.2 (each user brings 1.2 new users)
- Referral signup rate: Target 15% of new users
```

---

## 🚀 Step 5: PRD Completion and Output

Finally, integrate all sections and generate the final PRD (`prd.md`).

```json
{
  "type": "AskQuestion",
  "question": "Select the method for generating the PRD (prd.md)",
  "description": "Integrate all previous sections (press release, FAQ, user stories, scope, KPIs) to generate the final PRD.",
  "options": [
    {
      "label": "Have AI integrate and generate everything (auto-generate with pm-toolkit)",
      "value": "full_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-full-prd --input-files output/pm/requirements-brief.md,output/pm/prd-draft.md --output output/pm/prd.md"
    },
    {
      "label": "Manually assemble each section",
      "value": "manual_assembly",
      "next_action": "continue"
    },
    {
      "label": "Review AI's draft then finalize",
      "value": "review_then_finalize",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-draft --input-files output/pm/requirements-brief.md,output/pm/prd-draft.md"
    }
  ]
}
```

**Final PRD structure:**

```text
# Product Requirements Document (PRD)
## TaskFlow v1.0

---

## Executive Summary
[Condensed summary of the press release]

---

## Press Release
[Full press release text created in Step 2]

---

## FAQ

### User FAQ
[User FAQ created in Step 3]

### Stakeholder FAQ
[Stakeholder FAQ created in Step 3]

---

## User Stories

### MUST (MVP v1.0)
[Prioritized user stories]

### SHOULD (Future version)
[...]

### COULD (Further future)
[...]

---

## Scope Definition

### In Scope (MVP v1.0)
- Core Features
- Technical Requirements
- Design Scope

### Out of Scope (v2+)
- Future Features
- Not Planned

---

## Success Metrics (KPIs)

### AARRR Framework
- Acquisition: ...
- Activation: ...
- Retention: ...
- Revenue: ...
- Referral: ...

---

## Dependencies & Risks

### Dependencies
- Integration with existing systems
- Availability of external services

### Risk & Mitigation
- Risk factors and mitigation strategies

---

## Timeline & Milestones
- Kick-off: ...
- Soft launch: ...
- GA: ...
```

### Verify Output Files

```json
{
  "type": "AskQuestion",
  "question": "Would you like to review the generated PRD?",
  "description": "Verify that prd.md has been generated correctly.",
  "options": [
    {
      "label": "Display file contents (verification)",
      "value": "view",
      "next_action": "bash",
      "command": "cat output/pm/prd.md | head -100"
    },
    {
      "label": "Check file size and creation date",
      "value": "check_meta",
      "next_action": "bash",
      "command": "ls -lh output/pm/prd.md && wc -l output/pm/prd.md"
    },
    {
      "label": "Review the last section (KPIs)",
      "value": "view_end",
      "next_action": "bash",
      "command": "tail -50 output/pm/prd.md"
    }
  ]
}
```

---

## ⚠️ Common Issues and Solutions

### Trouble 1: Cannot think of a press release headline

**Symptom:** Rewriting the headline many times, or it only contains the word "TaskFlow"

**Cause:** The headline needs to convey "customer benefits" rather than the "product name"

**Solution:**

```json
{
  "type": "AskQuestion",
  "question": "Are you having trouble creating the headline?",
  "options": [
    {
      "label": "Yes, I'd like a template",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "No, I'm fine",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**Template:**

```text
Pattern 1) Solve [target]'s [problem] with [solution]
  Example: "Reduce the task management burden for busy team leaders with real-time visualization"

Pattern 2) [Product name] that achieves [business outcome]
  Example: "TaskFlow - Reduce project completion time by 30%"

Pattern 3) A [new approach] that is [qualitative benefit]
  Example: "Simple yet powerful. TaskFlow transforms task management"

Key points:
- Avoid jargon (bureaucratic terms like "visualization" or "optimization" are not recommended)
- Focus on "Why" (not "what features" but "what impact")
```

---

### Trouble 2: Scope is too broad and MVP definition is vague

**Symptom:** More than 20 features listed in In Scope, or everything is labeled as "all MVP"

**Cause:** Cannot distinguish between "nice to have" and "must have"

**Solution:**

```json
{
  "type": "AskQuestion",
  "question": "Do you feel the scope is too broad?",
  "options": [
    {
      "label": "Yes, I want to narrow it down",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "No, I'm fine",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**How to define MVP:**

```text
**MVP = A minimized scope set that completely solves one pain point**

TaskFlow MVP example:
  ✓ Include in MVP: Task create/edit/delete + team assignment + deadline setting
  ✗ Exclude from MVP: Statistics/analytics, Slack integration, time tracking, advanced permissions

Decision criteria:
- "Can the user feel value without this?" → Yes ⇒ MVP essential
- "Can it be handled with a hack/workaround?" → Yes ⇒ OK for v2+
- "Because competitors do it" → That alone is not a valid reason ✗
```

---

### Trouble 3: Do not know how to set KPIs

**Symptom:** KPI is just "increase user count" or has no numerical basis

**Cause:** The relationship between the business model and measurement metrics is unclear

**Solution:**

```json
{
  "type": "AskQuestion",
  "question": "Are you having trouble setting KPIs?",
  "options": [
    {
      "label": "Yes, teach me the framework",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "No, I'm fine",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**AARRR Framework Implementation Example:**

```text
### Acquisition (How to acquire users)
- KPI examples: Monthly signup rate, Cost per acquisition (CPA), Sign-up conversion rate
- TaskFlow example: Launch on Product Hunt ⇒ Target 1000 signups

### Activation (Time until user feels value)
- KPI examples: % users who complete onboarding, Time to first action, Feature adoption rate
- TaskFlow example: 70%+ of users create their first project within 7 days

### Retention
- KPI examples: Monthly/Weekly active users (MAU/WAU), Churn rate, Engagement score
- TaskFlow example: 80%+ monthly active users

### Revenue (Monetization)
- KPI examples: ARPU (Average Revenue Per User), Conversion to paid, LTV (Life Time Value)
- TaskFlow example: Freemium ⇒ 10%+ paid plan conversion rate ⇒ LTV $2400

### Referral (Viral growth)
- KPI examples: Viral coefficient, Referral rate, NPS (Net Promoter Score)
- TaskFlow example: Each user invites an average of 0.5 new users
```

---

### Trouble 4: requirements-brief.md not found

**Symptom:** Error "File not found" or `/output/pm/` directory does not exist

**Cause:** Lesson 18-2 was not completed, or the file was saved in a different location

**Solution:**

```json
{
  "type": "AskQuestion",
  "question": "Cannot find requirements-brief.md?",
  "options": [
    {
      "label": "Not found. I want to redo Lesson 18-2",
      "value": "redo_lesson",
      "next_action": "view_html",
      "url": "../../start-18-2"
    },
    {
      "label": "It might be in a different location (search for it)",
      "value": "search",
      "next_action": "bash",
      "command": "find . -name 'requirements-brief*' -o -name '*brief*' 2>/dev/null"
    },
    {
      "label": "I want to create new (I'd like a template)",
      "value": "create_new",
      "next_action": "continue"
    }
  ]
}
```

---

## ✅ Checkpoint

After completing this session, verify that all the following boxes are checked:

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "label": "Understood the Working Backwards method",
      "required": true
    },
    {
      "label": "PRD in press release format has been drafted",
      "required": true
    },
    {
      "label": "FAQ (user-facing + stakeholder-facing) contains 5+ items",
      "required": true
    },
    {
      "label": "3+ user stories defined (MUST priority)",
      "required": true
    },
    {
      "label": "Scope (In Scope / Out of Scope) is clearly defined",
      "required": true
    },
    {
      "label": "Success metrics (KPIs) are set using the AARRR framework",
      "required": true
    },
    {
      "label": "File `output/pm/prd.md` has been generated",
      "required": true
    },
    {
      "label": "prd.md has 300+ lines (sufficient detail)",
      "required": false,
      "hint": "Recommended: approximately 300-500 lines"
    }
  ]
}
```

**Final Verification Commands:**

```bash
# Check if file exists
ls -lh output/pm/prd.md

# Check line count
wc -l output/pm/prd.md

# Preview content
head -50 output/pm/prd.md
```


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── prd.md  (Product Requirements Document)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/prd.md

# Check the beginning (first 30 lines)
head -30 output/pm/prd.md
```

> 💡 Full text: Run `cat output/pm/prd.md` to display the full text

---

## ➡️ Next Steps

Lesson 18-3  is complete, proceed to the next lesson:

```json
{
  "type": "NextStep",
  "next_lesson": "start-18-4",
  "title": "18-4: Three Reviews (Business / UX / Tech)",
  "description": "Review the created PRD from three perspectives (business, user experience, technical feasibility) and finalize the final version.",
  "estimated_duration": "~25 min",
  "what_you_will_do": [
    "Check logical consistency of the PRD (business review)",
    "Evaluate feasibility of user experience (UX review)",
    "Verify technical feasibility (tech review)",
    "Integrate feedback to complete the final PRD",
    "PRD sign-off and version management"
  ],
  "button_label": "Proceed to 18-4",
  "button_action": "open_lesson",
  "button_target": "start-18-4"
}
```

---

## 📌 Supplementary Materials

### Reference: Official Information on Amazon Working Backwards

To learn more about the Working Backwards method, refer to the following resources:

- **Book:** "Working Backwards" by Colin Bryar & Bill Carr (authored by Amazon VP Product)
- **Amazon official guide:** "Customer Obsession," one of the Leadership Principles
- **Case study:** Kindle development example (press conference materials)

### Reference: PARD Framework (Extended Version)

In addition to Working Backwards, the following PRD frameworks are also useful:

```text
## PARD Framework
- P (Purpose): Why are we building this
- A (Approach): What approach solves this
- R (Result): Expected outcomes
- D (Dependency): Dependencies and risks
```

### Reference: PRD Template Variations

PRD templates vary by industry and stage:

| Template | Application | Features |
|---------|------|------|
| **Lean PRD** | Early-stage startups | 1-3 pages, agile |
| **Working Backwards** | Amazon style | Press release centered |
| **Full PRD** | Large/established companies | 100+ pages, detailed |
| **One-Pager** | For executives | Summarized in 1 page |

**TaskFlow adopts the Working Backwards (Lean version).**

---

## 🎓 Review Quiz

To review what you learned in this lesson、here is a short quiz：

```json
{
  "type": "AskQuestion",
  "question": "Which of the following are characteristics of the Working Backwards method? (Multiple selection allowed)",
  "options": [
    {
      "label": "Starts from the customer's perspective",
      "value": "correct_1",
      "is_correct": true
    },
    {
      "label": "Write the press release first",
      "value": "correct_2",
      "is_correct": true
    },
    {
      "label": "Starts from technical specifications",
      "value": "incorrect_1",
      "is_correct": false
    },
    {
      "label": "Think about how to use it after completion",
      "value": "incorrect_2",
      "is_correct": false
    }
  ]
}
```

```json
{
  "type": "AskQuestion",
  "question": "What is the best definition of MVP (Minimum Viable Product)?",
  "options": [
    {
      "label": "The first version packed with as many features as possible",
      "value": "wrong",
      "is_correct": false
    },
    {
      "label": "The minimum set of features that can deliver value to customers",
      "value": "correct",
      "is_correct": true
    },
    {
      "label": "A version that includes all planned features",
      "value": "wrong2",
      "is_correct": false
    }
  ]
}
```

```json
{
  "type": "AskQuestion",
  "question": "Name the three Rs of the AARRR framework. (Open-ended question)",
  "hint": "Retention, Revenue, Referral",
  "expected_answer": "Retention, Revenue, Referral"
}
```

---

**Congratulations! Lesson 18-3 (PRD Creation) is complete!**

Next, in Lesson 18-4, you will review the created PRD from multiple perspectives and finalize it.

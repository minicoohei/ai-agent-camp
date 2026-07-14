---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
duration: "~20 min"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["lp", "copywriting", "persona", "brief"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 13-1: Organizing Your Value Proposition (Hearing & Copywriting)

## 📍 What You'll Do

Welcome to **Lesson 13-1: Organizing Your Value Proposition**!

| Item | Details |
|------|---------|
| Goal | Conduct a hearing via AskQuestion, organize persona, value proposition, and copy to build the foundation for Landing Page creation |
| Duration | ~20 min |
| Skills Used | Interactive dialogue flow with choices, lp-designer skill |
| Prerequisites | Lesson 0-1 complete, ai-agent-camp is open |
| Course Page | Refer to [Module 13: Landing Page/Website Design](https://ai-agent.camp/en/course/module-13) in parallel |

**Session flow:**
1. Hearing on Landing Page/Website type and service information
2. Define target persona
3. Generate benefits and copy
4. Draft section structure

By the end of this session, the value proposition brief needed for Landing Page creation will be complete.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. Responses may pause depending on the tool, but this is not a malfunction.

---

## 🎯 Readiness Check

First, let's confirm everything is ready.

**AskQuestion settings:**
```json
{
  "title": "🎯 Pre-Session Check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Proceed to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Project Type Hearing

First, let's decide what kind of page to create. We'll use AskQuestionTool for the hearing.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: What kind of page will you create?",
  "questions": [
    {
      "id": "project_type",
      "prompt": "Select the type of page to create",
      "options": [
        {"id": "lp", "label": "Landing Page - Focused on a single CTA"},
        {"id": "hp", "label": "Homepage - Multi-section layout"},
        {"id": "product", "label": "Product Page - Feature showcase"},
        {"id": "event", "label": "Event/Campaign Page"}
      ]
    },
    {
      "id": "service_category",
      "prompt": "Select your service category",
      "options": [
        {"id": "saas", "label": "SaaS / Web Service"},
        {"id": "ec", "label": "E-commerce / Retail"},
        {"id": "consulting", "label": "Consulting / Professional Services"},
        {"id": "education", "label": "Education / School"},
        {"id": "event", "label": "Event / Seminar"},
        {"id": "portfolio", "label": "Portfolio / Personal"},
        {"id": "other", "label": "Other"}
      ]
    }
  ]
}
```

**After selection**: Confirm specific service information via free-text input based on the user's choices.

Enter the following information:
```text
Tell us about the Landing Page/Website you're creating:

1. Service name (official name):
2. Service overview (1-2 sentences):
3. The most important message to convey:
4. Reference site URL (if any):
```

**Expected result**: Basic service information is collected.

---

## 🚀 Step 2: Define Target Persona

Next, clarify who the page is for.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Target Persona",
  "questions": [
    {
      "id": "target_age",
      "prompt": "What is the main target age group?",
      "options": [
        {"id": "20s", "label": "20s"},
        {"id": "30s", "label": "30s"},
        {"id": "40s", "label": "40s"},
        {"id": "50plus", "label": "50s and above"},
        {"id": "all", "label": "Wide age range"}
      ]
    },
    {
      "id": "target_role",
      "prompt": "What is the target's main role/position?",
      "options": [
        {"id": "executive", "label": "Executive / Board Member"},
        {"id": "manager", "label": "Director / Manager"},
        {"id": "marketer", "label": "Marketer / PR"},
        {"id": "engineer", "label": "Engineer / Technical"},
        {"id": "sales", "label": "Sales"},
        {"id": "individual", "label": "Individual / General Consumer"},
        {"id": "other", "label": "Other"}
      ]
    },
    {
      "id": "cta_goal",
      "prompt": "What is the CTA goal? (The action you want users to take)",
      "options": [
        {"id": "signup", "label": "Free signup / Account creation"},
        {"id": "inquiry", "label": "Contact / Consultation"},
        {"id": "download", "label": "Download materials"},
        {"id": "purchase", "label": "Purchase / Sign up"},
        {"id": "trial", "label": "Start free trial"},
        {"id": "event", "label": "Event registration"}
      ]
    }
  ]
}
```

**After selection**: Confirm the persona's challenges (pain points).

Enter additional information:
```text
List 3 challenges your target audience faces:

1. The biggest challenge:
2. A daily frustration:
3. Something they want to solve but have given up on:
```

**Expected result**: A clear persona is defined.

---

## 🚀 Step 3: Generate Benefits and Copy

Generate value proposition copy based on the hearing results.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Design Tone Selection",
  "questions": [{
    "id": "design_tone",
    "prompt": "Select the design tone",
    "options": [
      {"id": "professional", "label": "Professional / Trustworthy"},
      {"id": "modern", "label": "Modern / Stylish"},
      {"id": "playful", "label": "Playful / Friendly"},
      {"id": "luxury", "label": "Luxury / Elegant"},
      {"id": "minimal", "label": "Minimal / Simple"},
      {"id": "tech", "label": "Tech / Cutting-edge"}
    ]
  }]
}
```

**Post-selection instructions**:

The AI will auto-generate the following:
```text
Based on the hearing results from Steps 1-2, generate the following:

## 3 Benefits
1. Main benefit (greatest value)
2. Sub-benefit 1 (efficiency / time-saving)
3. Sub-benefit 2 (peace of mind / support)

## Copy Proposals
- Headline (H1): Impactful copy within 15 characters
- Subheadline: Supplementary explanation within 30 characters
- CTA text: Action text within 7 characters
- CTA supplement: Reassurance text below the CTA button (e.g., Free, no credit card required)

Generate 3 patterns.
```

**Expected result**: 3 copy proposal patterns are generated.

---

## 🚀 Step 4: Draft Section Structure

Determine the Landing Page section structure based on the copy.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 4: Section Structure",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Compile all hearing results (service info, persona, benefits, copy) into
output/lp-brief.md.

Output in the following format:

# LP Brief: {Service Name}

## Persona
- Name: {Alias}
- Age: {Age}
- Role: {Role}
- Challenges: {3 challenges}

## Value Proposition
1. {Main benefit}
2. {Sub-benefit 1}
3. {Sub-benefit 2}

## Copy (Selected)
- Headline: {Selected copy}
- Subheadline: {Selected copy}
- CTA: {Selected CTA}

## Section Structure
1. Hero - Headline + CTA
2. Pain Points - 3 challenge statements
3. Solution - Solution introduction
4. Features - 3-4 features/highlights
5. Social Proof - Results/Testimonials
6. FAQ - 3-5 frequently asked questions
7. Final CTA - Final action

## Design Tone
{Selected tone}
```

**Expected result**: The brief is saved to `output/lp-brief.md`.

---

## ⚠️ Common Issues and Solutions

In Codex, you typically present choices in chat so the user can select their issue and get guidance instantly.

**AskQuestion settings example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "I don't know what to enter"},
      {"id": "trouble_2", "label": "The copy doesn't feel right"},
      {"id": "trouble_3", "label": "I'm unsure about the section structure"},
      {"id": "trouble_4", "label": "The output file isn't generated"}
    ]
  }]
}
```

### Issue 1: I don't know what to enter
**Solution**: A fictional service is fine. Try something familiar like "An AI-powered Landing Page auto-generation service."

### Issue 2: The copy doesn't feel right
**Solution**: Give instructions like "make it more casual," "add numbers," or "add urgency" to regenerate.

### Issue 3: I'm unsure about the section structure
**Solution**: Start with the basic structure (Hero → Pain → Solution → Features → Proof → CTA), then add or remove sections later.

### Issue 4: The output file isn't generated
**Solution**: Check if the `output/` directory exists. If not, create it with `mkdir -p output`.

---

## ✅ Checkpoint
- [ ] Service type and category are decided
- [ ] Target persona is defined
- [ ] 3 benefits are clear
- [ ] Headline and CTA text are decided
- [ ] Section structure draft exists
- [ ] `output/lp-brief.md` has been generated


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/
└── lp-brief.md  (Landing Page planning brief)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/lp-brief.md

# Check the beginning (first 30 lines)
head -30 output/lp-brief.md
```

> 💡 View full content: `cat output/lp-brief.md` to display the entire file

---

## ✅ Completion Check
Enter the following in the Codex chat to verify completion:

```text
Check the contents of output/lp-brief.md and verify that persona,
value proposition, copy, and section structure are all filled in.
```

**Expected result**: The brief's completeness is confirmed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin.

In Codex, you can typically select from choices in chat.

**AskQuestion settings example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (Wireframe Creation)"},
      {"id": "next_window", "label": "Open /start-13-2 in a new window"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → Run /start-13-2
- next_window → Open /start-13-2 in a new window
- finish → End

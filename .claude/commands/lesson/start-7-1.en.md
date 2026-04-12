---
description: "When the user says /start-7-1 — Module 7 Lesson 7-1: Skill Design Fundamentals (Anthropic Best Practices)"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-6-2"]
duration: "~20 min"
level: "intermediate"
tags: ["agent", "skill-design", "best-practices"]
---

# 🎓 Lesson 7-1: Skill Design Fundamentals

## 📍 What You'll Do

Welcome to **Lesson 7-1: Skill Design Fundamentals**!

| Item | Details |
|------|------|
| Goal | Understand Anthropic's skill design best practices and create a use-case specification for a meeting-notes skill |
| Duration | ~20 min |
| Skills used | None (design and conceptual lesson) |
| Prerequisites | Lesson 6-2 completion recommended (basic Skills knowledge) |
| Course page | Refer to [Module 7: Skill/Commands](https://ai-agent.camp/en/course/module-7) alongside this lesson |

**Session flow:**
1. Understand the 3 skill categories
2. Learn Progressive Disclosure (step-by-step information reveal)
3. Define the use case for the meeting-notes skill
4. Set success criteria

By the end of this session, you will have completed a use-case specification for the meeting-notes skill (meeting-notes-summarizer).

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite verification)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Understand the 3 Skill Categories

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Understand the 3 Skill Categories",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Anthropic's skill guide defines 3 categories:

1. **Document Creation** — Document generation and editing (e.g., meeting notes, reports, contracts)
2. **Workflow Automation** — Automating repetitive tasks (e.g., code review, deployment, testing)
3. **MCP Enhancement** — Extending MCP servers (e.g., API integration, data retrieval, external service integration)

Input:
```text
Explain the 3 skill categories (Document Creation / Workflow Automation / MCP Enhancement),
including their characteristics and concrete examples.
Which category does our "meeting-notes skill" belong to?
```

**Expected result**: Understanding of the 3 categories and confirmation that the meeting-notes skill falls under "Document Creation".

---

## 🚀 Step 2: Learn Progressive Disclosure

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Learn Progressive Disclosure",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Skills reveal information in 3 stages:

1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — Loaded on trigger (recommended under 5,000 words)
3. **Bundled resources** (scripts/, references/) — Loaded only when needed

Input:
```text
Explain the 3 stages of Progressive Disclosure using the meeting-notes skill as an example:

- Stage 1 (Metadata): What name and description to set
- Stage 2 (SKILL.md body): What procedures and guidelines to describe
- Stage 3 (Bundled resources): What to place in scripts/ and references/

Design each stage concisely, keeping token costs in mind.
```

**Expected result**: Concrete content design for the 3 stages and understanding of their impact on the context window.

---

## 🚀 Step 3: Define the Meeting-Notes Skill Use Case

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Define the Meeting-Notes Skill Use Case",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

The use-case specification should include:
- Skill name and category
- Trigger phrases (when it should activate)
- Input and output
- Differentiation from existing skills

Input:
```text
Create a use-case specification for the "meeting-notes-summarizer" skill.

Include the following items:

## Use-Case Specification

| Item | Details |
|------|------|
| Skill name | meeting-notes-summarizer |
| Category | Document Creation |
| Purpose | Automatically generate structured meeting notes from meeting text/memos |

### Trigger Phrases (when to activate)
- Phrases that should trigger: 5 or more
- Phrases that should NOT trigger: 3 or more

### Input Specification
- Input format (text, file, etc.)
- Required and optional information

### Output Specification
- Output format (Markdown)
- Required sections (Attendees, Agenda, Decisions, Action Items, Next Meeting)

### Differentiation from Existing Skills
- Differences from check-inbox, slack-search, and document-processor
```

**Expected result**: A completed use-case specification with a clear overview of the skill.

---

## 🚀 Step 4: Set Success Criteria

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Set Success Criteria",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Set success criteria from both quantitative and qualitative perspectives.

Input:
```text
Define success criteria for the meeting-notes-summarizer skill.

### Quantitative Metrics
- Trigger accuracy (correct activation rate / false-positive avoidance rate)
- Output completeness (required section coverage rate)
- Processing speed (response time)

### Qualitative Metrics
- Output readability
- Specificity of action items
- Accurate identification of attendees

### Test Cases
- Minimum test: Notes from a short meeting (5 min) with 3 people
- Standard test: Notes from a regular meeting (60 min) with 10 people
- Maximum test: Notes from a long workshop with mixed English/Japanese
```

**Expected result**: Quantitative and qualitative success criteria and test cases are defined.

---

## ⚠️ Common Issues and Solutions

Use AskQuestion to select the issue, then follow the guidance.

**AskQuestion configuration:**
```json
{
  "title": "Select the issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "I don't understand the category classification"},
      {"id": "trouble_2", "label": "I can't think of trigger phrases"},
      {"id": "trouble_3", "label": "The difference from existing skills is unclear"},
      {"id": "trouble_4", "label": "The success criteria are too abstract"}
    ]
  }]
}
```

### Issue 1: I don't understand the category classification
**Cause**: The skill spans multiple categories
**Solution prompt**:
```text
What is the primary purpose of this skill? Choose one category based on the most important function.
If there are elements of multiple categories, pick one main category and note the others as sub-categories.
```

### Issue 2: I can't think of trigger phrases
**Cause**: The user's use scenarios are unclear
**Solution prompt**:
```text
Imagine 5 scenarios where you would want to use this skill.
The first thing the user would say to the AI in each scenario is a trigger phrase.
```

### Issue 3: The difference from existing skills is unclear
**Cause**: The scope of feature overlap is ambiguous
**Solution prompt**:
```text
Read the SKILL.md for existing skills (check-inbox, slack-search, document-processor)
and compare their "Purpose" and "Output format".
```

### Issue 4: The success criteria are too abstract
**Cause**: No specific numerical targets
**Solution prompt**:
```text
If you were to score a "good meeting notes" out of 10 points, how would you allocate points to each item?
That point allocation becomes the priority of your success criteria.
```

---

## ✅ Checkpoint
- [ ] Understood the 3 skill categories (Document Creation / Workflow Automation / MCP Enhancement)
- [ ] Understood the 3 stages of Progressive Disclosure
- [ ] Created the use-case specification for the meeting-notes skill
- [ ] Defined trigger phrases (correct and incorrect)
- [ ] Set quantitative and qualitative success criteria
- [ ] Defined 3 types of test cases


---

## 📋 Deliverable Preview

### Expected Output
```text
📁 skills/{skill_name}/
├── SKILL.md  (skill definition)
├── scripts/    (execution scripts)
└── tests/      (test files)
```

### Verification Commands
```bash
# Check skill directory structure
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# Check the beginning of SKILL.md
head -30 skills/{skill_name}/SKILL.md
```

---

## ✅ Completion Check
Paste the following into Cursor's chat to verify completion:

```text
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail determination with any missing items listed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin a new section.

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-7-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-7-2
- finish → End

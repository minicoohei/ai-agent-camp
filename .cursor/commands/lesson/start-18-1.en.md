---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: []
level: "intermediate"
tags: ["pm", "interview", "customer-needs"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-1: Customer Interview & Needs Collection

## 📍 What You'll Do

**Lesson 18-1: Customer Interview & Needs Collection** — Welcome!

| Item | Details |
|------|------|
| Goal | AI plays the customer role for an interview simulation. Define personas and extract needs |
| Duration | ~25 min |
| Skills Used | pm-toolkit skill, interactive dialogue flow with choices |
| Prerequisites | ai-agent-camp is open |
| Lesson Page | [Module 18: PM & System Requirements Definition](https://ai-agent.camp/en/course/module-18) for parallel reference |

**Session flow:**
1. Review the TaskFlow project overview
2. Customer interview simulation with AI
3. Structure the interview results (personas, needs, pain points)
4. Generate and review customer-needs.md

By the end of this session, the TaskFlow customer needs analysis document will be completed.

> **💡 Tip**: If the AI response stops midway, type "continue" or "keep going" to resume. Responses may pause due to tool processing, but this is not a malfunction.

---

## 🎯 Readiness Check

Let's first verify that preparations are in order.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
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

## 🚀 Step 1: Introduction to the TaskFlow Project

First, let's review the overview of "TaskFlow," which we will build throughout this module.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: TaskFlow Project Overview",
  "questions": [{
    "id": "taskflow_intro",
    "prompt": "Let's learn about TaskFlow. Where would you like to start?",
    "options": [
      {"id": "overview", "label": "Tell me about TaskFlow"},
      {"id": "skip", "label": "I already know the overview, proceed to the interview"},
      {"id": "context", "label": "I want to know the overall flow of this module"}
    ]
  }]
}
```

**What is TaskFlow:**
```text
TaskFlow is a task management web application for small and medium businesses.

[Concept]
- See at a glance what everyone on the team needs to do today
- AI suggests priorities and prevents tasks from being overlooked
- Simple, yet equipped with features needed by growing companies

[Target Users]
- Companies with 10 to 100 employees
- Currently managing tasks with Excel/spreadsheets
- Find existing tools (Trello, Asana, etc.) too feature-rich to use effectively

In this module, you will experience TaskFlow's entire lifecycle:
Planning → Design → Implementation → Testing → Operations
across all 20 lessons.
```

**Expected result**: You will understand the TaskFlow overview.

---

## 🚀 Step 2: Preparing for the Customer Interview

AI will play the customer role for an interview simulation. First, select the interview target.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Select Interview Target",
  "questions": [
    {
      "id": "persona_type",
      "prompt": "Select the customer type to interview (AI will play the role)",
      "options": [
        {"id": "pm", "label": "Project Manager (age 35, IT company)"},
        {"id": "sales_mgr", "label": "Sales Director (age 42, manufacturing)"},
        {"id": "startup_ceo", "label": "Startup CEO (age 29, SaaS company)"},
        {"id": "hr", "label": "HR Staff (age 31, consulting firm)"}
      ]
    },
    {
      "id": "interview_style",
      "prompt": "Select the interview format",
      "options": [
        {"id": "structured", "label": "Structured interview (question list prepared)"},
        {"id": "semi", "label": "Semi-structured (topics decided, free-form discussion)"},
        {"id": "guided", "label": "Guided (AI suggests questions for you)"}
      ]
    }
  ]
}
```

**After selection**: The simulation will start with the chosen persona and interview format.

---

## 🚀 Step 3: Running the Interview Simulation

AI will respond as the selected customer. Ask questions on the following themes.

**Interview guide:**
```text
Interview the customer (AI) on the following themes:

1. [Current Situation] What is your current task management method? What tools do you use?
2. [Challenges] What is your biggest problem? Can you share a specific episode?
3. [Ideal State] What would make you happy? What is the ideal state?
4. [Priorities] If you could name the top 3 things you want improved?
5. [Constraints] What is your budget range, implementation timeline, and must-have requirements?

AI will give realistic answers as the selected persona.
Have 5 to 10 rounds of back-and-forth conversation.
```

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Interview Progress",
  "questions": [{
    "id": "interview_status",
    "prompt": "How is the interview going?",
    "options": [
      {"id": "continue", "label": "I still have questions, continue"},
      {"id": "enough", "label": "I've gathered enough, proceed to organize"},
      {"id": "help", "label": "I don't know what to ask"},
      {"id": "restart", "label": "Start over with a different persona"}
    ]
  }]
}
```

(continue → Continue the interview)
(enough → Proceed to Step 4)
(help → Show example questions)
(restart → Go back to Step 2)

**Expected result**: 5 to 10 rounds of interview will be completed.

---

## 🚀 Step 4: Structuring the Interview Results

Analyze the interview content and compile it into a document.

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: How to Organize Results",
  "questions": [{
    "id": "output_format",
    "prompt": "Select the output format",
    "options": [
      {"id": "full", "label": "Full analysis (Persona + Needs + Pain Points + Opportunities)"},
      {"id": "persona_focus", "label": "Focus on persona definition"},
      {"id": "needs_focus", "label": "Focus on needs list"},
      {"id": "auto", "label": "Let AI decide"}
    ]
  }]
}
```

**Document to generate:**
```text
Generate output/pm/customer-needs.md with the following content:

# Customer Needs Analysis: TaskFlow

## 1. Interview Overview
- Target: {Persona information}
- Date: {Today's date}
- Format: {Selected format}

## 2. Persona Definition
### Primary Persona
- Name (alias):
- Age:
- Job title:
- Company size:
- IT literacy:
- Current challenges:

## 3. Discovered Needs (by priority)
| # | Need | Type | Priority | Evidence (quote) |
|---|------|------|----------|-----------------|

## 4. Pain Points
1.
2.
3.

## 5. Opportunities
-

## 6. Implications for Next Steps
- Points to reflect in the requirements document
- Topics to explore deeper in the PRD

mkdir -p output/pm && save the file to output/pm/customer-needs.md
```

**Expected result**: `output/pm/customer-needs.md` will be generated.

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
      {"id": "trouble_1", "label": "AI's customer role gives unnatural responses"},
      {"id": "trouble_2", "label": "I don't know what to ask in the interview"},
      {"id": "trouble_3", "label": "I don't know how to organize the needs"},
      {"id": "trouble_4", "label": "The output file is not generated"}
    ]
  }]
}
```

### Issue 1: AI's customer role is unnatural
**Solution**: Instruct "Please answer more realistically, including specific episodes." You can also add specific constraints like "Budget is up to 10,000 yen per month."

### Issue 2: I don't know what to ask
**Solution**: Follow the interview guide in Step 3 (5 themes). Asking 2 questions per theme is sufficient.

### Issue 3: I don't know how to organize needs
**Solution**: Instruct the AI "Based on the interview content, organize the needs by priority" and it will be automatically organized.

### Issue 4: Output file is not generated
**Solution**: Check if the `output/pm/` directory exists. If not, create it with `mkdir -p output/pm`.

---

## ✅ Checkpoint
- [ ] Understood the TaskFlow project overview
- [ ] Conducted 5 or more rounds of customer interview with AI
- [ ] At least 1 persona is defined
- [ ] At least 3 needs are extracted
- [ ] Pain points are clearly identified
- [ ] `output/pm/customer-needs.md` is generated


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── stakeholder-map.md  (Stakeholder Map)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/stakeholder-map.md

# Check the beginning (first 30 lines)
head -30 output/pm/stakeholder-map.md
```

> 💡 Full text: Run `cat output/pm/stakeholder-map.md` to display the full text

---

## ✅ Completion Check
Enter the following in the Codex chat to check the completion status:

```text
Check the content of output/pm/customer-needs.md and verify that the persona definition,
needs list, and pain points are all filled in.
```

**Expected result**: The completeness of the document will be verified.

---

## ➡️ Next Steps

Lesson 18-1 is now complete. Next, you will create the requirements document based on the interview results.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select how to proceed",
    "options": [
      {"id": "next_auto", "label": "Start next lesson (Creating Requirements Document)"},
      {"id": "next_window", "label": "Start /start-18-2 in a new window"},
      {"id": "review", "label": "Review customer needs again"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

- next_auto → Run /start-18-2
- next_window → Open /start-18-2 in a new window
- review → Re-display customer-needs.md
- finish → End

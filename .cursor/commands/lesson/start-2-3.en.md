---
description: "When the user says /start-2-3 — Module 2 Lesson 2-3: Diagrams for Presentation Materials"
chapter: "courses/aiagent/lesson03-core/module02-diagram"
prerequisites: ["start-2-1"]
duration: "~30 min"
level: "intermediate"
tags: ["diagram", "presentation", "architecture"]
---

# 🎓 Lesson 2-3: Diagrams for Presentation Materials

## 📍 What You'll Do

Welcome to **Lesson 2-3: Diagrams for Presentation Materials**!

| Item | Details |
|------|---------|
| Goal | Create system architecture diagrams, sequence diagrams, and other diagrams for presentations and technical documentation |
| Duration | ~30 min |
| Skills Used | diagram-generator (Gemini image generation based) |
| Prerequisites | Lesson 2-1 completed, Gemini API key configured |
| Course Page | Refer to [Module 2: Diagrams & Flows](https://ai-agent.camp/en/course/module-2) in parallel |

**Session flow:**
1. Understand the types of diagrams needed for presentations
2. Create a system architecture diagram
3. Try sequence diagrams and other chart types

By the end of this session, diagrams usable in proposal materials will be saved in outputs.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-Session Check",
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
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Understand Diagram Types for Presentations

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Understand Diagram Types for Presentations",
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

**After selection (example)**:
Input:
```
Explain the types of diagrams used in business presentations and their respective use cases.
Cover overview diagrams, flow diagrams, comparison charts, impact charts, and roadmaps with specific usage guidelines.
```

**Expected result**: Five types of presentation diagrams are explained:
1. Overview diagrams (grasping the big picture)
2. Flow diagrams (explaining processes)
3. Comparison charts (evaluating options)
4. Impact charts (visualizing results)
5. Roadmaps (future planning)

---

## 🚀 Step 2: Create a System Architecture Diagram

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Create a System Architecture Diagram",
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

**After selection (example)**:
Input:
```
Use diagram-generator to create a system architecture diagram for a SaaS platform:

Components:
[Client Companies] → [Web App] → [API Gateway]
  ↓
[Microservices]
  - Authentication Service
  - Data Management Service
  - Analytics Service
  ↓
[Database] + [External Integrations] (Slack, Gmail)

Use a professional design suitable for technical documentation.
Output: ~/ai-agent-camp/output/system-architecture.png
```

**Expected result**: A professional diagram with hierarchically organized system architecture is generated.

---

## 🚀 Step 3: Create an Implementation Roadmap

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Create an Implementation Roadmap",
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

**After selection (example)**:
Input:
```
Create a roadmap for a new system implementation:

Month 1: Contract signing & kickoff
Month 2: Requirements definition & current state analysis
Month 3: Data migration & environment setup
Month 4: Test operation & training
Month 5: Production release & parallel operation
Month 6: Impact measurement & improvements

Use a timeline format showing milestones for each phase.
Output: ~/ai-agent-camp/output/roadmap.png
```

**Expected result**: A project plan visualized along a timeline is generated.

---

## 🚀 Step 4: Create a Competitor Comparison Table

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Create a Competitor Comparison Table",
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

**After selection (example)**:
Input:
```
Create a competitor comparison table in infographic format:

[Our Service]
- Price: 5,000 yen/month ◎
- Features: 15 features ◎
- Support: 24/7 support ◎

[Competitor A]
- Price: 8,000 yen/month △
- Features: 10 features ○
- Support: Weekdays only △

[Competitor B]
- Price: 6,000 yen/month ○
- Features: 8 features △
- Support: Email only ×

Design it so our competitive advantage is immediately clear.
Output: ~/ai-agent-camp/output/comparison.png
```

**Expected result**: A visually clear comparison of 3 companies is generated.

---

## 🚀 Step 5: Practice Exercise - Business System Renewal Proposal

Create a practical set of diagrams for proposal materials using the following prompts:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Practice Exercise - Business System Renewal Proposal",
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

**After selection (example)**:
Input:
```
Create the following 4 diagrams for a business system renewal proposal:

1. Current system issues diagram
   - Too much manual work (30% efficiency)
   - Data scattered across 3 systems
   - Frequent errors (20/month)
   Output: ~/ai-agent-camp/output/proposal-issues.png

2. New system architecture diagram
   - Unified database
   - Automated workflows
   - Real-time dashboard
   Output: ~/ai-agent-camp/output/proposal-new-system.png

3. Migration steps (6-month plan)
   Output: ~/ai-agent-camp/output/proposal-migration.png

4. Projected implementation benefits
   - Efficiency: 30% → 80%
   - Errors: 20/month → 2/month
   - Cost: 3 million yen annual savings
   Output: ~/ai-agent-camp/output/proposal-benefits.png
```

**Expected result**: A set of 4 diagrams aligned with the proposal narrative is generated.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select Your Issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "System architecture diagram is too complex"},
      {"id": "trouble_2", "label": "Roadmap timeline is unclear"},
      {"id": "trouble_3", "label": "Comparison table doesn't convey our advantage"},
      {"id": "trouble_4", "label": "Diagram set lacks consistency"}
    ]
  }]
}
```


### Issue 1: "System architecture diagram is too complex"
**Cause**: Everything packed into one diagram
**Solution prompt**:
```
Split the system architecture into 3 diagrams:
1. Overview level (big picture, main components only)
2. Detail level (internal structure of each service)
3. Data flow (focused on data movement)
```

### Issue 2: "Roadmap timeline is unclear"
**Cause**: Timeline representation is vague
**Solution prompt**:
```
Add the following to the roadmap:
- Clear date or period labels
- Milestones indicating start/end of each phase
- Use Gantt chart format if there are overlapping tasks
```

### Issue 3: "Comparison table doesn't convey our advantage"
**Cause**: Insufficient visual emphasis
**Solution prompt**:
```
To highlight our competitive advantage:
- Fill our column with a prominent color (blue or green)
- Add "Recommended" or "No.1" badges to superior items
- Display numbers that outperform competitors in larger font
```

### Issue 4: "Diagram set lacks consistency"
**Cause**: Each diagram created independently
**Solution prompt**:
```
Unify the following across all 4 diagrams:
- Color palette: Blue (#0066CC) as base
- Font: Sans-serif, bold for headings
- Layout: Title at top-left, page number at bottom-right
- Place logo or brand elements
```

---

## ✅ Checkpoint
- [ ] Understood the types of diagrams needed for presentations
- [ ] Created a system architecture diagram
- [ ] Created an implementation roadmap
- [ ] Created a competitor comparison table
- [ ] Completed the practice exercise (proposal diagram set)


---

## 📋 Output Preview

### Expected Output
```
📁 output/diagrams/
├── flow-{theme-name}.png
└── (variations)
```
> Format: PNG | Size: Auto-configured

### Verification Commands
```bash
# File listing
ls -la output/diagrams/

# Open images (macOS: open / Linux: xdg-open)
open output/diagrams/
```

> 💡 **Claude Code**: Specify the file path with the Read tool to preview images in chat
> 💡 **Cursor**: Click on the image in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose your next action",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in a new window (/start-3-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-3-1
- finish → End

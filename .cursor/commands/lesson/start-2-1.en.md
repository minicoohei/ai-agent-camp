---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module02-diagram"
duration: "~25 min"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["diagram", "flowchart", "gemini"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 2-1: Flowchart Generation

## 📍 What You'll Do

Welcome to **Lesson 2-1: Flowchart Generation**!

| Item | Details |
|------|---------|
| Goal | Create business flow diagrams such as expense approval using the diagram-generator skill |
| Duration | ~25 min |
| Skills Used | diagram-generator (Gemini Image Generation API) |
| Prerequisites | Gemini API key configured, Python environment set up |
| Course Page | Refer to [Module 2: Diagrams & Flows](https://ai-agent.camp/en/course/module-2) in parallel |

**Session flow:**
1. Understand basic flowchart elements
2. Create a simple flowchart
3. Try an advanced flowchart

By the end of this session, images illustrating business flows will be saved in outputs.

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

## 🚀 Step 1: Understand Basic Flowchart Elements

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Understand Basic Flowchart Elements",
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
Explain the basic shapes used in flowcharts and their meanings.
Cover start/end, process, decision, data, and arrows.
```

**Expected result**: Basic flowchart elements are explained:
- Start/End: Oval
- Process: Rectangle
- Decision: Diamond
- Data: Parallelogram
- Arrows: Process flow

---

## 🚀 Step 2: Create a Simple Flowchart

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Create a Simple Flowchart",
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
Use diagram-generator to create a flowchart for an expense approval process:

1. Applicant submits expense claim
2. Manager reviews
3. Approve or reject
4. If approved, accounting department processes
5. If rejected, return to applicant

Output: ~/ai-agent-camp/output/flow-expense.png
```

**Expected result**: An expense approval flow diagram with decision branches is generated.

---

## 🚀 Step 3: Create a Complex Flow with Conditional Branches

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Create a Complex Flow with Conditional Branches",
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
Create a flowchart for a recruitment screening process:

Application received → Document screening → Pass?
  → Yes: First interview → Pass?
    → Yes: Second interview → Pass?
      → Yes: Offer letter
      → No: Rejection notice
    → No: Rejection notice
  → No: Rejection notice

Make the decision branches clearly visible.
Output: ~/ai-agent-camp/output/flow-recruitment.png
```

**Expected result**: A recruitment flow with multiple decision branches is visualized.

---

## 🚀 Step 4: Practice Exercise - Product Ordering Process

Create a practical flowchart using the following prompts:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Practice Exercise - Product Ordering Process",
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
Create a flowchart for a product ordering process:

Inventory check → Low stock?
  → Yes: Create purchase order → Request approval → Approved?
    → Yes: Execute order → Wait for delivery → Confirm delivery → Inspection → Process payment
    → No: Revise purchase order (return to order creation)
  → No: No replenishment needed (end)

Output: ~/ai-agent-camp/output/flow-order.png
```

**Expected result**: An ordering process diagram including loop processing is generated.

---

## 🚀 Step 5: Practice Exercise - Bug Fix Workflow

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Practice Exercise - Bug Fix Workflow",
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
Create a flowchart for a software bug fix workflow:

Bug report → Triage → Priority assessment
  → High priority: Assign to immediate response team
  → Medium priority: Add to next sprint
  → Low priority: Add to backlog

Then, common flow:
Fix → Code review → Approved?
  → Yes: Test → Pass?
    → Yes: Release
    → No: Return to fix
  → No: Return to fix

Output: ~/ai-agent-camp/output/flow-bugfix.png
```

**Expected result**: A workflow diagram with multiple branches and return loops is generated.

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
      {"id": "trouble_1", "label": "Flow is too complex to read"},
      {"id": "trouble_2", "label": "Conditional branches are unclear"},
      {"id": "trouble_3", "label": "Arrow directions are confusing"},
      {"id": "trouble_4", "label": "Diagram is not generated"}
    ]
  }]
}
```


### Issue 1: "Flow is too complex to read"
**Cause**: Too much information packed into one diagram
**Solution prompt**:
```
Split this flow into sub-processes.
Separate it into a main flow and detailed flows, creating each as a separate diagram.
```

### Issue 2: "Conditional branches are unclear"
**Cause**: Decision conditions are expressed vaguely
**Solution prompt**:
```
Clarify the decision branch conditions:
- "Approved?" → "Amount under 100,000 yen?"
- "Pass?" → "Interview rating A or above?"
Include specific criteria in the diagram.
```

### Issue 3: "Arrow directions are confusing"
**Cause**: Flow is complex and hard to follow
**Solution prompt**:
```
Unify the flow direction from left to right, top to bottom.
Represent return loops with dashed lines.
```

### Issue 4: "Diagram is not generated"
**Cause**: Issue with diagram-generator execution environment
**Solution prompt**:
```
Run a health check on diagram-generator.
Verify that required packages are installed,
and display any error messages.
```

---

## ✅ Checkpoint
- [ ] Understood basic flowchart elements (start/end, process, decision, arrows)
- [ ] Created a simple linear flow
- [ ] Created a flow with conditional branches
- [ ] Completed the practice exercise (product ordering)
- [ ] Completed the practice exercise (bug fix workflow)


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
      {"id": "next_window", "label": "Start in a new window (/start-2-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-2-2
- finish → End

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1", "start-3-2", "start-3-3", "start-3-4", "start-3-5"]
duration: "~40 min"
level: "intermediate"
tags: ["screenshot", "capstone", "manual"]
---

# 🎓 Lesson 3-6: Screenshot Analysis Summary Exercise

## 📍 What You'll Do

**Lesson 3-6: Screenshot Analysis Summary Exercise** !

| Item | Details |
|------|---------|
| Goal | Integrate all Module 3 skills and complete the operation manual generation project |
| Duration | ~40 min |
| Skills Used | Comprehensive use of screenshot-analyzer, tutorial-generator, and screenshot-annotator |
| Prerequisites | Lessons 3-1 through 3-5 completed, Gemini API key configured |
| Course Page | [Module 3: Screenshot Analysis](https://ai-agent.camp/en/course/module-3) in parallel |

**Session flow:**
1. Select project and organize requirements
2. Execute the analysis, tutorial, and annotation workflow
3. Review finished product and reflect on Module 3

By the end of this session, a practical operation manual will be completed and Module 3 will be finished.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Select an Analysis Theme

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Select a Project",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Choose one from the following exercise projects:

[Beginner] Web App Manual (30-40 min)
- Target: Web app with about 5 features
- Deliverables: User manual in HTML format

[Intermediate] Error Diagnosis Report (40-50 min)
- Target: Multiple error screens
- Deliverables: Prioritized diagnosis report + resolution procedure guide

[Advanced] Multi-platform Support (60-90 min)
- Target: PC version + mobile version
- Deliverables: Complete manual supporting both platforms

Please choose which project to work on.
Once selected, detailed steps for that project will be provided.
```

**Expected result**: Detailed implementation steps for the selected project are presented.

---

## 🚀 Step 2: Multi-Screenshot Comprehensive Analysis

Here is an example of the beginner project:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: [Beginner] Create a Web App Manual",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
We will create a Gmail user manual.

Target audience: Beginners (seniors aged 60+)
Key features:
1. Login
2. Receiving and reading email
3. Composing and sending email
4. Label management
5. Email search

Deliverables requirements:
- Manual HTML: Cover all 5+ features
- Screenshots: 15+ images
- Troubleshooting: 3+ items

Assuming Gmail screenshots have been placed as official materials in
courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/,
begin creating the manual.
```

**Expected result**: A polished Gmail manual for seniors is created.

---

## 🚀 Step 3: Create Analysis Report and Presentation Materials

Here is an example of the intermediate project:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: [Intermediate] Create an Error Diagnosis Report",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Create a diagnosis report from multiple system error screens.

Input: All error images in courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/
Output: output/error-report/

Report content:
1. Error list table (priority, cause, solution)
2. Detailed analysis of each error
3. Response flowchart
4. Prevention measure proposals

Output format:
- HTML format diagnosis report
- Color-coded error images by priority
- Response checklist (Markdown)
```

**Expected result**: A systematic error diagnosis report is created.

---

## 🚀 Step 4: Review Deliverables and Export

Let's review the created deliverables:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Review Deliverables and Export",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Check the quality of the created manual/report.

Checklist:
- [ ] All images display correctly
- [ ] No character encoding issues
- [ ] Links function correctly
- [ ] Readable on mobile devices
- [ ] Language understandable by beginners

If there are issues, fix them and save the final version to output/final/.
```

**Expected result**: The quality check is complete and the final version is saved.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "Cannot finish within the time limit"},
      {"id": "trouble_2", "label": "Quality is insufficient"},
      {"id": "trouble_3", "label": "File structure is disorganized"}
    ]
  }]
}
```


- Cannot finish within the time limit
- Quality is insufficient
- File structure is disorganized

### Issue 1: "Cannot finish within the time limit"
**Cause**: Scope is too large
**Solution prompt**:
```
Check the current progress status.
Narrow down to what can be completed in the remaining time
and complete only the high-priority parts.
```

### Issue 2: "Quality is insufficient"
**Cause**: Insufficient review
**Solution prompt**:
```
To improve the manual quality,
review from the following perspectives:
- Clarity
- Accuracy
- Consistency
- Design

If there are areas for improvement, provide specific suggestions.
```

### Issue 3: "File structure is disorganized"
**Cause**: Output destination is not organized
**Solution prompt**:
```
Organize the project file structure.

Recommended structure:
project-output/
├── README.md
├── screenshots/
├── tutorials/
├── manual/
├── annotations/
└── scripts/

Move files to match this structure.
```

---

## ✅ Checkpoint

### Module 3 Completion Checklist

### Technical Skills
- [ ] Used screenshot-analyzer 3 or more times
- [ ] Used tutorial-generator 3 or more times
- [ ] Used screenshot-annotator 5 or more times
- [ ] Implemented automation with custom scripts
- [ ] Created an integrated HTML document

### Deliverables
- [ ] Completed a practical user manual
- [ ] Has an integrated HTML document
- [ ] Created annotated screenshots
- [ ] Based on actual use cases

---

## 🎉 Module 3 Complete！

Congratulations! You have mastered the following skills:
- Automatically diagnose error causes from screenshots
- Generate step-by-step tutorials
- Illustrate UIs using annotations
- Create practical user manuals
- Automate complex processes


---

## 📋 Output Preview

### Expected Output
```
📁 output/screenshots/
├── analyzed-{target-name}.png
└── (variations)
```
> Format: PNG | Size: Auto-configured

### Verification Commands
```bash
# File list
ls -la output/screenshots/

# Open image (macOS: open / Linux: xdg-open)
open output/screenshots/
```

> 💡 **Claude Code**: Specify the file path with the Read tool to preview images in chat
> 💡 **Cursor**: Click on the image in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-4-1)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-4-1
- finish → End

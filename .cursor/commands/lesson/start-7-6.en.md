---
description: "When the user says /start-7-6 — Module 7 Lesson 7-6: Creating Commands for Your Own Workflow"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "~35 min"
prerequisites: ["start-7-5"]
level: "intermediate"
tags: ["skill", "command", "workflow", "customization"]
---

# 🎓 Lesson 7-6: Creating Commands for Your Own Workflow

## 📍 What You'll Do

Welcome to **Lesson 7-6: Creating Commands for Your Own Workflow**!

| Item | Details |
|------|------|
| Goal | Create 3 custom Commands tailored to your own work workflows |
| Duration | ~35 min |
| Skills used | Markdown (YAML frontmatter), Cursor Commands |
| Prerequisites | Lesson 7-5 completed (understanding existing Skill/Command structure) |

**Session flow:**
1. Identify daily work workflows (using AskUserQuestion)
2. Create Command 1: Daily/Weekly report template generator
3. Create Command 2: Meeting preparation checklist
4. Create Command 3: Code review guide
5. Verify operation (run with /command-name)

By the end of this session, you will have 3 custom Commands directly linked to your daily work tasks.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. Responses may stop midway depending on the tool, but this is not a malfunction.

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
(view_html → Show course page URL https://ai-agent.camp/en/course/module-7)
(different_lesson → Display module list)

---

## 🚀 Step 1: Identify Daily Work Workflows

First, let's organize your daily tasks and find tasks that can be automated or templatized.

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Workflow Identification",
  "questions": [{
    "id": "workflow_type",
    "prompt": "What is the most repetitive task in your work?",
    "options": [
      {"id": "reporting", "label": "Creating daily/weekly/monthly reports"},
      {"id": "meeting", "label": "Meeting preparation and minutes"},
      {"id": "review", "label": "Code reviews or document reviews"},
      {"id": "planning", "label": "Task planning or sprint planning"},
      {"id": "custom", "label": "Other (I want to type my own)"}
    ]
  }]
}
```

**Guidance after selection:**

Regardless of which task you choose, Commands are built in these 3 steps:

1. **What to do** — Define the task purpose in one line
2. **What steps** — Step-by-step operation procedure
3. **What output** — Expected deliverables

Input:
```
Answer the following questions to organize your work workflows:

1. What is your role/job title? (e.g., Engineer, PM, Designer, Sales)
2. List 3 tasks you repeat daily or weekly
3. Is there anything you "always write in the same format"?
4. Are there any "check items you tend to forget every time"?
5. How much time could you save if this task were automated?

Based on your answers, suggest 3 workflows that should be turned into Commands.
```

**Expected result**: 3 workflows to be converted into Commands are determined.

---

## 🚀 Step 2: Create Command (1) Daily/Weekly Report Template

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Daily/Weekly Report Template Command",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed (create with your own work content)"},
      {"id": "review", "label": "Just review the example (view sample)"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Use the following sample as a reference and create a command tailored to your work.

Input:
```
Create .cursor/commands/utility/daily-report.md with the following content:

---
description: "Generate a daily/weekly report template"
---

# Daily/Weekly Report Template Generator

## How to Use
Running this command generates a daily report template with today's date.

## Daily Report Template

Create a daily report following this template:

### 📅 Daily Report: [Today's Date]

**Author**: [Name]

#### 🎯 Today's Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

#### ✅ Completed Tasks
| Task | Category | Time Spent | Notes |
|------|----------|-----------|-------|
| - | - | - | - |

#### 🔄 In-Progress Tasks
| Task | Progress | Blockers | Expected Completion |
|------|----------|----------|-------------------|
| - | - | - | - |

#### 💡 Learnings & Insights
-

#### ⚠️ Handoff for Tomorrow
-

#### 📊 Work Hours
- Start:
- End:
- Break:

---

## Weekly Report Template

To create a weekly report, instruct "in weekly report mode".

### 📅 Weekly Report: [This Week's Period]

**Author**: [Name]

#### This Week's Highlights (up to 3)
1.
2.
3.

#### KPT Retrospective
- **Keep (things to continue)**:
- **Problem (issues)**:
- **Try (things to try next)**:

#### Next Week's Plan
| Priority | Task | Deadline |
|----------|------|----------|
| High | - | - |
| Medium | - | - |
| Low | - | - |
```

**Expected result**: The `/daily-report` command is created and generates a daily report template when run.

---

## 🚀 Step 3: Create Command (2) Meeting Preparation Checklist

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Meeting Preparation Checklist Command",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed (create with your meeting style)"},
      {"id": "review", "label": "Just review the example (view sample)"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Input:
```
Create .cursor/commands/utility/meeting-prep.md with the following content:

---
description: "Generate a meeting preparation checklist"
---

# Meeting Preparation Checklist

## How to Use
Enter the meeting name to generate a preparation checklist.

## Enter Meeting Information

Answer the following questions:
1. What is the meeting name?
2. Who are the participants? (names and roles)
3. What is the meeting purpose? (decision-making / information sharing / brainstorming / progress report)
4. How long is the meeting?
5. What materials need to be prepared in advance?

## 📋 Meeting Preparation Checklist

### 🔔 3 Days Before the Meeting
- [ ] Draft the agenda
- [ ] Send advance notice/invitations to participants
- [ ] Identify required materials

### 📝 Day Before the Meeting
- [ ] Finalize and share the agenda
- [ ] Prepare and pre-share materials
- [ ] Confirm meeting room/online tool reservation
- [ ] Review previous meeting minutes and action items

### ⏰ Just Before the Meeting (15 min)
- [ ] Test material projection
- [ ] Confirm recording settings
- [ ] Assign a timekeeper
- [ ] Assign a note-taker

### 📊 Agenda Template

| Time | Topic | Owner | Purpose |
|------|-------|-------|---------|
| 0:00-0:05 | Opening / Previous review | Facilitator | Info sharing |
| 0:05-0:20 | Topic 1 | - | - |
| 0:20-0:35 | Topic 2 | - | - |
| 0:35-0:45 | Topic 3 | - | - |
| 0:45-0:55 | Action items review | All | Decision |
| 0:55-1:00 | Closing | Facilitator | Summary |

### 🔄 After the Meeting
- [ ] Create and share meeting minutes (within 24 hours)
- [ ] Finalize action item owners and deadlines
- [ ] Register follow-up tasks
```

**Expected result**: The `/meeting-prep` command is created and generates a preparation checklist appropriate to the meeting type.

---

## 🚀 Step 4: Create Command (3) Code Review Guide

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Code Review Guide Command",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed (create with your review criteria)"},
      {"id": "review", "label": "Just review the example (view sample)"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Input:
```
Create .cursor/commands/utility/code-review.md with the following content:

---
description: "Code review guidelines and checklist"
---

# Code Review Guide

## How to Use
Enter the file name or PR number to review, and review points will be generated.

## 🔍 Review Checklist

### 1. Readability
- [ ] Are variable/function names clear in intent
- [ ] Do comments explain "why" (not "what")
- [ ] Does each function focus on a single responsibility (target: under 20 lines)
- [ ] Is nesting not too deep (within 3 levels)

### 2. Correctness
- [ ] Are edge cases handled (null, empty arrays, boundary values)
- [ ] Is error handling appropriate (try-catch, validation)
- [ ] Are there no type mismatches
- [ ] Do all existing tests pass

### 3. Security
- [ ] Are there no hardcoded secrets (API keys, passwords)
- [ ] Is user input sanitized
- [ ] Are proper access controls configured

### 4. Performance
- [ ] Are there no unnecessary loops or computations
- [ ] Will N+1 problems not occur
- [ ] Is there no risk of memory leaks when processing large data

### 5. Testing
- [ ] Are tests added for new logic
- [ ] Do tests cover edge cases
- [ ] Can tests run independently

## 💬 Review Comment Templates

### Blocker (Must Fix)
```
🚫 [Blocker] XX is YY. Please fix to ZZ.
Reason: ...
```

### Suggestion
```
💡 [Suggestion] Changing XX to YY would improve ZZ.
Reference: ...
```

### Question
```
❓ [Question] What is the intent of doing XX here?
What happens in the YY case?
```

### Praise
```
👏 [Nice!] The XX implementation is excellent. The YY aspect is particularly good.
```
```

**Expected result**: The `/code-review` command is created and can be used as a guideline during reviews.

---

## 🚀 Step 5: Verify Operation and Improve

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Verify Operation and Improve",
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

Input:
```
Verify the operation of the 3 commands you created:

1. Confirm each command file is in the correct location
   - .cursor/commands/utility/daily-report.md
   - .cursor/commands/utility/meeting-prep.md
   - .cursor/commands/utility/code-review.md

2. Validate YAML frontmatter syntax
   - description is set
   - Correctly enclosed by ---

3. Run each command
   - /daily-report → Does the daily report template display?
   - /meeting-prep → Does the checklist display?
   - /code-review → Does the review guide display?

4. Make improvements if needed
   - Remove/add items that don't fit your work
   - Adjust wording to be generic enough for team sharing
```

**Expected result**: All 3 commands work correctly and are ready for practical use.

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
      {"id": "trouble_1", "label": "Command can't be invoked with /command-name"},
      {"id": "trouble_2", "label": "Template content doesn't match my work"},
      {"id": "trouble_3", "label": "YAML frontmatter error occurs"},
      {"id": "trouble_4", "label": "I want to share commands with my team"}
    ]
  }]
}
```

### Issue 1: Command can't be invoked with /command-name
**Cause**: File placement is incorrect
**Solution prompt**:
```
Check the following:
1. Is the file under .cursor/commands/? (subdirectories are OK)
2. Is the file extension .md?
3. Restart Cursor and check in the Command Palette (Cmd+Shift+P)
```

### Issue 2: Template content doesn't match my work
**Cause**: Samples may not work as-is for everyone
**Solution prompt**:
```
Templates are just a "starting point". Customize with these steps:
1. Remove unnecessary sections
2. Add items specific to your work
3. Replace with terminology used in your team
4. Use for one week and adjust based on experience
```

### Issue 3: YAML frontmatter error occurs
**Cause**: YAML syntax issue
**Solution prompt**:
```
Common causes:
- description value contains a colon (:) → Wrap in double quotes
- Indentation uses tabs → Change to 2 spaces
- Extra whitespace before/after --- → Remove it
```

### Issue 4: I want to share commands with my team
**Cause**: Don't know the sharing method
**Solution prompt**:
```
There are 2 methods:
1. Commit .cursor/commands/ to the Git repository (available for everyone who clones)
2. Place the same files in .claude/commands/ as well (for Claude Code users)
```

---

## ✅ Checkpoint
- [ ] Identified 3+ daily work workflows
- [ ] Created daily-report.md (daily/weekly report template)
- [ ] Created meeting-prep.md (meeting preparation checklist)
- [ ] Created code-review.md (code review guide)
- [ ] Verified operation of all 3 commands
- [ ] Customized to fit your work


---

## 📋 Deliverable Preview

### Expected Output
```
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
Paste the following into chat to verify completion:

```
# Completion check: Verify that the following command files have been created:
# 1. .cursor/commands/utility/daily-report.md
# 2. .cursor/commands/utility/meeting-prep.md
# 3. .cursor/commands/utility/code-review.md
# Also check that YAML frontmatter (description) is set in each file.
```

**Expected result**: All 3 command files are correctly created.

---

## 🎉 Next Steps

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
      {"id": "next_window", "label": "Start in new window (/start-7-7)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-7-7
- finish → End

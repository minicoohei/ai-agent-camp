---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-7-6", "start-7-7"]
level: "intermediate"
tags: ["skill", "command", "testing", "debugging", "iteration"]
---

# 🎓 Lesson 7-8: Testing, Debugging, and Iteration

## 📍 What You'll Do

Welcome to **Lesson 7-8: Testing, Debugging, and Iteration**!

| Item | Details |
|------|------|
| Goal | Verify and improve the quality of the Skills/Commands you created |
| Duration | ~30 min |
| Skills used | Testing, Debugging, Iteration |
| Prerequisites | Lesson 7-6 (Command creation) and Lesson 7-7 (Skill creation) completed |

**Session flow:**
1. Command operation tests (edge cases, error handling)
2. Skill operation tests (normal cases, error cases)
3. Self-review (using checklist)
4. Improvement iteration (feedback → fix → re-test)
5. Documentation maintenance (add usage guide)

By the end of this session, the Skills/Commands you created will be polished to "quality ready to hand off to others".

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
(check_prereq → Verify deliverables created in 7-6 and 7-7)
(view_html → Show course page URL https://ai-agent.camp/en/course/module-7)
(different_lesson → Display module list)

---

## 🚀 Step 1: Command Operation Tests

Test the 3 Commands created in Lesson 7-6.

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Command Operation Tests",
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

Test each Command from these 3 perspectives.

Input:
```
Test the 3 Commands created in 7-6 from the following perspectives:

### Test 1: Normal Case Tests
Run each command with /command-name and verify expected output:

- /daily-report → Does the daily report template display correctly?
  - Is the date correct?
  - Is the table format intact?
  - Do checkboxes function?

- /meeting-prep → Does the meeting preparation checklist display correctly?
  - Are all check items displayed without omissions?
  - Is the agenda template table intact?

- /code-review → Does the review guide display correctly?
  - Is categorization appropriate?
  - Can comment templates be used with copy-paste?

### Test 2: Edge Case Tests
- If the command description is too long, does the display break?
- Are all Markdown notations (code blocks, tables, checkboxes) rendered correctly?
- Does mixed Japanese and English display without issues?

### Test 3: Usability Tests
- Can a first-time user understand how to use it?
- Is there unnecessary information (information overload)?
- Is there missing information?

Report test results in the following format:

| Command | Normal | Edge Cases | Usability | Overall |
|---------|--------|-----------|-----------|---------|
| daily-report | OK/NG | OK/NG | OK/NG | PASS/FAIL |
| meeting-prep | OK/NG | OK/NG | OK/NG | PASS/FAIL |
| code-review | OK/NG | OK/NG | OK/NG | PASS/FAIL |
```

**Expected result**: Test result reports for all 3 Commands are complete and issues are identified.

---

## 🚀 Step 2: Skill Operation Tests

Test the Skill created in Lesson 7-7.

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Skill Operation Tests",
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
Verify the skill created in 7-7 with the following test cases:

### Test 1: Test Mode
python skills/[skill-name]/scripts/main.py --test

Expected: Test succeeds and sample output is displayed

### Test 2: Normal Case (Minimal Input)
python skills/[skill-name]/scripts/main.py --input [minimal test data]

Expected: Correct output is generated

### Test 3: Normal Case (Full Options)
python skills/[skill-name]/scripts/main.py --input [test data] --output output.md --format markdown --verbose

Expected: Output to file in specified format

### Test 4: Error Case (Non-existent File)
python skills/[skill-name]/scripts/main.py --input nonexistent_file.txt

Expected: Appropriate error message displayed and exits abnormally

### Test 5: Error Case (Invalid Arguments)
python skills/[skill-name]/scripts/main.py

Expected: Usage message is displayed

### Test 6: Error Case (Empty File)
touch /tmp/empty_test.txt
python skills/[skill-name]/scripts/main.py --input /tmp/empty_test.txt

Expected: Appropriate handling of empty file (warning or empty result)

Report test results in the following format:

| Test Case | Expected Result | Actual Result | Verdict |
|-----------|----------------|--------------|---------|
| Test mode | Test succeeds | - | PASS/FAIL |
| Normal (minimal) | Correct output | - | PASS/FAIL |
| Normal (full) | File output | - | PASS/FAIL |
| Error (not found) | Error message | - | PASS/FAIL |
| Error (no args) | Usage display | - | PASS/FAIL |
| Error (empty file) | Appropriate handling | - | PASS/FAIL |
```

**Expected result**: Results for 6 test cases are recorded and items needing fixes are clear.

---

## 🚀 Step 3: Self-Review

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Self-Review",
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

Self-evaluate the quality of your Commands/Skills using the following checklist.

Input:
```
Evaluate the deliverables from 7-6/7-7 based on this self-review checklist:

## Command Self-Review (for each command)

### Structure/Format
- [ ] Is YAML frontmatter valid syntax
- [ ] Is description concise and clear (under 50 characters recommended)
- [ ] Are Markdown heading levels appropriate (one H1, structured with H2+)
- [ ] Do code blocks have language specifications (```bash, ```python, etc.)

### Content/Quality
- [ ] Can a first-time user understand "what it does" in 10 seconds
- [ ] Are there no remaining TODO/placeholders in templates
- [ ] Is the language natural and readable
- [ ] Is the information volume appropriate (not too much, not too little)

### Practicality
- [ ] Can it be used daily/weekly in actual work
- [ ] Are there parts ready for immediate copy-paste use
- [ ] Is there room for customization

## Skill Self-Review

### SKILL.md
- [ ] Is metadata (name, description) under 100 words
- [ ] Is body under 5,000 words
- [ ] Do quick start commands work with copy-paste
- [ ] Is the parameter table complete
- [ ] Are output samples included
- [ ] Are there 5+ trigger phrases

### scripts/main.py
- [ ] Does --help display usage
- [ ] Does --test run tests
- [ ] Does it return appropriate messages and exit codes on errors
- [ ] Does it support UTF-8 encoding
- [ ] Are there no remaining unnecessary print statements or debug code

### Overall
- [ ] Does the directory structure follow the standard pattern
- [ ] Can someone else clone and use it immediately

Mark each item as PASS / FAIL / NA, and provide improvement suggestions for FAIL items.
```

**Expected result**: Self-review results are recorded and improvement items are organized by priority.

---

## 🚀 Step 4: Improvement Iteration

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Improvement Iteration",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed (fix issues from Step 3)"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Fix issues found in Steps 1-3. Fix in order of "highest impact first".

Input:
```
Improve based on the test/review results from Steps 1-3:

### Improvement Priority
1. **Critical (fix immediately)**: Doesn't work, errors occur
2. **High (fix in this session)**: Major usability issues
3. **Medium (OK for next time)**: Minor improvements
4. **Low (someday)**: Nice-to-have feature additions

### Improvement Iteration Cycle

For each issue, run through this cycle:

1. **Identify the problem**: What is the issue, reproduction steps
2. **Analyze the cause**: Why is this happening
3. **Apply the fix**: Fix with minimal changes
4. **Re-test**: Verify with the same test case after fix

### Fix Report

| Issue | Priority | Cause | Fix | Re-test Result |
|-------|----------|-------|-----|---------------|
| - | Critical/High/Medium/Low | - | - | PASS/FAIL |

Fix all Critical/High issues before proceeding to the next Step.
```

**Expected result**: All Critical/High issues are fixed and re-tests PASS.

---

## 🚀 Step 5: Documentation Maintenance

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Documentation Maintenance",
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

Finally, maintain documentation so others can use the Commands/Skills you created.

Input:
```
Maintain the following documentation:

### 1. Command Usage Guide

Check that each Command file has a "How to Use" section at the top,
and add if missing:
- What it does (one-line description)
- How to use it (execution method)
- Output example (what results to expect)

### 2. Skill Usage Guide

Check that SKILL.md includes the following, and add if missing:
- Quick start (copy-paste-ready command examples)
- Common use cases (3+ patterns)
- Troubleshooting (common errors and solutions)

### 3. Deliverables List

Create a list of all deliverables created in this module (7-1 through 7-8):

| File | Type | Overview |
|------|------|---------|
| .cursor/commands/utility/daily-report.md | Command | Daily/weekly report template |
| .cursor/commands/utility/meeting-prep.md | Command | Meeting preparation checklist |
| .cursor/commands/utility/code-review.md | Command | Code review guide |
| skills/[skill-name]/SKILL.md | Skill | [Skill description] |
| skills/[skill-name]/scripts/main.py | Script | [Script description] |

### 4. Retrospective

Answer the following questions:
1. What was the most valuable learning from this module?
2. What Command/Skill ideas do you want to create in the future?
3. What would you like to improve?
```

**Expected result**: Documentation is maintained, and the deliverables list and retrospective are complete.

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
      {"id": "trouble_1", "label": "Unexpected error in tests"},
      {"id": "trouble_2", "label": "Same error recurs after fixing"},
      {"id": "trouble_3", "label": "Too many review points, don't know where to start"},
      {"id": "trouble_4", "label": "Don't know how to write documentation"}
    ]
  }]
}
```

### Issue 1: Unexpected error in tests
**Cause**: Test environment differs from script assumptions
**Solution prompt**:
```
Paste the full error message. We'll isolate the cause in this order:
1. What is the Python version? (python3 --version)
2. Are all required packages installed? (uv pip list)
3. Is the file path correct? (verify with ls -la)
4. Are environment variables set? (echo $VARIABLE_NAME)
```

### Issue 2: Same error recurs after fixing
**Cause**: Wrong fix location or cache issue
**Solution prompt**:
```
Try the following:
1. Re-save the file (Cmd+S / Ctrl+S)
2. Delete Python cache: find . -name "__pycache__" -exec rm -rf {} +
3. Verify changes are reflected: cat [file-path] | head -20
4. Try running in a different terminal window
```

### Issue 3: Too many review points, don't know where to start
**Cause**: Falling into perfectionism
**Solution prompt**:
```
Apply the 80% rule:
1. First check only "does it work or not" (Critical)
2. Then check "is it usable" (High)
3. The rest is "nice to have" level (Medium/Low)
Fixing only Critical and High completes this lesson.
```

### Issue 4: Don't know how to write documentation
**Cause**: Haven't seen examples of good documentation
**Solution prompt**:
```
Refer to these existing skill SKILL.md files:
- skills/banner-creator/SKILL.md (simple example)
- skills/data-analyst/SKILL.md (detailed example)

Write documentation with this standard: "Can I understand it when reading it 3 months from now?"
```

---

## ✅ Checkpoint
- [ ] Operation tests for 3 Commands (normal / edge cases / usability) completed
- [ ] Skill operation tests (6 test cases) completed
- [ ] Self-review (Command: 11 items, Skill: 16 items) completed
- [ ] All Critical/High issues are fixed
- [ ] Documentation (usage guide) is maintained
- [ ] Deliverables list is created
- [ ] Retrospective is completed


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
# Completion check: Verify all Module 7 deliverables:
# 1. Do the 3 Commands (daily-report, meeting-prep, code-review) work
# 2. Does the 1 Skill (SKILL.md + scripts/main.py) pass tests
# 3. Is documentation maintained for each deliverable
# 4. Is the test result report created
```

**Expected result**: All Module 7 deliverables meet quality standards.

---

## 🎉 Next Steps

Module 7 "Skill/Commands Creation" is complete with all 8 lessons. Congratulations!

Skills you've acquired:
- Ability to analyze existing Command/Skill structures
- Ability to create Commands tailored to work workflows
- SKILL.md-driven skill development ability
- Practical experience with testing, debugging, and iteration

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_module", "label": "Proceed to Module 8 Data Analysis (/start-8-1)"},
      {"id": "review_all", "label": "Review Module 7 deliverables"},
      {"id": "share", "label": "Learn how to share Commands/Skills with your team"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- next_module → /start-8-1 (Module 8 Data Analysis)
- review_all → Display all Module 7 deliverables
- share → Guide for Git push → team sharing procedure
- finish → End

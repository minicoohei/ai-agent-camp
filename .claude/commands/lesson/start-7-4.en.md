---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-7-3"]
duration: "~20 min"
level: "advanced"
tags: ["agent", "design-patterns", "architecture"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 7-4: 5 Design Patterns

## 📍 What You'll Do

Welcome to **Lesson 7-4: 5 Design Patterns**!

| Item | Details |
|------|------|
| Goal | Learn 5 skill design patterns and apply the Iterative Refinement pattern to the meeting-notes skill |
| Duration | ~20 min |
| Skills used | meeting-notes-summarizer (created and improved in Lessons 7-2, 7-3) |
| Prerequisites | Lesson 7-3 completed (tested and improved skill) |
| Course page | Refer to [Module 7: Skill/Commands](https://ai-agent.camp/en/course/module-7) alongside this lesson |

**Session flow:**
1. Sequential Workflow pattern
2. Multi-MCP Coordination pattern
3. Iterative Refinement pattern
4. Context-aware Tool Selection pattern
5. Domain-specific Intelligence pattern
6. Apply Iterative Refinement to the meeting-notes skill (hands-on exercise)

By the end of this session, you will understand the 5 design patterns and have applied the Iterative Refinement pattern to the meeting-notes skill.

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
(check_prereq → Run prerequisite verification: Confirm Lesson 7-3 is completed and meeting-notes-summarizer exists in `skills/meeting-notes-summarizer/`)
(view_html → Show course page URL https://ai-agent.camp/en/course/module-7)
(different_lesson → Display module list)

---

## 🚀 Step 1: Sequential Workflow Pattern

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Sequential Workflow Pattern",
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

**Concept**: A pattern that executes tasks in a defined order, where the output of each step becomes the input for the next. Because processing is linear and predictable, it's easy to debug and each step can be tested independently.

**Application in the meeting-notes skill:**
Receive text → Extract attendees → Identify agenda → Organize decisions → Extract action items → Markdown output

Input:
```
Design the processing flow when applying the Sequential Workflow pattern to the meeting-notes skill.

Clearly define the input/output of each step, showing how the output of the previous step becomes the input for the next:
1. Receive and preprocess text
2. Extract attendees
3. Identify agenda/topics
4. Organize decisions
5. Extract action items (with owners and deadlines)
6. Generate Markdown meeting notes
```

**Expected result**: A 6-step processing flow is designed with clearly defined input/output for each step.

---

## 🚀 Step 2: Multi-MCP Coordination Pattern

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Multi-MCP Coordination Pattern",
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

**Concept**: A pattern that coordinates multiple tools and skills to accomplish complex tasks that cannot be achieved with a single tool. It's important to leverage each tool's strengths and design data passing and error handling.

**Application in the meeting-notes skill:**
Retrieve meeting logs from a channel via Slack search → Structure with meeting-notes skill → Save to Notion DB

Input:
```
Design an integration of the following 3 skills using the Multi-MCP Coordination pattern:

1. slack-search (Slack Search) → Retrieve meeting logs from a specific channel
2. meeting-notes-summarizer (Meeting Notes Generator) → Convert logs to structured meeting notes
3. notion-db (Notion Integration) → Save meeting notes to a Notion database

Design the data passing method between skills and the fallback handling for errors.
```

**Expected result**: The integration flow of 3 skills is designed, with clear data formats, passing methods, and error fallback logic between skills.

---

## 🚀 Step 3: Iterative Refinement Pattern

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Iterative Refinement Pattern",
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

**Concept**: A pattern that improves quality through a cycle of draft generation → review → improvement → re-review. Rather than aiming for perfection in a single generation, it takes an iterative approach to improve quality.

**Application in the meeting-notes skill:**
Initial draft generation → Self-review (gap check) → Improved version generation → Final confirmation

Input:
```
Design how to incorporate the Iterative Refinement pattern into the meeting-notes skill:

1. Initial draft: Generate meeting notes from input text
2. Self-review: Self-check from these perspectives
   - Are all attendees included?
   - Do action items have owners and deadlines?
   - Are decisions clear?
3. Improved version: Revise meeting notes based on review results
4. Final confirmation: Display the diff between before and after improvement

Show the specific prompt structure for how to describe this mechanism in SKILL.md.
```

**Expected result**: The 4 steps of Iterative Refinement are designed with clear SKILL.md notation and specific prompt structure.

---

## 🚀 Step 4: Context-aware Tool Selection Pattern

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Context-aware Tool Selection Pattern",
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

**Concept**: A pattern that selects different processing paths based on the context of the input. It automatically determines the input type and routes to the optimal handler.

**Application in the meeting-notes skill:**
Auto-detect input format → Route to the appropriate handler

Input:
```
Apply the Context-aware Tool Selection pattern to the meeting-notes skill.

Design branching based on input format:
- Text input → Convert directly to meeting notes
- Audio transcription text → Remove noise → Convert to meeting notes
- Chat log format → Organize by speaker → Convert to meeting notes
- Bullet-point memo → Estimate structure → Convert to meeting notes

Design the determination criteria for each branch and the differences in processing.
```

**Expected result**: Determination criteria for 4 input formats are defined with appropriate preprocessing flows for each format.

---

## 🚀 Step 5: Domain-specific Intelligence Pattern

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Domain-specific Intelligence Pattern",
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

**Concept**: A pattern that embeds domain-specific expertise into skills to achieve accuracy and quality that generic AI cannot. It incorporates meeting-domain knowledge (meeting types, templates, terminology) into the skill.

**Application in the meeting-notes skill:**
Auto-detect meeting type → Select type-specific template → Interpret industry terminology → Recommend follow-up actions

Input:
```
Design how to embed meeting-domain expertise into the meeting-notes skill using the Domain-specific Intelligence pattern:

1. Auto-detect meeting type (regular meeting/brainstorming/review/decision-making meeting)
2. Select an appropriate meeting-notes template for each type
3. Rules for interpreting industry terminology and abbreviations
4. Recommended follow-up action patterns

Show the specific file structure for placing this in the references/ directory of SKILL.md.
```

**Expected result**: Meeting-domain expertise is structured and the placement design in the references/ directory is complete.

---

## 🚀 Step 6: Hands-on Exercise — Applying Iterative Refinement

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 6: Hands-on Exercise — Applying Iterative Refinement",
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

Incorporate the Iterative Refinement pattern designed in Step 3 into the actual meeting-notes-summarizer SKILL.md. This is a hands-on exercise to translate the design into implementation.

Input:
```
Modify the SKILL.md of meeting-notes-summarizer created in Lesson 7-2 to incorporate the Iterative Refinement pattern.

Specific changes:
1. Add a "Self-review" step to the workflow
2. Add a review checklist (5+ items)
3. Define the improvement loop conditions (when to stop improving)
4. Display the diff before and after to confirm changes

After modification, verify operation with sample data.
```

**Expected result**: The Iterative Refinement pattern is incorporated into the meeting-notes-summarizer SKILL.md, and the self-review and improvement loop are confirmed to work.

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
      {"id": "trouble_1", "label": "I can't tell the patterns apart"},
      {"id": "trouble_2", "label": "I don't know how to combine multiple patterns"},
      {"id": "trouble_3", "label": "The skill broke after modifying SKILL.md"},
      {"id": "trouble_4", "label": "Iterative Refinement creates an infinite loop"}
    ]
  }]
}
```

### Issue 1: I can't tell the patterns apart
**Cause**: The 5 patterns feel conceptually similar
**Solution prompt**:
```
Create a comparison table summarizing each pattern in one line:

| Pattern | In a nutshell | Meeting-notes skill example |
|---------|--------------|---------------------------|
| Sequential Workflow | Process in order | Text → Extract → Organize → Output |
| Multi-MCP Coordination | Coordinate multiple tools | Slack → Meeting notes → Notion |
| Iterative Refinement | Improve iteratively | Draft → Review → Revise |
| Context-aware Tool Selection | Branch based on input | Format detection → Appropriate processing |
| Domain-specific Intelligence | Embed domain knowledge | Meeting type-specific templates |
```

### Issue 2: I don't know how to combine multiple patterns
**Cause**: Unclear how to combine patterns
**Solution prompt**:
```
Show an example combining Sequential Workflow + Iterative Refinement.

Example: Apply Iterative Refinement within each step of the Sequential Workflow
1. Receive and preprocess text
2. Extract attendees → Self-review → Improve
3. Identify agenda → Self-review → Improve
4. Organize decisions → Self-review → Improve
5. Extract action items → Self-review → Improve
6. Markdown output

Explain the improvement points at each step in detail.
```

### Issue 3: The skill broke after modifying SKILL.md
**Cause**: Syntax error or missing required sections in SKILL.md
**Solution prompt**:
```
Follow these steps to recover:
1. Check the changes with git diff
   git diff skills/meeting-notes-summarizer/SKILL.md
2. If there are problems, revert the changes
   cp skills/meeting-notes-summarizer/SKILL.md.backup skills/meeting-notes-summarizer/SKILL.md
3. Carefully re-apply the modifications
```

### Issue 4: Iterative Refinement creates an infinite loop
**Cause**: No termination condition defined for the improvement loop
**Solution prompt**:
```
Limit the improvement loop to a maximum of 2 iterations. Add the following to SKILL.md:

## Improvement Loop Limits
- Maximum improvement iterations: 2
- Termination conditions: When any of the following are met
  1. All review checklist items are OK
  2. Improvement count reaches 2
  3. No changes from the previous improvement
- If issues remain after 2 improvements, append them as a remaining-issues list in the output
```

---

## ✅ Checkpoint
- [ ] Understood the Sequential Workflow pattern processing flow
- [ ] Designed the Multi-MCP Coordination integration
- [ ] Understood the Iterative Refinement review/improvement cycle
- [ ] Designed Context-aware Tool Selection branching
- [ ] Understood Domain-specific Intelligence expertise embedding
- [ ] Applied the Iterative Refinement pattern to the meeting-notes skill
- [ ] Confirmed the modified skill works correctly


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
Paste the following into Cursor's chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail determination with any missing items listed.

---

## ➡️ Next Steps

This is the final lesson of the Skill Master series. Congratulations!

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "back_to_module", "label": "Return to other Module 7 lessons"},
      {"id": "course_top", "label": "Return home (open course top)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- back_to_module → Display Module 7 lesson list (/start-7-1 through /start-7-8)
- course_top → Open https://ai-agent.camp/en/course in browser
- finish → End

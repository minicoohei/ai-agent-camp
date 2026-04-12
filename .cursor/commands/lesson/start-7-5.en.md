---
description: "When the user says /start-7-5 — Module 7 Lesson 7-5: Understanding and Analyzing Existing Skill/Command Structure"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-6-1", "start-6-2"]
level: "intermediate"
tags: ["skill", "command", "agent", "analysis"]
---

# 🎓 Lesson 7-5: Understanding Existing Skill/Command Structure

## 📍 What You'll Do

Welcome to **Lesson 7-5: Understanding and Analyzing Existing Skill/Command Structure**!

| Item | Details |
|------|------|
| Goal | Understand the structure of existing Skills and Commands and gain foundational knowledge for creating your own |
| Duration | ~30 min |
| Skills used | File system exploration, Markdown |
| Prerequisites | Lessons 6-1 and 6-2 completed (Command/Skill fundamentals from the Agent Development module) |

**Session flow:**
1. Explore the structure of `.cursor/commands/` and `.claude/commands/`
2. Explore the structure of `skills/` (SKILL.md, scripts/)
3. Analyze common patterns in existing commands (frontmatter, Step structure, checklists)
4. Analyze common patterns in existing skills (SKILL.md structure, script integration)

By the end of this session, you will have a systematic understanding of Skill and Command design patterns and the knowledge to create your own.

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

## 🚀 Step 1: Explore the Command Directory Structure

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Explore the Command Directory Structure",
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

Commands are placed in two locations:
- `.cursor/commands/` — Custom commands for the current workspace
- `.claude/commands/` — Custom commands for Claude Code

Input:
```
Examine the following directory structures and create a report:

1. List of subdirectories in .cursor/commands/ with file count for each
2. List of subdirectories in .claude/commands/ with file count for each
3. Command file naming convention (start-X-Y.md pattern)

Also explain the difference in roles for each directory:
- lesson/ → Lesson commands (linked to the learning curriculum)
- utility/ → Utility commands (general-purpose tools)
```

**Expected result**: An overview of the Command directory structure is established, and the distinction between lesson/ and utility/ is understood.

---

## 🚀 Step 2: Explore the Skill Directory Structure

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Explore the Skill Directory Structure",
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

Skills are placed in `skills/`, and each skill is an independent directory.

Input:
```
Explore the skills/ directory and report on the following:

1. Skill list (directory names) with a brief description of each
2. Analyze the common structure of each skill directory:
   - Presence of SKILL.md
   - Presence of scripts/ directory
   - Other files (references/, templates/, etc.)

3. Select 3 representative skills and display each directory structure as a tree:
   - banner-creator (image generation)
   - data-analyst (data analysis)
   - check-inbox (communication)

4. Extract common sections from SKILL.md:
   - Sections common to all skills
   - Sections that vary by skill
```

**Expected result**: The standard Skill directory structure (SKILL.md + scripts/ + optional files) is understood.

---

## 🚀 Step 3: Analyze Common Patterns in Existing Commands

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Analyze Common Patterns in Existing Commands",
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

Lesson commands have a common "template". Understanding this template allows you to mass-produce your own commands.

Input:
```
Read the following 3 lesson commands and analyze common patterns:

1. .cursor/commands/lesson/start-6-1.md
2. .cursor/commands/lesson/start-7-1.md
3. .cursor/commands/lesson/start-1-1.md

Analyze from these perspectives and create a "Command Template":

### Common YAML Frontmatter Items
- How to write description, duration, prerequisites, level, tags

### Common Body Structure
- 📍 What You'll Do (table format)
- 🎯 Readiness Check (AskQuestion)
- 🚀 Step N: (structure of each step)
- ⚠️ Common Issues
- ✅ Checkpoint / Completion Check
- ➡️ Next Steps

### AskQuestion Patterns
- 3 choices per Step (practice / review / skip)
- Trouble selection
- Next step selection

Compile the analysis into a "Command Creation Cheat Sheet".
```

**Expected result**: Common patterns in lesson commands are extracted, and a reusable cheat sheet is created.

---

## 🚀 Step 4: Analyze Common Patterns in Existing Skills

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Analyze Common Patterns in Existing Skills",
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

SKILL.md is the "specification document" for a skill, and the most important file for the AI agent to understand the skill.

Input:
```
Read the SKILL.md of the following 3 skills and analyze common patterns:

1. skills/banner-creator/SKILL.md
2. skills/data-analyst/SKILL.md
3. skills/check-inbox/SKILL.md

Analyze from these perspectives and create a "SKILL.md Template":

### Standard SKILL.md Structure
- Metadata (name, description, version, dependencies)
- Overview/Purpose section
- Quick start (command examples)
- Parameters/Options
- Output examples
- Troubleshooting

### Integration Patterns with scripts/ Directory
- How SKILL.md references Python scripts in scripts/
- Script I/O patterns (CLI arguments, file input, standard output)

### Progressive Disclosure in Practice
- Stage 1 (Metadata): Description under 100 words
- Stage 2 (SKILL.md body): Details under 5,000 words
- Stage 3 (scripts/references/): Loaded only when needed

Compile the analysis into a "SKILL.md Creation Cheat Sheet".
```

**Expected result**: Standard SKILL.md patterns are extracted, and a reusable template is created.

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
      {"id": "trouble_1", "label": "The directory structure is too complex to understand"},
      {"id": "trouble_2", "label": "I don't understand the difference between Command and Skill"},
      {"id": "trouble_3", "label": "I don't know how to write SKILL.md"},
      {"id": "trouble_4", "label": "I don't know what to look for in pattern analysis"}
    ]
  }]
}
```

### Issue 1: The directory structure is too complex to understand
**Cause**: Too many skills/commands make it hard to see the big picture
**Solution prompt**:
```
Focus on just these 2 for now:
1. .cursor/commands/lesson/start-1-1.md (the simplest lesson)
2. skills/banner-creator/ (the simplest skill)
Fully understand the structure of these 2 before expanding to others.
```

### Issue 2: I don't understand the difference between Command and Skill
**Cause**: Both are Markdown files and look similar
**Solution prompt**:
```
Simply put:
- Command = "Recipe" (procedure document). An instruction sheet called by the user with /command-name
- Skill = "Toolbox" (toolkit). A capability that the AI agent uses automatically

Remember: Commands are read by humans, Skills are read by agents.
```

### Issue 3: I don't know how to write SKILL.md
**Cause**: Lack of concrete examples
**Solution prompt**:
```
Read skills/banner-creator/SKILL.md as the simplest SKILL.md example.
The minimum requirements are just 3 things: name, description, and usage (command examples).
```

### Issue 4: I don't know what to look for in pattern analysis
**Cause**: Unclear what to compare
**Solution prompt**:
```
Analyze by answering these 3 questions:
1. What is "always present"? (common structure)
2. What "sometimes exists and sometimes doesn't"? (optional elements)
3. What is "written differently"? (variations)
```

---

## ✅ Checkpoint
- [ ] Confirmed the directory structure of .cursor/commands/ and .claude/commands/
- [ ] Confirmed the directory structure of skills/
- [ ] Analyzed common patterns in lesson commands (frontmatter, Step structure, AskQuestion)
- [ ] Analyzed common patterns in SKILL.md (metadata, quick start, parameters)
- [ ] Created the "Command Creation Cheat Sheet"
- [ ] Created the "SKILL.md Creation Cheat Sheet"


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
# Completion check: Verify that the following cheat sheets have been created:
# 1. Command Creation Cheat Sheet (common patterns, frontmatter, Step structure)
# 2. SKILL.md Creation Cheat Sheet (standard structure, Progressive Disclosure)
```

**Expected result**: Both cheat sheets are complete, and you're ready to create your own Command/Skill in the next lesson.

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
      {"id": "next_window", "label": "Start in new window (/start-7-6)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-7-6
- finish → End

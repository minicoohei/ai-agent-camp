---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-7-1"]
duration: "~30 min"
level: "intermediate"
tags: ["agent", "skill-md", "implementation"]
---

# 🎓 Lesson 7-2: Implementing SKILL.md

## 📍 What You'll Do

Welcome to **Lesson 7-2: Implementing SKILL.md**!

| Item | Details |
|------|------|
| Goal | Create the SKILL.md for meeting-notes-summarizer from scratch and verify it works |
| Duration | ~30 min |
| Skills used | Claude Code Skills, SKILL.md |
| Prerequisites | Lesson 7-1 completed (use-case specification available) |

**Session flow:**
1. Optimize the YAML frontmatter
2. Create the directory structure
3. Write the SKILL.md body
4. Create the output template
5. Verify operation

By the end of this session, the SKILL.md for meeting-notes-summarizer will be complete, and you will have confirmed that it triggers correctly with trigger phrases.

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
(view_html → Show course page URL https://ai-agent.camp/en/course/module-7)
(different_lesson → Display module list)

---

## 🚀 Step 1: Optimize the YAML Frontmatter

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Optimize the YAML Frontmatter",
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
Create the YAML frontmatter for meeting-notes-summarizer.

The description should include both "what the skill does" and "when to use it (trigger phrases)".
Use only the name and description fields.

Key points:
- name should be concise in kebab-case
- description should include the skill's functional explanation + trigger phrases in natural language
- Enclose trigger phrases in quotation marks, including multiple patterns
- Condense to approximately 100 words

Example:
---
name: meeting-notes-summarizer
description: A skill that automatically generates structured meeting notes (attendees, agenda, decisions, action items) from meeting text or memos. Use when asked to "summarize the meeting notes", "organize the meeting memo", "extract action items", or "compile the meeting notes".
---
```

**Expected result**: The YAML frontmatter is created with a description that includes trigger phrases.

---

## 🚀 Step 2: Create the Directory Structure

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Create the Directory Structure",
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
Create the directory structure for the meeting-notes-summarizer skill.

Run the following commands:

mkdir -p skills/meeting-notes-summarizer/scripts
mkdir -p skills/meeting-notes-summarizer/references
touch skills/meeting-notes-summarizer/SKILL.md

After creation, verify the directory structure.

Expected directory structure:
skills/meeting-notes-summarizer/
├── SKILL.md
├── scripts/
└── references/

Key points:
- scripts/ holds Python scripts used by the skill
- references/ holds output templates and sample files
- SKILL.md is the skill's entry point
```

**Expected result**: The meeting-notes-summarizer skill directory structure is created.

---

## 🚀 Step 3: Write the SKILL.md Body

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Write the SKILL.md Body",
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
Write the body of skills/meeting-notes-summarizer/SKILL.md with the following structure.

SKILL.md structure:

1. YAML frontmatter (created in Step 1)
2. Skill name and title
3. When to use section
4. Workflow section
5. Output Format specification section
6. Edge Cases section

---
name: meeting-notes-summarizer
description: A skill that automatically generates structured meeting notes (attendees, agenda, decisions, action items) from meeting text or memos. Use when asked to "summarize the meeting notes", "organize the meeting memo", "extract action items", or "compile the meeting notes".
---

# meeting-notes-summarizer - Automated Meeting Notes Generator

## When to Use

Use this skill when receiving requests like:

- Creating meeting notes from meeting text or memos
- Extracting action items or decisions
- Structuring and organizing meeting memos
- Formatting meeting notes

Example trigger phrases:
- "Summarize the meeting notes"
- "Organize the meeting memo"
- "Extract action items"
- "Compile the meeting notes"
- "Organize the key points from this meeting"
- "List the decisions"

## Workflow

This skill processes in the following steps:

### Step 1: Receive input text
- Receive meeting text, memos, audio transcriptions, etc. from the user
- Determine the text format (bullet points, free-form, chat log, etc.)

### Step 2: Extract attendees
- Identify attendee/speaker names from the text
- Standardize name variations (full name, nickname, with/without honorifics)
- If attendees are not specified, note "Attendees unknown"

### Step 3: Identify agenda items
- Identify main meeting topics in chronological order
- Summarize the discussion for each topic
- Organize relationships between topics

### Step 4: Extract decisions
- Extract decisions using keywords like "decided", "agreed", "approved", etc.
- Briefly note the background/reasoning for each decision
- If no decisions were made, explicitly state "No decisions made"

### Step 5: Extract action items
- Extract action items using keywords like "will do", "handle", "check", "by next meeting", etc.
- Associate each action item with an owner and deadline
- If the owner is unknown, note "To be confirmed"
- If the deadline is unknown, note "Deadline TBD"

### Step 6: Format output
- Format output according to the references/output-template.md template
- Generate structured meeting notes in Markdown format
- Save output to the output/ directory

## Output Format

Output follows the template defined in references/output-template.md.
Main sections:
- Basic info (date/time, attendees, location/method)
- Agenda list
- Decisions
- Action items (table format with owner, task, deadline)
- Next meeting

## Edge Cases

### No action items
- State "No action items for this meeting" in the "Action Items" section
- Some meetings only have decisions, so this is not an error

### Unknown attendees
- If inferable from the content, note with "(estimated)"
- If completely unknown, state "Attendees: Unknown (not specified in text)"

### Mixed languages
- Output in the primary language of the input text
- Preserve proper nouns and technical terms in their original language
- If Japanese and English are mixed, prioritize Japanese

### Input text too short
- Create meeting notes with minimum information (agenda and decisions only)
- Explicitly state "Not specified" for missing information

### Chat log format
- Parse timestamps and speakers
- Filter out casual conversation and noise, extracting the essence of the discussion
- For threaded formats, classify topics by thread

Keep within 500 lines and 5,000 words.
```

**Expected result**: The SKILL.md is populated with workflow steps, output specification, and edge case handling.

---

## 🚀 Step 4: Create the Output Template

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Create the Output Template",
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
Create skills/meeting-notes-summarizer/references/output-template.md.

Write the following standard meeting-notes output format as a template:

# Meeting Notes: {Meeting Name}

## Basic Info
- **Date/Time**: {Date/Time}
- **Attendees**: {Attendee List}
- **Location/Method**: {Location or Online}
- **Recorder**: {Recorder Name or AI Auto-generated}

## Agenda

### 1. {Agenda Item 1}
{Summary of discussion for Agenda Item 1}

### 2. {Agenda Item 2}
{Summary of discussion for Agenda Item 2}

## Decisions
- {Decision 1}
  - Background: {Reasoning behind the decision}
- {Decision 2}
  - Background: {Reasoning behind the decision}

## Action Items

| Owner | Task | Deadline | Priority |
|-------|------|----------|----------|
| {Name} | {Task description} | {Deadline} | {High/Med/Low} |
| {Name} | {Task description} | {Deadline} | {High/Med/Low} |

## Discussion Notes
{Detailed discussion and supplementary info}

## Next Meeting
- **Next date/time**: {Next meeting date/time}
- **Planned agenda**: {Planned agenda for next meeting}
- **Preparation**: {What to prepare before next meeting}

---

This template is referenced from SKILL.md.
Placeholders (enclosed in {}) will be replaced with actual meeting content.
```

**Expected result**: The standard meeting-notes output template is created in references/output-template.md.

---

## 🚀 Step 5: Verify Operation

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Verify Operation",
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
Verify the meeting-notes-summarizer skill.

Check 1: Directory structure verification
Run the following commands to verify the directory structure is correct:
ls -la skills/meeting-notes-summarizer/
ls -la skills/meeting-notes-summarizer/scripts/
ls -la skills/meeting-notes-summarizer/references/

Check 2: SKILL.md content verification
Verify the beginning of SKILL.md to confirm the YAML frontmatter is correctly written:
head -5 skills/meeting-notes-summarizer/SKILL.md

Check 3: Trigger phrase test
Test whether the skill triggers correctly using the following sample meeting memo:

---Sample Meeting Memo---
January 15, 2024 14:00-15:00 Regular Meeting
Attendees: Tanaka, Sato, Suzuki

Tanaka: I'll report on the new project progress. Phase 1 is complete and we're transitioning to Phase 2.
Sato: When will the design review be completed?
Tanaka: It should be done by this Friday.
Suzuki: I'll start building the test environment next Monday.
Sato: Approved. Let's proceed with the budget as originally estimated.

Decisions:
- Complete Phase 2 design review by this Friday
- Budget proceeds as originally estimated

Next meeting: January 22 at 14:00
---End of sample---

Give the instruction "Summarize this meeting memo into meeting notes" for the above memo and verify that structured meeting notes following the output template are generated.

Check 4: Output verification
Verify the generated meeting notes include:
- Basic info (date/time, attendees, location) correctly extracted
- Agenda items identified
- Decisions correctly listed
- Action items linked to owners and deadlines
- Output in Markdown format
```

**Expected result**: The skill triggers correctly for the sample meeting memo and outputs structured meeting notes.

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
      {"id": "trouble_1", "label": "SKILL.md doesn't trigger"},
      {"id": "trouble_2", "label": "Output format is inconsistent"},
      {"id": "trouble_3", "label": "Directory isn't recognized"},
      {"id": "trouble_4", "label": "Description is too long (error)"}
    ]
  }]
}
```

### Issue 1: SKILL.md doesn't trigger
**Cause**: Trigger phrases are missing from description
**Solution prompt**:
```
Check the description in the YAML frontmatter of SKILL.md.

Verify the following:
1. Does the description include trigger phrases?
   e.g., "summarize the meeting notes", "organize the meeting memo"
2. Is the name field in correct kebab-case?
3. Are there any YAML syntax errors (indentation, quotes)?

Fix example:
description: A skill that automatically generates structured meeting notes (attendees, agenda, decisions, action items) from meeting text or memos. Use when asked to "summarize the meeting notes", "organize the meeting memo", or "extract action items".
```

### Issue 2: Output format is inconsistent
**Cause**: Missing reference to the output template
**Solution prompt**:
```
Check the "Output Format" section of SKILL.md.

Verify the following:
1. Does references/output-template.md exist?
2. Is the template file reference path correct in SKILL.md?
3. Are the template placeholders consistent?

Check the template file:
cat skills/meeting-notes-summarizer/references/output-template.md
```

### Issue 3: Directory isn't recognized
**Cause**: Not placed correctly under skills/
**Solution prompt**:
```
Verify the directory placement.

Correct placement:
skills/meeting-notes-summarizer/SKILL.md

Verify with the following command:
ls -la skills/meeting-notes-summarizer/

Common mistakes:
- .claude/skill/ (using "skill" instead of "skills")
- skills/meeting-notes-summarizer/ (correct path, with hyphens)
- SKILL.md placed in a different directory
```

### Issue 4: Description is too long (error)
**Cause**: Description has become too verbose
**Solution prompt**:
```
Condense the description to approximately 100 words.

Key points:
1. Explain the skill's function in one sentence
2. Limit trigger phrases to 3-4 representative ones
3. Move detailed explanations to the SKILL.md body

Before condensing (bad example):
description: This skill takes meeting text data, memos, audio transcription text, etc. as input, performs attendee identification, agenda organization, decision extraction, action item enumeration, and outputs as a highly structured Markdown-format meeting notes through advanced text processing.

After condensing (good example):
description: A skill that automatically generates structured meeting notes (attendees, agenda, decisions, action items) from meeting text or memos. Use when asked to "summarize the meeting notes", "organize the meeting memo", or "extract action items".
```

---

## ✅ Checkpoint
- [ ] YAML frontmatter (name + description) is optimized
- [ ] Directory structure is correctly created
- [ ] SKILL.md body contains workflow steps
- [ ] Output template is placed in references/
- [ ] Confirmed correct triggering with trigger phrases
- [ ] Confirmed output is in structured Markdown format


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
      {"id": "next_window", "label": "Start in new window (/start-7-3)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-7-3
- finish → End

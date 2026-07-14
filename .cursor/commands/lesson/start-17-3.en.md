---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "~35 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "copywriting", "lp", "ab-test"]
nonInteractiveMode: deferred
---
# Lesson 17-3: Copywriting

## What You Will Do in This Session

Welcome to **Lesson 17-3: Copywriting**!

| Item | Details |
|------|---------|
| Goal | Create Landing Page / feature page copy with the copywriting skill and generate A/B test variations |
| Duration | ~35 min |
| Skills used | copywriting, ab-test-setup |
| Prerequisites | Gemini API key configured |
| Course page | Refer to [Module 17: Marketing](https://ai-agent.camp/en/course/module-17) in parallel |

**Session flow:**
1. Understand effective Landing Page copy structure (hero, problem, solution, CTA)
2. Create copy for a "Cursor Bootcamp" Landing Page
3. Generate A/B test variations

By the end of this session, 1 Landing Page copy set and 2 variation patterns will be complete.

> **Tip**: If the AI response stops midway, type "please continue" to resume.

---

## Readiness Check

First, confirm that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Go to Step 1)
(check_prereq -> Run prerequisite check)
(view_html -> Show the course page path)
(different_lesson -> Show module list)

---

## Step 1: Understand Effective Landing Page Copy Structure

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Understand Landing Page copy structure",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Explain the copy structure for an effective Landing Page.
For each section, explain its role and writing tips:
1. Hero section (headline + subheadline)
2. Problem statement (articulate user pain points)
3. Solution (product value proposition)
4. Social proof (results, testimonials)
5. Features/benefits (3-5 items)
6. CTA (call to action)
7. FAQ (frequently asked questions)
```

**Expected result**: The role of each Landing Page section and effective copy writing patterns are explained.

---

## Step 2: Create "Cursor Bootcamp" Landing Page Copy

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Create Landing Page copy",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Use the copywriting skill to create Landing Page copy for "Cursor Bootcamp".

Product info:
- Name: Cursor Bootcamp
- Overview: AI agent (Claude Code / Cursor) training for non-engineers
- Target: Business professionals, corporate training participants
- Value: Dramatically improve work efficiency with AI, no programming required
- Track record: 11 modules, 85+ commands, 21 skills included
- Pricing: Contact-based

Create copy for the following sections:
1. Hero section (headline + subheadline)
2. Problem statement
3. Solution
4. Features (3 items)
5. CTA

Save the results to output/lp-copy-v1.md.
```

**Expected result**: Cursor Bootcamp Landing Page copy is generated for each section and saved as a Markdown file.

---

## Step 3: Generate A/B Test Variations

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Generate A/B test variations",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Based on the Landing Page copy created earlier (output/lp-copy-v1.md),
create 2 A/B test variation patterns.

Variation A (output/lp-copy-v2a.md):
- Change hero copy to "fear appeal" type (Are you still doing manual work?)
- Change CTA to "Try it now"

Variation B (output/lp-copy-v2b.md):
- Change hero copy to "results appeal" type (95% of participants experienced efficiency gains)
- Change CTA to "Get a free consultation"

Include the intent of each pattern and which metrics to measure effectiveness.
```

**Expected result**: 2 variations are generated along with A/B test measurement metrics.

---

## Common Issues and Solutions

**AskQuestion configuration:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "Copy is too long or verbose"},
      {"id": "trouble_2", "label": "Tone does not match the target"},
      {"id": "trouble_3", "label": "Variations are too similar"},
      {"id": "trouble_4", "label": "File is not saved"}
    ]
  }]
}
```

### Issue 1: "Copy is too long or verbose"
**Cause**: No character/word count specified in the prompt
**Solution**:
```
Specify target lengths per section and regenerate:
- Hero: headline 10 words max, subheadline 25 words max
- Problem statement: 50 words max
- Features: 25 words each max
- CTA: 5 words max
```

### Issue 2: "Tone does not match the target"
**Cause**: Target persona is too vague
**Solution**:
```
Specify the target more concretely and regenerate:
"Business professionals" -> "Sales managers aged 30-40, moderate IT literacy,
daily use of Excel and PowerPoint"
```

### Issue 3: "Variations are too similar"
**Cause**: Change instructions are not specific enough
**Solution**:
```
Specify the change points more clearly.
Changing the appeal axis itself (feature appeal vs emotional appeal vs results appeal)
creates larger differences.
```

### Issue 4: "File is not saved"
**Cause**: The output directory does not exist
**Solution**:
```
Check if the output directory exists; create it if not.
mkdir -p ~/ai-agent-camp/output
```

---

## Checkpoint
- [ ] Understood Landing Page copy structure (hero/problem/solution/features/CTA)
- [ ] Created 1 "Cursor Bootcamp" Landing Page copy set using the copywriting skill
- [ ] Generated 2 A/B test variation patterns
- [ ] lp-copy-v1.md, lp-copy-v2a.md, lp-copy-v2b.md are saved in the output folder

---

## Deliverables Preview

### Expected output
```
output/marketing/
  banner-*.png
  (variations)
```
> Format: PNG | Size: auto-configured

### Verification commands
```bash
# File list
ls -la output/marketing/

# Open image (macOS: open / Linux: xdg-open)
open output/marketing/
```

> **Claude Code**: Specify the file path with the Read tool to preview images in chat
> **Cursor**: Click images in the file explorer to preview

---

## Completion Check
Paste the following into the Cursor chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## Next Steps

This section is complete. Start the next section or open a new window to begin.

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Open in new window (/start-17-4)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection guide (example)**:
- next_auto -> /next_lesson
- next_window -> Open /start-17-4 in a new window
- finish -> End

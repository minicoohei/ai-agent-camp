---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "~15 min"
prerequisites: ["start-29-2"]
level: "beginner"
tags: ["slide", "revise"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 29-3: Revise an existing job with revise

## 📍 What You'll Do

**Lesson 29-3: Revise an existing job with revise** !

| Item | Details |
|------|------|
| Goal | Apply one revision instruction to an existing job and regenerate only the needed pages |
| Duration | ~15 min |
| Skills used | slide-forge, revise, difference review |
| Prerequisites | Lesson 29-2 |
| Course page | Use [Module 29: slide-forge](https://ai-agent.camp/en/course/module-29?slideId=revise) alongside this lesson |

**Session flow:**
1. Choose the target job and revision instruction
2. Run revise
3. Review the updated artifacts
4. Check for unnecessary changes

By the end of this session, you will have revised a generated deck and reviewed the updated PPTX / PDF / HTML / PNG outputs.

> **💡 Hint**: Do not add numbers or proper nouns that are absent from the source. Do not paste secrets or API keys into chat.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready to revise an existing job?",
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
(check_prereq → Check the Lesson 29-2 output folder and revision instruction)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Choose the Target Job and Revision Instruction

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Choose the Target Job and Revision Instruction",
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
Confirm the target job and revision instruction.

Check:
1. Target --out path, for example ./out/job1
2. A one-sentence instruction, such as "make p3 stronger" or "shorten the cover title"
3. Do not add numbers or proper nouns absent from the source
4. Do not display secrets or API key values
```

**Expected result:** The `--out` path and `--instruction` text are decided.

---

## 🚀 Step 2: Run revise

Run `revise` using the README / quickstart command shape.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Run revise",
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
Run revise with the confirmed job and instruction.

Example:
python cli.py revise --out ./out/job1 --tastes navy --instruction "p3をもっと強く"

Notes:
- Only changed page body images are regenerated
- Do not add information absent from the source
- Do not display secret values
```

**Expected result:** The existing job artifacts are updated.

---

## 🚀 Step 3: Review the Updated Artifacts

Open the updated outputs and confirm that the revision was applied.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Review the Updated Artifacts",
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
Review the updated artifacts.

Artifacts:
1. ./out/job1/deck/navy/deck.pptx
2. ./out/job1/deck/navy/deck.pdf
3. ./out/job1/deck/navy/deck.html
4. ./out/job1/deck/navy/contact_sheet.png

Check:
- The revision instruction is reflected
- PPTX text remains editable
- Fixed chrome coordinates are still aligned
```

**Expected result:** The target page improvement is visible.

---

## 🚀 Step 4: Check for Unnecessary Changes

Confirm that pages outside the revision target did not change unexpectedly.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Check for Unnecessary Changes",
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
Compare the outputs before and after revise, then check for unnecessary changes outside the target page.

Check:
1. Non-target pages keep the same story
2. Fixed chrome aligns across all pages
3. No new numbers or proper nouns absent from the source were added
4. If another revision is needed, write it as one focused sentence
```

**Expected result:** The revise operation stayed within the intended scope.

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
      {"id": "trouble_1", "label": "--out path not found"},
      {"id": "trouble_2", "label": "Revision not reflected"},
      {"id": "trouble_3", "label": "Unrelated pages changed"},
      {"id": "trouble_4", "label": "API key handling concern"}
    ]
  }]
}
```

### Issue 1: `--out` path not found
**Cause**: The path differs from the Lesson 29-2 output folder
**Resolution prompt**:
```
Find the out folder generated in Lesson 29-2 and identify the correct --out path for revise.
```

### Issue 2: Revision not reflected
**Cause**: The instruction is ambiguous or does not identify a target page
**Resolution prompt**:
```
Rewrite the revision instruction as one sentence that names the page and target element, such as "shorten the p3 headline".
```

### Issue 3: Unrelated pages changed
**Cause**: The instruction scope was too broad
**Resolution prompt**:
```
Narrow the revise instruction to one page and one target element so unrelated pages do not change.
```

### Issue 4: API key handling concern
**Cause**: The workflow is trying to print secret values
**Resolution prompt**:
```
Check only whether required keys exist in .env. Do not display values, and do not paste secrets into chat.
```

---

## ✅ Checkpoint
- [ ] Confirmed the target `--out` path
- [ ] Wrote a one-sentence revision instruction
- [ ] Did not paste secrets or API key values into chat
- [ ] Ran the full `python cli.py revise` command shown above
- [ ] Reviewed the updated PPTX / PDF / HTML / PNG outputs
- [ ] Confirmed that non-target pages did not change unexpectedly

---

## 📚 Artifact Preview

The artifact for this lesson is the existing job updated by revise.

### Expected output
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/deck.html
./out/job1/deck/navy/contact_sheet.png
```

> 💡 When applying more revisions, keep each revise instruction focused on the target page and change.

---

## ✅ Completion Check
Paste the following into Cursor chat to check completion:

```
# Completion check: review the revised deck.pptx / deck.pdf / deck.html / contact_sheet.png and judge whether the revision was applied without unnecessary changes.
```

**Expected result:** Cursor reports what is complete and what is still missing.

---

## ➡️ Next Step

This section is complete. Start the next section or open a new window for the next section.

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "What would you like to do next?",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in a new window (/start-29-4)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open a new window and run /start-29-4
- finish → Finish

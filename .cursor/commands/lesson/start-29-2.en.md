---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "~30 min"
prerequisites: ["start-29-1"]
level: "intermediate"
tags: ["slide", "generation", "ai"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 29-2: Production generation from meeting notes with five questions

## 📍 What You'll Do

**Lesson 29-2: Production generation from meeting notes with five questions** !

| Item | Details |
|------|------|
| Goal | Generate an editable proposal deck from meeting notes by selecting five deck parameters |
| Duration | ~30 min |
| Skills used | slide-forge, generate, AskUserQuestion |
| Prerequisites | Lesson 29-1 |
| Course page | Use [Module 29: slide-forge](https://ai-agent.camp/en/course/module-29?slideId=generate) alongside this lesson |

**Session flow:**
1. Confirm inputs and secret handling
2. Select the five answers
3. Run generate
4. Review the four output formats

By the end of this session, you will have generated PPTX / PDF / PNG / HTML from your own meeting notes.

> **💡 Hint**: Do not paste secrets or API keys into chat. Only confirm whether `.env` values exist.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready to generate a production deck from meeting notes?",
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
(check_prereq → Check Lesson 29-1, `.env`, `config.yaml`, and input files)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Confirm Inputs and Secret Handling

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Confirm Inputs and Secret Handling",
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
Confirm the inputs and settings for slide-forge production generation.

Check:
1. Meeting notes file (.md / .txt / .json / .pdf) or direct text
2. If a separate outline exists, treat it as --outline
3. Confirm that .env has OPENAI_API_KEY and LLM_BACKEND without printing values
4. Confirm that config.yaml exists
5. Do not display secrets or API key values in chat or logs
6. Do not invent proper nouns, numbers, dates, costs, or KPIs that are absent from the source material
```

**Expected result:** Inputs, settings, and generation policy are clear.

---

## 🚀 Step 2: Select the Five Answers

Choose the deck type, scenario, tone, goal, and target using the options from `config.yaml`.

Use AskQuestion to select all five answers.

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Select the Five Answers",
  "questions": [
    {
      "id": "deck_type",
      "prompt": "Choose the structure type",
      "options": [
        {"id": "SCQA", "label": "SCQA"},
        {"id": "PREP", "label": "PREP"},
        {"id": "golden_circle", "label": "Golden Circle"},
        {"id": "TAPS", "label": "TAPS"},
        {"id": "whole_part", "label": "Whole-part"}
      ]
    },
    {
      "id": "scenario",
      "prompt": "Choose the scenario",
      "options": [
        {"id": "problem", "label": "Problem-driven"},
        {"id": "vision", "label": "Vision-driven"},
        {"id": "capital", "label": "Capital-driven"},
        {"id": "people", "label": "People-driven"}
      ]
    },
    {
      "id": "tone",
      "prompt": "Choose the tone",
      "options": [
        {"id": "light", "label": "Light"},
        {"id": "navy", "label": "Corporate navy"},
        {"id": "dark", "label": "Cinema dark"},
        {"id": "editorial", "label": "Editorial white"}
      ]
    },
    {
      "id": "goal",
      "prompt": "Choose the goal",
      "options": [
        {"id": "approval", "label": "Win approval"},
        {"id": "share", "label": "Share for awareness"},
        {"id": "move", "label": "Move people with a vision"}
      ]
    },
    {
      "id": "target",
      "prompt": "Choose the target audience",
      "options": [
        {"id": "external", "label": "External first-time audience"},
        {"id": "internal", "label": "Internal decision makers"},
        {"id": "partner", "label": "Existing partners"}
      ]
    }
  ]
}
```

**Guidance after selection:**
Input:
```
Map the selected five answers to --type / --scenario / --tone / --goal / --target.

If you need the course example, use:
- input: examples/loop_engineering.md
- type: Golden Circle
- scenario: Vision-driven
- tone: Corporate navy
- goal: Share and inform
- target: External first-time audience
```

**Expected result:** The five CLI values are decided.

---

## 🚀 Step 3: Run generate

Run generation using the README command shape.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Run generate",
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
Run slide-forge generate with the confirmed input and five answers.

Example:
python cli.py generate --input examples/loop_engineering.md \
  --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー \
  --goal 共有して知ってほしい --target 社外・初対面 \
  --tastes navy --formats pptx pdf png html --out ./out/job1

Notes:
- --input / --outline can be provided multiple times
- Use pptx pdf png html for --formats
- The OpenAI key is used only for image generation, not passed to the LLM agent
- Do not display secret values
```

**Expected result:** A generation job is created under `./out/job1`, and JSON `artifacts` lists output paths under `./out/job1/deck/navy/`.

---

## 🚀 Step 4: Review the Four Output Formats

Inspect the generated PPTX / PDF / PNG / HTML outputs.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Review the Four Output Formats",
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
Review the generated artifacts and collect their absolute paths.

Artifacts:
1. ./out/job1/deck/navy/deck.pptx
2. ./out/job1/deck/navy/deck.pdf
3. ./out/job1/deck/navy/contact_sheet.png
4. ./out/job1/deck/navy/deck.html

Check:
- Fixed chrome aligns at the same coordinates on every page
- Headline, lead, and footer remain editable text in PPTX
- The deck does not add proper nouns, numbers, dates, costs, or KPIs absent from the source
- Write one sentence for anything you want to revise next
```

**Expected result:** The four formats and the next revision target are clear.

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
      {"id": "trouble_1", "label": "OPENAI_API_KEY is not available"},
      {"id": "trouble_2", "label": "claude / codex CLI is missing"},
      {"id": "trouble_3", "label": "render failed"},
      {"id": "trouble_4", "label": "Deck drifted from source"}
    ]
  }]
}
```

### Issue 1: `OPENAI_API_KEY is not available`
**Cause**: The image generation key is not configured in `.env`
**Resolution prompt**:
```
Check only whether OPENAI_API_KEY exists in .env. Do not display the key value, and guide safe setup if it is missing.
```

### Issue 2: `claude` / `codex` CLI is missing
**Cause**: The CLI for `LLM_BACKEND` is not on PATH
**Resolution prompt**:
```
Check the LLM_BACKEND value and whether the matching claude / codex CLI is on PATH, then guide the needed setup.
```

### Issue 3: render failed
**Cause**: Playwright Chromium, ImageMagick, or Poppler is missing
**Resolution prompt**:
```
Read the render failure log and isolate whether Chromium, ImageMagick, or Poppler is missing.
```

### Issue 4: Deck drifted from source
**Cause**: The deck inferred information not present in the input
**Resolution prompt**:
```
Compare the deck against the source and remove or mark as pending any proper nouns, numbers, dates, costs, or KPIs not present in the input.
```

---

## ✅ Checkpoint
- [ ] Confirmed the input file or direct text
- [ ] Confirmed `.env` and `config.yaml` exist
- [ ] Did not paste secrets or API key values into chat
- [ ] Selected the five answers
- [ ] Ran the full `python cli.py generate` command shown above
- [ ] Reviewed PPTX / PDF / PNG / HTML outputs

---

## 📚 Artifact Preview

The artifacts for this lesson are the proposal deck outputs generated from meeting notes.

### Expected output
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/contact_sheet.png
./out/job1/deck/navy/deck.html
```

> 💡 In Lesson 29-3, you will revise the existing job once.

---

## ✅ Completion Check
Paste the following into Cursor chat to check completion:

```
# Completion check: confirm that PPTX / PDF / PNG / HTML were generated under ./out/job1/deck/navy, and that fixed chrome plus editable text were inspected.
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
      {"id": "next_window", "label": "Start in a new window (/start-29-3)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open a new window and run /start-29-3
- finish → Finish

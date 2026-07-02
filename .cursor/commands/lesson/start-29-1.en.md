---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "~20 min"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["slide", "pptx", "demo"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 29-1: slide-forge demo without an API key

## 📍 What You'll Do

**Lesson 29-1: slide-forge demo without an API key** !

| Item | Details |
|------|------|
| Goal | Generate PPTX and HTML from the bundled sample without an OpenAI API key |
| Duration | ~20 min |
| Skills used | slide-forge, build-only, PPTX review |
| Prerequisites | Lesson 0-3 |
| Course page | Use [Module 29: slide-forge](https://ai-agent.camp/en/course/module-29?slideId=first-run) alongside this lesson |

**Session flow:**
1. Check the workspace and dependencies
2. Get slide-forge
3. Run the no-key demo
4. Review the PPTX and HTML outputs

By the end of this session, you will have inspected a fixed-chrome slide-forge deck without using an API key.

> **💡 Hint**: Do not paste secrets or API keys into chat. This lesson does not require an OpenAI API key.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready to run the no-key demo?",
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
(check_prereq → Check Python 3.11+, Node.js, ImageMagick, and Poppler)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Check the Workspace and Dependencies

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Check the Workspace and Dependencies",
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
Before running the slide-forge no-key demo, check the workspace and dependencies.

Check:
1. Do not overwrite an existing slide-forge directory without confirmation
2. Python 3.11+ is available
3. Node.js is available
4. ImageMagick magick is available
5. Poppler pdfinfo / pdftoppm are available
6. macOS: brew install imagemagick poppler / Windows and Linux: install ImageMagick and Poppler with each package manager

Do not display secrets or API key values.
```

**Expected result:** Missing dependencies and the working directory state are clear.

---

## 🚀 Step 2: Get slide-forge

If the repository is not present yet, clone the official repository.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Get slide-forge",
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
If slide-forge is not already present, get it with:

git clone --depth 1 --branch v0.1.0 https://github.com/minicoohei/slide-forge.git
cd slide-forge

Use the verified fixed version as a supply-chain precaution.
If the directory or checkout already exists, do not overwrite it without confirmation. Later setup commands must not overwrite existing .env or config.yaml files.
```

**Expected result:** You are at the slide-forge repository root.

---

## 🚀 Step 3: Run the No-key Demo

Use bundled sample images to generate PPTX and HTML without an OpenAI API key.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Run the No-key Demo",
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
Install dependencies and run the no-key demo.

pip install -r requirements.txt
cd pipeline/lib && npm ci && npx playwright install chromium && cd ../..
cp -n .env.example .env
cp -n config.default.yaml config.yaml
python cli.py build-only --manifest examples/sample_manifest.json \
  --tastes lime --formats pptx html --no-regen --out examples/sample

Notes:
- Existing .env / config.yaml files are not overwritten because the commands use cp -n
- The offline demo must use --out examples/sample --tastes lime
- Changing those values can produce an empty deck with missing_bodies
- No OpenAI API key is required
```

**Expected result:** `examples/sample/lime/deck.pptx` and `examples/sample/lime/deck.html` are generated.

---

## 🚀 Step 4: Review the PPTX and HTML Outputs

Open the generated files and inspect the fixed chrome.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Review the PPTX and HTML Outputs",
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
Open and inspect the generated PPTX and HTML.

open examples/sample/lime/deck.pptx

Check:
1. Headline, lead, and footer are editable text
2. Fixed chrome aligns at the same coordinates on every page
3. Only the body illustration is an image
4. deck.html shows the same deck in the browser
```

**Expected result:** You can inspect the sample deck in both PPTX and HTML.

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
      {"id": "trouble_1", "label": "missing_bodies appears"},
      {"id": "trouble_2", "label": "magick / pdfinfo is missing"},
      {"id": "trouble_3", "label": "Playwright Chromium is missing"},
      {"id": "trouble_4", "label": "PPTX does not open"}
    ]
  }]
}
```

### Issue 1: `missing_bodies` appears
**Cause**: The command did not use the fixed `--out examples/sample --tastes lime` values
**Resolution prompt**:
```
Re-run the slide-forge no-key demo with --out examples/sample --tastes lime, and explain why those values are fixed.
```

### Issue 2: `magick` / `pdfinfo` is missing
**Cause**: ImageMagick or Poppler is not installed
**Resolution prompt**:
```
Guide me through installing ImageMagick and Poppler on macOS, then verify magick / pdfinfo / pdftoppm.
```

### Issue 3: Playwright Chromium is missing
**Cause**: `npx playwright install chromium` has not been run
**Resolution prompt**:
```
Show the steps to reinstall Chromium from slide-forge/pipeline/lib.
```

### Issue 4: PPTX does not open
**Cause**: Generation failed or the deck is empty
**Resolution prompt**:
```
Check whether deck.pptx exists, its file size, and the build-only JSON output to isolate the failure.
```

---

## ✅ Checkpoint
- [ ] Confirmed the slide-forge working directory
- [ ] Checked Python 3.11+, Node.js, ImageMagick, and Poppler
- [ ] Ran the no-key demo with `--out examples/sample --tastes lime`
- [ ] Opened `examples/sample/lime/deck.pptx`
- [ ] Checked `examples/sample/lime/deck.html`
- [ ] Did not paste secrets or API keys into chat

---

## 📚 Artifact Preview

The artifacts for this lesson are the sample deck generated without an API key.

### Expected output
```
examples/sample/lime/deck.pptx
examples/sample/lime/deck.html
```

> 💡 To also inspect PDF / PNG, add `--formats pdf png`.

---

## ✅ Completion Check
Paste the following into Cursor chat to check completion:

```
# Completion check: confirm that examples/sample/lime/deck.pptx and deck.html were generated, and that fixed chrome plus editable text were inspected.
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
      {"id": "next_window", "label": "Start in a new window (/start-29-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open a new window and run /start-29-2
- finish → Finish

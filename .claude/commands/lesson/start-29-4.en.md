---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "~20 min"
prerequisites: ["start-29-2"]
level: "intermediate"
tags: ["slide", "assets", "vision"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 29-4: Fetch real images with fetch-assets

## 📍 What You'll Do

**Lesson 29-4: Fetch real images with fetch-assets** !

| Item | Details |
|------|------|
| Goal | Safely add real company logos, profile photos, and product images to an existing job |
| Duration | ~20 min |
| Skills used | slide-forge, fetch-assets, vision verification |
| Prerequisites | Lesson 29-2 |
| Course page | Use [Module 29: slide-forge](https://ai-agent.camp/en/course/module-29?slideId=fetch-assets) alongside this lesson |

**Session flow:**
1. Confirm the target job and key setup
2. Confirm image rights and usage responsibility
3. Run fetch-assets
4. Review the results and updated deck

By the end of this session, you will understand how to use only real images that pass vision verification.

> **💡 Hint**: Users are responsible for checking image rights and permitted use. Do not paste secrets or API keys into chat.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready to run fetch-assets?",
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
(check_prereq → Check the Lesson 29-2 output, GEMINI_API_KEY, SERPAPI_KEY, and image rights responsibility)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Confirm the Target Job and Key Setup

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Confirm the Target Job and Key Setup",
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
Confirm the target job and key setup for fetch-assets.

Check:
1. Existing job --out path, for example ./out/job1
2. Confirm that .env has GEMINI_API_KEY
3. SERPAPI_KEY is recommended for Google Images search
4. Do not display key values
5. Confirm that the meeting notes contain real company, product, or person names
```

**Expected result:** The target and settings for fetch-assets are clear.

---

## 🚀 Step 2: Confirm Image Rights and Usage Responsibility

Confirm the handling policy for images fetched from the web.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Confirm Image Rights and Usage Responsibility",
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
Before running fetch-assets, confirm image rights and usage responsibility.

Important:
1. Users are responsible for checking image rights and permitted use
2. Source URLs remain in catalog[].note in the result JSON
3. Materials with low vision verification scores are not used
4. Slides without accepted assets stay as diagrams
5. If you do not want web fetching, use --photo-catalog with a local image catalog JSON
```

**Expected result:** The usage boundary and responsibility are clear.

---

## 🚀 Step 3: Run fetch-assets

Inject real images into the existing job.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Run fetch-assets",
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
Run fetch-assets on the existing job.

python cli.py fetch-assets --out ./out/job1

To fetch assets during a new generation:
python cli.py generate --input examples/loop_engineering.md \
  --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー \
  --goal 共有して知ってほしい --target 社外・初対面 \
  --tastes navy --formats pptx pdf png html --out ./out/job1 --fetch-assets

Notes:
- GEMINI_API_KEY is required for extraction and vision verification
- SERPAPI_KEY is recommended for Google Images search
- Do not display secret values
- If no asset passes verification, the slide stays as a diagram
```

**Expected result:** Candidate images are fetched, and only assets that pass vision verification are reflected in the deck.

---

## 🚀 Step 4: Review the Results and Updated Deck

Review the result JSON and the updated deck.

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Review the Results and Updated Deck",
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
Review the fetch-assets result and updated deck.

Check:
1. Source URLs remain in catalog[].note in the result JSON
2. The name and image actually match
3. Low-score assets are not forced into the deck
4. The user still needs to verify image rights and permitted use
5. Fixed chrome and editable PPTX text are preserved
```

**Expected result:** Source URLs, verification results, and deck changes are clear.

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
      {"id": "trouble_1", "label": "GEMINI_API_KEY is missing"},
      {"id": "trouble_2", "label": "No assets were accepted"},
      {"id": "trouble_3", "label": "Wrong company logo appears"},
      {"id": "trouble_4", "label": "Image rights concern"}
    ]
  }]
}
```

### Issue 1: `GEMINI_API_KEY` is missing
**Cause**: The required key for extraction and vision verification is not configured
**Resolution prompt**:
```
Check only whether GEMINI_API_KEY exists in .env. Do not display the value, and guide safe setup if it is missing.
```

### Issue 2: No assets were accepted
**Cause**: Vision verification score was too low or no candidate was found
**Resolution prompt**:
```
Review the fetch-assets result JSON, summarize low-score or missing-candidate reasons, and explain that keeping the diagram is acceptable.
```

### Issue 3: Wrong company logo appears
**Cause**: Search mixed in a similarly named company
**Resolution prompt**:
```
Check candidate names, source URLs, and vision verification results in catalog, then exclude assets whose name and image do not match.
```

### Issue 4: Image rights concern
**Cause**: Usage terms for fetched web images have not been checked
**Resolution prompt**:
```
List the source URLs for fetched images and create a checklist for the user to verify rights and permitted use.
```

---

## ✅ Checkpoint
- [ ] Confirmed the existing job `--out` path
- [ ] Confirmed `GEMINI_API_KEY` exists without printing its value
- [ ] Understood when `SERPAPI_KEY` is useful
- [ ] Understood that users are responsible for image rights and permitted use
- [ ] Ran `python cli.py fetch-assets --out ./out/job1`
- [ ] Reviewed `catalog[].note` in the result JSON and the updated deck
- [ ] Did not paste secrets or API keys into chat

---

## 📚 Artifact Preview

The artifacts for this lesson are the image verification results and the updated deck.

### Expected output
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/deck.html
./out/job1/deck/navy/contact_sheet.png
```

> 💡 Check source URLs in `catalog[].note`. Rights and permitted use must be judged by the user.

---

## ✅ Completion Check
Paste the following into Cursor chat to check completion:

```
# Completion check: review the fetch-assets result JSON and updated deck.pptx, then judge source URLs, vision verification, and remaining image-rights checks.
```

**Expected result:** Cursor reports what is complete and what is still missing.

---

## ➡️ Next Step

This section is complete. Start another lesson in a new window if needed.

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
      {"id": "next_window", "label": "Start in a new window (/start-29-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open a new window and run /start-29-1
- finish → Finish

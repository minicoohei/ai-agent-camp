---
description: "When the user says /start-14-4 — Module 14 Lesson 14-4: Article Writing - Illustration Planning and Generation with nanobanana + PlantUML"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~40 min"
prerequisites: ["start-14-3"]
level: "intermediate"
tags: ["article", "illustration"]
---

# 🎓 Lesson 14-4: Illustration Planning and Generation - nanobanana + PlantUML

## 📍 What You'll Do

Welcome to **Lesson 14-4: Illustration Planning and Generation - nanobanana + PlantUML**!

| Item | Details |
|------|---------|
| Goal | Detect illustration markers in the article and auto-generate illustrations with nanobanana and PlantUML |
| Duration | ~40 min |
| Skills Used | nanobanana, diagram-generator |
| Prerequisites | Gemini API key configured, Lesson 14-3 (draft) complete |
| Course Page | Refer to [Module 14: Article Writing](https://ai-agent.camp/en/course/module-14) in parallel |

**Session flow:**
1. Check illustration markers (`<!-- illustration: ... -->`) in the draft
2. For type=diagram markers → generate diagrams with PlantUML
3. For type=image markers → generate images with nanobanana
4. Embed the generated images in Markdown

By the end of this session, an article draft with illustrations will be complete.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. Responses may pause depending on the tool, but this is not a malfunction.

---

## 🎯 Readiness Check

First, let's confirm everything is ready.

**AskQuestion settings:**
```json
{
  "title": "🎯 Pre-Session Check",
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

(ready → Proceed to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Check Illustration Markers in the Draft

In Codex, you typically select from choices in chat to choose the marker detection method.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Check Illustration Markers",
  "questions": [{
    "id": "marker_method",
    "prompt": "How would you like to detect illustration markers?",
    "options": [
      {"id": "auto_detect", "label": "Auto-detect markers"},
      {"id": "manual_specify", "label": "Manually specify illustration locations"}
    ]
  }]
}
```

**If "Auto-detect markers":**
Input:
```text
Read output/article-14-3-draft-final.md and
extract all illustration markers (<!-- illustration: ... -->).

List the following for each marker:
1. Line number
2. Type (image / diagram)
3. Description text
4. Surrounding context (which section it belongs to)

If markers are missing, suggest locations where they should be added.
```

**If "Manually specify illustration locations":**
```text
Display the contents of output/article-14-3-draft-final.md.
Specify where you want to insert illustrations, and markers will be added.
```

**Expected result**: All illustration markers in the draft are listed, and a generation plan is established.

---

## 🚀 Step 2: Generate Diagrams with PlantUML (type=diagram)

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Generate Diagrams with PlantUML",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip (if no diagram markers)"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Use the diagram-generator skill to generate diagrams for the following illustration markers.

Target marker:
<!-- illustration: type=diagram, description="Work efficiency improvement flow chart" -->

Generation conditions:
- Format: PlantUML → PNG image
- Style: Simple, easy-to-read color scheme
- Output: output/images/article-14-4-diagram-1.png

Execution command:
uv run python tools/generate_diagram.py --type flowchart --topic "Work efficiency improvement flow" --output output/images/article-14-4-diagram-1.png

Generate images for all diagram markers.
```

**Expected result**: PlantUML-based diagram images are generated in output/images/.

---

## 🚀 Step 3: Generate Images with nanobanana (type=image)

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Generate Images with nanobanana",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip (if no image markers)"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Use the nanobanana skill to generate images for the following illustration markers.

Target marker:
<!-- illustration: type=image, description="Business professional working with AI tools" -->

Generation conditions:
- Style: Modern, clean illustration style
- Size: Aspect ratio suitable for article illustrations (16:9 or 4:3)
- Output: output/images/article-14-4-image-1.png

Execution command:
uv run python tools/nanobanana.py --prompt "Business professional working with AI tools, modern illustration style" --output output/images/article-14-4-image-1.png

Generate images for all image markers.
```

**Expected result**: Illustration images generated with nanobanana are saved in output/images/.

---

## 🚀 Step 4: Embed Generated Images in Markdown

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 4: Embed Images in Markdown",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Replace the illustration markers in output/article-14-3-draft-final.md
with Markdown image syntax for the generated images.

Replacement rules:
- <!-- illustration: type=diagram, description="..." -->
  → ![Description](images/article-14-4-diagram-N.png)
- <!-- illustration: type=image, description="..." -->
  → ![Description](images/article-14-4-image-N.png)

Add alt text (description) and a caption (*Figure N: Description*) to each image.

Save the result to output/article-14-4-with-images.md.
```

**Expected result**: Illustration markers are replaced with actual image references, and the complete article draft is saved.

---

## ⚠️ Common Issues and Solutions

In Codex, you typically present choices in chat so the user can select their issue and get guidance instantly.

**AskQuestion settings example:**
```json
{
  "title": "Select Your Issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "PlantUML diagrams aren't generated correctly"},
      {"id": "trouble_2", "label": "nanobanana images don't match expectations"},
      {"id": "trouble_3", "label": "Illustration markers aren't found"},
      {"id": "trouble_4", "label": "Image embedding paths are broken"}
    ]
  }]
}
```


### Issue 1: "PlantUML diagrams aren't generated correctly"
**Cause**: PlantUML syntax error or Java environment issue
**Solution prompt**:
```text
Check the PlantUML syntax.
First verify operation with a simple diagram, then gradually add elements.
If a Java environment is needed: check with java -version.
Alternative: You can also generate diagrams directly with the Gemini Image Generation API.
```

### Issue 2: "nanobanana images don't match expectations"
**Cause**: The prompt isn't specific enough
**Solution prompt**:
```text
Make the image generation prompt more specific:
- Style specification: "flat design illustration", "photo-realistic", "watercolor style"
- Color specification: "calm blue tones"
- Composition specification: "main object centered, simple background"
Try regenerating and comparing results.
```

### Issue 3: "Illustration markers aren't found"
**Cause**: Markers weren't inserted in Lesson 14-1/14-3
**Solution prompt**:
```text
Add illustration markers to the draft.
Insert at the beginning or end of each H2 section in this format:
<!-- illustration: type=image|diagram, description="Description of section content" -->
```

### Issue 4: "Image embedding paths are broken"
**Cause**: Mismatch between relative and absolute paths
**Solution prompt**:
```bash
Use relative paths from the article file for image paths in Markdown.
If the article is in output/: ![alt](images/filename.png)
Verify images are in output/images/: ls output/images/
```

---

## ✅ Checkpoint
- [ ] Detected and confirmed all illustration markers in the draft
- [ ] Generated PlantUML diagrams for type=diagram markers
- [ ] Generated nanobanana images for type=image markers
- [ ] Saved the article with all illustrations embedded in Markdown to output/

---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/
└── article-14-4-*.md  (article documents)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/article-14-4-*.md

# Check the beginning (first 30 lines)
head -30 output/article-14-4-*.md
```

> 💡 View full text: `cat output/article-14-4-*.md` to display the entire file

---

## ✅ Completion Check
Enter the following in the Codex chat to verify completion:

```bash
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin.

In Codex, you can typically select from choices in chat.

**AskQuestion settings example:**
```json
{
  "title": "Select Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Open in new window (/start-14-5)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → /next_lesson
- next_window → Open /start-14-5 in a new window
- finish → End

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1", "start-3-2", "start-3-3", "start-3-4"]
duration: "~30 min"
level: "intermediate"
tags: ["screenshot", "batch-processing", "manual"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 3-5: A/B Test Result Analysis

## 📍 What You'll Do

**Lesson 3-5: A/B Test Result Analysis** !

| Item | Details |
|------|---------|
| Goal | Batch process multiple screenshots and create an integrated user manual |
| Duration | ~30 min |
| Skills Used | Integration of screenshot-analyzer, tutorial-generator, and screenshot-annotator |
| Prerequisites | Lessons 3-1 through 3-4 completed, Gemini API key configured |
| Course Page | [Module 3: Screenshot Analysis](https://ai-agent.camp/en/course/module-3) in parallel |

**Session flow:**
1. Define manual creation requirements
2. Batch analysis of multiple screenshots and structure design
3. Output the integrated manual

By the end of this session, you will be able to create production-level operation manuals.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Analyze A/B Test Screens

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Define manual creation requirements",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
We will create a web app user manual.

Target features:
1. Login
2. Dashboard
3. Data entry
4. Report generation
5. User settings

Screenshots for each feature are placed as official materials under `courses/aiagent/lesson03-core/module03-screenshot/practice/data/`.
Assets not in `practice/` but needed for training should be moved to the corresponding `practice/` or `final/` directory before use.

Create a manual creation plan:
- Number of screenshots needed for each feature
- Tutorial generation order
- Integration method
```

**Expected result**: A detailed manual creation plan is presented.

---

## 🚀 Step 2: Statistical Significance Assessment

Batch generate tutorials from multiple screenshots:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Batch Generate Tutorials",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Batch generate tutorials from the following screenshots.

Input files:
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/dashboard.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/data-input.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/report.png

Output: output/manual/

For each file:
1. Generate tutorial with tutorial-generator
2. Add annotations to key areas with screenshot-annotator
3. Save in HTML format

Report progress while executing.
```

**Expected result**: Tutorials are generated for each screenshot and progress is reported.

---

## 🚀 Step 3: Generate Analysis Report

Apply consistent annotation styles to all images:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Batch Add Annotations",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
For PNG images under courses/aiagent/lesson03-core/module03-screenshot/practice/data/,
highlight important action buttons with red frames.

Output: output/annotated/

For each image:
- Auto-detect main action buttons
- Highlight with red_box style
- Add operation descriptions with callouts

Display the list of processed images.
```

**Expected result**: Annotations are added to all images with a consistent style.

---

## 🚀 Step 4: Integrate into an HTML Manual

Integrate generated content into a single HTML document:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Integrate into an HTML Manual",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Integrate the generated tutorials and annotated images
into a single HTML manual.

Files to integrate:
- output/manual/*.html (tutorials)
- output/annotated/*.png (annotated images)

Output: output/complete-manual.html

Structure:
1. Table of contents (links to each feature)
2. Tutorial for each feature
3. Troubleshooting section
4. FAQ

Create with beginner-friendly language.
```

**Expected result**: A complete HTML manual with a table of contents is generated.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "Error occurs during batch processing"},
      {"id": "trouble_2", "label": "Manual is too long"},
      {"id": "trouble_3", "label": "HTML does not display correctly"},
      {"id": "trouble_4", "label": "Images are not displayed"}
    ]
  }]
}
```


### Issue 1: "Error occurs during batch processing"
**Cause**: Some file paths are incorrect
**Solution prompt**:
```
Check the list of files to be processed.
If any files do not exist, report them
and continue processing with only the existing files.
```

### Issue 2: "Manual is too long"
**Cause**: Too much information makes it hard to read
**Solution prompt**:
```
Split the manual as follows:
- Basics (essential operations only)
- Advanced (detailed settings)
- Administrator (management features)

Output each part as a separate HTML file.
```

### Issue 3: "HTML does not display correctly"
**Cause**: HTML tag structure error
**Solution prompt**:
```
Validate the structure of the generated HTML file.
If there are errors, fix them and regenerate in proper HTML5 format.
```

### Issue 4: "Images are not displayed"
**Cause**: Image paths are relative and do not resolve correctly
**Solution prompt**:
```
Check the image paths in the HTML manual.
Verify that all images are correctly referenced
and fix paths as needed.
```

---

## ✅ Checkpoint
- [ ] Can define manual creation requirements
- [ ] Can batch process multiple files
- [ ] Can efficiently combine auto-generation with manual editing
- [ ] Can integrate into an HTML document
- [ ] Can create a manual with table of contents and structure


---

## 📋 Output Preview

### Expected Output
```
📁 output/screenshots/
├── analyzed-{target-name}.png
└── (variations)
```
> Format: PNG | Size: Auto-configured

### Verification Commands
```bash
# File list
ls -la output/screenshots/

# Open image (macOS: open / Linux: xdg-open)
open output/screenshots/
```

> 💡 **Claude Code**: Specify the file path with the Read tool to preview images in chat
> 💡 **Cursor**: Click on the image in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-3-6)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-3-6
- finish → End

---
description: "When the user says /start-3-1 — Module 3 Lesson 3-1: Screenshot Analysis Fundamentals"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
duration: "~25 min"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["screenshot", "analysis", "gemini-vision"]
---

# 🎓 Lesson 3-1: Screenshot Analysis Fundamentals

## 📍 What You'll Do

Welcome to **Lesson 3-1: Introduction to Screenshot Analysis**!

| Item | Details |
|------|---------|
| Goal | Automatically analyze on-screen errors and suggest solutions using the screenshot-analyzer skill |
| Duration | ~25 min |
| Skills Used | screenshot-analyzer (Gemini Vision API) |
| Prerequisites | Gemini API key configured, Python environment set up |
| Course Page | Refer to [Module 3: Screenshot Analysis](https://ai-agent.camp/en/course/module-3) in parallel |

**Session flow:**
1. Prepare screenshots
2. Analyze error screens and get solutions
3. Apply analysis results

By the end of this session, you will be able to obtain error diagnosis results and solution suggestions.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-Session Check",
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
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Prepare Screenshots

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Prepare Screenshots",
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

**After selection (example)**:
Input:
```
Check if sample images exist in courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/.
If not, show me how to add training images to the same directory
and how to move personal temporary assets to official lesson materials.
```

**Expected result**: The inputs folder status is confirmed, and test image preparation instructions are provided as needed.

---

## 🚀 Step 2: Run Basic Error Analysis

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Run Basic Error Analysis",
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

**After selection (example)**:
Input:
```
Use the screenshot-analyzer skill to analyze errors from a screenshot.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/error-screenshot.png
Output: output/screenshots/analyzed-error.png

Analysis:
- Identify the error cause
- Suggest solutions
- Mark important areas
```

**Expected result**: Error areas are marked with red borders, and an image with solution annotations is generated.

---

## 🚀 Step 3: Identify UI Issues

Let's analyze UI design problems:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Identify UI Issues",
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

**After selection (example)**:
Input:
```
Analyze the UI issues in this screenshot.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/ui-issue.png
Output: output/screenshots/ui-issue-annotated.png

Analysis criteria:
- Button placement
- Font size
- Color contrast
- Usability

Add annotations to problem areas and present improvement suggestions.
```

**Expected result**: UI issues are visually marked, and improvement suggestions are added as annotations.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select Your Issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "Screenshot file not found"},
      {"id": "trouble_2", "label": "Analysis results are inaccurate"},
      {"id": "trouble_3", "label": "Annotations not displayed"},
      {"id": "trouble_4", "label": "Gemini API error"}
    ]
  }]
}
```


### Issue 1: "Screenshot file not found"
**Cause**: File path is wrong or file does not exist
**Solution prompt**:
```
Check the contents of courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/.
List any image files (.png, .jpg) found there.
```

### Issue 2: "Analysis results are inaccurate"
**Cause**: Screenshot quality is low or information is insufficient
**Solution prompt**:
```
Tell me what additional information should be provided
to make the screenshot analysis more accurate.
```

### Issue 3: "Annotations not displayed"
**Cause**: Output folder does not exist
**Solution prompt**:
```
Create the output/screenshots/ folder.
If it doesn't exist, create it. If it does, check its contents.
```

### Issue 4: "Gemini API error"
**Cause**: API key is not set
**Solution prompt**:
```
Check if the GEMINI_API_KEY environment variable is set.
If not, show me how to set it up.
```

---

## ✅ Checkpoint
- [ ] Can identify issues from screenshots
- [ ] Can correctly interpret error messages
- [ ] Can visually mark problem areas
- [ ] Can suggest specific solutions
- [ ] Analysis results saved to the output folder


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
# File listing
ls -la output/screenshots/

# Open images (macOS: open / Linux: xdg-open)
open output/screenshots/
```

> 💡 **Claude Code**: Specify the file path with the Read tool to preview images in chat
> 💡 **Cursor**: Click on the image in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose your next action",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in a new window (/start-3-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-3-2
- finish → End

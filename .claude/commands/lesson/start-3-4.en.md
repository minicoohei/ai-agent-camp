---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "~25 min"
level: "intermediate"
tags: ["screenshot", "annotation", "manual"]
---

# 🎓 Lesson 3-4: Dashboard Monitoring Setup

## 📍 What You'll Do

**Lesson 3-4: Dashboard Monitoring Setup** !

| Item | Details |
|------|---------|
| Goal | Add arrows, frames, numbers, and text using the screenshot-annotator skill to create manual images |
| Duration | ~25 min |
| Skills Used | screenshot-annotator (Gemini Vision API) |
| Prerequisites | Lesson 3-1 completed, Gemini API key configured |
| Course Page | [Module 3: Screenshot Analysis](https://ai-agent.camp/en/course/module-3) in parallel |

**Session flow:**
1. Highlight buttons with red frames
2. Add arrows and callouts
3. Create annotated images with step numbers

By the end of this session, annotated images for manuals will be saved in outputs.

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

## 🚀 Step 1: Capture Dashboard Screenshots

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Highlight buttons with red frames",
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
Use the screenshot-annotator skill to highlight the dashboard help button.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/dashboard.png
Output: output/screenshots/help-button-annotated.png

Annotations:
- Frame the help button in the upper right with a red box
- Point with an arrow saying "Click here"
- Style: red_box
```

**Expected result**: An image is generated with the help button framed in red and arrows with explanatory text added.

---

## 🚀 Step 2: Analyze Metrics and KPI

Add explanations to the search form:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Add Explanations with Callouts",
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
Add callout explanations to the search form.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/search-form.png
Output: output/screenshots/search-annotated.png

Annotations:
- Identify the search form
- Style: callout (speech bubble)
- Text: "Enter a keyword and press the Enter key"
```

**Expected result**: A callout is added to the search form explaining how to use it.

---

## 🚀 Step 3: Generate Monitoring Report

Add numbers to operation steps:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Add Step Numbers",
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
Add numbers to the menu operation steps.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/menu-operation.png
Output: output/screenshots/menu-steps-annotated.png

Annotations (add in order):
1. Menu icon in the upper left -> Add "1" (circle style)
2. Settings menu item -> Add "2"
3. Profile settings -> Add "3"

Enclose each number in a red circle to clarify the operation order.
```

**Expected result**: An image with numbered steps 1, 2, 3 in red circles is generated.

---

## 🚀 Step 4: Review Annotation Styles

Let's review the available annotation styles:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Review Annotation Styles",
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
Tell me all annotation styles available in screenshot-annotator.

For each style, explain the following:
- Style name
- Visual description
- Suitable use cases
- Usage example
```

**Expected result**: A list of styles such as red_box, arrow, callout, highlight, circle, number, etc. is displayed.

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
      {"id": "trouble_1", "label": "Annotations are not displayed"},
      {"id": "trouble_2", "label": "Annotation position is wrong"},
      {"id": "trouble_3", "label": "Arrow direction is reversed"},
      {"id": "trouble_4", "label": "Text is hard to read"}
    ]
  }]
}
```


### Issue 1: "Annotations are not displayed"
**Cause**: The specified element is not included in the screenshot
**Solution prompt**:
```
Analyze the UI elements contained in the screenshot.
Tell me which elements can have annotations added, in a list.
```

### Issue 2: "Annotation position is wrong"
**Cause**: Element description is inaccurate
**Solution prompt**:
```
I want to specify the position of the element to annotate more precisely.
Can I specify by coordinates, like
"The button at approximately 100px from the left and 50px from the top of the screen"?
```

### Issue 3: "Arrow direction is reversed"
**Cause**: Arrow start and end points are ambiguous
**Solution prompt**:
```
Adjust the arrow direction.
Tell me how to explicitly specify the start and end points.
```

### Issue 4: "Text is hard to read"
**Cause**: Low contrast with the background color
**Solution prompt**:
```
Improve the visibility of annotation text.
Tell me how to adjust the background color, font size, and text color.
```

---

## ✅ Checkpoint
- [ ] Can highlight buttons with the red_box style
- [ ] Can add callout explanations with the callout style
- [ ] Can add step numbers with the number/circle style
- [ ] Can add annotations to multiple elements simultaneously
- [ ] Can place annotations that correctly guide the user's eye


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
      {"id": "next_window", "label": "Start in new window (/start-3-5)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-3-5
- finish → End

---
description: "When the user says /start-5-2 — Module 5 Lesson 5-2: PPTX Editing and Auto-generation"
chapter: "courses/aiagent/lesson03-core/module05-pptx"
prerequisites: ["start-5-1"]
duration: "~30 min"
level: "intermediate"
tags: ["pptx", "generation", "automation", "document"]
---

# 🎓 Lesson 5-2: PPTX Editing and Auto-generation

## 📍 What You'll Do

**Lesson 5-2: PPTX Editing and Auto-generation** !

| Item | Details |
|------|---------|
| Goal | Create new slides, edit text, and add shapes, tables, and images using python-pptx |
| Duration | ~30 min |
| Skills Used | pptx_ops, generate_slide, document-processor |
| Prerequisites | Lesson 5-1 completed, Python environment set up |
| Course Page | [Module 5: PPTX](https://ai-agent.camp/en/course/module-5) in parallel |

**Session flow:**
1. Add new slides and edit text
2. Add shapes, tables, and images
3. Auto-generate slides from templates

By the end of this session, you will be able to edit and generate PPTX files programmatically.

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

## 🚀 Step 1: Create New Presentation

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Create new presentation",
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
Create a new 16:9 presentation using python-pptx.
Add a title slide with the title "AI Agent Workshop",
subtitle "February 2026",
and save as ~/ai-agent-camp/output/new_presentation.pptx.
```

**Expected result**: A new PPTX file is created containing a title slide.

---

## 🚀 Step 2: Add Content Slides

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Add content slides",
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
Add content slides to the PPTX you just created with the following content:

Slide 2:
- Title: "Today's Agenda"
- Bullet points:
  1. What are AI Agents
  2. How to use Claude Code
  3. Hands-on Workshop
  4. Q&A

Slide 3:
- Title: "What are AI Agents"
- Bullet points:
  1. AI that autonomously executes tasks
  2. Understands user instructions and acts
  3. Can combine multiple tools
```

**Expected result**: A slide with bullet point format is added.

---

## 🚀 Step 3: Add Tables

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Add tables",
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
Add a new slide to the PPTX and create a table with the following data:

Title: "Feature Comparison"

| Feature | Claude Code | Traditional Tools |
|---------|------------|-------------------|
| Natural language | ◯ | △ |
| Code generation | ◯ | × |
| File operations | ◯ | △ |
| Learning curve | Low | High |

Apply bold to the header row with a readable style.
```

**Expected result**: A slide containing a table is added.

---

## 🚀 Step 4: Add Shapes and Design Elements

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Add shapes and design elements",
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
Add a new slide to the PPTX and add the following design elements:

- Title: "Workflow"
- 3 rectangles arranged horizontally
- Text "Input" "Process" "Output" in each rectangle
- Arrows placed between rectangles
- Background: Blue gradient

Make it a professional flow diagram design.
```

**Expected result**: A flow diagram using shapes is created.

---

## 🚀 Step 5: Auto-generate from Template

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Auto-generate from template",
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
Automatically generate a presentation from the following JSON data:

{
  "title": "Quarterly Report",
  "subtitle": "2026 Q1",
  "author": "Sales Department",
  "slides": [
    {
      "type": "content",
      "title": "Sales Results",
      "points": ["Target achievement: 115%", "Year-over-year: +20%", "New customers: 50"]
    },
    {
      "type": "content",
      "title": "Future Plans",
      "points": ["New product launch", "Global expansion", "DX promotion"]
    }
  ]
}

Output: ~/ai-agent-camp/output/quarterly_report.pptx
```

**Expected result**: A presentation is automatically generated from JSON data.

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
      {"id": "trouble_1", "label": "Layout index out of range"},
      {"id": "trouble_2", "label": "Japanese fonts not displayed"},
      {"id": "trouble_3", "label": "Image aspect ratio is distorted"},
      {"id": "trouble_4", "label": "Table cell widths are not equal"}
    ]
  }]
}
```


### Issue 1: "Layout index out of range"
**Cause**: The layout you are trying to use does not exist
**Solution prompt**:
```
Display all available layouts and their indices.
I want to check the prs.slide_layouts list.
```

### Issue 2: "Japanese fonts not displayed"
**Cause**: Font specification issue
**Solution prompt**:
```
Apply the Japanese font "Meiryo" to slide text.
Please show how to set paragraph.font.name = "Meiryo".
```

### Issue 3: "Image aspect ratio is distorted"
**Cause**: Both width and height are specified
**Solution prompt**:
```
When inserting an image, show how to insert while maintaining aspect ratio.
Please use the method of specifying width only.
```

### Issue 4: "Table cell widths are not equal"
**Cause**: Column widths are auto-calculated
**Solution prompt**:
```
Show how to explicitly set the width of each column in the table.
Please use the table.columns[i].width setting.
```

---

## ✅ Checkpoint
- [ ] Was able to create a new presentation
- [ ] Was able to add a title slide
- [ ] Was able to add bullet point content
- [ ] Was able to create and place a table
- [ ] Was able to place shapes (rectangles, arrows)
- [ ] Was able to auto-generate from JSON data
- [ ] Was able to save the file correctly


---

## 📋 Output Preview

### Expected Output
```
📁 output/
└── presentation.pptx  (PowerPoint presentation)
    Slide count: N slides
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/presentation.pptx

# Open in PowerPoint (macOS: open / Linux: xdg-open)
open output/presentation.pptx
```

> 💡 Check slide count: `python3 -c "from pptx import Presentation; p=Presentation('output/presentation.pptx'); print(f'Slide count: {len(p.slides)}')"`

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
      {"id": "next_window", "label": "Start in new window (/start-6-1)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-6-1
- finish → End

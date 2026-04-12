---
description: "When the user says /start-5-1 — Module 5 Lesson 5-1: PPTX Analysis"
chapter: "courses/aiagent/lesson03-core/module05-pptx"
duration: "~25 min"
prerequisites: ["start-0-1"]
level: "beginner"
tags: ["pptx", "analysis", "document"]
---

# 🎓 Lesson 5-1: PPTX Analysis

## 📍 What You'll Do

**Lesson 5-1: PPTX Analysis** !

| Item | Details |
|------|---------|
| Goal | Parse PPTX file structures and extract slide information, layouts, and text |
| Duration | ~25 min |
| Skills Used | pptx-analyzer, document-processor |
| Prerequisites | Python environment set up, having a sample PPTX file is recommended |
| Course Page | [Module 5: PPTX](https://ai-agent.camp/en/course/module-5) in parallel |

**Session flow:**
1. Check PPTX file structure
2. Extract slides, text, and shapes
3. Retrieve template information

By the end of this session, you will be able to handle PPTX structures programmatically.

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

## 🚀 Step 1: Verify Required Library Installation

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Verify required library installation",
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
Check if python-pptx is installed.
If not installed, run pip install python-pptx.
```

**Expected result**: python-pptx is installed and the version is displayed.

---

## 🚀 Step 2: Prepare Sample PPTX File

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Prepare sample PPTX file",
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
Check if you have a sample PowerPoint file.
If not, create a simple test PPTX file (about 3 slides).
```

> **Note**: Sample PPTX files may not exist in the `data/` directory. Use any `.pptx` file you have on hand, or ask the AI to generate a test PPTX file in `output/`.

**Expected result**: A sample PPTX file is prepared.

---

## 🚀 Step 3: Extract Basic PPTX Information

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Extract basic PPTX information",
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
Load the PPTX file in ~/ai-agent-camp/data/ and provide the following information:
- Total number of slides
- Layout name for each slide
- Number of shapes in each slide
- List of fonts used
```

**Expected result**: PPTX file structure information is displayed in JSON format.

---

## 🚀 Step 4: Detailed Analysis Per Slide

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Detailed analysis per slide",
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
Perform a detailed analysis of each slide in the PPTX file:
- Text content (including bullet points)
- Image size and position if present
- Number of rows and columns if a table is present
Save the results as a JSON file to ~/ai-agent-camp/output/pptx-analysis.json.
```

**Expected result**: Detailed analysis results are saved as a JSON file.

---

## 🚀 Step 5: Extract Template Information

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Extract template information",
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
Extract the slide master and layout information from the PPTX file:
- List of available layouts
- Placeholder information for each layout
- Theme color settings
Organize these as reusable template information.
```

**Expected result**: Template information is extracted and layout options become clear.

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
      {"id": "trouble_1", "label": "Cannot open PPTX file"},
      {"id": "trouble_2", "label": "Character encoding issues occur"},
      {"id": "trouble_3", "label": "Cannot retrieve image information"}
    ]
  }]
}
```


### Issue 1: "Cannot open PPTX file"
**Cause**: File path is incorrect, or the file is corrupted
**Solution prompt**:
```
Check if the PPTX file can be loaded correctly.
If an error occurs, identify the cause and solution.
```

### Issue 2: "Character encoding issues occur"
**Cause**: Encoding issue
**Solution prompt**:
```
Japanese text in the PPTX has character encoding issues.
Please explain how to save correctly with UTF-8 encoding.
```

### Issue 3: "Cannot retrieve image information"
**Cause**: Image is not correctly embedded within the shape
**Solution prompt**:
```
Cannot retrieve image information from the PPTX.
Please verify the hasattr(shape, 'image') check method.
```

---

## ✅ Checkpoint
- [ ] Was able to install python-pptx
- [ ] Was able to load a PPTX file
- [ ] Was able to retrieve basic slide information
- [ ] Was able to extract text and shape information
- [ ] Was able to retrieve layout and placeholder information
- [ ] Was able to save analysis results as JSON


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
      {"id": "next_window", "label": "Start in new window (/start-5-2)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-5-2
- finish → End

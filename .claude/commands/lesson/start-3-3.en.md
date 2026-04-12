---
description: "When the user says /start-3-3 — Module 3 Lesson 3-3: Automatic Tutorial Generation"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "~25 min"
level: "intermediate"
tags: ["screenshot", "tutorial", "documentation"]
---

# 🎓 Lesson 3-3: Automatic Tutorial Generation

## 📍 What You'll Do

**Lesson 3-3: Automatic Tutorial Generation** !

| Item | Details |
|------|---------|
| Goal | Automatically generate operation tutorials from screenshots using the tutorial-generator skill |
| Duration | ~25 min |
| Skills Used | tutorial-generator (Gemini Vision API) |
| Prerequisites | Lesson 3-1 completed, Gemini API key configured |
| Course Page | [Module 3: Screenshot Analysis](https://ai-agent.camp/en/course/module-3) in parallel |

**Session flow:**
1. Generate a login screen tutorial
2. Create multi-step tutorials
3. Output in manual format

By the end of this session, you will be able to generate operation manuals and onboarding documents.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 📁 Prepare Sample Images

This lesson uses screenshot images as input. Please prepare the following materials under `courses/aiagent/lesson03-core/module03-screenshot/practice/data/`:

- **login-screen.png** — A screenshot of any website's login screen
- **signup-form.png** — A screenshot of any registration form
- **purchase-step1~4.png** — Screenshots of each step in an e-commerce purchase flow (4 images)

> **Hint**: If you do not have screenshots available, prepare them using one of the following methods:
> - Take screenshots of any website and save them to `practice/data/tutorial-samples/` (macOS: `Cmd+Shift+4`, Windows: `Win+Shift+S`)
> - Auto-generate sample images using the nanobanana skill:
>   ```bash
>   uv run python tools/nanobanana.py --prompt "Login form screenshot with email and password fields and login button" --output courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login-screen.png
>   uv run python tools/nanobanana.py --prompt "Registration form with name, email, and password fields" --output courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/signup-form.png
>   ```
> - You can also use existing images in `practice/data/screenshots/` (`dashboard.png`, `ui-issue.png`, etc.) as alternatives
> - Assets not in `practice/` but needed for training should not be deleted; move them as official materials to the corresponding lesson's `practice/` or `final/` directory

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

## 🚀 Step 1: Generate Login Screen Tutorial

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Generate a login screen tutorial",
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
Use the tutorial-generator skill to generate a login screen tutorial.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login-screen.png
Output: output/tutorials/login-tutorial.html

Target audience: Beginners
Purpose: Explain the login procedure
Output format: HTML
```

> **Note**: When running scripts, set PYTHONPATH like `PYTHONPATH=. python skills/tutorial-generator/scripts/generate_tutorial.py ...`.

**Expected result**: A step-by-step login tutorial is generated in HTML format.

---

## 🚀 Step 2: Tutorial with Added Context Information

Add context information for more detailed explanations:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Tutorial with Added Context Information",
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
Generate a user registration screen tutorial.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/signup-form.png
Output: output/tutorials/signup-tutorial.html

Context information:
- This is a new user registration screen
- Enter email, password, and name to register
- Password must be 8+ characters
- Email verification is required

Create a detailed tutorial reflecting this information.
```

**Expected result**: A tutorial with detailed explanations reflecting the context information is generated.

---

## 🚀 Step 3: Generate Multi-Step Operation Flow

Generate tutorials spanning multiple screens, such as e-commerce purchase flows:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Generate a Multi-Step Operation Flow",
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
Create a purchase flow tutorial.

Process in the following screen order:
1. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step1.png - Product selection
2. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step2.png - Cart confirmation
3. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step3.png - Shipping address entry
4. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step4.png - Payment complete

Output: output/tutorials/purchase-tutorial.html

Explain each step's operations in detail
and compile everything into a single HTML document.
```

**Expected result**: A tutorial document with 4 consecutive steps is generated.

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
      {"id": "trouble_1", "label": "Tutorial is not generated"},
      {"id": "trouble_2", "label": "AI explanation is inaccurate"},
      {"id": "trouble_3", "label": "Japanese characters are garbled"},
      {"id": "trouble_4", "label": "Processing stops midway through multiple files"}
    ]
  }]
}
```


### Issue 1: "Tutorial is not generated"
**Cause**: The screenshot file format is not supported
**Solution prompt**:
```
Tell me the supported image file formats.
Also, check the format of the current screenshot.
```

### Issue 2: "AI explanations are inaccurate"
**Cause**: Context information is insufficient
**Solution prompt**:
```
What context information should be added
to improve the tutorial accuracy?
Please explain with specific examples.
```

### Issue 3: "Japanese text has character encoding issues"
**Cause**: Encoding issue
**Solution prompt**:
```
Check the character encoding of the generated HTML file.
Verify that it is correctly saved in UTF-8, and fix any issues.
```

### Issue 4: "Processing multiple files stops midway"
**Cause**: File not found or timeout
**Solution prompt**:
```
Check that all specified files exist.
Generate the tutorial using only the files that exist.
```

---

## ✅ Checkpoint
- [ ] Can automatically generate tutorials from screenshots
- [ ] Can generate detailed explanations using context information
- [ ] Can cover the entire multi-step operation flow
- [ ] HTML format tutorials display correctly
- [ ] Appropriate tutorials are generated in Japanese


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
      {"id": "next_window", "label": "Start in new window (/start-3-4)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-3-4
- finish → End

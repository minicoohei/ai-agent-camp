---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module01-banner"
duration: "~30 min"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["banner", "image", "gemini"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 1-1: Introduction to Banner Generation

## 📍 What You'll Do

Welcome to **Lesson 1-1: Introduction to Banner Generation**!

| Item | Details |
|------|---------|
| Goal | Create one X post banner using the banner-creator skill |
| Duration | ~30 min |
| Skills Used | banner-creator (Gemini Image Generation API) |
| Prerequisites | Gemini API key configured, Python environment set up |
| Course Page | Refer to [Module 1: Banner & Image Generation](https://ai-agent.camp/en/course/module-1) in parallel |

**Session flow:**
1. Understand X post banner sizes
2. Generate your first banner
3. Practice with 3 different topics

By the end of this session, your generated banner images will be saved in the outputs folder.

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

## 🚀 Step 1: Understand X Post Banner Sizes

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Understand X Post Banner Sizes",
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
Tell me the recommended sizes for X (Twitter) post banners and the differences in image sizes across social media platforms.
```

**Expected result**: The recommended size for X posts (1200x675px, 16:9) and differences from other platforms are explained.

---

## 🚀 Step 2: Generate Your First Banner

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Generate Your First Banner",
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
Use banner-creator to create a banner for X posts.
Topic: "Boosting Business Efficiency with AI"
Style: Modern, business-oriented
Output: docs/generated/banners/banner-1-1.png
```

**Expected result**: A banner image is generated in the `docs/generated/banners/` folder.

---

## 🚀 Step 3: Practice with Different Topics

Create banners with different topics using the following prompts:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Practice with Different Topics",
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
Create X post banners for the following 3 topics:
1. "Weekend-Only Sale Now On"
2. "New Service Launch Campaign"
3. "We're Hiring: Engineers Wanted"

Save each with a different file name.
```

**Expected result**: Three different banners are generated, with designs varying by topic.

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
      {"id": "trouble_1", "label": "\"Module not found\" error"},
      {"id": "trouble_2", "label": "Image is not generated"},
      {"id": "trouble_3", "label": "Not happy with the design"},
      {"id": "trouble_4", "label": "API error occurs"}
    ]
  }]
}
```


### Issue 1: "Module not found" error
**Cause**: Required Python packages are not installed
**Solution prompt**:
```
Install the packages required to run banner-creator.
Run `uv add pillow requests`.
```

### Issue 2: "Image is not generated"
**Cause**: Output directory does not exist or permission issue
**Solution prompt**:
```
Check if the docs/generated/banners/ directory exists, and create it if it doesn't.
```

### Issue 3: "Not happy with the design"
**Cause**: Topic description is too abstract
**Solution prompt**:
```
Regenerate with a more specific topic:
"Boosting Business Efficiency with AI" → "Automate 80% of customer inquiries with an AI chatbot"
```

### Issue 4: "API error occurs"
**Cause**: Gemini API key is not set or rate limit reached
**Solution prompt**:
```
Verify that the Gemini API key is correctly configured.
Check whether the environment variable GEMINI_API_KEY is set (not empty).
* For security, do not display the actual key value.
```

---

## ✅ Checkpoint
- [ ] Understood the recommended sizes for X post banners
- [ ] Successfully generated a banner using banner-creator
- [ ] Image files saved in the `docs/generated/banners/` folder
- [ ] Completed the practice exercise (3 banners)


---

## 📋 Output Preview

### Expected Output
```
📁 docs/generated/banners/
├── banner-{theme-name}.png
└── (variations)
```
> Format: PNG | Size: Auto-configured

### Verification Commands
```bash
# File listing
ls -la docs/generated/banners/

# Open images (macOS: open / Linux: xdg-open)
open docs/generated/banners/
```

> 💡 **Claude Code**: Specify the file path with the Read tool to preview images in chat
> 💡 **Cursor**: Click on the image in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that banner images have been generated in the docs/generated/banners/ folder.
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
      {"id": "next_window", "label": "Start in a new window (/start-1-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-1-2
- finish → End

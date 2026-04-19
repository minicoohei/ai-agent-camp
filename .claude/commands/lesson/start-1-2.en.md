---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module01-banner"
prerequisites: ["start-1-1"]
duration: "~30 min"
level: "beginner"
tags: ["banner", "image", "sns", "multi-platform"]
---

# 🎓 Lesson 1-2: Advanced Banners (Instagram, Facebook)

## 📍 What You'll Do

Welcome to **Lesson 1-2: Advanced Banners (Instagram, Facebook)**!

| Item | Details |
|------|---------|
| Goal | Batch-generate banners optimized for X, Instagram, and Facebook |
| Duration | ~30 min |
| Skills Used | banner-creator (multi-platform support) |
| Prerequisites | Lesson 1-1 completed, Gemini API key configured |
| Course Page | Refer to [Module 1: Banner & Image Generation](https://ai-agent.camp/en/course/module-1) in parallel |

**Session flow:**
1. Review sizes for each platform
2. Batch-generate banners for 3 platforms
3. Verify design consistency
4. Practice with a different campaign

By the end of this session, banners for multiple social media platforms will be saved in outputs.

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

## 🚀 Step 1: Review Sizes for Each Platform

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Review Sizes for Each Platform",
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
Show me the recommended banner sizes for X, Instagram, and Facebook posts in table format.
Include the aspect ratio and use case.
```

**Expected result**: A table like the following is displayed:
| Platform | Size | Aspect Ratio |
|----------|------|-------------|
| X | 1200x675px | 16:9 |
| Instagram | 1080x1080px | 1:1 |
| Facebook | 1200x630px | 1.91:1 |

---

## 🚀 Step 2: Batch-Generate Banners for 3 Platforms

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Batch-Generate Banners for 3 Platforms",
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
Create banners for the following 3 platforms with the topic "Summer Sale Event":

1. For X (1200x675px)
2. For Instagram (1080x1080px)
3. For Facebook (1200x630px)

Save them as banner-1-2-x.png, banner-1-2-ig.png, and banner-1-2-fb.png respectively.
```

**Expected result**: Three banners of different sizes are generated, each optimized for its platform.

---

## 🚀 Step 3: Verify Design Consistency

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Verify Design Consistency",
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
Review the 3 banners just created.
Check whether design consistency (colors, fonts, messaging) is maintained,
and point out any areas for improvement.
```

**Expected result**: Brand consistency across the 3 banners is evaluated, with improvement suggestions provided as needed.

---

## 🚀 Step 4: Practice with a Different Campaign

Create a banner set for a different campaign using the following prompts:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Practice with a Different Campaign",
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
Create a banner set for X, Instagram, and Facebook with the topic
"New Product Launch - Exclusive Bonus for the First 100 Customers."
Style: Luxurious, premium feel
Colors: Gold and black base
```

**Expected result**: Banners for 3 platforms are generated with a unified design theme.

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
      {"id": "trouble_1", "label": "Platform name not recognized"},
      {"id": "trouble_2", "label": "Error during batch generation"},
      {"id": "trouble_3", "label": "Designs lack consistency"},
      {"id": "trouble_4", "label": "Instagram square layout is broken"}
    ]
  }]
}
```


### Issue 1: "Platform name not recognized"
**Cause**: Incorrect platform name specified
**Solution prompt**:
```
Show me the list of available platform names for banner-creator.
Check with the --help option.
```

### Issue 2: "Error during batch generation"
**Cause**: API error or file write error occurred midway
**Solution prompt**:
```
Run banner generation one at a time to identify which platform causes the error.
Display the error message.
```

### Issue 3: "Designs lack consistency"
**Cause**: Prompt interpreted separately for each platform
**Solution prompt**:
```
Unify the following across all 3 banners:
- Main color: #FF6B00 (orange)
- Font: Modern sans-serif
- Catchphrase: Same text
```

### Issue 4: "Instagram square layout is broken"
**Cause**: Landscape design forced into a square format
**Solution prompt**:
```
Regenerate the Instagram banner with a layout optimized for square (1:1).
Center the text and provide ample margins.
```

---

## ✅ Checkpoint
- [ ] Understood the recommended sizes for each platform
- [ ] Generated banners for X, Instagram, and Facebook
- [ ] Verified design consistency
- [ ] Completed the practice exercise (banner set for a different campaign)


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
      {"id": "next_window", "label": "Start in a new window (/start-1-3)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-1-3
- finish → End

---
description: "When the user says /start-1-3 — Module 1 Lesson 1-3: nanobanana Image Editing"
chapter: "courses/aiagent/lesson03-core/module01-banner"
prerequisites: ["start-1-1"]
duration: "~30 min"
level: "beginner"
tags: ["image", "nanobanana", "gemini", "editing"]
---

# 🎓 Lesson 1-3: nanobanana Image Editing

## 📍 What You'll Do

Welcome to **Lesson 1-3: nanobanana Image Editing**!

| Item | Details |
|------|---------|
| Goal | Generate images from text and edit existing images using the nanobanana skill |
| Duration | ~30 min |
| Skills Used | nanobanana (Gemini Image Generation API) |
| Prerequisites | Lesson 1-1 completed, Gemini API key configured |
| Course Page | Refer to [Module 1: Banner & Image Generation](https://ai-agent.camp/en/course/module-1) in parallel |

**Session flow:**
1. Generate images from text
2. Generate images of specific scenes
3. Edit existing images (optional)

By the end of this session, generated and edited images will be saved in outputs.

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

## 🚀 Step 1: Generate Images from Text

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Generate Images from Text",
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
Use nanobanana to generate the following image:
- Style: Flat design
- Theme: Teamwork
- Purpose: Business presentation
Output: ~/ai-agent-camp/output/nanobanana-teamwork.png
```

**Expected result**: A flat-design image themed around teamwork is generated.

---

## 🚀 Step 2: Generate Images of Specific Scenes

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Generate Images of Specific Scenes",
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
Generate a "modern office scene" image with nanobanana.
Conditions:
- Flat design, minimal
- Bright color tones
- Include a desk, indoor plants, and windows
Output: ~/ai-agent-camp/output/nanobanana-office.png
```

**Expected result**: An office image meeting the specified conditions is generated.

---

## 🚀 Step 3: Edit Existing Images

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Edit Existing Images",
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
Edit the office image generated earlier (nanobanana-office.png):
- Change the background to a sunset sky
- Add warm lighting effects
Output: ~/ai-agent-camp/output/nanobanana-office-sunset.png
```

**Expected result**: An image based on the original is generated with the background changed to a sunset sky.

---

## 🚀 Step 4: Generate Logo-Style Images and Icons

Create business-ready images using the following prompts:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Generate Logo-Style Images and Icons",
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
Generate the following 2 images with nanobanana:

1. A coffee shop logo-style image
   - Simple, flat design
   - Coffee cup silhouette
   - Output: ~/ai-agent-camp/output/logo-coffee.png

2. An icon representing an AI agent
   - Tech feel, futuristic
   - Blue and white base colors
   - Output: ~/ai-agent-camp/output/icon-ai.png
```

**Expected result**: A logo-style image and an icon are generated.

---

## 🚀 Step 5: Compare Different Styles

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Compare Different Styles",
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
Generate images on the theme "Growing Business" in 3 different styles:

1. Flat design (simple, minimal)
2. 3D illustration style (dimensional, pop)
3. Watercolor style (hand-drawn feel, warm)

Save each as a separate file.
```

**Expected result**: Three images with the same theme but different styles are generated for comparison.

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
      {"id": "trouble_1", "label": "Generated image differs from expectations"},
      {"id": "trouble_2", "label": "Image edits not reflected"},
      {"id": "trouble_3", "label": "API rate limit error"},
      {"id": "trouble_4", "label": "Logo is too complex"}
    ]
  }]
}
```


### Issue 1: "Generated image differs from expectations"
**Cause**: Prompt is too abstract
**Solution prompt**:
```
Rewrite your prompt more specifically:
Bad example: "a beautiful image"
Good example: "A family having a picnic on green grass under a blue sky,
             flat design, bright color tones, 16:9 aspect ratio"
```

### Issue 2: "Image edits not reflected"
**Cause**: Edit instructions are unclear, or input image path is wrong
**Solution prompt**:
```
Verify the input image path:
ls ~/ai-agent-camp/output/nanobanana-office.png

If the file exists, make the edit instructions more specific:
"Change background only" "Keep the subject"
```

### Issue 3: "API rate limit error"
**Cause**: Too many requests sent in a short time
**Solution prompt**:
```
API rate limit reached.
Wait about 1 minute and try again.
For continuous generation, add a 5-second wait between each request.
```

### Issue 4: "Logo is too complex"
**Cause**: Insufficient specification of simplicity
**Solution prompt**:
```
Regenerate the logo with simpler constraints:
- Maximum 3 colors
- Single symbol only
- No text
- Transparent or solid color background
```

---

## ✅ Checkpoint
- [ ] Generated images from text
- [ ] Generated images with specific conditions
- [ ] Edited existing images
- [ ] Generated logo-style images and icons
- [ ] Generated images of the same theme in different styles for comparison


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
      {"id": "next_window", "label": "Start in a new window (/start-2-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-2-1
- finish → End

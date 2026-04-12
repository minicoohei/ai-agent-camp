---
description: "When the user says /start-17-1 — Module 17 Lesson 17-1: X post & banner creation"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "~30 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "x-post", "banner", "sns"]
---

# Lesson 17-1: X Post & Banner Creation

## What You Will Do in This Session

Welcome to **Lesson 17-1: X Post & Banner Creation**!

| Item | Details |
|------|---------|
| Goal | Create X post text and a banner using the social-content + banner-creator skills |
| Duration | ~30 min |
| Skills used | social-content, banner-creator (Gemini Image Generation API) |
| Prerequisites | Gemini API key configured |
| Course page | Refer to [Module 17: Marketing](https://ai-agent.camp/en/course/module-17) in parallel |

**Session flow:**
1. Understand X post best practices (posting times, hashtags, character limits)
2. Create 3 X post text patterns using the social-content skill
3. Create an X post banner with banner-creator (1200x675px)

By the end of this session, 3 X post text patterns and 1 banner image will be complete.

> **Tip**: If the AI response stops midway, type "please continue" to resume.

---

## Readiness Check

First, confirm that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "Pre-session check",
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

(ready -> Go to Step 1)
(check_prereq -> Run prerequisite check)
(view_html -> Show the course page path)
(different_lesson -> Show module list)

---

## Step 1: Understand X Post Best Practices

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Understand X post best practices",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Explain best practices for X (Twitter) posts.
Cover the following:
- Optimal posting times
- Effective use of hashtags (count, selection)
- Character limits (140 vs 280 characters) and ideal length
- Techniques to boost engagement
```

**Expected result**: Optimal posting times, hashtag strategies, and character count best practices for X posts are explained.

---

## Step 2: Create 3 X Post Text Patterns with social-content

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Create 3 X post text patterns",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Use the social-content skill to create 3 X post text patterns on the following topic:
Topic: "Cursor Bootcamp - AI Agent Training"
Target: Business professionals, non-engineers
Tone: Friendly and engaging

Pattern 1: Question type ("Are you still doing...?")
Pattern 2: Results/numbers type ("X% efficiency improvement")
Pattern 3: Story type (testimonial style)

Include hashtags for each pattern.
```

**Expected result**: 3 X post text patterns are generated, each with a different approach.

---

## Step 3: Create an X Post Banner with banner-creator

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Create an X post banner",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Use banner-creator to create a banner for X posts.
Topic: "Cursor Bootcamp - 10x Your Productivity with AI"
Platform: x_post (1200x675px)
Style: Modern, tech-oriented, business-focused
Output: ~/ai-agent-camp/outputs/marketing-12-1-banner.png
```

**Expected result**: A 1200x675px X post banner image is generated in the outputs folder.

---

## Common Issues and Solutions

**AskQuestion configuration:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "API error occurs"},
      {"id": "trouble_2", "label": "Post text is too long"},
      {"id": "trouble_3", "label": "Banner size is wrong"},
      {"id": "trouble_4", "label": "Image is not generated"}
    ]
  }]
}
```

### Issue 1: "API error occurs"
**Cause**: Gemini API key is not set or rate limited
**Solution**:
```
Verify that the Gemini API key is correctly configured.
Check the GEMINI_API_KEY environment variable value.
If rate limited, wait about 30 seconds and retry.
```

### Issue 2: "Post text is too long"
**Cause**: Exceeds X post 280-character limit
**Solution**:
```
Shorten the generated text to fit within 280 characters.
Note that hashtags count toward the character limit.
```

### Issue 3: "Banner size is wrong"
**Cause**: Incorrect platform specification
**Solution**:
```
Specify the --platform option as "x_post" in banner-creator.
This will automatically generate at 1200x675px (16:9).
```

### Issue 4: "Image is not generated"
**Cause**: The outputs directory does not exist or permission issue
**Solution**:
```
Check if the outputs directory exists; create it if not.
mkdir -p ~/ai-agent-camp/outputs
```

---

## Checkpoint
- [ ] Understood X post best practices (posting times, hashtags, character limits)
- [ ] Created 3 X post text patterns using the social-content skill
- [ ] Generated 1 X post banner (1200x675px) with banner-creator
- [ ] Banner image file is saved in the outputs folder

---

## Deliverables Preview

### Expected output
```
output/marketing/
  banner-*.png
  (variations)
```
> Format: PNG | Size: auto-configured

### Verification commands
```bash
# File list
ls -la output/marketing/

# Open image (macOS: open / Linux: xdg-open)
open output/marketing/
```

> **Claude Code**: Specify the file path with the Read tool to preview images in chat
> **Cursor**: Click images in the file explorer to preview

---

## Completion Check
Paste the following into the Cursor chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the outputs/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## Next Steps

This section is complete. Start the next section or open a new window to begin.

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Open in new window (/start-17-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection guide (example)**:
- next_auto -> /next_lesson
- next_window -> Open /start-17-2 in a new window
- finish -> End

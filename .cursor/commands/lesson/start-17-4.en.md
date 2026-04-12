---
description: "When the user says /start-17-4 — Module 17 Lesson 17-4: Design mockups with Pencil MCP"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "~35 min"
prerequisites: ["start-17-3"]
level: "intermediate"
tags: ["marketing", "pencil", "design", "mockup"]
---

# Lesson 17-4: Design Mockups with Pencil MCP

## What You Will Do in This Session

Welcome to **Lesson 17-4: Design Mockups with Pencil MCP**!

| Item | Details |
|------|---------|
| Goal | Create marketing banner design mockups with Pencil MCP |
| Duration | ~35 min |
| Skills used | Pencil MCP (get_editor_state, batch_design, get_screenshot) |
| Prerequisites | Pencil MCP enabled |
| Course page | Refer to [Module 17: Marketing](https://ai-agent.camp/en/course/module-17) in parallel |

> **Tool info**: This lesson uses Pencil MCP. It is available in both Cursor IDE and Claude Code (CLI/Desktop). In some environments like Codex CLI, you may get a `request_user_input is not supported` error. If so, refer to the "Alternative Workflow" section.

**Session flow:**
1. Understand Pencil MCP basics (get_editor_state, batch_design)
2. Create an ad banner mockup
3. Capture with get_screenshot and save to output/pencil/

By the end of this session, 1 banner design mockup and an image capture will be complete.

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

## Step 1: Understand Pencil MCP Basics

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Understand Pencil MCP basics",
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
Explain the basic operations of Pencil MCP. Describe how to use the following tools:

1. get_editor_state() - Get the current editor state
2. open_document() - Create a new document or open an existing one
3. batch_design() - Insert, update, or delete design elements
   - I() (Insert): Insert new elements
   - U() (Update): Update existing elements
   - D() (Delete): Delete elements
4. get_screenshot() - Get a screenshot of the design
5. batch_get() - Get node information

Explain the basic usage and parameters for each.
```

**Expected result**: Usage and parameters for the 5 main Pencil MCP tools are explained.

---

## Step 2: Create an Ad Banner Mockup

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Create an ad banner mockup",
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
Use Pencil MCP to create an ad banner mockup with the following specifications.

Steps:
1. mkdir -p output/pencil
2. open_document("output/pencil/marketing-banner.pen") to create a .pen file
3. Design the banner with the following specifications

Banner specifications:
- Size: 1200x628px (Facebook/Instagram ad size)
- Theme: "Cursor Bootcamp" promotion
- Copy:
  - Main copy: "Transform Your Work with AI"
  - Sub copy: "AI Agent Training for Non-Engineers"
  - CTA: "Sign Up Now"
- Design:
  - Background: Gradient (dark blue -> purple)
  - Text: White, main copy in bold and larger size
  - CTA button: Orange rounded button
  - Logo placement: Cursor Bootcamp logo text in bottom right
```

**Expected result**: An ad banner mockup is created in the Pencil MCP editor.

---

## Step 3: Capture with get_screenshot and Save

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Capture screenshot and save",
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
Get a screenshot of the created banner mockup and save it to the following path:

Output: output/pencil/marketing-banner-mockup.png
Design file: output/pencil/marketing-banner.pen (created in Step 2)

Steps:
1. Use get_screenshot() to capture the mockup
2. Save the image to output/pencil/marketing-banner-mockup.png
3. Verify the saved file path and size

Also provide 3 design feedback points
(from perspectives such as color scheme, layout, and typography).
```

**Expected result**: Banner mockup image is saved in output/pencil/ and improvement points are presented.

---

## Alternative Workflow (Non-GUI Environments)

In environments where Pencil MCP is unavailable (Claude Code, Codex CLI, SSH, etc.), create mockups directly with HTML + Tailwind CSS.

1. Create the `output/pencil/` directory
2. Create a banner mockup with HTML + Tailwind CSS CDN:
   ```bash
   mkdir -p output/pencil
   ```
3. Implement the banner design in `output/pencil/marketing-banner-mockup.html`
   - Use `<script src="https://cdn.tailwindcss.com"></script>`
   - Apply the same banner specifications from Step 2 (size, copy, colors)
4. Open in a browser to take a screenshot, or capture with Playwright:
   ```bash
   npx playwright screenshot output/pencil/marketing-banner-mockup.html output/pencil/marketing-banner-mockup.png
   ```

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
      {"id": "trouble_1", "label": "Cannot connect to Pencil MCP"},
      {"id": "trouble_2", "label": "batch_design returns an error"},
      {"id": "trouble_3", "label": "Cannot get screenshot"},
      {"id": "trouble_4", "label": "Design does not match intent"}
    ]
  }]
}
```

### Issue 1: "Cannot connect to Pencil MCP"
**Cause**: Pencil MCP server is disabled
**Solution**:
```
Verify that Pencil MCP is enabled.
Check the MCP server status in Cursor settings and
confirm that the user-pencil server is enabled.
```

### Issue 2: "batch_design returns an error"
**Cause**: Incorrect operation syntax or wrong parent node ID
**Solution**:
```
Check the batch_design operation syntax.
First get the current state with get_editor_state() and
verify valid node IDs before executing operations.
Write one operation per line:
Example: foo=I("parent", { ... })
```

### Issue 3: "Cannot get screenshot"
**Cause**: No document is open in the editor
**Solution**:
```
Check the current editor state with get_editor_state().
If no document is open,
create a new document with open_document("new").
```

### Issue 4: "Design does not match intent"
**Cause**: Design instructions are not specific enough or node placement is off
**Solution**:
```
Check the current layout with snapshot_layout and
understand the position and size of each node.
Then use U() (Update) operations to adjust position and style.
Iteratively adjusting while checking results with get_screenshot is effective.
```

---

## Checkpoint
- [ ] Understood Pencil MCP basics (get_editor_state, batch_design, get_screenshot)
- [ ] Created an ad banner mockup with Pencil MCP
- [ ] Captured a screenshot with get_screenshot
- [ ] Banner mockup image is saved in output/pencil/

---

## Deliverables Preview

### Expected output
```
output/pencil/
  marketing-banner.pen             <- Pencil design file (main)
  marketing-banner-mockup.png      <- Screenshot (1200x628px)
  marketing-banner-mockup.html     (alternative: HTML version)
```
> Format: PNG | Size: 1200x628px (Facebook/Instagram ad size)

### Verification commands
```bash
# Check .pen file and screenshot
ls -lh output/pencil/marketing-banner.pen
ls -lh output/pencil/marketing-banner-mockup.png

# Open image (macOS: open / Linux: xdg-open)
open output/pencil/marketing-banner-mockup.png
```

> **Claude Code**: `Read output/pencil/marketing-banner-mockup.png` for in-chat preview
> **Cursor**: Click images in the file explorer to preview
> **.pen files**: Use Pencil MCP's `batch_get` or `get_screenshot` to inspect contents

---

## Completion Check
Paste the following into the Cursor chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## Next Steps

All lessons in Module 17: Marketing are now complete!

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select the next action",
    "options": [
      {"id": "next_module", "label": "Start the next module (/start-18-1)"},
      {"id": "review_module", "label": "Review Module 17"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection guide (example)**:
- next_module -> /start-18-1 to begin the Requirements/System Development module
- review_module -> Review each lesson in Module 17
- finish -> End

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
prerequisites: ["start-13-2", "setup-pencil"]
duration: "~30 min"
level: "intermediate"
tags: ["lp", "pencil", "design", "mockup"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 13-3: Create Design File (Pencil MCP)

## 📍 What You'll Do

Welcome to **Lesson 13-3: Create Design File**!

| Item | Details |
|------|---------|
| Goal | Create a Landing Page/Website design file (.pen) using Pencil MCP |
| Duration | ~30 min |
| Skills Used | lp-designer, Pencil MCP (user-pencil) |
| Prerequisites | Lesson 13-2 complete (output/lp-wireframe.txt exists), Pencil MCP set up (/setup-pencil) |
| Course Page | Refer to [Module 13: Landing Page/Website Design](https://ai-agent.camp/en/course/module-13) in parallel |

> **💡 Tool Info**: This lesson uses Pencil MCP. It is available in the current workspace and in Claude Code (CLI/Desktop). In some environments like Codex CLI, you may see a `request_user_input is not supported` error. In that case, refer to the "Alternative Workflow" section.

**Session flow:**
1. Create design file at `output/lp/lp-design.pen` with Pencil
2. Retrieve Landing Page design guidelines
3. Apply style guide
4. Create design for each section
5. Review design and export screenshots

By the end of this session, a professional-quality design file will be complete.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. Responses may pause depending on the tool, but this is not a malfunction.

---

## 🎯 Readiness Check

First, let's confirm everything is ready.

**AskQuestion settings:**
```json
{
  "title": "🎯 Pre-Session Check",
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

(ready → Proceed to Step 1)
(check_prereq → Check Pencil MCP connection)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Create New Pencil Document

Create a new .pen file with Pencil MCP.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Create Pencil Document",
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

**Post-selection instructions (example)**:
Input:
```text
Create a new document for Landing Page design with Pencil MCP.

Steps:
1. Create destination directory with mkdir -p output/lp
2. Check current state with get_editor_state()
3. Create .pen file with open_document("output/lp/lp-design.pen")
4. Confirm the file is open

Destination: output/lp/lp-design.pen
```

**Expected result**: A design file is created and opened at `output/lp/lp-design.pen`.

---

## 🚀 Step 2: Retrieve Landing Page Design Guidelines

Retrieve Pencil's Landing Page design guidelines.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Design Guidelines",
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

**Post-selection instructions (example)**:
Input:
```text
Retrieve Landing Page design guidelines from Pencil MCP.

Steps:
1. Get Landing Page design rules with get_guidelines(topic="landing-page")
2. Summarize key points of the guidelines
3. Highlight especially important rules (layout, typography, color)

We will follow these guidelines for the design.
```

**Expected result**: Landing Page design rules and best practices are displayed.

---

## 🚀 Step 3: Apply Style Guide

Select and apply a style guide matching the design tone.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Style Guide Selection",
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

**Post-selection instructions (example)**:
Input:
```text
Read the design tone from output/lp-brief.md and apply a style guide
using Pencil MCP.

Steps:
1. Get tag list with get_style_guide_tags
2. Select tags matching the brief's design tone
3. Get style with get_style_guide(tags=["landing-page", "{tone}", "{category}"])
4. Review the style's color scheme, fonts, and layout patterns

Summarize the selected style overview.
```

**Expected result**: A style guide matching the design tone is applied.

---

## 🚀 Step 4: Create Section Designs

Create each section using batch_design.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 4: Section Design",
  "questions": [{
    "id": "design_approach",
    "prompt": "Select the design approach",
    "options": [
      {"id": "all_at_once", "label": "Create all sections at once"},
      {"id": "step_by_step", "label": "Create one section at a time with review"},
      {"id": "hero_first", "label": "Create only the Hero section first"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Reference output/lp-brief.md and output/lp-wireframe.txt,
and create the Landing Page design using Pencil MCP's batch_design.

Create the following sections in order:

1. **Hero Section**
   - Background: gradient or image
   - Headline (H1): Use copy from the brief
   - Subheadline
   - CTA button (prominent color, rounded corners)
   - Hero image or mockup

2. **Pain Points Section**
   - Section title
   - 3 challenge cards (icon + text)

3. **Solution Section**
   - Left: explanation text (3 benefits)
   - Right: service screenshot or illustration

4. **Features Section**
   - Section title
   - 3-4 feature cards (icon + title + description)

5. **Social Proof Section**
   - Testimonial cards (photo + name + company + comment)
   - Star rating

6. **FAQ Section**
   - Accordion-style Q&A, 3-5 items

7. **Final CTA Section**
   - Background color
   - Headline + CTA button

8. **Footer**
   - Link groups + copyright

Verify each section with get_screenshot after creation.
```

**Expected result**: A .pen file with all sections designed is complete.

---

## 🚀 Step 5: Review and Adjust Design

Visually review the completed design.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 5: Design Review",
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

**Post-selection instructions (example)**:
Input:
```text
Get a screenshot of the entire design with Pencil MCP's get_screenshot
and review from the following perspectives:

1. **Consistency**: Do colors, fonts, and spacing match the style guide?
2. **Visual hierarchy**: Are headlines prominent and CTAs easy to find?
3. **Whitespace**: Is spacing between sections appropriate?
4. **Contrast**: Is text readability sufficient?
5. **CTA**: Are buttons prominent and clickable?

If there are issues, fix with batch_design and verify again with get_screenshot.

Finally, save a screenshot of the completed design:
1. mkdir -p output/lp/design
2. Get full-page screenshot with get_screenshot()
3. Save to output/lp/design/lp-full.png
```

**Expected result**: The design is reviewed, adjusted, and a screenshot is saved to `output/lp/design/lp-full.png`.

---

## 🔄 Alternative Workflow (For Non-GUI Environments)

In environments where Pencil MCP is not available (Claude Code, Codex CLI, SSH, etc.), create the design mockup directly with HTML + Tailwind CSS.

1. Reference `output/lp-wireframe.txt` and `output/lp-brief.md` to confirm design requirements
2. Implement mockup directly with HTML + Tailwind CSS CDN in `output/lp-project/`:
   ```bash
   mkdir -p output/lp-project
   ```
3. Create each section (Hero, Pain Points, Solution, Features, Social Proof, FAQ, CTA, Footer) in HTML
4. Apply style guide equivalent colors, fonts, and spacing with Tailwind utility classes
5. Use the completed HTML file as the deliverable instead of a .pen file, and proceed directly to 13-4

> With this method, you can skip the ".pen file prerequisite" steps in 13-4 and work directly on HTML implementation.

---

## ⚠️ Common Issues and Solutions

In Codex, you typically present choices in chat so the user can select their issue and get guidance instantly.

**AskQuestion settings example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "Cannot connect to Pencil MCP"},
      {"id": "trouble_2", "label": "batch_design throws an error"},
      {"id": "trouble_3", "label": "Style guide not found"},
      {"id": "trouble_4", "label": "Design appears broken"}
    ]
  }]
}
```

### Issue 1: Cannot connect to Pencil MCP
**Solution**: Check that user-pencil is enabled in Cursor's MCP settings. You can verify under Settings → MCP Servers.

### Issue 2: batch_design throws an error
**Solution**: Check that the operation syntax is correct. You can get the latest syntax rules with `get_guidelines`.

### Issue 3: Style guide not found
**Solution**: Check available tags with `get_style_guide_tags` and select the closest match.

### Issue 4: Design appears broken
**Solution**: Check the layout structure with `snapshot_layout` and adjust node placement.

---

## ✅ Checkpoint
- [ ] `output/lp/lp-design.pen` has been created
- [ ] Landing Page design guidelines have been reviewed
- [ ] Style guide has been applied
- [ ] All sections (Hero through Footer) are designed
- [ ] Screenshot saved to `output/lp/design/lp-full.png`


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/lp/
├── lp-design.pen          ← Pencil design file (main)
└── design/
    └── lp-full.png        ← Design screenshot
```

### Verification Commands
```bash
# Check .pen file existence
ls -lh output/lp/lp-design.pen

# Check screenshots
ls -la output/lp/design/

# Open image (macOS: open / Linux: xdg-open)
open output/lp/design/lp-full.png
```

> 💡 **Claude Code**: `Read output/lp/design/lp-full.png` for in-chat preview
> 💡 **Cursor**: Click the image in the file explorer to preview
> 💡 **.pen file**: Use Pencil MCP's `batch_get` or `get_screenshot` to inspect contents

---

## ✅ Completion Check
Paste the following in chat to verify completion:

```text
Check if the following files exist:
1. output/lp/lp-design.pen (Pencil design file)
2. output/lp/design/lp-full.png (screenshot)

Also, check the current document state with get_editor_state()
and display a list of created sections (nodes).
```

**Expected result**: Existence of .pen file and screenshot is confirmed, and design element list is displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin.

In Codex, you can typically select from choices in chat.

**AskQuestion settings example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (LP Implementation)"},
      {"id": "next_window", "label": "Open /start-13-4 in a new window"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → Run /start-13-4
- next_window → Open /start-13-4 in a new window
- finish → End

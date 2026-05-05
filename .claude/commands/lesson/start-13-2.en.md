---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
prerequisites: ["start-13-1"]
duration: "~25 min"
level: "intermediate"
tags: ["lp", "wireframe", "design", "information-architecture"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 13-2: Wireframe Creation (ASCII + Visual WF)

## 📍 What You'll Do

Welcome to **Lesson 13-2: Wireframe Creation**!

| Item | Details |
|------|---------|
| Goal | Design the Landing Page/Website section structure using ASCII WF and visual WF |
| Duration | ~25 min |
| Skills Used | lp-designer, diagram-generator |
| Prerequisites | Lesson 13-1 complete (output/lp-brief.md exists) |
| Course Page | Refer to [Module 13: Landing Page/Website Design](https://ai-agent.camp/en/course/module-13) in parallel |

**Session flow:**
1. Load brief and confirm sections
2. Create ASCII wireframe
3. Generate visual WF with diagram-generator
4. Review information architecture between sections

By the end of this session, the Landing Page structural design will be complete.

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
(check_prereq → Check for output/lp-brief.md existence)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Load Brief

Review the brief created in 13-1.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Load Brief",
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
Load output/lp-brief.md and verify the following:

1. Is the section structure clear?
2. Is the necessary content defined for each section?
3. Is the logical flow between sections appropriate?

Display the verification results as a summary.
```

**Expected result**: The brief contents are displayed as a summary.

---

## 🚀 Step 2: Create ASCII Wireframe

Design the Landing Page structure using text-based wireframes.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: ASCII Wireframe",
  "questions": [{
    "id": "wf_style",
    "prompt": "Select the wireframe style",
    "options": [
      {"id": "single_column", "label": "Single column (for simple Landing Pages)"},
      {"id": "two_column", "label": "Two-column layout (text + image side by side)"},
      {"id": "card_grid", "label": "Card grid (for feature showcases)"},
      {"id": "full_width", "label": "Full width (impact-focused)"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Create an ASCII wireframe based on the section structure in output/lp-brief.md.

Format:
- Use box-drawing characters (┌─┐│└─┘)
- Visually represent width/height ratios for each section
- Show text placement, image placement, and button positions with [ ]
- Include responsive layout changes

Output to: output/lp-wireframe.txt

Include the following sections:
1. Header / Navigation
2. Hero section
3. Pain Points section
4. Solution section
5. Features section
6. Social Proof section
7. FAQ section
8. Final CTA section
9. Footer
```

**Expected result**: The ASCII wireframe is saved to `output/lp-wireframe.txt`.

---

## 🚀 Step 3: Generate Visual WF (diagram-generator)

Use diagram-generator to create a visual wireframe.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Visual WF Generation",
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
Generate a visual wireframe from output/lp-wireframe.txt ASCII WF
using diagram-generator.

Run command:
uv run python tools/generate_diagram.py --topic "LP Wireframe: Hero→PainPoints→Solution→Features→SocialProof→FAQ→CTA layout diagram. Illustrate placement and content elements for each section" --style minimalist

Output to: output/images/lp-wireframe.png

After generation, verify that the section structure is correct.
```

**Expected result**: A visual WF is generated at `output/images/lp-wireframe.png`.

---

## 🚀 Step 4: Information Architecture Review

Review the information architecture of the generated WF and check for improvements.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 4: Information Architecture Review",
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
Review the created WF (output/lp-wireframe.txt and output/images/lp-wireframe.png),
and provide improvement suggestions from the following perspectives:

## Review Criteria
1. **Story flow**: Is the flow from problem → solution → evidence → action natural?
2. **CTA placement**: Are there sufficient CTAs in the first view and at the end?
3. **Information balance**: Is the amount of information in each section appropriate (too much/too little)?
4. **Scannability**: Can the key points be grasped by skimming?
5. **Mobile support**: Are there issues with the mobile layout?

If improvements are needed, update output/lp-wireframe.txt.
```

**Expected result**: Review results and the improved WF are complete.

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
      {"id": "trouble_1", "label": "Brief file not found"},
      {"id": "trouble_2", "label": "diagram-generator throws an error"},
      {"id": "trouble_3", "label": "WF layout is broken"},
      {"id": "trouble_4", "label": "I'm unsure about the section structure"}
    ]
  }]
}
```

### Issue 1: Brief file not found
**Solution**: Create a brief with `/start-13-1`, or generate one with fictional content.

### Issue 2: diagram-generator throws an error
**Solution**: Check if `GEMINI_API_KEY` is set (`echo $GEMINI_API_KEY`).

### Issue 3: WF layout is broken
**Solution**: Make sure it's displayed with a monospaced font. Viewing in the Cursor terminal is recommended.

### Issue 4: I'm unsure about the section structure
**Solution**: Use the basic template (Hero → Pain → Solution → Features → Proof → CTA), then remove unnecessary sections later.

---

## ✅ Checkpoint
- [ ] Brief has been loaded
- [ ] ASCII WF is saved to `output/lp-wireframe.txt`
- [ ] Visual WF is generated at `output/images/lp-wireframe.png`
- [ ] Information architecture review is complete
- [ ] Flow between sections is logical


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/lp/
├── index.html  (Landing Page)
├── style.css
└── assets/
```

### Verification Commands
```bash
# File list
ls -lh output/lp/

# Open in browser (macOS: open / Linux: xdg-open)
open output/lp/index.html
```

> 💡 Check HTML structure: `head -30 output/lp/index.html`

---

## ✅ Completion Check
Enter the following in the Codex chat to verify completion:

```text
Check if output/lp-wireframe.txt and output/images/lp-wireframe.png exist,
and display a summary of the section structure.
```

**Expected result**: WF file existence check and structure summary are displayed.

---

## ➡️ Next Steps

This section is now complete. Next, set up Pencil MCP and proceed to design file creation.

In Codex, you can typically select from choices in chat.

**AskQuestion settings example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select what to do next",
    "options": [
      {"id": "setup_pencil", "label": "Start Pencil setup (/setup-pencil)"},
      {"id": "skip_pencil", "label": "Pencil already set up → Go to design creation (/start-13-3)"},
      {"id": "next_window", "label": "Open /setup-pencil in a new window"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- setup_pencil → Run /setup-pencil (if Pencil is not installed)
- skip_pencil → Run /start-13-3 (if Pencil is already installed)
- next_window → Open /setup-pencil in a new window
- finish → End

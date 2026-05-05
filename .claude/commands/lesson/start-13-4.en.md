---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
prerequisites: ["start-13-3"]
duration: "~30 min"
level: "intermediate"
tags: ["lp", "html", "tailwind", "implementation"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 13-4: Build a Working Landing Page (HTML/CSS/JS)

## 📍 What You'll Do

Welcome to **Lesson 13-4: Landing Page Implementation**!

| Item | Details |
|------|---------|
| Goal | Convert Pencil design into a working HTML/CSS(Tailwind)/JS Landing Page |
| Duration | ~30 min |
| Skills Used | lp-designer, Pencil MCP (code/tailwind guidelines), cursor-ide-browser |
| Prerequisites | Lesson 13-3 complete (.pen design file exists) |
| Course Page | Refer to [Module 13: Landing Page/Website Design](https://ai-agent.camp/en/course/module-13) in parallel |

> **💡 Tool Info**: This lesson uses Pencil MCP. It is available in the current workspace and in Claude Code (CLI/Desktop). In some environments like Codex CLI, you may see a `request_user_input is not supported` error. In that case, refer to the "Alternative Workflow" section.

**Session flow:**
1. Retrieve code conversion guidelines
2. Create project structure
3. Implement HTML/CSS(Tailwind)/JS
4. Add responsive design and animations
5. Verify in browser

By the end of this session, a Landing Page/Website that actually works in the browser will be complete.

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
(check_prereq → Check .pen file existence)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Retrieve Code Conversion Guidelines

Retrieve the guidelines for converting Pencil designs to code.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Code Conversion Guidelines",
  "questions": [{
    "id": "tech_stack",
    "prompt": "Select the tech stack for implementation",
    "options": [
      {"id": "tailwind", "label": "HTML + Tailwind CSS (recommended, CDN)"},
      {"id": "vanilla", "label": "HTML + Vanilla CSS"},
      {"id": "react", "label": "React + Tailwind CSS"},
      {"id": "nextjs", "label": "Next.js + Tailwind CSS"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Retrieve the code conversion guidelines from Pencil MCP.

Steps:
1. Get coding guidelines with get_guidelines(topic="code")
2. Get Tailwind-specific rules with get_guidelines(topic="tailwind")
3. Load the .pen file design with batch_get
4. Summarize the design-to-code conversion approach

Specifically check:
- Color codes (convert to Tailwind class names)
- Font sizes (mapping to text-sm, text-lg, etc.)
- Spacing/margins (mapping to p-4, m-8, etc.)
- Layout structure (usage of flex, grid)
```

**Expected result**: Information needed for code conversion is organized.

---

## 🚀 Step 2: Create Project Structure

Create the file structure for the Landing Page.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Project Structure",
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
Create the project structure for the Landing Page.

Directory creation:
mkdir -p output/lp-project/images
mkdir -p output/lp-project/css
mkdir -p output/lp-project/js

File creation:
- output/lp-project/index.html   # Main HTML
- output/lp-project/css/style.css # Custom CSS
- output/lp-project/js/main.js   # Interactions
- output/lp-project/package.json  # For Vercel deployment

package.json contents:
{
  "name": "lp-project",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "npx serve ."
  }
}
```

**Expected result**: The Landing Page project structure is created.

---

## 🚀 Step 3: Implement HTML/CSS(Tailwind)/JS

Implement the code based on the Pencil design.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Code Implementation",
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
Implement output/lp-project/index.html based on the Pencil .pen file
and output/lp-brief.md.

Requirements:
1. Use Tailwind CSS CDN
   <script src="https://cdn.tailwindcss.com"></script>

2. Section structure (based on output/lp-brief.md):
   - Header: Logo + Nav + CTA button (sticky header)
   - Hero: Headline + Subheadline + CTA + Hero image
   - Pain Points: 3-column icon cards
   - Solution: 2-column (text + image)
   - Features: 3-4 column feature cards
   - Social Proof: Testimonials (carousel or grid)
   - FAQ: Accordion format
   - Final CTA: CTA section with background color
   - Footer: Link groups + copyright

3. Faithful design reproduction:
   - Use colors and fonts from the Pencil style guide
   - Match spacing and margins to the design
   - Button styles (rounded corners, hover effects)

4. Responsive design:
   - Mobile-first (sm: → md: → lg:)
   - 1 column on mobile, 2-4 columns on desktop

5. OGP and meta tags:
   - Set title, description, og:image

Implement with a beautiful, modern design.
```

**Expected result**: Complete HTML/CSS/JS is implemented.

---

## 🚀 Step 4: Add Animations and Interactions

Add scroll animations and interactions.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 4: Add Animations",
  "questions": [{
    "id": "animation_level",
    "prompt": "Select the animation level",
    "options": [
      {"id": "minimal", "label": "Minimal (hover effects only)"},
      {"id": "standard", "label": "Standard (scroll fade-in + hover)"},
      {"id": "rich", "label": "Rich (parallax + counter + slide-in)"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Add animations to output/lp-project/js/main.js.

Features to add:
1. Scroll fade-in (Intersection Observer)
   - Fade in each section when it enters the viewport
   - Animation: opacity 0→1, translateY 20px→0

2. Smooth scroll
   - Smooth scroll on nav link click

3. FAQ accordion
   - Expand/collapse answers on question click

4. Sticky header
   - Add shadow to header on scroll

5. Custom CSS (output/lp-project/css/style.css)
   - CSS variables and keyframes for animations
   - Dark mode support (optional)

Implement with vanilla JS, no external libraries.
```

**Expected result**: Animations and interactions are added.

---

## 🚀 Step 5: Verify in Browser

Check the created Landing Page in a browser.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 5: Browser Verification",
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
Verify the created Landing Page in a browser.

Steps:
1. Start local server
   cd output/lp-project && npx serve .

2. Open http://localhost:3000 in a browser
   (Using cursor-ide-browser MCP)

3. Verify the following:
   - Desktop display (1280px width)
   - Mobile display (375px width)
   - Animation behavior
   - CTA button clicks
   - FAQ accordion behavior
   - Smooth scrolling

4. Fix any issues

Save screenshots of the verification results.
```

**Expected result**: The Landing Page is confirmed to work correctly in the browser.

---

## 🔄 Alternative Workflow (For Non-GUI Environments)

In environments where Pencil MCP is not available (Claude Code, Codex CLI, SSH, etc.), create HTML directly without a .pen file.

1. If you created an HTML mockup with the alternative workflow in 13-3, proceed directly to Step 2 onward in this lesson
2. Reference `output/lp-brief.md` and `output/lp-wireframe.txt` to confirm design specifications
3. Skip the Pencil MCP portion of Step 1's "Code Conversion Guidelines" and refer to Tailwind CSS documentation instead
4. Steps 3 onward (HTML/CSS/JS implementation, animations, browser verification) can be done as-is

> Even without a .pen file, you can implement directly from the wireframe and brief using HTML + Tailwind CSS.

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
      {"id": "trouble_1", "label": "Tailwind CSS isn't working"},
      {"id": "trouble_2", "label": "Responsive layout is broken"},
      {"id": "trouble_3", "label": "Animations don't work"},
      {"id": "trouble_4", "label": "Images aren't displaying"}
    ]
  }]
}
```

### Issue 1: Tailwind CSS isn't working
**Solution**: Check that `<script src="https://cdn.tailwindcss.com"></script>` is inside `<head>`.

### Issue 2: Responsive layout is broken
**Solution**: Check that `<meta name="viewport" content="width=device-width, initial-scale=1.0">` exists. Verify that Tailwind breakpoints (sm: md: lg:) are used correctly.

### Issue 3: Animations don't work
**Solution**: Check that `main.js` is loaded correctly. Place `<script src="js/main.js" defer></script>` before `</body>`.

### Issue 4: Images aren't displaying
**Solution**: Check that image paths are correct relative paths. Verify that files exist in the `images/` directory.

---

## ✅ Checkpoint
- [ ] Code conversion guidelines have been retrieved
- [ ] Project structure is created
- [ ] index.html is complete
- [ ] Responsive design is implemented
- [ ] Animations work
- [ ] Verified in browser


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
Display the file list for output/lp-project/,
and check the number of sections and file size of index.html.
```

**Expected result**: Project file list and sizes are displayed.

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
      {"id": "next_auto", "label": "Start next section (Vercel Deploy)"},
      {"id": "next_window", "label": "Open /start-13-5 in a new window"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → Run /start-13-5
- next_window → Open /start-13-5 in a new window
- finish → End

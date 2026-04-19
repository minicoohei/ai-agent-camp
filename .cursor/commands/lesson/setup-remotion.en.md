---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Node.js 18 or higher installed"]
level: "beginner"
tags: ["setup", "remotion", "video", "react", "npm"]
---

# Remotion Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-remotion` to display progress
2. Auto-detect existing environment:
   - Check Node.js version with `node --version` (18 or higher required)
   - Check whether `mv-composer/node_modules/remotion` exists
   - If already set up, only run Step 3 (operation test) and mark as complete

## What You'll Do in This Session

| Item | Details |
|------|---------|
| Goal | Set up Remotion (a React-based video generation framework) in mv-composer/ and get Remotion Studio ready to launch |
| Duration | ~10 minutes |
| Prerequisites | Node.js 18 or higher installed |
| Skill Level | Everything is auto-run by AI (confirmation only) |

**What is Remotion:**
Remotion is a framework that lets you create videos using React components. It can programmatically generate animated videos, and is used for creating promotional MVs, TikTok/YouTube Shorts, product introduction videos, and more.

**About pricing:**
Remotion is open source, and local rendering is free. A separate license is only required when using Remotion Lambda (cloud rendering), which we will not use in this training.

**Session flow:**
1. Check Node.js version
2. Install dependency packages with npm install
3. Remotion Studio launch test
4. Test rendering (optional)

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

---

## Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(check_prereq -> Guide: "Node.js 18 or higher is required. You can check with `node --version`. If not installed, download it from https://nodejs.org")
(different_lesson -> Show module list)

---

## Step 1: Check Node.js

**What the AI does:**
1. Check the Node.js version:

```bash
node --version
```

2. Check the npm version:

```bash
npm --version
```

**Criteria:**
- Node.js 18.x or higher -> OK, proceed to Step 2
- Node.js not installed or below 18 -> Guide installation

**If Node.js is not installed:**

```text
Node.js 18 or higher is required. Please install it from:
  https://nodejs.org (LTS version recommended)

On Mac, you can also install via Homebrew:
  brew install node
```

**Browser launch commands:**
```bash
# Mac:
open https://nodejs.org
# Windows:
start https://nodejs.org
# Linux:
xdg-open https://nodejs.org
```

After installation, ask the user to type "done", then re-run `node --version` to verify.

---

## Step 2: Install Remotion

**What the AI does:**
1. Navigate to the mv-composer directory and run npm install:

```bash
cd mv-composer && npm install
```

2. Verify installation:

```bash
ls mv-composer/node_modules/remotion/package.json && echo "Remotion installed OK"
```

**Expected result:**
- An `added XX packages` message is displayed
- `Remotion installed OK` is displayed

**Troubleshooting:**
- `EACCES` error -> Do not use `sudo`. Work around it with `npm config set prefix ~/.npm-global`
- `ERESOLVE` error -> Try `npm install --legacy-peer-deps`
- Network error -> Check proxy settings

---

## Step 3: Remotion Studio Launch Test

**What the AI does:**
1. Launch Remotion Studio:

```bash
cd mv-composer && npx remotion studio
```

**Expected result:**
- The browser opens automatically and displays Remotion Studio
- A composition list (ScreenExplainer, etc.) appears in the left panel
- A video is rendered in the preview area

**User guidance:**
```text
Did Remotion Studio appear in your browser?
If you can see the composition list in the left panel, it's working!

Once confirmed, press Ctrl+C to stop the server.
```

**AskQuestion configuration:**
```json
{
  "title": "Remotion Studio Check",
  "questions": [{
    "id": "studio_check",
    "prompt": "Did Remotion Studio appear in your browser?",
    "options": [
      {"id": "success", "label": "It appeared!"},
      {"id": "no_browser", "label": "The browser didn't open"},
      {"id": "error", "label": "I got an error"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

(success -> Proceed to Step 4)
(no_browser -> Guide to manually enter `http://localhost:3000` in the browser)
(error -> Ask them to paste the error message and troubleshoot)
(skip -> Proceed to Step 4)

---

## Step 4: Test Rendering (Optional)

**AskQuestion configuration:**
```json
{
  "title": "Test Rendering",
  "questions": [{
    "id": "render_test",
    "prompt": "Would you like to try a test render? (~30 seconds to 1 minute)",
    "options": [
      {"id": "yes", "label": "Try it"},
      {"id": "no", "label": "Skip and finish"}
    ]
  }]
}
```

(yes -> Run test rendering)
(no -> Go to completion check)

**What the AI does (if yes):**
1. Render a short composition:

```bash
cd mv-composer && npx remotion render src/index.ts ScreenExplainer --frames=0-30 --codec h264 out/test_render.mp4
```

2. Verify output file:

```bash
ls -lh mv-composer/out/test_render.mp4
```

**Expected result:**
- `out/test_render.mp4` is generated
- File size is greater than 0

**Post-rendering guidance:**
```text
Test rendering is complete.
out/test_render.mp4 has been generated.

To view the video:
  open mv-composer/out/test_render.mp4  (Mac)
  start mv-composer\out\test_render.mp4  (Windows)
```

---

## Common Troubleshooting

**AskQuestion configuration:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "npm install fails"},
      {"id": "trouble_2", "label": "Remotion Studio won't open"},
      {"id": "trouble_3", "label": "Rendering fails"},
      {"id": "trouble_4", "label": "TypeScript errors"}
    ]
  }]
}
```

### Issue 1: "npm install fails"
**Cause**: Node.js version too old, network issues
**Resolution guide:**
```text
Please check the following in order:
1. Is node --version 18.x or higher?
2. Run npm cache clean --force and retry
3. Try npm install --legacy-peer-deps
```

### Issue 2: "Remotion Studio won't open"
**Cause**: Port conflict, browser settings
**Resolution guide:**
```text
1. Enter http://localhost:3000 directly in your browser
2. Change port: npx remotion studio --port 3001
3. Check firewall settings
```

### Issue 3: "Rendering fails"
**Cause**: FFmpeg not installed, insufficient memory
**Resolution guide:**
```text
Remotion uses a built-in FFmpeg, so no additional installation is usually needed.
Check the error message.
If out of memory: add the --concurrency=1 option
```

### Issue 4: "TypeScript errors"
**Cause**: Type definition mismatch
**Resolution guide:**
```text
1. Delete node_modules and reinstall:
   rm -rf mv-composer/node_modules && cd mv-composer && npm install
2. Check TypeScript version:
   npx tsc --version
```

---

## Checkpoint
- [ ] Node.js 18 or higher is installed
- [ ] mv-composer/node_modules/remotion exists
- [ ] Remotion Studio displayed in the browser
- [ ] (Optional) Test rendering succeeded

---

## Completion Check

**What the AI does:**
```bash
# Check Node.js version
node --version

# Verify Remotion installation
ls mv-composer/node_modules/remotion/package.json && echo "OK: Remotion installed"

# Mark setup progress as complete
uv run python tools/setup_progress.py complete setup-remotion
```

---

## Output Preview

The deliverable for this lesson is terminal output.

### Expected output example
```text
┌─────────────────────────────────────┐
│  Remotion Setup Complete             │
│  Node.js: v18.x.x                  │
│  Remotion: 4.0.434                  │
│  Studio: Launch verified            │
└─────────────────────────────────────┘
```

---

## Next Steps

Remotion setup is complete. You can now proceed to video production lessons.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please choose what to do next",
    "options": [
      {"id": "lesson_15_8", "label": "Lesson 15-8: Auto-generate marketing assets with Remotion"},
      {"id": "mv_composer", "label": "Create a video with MV Composer"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- lesson_15_8 -> /start-15-8
- mv_composer -> Type "create an MV video" to launch the mv-composer skill
- finish -> End

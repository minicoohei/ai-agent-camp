---
description: "When the user says /start-15-5 — Module 15 Lesson 15-5: Create a slide narration video (HTML parsing + TTS + presenter compositing)"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~35 min"
prerequisites: ["start-15-2"]
level: "advanced"
tags: ["video", "slides", "narration", "tts"]
---

# Lesson 15-5: Slide Narration Video

## What You Will Do in This Session

Welcome to **Lesson 15-5: Slide Narration Video**!

| Item | Details |
|------|---------|
| Goal | Automatically generate a video where a presenter narrates HTML materials or slide images |
| Duration | ~35 min |
| Tools used | slide_narration_pipeline (Gemini + ElevenLabs + Fabric/Kling + FFmpeg) |
| Prerequisites | FAL_KEY, GEMINI_API_KEY, ELEVEN_API_KEY configured |
| Cost guide | Review the [Video AI Cost Strategy Guide](https://ai-agent.camp/en/course/module-15) first (recommended) |
| Course page | Refer to [Module 15: Video Generation](https://ai-agent.camp/en/course/module-15) in parallel |

**Cost estimate**: 5 segments x Fabric 720p approx. **$12/video**; script only **$0.03**

**Session flow:**
1. Verify environment & prepare materials
2. Auto-generate and review the script
3. Generate presenter video
4. Composite slides + presenter
5. Add BGM (optional)
6. Review completed video

By the end of this session, a slide narration video will be saved in `output/ugc/slide_narration/`.

> **Tip**: If the AI response stops midway, type "please continue" to resume.

---

## Readiness Check

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
      {"id": "cost_guide", "label": "I want to see the cost guide first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

---

## Step 1: Verify Environment & Prepare Materials

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Select materials",
  "questions": [{
    "id": "source_choice",
    "prompt": "What materials do you want to create a slide video from?",
    "options": [
      {"id": "html", "label": "From HTML materials (use this course's materials)"},
      {"id": "slides", "label": "From slide images (specify PNG/JPG folder)"},
      {"id": "script_only", "label": "Generate script only first to review"}
    ]
  }]
}
```

**From HTML materials:**
```bash
cd ~/ai-agent-camp
# Example: turn Module 1 banner creation materials into a narration video
python -m ugc.slide_narration_pipeline \
  --html https://ai-agent.camp/en/course/module-1 \
  --engine fabric --resolution 720p
```

**From slide images:**
```bash
cd ~/ai-agent-camp
python -m ugc.slide_narration_pipeline \
  --slides ./my_slides/ \
  --topic "Introduction to AI Agents" \
  --engine fabric
```

**Script only:**
```bash
cd ~/ai-agent-camp
python -m ugc.slide_narration_pipeline \
  --html https://ai-agent.camp/en/course/module-1 \
  --script-only
```

---

## Step 2: Review and Adjust Script

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Script review",
  "questions": [{
    "id": "step_action",
    "prompt": "Do you want to review the generated script?",
    "options": [
      {"id": "check", "label": "Review and edit if needed"},
      {"id": "change_style", "label": "Regenerate with a different style"},
      {"id": "skip", "label": "Proceed as is"}
    ]
  }]
}
```

**Script styles:**
- `friendly` - Friendly conversational tone (default)
- `formal` - Formal presentation style
- `casual` - Casual chat style

**Check points:**
- Is each segment the right length (30-60 seconds/segment recommended)?
- Does it sound natural as spoken language?
- Are technical terms explained?

---

## Step 3: Generate Presenter Video

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Select engine",
  "questions": [{
    "id": "engine_choice",
    "prompt": "Select the presenter video engine",
    "options": [
      {"id": "fabric", "label": "Fabric 1.0 (with lip sync $2.50/30s)"},
      {"id": "kling", "label": "Kling 2.6 Pro (natural motion $2.80/30s)"},
      {"id": "skip_presenter", "label": "No presenter (slides only)"}
    ]
  }]
}
```

**Steps the pipeline executes:**
1. Generate avatar image (Gemini Image)
2. Generate TTS audio per segment (ElevenLabs)
3. Generate presenter video per segment (selected engine)
4. Generate Ken Burns background video from slide images
5. Overlay presenter in bottom-right corner

---

## Step 4: Review Compositing Result

**AskQuestion configuration:**
```json
{
  "title": "Step 4: Compositing result",
  "questions": [{
    "id": "step_action",
    "prompt": "Do you want to review the compositing result?",
    "options": [
      {"id": "check", "label": "Review the video"},
      {"id": "change_position", "label": "Change presenter position"},
      {"id": "skip", "label": "Proceed"}
    ]
  }]
}
```

**Presenter position options:**
- `right` - Bottom right (default)
- `left` - Bottom left
- `bottom` - Bottom center

---

## Step 5: Add BGM (Optional)

**AskQuestion configuration:**
```json
{
  "title": "Step 5: Add BGM",
  "questions": [{
    "id": "bgm_choice",
    "prompt": "Do you want to add BGM?",
    "options": [
      {"id": "add_bgm", "label": "Add BGM (specify file, 12% volume recommended)"},
      {"id": "no_bgm", "label": "Complete without BGM"},
      {"id": "generate", "label": "Learn BGM generation in next lesson (15-6 MV)"}
    ]
  }]
}
```

---

## Step 6: Review Completed Video

**Content:**
```text
Check summary.json in output/ugc/slide_narration/<timestamp>/ (output is in a timestamped subdirectory).

Check items:
- Final video path
- Number of segments
- Engine used
- Generation cost

Cost optimization tips:
- Using 480p cuts Fabric cost in half
- --script-only to review script first ($0.03)
- Without presenter, slides Ken Burns + TTS audio only ($0.05)
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
      {"id": "trouble_1", "label": "HTML parsing cannot extract sections"},
      {"id": "trouble_2", "label": "TTS audio sounds unnatural"},
      {"id": "trouble_3", "label": "Presenter video timed out"},
      {"id": "trouble_4", "label": "Overlay compositing is misaligned"}
    ]
  }]
}
```

### Issue 1: "HTML parsing cannot extract sections"
**Cause**: The HTML structure differs from expected
**Solution**: Use the --slides option to specify slide images directly

### Issue 2: "TTS audio sounds unnatural"
**Cause**: The script text is not suited for reading aloud
**Solution**: Use --script-only to generate the script first -> manually edit -> re-run

### Issue 3: "Presenter video timed out"
**Cause**: fal.ai processing delay
**Solution**: Switch engine (fabric -> kling), shorten segments

### Issue 4: "Overlay compositing is misaligned"
**Cause**: Length mismatch between presenter and slides
**Solution**: FFmpeg's -shortest option auto-adjusts (enabled by default)

---

## Checkpoint
- [ ] API keys are correctly configured
- [ ] HTML parsing or slide images are prepared
- [ ] Script was generated with natural spoken language
- [ ] Presenter video was generated
- [ ] Slides and presenter were composited
- [ ] The final video was reviewed

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select the next action",
    "options": [
      {"id": "next_auto", "label": "Next section (/start-15-6 Music video)"},
      {"id": "retry", "label": "Regenerate with different materials"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

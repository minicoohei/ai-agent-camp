---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~40 min"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "storyboard", "anime", "kling"]
nonInteractiveMode: deferred
---
# 15-6: Storyboard Anime Video

## What You Will Do in This Session

Welcome to **Lesson 15-6: Storyboard Anime Video**!

| Item | Details |
|------|---------|
| Goal | Generate storyboard images from a text scenario, turn them into video with AI engines, and combine into a single work |
| Duration | ~40 min |
| Tools used | storyboard_anime_pipeline (Gemini + Kling/Veo + FFmpeg) |
| Prerequisites | FAL_KEY, GEMINI_API_KEY configured |
| Cost guide | Review the [Video AI Cost Strategy Guide](https://ai-agent.camp/en/course/module-15) first (recommended) |
| Course page | Refer to [Module 15: Video Generation](https://ai-agent.camp/en/course/module-15) in parallel |

**Cost estimate**:
- Full frame I2V (Kling x8): approx. **$5.60**
- Cost-optimized mode (A-roll x4 + B-roll x4): approx. **$2.80**
- Ken Burns B-roll only (for testing): **$0** (local processing)

**Session flow:**
1. Verify environment & prepare scenario
2. Scene decomposition & frame image generation
3. A-roll / B-roll classification and video conversion
4. Crossfade joining with transitions
5. Add BGM (optional)
6. Review completed video & cost summary

By the end of this session, a storyboard anime video will be saved in `output/ugc/storyboard_anime/`.

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
      {"id": "cost_guide", "label": "I want to see the cost guide first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Go to Step 1)
(check_prereq -> Run FAL_KEY / GEMINI_API_KEY existence check)
(cost_guide -> Guide to https://ai-agent.camp/en/course/module-15)
(different_lesson -> Show module list)

---

## Step 1: Verify Environment & Prepare Scenario

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Verify environment",
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

**Content:**
```text
Verify the following:
1. Required API keys are set as environment variables
   - echo $FAL_KEY
   - echo $GEMINI_API_KEY
2. FFmpeg is installed
   - ffmpeg -version
3. Have a scenario (story) in mind
   - Example: "An adventure story about a girl meeting mysterious creatures in a magical forest"
   - Example: "A slice-of-life depicting a day at a cafe"
   - Example: "An astronaut exploring an unknown planet"
```

**Expected result**: API keys are confirmed and a scenario idea is ready.

---

## Step 2: Fully Automated Pipeline Execution

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Select execution mode",
  "questions": [{
    "id": "mode_choice",
    "prompt": "Which mode do you want to run?",
    "options": [
      {"id": "cost_optimize", "label": "Cost-optimized mode (A-roll x4 + B-roll Ken Burns, ~$2.80)"},
      {"id": "full_i2v", "label": "Full I2V mode (all scenes as video, ~$5.60)"},
      {"id": "broll_only", "label": "Ken Burns only (for testing, $0)"},
      {"id": "explain", "label": "Explain the difference between A-roll / B-roll"}
    ]
  }]
}
```

**Cost-optimized mode:**
```bash
cd ~/ai-agent-camp
python -m ugc.storyboard_anime_pipeline \
  --scenario "(user-specified scenario)" \
  --style anime --engine kling --num-scenes 8 \
  --cost-optimize --aroll-count 4
```

**Full I2V mode:**
```bash
cd ~/ai-agent-camp
python -m ugc.storyboard_anime_pipeline \
  --scenario "(user-specified scenario)" \
  --style anime --engine kling --num-scenes 8
```

**5 steps the pipeline auto-executes:**
1. **Scene decomposition** (Gemini Flash) -> `scenes.json` (scenario split into 8 scenes)
2. **Frame image generation** (Gemini Image) -> `frames/frame_000.png` ~ `frame_007.png`
3. **Video clip generation** (Kling I2V or Ken Burns) -> `clips/clip_000.mp4` ~
4. **Crossfade joining** (FFmpeg xfade) -> `joined.mp4`
5. **Final output** -> `final.mp4`

**Expected result**: Frame images and video are generated in `output/ugc/storyboard_anime/`.

---

## Step 3: Review Frame Images

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Review frame images",
  "questions": [{
    "id": "step_action",
    "prompt": "Do you want to review the generated frame images?",
    "options": [
      {"id": "check", "label": "Review frame images"},
      {"id": "regenerate", "label": "Regenerate specific frames"},
      {"id": "change_style", "label": "Regenerate with a different style"},
      {"id": "skip", "label": "Proceed"}
    ]
  }]
}
```

**Available styles:**
- `anime` - Anime style (default)
- `modern_clean` - Modern clean
- `vibrant_ugc` - Vibrant UGC style
- `animal_crossing` - Animal Crossing style
- `watercolor` - Watercolor style
- `pixel_art` - Pixel art style
- `cinematic_live` - Cinematic live-action style

---

## Step 4: Review A-roll / B-roll and Video Clips

**AskQuestion configuration:**
```json
{
  "title": "Step 4: Review video clips",
  "questions": [{
    "id": "step_action",
    "prompt": "Select how to review video clips",
    "options": [
      {"id": "check_all", "label": "Review all clips"},
      {"id": "check_aroll", "label": "Review A-roll clips only"},
      {"id": "explain_aroll", "label": "Explain A-roll / B-roll mechanics"},
      {"id": "skip", "label": "Proceed"}
    ]
  }]
}
```

**A-roll / B-roll explanation:**
```text
[A-roll (main footage)]
- Converted to video by I2V (Image-to-Video) engine
- Character movement, important action scenes
- Cost: Kling $0.70/clip, Veo $8/clip

[B-roll (supplementary footage)]
- Pseudo-video using Ken Burns effect (FFmpeg zoompan)
- Scenery, backgrounds, transitions
- Cost: $0 (local processing)

[Effect types (Ken Burns)]
zoom_in, zoom_out, pan_left, pan_right, slow_zoom, pan_down, pan_up
```

**Check points:**
- A-roll clips: Is the motion natural?
- B-roll clips: Is the Ken Burns effect appropriate?
- Is `is_key_scene` in scenes.json correctly determined?

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
      {"id": "add_bgm", "label": "Add BGM (specify file)"},
      {"id": "no_bgm", "label": "Complete without BGM"},
      {"id": "generate", "label": "Generate BGM with Suno AI (covered in a later lesson)"}
    ]
  }]
}
```

**BGM addition:**
```bash
cd ~/ai-agent-camp
python -m ugc.storyboard_anime_pipeline \
  --scenario "(same scenario)" \
  --style anime --engine kling \
  --cost-optimize --aroll-count 4 \
  --bgm ./my_bgm.mp3 --bgm-volume 0.20
```

---

## Step 6: Review Completed Video & Cost Summary

**Content:**
```text
Read summary.json in output/ugc/storyboard_anime/ and review the results.

Check items:
- Final video path
- Number of scenes (A-roll / B-roll breakdown)
- Generation cost ($)
- Success/failure of each step

Cost optimization tips:
- Limiting to 4 A-roll clips is 1/4 the normal cost
- Ken Burns effects are $0 so B-roll can be freely added
- For bulk generation, consider flat-rate services like GenSpark
  -> Details: https://ai-agent.camp/en/course/module-15
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
      {"id": "trouble_1", "label": "API key error"},
      {"id": "trouble_2", "label": "Frame image styles are inconsistent"},
      {"id": "trouble_3", "label": "I2V video conversion timed out"},
      {"id": "trouble_4", "label": "Crossfade joining failed"}
    ]
  }]
}
```

### Issue 1: "API key error"
**Cause**: Environment variables are not set
**Solution**:
```bash
cat .env | grep -E "FAL_KEY|GEMINI"
```

### Issue 2: "Frame image styles are inconsistent"
**Cause**: Variation in Gemini image generation
**Solution**: Fix the character description with the `--character` option
```bash
python -m ugc.storyboard_anime_pipeline \
  --scenario "..." --style anime --engine kling \
  --character "A girl with short brown hair, white dress, large eyes"
```

### Issue 3: "I2V video conversion timed out"
**Cause**: fal.ai processing is slow
**Solution**: Reduce I2V count with `--cost-optimize`, or switch Kling -> Veo

### Issue 4: "Crossfade joining failed"
**Cause**: Video format mismatch
**Solution**: The pipeline automatically falls back to simple concat

---

## Checkpoint
- [ ] API keys are correctly configured
- [ ] Scene decomposition from scenario completed
- [ ] Frame images were generated
- [ ] Understood the A-roll / B-roll difference
- [ ] The final video was reviewed
- [ ] Understood the cost strategy guide

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
      {"id": "next_auto", "label": "Next section (/start-15-7 Music video)"},
      {"id": "retry", "label": "Regenerate with a different scenario/style"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

## Reference links (mirrors aiagent-course Module 15 slides)

Five resources you can use to find templates or inspiration.

- [Dribbble (motion design portfolios)](https://dribbble.com/)
- [Envato Elements — video templates / logo animation](https://elements.envato.com/video-templates/logo+animation)
- [Placeit — minimalist motion-graphics intro maker](https://placeit.net/c/videos/stages/intro-maker-with-minimalist-motion-graphics-988)
- [YouTube — After Effects templates project channel](https://www.youtube.com/@paftereffectstemplatesproj6705)
- [YouTube — motion-graphics templates playlist](https://www.youtube.com/playlist?list=PLCWRuswMLN-huRtRNjplBjZGuIknrhckj)


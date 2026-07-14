---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~30 min"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "product-demo", "avatar", "kling"]
nonInteractiveMode: deferred
---
# 15-9: Product Demo Video

## What You Will Do in This Session

Welcome to **Lesson 15-9: Product Demo Video**!

| Item | Details |
|------|---------|
| Goal | Generate a video where a green screen avatar introduces an app on a smartphone screen |
| Duration | ~30 min |
| Tools used | product_demo_pipeline (Gemini + ElevenLabs + Fabric/Kling + FFmpeg) |
| Prerequisites | FAL_KEY, GEMINI_API_KEY, ELEVEN_API_KEY configured |
| Cost guide | Review the [Video AI Cost Strategy Guide](https://ai-agent.camp/en/course/module-15) first (recommended) |
| Course page | Refer to [Module 15: Video Generation](https://ai-agent.camp/en/course/module-15) in parallel |

**Cost estimate**: Fabric engine 480p approx. **$2.50/video**, Kling approx. **$2.80/video**

**Session flow:**
1. Verify environment & prepare screenshots
2. Select engine & run pipeline
3. Review and adjust the script
4. Review the green screen compositing
5. Add BGM (optional)
6. Review completed video & cost summary

By the end of this session, a product demo video will be saved in `output/ugc/product_demo/`.

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
(check_prereq -> Run FAL_KEY / GEMINI_API_KEY / ELEVEN_API_KEY existence check)
(cost_guide -> Guide to https://ai-agent.camp/en/course/module-15)
(different_lesson -> Show module list)

---

## Step 1: Verify Environment & Prepare Screenshots

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
   - echo $ELEVEN_API_KEY (or $ELEVENLABS_API_KEY)
2. FFmpeg is installed
   - ffmpeg -version
3. Prepare a screenshot of the app/service you want to introduce
   - Smartphone screen size (portrait) recommended
   - If unavailable, a sample will be created
```

**Expected result**: API keys are confirmed and screenshots are ready.

---

## Step 2: Fully Automated Pipeline Execution

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Select video generation engine",
  "questions": [{
    "id": "engine_choice",
    "prompt": "Which engine do you want to use?",
    "options": [
      {"id": "fabric", "label": "Fabric 1.0 (good value $2.50, with lip sync)"},
      {"id": "kling", "label": "Kling 2.6 Pro (natural motion $2.80, UGC style)"},
      {"id": "veo", "label": "Veo 3.1 (highest quality $15+, watch cost)"},
      {"id": "longcat", "label": "LongCat (full-body animation $3.00)"}
    ]
  }]
}
```

**Post-selection execution:**

```bash
cd ~/ai-agent-camp
python -m ugc.product_demo_pipeline \
  --product "(user-specified product name)" \
  --screenshot ./(user's screenshot) \
  --engine fabric \
  --platform tiktok \
  --resolution 480p
```

**6 steps the pipeline auto-executes:**
1. **Script generation** (Gemini Flash) -> `script.txt`
2. **Avatar image generation** (Gemini Image) -> `avatar.png` (person holding phone on green screen)
3. **TTS audio generation** (ElevenLabs) -> `speech.mp3`
4. **Video generation** (Fabric/Kling/Veo) -> `raw_video.mp4`
5. **Green screen compositing** (FFmpeg) -> `composited.mp4` (screenshot composited onto phone screen)
6. **Final output** -> `final.mp4`

**Expected result**: A video is generated in `output/ugc/product_demo/`.

---

## Step 3: Review and Adjust the Generated Script

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Script review",
  "questions": [{
    "id": "step_action",
    "prompt": "Do you want to review the generated script?",
    "options": [
      {"id": "check", "label": "Review and edit if needed"},
      {"id": "regenerate", "label": "Regenerate a different script"},
      {"id": "skip", "label": "Proceed as is"}
    ]
  }]
}
```

**Content:**
```text
Read script.txt in output/ugc/product_demo/ and review the content.

Check points:
- Does the hook (first 2 seconds) grab attention?
- Does it convey the product's appeal?
- Is it natural as spoken language?
- Is it too long (30 seconds = approx. 90 characters target)?
```

---

## Step 4: Review Green Screen Compositing

**AskQuestion configuration:**
```json
{
  "title": "Step 4: Review compositing result",
  "questions": [{
    "id": "step_action",
    "prompt": "Do you want to review the compositing result?",
    "options": [
      {"id": "check", "label": "Review the video"},
      {"id": "retry_opencv", "label": "Recomposite with OpenCV backend"},
      {"id": "skip", "label": "Proceed"}
    ]
  }]
}
```

**Check points:**
- Is the screenshot correctly composited onto the phone screen?
- Is there any green residue?
- Is the balance between the avatar and the screenshot good?

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
      {"id": "generate", "label": "Generate BGM with Suno AI (fal.ai, covered in a later lesson)"}
    ]
  }]
}
```

**BGM addition:**
```python
from tools.ugc.audio_post import mix_bgm
mix_bgm(
    video_path="output/ugc/product_demo/.../composited.mp4",
    bgm_path="./my_bgm.mp3",
    output_path="output/ugc/product_demo/.../final_with_bgm.mp4",
    bgm_volume=0.15,
)
```

---

## Step 6: Review Completed Video & Cost Summary

**Content:**
```text
Read summary.json in output/ugc/product_demo/ and review the results.

Check items:
- Final video path
- Engine used
- Generation cost ($)
- Success/failure of each step

Cost optimization tips:
- Using 480p cuts Fabric cost in half
- Reusing the avatar image saves $0.02 each time
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
      {"id": "trouble_2", "label": "Green screen compositing failed"},
      {"id": "trouble_3", "label": "Video generation timed out"},
      {"id": "trouble_4", "label": "Audio and lip movement are out of sync"}
    ]
  }]
}
```

### Issue 1: "API key error"
**Cause**: Environment variables are not set
**Solution**:
```bash
cat .env | grep -E "FAL_KEY|GEMINI|ELEVEN"    # Mac/Linux/WSL
```

### Issue 2: "Green screen compositing failed"
**Cause**: Difficulty detecting green in the image
**Solution**: Try the OpenCV backend
```python
from ugc import composite_video
composite_video(video, screenshot, output, backend="opencv")
```

### Issue 3: "Video generation timed out"
**Cause**: fal.ai processing is slow
**Solution**: Switch to Fabric or retry

### Issue 4: "Audio and lip movement are out of sync"
**Solution**: Apply lip sync correction with MuseTalk
```python
from ugc.audio_post import apply_musetalk
apply_musetalk(video, audio, output)
```

---

## Checkpoint
- [ ] API keys are correctly configured
- [ ] Screenshots were prepared
- [ ] The pipeline completed successfully
- [ ] Green screen compositing succeeded
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
      {"id": "next_auto", "label": "Next module (/start-16-1)"},
      {"id": "retry", "label": "Regenerate the same video with a different engine"},
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


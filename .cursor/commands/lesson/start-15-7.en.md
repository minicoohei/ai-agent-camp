---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~45 min"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "music-video", "suno", "beat-sync"]
---

# Lesson 15-7: Music Video

## What You Will Do in This Session

Welcome to **Lesson 15-7: Music Video**!

| Item | Details |
|------|---------|
| Goal | Generate an AI music track, combine beat-synced scene videos to create a music video |
| Duration | ~45 min |
| Tools used | mv_pipeline (Suno/fal.ai + librosa + Gemini + Kling + FFmpeg) |
| Prerequisites | FAL_KEY, GEMINI_API_KEY configured. pip install librosa recommended |
| Cost guide | Review the [Video AI Cost Strategy Guide](https://ai-agent.camp/en/course/module-15) first (recommended) |
| Course page | Refer to [Module 15: Video Generation](https://ai-agent.camp/en/course/module-15) in parallel |

**Cost estimate**:
- Full I2V (Kling x8) + AI music: approx. **$6-12**
- Cost-optimized (A-roll x3 + B-roll x5): approx. **$3-5**
- Existing music + Ken Burns only: approx. **$0.10** (image generation only)

**Session flow:**
1. Verify environment & prepare music
2. AI music generation or load existing music
3. Beat analysis & scene timeline
4. Scene image + video clip generation
5. Beat-synced joining & music mixing
6. Review completed MV

By the end of this session, a music video will be saved in `output/ugc/mv/`.

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
      {"id": "install_librosa", "label": "I want to install librosa"},
      {"id": "cost_guide", "label": "I want to see the cost guide first"}
    ]
  }]
}
```

(install_librosa -> Run `pip install librosa`)

---

## Step 1: Verify Environment & Prepare Music

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Prepare music",
  "questions": [{
    "id": "music_source",
    "prompt": "How do you want to prepare the music?",
    "options": [
      {"id": "generate", "label": "Generate music with AI (fal.ai Suno)"},
      {"id": "existing", "label": "Use an existing music file"},
      {"id": "explain", "label": "Explain how AI music generation works"}
    ]
  }]
}
```

**Environment check:**
```text
Verify the following:
1. API keys
   - echo $FAL_KEY
   - echo $GEMINI_API_KEY
2. FFmpeg
   - ffmpeg -version
3. librosa (for beat analysis, optional)
   - python -c "import librosa; print(librosa.__version__)"
   - Install: pip install librosa
```

---

## Step 2: Run Pipeline

**AI music generation + MV creation:**
```bash
cd ~/ai-agent-camp
python -m ugc.mv_pipeline \
  --prompt "Bright pop song, positive lyrics, tempo 120BPM" \
  --style anime \
  --engine kling \
  --num-scenes 8 \
  --cost-optimize --aroll-count 3
```

**Existing music + MV creation:**
```bash
cd ~/ai-agent-camp
python -m ugc.mv_pipeline \
  --music ./my_song.mp3 \
  --style cinematic_live \
  --engine kling \
  --num-scenes 8
```

**7 steps the pipeline auto-executes:**
1. **Music preparation** -> AI generation or existing file copy
2. **Beat analysis** (librosa) -> `beat_analysis.json` (tempo, beat positions, sections)
3. **Scene prompt generation** (Gemini) -> `scenes.json` (lyrics/mood -> visual prompt conversion)
4. **Frame image generation** (Gemini Image) -> 8 scene images
5. **Video clip generation** (Kling I2V + Ken Burns) -> 8 clips
6. **Beat-synced joining** (FFmpeg xfade) -> `joined.mp4`
7. **Music mixing** (FFmpeg) -> `final.mp4`

---

## Step 3: Review Beat Analysis

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Beat analysis results",
  "questions": [{
    "id": "step_action",
    "prompt": "Do you want to review the beat analysis results?",
    "options": [
      {"id": "check", "label": "Review analysis results"},
      {"id": "explain_beat", "label": "Explain beat sync mechanics"},
      {"id": "skip", "label": "Proceed"}
    ]
  }]
}
```

**Check points:**
- Does the tempo (BPM) match the music?
- Are sections (verse/chorus) correctly detected?
- Does each scene length align with beats?

**Beat sync mechanics:**
```text
Detect beat positions in the music
    |
Split at downbeats (strong beats)
    |
chorus sections -> A-roll (dynamic I2V)
verse sections -> B-roll (calm Ken Burns footage)
    |
Cut transitions at beat positions
```

---

## Step 4: Review Scene Images and Video Clips

**AskQuestion configuration:**
```json
{
  "title": "Step 4: Review clips",
  "questions": [{
    "id": "step_action",
    "prompt": "Select review method",
    "options": [
      {"id": "check_frames", "label": "Review frame images"},
      {"id": "check_clips", "label": "Review video clips"},
      {"id": "regenerate", "label": "Regenerate specific scenes"},
      {"id": "skip", "label": "Proceed"}
    ]
  }]
}
```

**Available visual styles:**
- `anime` - Anime style
- `cinematic_live` - Cinematic live-action style
- `abstract` - Abstract/artistic style
- `watercolor` - Watercolor style
- `pixel_art` - Pixel art style
- `vibrant_ugc` - Vibrant social media style

**Scene prompt tips:**
```text
verse (A/B section) -> narrative or landscape
chorus -> performance or abstract
bridge -> abstract or landscape
```

---

## Step 5: Review Completed MV & Cost Summary

**Content:**
```text
Check summary.json in output/ugc/mv/.

Check items:
- Music path & length
- Visual style
- Number of scenes (A-roll / B-roll breakdown)
- Generation cost

Cost optimization techniques:
- Use A-roll (I2V) only for chorus sections to concentrate impact
- Use Ken Burns B-roll for verse sections with calm footage
- This yields A-roll x3 + B-roll x5 = $2.10 + $0 = $2.10 (video only)
- Details: https://ai-agent.camp/en/course/module-15
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
      {"id": "trouble_1", "label": "AI music generation fails"},
      {"id": "trouble_2", "label": "Error installing librosa"},
      {"id": "trouble_3", "label": "Beats and scene transitions are out of sync"},
      {"id": "trouble_4", "label": "Video and music mood don't match"}
    ]
  }]
}
```

### Issue 1: "AI music generation fails"
**Cause**: Change in fal.ai music generation endpoint
**Solution**: Use the --music option with an existing music file

### Issue 2: "Error installing librosa"
**Cause**: Dependency library issues
**Solution**:
```bash
pip install librosa soundfile
# If that doesn't work:
pip install librosa --no-deps
pip install soundfile numba
```
It also works with equal-interval splitting without librosa.

### Issue 3: "Beats and scene transitions are out of sync"
**Cause**: Beat detection precision
**Solution**: Reduce `--num-scenes` (8 -> 6) to better align with beats

### Issue 4: "Video and music mood don't match"
**Cause**: Style selection mismatch
**Solution**: Change the style to match the music genre
- Pop -> `anime` or `vibrant_ugc`
- Rock -> `cinematic_live`
- Electronic -> `abstract`
- Classical -> `watercolor`

---

## Checkpoint
- [ ] API keys are correctly configured
- [ ] Music was prepared (AI generated or existing)
- [ ] Beat analysis was executed
- [ ] Scene images were generated
- [ ] A-roll / B-roll video clips were generated
- [ ] MV was completed with beat sync
- [ ] Music mixing succeeded

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
      {"id": "next_auto", "label": "Next section (/start-15-8 Slide narration video)"},
      {"id": "retry", "label": "Regenerate with different music/style"},
      {"id": "review_all", "label": "Review Module 15"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

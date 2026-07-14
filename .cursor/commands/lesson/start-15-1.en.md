---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~30 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["video", "keyframe", "analysis", "ffmpeg"]
nonInteractiveMode: deferred
---
# Lesson 15-1: Video Frame Analysis

## What You Will Do in This Session

Welcome to **Lesson 15-1: Video Frame Analysis**!

| Item | Details |
|------|---------|
| Goal | Extract keyframes from a video, analyze the content, and create a summary report |
| Duration | ~30 min |
| Skills used | video-frame-reader (FFmpeg, Gemini Vision API) |
| Prerequisites | FFmpeg, Python 3.9+, and Gemini API key configured |
| Course page | Refer to [Module 15: Video Generation](https://ai-agent.camp/en/course/module-15) in parallel |

**Session flow:**
1. Verify environment
2. Prepare sample video
3. Extract and analyze keyframes
4. Create a video summary report

By the end of this session, keyframes and a summary will be saved in outputs.

> **Tip**: If the AI response stops midway, type "please continue" or "it stopped" to resume. Responses may pause depending on the tool, but this is not an error.

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

## Step 0: Prepare a Test Video

Use the bundled sample video first. Only add a practice video via FFmpeg if you don't have one.

```bash
# Create the data directory under lesson (if needed)
mkdir -p courses/aiagent/lesson03-core/module15-video/practice/data/videos

# Generate a test video with FFmpeg (10 seconds, 640x480, 30fps):
ffmpeg -f lavfi -i testsrc=duration=10:size=640x480:rate=30 -pix_fmt yuv420p courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4
```

> **Note**: If FFmpeg is not installed, Step 1 environment check will guide you.

---

## Step 1: Verify Environment

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Verify Environment",
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
Verify the environment needed for video frame extraction:
- Is FFmpeg installed?
- Is Python 3.9+ installed?
- Is the video-frame-reader skill available?

If anything is missing, show the installation steps.
```

**Expected result**: The required environment is verified, and installation steps are shown if anything is missing.

---

## Step 2: Prepare Sample Video

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Prepare Sample Video",
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
For video frame extraction testing, verify the following:
1. The `courses/aiagent/lesson03-core/module15-video/practice/data/videos/` folder exists
2. The default official sample `data/videos/module7-lesson1-frame-lab-sample.mp4` or `courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4` can be used

If trying a different video, you may place an MP4 of 30 seconds or less in `courses/aiagent/lesson03-core/module15-video/practice/data/videos/`.
```

**Expected result**: Test videos including `data/videos/module7-lesson1-frame-lab-sample.mp4` are ready and paths are confirmed.

---

## Step 3: Extract Keyframes

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Extract Keyframes",
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
Extract keyframes from data/videos/module7-lesson1-frame-lab-sample.mp4 or
courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4
(use video-frame-reader's extract_keyframes.py).

Settings:
- Extraction interval: every 5 seconds (or skill default)
- Output format: follow skill (PNG, etc.)
- Output path: data/frames/ or another clear path

After extraction, display the list of generated frame images.
```

**Expected result**: Keyframes are saved as PNG at the specified interval.

---

## Step 4: Analyze Extracted Frames

**AskQuestion configuration:**
```json
{
  "title": "Step 4: Analyze Extracted Frames",
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
Analyze the extracted frame images:

For each image in data/frames/, provide:
- Scene content description
- Detected objects
- OCR results if text is present
- Differences from the previous frame
```

**Expected result**: The content of each frame is described.

---

## Step 5: Create Video Summary Report

**AskQuestion configuration:**
```json
{
  "title": "Step 5: Create Video Summary Report",
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
Based on the frame analysis results, create a video summary report.

Report content:
- Video overview (1-2 sentences)
- List of key scenes
- Timeline-format content description
- Notable points

Output: output/video_summary.md
```

**Expected result**: The video content is summarized in Markdown format.

---

## Step 6: Detect Scene Changes

**AskQuestion configuration:**
```json
{
  "title": "Step 6: Detect Scene Changes",
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
Automatically detect scene changes in the video.

Detection method:
- Analyze color distribution changes between frames
- Record points with large changes as scene boundaries
- Identify start and end times for each scene

Save the results in JSON format:
Output: output/scene_detection.json
```

> **Note**: Scene change detection is a future extension. Currently only keyframe extraction is supported.
> In this step, you can use FFmpeg's `select='gt(scene,0.3)'` filter or manual inter-frame difference comparison as alternatives.

**Expected result**: Scene change timestamps are saved in JSON format.

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
      {"id": "trouble_1", "label": "FFmpeg not found"},
      {"id": "trouble_2", "label": "Cannot load the video"},
      {"id": "trouble_3", "label": "Out of memory error"},
      {"id": "trouble_4", "label": "Frame images are all black"}
    ]
  }]
}
```


### Issue 1: "FFmpeg not found"
**Cause**: FFmpeg is not installed
**Solution prompt**:
```
Install FFmpeg.
macOS: brew install ffmpeg
Windows: winget install ffmpeg or download from https://ffmpeg.org/download.html
After installation, verify with ffmpeg -version.
```

### Issue 2: "Cannot load the video"
**Cause**: The video format is unsupported or there is a codec issue
**Solution prompt**:
```
Check the video file format.
Use ffprobe to get codec information, and
show how to convert to a supported format (MP4/H.264).
```

### Issue 3: "Out of memory error"
**Cause**: The video is long or the resolution is high
**Solution prompt**:
```
Show how to resolve the out-of-memory error:
- Increase the extraction interval (e.g., every 30 seconds)
- Lower the video resolution
- Process in batches using split processing
```

### Issue 4: "Frame images are all black"
**Cause**: The video starts with a fade-in or there is a codec issue
**Solution prompt**:
```
The extracted frames are black images.
- Shift the start position by a few seconds
- Try a different frame extraction method
Show how to fix this.
```

---

## Checkpoint
- [ ] FFmpeg was installed successfully
- [ ] A test video was prepared
- [ ] Keyframes were extracted
- [ ] Extracted images were saved correctly
- [ ] Frame content was analyzed
- [ ] A video summary report was created


---

## Deliverables Preview

### Expected output
```
output/ugc/
  *.mp4           (video files)
  metadata.json   (metadata)
  thumbnails/     (thumbnails)
```

### Verification commands
```bash
# List and size of output files
ls -lh output/ugc/

# Check metadata
cat output/ugc/*metadata*.json 2>/dev/null | head -20

# Play video (macOS: open / Linux: xdg-open)
open output/ugc/*.mp4
```

---

## Completion Check
Paste the following into the Cursor chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
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
      {"id": "next_window", "label": "Open in new window (/start-15-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection guide (example)**:
- next_auto -> /next_lesson
- next_window -> Open /start-15-2 in a new window
- finish -> End

## Reference links (mirrors aiagent-course Module 15 slides)

Five resources you can use to find templates or inspiration.

- [Dribbble (motion design portfolios)](https://dribbble.com/)
- [Envato Elements — video templates / logo animation](https://elements.envato.com/video-templates/logo+animation)
- [Placeit — minimalist motion-graphics intro maker](https://placeit.net/c/videos/stages/intro-maker-with-minimalist-motion-graphics-988)
- [YouTube — After Effects templates project channel](https://www.youtube.com/@paftereffectstemplatesproj6705)
- [YouTube — motion-graphics templates playlist](https://www.youtube.com/playlist?list=PLCWRuswMLN-huRtRNjplBjZGuIknrhckj)


---
description: "When the user says /start-15-2 — Module 15 Lesson 15-2: Understand the video AI engine landscape and learn how to use fal.ai"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~20 min"
prerequisites: ["start-15-1"]
level: "intermediate"
tags: ["video", "ai-engine", "fal"]
---

# 15-2: Video AI Engine Overview

## What You Will Do in This Session

Welcome to **Lesson 15-2: Video AI Engine Overview**!

| Item | Details |
|------|---------|
| Goal | Understand the latest video AI engines and learn the basics of fal.ai |
| Duration | ~20 min |
| Tools used | fal.ai (FAL_KEY) |
| Prerequisites | FAL_KEY configured, Python 3.10+ recommended |
| Cost guide | * Cost guide is in preparation |
| Course page | Refer to [Module 15: Video Generation](https://ai-agent.camp/en/course/module-15) in parallel |

**Important**: This lesson does not run a hands-on comparison of all engines (due to high cost).
You will understand each engine's features and pricing, and only do a hands-on exercise with the basic fal.ai pattern.
Actual API calls will be made as needed starting from Lesson 15-3's project lessons.

**Prerequisite: FAL_KEY configuration**

An API key must be configured in advance to use the fal.ai API.
If not configured, run `/setup-fal` to set it up.

> **Note**: fal-client recommends Python 3.10+. Check with `python3 --version`.

**Session flow:**
1. Video AI engine landscape
2. API pay-per-use vs flat-rate services
3. Basic fal.ai usage (hands-on)
4. Engine selection criteria

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
      {"id": "check_prereq", "label": "I want to check FAL_KEY setup"},
      {"id": "cost_guide", "label": "I want to see the cost guide first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

---

## Step 1: Video AI Engine Landscape

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Engine overview",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Explore together"},
      {"id": "review", "label": "Just review the summary"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Content:**

Here is an introduction to the major video AI engines as of 2025-2026.

### Image-to-Video Engines

| Engine | Provider | Price | Features |
|--------|----------|-------|----------|
| **Kling 2.6 Pro** | fal.ai | $0.07/s | Natural motion, UGC style, green screen support |
| **Veo 3.1** | fal.ai | $0.50-1.00/s | Highest quality, native audio, Text-to-Video support |
| **Runway Gen-3** | Runway | Flat $15-76/mo | High quality, easy-to-use Web UI |
| **Pika 2.0** | Pika | Flat $8-58/mo | Text/image to video, rich effects |
| **Minimax** | fal.ai | Check pricing | Strong for long videos |
| **LTX Video** | fal.ai | Low cost | Open source based |

### Lip-sync Engines

| Engine | Provider | Price | Features |
|--------|----------|-------|----------|
| **Fabric 1.0** | fal.ai | $0.08-0.15/s | High-precision lip sync |
| **LongCat** | fal.ai | $0.10/s | Full-body motion + lip sync |
| **HeyGen** | Direct API | $0.05/s | Built-in avatars, multilingual |
| **MuseTalk** | fal.ai | Check pricing | Lip sync via fal.ai |

### Other

| Tool | Type | Price | Use case |
|------|------|-------|----------|
| **Suno** | Music generation | Via fal.ai | AI composition |
| **Remotion** | Code video | $0 (local) | Template video, slides |
| **FFmpeg** | Editing | $0 (local) | Transitions, compositing, Ken Burns |

### Flat-rate Services (for bulk generation)

| Service | Monthly | Features |
|---------|---------|----------|
| **GenSpark** | $19/mo | AI video + images + search |
| **Runway** | $15-76/mo | Gen-3 Alpha, high quality |
| **Pika** | $8-58/mo | Easy, rich effects |
| **CapCut Pro** | $10/mo | Editing + templates |

**Key point**: APIs are suited for automation but expensive. Flat-rate services are manual but suited for mass production.
See the cost strategy guide (in preparation) for details.

---

## Step 2: API vs Flat-rate Services

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Cost strategy",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Think through together"},
      {"id": "review", "label": "Just review the summary"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Content:**

```text
Decision flowchart:

Need automation?
  YES -> API (fal.ai)
    More than 10 videos/month?
      YES -> Also consider flat-rate services
      NO  -> API is sufficient (learning phase)
  NO  -> Flat-rate service (manual operation OK)

Are there scenes that can be replaced with B-roll?
  YES -> A-roll (API) + B-roll (Ken Burns/Remotion) = cost optimal
  NO  -> All scenes I2V (be prepared for cost)
```

---

## Step 3: fal.ai Basics (Hands-on)

**AskQuestion configuration:**
```json
{
  "title": "Step 3: fal.ai hands-on",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Actually run it"},
      {"id": "review", "label": "Just review the code"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Content:**

Review the basic fal.ai client pattern.
Keep actual API calls to a minimum (text generation level only).

```python
# Basic fal.ai pattern
import fal_client

# 1. File upload
url = fal_client.upload_file("image.png")

# 2. Subscribe pattern (wait for result)
result = fal_client.subscribe(
    "fal-ai/kling-video/v2.6/pro/image-to-video",
    arguments={
        "image_url": url,
        "prompt": "A person talking naturally",
        "duration": "5",
        "aspect_ratio": "9:16",
    },
    with_logs=True,
    on_queue_update=lambda update: print(f"Status: {update}"),
)

# 3. Get result
video_url = result["video"]["url"]
```

```text
Verification items:
1. Is FAL_KEY configured?
   echo $FAL_KEY
2. Is fal-client installed?
   pip show fal-client
3. Understand the code structure above (subscribe + arguments + callback)
```

---

## Step 4: Engine Selection Criteria

**Summary:**

| Use case | Recommended engine | Reason |
|----------|-------------------|--------|
| Product intro (UGC style) | Fabric / Kling | Lip sync + cost performance |
| Anime / story | Kling | Good I2V quality |
| Highest quality demo | Veo 3.1 | Best quality (watch cost) |
| Slides / templates | Remotion | $0, freely customizable |
| MV / music | Suno + Kling | Music generation + video generation |
| Bulk generation | GenSpark/Runway | Flat rate for budget management |
| B-roll filler | Ken Burns (FFmpeg) | $0, pseudo-video from stills |

---

## Checkpoint
- [ ] Understood the major types of video AI engines
- [ ] Understood the difference between API pay-per-use and flat-rate services
- [ ] Understood the fal.ai subscribe pattern
- [ ] Reviewed the cost strategy guide
- [ ] Can select an engine for your use case

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
      {"id": "next_73", "label": "15-3: Product demo video (green screen compositing)"},
      {"id": "next_74", "label": "15-4: Storyboard anime video"},
      {"id": "next_75", "label": "15-5: Slide narration video (Remotion)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

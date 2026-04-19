---
name: viral-short-video
description: "Viral video script & storyboard generation skill for TikTok/YouTube Shorts. Automatically incorporates researched viral techniques (3-second hook, modular structure, loop bridge, flash text, split screen, etc.) into scripting and storyboard creation. Triggered by 'TikTok video script', 'Want to make a viral video', 'Short video script', etc."
triggers:
  - Want to make a viral video
  - TikTok video script
  - Short video script
  - Want to make a viral hit
  - Reels video plan
  - viral-short-video
  - TikTok Shorts
---

# Viral Short Video - Viral Short Video Script & Storyboard

Viral video production pipeline for TikTok / YouTube Shorts.
Automatically embeds research-based viral techniques into scripts,
integrating with existing `storyboard-generator` / `video-editor` for video production.

## Full Pipeline Overview

```
[Topic/Product/Target]
  |
[generate_viral_script.py]  <- Core of this skill
  +-- viral_script.json       (Viral structured script)
  +-- scenes.json             (storyboard-generator compatible)
  +-- hook_variants.json      (Hook variations x3)
  +-- hook_analysis.json      (--analyze-video: peak hook analysis)
  |
[storyboard-generator]       <- Existing skill
  +-- frames/                 (Storyboard images)
  +-- scenes.json             (Enhanced)
  |
[video-editor]               <- Existing skill (enhanced)
  +-- Caption burn-in
  +-- Flash text insertion
  +-- Split screen composition (background overlay method)
  +-- Final video.mp4
```

## Included Assets

### Gameplay Background Assets (`assets/gameplay/`)

| Preset Name | Game | Length | Notes |
|-------------|------|--------|-------|
| subway_surfers | Subway Surfers | 26 min | Vertical HD, No Copyright |
| minecraft | Minecraft Parkour | 5 min | Vertical 2K 60fps, No Copyright |

### Hook Compilation Assets (`assets/hooks/`)

| Preset Name | Content | Use Case |
|-------------|---------|----------|
| hook_viral_10 | 10 TikTok Hooks You Can Use To Go Viral | Hook examples: 10 patterns |
| hook_trifecta | This HOOK Combo Will Get You Viral on TikTok | Hook trifecta strategy + examples |
| hook_600k_gmv | This Hook Made $600K GMV on TikTok Shop | $600K revenue hook breakdown |

First-time setup: `bash skills/viral-short-video/scripts/download_assets.sh`

## Usage

```bash
# Basic: Generate viral script from topic
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "How to safely use a crypto wallet" \
  --duration 30 \
  --target "Crypto beginners in their 20s-30s" \
  --session "crypto_wallet_tips"

# Generate script with product name
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "Cut transfer fees by 90% with this app" \
  --product "My Product" \
  --duration 15 \
  --tone casual \
  --session "product_fees"

# End-to-end with storyboard generation
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "How to make videos with AI" \
  --duration 60 \
  --generate-storyboard \
  --character "Japanese woman in her 20s, casual clothing" \
  --session "ai_video_tutorial"

# Dry-run (script only, no image generation)
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "3 investment mistakes" \
  --duration 30 \
  --dry-run

# Peak hook extraction: Analyze included hook compilation video
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video hook_viral_10 \
  --topic "Crypto wallet" --duration 30

# Peak hook extraction: Analyze custom video
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video path/to/any_viral_video.mp4 \
  --topic "App introduction" --duration 15

# Peak hook extraction: Dry-run (display analysis results only)
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video hook_trifecta \
  --topic "Side hustle" --dry-run
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --topic | Yes | - | Video topic/theme |
| --product | No | - | Product/service name |
| --duration | No | 30 | Video duration (seconds): 15, 30, 60 |
| --target | No | - | Target audience description |
| --tone | No | casual | Tone: casual, professional, energetic, storytelling |
| --hook-style | No | auto | Hook style: curiosity, fomo, social_proof, pattern_interrupt, contrarian |
| --split-screen | No | false | Include split screen instructions |
| --flash-text | No | true | Include flash text (rewatch trigger) |
| --loop | No | true | Include loop bridge (return to start) |
| --variants | No | 3 | Number of hook variations |
| --generate-storyboard | No | false | Call storyboard-generator after scenes.json generation |
| --character | No | - | Character description for storyboard |
| --session | No | - | Session name (output folder name) |
| --dry-run | No | false | Generate script only (minimal API calls) |
| --lang | No | ja | Script language: ja, en |
| --analyze-video | No | - | Peak hook extraction. Preset name (hook_viral_10, hook_trifecta, hook_600k_gmv) or file path |

## Output Structure

```
output/viral-scripts/
+-- YYYYMMDD_HHMMSS_session/
    +-- viral_script.json      # Main script (viral structured)
    +-- scenes.json            # storyboard-generator compatible format
    +-- hook_variants.json     # Hook variations
    +-- hook_analysis.json     # Peak hook analysis results (--analyze-video only)
    +-- storyboard/            # --generate-storyboard only
        +-- frames/
        +-- storyboard_sheet.png
        +-- scenes.json
```

## viral_script.json Format

```json
{
  "meta": {
    "topic": "Topic",
    "product": "Product name",
    "duration": 30,
    "target": "Target audience",
    "tone": "casual"
  },
  "hook": {
    "text": "Honestly I didn't want to share this but...",
    "duration": 3,
    "trigger_type": "curiosity_gap",
    "visual_note": "Eyes wide open, talking to camera",
    "emotion": "surprise"
  },
  "body": [
    {
      "text": "Actually, just by using this app, transfer fees...",
      "duration": 5,
      "visual_note": "Showing smartphone screen while explaining",
      "motion_type": "i2v"
    }
  ],
  "cta": {
    "text": "Link in profile. Check it out now",
    "duration": 3,
    "visual_note": "Pointing to bottom of screen",
    "emotion": "friendly"
  },
  "loop_bridge": {
    "enabled": true,
    "end_text": "That thing I mentioned earlier...",
    "connects_to": "hook",
    "visual_note": "Return to same camera angle as opening"
  },
  "flash_text": {
    "enabled": true,
    "text": "Did you watch to the end? Watch again",
    "color": "red",
    "duration_frames": 3,
    "position": "center"
  },
  "viral_techniques": {
    "split_screen": false,
    "captions": true,
    "lofi_aesthetic": true,
    "fast_pace": true,
    "speech_speed": 1.2
  },
  "hook_variants": [
    {
      "text": "99% of people don't know this...",
      "trigger_type": "curiosity_gap"
    },
    {
      "text": "If you miss this you'll seriously regret it",
      "trigger_type": "fomo"
    },
    {
      "text": "1 million people use it but nobody talks about it",
      "trigger_type": "social_proof"
    }
  ]
}
```

---

## Viral Technique Cheat Sheet

### 1. Opening 3-Second Hook (Most Important)

**Data**: 65%+ 3-second retention -> 4-7x impressions / engagement +340%

**7 Psychological Triggers** (used in 84.3% of viral videos):

| # | Trigger | English Hook Example |
|---|---------|---------------------|
| 1 | Pattern Interrupt | "Wait, look at this" |
| 2 | Curiosity Gap | "Nobody tells you this about..." |
| 3 | FOMO | "You're missing out on..." |
| 4 | Social Proof | "1M people already use this" |
| 5 | Emotional Arousal | "I can't believe this works" |
| 6 | Surprise | (wide eyes + 1s pause) |
| 7 | Personal Relevance | "If you're a [target], watch this" |

### 2. Modular Structure

```text
[Hook: 0-3s] -> [Body: 3-15s] -> [CTA: 15s+]
```

- Effect: Production cost -40%, test speed 2x
- Swap only the Hook part for A/B testing

### 3. Loop Bridge

- Effect: Rewatch = algorithm boost +84%
- 70% completion rate -> algorithm promotion
- 92% completion rate -> 3x reach (Sticky Content certification)
- Pattern: At end of video "About that thing I mentioned earlier..." -> loops back to start

### 4. Flash Text (Rewatch Trigger)

- Display red/black text for 2-3 frames (under 0.1 seconds) at the end
- Speed too fast to consciously read -> "Did I just see something?" -> Rewatch
- Text examples: "Watch again", "Hidden message", "Did you notice?"
- Color: Red (urgency/visibility) or white text on black background (mysterious)

### 5. Background Gameplay (Overlay Method)

- Full-screen background: Minecraft/Subway Surfers -> overlay main content on top
- TikTok style: Gameplay is full screen (1080x1920), main content on top half (1080x960)
- Effect: Average watch time +40%, comments/shares 2x
- Especially effective for 67% of Gen Z (18-24)
- Preset assets included: `subway_surfers`, `minecraft`
- Note: May damage brand image -> recommended for organic posts

### 6. Peak Hook Extraction

- Automatically identify the strongest hook moments from viral videos
- Scoring via video-frame-reader + Gemini Flash Vision
- Automatically generate restructured script proposals from extracted hook patterns
- 3 included hook compilation assets available for immediate analysis

### 7. Captions

- 85% watch on mute -> captions increase retention +31%, engagement +38%
- TikTok safe zone: Y position 55-65% (avoid top 15%, bottom 20%)
- Japanese: 5-8 chars per line, max 2 lines, bold white + black stroke 3px

### 8. Lo-fi Feel (UGC Style)

- UGC style vs professional quality: CTR 4x, conversion rate +29%
- iPhone-shot casual vibe
- Background: Home-like, cafe-like natural environments

### 9. Audio Pacing

- 1.1-1.3x speech speed -> prevents drop-off
- Reduce gaps to increase information density

---

## Related Skills

| Skill | Role | Integration Method |
|-------|------|-------------------|
| `storyboard-generator` | scenes.json -> storyboard images | Auto-integrate with `--generate-storyboard` |
| `video-editor` | Final video composition (captions/flash/background overlay) | `compose_video.py --flash-text --split-screen subway_surfers` |
| `video-frame-reader` | Video keyframe extraction | Auto-integrate with `--analyze-video` |
| `banner-creator` | Thumbnail generation | Run separately |
| `social-content` | Post text & hashtag generation | Run separately |

## Requirements

- `GEMINI_API_KEY`: For Gemini Flash (script generation)
- Python packages: google-genai, python-dotenv
- `storyboard-generator` dependencies (storyboard generation only)
- `ffmpeg` (video composition only)

## Trigger Phrases

- "Create a TikTok video script"
- "I want to make a viral video"
- "Short video script"
- "Generate a TikTok script"
- "I want to make a viral hit"
- "Reels video plan"

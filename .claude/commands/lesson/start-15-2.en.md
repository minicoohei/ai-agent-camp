---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~40 min"
prerequisites: ["setup-remotion"]
level: "intermediate"
tags: ["video", "remotion", "animation", "text", "slide-shoot"]
nonInteractiveMode: deferred
---
# Lesson 15-2: Remotion Animation Basics — Slide-Shoot Text Animation

## Learning Objectives

Use Remotion's `spring` / `interpolate` to create cool slide-in text animations.

| Item | Details |
|------|---------|
| Goal | Build slide-shoot style text animation videos using spring / interpolate |
| Duration | ~40 min |
| Tools | Remotion (React + FFmpeg local rendering) |
| Prerequisites | Node.js 18+, setup-remotion completed |
| Cost | **$0** (fully local, no external APIs) |
| Course page | [Module 15: Video Generation](https://ai-agent.camp/en/course/module-15) |

**Session flow:**
1. Understand Remotion basics
2. Learn `useCurrentFrame` / `spring` / `interpolate`
3. Build a slide-shoot text animation
4. Add stagger effects for multi-line text
5. Render the video

---

## Step 1: Remotion Basics

Remotion is a framework for **creating videos with React**:

- **Frame-based animation**: `useCurrentFrame()` gets the current frame number
- **spring()**: Natural spring physics. Control with `damping`, `mass`, `stiffness`
- **interpolate()**: Map frame numbers to values (e.g., frames 0→30 to opacity 0→1)
- **Rendering**: Local FFmpeg export to MP4. No API needed, $0 cost

```tsx
import { useCurrentFrame, spring, interpolate, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const progress = spring({ frame, fps, config: { damping: 16, mass: 0.5, stiffness: 120 } });
const translateX = interpolate(progress, [0, 1], [200, 0]);
const opacity = interpolate(progress, [0, 1], [0, 1]);
```

---

## Step 2: Create a Basic Slide-In Text

```
Create a slide-in text component in the mv-composer directory.

■ File: src/components/scenes/SlideShootText.tsx

■ Specs:
- Black background (#000000)
- Text slides in from right to left with fade-in
- Spring config: damping: 16, mass: 0.5, stiffness: 120
- Font: white, bold, 60px
- Single line of text from props

■ Reference: CinematicTextHook.tsx WordReveal pattern
- translateX: 200px → 0px slide-in
- opacity: 0 → 1 fade-in
```

---

## Step 3: Add Stagger Effects (Multi-Line Text)

```
Extend SlideShootText for multi-line stagger animation.

■ Specs:
- Accept text array (e.g., ["AI Agent Camp", "The Video Era", "Start Free Today"])
- Each line slides in sequentially (stagger: 15 frames apart)
- Configurable delayFrames per line
- Last line appears slower (lower stiffness)
- Hold for 2 seconds after all lines appear, then fade out

■ Register in Root.tsx:
- id: "SlideShootDemo", durationInFrames: 150, fps: 30, 1920x1080
```

---

## Step 4: Animation Variations

```
Add direction variants to SlideShootText (via direction prop):
1. "right" — slide from right (default)
2. "left" — slide from left
3. "bottom" — slide up from bottom
4. "scale" — scale 0.5 → 1.0 center fade-in

Optional: Add text glow (textShadow) and ambient orbs (ref: CinematicTextHook orbDrift)

Register: "SlideShoot-Right", "SlideShoot-Left", "SlideShoot-Bottom", "SlideShoot-Scale"
```

---

## Step 5: Render Videos

```bash
cd mv-composer
npx remotion render src/index.ts SlideShootDemo out/slide-shoot-demo.mp4
npx remotion render src/index.ts SlideShoot-Right out/slide-shoot-right.mp4
npx remotion render src/index.ts SlideShoot-Left out/slide-shoot-left.mp4
npx remotion render src/index.ts SlideShoot-Bottom out/slide-shoot-bottom.mp4
npx remotion render src/index.ts SlideShoot-Scale out/slide-shoot-scale.mp4
```

---

## Step 6: Quality Check with /motion-review

**After rendering, always run a quality review.**

```
/motion-review

Review the quality of the rendered SlideShootText component.

■ Check targets:
- src/components/scenes/SlideShootText.tsx
- out/slide-shoot-demo.mp4

■ Focus areas:
- Transitions: No black frames, natural fades
- Motion quality: No spring oscillation artifacts
- Typography: Font size and readability
- Overall polish
```

`/motion-review` runs a 26-point checklist for Remotion quality. Issues are rated P1 (critical) / P2 (important) / P3 (nice-to-have).

**If P1/P2 issues found**: Fix, re-render, and re-review.

---

## Step 7 (Advanced): Create Your Own Theme

Try making an original slide-shoot video with your own content:
- Self-introduction (Name → Title → Message)
- Product showcase (Service → Tagline → URL)
- Event announcement (Date → Venue → Title)

---

## Troubleshooting

- **Studio won't start**: Check Node.js ≥ 18, run `npm install`
- **Render error**: Check `ffmpeg -version`, verify Composition id matches
- **Jerky animation**: Increase damping (14-20), lower stiffness (100-150)
- **Japanese font missing**: Set fontFamily to "Noto Sans JP", "Hiragino Sans", sans-serif

---

## ✅ Checklist
- [ ] Understood useCurrentFrame / spring / interpolate
- [ ] Single text slide-in works
- [ ] Multi-line stagger animation works
- [ ] Tried 4 direction variants
- [ ] Rendered to MP4

---

## ➡️ Next Steps

```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "What would you like to do next?",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Open new window (/start-15-3)"},
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


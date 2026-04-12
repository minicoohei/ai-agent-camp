---
name: remotion-trace
description: "A workflow skill for reproducing professional-quality Remotion videos from reference videos. Triggered by 'I want to recreate from a reference video', 'Video trace', 'I want to make a PV', 'I want to create a Remotion video based on a reference'."
triggers:
  - I want to recreate from a reference video
  - Video trace
  - I want to make a PV
  - I want to create a Remotion video
  - Create video based on reference
  - remotion-trace
  - Remotion
---


# Remotion Video Trace

A workflow skill for reproducing professional-quality Remotion videos from reference videos.
A methodology established through real corporate PV production projects (16 iterations), systematized into a reusable framework.

## Trigger Words
"I want to create a Remotion video", "I want to make a PV", "Recreate from reference video", "Video trace"

## Prerequisites
- Node.js + Remotion (`mv-composer/` project or new)
- ffmpeg (frame extraction / audio processing)
- yt-dlp (reference video download)

---

## Part 1: Reference Research

### 1.1 Reference Video Sources

Use different sources depending on the purpose:

| Source | URL | Purpose |
|--------|-----|---------|
| Vimeo Staff Picks | `vimeo.com/channels/staffpicks` | Transitions, color grading |
| Art of the Title | `artofthetitle.com` | Title sequences, motion graphics |
| Stash Media | `stashmedia.tv` | CM/promo video trends |
| YouTube | Search by industry/competitors | Understanding industry standards for corporate PVs |
| Game trailers | Brikk etc. | Dynamic cuts and effects |

### 1.2 Clip Collection

Collect **5-10 second clips** at the "I want this scene's expression" level. Focus on specific directions/transitions, not entire videos.

```bash
# Download clips from YouTube/Vimeo
yt-dlp --download-sections "*57-59" -o "data/video_refs/{project}/{id}_%(section_start)s-%(section_end)s.%(ext)s" "https://youtube.com/watch?v={id}"

# For Vimeo
yt-dlp --download-sections "*20-30" -o "data/video_refs/{project}/vimeo_{id}_0020-0030.%(ext)s" "https://vimeo.com/{id}"
```

### 1.3 File Management

```
data/video_refs/{project_name}/
├── {videoId}_{startSec}-{endSec}.mp4   # Reference clips
├── frames/                              # Extracted frames (generated in Part 2)
└── README.md                           # Source/purpose notes for each clip
```

**Always record sources in README.md**:
```markdown
## {videoId}_{start}-{end}.mp4
- Source: {Company name} Official PV (YouTube)
- Purpose: Person introduction wipe effect (dark background → rectangle scatter → photo reveal)
```

---

## Part 2: Frame Analysis

### 2.1 Frame Extraction

```bash
# Extract frames from reference video (6-10fps recommended)
ffmpeg -i data/video_refs/{project}/clip.mp4 \
  -vf "fps=8" \
  data/video_refs/{project}/frames/clip_%04d.png

# Extract specific section only
ffmpeg -i clip.mp4 -ss 2.0 -t 3.0 -vf "fps=10" frames/%04d.png
```

### 2.2 Visual Analysis Checklist

Open extracted frames with the Read tool and analyze from these perspectives:

- [ ] **Transition technique**: Wipe/fade/scale/clipPath/slide
- [ ] **Timing & easing**: spring/ease-out/linear/stepped
- [ ] **Text expression**: Punch-in/typewriter/cascade/slide-in
- [ ] **Background treatment**: Blackout/blur/particle/gradient/image overlay
- [ ] **Color & contrast**: Brand colors/color temperature/light-dark balance
- [ ] **Layout**: Grid/full-bleed/split/centering
- [ ] **BGM sync points**: Cut switches on beat drops/text appearances

### 2.3 Recording Analysis Results

Describe the following for each clip:
```
## clip: {videoId}_{start}-{end}.mp4
### Animation Breakdown
- 0.0s: Dark background + white rectangles scattered in random positions
- 0.5s: clipPath inset wipes photo in from left to right
- 1.5s: Full photo display + name caption at bottom-left (white text with shadow)
- 3.0s: Split into 3 strips, each strip shows different angle
### Remotion Implementation Notes
- clipPath: Achievable with `inset(0 ${100 - progress}% 0 0)`
- Rectangle scatter: position:absolute + random top/left/rotation
```

### 2.4 draw.io PNG → React SVG Animation Guide

Steps to convert diagrams created with draw.io etc. into React SVG animations on Remotion.

#### Why Convert

| Aspect | PNG (as-is) | React SVG |
|--------|------------|-----------|
| Animation | Not possible (static image) | Elements appear sequentially with `spring()` |
| Resolution | Blurry when enlarged | SVG is sharp at any size |
| Fine-tuning | Re-edit in draw.io → re-export | Control px values and timing instantly in code |
| 2-phase transition | Not possible | Display different info in first/second half of one scene |

#### Conversion Steps

1. **Decompose elements**: Break down draw.io diagram into nodes (boxes), arrows (connectors), text labels. Note coordinates, sizes, and colors of each element
2. **Convert to React components**: Re-implement each element with SVG primitives
   ```typescript
   // Node → rect + text
   <rect x={node.x} y={node.y} width={node.w} height={node.h}
     rx={8} fill={node.color} opacity={nodeOpacity} />
   <text x={node.x + node.w/2} y={node.y + node.h/2}
     textAnchor="middle" dominantBaseline="central"
     fill="#FFF" fontSize={16}>{node.label}</text>

   // Arrow → path or line
   <line x1={arrow.x1} y1={arrow.y1} x2={arrow.x2} y2={arrow.y2}
     stroke="#666" strokeWidth={2} markerEnd="url(#arrowhead)" />
   ```
3. **Add staggered animation**: Make elements appear sequentially with `spring()`
   ```typescript
   const nodeOpacity = spring({
     frame: frame - index * STAGGER_DELAY,
     fps, config: { damping: 14, mass: 0.6, stiffness: 160 },
   });
   const nodeScale = spring({
     frame: frame - index * STAGGER_DELAY,
     fps, config: { damping: 14, mass: 0.6, stiffness: 160 },
   });
   // style: { opacity: nodeOpacity, transform: `scale(${nodeScale})` }
   ```
4. **Coordinate management**: Manage SVG path coordinates for arrows as TypeScript constants, updating in sync when node positions change
   ```typescript
   const NODES = {
     input:   { x: 100, y: 200, w: 180, h: 60, color: '#3B82F6', label: 'Input' },
     process: { x: 400, y: 200, w: 180, h: 60, color: '#10B981', label: 'Process' },
     output:  { x: 700, y: 200, w: 180, h: 60, color: '#F59E0B', label: 'Output' },
   } as const;
   ```

#### Check

If a static PNG is displayed via `<Img>` for more than 3 seconds → flag as "consider animation".
Linked with motion-review skill's **J3** check item.

---

## Part 3: BPM & Audio Analysis

### 3.1 BPM Analysis

```bash
# Extract audio from reference video
ffmpeg -i reference.mp4 -vn -acodec pcm_s16le ref_audio.wav

# Manual count: Count beats in 10 seconds and multiply by 6
# Or visualize waveform with ffmpeg energy detection
ffmpeg -i ref_audio.wav -af "showinfo" -f null - 2>&1 | head -50
```

### 3.2 Beat-Aligned Duration Design

```
BPM = 103:
1 beat = 60/103 = 0.5825s
5 beats = 2.91s
9 beats = 5.24s
```

**sectionDurations must always be integer multiples of beat length**. This ensures BGM beats sync naturally with scene transitions.

### 3.3 BGM Generation (fal.ai Stable Audio)

**Stable Audio 2.5** (recommended): Can generate up to 190 seconds in one shot. No joint issues.

```javascript
// fal.ai Stable Audio 2.5 (max 190 seconds)
const result = await fal.subscribe("fal-ai/stable-audio-25/text-to-audio", {
  input: { prompt: "...", seconds_total: 80 },
});
const url = result.data?.audio?.url;
```

```bash
# Apply fade-out at the end (4 seconds) and convert to mp3
ffmpeg -y -i raw.wav -af "afade=t=out:st=76:d=4" -q:a 2 bgm_final.mp3
```

**Alternative models (fal.ai)**:
| Model | API ID | Max Length | Purpose |
|-------|--------|-----------|---------|
| Stable Audio 2.5 | `fal-ai/stable-audio-25/text-to-audio` | 190s | General (recommended) |
| Beatoven maestro | `beatoven/music-generation` | 150s | Licensed commercial BGM |
| CassetteAI | `cassetteai/music-generator` | 180s | Low cost, fast |
| Stable Audio (old) | `fal-ai/stable-audio` | 47s | **Not recommended** (requires split+crossfade) |

**Legacy method (only for 47-second limit)**: Concatenate multiple parts with crossfade

```bash
ffmpeg -i part1.mp3 -i part2.mp3 \
  -filter_complex "[0][1]acrossfade=d=2:c1=tri:c2=tri" \
  -y bgm_full.mp3
```

### 3.4 Narration Generation (ElevenLabs TTS)

Workflow established in TaxAccountantDemo v34-v40.

#### 3.4.1 Voice Generation
```bash
# ElevenLabs multilingual v2 + recommended settings for Japanese
VOICE_ID="StTDrGrPSyfaHGmzwXbj"  # Masa (calm Japanese male voice)
SETTINGS='{"stability":0.70,"similarity_boost":0.80,"style":0.10,"use_speaker_boost":true}'

curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"text":"Text here","model_id":"eleven_multilingual_v2","voice_settings":'"${SETTINGS}"'}' \
  --output "narration.mp3"
```

#### 3.4.2 Chinese Pronunciation Contamination Countermeasures (Important)
ElevenLabs multilingual v2 sometimes reads Japanese kanji with Chinese pronunciation.

**Countermeasure**: Replace problematic kanji with hiragana before generation
```
税理士 → ぜいりし    記帳 → きちょう      仕訳 → しわけ
取引 → とりひき      損益 → そんえき      即時 → そくじ
即座 → そくざ        監視 → かんし        瞬時 → しゅんじ
24時間365日 → にじゅうよじかん さんびゃくろくじゅうごにち
12,800円 → いちまん にせん はっぴゃく えん
```

**Raising stability to 0.55→0.70** reduces Chinese contamination.

#### 3.4.3 Gemini Pronunciation Evaluation (Required QA)
```python
import google.generativeai as genai
model = genai.GenerativeModel("gemini-2.0-flash")
audio = genai.upload_file("narration.mp3")
resp = model.generate_content([
    audio,
    "Accurately transcribe this Japanese audio."
    "Check if any Chinese pronunciation has been mixed in, and point out any reading errors."
])
```
Run for all clips, regenerate only problematic clips.

#### 3.4.4 atempo Speed Adjustment
When narration length exceeds scene length, adjust with ffmpeg atempo:
```bash
# Example: Fit 5.1s narration into 3.6s (atempo 1.42)
ffmpeg -y -i raw.mp3 -af "atempo=1.42" adjusted.mp3
```
**Limit**: atempo 1.35x is the upper limit. Beyond that, speech becomes too fast to understand → shorten text or extend scene duration.

#### 3.4.5 Integration into Remotion
```typescript
// Define narration prefix in props
interface Props {
  narrationPrefix?: string;  // e.g. "tax/audio/narration/v4_s"
}

// Place Audio in each scene
{p.narrationPrefix && starts.map((st, i) => {
  const padNum = String(i + 1).padStart(2, "0");
  return (
    <Sequence key={`narr-${i}`} from={st} durationInFrames={frames[i]}>
      <Audio src={staticFile(`${p.narrationPrefix}${padNum}.mp3`)} volume={1.2} />
    </Sequence>
  );
})}
```

**Volume balance**: Narration `volume={1.0-1.2}`, BGM `volume={0.18-0.25}`

### 3.5 Audio Rules
- **No SE, drive through with one BGM track** is the basic style
- Consider key changes only for videos over 45 seconds
- When inserting live footage directly, use `muted` to prevent BGM interference
- **Videos with narration**: Lower BGM volume to 0.20-0.25 to make narration stand out
- **Caption-narration alignment**: Caption text should match narration content (unify % notation for numbers too)

---

## Part 4: Storyboard

### 4.1 Scene Division Table

Define all scenes using the following template before starting implementation:

| Scene | Duration | Beats | Reference Clip | Direction Overview | Component Name |
|-------|----------|-------|---------------|-------------------|----------------|
| 01 | 2.91 | 5 | {clip_id} | Logo blur→focus + particles | LogoFocusIn |
| 02 | 2.91 | 5 | {clip_id} | Value proposition punch-in | ValuePunch |
| 03 | 5.24 | 9 | {clip_id} | Member introduction wipe | MemberShowcase |
| ... | | | | | |

### 4.2 Props Interface Design

```typescript
interface CompositionProps {
  // Common to all scenes
  bgmSrc?: string;
  sectionDurations?: number[];  // Beat-aligned

  // Scene-specific props
  logoSrc?: string;
  // ...
}

export const DEFAULT_PROPS: CompositionProps = {
  sectionDurations: [2.91, 2.91, 5.24, 5.24, 12.23, 6.99, 8.74], // BPM multiples
  bgmSrc: '{project}/audio/bgm.mp3',
  // ...
};
```

### 4.3 sectionDurations Priority

**Finalize the sectionDurations array first** → Each scene component receives frame count and distributes internally. Root.tsx's `durationInFrames` is auto-calculated as `Math.round(sum(sectionDurations) * FPS)`.

---

## Part 5: Implementation Patterns (Remotion Technique Collection)

13 techniques established through corporate PV production. Directly applicable to new projects.

### P1: Blur→Focus Logo
```typescript
const blurPx = interpolate(frame, [0, 20], [20, 0], { extrapolateRight: 'clamp' });
// style: { filter: `blur(${blurPx}px)` }
```
Start with blurred logo image that gradually becomes sharp. Don't recreate logos with text (font mismatch risk).

### P2: Punch-in Text
```typescript
const scale = spring({ frame: f, fps, config: { damping: 12, mass: 0.5, stiffness: 200 } });
// style: { transform: `scale(${scale})`, opacity: Math.min(1, f / 5) }
```
Text appears with a bounce effect. Don't set `damping` too low or oscillation becomes noticeable—10-15 is appropriate.

### P3: clipPath Wipe
```typescript
const progress = interpolate(frame, [startF, endF], [0, 100], { extrapolateRight: 'clamp' });
// style: { clipPath: `inset(0 ${100 - progress}% 0 0)` }
```
Photo wipes in from right to left. Change direction by adjusting `inset()` values.

### P4: Rectangle Scatter → Photo Wipe
A two-stage effect: scatter random white/colored rectangles on a dark background, then reveal photo with clipPath.
```typescript
// Phase A: Rectangle scatter (no text)
{rects.map((r, i) => (
  <div key={i} style={{
    position: 'absolute', top: r.y, left: r.x,
    width: r.w, height: r.h, background: r.color,
    transform: `rotate(${r.rot}deg)`,
    opacity: interpolate(f, [0, phaseAEnd], [1, 0])
  }} />
))}
// Phase B: Photo wipe with clipPath
```

### P5: 3-Strip Split
Divide the screen into 3 vertical strips, placing different angle photos in each. Slightly staggering timing per strip creates a rich feel.

### P6: Apple-style Card Grid
```typescript
const scrollY = interpolate(frame, [0, dur], [0, -totalHeight], { extrapolateRight: 'clamp' });
// Scroll grid with translateY
// Decelerate at specific card → cursor follow → click effect
```
Calculate cursor position by reverse-calculating card's actual screen coordinates from scroll offset.

### P7: 4-Panel Stagger
```typescript
const panelDelay = panelIndex * 4; // Frame-unit offset
const slideIn = interpolate(frame - panelDelay, [0, 15], [100, 0], { extrapolateRight: 'clamp' });
// Display different images per panel using baseOffset
const imgIdx = (cycleIndex + pi * Math.ceil(images.length / 4)) % images.length;
```
Stagger update timing of 4-split panels. **baseOffset is required to prevent all panels from showing the same image**.

### P8: Count-up
```typescript
// NEVER use spring() as it oscillates
const eased = 1 - Math.pow(1 - ratio, 3); // cubic ease-out
const displayNum = Math.round(eased * targetNumber);
```
**Using spring() for count-up causes numbers to go up, down, then back. Use cubic ease-out.**

### P9: CSS Particles
```typescript
// Alternative to i2v. position:absolute + CSS animation for floating dots
{particles.map((p, i) => (
  <div key={i} style={{
    position: 'absolute', borderRadius: '50%',
    width: p.size, height: p.size, background: p.color,
    top: `${p.y}%`, left: `${p.x}%`, opacity: p.opacity,
    animation: `float ${p.duration}s ease-in-out infinite`,
  }} />
))}
```
**i2v (Kling etc.) quality is mediocre** → Use CSS particles or Remotion animations instead.

### P10: SceneWrap Exit
```typescript
const exitProgress = interpolate(frame, [dur - exitFrames, dur], [0, 1], { extrapolateLeft: 'clamp' });
// style: { transform: `scale(${1 - 0.05 * exitProgress})`, opacity: 1 - exitProgress }
```
Natural transition to next scene with `scale: 0.95` + `opacity: 0` at scene end. Disable with `noExit` prop.

### P11: Face Protection
```typescript
// objectFit: "cover" crops faces → "contain" + blurred background
<div style={{ position: 'relative', overflow: 'hidden' }}>
  {/* Blurred background */}
  <Img src={src} style={{ position: 'absolute', width: '120%', filter: 'blur(20px)', objectFit: 'cover' }} />
  {/* Main image */}
  <Img src={src} style={{ position: 'relative', objectFit: 'contain', width: '100%', height: '100%' }} />
</div>
```

### P12: Text Readability
```typescript
// Black bars look bad → use text-shadow for readability
style: {
  textShadow: '0 2px 8px rgba(0,0,0,0.8), 0 0 20px rgba(0,0,0,0.5), 0 0 40px rgba(0,0,0,0.3)',
  // Keep font size large (minimum 48px)
}
```

### P13: Direct Video Insertion
```typescript
import { OffthreadVideo } from 'remotion';
// <OffthreadVideo src={staticFile('{project}/video/live_muted.mp4')} muted />
```
Insert live footage etc. with `muted` to prevent BGM track interference. Pre-extract thumbnails with ffmpeg:
```bash
ffmpeg -i video.mp4 -ss 5 -frames:v 1 thumb.jpg
```

---

## Part 6: Comparison Loop

### 6.1 Rendering

```bash
cd mv-composer
npx remotion render src/index.ts {CompositionId} out/{Name}_v{N}.mp4
```

### 6.2 Output Video Frame Extraction

```bash
ffmpeg -i out/{Name}_v{N}.mp4 -vf "fps=8" data/video_refs/{project}/output_frames/v{N}_%04d.png
```

### 6.3 Comparison Analysis

Place reference video frames and output frames side by side, checking from a **professional video creator's perspective**:

- [ ] Timing discrepancies (frame-by-frame comparison)
- [ ] Easing quality (mechanical vs. organic)
- [ ] Color temperature/contrast differences
- [ ] Text size, placement, readability
- [ ] Image crop, aspect ratio (face cropping)
- [ ] BGM sync point discrepancies
- [ ] "Dead frames" (static sections with no movement for 0.5s+)
- [ ] Black frames between scenes (unintended blackouts)
- [ ] Duplicate display (same text/image appearing twice)

### 6.4 Fix → Re-render

Fix noted issues → render as `v{N+1}` → compare again.
**Iterations from v1→v18 are normal. 5-10 iterations is standard for convergence.**

---

## Part 7: Lessons Learned (Prohibited & Recommended)

### Prohibited
| Rule | Reason |
|------|--------|
| Don't use emoji as icons | Font missing in rendering environment → Use SVG/images |
| Don't rely on i2v (Kling/fal.ai etc.) | Quality is mediocre, Remotion CSS can substitute |
| Don't use spring() for count-up | Oscillates — numbers go up and back down |
| Don't use objectFit "cover" for people photos | Crops faces → "contain" + blurred bg |
| No black bar captions | Looks bad → text-shadow for readability |
| Don't use images over 7MB as-is | Decode error → `sips --resampleWidth 1200` |
| Don't recreate logos with text | Font mismatch → Use logo images |

### Recommended
| Rule | Reason |
|------|--------|
| No SE, one BGM track | Creates driving momentum |
| sectionDurations as BPM multiples | Natural beat sync |
| Resize images to 1200px width or less | Remotion decode stability |
| Overlap scenes by ±5 frames | Prevents black frames |
| Name captions once per scene | Twice feels awkward |
| Distribute panel images with baseOffset | Prevents all panels showing same image |
| Insert live footage as muted | Prevents BGM interference |
| Get brand colors from OGP/official site | Visual estimation is inaccurate |

---

## Overall Workflow

```
[1. Reference Research]
  ↓ Collect reference clips (5-10 second units)
[2. Frame Analysis]
  ↓ Extract frames → Decompose direction
[3. BPM & Audio]
  ↓ Tempo analysis → Finalize sectionDurations → Generate BGM
[4. Storyboard]
  ↓ Scene division table → Props design
[5. Implementation]
  ↓ Implement using pattern collection (P1-P13)
[6. Comparison Loop]  ←─── 5-10 iterations
  ↓ Render → Frame comparison → Fix
[7. Final Check]
  ↓ Lessons Learned check → Complete
```

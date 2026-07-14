---
name: motion-review
description: "Quality reviews Remotion compositions with a 20-item checklist. Triggered by requests like 'video review', 'motion review', 'Remotion quality check', etc."
triggers:
  - video review
  - video quality check
  - motion review
  - motion-review
  - Remotion quality check
  - PV review
  - video review
---

# Motion Review Skill

A skill that reviews Remotion compositions from a professional video creator's perspective and provides quality improvement instructions.
Automatically invoked at the Quality Review step of the GTM Manager / Campaign Orchestrator.

## Trigger Words

`motion review`, `video review`, `video quality check`, `PV review`, `Remotion quality check`

## Input

- Path to a Remotion composition file (`.tsx`)
- (Optional) Path to a rendered mp4

## Execution Flow

```
1. Read composition .tsx
2. Run 26-point checklist (A-I categories below)
3. Output structured review with P1/P2/P3 ratings
4. If any P1 exists -> VERDICT: FIX_REQUIRED
5. If P2 only -> VERDICT: FIX_RECOMMENDED
6. If P3 only -> VERDICT: PASS
```

## Manual QA Frame Extraction

After rendering, extract 12 evenly spaced frames directly with `ffprobe` and `ffmpeg`:

```bash
VIDEO=out/Composition_v1.mp4
QA_DIR=data/qa_Composition_v1
mkdir -p "$QA_DIR"
DURATION="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")"
ffmpeg -y -i "$VIDEO" -vf "fps=12/${DURATION}" -frames:v 12 "$QA_DIR/qa_%02d.png"
```

## Tone (Review Output Style)

- Use the tone of "a professional video director doing a final pre-delivery check"
- Each check item is formatted as "OK -- reason" or "P1/P2/P3 -- current state -> fix instruction". No subjective impressions or vague adjectives
- Acknowledge 1-2 good points before listing issues (e.g., "A1 OK -- 12f OVERLAP is secured with no black frames. B1 P1 -- spring config uses damping:12 for all elements -> separate into 4 tiers: snappy/balanced/weighty/liquid")
- Fix instructions must include the 3-point set: "filename:line number + current code + fixed code"

## Trade-off Decision Criteria

- Fixing all P1s > fixing many P2s (even one P1 means FIX_REQUIRED)
- Reliable stasis with interpolate > good-looking spring with oscillation risk
- Splitting scenes to reduce information density > cramming into one scene to save duration
- Larger OVERLAP (12f) for safety margin > minimal (4f) to extend scene length

---

## 26-Point Pro Review Checklist

### Category A: Transitions

#### A1. Black Frames Between Scenes [P1]
**Check**: Does the Sequence overlap by OVERLAP frames?
- NG: Non-overlapping Sequence (`from={starts[i]}` matches previous scene's end)
- OK: `from={starts[i] - OVERLAP}`, `durationInFrames={frames[i] + OVERLAP * 2}`
- **Criteria**: P1 if 2+ frames of black appear

#### A1.5. Crossfade + Zoom Transition [P1]
**Check**: Are phases smoothly connected with CrossFadeWrap (opacity fade + subtle scale)?
- NG: Only hard cuts with white flash (opacity 0.85) -> choppy feel
- OK: XFADE=10 frames (0.33s) overlap + exit `scale(1.0->1.03)` for depth + supporting thin flash (opacity 0.2)
- **Criteria**: P1 if no opacity crossfade between Sequences

#### A2. Transition Method Diversity [P2]
**Check**: Are all scenes using the same exit/entrance pattern?
- NG: All `opacity fade` only
- OK: Mix of Direction Blur, clipPath wipe, scale zoom, flash wipe
- **Criteria**: OK if 3+ different transition methods exist

#### A3. clipPath Continuity [P2]
**Check**: Are clipPath wipes linked in Before->After comparison scenes?

---

### Category B: Motion Quality

#### B1. Spring Profile Differentiation [P1]
**Check**: Are different spring configs used based on element weight?
- NG: All elements use the same `{ damping: 12, mass: 0.5, stiffness: 200 }`
- OK: At least 4 tiers (snappy / balanced / weighty / liquid) differentiated
- **Criteria**: P1 if 2 or fewer variants

#### B2. Secondary Motion [P2]
**Check**: Are at least 2 of the following implemented?
- Post-landing breathing (sin wave micro-movement +/-1-2%)
- Follow-through rotation (slight rotation +/-2-3deg on entrance)
- Scale bounce (scale 0.9->1.0 simultaneous with opacity)
- Post-count pulse (pulsation after counter animation completes)
- Drift (upward drift + slight scale-up after all text enters)

#### B3. BPM Sync [P2]
**Check**: Are sectionDurations and animation delays on the beat grid?

---

### Category C: Visual Polish

#### C1. Film Grain Animation [P1]
**Check**: Does Film Grain change every frame?
- NG: Fixed seed (`seed='2'`) -> frozen texture = worse than none
- OK: `seed={frame % 5}` for frame-by-frame rotation
- **Criteria**: P1 if Film Grain exists with a fixed seed (remove or fix)

#### C2. Background Ken Burns [P2]
**Check**: Do i2v / image backgrounds have subtle zoom (Ken Burns)?

#### C3. Vignette + Grain + ScanLines [P3]
**Check**: Are the following visual filters applied?

---

### Category D: Typography

#### D1. Font Size Readability [P1]
**Check**: Is the smallest text readable in 1080p video?
- NG: Result rows 14px, labels 12px (unreadable during video playback)
- OK: Body text 18px+, labels 14px+
- **Criteria**: P1 if any body text is below 18px

#### D2. Typography Base Settings [P3]
**Check**: Are the following configured?
- WebkitFontSmoothing: "antialiased"
- textRendering: "optimizeLegibility"
- lineHeight explicitly specified
- letterSpacing systematic (4 tiers: tight / normal / wide / label)

---

### Category E: Color & Layout

#### E1. Color Temperature Shift [P3]
#### E2. Layout Asymmetry [P2]

---

### Category F: Content & Timing Integrity

#### F1. Typing Animation Frame Calculation [P1]
#### F2. Sub-pixel Rendering Blur [P1]
#### F3. Text Readability on Backgrounds [P1]
#### F4. Logo/Image Transparency and Background Interference [P2]
#### F5. Scroll Range and Content Volume Alignment [P2]
#### F6. Card Stagger Exceeding Section Duration [P1]
#### F7. BGM Duration vs Video Duration Mismatch [P2]
#### F8. Label/Header Consistency [P2]

---

### Category G: Production Implementation Quality

#### G1. --props Default Value Override Failure [P1]
#### G2. Linter/External Tool File Rollback [P1]
#### G3. Focus Zoom Screen Overflow [P1]
#### G4. Insufficient Subtitle Display Time [P2]
#### G5. Inconsistent Subtitle Font Sizes [P2]
#### G6. Text Residue at Scene Boundaries [P2]
#### G7. Photo Count and Layout Mismatch [P2]
#### G8. BGM Generation Prompt Differentiation [P3]
#### G9. Always-On vs Sequential Display Selection [P3]

---

### Category H: Content Quality

#### H9. Claude Code UI Color Consistency [P1]
**Check**: Is the Claude Code UI representation using black (official) rather than purple (Cursor-style)?

#### H10. Brand Icon Consistency [P2]
#### H11. SVG Diagram Center Alignment [P2]

For full details on each check item, refer to the original SKILL.md which contains implementation code examples and fix patterns for every item.

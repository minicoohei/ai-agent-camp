import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { SHOWCASE_FONT } from "../../constants";

// ─── Types ──────────────────────────────────────────────
interface ComparisonItem {
  label: string;
  before: string;
  after: string;
}

interface TimeComparisonProps {
  comparisons: ComparisonItem[];
}

// ─── SVG Illustrations ──────────────────────────────────

// LP制作: Browser window assembling
const LPIllustration: React.FC<{ progress: number }> = ({ progress }) => {
  const headerP = Math.min(1, progress * 3);
  const block1P = Math.min(1, Math.max(0, progress * 3 - 0.8));
  const block2P = Math.min(1, Math.max(0, progress * 3 - 1.5));
  const block3P = Math.min(1, Math.max(0, progress * 3 - 2.2));

  return (
    <svg width={280} height={280} viewBox="0 0 280 280" fill="none">
      {/* Browser frame */}
      <rect x={20} y={20} width={240} height={240} rx={12} stroke="rgba(255,255,255,0.15)" strokeWidth={1.5} fill="rgba(255,255,255,0.03)" />
      {/* Title bar dots */}
      <circle cx={40} cy={36} r={4} fill="#FF5F56" opacity={headerP} />
      <circle cx={54} cy={36} r={4} fill="#FFBD2E" opacity={headerP} />
      <circle cx={68} cy={36} r={4} fill="#27C93F" opacity={headerP} />
      {/* URL bar */}
      <rect x={90} y={30} width={150} height={12} rx={6} fill="rgba(255,255,255,0.08)" opacity={headerP} />
      {/* Divider */}
      <line x1={20} y1={50} x2={260} y2={50} stroke="rgba(255,255,255,0.08)" strokeWidth={1} opacity={headerP} />
      {/* Hero block */}
      <rect x={40} y={62} width={200} height={50} rx={6} fill="rgba(100,140,255,0.15)" opacity={block1P} />
      <rect x={60} y={72} width={120} height={8} rx={4} fill="rgba(100,140,255,0.3)" opacity={block1P} />
      <rect x={80} y={86} width={80} height={6} rx={3} fill="rgba(100,140,255,0.15)" opacity={block1P} />
      {/* Content block 1 */}
      <rect x={40} y={122} width={95} height={60} rx={6} fill="rgba(16,185,129,0.12)" opacity={block2P} />
      <rect x={145} y={122} width={95} height={60} rx={6} fill="rgba(16,185,129,0.12)" opacity={block2P} />
      <rect x={50} y={134} width={60} height={6} rx={3} fill="rgba(16,185,129,0.2)" opacity={block2P} />
      <rect x={155} y={134} width={60} height={6} rx={3} fill="rgba(16,185,129,0.2)" opacity={block2P} />
      {/* Content block 2 */}
      <rect x={40} y={195} width={200} height={45} rx={6} fill="rgba(139,92,246,0.1)" opacity={block3P} />
      <rect x={60} y={207} width={100} height={6} rx={3} fill="rgba(139,92,246,0.2)" opacity={block3P} />
      <rect x={60} y={219} width={140} height={6} rx={3} fill="rgba(139,92,246,0.12)" opacity={block3P} />
    </svg>
  );
};

// 競合調査: Magnifying glass + bar chart
const ResearchIllustration: React.FC<{ progress: number }> = ({ progress }) => {
  const lensP = Math.min(1, progress * 2.5);
  const bar1P = Math.min(1, Math.max(0, progress * 3 - 0.8));
  const bar2P = Math.min(1, Math.max(0, progress * 3 - 1.3));
  const bar3P = Math.min(1, Math.max(0, progress * 3 - 1.8));
  const bar4P = Math.min(1, Math.max(0, progress * 3 - 2.3));

  return (
    <svg width={280} height={280} viewBox="0 0 280 280" fill="none">
      {/* Magnifying glass */}
      <circle cx={100} cy={90} r={40} stroke="rgba(100,140,255,0.4)" strokeWidth={2.5} fill="rgba(100,140,255,0.05)" opacity={lensP} />
      <line x1={128} y1={118} x2={155} y2={145} stroke="rgba(100,140,255,0.4)" strokeWidth={3} strokeLinecap="round" opacity={lensP} />
      {/* Lens highlight */}
      <path d="M75 75 Q85 65 95 70" stroke="rgba(255,255,255,0.15)" strokeWidth={2} strokeLinecap="round" opacity={lensP} />
      {/* Bar chart */}
      <rect x={60} y={250 - 60 * bar1P} width={30} height={60 * bar1P} rx={4} fill="rgba(100,140,255,0.3)" />
      <rect x={100} y={250 - 90 * bar2P} width={30} height={90 * bar2P} rx={4} fill="rgba(16,185,129,0.3)" />
      <rect x={140} y={250 - 75 * bar3P} width={30} height={75 * bar3P} rx={4} fill="rgba(139,92,246,0.3)" />
      <rect x={180} y={250 - 110 * bar4P} width={30} height={110 * bar4P} rx={4} fill="rgba(245,158,11,0.3)" />
      {/* Baseline */}
      <line x1={50} y1={250} x2={220} y2={250} stroke="rgba(255,255,255,0.1)" strokeWidth={1} />
    </svg>
  );
};

// 議事録作成: Document with text lines
const DocumentIllustration: React.FC<{ progress: number }> = ({ progress }) => {
  const docP = Math.min(1, progress * 2);
  const line1P = Math.min(1, Math.max(0, progress * 4 - 0.8));
  const line2P = Math.min(1, Math.max(0, progress * 4 - 1.3));
  const line3P = Math.min(1, Math.max(0, progress * 4 - 1.8));
  const line4P = Math.min(1, Math.max(0, progress * 4 - 2.3));
  const line5P = Math.min(1, Math.max(0, progress * 4 - 2.8));
  const checkP = Math.min(1, Math.max(0, progress * 4 - 3.2));

  return (
    <svg width={280} height={280} viewBox="0 0 280 280" fill="none">
      {/* Document */}
      <rect x={50} y={20} width={180} height={230} rx={10} stroke="rgba(255,255,255,0.15)" strokeWidth={1.5} fill="rgba(255,255,255,0.03)" opacity={docP} />
      {/* Header */}
      <rect x={70} y={40} width={100} height={10} rx={5} fill="rgba(139,92,246,0.25)" opacity={docP} />
      <line x1={70} y1={60} x2={210} y2={60} stroke="rgba(255,255,255,0.08)" strokeWidth={1} opacity={docP} />
      {/* Text lines writing in */}
      <rect x={70} y={75} width={140 * line1P} height={6} rx={3} fill="rgba(255,255,255,0.15)" />
      <rect x={70} y={95} width={120 * line2P} height={6} rx={3} fill="rgba(255,255,255,0.12)" />
      <rect x={70} y={115} width={150 * line3P} height={6} rx={3} fill="rgba(255,255,255,0.15)" />
      <rect x={70} y={135} width={110 * line4P} height={6} rx={3} fill="rgba(255,255,255,0.1)" />
      <rect x={70} y={155} width={130 * line5P} height={6} rx={3} fill="rgba(255,255,255,0.12)" />
      {/* Checkmark */}
      <circle cx={200} cy={200} r={20} fill="rgba(16,185,129,0.2)" opacity={checkP} />
      <path d="M190 200 L197 207 L212 192" stroke="#10B981" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" opacity={checkP} />
    </svg>
  );
};

// ─── AfterBurst ─────────────────────────────────────────
const AfterBurst: React.FC<{ startFrame: number; x: number; y: number }> = ({
  startFrame, x, y,
}) => {
  const frame = useCurrentFrame();
  const elapsed = frame - startFrame;

  if (elapsed < 0 || elapsed > 35) return null;

  const ring1Scale = interpolate(elapsed, [0, 20], [0.3, 4], { extrapolateRight: "clamp" });
  const ring1Opacity = interpolate(elapsed, [0, 5, 20], [0, 0.9, 0], { extrapolateRight: "clamp" });
  const ring2Scale = interpolate(elapsed, [5, 30], [0.5, 3], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ring2Opacity = interpolate(elapsed, [5, 10, 30], [0, 0.6, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div style={{ position: "absolute", left: x, top: y, width: 0, height: 0, pointerEvents: "none" }}>
      <div style={{
        position: "absolute", width: 60, height: 60, marginLeft: -30, marginTop: -30,
        borderRadius: "50%", border: "2px solid rgba(16,185,129,0.8)",
        transform: `scale(${ring1Scale})`, opacity: ring1Opacity,
        boxShadow: "0 0 20px rgba(16,185,129,0.4)",
      }} />
      <div style={{
        position: "absolute", width: 40, height: 40, marginLeft: -20, marginTop: -20,
        borderRadius: "50%", border: "1.5px solid rgba(16,185,129,0.6)",
        transform: `scale(${ring2Scale})`, opacity: ring2Opacity,
      }} />
    </div>
  );
};

// ─── Single Comparison Slide ────────────────────────────
const ComparisonSlide: React.FC<{
  item: ComparisonItem;
  index: number;
  slideStart: number;
  slideDuration: number;
}> = ({ item, index, slideStart, slideDuration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - slideStart;
  if (localFrame < -5 || localFrame > slideDuration + 10) return null;

  // Fade in/out
  const fadeIn = interpolate(localFrame, [0, 15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const fadeOut = interpolate(localFrame, [slideDuration - 15, slideDuration], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // SVG illustration progress
  const svgProgress = spring({
    frame: Math.max(0, localFrame),
    fps,
    config: { damping: 20, mass: 1, stiffness: 60 },
  });

  // Label entrance
  const labelE = spring({
    frame: Math.max(0, localFrame - 15),
    fps,
    config: { damping: 18, mass: 0.5, stiffness: 120 },
  });

  // Before value
  const beforeE = spring({
    frame: Math.max(0, localFrame - 30),
    fps,
    config: { damping: 18, mass: 0.5, stiffness: 100 },
  });

  // Strikethrough
  const strikeE = spring({
    frame: Math.max(0, localFrame - 45),
    fps,
    config: { damping: 12, mass: 0.8, stiffness: 100 },
  });

  // After value
  const afterDelay = 55;
  const afterE = spring({
    frame: Math.max(0, localFrame - afterDelay),
    fps,
    config: { damping: 10, mass: 0.3, stiffness: 200 },
  });

  // Background orb colors per slide
  const orbColors = [
    "rgba(100,140,255,0.08)",
    "rgba(16,185,129,0.08)",
    "rgba(139,92,246,0.08)",
  ];

  const illustrations = [LPIllustration, ResearchIllustration, DocumentIllustration];
  const Illustration = illustrations[index] || illustrations[0];

  return (
    <AbsoluteFill style={{ opacity: fadeIn * fadeOut }}>
      {/* Background orb */}
      <div style={{
        position: "absolute", width: 600, height: 600, borderRadius: "50%",
        background: `radial-gradient(circle, ${orbColors[index]} 0%, transparent 60%)`,
        filter: "blur(60px)", left: "30%", top: "25%", pointerEvents: "none",
      }} />

      {/* Content: left illustration + right comparison */}
      <div style={{
        position: "absolute", inset: 0,
        display: "flex", alignItems: "center", justifyContent: "center", gap: 80,
      }}>
        {/* Left: SVG Illustration */}
        <div style={{
          opacity: svgProgress,
          transform: `scale(${interpolate(svgProgress, [0, 1], [0.8, 1], { extrapolateRight: "clamp" })})`,
        }}>
          <Illustration progress={svgProgress} />
        </div>

        {/* Right: Label + Before → After */}
        <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          {/* Label */}
          <div style={{
            fontFamily: SHOWCASE_FONT.primary,
            fontSize: 48,
            fontWeight: 700,
            color: "#FFFFFF",
            letterSpacing: "-0.02em",
            opacity: labelE,
            transform: `translateX(${interpolate(labelE, [0, 1], [30, 0], { extrapolateRight: "clamp" })}px)`,
            textShadow: "0 0 30px rgba(255,255,255,0.15)",
          }}>
            {item.label}
          </div>

          {/* Before → After */}
          <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
            {/* Before */}
            <div style={{ position: "relative" }}>
              <span style={{
                fontFamily: SHOWCASE_FONT.primary,
                fontSize: 36,
                fontWeight: 400,
                color: `rgba(255,255,255,${interpolate(strikeE, [0, 1], [0.7, 0.25], { extrapolateRight: "clamp" })})`,
                opacity: beforeE,
                display: "inline-block",
                transform: `scale(${interpolate(beforeE, [0, 1], [0.8, 1], { extrapolateRight: "clamp" })})`,
              }}>
                {item.before}
              </span>
              {/* Red strikethrough */}
              <div style={{
                position: "absolute", top: "50%", left: 0,
                width: `${strikeE * 100}%`, height: 3,
                background: "linear-gradient(90deg, transparent 0%, #ef4444 10%, #ef4444 90%, transparent 100%)",
                boxShadow: "0 0 15px rgba(239,68,68,0.6), 0 0 30px rgba(239,68,68,0.3)",
                marginTop: -1.5,
              }} />
              {/* Swipe head */}
              {strikeE > 0.05 && strikeE < 0.95 && (
                <div style={{
                  position: "absolute", top: "50%", left: `${strikeE * 100}%`,
                  width: 8, height: 8, borderRadius: "50%", background: "#ef4444",
                  filter: "blur(3px)", marginTop: -4, marginLeft: -4,
                  boxShadow: "0 0 12px rgba(239,68,68,0.8)",
                }} />
              )}
            </div>

            {/* Arrow */}
            <svg width={32} height={32} viewBox="0 0 24 24" fill="none" style={{
              opacity: strikeE, flexShrink: 0,
              filter: `drop-shadow(0 0 6px rgba(16,185,129,${strikeE * 0.4}))`,
            }}>
              <path d="M5 12h14M12 5l7 7-7 7" stroke="rgba(16,185,129,0.7)" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
            </svg>

            {/* After */}
            <span style={{
              fontFamily: SHOWCASE_FONT.primary,
              fontSize: 48,
              fontWeight: 700,
              color: "#10B981",
              opacity: afterE,
              transform: `scale(${interpolate(afterE, [0, 1], [0.5, 1], { extrapolateRight: "clamp" })})`,
              display: "inline-block",
              textShadow: "0 0 20px rgba(16,185,129,0.6), 0 0 40px rgba(16,185,129,0.25), 0 0 60px rgba(16,185,129,0.1)",
            }}>
              {item.after}
            </span>
          </div>

          {/* AfterBurst */}
          {afterE > 0.1 && (
            <AfterBurst startFrame={slideStart + afterDelay} x={400} y={-20} />
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ─── Main Component ─────────────────────────────────────
export const TimeComparison: React.FC<TimeComparisonProps> = ({
  comparisons,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // 3 slides across durationInFrames (420f for 7s@60fps)
  // f0-15: global fade in
  // f15-145: slide 1 (130f)
  // f145-155: crossfade
  // f155-280: slide 2 (125f)
  // f280-290: crossfade
  // f290-400: slide 3 (110f)
  // f400-420: global fade out
  const slideTimings = [
    { start: 15, duration: 130 },
    { start: 155, duration: 125 },
    { start: 290, duration: 110 },
  ];

  // Global fade
  const globalIn = interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const globalOut = interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000", opacity: globalIn * globalOut }}>
      {comparisons.map((item, i) => {
        if (i >= slideTimings.length) return null;
        return (
          <ComparisonSlide
            key={i}
            item={item}
            index={i}
            slideStart={slideTimings[i].start}
            slideDuration={slideTimings[i].duration}
          />
        );
      })}
    </AbsoluteFill>
  );
};

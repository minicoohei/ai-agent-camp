import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { SHOWCASE_FONT } from "../../constants";

interface PromptBarProps {
  text: string;
  typingSpeed?: number;
  resultText?: string;
}

export const PromptBar: React.FC<PromptBarProps> = ({
  text,
  typingSpeed = 3,
  resultText,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Bar entrance
  const barEntrance = spring({
    frame,
    fps,
    config: { damping: 18, mass: 0.6, stiffness: 100 },
  });

  const barScale = interpolate(barEntrance, [0, 1], [0.85, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const barOpacity = interpolate(barEntrance, [0, 1], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  // Typing starts after bar is mostly visible
  const typingStart = 15;
  const typingFrame = Math.max(0, frame - typingStart);
  const charCount = Math.min(text.length, Math.floor(typingFrame / typingSpeed));
  const displayText = text.slice(0, charCount);
  const typingDone = charCount >= text.length;

  // Cursor blink
  const cursorVisible = !typingDone || Math.floor(frame / 15) % 2 === 0;

  // Arrow button appears after typing done
  const arrowEntrance = typingDone
    ? spring({
        frame: Math.max(0, frame - (typingStart + text.length * typingSpeed + 5)),
        fps,
        config: { damping: 14, mass: 0.5 },
      })
    : 0;

  // Glow intensity builds up as typing progresses
  const typingProgress = charCount / text.length;
  const glowOpacity = interpolate(typingProgress, [0, 0.5, 1], [0.1, 0.3, 0.6], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });

  // ─── Cinematic completion phases ──────────────────────
  const completionStart = typingStart + text.length * typingSpeed + 20;

  // Phase 1: Progress bar scan (f+0 to f+30)
  const progressPhase = frame >= completionStart && frame < completionStart + 35;
  const progressScan = progressPhase
    ? interpolate(frame, [completionStart, completionStart + 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : 0;

  // Phase 2: Bloom burst (f+30 to f+55)
  const bloomStart = completionStart + 28;
  const bloomPhase = frame >= bloomStart && frame < bloomStart + 30;
  const bloomProgress = bloomPhase
    ? interpolate(frame, [bloomStart, bloomStart + 25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : 0;
  const bloomScale = interpolate(bloomProgress, [0, 1], [0.3, 6], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const bloomOpacity = bloomProgress > 0
    ? interpolate(bloomProgress, [0, 0.2, 0.6, 1], [0, 1, 0.5, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : 0;

  // Phase 3: Result document SVG (f+50 onward)
  const resultStart = completionStart + 48;
  const resultPhase = frame >= resultStart;
  const docEntrance = resultPhase
    ? spring({
        frame: Math.max(0, frame - resultStart),
        fps,
        config: { damping: 10, stiffness: 200, mass: 0.4 },
      })
    : 0;

  // Checkmark bursts around document
  const checkDelays = [8, 16, 24, 32];
  const checkEntrances = checkDelays.map((d) =>
    resultPhase
      ? spring({
          frame: Math.max(0, frame - resultStart - d),
          fps,
          config: { damping: 12, mass: 0.3, stiffness: 180 },
        })
      : 0
  );

  // Bar fades out when bloom starts
  const barFadeOut = frame >= bloomStart
    ? interpolate(frame, [bloomStart, bloomStart + 10], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : 1;

  // Document float effect
  const docFloat = resultPhase ? Math.sin((frame - resultStart) * 0.04) * 4 : 0;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* Massive horizontal glow behind bar */}
      <div style={{
        position: "absolute", width: 1200, height: 200,
        background: "radial-gradient(ellipse 100% 80% at 50% 50%, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0.08) 40%, transparent 70%)",
        filter: "blur(50px)", opacity: glowOpacity * barOpacity * barFadeOut, pointerEvents: "none",
      }} />

      {/* ─── Prompt Bar ─────────────────────────────── */}
      <div style={{
        transform: `scale(${barScale})`,
        opacity: barOpacity * barFadeOut,
        display: "flex", alignItems: "center",
        width: 820, height: 72, borderRadius: 16,
        border: "1px solid rgba(255,255,255,0.15)",
        background: "rgba(255,255,255,0.08)",
        boxShadow: `0 0 60px 15px rgba(255,255,255,${0.08 * glowOpacity}), 0 0 120px 40px rgba(255,255,255,${0.03 * glowOpacity})`,
        padding: "0 24px", position: "relative",
      }}>
        <span style={{
          fontFamily: SHOWCASE_FONT.primary, fontSize: 22, fontWeight: 400,
          color: "#FFFFFF", letterSpacing: "-0.01em", flex: 1,
          textShadow: "0 0 15px rgba(255,255,255,0.15)",
        }}>
          {displayText}
          {cursorVisible && barFadeOut > 0.5 && (
            <span style={{
              display: "inline-block", width: 2, height: 24,
              backgroundColor: "rgba(255,255,255,0.7)", marginLeft: 1, verticalAlign: "middle",
            }} />
          )}
        </span>
        <div style={{
          width: 40, height: 40, borderRadius: "50%",
          border: "1px solid rgba(255,255,255,0.3)",
          display: "flex", alignItems: "center", justifyContent: "center",
          opacity: arrowEntrance, transform: `scale(${arrowEntrance})`, flexShrink: 0,
        }}>
          <svg width={18} height={18} viewBox="0 0 24 24" fill="none">
            <path d="M5 12h14M12 5l7 7-7 7" stroke="#FFFFFF" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>

        {/* Progress bar scan line */}
        {progressPhase && (
          <div style={{
            position: "absolute", bottom: 0, left: 0, right: 0, height: 3, borderRadius: "0 0 16px 16px",
            overflow: "hidden",
          }}>
            <div style={{
              width: `${progressScan * 100}%`, height: "100%",
              background: "linear-gradient(90deg, rgba(100,140,255,0.3), rgba(100,140,255,0.8))",
              boxShadow: "0 0 20px rgba(100,140,255,0.6), 0 0 40px rgba(100,140,255,0.3)",
            }} />
            {/* Scan head glow */}
            {progressScan > 0.02 && progressScan < 0.98 && (
              <div style={{
                position: "absolute", top: -4, left: `${progressScan * 100}%`,
                width: 10, height: 10, borderRadius: "50%",
                background: "rgba(100,140,255,0.9)", filter: "blur(4px)",
                marginLeft: -5,
              }} />
            )}
          </div>
        )}
      </div>

      {/* ─── Bloom Burst ─────────────────────────────── */}
      {bloomPhase && (
        <div style={{
          position: "absolute", top: "50%", left: "50%",
          width: 300, height: 300, marginLeft: -150, marginTop: -150,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.3) 40%, transparent 70%)",
          transform: `scale(${bloomScale})`, opacity: bloomOpacity,
          pointerEvents: "none",
          boxShadow: `0 0 120px 60px rgba(255,255,255,${bloomOpacity * 0.5})`,
        }} />
      )}

      {/* ─── Result: Document SVG + Text ─────────────── */}
      {resultPhase && (
        <div style={{
          position: "absolute",
          display: "flex", flexDirection: "column", alignItems: "center", gap: 20,
          opacity: docEntrance,
          transform: `scale(${interpolate(docEntrance, [0, 1], [0.5, 1], { extrapolateRight: "clamp" })}) translateY(${docFloat}px)`,
        }}>
          {/* PPTX Document Icon */}
          <svg width={160} height={190} viewBox="0 0 100 120" fill="none">
            {/* Document body */}
            <rect x={10} y={5} width={80} height={100} rx={8} fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.2)" strokeWidth={1.5} />
            {/* Folded corner */}
            <path d="M70 5 L90 25 L70 25 Z" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.2)" strokeWidth={1} />
            {/* Content lines */}
            <rect x={22} y={35} width={40} height={6} rx={3} fill="rgba(100,140,255,0.3)" />
            <rect x={22} y={48} width={56} height={4} rx={2} fill="rgba(255,255,255,0.1)" />
            <rect x={22} y={58} width={48} height={4} rx={2} fill="rgba(255,255,255,0.08)" />
            <rect x={22} y={68} width={52} height={4} rx={2} fill="rgba(255,255,255,0.1)" />
            {/* Chart icon */}
            <rect x={28} y={80} width={8} height={16} rx={2} fill="rgba(16,185,129,0.3)" />
            <rect x={40} y={74} width={8} height={22} rx={2} fill="rgba(100,140,255,0.3)" />
            <rect x={52} y={78} width={8} height={18} rx={2} fill="rgba(139,92,246,0.3)" />
            {/* PPTX badge */}
            <rect x={55} y={85} width={30} height={16} rx={4} fill="rgba(239,68,68,0.2)" />
            <text x={60} y={97} fontFamily={SHOWCASE_FONT.mono} fontSize={8} fontWeight={600} fill="rgba(239,68,68,0.8)">.pptx</text>
          </svg>

          {/* Result text */}
          {resultText && (
            <div style={{
              fontFamily: SHOWCASE_FONT.primary, fontSize: 32, fontWeight: 600,
              color: "#10B981", letterSpacing: "0.01em",
              textShadow: "0 0 25px rgba(16,185,129,0.5), 0 0 50px rgba(16,185,129,0.2), 0 0 80px rgba(16,185,129,0.1)",
            }}>
              {resultText}
            </div>
          )}

          {/* Checkmark bursts around document */}
          {[
            { x: -80, y: -30 },
            { x: 90, y: -20 },
            { x: -70, y: 60 },
            { x: 80, y: 70 },
          ].map((pos, i) => (
            <div key={i} style={{
              position: "absolute", left: `calc(50% + ${pos.x}px)`, top: `calc(40% + ${pos.y}px)`,
              opacity: checkEntrances[i],
              transform: `scale(${interpolate(checkEntrances[i], [0, 1], [0.3, 1], { extrapolateRight: "clamp" })})`,
            }}>
              <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
                <circle cx={12} cy={12} r={10} fill="rgba(16,185,129,0.15)" />
                <path d="M8 12l3 3 5-5" stroke="#10B981" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
          ))}
        </div>
      )}
    </AbsoluteFill>
  );
};

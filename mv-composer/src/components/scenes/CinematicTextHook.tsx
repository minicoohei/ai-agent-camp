import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { SHOWCASE_FONT } from "../../constants";

interface TextLine {
  text: string;
  delayMs?: number;
}

interface CinematicTextHookProps {
  lines: TextLine[];
}

const WORD_INTERVAL = 6; // frames between each word reveal (space-separated)
const CHAR_INTERVAL = 3; // frames between each character reveal (Japanese mode)
const CHAR_INTERVAL_SLOW = 5; // slower reveal for emphasis (final line)

/** Detect whether text contains spaces — if not, treat as Japanese and split by character */
const splitText = (text: string): string[] => {
  if (text.includes(" ")) {
    return text.split(" ");
  }
  // Japanese mode: split into individual characters
  return [...text];
};

/** Return the inter-token interval based on the split mode */
const getInterval = (text: string, isLastLine?: boolean): number => {
  if (text.includes(" ")) return WORD_INTERVAL;
  return isLastLine ? CHAR_INTERVAL_SLOW : CHAR_INTERVAL;
};

const WordReveal: React.FC<{
  word: string;
  startFrame: number;
  isLast?: boolean;
  isCharMode?: boolean;
}> = ({ word, startFrame, isCharMode }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: Math.max(0, frame - startFrame),
    fps,
    config: { damping: 22, mass: 0.5, stiffness: 120 },
  });

  const opacity = interpolate(progress, [0, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const translateX = interpolate(progress, [0, 1], [20, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <span
      style={{
        display: "inline-block",
        opacity,
        transform: `translateX(${translateX}px)`,
        marginRight: isCharMode ? 0 : 18,
      }}
    >
      {word}
    </span>
  );
};

export const CinematicTextHook: React.FC<CinematicTextHookProps> = ({
  lines,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Calculate frame offsets for each line
  let lineOffsets: number[] = [];
  let offset = 0;
  for (let li = 0; li < lines.length; li++) {
    const line = lines[li];
    const isLast = li === lines.length - 1;
    lineOffsets.push(offset);
    const tokens = splitText(line.text);
    const interval = getInterval(line.text, isLast);
    const lineDuration = tokens.length * interval + Math.round((line.delayMs ?? 800) / (1000 / fps));
    offset += lineDuration;
  }

  // Ambient floating orbs (I2V-style depth)
  const orbDrift1 = { x: Math.sin(frame * 0.012) * 60, y: Math.cos(frame * 0.009) * 40 };
  const orbDrift2 = { x: Math.cos(frame * 0.015) * 50, y: Math.sin(frame * 0.011) * 35 };
  const orbOpacity = interpolate(frame, [0, 30, offset - 20, offset], [0, 0.6, 0.6, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* I2V ambient glow orbs */}
      <div style={{
        position: "absolute",
        width: 500, height: 500, borderRadius: "50%",
        background: "radial-gradient(circle, rgba(120,130,255,0.12) 0%, transparent 70%)",
        filter: "blur(80px)",
        left: `calc(30% + ${orbDrift1.x}px)`, top: `calc(40% + ${orbDrift1.y}px)`,
        opacity: orbOpacity, pointerEvents: "none",
      }} />
      <div style={{
        position: "absolute",
        width: 400, height: 400, borderRadius: "50%",
        background: "radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%)",
        filter: "blur(60px)",
        left: `calc(60% + ${orbDrift2.x}px)`, top: `calc(50% + ${orbDrift2.y}px)`,
        opacity: orbOpacity, pointerEvents: "none",
      }} />

      {lines.map((line, lineIndex) => {
        const lineStart = lineOffsets[lineIndex];
        const isLastLine = lineIndex === lines.length - 1;
        const nextLineStart = lineIndex < lines.length - 1 ? lineOffsets[lineIndex + 1] : Infinity;
        const tokens = splitText(line.text);
        const interval = getInterval(line.text, isLastLine);
        const isCharMode = !line.text.includes(" ");
        const lineEndReveal = lineStart + tokens.length * interval;

        // Line fade out when next line starts
        const lineOpacity = nextLineStart < Infinity
          ? interpolate(
              frame,
              [nextLineStart - 15, nextLineStart],
              [1, 0],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
            )
          : 1;

        // Line entrance opacity
        const lineEntranceOpacity = interpolate(
          frame,
          [lineStart, lineStart + 5],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        // Don't show line before its start or well after fade out
        if (frame < lineStart - 5 || (nextLineStart < Infinity && frame > nextLineStart + 10)) {
          return null;
        }

        const translateY = nextLineStart < Infinity
          ? interpolate(
              frame,
              [nextLineStart - 15, nextLineStart],
              [0, -15],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
            )
          : 0;

        return (
          <div
            key={lineIndex}
            style={{
              position: "absolute",
              display: "flex",
              flexWrap: "wrap",
              justifyContent: "center",
              alignItems: "center",
              opacity: lineOpacity * lineEntranceOpacity,
              transform: `translateY(${translateY}px)`,
              fontSize: 54,
              fontWeight: 600,
              fontFamily: SHOWCASE_FONT.primary,
              color: "#FFFFFF",
              letterSpacing: "-0.02em",
              maxWidth: "80%",
              textShadow: "0 0 40px rgba(255,255,255,0.25), 0 0 80px rgba(150,160,255,0.1), 0 2px 4px rgba(0,0,0,0.5)",
            }}
          >
            {tokens.map((token, tokenIndex) => (
              <WordReveal
                key={tokenIndex}
                word={token}
                startFrame={lineStart + tokenIndex * interval}
                isCharMode={isCharMode}
              />
            ))}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

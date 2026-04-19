import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { SHOWCASE_FONT } from "../../constants";

interface ShowcaseClosingProps {
  closingText: string;
  brandName: string;
  brandLogoSrc?: string;
  closingUrl: string;
  closingSubText?: string;
  urlSubText?: string;
}

const F = `${SHOWCASE_FONT.primary}, 'Hiragino Sans', 'Noto Sans JP', sans-serif`;

// AI Agent Camp Logo SVG (light version for dark bg)
const CampLogoLarge: React.FC<{ entrance: number }> = ({ entrance }) => (
  <div style={{
    display: "flex", alignItems: "center", gap: 16,
    opacity: entrance,
    transform: `scale(${interpolate(entrance, [0, 1], [0.8, 1], { extrapolateRight: "clamp" })})`,
  }}>
    <svg width={56} height={56} viewBox="0 0 40 40" fill="none">
      {/* Tent */}
      <path d="M20 4L6 32h28L20 4z" fill="url(#closingTentGrad)" opacity={0.9} />
      <path d="M20 4L14 32h12L20 4z" fill="rgba(255,255,255,0.15)" />
      {/* "Ai" text */}
      <text x={16} y={24} fontFamily={F} fontSize={10} fontWeight={800} fill="#fff">Ai</text>
      {/* Blue sphere */}
      <circle cx={32} cy={10} r={5} fill="#2b6cb0" />
      <circle cx={30.5} cy={8.5} r={1.5} fill="rgba(255,255,255,0.4)" />
      <defs>
        <linearGradient id="closingTentGrad" x1="6" y1="32" x2="34" y2="4">
          <stop offset="0%" stopColor="#1a365d" />
          <stop offset="100%" stopColor="#2b6cb0" />
        </linearGradient>
      </defs>
    </svg>
    <div style={{ display: "flex", flexDirection: "column" }}>
      <span style={{
        fontFamily: F, fontSize: 24, fontWeight: 800,
        color: "rgba(255,255,255,0.9)", lineHeight: 1.1, letterSpacing: "-0.02em",
      }}>
        AI AGENT
      </span>
      <span style={{
        fontFamily: F, fontSize: 18, fontWeight: 600,
        color: "rgba(255,255,255,0.6)", lineHeight: 1.1, letterSpacing: "0.08em",
      }}>
        CAMP
      </span>
    </div>
  </div>
);

export const ShowcaseClosing: React.FC<ShowcaseClosingProps> = ({
  closingText,
  closingUrl,
  closingSubText,
  urlSubText,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const midpoint = Math.floor(durationInFrames * 0.55);

  // Phase 1: Light background with closing text
  const textEntrance = spring({
    frame,
    fps,
    config: { damping: 20, mass: 0.6, stiffness: 100 },
  });

  // Phase 2: Dark flip
  const flipProgress = interpolate(
    frame,
    [midpoint, midpoint + 15],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const bgColor = interpolate(flipProgress, [0, 1], [245, 0]);

  // URL entrance
  const urlEntrance = spring({
    frame: Math.max(0, frame - midpoint - 10),
    fps,
    config: { damping: 16, mass: 0.5 },
  });

  // Logo entrance (after URL)
  const logoEntrance = spring({
    frame: Math.max(0, frame - midpoint - 30),
    fps,
    config: { damping: 14, mass: 0.5 },
  });

  // I2V ambient drift
  const driftX = Math.sin(frame * 0.015) * 40;
  const driftY = Math.cos(frame * 0.012) * 25;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: `rgb(${bgColor},${bgColor},${bgColor})`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* I2V ambient orb (Phase 2 only) */}
      {frame >= midpoint && (
        <div style={{
          position: "absolute",
          width: 700, height: 700, borderRadius: "50%",
          background: "radial-gradient(circle, rgba(100,120,255,0.06) 0%, transparent 60%)",
          filter: "blur(80px)",
          left: `calc(50% + ${driftX}px)`, top: `calc(50% + ${driftY}px)`,
          transform: "translate(-50%, -50%)",
          pointerEvents: "none",
        }} />
      )}

      {/* Phase 1: Light background + dark text → fade out */}
      {frame < midpoint + 15 && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 12,
            opacity: frame < midpoint
              ? textEntrance
              : interpolate(frame, [midpoint, midpoint + 12], [1, 0], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                }),
          }}
        >
          <div style={{
            display: "flex",
            alignItems: "center",
            gap: 16,
            fontSize: 52,
            fontWeight: 700,
            fontFamily: SHOWCASE_FONT.primary,
            color: "transparent",
            letterSpacing: "-0.03em",
            backgroundImage: "linear-gradient(135deg, rgb(20,20,20) 0%, rgb(60,60,80) 50%, rgb(20,20,20) 100%)",
            backgroundClip: "text",
            WebkitBackgroundClip: "text",
            textShadow: "0 2px 30px rgba(0,0,0,0.1)",
          }}>
            {closingText}
          </div>
          {closingSubText && (
            <div style={{
              fontSize: 24,
              fontWeight: 400,
              fontFamily: SHOWCASE_FONT.primary,
              color: "rgb(80,80,80)",
            }}>
              {closingSubText}
            </div>
          )}
        </div>
      )}

      {/* Phase 2: Dark background + Logo + URL text → fade in */}
      {frame >= midpoint && (
        <div
          style={{
            position: "absolute",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 24,
          }}
        >
          {/* AI Agent Camp Logo */}
          <CampLogoLarge entrance={logoEntrance} />

          {/* URL */}
          <div style={{
            opacity: urlEntrance,
            transform: `scale(${interpolate(urlEntrance, [0, 1], [0.9, 1])})`,
            display: "flex", flexDirection: "column", alignItems: "center", gap: 10,
          }}>
            <span
              style={{
                fontSize: 38,
                fontWeight: 500,
                fontFamily: SHOWCASE_FONT.mono,
                color: "#FFFFFF",
                letterSpacing: "0.04em",
                textShadow: "0 0 30px rgba(255,255,255,0.3), 0 0 60px rgba(150,160,255,0.15)",
              }}
            >
              {closingUrl}
            </span>
            {urlSubText && (
              <span style={{
                fontSize: 20,
                fontWeight: 400,
                fontFamily: SHOWCASE_FONT.primary,
                color: "rgba(255,255,255,0.5)",
              }}>
                {urlSubText}
              </span>
            )}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

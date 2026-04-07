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
interface Testimonial {
  name: string;
  title: string;
  company: string;
  comment?: string;
}

interface VoiceRushProps {
  testimonials: Testimonial[];
}

// ─── Avatar colors ──────────────────────────────────────
const AVATAR_GRADIENTS = [
  "linear-gradient(135deg, #667eea, #764ba2)",
  "linear-gradient(135deg, #f093fb, #f5576c)",
  "linear-gradient(135deg, #4facfe, #00f2fe)",
  "linear-gradient(135deg, #43e97b, #38f9d7)",
];

// ─── Stacking Testimonial Card ──────────────────────────
const StackCard: React.FC<{
  testimonial: Testimonial;
  index: number;
  totalCards: number;
}> = ({ testimonial, index, totalCards }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Slower stagger for readability: 50f between cards
  const cardStart = 15 + index * 50;

  // Fast spring entrance from bottom
  const entrance = spring({
    frame: Math.max(0, frame - cardStart),
    fps,
    config: { damping: 12, stiffness: 150, mass: 0.5 },
  });

  // Don't render before entrance
  if (frame < cardStart - 2) return null;

  // Stack offsets: each card slightly offset for pile effect
  const stackOffsetY = index * -25;
  const stackOffsetX = index * 10;
  const stackRotateZ = (index - (totalCards - 1) / 2) * 1.5;
  const stackScale = 1 - (totalCards - 1 - index) * 0.02;

  // Entrance from bottom
  const translateY = interpolate(entrance, [0, 1], [300, stackOffsetY], {
    extrapolateRight: "clamp",
  });
  const translateX = interpolate(entrance, [0, 1], [0, stackOffsetX], {
    extrapolateRight: "clamp",
  });
  const rotateZ = interpolate(entrance, [0, 1], [8, stackRotateZ], {
    extrapolateRight: "clamp",
  });
  const scale = interpolate(entrance, [0, 1], [0.7, stackScale], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(entrance, [0, 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Rear cards dim slightly
  const isTopCard = index === totalCards - 1;
  const dimFactor = isTopCard ? 1 : interpolate(index, [0, totalCards - 1], [0.6, 1], {
    extrapolateRight: "clamp",
  });

  // Subtle glow pulse on top card
  const glowPulse = isTopCard
    ? Math.sin(frame * 0.06) * 0.3 + 0.7
    : 0.4;

  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        top: "50%",
        width: 800,
        transform: `translate(-50%, -50%) translateY(${translateY}px) translateX(${translateX}px) rotate(${rotateZ}deg) scale(${scale})`,
        opacity: opacity * dimFactor,
        zIndex: index,
      }}
    >
      {/* Card glow */}
      {isTopCard && (
        <div
          style={{
            position: "absolute",
            inset: -25,
            borderRadius: 36,
            background: `radial-gradient(ellipse at 50% 50%, rgba(120,130,255,${0.06 * glowPulse}) 0%, transparent 70%)`,
            filter: "blur(25px)",
            pointerEvents: "none",
          }}
        />
      )}

      {/* Card body */}
      <div
        style={{
          borderRadius: 22,
          background:
            "linear-gradient(145deg, rgba(25,25,45,0.95), rgba(15,15,30,0.9))",
          border: "1px solid rgba(255,255,255,0.1)",
          boxShadow: `
            0 16px 50px rgba(0,0,0,0.5),
            0 0 ${60 * glowPulse}px rgba(100,120,255,${0.03 * glowPulse}),
            inset 0 1px 0 rgba(255,255,255,0.08)
          `,
          backdropFilter: "blur(20px)",
          padding: "28px 34px",
        }}
      >
        {/* Quote + Comment */}
        <div style={{ marginBottom: 18 }}>
          <span
            style={{
              fontSize: 52,
              fontWeight: 700,
              color: "rgba(120,130,255,0.2)",
              lineHeight: 0.6,
              fontFamily: "Georgia, serif",
              display: "block",
              marginBottom: 10,
            }}
          >
            &ldquo;
          </span>
          <div
            style={{
              fontFamily: SHOWCASE_FONT.primary,
              fontSize: 24,
              fontWeight: 400,
              color: "rgba(255,255,255,0.9)",
              lineHeight: 1.7,
              letterSpacing: "0.01em",
              textShadow: "0 0 20px rgba(255,255,255,0.08)",
            }}
          >
            {testimonial.comment || ""}
          </div>
        </div>

        {/* Divider */}
        <div
          style={{
            height: 1,
            background:
              "linear-gradient(90deg, transparent, rgba(255,255,255,0.1) 20%, rgba(255,255,255,0.1) 80%, transparent)",
            marginBottom: 16,
          }}
        />

        {/* Name + Title + Company */}
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: "50%",
              background: AVATAR_GRADIENTS[index % AVATAR_GRADIENTS.length],
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
              boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
            }}
          >
            <span
              style={{
                fontSize: 18,
                fontWeight: 700,
                color: "#FFF",
                fontFamily: SHOWCASE_FONT.primary,
              }}
            >
              {testimonial.name.charAt(0)}
            </span>
          </div>
          <div>
            <div
              style={{
                fontSize: 20,
                fontWeight: 600,
                color: "#FFFFFF",
                fontFamily: SHOWCASE_FONT.primary,
                letterSpacing: "0.01em",
              }}
            >
              {testimonial.name}
            </div>
            <div
              style={{
                fontSize: 15,
                fontWeight: 400,
                color: "rgba(255,255,255,0.45)",
                fontFamily: SHOWCASE_FONT.primary,
                marginTop: 1,
              }}
            >
              {testimonial.title} / {testimonial.company}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ─── Main Component ─────────────────────────────────────
export const VoiceRush: React.FC<VoiceRushProps> = ({
  testimonials,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Global fade in/out
  const globalIn = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const globalOut = interpolate(
    frame,
    [durationInFrames - 20, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
        opacity: globalIn * globalOut,
      }}
    >
      {/* I2V ambient glow orbs */}
      <div
        style={{
          position: "absolute",
          width: 800,
          height: 800,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(100,110,255,0.05) 0%, transparent 60%)",
          filter: "blur(80px)",
          left: "30%",
          top: "30%",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 600,
          height: 600,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(200,100,255,0.04) 0%, transparent 60%)",
          filter: "blur(70px)",
          left: "60%",
          top: "55%",
          pointerEvents: "none",
        }}
      />

      {/* Testimonials: fast stack */}
      {testimonials.map((t, i) => (
        <StackCard
          key={`testimonial-${i}`}
          testimonial={t}
          index={i}
          totalCards={testimonials.length}
        />
      ))}
    </AbsoluteFill>
  );
};

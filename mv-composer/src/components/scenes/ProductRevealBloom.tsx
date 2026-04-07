import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { SHOWCASE_FONT } from "../../constants";

interface ProductRevealBloomProps {
  brandName: string;
  taskTitle: string;
  taskCompleted: number;
  taskTotal: number;
  brandDescription: string;
  promptText?: string;
}

// Bloom light burst effect
const BloomBurst: React.FC<{ startFrame: number }> = ({ startFrame }) => {
  const frame = useCurrentFrame();
  const elapsed = frame - startFrame;

  if (elapsed < 0 || elapsed > 70) return null;

  const progress = elapsed / 65;
  const scale = interpolate(progress, [0, 1], [0.3, 5], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(progress, [0, 0.15, 0.6, 1], [0, 0.9, 0.4, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: "50%",
        left: "50%",
        width: 400,
        height: 400,
        marginLeft: -200,
        marginTop: -200,
        borderRadius: "50%",
        background: `radial-gradient(circle, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.3) 40%, transparent 70%)`,
        transform: `scale(${scale})`,
        opacity,
        pointerEvents: "none",
        boxShadow: `0 0 120px 60px rgba(255,255,255,${opacity * 0.5})`,
      }}
    />
  );
};

export const ProductRevealBloom: React.FC<ProductRevealBloomProps> = ({
  brandName,
  taskTitle,
  taskCompleted,
  taskTotal,
  brandDescription,
  promptText,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bloomStart = 10;

  // Background glow transition
  const bgGlow = interpolate(frame, [bloomStart, bloomStart + 40], [0, 0.15], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Prompt bar (carried over from previous scene)
  const promptOpacity = interpolate(frame, [0, 10], [0.8, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const promptScale = interpolate(
    frame,
    [bloomStart, bloomStart + 20],
    [1, 0.92],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const promptY = interpolate(
    frame,
    [bloomStart, bloomStart + 30],
    [0, -60],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Brand card entrance
  const cardEntrance = spring({
    frame: Math.max(0, frame - bloomStart - 25),
    fps,
    config: { damping: 16, mass: 0.5, stiffness: 100 },
  });

  // Task completion entrance
  const taskEntrance = spring({
    frame: Math.max(0, frame - bloomStart - 40),
    fps,
    config: { damping: 18, mass: 0.6 },
  });

  // Description text entrance
  const descEntrance = spring({
    frame: Math.max(0, frame - bloomStart - 55),
    fps,
    config: { damping: 20, mass: 0.7 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
      }}
    >
      {/* Background glow */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `radial-gradient(ellipse 80% 60% at 50% 40%, rgba(255,255,255,${bgGlow}) 0%, transparent 100%)`,
        }}
      />

      <BloomBurst startFrame={bloomStart} />

      {/* Content container */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 20,
        }}
      >
        {/* Prompt bar (top) */}
        {promptText && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              width: 820,
              height: 68,
              borderRadius: 16,
              border: "1px solid rgba(255,255,255,0.15)",
              background: "rgba(255,255,255,0.05)",
              padding: "0 24px",
              opacity: promptOpacity,
              transform: `scale(${promptScale}) translateY(${promptY}px)`,
            }}
          >
            <span
              style={{
                fontFamily: SHOWCASE_FONT.primary,
                fontSize: 21,
                color: "rgba(255,255,255,0.8)",
                flex: 1,
              }}
            >
              {promptText}
            </span>
            <div
              style={{
                width: 38,
                height: 38,
                borderRadius: "50%",
                border: "1px solid rgba(255,255,255,0.25)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <svg width={16} height={16} viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M12 5l7 7-7 7" stroke="#FFF" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
          </div>
        )}

        {/* Brand name */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            opacity: cardEntrance,
            transform: `translateY(${interpolate(cardEntrance, [0, 1], [20, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}px)`,
            marginTop: 16,
          }}
        >
          {/* Cloud icon placeholder */}
          <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
            <path
              d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"
              stroke="rgba(255,255,255,0.6)"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span
            style={{
              fontFamily: SHOWCASE_FONT.primary,
              fontSize: 24,
              fontWeight: 500,
              color: "rgba(255,255,255,0.7)",
            }}
          >
            {brandName}
          </span>
        </div>

        {/* Task completion card */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 14,
            padding: "14px 24px",
            borderRadius: 12,
            background: "rgba(255,255,255,0.06)",
            border: "1px solid rgba(255,255,255,0.1)",
            opacity: taskEntrance,
            transform: `scale(${interpolate(taskEntrance, [0, 1], [0.9, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})`,
          }}
        >
          {/* Check circle */}
          <div
            style={{
              width: 28,
              height: 28,
              borderRadius: "50%",
              backgroundColor: "#10B981",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <svg width={14} height={14} viewBox="0 0 24 24" fill="none">
              <path d="M20 6L9 17l-5-5" stroke="#FFF" strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <div>
            <div
              style={{
                fontFamily: SHOWCASE_FONT.primary,
                fontSize: 17,
                fontWeight: 600,
                color: "#FFFFFF",
              }}
            >
              {taskTitle}
            </div>
            <div
              style={{
                fontFamily: SHOWCASE_FONT.primary,
                fontSize: 13,
                color: "#10B981",
              }}
            >
              {taskCompleted}/{taskTotal} 完了
            </div>
          </div>
        </div>

        {/* Brand description */}
        <div
          style={{
            maxWidth: 700,
            textAlign: "left",
            opacity: descEntrance,
            transform: `translateY(${interpolate(descEntrance, [0, 1], [15, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}px)`,
            marginTop: 8,
          }}
        >
          <div
            style={{
              fontFamily: SHOWCASE_FONT.primary,
              fontSize: 22,
              fontWeight: 700,
              color: "#FFFFFF",
              marginBottom: 10,
            }}
          >
            About {brandName}
          </div>
          <div
            style={{
              fontFamily: SHOWCASE_FONT.primary,
              fontSize: 17,
              fontWeight: 400,
              color: "rgba(255,255,255,0.7)",
              lineHeight: 1.6,
            }}
          >
            {brandDescription}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

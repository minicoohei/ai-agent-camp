import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { SHOWCASE_FONT } from "../../constants";

interface MeshGradientTransitionProps {
  text?: string;
}

export const MeshGradientTransition: React.FC<MeshGradientTransitionProps> = ({
  text = "Now.",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Mesh gradient blob positions (organic movement)
  const blob = (speed: number, offset: number) => ({
    x: 50 + Math.sin(frame * speed + offset) * 30,
    y: 50 + Math.cos(frame * speed * 0.7 + offset + 1) * 25,
  });

  const b1 = blob(0.025, 0);
  const b2 = blob(0.018, 2.1);
  const b3 = blob(0.022, 4.2);
  const b4 = blob(0.015, 1.4);
  const b5 = blob(0.02, 3.5);

  // Panel entrance
  const panelEntrance = spring({
    frame,
    fps,
    config: { damping: 20, mass: 0.8, stiffness: 80 },
  });
  const panelScale = interpolate(panelEntrance, [0, 1], [0.85, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const panelOpacity = interpolate(panelEntrance, [0, 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Text entrance (delayed)
  const textEntrance = spring({
    frame: Math.max(0, frame - 20),
    fps,
    config: { damping: 18, mass: 0.5, stiffness: 100 },
  });
  const textOpacity = interpolate(textEntrance, [0, 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const textX = interpolate(textEntrance, [0, 1], [40, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Exit fade
  const exitOpacity = interpolate(
    frame,
    [durationInFrames - 20, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Background transition: black → white → black
  const bgProgress = interpolate(frame, [0, 30, durationInFrames - 15, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const bgLum = Math.round(bgProgress * 230);

  const meshGradient = [
    `radial-gradient(ellipse 60% 50% at ${b1.x}% ${b1.y}%, rgba(200,200,215,0.9) 0%, transparent 55%)`,
    `radial-gradient(ellipse 50% 60% at ${b2.x}% ${b2.y}%, rgba(170,175,195,0.7) 0%, transparent 50%)`,
    `radial-gradient(ellipse 70% 40% at ${b3.x}% ${b3.y}%, rgba(220,220,235,0.8) 0%, transparent 45%)`,
    `radial-gradient(ellipse 40% 55% at ${b4.x}% ${b4.y}%, rgba(190,185,200,0.6) 0%, transparent 60%)`,
    `radial-gradient(ellipse 55% 45% at ${b5.x}% ${b5.y}%, rgba(210,215,225,0.7) 0%, transparent 50%)`,
    `linear-gradient(135deg, #d8d8e0 0%, #b8b8c5 30%, #a0a0b0 60%, #c0c0cc 100%)`,
  ].join(", ");

  return (
    <AbsoluteFill
      style={{
        backgroundColor: `rgb(${bgLum},${bgLum},${bgLum})`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        opacity: exitOpacity,
      }}
    >
      {/* Outer blur glow */}
      <div
        style={{
          position: "absolute",
          width: 1500,
          height: 900,
          borderRadius: 60,
          background: "radial-gradient(ellipse at 50% 50%, rgba(180,180,200,0.3) 0%, transparent 70%)",
          filter: "blur(80px)",
          opacity: panelOpacity * 0.6,
        }}
      />

      {/* Main gradient panel */}
      <div
        style={{
          width: 1300,
          height: 700,
          borderRadius: 32,
          overflow: "hidden",
          transform: `scale(${panelScale})`,
          opacity: panelOpacity,
          boxShadow: "0 40px 120px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.2)",
          position: "relative",
        }}
      >
        {/* Animated mesh gradient */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: meshGradient,
          }}
        />

        {/* Subtle noise texture overlay */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            opacity: 0.03,
            backgroundImage:
              "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='256' height='256' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E\")",
            backgroundSize: "128px 128px",
          }}
        />

        {/* Text */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "flex-end",
            paddingRight: 120,
          }}
        >
          <span
            style={{
              fontFamily: SHOWCASE_FONT.primary,
              fontSize: 64,
              fontWeight: 600,
              color: "rgba(255,255,255,0.95)",
              letterSpacing: "-0.03em",
              opacity: textOpacity,
              transform: `translateX(${textX}px)`,
              textShadow: "0 2px 20px rgba(0,0,0,0.15), 0 0 40px rgba(255,255,255,0.2)",
            }}
          >
            {text}
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

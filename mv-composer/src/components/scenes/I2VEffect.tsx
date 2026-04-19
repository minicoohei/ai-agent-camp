import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// ─── Types ──────────────────────────────────────────────
export interface I2VEffectProps {
  imageSrc: string; // staticFile() path
  duration: number; // frames
  effect: "parallax" | "zoom_drift" | "reveal" | "float_3d";
  direction?: "in" | "out" | "left" | "right";
  intensity?: number; // 0.5 - 2.0
}

// ─── Common styles ──────────────────────────────────────
const COMMON_CONTAINER: React.CSSProperties = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  overflow: "hidden",
};

const GLOW_SHADOW = "0 0 60px rgba(255,255,255,0.08), 0 0 120px rgba(100,140,255,0.05)";

// ─── Effect Implementations ─────────────────────────────
const ParallaxEffect: React.FC<{ src: string; intensity: number }> = ({ src, intensity }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;

  const translateX = interpolate(progress, [0, 1], [10 * intensity, -10 * intensity]);
  const translateY = interpolate(progress, [0, 1], [5 * intensity, -5 * intensity]);
  const opacity = interpolate(frame, [0, 15, durationInFrames - 10, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ ...COMMON_CONTAINER, opacity }}>
      <Img
        src={src}
        style={{
          width: "115%",
          height: "115%",
          objectFit: "cover",
          transform: `translate(${translateX}px, ${translateY}px)`,
          filter: "brightness(1.02)",
          boxShadow: GLOW_SHADOW,
        }}
      />
    </AbsoluteFill>
  );
};

const ZoomDriftEffect: React.FC<{ src: string; intensity: number }> = ({ src, intensity }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;

  const scale = interpolate(progress, [0, 1], [1.0, 1.0 + 0.06 * intensity]);
  const translateX = interpolate(progress, [0, 1], [0, -15 * intensity]);
  const opacity = interpolate(frame, [0, 15, durationInFrames - 10, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ ...COMMON_CONTAINER, opacity }}>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translateX(${translateX}px)`,
          filter: "brightness(1.02)",
          boxShadow: GLOW_SHADOW,
        }}
      />
    </AbsoluteFill>
  );
};

const RevealEffect: React.FC<{ src: string; intensity: number; direction: string }> = ({
  src,
  intensity,
  direction,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const isLeft = direction === "left";
  const slideProgress = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const translateX = interpolate(slideProgress, [0, 1], [isLeft ? -100 * intensity : 100 * intensity, 0]);
  const opacity = interpolate(frame, [0, 20, durationInFrames - 10, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const gradientDir = isLeft ? "to right" : "to left";

  return (
    <AbsoluteFill style={{ ...COMMON_CONTAINER, opacity }}>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `translateX(${translateX}px)`,
          filter: "brightness(1.02)",
          boxShadow: GLOW_SHADOW,
          WebkitMaskImage: `linear-gradient(${gradientDir}, black 80%, transparent 100%)`,
          maskImage: `linear-gradient(${gradientDir}, black 80%, transparent 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};

const Float3DEffect: React.FC<{ src: string; intensity: number }> = ({ src, intensity }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const rotateX = Math.sin(frame * 0.04) * 3 * intensity;
  const rotateY = Math.cos(frame * 0.03) * 4 * intensity;
  const floatY = Math.sin(frame * 0.05) * 8 * intensity;
  const opacity = interpolate(frame, [0, 15, durationInFrames - 10, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        ...COMMON_CONTAINER,
        opacity,
        perspective: 1200,
      }}
    >
      <Img
        src={src}
        style={{
          width: "85%",
          height: "85%",
          objectFit: "contain",
          transform: `perspective(1200px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(${floatY}px)`,
          filter: "brightness(1.02)",
          boxShadow: GLOW_SHADOW,
          borderRadius: 12,
        }}
      />
    </AbsoluteFill>
  );
};

// ─── Main Component ─────────────────────────────────────
export const I2VEffect: React.FC<I2VEffectProps> = ({
  imageSrc,
  duration,
  effect,
  direction = "left",
  intensity = 1.0,
}) => {
  const clampedIntensity = Math.max(0.5, Math.min(2.0, intensity));

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {effect === "parallax" && <ParallaxEffect src={imageSrc} intensity={clampedIntensity} />}
      {effect === "zoom_drift" && <ZoomDriftEffect src={imageSrc} intensity={clampedIntensity} />}
      {effect === "reveal" && (
        <RevealEffect src={imageSrc} intensity={clampedIntensity} direction={direction} />
      )}
      {effect === "float_3d" && <Float3DEffect src={imageSrc} intensity={clampedIntensity} />}
    </AbsoluteFill>
  );
};

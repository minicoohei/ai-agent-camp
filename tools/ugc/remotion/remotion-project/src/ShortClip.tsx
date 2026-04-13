import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  staticFile,
} from "remotion";

interface ClipData {
  clip_id: string;
  clip_path: string;
  summary: {
    title: string;
    summary: string;
    keywords: string[];
    hashtags: string[];
  };
  bilingual_srt?: string;
}

export interface ShortClipProps {
  clips: ClipData[];
  metadata: {
    title: string;
    channel: string;
  };
  brand?: string;
  template?: string;
  [key: string]: unknown;
}

export const ShortClip: React.FC<ShortClipProps> = ({
  clips,
  metadata,
  brand = "cursorbootcamp",
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames, width, height} = useVideoConfig();
  const clip = clips?.[0];

  const titleOpacity = interpolate(frame, [10, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const titleY = Math.round(
    interpolate(frame, [10, 30], [40, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  const hashtagOpacity = interpolate(frame, [40, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const outroOpacity = interpolate(
    frame,
    [durationInFrames - 30, durationInFrames - 10],
    [1, 0],
    {extrapolateLeft: "clamp", extrapolateRight: "clamp"}
  );

  const title = clip?.summary?.title || metadata?.title || "";
  const hashtags = clip?.summary?.hashtags || [];

  return (
    <AbsoluteFill style={{backgroundColor: "#000"}}>
      {/* Background video */}
      {clip?.clip_path && (
        <OffthreadVideo
          src={clip.clip_path}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      )}

      {/* Gradient overlay */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 40%, transparent 60%)",
          opacity: outroOpacity,
        }}
      />

      {/* Title */}
      <div
        style={{
          position: "absolute",
          bottom: 200,
          left: 40,
          right: 40,
          opacity: titleOpacity * outroOpacity,
          transform: `translateY(${titleY}px)`,
        }}
      >
        <div
          style={{
            color: "#FFF",
            fontSize: 48,
            fontWeight: "bold",
            fontFamily: "sans-serif",
            textShadow: "0 2px 20px rgba(0,0,0,0.8)",
            lineHeight: 1.3,
          }}
        >
          {title}
        </div>
      </div>

      {/* Hashtags */}
      <div
        style={{
          position: "absolute",
          bottom: 120,
          left: 40,
          right: 40,
          opacity: hashtagOpacity * outroOpacity,
        }}
      >
        <div
          style={{
            color: "#CCC",
            fontSize: 24,
            fontFamily: "sans-serif",
          }}
        >
          {hashtags.join("  ")}
        </div>
      </div>

      {/* Channel badge */}
      <div
        style={{
          position: "absolute",
          top: 60,
          left: 40,
          opacity: titleOpacity,
        }}
      >
        <div
          style={{
            background: "rgba(0,0,0,0.6)",
            borderRadius: 20,
            padding: "8px 16px",
            color: "#FFF",
            fontSize: 20,
            fontFamily: "sans-serif",
          }}
        >
          @{metadata?.channel || brand}
        </div>
      </div>
    </AbsoluteFill>
  );
};

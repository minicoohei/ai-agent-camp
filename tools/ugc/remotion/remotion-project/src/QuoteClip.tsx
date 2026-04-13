import {
  AbsoluteFill,
  OffthreadVideo,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

interface ClipData {
  clip_id: string;
  clip_path: string;
  summary: {
    title: string;
    summary: string;
    keywords: string[];
    hashtags: string[];
    duration_display: string;
  };
}

export interface QuoteClipProps {
  clips: ClipData[];
  metadata: {
    title: string;
    channel: string;
  };
  brand?: string;
  template?: string;
  [key: string]: unknown;
}

export const QuoteClip: React.FC<QuoteClipProps> = ({
  clips,
  metadata,
  brand = "cursorbootcamp",
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames, width, height} = useVideoConfig();
  const clip = clips?.[0];

  const fadeIn = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const slideIn = Math.round(
    interpolate(frame, [5, 25], [60, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  const summaryFade = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const outroFade = interpolate(
    frame,
    [durationInFrames - 20, durationInFrames - 5],
    [1, 0],
    {extrapolateLeft: "clamp", extrapolateRight: "clamp"}
  );

  const title = clip?.summary?.title || metadata?.title || "";
  const summary = clip?.summary?.summary || "";
  const channel = metadata?.channel || brand;

  return (
    <AbsoluteFill style={{backgroundColor: "#0F172A"}}>
      {/* Two-column layout: video left, text right */}
      <div
        style={{
          display: "flex",
          width: "100%",
          height: "100%",
          opacity: outroFade,
        }}
      >
        {/* Left: video */}
        <div
          style={{
            width: "55%",
            height: "100%",
            position: "relative",
            overflow: "hidden",
          }}
        >
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
          {/* Subtle gradient on right edge */}
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              width: 100,
              height: "100%",
              background:
                "linear-gradient(to left, #0F172A, transparent)",
            }}
          />
        </div>

        {/* Right: text */}
        <div
          style={{
            width: "45%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            padding: "60px 50px",
          }}
        >
          {/* Channel */}
          <div
            style={{
              color: "#94A3B8",
              fontSize: 22,
              fontFamily: "sans-serif",
              marginBottom: 20,
              opacity: fadeIn,
            }}
          >
            @{channel}
          </div>

          {/* Title */}
          <div
            style={{
              color: "#F8FAFC",
              fontSize: 42,
              fontWeight: "bold",
              fontFamily: "sans-serif",
              lineHeight: 1.3,
              opacity: fadeIn,
              transform: `translateY(${slideIn}px)`,
              marginBottom: 30,
            }}
          >
            {title}
          </div>

          {/* Accent line */}
          <div
            style={{
              width: interpolate(frame, [20, 40], [0, 80], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
              height: 3,
              backgroundColor: "#3B82F6",
              marginBottom: 30,
            }}
          />

          {/* Summary */}
          <div
            style={{
              color: "#CBD5E1",
              fontSize: 24,
              fontFamily: "sans-serif",
              lineHeight: 1.6,
              opacity: summaryFade,
            }}
          >
            {summary.length > 120
              ? summary.substring(0, 120) + "..."
              : summary}
          </div>

          {/* Keywords */}
          <div
            style={{
              display: "flex",
              gap: 12,
              marginTop: 30,
              opacity: summaryFade,
              flexWrap: "wrap",
            }}
          >
            {(clip?.summary?.keywords || []).map((kw, i) => (
              <div
                key={i}
                style={{
                  background: "rgba(59,130,246,0.2)",
                  border: "1px solid rgba(59,130,246,0.4)",
                  borderRadius: 16,
                  padding: "6px 14px",
                  color: "#93C5FD",
                  fontSize: 18,
                  fontFamily: "sans-serif",
                }}
              >
                {kw}
              </div>
            ))}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

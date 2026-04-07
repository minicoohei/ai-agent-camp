import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  Audio,
  staticFile,
  interpolate,
  spring,
  Easing,
} from "remotion";

// ─── Constants ──────────────────────────────────────────
const COLORS = {
  navy: "#031637",
  blue: "#1674EB",
  purple: "#7C3AED",
  cyan: "#06B6D4",
  green: "#10B981",
  orange: "#F59E0B",
  red: "#EF4444",
  pink: "#EC4899",
  white: "#FFFFFF",
  offWhite: "#FAFBFC",
  gray50: "#F9FAFB",
  gray100: "#F3F4F6",
  gray200: "#E5E7EB",
  gray300: "#D1D5DB",
  gray400: "#9CA3AF",
  gray500: "#6B7280",
  gray600: "#4B5563",
  gray700: "#374151",
  gray800: "#1F2937",
  gray900: "#111827",
};

const FONT = {
  primary: "'Noto Sans JP', 'Hiragino Sans', sans-serif",
  mono: "'SF Mono', 'Fira Code', monospace",
};

// ─── Scene durations (narration frames + 24 padding) ─────
const SCENE_FRAMES = [188, 161, 183, 165, 185, 120, 187, 82];

// ─── SVG Icons (replacing all emoji) ─────────────────────
const Icon: React.FC<{ path: string; size?: number; color?: string }> = ({
  path,
  size = 24,
  color = COLORS.blue,
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d={path} />
  </svg>
);

// Lucide-style icon paths
const ICONS = {
  book: "M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 0 6.5 22H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15z",
  box: "M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z",
  building:
    "M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2M10 6h4M10 10h4M10 14h4M10 18h4",
  palette:
    "M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.9 0 1.5-.7 1.5-1.5 0-.4-.1-.7-.4-1-.3-.3-.4-.7-.4-1.1 0-.8.7-1.5 1.5-1.5H16c3.3 0 6-2.7 6-6 0-5.5-4.5-9.9-10-9.9z",
  barChart: "M12 20V10M18 20V4M6 20v-4",
  video: "M23 7l-7 5 7 5V7zM14 5H3a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2z",
  cpu: "M18 12h2M4 12h2M12 4v2M12 18v2M7 7l1.5 1.5M15.5 15.5L17 17M7 17l1.5-1.5M15.5 8.5L17 7M9 9h6v6H9z",
  mail: "M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zM22 6l-10 7L2 6",
  messageSquare: "M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z",
  fileText:
    "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M16 13H8M16 17H8M10 9H8",
  search: "M21 21l-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0z",
  star: "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z",
  terminal: "M4 17l6-6-6-6M12 19h8",
  check: "M20 6L9 17l-5-5",
};

// ─── Helper: CountUp ────────────────────────────────────
const CountUp: React.FC<{
  frame: number;
  start: number;
  end: number;
  from: number;
  to: number;
  suffix?: string;
  fps: number;
}> = ({ frame, start, end, from, to, suffix = "", fps }) => {
  const progress = spring({
    frame: Math.max(0, frame - start),
    fps,
    config: { damping: 20, stiffness: 80, mass: 1 },
    durationInFrames: end - start,
  });
  const val = Math.round(from + (to - from) * progress);
  return (
    <span>
      {val}
      {suffix}
    </span>
  );
};

// ─── Helper: Typewriter ─────────────────────────────────
const Typewriter: React.FC<{
  text: string;
  frame: number;
  delay: number;
  speed?: number;
  style?: React.CSSProperties;
}> = ({ text, frame, delay, speed = 1.8, style }) => {
  const chars = Math.min(
    Math.floor(Math.max(0, frame - delay) * speed),
    text.length
  );
  const cursorOpacity = frame % 12 < 6 ? 1 : 0;
  return (
    <span style={style}>
      {text.slice(0, chars)}
      <span style={{ opacity: cursorOpacity, color: COLORS.cyan }}>|</span>
    </span>
  );
};

// ─── Browser Chrome (shared) ────────────────────────────
const BrowserChrome: React.FC<{
  url: string;
  children: React.ReactNode;
}> = ({ url, children }) => (
  <div style={{ padding: "0 40px", paddingTop: 30 }}>
    {/* Title bar */}
    <div
      style={{
        background: COLORS.white,
        borderRadius: "12px 12px 0 0",
        padding: "12px 16px",
        display: "flex",
        alignItems: "center",
        gap: 8,
        borderBottom: `1px solid ${COLORS.gray200}`,
      }}
    >
      <div
        style={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: "#FF5F56",
        }}
      />
      <div
        style={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: "#FFBD2E",
        }}
      />
      <div
        style={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: "#27C93F",
        }}
      />
      <div
        style={{
          flex: 1,
          marginLeft: 20,
          background: COLORS.gray100,
          borderRadius: 8,
          padding: "8px 16px",
          fontFamily: FONT.mono,
          fontSize: 14,
          color: COLORS.gray600,
        }}
      >
        {url}
      </div>
    </div>
    {/* Browser content */}
    <div
      style={{
        background: COLORS.offWhite,
        minHeight: 920,
        borderRadius: "0 0 12px 12px",
        overflow: "hidden",
      }}
    >
      {children}
    </div>
  </div>
);

// ═══════════════════════════════════════════════════════════
// Scene 1: Hero Landing
// ═══════════════════════════════════════════════════════════
const S1_HeroLanding: React.FC = () => {
  const frame = useCurrentFrame();

  const chromeOpacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const chromeY = interpolate(frame, [0, 15], [-30, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  // URL typing
  const urlText = "aiagent.camp";
  const urlChars = Math.min(
    Math.floor(Math.max(0, frame - 15) * 2),
    urlText.length
  );
  const typedUrl =
    urlChars < urlText.length
      ? urlText.slice(0, urlChars)
      : urlText;

  // Hero fade in
  const heroOpacity = interpolate(frame, [35, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const heroY = interpolate(frame, [35, 50], [30, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  // Rotating text
  const words = [
    "コード生成",
    "データ分析",
    "画像生成",
    "動画制作",
    "エージェント開発",
  ];
  const wordIdx = Math.floor(frame / 36) % words.length;
  const wp = (frame % 36) / 36;
  const wordOpacity =
    wp < 0.15
      ? interpolate(wp, [0, 0.15], [0, 1])
      : wp > 0.85
        ? interpolate(wp, [0.85, 1], [1, 0])
        : 1;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: COLORS.gray50,
        fontFamily: FONT.primary,
      }}
    >
      <div
        style={{
          opacity: chromeOpacity,
          transform: `translateY(${chromeY}px)`,
          padding: "0 40px",
          paddingTop: 30,
        }}
      >
        {/* Title bar */}
        <div
          style={{
            background: COLORS.white,
            borderRadius: "12px 12px 0 0",
            padding: "12px 16px",
            display: "flex",
            alignItems: "center",
            gap: 8,
            borderBottom: `1px solid ${COLORS.gray200}`,
          }}
        >
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#FF5F56" }} />
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#FFBD2E" }} />
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#27C93F" }} />
          <div
            style={{
              flex: 1,
              marginLeft: 20,
              background: COLORS.gray100,
              borderRadius: 8,
              padding: "8px 16px",
              fontFamily: FONT.mono,
              fontSize: 14,
              color: COLORS.gray600,
            }}
          >
            {typedUrl}
            {urlChars < urlText.length && (
              <span style={{ opacity: frame % 10 < 5 ? 1 : 0, color: COLORS.blue }}>|</span>
            )}
          </div>
        </div>

        {/* Hero section with gradient */}
        <div
          style={{
            background: `linear-gradient(135deg, ${COLORS.navy} 0%, #0D2B5E 50%, ${COLORS.blue} 100%)`,
            minHeight: 920,
            borderRadius: "0 0 12px 12px",
            padding: "100px 80px",
            position: "relative",
            overflow: "hidden",
          }}
        >
          {/* Subtle gradient orbs */}
          <div
            style={{
              position: "absolute",
              width: 600,
              height: 600,
              borderRadius: "50%",
              background: `radial-gradient(circle, rgba(22,116,235,0.2) 0%, transparent 70%)`,
              top: -100,
              right: -100,
            }}
          />
          <div
            style={{
              position: "absolute",
              width: 400,
              height: 400,
              borderRadius: "50%",
              background: `radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%)`,
              bottom: 50,
              left: -50,
            }}
          />

          {/* Content */}
          <div
            style={{
              opacity: heroOpacity,
              transform: `translateY(${heroY}px)`,
              position: "relative",
              zIndex: 1,
              textAlign: "center",
              paddingTop: 100,
            }}
          >
            <div
              style={{
                display: "inline-flex",
                background: "rgba(255,255,255,0.1)",
                border: "1px solid rgba(255,255,255,0.2)",
                borderRadius: 24,
                padding: "8px 24px",
                fontSize: 15,
                color: "rgba(255,255,255,0.8)",
                marginBottom: 36,
                letterSpacing: 3,
              }}
            >
              PRACTICAL AI SKILLS PLATFORM
            </div>

            <div
              style={{
                fontSize: 76,
                fontWeight: 900,
                color: COLORS.white,
                lineHeight: 1.15,
                marginBottom: 28,
              }}
            >
              AI Agent Camp
            </div>

            <div
              style={{
                fontSize: 48,
                fontWeight: 700,
                height: 64,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                marginBottom: 28,
              }}
            >
              <span
                style={{
                  opacity: wordOpacity,
                  background: `linear-gradient(90deg, ${COLORS.cyan}, #A78BFA)`,
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                {words[wordIdx]}
              </span>
            </div>

            <div
              style={{
                fontSize: 24,
                color: "rgba(255,255,255,0.7)",
                maxWidth: 700,
                margin: "0 auto",
                lineHeight: 1.6,
              }}
            >
              100以上の実践レッスンで、
              <br />
              AIを業務に組み込む力が身につく
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// Scene 2: Stats Bar
// ═══════════════════════════════════════════════════════════
const S2_StatsBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const stats = [
    { label: "レッスン", value: 95, suffix: "+", icon: ICONS.book, color: COLORS.blue },
    { label: "モジュール", value: 18, suffix: "", icon: ICONS.box, color: COLORS.purple },
    { label: "導入企業", value: 9, suffix: "社", icon: ICONS.building, color: COLORS.green },
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: COLORS.gray50,
        fontFamily: FONT.primary,
      }}
    >
      <BrowserChrome url="aiagent.camp">
        <div
          style={{
            padding: "100px 80px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            minHeight: 920,
            gap: 48,
          }}
        >
          <div
            style={{
              fontSize: 16,
              color: COLORS.blue,
              letterSpacing: 4,
              fontWeight: 600,
              opacity: interpolate(frame, [5, 15], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
            }}
          >
            PLATFORM STATS
          </div>

          <div style={{ display: "flex", gap: 48 }}>
            {stats.map((stat, i) => {
              const delay = 12 + i * 10;
              const s = spring({
                frame: Math.max(0, frame - delay),
                fps,
                config: { damping: 14, stiffness: 80 },
              });
              return (
                <div
                  key={i}
                  style={{
                    opacity: s,
                    transform: `translateY(${(1 - s) * 30}px)`,
                    background: COLORS.white,
                    borderRadius: 20,
                    border: `1px solid ${COLORS.gray200}`,
                    padding: "48px 56px",
                    textAlign: "center",
                    minWidth: 260,
                    boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
                  }}
                >
                  <div
                    style={{
                      width: 56,
                      height: 56,
                      borderRadius: 14,
                      background: `${stat.color}10`,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      margin: "0 auto 20px",
                    }}
                  >
                    <Icon path={stat.icon} size={28} color={stat.color} />
                  </div>
                  <div
                    style={{
                      fontSize: 64,
                      fontWeight: 900,
                      color: COLORS.gray900,
                      lineHeight: 1,
                      marginBottom: 8,
                    }}
                  >
                    <CountUp
                      frame={frame}
                      start={delay + 5}
                      end={delay + 45}
                      from={0}
                      to={stat.value}
                      suffix={stat.suffix}
                      fps={fps}
                    />
                  </div>
                  <div
                    style={{
                      fontSize: 20,
                      color: COLORS.gray500,
                      letterSpacing: 1,
                    }}
                  >
                    {stat.label}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </BrowserChrome>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// Scene 3: Use Cases Grid
// ═══════════════════════════════════════════════════════════
const S3_UseCases: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const useCases = [
    { title: "バナー生成", desc: "SNS広告を秒速で", color: COLORS.blue, icon: ICONS.palette },
    { title: "データ分析", desc: "BQ / Snowflake連携", color: COLORS.green, icon: ICONS.barChart },
    { title: "動画制作", desc: "Remotion + AI", color: COLORS.purple, icon: ICONS.video },
    { title: "エージェント開発", desc: "自律型AI構築", color: COLORS.cyan, icon: ICONS.cpu },
    { title: "メール自動化", desc: "受信→分析→返信", color: COLORS.orange, icon: ICONS.mail },
    { title: "Slack Bot", desc: "社内ナレッジ検索", color: COLORS.pink, icon: ICONS.messageSquare },
    { title: "請求書処理", desc: "PDF→仕訳→送信", color: COLORS.red, icon: ICONS.fileText },
    { title: "SEO最適化", desc: "記事量産パイプライン", color: COLORS.green, icon: ICONS.search },
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: COLORS.gray50,
        fontFamily: FONT.primary,
      }}
    >
      <BrowserChrome url="aiagent.camp/use-cases">
        <div style={{ padding: "50px 60px" }}>
          <div
            style={{
              textAlign: "center",
              marginBottom: 36,
              opacity: interpolate(frame, [0, 12], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              }),
            }}
          >
            <div
              style={{
                fontSize: 15,
                color: COLORS.blue,
                letterSpacing: 4,
                fontWeight: 600,
                marginBottom: 8,
              }}
            >
              USE CASES
            </div>
            <div style={{ fontSize: 40, fontWeight: 800, color: COLORS.gray900 }}>
              やりたいことが、全部ある
            </div>
          </div>

          <div style={{ display: "flex", flexWrap: "wrap", gap: 18, justifyContent: "center" }}>
            {useCases.map((uc, i) => {
              const delay = 15 + i * 5;
              const s = spring({
                frame: Math.max(0, frame - delay),
                fps,
                config: { damping: 16, stiffness: 90 },
              });
              const isActive = frame > delay + 30 && i === Math.floor((frame - 60) / 20) % 8;
              return (
                <div
                  key={i}
                  style={{
                    opacity: s,
                    transform: `translateY(${(1 - s) * 20}px) scale(${isActive ? 1.03 : 1})`,
                    background: COLORS.white,
                    borderRadius: 16,
                    border: `1px solid ${isActive ? uc.color : COLORS.gray200}`,
                    padding: "28px 28px",
                    width: "calc(25% - 18px)",
                    minWidth: 190,
                    boxShadow: isActive
                      ? `0 8px 24px ${uc.color}22`
                      : "0 2px 8px rgba(0,0,0,0.04)",
                  }}
                >
                  <div
                    style={{
                      width: 48,
                      height: 48,
                      borderRadius: 12,
                      background: `${uc.color}10`,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      marginBottom: 14,
                    }}
                  >
                    <Icon path={uc.icon} size={24} color={uc.color} />
                  </div>
                  <div
                    style={{
                      fontSize: 20,
                      fontWeight: 700,
                      color: COLORS.gray900,
                      marginBottom: 4,
                    }}
                  >
                    {uc.title}
                  </div>
                  <div style={{ fontSize: 14, color: COLORS.gray500 }}>{uc.desc}</div>
                </div>
              );
            })}
          </div>
        </div>
      </BrowserChrome>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// Scene 4: Curriculum Modules
// ═══════════════════════════════════════════════════════════
const S4_Curriculum: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const modules = [
    { num: "01", title: "AI Basics", color: COLORS.blue },
    { num: "02", title: "Prompt Engineering", color: COLORS.blue },
    { num: "03", title: "Claude Code", color: COLORS.purple },
    { num: "04", title: "MCP Servers", color: COLORS.purple },
    { num: "05", title: "Data Analysis", color: COLORS.green },
    { num: "06", title: "Banner Creator", color: COLORS.orange },
    { num: "07", title: "Video Production", color: COLORS.red },
    { num: "08", title: "SEO Automation", color: COLORS.green },
    { num: "09", title: "Slack Integration", color: COLORS.cyan },
    { num: "10", title: "Email Automation", color: COLORS.orange },
    { num: "11", title: "Invoice Processing", color: COLORS.red },
    { num: "12", title: "CRM Integration", color: COLORS.blue },
    { num: "13", title: "Agent SDK", color: COLORS.purple },
    { num: "14", title: "Multi-Agent", color: COLORS.purple },
    { num: "15", title: "RAG Pipeline", color: COLORS.green },
    { num: "16", title: "Security", color: COLORS.red },
    { num: "17", title: "Deployment", color: COLORS.cyan },
    { num: "18", title: "Capstone Project", color: COLORS.orange },
  ];

  const expandedIdx = 2;
  const expandStart = 80;
  const isExpanded = frame > expandStart;
  const expandProgress = spring({
    frame: Math.max(0, frame - expandStart),
    fps,
    config: { damping: 14, stiffness: 60 },
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: COLORS.gray50,
        fontFamily: FONT.primary,
      }}
    >
      <BrowserChrome url="aiagent.camp/curriculum">
        <div style={{ padding: "40px 50px", position: "relative" }}>
          <div style={{ textAlign: "center", marginBottom: 28 }}>
            <div
              style={{
                fontSize: 15,
                color: COLORS.blue,
                letterSpacing: 4,
                fontWeight: 600,
                marginBottom: 8,
              }}
            >
              CURRICULUM
            </div>
            <div style={{ fontSize: 36, fontWeight: 800, color: COLORS.gray900 }}>
              18モジュール・体系的カリキュラム
            </div>
          </div>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: 10,
              justifyContent: "center",
              opacity: isExpanded ? 1 - expandProgress * 0.2 : 1,
            }}
          >
            {modules.map((mod, i) => {
              const delay = 8 + i * 2.5;
              const s = spring({
                frame: Math.max(0, frame - delay),
                fps,
                config: { damping: 16, stiffness: 100 },
              });
              const isHighlighted = i === expandedIdx && isExpanded;
              return (
                <div
                  key={i}
                  style={{
                    opacity: s,
                    transform: `translateY(${(1 - s) * 15}px)`,
                    background: isHighlighted ? `${mod.color}08` : COLORS.white,
                    borderRadius: 12,
                    border: `1px solid ${isHighlighted ? mod.color : COLORS.gray200}`,
                    padding: "14px 18px",
                    width: "calc(16.666% - 10px)",
                    minWidth: 140,
                    textAlign: "center",
                    boxShadow: isHighlighted
                      ? `0 4px 16px ${mod.color}22`
                      : "0 1px 4px rgba(0,0,0,0.04)",
                  }}
                >
                  <div
                    style={{
                      fontSize: 11,
                      color: mod.color,
                      fontWeight: 700,
                      marginBottom: 2,
                    }}
                  >
                    Module {mod.num}
                  </div>
                  <div
                    style={{
                      fontSize: 13,
                      fontWeight: 600,
                      color: COLORS.gray800,
                    }}
                  >
                    {mod.title}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Expanded detail */}
          {isExpanded && (
            <div
              style={{
                position: "absolute",
                bottom: 30,
                left: "50%",
                transform: `translateX(-50%) translateY(${(1 - expandProgress) * 20}px)`,
                opacity: expandProgress,
                background: COLORS.white,
                borderRadius: 20,
                border: `2px solid ${COLORS.purple}`,
                padding: "28px 44px",
                width: 820,
                boxShadow: `0 12px 48px rgba(124,58,237,0.12)`,
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  marginBottom: 12,
                }}
              >
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: COLORS.purple,
                  }}
                />
                <span
                  style={{
                    fontSize: 13,
                    color: COLORS.purple,
                    fontWeight: 700,
                    letterSpacing: 2,
                  }}
                >
                  Module 03 — Claude Code
                </span>
              </div>
              <div
                style={{
                  fontSize: 24,
                  fontWeight: 800,
                  color: COLORS.gray900,
                  marginBottom: 16,
                }}
              >
                ターミナルからAIを操る
              </div>
              <div style={{ display: "flex", gap: 16 }}>
                {[
                  "基本操作とセットアップ",
                  "MCP Server構築",
                  "Skills & Hooks",
                  "チーム開発ワークフロー",
                ].map((item, j) => (
                  <div
                    key={j}
                    style={{
                      background: COLORS.gray50,
                      borderRadius: 8,
                      padding: "10px 16px",
                      flex: 1,
                      textAlign: "center",
                      fontSize: 14,
                      color: COLORS.gray700,
                      border: `1px solid ${COLORS.gray200}`,
                    }}
                  >
                    {item}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </BrowserChrome>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// Scene 5: Pricing Comparison
// ═══════════════════════════════════════════════════════════
const S5_Pricing: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const plans = [
    {
      name: "他社 A",
      price: "¥49,800/月",
      features: ["動画のみ", "英語中心", "サポートなし", "自習型"],
      highlight: false,
    },
    {
      name: "AI Agent Camp",
      price: "¥12,800/月",
      features: ["全18モジュール", "日本語完全対応", "AI Tutor 24/7", "実務直結"],
      highlight: true,
    },
    {
      name: "他社 B",
      price: "¥29,800/月",
      features: ["基礎のみ", "月2回ライブ", "コミュニティ", "半年契約"],
      highlight: false,
    },
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: COLORS.gray50,
        fontFamily: FONT.primary,
      }}
    >
      <BrowserChrome url="aiagent.camp/pricing">
        <div
          style={{
            padding: "60px 80px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            minHeight: 920,
          }}
        >
          <div
            style={{
              fontSize: 15,
              color: COLORS.blue,
              letterSpacing: 4,
              fontWeight: 600,
              marginBottom: 8,
            }}
          >
            PRICING
          </div>
          <div
            style={{
              fontSize: 36,
              fontWeight: 800,
              color: COLORS.gray900,
              marginBottom: 48,
            }}
          >
            圧倒的コストパフォーマンス
          </div>

          <div style={{ display: "flex", gap: 28 }}>
            {plans.map((plan, i) => {
              const delay = 18 + i * 10;
              const s = spring({
                frame: Math.max(0, frame - delay),
                fps,
                config: { damping: 14, stiffness: 70 },
              });
              const glowPulse = plan.highlight ? 0.5 + 0.5 * Math.sin(frame * 0.08) : 0;
              return (
                <div
                  key={i}
                  style={{
                    opacity: plan.highlight ? s : s * 0.7,
                    transform: `translateY(${(1 - s) * 30}px) scale(${plan.highlight ? 1.02 : 0.97})`,
                    background: COLORS.white,
                    borderRadius: 20,
                    border: plan.highlight
                      ? `2px solid ${COLORS.blue}`
                      : `1px solid ${COLORS.gray200}`,
                    padding: "44px 36px",
                    width: 320,
                    textAlign: "center",
                    boxShadow: plan.highlight
                      ? `0 8px ${24 + glowPulse * 16}px ${COLORS.blue}18`
                      : "0 2px 8px rgba(0,0,0,0.04)",
                    position: "relative",
                  }}
                >
                  {plan.highlight && (
                    <div
                      style={{
                        position: "absolute",
                        top: -14,
                        left: "50%",
                        transform: "translateX(-50%)",
                        background: `linear-gradient(90deg, ${COLORS.blue}, ${COLORS.purple})`,
                        borderRadius: 12,
                        padding: "4px 20px",
                        fontSize: 12,
                        fontWeight: 700,
                        color: COLORS.white,
                        letterSpacing: 2,
                      }}
                    >
                      BEST VALUE
                    </div>
                  )}
                  <div
                    style={{
                      fontSize: 20,
                      fontWeight: 700,
                      color: plan.highlight ? COLORS.blue : COLORS.gray400,
                      marginBottom: 16,
                    }}
                  >
                    {plan.name}
                  </div>
                  <div
                    style={{
                      fontSize: plan.highlight ? 44 : 32,
                      fontWeight: 900,
                      color: plan.highlight ? COLORS.gray900 : COLORS.gray400,
                      marginBottom: 28,
                    }}
                  >
                    {plan.price}
                  </div>
                  {plan.features.map((feat, j) => (
                    <div
                      key={j}
                      style={{
                        fontSize: 15,
                        color: plan.highlight ? COLORS.gray700 : COLORS.gray400,
                        padding: "10px 0",
                        borderBottom: `1px solid ${COLORS.gray100}`,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        gap: 8,
                      }}
                    >
                      {plan.highlight && (
                        <svg width={16} height={16} viewBox="0 0 24 24" fill="none" stroke={COLORS.green} strokeWidth={3}>
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                      )}
                      {feat}
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        </div>
      </BrowserChrome>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// Scene 6: Terminal Demo
// ═══════════════════════════════════════════════════════════
const S6_TerminalDemo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const command = "claude /skill banner-creator --topic 'AI Agent Camp'";
  const outputLines = [
    { text: "Generating banner for X post...", delay: 45, color: COLORS.cyan },
    { text: "Using Gemini Image Generation API", delay: 52, color: COLORS.gray400 },
    { text: "Prompt: Modern tech banner, AI Agent Camp...", delay: 57, color: COLORS.gray400 },
    { text: "Banner generated: output/banner_agentcamp.png", delay: 64, color: COLORS.green },
    { text: "Uploaded to Google Drive", delay: 70, color: COLORS.green },
    { text: "Done in 12.3s", delay: 76, color: COLORS.orange },
  ];

  const thumbSpring = spring({
    frame: Math.max(0, frame - 82),
    fps,
    config: { damping: 12, stiffness: 80 },
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: COLORS.gray50,
        fontFamily: FONT.primary,
      }}
    >
      <div style={{ padding: "0 40px", paddingTop: 30 }}>
        {/* Terminal chrome */}
        <div
          style={{
            background: COLORS.gray800,
            borderRadius: "12px 12px 0 0",
            padding: "12px 16px",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#FF5F56" }} />
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#FFBD2E" }} />
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#27C93F" }} />
          <div
            style={{
              flex: 1,
              textAlign: "center",
              fontSize: 13,
              color: COLORS.gray400,
            }}
          >
            Terminal — claude
          </div>
        </div>

        {/* Terminal body */}
        <div
          style={{
            background: "#1E1E2E",
            minHeight: 920,
            borderRadius: "0 0 12px 12px",
            padding: "40px 48px",
            fontFamily: FONT.mono,
            fontSize: 17,
          }}
        >
          <div style={{ marginBottom: 8, display: "flex", gap: 8 }}>
            <span style={{ color: COLORS.green }}>$</span>
            <Typewriter
              text={command}
              frame={frame}
              delay={8}
              speed={2.5}
              style={{ color: COLORS.white }}
            />
          </div>

          <div style={{ marginTop: 24 }}>
            {outputLines.map((line, i) => {
              const visible = frame > line.delay;
              const lineOpacity = visible
                ? interpolate(frame, [line.delay, line.delay + 4], [0, 1], {
                    extrapolateLeft: "clamp",
                    extrapolateRight: "clamp",
                  })
                : 0;
              return (
                <div
                  key={i}
                  style={{
                    opacity: lineOpacity,
                    color: line.color,
                    padding: "3px 0",
                    fontSize: 15,
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                  }}
                >
                  {line.color === COLORS.green && (
                    <svg width={14} height={14} viewBox="0 0 24 24" fill="none" stroke={COLORS.green} strokeWidth={3}>
                      <path d="M20 6L9 17l-5-5" />
                    </svg>
                  )}
                  {line.text}
                </div>
              );
            })}
          </div>

          {/* Result card */}
          <div
            style={{
              opacity: thumbSpring,
              transform: `translateY(${(1 - thumbSpring) * 15}px)`,
              marginTop: 36,
              display: "flex",
              gap: 24,
              alignItems: "center",
            }}
          >
            <div
              style={{
                width: 400,
                height: 210,
                borderRadius: 12,
                background: `linear-gradient(135deg, ${COLORS.blue}, ${COLORS.purple})`,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 28,
                fontWeight: 800,
                color: COLORS.white,
                fontFamily: FONT.primary,
                boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
              }}
            >
              AI Agent Camp
            </div>
            <div>
              <div
                style={{
                  fontSize: 18,
                  fontWeight: 700,
                  color: COLORS.white,
                  fontFamily: FONT.primary,
                  marginBottom: 8,
                }}
              >
                banner_agentcamp.png
              </div>
              <div style={{ fontSize: 14, color: COLORS.gray400 }}>1200 x 630 px — X Post</div>
              <div style={{ fontSize: 14, color: COLORS.green, marginTop: 8 }}>
                Google Drive uploaded
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// Scene 7: Social Proof
// ═══════════════════════════════════════════════════════════
const S7_SocialProof: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const reviews = [
    {
      name: "田中 太郎",
      role: "マーケティング部長",
      text: "業務効率が3倍に。特にバナー生成とデータ分析が素晴らしい",
    },
    {
      name: "佐藤 花子",
      role: "経理担当",
      text: "請求書処理が自動化されて、月30時間の工数削減を実現",
    },
    {
      name: "鈴木 一郎",
      role: "エンジニア",
      text: "AIエージェント開発の実践的なスキルが最短で身についた",
    },
  ];

  const circleProgress = spring({
    frame: Math.max(0, frame - 25),
    fps,
    config: { damping: 20, stiffness: 40 },
  });
  const circlePercent = 94;
  const circumference = 2 * Math.PI * 80;
  const dashOffset = circumference * (1 - circleProgress * (circlePercent / 100));

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: COLORS.gray50,
        fontFamily: FONT.primary,
      }}
    >
      <BrowserChrome url="aiagent.camp/reviews">
        <div
          style={{
            padding: "50px 60px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            minHeight: 920,
          }}
        >
          {/* Satisfaction circle */}
          <div style={{ position: "relative", width: 200, height: 200, marginBottom: 36 }}>
            <svg width={200} height={200} style={{ transform: "rotate(-90deg)" }}>
              <circle
                cx={100}
                cy={100}
                r={80}
                fill="none"
                stroke={COLORS.gray200}
                strokeWidth={10}
              />
              <circle
                cx={100}
                cy={100}
                r={80}
                fill="none"
                stroke={COLORS.blue}
                strokeWidth={10}
                strokeDasharray={circumference}
                strokeDashoffset={dashOffset}
                strokeLinecap="round"
              />
            </svg>
            <div
              style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: 48, fontWeight: 900, color: COLORS.gray900 }}>
                {Math.round(circlePercent * circleProgress)}%
              </div>
              <div style={{ fontSize: 14, color: COLORS.gray500 }}>満足度</div>
            </div>
          </div>

          {/* Review cards */}
          <div style={{ display: "flex", gap: 24 }}>
            {reviews.map((review, i) => {
              const delay = 15 + i * 10;
              const s = spring({
                frame: Math.max(0, frame - delay),
                fps,
                config: { damping: 14, stiffness: 80 },
              });
              return (
                <div
                  key={i}
                  style={{
                    opacity: s,
                    transform: `translateX(${(1 - s) * (i === 0 ? -30 : i === 2 ? 30 : 0)}px)`,
                    background: COLORS.white,
                    borderRadius: 16,
                    border: `1px solid ${COLORS.gray200}`,
                    padding: "32px",
                    width: 320,
                    boxShadow: "0 2px 12px rgba(0,0,0,0.04)",
                  }}
                >
                  {/* Stars as SVG */}
                  <div style={{ display: "flex", gap: 4, marginBottom: 16 }}>
                    {[0, 1, 2, 3, 4].map((j) => (
                      <svg key={j} width={20} height={20} viewBox="0 0 24 24" fill={COLORS.orange} stroke="none">
                        <path d={ICONS.star} />
                      </svg>
                    ))}
                  </div>
                  <div
                    style={{
                      fontSize: 15,
                      color: COLORS.gray700,
                      lineHeight: 1.6,
                      marginBottom: 20,
                    }}
                  >
                    {review.text}
                  </div>
                  <div style={{ fontSize: 16, fontWeight: 700, color: COLORS.gray900 }}>
                    {review.name}
                  </div>
                  <div style={{ fontSize: 13, color: COLORS.gray500 }}>{review.role}</div>
                </div>
              );
            })}
          </div>
        </div>
      </BrowserChrome>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// Scene 8: CTA
// ═══════════════════════════════════════════════════════════
const S8_CTA: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoSpring = spring({
    frame: Math.max(0, frame - 5),
    fps,
    config: { damping: 12, stiffness: 60 },
  });
  const buttonPulse = 1 + 0.03 * Math.sin(frame * 0.15);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: COLORS.white,
        fontFamily: FONT.primary,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 28,
      }}
    >
      <div
        style={{
          opacity: logoSpring,
          transform: `scale(${0.85 + logoSpring * 0.15})`,
          fontSize: 72,
          fontWeight: 900,
          background: `linear-gradient(135deg, ${COLORS.navy}, ${COLORS.blue})`,
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}
      >
        AI Agent Camp
      </div>
      <div
        style={{
          opacity: logoSpring,
          fontSize: 22,
          color: COLORS.gray600,
          letterSpacing: 2,
        }}
      >
        AIを業務に組み込む実践スキル
      </div>
      <div
        style={{
          opacity: logoSpring,
          transform: `scale(${buttonPulse})`,
          background: `linear-gradient(135deg, ${COLORS.blue}, ${COLORS.purple})`,
          borderRadius: 16,
          padding: "18px 60px",
          fontSize: 22,
          fontWeight: 700,
          color: COLORS.white,
          boxShadow: `0 8px 24px ${COLORS.blue}33`,
          marginTop: 12,
        }}
      >
        今すぐ始める
      </div>
      <div
        style={{
          opacity: logoSpring,
          fontSize: 18,
          color: COLORS.gray400,
          fontFamily: FONT.mono,
          marginTop: 4,
        }}
      >
        aiagent.camp
      </div>
    </div>
  );
};

// ═══════════════════════════════════════════════════════════
// Main Composition
// ═══════════════════════════════════════════════════════════
export const AgentCampContentScreenDemoComposition: React.FC = () => {
  const scenes = [
    S1_HeroLanding,
    S2_StatsBar,
    S3_UseCases,
    S4_Curriculum,
    S5_Pricing,
    S6_TerminalDemo,
    S7_SocialProof,
    S8_CTA,
  ];

  let offset = 0;
  const sceneStarts: number[] = [];
  for (const dur of SCENE_FRAMES) {
    sceneStarts.push(offset);
    offset += dur;
  }

  return (
    <div style={{ width: "100%", height: "100%", background: COLORS.gray50 }}>
      {scenes.map((SceneComponent, i) => (
        <Sequence key={i} from={sceneStarts[i]} durationInFrames={SCENE_FRAMES[i]}>
          <SceneComponent />
        </Sequence>
      ))}

      {SCENE_FRAMES.map((_, i) => (
        <Sequence key={`audio-${i}`} from={sceneStarts[i]} durationInFrames={SCENE_FRAMES[i]}>
          <Audio
            src={staticFile(
              `narration_fast/agentcamp_content_screen/frame_${String(i + 1).padStart(2, "0")}.mp3`
            )}
            volume={1}
          />
        </Sequence>
      ))}

      <Audio src={staticFile("agentcamp_content_bgm.mp3")} volume={0.15} />
    </div>
  );
};

import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

// ─── Constants ──────────────────────────────────────────
const COLORS = {
  navy: "#031637",
  blue: "#1674EB",
  purple: "#7C3AED",
  cyan: "#06B6D4",
  green: "#10B981",
  red: "#EF4444",
  orange: "#F59E0B",
  white: "#FFFFFF",
  gray100: "#F3F4F6",
  gray200: "#E5E7EB",
  gray300: "#D1D5DB",
  gray500: "#6B7280",
  gray700: "#374151",
  gray800: "#1F2937",
  gray900: "#111827",
  editorBg: "#1E1E2E",
  sidebarBg: "#181825",
  terminalBg: "#11111B",
  chatBg: "#1E1E2E",
};

const FONT = {
  primary: "'Noto Sans JP', 'Hiragino Sans', sans-serif",
  mono: "'SF Mono', 'Fira Code', 'Menlo', monospace",
};

// ─── Types ──────────────────────────────────────────────
interface Scene {
  scene_number: number;
  layout: string;
  caption: string;
  duration: number;
  title?: string;
  subtitle?: string;
  before_text?: string;
  after_text?: string;
  cta_text?: string;
  cta_url?: string;
}

interface ScreenExplainerProps {
  scenes?: Scene[];
  productName?: string;
  accentColor?: string;
}

// ─── Background ─────────────────────────────────────────
const Background: React.FC<{
  variant?: "dark" | "gradient" | "accent";
}> = ({ variant = "dark" }) => {
  const bg =
    variant === "accent"
      ? `linear-gradient(135deg, ${COLORS.purple} 0%, ${COLORS.blue} 100%)`
      : variant === "gradient"
        ? `linear-gradient(135deg, #0a1628 0%, #1a1040 100%)`
        : `linear-gradient(135deg, ${COLORS.navy} 0%, #0d1b3e 100%)`;

  return (
    <AbsoluteFill style={{ background: bg }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
      />
    </AbsoluteFill>
  );
};

// ─── Top Bar ────────────────────────────────────────────
const TopBar: React.FC<{
  productName: string;
  accentColor: string;
  frame: number;
  fps: number;
}> = ({ productName, accentColor, frame, fps }) => {
  const { height } = useVideoConfig();
  const isVertical = height > 1200;
  const barHeight = isVertical ? 72 : 52;
  const fontSize = isVertical ? 28 : 20;
  const dotSize = isVertical ? 14 : 10;
  const slideIn = spring({ frame, fps, config: { damping: 20, stiffness: 200 } });
  const y = interpolate(slideIn, [0, 1], [-(barHeight + 4), 0]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        height: barHeight,
        background: "rgba(0,0,0,0.7)",
        backdropFilter: "blur(10px)",
        display: "flex",
        alignItems: "center",
        paddingLeft: 28,
        transform: `translateY(${y}px)`,
        zIndex: 50,
        borderBottom: `2px solid ${accentColor}40`,
      }}
    >
      <div style={{ width: dotSize, height: dotSize, borderRadius: "50%", background: accentColor, marginRight: 10 }} />
      <span style={{ fontFamily: FONT.primary, fontSize, fontWeight: 700, color: COLORS.white, letterSpacing: "0.04em" }}>
        {productName}
      </span>
    </div>
  );
};

// ─── Caption Bar ────────────────────────────────────────
const CaptionBar: React.FC<{ text: string; frame: number; fps: number }> = ({ text, frame, fps }) => {
  const { height } = useVideoConfig();
  const isVertical = height > 1200;
  const barHeight = isVertical ? 96 : 64;
  const fontSize = isVertical ? 40 : 26;
  const slideIn = spring({ frame: Math.max(0, frame - 5), fps, config: { damping: 15, stiffness: 180 } });
  const y = interpolate(slideIn, [0, 1], [barHeight + 4, 0]);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height: barHeight,
        background: "rgba(0,0,0,0.75)",
        backdropFilter: "blur(8px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transform: `translateY(${y}px)`,
        zIndex: 50,
      }}
    >
      <span style={{ fontFamily: FONT.primary, fontSize, fontWeight: 700, color: COLORS.white }}>
        {text}
      </span>
    </div>
  );
};

// ═══════════════════════════════════════════════════════
// DEMO UI COMPONENTS (Remotion-built, not screenshots)
// ═══════════════════════════════════════════════════════

// ─── Cursor IDE Mock ────────────────────────────────────
const CursorIDEDemo: React.FC<{ frame: number; fps: number; durationFrames: number }> = ({
  frame,
  fps,
  durationFrames,
}) => {
  const scaleIn = spring({ frame, fps, config: { damping: 18, stiffness: 120 } });

  // Typing animation for code
  const codeLines = [
    { text: "import { analyzeCompetitors } from './agent';", color: COLORS.purple },
    { text: "import { generateLP } from './lp-builder';", color: COLORS.purple },
    { text: "", color: COLORS.white },
    { text: "// AI Agentが競合調査を自動実行", color: COLORS.gray500 },
    { text: "const competitors = await analyzeCompetitors({", color: COLORS.cyan },
    { text: '  industry: "SaaS",', color: COLORS.orange },
    { text: '  region: "Japan",', color: COLORS.orange },
    { text: "  depth: 3,", color: COLORS.orange },
    { text: "});", color: COLORS.cyan },
    { text: "", color: COLORS.white },
    { text: "// LP自動生成 + デプロイ", color: COLORS.gray500 },
    { text: "const lp = await generateLP(competitors);", color: COLORS.green },
    { text: 'await lp.deploy("production");', color: COLORS.green },
  ];

  // AI chat messages
  const chatMessages = [
    { role: "user", text: "SaaS業界の競合分析をして、LPを作成してください", delay: 10 },
    { role: "ai", text: "了解しました。競合3社を分析中...", delay: 40 },
    { role: "ai", text: "分析完了。LP構成を生成します。\nヒーロー / 機能比較 / CTA の3セクション構成を提案します。", delay: 80 },
  ];

  // File tree items
  const files = [
    { name: "src/", indent: 0, icon: "dir" },
    { name: "agent.ts", indent: 1, icon: "ts" },
    { name: "lp-builder.ts", indent: 1, icon: "ts", active: true },
    { name: "competitors.ts", indent: 1, icon: "ts" },
    { name: "deploy.ts", indent: 1, icon: "ts" },
    { name: "config/", indent: 0, icon: "dir" },
    { name: "settings.json", indent: 1, icon: "json" },
    { name: "package.json", indent: 0, icon: "json" },
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        padding: "64px 28px 76px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        transform: `scale(${scaleIn})`,
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          borderRadius: 12,
          overflow: "hidden",
          boxShadow: "0 20px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08)",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Title bar */}
        <div
          style={{
            height: 36,
            background: COLORS.sidebarBg,
            display: "flex",
            alignItems: "center",
            padding: "0 14px",
            gap: 7,
            borderBottom: "1px solid rgba(255,255,255,0.06)",
          }}
        >
          <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#FF5F56" }} />
          <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#FFBD2E" }} />
          <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#27C93F" }} />
          <span style={{ marginLeft: 14, fontFamily: FONT.mono, fontSize: 12, color: COLORS.gray500 }}>
            lp-builder.ts - AI Agent Camp
          </span>
        </div>

        {/* Main area */}
        <div style={{ flex: 1, display: "flex" }}>
          {/* Sidebar - File tree */}
          <div
            style={{
              width: 200,
              background: COLORS.sidebarBg,
              borderRight: "1px solid rgba(255,255,255,0.06)",
              padding: "12px 0",
            }}
          >
            <div style={{ padding: "0 14px 8px", fontFamily: FONT.mono, fontSize: 11, color: COLORS.gray500, textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Explorer
            </div>
            {files.map((file, i) => {
              const fileSpring = spring({ frame: Math.max(0, frame - i * 3), fps, config: { damping: 20, stiffness: 200 } });
              return (
                <div
                  key={i}
                  style={{
                    padding: "3px 14px",
                    paddingLeft: 14 + file.indent * 16,
                    fontFamily: FONT.mono,
                    fontSize: 13,
                    color: file.active ? COLORS.white : COLORS.gray500,
                    background: file.active ? "rgba(22,116,235,0.15)" : "transparent",
                    borderLeft: file.active ? `2px solid ${COLORS.blue}` : "2px solid transparent",
                    opacity: fileSpring,
                  }}
                >
                  <span style={{ color: file.icon === "dir" ? COLORS.orange : file.icon === "ts" ? COLORS.blue : COLORS.green, marginRight: 6 }}>
                    {file.icon === "dir" ? ">" : "#"}
                  </span>
                  {file.name}
                </div>
              );
            })}
          </div>

          {/* Code editor */}
          <div
            style={{
              flex: 1,
              background: COLORS.editorBg,
              padding: "16px 0",
              overflow: "hidden",
            }}
          >
            {codeLines.map((line, i) => {
              const lineDelay = 5 + i * 4;
              const charsVisible = Math.max(0, Math.floor((frame - lineDelay) * 2));
              const visibleText = line.text.slice(0, charsVisible);
              const cursorVisible = frame % 16 < 8 && charsVisible < line.text.length && charsVisible > 0;

              return (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    fontFamily: FONT.mono,
                    fontSize: 15,
                    lineHeight: "26px",
                    height: 26,
                    opacity: frame > lineDelay ? 1 : 0.15,
                  }}
                >
                  <span style={{ width: 48, textAlign: "right", color: "rgba(255,255,255,0.2)", paddingRight: 16, userSelect: "none" }}>
                    {i + 1}
                  </span>
                  <span style={{ color: line.color }}>{visibleText}</span>
                  {cursorVisible && <span style={{ color: COLORS.blue, fontWeight: 700 }}>|</span>}
                </div>
              );
            })}
          </div>

          {/* AI Chat panel */}
          <div
            style={{
              width: 320,
              background: COLORS.chatBg,
              borderLeft: "1px solid rgba(255,255,255,0.06)",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div style={{ padding: "10px 16px", borderBottom: "1px solid rgba(255,255,255,0.06)", display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ width: 8, height: 8, borderRadius: "50%", background: COLORS.purple }} />
              <span style={{ fontFamily: FONT.mono, fontSize: 13, color: COLORS.gray500 }}>AI Agent</span>
              <div style={{ marginLeft: "auto", width: 50, height: 6, borderRadius: 3, background: `linear-gradient(90deg, ${COLORS.blue}, ${COLORS.purple})` }} />
            </div>
            <div style={{ flex: 1, padding: 12, display: "flex", flexDirection: "column", gap: 10, overflow: "hidden" }}>
              {chatMessages.map((msg, i) => {
                const msgSpring = spring({ frame: Math.max(0, frame - msg.delay), fps, config: { damping: 16, stiffness: 120 } });
                const isUser = msg.role === "user";
                return (
                  <div
                    key={i}
                    style={{
                      opacity: msgSpring,
                      transform: `translateY(${interpolate(msgSpring, [0, 1], [15, 0])}px)`,
                      alignSelf: isUser ? "flex-end" : "flex-start",
                      maxWidth: "90%",
                      background: isUser ? COLORS.blue + "30" : "rgba(255,255,255,0.05)",
                      border: `1px solid ${isUser ? COLORS.blue + "40" : "rgba(255,255,255,0.08)"}`,
                      borderRadius: 10,
                      padding: "8px 12px",
                      fontFamily: FONT.primary,
                      fontSize: 12,
                      color: COLORS.gray200,
                      lineHeight: 1.5,
                      whiteSpace: "pre-wrap",
                    }}
                  >
                    {msg.text}
                  </div>
                );
              })}
              {/* Typing indicator */}
              {frame > 120 && (
                <div style={{ display: "flex", gap: 4, padding: "8px 12px" }}>
                  {[0, 1, 2].map((d) => (
                    <div
                      key={d}
                      style={{
                        width: 6,
                        height: 6,
                        borderRadius: "50%",
                        background: COLORS.purple,
                        opacity: interpolate(Math.sin((frame / fps) * Math.PI * 3 + d * 1.2), [-1, 1], [0.3, 1]),
                      }}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Status bar */}
        <div
          style={{
            height: 24,
            background: COLORS.blue,
            display: "flex",
            alignItems: "center",
            padding: "0 12px",
            gap: 16,
            fontFamily: FONT.mono,
            fontSize: 11,
            color: "rgba(255,255,255,0.9)",
          }}
        >
          <span>AI Agent Camp</span>
          <span>TypeScript</span>
          <span>UTF-8</span>
          <span style={{ marginLeft: "auto" }}>Ln 12, Col 35</span>
        </div>
      </div>
    </div>
  );
};

// ─── Terminal Demo ──────────────────────────────────────
const TerminalDemo: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const scaleIn = spring({ frame, fps, config: { damping: 18, stiffness: 120 } });

  const commands = [
    { prompt: "$ agent run competitive-analysis", output: null, delay: 0 },
    { prompt: null, output: "[1/4] Fetching competitor data...", delay: 20, color: COLORS.cyan },
    { prompt: null, output: "[2/4] Analyzing pricing models...", delay: 35, color: COLORS.cyan },
    { prompt: null, output: "[3/4] Generating comparison matrix...", delay: 50, color: COLORS.cyan },
    { prompt: null, output: "[4/4] Creating LP draft...", delay: 65, color: COLORS.cyan },
    { prompt: null, output: "", delay: 75 },
    { prompt: null, output: "  Competitors analyzed:  12", delay: 80, color: COLORS.green },
    { prompt: null, output: "  Features compared:    48", delay: 85, color: COLORS.green },
    { prompt: null, output: "  LP sections:           5", delay: 90, color: COLORS.green },
    { prompt: null, output: "  Estimated time saved: 96%", delay: 95, color: COLORS.orange },
    { prompt: null, output: "", delay: 100 },
    { prompt: null, output: "  LP deployed to: https://ai-agent.camp/lp/demo", delay: 108, color: COLORS.blue },
    { prompt: null, output: "  Done in 47.2s", delay: 115, color: COLORS.green },
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        padding: "64px 60px 76px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        transform: `scale(${scaleIn})`,
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          borderRadius: 12,
          overflow: "hidden",
          boxShadow: "0 20px 80px rgba(0,0,0,0.6)",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Terminal title bar */}
        <div
          style={{
            height: 36,
            background: "#2D2D3D",
            display: "flex",
            alignItems: "center",
            padding: "0 14px",
            gap: 7,
          }}
        >
          <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#FF5F56" }} />
          <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#FFBD2E" }} />
          <div style={{ width: 11, height: 11, borderRadius: "50%", background: "#27C93F" }} />
          <span style={{ marginLeft: 14, fontFamily: FONT.mono, fontSize: 12, color: COLORS.gray500 }}>
            agent-cli ~ AI Agent Camp
          </span>
        </div>

        {/* Terminal body */}
        <div
          style={{
            flex: 1,
            background: COLORS.terminalBg,
            padding: "20px 24px",
            fontFamily: FONT.mono,
            fontSize: 16,
            lineHeight: 2,
            overflow: "hidden",
          }}
        >
          {commands.map((cmd, i) => {
            const visible = frame > cmd.delay;
            if (!visible) return null;

            const charsVisible = Math.max(0, Math.floor((frame - cmd.delay) * 2.5));

            if (cmd.prompt) {
              const visibleText = cmd.prompt.slice(0, charsVisible);
              const cursorOn = frame % 14 < 7 && charsVisible < cmd.prompt.length;
              return (
                <div key={i}>
                  <span style={{ color: COLORS.green }}>{visibleText.slice(0, 2)}</span>
                  <span style={{ color: COLORS.white }}>{visibleText.slice(2)}</span>
                  {cursorOn && <span style={{ color: COLORS.green }}>_</span>}
                </div>
              );
            }

            return (
              <div key={i} style={{ color: cmd.color || COLORS.gray500 }}>
                {cmd.output}
              </div>
            );
          })}

          {/* Blinking cursor at end */}
          {frame > 120 && (
            <div style={{ opacity: frame % 20 < 10 ? 1 : 0 }}>
              <span style={{ color: COLORS.green }}>$ </span>
              <span style={{ color: COLORS.green }}>_</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ─── Dashboard / Results Demo ───────────────────────────
const DashboardDemo: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const scaleIn = spring({ frame, fps, config: { damping: 18, stiffness: 120 } });

  const metrics = [
    { label: "LP作成時間", value: "47秒", prev: "2週間", color: COLORS.green, delay: 15 },
    { label: "競合分析数", value: "12社", prev: "手動3社", color: COLORS.blue, delay: 25 },
    { label: "コスト削減", value: "96%", prev: "-", color: COLORS.purple, delay: 35 },
    { label: "品質スコア", value: "94/100", prev: "手動72", color: COLORS.orange, delay: 45 },
  ];

  const tasks = [
    { name: "競合調査 (12社)", status: "done", delay: 50 },
    { name: "市場分析レポート", status: "done", delay: 55 },
    { name: "LP構成設計", status: "done", delay: 60 },
    { name: "コピーライティング", status: "done", delay: 65 },
    { name: "デザイン適用", status: "done", delay: 70 },
    { name: "SEO最適化", status: "running", delay: 78 },
    { name: "A/Bテスト設定", status: "pending", delay: 85 },
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        padding: "64px 40px 76px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        transform: `scale(${scaleIn})`,
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          borderRadius: 12,
          overflow: "hidden",
          boxShadow: "0 20px 80px rgba(0,0,0,0.6)",
          background: COLORS.editorBg,
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Header */}
        <div style={{ height: 48, background: COLORS.sidebarBg, display: "flex", alignItems: "center", padding: "0 24px", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
          <div style={{ width: 8, height: 8, borderRadius: "50%", background: COLORS.green, marginRight: 10 }} />
          <span style={{ fontFamily: FONT.primary, fontSize: 16, fontWeight: 700, color: COLORS.white }}>AI Agent Dashboard</span>
          <span style={{ marginLeft: "auto", fontFamily: FONT.mono, fontSize: 12, color: COLORS.gray500 }}>Last run: just now</span>
        </div>

        <div style={{ flex: 1, display: "flex", padding: 20, gap: 20 }}>
          {/* Left: Metrics grid */}
          <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 16 }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              {metrics.map((m, i) => {
                const cardSpring = spring({ frame: Math.max(0, frame - m.delay), fps, config: { damping: 14, stiffness: 120 } });
                return (
                  <div
                    key={i}
                    style={{
                      background: "rgba(255,255,255,0.04)",
                      border: "1px solid rgba(255,255,255,0.08)",
                      borderRadius: 10,
                      padding: "16px 20px",
                      transform: `scale(${cardSpring})`,
                    }}
                  >
                    <div style={{ fontFamily: FONT.primary, fontSize: 12, color: COLORS.gray500, marginBottom: 6 }}>{m.label}</div>
                    <div style={{ fontFamily: FONT.mono, fontSize: 32, fontWeight: 800, color: m.color }}>{m.value}</div>
                    <div style={{ fontFamily: FONT.mono, fontSize: 11, color: COLORS.gray500, marginTop: 4 }}>Before: {m.prev}</div>
                  </div>
                );
              })}
            </div>

            {/* Progress bar */}
            <div style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 10, padding: "16px 20px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <span style={{ fontFamily: FONT.primary, fontSize: 13, color: COLORS.gray200 }}>Overall Progress</span>
                <span style={{ fontFamily: FONT.mono, fontSize: 13, color: COLORS.green }}>86%</span>
              </div>
              <div style={{ height: 8, background: "rgba(255,255,255,0.1)", borderRadius: 4, overflow: "hidden" }}>
                <div
                  style={{
                    width: `${interpolate(frame, [60, 100], [0, 86], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}%`,
                    height: "100%",
                    background: `linear-gradient(90deg, ${COLORS.blue}, ${COLORS.green})`,
                    borderRadius: 4,
                  }}
                />
              </div>
            </div>
          </div>

          {/* Right: Task list */}
          <div style={{ width: 340, background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: 10, padding: 16 }}>
            <div style={{ fontFamily: FONT.primary, fontSize: 14, fontWeight: 600, color: COLORS.white, marginBottom: 12 }}>Agent Tasks</div>
            {tasks.map((task, i) => {
              const taskSpring = spring({ frame: Math.max(0, frame - task.delay), fps, config: { damping: 20, stiffness: 200 } });
              const statusColor = task.status === "done" ? COLORS.green : task.status === "running" ? COLORS.blue : COLORS.gray500;
              const statusIcon = task.status === "done" ? "OK" : task.status === "running" ? ">>" : "--";
              return (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 10,
                    padding: "6px 0",
                    opacity: taskSpring,
                    borderBottom: "1px solid rgba(255,255,255,0.04)",
                  }}
                >
                  <span style={{ fontFamily: FONT.mono, fontSize: 12, color: statusColor, width: 24 }}>
                    {task.status === "running" && frame % 20 < 10 ? ">>" : statusIcon}
                  </span>
                  <span style={{ fontFamily: FONT.primary, fontSize: 13, color: task.status === "pending" ? COLORS.gray500 : COLORS.gray200, flex: 1 }}>{task.name}</span>
                  {task.status === "running" && (
                    <div style={{ width: 40, height: 4, borderRadius: 2, background: "rgba(255,255,255,0.1)", overflow: "hidden" }}>
                      <div style={{ width: `${interpolate(Math.sin((frame / fps) * Math.PI * 2), [-1, 1], [30, 90])}%`, height: "100%", background: COLORS.blue, borderRadius: 2 }} />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

// ─── Title Scene ────────────────────────────────────────
const TitleScene: React.FC<{ scene: Scene; frame: number; fps: number; accentColor: string }> = ({
  scene, frame, fps, accentColor,
}) => {
  const titleSpring = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  const subtitleSpring = spring({ frame: Math.max(0, frame - 10), fps, config: { damping: 14, stiffness: 100 } });

  return (
    <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 80 }}>
      <div style={{ transform: `scale(${titleSpring})`, fontFamily: FONT.primary, fontSize: 60, fontWeight: 900, color: COLORS.white, textAlign: "center", lineHeight: 1.3 }}>
        {scene.title}
      </div>
      {scene.subtitle && (
        <div style={{ opacity: subtitleSpring, transform: `translateY(${interpolate(subtitleSpring, [0, 1], [20, 0])}px)`, fontFamily: FONT.primary, fontSize: 30, color: accentColor, textAlign: "center", marginTop: 20 }}>
          {scene.subtitle}
        </div>
      )}
    </div>
  );
};

// ─── Comparison Scene ───────────────────────────────────
const ComparisonScene: React.FC<{ scene: Scene; frame: number; fps: number; accentColor: string }> = ({
  scene, frame, fps, accentColor,
}) => {
  const beforeSpring = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  const afterSpring = spring({ frame: Math.max(0, frame - 15), fps, config: { damping: 14, stiffness: 100 } });
  const arrowOpacity = interpolate(frame, [10, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div style={{ width: "100%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center", gap: 60, padding: "72px 100px 88px" }}>
      <div style={{ transform: `scale(${beforeSpring})`, background: "rgba(239,68,68,0.12)", border: "2px solid rgba(239,68,68,0.4)", borderRadius: 24, padding: "40px 60px", textAlign: "center" }}>
        <div style={{ fontFamily: FONT.primary, fontSize: 20, color: COLORS.red, marginBottom: 12, fontWeight: 600 }}>Before</div>
        <div style={{ fontFamily: FONT.primary, fontSize: 56, fontWeight: 900, color: COLORS.white }}>{scene.before_text}</div>
      </div>
      <svg width="80" height="40" viewBox="0 0 80 40" style={{ opacity: arrowOpacity }}>
        <path d="M5 20 L60 20 M50 8 L65 20 L50 32" stroke={accentColor} strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <div style={{ transform: `scale(${afterSpring})`, background: "rgba(16,185,129,0.12)", border: "2px solid rgba(16,185,129,0.4)", borderRadius: 24, padding: "40px 60px", textAlign: "center" }}>
        <div style={{ fontFamily: FONT.primary, fontSize: 20, color: COLORS.green, marginBottom: 12, fontWeight: 600 }}>After</div>
        <div style={{ fontFamily: FONT.primary, fontSize: 56, fontWeight: 900, color: COLORS.white }}>{scene.after_text}</div>
      </div>
    </div>
  );
};

// ─── CTA Scene ──────────────────────────────────────────
const CTAScene: React.FC<{ scene: Scene; frame: number; fps: number; accentColor: string; productName: string }> = ({
  scene, frame, fps, accentColor, productName,
}) => {
  const titleScale = spring({ frame, fps, config: { damping: 12, stiffness: 80 } });
  const btnSpring = spring({ frame: Math.max(0, frame - 12), fps, config: { damping: 14, stiffness: 120 } });
  const pulse = Math.sin((frame / fps) * Math.PI * 2) * 0.02 + 1;

  return (
    <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 36, padding: 80 }}>
      <div style={{ transform: `scale(${titleScale})`, fontFamily: FONT.primary, fontSize: 56, fontWeight: 900, color: COLORS.white, textAlign: "center", lineHeight: 1.4 }}>
        {scene.title || productName}
      </div>
      {scene.cta_text && (
        <div style={{ transform: `scale(${btnSpring * pulse})`, background: accentColor, borderRadius: 16, padding: "20px 56px", fontFamily: FONT.primary, fontSize: 28, fontWeight: 700, color: COLORS.white, boxShadow: `0 8px 32px ${accentColor}60` }}>
          {scene.cta_text}
        </div>
      )}
      {scene.cta_url && (
        <div style={{ opacity: btnSpring, fontFamily: FONT.mono, fontSize: 22, color: COLORS.gray500 }}>
          {scene.cta_url}
        </div>
      )}
    </div>
  );
};

// ─── Scene Router ───────────────────────────────────────
const SceneContent: React.FC<{
  scene: Scene;
  durationFrames: number;
  accentColor: string;
  productName: string;
}> = ({ scene, durationFrames, accentColor, productName }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" });
  const fadeOut = interpolate(frame, [durationFrames - 8, durationFrames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const opacity = Math.min(fadeIn, fadeOut);

  const bgVariant: "dark" | "gradient" | "accent" =
    scene.layout === "cta" ? "accent" : scene.layout === "comparison" ? "gradient" : "dark";

  return (
    <AbsoluteFill style={{ opacity }}>
      <Background variant={bgVariant} />
      <TopBar productName={productName} accentColor={accentColor} frame={frame} fps={fps} />

      {scene.layout === "title" && <TitleScene scene={scene} frame={frame} fps={fps} accentColor={accentColor} />}
      {scene.layout === "cursor_ide" && <CursorIDEDemo frame={frame} fps={fps} durationFrames={durationFrames} />}
      {scene.layout === "terminal" && <TerminalDemo frame={frame} fps={fps} />}
      {scene.layout === "dashboard" && <DashboardDemo frame={frame} fps={fps} />}
      {scene.layout === "comparison" && <ComparisonScene scene={scene} frame={frame} fps={fps} accentColor={accentColor} />}
      {scene.layout === "cta" && <CTAScene scene={scene} frame={frame} fps={fps} accentColor={accentColor} productName={productName} />}

      <CaptionBar text={scene.caption} frame={frame} fps={fps} />
    </AbsoluteFill>
  );
};

// ─── Default Scenes ─────────────────────────────────────
const DEFAULT_SCENES: Scene[] = [
  {
    scene_number: 1,
    layout: "title",
    title: "この作業、まだ手動でやってますか?",
    subtitle: "AIエージェントが全自動で実行する時代",
    caption: "AI Agent Camp",
    duration: 4,
  },
  {
    scene_number: 2,
    layout: "cursor_ide",
    caption: "Cursor IDEでAI Agentに一言指示するだけ",
    duration: 8,
  },
  {
    scene_number: 3,
    layout: "terminal",
    caption: "競合分析からLP作成まで全自動",
    duration: 6,
  },
  {
    scene_number: 4,
    layout: "dashboard",
    caption: "リアルタイムで進捗を可視化",
    duration: 6,
  },
  {
    scene_number: 5,
    layout: "comparison",
    caption: "圧倒的な時間短縮を実現",
    duration: 4,
    before_text: "2週間",
    after_text: "1時間",
  },
  {
    scene_number: 6,
    layout: "cta",
    title: "AI Agent Camp で学ぼう",
    caption: "詳しくはプロフィールのリンクから",
    duration: 4,
    cta_text: "今すぐ始める",
    cta_url: "ai-agent.camp",
  },
];

// ─── Main Composition ───────────────────────────────────
export const ScreenExplainer: React.FC<ScreenExplainerProps> = ({
  scenes: propScenes,
  productName = "AI Agent Camp",
  accentColor = COLORS.blue,
}) => {
  const { fps } = useVideoConfig();
  const scenes = propScenes || DEFAULT_SCENES;

  let currentFrame = 0;
  const timeline = scenes.map((scene) => {
    const durationFrames = scene.duration * fps;
    const startFrame = currentFrame;
    currentFrame += durationFrames;
    return { scene, startFrame, durationFrames };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.navy }}>
      {timeline.map(({ scene, startFrame, durationFrames }) => (
        <Sequence key={scene.scene_number} from={startFrame} durationInFrames={durationFrames}>
          <SceneContent scene={scene} durationFrames={durationFrames} accentColor={accentColor} productName={productName} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

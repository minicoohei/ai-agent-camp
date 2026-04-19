import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { SHOWCASE_FONT } from "../../constants";

interface AppUIDemoProps {
  brandName?: string;
}

// ─── Colors ─────────────────────────────────────────────
const C = {
  navy: "#1a365d",
  teal: "#2b6cb0",
  brand500: "#1674EB",
  violet500: "#8b5cf6",
  emerald500: "#10b981",
  amber500: "#f59e0b",
  red500: "#ef4444",
  indigo500: "#6366f1",
  slate50: "#f8fafc", slate100: "#f1f5f9", slate200: "#e2e8f0",
  slate400: "#94a3b8", slate500: "#64748b", slate600: "#475569",
  slate700: "#334155", slate800: "#1e293b", slate900: "#0f172a",
  white: "#ffffff", mainBg: "#f4f6f8",
};

const F = `${SHOWCASE_FONT.primary}, 'Hiragino Sans', 'Noto Sans JP', sans-serif`;
const M = "'JetBrains Mono', 'Fira Code', monospace";

// ─── Data ───────────────────────────────────────────────
const ENV_TOOLS = [
  { name: "macOS 14.6", status: "ok" as const, color: C.slate600 },
  { name: "Claude CLI", status: "ok" as const, color: "#D4A574" },
  { name: "Python 3.12", status: "ok" as const, color: "#3776AB" },
  { name: "Node.js 22", status: "ok" as const, color: "#339933" },
  { name: "Docker", status: "warn" as const, color: "#2496ED" },
  { name: "Git 2.44", status: "ok" as const, color: "#F05032" },
  { name: "GitHub CLI", status: "ok" as const, color: C.slate700 },
  { name: "Java (JDK)", status: "none" as const, color: "#ED8B00" },
];

// ─── AI Agent Camp Logo SVG ─────────────────────────────
const CampLogo: React.FC<{ size?: number; light?: boolean }> = ({ size = 28, light = false }) => {
  const textColor = light ? "rgba(255,255,255,0.9)" : C.navy;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <svg width={size} height={size} viewBox="0 0 40 40" fill="none">
        {/* Tent */}
        <path d="M20 4L6 32h28L20 4z" fill={`url(#tentGrad-${light ? 'l' : 'd'})`} opacity={0.9} />
        <path d="M20 4L14 32h12L20 4z" fill="rgba(255,255,255,0.15)" />
        {/* "Ai" text inside tent */}
        <text x={16} y={24} fontFamily={F} fontSize={10} fontWeight={800} fill="#fff">Ai</text>
        {/* Blue sphere */}
        <circle cx={32} cy={10} r={5} fill={C.teal} />
        <circle cx={30.5} cy={8.5} r={1.5} fill="rgba(255,255,255,0.4)" />
        <defs>
          <linearGradient id={`tentGrad-${light ? 'l' : 'd'}`} x1="6" y1="32" x2="34" y2="4">
            <stop offset="0%" stopColor={C.navy} />
            <stop offset="100%" stopColor={C.teal} />
          </linearGradient>
        </defs>
      </svg>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <span style={{ fontFamily: F, fontSize: size * 0.42, fontWeight: 800, color: textColor, lineHeight: 1.1, letterSpacing: "-0.02em" }}>
          AI AGENT
        </span>
        <span style={{ fontFamily: F, fontSize: size * 0.32, fontWeight: 600, color: textColor, lineHeight: 1.1, letterSpacing: "0.08em", opacity: 0.7 }}>
          CAMP
        </span>
      </div>
    </div>
  );
};

// ─── Window frame helpers ───────────────────────────────
const ElectronBar: React.FC<{ title: string }> = ({ title }) => (
  <div style={{
    background: C.mainBg, padding: "8px 14px",
    display: "flex", alignItems: "center", gap: 7,
    borderBottom: "1px solid #e5e7eb",
  }}>
    {["#FF5F56", "#FFBD2E", "#27C93F"].map((c) => (
      <div key={c} style={{ width: 10, height: 10, borderRadius: "50%", background: c }} />
    ))}
    <span style={{ fontFamily: F, fontSize: 11, color: C.slate500, marginLeft: 8 }}>{title}</span>
  </div>
);

// ─── Main ───────────────────────────────────────────────
export const AppUIDemo: React.FC<AppUIDemoProps> = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // ── Phase timing: setup → chat switch ──
  const midpoint = Math.floor(durationInFrames * 0.5);

  // Global
  const gIn = spring({ frame, fps, config: { damping: 20, mass: 0.8 } });
  const gOut = interpolate(frame, [durationInFrames - 18, durationInFrames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const glowP = Math.sin(frame * 0.08) * 0.5 + 0.5;

  // Phase 1: Setup screen
  const setupE = spring({ frame, fps, config: { damping: 20, mass: 0.7 } });
  const setupOut = interpolate(frame, [midpoint - 20, midpoint + 5], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const setupScale = interpolate(setupE, [0, 1], [0.88, 0.94], { extrapolateRight: "clamp" });

  // Phase 2: Chat screen
  const chatScreenE = spring({ frame: Math.max(0, frame - midpoint), fps, config: { damping: 18, mass: 0.7 } });

  // Setup tool check cascade
  const setupItems = ENV_TOOLS.map((_, i) => spring({
    frame: Math.max(0, frame - 15 - i * 6), fps, config: { damping: 16, mass: 0.3 },
  }));

  // Chat content
  const chatE = spring({ frame: Math.max(0, frame - midpoint - 20), fps, config: { damping: 18, mass: 0.5 } });
  const chatText = "Transformerは「Self-Attention」により、入力テキスト内のすべてのトークンの関係を同時に計算します。従来のRNNが逐次処理だったのに対し、並列処理が可能になったことで学習速度が飛躍的に向上しました。";
  const chatElapsed = Math.max(0, frame - midpoint - 40);
  const chatChars = Math.min(chatText.length, Math.floor(chatElapsed * 1.6));

  return (
    <AbsoluteFill style={{
      backgroundColor: "#000",
      display: "flex", alignItems: "center", justifyContent: "center",
      perspective: 2000, opacity: gIn * gOut,
    }}>
      {/* ══ Phase 1: Setup Screen ══ */}
      <div style={{
        position: "absolute",
        transform: `perspective(2000px) rotateY(-3deg) rotateX(2deg) scale(${setupScale})`,
        transformOrigin: "center center",
      }}>
        <div style={{
          width: 1200, borderRadius: 12, overflow: "hidden",
          boxShadow: "0 20px 80px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.06)",
          opacity: setupE * setupOut,
          transform: `scale(${interpolate(setupE, [0, 1], [0.93, 1])})`,
        }}>
          <ElectronBar title="AI Agent Camp" />
          <div style={{ background: C.mainBg, height: 700, display: "flex", overflow: "hidden" }}>
            {/* Left sidebar */}
            <div style={{
              width: 260, flexShrink: 0, background: C.white,
              borderRight: `1px solid ${C.slate200}`, padding: "16px 14px",
              display: "flex", flexDirection: "column", gap: 16,
            }}>
              <CampLogo size={26} />
              {/* Course list */}
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                <div style={{ fontFamily: F, fontSize: 10, fontWeight: 600, color: C.slate400, textTransform: "uppercase" as const, letterSpacing: "0.05em" }}>COURSES</div>
                {[
                  { name: "Foundation 1: AI Agentの基礎", active: true },
                  { name: "Foundation 2: 実践ワークショップ", active: false },
                ].map((c) => (
                  <div key={c.name} style={{
                    padding: "8px 10px", borderRadius: 8,
                    background: c.active ? `linear-gradient(135deg, ${C.navy}10, ${C.teal}10)` : "transparent",
                    border: c.active ? `1px solid ${C.teal}30` : "1px solid transparent",
                    fontFamily: F, fontSize: 12, fontWeight: c.active ? 600 : 400,
                    color: c.active ? C.navy : C.slate500,
                  }}>
                    {c.name}
                  </div>
                ))}
              </div>
            </div>

            {/* Main: Environment Check */}
            <div style={{ flex: 1, padding: "24px 32px" }}>
              {/* Rainbow header */}
              <div style={{
                height: 4, borderRadius: 2, marginBottom: 20,
                background: "linear-gradient(90deg, #ef4444, #f97316, #eab308, #22c55e, #3b82f6, #8b5cf6, #ec4899)",
              }} />
              <h3 style={{ fontFamily: F, fontSize: 20, fontWeight: 700, color: C.slate800, margin: "0 0 4px" }}>
                開発環境をチェック中...
              </h3>
              <p style={{ fontFamily: F, fontSize: 13, color: C.slate500, margin: "0 0 20px" }}>
                必要なツールがインストールされているか確認します
              </p>
              {/* Tool list */}
              <div style={{ display: "flex", flexDirection: "column", gap: 6, maxWidth: 500 }}>
                {ENV_TOOLS.map((tool, i) => (
                  <div key={tool.name} style={{
                    display: "flex", alignItems: "center", justifyContent: "space-between",
                    padding: "9px 14px", borderRadius: 8, background: C.white,
                    border: `1px solid ${C.slate200}`,
                    opacity: setupItems[i],
                    transform: `translateX(${interpolate(setupItems[i], [0, 1], [-15, 0])}px)`,
                  }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <div style={{ width: 10, height: 10, borderRadius: "50%", background: tool.color }} />
                      <span style={{ fontFamily: F, fontSize: 13, fontWeight: 500, color: C.slate700 }}>{tool.name}</span>
                    </div>
                    <div style={{
                      display: "flex", alignItems: "center", gap: 5,
                      fontFamily: F, fontSize: 11, fontWeight: 600,
                      color: tool.status === "ok" ? C.emerald500 : tool.status === "warn" ? C.amber500 : C.red500,
                    }}>
                      {tool.status === "ok" && <svg width={13} height={13} viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke={C.emerald500} strokeWidth={2.5} strokeLinecap="round" /></svg>}
                      {tool.status === "warn" && <svg width={13} height={13} viewBox="0 0 24 24" fill="none"><path d="M12 9v4M12 17h.01" stroke={C.amber500} strokeWidth={2} strokeLinecap="round" /><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke={C.amber500} strokeWidth={1.5} /></svg>}
                      {tool.status === "none" && <svg width={13} height={13} viewBox="0 0 24 24" fill="none"><circle cx={12} cy={12} r={10} stroke={C.red500} strokeWidth={1.5} /><path d="M15 9l-6 6M9 9l6 6" stroke={C.red500} strokeWidth={1.5} /></svg>}
                      {tool.status === "ok" ? "installed" : tool.status === "warn" ? "outdated" : "not found"}
                    </div>
                  </div>
                ))}
              </div>
              {/* Next button */}
              <div style={{
                marginTop: 18, maxWidth: 500,
                background: `linear-gradient(135deg, ${C.emerald500}, #14b8a6)`,
                borderRadius: 10, padding: "12px 0", textAlign: "center" as const,
                fontFamily: F, fontSize: 14, fontWeight: 700, color: "#fff",
                opacity: setupItems[7],
                boxShadow: `0 0 ${12 + 18 * glowP}px rgba(16,185,129,${0.3 + 0.2 * glowP})`,
              }}>
                次へ進む
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ══ Phase 2: AI Tutor Chat (Full Screen) ══ */}
      {frame > midpoint - 10 && (
        <div style={{
          position: "absolute",
          left: "50%", top: "50%",
          transform: `perspective(2000px) rotateY(-3deg) rotateX(2deg) translate(-50%, -50%) scale(0.95)`,
          transformOrigin: "center center",
        }}>
          <div style={{
            width: 1100, borderRadius: 12, overflow: "hidden",
            boxShadow: "0 25px 100px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.08)",
            opacity: chatScreenE,
            transform: `scale(${interpolate(chatScreenE, [0, 1], [0.9, 1])}) translateX(${interpolate(chatScreenE, [0, 1], [60, 0])}px)`,
          }}>
            <ElectronBar title="AI Agent Camp" />
            <div style={{ background: C.mainBg, height: 680, display: "flex", flexDirection: "column", overflow: "hidden" }}>
              {/* Chat header */}
              <div style={{
                padding: "14px 24px", borderBottom: "1px solid #e5e7eb",
                display: "flex", alignItems: "center", gap: 12,
                opacity: chatE,
              }}>
                <CampLogo size={22} />
                <div style={{ width: 1, height: 20, background: C.slate200 }} />
                <div style={{
                  display: "flex", alignItems: "center", gap: 6,
                }}>
                  <div style={{
                    width: 28, height: 28, borderRadius: 8,
                    background: `linear-gradient(135deg, ${C.indigo500}, #3b82f6)`,
                    display: "flex", alignItems: "center", justifyContent: "center",
                  }}>
                    <span style={{ fontFamily: F, fontSize: 11, fontWeight: 800, color: "#fff" }}>Ai</span>
                  </div>
                  <span style={{ fontFamily: F, fontSize: 15, fontWeight: 600, color: C.slate800 }}>AI Tutor</span>
                  <span style={{
                    fontFamily: F, fontSize: 10, color: C.emerald500,
                    background: "#ecfdf5", padding: "2px 8px", borderRadius: 4, fontWeight: 500,
                  }}>回答中...</span>
                </div>
              </div>

              {/* Chat content */}
              <div style={{ flex: 1, padding: "24px 40px", overflow: "hidden", opacity: chatE }}>
                {/* User message */}
                <div style={{
                  background: `linear-gradient(135deg, ${C.navy}08, ${C.teal}08)`,
                  border: `1px solid ${C.teal}20`,
                  borderRadius: 14, padding: "12px 18px", marginBottom: 20,
                  maxWidth: 500, marginLeft: "auto",
                }}>
                  <div style={{ fontFamily: F, fontSize: 14, color: C.slate700, lineHeight: 1.6 }}>
                    Transformerの並列処理と従来のRNNの違いを教えてください
                  </div>
                </div>
                {/* AI response */}
                <div style={{ display: "flex", gap: 12 }}>
                  <div style={{
                    width: 32, height: 32, borderRadius: 8,
                    background: `linear-gradient(135deg, ${C.indigo500}, #3b82f6)`,
                    display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
                  }}>
                    <span style={{ fontFamily: F, fontSize: 11, fontWeight: 800, color: "#fff" }}>Ai</span>
                  </div>
                  <div style={{
                    fontFamily: F, fontSize: 14, color: C.slate700, lineHeight: 1.8,
                    maxWidth: 700,
                  }}>
                    {chatText.slice(0, chatChars)}
                    {chatChars < chatText.length && (
                      <span style={{
                        display: "inline-block", width: 2, height: 16,
                        background: C.indigo500, marginLeft: 1,
                        opacity: Math.floor(frame / 15) % 2 === 0 ? 1 : 0,
                      }} />
                    )}
                  </div>
                </div>
              </div>

              {/* Input bar */}
              <div style={{
                padding: "14px 24px", borderTop: "1px solid #e5e7eb",
                display: "flex", alignItems: "center", gap: 10, opacity: chatE,
              }}>
                <div style={{
                  flex: 1, borderRadius: 10, border: `1px solid ${C.slate200}`, padding: "10px 16px",
                  fontFamily: F, fontSize: 13, color: C.slate400,
                }}>
                  質問を入力...
                </div>
                <div style={{
                  width: 36, height: 36, borderRadius: 10,
                  background: `linear-gradient(135deg, ${C.indigo500}, ${C.teal})`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                }}>
                  <svg width={16} height={16} viewBox="0 0 24 24" fill="none"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="#fff" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" /></svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Img,
} from "remotion";
import { SHOWCASE_FONT } from "../../constants";

interface Integration {
  name: string;
  logoSrc?: string;
}

interface IntegrationsGridProps {
  title?: string;
  integrations: Integration[];
  useCases?: string[];
  scrollSpeed?: number;
}

const CARD_WIDTH = 150;
const CARD_HEIGHT = 130;
const CARD_GAP = 16;
const ROWS = 2;

// Use case SVG icons
const USE_CASE_ICONS: Record<string, React.ReactNode> = {
  "LP制作を自動化": (
    <svg width={22} height={22} viewBox="0 0 24 24" fill="none">
      <rect x={3} y={3} width={18} height={18} rx={3} stroke="rgba(100,140,255,0.7)" strokeWidth={1.5} />
      <path d="M3 9h18M7 6h2" stroke="rgba(100,140,255,0.5)" strokeWidth={1.5} strokeLinecap="round" />
    </svg>
  ),
  "競合調査をAIで": (
    <svg width={22} height={22} viewBox="0 0 24 24" fill="none">
      <circle cx={10} cy={10} r={7} stroke="rgba(16,185,129,0.7)" strokeWidth={1.5} />
      <path d="M15.5 15.5L21 21" stroke="rgba(16,185,129,0.7)" strokeWidth={1.5} strokeLinecap="round" />
    </svg>
  ),
  "議事録の自動要約": (
    <svg width={22} height={22} viewBox="0 0 24 24" fill="none">
      <rect x={4} y={2} width={16} height={20} rx={2} stroke="rgba(139,92,246,0.7)" strokeWidth={1.5} />
      <path d="M8 7h8M8 11h8M8 15h5" stroke="rgba(139,92,246,0.5)" strokeWidth={1.5} strokeLinecap="round" />
    </svg>
  ),
  "請求書の自動仕訳": (
    <svg width={22} height={22} viewBox="0 0 24 24" fill="none">
      <path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" stroke="rgba(245,158,11,0.7)" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  ),
  "Slack Bot構築": (
    <svg width={22} height={22} viewBox="0 0 24 24" fill="none">
      <rect x={3} y={11} width={18} height={10} rx={2} stroke="rgba(236,72,153,0.7)" strokeWidth={1.5} />
      <path d="M8 11V7a4 4 0 018 0v4" stroke="rgba(236,72,153,0.5)" strokeWidth={1.5} />
      <circle cx={9} cy={16} r={1} fill="rgba(236,72,153,0.7)" />
      <circle cx={15} cy={16} r={1} fill="rgba(236,72,153,0.7)" />
    </svg>
  ),
  "データ分析レポート": (
    <svg width={22} height={22} viewBox="0 0 24 24" fill="none">
      <path d="M18 20V10M12 20V4M6 20v-6" stroke="rgba(59,130,246,0.7)" strokeWidth={2} strokeLinecap="round" />
    </svg>
  ),
};

// Recognizable SVG icons for common integrations
const INTEGRATION_ICONS: Record<string, React.ReactNode> = {
  Cursor: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <path d="M5 3l14 9-6 2-3 7z" fill="rgba(255,255,255,0.7)" />
    </svg>
  ),
  Claude: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <circle cx={12} cy={12} r={9} stroke="#D4A574" strokeWidth={2} />
      <path d="M9 9c0-1.5 1.3-3 3-3s3 1.5 3 3" stroke="#D4A574" strokeWidth={2} strokeLinecap="round" />
    </svg>
  ),
  Notion: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <rect x={4} y={3} width={16} height={18} rx={2} stroke="rgba(255,255,255,0.7)" strokeWidth={1.5} />
      <path d="M8 8h4M8 12h8M8 16h6" stroke="rgba(255,255,255,0.5)" strokeWidth={1.5} strokeLinecap="round" />
    </svg>
  ),
  Slack: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <path d="M14.5 10c-.83 0-1.5-.67-1.5-1.5v-5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5v5c0 .83-.67 1.5-1.5 1.5z" fill="#E01E5A" />
      <path d="M20.5 10H19v-1.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z" fill="#E01E5A" />
      <path d="M9.5 14c.83 0 1.5.67 1.5 1.5v5c0 .83-.67 1.5-1.5 1.5S8 21.33 8 20.5v-5c0-.83.67-1.5 1.5-1.5z" fill="#2EB67D" />
      <path d="M3.5 14H5v1.5c0 .83-.67 1.5-1.5 1.5S2 16.33 2 15.5 2.67 14 3.5 14z" fill="#2EB67D" />
      <path d="M14 14.5c0-.83.67-1.5 1.5-1.5h5c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5h-5c-.83 0-1.5-.67-1.5-1.5z" fill="#ECB22E" />
      <path d="M14 20.5v-1.5h1.5c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5-1.5-.67-1.5-1.5z" fill="#ECB22E" />
      <path d="M10 9.5c0 .83-.67 1.5-1.5 1.5h-5C2.67 11 2 10.33 2 9.5S2.67 8 3.5 8h5c.83 0 1.5.67 1.5 1.5z" fill="#36C5F0" />
      <path d="M10 3.5V5H8.5C7.67 5 7 4.33 7 3.5S7.67 2 8.5 2s1.5.67 1.5 1.5z" fill="#36C5F0" />
    </svg>
  ),
  "Google Apps Script": (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <path d="M4 6h16M4 10h16M4 14h12M4 18h8" stroke="#4285F4" strokeWidth={2} strokeLinecap="round" />
    </svg>
  ),
  BigQuery: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <rect x={4} y={4} width={16} height={16} rx={2} stroke="#4285F4" strokeWidth={1.5} />
      <rect x={7} y={12} width={3} height={5} fill="#4285F4" opacity={0.7} />
      <rect x={11} y={9} width={3} height={8} fill="#4285F4" opacity={0.85} />
      <rect x={15} y={6} width={3} height={11} fill="#4285F4" />
    </svg>
  ),
  "GitHub Actions": (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <circle cx={12} cy={12} r={10} stroke="rgba(255,255,255,0.7)" strokeWidth={1.5} />
      <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke="rgba(255,255,255,0.7)" strokeWidth={1.5} strokeLinecap="round" />
      <circle cx={9} cy={10} r={1} fill="rgba(255,255,255,0.7)" />
      <circle cx={15} cy={10} r={1} fill="rgba(255,255,255,0.7)" />
    </svg>
  ),
  Vercel: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <path d="M12 3L22 20H2z" fill="rgba(255,255,255,0.7)" />
    </svg>
  ),
  GA4: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <path d="M20 20V10M14 20V6M8 20v-6" stroke="#F9AB00" strokeWidth={2.5} strokeLinecap="round" />
    </svg>
  ),
  Remotion: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <rect x={3} y={3} width={18} height={18} rx={3} stroke="#0B84F3" strokeWidth={1.5} />
      <path d="M10 8l6 4-6 4z" fill="#0B84F3" />
    </svg>
  ),
  Figma: (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <circle cx={15} cy={12} r={3} stroke="#A259FF" strokeWidth={1.5} />
      <path d="M12 3H9a3 3 0 0 0 0 6h3V3z" stroke="#F24E1E" strokeWidth={1.5} />
      <path d="M12 9H9a3 3 0 0 0 0 6h3V9z" stroke="#FF7262" strokeWidth={1.5} />
      <path d="M12 15H9a3 3 0 0 0 0 6 3 3 0 0 0 3-3v-3z" stroke="#0ACF83" strokeWidth={1.5} />
      <path d="M12 3h3a3 3 0 0 1 0 6h-3V3z" stroke="#1ABCFE" strokeWidth={1.5} />
    </svg>
  ),
  "LINE Bot": (
    <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
      <path d="M12 2C6.48 2 2 5.58 2 10c0 3.54 3.14 6.54 7.36 7.56.28.06.68.18.78.42.1.22.06.56.03.78l-.13.78c-.04.22-.16.86.76.47s5.04-2.96 6.88-5.08C19.78 12.74 22 11.5 22 10c0-4.42-4.48-8-10-8z" fill="#06C755" />
    </svg>
  ),
};

// ─── Use Case Card ──────────────────────────────────────
const UseCaseCard: React.FC<{
  text: string;
  index: number;
}> = ({ text, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: Math.max(0, frame - 15 - index * 6),
    fps,
    config: { damping: 16, mass: 0.4, stiffness: 120 },
  });

  const icon = USE_CASE_ICONS[text];

  return (
    <div
      style={{
        width: 260,
        borderRadius: 12,
        background: "rgba(255,255,255,0.04)",
        border: "1px solid rgba(255,255,255,0.08)",
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "14px 18px",
        opacity: entrance,
        transform: `translateY(${interpolate(entrance, [0, 1], [15, 0], { extrapolateRight: "clamp" })}px)`,
      }}
    >
      {icon && <div style={{ flexShrink: 0 }}>{icon}</div>}
      <span
        style={{
          fontFamily: SHOWCASE_FONT.primary,
          fontSize: 14,
          fontWeight: 500,
          color: "rgba(255,255,255,0.75)",
          whiteSpace: "nowrap",
        }}
      >
        {text}
      </span>
    </div>
  );
};

// ─── Integration Card ───────────────────────────────────
const IntegrationCard: React.FC<{
  integration: Integration;
  index: number;
}> = ({ integration, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: Math.max(0, frame - 20 - index * 2),
    fps,
    config: { damping: 20, mass: 0.5 },
  });

  const iconSvg = INTEGRATION_ICONS[integration.name];

  return (
    <div
      style={{
        width: CARD_WIDTH,
        height: CARD_HEIGHT,
        borderRadius: 14,
        background: "rgba(255,255,255,0.04)",
        border: "1px solid rgba(255,255,255,0.08)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 12,
        flexShrink: 0,
        opacity: entrance,
      }}
    >
      <div
        style={{
          width: 48, height: 48, borderRadius: 10,
          background: "rgba(255,255,255,0.06)",
          display: "flex", alignItems: "center", justifyContent: "center",
          overflow: "hidden",
        }}
      >
        {integration.logoSrc ? (
          <Img
            src={staticFile(integration.logoSrc)}
            style={{ width: 36, height: 36, objectFit: "contain" }}
          />
        ) : iconSvg ? (
          iconSvg
        ) : (
          <svg width={28} height={28} viewBox="0 0 24 24" fill="none">
            <rect x={3} y={3} width={18} height={18} rx={4} stroke="rgba(255,255,255,0.3)" strokeWidth={1.5} />
            <path d="M8 12h8M12 8v8" stroke="rgba(255,255,255,0.3)" strokeWidth={1.5} strokeLinecap="round" />
          </svg>
        )}
      </div>
      <span
        style={{
          fontFamily: SHOWCASE_FONT.primary, fontSize: 13, fontWeight: 500,
          color: "rgba(255,255,255,0.6)", textAlign: "center",
        }}
      >
        {integration.name}
      </span>
    </div>
  );
};

// ─── Main ───────────────────────────────────────────────
export const IntegrationsGrid: React.FC<IntegrationsGridProps> = ({
  title = "Plugs into everything",
  integrations,
  useCases = [],
  scrollSpeed = 2.4,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Title entrance
  const titleEntrance = spring({
    frame,
    fps,
    config: { damping: 18, mass: 0.5 },
  });

  // Split integrations into rows
  const perRow = Math.ceil(integrations.length / ROWS);
  const row1 = integrations.slice(0, perRow);
  const row2 = integrations.slice(perRow);

  // Duplicate for seamless loop
  const row1Loop = [...row1, ...row1, ...row1];
  const row2Loop = [...row2, ...row2, ...row2];

  const rowWidth = perRow * (CARD_WIDTH + CARD_GAP);
  const scrollOffset1 = (frame * scrollSpeed) % rowWidth;
  const scrollOffset2 = (frame * scrollSpeed * 0.8) % rowWidth;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      {/* Title */}
      <div
        style={{
          fontSize: 40,
          fontWeight: 600,
          fontFamily: SHOWCASE_FONT.primary,
          color: "#FFFFFF",
          marginBottom: useCases.length > 0 ? 30 : 50,
          opacity: titleEntrance,
          transform: `translateY(${interpolate(titleEntrance, [0, 1], [20, 0])}px)`,
          letterSpacing: "-0.02em",
        }}
      >
        {title}
      </div>

      {/* Use Cases Grid (2×3) */}
      {useCases.length > 0 && (
        <div style={{
          display: "flex", flexWrap: "wrap", gap: 12,
          justifyContent: "center", maxWidth: 860,
          marginBottom: 36,
        }}>
          {useCases.map((uc, i) => (
            <UseCaseCard key={`uc-${i}`} text={uc} index={i} />
          ))}
        </div>
      )}

      {/* Subtle divider */}
      {useCases.length > 0 && (
        <div style={{
          width: 200, height: 1, marginBottom: 24,
          background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)",
        }} />
      )}

      {/* Row 1 - scrolls left */}
      <div style={{ width: "100%", overflow: "hidden", marginBottom: CARD_GAP }}>
        <div
          style={{
            display: "flex", gap: CARD_GAP,
            transform: `translateX(-${scrollOffset1}px)`,
            willChange: "transform",
          }}
        >
          {row1Loop.map((item, i) => (
            <IntegrationCard key={`r1-${i}`} integration={item} index={i % perRow} />
          ))}
        </div>
      </div>

      {/* Row 2 - scrolls left (slightly slower) */}
      <div style={{ width: "100%", overflow: "hidden" }}>
        <div
          style={{
            display: "flex", gap: CARD_GAP,
            transform: `translateX(-${scrollOffset2}px)`,
            willChange: "transform",
          }}
        >
          {row2Loop.map((item, i) => (
            <IntegrationCard key={`r2-${i}`} integration={item} index={i % (integrations.length - perRow)} />
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

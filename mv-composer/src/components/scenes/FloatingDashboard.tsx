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
interface DashboardCard {
  id: string;
  title: string;
  type: "team" | "live" | "progress" | "stats" | "activity" | "custom";
  data?: Record<string, any>;
  position: { x: number; y: number };
  size: { width: number; height: number };
  delay?: number; // entrance delay in frames
}

interface StatsItem {
  label: string;
  value: string;
  change?: string;
}

interface FloatingDashboardProps {
  cards: DashboardCard[];
  statsRow?: StatsItem[];
  teamName?: string;
  teamRoles?: string[];
  progressPercent?: number;
  arrValue?: string;
  arrLabel?: string;
  activities?: string[];
}

// ─── Dot Matrix Progress ────────────────────────────────
const DotMatrixProgress: React.FC<{ percent: number }> = ({ percent }) => {
  const frame = useCurrentFrame();
  const cols = 25;
  const rows = 3;
  const total = cols * rows;
  const filled = Math.floor((percent / 100) * total);

  // Animate fill progression
  const animFilled = Math.min(
    filled,
    Math.floor(interpolate(frame, [0, 40], [0, filled], { extrapolateRight: "clamp" }))
  );

  // Glow intensity when near complete
  const completionRatio = animFilled / total;
  const glowIntensity = interpolate(completionRatio, [0.7, 1], [0, 0.6], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      gap: 3,
      boxShadow: `0 0 ${30 * glowIntensity}px ${10 * glowIntensity}px rgba(16,185,129,${glowIntensity * 0.4})`,
      borderRadius: 6,
      padding: 2,
    }}>
      {Array.from({ length: rows }).map((_, row) => (
        <div key={row} style={{ display: "flex", gap: 3 }}>
          {Array.from({ length: cols }).map((_, col) => {
            const idx = row * cols + col;
            const isFilled = idx < animFilled;
            return (
              <div
                key={col}
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: 2,
                  backgroundColor: isFilled ? "#10B981" : "rgba(255,255,255,0.08)",
                  boxShadow: isFilled
                    ? `0 0 6px rgba(16,185,129,0.5), 0 0 ${12 * glowIntensity}px rgba(16,185,129,${0.3 * glowIntensity})`
                    : "none",
                }}
              />
            );
          })}
        </div>
      ))}
    </div>
  );
};

// ─── Card Renderers ─────────────────────────────────────
const TeamCard: React.FC<{ teamName?: string; roles?: string[] }> = ({
  teamName = "My Team",
  roles = ["BSG", "SDR", "MRA", "Engineer"],
}) => (
  <div style={{ padding: 20 }}>
    <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
      <span style={{ fontSize: 22, fontWeight: 600, color: "#FFF", fontFamily: SHOWCASE_FONT.primary }}>
        {teamName}
      </span>
      <div
        style={{
          display: "flex",
          gap: 2,
          background: "rgba(255,255,255,0.06)",
          borderRadius: 8,
          padding: "4px 6px",
        }}
      >
        {roles.map((role) => (
          <span
            key={role}
            style={{
              fontSize: 12,
              fontWeight: 500,
              color: "rgba(255,255,255,0.6)",
              padding: "4px 10px",
              borderRadius: 5,
              background: "rgba(255,255,255,0.05)",
              fontFamily: SHOWCASE_FONT.primary,
            }}
          >
            {role}
          </span>
        ))}
      </div>
    </div>
  </div>
);

const LiveDashCard: React.FC<{ arrValue?: string; arrLabel?: string; activities?: string[] }> = ({
  arrValue = "$3.7M",
  arrLabel = "ARR",
  activities = [],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Count up ARR
  const countProgress = spring({ frame, fps, config: { damping: 20, mass: 1 } });
  let displayVal: string;
  const arrMatch = arrValue.match(/^([^0-9]*)([0-9,.]+)(.*)$/);
  if (arrMatch) {
    const prefix = arrMatch[1];
    const numVal = parseFloat(arrMatch[2].replace(/,/g, ""));
    const suffix = arrMatch[3];
    const animated = Math.round(numVal * countProgress);
    displayVal = `${prefix}${animated.toLocaleString()}${suffix}`;
  } else {
    displayVal = arrValue;
  }

  return (
    <div style={{ padding: 16 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
        <span style={{ fontSize: 16, fontWeight: 600, color: "#FFF", fontFamily: SHOWCASE_FONT.primary }}>
          {arrLabel}
        </span>
        <span style={{ fontSize: 20, fontWeight: 700, color: "#10B981", fontFamily: SHOWCASE_FONT.primary }}>
          {displayVal}
        </span>
      </div>
      {/* Mini chart line */}
      <svg width="100%" height={50} viewBox="0 0 300 50">
        <path
          d="M0 45 Q50 40 80 35 T150 20 T220 15 T300 5"
          fill="none"
          stroke="rgba(255,255,255,0.3)"
          strokeWidth={2}
        />
      </svg>
      {/* Activity feed — hidden when empty */}
      {activities.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <div style={{ fontSize: 12, fontWeight: 600, color: "rgba(255,255,255,0.5)", marginBottom: 8, fontFamily: SHOWCASE_FONT.primary }}>
            ACTIVITY
          </div>
          {activities.slice(0, 4).map((a, i) => (
            <div
              key={i}
              style={{
                fontSize: 11,
                color: "rgba(255,255,255,0.45)",
                padding: "4px 0",
                borderTop: i > 0 ? "1px solid rgba(255,255,255,0.04)" : "none",
                fontFamily: SHOWCASE_FONT.primary,
              }}
            >
              {a}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const ProgressCard: React.FC<{ percent?: number }> = ({ percent = 45 }) => (
  <div style={{ padding: 20, display: "flex", alignItems: "center", gap: 16 }}>
    <DotMatrixProgress percent={percent} />
    <span style={{ fontSize: 28, fontWeight: 700, color: "#FFF", fontFamily: SHOWCASE_FONT.primary }}>
      {percent}%
    </span>
  </div>
);

const StatsRowCard: React.FC<{ stats: StatsItem[] }> = ({ stats }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ padding: 16, display: "flex", gap: 24 }}>
      {stats.map((stat, i) => {
        const countProgress = spring({
          frame: Math.max(0, frame - i * 5),
          fps,
          config: { damping: 20, mass: 1 },
        });
        let displayVal: string;
        const match = stat.value.match(/^([^0-9]*)([0-9,.]+)(.*)$/);
        if (match) {
          const prefix = match[1];
          const numVal = parseFloat(match[2].replace(/,/g, ""));
          const suffix = match[3];
          const animated = Math.round(numVal * countProgress);
          displayVal = `${prefix}${animated.toLocaleString()}${suffix}`;
        } else {
          displayVal = stat.value;
        }

        return (
          <div key={i} style={{ textAlign: "center" }}>
            <div style={{ fontSize: 18, fontWeight: 700, color: "#FFF", fontFamily: SHOWCASE_FONT.primary }}>
              {displayVal}
            </div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.4)", marginTop: 4, fontFamily: SHOWCASE_FONT.primary }}>
              {stat.label}
            </div>
            {stat.change && (
              <div style={{ fontSize: 10, color: "#10B981", marginTop: 2, fontFamily: SHOWCASE_FONT.primary }}>
                {stat.change}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

const CustomCard: React.FC<{ title: string; data?: Record<string, any> }> = ({ title, data }) => (
  <div style={{ padding: 20 }}>
    <div style={{ fontSize: 16, fontWeight: 700, color: "#FFF", marginBottom: 8, fontFamily: SHOWCASE_FONT.primary }}>
      {title}
    </div>
    {data?.lines && (data.lines as string[]).map((line: string, i: number) => (
      <div
        key={i}
        style={{
          fontSize: 13,
          color: "rgba(255,255,255,0.5)",
          padding: "3px 0",
          fontFamily: SHOWCASE_FONT.primary,
        }}
      >
        {line}
      </div>
    ))}
  </div>
);

// ─── Main Component ─────────────────────────────────────
export const FloatingDashboard: React.FC<FloatingDashboardProps> = ({
  cards,
  statsRow,
  teamName,
  teamRoles,
  progressPercent,
  arrValue,
  arrLabel,
  activities,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Camera rig: zoom and pan through dashboard
  const camScale = interpolate(
    frame,
    [0, 120, 300, 480, durationInFrames],
    [0.55, 0.85, 0.95, 0.85, 0.6],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const camX = interpolate(
    frame,
    [0, 120, 300, 480, durationInFrames],
    [0, 60, -80, 40, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const camY = interpolate(
    frame,
    [0, 120, 300, 480, durationInFrames],
    [0, -100, -40, 80, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
        perspective: 1200,
      }}
    >
      {/* Subtle background glow */}
      <div
        style={{
          position: "absolute",
          top: "30%",
          left: "40%",
          width: 600,
          height: 400,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 70%)",
          filter: "blur(60px)",
        }}
      />

      {/* Camera rig container */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `scale(${camScale}) translate(${camX}px, ${camY}px)`,
          transformOrigin: "center center",
        }}
      >
      {cards.map((card, index) => {
        const delay = card.delay ?? index * 8;
        const entrance = spring({
          frame: Math.max(0, frame - delay),
          fps,
          config: { damping: 16, mass: 0.6, stiffness: 90 },
        });

        // Floating drift
        const floatY = Math.sin(frame * 0.015 + index * 1.8) * 4;
        const floatX = Math.cos(frame * 0.012 + index * 2.1) * 3;

        // 3D perspective
        const rotateY = Math.sin(frame * 0.008 + index * 0.7) * 1.5;
        const rotateX = Math.cos(frame * 0.01 + index * 0.9) * 1;

        // Entrance direction
        const enterX = card.position.x > 960 ? 120 : -120;
        const enterY = card.position.y > 540 ? 80 : -80;

        const translateX = interpolate(entrance, [0, 1], [enterX, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) + floatX;
        const translateY = interpolate(entrance, [0, 1], [enterY, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) + floatY;

        return (
          <div
            key={card.id}
            style={{
              position: "absolute",
              left: card.position.x - card.size.width / 2,
              top: card.position.y - card.size.height / 2,
              width: card.size.width,
              height: card.size.height,
              borderRadius: 16,
              background: "rgba(18,18,30,0.75)",
              border: "1px solid rgba(255,255,255,0.08)",
              boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
              overflow: "hidden",
              opacity: entrance,
              transform: `translate(${translateX}px, ${translateY}px) rotateY(${rotateY}deg) rotateX(${rotateX}deg)`,
              transformStyle: "preserve-3d",
            }}
          >
            {card.type === "team" && <TeamCard teamName={teamName} roles={teamRoles} />}
            {card.type === "live" && <LiveDashCard arrValue={arrValue} arrLabel={arrLabel} activities={activities} />}
            {card.type === "progress" && <ProgressCard percent={progressPercent} />}
            {card.type === "stats" && statsRow && <StatsRowCard stats={statsRow} />}
            {(card.type === "custom" || card.type === "activity") && (
              <CustomCard title={card.title} data={card.data} />
            )}
          </div>
        );
      })}
      </div>{/* end camera rig */}
    </AbsoluteFill>
  );
};

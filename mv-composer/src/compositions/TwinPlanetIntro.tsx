import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { TP_COLORS, TP_FONT } from "../constants";

// ─── Types ──────────────────────────────────────────────

interface TalentInfo {
  name: string;
  imageSrc: string;
}

export interface TwinPlanetIntroProps {
  logoSrc?: string;
  slogan?: string;
  pillars?: { title: string; subtitle: string; imageSrc: string }[];
  mainTalent?: TalentInfo[];
  talentGridImages?: string[];
  leadersImage?: string;
  achievements?: string[];
  panDoroboImages?: string[];
  visitorCount?: number;
  bgmSrc?: string;
  sectionDurations?: number[];
}

// ─── Default Props ──────────────────────────────────────

const MAIN_TALENT: TalentInfo[] = [
  { name: "杉浦太陽", imageSrc: "tp/talent_main/01_sugiura.jpg" },
  { name: "ミチ・よしあき", imageSrc: "tp/talent_main/02_michi.jpg" },
  { name: "矢吹奈子", imageSrc: "tp/talent_main/03_yabuki.jpg" },
  { name: "伊藤歩", imageSrc: "tp/talent_main/04_ito.jpg" },
  { name: "ハ・ヨンス", imageSrc: "tp/talent_main/05_ha.jpg" },
  { name: "東村芽依", imageSrc: "tp/talent_main/06_higashimura.png" },
];

const TALENT_GRID = Array.from({ length: 22 }, (_, i) => {
  const num = String(i + 1).padStart(2, "0");
  const ext = i === 19 || i === 20 ? "jpeg" : i === 21 ? "png" : "jpg";
  return `tp/talent_grid/${num}.${ext}`;
});

const PANDOROBO_IMAGES = Array.from({ length: 9 }, (_, i) => {
  const num = String(i + 1).padStart(2, "0");
  return `tp/pandorobo/${num}.jpg`;
}).concat(["tp/pandorobo/10.png"]);

export const DEFAULT_PROPS: TwinPlanetIntroProps = {
  logoSrc: "tp/logo/logo_black.png",
  slogan: "世の中に、次の空気を。",
  pillars: [
    { title: "Management Agency", subtitle: "TALENT", imageSrc: "tp/pillars/management.png" },
    { title: "Marketing Company", subtitle: "EVENT・PR・SNS", imageSrc: "tp/pillars/marketing.png" },
    { title: "IP Production", subtitle: "CHARACTER", imageSrc: "tp/pillars/ip_production.png" },
  ],
  mainTalent: MAIN_TALENT,
  talentGridImages: TALENT_GRID,
  leadersImage: "tp/pillars/management.png",
  achievements: [
    "結成10周年",
    "紅白出場",
    "ワールドツアー敢行",
    "コーチェラ出場",
    "ハリウッド映画主題歌",
  ],
  panDoroboImages: PANDOROBO_IMAGES,
  visitorCount: 30000,
  bgmSrc: "tp/audio/bgm.mp3",
  sectionDurations: [2, 3, 5, 10, 8, 7, 4.5], // seconds per scene (ending trimmed 0.5s)
};

// ─── Scene 01: Logo Opening ─────────────────────────────

const LogoOpening: React.FC<{ logoSrc: string }> = ({ logoSrc }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scaleProgress = spring({ frame, fps, config: { damping: 14, mass: 0.8, stiffness: 100 } });
  const entryScale = interpolate(scaleProgress, [0, 1], [0.6, 1]);
  const opacity = interpolate(scaleProgress, [0, 1], [0, 1]);

  // Breathing pulse after landing
  const breathe = Math.sin(frame * 0.08) * 0.015;
  const scale = entryScale + (scaleProgress > 0.9 ? breathe : 0);

  // Flash on entry
  const flashOpacity = interpolate(frame, [0, 3, 8], [1, 0.9, 0], {
    extrapolateRight: "clamp",
  });

  // Accent line pulsing width
  const lineBase = interpolate(scaleProgress, [0, 1], [0, 60]);
  const linePulse = scaleProgress > 0.9 ? Math.sin(frame * 0.12) * 3 : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: TP_COLORS.white, display: "flex", alignItems: "center", justifyContent: "center" }}>
      {/* Neon yellow accent line */}
      <div
        style={{
          position: "absolute",
          bottom: "15%",
          width: (lineBase + linePulse) + "%",
          height: 4,
          backgroundColor: TP_COLORS.neonYellow,
        }}
      />
      <Img
        src={staticFile(logoSrc)}
        style={{
          width: "50%",
          objectFit: "contain",
          transform: `scale(${scale})`,
          opacity,
        }}
      />
      {/* Entry flash */}
      <AbsoluteFill
        style={{
          backgroundColor: TP_COLORS.neonYellow,
          opacity: flashOpacity,
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};

// ─── Scene 02: Vision Statement ─────────────────────────

const VisionStatement: React.FC<{ slogan: string }> = ({ slogan }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const chars = [...slogan];
  const CHAR_INTERVAL = 4;

  // After text is done, whole block drifts up gently
  const textDoneFrame = chars.length * CHAR_INTERVAL + 15;
  const driftY = frame > textDoneFrame
    ? interpolate(frame, [textDoneFrame, textDoneFrame + 60], [0, -8], { extrapolateRight: "clamp" })
    : 0;
  const driftScale = frame > textDoneFrame
    ? 1 + interpolate(frame, [textDoneFrame, textDoneFrame + 60], [0, 0.02], { extrapolateRight: "clamp" })
    : 1;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: TP_COLORS.white,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transform: `translateY(${driftY}px) scale(${driftScale})`,
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          maxWidth: "80%",
        }}
      >
        {chars.map((char, i) => {
          const startFrame = i * CHAR_INTERVAL;
          const progress = spring({
            frame: Math.max(0, frame - startFrame),
            fps,
            config: { damping: 20, mass: 0.5, stiffness: 110 },
          });
          const opacity = interpolate(progress, [0, 1], [0, 1]);
          const translateY = interpolate(progress, [0, 1], [30, 0]);

          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                fontSize: 72,
                fontWeight: 900,
                fontFamily: TP_FONT.primary,
                color: TP_COLORS.darkGray,
                opacity,
                transform: `translateY(${translateY}px)`,
                letterSpacing: "0.05em",
              }}
            >
              {char}
            </span>
          );
        })}
      </div>
      {/* Subtle accent bar */}
      <div
        style={{
          position: "absolute",
          bottom: "20%",
          width: 80,
          height: 4,
          backgroundColor: TP_COLORS.neonYellow,
          opacity: interpolate(frame, [chars.length * CHAR_INTERVAL, chars.length * CHAR_INTERVAL + 15], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      />
    </AbsoluteFill>
  );
};

// ─── Scene 03: Three Pillars ────────────────────────────

const ThreePillars: React.FC<{
  pillars: { title: string; subtitle: string; imageSrc: string }[];
}> = ({ pillars }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const STAGGER = 30; // 1s = 2 beats at 120BPM

  return (
    <AbsoluteFill style={{ backgroundColor: TP_COLORS.white, display: "flex" }}>
      {pillars.map((pillar, i) => {
        const delay = i * STAGGER;
        const progress = spring({
          frame: Math.max(0, frame - delay),
          fps,
          config: { damping: 16, mass: 0.7, stiffness: 90 },
        });

        const clipX = interpolate(progress, [0, 1], [100, 0]);
        const textOpacity = interpolate(frame, [delay + 20, delay + 35], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });

        return (
          <div
            key={i}
            style={{
              flex: 1,
              position: "relative",
              overflow: "hidden",
              clipPath: `inset(0 ${clipX}% 0 0)`,
            }}
          >
            <Img
              src={staticFile(pillar.imageSrc)}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                // Slow Ken Burns zoom after entrance
                transform: `scale(${1 + interpolate(Math.max(0, frame - delay - 30), [0, 120], [0, 0.08], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})`,
              }}
            />
            {/* Overlay */}
            <div
              style={{
                position: "absolute",
                inset: 0,
                background: "linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 60%)",
              }}
            />
            {/* Text */}
            <div
              style={{
                position: "absolute",
                bottom: 60,
                left: 0,
                right: 0,
                textAlign: "center",
                opacity: textOpacity,
              }}
            >
              <div
                style={{
                  fontSize: 42,
                  fontWeight: 900,
                  fontFamily: TP_FONT.primary,
                  color: TP_COLORS.white,
                  letterSpacing: "0.06em",
                  textTransform: "uppercase",
                  textShadow: "0 2px 12px rgba(0,0,0,0.6)",
                }}
              >
                {pillar.title}
              </div>
              <div
                style={{
                  fontSize: 24,
                  fontWeight: 700,
                  fontFamily: TP_FONT.primary,
                  color: TP_COLORS.neonYellow,
                  marginTop: 12,
                  letterSpacing: "0.12em",
                  textShadow: "0 1px 6px rgba(0,0,0,0.4)",
                }}
              >
                {pillar.subtitle}
              </div>
            </div>
            {/* Separator line */}
            {i < pillars.length - 1 && (
              <div
                style={{
                  position: "absolute",
                  right: 0,
                  top: 0,
                  bottom: 0,
                  width: 2,
                  backgroundColor: TP_COLORS.neonYellow,
                  opacity: 0.6,
                }}
              />
            )}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ─── Scene 04: Talent Showcase (Main 6) ─────────────────

const TalentShowcase: React.FC<{ talent: TalentInfo[] }> = ({ talent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const FRAMES_PER_TALENT = 45; // 1.5s at 30fps
  const effects: Array<"parallax" | "zoom_drift"> = ["parallax", "zoom_drift", "parallax", "zoom_drift", "parallax", "zoom_drift"];

  const currentIndex = Math.min(Math.floor(frame / FRAMES_PER_TALENT), talent.length - 1);
  const localFrame = frame - currentIndex * FRAMES_PER_TALENT;

  const current = talent[currentIndex];
  const effect = effects[currentIndex % effects.length];

  // Ken Burns style movement
  const progress = localFrame / FRAMES_PER_TALENT;
  const scale = effect === "zoom_drift"
    ? interpolate(progress, [0, 1], [1.0, 1.08])
    : 1.05;
  const translateX = effect === "parallax"
    ? interpolate(progress, [0, 1], [10, -10])
    : interpolate(progress, [0, 1], [0, -12]);
  const translateY = effect === "parallax"
    ? interpolate(progress, [0, 1], [5, -5])
    : 0;

  // Fade in/out
  const imgOpacity = interpolate(localFrame, [0, 8, FRAMES_PER_TALENT - 5, FRAMES_PER_TALENT], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Name telop slide in
  const nameProgress = spring({
    frame: Math.max(0, localFrame - 10),
    fps,
    config: { damping: 18, mass: 0.5, stiffness: 100 },
  });
  const nameX = interpolate(nameProgress, [0, 1], [100, 0]);
  const nameOpacity = interpolate(nameProgress, [0, 1], [0, 1]);

  return (
    <AbsoluteFill style={{ backgroundColor: TP_COLORS.lightGray }}>
      {/* Two-column layout: portrait photo left, name right */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          opacity: imgOpacity,
        }}
      >
        {/* Portrait photo area — contain ensures full face visible */}
        <div
          style={{
            width: "55%",
            height: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            overflow: "hidden",
            backgroundColor: TP_COLORS.white,
          }}
        >
          <Img
            src={staticFile(current.imageSrc)}
            style={{
              maxWidth: "90%",
              maxHeight: "92%",
              objectFit: "contain",
              transform: `scale(${scale}) translate(${translateX * 0.5}px, ${translateY * 0.3}px)`,
            }}
          />
        </div>

        {/* Right side: name + label */}
        <div
          style={{
            width: "45%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            paddingLeft: 60,
            paddingRight: 60,
            backgroundColor: TP_COLORS.darkGray,
          }}
        >
          {/* Scene label */}
          <div
            style={{
              fontSize: 16,
              fontWeight: 700,
              fontFamily: TP_FONT.primary,
              color: TP_COLORS.neonYellow,
              letterSpacing: "0.2em",
              marginBottom: 24,
              opacity: 0.9,
            }}
          >
            TWIN PLANET
          </div>

          {/* Yellow accent line */}
          <div
            style={{
              width: 60,
              height: 4,
              backgroundColor: TP_COLORS.neonYellow,
              marginBottom: 28,
              opacity: nameOpacity,
            }}
          />

          {/* Name */}
          <div
            style={{
              fontSize: 52,
              fontWeight: 900,
              fontFamily: TP_FONT.primary,
              color: TP_COLORS.white,
              opacity: nameOpacity,
              transform: `translateX(${nameX * 0.5}px)`,
              lineHeight: 1.2,
            }}
          >
            {current.name}
          </div>

        </div>
      </AbsoluteFill>

      {/* Color tint overlay */}
      <AbsoluteFill style={{ backgroundColor: TP_COLORS.overlayTint, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};

// ─── Scene 05: Talent Grid + Leaders Highlight ──────────

const TalentGridAndLeaders: React.FC<{
  gridImages: string[];
  leadersImage: string;
  achievements: string[];
}> = ({ gridImages, leadersImage, achievements }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const halfDuration = Math.floor(durationInFrames / 2);
  const isLeadersPhase = frame >= halfDuration;

  if (isLeadersPhase) {
    // Phase 2: Leaders focus + achievements
    const localFrame = frame - halfDuration;

    const imgProgress = spring({
      frame: localFrame,
      fps,
      config: { damping: 14, mass: 0.8 },
    });

    // Continuous slow zoom instead of settling static
    const continuousZoom = interpolate(localFrame, [0, halfDuration], [1.15, 1.0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    const imgScale = continuousZoom;

    return (
      <AbsoluteFill style={{ backgroundColor: TP_COLORS.darkGray }}>
        {/* Leaders image */}
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <Img
            src={staticFile(leadersImage)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${imgScale})`,
              filter: "brightness(0.8)",
            }}
          />
        </AbsoluteFill>

        <AbsoluteFill
          style={{
            background: "linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 100%)",
          }}
        />

        {/* Artist label */}
        <div
          style={{
            position: "absolute",
            top: 80,
            left: 80,
            fontSize: 18,
            fontWeight: 700,
            fontFamily: TP_FONT.primary,
            color: TP_COLORS.neonYellow,
            letterSpacing: "0.2em",
          }}
        >
          ARTIST PICK UP
        </div>
        <div
          style={{
            position: "absolute",
            top: 110,
            left: 80,
            fontSize: 48,
            fontWeight: 900,
            fontFamily: TP_FONT.primary,
            color: TP_COLORS.white,
          }}
        >
          新しい学校のリーダーズ
        </div>

        {/* Achievements */}
        <div style={{ position: "absolute", bottom: 80, left: 80, right: 80 }}>
          {achievements.map((ach, i) => {
            const achDelay = 10 + i * 12;
            const achProgress = spring({
              frame: Math.max(0, localFrame - achDelay),
              fps,
              config: { damping: 18, mass: 0.5, stiffness: 120 },
            });
            const achX = interpolate(achProgress, [0, 1], [-60, 0]);
            const achOpacity = interpolate(achProgress, [0, 1], [0, 1]);

            return (
              <div
                key={i}
                style={{
                  fontSize: 28,
                  fontWeight: 700,
                  fontFamily: TP_FONT.primary,
                  color: TP_COLORS.white,
                  opacity: achOpacity,
                  transform: `translateX(${achX}px)`,
                  marginBottom: 12,
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                }}
              >
                <div style={{ width: 8, height: 8, backgroundColor: TP_COLORS.neonYellow, borderRadius: "50%" }} />
                {ach}
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    );
  }

  // Phase 1: Grid montage with continuous Ken Burns motion
  const COLS = 6;
  const ROWS = 4;
  const cellW = 1920 / COLS;
  const cellH = 1080 / ROWS;

  // Deterministic per-cell motion parameters (seeded by index)
  const cellMotion = (i: number) => {
    const seed = ((i * 7 + 3) % 11) / 11; // 0-1 pseudo-random
    const zoomDir = seed > 0.5 ? 1 : -1;
    const panX = ((i * 13 + 5) % 9 - 4) * 3; // -12 to 12
    const panY = ((i * 11 + 7) % 7 - 3) * 2; // -6 to 6
    return { zoomDir, panX, panY };
  };

  return (
    <AbsoluteFill style={{ backgroundColor: TP_COLORS.darkGray }}>
      {gridImages.slice(0, COLS * ROWS).map((img, i) => {
        const col = i % COLS;
        const row = Math.floor(i / COLS);
        const isFromLeft = row % 2 === 0;
        const delay = Math.abs(col - (isFromLeft ? 0 : COLS - 1)) * 3 + row * 5;

        const cellProgress = spring({
          frame: Math.max(0, frame - delay),
          fps,
          config: { damping: 16, mass: 0.6, stiffness: 100 },
        });

        const slideX = interpolate(cellProgress, [0, 1], [isFromLeft ? -200 : 200, 0]);
        const cellOpacity = interpolate(cellProgress, [0, 1], [0, 1]);

        // Continuous Ken Burns motion after entrance
        const { zoomDir, panX, panY } = cellMotion(i);
        const motionProgress = interpolate(frame, [0, halfDuration], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const imgZoom = 1.05 + zoomDir * 0.08 * motionProgress;
        const imgPanX = panX * motionProgress;
        const imgPanY = panY * motionProgress;

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: col * cellW,
              top: row * cellH,
              width: cellW,
              height: cellH,
              overflow: "hidden",
              opacity: cellOpacity,
              transform: `translateX(${slideX}px)`,
              willChange: "transform",
            }}
          >
            <Img
              src={staticFile(img)}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                objectPosition: "center center",
                transform: `scale(${imgZoom}) translate(${imgPanX}px, ${imgPanY}px)`,
              }}
            />
          </div>
        );
      })}

      {/* Category labels — staggered with longer intervals */}
      {["TALENT", "ARTIST", "INFLUENCER", "CREATOR"].map((label, i) => {
        const labelDelay = 15 + i * 30; // 1s = 2 beats at 120BPM
        const labelProgress = spring({
          frame: Math.max(0, frame - labelDelay),
          fps,
          config: { damping: 20, mass: 0.4, stiffness: 150 },
        });
        const labelOpacity = interpolate(
          frame,
          [labelDelay, labelDelay + 8, labelDelay + 35, labelDelay + 45],
          [0, 0.9, 0.9, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        return (
          <div
            key={label}
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              pointerEvents: "none",
            }}
          >
            <div
              style={{
                fontSize: 96,
                fontWeight: 900,
                fontFamily: TP_FONT.primary,
                color: TP_COLORS.white,
                opacity: labelOpacity,
                letterSpacing: "0.15em",
                textShadow: "0 4px 20px rgba(0,0,0,0.8)",
                transform: `scale(${interpolate(labelProgress, [0, 1], [0.8, 1])})`,
              }}
            >
              {label}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ─── Scene 06: Pan Dorobo Slideshow ─────────────────────

const PanDoroboSlideshow: React.FC<{
  images: string[];
  visitorCount: number;
}> = ({ images, visitorCount }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const FRAMES_PER_IMAGE = Math.floor((durationInFrames - 60) / images.length); // Leave 60 frames for count-up

  const currentIndex = Math.min(Math.floor(frame / FRAMES_PER_IMAGE), images.length - 1);
  const localFrame = frame - currentIndex * FRAMES_PER_IMAGE;

  // Bounce entrance
  const bounceProgress = spring({
    frame: localFrame,
    fps,
    config: { damping: 10, mass: 0.5, stiffness: 200 },
  });

  // Bounce in + continuous gentle zoom after landing
  const entryScale = interpolate(bounceProgress, [0, 1], [0.85, 1.0]);
  const postZoom = interpolate(localFrame, [10, FRAMES_PER_IMAGE], [0, 0.04], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const scale = entryScale + (bounceProgress > 0.9 ? postZoom : 0);
  const imgOpacity = interpolate(localFrame, [0, 5, FRAMES_PER_IMAGE - 3, FRAMES_PER_IMAGE], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Count-up in the last 2 seconds
  const countUpStart = durationInFrames - 60;
  const isCountUpPhase = frame >= countUpStart;
  const countFrame = Math.max(0, frame - countUpStart);

  // Ease-out curve: fast start, settles exactly at visitorCount (no overshoot)
  const countRatio = interpolate(countFrame, [0, 50], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const eased = 1 - Math.pow(1 - countRatio, 3); // cubic ease-out
  const displayCount = Math.round(eased * visitorCount);

  // After count reaches target, pulse the number
  const countDone = countFrame >= 50;
  const countPulse = countDone ? 1 + Math.sin((countFrame - 50) * 0.15) * 0.03 : eased;

  return (
    <AbsoluteFill style={{ backgroundColor: TP_COLORS.neonYellow }}>
      {/* Blurred background image (prevents empty space with contain) */}
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img
          src={staticFile(images[currentIndex])}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: "blur(30px) brightness(1.1)",
            opacity: isCountUpPhase ? 0.15 : 0.25,
            transform: "scale(1.1)",
          }}
        />
      </AbsoluteFill>

      {/* Image with bounce */}
      <AbsoluteFill
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: 40,
        }}
      >
        <div
          style={{
            width: "85%",
            height: "75%",
            borderRadius: 20,
            overflow: "hidden",
            boxShadow: "0 20px 60px rgba(0,0,0,0.2)",
            transform: `scale(${scale})`,
            opacity: isCountUpPhase ? 0.3 : imgOpacity,
          }}
        >
          <Img
            src={staticFile(images[currentIndex])}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
            }}
          />
        </div>
      </AbsoluteFill>

      {/* Marketing / IP Production label */}
      <div
        style={{
          position: "absolute",
          top: 40,
          left: 60,
          fontSize: 16,
          fontWeight: 700,
          fontFamily: TP_FONT.primary,
          color: TP_COLORS.darkGray,
          letterSpacing: "0.15em",
          opacity: 0.7,
        }}
      >
        MARKETING / IP PRODUCTION
      </div>

      {/* Event name */}
      <div
        style={{
          position: "absolute",
          bottom: isCountUpPhase ? "50%" : 60,
          left: 0,
          right: 0,
          textAlign: "center",
          transform: isCountUpPhase ? "translateY(50%)" : "none",
        }}
      >
        <div
          style={{
            fontSize: isCountUpPhase ? 36 : 28,
            fontWeight: 900,
            fontFamily: TP_FONT.primary,
            color: TP_COLORS.darkGray,
          }}
        >
          パンどろぼうひろば
        </div>

        {/* Count up */}
        {isCountUpPhase && (
          <div
            style={{
              fontSize: 96,
              fontWeight: 900,
              fontFamily: TP_FONT.primary,
              color: TP_COLORS.darkGray,
              marginTop: 20,
              transform: `scale(${countPulse})`,
            }}
          >
            来場者 {displayCount.toLocaleString()}人 突破!
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

// ─── Scene 07: Closing Flashback ────────────────────────

const ClosingFlashback: React.FC<{
  logoSrc: string;
  allImages: string[];
}> = ({ logoSrc, allImages }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const flashbackDuration = 60; // 2s of rapid flashback
  const logoPhaseStart = flashbackDuration;
  const isLogoPhase = frame >= logoPhaseStart;

  if (isLogoPhase) {
    const localFrame = frame - logoPhaseStart;
    const logoProgress = spring({
      frame: localFrame,
      fps,
      config: { damping: 16, mass: 0.8, stiffness: 80 },
    });

    const sloganOpacity = interpolate(localFrame, [0, 15], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    const logoOpacity = interpolate(localFrame, [15, 30], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

    // Continuous breathing after logo lands
    const breathe = localFrame > 30 ? Math.sin((localFrame - 30) * 0.07) * 0.01 : 0;
    const logoScale = interpolate(logoProgress, [0, 1], [0.9, 1]) + breathe;

    // Accent line keeps expanding slowly
    const lineWidth = interpolate(localFrame, [0, 30, durationInFrames - flashbackDuration], [0, 120, 200], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

    return (
      <AbsoluteFill
        style={{
          backgroundColor: TP_COLORS.white,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 40,
        }}
      >
        <div
          style={{
            fontSize: 36,
            fontWeight: 700,
            fontFamily: TP_FONT.primary,
            color: TP_COLORS.darkGray,
            opacity: sloganOpacity,
            letterSpacing: "0.1em",
          }}
        >
          世の中に、次の空気を。
        </div>
        <Img
          src={staticFile(logoSrc)}
          style={{
            width: "35%",
            objectFit: "contain",
            opacity: logoOpacity,
            transform: `scale(${logoScale})`,
          }}
        />
        {/* Yellow accent line — keeps growing */}
        <div
          style={{
            width: lineWidth,
            height: 3,
            backgroundColor: TP_COLORS.neonYellow,
          }}
        />
      </AbsoluteFill>
    );
  }

  // Flashback phase: rapid image cycling
  const flashInterval = 3; // 3 frames per image = 10fps effective
  const currentImageIndex = Math.floor(frame / flashInterval) % allImages.length;

  // Increasing intensity toward the end
  const flashOpacity = interpolate(
    frame,
    [0, flashbackDuration * 0.7, flashbackDuration],
    [0.8, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: TP_COLORS.black }}>
      <Img
        src={staticFile(allImages[currentImageIndex])}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: flashOpacity,
        }}
      />
      <AbsoluteFill
        style={{
          background: `linear-gradient(45deg, ${TP_COLORS.neonYellow}20, transparent)`,
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};

// ─── Scene Exit Wrapper ─────────────────────────────────
// Adds a quick scale-up + fade-out in the last EXIT_FRAMES to kill dead time

const SceneWrap: React.FC<{
  children: React.ReactNode;
  exitFrames?: number;
  noExit?: boolean;
}> = ({ children, exitFrames = 10, noExit = false }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  if (noExit) return <AbsoluteFill>{children}</AbsoluteFill>;

  const exitStart = durationInFrames - exitFrames;
  const exitProgress = interpolate(frame, [exitStart, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const scale = 1 + exitProgress * 0.06; // subtle zoom out
  const opacity = 1 - exitProgress;

  return (
    <AbsoluteFill
      style={{
        transform: `scale(${scale})`,
        opacity,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

// ─── Main Composition ───────────────────────────────────

export const TwinPlanetIntro: React.FC<TwinPlanetIntroProps> = (props) => {
  const p = { ...DEFAULT_PROPS, ...props };
  const { fps } = useVideoConfig();

  const durations = p.sectionDurations!;
  const frameDurations = durations.map((s) => Math.round(s * fps));

  const offsets = useMemo(() => {
    let offset = 0;
    return frameDurations.map((d) => {
      const o = offset;
      offset += d;
      return o;
    });
  }, [frameDurations]);

  // Collect all images for flashback
  const allImages = useMemo(() => [
    ...p.mainTalent!.map((t) => t.imageSrc),
    ...(p.talentGridImages || []).slice(0, 8),
    ...(p.panDoroboImages || []).slice(0, 4),
  ], [p.mainTalent, p.talentGridImages, p.panDoroboImages]);

  return (
    <AbsoluteFill>
      {/* BGM */}
      {p.bgmSrc && <Audio src={staticFile(p.bgmSrc)} volume={0.28} />}

      {/* Scene 01: Logo Opening */}
      <Sequence from={offsets[0]} durationInFrames={frameDurations[0]}>
        <SceneWrap>
          <LogoOpening logoSrc={p.logoSrc!} />
        </SceneWrap>
      </Sequence>

      {/* Scene 02: Vision Statement */}
      <Sequence from={offsets[1]} durationInFrames={frameDurations[1]}>
        <SceneWrap>
          <VisionStatement slogan={p.slogan!} />
        </SceneWrap>
      </Sequence>

      {/* Scene 03: Three Pillars */}
      <Sequence from={offsets[2]} durationInFrames={frameDurations[2]}>
        <SceneWrap>
          <ThreePillars pillars={p.pillars!} />
        </SceneWrap>
      </Sequence>

      {/* Scene 04: Talent Showcase (Main 6) */}
      <Sequence from={offsets[3]} durationInFrames={frameDurations[3]}>
        <SceneWrap>
          <TalentShowcase talent={p.mainTalent!} />
        </SceneWrap>
      </Sequence>

      {/* Scene 05: Talent Grid + Leaders */}
      <Sequence from={offsets[4]} durationInFrames={frameDurations[4]}>
        <SceneWrap>
          <TalentGridAndLeaders
            gridImages={p.talentGridImages!}
            leadersImage={p.leadersImage!}
            achievements={p.achievements!}
          />
        </SceneWrap>
      </Sequence>

      {/* Scene 06: Pan Dorobo */}
      <Sequence from={offsets[5]} durationInFrames={frameDurations[5]}>
        <SceneWrap>
          <PanDoroboSlideshow images={p.panDoroboImages!} visitorCount={p.visitorCount!} />
        </SceneWrap>
      </Sequence>

      {/* Scene 07: Closing — no exit, ends clean */}
      <Sequence from={offsets[6]} durationInFrames={frameDurations[6]}>
        <SceneWrap noExit>
          <ClosingFlashback logoSrc={p.logoSrc!} allImages={allImages} />
        </SceneWrap>
      </Sequence>
    </AbsoluteFill>
  );
};

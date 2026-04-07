import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig, useCurrentFrame, interpolate } from "remotion";

import { CinematicTextHook } from "../components/scenes/CinematicTextHook";
import { MeshGradientTransition } from "../components/scenes/MeshGradientTransition";
import { PromptBar } from "../components/scenes/PromptBar";
import { TimeComparison } from "../components/scenes/TimeComparison";
import { AppUIDemo } from "../components/scenes/AppUIDemo";
import { VoiceRush } from "../components/scenes/VoiceRush";
import { IntegrationsGrid } from "../components/scenes/IntegrationsGrid";
import { ShowcaseClosing } from "../components/scenes/ShowcaseClosing";

// ─── Types ──────────────────────────────────────────────
interface TextLine {
  text: string;
  delayMs?: number;
}

interface ComparisonItem {
  label: string;
  before: string;
  after: string;
}

interface Testimonial {
  name: string;
  title: string;
  company: string;
  comment?: string;
}

interface Integration {
  name: string;
  logoSrc?: string;
}

interface NarrationTrack {
  section: number;
  src: string;
}

export interface ProductShowcaseProps {
  // Section 1: Cinematic Text Hook
  hookLines?: TextLine[];
  // Section 2: Mesh Gradient Transition
  meshText?: string;
  // Section 3: Prompt Bar
  promptText?: string;
  promptResultText?: string;
  // Section 4: Time Comparison (Before→After)
  comparisons?: ComparisonItem[];
  // Section 5: App UI Demo
  brandName?: string;
  // Section 6: Voice Rush (Testimonials)
  testimonials?: Testimonial[];
  // Section 7: Integrations + Use Cases
  integrations?: Integration[];
  integrationsTitle?: string;
  useCases?: string[];
  // Section 8: Closing
  closingText?: string;
  closingSubText?: string;
  closingUrl?: string;
  urlSubText?: string;
  // Audio
  narrationTracks?: NarrationTrack[];
  bgmSrc?: string;
  bgmVolume?: number;
  // Timing
  sectionDurations?: number[];
}

// ─── Default Props ──────────────────────────────────────
export const DEFAULT_PROPS: ProductShowcaseProps = {
  // S1: 共感フック
  hookLines: [
    { text: "レポート作成、3時間。", delayMs: 800 },
    { text: "データ集計、半日。", delayMs: 600 },
    { text: "その仕事、まだ手動？", delayMs: 1000 },
  ],
  // S2: 転換
  meshText: "15分で終わる。",
  // S3: デモ
  promptText: "先月の売上データをまとめて、PowerPointにして",
  promptResultText: "売上レポート.pptx を生成しました",
  // S4: Before→After
  comparisons: [
    { label: "LP制作", before: "2週間", after: "1時間" },
    { label: "競合調査", before: "丸1日", after: "15分" },
    { label: "議事録作成", before: "2時間", after: "5分" },
  ],
  // S5: プラットフォーム
  brandName: "AI Agent Camp",
  // S6: 顧客の声ラッシュ
  testimonials: [
    { name: "山碕峻太郎", title: "取締役副社長", company: "プログリット", comment: "AIエージェントの活用方法を知ることができ、仕事の進め方が大きく変わった。社内でのAI活用について考えるきっかけとなった。" },
    { name: "Nayu Yamamoto", title: "Strategy Manager", company: "Startale", comment: "講座後、ビジネスチームで研修を行い、半数以上が「作業効率が向上した」と回答。現在も継続利用中です。" },
    { name: "川口修平", title: "社長室", company: "ビットエー", comment: "初期設定を事前に用意してくださっており、すぐに動かせる状態になっていました。MCPでの各種アプリケーション接続で業務の可能性が広がりました。" },
  ],
  // S7: ツール
  integrations: [
    { name: "Cursor" },
    { name: "Claude" },
    { name: "Notion" },
    { name: "Slack" },
    { name: "Google Apps Script" },
    { name: "BigQuery" },
    { name: "GitHub Actions" },
    { name: "Vercel" },
    { name: "GA4" },
    { name: "Remotion" },
    { name: "Figma" },
    { name: "LINE Bot" },
  ],
  integrationsTitle: "こんな業務を、AIで自動化",
  useCases: [
    "LP制作を自動化",
    "競合調査をAIで",
    "議事録の自動要約",
    "請求書の自動仕訳",
    "Slack Bot構築",
    "データ分析レポート",
  ],
  // S8: CTA
  closingText: "あなたの仕事を、AIで変えよう。",
  closingSubText: "月額 ¥12,800 から",
  closingUrl: "ai-agent.camp",
  urlSubText: "無料体験レッスン公開中",
  // Audio
  narrationTracks: [],
  bgmSrc: "sns_mv_bgm.mp3",
  bgmVolume: 0.15,
  // Timing: [5, 3, 5, 7, 7, 9, 7, 7] = 50s
  sectionDurations: [5, 3, 5, 7, 7, 9, 7, 7],
};

// ─── Scene Transition ────────────────────────────────────
const SceneTransition: React.FC<{
  children: React.ReactNode;
  fadeIn?: boolean;
  fadeOut?: boolean;
  fadeFrames?: number;
}> = ({ children, fadeIn = true, fadeOut = true, fadeFrames = 15 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  let opacity = 1;
  if (fadeIn) {
    opacity *= interpolate(frame, [0, fadeFrames], [0, 1], { extrapolateRight: "clamp" });
  }
  if (fadeOut) {
    opacity *= interpolate(frame, [durationInFrames - fadeFrames, durationInFrames], [1, 0], { extrapolateLeft: "clamp" });
  }

  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};

// ─── Main Composition ───────────────────────────────────
type ResolvedProps = Required<ProductShowcaseProps>;

export const ProductShowcase: React.FC<ProductShowcaseProps> = (props) => {
  const p = { ...DEFAULT_PROPS, ...props } as ResolvedProps;
  const { fps } = useVideoConfig();

  const durations = p.sectionDurations;
  const frameDurations = durations.map((s) => Math.round(s * fps));

  let offset = 0;
  const offsets = frameDurations.map((d) => {
    const o = offset;
    offset += d;
    return o;
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {/* Section 1: Cinematic Text Hook */}
      <Sequence from={offsets[0]} durationInFrames={frameDurations[0]}>
        <SceneTransition fadeIn={true} fadeOut={true}>
          <CinematicTextHook lines={p.hookLines} />
        </SceneTransition>
      </Sequence>

      {/* Section 2: Mesh Gradient Transition */}
      <Sequence from={offsets[1]} durationInFrames={frameDurations[1]}>
        <MeshGradientTransition text={p.meshText} />
      </Sequence>

      {/* Section 3: Prompt Bar with Result */}
      <Sequence from={offsets[2]} durationInFrames={frameDurations[2]}>
        <SceneTransition fadeIn={true} fadeOut={true}>
          <PromptBar text={p.promptText} resultText={p.promptResultText} />
        </SceneTransition>
      </Sequence>

      {/* Section 4: Before→After Time Comparison */}
      <Sequence from={offsets[3]} durationInFrames={frameDurations[3]}>
        <SceneTransition fadeIn={true} fadeOut={true}>
          <TimeComparison comparisons={p.comparisons} />
        </SceneTransition>
      </Sequence>

      {/* Section 5: App UI Demo */}
      <Sequence from={offsets[4]} durationInFrames={frameDurations[4]}>
        <SceneTransition fadeIn={true} fadeOut={true} fadeFrames={10}>
          <AppUIDemo
            brandName={p.brandName}
          />
        </SceneTransition>
      </Sequence>

      {/* Section 6: Voice Rush (Testimonials + Use Cases) */}
      <Sequence from={offsets[5]} durationInFrames={frameDurations[5]}>
        <SceneTransition fadeIn={true} fadeOut={true}>
          <VoiceRush
            testimonials={p.testimonials}
          />
        </SceneTransition>
      </Sequence>

      {/* Section 7: Integrations Grid */}
      <Sequence from={offsets[6]} durationInFrames={frameDurations[6]}>
        <SceneTransition fadeIn={true} fadeOut={true}>
          <IntegrationsGrid
            title={p.integrationsTitle}
            integrations={p.integrations}
            useCases={p.useCases}
          />
        </SceneTransition>
      </Sequence>

      {/* Section 8: Closing with CTA */}
      <Sequence from={offsets[7]} durationInFrames={frameDurations[7]}>
        <SceneTransition fadeIn={true} fadeOut={true}>
          <ShowcaseClosing
            closingText={p.closingText}
            brandName={p.brandName}
            closingUrl={p.closingUrl}
            closingSubText={p.closingSubText}
            urlSubText={p.urlSubText}
          />
        </SceneTransition>
      </Sequence>

      {/* ─── Audio: Narration tracks ──────────────────────── */}
      {p.narrationTracks.map((track) => {
        const sectionIndex = track.section - 1;
        if (sectionIndex >= 0 && sectionIndex < offsets.length) {
          return (
            <Sequence
              key={`narration-${track.section}`}
              from={offsets[sectionIndex]}
              durationInFrames={frameDurations[sectionIndex]}
            >
              <Audio src={staticFile(track.src)} volume={0.9} />
            </Sequence>
          );
        }
        return null;
      })}

      {/* ─── Audio: Background music ─────────────────────── */}
      {p.bgmSrc && (
        <Audio src={staticFile(p.bgmSrc)} volume={p.bgmVolume} />
      )}
    </AbsoluteFill>
  );
};

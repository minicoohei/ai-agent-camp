import React from "react";
import { Composition } from "remotion";
import { AgentCampContentScreenDemoComposition } from "./AgentCampContentScreenDemoComposition";
import { ScreenExplainer } from "./compositions/ScreenExplainer";
import { ProductShowcase, DEFAULT_PROPS as SHOWCASE_DEFAULT_PROPS } from "./compositions/ProductShowcase";
import { TwinPlanetIntro, DEFAULT_PROPS as TP_DEFAULT_PROPS } from "./compositions/TwinPlanetIntro";

const FPS_24 = 24;
const FPS = 30;
const FPS_60 = 60;

export const PRESETS = {
  vertical: { width: 1080, height: 1920 },
  horizontal: { width: 1920, height: 1080 },
  square: { width: 1080, height: 1080 },
} as const;

// Vertical-only scenes (demo screens only, no title/comparison/CTA)
const VERTICAL_DEMO_SCENES = [
  {
    scene_number: 1,
    layout: "cursor_ide",
    caption: "Cursor IDEでAI Agentに一言指示するだけ",
    duration: 8,
  },
  {
    scene_number: 2,
    layout: "terminal",
    caption: "競合分析からLP作成まで全自動",
    duration: 6,
  },
  {
    scene_number: 3,
    layout: "dashboard",
    caption: "リアルタイムで進捗を可視化",
    duration: 6,
  },
];

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="AgentCamp-content-screen"
        component={AgentCampContentScreenDemoComposition}
        durationInFrames={1271}
        fps={FPS_24}
        width={PRESETS.horizontal.width}
        height={PRESETS.horizontal.height}
      />
      <Composition
        id="ScreenExplainer"
        component={ScreenExplainer}
        durationInFrames={32 * FPS}
        fps={FPS}
        width={PRESETS.horizontal.width}
        height={PRESETS.horizontal.height}
        defaultProps={{}}
      />
      <Composition
        id="ScreenExplainerVertical"
        component={ScreenExplainer}
        durationInFrames={20 * FPS}
        fps={FPS}
        width={PRESETS.vertical.width}
        height={PRESETS.vertical.height}
        defaultProps={{
          scenes: VERTICAL_DEMO_SCENES,
        }}
      />
      <Composition
        id="ProductShowcase"
        component={ProductShowcase}
        durationInFrames={50 * FPS_60}
        fps={FPS_60}
        width={PRESETS.horizontal.width}
        height={PRESETS.horizontal.height}
        defaultProps={SHOWCASE_DEFAULT_PROPS}
      />
      <Composition
        id="TwinPlanetIntro"
        component={TwinPlanetIntro}
        durationInFrames={Math.round(39.5 * FPS)}
        fps={FPS}
        width={PRESETS.horizontal.width}
        height={PRESETS.horizontal.height}
        defaultProps={TP_DEFAULT_PROPS}
      />
    </>
  );
};

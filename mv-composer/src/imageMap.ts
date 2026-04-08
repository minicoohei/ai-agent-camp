/**
 * Image path mapping for AI-generated scene backgrounds
 * Generated images live in: public/ac/generated/{category}/{name}.png
 *
 * Falls back to i2v video paths if generated images don't exist.
 */

type SceneImages = {
  hook: string;
  pain: string;
  solution: string;
  demo: string;
  result: string;
  cta: string;
  tool: string;
};

type PersonaKey =
  | "marketer"
  | "sales"
  | "accounting"
  | "consultant"
  | "lawyer"
  | "planning"
  | "writer"
  | "exam_parent";

/* ═══════════════════ Common backgrounds (shared across personas) ═══════════════════ */

export const COMMON_BG = {
  hook_dark: "ac/generated/common/hook_dark.png",
  hook_numbers: "ac/generated/common/hook_numbers.png",
  solution_glow: "ac/generated/common/solution_glow.png",
  solution_process: "ac/generated/common/solution_process.png",
  result_celebration: "ac/generated/common/result_celebration.png",
  result_chart: "ac/generated/common/result_chart.png",
  cta_gradient: "ac/generated/common/cta_gradient.png",
  before_stress: "ac/generated/common/before_stress.png",
  before_overtime: "ac/generated/common/before_overtime.png",
  transition_mesh: "ac/generated/common/transition_mesh.png",
} as const;

/* ═══════════════════ Per-persona images ═══════════════════ */

const personaImages: Record<PersonaKey, SceneImages> = {
  marketer: {
    hook: COMMON_BG.hook_numbers,
    pain: "ac/generated/marketer/pain.png",
    solution: "ac/generated/marketer/demo.png",
    demo: "ac/generated/marketer/tool.png",
    result: "ac/generated/marketer/result.png",
    cta: COMMON_BG.cta_gradient,
    tool: "ac/generated/marketer/tool.png",
  },
  sales: {
    hook: COMMON_BG.hook_dark,
    pain: "ac/generated/sales/pain.png",
    solution: "ac/generated/sales/demo.png",
    demo: "ac/generated/sales/tool.png",
    result: "ac/generated/sales/result.png",
    cta: COMMON_BG.cta_gradient,
    tool: "ac/generated/sales/tool.png",
  },
  accounting: {
    hook: COMMON_BG.hook_dark,
    pain: "ac/generated/accounting/pain.png",
    solution: "ac/generated/accounting/demo.png",
    demo: "ac/generated/accounting/tool.png",
    result: "ac/generated/accounting/result.png",
    cta: COMMON_BG.cta_gradient,
    tool: "ac/generated/accounting/tool.png",
  },
  consultant: {
    hook: COMMON_BG.hook_numbers,
    pain: "ac/generated/consultant/pain.png",
    solution: "ac/generated/consultant/demo.png",
    demo: "ac/generated/consultant/tool.png",
    result: "ac/generated/consultant/result.png",
    cta: COMMON_BG.cta_gradient,
    tool: "ac/generated/consultant/tool.png",
  },
  lawyer: {
    hook: COMMON_BG.hook_dark,
    pain: "ac/generated/lawyer/pain.png",
    solution: "ac/generated/lawyer/demo.png",
    demo: "ac/generated/lawyer/tool.png",
    result: "ac/generated/lawyer/result.png",
    cta: COMMON_BG.cta_gradient,
    tool: "ac/generated/lawyer/tool.png",
  },
  planning: {
    hook: COMMON_BG.hook_numbers,
    pain: "ac/generated/planning/pain.png",
    solution: "ac/generated/planning/demo.png",
    demo: "ac/generated/planning/tool.png",
    result: "ac/generated/planning/result.png",
    cta: COMMON_BG.cta_gradient,
    tool: "ac/generated/planning/tool.png",
  },
  writer: {
    hook: COMMON_BG.hook_dark,
    pain: "ac/generated/writer/pain.png",
    solution: "ac/generated/writer/demo.png",
    demo: "ac/generated/writer/tool.png",
    result: "ac/generated/writer/result.png",
    cta: COMMON_BG.cta_gradient,
    tool: "ac/generated/writer/tool.png",
  },
  exam_parent: {
    hook: COMMON_BG.hook_dark,
    pain: "ac/generated/exam_parent/pain.png",
    solution: "ac/generated/exam_parent/demo.png",
    demo: "ac/generated/exam_parent/tool.png",
    result: "ac/generated/exam_parent/result.png",
    cta: COMMON_BG.cta_gradient,
    tool: "ac/generated/exam_parent/tool.png",
  },
};

export function getPersonaImages(persona: PersonaKey): SceneImages {
  return personaImages[persona];
}

export function getSceneBg(persona: PersonaKey, scene: keyof SceneImages): string {
  return personaImages[persona][scene];
}

export type { PersonaKey, SceneImages };

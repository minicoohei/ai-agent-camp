import { getPersonaImages, PersonaKey } from "../imageMap";
import { TextLine } from "../components/scenes/CinematicTextHook";

/* ═══════════════════ Types ═══════════════════ */

export interface TikTok60Props extends PresetBase {
  persona: PersonaKey | string;
  bgImages: {
    hook: string;
    pain: string;
    solution: string;
    result: string;
    cta: string;
  };
  bgmSrc: string;
  sectionDurations: number[];
  locale?: string;
}

/* ═══════════════════ Preset Data ═══════════════════ */

interface PresetBase {
  segment: string;
  segmentIcon: string;
  hookLines: TextLine[];
  painLines: string[];
  promptText: string;
  promptResult: string;
  demoSteps: { icon: string; label: string; sublabel?: string }[];
  statLabel: string;
  statValue: number;
  statSuffix: string;
  beforeLabel: string;
  afterLabel: string;
  ctaText?: string;
}

const PRESETS: Record<string, PresetBase> = {
  marketer: {
    segment: "マーケター",
    segmentIcon: "M",
    hookLines: [
      { text: "月40時間の"},
      { text: "レポート作業", delayMs: 800},
      { text: "まだ手作業？", delayMs: 800},
    ],
    painLines: [
      "GA4→スプレッドシートの手動コピペ",
      "5ツールからのデータ統合に半日",
      "レポート作成で施策立案の時間がない",
    ],
    promptText: "毎週月曜にGA4+Meta Ads+メールの統合レポートを自動生成して",
    promptResult: "週次マーケティングレポート自動化完了",
    demoSteps: [
      { icon: "M12 8v8m-4-4h8", label: "GA4 データ自動取得", sublabel: "pageview, session, conversion" },
      { icon: "M9 5l7 7-7 7", label: "Meta Ads API 連携", sublabel: "CPA, ROAS, impression" },
      { icon: "M4 6h16M4 12h16m-7 6h7", label: "統合レポート生成", sublabel: "チャート + インサイト + 提案" },
    ],
    statLabel: "レポート作業時間削減",
    statValue: 90,
    statSuffix: "%",
    beforeLabel: "月40時間",
    afterLabel: "月4時間",
    ctaText: "レポート地獄から解放されよう",
  },

  sales: {
    segment: "営業",
    segmentIcon: "S",
    hookLines: [
      { text: "商談後の"},
      { text: "CRM入力", delayMs: 800},
      { text: "AI で自動化", delayMs: 800},
    ],
    painLines: [
      "商談メモ→CRM転記に毎回30分",
      "フォローメール作成が後回しに",
      "日報作成で営業時間が削られる",
    ],
    promptText: "商談録音からCRM更新とフォローメールを自動生成して",
    promptResult: "CRM更新+フォローメール自動化完了",
    demoSteps: [
      { icon: "M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4", label: "商談音声を自動文字起こし" },
      { icon: "M4 7v10c0 1 1 2 2 2h12c1 0 2-1 2-2V7", label: "CRM項目を自動入力" },
      { icon: "M3 8l7.89 5.26a2 2 0 002.22 0L21 8", label: "パーソナライズメール生成" },
    ],
    statLabel: "営業事務時間削減",
    statValue: 85,
    statSuffix: "%",
    beforeLabel: "1商談あたり45分",
    afterLabel: "1商談あたり5分",
    ctaText: "営業に集中できる環境を作ろう",
  },

  accounting: {
    segment: "経理",
    segmentIcon: "A",
    hookLines: [
      { text: "確定申告"},
      { text: "まだ手作業?", delayMs: 800},
      { text: "10倍速へ", delayMs: 800},
    ],
    painLines: [
      "領収書の手入力で1件3時間",
      "仕訳判定ミスの手戻り",
      "繁忙期は毎日終電",
    ],
    promptText: "領収書画像から仕訳を自動生成して会計ソフトに登録して",
    promptResult: "領収書→仕訳→登録 自動化完了",
    demoSteps: [
      { icon: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16", label: "領収書をOCR読み取り", sublabel: "日付・金額・取引先を自動抽出" },
      { icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2", label: "仕訳を自動判定", sublabel: "勘定科目・税区分を推定" },
      { icon: "M5 13l4 4L19 7", label: "会計ソフトに自動登録", sublabel: "異常値アラート付き" },
    ],
    statLabel: "処理時間削減",
    statValue: 90,
    statSuffix: "%",
    beforeLabel: "1件3時間",
    afterLabel: "1件20分",
    ctaText: "繁忙期でも定時退社へ",
  },

  consultant: {
    segment: "コンサルタント",
    segmentIcon: "C",
    hookLines: [
      { text: "提案資料"},
      { text: "毎回ゼロから?", delayMs: 800},
      { text: "AIで瞬殺", delayMs: 800},
    ],
    painLines: [
      "競合分析に毎回2日かかる",
      "市場データの収集が属人的",
      "クライアント提案がテンプレ化できない",
    ],
    promptText: "SaaS業界の競合分析レポートと戦略提案書を生成して",
    promptResult: "競合分析+戦略提案書 自動生成完了",
    demoSteps: [
      { icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z", label: "業界データ自動収集", sublabel: "IR資料・ニュース・SNS分析" },
      { icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6", label: "競合マッピング生成", sublabel: "ポジショニング・SWOT・市場シェア" },
      { icon: "M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z", label: "戦略提案書を自動作成" },
    ],
    statLabel: "提案準備時間削減",
    statValue: 80,
    statSuffix: "%",
    beforeLabel: "2日",
    afterLabel: "4時間",
    ctaText: "分析はAIに、戦略は人に",
  },

  lawyer: {
    segment: "弁護士",
    segmentIcon: "L",
    hookLines: [
      { text: "契約書レビュー"},
      { text: "毎回3時間?", delayMs: 800},
      { text: "15分で完了", delayMs: 800},
    ],
    painLines: [
      "契約書チェックに毎回3時間",
      "判例調査の検索が非効率",
      "書面作成の定型部分が多すぎる",
    ],
    promptText: "この業務委託契約書のリスク分析と修正案を出して",
    promptResult: "契約書リスク分析+修正案 生成完了",
    demoSteps: [
      { icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586", label: "契約条項を自動解析", sublabel: "リスク条項をハイライト" },
      { icon: "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13", label: "関連判例を自動検索", sublabel: "最新判例データベース参照" },
      { icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5", label: "修正案を自動生成" },
    ],
    statLabel: "レビュー時間削減",
    statValue: 85,
    statSuffix: "%",
    beforeLabel: "3時間",
    afterLabel: "15分",
    ctaText: "法務をAIでアップグレード",
  },

  planning: {
    segment: "企画",
    segmentIcon: "P",
    hookLines: [
      { text: "市場調査"},
      { text: "属人的すぎ", delayMs: 800},
      { text: "AIが即分析", delayMs: 800},
    ],
    painLines: [
      "競合情報の収集が毎回手動",
      "企画書作成がテンプレなし",
      "データに基づく意思決定ができてない",
    ],
    promptText: "ターゲット市場の競合分析とGo-To-Market戦略を立案して",
    promptResult: "市場分析+GTM戦略 立案完了",
    demoSteps: [
      { icon: "M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945", label: "市場データ自動収集" },
      { icon: "M16 8v8m-4-5v5m-4-2v2", label: "トレンド分析レポート生成" },
      { icon: "M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7", label: "戦略企画書を自動作成" },
    ],
    statLabel: "企画立案スピード",
    statValue: 5,
    statSuffix: "倍",
    beforeLabel: "1週間",
    afterLabel: "1日",
    ctaText: "企画力をAIで加速しよう",
  },

  writer: {
    segment: "ライター",
    segmentIcon: "W",
    hookLines: [
      { text: "リサーチから"},
      { text: "入稿まで", delayMs: 800},
      { text: "全自動化", delayMs: 800},
    ],
    painLines: [
      "リサーチに記事の半分の時間",
      "構成案→執筆→校正が毎回ゼロから",
      "入稿フォーマット変換の繰り返し",
    ],
    promptText: "AI Agent Campのターゲット向けSEO記事を構成から執筆まで",
    promptResult: "SEO記事 構成→執筆→校正 完了",
    demoSteps: [
      { icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z", label: "キーワードリサーチ自動化" },
      { icon: "M4 6h16M4 12h16M4 18h7", label: "構成案+記事本文を生成" },
      { icon: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z", label: "SEO最適化+校正チェック" },
    ],
    statLabel: "記事制作時間削減",
    statValue: 75,
    statSuffix: "%",
    beforeLabel: "1記事8時間",
    afterLabel: "1記事2時間",
    ctaText: "書く仕事をAIでブーストしよう",
  },

  exam_parent: {
    segment: "受験の親",
    segmentIcon: "E",
    hookLines: [
      { text: "お子さんの"},
      { text: "受験対策", delayMs: 800},
      { text: "AIチューターで", delayMs: 800},
    ],
    painLines: [
      "塾選びに毎回悩む",
      "子どもの弱点把握が難しい",
      "学習計画が立てられない",
    ],
    promptText: "中学受験の算数の弱点を分析して個別学習プランを作って",
    promptResult: "弱点分析+個別学習プラン 生成完了",
    demoSteps: [
      { icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2", label: "テスト結果を自動分析", sublabel: "単元別の正答率を可視化" },
      { icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z", label: "最適な学習プラン生成", sublabel: "弱点集中+復習サイクル" },
      { icon: "M13 10V3L4 14h7v7l9-11h-7z", label: "AI練習問題を出題", sublabel: "レベル適応型ドリル" },
    ],
    statLabel: "学習効率アップ",
    statValue: 3,
    statSuffix: "倍",
    beforeLabel: "やみくもに勉強",
    afterLabel: "弱点集中で効率3倍",
    ctaText: "お子さんの可能性を広げよう",
  },
};

/* ═══════════════════ Reddit EN Presets ═══════════════════ */

const REDDIT_PRESETS: Record<string, PresetBase> = {
  reddit_marketer: {
    segment: "Marketer",
    segmentIcon: "M",
    hookLines: [
      { text: "I spent 40 hours/month" },
      { text: "on marketing reports.", delayMs: 700 },
      { text: "Then I built an AI agent.", delayMs: 700 },
    ],
    painLines: [
      "Manually copying data from GA4 to spreadsheets",
      "Half a day merging data from 5 different tools",
      "Zero time left for actual strategy work",
    ],
    promptText: "Build a weekly report that pulls GA4 + Meta Ads + email metrics automatically",
    promptResult: "Weekly marketing report automated — done.",
    demoSteps: [
      { icon: "M12 8v8m-4-4h8", label: "Auto-pull GA4 data", sublabel: "pageviews, sessions, conversions" },
      { icon: "M9 5l7 7-7 7", label: "Connect Meta Ads API", sublabel: "CPA, ROAS, impressions" },
      { icon: "M4 6h16M4 12h16m-7 6h7", label: "Generate unified report", sublabel: "charts + insights + next actions" },
    ],
    statLabel: "Report time saved",
    statValue: 90,
    statSuffix: "%",
    beforeLabel: "40 hrs/month",
    afterLabel: "4 hrs/month",
    ctaText: "No code. Just natural language.",
  },

  reddit_freelancer: {
    segment: "Freelancer",
    segmentIcon: "F",
    hookLines: [
      { text: "I automated my entire" },
      { text: "client workflow.", delayMs: 700 },
      { text: "Zero coding required.", delayMs: 700 },
    ],
    painLines: [
      "Invoicing, follow-ups, reports — all manual",
      "Losing 10+ hours/week on admin tasks",
      "Clients waiting because you're buried in busywork",
    ],
    promptText: "When a project ends, generate invoice + send follow-up email + update my tracker",
    promptResult: "Client workflow fully automated — 3 steps, 1 prompt.",
    demoSteps: [
      { icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2", label: "Auto-generate invoice", sublabel: "from project data" },
      { icon: "M3 8l7.89 5.26a2 2 0 002.22 0L21 8", label: "Send personalized email", sublabel: "thank you + next steps" },
      { icon: "M4 7v10c0 1 1 2 2 2h12c1 0 2-1 2-2V7", label: "Update client tracker", sublabel: "status, revenue, follow-up date" },
    ],
    statLabel: "Admin time eliminated",
    statValue: 85,
    statSuffix: "%",
    beforeLabel: "10+ hrs/week on admin",
    afterLabel: "Under 2 hrs/week",
    ctaText: "Built by a non-engineer. Seriously.",
  },

  reddit_vibe_coder: {
    segment: "Vibe Coder",
    segmentIcon: "V",
    hookLines: [
      { text: "Vibe coding got me" },
      { text: "80% there.", delayMs: 700 },
      { text: "The last 20% broke me.", delayMs: 700 },
    ],
    painLines: [
      "App looks great in dev, falls apart in production",
      "Edge cases, auth, deployment — AI couldn't finish it",
      "3 weeks debugging code I didn't write or understand",
    ],
    promptText: "Build a lead tracking dashboard with auth, Stripe billing, and email notifications",
    promptResult: "Full-stack app shipped — auth, billing, email all wired up.",
    demoSteps: [
      { icon: "M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5", label: "AI agent plans architecture", sublabel: "auth flow, DB schema, API routes" },
      { icon: "M13 2L3 14h9l-1 8 10-12h-9l1-8z", label: "Implements & tests each module", sublabel: "unit tests + integration tests" },
      { icon: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z", label: "Deploys to production", sublabel: "CI/CD + monitoring included" },
    ],
    statLabel: "Ship time reduced",
    statValue: 90,
    statSuffix: "%",
    beforeLabel: "3 weeks of debugging",
    afterLabel: "2 days, fully shipped",
    ctaText: "Stop vibe coding. Start agent building.",
  },

  reddit_agent_skeptic: {
    segment: "AI Realist",
    segmentIcon: "R",
    hookLines: [
      { text: "90% of 'AI agents'" },
      { text: "are just chatbots", delayMs: 700 },
      { text: "with a cron job.", delayMs: 700 },
    ],
    painLines: [
      "10-step workflow at 85% accuracy = 20% success rate",
      "Session drift: agents lose context after 5 minutes",
      "'Agent-washing' — every SaaS slaps 'AI agent' on a wrapper",
    ],
    promptText: "Analyze my competitor's product pages, extract pricing data, and generate a positioning report",
    promptResult: "Multi-step agent completed — 4 tools orchestrated, zero hallucination.",
    demoSteps: [
      { icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z", label: "Scrapes 3 competitor sites", sublabel: "structured data extraction" },
      { icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6", label: "Cross-references pricing tiers", sublabel: "feature parity matrix" },
      { icon: "M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z", label: "Generates positioning report", sublabel: "with data citations" },
    ],
    statLabel: "Accuracy on real tasks",
    statValue: 97,
    statSuffix: "%",
    beforeLabel: "Chatbot hype",
    afterLabel: "Verifiable agent output",
    ctaText: "Real agents. Real results. No BS.",
  },

  reddit_tax_accountant: {
    segment: "Accountant",
    segmentIcon: "T",
    hookLines: [
      { text: "Tax season used to mean" },
      { text: "80-hour weeks.", delayMs: 700 },
      { text: "This year: 35 hours.", delayMs: 700 },
    ],
    painLines: [
      "Manually entering receipts — 3 hours per client",
      "Misclassified expenses causing re-work every month",
      "Busy season = no weekends from January to April",
    ],
    promptText: "Scan these 50 receipts, classify expenses, and generate journal entries for QuickBooks",
    promptResult: "50 receipts → classified → journal entries ready for import.",
    demoSteps: [
      { icon: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16", label: "OCR scans all receipts", sublabel: "date, amount, vendor extracted" },
      { icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2", label: "Auto-classifies expenses", sublabel: "account codes + tax categories" },
      { icon: "M5 13l4 4L19 7", label: "Exports to accounting software", sublabel: "anomaly alerts included" },
    ],
    statLabel: "Processing time saved",
    statValue: 90,
    statSuffix: "%",
    beforeLabel: "3 hrs per client",
    afterLabel: "20 min per client",
    ctaText: "Finish tax season with your sanity intact.",
  },
};

/* ═══════════════════ Build Full Props ═══════════════════ */

export function getTikTok60Props(persona: PersonaKey): TikTok60Props {
  const base = PRESETS[persona];
  if (!base) throw new Error(`Unknown persona: ${persona}`);
  const images = getPersonaImages(persona);

  return {
    persona,
    ...base,
    bgImages: {
      hook: images.hook,
      pain: images.pain,
      solution: images.solution,
      result: images.result,
      cta: images.cta,
    },
    bgmSrc: "ac/audio/bgm_short_v2.mp3",
    sectionDurations: [3, 4, 39, 5, 9], // 60s — Hook/Problem最短→Demo最大化
  };
}

export const TIKTOK60_PERSONAS: PersonaKey[] = [
  "marketer",
  "sales",
  "accounting",
  "consultant",
  "lawyer",
  "planning",
  "writer",
  "exam_parent",
];

/* ═══════════════════ Reddit EN Props ═══════════════════ */

type RedditPersona = "reddit_marketer" | "reddit_freelancer" | "reddit_vibe_coder" | "reddit_agent_skeptic" | "reddit_tax_accountant";

/** Maps reddit persona to existing image persona for bg reuse */
const REDDIT_IMAGE_MAP: Record<RedditPersona, PersonaKey> = {
  reddit_marketer: "marketer",
  reddit_freelancer: "sales",
  reddit_vibe_coder: "writer",         // creative/builder vibe
  reddit_agent_skeptic: "consultant",   // analytical/skeptical tone
  reddit_tax_accountant: "accounting",  // reuse accounting assets
};

export function getRedditTikTok60Props(persona: RedditPersona): TikTok60Props {
  const base = REDDIT_PRESETS[persona];
  if (!base) throw new Error(`Unknown reddit persona: ${persona}`);
  const imagePersona = REDDIT_IMAGE_MAP[persona];
  const images = getPersonaImages(imagePersona);

  return {
    persona: imagePersona,
    ...base,
    locale: "en" as const,
    bgImages: {
      hook: images.hook,
      pain: images.pain,
      solution: images.solution,
      result: images.result,
      cta: images.cta,
    },
    bgmSrc: "ac/audio/bgm_short_v2.mp3",
    sectionDurations: [3, 4, 39, 5, 9],
  };
}

export const REDDIT_PERSONAS: RedditPersona[] = [
  "reddit_marketer",
  "reddit_freelancer",
  "reddit_vibe_coder",
  "reddit_agent_skeptic",
  "reddit_tax_accountant",
];

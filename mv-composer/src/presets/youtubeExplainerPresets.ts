import { PersonaKey, getPersonaImages } from "../imageMap";
import { TextLine } from "../components/scenes/CinematicTextHook";

/* ═══════════════════ Types ═══════════════════ */

export interface YouTubeExplainerProps {
  persona: string;
  hookLines: TextLine[];
  hookStat: { value: string; label: string };
  painPoints: { title: string; detail: string }[];
  demoPrompt: string;
  demoSteps: { icon: string; label: string; detail: string; durationSec: number }[];
  resultStats: { label: string; before: string; after: string }[];
  ctaText: string;
  ctaUrl: string;
  bgImages: {
    hook: string;
    pain: string;
    solution: string;
    demo: string;
    result: string;
    cta: string;
  };
  bgmSrc: string;
  /** [hook, pain, demo1, demo2, demo3, stats, cta] — 7 sections totaling ~90s */
  sectionDurations: number[];
}

/* ═══════════════════ Presets ═══════════════════ */

interface PresetBase {
  hookLines: TextLine[];
  hookStat: { value: string; label: string };
  painPoints: { title: string; detail: string }[];
  demoPrompt: string;
  demoSteps: { icon: string; label: string; detail: string; durationSec: number }[];
  resultStats: { label: string; before: string; after: string }[];
  ctaText: string;
}

const PRESETS: Record<string, PresetBase> = {
  marketer: {
    hookLines: [
      { text: "マーケターの" },
      { text: "月40時間が", delayMs: 400 },
      { text: "月4時間に。", delayMs: 800 },
    ],
    hookStat: { value: "90%", label: "レポート作業時間削減" },
    painPoints: [
      { title: "GA4→スプレッドシートの手動コピペ", detail: "毎週月曜日の朝、GA4からスクリーンショットを撮ってスプレッドシートに貼り付ける" },
      { title: "5ツールからのデータ統合に半日", detail: "GA4、Meta Ads、Google Ads、メール配信ツール、CRMからデータを集めて一つのレポートに" },
      { title: "レポート作成で施策立案の時間がない", detail: "本来やるべきマーケティング戦略の立案や新施策のテストに時間を使えていない" },
    ],
    demoPrompt: "毎週月曜にGA4+Meta Ads+メールの統合レポートを自動生成して",
    demoSteps: [
      { icon: "M12 8v8m-4-4h8", label: "GA4 データ自動取得", detail: "API接続でpageview、session、conversionを自動取得", durationSec: 15 },
      { icon: "M9 5l7 7-7 7", label: "Meta Ads API 連携", detail: "CPA、ROAS、impressionを自動集計。キャンペーン横断で一覧化", durationSec: 15 },
      { icon: "M4 6h16M4 12h16m-7 6h7", label: "統合レポート自動生成", detail: "チャート、インサイト、改善提案まで含む週次レポートを生成", durationSec: 15 },
    ],
    resultStats: [
      { label: "レポート作業", before: "月40時間", after: "月4時間" },
      { label: "データ統合", before: "半日", after: "5分" },
      { label: "施策テスト回数", before: "月2回", after: "月8回" },
    ],
    ctaText: "レポート地獄から解放されよう",
  },
  sales: {
    hookLines: [
      { text: "営業の提案書が" },
      { text: "3時間→15分に。", delayMs: 400 },
    ],
    hookStat: { value: "80%", label: "提案書作成時間削減" },
    painPoints: [
      { title: "毎回ゼロから提案書を作成", detail: "過去の提案書をコピペして修正する作業に毎回3時間以上" },
      { title: "競合情報の収集が属人化", detail: "担当者ごとに情報ソースが異なり、チームで共有できていない" },
      { title: "提案書を作る時間で商談が減る", detail: "事務作業に追われて新規アポイントの時間が取れない" },
    ],
    demoPrompt: "競合3社の分析を元にSaaS導入の提案書を自動生成して",
    demoSteps: [
      { icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z", label: "競合情報の自動リサーチ", detail: "Web上の競合製品・価格・機能を自動収集して比較表に", durationSec: 15 },
      { icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z", label: "提案書テンプレート自動構成", detail: "顧客課題に合わせたストーリー構成で提案書のドラフトを生成", durationSec: 15 },
      { icon: "M4 6h16M4 12h16m-7 6h7", label: "PowerPoint出力", detail: "グラフ・図解付きのPPTXファイルとして自動出力。微修正だけで完成", durationSec: 15 },
    ],
    resultStats: [
      { label: "提案書作成", before: "3時間", after: "15分" },
      { label: "競合リサーチ", before: "2時間", after: "即時" },
      { label: "月間商談数", before: "12件", after: "20件" },
    ],
    ctaText: "営業の武器をAIで強化しよう",
  },
  accounting: {
    hookLines: [
      { text: "経理の月次締めが" },
      { text: "5日→1日に。", delayMs: 400 },
    ],
    hookStat: { value: "80%", label: "月次決算の短縮" },
    painPoints: [
      { title: "領収書・請求書の手入力が終わらない", detail: "紙の領収書をスキャンして目視で金額を確認し、仕訳帳に手入力" },
      { title: "部署ごとの経費集計に丸一日", detail: "各部署からバラバラに届くExcelを統合し、勘定科目を振り分ける作業" },
      { title: "月末に残業が集中する", detail: "月次締めの5日間は毎日終電。ミスが許されないプレッシャーの中での作業" },
    ],
    demoPrompt: "領収書画像をOCRで読み取り、自動仕訳して月次レポートを生成して",
    demoSteps: [
      { icon: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14", label: "OCR自動読み取り", detail: "領収書・請求書の画像からAIが金額・日付・取引先を自動抽出", durationSec: 15 },
      { icon: "M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01", label: "自動仕訳・分類", detail: "過去の仕訳パターンを学習し、勘定科目を自動で振り分け", durationSec: 15 },
      { icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10", label: "月次レポート生成", detail: "P/L・B/S・キャッシュフローを自動集計してレポートを出力", durationSec: 15 },
    ],
    resultStats: [
      { label: "月次決算", before: "5日", after: "1日" },
      { label: "入力ミス", before: "月5件", after: "月0件" },
      { label: "残業時間", before: "月40時間", after: "月5時間" },
    ],
    ctaText: "月末の残業地獄から解放されよう",
  },
  consultant: {
    hookLines: [
      { text: "リサーチ3日分を" },
      { text: "30分で完了。", delayMs: 400 },
    ],
    hookStat: { value: "95%", label: "リサーチ時間削減" },
    painPoints: [
      { title: "業界レポートの読み込みに3日", detail: "市場調査レポートを10本以上読み、要点を抽出してまとめる作業" },
      { title: "提案フレームワークの再構築が毎回", detail: "業界×課題の組み合わせごとにフレームワークを作り直す" },
      { title: "パートナー向け資料のクオリティ担保", detail: "複数のジュニアが作った資料のレビュー・統一に時間を取られる" },
    ],
    demoPrompt: "製造業DXの市場動向と競合3社の分析レポートを作成して",
    demoSteps: [
      { icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z", label: "市場データ自動収集", detail: "業界レポート・ニュース・財務情報をAIが横断的に収集", durationSec: 15 },
      { icon: "M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343", label: "フレームワーク自動適用", detail: "収集データをSWOT・5Forces等のフレームワークに自動整理", durationSec: 15 },
      { icon: "M4 6h16M4 12h16m-7 6h7", label: "プレゼン資料生成", detail: "グラフ・図解入りのコンサルクオリティ資料をPPTXで出力", durationSec: 15 },
    ],
    resultStats: [
      { label: "リサーチ", before: "3日", after: "30分" },
      { label: "レポート品質", before: "バラつき", after: "統一" },
      { label: "提案回転率", before: "月3案件", after: "月8案件" },
    ],
    ctaText: "コンサルの武器をAIで強化しよう",
  },
  lawyer: {
    hookLines: [
      { text: "契約書レビューが" },
      { text: "2時間→10分に。", delayMs: 400 },
    ],
    hookStat: { value: "90%", label: "レビュー時間短縮" },
    painPoints: [
      { title: "契約書の条項チェックに毎回2時間", detail: "NDA・業務委託契約書の一字一句を目視で確認する作業" },
      { title: "判例リサーチが膨大", detail: "関連判例を検索し、適用可能性を一つずつ確認する作業" },
      { title: "修正履歴の管理が煩雑", detail: "複数バージョンの契約書のどこが変わったか把握するのに時間がかかる" },
    ],
    demoPrompt: "この業務委託契約書のリスク条項を洗い出し、修正案を提示して",
    demoSteps: [
      { icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z", label: "契約書リスク分析", detail: "AIが条項を解析し、リスクの高い条項をハイライトで警告", durationSec: 15 },
      { icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z", label: "判例自動リサーチ", detail: "関連判例をAIが横断検索し、適用可能性をスコア付きで表示", durationSec: 15 },
      { icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z", label: "修正案の自動生成", detail: "リスク条項ごとに代替文言を自動提案。修正履歴も自動管理", durationSec: 15 },
    ],
    resultStats: [
      { label: "契約書レビュー", before: "2時間", after: "10分" },
      { label: "判例リサーチ", before: "半日", after: "5分" },
      { label: "見落としリスク", before: "年3件", after: "年0件" },
    ],
    ctaText: "契約書レビューをAIで効率化しよう",
  },
  planning: {
    hookLines: [
      { text: "企画書・LP作成が" },
      { text: "1週間→1日に。", delayMs: 400 },
    ],
    hookStat: { value: "85%", label: "企画制作時間削減" },
    painPoints: [
      { title: "企画書の構成に毎回悩む", detail: "ターゲット設定・ペルソナ・訴求軸を考えるだけで丸一日" },
      { title: "LP制作の外注コストが高い", detail: "1ページ30万円、修正のたびに追加費用。社内で作れない" },
      { title: "A/Bテストの実行が追いつかない", detail: "バリエーション制作に時間がかかり、テスト回数が限られる" },
    ],
    demoPrompt: "ターゲット30代女性向けのSaaS紹介LPを競合分析込みで作成して",
    demoSteps: [
      { icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z", label: "競合LP自動分析", detail: "競合3社のLPの構成・訴求・CTAを自動分析して差別化ポイントを特定", durationSec: 15 },
      { icon: "M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm0 8a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6z", label: "LP構成自動生成", detail: "ファーストビュー・ベネフィット・CTA配置まで自動設計", durationSec: 15 },
      { icon: "M4 6h16M4 12h16m-7 6h7", label: "HTML出力+ABテスト案", detail: "レスポンシブHTMLとして出力。ABテスト用のバリエーションも自動生成", durationSec: 15 },
    ],
    resultStats: [
      { label: "LP制作期間", before: "1週間", after: "1日" },
      { label: "制作コスト", before: "30万円", after: "0円" },
      { label: "ABテスト回数", before: "月1回", after: "月4回" },
    ],
    ctaText: "企画・LP制作をAIで加速しよう",
  },
  writer: {
    hookLines: [
      { text: "記事執筆が" },
      { text: "8時間→1時間に。", delayMs: 400 },
    ],
    hookStat: { value: "87%", label: "執筆時間削減" },
    painPoints: [
      { title: "リサーチに半日かかる", detail: "テーマに関する情報収集・ファクトチェックだけで4時間以上" },
      { title: "SEOと読みやすさの両立が難しい", detail: "キーワード配置を考えながら自然な文章を書くストレス" },
      { title: "量産すると品質が下がる", detail: "月10本以上の記事を書くとクオリティの維持が困難" },
    ],
    demoPrompt: "AI Agentの業務活用に関する3000字のSEO記事を執筆して",
    demoSteps: [
      { icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z", label: "自動リサーチ", detail: "テーマに関する最新情報・統計データ・事例を自動収集", durationSec: 15 },
      { icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z", label: "構成案+本文生成", detail: "SEO最適化された見出し構成で、H2/H3付きの本文を自動執筆", durationSec: 15 },
      { icon: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z", label: "品質チェック+最終調整", detail: "誤字脱字・ファクトチェック・コピー率を自動検証して完成", durationSec: 15 },
    ],
    resultStats: [
      { label: "記事執筆", before: "8時間", after: "1時間" },
      { label: "月間記事数", before: "4本", after: "15本" },
      { label: "検索順位", before: "圏外", after: "10位以内" },
    ],
    ctaText: "記事量産をAIで実現しよう",
  },
  exam_parent: {
    hookLines: [
      { text: "お子様の学習管理が" },
      { text: "自動化できる時代に。", delayMs: 400 },
    ],
    hookStat: { value: "60%", label: "学習効率向上" },
    painPoints: [
      { title: "何をどう勉強させればいいかわからない", detail: "教科書・塾・参考書の内容を把握して学習計画を立てるのが大変" },
      { title: "弱点の発見が遅れる", detail: "テスト結果を見て初めて苦手分野に気づく。手遅れになりがち" },
      { title: "親が付きっきりで教える時間がない", detail: "共働きで平日夜は疲れている。週末もやることが多い" },
    ],
    demoPrompt: "中学受験の算数、今週の弱点分析と最適な復習問題を出して",
    demoSteps: [
      { icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2", label: "学習データ自動分析", detail: "テスト結果・宿題の正答率から弱点分野をAIが自動特定", durationSec: 15 },
      { icon: "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253", label: "最適問題セット生成", detail: "弱点に合わせた復習問題を難易度順に自動生成", durationSec: 15 },
      { icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10", label: "進捗レポート自動送信", detail: "親御さんに週次で学習進捗レポートをメール送信", durationSec: 15 },
    ],
    resultStats: [
      { label: "弱点発見", before: "テスト後", after: "リアルタイム" },
      { label: "学習効率", before: "低い", after: "60%向上" },
      { label: "親の管理時間", before: "毎日1時間", after: "週15分" },
    ],
    ctaText: "お子様の学習をAIでサポートしよう",
  },
};

/* ═══════════════════ Build Full Props ═══════════════════ */

export function getYouTubeExplainerProps(persona: PersonaKey): YouTubeExplainerProps {
  const base = PRESETS[persona];
  if (!base) throw new Error(`YouTube preset not found for: ${persona}`);
  const images = getPersonaImages(persona);

  return {
    persona,
    ...base,
    ctaUrl: "ai-agent.camp",
    bgImages: {
      hook: images.hook,
      pain: images.pain,
      solution: images.solution,
      demo: images.solution,
      result: images.result,
      cta: images.cta,
    },
    bgmSrc: "tp/audio/bgm_v2_partA.mp3",
    // 7 sections totaling 90s
    // hook(8s), pain(12s), demo1(15s), demo2(15s), demo3(15s), stats(15s), cta(10s)
    sectionDurations: [8, 12, 15, 15, 15, 15, 10],
  };
}

export const YOUTUBE_PERSONAS: PersonaKey[] = [
  "marketer", "sales", "accounting", "consultant",
  "lawyer", "planning", "writer", "exam_parent",
];

#!/usr/bin/env node
/**
 * Generate AI images for GTM video backgrounds using fal.ai FLUX
 * Usage: node scripts/generate_images.mjs [--persona marketer] [--pro]
 */
import { fal } from "@fal-ai/client";
import { execSync } from "child_process";
import { existsSync, mkdirSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

const __dirname = dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: resolve(__dirname, "../../.env") });
fal.config({ credentials: process.env.FAL_KEY });

const OUT_BASE = resolve(__dirname, "../public/ac/generated");

// Parse args
const args = process.argv.slice(2);
const onlyPersona = args.includes("--persona") ? args[args.indexOf("--persona") + 1] : null;
const usePro = args.includes("--pro");
const MODEL = usePro ? "fal-ai/flux-pro/v1.1" : "fal-ai/flux/schnell";

/* ═══════════════════ Prompt Definitions ═══════════════════ */

const COMMON = [
  { name: "hook_dark", prompt: "dark modern japanese office at night, single laptop glowing on desk, dramatic blue ambient lighting, cinematic wide angle, moody atmosphere, no people, no text, 4k" },
  { name: "hook_numbers", prompt: "abstract data visualization with floating numbers and charts, dark background with blue and cyan glowing particles, futuristic holographic display, no text, cinematic" },
  { name: "solution_glow", prompt: "clean futuristic workspace with holographic AI interface floating above desk, blue and cyan neon glow, minimalist modern office, no people, no text, cinematic wide" },
  { name: "solution_process", prompt: "abstract neural network visualization, data flowing through connected nodes, dark background with blue cyan purple gradients, futuristic tech, no text" },
  { name: "result_celebration", prompt: "bright modern office with warm golden hour sunlight streaming through windows, clean organized desk, optimistic atmosphere, professional environment, no people, no text" },
  { name: "result_chart", prompt: "futuristic dashboard screen showing upward trending graphs and charts, dark UI with green and blue accents, data analytics visualization, no text, clean design" },
  { name: "cta_gradient", prompt: "abstract geometric gradient background, deep blue to cyan to purple smooth color flow, subtle light rays, premium corporate feel, no text, minimalist" },
  { name: "before_stress", prompt: "messy office desk covered in stacked papers and folders, dim overhead lighting casting shadows, stressed atmosphere, cluttered workspace, no people, no text" },
  { name: "before_overtime", prompt: "dark office at night with single desk lamp on, clock showing late hour, coffee cups on desk, overtime work atmosphere, no people, no text, cinematic" },
  { name: "transition_mesh", prompt: "abstract flowing mesh gradient, organic curves blending blue cyan and purple, smooth ethereal background, no text, wallpaper quality, 4k" },
];

const PERSONA_PROMPTS = {
  marketer: [
    { name: "desk", prompt: "modern marketing office desk with multiple screens showing analytics dashboards and ad campaigns, bright colorful charts, professional workspace, no people, no text" },
    { name: "pain", prompt: "overwhelming multiple browser tabs open on screen showing GA4 Meta Ads spreadsheets, cluttered data, stressful digital workspace, no people, no text" },
    { name: "demo", prompt: "clean marketing dashboard on modern monitor, automated report with charts and KPIs, AI-generated insights, sleek professional UI, no people, no text" },
    { name: "result", prompt: "creative brainstorming workspace with whiteboard full of campaign ideas, bright inspiring office, post-it notes and markers, no people, no text, optimistic" },
    { name: "tool", prompt: "modern SaaS marketing automation platform interface, clean UI with campaign workflows and analytics, blue accent colors, no people, no text" },
  ],
  sales: [
    { name: "desk", prompt: "sales team office with CRM dashboard on screen, phone headset on desk, client meeting notes, professional business environment, no people, no text" },
    { name: "pain", prompt: "CRM data entry screen with many empty fields, spreadsheet with follow-up tasks, overwhelming sales pipeline, tedious manual work feeling, no people, no text" },
    { name: "demo", prompt: "AI-powered CRM with automated follow-ups and smart suggestions, clean modern interface, green checkmarks, efficient workflow visualization, no people, no text" },
    { name: "result", prompt: "successful business meeting room with handshake moment atmosphere, bright confident setting, deal closed celebration feel, no people, no text, warm lighting" },
    { name: "tool", prompt: "modern CRM dashboard showing deal pipeline and automated email sequences, clean professional UI with blue accents, no people, no text" },
  ],
  accounting: [
    { name: "desk", prompt: "accounting office with calculator receipt stacks and tax forms on desk, accounting software on screen, meticulous organized workspace, no people, no text" },
    { name: "pain", prompt: "pile of paper receipts and invoices scattered on desk, calculator and pen, manual bookkeeping ledger open, overwhelming paperwork, no people, no text" },
    { name: "demo", prompt: "automated receipt scanning interface with AI extracting data from receipts, clean modern accounting software UI, green checkmarks, no people, no text" },
    { name: "result", prompt: "clean organized accounting desk with digital dashboard showing monthly reports, everything filed neatly, calm professional atmosphere, no people, no text" },
    { name: "tool", prompt: "modern cloud accounting software interface showing journal entries and financial reports, clean design with charts, professional blue theme, no people, no text" },
  ],
  consultant: [
    { name: "desk", prompt: "strategy consulting workspace with presentation slides on screen, research documents, premium modern office, professional atmosphere, no people, no text" },
    { name: "pain", prompt: "late night consulting work with multiple open research tabs and blank PowerPoint slides, deadline pressure atmosphere, dim lighting, no people, no text" },
    { name: "demo", prompt: "AI-generated market analysis report with charts competitive landscape and strategic recommendations, professional document layout, no people, no text" },
    { name: "result", prompt: "polished consulting deliverable presentation on large screen, executive boardroom setting, confident professional atmosphere, no people, no text" },
    { name: "tool", prompt: "competitive intelligence dashboard showing market trends and company comparisons, clean analytical interface, data visualization, no people, no text" },
  ],
  lawyer: [
    { name: "desk", prompt: "law office with legal books on shelf, contract documents on desk, laptop showing legal research, sophisticated professional workspace, no people, no text" },
    { name: "pain", prompt: "stacks of legal contracts and court documents covering desk, highlighted text with sticky notes, overwhelming legal review work, no people, no text" },
    { name: "demo", prompt: "AI contract review interface highlighting key clauses and risks, clean legal tech UI with green and red annotations, modern law tech, no people, no text" },
    { name: "result", prompt: "organized legal office with digital case management system on screen, everything filed and tracked, calm efficient atmosphere, no people, no text" },
    { name: "tool", prompt: "legal research platform showing case law and statute references, clean professional interface, judicial database visualization, no people, no text" },
  ],
  planning: [
    { name: "desk", prompt: "business planning office with market research reports and strategy documents, dual monitors showing data and presentations, no people, no text" },
    { name: "pain", prompt: "competitive analysis spreadsheet with many empty cells, market research tabs open, manual data gathering frustration, no people, no text" },
    { name: "demo", prompt: "AI-generated competitive analysis report with market maps and positioning charts, automated strategy document, clean professional layout, no people, no text" },
    { name: "result", prompt: "executive presentation room with polished business plan on screen, confident strategy meeting atmosphere, bright professional setting, no people, no text" },
    { name: "tool", prompt: "market intelligence platform showing industry trends and competitor tracking, clean analytical dashboard, professional blue theme, no people, no text" },
  ],
  writer: [
    { name: "desk", prompt: "content writer workspace with minimalist desk, large monitor showing blank document, coffee and notebook, creative atmosphere, no people, no text" },
    { name: "pain", prompt: "writers block scene with empty document cursor blinking, crumpled paper drafts, multiple research tabs open, frustrated creative process, no people, no text" },
    { name: "demo", prompt: "AI writing assistant generating structured article with headings and content, SEO analysis sidebar, clean modern editor interface, no people, no text" },
    { name: "result", prompt: "published blog post with beautiful typography and layout, social media shares counter, successful content marketing atmosphere, no people, no text" },
    { name: "tool", prompt: "modern content management system with AI writing tools, clean editor with sidebar suggestions, word count and SEO score, no people, no text" },
  ],
  exam_parent: [
    { name: "desk", prompt: "home study room for student with textbooks and exam prep materials on desk, warm family atmosphere, educational environment, no people, no text" },
    { name: "pain", prompt: "overwhelming pile of study guides test papers and reference books on student desk, anxiety-inducing exam preparation scene, no people, no text" },
    { name: "demo", prompt: "AI tutoring dashboard showing personalized study plan with progress tracking and practice tests, clean educational interface, colorful and encouraging, no people, no text" },
    { name: "result", prompt: "happy graduation celebration setup with diploma and flowers on desk, bright optimistic atmosphere, achievement and success mood, no people, no text" },
    { name: "tool", prompt: "educational AI platform showing adaptive learning path and quiz results, friendly modern UI with warm colors, progress charts, no people, no text" },
  ],
};

/* ═══════════════════ Generation ═══════════════════ */

async function generateImage(prompt) {
  const result = await fal.subscribe(MODEL, {
    input: {
      prompt,
      image_size: "landscape_16_9",
      num_images: 1,
      ...(usePro ? {} : { num_inference_steps: 4 }),
    },
    logs: true,
    onQueueUpdate(update) {
      if (update.status === "IN_PROGRESS") process.stdout.write(".");
    },
  });
  return result.data?.images?.[0]?.url;
}

async function downloadImage(url, outPath) {
  execSync(`curl -sL "${url}" -o "${outPath}"`);
}

async function processSet(category, items) {
  const outDir = resolve(OUT_BASE, category);
  if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });

  const results = [];
  for (const item of items) {
    const outPath = resolve(outDir, `${item.name}.png`);
    if (existsSync(outPath)) {
      console.log(`  Skip (exists): ${category}/${item.name}`);
      results.push({ name: item.name, status: "exists" });
      continue;
    }
    console.log(`  Generating: ${category}/${item.name}...`);
    try {
      const url = await generateImage(item.prompt);
      if (!url) { console.error(`  No URL`); results.push({ name: item.name, status: "failed" }); continue; }
      await downloadImage(url, outPath);
      console.log(` done`);
      results.push({ name: item.name, status: "ok", path: outPath });
    } catch (err) {
      console.error(`  Error: ${err.message}`);
      results.push({ name: item.name, status: "error", error: err.message });
    }
  }
  return results;
}

async function main() {
  console.log(`=== GTM Image Generation (${MODEL}) ===\n`);

  if (!process.env.FAL_KEY) {
    console.error("FAL_KEY not set in .env");
    process.exit(1);
  }

  const allResults = {};

  // Common images
  if (!onlyPersona) {
    console.log(`\n[common] ${COMMON.length} images`);
    allResults.common = await processSet("common", COMMON);
  }

  // Persona images
  const personas = onlyPersona ? [onlyPersona] : Object.keys(PERSONA_PROMPTS);
  for (const persona of personas) {
    if (!PERSONA_PROMPTS[persona]) { console.error(`Unknown persona: ${persona}`); continue; }
    console.log(`\n[${persona}] ${PERSONA_PROMPTS[persona].length} images`);
    allResults[persona] = await processSet(persona, PERSONA_PROMPTS[persona]);
  }

  // Summary
  const total = Object.values(allResults).flat();
  const ok = total.filter(r => r.status === "ok" || r.status === "exists").length;
  const failed = total.filter(r => r.status === "failed" || r.status === "error").length;
  console.log(`\n=== Done: ${ok} ok, ${failed} failed, ${total.length} total ===`);

  // Write manifest
  const manifest = {};
  for (const [cat, items] of Object.entries(allResults)) {
    manifest[cat] = {};
    for (const item of items) {
      if (item.status === "ok" || item.status === "exists") {
        manifest[cat][item.name] = `ac/generated/${cat}/${item.name}.png`;
      }
    }
  }
  writeFileSync(resolve(OUT_BASE, "manifest.json"), JSON.stringify(manifest, null, 2));
  console.log(`Manifest: ${resolve(OUT_BASE, "manifest.json")}`);
}

main().catch(console.error);

#!/usr/bin/env node
import { fal } from "@fal-ai/client";
import { execSync } from "child_process";
import { existsSync, mkdirSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

const __dirname = dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: resolve(__dirname, "../../.env") });
fal.config({ credentials: process.env.FAL_KEY });

const OUT_DIR = resolve(__dirname, "../public/tp/audio");

const PATTERNS = [
  {
    name: "clap_hard1",
    prompt: "heavy loud hand claps and stomps driving the beat, strong four on the floor kick drum, punchy snare, upbeat pop anthem, powerful and energetic, festival energy, 126 bpm, no vocals, loud percussion mix",
  },
  {
    name: "clap_hard2",
    prompt: "aggressive clap pattern with layered handclaps, hard hitting 808 kick drum, trap-pop hybrid beat, bright synth stabs, high energy corporate hype video, powerful drums up front, 130 bpm, no vocals",
  },
  {
    name: "clap_hard3",
    prompt: "stadium clap chant rhythm, boom clap boom boom clap pattern, massive kick and snare, epic pop rock energy, driving bass, anthemic build up, powerful and fresh, 128 bpm, no vocals, drums forward in mix",
  },
  {
    name: "clap_hard4",
    prompt: "thick layered handclap groove, punchy deep kick drum, crisp hi-hats, modern pop production, catchy melodic hook, strong beat emphasis, uplifting and powerful, 124 bpm, no vocals, percussion heavy mix",
  },
  {
    name: "clap_hard5",
    prompt: "double time clap pattern, hard hitting dance pop beat, strong bass drop, energetic and driving rhythm, festival main stage energy, bright lead synth, 132 bpm, no vocals, loud drums and claps",
  },
];

async function genAudio(prompt, duration) {
  const result = await fal.subscribe("fal-ai/stable-audio", {
    input: { prompt, duration },
    logs: true,
    onQueueUpdate(update) {
      if (update.status === "IN_PROGRESS" && update.logs) {
        update.logs.forEach(() => process.stdout.write("."));
      }
    },
  });
  return result.data?.audio_file?.url;
}

async function generateBGM(pattern) {
  console.log(`\nGenerating: ${pattern.name}...`);
  try {
    console.log(`  Half 1...`);
    const url1 = await genAudio(pattern.prompt, 47);
    if (!url1) { console.error("  No URL half 1"); return null; }

    console.log(`\n  Half 2...`);
    const url2 = await genAudio(pattern.prompt + ", building to climax, maximum energy", 47);
    if (!url2) { console.error("  No URL half 2"); return null; }

    const half1 = resolve(OUT_DIR, `bgm_${pattern.name}_h1.wav`);
    const half2 = resolve(OUT_DIR, `bgm_${pattern.name}_h2.wav`);
    execSync(`curl -sL "${url1}" -o "${half1}"`);
    execSync(`curl -sL "${url2}" -o "${half2}"`);
    console.log(`\n  Downloaded`);

    const fullPath = resolve(OUT_DIR, `bgm_${pattern.name}_full.mp3`);
    execSync(`ffmpeg -y -i "${half1}" -i "${half2}" -filter_complex "[0]afade=t=out:st=42:d=5[a];[1]afade=t=in:d=3[b];[a][b]concat=n=2:v=0:a=1" -q:a 2 "${fullPath}" 2>/dev/null`);
    console.log(`  Concat done`);
    execSync(`rm -f "${half1}" "${half2}"`);
    return pattern.name;
  } catch (err) {
    console.error(`  Error: ${err.message || err}`);
    return null;
  }
}

async function main() {
  console.log("=== Clap+Beat HARD BGM x5 ===");
  if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive: true });

  const results = [];
  for (const pattern of PATTERNS) {
    const name = await generateBGM(pattern);
    if (name) results.push(name);
  }
  console.log(`\n=== Done: ${results.length}/${PATTERNS.length} ===`);
}

main().catch(console.error);

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
    name: "clap_fresh1",
    prompt: "hand clap driven pop music, crisp snappy claps on every beat, bright whistle melody, fresh and refreshing summer feel, positive energy, corporate promo video, 122 bpm, C major, no vocals, clean mix",
  },
  {
    name: "clap_fresh2",
    prompt: "rhythmic hand claps with finger snaps, upbeat pop rock, clean electric guitar riff, refreshing breeze feeling, cheerful and light, presentation background music, 126 bpm, G major, no vocals",
  },
  {
    name: "clap_fresh3",
    prompt: "loud hand clap pattern, stomps and claps, anthemic pop, soaring synth pad, fresh and invigorating, stadium energy, inspiring corporate video music, 130 bpm, D major, no vocals",
  },
  {
    name: "clap_fresh4",
    prompt: "syncopated hand clap groove, bouncy pop beat, bright piano chords, xylophone melody, refreshing and playful, feel-good commercial music, 120 bpm, F major, no vocals, clean production",
  },
  {
    name: "clap_fresh5",
    prompt: "driving hand clap rhythm, uplifting pop anthem, bright brass fanfare, shimmering hi-hats, fresh morning energy, motivational corporate promo, 124 bpm, Bb major, no vocals",
  },
];

const SPLITS = [
  { name: "partA", start: 0, end: 21 },
  { name: "partB", start: 21, end: 55 },
  { name: "partC", start: 55, end: 75 },
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
    if (!url1) { console.error("  No URL for half 1"); return null; }

    console.log(`\n  Half 2...`);
    const url2 = await genAudio(pattern.prompt + ", building intensity, climax section", 47);
    if (!url2) { console.error("  No URL for half 2"); return null; }

    const half1 = resolve(OUT_DIR, `bgm_${pattern.name}_h1.wav`);
    const half2 = resolve(OUT_DIR, `bgm_${pattern.name}_h2.wav`);
    execSync(`curl -sL "${url1}" -o "${half1}"`);
    execSync(`curl -sL "${url2}" -o "${half2}"`);
    console.log(`\n  Downloaded`);

    const fullPath = resolve(OUT_DIR, `bgm_${pattern.name}_full.mp3`);
    execSync(`ffmpeg -y -i "${half1}" -i "${half2}" -filter_complex "[0]afade=t=out:st=42:d=5[a];[1]afade=t=in:d=3[b];[a][b]concat=n=2:v=0:a=1" -q:a 2 "${fullPath}" 2>/dev/null`);
    console.log(`  Concat done`);
    execSync(`rm -f "${half1}" "${half2}"`);

    for (const split of SPLITS) {
      const dur = split.end - split.start;
      const partPath = resolve(OUT_DIR, `bgm_${pattern.name}_${split.name}.mp3`);
      const fadeIn = split.start > 0 ? "afade=t=in:d=0.5," : "";
      const fadeOut = `afade=t=out:st=${dur - 1}:d=1`;
      execSync(`ffmpeg -y -ss ${split.start} -t ${dur + 2} -i "${fullPath}" -af "${fadeIn}${fadeOut}" -q:a 2 "${partPath}" 2>/dev/null`);
      console.log(`  ${split.name} done`);
    }
    return pattern.name;
  } catch (err) {
    console.error(`  Error: ${err.message || err}`);
    return null;
  }
}

async function main() {
  console.log("=== Clap-focused Fresh Pop BGM x5 ===");
  if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive: true });

  const results = [];
  for (const pattern of PATTERNS) {
    const name = await generateBGM(pattern);
    if (name) results.push(name);
  }
  console.log(`\n=== Done: ${results.length}/${PATTERNS.length} ===`);
  console.log("Generated:", results.join(", "));
}

main().catch(console.error);

#!/usr/bin/env node
/**
 * Generate 5 pop/clap BGM patterns via fal.ai (stable-audio)
 * stable-audio max ~47s, so generate 2 halves and concat
 * Then split into 3 parts for TwinPlanetIntro
 */
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
    name: "pop_bright",
    prompt: "upbeat bright pop music with clap beats, cheerful synth melody, energetic and positive corporate video background music, 120 bpm, major key, no vocals",
  },
  {
    name: "pop_funky",
    prompt: "funky pop music with handclap rhythm, groovy bass line, bright brass stabs, energetic and fun corporate video music, 125 bpm, major key, no vocals",
  },
  {
    name: "pop_tropical",
    prompt: "tropical pop music with clap beat, steel drums, bright marimba melody, uplifting and cheerful corporate presentation music, 115 bpm, major key, no vocals",
  },
  {
    name: "pop_electro",
    prompt: "electro pop music with clap snare, pulsing synth chords, bright arpeggios, modern and energetic corporate video soundtrack, 128 bpm, major key, no vocals",
  },
  {
    name: "pop_acoustic",
    prompt: "acoustic pop music with clap percussion, ukulele strumming, bright piano melody, warm and cheerful corporate video background music, 118 bpm, major key, no vocals",
  },
];

// Split points for 73s video
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
        update.logs.forEach((log) => process.stdout.write("."));
      }
    },
  });
  return result.data?.audio_file?.url;
}

async function generateBGM(pattern) {
  console.log(`\nGenerating: ${pattern.name}...`);

  try {
    // Generate 2 halves (45s each, overlap 5s for crossfade)
    console.log(`  Part 1/2 (0-45s)...`);
    const url1 = await genAudio(pattern.prompt, 47);
    if (!url1) { console.error("  No URL for part 1"); return null; }

    console.log(`\n  Part 2/2 (40-80s)...`);
    const url2 = await genAudio(pattern.prompt + ", continuation, building energy", 47);
    if (!url2) { console.error("  No URL for part 2"); return null; }

    // Download both halves
    const half1 = resolve(OUT_DIR, `bgm_${pattern.name}_h1.wav`);
    const half2 = resolve(OUT_DIR, `bgm_${pattern.name}_h2.wav`);
    execSync(`curl -sL "${url1}" -o "${half1}"`);
    execSync(`curl -sL "${url2}" -o "${half2}"`);
    console.log(`\n  Downloaded both halves`);

    // Concat with crossfade (5s overlap)
    const fullPath = resolve(OUT_DIR, `bgm_${pattern.name}_full.mp3`);
    execSync(`ffmpeg -y -i "${half1}" -i "${half2}" -filter_complex "[0]afade=t=out:st=42:d=5[a];[1]afade=t=in:d=3[b];[a][b]concat=n=2:v=0:a=1" -q:a 2 "${fullPath}" 2>/dev/null`);
    console.log(`  Concatenated: ${fullPath}`);

    // Clean up halves
    execSync(`rm -f "${half1}" "${half2}"`);

    // Split into 3 parts
    for (const split of SPLITS) {
      const dur = split.end - split.start;
      const partPath = resolve(OUT_DIR, `bgm_${pattern.name}_${split.name}.mp3`);
      const fadeIn = split.start > 0 ? "afade=t=in:d=0.5," : "";
      const fadeOut = `afade=t=out:st=${dur - 1}:d=1`;
      execSync(`ffmpeg -y -ss ${split.start} -t ${dur + 2} -i "${fullPath}" -af "${fadeIn}${fadeOut}" -q:a 2 "${partPath}" 2>/dev/null`);
      console.log(`  Split: ${split.name} (${split.start}s-${split.end}s)`);
    }

    return pattern.name;
  } catch (err) {
    console.error(`  Error: ${err.message || err}`);
    return null;
  }
}

async function main() {
  console.log("=== BGM Generation: 5 Pop/Clap Patterns ===");
  if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive: true });

  const results = [];
  for (const pattern of PATTERNS) {
    const name = await generateBGM(pattern);
    if (name) results.push(name);
  }

  console.log(`\n=== Done: ${results.length}/${PATTERNS.length} ===`);
  console.log("Patterns:", results.join(", "));
}

main().catch(console.error);

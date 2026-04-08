#!/usr/bin/env node
/**
 * Generate product-intro BGM for TaxAccountantDemo (73.2s)
 * stable-audio max ~47s → generate 2 halves + crossfade concat
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

const OUT_DIR = resolve(__dirname, "../public/tax/audio");

const PROMPT_PART1 =
  "upbeat modern corporate product introduction music, bright piano and light synth, " +
  "confident and professional, clap snare rhythm, 120 bpm, major key, " +
  "inspiring and energetic, Japanese tech company presentation style, no vocals, high quality";

const PROMPT_PART2 =
  "upbeat modern corporate product introduction music continuation, bright piano and light synth, " +
  "building to emotional climax, clap snare rhythm, 120 bpm, major key, " +
  "inspiring call-to-action energy, Japanese tech company presentation style, no vocals, high quality";

async function genAudio(prompt, duration) {
  console.log(`  Generating ${duration}s audio...`);
  const result = await fal.subscribe("fal-ai/stable-audio", {
    input: { prompt, duration },
    logs: true,
    onQueueUpdate(update) {
      if (update.status === "IN_PROGRESS" && update.logs) {
        update.logs.forEach(() => process.stdout.write("."));
      }
    },
  });
  console.log();
  return result.data?.audio_file?.url;
}

async function main() {
  console.log("=== BGM Generation: TaxAccountantDemo (73.2s) ===");
  if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive: true });

  // Part 1: 0-45s
  console.log("\nPart 1/2 (0-45s)...");
  const url1 = await genAudio(PROMPT_PART1, 47);
  if (!url1) { console.error("No URL for part 1"); return; }

  // Part 2: overlap zone → end
  console.log("Part 2/2 (40-80s)...");
  const url2 = await genAudio(PROMPT_PART2, 47);
  if (!url2) { console.error("No URL for part 2"); return; }

  // Download
  const h1 = resolve(OUT_DIR, "bgm_tax_h1.wav");
  const h2 = resolve(OUT_DIR, "bgm_tax_h2.wav");
  execSync(`curl -sL "${url1}" -o "${h1}"`);
  execSync(`curl -sL "${url2}" -o "${h2}"`);
  console.log("Downloaded both halves");

  // Concat with 5s crossfade, total target ~80s, then trim to 76s (73.2 + 3s fadeout margin)
  const fullPath = resolve(OUT_DIR, "bgm_tax_v3.mp3");
  execSync(
    `ffmpeg -y -i "${h1}" -i "${h2}" ` +
    `-filter_complex "[0]afade=t=out:st=42:d=5[a];[1]afade=t=in:d=3[b];[a][b]concat=n=2:v=0:a=1,afade=t=out:st=73:d=3.2" ` +
    `-t 76.2 -q:a 2 "${fullPath}" 2>/dev/null`
  );
  console.log(`\nFull BGM: ${fullPath}`);

  // Clean up
  execSync(`rm -f "${h1}" "${h2}"`);

  // Verify duration
  const dur = execSync(`ffprobe -v quiet -show_entries format=duration -of csv=p=0 "${fullPath}"`).toString().trim();
  console.log(`Duration: ${dur}s (target: ~76.2s)`);
  console.log("Done!");
}

main().catch(console.error);

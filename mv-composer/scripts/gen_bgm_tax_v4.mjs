#!/usr/bin/env node
/**
 * Generate 80s BGM for TaxAccountantDemo using Stable Audio 2.5
 * Single generation (no crossfade joints) — max 190s supported
 */
import { fal } from "@fal-ai/client";
import { execFileSync } from "child_process";
import { createWriteStream, existsSync, mkdirSync, unlinkSync } from "fs";
import https from "https";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

const __dirname = dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: resolve(__dirname, "../../.env") });

fal.config({ credentials: process.env.FAL_KEY });

const OUT_DIR = resolve(__dirname, "../public/tax/audio");
const DURATION = 80; // 73.2s video + margin for fadeout

const PROMPT =
  "catchy modern TV commercial music for a tech product ad, " +
  "starts with bright synth stabs and snappy claps building anticipation, " +
  "transitions into a confident driving beat with melodic piano hook and electronic arpeggios, " +
  "builds energy through the middle section with layered percussion and uplifting chords, " +
  "resolves into an inspiring triumphant finale, " +
  "128 bpm, major key, polished and sleek like an Apple or Google product launch ad, " +
  "no vocals, high quality stereo, professional mixing";

async function main() {
  console.log("=== BGM Generation: Stable Audio 2.5 (single 80s) ===");
  console.log(`Duration: ${DURATION}s | Prompt: ${PROMPT.slice(0, 80)}...`);
  console.log();

  if (!existsSync(OUT_DIR)) mkdirSync(OUT_DIR, { recursive: true });

  console.log("Generating...");
  const result = await fal.subscribe("fal-ai/stable-audio-25/text-to-audio", {
    input: {
      prompt: PROMPT,
      seconds_total: DURATION,
    },
    logs: true,
    onQueueUpdate(update) {
      if (update.status === "IN_PROGRESS" && update.logs) {
        update.logs.forEach(() => process.stdout.write("."));
      }
    },
  });
  console.log();

  const url = result.data?.audio_file?.url || result.data?.audio?.url;
  if (!url) {
    console.error("No audio URL returned");
    console.log("Full response:", JSON.stringify(result.data, null, 2));
    return;
  }

  // Validate URL before downloading
  const parsedUrl = new URL(url);
  if (parsedUrl.protocol !== "https:") {
    throw new Error(`Unexpected protocol: ${parsedUrl.protocol}`);
  }

  const rawPath = resolve(OUT_DIR, "bgm_tax_v5_raw.wav");
  await new Promise((res, rej) => {
    const file = createWriteStream(rawPath);
    https.get(url, (response) => {
      response.pipe(file);
      file.on("finish", () => { file.close(); res(); });
    }).on("error", rej);
  });
  console.log("Downloaded raw audio");

  // Add 4s fadeout at the end and convert to mp3
  const finalPath = resolve(OUT_DIR, "bgm_tax_v5.mp3");
  const fadeStart = DURATION - 4;
  execFileSync("ffmpeg", [
    "-y", "-i", rawPath,
    "-af", `afade=t=out:st=${fadeStart}:d=4`,
    "-q:a", "2", finalPath,
  ], { stdio: "ignore" });

  const dur = execFileSync("ffprobe", [
    "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", finalPath,
  ]).toString().trim();
  console.log(`\nFinal BGM: ${finalPath}`);
  console.log(`Duration: ${dur}s (target: ~${DURATION}s for 73.2s video)`);

  // Cleanup
  unlinkSync(rawPath);
  console.log("Done!");
}

main().catch(console.error);

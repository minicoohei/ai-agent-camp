#!/usr/bin/env node
/**
 * Generate i2v video backgrounds for TaxAccountantDemo
 * Step 1: Generate source images with FLUX
 * Step 2: Convert to video with Kling i2v
 *
 * Usage: node scripts/generate_tax_i2v.mjs [--step images|videos|all] [--scene s01|s15|s16|s19]
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

const OUT_DIR = resolve(__dirname, "../public/tax/i2v");
const IMG_DIR = resolve(OUT_DIR, "src_images");
if (!existsSync(IMG_DIR)) mkdirSync(IMG_DIR, { recursive: true });

/* ═══════════════════ Scene Definitions ═══════════════════ */

const SCENES = {
  s01_hook: {
    imagePrompt:
      "overwhelming pile of paper tax documents receipts and accounting ledgers on wooden desk, calculator and pen, dim overhead lighting, stressed atmosphere, japanese office, no people, no text, cinematic wide angle, 4k",
    videoPrompt:
      "slow camera dolly across cluttered desk, papers gently shifting in air conditioning breeze, warm desk lamp flickering subtly",
    duration: "5",
  },
  s15_painpoints: {
    imagePrompt:
      "worried japanese businessperson silhouette standing in front of massive wall of question marks and exclamation marks, dark moody blue lighting, abstract data visualization in background, uncertainty atmosphere, no text, cinematic",
    videoPrompt:
      "slow zoom in with particles floating, question marks gently rotating, dramatic lighting shifts from blue to warm",
    duration: "5",
  },
  s16_safeenv: {
    imagePrompt:
      "bright modern japanese office workshop room with large screens showing friendly AI interface, warm sunlight streaming through windows, clean organized workspace, welcoming atmosphere, plants on desks, no people, no text, optimistic cinematic",
    videoPrompt:
      "gentle camera pan right revealing bright workspace, sunlight rays slowly moving across desk, warm inviting atmosphere",
    duration: "5",
  },
  s19_cta: {
    imagePrompt:
      "futuristic holographic AI assistant interface floating above modern desk, blue and cyan neon glow, abstract neural network connections in background, clean minimalist office, inspiring future of work, no people, no text, cinematic 4k",
    videoPrompt:
      "slow zoom out revealing full holographic display, particles and data streams flowing upward, blue light pulsing gently",
    duration: "5",
  },
};

/* ═══════════════════ Image Generation (FLUX) ═══════════════════ */

async function generateImage(scene, name) {
  const outPath = resolve(IMG_DIR, `${name}.png`);
  if (existsSync(outPath)) {
    console.log(`  [img] Skip (exists): ${name}`);
    return outPath;
  }
  console.log(`  [img] Generating: ${name}...`);
  const result = await fal.subscribe("fal-ai/flux/schnell", {
    input: {
      prompt: scene.imagePrompt,
      image_size: "landscape_16_9",
      num_images: 1,
      num_inference_steps: 4,
    },
    logs: true,
    onQueueUpdate(u) {
      if (u.status === "IN_PROGRESS") process.stdout.write(".");
    },
  });
  const url = result.data?.images?.[0]?.url;
  if (!url) throw new Error("No image URL returned");
  execSync(`curl -sL "${url}" -o "${outPath}"`);
  console.log(` done → ${outPath}`);
  return outPath;
}

/* ═══════════════════ i2v Generation (Kling) ═══════════════════ */

async function generateVideo(scene, name, imagePath) {
  const outPath = resolve(OUT_DIR, `${name}.mp4`);
  if (existsSync(outPath)) {
    console.log(`  [vid] Skip (exists): ${name}`);
    return outPath;
  }
  console.log(`  [vid] Generating i2v: ${name}...`);

  // Upload image to get a URL
  const imageUrl = await uploadImage(imagePath);

  const result = await fal.subscribe("fal-ai/kling-video/v1/standard/image-to-video", {
    input: {
      prompt: scene.videoPrompt,
      image_url: imageUrl,
      duration: scene.duration,
      aspect_ratio: "16:9",
    },
    logs: true,
    onQueueUpdate(u) {
      if (u.status === "IN_PROGRESS") process.stdout.write(".");
      if (u.status === "IN_QUEUE") console.log(`    Queue position: ${u.queue_position || "?"}`);
    },
  });

  const videoUrl = result.data?.video?.url;
  if (!videoUrl) {
    console.error("  No video URL. Response:", JSON.stringify(result.data, null, 2));
    throw new Error("No video URL returned");
  }
  execSync(`curl -sL "${videoUrl}" -o "${outPath}"`);
  console.log(` done → ${outPath}`);
  return outPath;
}

async function uploadImage(imagePath) {
  // Use fal storage to upload
  const file = await import("fs").then((fs) => fs.readFileSync(imagePath));
  const blob = new Blob([file], { type: "image/png" });
  const url = await fal.storage.upload(blob);
  return url;
}

/* ═══════════════════ Main ═══════════════════ */

async function main() {
  const args = process.argv.slice(2);
  const step = args.includes("--step") ? args[args.indexOf("--step") + 1] : "all";
  const onlyScene = args.includes("--scene") ? args[args.indexOf("--scene") + 1] : null;

  if (!process.env.FAL_KEY) {
    console.error("FAL_KEY not set in .env");
    process.exit(1);
  }

  const scenes = onlyScene
    ? { [onlyScene]: SCENES[onlyScene] }
    : SCENES;

  if (!Object.keys(scenes).length || Object.values(scenes).some((v) => !v)) {
    console.error("Invalid scene name. Available:", Object.keys(SCENES).join(", "));
    process.exit(1);
  }

  console.log(`=== TaxAccountantDemo i2v Generation ===`);
  console.log(`Step: ${step} | Scenes: ${Object.keys(scenes).join(", ")}\n`);

  const results = [];

  for (const [name, scene] of Object.entries(scenes)) {
    console.log(`\n── ${name} ──`);
    try {
      let imagePath;
      if (step === "images" || step === "all") {
        imagePath = await generateImage(scene, name);
      } else {
        imagePath = resolve(IMG_DIR, `${name}.png`);
        if (!existsSync(imagePath)) {
          console.error(`  Image not found: ${imagePath}. Run --step images first.`);
          continue;
        }
      }

      if (step === "videos" || step === "all") {
        await generateVideo(scene, name, imagePath);
      }

      results.push({ name, status: "ok" });
    } catch (err) {
      console.error(`  ERROR: ${err.message}`);
      results.push({ name, status: "error", error: err.message });
    }
  }

  console.log(`\n=== Summary ===`);
  for (const r of results) {
    console.log(`  ${r.name}: ${r.status}${r.error ? ` (${r.error})` : ""}`);
  }
  console.log(`\nOutput: ${OUT_DIR}`);
}

main().catch(console.error);

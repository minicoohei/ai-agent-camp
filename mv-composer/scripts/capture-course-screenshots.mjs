import { chromium } from "playwright";
import { join } from "path";

const OUT_DIR = join(import.meta.dirname, "../public/course-assets");
const BASE = "http://localhost:3000";

const MODULES = [
  { id: "module-0", file: "course_01.png" },
  { id: "foundation-1", file: "course_02.png" },
  { id: "foundation-3", file: "course_03.png" },
  { id: "module-1", file: "course_04.png" },
  { id: "module-2", file: "course_05.png" },
  { id: "module-5", file: "course_06.png" },
  { id: "module-8", file: "course_07.png" },
  { id: "module-10", file: "course_08.png" },
  { id: "module-13", file: "course_09.png" },
];

async function main() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    locale: "ja-JP",
  });

  for (const mod of MODULES) {
    const page = await context.newPage();
    const url = `${BASE}/ja/course/${mod.id}`;
    console.log(`Capturing ${url} → ${mod.file}`);
    try {
      await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
      // Wait a bit for any animations to settle
      await page.waitForTimeout(2000);
      await page.screenshot({ path: join(OUT_DIR, mod.file) });
      console.log(`  ✓ ${mod.file}`);
    } catch (e) {
      console.error(`  ✗ ${mod.file}: ${e.message}`);
    }
    await page.close();
  }

  await browser.close();
  console.log("Done!");
}

main();

"""
Banner Pipeline - バナー自動生成パイプライン

サイズ × 訴求のクロス積でバナーをバッチ生成し、
Gemini Vision で品質スコアリング → 自動選定まで全自動で実行する。

banner-creator スキルの発展版。1枚ずつ手動で作るのではなく、
「複数サイズ × 複数訴求を一括生成して、AIが品質判定して良いものを選ぶ」パイプライン。

Usage:
    uv run python tools/banner_pipeline.py \
      --sizes "1200x675,1080x1080,300x250" \
      --appeals "AIエージェント研修,業務効率3倍,非エンジニアでもできる" \
      --brand "AI Agent Camp" --price "月額12,800円" \
      --session my_campaign --top-k 2

    # ロゴ合成する場合
    uv run python tools/banner_pipeline.py \
      --sizes "240x120,200x120" \
      --appeals "Claude Code実践講座,AIを武器にする" \
      --logo path/to/logo.png \
      --session a8_banners --top-k 3
"""

import argparse
import base64
import json
import os
import shutil
import sys
import tempfile
import time
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env
from bootcamp_utils import get_client, get_image_model

load_runtime_env()

from PIL import Image, ImageDraw  # noqa: E402
from google.genai import types  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path("output/banners")
IMAGE_MODEL = None  # Set dynamically from get_image_model()
VISION_MODEL = "gemini-2.0-flash"

BASE_PROMPT = (
    "Create a professional banner ad for a Japanese EdTech product. "
    "{white_top_instruction}"
    "Style: Clean, modern, premium Japanese EdTech. "
    "Primary: white and blue (#2563EB). Subtle gradients, light shadows. "
    "Typography: sharp, readable Japanese text — NO garbled text. "
    "Include '{brand}' branding and price '{price}'. "
    "Do NOT include buttons, CTA, or '無料体験'. "
)

VISION_PROMPT = """\
You are a harsh, senior creative director at a top-tier ad agency.
Score this banner ad STRICTLY on 4 dimensions (each 0-25, total 100).

**Design (0-25):** Visual sophistication. Flat text-only = max 14.
**Visibility (0-25):** Text readability, contrast, Japanese accuracy.
  If ANY mojibake (garbled Japanese) → score 0-5.
**Persuasion (0-25):** Copy strength, emotional hook, value clarity.
**CTR (0-25):** Would you click this? Be honest.

Flags: mojibake (garbled text), alignment_issues
Verdict: "approve" (≥80, no issues), "review" (60-79), "reject" (<60 or issues)

Respond ONLY in JSON:
{"design":N,"visibility":N,"persuasion":N,"ctr":N,"mojibake":BOOL,"alignment_issues":BOOL,"issues":["..."],"verdict":"..."}
"""


# ---------------------------------------------------------------------------
# Step 1: Generate banners
# ---------------------------------------------------------------------------

def generate_banners(client, sizes, appeals, brand, price, out_dir, logo_path=None):
    """Generate banners for all size × appeal combinations."""
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    model = get_image_model()

    for w, h in sizes:
        white_top = max(20, int(h * 0.23)) if logo_path else 0
        gen_w, gen_h = min(w * 2, 2048), min(h * 2, 2048)

        white_instruction = ""
        if logo_path:
            white_instruction = (
                f"CRITICAL: The TOP {white_top * 2} pixels MUST be plain white "
                "— NO text, NO logo, NO graphics there. "
            )

        for i, appeal in enumerate(appeals, 1):
            slug = f"{w}x{h}_{i:02d}"
            out_path = out_dir / f"{slug}.png"

            if out_path.exists():
                print(f"  SKIP: {slug}")
                generated.append(out_path)
                continue

            prompt = (
                f"Create a banner ad ({gen_w}x{gen_h} pixels). "
                + BASE_PROMPT.format(
                    white_top_instruction=white_instruction,
                    brand=brand, price=price)
                + f"Main headline: '{appeal}' bold, prominent. "
            )

            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE", "TEXT"]),
                )
                for part in response.candidates[0].content.parts:
                    if (part.inline_data
                            and part.inline_data.mime_type.startswith("image/")):
                        img = Image.open(
                            BytesIO(part.inline_data.data)).convert("RGBA")
                        img = img.resize((w, h), Image.LANCZOS)
                        img.convert("RGB").save(out_path, "PNG")
                        print(f"  OK: {slug} ({appeal})")
                        generated.append(out_path)
                        break
                else:
                    print(f"  WARN: No image for {slug}")
            except Exception as e:
                print(f"  ERROR: {slug}: {e}")

            time.sleep(2)

    return generated


# ---------------------------------------------------------------------------
# Step 2: Logo overlay (optional)
# ---------------------------------------------------------------------------

def overlay_logo(images, logo_path):
    """Apply white strip + logo overlay to all generated images."""
    logo_src = Image.open(logo_path).convert("RGBA")

    for img_path in images:
        img = Image.open(img_path).convert("RGBA")
        w, h = img.size
        white_top = max(20, int(h * 0.23))
        logo_h = int(white_top * 0.7)

        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, w, white_top], fill=(255, 255, 255, 255))

        lw = int(logo_src.width * logo_h / logo_src.height)
        logo_r = logo_src.resize((lw, logo_h), Image.LANCZOS)
        logo_x = (w - lw) // 2 if w < 400 else 6
        logo_y = (white_top - logo_h) // 2
        img.paste(logo_r, (logo_x, logo_y), logo_r)

        img.convert("RGB").save(img_path, "PNG")


# ---------------------------------------------------------------------------
# Step 3: Vision scoring
# ---------------------------------------------------------------------------

def score_banners(client, images, cache_path):
    """Score each image with Gemini Vision."""
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    results = []
    scored = 0

    for img_path in images:
        key = img_path.name
        if key in cache:
            results.append({"path": img_path, **cache[key]})
            continue

        try:
            upload_path = str(img_path)
            tmp_file = None
            try:
                upload_path.encode("ascii")
            except UnicodeEncodeError:
                tmp_file = tempfile.NamedTemporaryFile(
                    suffix=img_path.suffix, delete=False)
                tmp_file.write(img_path.read_bytes())
                tmp_file.close()
                upload_path = tmp_file.name

            uploaded = None
            for attempt in range(3):
                try:
                    uploaded = client.files.upload(file=upload_path)
                    break
                except Exception as ue:
                    if attempt < 2:
                        time.sleep(3 * (attempt + 1))
                    else:
                        raise ue

            if tmp_file:
                Path(tmp_file.name).unlink(missing_ok=True)
            time.sleep(1)

            response = client.models.generate_content(
                model=VISION_MODEL, contents=[VISION_PROMPT, uploaded])

            text = response.text.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()

            result = json.loads(text)
            scores = {
                "design": max(0, min(25, int(result.get("design", 15)))),
                "visibility": max(0, min(25, int(result.get("visibility", 15)))),
                "persuasion": max(0, min(25, int(result.get("persuasion", 15)))),
                "ctr": max(0, min(25, int(result.get("ctr", 15)))),
            }
            total = sum(scores.values())
            mojibake = result.get("mojibake", False)
            verdict = result.get("verdict", "review")
            if mojibake:
                verdict = "reject"

            entry = {
                "scores": scores, "total": total,
                "mojibake": mojibake,
                "alignment_issues": result.get("alignment_issues", False),
                "issues": result.get("issues", []),
                "verdict": verdict,
            }
            cache[key] = entry
            results.append({"path": img_path, **entry})
            scored += 1

            if scored % 5 == 0:
                cache_path.write_text(
                    json.dumps(cache, ensure_ascii=False, indent=2),
                    encoding="utf-8")

            time.sleep(1.5)

        except Exception as e:
            print(f"  WARN: Scoring failed for {img_path.name}: {e}",
                  file=sys.stderr)
            results.append({
                "path": img_path,
                "scores": {"design": 0, "visibility": 0,
                           "persuasion": 0, "ctr": 0},
                "total": 0, "verdict": "reject",
                "mojibake": False, "alignment_issues": False,
                "issues": [str(e)],
            })

    cache_path.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Vision: {scored} scored, {len(results) - scored} cached")
    return results


# ---------------------------------------------------------------------------
# Step 4: Auto-select
# ---------------------------------------------------------------------------

def select_top_k(results, sizes, top_k, approved_dir):
    """Select top-K banners per size."""
    approved_dir.mkdir(parents=True, exist_ok=True)
    selected = []

    for w, h in sizes:
        prefix = f"{w}x{h}_"
        size_results = [
            r for r in results
            if r["path"].name.startswith(prefix)
            and r["verdict"] != "reject"
        ]
        size_results.sort(key=lambda r: r["total"], reverse=True)

        for r in size_results[:top_k]:
            dst = approved_dir / r["path"].name
            shutil.copy2(r["path"], dst)
            r["approved"] = True
            selected.append(r)
            print(f"  APPROVED: {r['path'].name} (score={r['total']})")

    return selected


# ---------------------------------------------------------------------------
# Step 5: Review HTML
# ---------------------------------------------------------------------------

def build_review_html(results, session_dir):
    """Generate a self-contained review HTML."""
    cards = ""
    for r in sorted(results, key=lambda x: x["total"], reverse=True):
        img = Image.open(r["path"])
        buf = BytesIO()
        img.save(buf, "PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        w, h = img.size
        s = r["scores"]
        total = r["total"]
        badge = ("score-s" if total >= 88 else "score-a" if total >= 80
                 else "score-b" if total >= 70 else "score-c")
        verdict = r.get("verdict", "")
        flags = ""
        if r.get("mojibake"):
            flags += '<span class="f fr">MOJIBAKE</span>'
        if verdict == "approve":
            flags += '<span class="f fg">OK</span>'
        elif verdict == "reject":
            flags += '<span class="f fr">REJECT</span>'
        if r.get("approved"):
            flags += '<span class="f fb">TOP-K</span>'

        cards += f'''
<div class="c{' rej' if verdict=='reject' else ''}">
  <div class="b {badge}">{total}</div>
  <img src="data:image/png;base64,{b64}">
  <div class="i">
    <div class="n">{r['path'].name}</div>
    <div class="m">{w}x{h}</div>
    <div class="fl">{flags}</div>
    <div class="sc">
      <div class="sr"><span>Design</span><div class="t"><div class="f1" style="width:{s['design']*4}%;background:#3B82F6"></div></div><span>{s['design']}</span></div>
      <div class="sr"><span>Visibility</span><div class="t"><div class="f1" style="width:{s['visibility']*4}%;background:#059669"></div></div><span>{s['visibility']}</span></div>
      <div class="sr"><span>Persuasion</span><div class="t"><div class="f1" style="width:{s['persuasion']*4}%;background:#F59E0B"></div></div><span>{s['persuasion']}</span></div>
      <div class="sr"><span>CTR</span><div class="t"><div class="f1" style="width:{s['ctr']*4}%;background:#EF4444"></div></div><span>{s['ctr']}</span></div>
    </div>
  </div>
</div>'''

    html = f'''<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<title>Banner Pipeline Review</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,sans-serif;background:#0F172A;color:#E2E8F0;padding:24px}}
h1{{font-size:1.5rem;margin-bottom:16px}}
.st{{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap}}
.sv{{background:#1E293B;padding:10px 16px;border-radius:8px;text-align:center}}
.sv .num{{font-size:1.6rem;font-weight:700;color:#3B82F6}}
.sv .lab{{font-size:.7rem;color:#94A3B8}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}
.c{{background:#1E293B;border-radius:12px;overflow:hidden;position:relative}}
.c.rej{{opacity:.4}}
.c img{{width:100%;display:block;background:#fff}}
.b{{position:absolute;top:8px;right:8px;padding:4px 10px;border-radius:6px;font-weight:700;z-index:2}}
.score-s{{background:linear-gradient(135deg,#F59E0B,#EF4444);color:#fff}}
.score-a{{background:#059669;color:#fff}}
.score-b{{background:#3B82F6;color:#fff}}
.score-c{{background:#64748B;color:#fff}}
.i{{padding:10px}}
.n{{font-weight:600;font-size:.85rem}}
.m{{font-size:.7rem;color:#94A3B8;margin:4px 0}}
.fl{{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px}}
.f{{padding:2px 6px;border-radius:4px;font-size:.65rem;font-weight:600}}
.fr{{background:#DC2626;color:#fff}}.fg{{background:#059669;color:#fff}}.fb{{background:#3B82F6;color:#fff}}
.sc{{display:flex;flex-direction:column;gap:3px}}
.sr{{display:flex;align-items:center;gap:4px;font-size:.65rem;color:#94A3B8}}
.sr span:first-child{{width:60px}}
.t{{flex:1;height:5px;background:#334155;border-radius:3px;overflow:hidden}}
.f1{{height:100%;border-radius:3px}}
.sr span:last-child{{width:16px;text-align:right}}
</style></head><body>
<h1>Banner Pipeline Review</h1>
<div class="st">
  <div class="sv"><div class="num">{len(results)}</div><div class="lab">Total</div></div>
  <div class="sv"><div class="num">{sum(1 for r in results if r.get('verdict')=='approve')}</div><div class="lab">Approved</div></div>
  <div class="sv"><div class="num">{sum(1 for r in results if r.get('verdict')=='reject')}</div><div class="lab">Rejected</div></div>
  <div class="sv"><div class="num">{sum(1 for r in results if r.get('approved'))}</div><div class="lab">Top-K</div></div>
</div>
<div class="g">{cards}</div>
</body></html>'''

    out = session_dir / "review.html"
    out.write_text(html, encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Banner auto-generation pipeline")
    parser.add_argument("--sizes", required=True,
                        help="Comma-separated WxH (e.g. 240x120,300x250)")
    parser.add_argument("--appeals", required=True,
                        help="Comma-separated appeal headlines")
    parser.add_argument("--logo",
                        help="Path to logo PNG for overlay (optional)")
    parser.add_argument("--brand", default="AI Agent Camp")
    parser.add_argument("--price", default="月額12,800円")
    parser.add_argument("--session", default="default",
                        help="Session name for output directory")
    parser.add_argument("--top-k", type=int, default=3,
                        help="Select top-K per size (default: 3)")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR),
                        help="Base output directory")
    parser.add_argument("--skip-scoring", action="store_true",
                        help="Skip vision scoring")

    args = parser.parse_args()

    sizes = []
    for s in args.sizes.split(","):
        parts = s.strip().lower().split("x")
        sizes.append((int(parts[0]), int(parts[1])))

    appeals = [a.strip() for a in args.appeals.split(",") if a.strip()]

    logo_path = Path(args.logo).resolve() if args.logo else None
    if logo_path and not logo_path.exists():
        print(f"ERROR: Logo not found: {logo_path}", file=sys.stderr)
        sys.exit(1)

    session_dir = Path(args.output_dir) / args.session
    gen_dir = session_dir / "generated"
    approved_dir = session_dir / "approved"
    cache_path = session_dir / "vision_cache.json"

    total = len(sizes) * len(appeals)
    print(f"Banner Pipeline: {total} banners "
          f"({len(sizes)} sizes × {len(appeals)} appeals)\n")

    client = get_client()
    if not client:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Step 1
    print("=== Step 1: Generate ===")
    images = generate_banners(
        client, sizes, appeals, args.brand, args.price, gen_dir, logo_path)
    print(f"  Generated: {len(images)} images\n")

    # Step 2 (optional)
    if logo_path:
        print("=== Step 2: Logo Overlay ===")
        overlay_logo(images, logo_path)
        print(f"  Overlaid logo on {len(images)} images\n")
    else:
        print("=== Step 2: Logo Overlay — SKIPPED (no --logo) ===\n")

    # Step 3
    if args.skip_scoring:
        print("=== Step 3: Scoring SKIPPED ===\n")
        results = [{"path": p, "scores": {"design": 15, "visibility": 15,
                    "persuasion": 15, "ctr": 15}, "total": 60,
                    "verdict": "review", "mojibake": False,
                    "alignment_issues": False, "issues": []}
                   for p in images]
    else:
        print("=== Step 3: Vision Scoring ===")
        results = score_banners(client, images, cache_path)
        print()

    # Step 4
    print("=== Step 4: Auto-Select ===")
    selected = select_top_k(results, sizes, args.top_k, approved_dir)
    print(f"  Selected: {len(selected)} banners\n")

    # Save results JSON
    results_json = []
    for r in sorted(results, key=lambda x: x["total"], reverse=True):
        results_json.append({
            "file": r["path"].name,
            "scores": r["scores"],
            "total": r["total"],
            "verdict": r.get("verdict", ""),
            "approved": r.get("approved", False),
            "issues": r.get("issues", []),
        })
    results_path = session_dir / "results.json"
    results_path.write_text(
        json.dumps(results_json, ensure_ascii=False, indent=2),
        encoding="utf-8")

    # Step 5
    print("=== Step 5: Review HTML ===")
    review_path = build_review_html(results, session_dir)
    print(f"  Review: {review_path}\n")

    print("=" * 50)
    print(f"Session:   {session_dir}")
    print(f"Generated: {len(images)}")
    print(f"Approved:  {len(selected)}")
    print(f"Review:    {review_path}")
    if approved_dir.exists():
        print(f"Top-K dir: {approved_dir}/ "
              f"({len(list(approved_dir.glob('*.png')))} files)")


if __name__ == "__main__":
    main()

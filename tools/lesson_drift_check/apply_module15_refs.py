#!/usr/bin/env python3
"""
One-off content fix: append a 'reference resources' section to module-15
commands that align with the canonical template-gallery URLs in the
aiagent-course module-15 slide (S07_Resources / S08).

Idempotent: if the section already exists, the file is left unchanged.

Usage:
    python3 tools/lesson_drift_check/apply_module15_refs.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REFS = [
    ("Dribbble (motion design portfolios)", "https://dribbble.com/"),
    ("Envato Elements — video templates / logo animation",
     "https://elements.envato.com/video-templates/logo+animation"),
    ("Placeit — minimalist motion-graphics intro maker",
     "https://placeit.net/c/videos/stages/intro-maker-with-minimalist-motion-graphics-988"),
    ("YouTube — After Effects templates project channel",
     "https://www.youtube.com/@paftereffectstemplatesproj6705"),
    ("YouTube — motion-graphics templates playlist",
     "https://www.youtube.com/playlist?list=PLCWRuswMLN-huRtRNjplBjZGuIknrhckj"),
]

HEADERS = {
    "ja": "## 参考リンク（aiagent-course Module 15 スライドと共通）",
    "en": "## Reference links (mirrors aiagent-course Module 15 slides)",
    "es": "## Enlaces de referencia (sincronizado con las slides de Module 15)",
}

INTRO = {
    "ja": "テンプレートやインスピレーションを探すときに使う 5 つのリソース。",
    "en": "Five resources you can use to find templates or inspiration.",
    "es": "Cinco recursos para buscar plantillas o inspiración.",
}


def detect_locale(path: Path) -> str:
    if path.stem.endswith(".en"):
        return "en"
    if path.stem.endswith(".es"):
        return "es"
    return "ja"


def build_section(locale: str) -> str:
    lines = ["", HEADERS[locale], "", INTRO[locale], ""]
    for label, url in REFS:
        lines.append(f"- [{label}]({url})")
    lines.append("")
    return "\n".join(lines)


# Files we patch: 9 start-15-*.md + 3 setup-* lessons that anchor module 15
TARGETS = [
    "start-15-1",
    "start-15-2",
    "start-15-3",
    "start-15-4",
    "start-15-5",
    "start-15-6",
    "start-15-7",
    "start-15-8",
    "start-15-9",
    "setup-remotion",
    "setup-elevenlabs",
    "setup-fal",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".claude/commands/lesson")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: {root} not found", file=sys.stderr)
        return 1

    edited = skipped = 0
    for stem in TARGETS:
        for ext in ("md", "en.md", "es.md"):
            path = root / f"{stem}.{ext}"
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            locale = detect_locale(path)
            header = HEADERS[locale]
            if header in text:
                skipped += 1
                continue
            new_text = text.rstrip() + "\n" + build_section(locale) + "\n"
            print(f"+ {path.relative_to(root.parent.parent)}")
            if not args.dry_run:
                path.write_text(new_text, encoding="utf-8")
            edited += 1

    print(f"\nedited={edited}, skipped={skipped} (already present)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Scaffold the 2 missing module-15 lesson commands (15-10, 15-11)
in three locales each. Pulls title/description from the aiagent-course
slide JSON (module15.json) so the command title matches the slide badge.

Idempotent: skips files that already exist.

Usage:
    python3 tools/lesson_drift_check/scaffold_module15.py [--course /path/to/aiagent-course] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# tags_extra is a per-locale dict so en/es scaffolds don't carry residual
# Japanese (which fails tools/check_residual_japanese.py).
LESSONS = [
    ("start-15-10", "s23", "intermediate", {
        "ja": "Remotion / 記事 / SNS",
        "en": "Remotion / articles / social",
        "es": "Remotion / artículos / redes sociales",
    }),
    ("start-15-11", "s24", "advanced", {
        "ja": "Remotion / 品質 / リファレンス",
        "en": "Remotion / quality / references",
        "es": "Remotion / calidad / referencias",
    }),
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


def render(slug: str, badge: str, title: str, description: str, level: str,
           tags_extra: str, locale: str) -> str:
    if locale == "ja":
        body = f"""---
description: "Lesson command — {title}"
duration: "約30分"
prerequisites: ["Module 15 のセットアップ完了 (`/setup-remotion` / `/setup-elevenlabs` / `/setup-fal`)"]
level: "{level}"
nonInteractiveMode: deferred
tags: ["lesson", "module-15", "video"]
---

# /{slug} -- {badge}: {title}

> aiagent-course Module 15 のスライド `{badge}` と一対一対応。詳細はスライド本体を参照。

## このレッスンでやること

{description}

## 進め方

1. aiagent-course の対応スライドを開いて `{badge}: {title}` を表示
2. スライド本文の指示に従って手を動かす
3. 困ったら `/check-setup` で環境を再確認
4. 終わったら次のレッスンへ

## ヒント

- {tags_extra}
- 参照リソース: 下記「参考リンク」

"""
    elif locale == "en":
        body = f"""---
description: "Lesson command — {title}"
duration: "~30 min"
prerequisites: ["Module 15 setup complete (`/setup-remotion` / `/setup-elevenlabs` / `/setup-fal`)"]
level: "{level}"
nonInteractiveMode: deferred
tags: ["lesson", "module-15", "video"]
---

# /{slug} -- {badge}: {title}

> Pairs 1:1 with the aiagent-course Module 15 slide `{badge}`. Refer to the
> slide for the full body.

## What this lesson covers

{description}

## How to proceed

1. Open the matching aiagent-course slide showing `{badge}: {title}`.
2. Follow the slide body and work through it hands-on.
3. If you get stuck, run `/check-setup` to re-verify the environment.
4. When you're done, move to the next lesson.

## Hints

- {tags_extra}
- See "Reference links" below for inspiration sources.

"""
    else:  # es
        body = f"""---
description: "Lesson command — {title}"
duration: "~30 min"
prerequisites: ["Setup del Module 15 completo (`/setup-remotion` / `/setup-elevenlabs` / `/setup-fal`)"]
level: "{level}"
nonInteractiveMode: deferred
tags: ["lesson", "module-15", "video"]
---

# /{slug} -- {badge}: {title}

> Apareja 1:1 con la slide `{badge}` del Module 15 de aiagent-course. Para el
> cuerpo completo, consulta la slide.

## Qué cubre esta lección

{description}

## Cómo avanzar

1. Abre la slide correspondiente en aiagent-course con `{badge}: {title}`.
2. Sigue el cuerpo de la slide y trabájalo de forma práctica.
3. Si te atascas, ejecuta `/check-setup` para re-verificar el entorno.
4. Cuando termines, pasa a la siguiente lección.

## Pistas

- {tags_extra}
- Mira "Enlaces de referencia" abajo para fuentes de inspiración.

"""
    body += HEADERS[locale] + "\n\n" + INTRO[locale] + "\n\n"
    for label, url in REFS:
        body += f"- [{label}]({url})\n"
    return body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", default="../aiagent-course")
    parser.add_argument("--root", default=".claude/commands/lesson")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    course = Path(args.course).resolve()
    root = Path(args.root).resolve()
    if not (course / "messages/ja/course/module15.json").exists():
        print(f"ERROR: aiagent-course not found at {course}", file=sys.stderr)
        return 1

    json_data = {
        loc: json.loads((course / f"messages/{loc}/course/module15.json").read_text(encoding="utf-8"))
        for loc in ("ja", "en", "es")
    }

    created = skipped = 0
    for slug, sid, level, tags_extra_map in LESSONS:
        for loc in ("ja", "en", "es"):
            section = json_data[loc].get("module15", {}).get(sid, {})
            badge = section.get("badge", f"Lesson 15-{slug.split('-')[-1]}")
            title = section.get("title", slug)
            description = section.get("description", "")
            ext = ".md" if loc == "ja" else f".{loc}.md"
            path = root / f"{slug}{ext}"
            if path.exists():
                skipped += 1
                continue
            tags_extra = (
                tags_extra_map[loc] if isinstance(tags_extra_map, dict) else tags_extra_map
            )
            content = render(slug, badge, title, description, level, tags_extra, loc)
            print(f"+ {path.relative_to(root.parent.parent)}")
            if not args.dry_run:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            created += 1

    print(f"\ncreated={created}, skipped={skipped} (already existed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

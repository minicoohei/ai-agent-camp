#!/usr/bin/env python3
"""Module completion verifier.

Checks all lessons in a module for output file existence and validity.
Extracts checkpoints from lesson Markdown files for AI evaluation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Ensure tools/ is on sys.path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))

from lesson_progress import (
    PROJECT_ROOT,
    extract_outputs,
    lesson_order,
    load_progress,
)

CHECKPOINT_RE = re.compile(r"^- \[[ x]\]\s+(.+)$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_RE = re.compile(r"^#\s+.*?Lesson\s+\d+-\d+:\s*(.+)$", re.MULTILINE)

MODULE_NAMES: dict[int, str] = {
    0: "セットアップ",
    1: "バナー・画像生成",
    2: "図表・フロー作成",
    3: "スクショ分析",
    4: "データ分析",
    5: "PPTX操作",
    6: "Slack連携",
    7: "動画生成",
    8: "GAS操作",
    9: "GitHub Actions",
    10: "Notion連携",
    11: "エージェント開発",
    12: "マーケティング",
    13: "LP/HP制作",
    14: "PM・システム要件定義",
    15: "メール自動化",
    16: "記事作成",
    17: "マーケティング応用",
    18: "PM総合",
}

# Magic bytes for image format validation
IMAGE_MAGIC = {
    ".png": b"\x89PNG",
    ".jpg": b"\xff\xd8\xff",
    ".jpeg": b"\xff\xd8\xff",
    ".gif": b"GIF8",
}
# WebP uses RIFF container: bytes 0-3 = "RIFF", bytes 8-11 = "WEBP"
WEBP_MAGIC = (b"RIFF", b"WEBP")


def extract_checkpoints(text: str) -> list[str]:
    """Extract checkpoint items from lesson Markdown."""
    checkpoints: list[str] = []
    in_section = False
    for line in text.splitlines():
        if "チェックポイント" in line and line.strip().startswith("#"):
            in_section = True
            continue
        if in_section:
            if line.strip().startswith("#"):
                in_section = False
                continue
            m = CHECKPOINT_RE.match(line.strip())
            if m:
                checkpoints.append(m.group(1).strip())
    return checkpoints


def extract_title(text: str) -> str:
    """Extract lesson title from Markdown."""
    m = TITLE_RE.search(text)
    if m:
        return m.group(1).strip()
    # Fallback: first H1
    for line in text.splitlines():
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    return ""


def extract_frontmatter(text: str) -> dict:
    """Extract YAML-like frontmatter as a simple dict."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    result = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"\'')
    return result


def validate_file(path: Path) -> dict:
    """Check if a file exists and has valid content."""
    # Directory check first (path ending with / or no suffix)
    treat_as_dir = str(path).endswith("/") or not path.suffix
    if treat_as_dir:
        if path.is_dir():
            files = [f for f in path.iterdir() if f.is_file()]
            return {
                "path": str(path),
                "exists": True,
                "is_dir": True,
                "file_count": len(files),
                "valid": len(files) > 0,
            }
        return {"path": str(path), "exists": False, "valid": False}

    if not path.exists():
        return {"path": str(path), "exists": False, "valid": False}

    if path.is_dir():
        files = [f for f in path.iterdir() if f.is_file()]
        return {
            "path": str(path),
            "exists": True,
            "is_dir": True,
            "file_count": len(files),
            "valid": len(files) > 0,
        }

    size = path.stat().st_size
    if size == 0:
        return {"path": str(path), "exists": True, "size": 0, "valid": False}

    valid = True
    suffix = path.suffix.lower()

    # Image format check — accept any known image format regardless of extension
    if suffix in IMAGE_MAGIC or suffix == ".webp":
        try:
            with open(path, "rb") as f:
                header = f.read(12)
            # Check standard image formats
            is_known_image = any(
                header[: len(magic)] == magic for magic in IMAGE_MAGIC.values()
            )
            # Check WebP (RIFF????WEBP)
            is_webp = header[:4] == WEBP_MAGIC[0] and header[8:12] == WEBP_MAGIC[1]
            valid = is_known_image or is_webp
        except OSError:
            valid = False

    # JSON parse check
    elif suffix == ".json":
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            valid = False

    # HTML tag check
    elif suffix in (".html", ".htm"):
        try:
            content = path.read_text(encoding="utf-8")
            valid = "<html" in content.lower() or "<!doctype" in content.lower()
        except UnicodeDecodeError:
            valid = False

    # Python syntax check
    elif suffix == ".py":
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
        except (SyntaxError, UnicodeDecodeError):
            valid = False

    return {"path": str(path), "exists": True, "size": size, "valid": valid}


def verify_module(module_num: int) -> dict:
    """Verify all lessons in a module."""
    order, mapping = lesson_order()
    progress = load_progress()

    # Filter lessons for this module
    prefix = f"start-{module_num}-"
    module_lessons = [lid for lid in order if lid.startswith(prefix)]

    if not module_lessons:
        return {
            "module": module_num,
            "module_name": MODULE_NAMES.get(module_num, f"Module {module_num}"),
            "error": f"モジュール {module_num} にレッスンが見つかりません",
            "lessons": [],
            "summary": {},
        }

    lessons_result = []
    total_outputs_found = 0
    total_outputs_missing = 0
    total_outputs_invalid = 0
    completed_lessons = 0

    for lesson_id in module_lessons:
        path = mapping[lesson_id]
        text = path.read_text(encoding="utf-8")

        title = extract_title(text)
        frontmatter = extract_frontmatter(text)
        checkpoints = extract_checkpoints(text)
        raw_outputs = extract_outputs(text)

        # Validate each output
        output_checks = []
        for out_path in raw_outputs:
            check = validate_file(out_path)
            output_checks.append(check)
            if check["exists"] and check["valid"]:
                total_outputs_found += 1
            elif check["exists"] and not check["valid"]:
                total_outputs_invalid += 1
            else:
                total_outputs_missing += 1

        # Check progress status
        lesson_state = progress.get("lessons", {}).get(lesson_id, {})
        is_completed = lesson_state.get("completed", False)
        if is_completed:
            completed_lessons += 1

        lessons_result.append(
            {
                "lesson_id": lesson_id,
                "title": title or frontmatter.get("description", lesson_id),
                "description": frontmatter.get("description", ""),
                "checkpoints": checkpoints,
                "outputs": output_checks,
                "progress_status": "completed" if is_completed else "incomplete",
            }
        )

    module_name = MODULE_NAMES.get(module_num, f"Module {module_num}")

    return {
        "module": module_num,
        "module_name": module_name,
        "lessons": lessons_result,
        "summary": {
            "total_lessons": len(module_lessons),
            "completed_lessons": completed_lessons,
            "outputs_found": total_outputs_found,
            "outputs_missing": total_outputs_missing,
            "outputs_invalid": total_outputs_invalid,
            "total_checkpoints": sum(
                len(l["checkpoints"]) for l in lessons_result
            ),
        },
    }


def print_text_result(result: dict) -> None:
    """Print human-readable verification result."""
    if "error" in result:
        print(f"エラー: {result['error']}")
        return

    print(f"=== Module {result['module']}: {result['module_name']} ===")
    print()

    s = result["summary"]
    print(f"レッスン数: {s['total_lessons']}")
    print(f"完了済み: {s['completed_lessons']}/{s['total_lessons']}")
    print(
        f"成果物: {s['outputs_found']}個OK / {s['outputs_missing']}個不足 / {s['outputs_invalid']}個不正"
    )
    print(f"チェックポイント: {s['total_checkpoints']}項目")
    print()

    for lesson in result["lessons"]:
        status_icon = "✅" if lesson["progress_status"] == "completed" else "⬜"
        print(f"{status_icon} {lesson['lesson_id']}: {lesson['title']}")

        if lesson["outputs"]:
            for out in lesson["outputs"]:
                if out["exists"] and out.get("valid", True):
                    if out.get("is_dir"):
                        print(f"    📁 OK: {out['path']} ({out.get('file_count', 0)}ファイル)")
                    else:
                        size_kb = out.get("size", 0) / 1024
                        print(f"    📄 OK: {out['path']} ({size_kb:.1f}KB)")
                elif out["exists"]:
                    print(f"    ⚠️  不正: {out['path']}")
                else:
                    print(f"    ❌ 不足: {out['path']}")
        else:
            print("    (成果物の出力先指定なし)")

        if lesson["checkpoints"]:
            print(f"    チェックポイント ({len(lesson['checkpoints'])}項目):")
            for cp in lesson["checkpoints"]:
                print(f"      - {cp}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="モジュール完了チェッカー（AI評価用データ生成）"
    )
    parser.add_argument(
        "--module",
        type=int,
        required=True,
        help="チェックするモジュール番号",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON形式で出力",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="結果JSONの保存先パス",
    )
    args = parser.parse_args()

    result = verify_module(args.module)

    if args.json:
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        print(json_str)
    else:
        print_text_result(result)

    # Save JSON if output path specified
    if args.output:
        out_path = Path(args.output).resolve()
        if not str(out_path).startswith(str(PROJECT_ROOT)):
            print(f"エラー: 出力先はプロジェクト内に限定されます: {PROJECT_ROOT}", file=sys.stderr)
            sys.exit(1)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if not args.json:
            print(f"結果を保存しました: {out_path}")


if __name__ == "__main__":
    main()

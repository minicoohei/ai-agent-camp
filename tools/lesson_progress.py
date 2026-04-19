#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = PROJECT_ROOT / ".cursor" / "commands" / "lesson"
PROGRESS_PATH = PROJECT_ROOT / ".cursor" / "lesson_progress.json"

OUTPUT_LINE_RE = re.compile(r"^(出力先|出力)\s*:\s*(.+)$")
COMMAND_PREFIXES = (
    "/",
    "python ",
    "pip ",
    "npm ",
    "npx ",
    "node ",
    "git ",
    "brew ",
    "ffmpeg ",
    "ffprobe ",
    "curl ",
    "mkdir ",
    "ls ",
    "cd ",
    "echo ",
    "source ",
    "playwright ",
    "export ",
    "set ",
    "pytest ",
)


def load_progress() -> dict:
    if PROGRESS_PATH.exists():
        try:
            return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"lessons": {}}
    return {"lessons": {}}


def save_progress(progress: dict) -> None:
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    progress["updated_at"] = datetime.now(timezone.utc).isoformat()
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def lesson_order() -> tuple[list[str], dict[str, Path]]:
    items = []
    for path in LESSON_DIR.glob("start-*.md"):
        match = re.match(r"start-(\d+)-(\d+)\.md", path.name)
        if not match:
            continue
        module = int(match.group(1))
        lesson = int(match.group(2))
        items.append((module, lesson, path))
    items.sort()
    order = [f"start-{m}-{l}" for m, l, _ in items]
    mapping = {f"start-{m}-{l}": p for m, l, p in items}
    return order, mapping


def is_command_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return stripped.startswith(COMMAND_PREFIXES)


def has_placeholder(line: str) -> bool:
    return bool(re.search(r"(?i)(your|xxx|xxxx|<[^>]+>)", line))


def normalize_path(path_str: str) -> Path:
    path_str = path_str.strip().strip("`\"'").rstrip("。.")
    if path_str.startswith("~/"):
        return Path(path_str).expanduser()
    if path_str.startswith("/"):
        return Path(path_str)
    return PROJECT_ROOT / path_str


def extract_outputs(text: str) -> list[Path]:
    outputs: list[Path] = []
    for line in text.splitlines():
        match = OUTPUT_LINE_RE.match(line.strip())
        if not match:
            continue
        raw = match.group(2).strip()
        for part in re.split(r"[、,]", raw):
            part = part.strip().strip("`\"'").rstrip("。.")
            if not part:
                continue
            outputs.append(normalize_path(part))
    return outputs


def extract_commands(text: str) -> list[str]:
    commands: list[str] = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            continue
        if is_command_line(line):
            commands.append(line.strip())
    # Remove duplicates while preserving order
    seen = set()
    ordered = []
    for cmd in commands:
        if cmd in seen:
            continue
        seen.add(cmd)
        ordered.append(cmd)
    return ordered


def check_lesson(lesson_id: str, path: Path, progress: dict) -> dict:
    text = path.read_text(encoding="utf-8")
    outputs = extract_outputs(text)
    commands = extract_commands(text)

    output_checks = [
        {"path": str(p), "exists": p.exists()} for p in outputs
    ]

    lesson_state = progress.get("lessons", {}).get(lesson_id, {})
    command_confirmed = bool(lesson_state.get("command_confirmed"))
    manual_confirmed = bool(lesson_state.get("manual_confirmed"))

    outputs_ok = all(item["exists"] for item in output_checks)
    commands_ok = True if not commands else command_confirmed
    manual_ok = True if outputs else manual_confirmed
    completed = outputs_ok and commands_ok and manual_ok

    result = {
        "lesson_id": lesson_id,
        "outputs": output_checks,
        "commands": commands,
        "command_confirmed": command_confirmed,
        "manual_confirmed": manual_confirmed,
        "completed": completed,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    progress.setdefault("lessons", {})[lesson_id] = result
    return result


def print_result(result: dict) -> None:
    print(f"レッスン: {result['lesson_id']}")

    if result["outputs"]:
        print("成果物チェック:")
        for item in result["outputs"]:
            status = "OK" if item["exists"] else "NG"
            print(f"  - {status}: {item['path']}")
    else:
        print("成果物チェック: 対象なし")

    if result["commands"]:
        status = "OK" if result["command_confirmed"] else "要確認"
        print(f"コマンド確認: {status}")
        for cmd in result["commands"]:
            print(f"  - {cmd}")
    else:
        print("コマンド確認: 対象なし")

    if not result["outputs"]:
        manual = "OK" if result["manual_confirmed"] else "要確認"
        print(f"手動確認: {manual}")

    final_status = "完了" if result["completed"] else "未完"
    print(f"判定: {final_status}")


def mark_lesson(lesson_id: str, progress: dict) -> None:
    progress.setdefault("lessons", {}).setdefault(lesson_id, {})
    progress["lessons"][lesson_id]["command_confirmed"] = True
    progress["lessons"][lesson_id]["manual_confirmed"] = True
    progress["lessons"][lesson_id]["checked_at"] = datetime.now(timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson completion checker")
    parser.add_argument("--check", dest="check_id", help="Check a lesson by id")
    parser.add_argument("--next", action="store_true", help="Check and suggest next lesson")
    parser.add_argument("--mark", dest="mark_id", help="Manually mark a lesson as confirmed")
    parser.add_argument("--list", action="store_true", help="List lesson order")
    args = parser.parse_args()

    order, mapping = lesson_order()
    progress = load_progress()

    if args.list:
        print("レッスン順:")
        for lesson_id in order:
            print(f"  - {lesson_id}")
        return

    if args.mark_id:
        if args.mark_id not in mapping:
            print(f"未対応のレッスンIDです: {args.mark_id}")
            return
        mark_lesson(args.mark_id, progress)
        save_progress(progress)
        print(f"手動確認を完了として登録しました: {args.mark_id}")
        return

    if args.check_id:
        if args.check_id not in mapping:
            print(f"未対応のレッスンIDです: {args.check_id}")
            return
        result = check_lesson(args.check_id, mapping[args.check_id], progress)
        save_progress(progress)
        print_result(result)
        return

    if args.next:
        for lesson_id in order:
            result = check_lesson(lesson_id, mapping[lesson_id], progress)
            if result["completed"]:
                continue
            save_progress(progress)
            print_result(result)
            print("")
            print(f"次に実行: /lesson/{lesson_id}")
            print("完了済みなら /next_lesson を再実行してください。")
            return
        save_progress(progress)
        print("全レッスン完了です。")
        return

    parser.print_help()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Shared helpers for Codex command manifest generation and routing."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMANDS_ROOT = ROOT / ".cursor" / "commands"
MANIFEST_PATH = ROOT / "data" / "codex-command-manifest.json"


@dataclass(frozen=True)
class CommandEntry:
    kind: str
    canonicalId: str
    aliases: list[str]
    sourcePath: str
    codexRoute: dict[str, str]
    expectedHandler: str
    status: str


def _aliases_for(path: Path) -> list[str]:
    stem = path.stem
    relative = path.relative_to(COMMANDS_ROOT)
    aliases: list[str] = [f"/{stem}", stem]

    if len(relative.parts) > 1:
        aliases.append("/" + "/".join(relative.with_suffix("").parts))

    deduped: list[str] = []
    for alias in aliases:
        if alias not in deduped:
            deduped.append(alias)
    return deduped


def _classify(path: Path) -> tuple[str, dict[str, str], str]:
    stem = path.stem
    relative = path.relative_to(COMMANDS_ROOT)

    if relative.parts[0] == "lesson" and stem.startswith("start-"):
        route = {
            "handler": "aiagent-lesson-runner",
            "mode": "lesson",
            "target": stem,
        }
        return "lesson", route, "aiagent-lesson-runner"

    route = {
        "handler": "aiagent-utility-runner",
        "mode": "utility",
        "target": stem,
    }
    return "utility", route, "aiagent-utility-runner"


def iter_command_files() -> list[Path]:
    paths = sorted(COMMANDS_ROOT.rglob("*.md"))
    return [path for path in paths if path.is_file()]


def build_manifest() -> list[CommandEntry]:
    entries: list[CommandEntry] = []
    for path in iter_command_files():
        kind, route, expected_handler = _classify(path)
        entries.append(
            CommandEntry(
                kind=kind,
                canonicalId=path.stem,
                aliases=_aliases_for(path),
                sourcePath=str(path.relative_to(ROOT)),
                codexRoute=route,
                expectedHandler=expected_handler,
                status="ready",
            )
        )
    return entries


def manifest_as_dict() -> dict[str, object]:
    entries = [asdict(entry) for entry in build_manifest()]
    return {
        "version": 1,
        "entries": entries,
    }


def write_manifest(path: Path = MANIFEST_PATH) -> Path:
    payload = manifest_as_dict()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_entries(path: Path = MANIFEST_PATH) -> list[dict[str, object]]:
    payload = load_manifest(path)
    entries = payload.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("Manifest entries must be a list")
    return entries


def resolve_command(command: str, path: Path = MANIFEST_PATH) -> dict[str, object]:
    normalized = command.strip()
    entries = load_entries(path)

    for entry in entries:
        aliases = entry.get("aliases", [])
        if normalized in aliases:
            route = entry["codexRoute"]
            return {
                "ok": True,
                "status": entry["status"],
                "input": command,
                "resolvedAlias": normalized,
                "canonicalId": entry["canonicalId"],
                "kind": entry["kind"],
                "expectedHandler": entry["expectedHandler"],
                "handler": route["handler"],
                "mode": route["mode"],
                "target": route["target"],
                "sourcePath": entry["sourcePath"],
            }

    return {
        "ok": False,
        "status": "unmapped",
        "input": command,
        "message": f"Unsupported Codex command: {command}",
    }

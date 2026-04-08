#!/usr/bin/env python3
"""Automate Lesson 14-11 with best-effort Notion execution."""

from __future__ import annotations

import csv
import json
import os
import re
import socket
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - runtime dependency check
    requests = None


REPO_ROOT = Path(__file__).resolve().parent.parent
REQ_SPEC_PATH = REPO_ROOT / "output/pm/requirements-spec.md"
EXPORT_MD_PATH = REPO_ROOT / "output/pm/notion-export.md"
EXPORT_CSV_PATH = REPO_ROOT / "output/pm/notion-export.csv"
TRACKER_MD_PATH = REPO_ROOT / "output/pm/requirement-tracker.md"
REPORT_PATH = REPO_ROOT / "output/test-results/start-14-11-report.json"

NOTION_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"


@dataclass
class StepResult:
    step: str
    default_choice: str
    status: str
    details: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


def now_jst() -> datetime:
    return datetime.now().astimezone()


def env_present(name: str) -> bool:
    return bool(os.getenv(name))


def notion_headers(api_key: str | None) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key or ''}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def split_markdown_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def map_priority(req_id: str, raw_priority: str, release: str | None = None) -> str:
    if req_id.startswith("REQ-F-"):
        if release and "Phase 2" in release:
            return "Could"
        return {"P0": "Must", "P1": "Should", "P2": "Could"}.get(raw_priority, "Should")

    if req_id in {
        "REQ-NFR-P-001",
        "REQ-NFR-P-002",
        "REQ-NFR-A-001",
        "REQ-NFR-A-003",
        "REQ-NFR-S-001",
        "REQ-NFR-S-002",
        "REQ-NFR-S-003",
        "REQ-NFR-S-004",
        "REQ-NFR-S-005",
        "REQ-NFR-U-001",
        "REQ-NFR-U-005",
    }:
        return "Must"
    if req_id.startswith("REQ-NFR-SC-"):
        return "Could"
    return "Should"


def parse_requirements(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in text.splitlines():
        header = re.match(r"^#### (REQ-(?:F|NFR-[A-Z]+)-\d+): (.+)$", line)
        if header:
            if current:
                rows.append(current)
            req_id = header.group(1)
            current = {
                "requirement_id": req_id,
                "requirement_name": header.group(2).strip(),
                "category": "機能" if req_id.startswith("REQ-F-") else "非機能",
                "status": "未着手",
                "priority": map_priority(req_id, ""),
                "source_priority": "",
                "release": "MVP",
                "screen": "",
                "notes": "",
            }
            continue

        if not current or not line.startswith("|"):
            continue

        cells = split_markdown_row(line)
        if len(cells) < 2:
            continue

        key = cells[0]
        value = cells[1]
        if key == "優先度":
            raw_priority = value.split("（", 1)[0].strip()
            current["source_priority"] = raw_priority
            current["priority"] = map_priority(current["requirement_id"], raw_priority, current.get("release"))
        elif key in {"説明", "要件"}:
            current["notes"] = value
        elif key == "対象画面":
            current["screen"] = value
        elif key in {"対象リリース", "MVP 段階", "将来"} and not current.get("release"):
            current["release"] = value

    if current:
        rows.append(current)

    if not rows:
        raise ValueError(f"No requirement rows found in {path}")
    return rows


def stats_for(rows: list[dict[str, str]]) -> dict[str, Counter]:
    return {
        "status": Counter(row["status"] for row in rows),
        "priority": Counter(row["priority"] for row in rows),
        "category": Counter(row["category"] for row in rows),
    }


def pct(count: int, total: int) -> str:
    return f"{(count / total * 100):.1f}%" if total else "0.0%"


def write_markdown_export(
    rows: list[dict[str, str]],
    path: Path,
    database_id: str,
    source_label: str,
    source_url: str | None,
    note: str,
) -> None:
    counters = stats_for(rows)
    total = len(rows)
    export_time = now_jst().strftime("%Y-%m-%d %H:%M:%S %Z")

    lines = [
        "# TaskFlow Requirements Tracker - Export",
        "",
        f"**エクスポート日時**: {export_time}",
        f"**データベースID**: {database_id or 'N/A'}",
        f"**URL**: {source_url or 'N/A'}",
        f"**データソース**: {source_label}",
        f"**備考**: {note}",
        "",
        "## 📊 統計情報",
        "",
        "| 項目 | 件数 |",
        "|------|------|",
        f"| 総要件数 | {total} |",
        f"| 未着手 | {counters['status'].get('未着手', 0)} |",
        f"| 設計中 | {counters['status'].get('設計中', 0)} |",
        f"| 実装中 | {counters['status'].get('実装中', 0)} |",
        f"| テスト中 | {counters['status'].get('テスト中', 0)} |",
        f"| 完了 | {counters['status'].get('完了', 0)} |",
        "",
        "### 優先度別",
        "",
        "| 優先度 | 件数 | 割合 |",
        "|--------|------|------|",
    ]

    for label in ["Must", "Should", "Could", "Won't"]:
        count = counters["priority"].get(label, 0)
        lines.append(f"| {label} | {count} | {pct(count, total)} |")

    lines.extend(
        [
            "",
            "### カテゴリ別",
            "",
            "| カテゴリ | 件数 | 割合 |",
            "|---------|------|------|",
        ]
    )

    for label in ["機能", "非機能", "その他"]:
        count = counters["category"].get(label, 0)
        lines.append(f"| {label} | {count} | {pct(count, total)} |")

    lines.extend(
        [
            "",
            "## 📋 要件一覧",
            "",
            "| 要件ID | 要件名 | カテゴリ | ステータス | 優先度 |",
            "|--------|--------|---------|------------|--------|",
        ]
    )

    for row in rows:
        lines.append(
            f"| {row['requirement_id']} | {row['requirement_name']} | "
            f"{row['category']} | {row['status']} | {row['priority']} |"
        )

    lines.extend(["", "---", "", "**Generated by TaskFlow PM Training Platform**", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv_export(rows: list[dict[str, str]], path: Path) -> None:
    fieldnames = ["requirement_id", "requirement_name", "category", "status", "priority"]
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_tracker(rows: list[dict[str, str]], path: Path) -> None:
    lines = [
        "# TaskFlow Requirement Tracker",
        "",
        "> 自動生成されたローカルトラッカーです。Notion 連携に失敗した場合の代替成果物として使用します。",
        "",
        "| 要件ID | 要件名 | カテゴリ | ステータス | 優先度 |",
        "|--------|--------|---------|------------|--------|",
    ]
    for row in rows:
        lines.append(
            f"| {row['requirement_id']} | {row['requirement_name']} | "
            f"{row['category']} | {row['status']} | {row['priority']} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def dns_probe(host: str) -> tuple[bool, str]:
    try:
        return True, socket.gethostbyname(host)
    except OSError as exc:
        return False, str(exc)


def notion_request(
    method: str,
    endpoint: str,
    api_key: str | None,
    payload: dict[str, Any] | None = None,
) -> tuple[bool, dict[str, Any] | str]:
    if requests is None:
        return False, "requests is not installed"

    try:
        response = requests.request(
            method=method,
            url=f"{NOTION_BASE_URL}/{endpoint}",
            headers=notion_headers(api_key),
            json=payload,
            timeout=10,
        )
        try:
            body: dict[str, Any] = response.json()
        except ValueError:
            body = {"text": response.text}
        return response.ok, {"status_code": response.status_code, "body": body}
    except Exception as exc:  # pragma: no cover - network-dependent
        return False, str(exc)


def step1_verify_connection() -> StepResult:
    api_key_present = env_present("NOTION_API_KEY")
    db_id_present = env_present("NOTION_DATABASE_ID")
    parent_page_present = env_present("NOTION_PARENT_PAGE_ID")
    dns_ok, dns_detail = dns_probe("api.notion.com")
    api_ok, api_detail = notion_request(
        "POST",
        "search",
        os.getenv("NOTION_API_KEY"),
        {"page_size": 1, "filter": {"property": "object", "value": "database"}},
    )

    details = [
        f"NOTION_API_KEY present: {'yes' if api_key_present else 'no'}",
        f"NOTION_DATABASE_ID present: {'yes' if db_id_present else 'no'}",
        f"NOTION_PARENT_PAGE_ID present: {'yes' if parent_page_present else 'no'}",
        f"DNS probe: {'ok' if dns_ok else 'failed'} ({dns_detail})",
        f"API probe: {'ok' if api_ok else 'failed'} ({api_detail})",
    ]
    status = "success" if api_key_present and dns_ok and api_ok else "failed"

    return StepResult(
        step="Step 1: Notion API接続の確認",
        default_choice="ready",
        status=status,
        details=details,
        metrics={
            "notion_api_key_present": api_key_present,
            "notion_database_id_present": db_id_present,
            "notion_parent_page_id_present": parent_page_present,
        },
    )


def step2_create_database() -> tuple[StepResult, str | None, str | None]:
    api_key = os.getenv("NOTION_API_KEY")
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    if not api_key or not parent_page_id:
        details = []
        if not api_key:
            details.append("NOTION_API_KEY が未設定のため DB 作成を実行できません。")
        if not parent_page_id:
            details.append("NOTION_PARENT_PAGE_ID が未設定のため作成先ページを特定できません。")
        return (
            StepResult(
                step="Step 2: 要件トラッカーDBの作成",
                default_choice="simple",
                status="failed",
                details=details,
            ),
            None,
            None,
        )

    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "icon": {"type": "emoji", "emoji": "📋"},
        "title": [
            {
                "type": "text",
                "text": {"content": "TaskFlow Requirements Tracker"},
            }
        ],
        "properties": {
            "要件名": {"title": {}},
            "要件ID": {"rich_text": {}},
            "カテゴリ": {
                "select": {
                    "options": [
                        {"name": "機能", "color": "blue"},
                        {"name": "非機能", "color": "yellow"},
                        {"name": "その他", "color": "gray"},
                    ]
                }
            },
            "ステータス": {
                "select": {
                    "options": [
                        {"name": "未着手", "color": "default"},
                        {"name": "設計中", "color": "blue"},
                        {"name": "実装中", "color": "orange"},
                        {"name": "テスト中", "color": "purple"},
                        {"name": "完了", "color": "green"},
                    ]
                }
            },
            "優先度": {
                "select": {
                    "options": [
                        {"name": "Must", "color": "red"},
                        {"name": "Should", "color": "yellow"},
                        {"name": "Could", "color": "blue"},
                        {"name": "Won't", "color": "gray"},
                    ]
                }
            },
        },
    }

    ok, response = notion_request("POST", "databases", api_key, payload)
    if not ok or not isinstance(response, dict):
        return (
            StepResult(
                step="Step 2: 要件トラッカーDBの作成",
                default_choice="simple",
                status="failed",
                details=[f"DB 作成 API 失敗: {response}"],
            ),
            None,
            None,
        )

    body = response.get("body", {})
    database_id = body.get("id")
    database_url = body.get("url")
    status = "success" if database_id else "failed"
    return (
        StepResult(
            step="Step 2: 要件トラッカーDBの作成",
            default_choice="simple",
            status=status,
            details=[f"HTTP {response.get('status_code')}", f"DB URL: {database_url or 'N/A'}"],
            metrics={"database_id_created": bool(database_id)},
        ),
        database_id,
        database_url,
    )


def notion_page_properties(row: dict[str, str]) -> dict[str, Any]:
    return {
        "要件名": {"title": [{"text": {"content": row["requirement_name"]}}]},
        "要件ID": {"rich_text": [{"text": {"content": row["requirement_id"]}}]},
        "カテゴリ": {"select": {"name": row["category"]}},
        "ステータス": {"select": {"name": row["status"]}},
        "優先度": {"select": {"name": row["priority"]}},
    }


def step3_import_requirements(rows: list[dict[str, str]], database_id: str | None) -> StepResult:
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key or not database_id:
        details = [
            f"ローカル抽出件数: {len(rows)}",
            "Notion への投入は API キーまたは DB ID が不足しているため失敗しました。",
        ]
        return StepResult(
            step="Step 3: 要件データの投入",
            default_choice="auto_extract",
            status="partial",
            details=details,
            metrics={"extracted_requirements": len(rows), "imported_to_notion": 0},
        )

    imported = 0
    failures = 0
    for row in rows:
        ok, response = notion_request(
            "POST",
            "pages",
            api_key,
            {"parent": {"database_id": database_id}, "properties": notion_page_properties(row)},
        )
        if ok and isinstance(response, dict) and response.get("body", {}).get("id"):
            imported += 1
        else:
            failures += 1

    status = "success" if imported == len(rows) and failures == 0 else "partial"
    return StepResult(
        step="Step 3: 要件データの投入",
        default_choice="auto_extract",
        status=status,
        details=[
            f"抽出件数: {len(rows)}",
            f"Notion 成功件数: {imported}",
            f"Notion 失敗件数: {failures}",
        ],
        metrics={"extracted_requirements": len(rows), "imported_to_notion": imported},
    )


def parse_notion_page(page: dict[str, Any]) -> dict[str, str]:
    props = page.get("properties", {})
    title = "".join(
        part.get("plain_text", "")
        for part in props.get("要件名", {}).get("title", [])
    )
    rich_text = "".join(
        part.get("plain_text", "")
        for part in props.get("要件ID", {}).get("rich_text", [])
    )
    return {
        "requirement_id": rich_text,
        "requirement_name": title,
        "category": (props.get("カテゴリ", {}).get("select") or {}).get("name", ""),
        "status": (props.get("ステータス", {}).get("select") or {}).get("name", ""),
        "priority": (props.get("優先度", {}).get("select") or {}).get("name", ""),
    }


def step4_export(
    extracted_rows: list[dict[str, str]],
    database_id: str | None,
    database_url: str | None,
) -> StepResult:
    api_key = os.getenv("NOTION_API_KEY")
    export_rows = extracted_rows
    source_label = "local-fallback"
    note = "Notion API 実行に失敗したため、requirements-spec.md から抽出したローカルデータを出力しました。"
    status = "partial"
    details: list[str] = []

    if api_key and database_id:
        ok, response = notion_request("POST", f"databases/{database_id}/query", api_key, {})
        if ok and isinstance(response, dict):
            body = response.get("body", {})
            export_rows = [parse_notion_page(page) for page in body.get("results", [])]
            source_label = "notion"
            note = "Notion DB からエクスポートしました。"
            status = "success"
            details.append(f"Notion query HTTP {response.get('status_code')}")
        else:
            details.append(f"Notion export failed: {response}")
    else:
        details.append("Notion DB からのエクスポートは前提不足のため失敗しました。")

    write_markdown_export(export_rows, EXPORT_MD_PATH, database_id or "", source_label, database_url, note)
    write_csv_export(export_rows, EXPORT_CSV_PATH)
    write_tracker(extracted_rows, TRACKER_MD_PATH)

    details.extend(
        [
            f"Markdown export: {EXPORT_MD_PATH.relative_to(REPO_ROOT)}",
            f"CSV export: {EXPORT_CSV_PATH.relative_to(REPO_ROOT)}",
            f"Fallback tracker: {TRACKER_MD_PATH.relative_to(REPO_ROOT)}",
        ]
    )

    return StepResult(
        step="Step 4: Markdownエクスポート",
        default_choice="markdown_table",
        status=status,
        details=details,
        artifacts=[
            str(EXPORT_MD_PATH.relative_to(REPO_ROOT)),
            str(EXPORT_CSV_PATH.relative_to(REPO_ROOT)),
            str(TRACKER_MD_PATH.relative_to(REPO_ROOT)),
        ],
        metrics={"exported_rows": len(export_rows), "source": source_label},
    )


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPORT_MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    results: list[StepResult] = []
    errors: list[str] = []

    if not REQ_SPEC_PATH.exists():
        message = f"Missing prerequisite: {REQ_SPEC_PATH}"
        report = {
            "lesson": "Lesson 14-11: Notion連携",
            "executed_at": now_jst().isoformat(),
            "results": [],
            "errors": [message],
        }
        REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(message)
        return 1

    try:
        extracted_rows = parse_requirements(REQ_SPEC_PATH)
    except Exception as exc:
        message = f"requirements-spec parse failed: {exc}"
        report = {
            "lesson": "Lesson 14-11: Notion連携",
            "executed_at": now_jst().isoformat(),
            "results": [],
            "errors": [message],
        }
        REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(message)
        return 1

    step1 = step1_verify_connection()
    results.append(step1)

    step2, database_id, database_url = step2_create_database()
    results.append(step2)

    database_id = database_id or os.getenv("NOTION_DATABASE_ID")
    step3 = step3_import_requirements(extracted_rows, database_id)
    results.append(step3)

    step4 = step4_export(extracted_rows, database_id, database_url)
    results.append(step4)

    if step1.status == "failed":
        errors.append("Step 1 failed: Notion 接続前提を満たしていません。")
    if step2.status == "failed":
        errors.append("Step 2 failed: Notion DB を作成できませんでした。")
    if step3.status == "partial":
        errors.append("Step 3 partial: 要件抽出は成功したが Notion への投入は完了していません。")
    if step4.status != "success":
        errors.append("Step 4 partial: Markdown/CSV は生成したが Notion DB からの実エクスポートではありません。")

    report = {
        "lesson": "Lesson 14-11: Notion連携",
        "executed_at": now_jst().isoformat(),
        "default_choices": {
            "step1": "ready",
            "step2": "simple",
            "step3": "auto_extract",
            "step4": "markdown_table",
        },
        "input_file": str(REQ_SPEC_PATH.relative_to(REPO_ROOT)),
        "results": [asdict(result) for result in results],
        "errors": errors,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for result in results:
        print(f"[{result.status.upper()}] {result.step}")
        for detail in result.details:
            print(f"  - {detail}")

    print(f"Report: {REPORT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

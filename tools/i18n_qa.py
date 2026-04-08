#!/usr/bin/env python3
"""Unified i18n QA runner.

HTML / MD / CLI の3ドメインの品質チェックを単一コマンドで実行する。

Usage:
    uv run python tools/i18n_qa.py                          # 全ドメイン
    uv run python tools/i18n_qa.py --lang en                 # 特定言語
    uv run python tools/i18n_qa.py --domain md cli           # ドメイン指定
    uv run python tools/i18n_qa.py --json                    # JSON 出力 (CI向け)
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

_tools_dir = str(Path(__file__).resolve().parent)
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

try:
    from i18n_common import DIST_DIR_ROOT
except ImportError:
    from tools.i18n_common import DIST_DIR_ROOT


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------

@dataclass
class DomainResult:
    domain: str
    passed: bool = True
    checks: List[Dict[str, Any]] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "domain": self.domain,
            "passed": self.passed,
            "checks": self.checks,
        }
        if self.error:
            d["error"] = self.error
        return d


# ---------------------------------------------------------------------------
# Domain runners
# ---------------------------------------------------------------------------

VALID_DOMAINS = ("html", "md", "cli")


def run_html_qa(lang: str) -> DomainResult:
    """HTML ドメイン: i18n_check.run_checks + check_i18n_coverage"""
    result = DomainResult(domain="html")
    try:
        from i18n_check import run_checks
        checks = run_checks(lang)
        result.checks = [c.to_dict() for c in checks]
        if any(c.status == "FAIL" for c in checks):
            result.passed = False
    except Exception as e:
        result.passed = False
        result.error = f"HTML QA error: {e}"
    return result


def run_md_qa(lang: str) -> DomainResult:
    """MD ドメイン: i18n_check_md.run_checks"""
    result = DomainResult(domain="md")
    try:
        from i18n_check_md import run_checks
        checks = run_checks(lang)
        result.checks = [c.to_dict() for c in checks]
        if any(c.status == "FAIL" for c in checks):
            result.passed = False
    except Exception as e:
        result.passed = False
        result.error = f"MD QA error: {e}"
    return result


def run_cli_qa() -> DomainResult:
    """CLI ドメイン: POT 鮮度 + 未マーキング print() スキャン"""
    result = DomainResult(domain="cli")
    try:
        from i18n_extract_cli import (
            check_pot_freshness,
            scan_unmarked_prints,
            DEFAULT_CLI_FILES,
            CLI_LOCALES_DIR as cli_loc,
        )
        pot_path = cli_loc / "aiagent.pot"

        # POT 鮮度チェック
        pot_fresh = check_pot_freshness(pot_path, DEFAULT_CLI_FILES)
        result.checks.append({
            "name": "pot_freshness",
            "status": "PASS" if pot_fresh else "FAIL",
            "detail": "POT is up-to-date" if pot_fresh else "POT is stale or missing",
        })

        # 未マーキング print() スキャン
        total_unmarked = 0
        for filepath in DEFAULT_CLI_FILES:
            hits = scan_unmarked_prints(filepath)
            total_unmarked += len(hits)

        result.checks.append({
            "name": "unmarked_prints",
            "status": "PASS" if total_unmarked == 0 else "WARN",
            "count": total_unmarked,
            "detail": f"{total_unmarked} unmarked print() calls found",
        })

        if any(c.get("status") == "FAIL" for c in result.checks):
            result.passed = False

    except Exception as e:
        result.passed = False
        result.error = f"CLI QA error: {e}"
    return result


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def run_all(
    langs: List[str],
    domains: List[str] | None = None,
) -> List[DomainResult]:
    """全ドメインのQAを実行"""
    target_domains = domains or list(VALID_DOMAINS)
    invalid = [d for d in target_domains if d not in VALID_DOMAINS]
    if invalid:
        return [DomainResult(domain=d, passed=False, error=f"不明なドメイン: {d}") for d in invalid]
    results: List[DomainResult] = []

    for domain in target_domains:
        if domain == "html":
            for lang in langs:
                r = run_html_qa(lang)
                r.domain = f"html:{lang}"
                results.append(r)
        elif domain == "md":
            for lang in langs:
                r = run_md_qa(lang)
                r.domain = f"md:{lang}"
                results.append(r)
        elif domain == "cli":
            results.append(run_cli_qa())

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unified i18n QA runner (HTML + MD + CLI)"
    )
    parser.add_argument("--lang", nargs="+", default=["en"],
                        help="Target languages (default: en)")
    parser.add_argument("--domain", nargs="+", default=None,
                        choices=VALID_DOMAINS,
                        help="Domains to check (default: all)")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output results as JSON")
    args = parser.parse_args()

    results = run_all(args.lang, args.domain)

    if args.json_output:
        print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))
    else:
        for r in results:
            icon = "\u2705" if r.passed else "\u274c"
            print(f"\n{icon} {r.domain}")
            if r.error:
                print(f"  ERROR: {r.error}")
            for c in r.checks:
                status = c.get("status", "?")
                name = c.get("name", "?")
                s_icon = {"PASS": "\u2705", "WARN": "\u26a0\ufe0f ", "FAIL": "\u274c"}.get(status, "?")
                print(f"  {s_icon} {name}: {status}")

    has_fail = any(not r.passed for r in results)
    return 1 if has_fail else 0


if __name__ == "__main__":
    sys.exit(main())

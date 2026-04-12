#!/usr/bin/env python3
"""E2E Skill Trigger Test Runner

Tests skill triggers by invoking `claude -p` with trigger phrases
and verifying the correct skill is invoked via stream-json output.
"""
import subprocess
import json
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TestCase:
    trigger: str
    expected_skill: str
    category: str = "positive"  # positive, negative, command

@dataclass
class TestResult:
    test: TestCase
    passed: bool
    invoked_skill: Optional[str] = None
    error: Optional[str] = None
    duration: float = 0.0

def run_claude_test(test: TestCase, timeout: int = 30) -> TestResult:
    """Run a single claude -p test and parse stream-json output."""
    start = time.time()
    try:
        proc = subprocess.run(
            ["claude", "-p", test.trigger, "--output-format", "stream-json"],
            capture_output=True, text=True, timeout=timeout,
            cwd=str(Path(__file__).resolve().parent.parent)
        )
        output = proc.stdout
        invoked_skills = []
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("type") == "assistant":
                # stream-json nests content under message.content
                message = msg.get("message", {})
                content = message.get("content", []) or msg.get("content", [])
                for c in content:
                    if c.get("type") == "tool_use" and c.get("name") == "Skill":
                        skill_name = c.get("input", {}).get("skill", "")
                        invoked_skills.append(skill_name)

        duration = time.time() - start

        if test.category == "negative":
            # Negative test: should NOT invoke the expected skill
            passed = test.expected_skill not in invoked_skills
            return TestResult(
                test=test, passed=passed,
                invoked_skill=invoked_skills[0] if invoked_skills else None,
                duration=duration
            )
        else:
            # Positive test: should invoke the expected skill
            passed = test.expected_skill in invoked_skills
            return TestResult(
                test=test, passed=passed,
                invoked_skill=invoked_skills[0] if invoked_skills else None,
                duration=duration
            )
    except subprocess.TimeoutExpired:
        return TestResult(
            test=test, passed=False,
            error="TIMEOUT", duration=time.time() - start
        )
    except Exception as e:
        return TestResult(
            test=test, passed=False,
            error=str(e), duration=time.time() - start
        )

# ── Test Cases ──────────────────────────────────────────────

SKILL_TESTS: list[TestCase] = [
    # Category: Content Creation
    TestCase("バナーを作って", "banner-creator"),
    TestCase("記事を書いて", "article-writer"),
    TestCase("コピーを書いて", "copywriting"),
    TestCase("SNS投稿を作って", "social-content"),
    TestCase("投稿作って", "content-creator"),
    TestCase("LPを作って", "lp-designer"),
    TestCase("プレゼンを作って", "pptx-creator"),

    # Category: SEO/Marketing
    TestCase("SEOを監査して", "seo-audit"),
    TestCase("広告を出したい", "paid-ads"),
    TestCase("マーケティングアイデア", "marketing-ideas"),
    TestCase("コンテンツ戦略", "content-strategy"),
    TestCase("競合比較", "competitor-alternatives"),
    TestCase("購買心理を教えて", "marketing-psychology"),
    TestCase("ローンチ戦略", "launch-strategy"),
    TestCase("料金を決めたい", "pricing-strategy"),

    # Category: Data/Analytics
    TestCase("データ分析", "data-analyst"),
    TestCase("CSV分析", "csv-analyzer"),
    TestCase("統計分析をして", "statistical-analysis"),
    TestCase("SQLを書いて", "sql-queries"),
    TestCase("データ探索", "exploratory-data-analysis"),

    # Category: Visualization
    TestCase("グラフを作って", "matplotlib"),
    TestCase("インタラクティブグラフを作って", "plotly"),
    TestCase("図を作って", "diagram-generator"),
    TestCase("ダッシュボード作成", "interactive-dashboard-builder"),
    TestCase("論文用のグラフを作って", "scientific-visualization"),

    # Category: Video/Media
    TestCase("動画レビュー", "motion-review"),
    TestCase("MV作成", "mv-composer"),
    TestCase("絵コンテを作って", "storyboard-generator"),
    TestCase("動画のスクリプトを作成", "video-scriptwriter"),
    TestCase("動画を分析", "video-analyzer"),
    TestCase("画像を生成して", "nanobanana"),

    # Category: Document Processing
    TestCase("PDFを圧縮して", "pdf-compressor"),
    TestCase("PDFを分析", "document-processor"),
    TestCase("PPTXを解析して", "pptx-analyzer"),
    TestCase("校閲して", "proofreading-agent"),
    TestCase("議事録をまとめて", "meeting-notes-summarizer"),

    # Category: Communication
    TestCase("Slackで検索して", "slack-search"),
    TestCase("受信箱チェック", "check-inbox"),
    TestCase("メール設計", "email-sequence"),
    TestCase("未返信メッセージ", "slack-unanswered"),

    # Category: Development
    TestCase("コードレビュー", "code-reviewer"),
    TestCase("テスト計画を作って", "test-planner"),
    TestCase("PRD作成", "feature-spec"),
    TestCase("GASデプロイ", "gas-clasp-ops"),
    TestCase("UI設計", "ui-ux-pro-max"),

    # Category: AI Agent Camp specific
    TestCase("セットアップ確認", "aiagent-check-setup"),
    TestCase("リポジトリ案内", "aiagent-guide"),
    TestCase("レッスン開始", "aiagent-lesson-runner"),

    # Category: Misc
    TestCase("A/Bテスト", "ab-test-setup"),
    TestCase("ファクトチェック", "fact-checker"),
    TestCase("操作マニュアルを作って", "tutorial-generator"),
]

NEGATIVE_TESTS: list[TestCase] = [
    TestCase("こんにちは", "banner-creator", category="negative"),
    TestCase("天気を教えて", "seo-audit", category="negative"),
    TestCase("このファイルを読んで", "document-processor", category="negative"),
]

COMMAND_TESTS: list[TestCase] = [
    TestCase("/start-0-1", "start-0-1", category="command"),
    TestCase("/start-1-1", "start-1-1", category="command"),
    TestCase("/check-setup", "check-setup", category="command"),
]


def print_report(results: list[TestResult]):
    """Print test results as a formatted report."""
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    errors = sum(1 for r in results if r.error)

    print("\n" + "=" * 80)
    print("E2E SKILL TRIGGER TEST REPORT")
    print("=" * 80)
    print(f"\nTotal: {len(results)} | Pass: {passed} | Fail: {failed} | Error: {errors}")
    print(f"Duration: {sum(r.duration for r in results):.1f}s total")
    print()

    # Group by category
    for cat_label, cat_key in [("Positive (should fire)", "positive"),
                                ("Negative (should NOT fire)", "negative"),
                                ("Commands", "command")]:
        cat_results = [r for r in results if r.test.category == cat_key]
        if not cat_results:
            continue
        print(f"\n── {cat_label} {'─' * (60 - len(cat_label))}")
        print(f"{'Status':<6} {'Trigger':<30} {'Expected':<28} {'Got':<20} {'Time':<6}")
        print("-" * 90)
        for r in cat_results:
            status = "✅" if r.passed else ("⚠️" if r.error else "❌")
            got = r.error or r.invoked_skill or "(none)"
            print(f"{status:<6} {r.test.trigger:<30} {r.test.expected_skill:<28} {got:<20} {r.duration:.1f}s")

    print("\n" + "=" * 80)

    # Summary of failures
    failures = [r for r in results if not r.passed]
    if failures:
        print("\n🔴 FAILURES:")
        for r in failures:
            got = r.error or r.invoked_skill or "(no skill invoked)"
            print(f"  - '{r.test.trigger}' → expected '{r.test.expected_skill}', got '{got}'")
    else:
        print("\n🟢 ALL TESTS PASSED")


def main():
    all_tests = SKILL_TESTS + NEGATIVE_TESTS + COMMAND_TESTS
    max_workers = int(os.environ.get("E2E_PARALLEL", "5"))
    timeout = int(os.environ.get("E2E_TIMEOUT", "45"))

    # Allow subset via CLI arg
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        all_tests = all_tests[:n]

    print(f"Running {len(all_tests)} E2E tests (parallel={max_workers}, timeout={timeout}s)...")
    print(f"Start: {time.strftime('%H:%M:%S')}")

    results: list[TestResult] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_claude_test, t, timeout): t for t in all_tests}
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            status = "PASS" if result.passed else "FAIL"
            print(f"  [{i}/{len(all_tests)}] {status}: {result.test.trigger} → {result.invoked_skill or result.error or '(none)'} ({result.duration:.1f}s)")
            results.append(result)

    # Sort by original order
    test_order = {id(t): i for i, t in enumerate(all_tests)}
    results.sort(key=lambda r: test_order.get(id(r.test), 999))

    print_report(results)

    # Write JSON report
    report_path = Path(__file__).resolve().parent.parent / "data" / "e2e_trigger_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total": len(results),
        "passed": sum(1 for r in results if r.passed),
        "failed": sum(1 for r in results if not r.passed),
        "results": [
            {
                "trigger": r.test.trigger,
                "expected": r.test.expected_skill,
                "category": r.test.category,
                "passed": r.passed,
                "invoked": r.invoked_skill,
                "error": r.error,
                "duration": round(r.duration, 1),
            }
            for r in results
        ],
    }
    report_path.write_text(json.dumps(report_data, ensure_ascii=False, indent=2))
    print(f"\nJSON report: {report_path}")

    sys.exit(0 if all(r.passed for r in results) else 1)


if __name__ == "__main__":
    main()

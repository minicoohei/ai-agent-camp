#!/usr/bin/env python3
"""
テスト結果を分析し、analysis-report.md を生成する。
テスト実行中でも部分結果から中間レポートを生成可能。
"""

import glob
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "output" / "test-results"
REPORT_PATH = RESULTS_DIR / "analysis-report.md"
REPORT_JSON = RESULTS_DIR / "analysis-report.json"


def analyze_file(filepath):
    """1つの結果ファイルを分析"""
    content = Path(filepath).read_text(errors="replace")
    lines = content.strip().split("\n")
    name = Path(filepath).stem

    result = {
        "name": name,
        "lines": len(lines),
        "status": "unknown",
        "has_summary": False,
        "improvements": [],
        "errors": [],
        "failed_steps": [],
    }

    if len(lines) <= 2 or content.strip() == "":
        result["status"] = "empty"
        return result

    if "TIMEOUT or ERROR" in content and len(lines) < 10:
        result["status"] = "timeout"
        return result

    result["status"] = "ok"

    # Check for summary
    if "実行結果サマリー" in content:
        result["has_summary"] = True

    # Extract improvements
    for line in lines:
        line_stripped = line.strip()
        # Table rows with improvements
        if line_stripped.startswith("|") and any(
            kw in line_stripped
            for kw in ["修正", "更新", "追加", "追記", "存在しない", "不正確", "間違", "FAIL", "リンク切れ", "未作成", "不足"]
        ):
            result["improvements"].append(line_stripped)
        # Numbered improvements
        elif re.match(r"^\d+[.)]", line_stripped) and any(
            kw in line_stripped
            for kw in ["修正", "更新", "追加", "追記", "存在しない", "不正確", "間違", "不足", "未作成", "リンク切れ", "FAIL"]
        ):
            result["improvements"].append(line_stripped)

    # Extract errors/failures
    for line in lines:
        if "FAIL" in line.upper() or "エラー" in line:
            result["errors"].append(line.strip()[:200])

    return result


def generate_report():
    """全結果を分析しレポートを生成"""
    all_results = {"claude-code": {}, "codex": {}, "cursor": {}}

    for cli in all_results:
        pattern = str(RESULTS_DIR / cli / "start-*.txt")
        for f in sorted(glob.glob(pattern)):
            r = analyze_file(f)
            all_results[cli][r["name"]] = r

    # Aggregate stats
    stats = {}
    for cli, results in all_results.items():
        s = Counter()
        for r in results.values():
            s[r["status"]] += 1
            s["total"] += 1
            if r["has_summary"]:
                s["with_summary"] += 1
            s["improvements"] += len(r["improvements"])
        stats[cli] = dict(s)

    # Collect all improvements across CLIs
    all_improvements = defaultdict(list)
    for cli, results in all_results.items():
        for name, r in results.items():
            for imp in r["improvements"]:
                all_improvements[name].append({"cli": cli, "text": imp})

    # Categorize issues
    categories = {
        "broken_links": [],  # リンク切れ・パス不在
        "content_accuracy": [],  # 内容の不正確さ
        "missing_resources": [],  # 必要ファイル・画像の未同梱
        "ux_improvements": [],  # わかりにくさ・UX改善
        "version_updates": [],  # バージョン・数値の更新
        "cross_tool": [],  # ツール間差異
    }

    for name, imps in all_improvements.items():
        for imp in imps:
            text = imp["text"].lower()
            if any(kw in text for kw in ["リンク切れ", "存在しない", "未作成", "パス"]):
                categories["broken_links"].append({"lesson": name, **imp})
            elif any(kw in text for kw in ["不正確", "間違", "fail"]):
                categories["content_accuracy"].append({"lesson": name, **imp})
            elif any(kw in text for kw in ["未同梱", "サンプル", "不足", "画像"]):
                categories["missing_resources"].append({"lesson": name, **imp})
            elif any(kw in text for kw in ["わかり", "説明", "追記", "注記", "ガイダンス"]):
                categories["ux_improvements"].append({"lesson": name, **imp})
            elif any(kw in text for kw in ["バージョン", "数値", "更新", "料金"]):
                categories["version_updates"].append({"lesson": name, **imp})
            else:
                categories["cross_tool"].append({"lesson": name, **imp})

    # Generate markdown report
    report = []
    report.append("# 全レッスン × 3 CLI テスト分析レポート\n")
    report.append(f"生成日時: {__import__('datetime').datetime.now().isoformat()}\n")

    report.append("## 1. 実行結果サマリー\n")
    report.append("| CLI | 完了 | OK | Empty | Timeout | 改善提案数 |")
    report.append("|-----|------|-----|-------|---------|-----------|")
    for cli, s in stats.items():
        report.append(
            f"| {cli} | {s.get('total',0)} | {s.get('ok',0)} | "
            f"{s.get('empty',0)} | {s.get('timeout',0)} | {s.get('improvements',0)} |"
        )

    report.append("\n## 2. 問題カテゴリ別一覧\n")

    cat_names = {
        "broken_links": "リンク切れ・パス不在",
        "content_accuracy": "内容の不正確さ",
        "missing_resources": "必要リソースの未同梱",
        "ux_improvements": "UX・わかりやすさ改善",
        "version_updates": "バージョン・数値の更新",
        "cross_tool": "その他・ツール間差異",
    }

    for cat_key, cat_label in cat_names.items():
        items = categories[cat_key]
        report.append(f"### {cat_label} ({len(items)}件)\n")
        if items:
            for item in items:
                report.append(f"- **{item['lesson']}** [{item['cli']}]: {item['text'][:200]}")
        else:
            report.append("(なし)")
        report.append("")

    report.append("## 3. レッスン別詳細\n")
    # Get all unique lesson names
    all_lessons = set()
    for cli_results in all_results.values():
        all_lessons.update(cli_results.keys())

    for lesson in sorted(all_lessons):
        statuses = []
        for cli in ["claude-code", "codex", "cursor"]:
            r = all_results[cli].get(lesson)
            if r:
                statuses.append(f"{cli}={r['status']}")
            else:
                statuses.append(f"{cli}=未実行")

        imps = all_improvements.get(lesson, [])
        if imps:
            report.append(f"#### {lesson}")
            report.append(f"状態: {', '.join(statuses)}")
            report.append(f"改善提案: {len(imps)}件")
            for imp in imps:
                report.append(f"  - [{imp['cli']}] {imp['text'][:200]}")
            report.append("")

    # Write report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(report))

    # Write JSON
    json_data = {
        "stats": stats,
        "categories": {k: len(v) for k, v in categories.items()},
        "improvements_by_lesson": {k: [i["text"] for i in v] for k, v in all_improvements.items()},
        "all_results_status": {
            cli: {name: r["status"] for name, r in results.items()}
            for cli, results in all_results.items()
        },
    }
    with open(REPORT_JSON, "w") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"Report: {REPORT_PATH}")
    print(f"JSON:   {REPORT_JSON}")
    print(f"\nStats: {json.dumps(stats, indent=2, ensure_ascii=False)}")
    print(f"\nCategories: {json.dumps({k: len(v) for k, v in categories.items()}, indent=2)}")


if __name__ == "__main__":
    generate_report()

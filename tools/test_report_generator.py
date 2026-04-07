#!/usr/bin/env python3
"""
test_report_generator.py - pytest HTML レポートからサマリーを生成する

Usage:
    uv run python tools/test_report_generator.py \
        --input output/pm/unit-test-evidence/report.html \
        --output output/pm/unit-test-evidence/summary.md

Lesson 14-16 (単体テスト実施) で使用するユーティリティスクリプト。
pytest-html が生成した HTML レポートを読み取り、Markdown 形式のサマリーを出力します。
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="pytest HTML レポートからテスト結果サマリーを生成する"
    )
    parser.add_argument(
        "--input", "-i", required=True, help="pytest-html が生成した HTML レポートファイル"
    )
    parser.add_argument(
        "--output", "-o", default=None, help="出力先 Markdown ファイル（省略時は stdout）"
    )
    return parser.parse_args()


def extract_summary_from_html(html_content: str) -> dict:
    """HTML レポートからテスト結果の数値を抽出する（簡易パーサー）"""
    summary = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
        "duration": "N/A",
    }

    # pytest-html の結果行からデータ抽出を試みる
    passed_match = re.search(r"(\d+)\s+passed", html_content)
    failed_match = re.search(r"(\d+)\s+failed", html_content)
    skipped_match = re.search(r"(\d+)\s+skipped", html_content)
    error_match = re.search(r"(\d+)\s+error", html_content)
    duration_match = re.search(r"([\d.]+)\s*seconds?", html_content)

    if passed_match:
        summary["passed"] = int(passed_match.group(1))
    if failed_match:
        summary["failed"] = int(failed_match.group(1))
    if skipped_match:
        summary["skipped"] = int(skipped_match.group(1))
    if error_match:
        summary["errors"] = int(error_match.group(1))
    if duration_match:
        summary["duration"] = f"{duration_match.group(1)} 秒"

    summary["total"] = summary["passed"] + summary["failed"] + summary["skipped"] + summary["errors"]
    return summary


def generate_markdown(summary: dict, input_path: str) -> str:
    """Markdown 形式のサマリーを生成する"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = summary["total"] or 1  # avoid division by zero
    pass_rate = (summary["passed"] / total) * 100

    md = f"""# 単体テスト実行レポート

## 概要
- 実行日時: {now}
- 入力レポート: `{input_path}`

## テスト結果

| 項目 | 結果 |
|------|------|
| 実行テスト数 | {summary['total']} |
| 成功 | {summary['passed']} ({pass_rate:.1f}%) |
| 失敗 | {summary['failed']} |
| スキップ | {summary['skipped']} |
| エラー | {summary['errors']} |
| 実行時間 | {summary['duration']} |

## 判定

{'**PASS** - すべてのテストが成功しました。' if summary['failed'] == 0 and summary['errors'] == 0 else '**FAIL** - 失敗またはエラーのあるテストがあります。詳細は HTML レポートを確認してください。'}
"""
    return md


def main():
    args = parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"エラー: 入力ファイルが見つかりません: {args.input}", file=sys.stderr)
        sys.exit(1)

    html_content = input_path.read_text(encoding="utf-8")
    summary = extract_summary_from_html(html_content)
    markdown = generate_markdown(summary, args.input)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
        print(f"サマリーを出力しました: {args.output}", file=sys.stderr)
    else:
        print(markdown)


if __name__ == "__main__":
    main()

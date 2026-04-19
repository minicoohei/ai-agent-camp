"""レッスン CLI 実行スモークテスト

各モジュールから1本ずつレッスンを claude -p で実行し、
エラーなく応答が返ることを検証する。

実行:
    python -m pytest tests/e2e/test_smoke_invocation.py -v -m slow
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tests.e2e.lesson_quality_helpers import write_evidence_report

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLAUDE_LESSON_DIR = PROJECT_ROOT / ".claude" / "commands" / "lesson"
OUTPUT_DIR = PROJECT_ROOT / "output" / "test-results" / "claude-code"

# 各モジュールから1本ずつ（計21本）
SAMPLE_LESSONS = [
    "start-0-1",   # Module 0: セットアップ
    "start-1-1",   # Module 1: バナー
    "start-2-1",   # Module 2: 図解
    "start-3-1",   # Module 3: チュートリアル
    "start-4-1",   # Module 4: Google Workspace
    "start-5-1",   # Module 5: PowerPoint
    "start-6-1",   # Module 6: エージェント開発
    "start-7-1",   # Module 7: Skill/Commands
    "start-8-1",   # Module 8: データ分析
    "start-9-1",   # Module 9: Slack連携
    "start-10-1",  # Module 10: GAS
    "start-11-1",  # Module 11: GitHub Actions
    "start-12-1",  # Module 12: Notion
    "start-13-1",  # Module 13: LP制作
    "start-14-1",  # Module 14: 記事制作
    "start-15-1",  # Module 15: 動画制作
    "start-16-1",  # Module 16: メール/LINE
    "start-17-1",  # Module 17: マーケティング
    "start-18-1",  # Module 18: 要件定義
    "start-19-1",  # Module 19: Outlook
    "start-20-1",  # Module 20: Freee
]

SUFFIX_PROMPT = """

---
【自動テスト指示】
上記レッスンの内容を読み、以下を実行してください：
1. 最初の AskQuestion には「準備OK！始めましょう」を選択
2. 各ステップは「例だけ確認する」を選択
3. 最後に以下の形式で要約を出力：
---
## テスト実行サマリー
- レッスン名: (ファイル名)
- ステップ数: (確認したステップ数)
- 図解の有無: (Mermaid/ASCII art/テーブルの有無)
- 初学者向け評価: (1-5点、5が最もわかりやすい)
- 改善提案: (あれば)
---"""

ERROR_INDICATORS = [
    "Traceback",
    "ModuleNotFoundError",
    "ImportError",
    "SyntaxError",
    "command not found",
    "TIMEOUT or ERROR",
    "Permission denied",
    "FileNotFoundError",
]


@pytest.mark.slow
@pytest.mark.integration
class TestLessonSmokeInvocation:
    """各モジュール代表レッスンの CLI 実行テスト"""

    @pytest.mark.parametrize("lesson_id", SAMPLE_LESSONS, ids=lambda x: x)
    def test_lesson_invokes_without_error(self, lesson_id: str):
        """claude -p でレッスンを実行しエラーがないこと"""
        md_file = CLAUDE_LESSON_DIR / f"{lesson_id}.md"
        if not md_file.exists():
            pytest.skip(f"{lesson_id}.md not found")

        out_file = OUTPUT_DIR / f"{lesson_id}.txt"

        # 既存の結果が十分な長さならスキップ（再実行コスト回避）
        if out_file.exists() and out_file.stat().st_size > 500:
            output = out_file.read_text(encoding="utf-8", errors="replace")
        else:
            # claude CLI が使えるか確認
            try:
                subprocess.run(["claude", "--version"], capture_output=True, timeout=10, check=True)
            except (FileNotFoundError, subprocess.CalledProcessError):
                pytest.skip("claude CLI not available")

            prompt = md_file.read_text(encoding="utf-8") + SUFFIX_PROMPT
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            try:
                result = subprocess.run(
                    ["claude", "-p", "-", "--allowedTools", "*"],
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                output = result.stdout + result.stderr
            except subprocess.TimeoutExpired:
                output = "TIMEOUT or ERROR"

            out_file.write_text(output, encoding="utf-8")

        # エラーインジケーターをチェック
        errors_found = [ind for ind in ERROR_INDICATORS if ind in output]
        if errors_found:
            # TIMEOUT は xfail（API制限等の外部要因）
            if "TIMEOUT or ERROR" in errors_found:
                pytest.xfail(f"Timeout: {lesson_id}")
            pytest.fail(f"Error indicators found in {lesson_id}: {errors_found}")

    @pytest.mark.parametrize("lesson_id", SAMPLE_LESSONS, ids=lambda x: x)
    def test_output_has_reasonable_length(self, lesson_id: str):
        """実行結果が10行以上あること"""
        out_file = OUTPUT_DIR / f"{lesson_id}.txt"
        if not out_file.exists():
            pytest.skip(f"No output for {lesson_id} (run smoke test first)")
        lines = out_file.read_text(encoding="utf-8", errors="replace").strip().split("\n")
        assert len(lines) >= 10, f"{lesson_id}: output too short ({len(lines)} lines)"

    def test_generate_smoke_report(self):
        """smoke-invocation-report.json を生成"""
        results = []
        for lesson_id in SAMPLE_LESSONS:
            out_file = OUTPUT_DIR / f"{lesson_id}.txt"
            if out_file.exists():
                output = out_file.read_text(encoding="utf-8", errors="replace")
                errors = [ind for ind in ERROR_INDICATORS if ind in output]
                line_count = len(output.strip().split("\n"))
                has_summary = "テスト実行サマリー" in output or "実行結果サマリー" in output
                results.append({
                    "lesson": lesson_id,
                    "status": "FAIL" if errors else "PASS",
                    "line_count": line_count,
                    "has_summary": has_summary,
                    "errors": errors,
                })
            else:
                results.append({
                    "lesson": lesson_id,
                    "status": "SKIP",
                    "line_count": 0,
                    "has_summary": False,
                    "errors": ["no output file"],
                })

        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        skipped = sum(1 for r in results if r["status"] == "SKIP")

        report = {
            "total_lessons": len(SAMPLE_LESSONS),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "results": results,
        }
        path = write_evidence_report(report, "smoke-invocation-report.json")
        assert path.exists()

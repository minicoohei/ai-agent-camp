"""analyze_lesson_results.py の単体テスト。

テスト結果ファイルの分析、レポート生成を検証する。
"""

import json
from pathlib import Path

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    return import_module_from_repo("analyze_lesson_results", "tools/analyze_lesson_results.py")


# ===========================================================================
# analyze_file
# ===========================================================================

class TestAnalyzeFile:
    def test_empty_file(self, mod, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        result = mod.analyze_file(str(f))
        assert result["status"] == "empty"

    def test_two_line_file(self, mod, tmp_path):
        f = tmp_path / "short.txt"
        f.write_text("line1\nline2")
        result = mod.analyze_file(str(f))
        assert result["status"] == "empty"

    def test_timeout_file(self, mod, tmp_path):
        f = tmp_path / "timeout.txt"
        # Need > 2 lines but < 10 lines with "TIMEOUT or ERROR"
        f.write_text("TIMEOUT or ERROR\nline2\nline3\nline4\n")
        result = mod.analyze_file(str(f))
        assert result["status"] == "timeout"

    def test_ok_file(self, mod, tmp_path):
        f = tmp_path / "ok.txt"
        content = "\n".join([f"Line {i}" for i in range(20)])
        f.write_text(content)
        result = mod.analyze_file(str(f))
        assert result["status"] == "ok"
        assert result["lines"] == 20

    def test_with_summary(self, mod, tmp_path):
        f = tmp_path / "summary.txt"
        f.write_text("実行結果サマリー\n" + "\n".join([f"line {i}" for i in range(10)]))
        result = mod.analyze_file(str(f))
        assert result["has_summary"] is True

    def test_improvements_table_row(self, mod, tmp_path):
        """テーブル行形式の改善提案"""
        f = tmp_path / "improvements.txt"
        content = "\n".join([
            "header",
            "| ページ | 修正が必要 |",
            "| リンク切れ | 更新してください |",
            "| 追加すべき | 追記してください |",
        ] + [f"line {i}" for i in range(10)])
        f.write_text(content)
        result = mod.analyze_file(str(f))
        assert len(result["improvements"]) >= 2

    def test_improvements_numbered(self, mod, tmp_path):
        """番号付き改善提案"""
        f = tmp_path / "numbered.txt"
        content = "\n".join([
            "heading",
            "1. 修正が必要なファイル",
            "2) 追加すべきドキュメント",
            "3. 正常な行",
        ] + [f"line {i}" for i in range(10)])
        f.write_text(content)
        result = mod.analyze_file(str(f))
        assert len(result["improvements"]) >= 2

    def test_errors_detected(self, mod, tmp_path):
        """FAIL/エラー検出"""
        f = tmp_path / "errors.txt"
        content = "\n".join([
            "Test FAIL: something broke",
            "エラーが発生しました",
            "This is fine",
        ] + [f"line {i}" for i in range(10)])
        f.write_text(content)
        result = mod.analyze_file(str(f))
        assert len(result["errors"]) >= 2

    def test_error_text_truncated(self, mod, tmp_path):
        """エラーテキストが200文字で切られる"""
        f = tmp_path / "long_error.txt"
        long_line = "FAIL " + "x" * 300
        content = long_line + "\n" + "\n".join([f"l{i}" for i in range(10)])
        f.write_text(content)
        result = mod.analyze_file(str(f))
        assert all(len(e) <= 200 for e in result["errors"])

    def test_name_from_stem(self, mod, tmp_path):
        f = tmp_path / "start-1-2.txt"
        f.write_text("\n".join([f"line {i}" for i in range(10)]))
        result = mod.analyze_file(str(f))
        assert result["name"] == "start-1-2"

    def test_keywords_detection(self, mod, tmp_path):
        """各種キーワード: 存在しない, 不正確, 間違, 未作成, 不足, リンク切れ"""
        keywords = ["存在しない", "不正確", "間違い", "FAIL", "リンク切れ", "未作成", "不足"]
        for kw in keywords:
            f = tmp_path / f"kw_{kw}.txt"
            content = f"| test | {kw} |\n" + "\n".join([f"l{i}" for i in range(10)])
            f.write_text(content)
            result = mod.analyze_file(str(f))
            assert len(result["improvements"]) >= 1, f"Failed to detect keyword: {kw}"


# ===========================================================================
# generate_report
# ===========================================================================

class TestGenerateReport:
    def test_empty_results(self, mod, tmp_path):
        """結果ファイルがない場合"""
        results_dir = tmp_path / "output" / "test-results"
        for cli in ["claude-code", "codex", "cursor"]:
            (results_dir / cli).mkdir(parents=True)

        with _patch_dirs(mod, results_dir):
            mod.generate_report()

        report_path = results_dir / "analysis-report.md"
        assert report_path.exists()
        json_path = results_dir / "analysis-report.json"
        assert json_path.exists()

    def test_with_result_files(self, mod, tmp_path):
        """結果ファイルがある場合"""
        results_dir = tmp_path / "output" / "test-results"
        for cli in ["claude-code", "codex", "cursor"]:
            cli_dir = results_dir / cli
            cli_dir.mkdir(parents=True)
            (cli_dir / "start-1-1.txt").write_text(
                "実行結果サマリー\n" + "\n".join([f"line {i}" for i in range(20)])
            )
            (cli_dir / "start-1-2.txt").write_text(
                "| 修正が必要 |\n" + "\n".join([f"line {i}" for i in range(20)])
            )

        with _patch_dirs(mod, results_dir):
            mod.generate_report()

        json_path = results_dir / "analysis-report.json"
        data = json.loads(json_path.read_text())
        assert "stats" in data
        assert "categories" in data

    def test_categorization(self, mod, tmp_path):
        """カテゴリ分類"""
        results_dir = tmp_path / "output" / "test-results"
        cli_dir = results_dir / "claude-code"
        cli_dir.mkdir(parents=True)
        (results_dir / "codex").mkdir(parents=True)
        (results_dir / "cursor").mkdir(parents=True)

        content_lines = [
            "| リンク切れ発見 |",
            "| 不正確な記述 |",
            "| サンプル不足 |",
            "| わかりにくい説明 |",
            "| バージョン更新 |",
            "| その他の問題 |",
        ] + [f"line {i}" for i in range(10)]
        (cli_dir / "start-2-1.txt").write_text("\n".join(content_lines))

        with _patch_dirs(mod, results_dir):
            mod.generate_report()

        json_path = results_dir / "analysis-report.json"
        data = json.loads(json_path.read_text())
        # At least some categories should have items
        total = sum(data["categories"].values())
        assert total >= 1


def _patch_dirs(mod, results_dir):
    """RESULTS_DIR, REPORT_PATH, REPORT_JSON を tmp_path 下にパッチ"""
    from unittest.mock import patch
    return patch.multiple(
        mod,
        RESULTS_DIR=results_dir,
        REPORT_PATH=results_dir / "analysis-report.md",
        REPORT_JSON=results_dir / "analysis-report.json",
    )


# ===========================================================================
# Boundary tests
# ===========================================================================

class TestBoundary:
    def test_single_line_file(self, mod, tmp_path):
        f = tmp_path / "single.txt"
        f.write_text("only one line")
        result = mod.analyze_file(str(f))
        assert result["status"] == "empty"  # <= 2 lines

    def test_three_lines_ok(self, mod, tmp_path):
        f = tmp_path / "three.txt"
        f.write_text("a\nb\nc")
        result = mod.analyze_file(str(f))
        assert result["status"] == "ok"

    def test_timeout_with_many_lines_is_ok(self, mod, tmp_path):
        """TIMEOUT or ERRORがあっても10行以上ならok"""
        f = tmp_path / "long_timeout.txt"
        content = "TIMEOUT or ERROR\n" + "\n".join([f"line {i}" for i in range(20)])
        f.write_text(content)
        result = mod.analyze_file(str(f))
        assert result["status"] == "ok"

    def test_unicode_content(self, mod, tmp_path):
        """Unicode文字を含むファイル"""
        f = tmp_path / "unicode.txt"
        content = "日本語テスト\n" + "\n".join([f"行 {i}" for i in range(10)])
        f.write_text(content, encoding="utf-8")
        result = mod.analyze_file(str(f))
        assert result["status"] == "ok"

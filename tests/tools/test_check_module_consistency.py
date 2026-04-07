"""check_module_consistency.py の単体テスト。

CURRICULUM.md と MODULES_GUIDE.md の整合性チェックロジックをテストする。
"""
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import import_module_from_repo

cmc = import_module_from_repo("check_module_consistency", "tools/check_module_consistency.py")

parse_curriculum = cmc.parse_curriculum
parse_modules_guide = cmc.parse_modules_guide
main = cmc.main
CURRICULUM_ROW_RE = cmc.CURRICULUM_ROW_RE
MODULE_HEADER_RE = cmc.MODULE_HEADER_RE
MODULE_HEADER_NOPAREN_RE = cmc.MODULE_HEADER_NOPAREN_RE


# ---------------------------------------------------------------------------
# parse_curriculum
# ---------------------------------------------------------------------------

class TestParseCurriculum:
    def test_basic_table(self):
        text = """\
## Phase 3: コアスキル習得
| モジュール | 名前 | 時間 |
|--|--|--|
| 1 | バナー・画像生成 | 90分 |
| 2 | 図表・フロー作成 | 60分 |
"""
        result = parse_curriculum(text)
        assert result == {1: "バナー・画像生成", 2: "図表・フロー作成"}

    def test_stops_at_next_section(self):
        text = """\
## Phase 3: コアスキル習得
| 1 | バナー・画像生成 | 90分 |
## Phase 4
| 99 | Should not appear |
"""
        result = parse_curriculum(text)
        assert 1 in result
        assert 99 not in result

    def test_stops_at_separator(self):
        text = """\
## Phase 3: コアスキル習得
| 1 | バナー・画像生成 | 90分 |
---
| 99 | Should not appear |
"""
        result = parse_curriculum(text)
        assert 1 in result
        assert 99 not in result

    def test_empty_text(self):
        assert parse_curriculum("") == {}

    def test_no_phase3(self):
        text = "## Phase 1: Intro\nSome text\n"
        assert parse_curriculum(text) == {}

    def test_skips_header_row(self):
        text = """\
## Phase 3: コアスキル習得
| モジュール | 名前 |
|--|--|
| 1 | Test |
"""
        result = parse_curriculum(text)
        assert 1 in result
        # "モジュール" should not be parsed as a number
        assert len(result) == 1

    def test_single_module(self):
        text = "## Phase 3: コアスキル習得\n| 5 | PPTX操作 | 45分 |\n"
        result = parse_curriculum(text)
        assert result == {5: "PPTX操作"}

    def test_many_modules(self):
        lines = ["## Phase 3: コアスキル習得\n"]
        for i in range(1, 19):
            lines.append(f"| {i} | Module{i} | 60分 |\n")
        text = "".join(lines)
        result = parse_curriculum(text)
        assert len(result) == 18


# ---------------------------------------------------------------------------
# parse_modules_guide
# ---------------------------------------------------------------------------

class TestParseModulesGuide:
    def test_with_english_name(self):
        text = "### Module 1: バナー・画像生成 (Banner & Image Generation)\n"
        result = parse_modules_guide(text)
        assert result == {1: "バナー・画像生成"}

    def test_without_english_name(self):
        text = "### Module 1: バナー・画像生成\n"
        result = parse_modules_guide(text)
        assert result == {1: "バナー・画像生成"}

    def test_multiple_modules(self):
        text = """\
### Module 1: バナー・画像生成 (Banner)
### Module 2: 図表・フロー作成 (Charts)
### Module 3: スクショ分析 (Screenshot)
"""
        result = parse_modules_guide(text)
        assert len(result) == 3
        assert result[2] == "図表・フロー作成"

    def test_empty_text(self):
        assert parse_modules_guide("") == {}

    def test_non_module_headers_ignored(self):
        text = """\
### Introduction
### Module 1: Test (Eng)
### Other section
"""
        result = parse_modules_guide(text)
        assert len(result) == 1

    def test_module_zero(self):
        text = "### Module 0: セットアップ (Setup)\n"
        result = parse_modules_guide(text)
        assert result == {0: "セットアップ"}


# ---------------------------------------------------------------------------
# Regex tests
# ---------------------------------------------------------------------------

class TestRegexPatterns:
    def test_curriculum_row_re_match(self):
        line = "| 1 | バナー・画像生成 | 90分 | 3 |"
        m = CURRICULUM_ROW_RE.match(line)
        assert m is not None
        assert m.group(1) == "1"
        assert m.group(2).strip() == "バナー・画像生成"

    def test_curriculum_row_re_no_match_header(self):
        line = "| モジュール | 名前 |"
        m = CURRICULUM_ROW_RE.match(line)
        assert m is None  # "モジュール" is not a digit

    def test_module_header_re_with_parens(self):
        line = "### Module 10: Notion連携 (Notion Integration)"
        m = MODULE_HEADER_RE.match(line)
        assert m is not None
        assert m.group(1) == "10"
        assert m.group(2) == "Notion連携"

    def test_module_header_noparen_re(self):
        line = "### Module 5: PPTX操作"
        m = MODULE_HEADER_NOPAREN_RE.match(line)
        assert m is not None
        assert m.group(1) == "5"


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

class TestMain:
    def test_files_missing(self, tmp_path, capsys):
        with patch.object(cmc, "CURRICULUM_PATH", tmp_path / "CURRICULUM.md"), \
             patch.object(cmc, "MODULES_GUIDE_PATH", tmp_path / "MODULES_GUIDE.md"), \
             patch.object(cmc, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 1
        assert "FAIL" in capsys.readouterr().out

    def test_curriculum_missing_only(self, tmp_path, capsys):
        guide = tmp_path / "MODULES_GUIDE.md"
        guide.write_text("### Module 1: Test (Eng)\n")
        with patch.object(cmc, "CURRICULUM_PATH", tmp_path / "CURRICULUM.md"), \
             patch.object(cmc, "MODULES_GUIDE_PATH", guide), \
             patch.object(cmc, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 1

    def test_consistent_modules(self, tmp_path, capsys):
        curriculum = tmp_path / "CURRICULUM.md"
        curriculum.write_text(
            "## Phase 3: コアスキル習得\n"
            "| 1 | バナー | 90分 |\n"
        )
        guide = tmp_path / "MODULES_GUIDE.md"
        guide.write_text("### Module 1: バナー (Banner)\n")

        with patch.object(cmc, "CURRICULUM_PATH", curriculum), \
             patch.object(cmc, "MODULES_GUIDE_PATH", guide), \
             patch.object(cmc, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 0
        assert "OK" in capsys.readouterr().out

    def test_name_mismatch(self, tmp_path, capsys):
        curriculum = tmp_path / "CURRICULUM.md"
        curriculum.write_text(
            "## Phase 3: コアスキル習得\n"
            "| 1 | バナー生成 | 90分 |\n"
        )
        guide = tmp_path / "MODULES_GUIDE.md"
        guide.write_text("### Module 1: 画像生成 (Image)\n")

        with patch.object(cmc, "CURRICULUM_PATH", curriculum), \
             patch.object(cmc, "MODULES_GUIDE_PATH", guide), \
             patch.object(cmc, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 1
        out = capsys.readouterr().out
        assert "mismatch" in out

    def test_module_only_in_curriculum(self, tmp_path, capsys):
        curriculum = tmp_path / "CURRICULUM.md"
        curriculum.write_text(
            "## Phase 3: コアスキル習得\n"
            "| 1 | バナー | 90分 |\n"
            "| 2 | 図表 | 60分 |\n"
        )
        guide = tmp_path / "MODULES_GUIDE.md"
        guide.write_text("### Module 1: バナー (Banner)\n")

        with patch.object(cmc, "CURRICULUM_PATH", curriculum), \
             patch.object(cmc, "MODULES_GUIDE_PATH", guide), \
             patch.object(cmc, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 1

    def test_module_0_excluded_from_error(self, tmp_path, capsys):
        """Module 0 is in Phase 2, so it being only in guide should not cause error."""
        curriculum = tmp_path / "CURRICULUM.md"
        curriculum.write_text(
            "## Phase 3: コアスキル習得\n"
            "| 1 | バナー | 90分 |\n"
        )
        guide = tmp_path / "MODULES_GUIDE.md"
        guide.write_text(
            "### Module 0: セットアップ (Setup)\n"
            "### Module 1: バナー (Banner)\n"
        )

        with patch.object(cmc, "CURRICULUM_PATH", curriculum), \
             patch.object(cmc, "MODULES_GUIDE_PATH", guide), \
             patch.object(cmc, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 0

    def test_empty_files(self, tmp_path, capsys):
        curriculum = tmp_path / "CURRICULUM.md"
        curriculum.write_text("")
        guide = tmp_path / "MODULES_GUIDE.md"
        guide.write_text("")

        with patch.object(cmc, "CURRICULUM_PATH", curriculum), \
             patch.object(cmc, "MODULES_GUIDE_PATH", guide), \
             patch.object(cmc, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 0  # No modules to compare

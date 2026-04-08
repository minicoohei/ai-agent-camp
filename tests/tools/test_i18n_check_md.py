"""tests for tools/i18n_check_md.py — Phase 5: MD QA checks"""

import json
from pathlib import Path

import pytest

from tests.conftest import import_module_from_repo

_MOD_PATH = "tools/i18n_check_md.py"
_COMMON_PATH = "tools/i18n_common.py"
_CHECK_PATH = "tools/i18n_check.py"


@pytest.fixture
def mod():
    import_module_from_repo("i18n_common", _COMMON_PATH)
    import_module_from_repo("i18n_check", _CHECK_PATH)
    return import_module_from_repo("i18n_check_md", _MOD_PATH)


# ===========================================================================
# helpers
# ===========================================================================

def _write_md(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


VALID_MD = """\
---
description: "Test lesson"
---

# Hello

Some text with `git clone` command.

| Col1 | Col2 |
|------|------|
| a    | b    |

![alt](images/test.png)
"""

SOURCE_MD = VALID_MD


# ===========================================================================
# TestFrontmatterIntegrity
# ===========================================================================


class TestFrontmatterIntegrity:
    def test_valid_frontmatter_passes(self, mod):
        """有効な frontmatter は PASS"""
        src = {"test.md": SOURCE_MD}
        trans = {"test.md": VALID_MD}
        result = mod.check_frontmatter_integrity("en", src, trans)
        assert result.status == "PASS"
        assert result.passed == 1

    def test_missing_frontmatter_fails(self, mod):
        """frontmatter がない MD は FAIL"""
        trans = {"test.md": "# No frontmatter\n\nSome text.\n"}
        result = mod.check_frontmatter_integrity("en", {}, trans)
        assert result.status == "FAIL"
        assert len(result.issues) == 1

    def test_missing_description_fails(self, mod):
        """description フィールドがない場合 FAIL"""
        trans = {"test.md": "---\ntitle: Test\n---\n\n# Hello\n"}
        result = mod.check_frontmatter_integrity("en", {}, trans)
        assert result.status == "FAIL"

    def test_japanese_residue_warns(self, mod):
        """非日本語言語で frontmatter に日本語残留 → WARN"""
        trans = {"test.md": '---\ndescription: "テストレッスン"\n---\n\n# Hello\n'}
        result = mod.check_frontmatter_integrity("en", {}, trans)
        assert result.status == "WARN"

    def test_japanese_residue_ignored_for_ja(self, mod):
        """lang=ja なら日本語残留チェックはスキップ"""
        trans = {"test.md": '---\ndescription: "テストレッスン"\n---\n\n# Hello\n'}
        result = mod.check_frontmatter_integrity("ja", {}, trans)
        assert result.status == "PASS"

    def test_multiple_files_pass_count(self, mod):
        """複数ファイル時の passed カウントが正確"""
        trans = {
            "a.md": '---\ndescription: "A"\n---\n',
            "b.md": "# no frontmatter\n",
            "c.md": '---\ndescription: "C"\n---\n',
        }
        result = mod.check_frontmatter_integrity("en", {}, trans)
        assert result.passed == 2
        assert result.total == 3


# ===========================================================================
# TestKeyCoverage
# ===========================================================================


class TestKeyCoverage:
    def test_full_coverage_passes(self, mod, tmp_path):
        """完全一致は PASS"""
        ja = {"file.md": {"key1": "値1", "key2": "値2"}}
        en = {"file.md": {"key1": "val1", "key2": "val2"}}
        ja_path = tmp_path / "locales" / "md" / "ja.json"
        en_path = tmp_path / "locales" / "md" / "en.json"
        ja_path.parent.mkdir(parents=True)
        ja_path.write_text(json.dumps(ja), encoding="utf-8")
        en_path.write_text(json.dumps(en), encoding="utf-8")

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "MD_LOCALES_DIR", tmp_path / "locales" / "md")
            result = mod.check_key_coverage("en")

        assert result.status == "PASS"
        assert result.passed == 1

    def test_missing_keys_warns(self, mod, tmp_path):
        """キー欠落は WARN"""
        ja = {"file.md": {"key1": "値1", "key2": "値2", "key3": "値3"}}
        en = {"file.md": {"key1": "val1"}}
        ja_path = tmp_path / "locales" / "md" / "ja.json"
        en_path = tmp_path / "locales" / "md" / "en.json"
        ja_path.parent.mkdir(parents=True)
        ja_path.write_text(json.dumps(ja), encoding="utf-8")
        en_path.write_text(json.dumps(en), encoding="utf-8")

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "MD_LOCALES_DIR", tmp_path / "locales" / "md")
            result = mod.check_key_coverage("en")

        assert result.status == "WARN"
        assert "2 キーが欠落" in result.issues[0].message

    def test_missing_lang_json_fails(self, mod, tmp_path):
        """lang.json が存在しない場合 FAIL"""
        ja = {"file.md": {"key1": "値1"}}
        ja_path = tmp_path / "locales" / "md" / "ja.json"
        ja_path.parent.mkdir(parents=True)
        ja_path.write_text(json.dumps(ja), encoding="utf-8")

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "MD_LOCALES_DIR", tmp_path / "locales" / "md")
            result = mod.check_key_coverage("en")

        assert result.status == "FAIL"


# ===========================================================================
# TestTableCellCount
# ===========================================================================


class TestTableCellCount:
    def test_matching_columns_passes(self, mod):
        """列数一致は PASS"""
        md = "| A | B |\n|---|---|\n| 1 | 2 |\n"
        result = mod.check_table_cell_count("en", {"f.md": md}, {"f.md": md})
        assert result.status == "PASS"

    def test_mismatched_columns_fails(self, mod):
        """列数不一致は FAIL"""
        src = "| A | B |\n|---|---|\n| 1 | 2 |\n"
        trans = "| A | B | C |\n|---|---|---|\n| 1 | 2 | 3 |\n"
        result = mod.check_table_cell_count("en", {"f.md": src}, {"f.md": trans})
        assert result.status == "FAIL"

    def test_no_tables_total_zero(self, mod):
        """テーブルなしファイルは total=0"""
        md = "# Just text\n\nNo tables here.\n"
        result = mod.check_table_cell_count("en", {"f.md": md}, {"f.md": md})
        assert result.total == 0
        assert result.status == "PASS"

    def test_trailing_space_in_pipe(self, mod):
        """末尾スペース付きのテーブル行も正しくカウント"""
        src = "| A | B |  \n|---|---|\n| 1 | 2 |\n"
        trans = "| A | B |\n|---|---|\n| 1 | 2 |\n"
        result = mod.check_table_cell_count("en", {"f.md": src}, {"f.md": trans})
        assert result.status == "PASS"


# ===========================================================================
# TestInlineCodePreserved
# ===========================================================================


class TestInlineCodePreserved:
    def test_preserved_passes(self, mod):
        """コードが保持されている場合 PASS"""
        md = "Run `git clone` then `npm install`.\n"
        result = mod.check_inline_code_preserved("en", {"f.md": md}, {"f.md": md})
        assert result.status == "PASS"

    def test_missing_code_warns(self, mod):
        """コードが欠落している場合 WARN"""
        src = "Run `git clone` and `npm install`.\n"
        trans = "Run git clone and `npm install`.\n"
        result = mod.check_inline_code_preserved("en", {"f.md": src}, {"f.md": trans})
        assert result.status == "WARN"
        assert "git clone" in result.issues[0].message


# ===========================================================================
# TestImageRefsPreserved
# ===========================================================================


class TestImageRefsPreserved:
    def test_preserved_passes(self, mod):
        """画像パスが保持されている場合 PASS"""
        md = "![alt](images/test.png)\n"
        result = mod.check_image_refs_preserved("en", {"f.md": md}, {"f.md": md})
        assert result.status == "PASS"

    def test_missing_ref_fails(self, mod):
        """画像パスが変更されている場合 FAIL"""
        src = "![alt](images/test.png)\n"
        trans = "![alt](images/changed.png)\n"
        result = mod.check_image_refs_preserved("en", {"f.md": src}, {"f.md": trans})
        assert result.status == "FAIL"


# ===========================================================================
# TestAskqJsonValidity
# ===========================================================================


class TestAskqJsonValidity:
    def test_valid_json_passes(self, mod):
        """有効な JSON ブロックは PASS"""
        block = '```json\n{"title": "Test", "questions": []}\n```\n'
        result = mod.check_askq_json_validity("en", {"f.md": block}, {"f.md": block})
        assert result.status == "PASS"

    def test_invalid_json_fails(self, mod):
        """無効な JSON ブロックは FAIL"""
        src = '```json\n{"title": "Test", "questions": []}\n```\n'
        trans = '```json\n{"title": "Test", BROKEN}\n```\n'
        result = mod.check_askq_json_validity("en", {"f.md": src}, {"f.md": trans})
        assert result.status == "FAIL"

    def test_missing_keys_fails(self, mod):
        """キーが欠落した JSON は FAIL"""
        src = '```json\n{"title": "Test", "questions": [], "type": "quiz"}\n```\n'
        trans = '```json\n{"title": "Test"}\n```\n'
        result = mod.check_askq_json_validity("en", {"f.md": src}, {"f.md": trans})
        assert result.status == "FAIL"


# ===========================================================================
# TestRunChecks — 統合
# ===========================================================================


class TestRunChecks:
    def test_run_all_checks(self, mod, tmp_path):
        """全チェックが実行される"""
        src_dir = tmp_path / "src"
        trans_dir = tmp_path / "trans"
        _write_md(src_dir / "test.md", SOURCE_MD)
        _write_md(trans_dir / "test.md", VALID_MD)

        results = mod.run_checks(
            "en",
            source_dir=src_dir,
            translated_dir=trans_dir,
        )
        assert len(results) == len(mod.CHECK_REGISTRY)
        names = {r.name for r in results}
        assert names == set(mod.CHECK_REGISTRY.keys())

    def test_filter_checks(self, mod, tmp_path):
        """check_names でフィルタ可能"""
        src_dir = tmp_path / "src"
        trans_dir = tmp_path / "trans"
        _write_md(src_dir / "test.md", SOURCE_MD)
        _write_md(trans_dir / "test.md", VALID_MD)

        results = mod.run_checks(
            "en",
            check_names=["table_cell_count"],
            source_dir=src_dir,
            translated_dir=trans_dir,
        )
        assert len(results) == 1
        assert results[0].name == "table_cell_count"

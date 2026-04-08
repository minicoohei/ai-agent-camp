"""tests for tools/i18n_extract_cli.py — Phase 3: CLI gettext"""

import gettext as gettext_mod
import json
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import import_module_from_repo

_MOD_PATH = "tools/i18n_extract_cli.py"
_COMMON_PATH = "tools/i18n_common.py"


@pytest.fixture
def mod():
    import_module_from_repo("i18n_common", _COMMON_PATH)
    return import_module_from_repo("i18n_extract_cli", _MOD_PATH)


# ===========================================================================
# TestAstExtraction
# ===========================================================================

class TestAstExtraction:
    def test_extract_gettext_call(self, mod, tmp_path):
        """_("msg") を抽出"""
        src = tmp_path / "sample.py"
        src.write_text('from i18n_common import setup_gettext\n_ = setup_gettext()\nprint(_("テスト"))\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            entries = mod.extract_strings_from_file("sample.py")
        assert len(entries) == 1
        assert entries[0].msgid == "テスト"
        assert "sample.py:3" in entries[0].references[0]

    def test_extract_multiple_calls(self, mod, tmp_path):
        """同一ファイル内の複数 _()"""
        src = tmp_path / "multi.py"
        src.write_text('_ = lambda x: x\nprint(_("AAA"))\nprint(_("BBB"))\nprint(_("CCC"))\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            entries = mod.extract_strings_from_file("multi.py")
        assert len(entries) == 3
        msgids = {e.msgid for e in entries}
        assert msgids == {"AAA", "BBB", "CCC"}

    def test_skip_non_string_arg(self, mod, tmp_path):
        """_() の引数が変数の場合はスキップ"""
        src = tmp_path / "var.py"
        src.write_text('_ = lambda x: x\nmsg = "hello"\nprint(_(msg))\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            entries = mod.extract_strings_from_file("var.py")
        assert len(entries) == 0

    def test_extract_with_format(self, mod, tmp_path):
        """_("...{x}...") も抽出"""
        src = tmp_path / "fmt.py"
        src.write_text('_ = lambda x: x\nprint(_("保存: {key}").format(key="test"))\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            entries = mod.extract_strings_from_file("fmt.py")
        assert len(entries) == 1
        assert "{key}" in entries[0].msgid

    def test_skip_empty_string(self, mod, tmp_path):
        """_("") は除外"""
        src = tmp_path / "empty.py"
        src.write_text('_ = lambda x: x\nprint(_(""))\nprint(_("  "))\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            entries = mod.extract_strings_from_file("empty.py")
        assert len(entries) == 0

    def test_syntax_error_skipped(self, mod, tmp_path):
        """SyntaxError のファイルはスキップ"""
        src = tmp_path / "bad.py"
        src.write_text("def (broken syntax\n")
        with patch.object(mod, "ROOT_DIR", tmp_path):
            entries = mod.extract_strings_from_file("bad.py")
        assert entries == []


# ===========================================================================
# TestScanUnmarked
# ===========================================================================

class TestScanUnmarked:
    def test_detect_bare_print(self, mod, tmp_path):
        """print("日本語") を検出"""
        src = tmp_path / "bare.py"
        src.write_text('print("日本語メッセージ")\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.scan_unmarked_prints("bare.py")
        assert len(result) == 1
        assert "日本語メッセージ" in result[0]["text"]

    def test_ignore_print_with_gettext(self, mod, tmp_path):
        """print(_("...")) はスキップ"""
        src = tmp_path / "marked.py"
        src.write_text('_ = lambda x: x\nprint(_("翻訳済み"))\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.scan_unmarked_prints("marked.py")
        assert len(result) == 0

    def test_skip_stderr(self, mod, tmp_path):
        """print(..., file=sys.stderr) はスキップ"""
        src = tmp_path / "stderr.py"
        src.write_text('import sys\nprint("debug", file=sys.stderr)\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.scan_unmarked_prints("stderr.py")
        assert len(result) == 0

    def test_skip_decoration(self, mod, tmp_path):
        """print("-" * 60) はスキップ"""
        src = tmp_path / "deco.py"
        src.write_text('print("-" * 60)\nprint("=" * 40)\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.scan_unmarked_prints("deco.py")
        assert len(result) == 0

    def test_detect_fstring(self, mod, tmp_path):
        """f-string を含む print を検出"""
        src = tmp_path / "fstr.py"
        src.write_text('name = "test"\nprint(f"こんにちは {name}")\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.scan_unmarked_prints("fstr.py")
        assert len(result) == 1
        assert result[0]["is_fstring"] is True


# ===========================================================================
# TestPotGeneration
# ===========================================================================

class TestPotGeneration:
    def test_generate_pot_header(self, mod):
        """ヘッダに必要なフィールドが含まれる"""
        pot = mod.generate_pot([])
        assert "Project-Id-Version" in pot
        assert "Content-Type: text/plain; charset=UTF-8" in pot

    def test_generate_pot_entries(self, mod):
        """エントリが .pot 形式で出力される"""
        entries = [mod.PotEntry(msgid="テスト", references=["test.py:10"])]
        pot = mod.generate_pot(entries)
        assert '#: test.py:10' in pot
        assert 'msgid "テスト"' in pot or 'msgid "\\u' in pot  # Unicode or direct
        assert 'msgstr ""' in pot

    def test_deduplicate_msgid(self, mod, tmp_path):
        """extract_all で同一 msgid の参照が統合される"""
        # 2つのファイルに同じ _("同じ") を配置
        f1 = tmp_path / "a.py"
        f1.write_text('from i18n_common import setup_gettext\n_ = setup_gettext()\nprint(_("同じメッセージ"))\n')
        f2 = tmp_path / "b.py"
        f2.write_text('from i18n_common import setup_gettext\n_ = setup_gettext()\nprint(_("同じメッセージ"))\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.extract_all(["a.py", "b.py"])
        matching = [e for e in result if e.msgid == "同じメッセージ"]
        assert len(matching) == 1
        assert len(matching[0].references) == 2

    def test_escape_quotes_in_msgid(self, mod):
        """msgid 内の " がエスケープされる"""
        entries = [mod.PotEntry(msgid='He said "hello"', references=["t.py:1"])]
        pot = mod.generate_pot(entries)
        assert '\\"hello\\"' in pot


# ===========================================================================
# TestMoCompile
# ===========================================================================

class TestMoCompile:
    def test_compile_creates_file(self, mod, tmp_path):
        """.mo ファイルが生成される"""
        po_content = textwrap.dedent("""\
        msgid ""
        msgstr ""
        "Content-Type: text/plain; charset=UTF-8\\n"

        msgid "テスト"
        msgstr "Test"
        """)
        po_path = tmp_path / "en" / "LC_MESSAGES" / "aiagent.po"
        po_path.parent.mkdir(parents=True)
        po_path.write_text(po_content, encoding="utf-8")

        mo_path = po_path.with_suffix(".mo")
        result = mod.compile_mo(po_path, mo_path)
        assert result is True
        assert mo_path.exists()

    def test_gettext_roundtrip(self, mod, tmp_path):
        """.po → .mo → gettext.translation で読める"""
        po_content = textwrap.dedent("""\
        msgid ""
        msgstr ""
        "Content-Type: text/plain; charset=UTF-8\\n"
        "Language: en\\n"

        msgid "テスト"
        msgstr "Test"

        msgid "✅ 保存しました"
        msgstr "✅ Saved"
        """)
        po_path = tmp_path / "en" / "LC_MESSAGES" / "aiagent.po"
        po_path.parent.mkdir(parents=True)
        po_path.write_text(po_content, encoding="utf-8")

        mo_path = po_path.with_suffix(".mo")
        mod.compile_mo(po_path, mo_path)

        t = gettext_mod.translation("aiagent", localedir=str(tmp_path), languages=["en"])
        assert t.gettext("テスト") == "Test"
        assert t.gettext("✅ 保存しました") == "✅ Saved"

    def test_header_only_po_compiles(self, mod, tmp_path):
        """ヘッダのみの .po でもコンパイルは成功する（ヘッダは MO に必要）"""
        po_path = tmp_path / "header_only.po"
        po_path.write_text('msgid ""\nmsgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"\n', encoding="utf-8")
        mo_path = tmp_path / "header_only.mo"
        result = mod.compile_mo(po_path, mo_path)
        assert result is True
        assert mo_path.exists()


# ===========================================================================
# TestPoParser
# ===========================================================================

class TestPoParser:
    def test_parse_simple_po(self, mod, tmp_path):
        po_content = textwrap.dedent("""\
        msgid ""
        msgstr ""
        "Content-Type: text/plain; charset=UTF-8\\n"

        msgid "あいう"
        msgstr "abc"

        msgid "かきく"
        msgstr "def"
        """)
        po_path = tmp_path / "test.po"
        po_path.write_text(po_content, encoding="utf-8")
        entries = mod.parse_po_file(po_path)
        # ヘッダ + 2エントリ
        assert len(entries) == 3
        assert entries[0][0] == ""  # ヘッダ
        assert entries[1] == ("あいう", "abc")
        assert entries[2] == ("かきく", "def")

    def test_parse_empty_msgstr(self, mod, tmp_path):
        """msgstr が空の場合"""
        po_content = 'msgid ""\nmsgstr ""\n\nmsgid "テスト"\nmsgstr ""\n'
        po_path = tmp_path / "empty_str.po"
        po_path.write_text(po_content, encoding="utf-8")
        entries = mod.parse_po_file(po_path)
        # ヘッダ + 1エントリ
        assert len(entries) == 2
        assert entries[1] == ("テスト", "")


# ===========================================================================
# TestSetupGettextRuntime
# ===========================================================================

class TestSetupGettextRuntime:
    def test_fallback_returns_original(self, mod, tmp_path, monkeypatch):
        """.mo なし → 原文がそのまま返る"""
        common = import_module_from_repo("i18n_common", _COMMON_PATH)
        monkeypatch.setattr(common, "CLI_LOCALES_DIR", tmp_path / "nonexistent")
        monkeypatch.setenv("AIAGENT_LANG", "en")
        _ = common.setup_gettext()
        assert _("テスト") == "テスト"

    def test_with_mo_translates(self, mod, tmp_path, monkeypatch):
        """.mo ファイルがあれば翻訳される"""
        # テスト用 .po → .mo を作成
        po_content = textwrap.dedent("""\
        msgid ""
        msgstr ""
        "Content-Type: text/plain; charset=UTF-8\\n"

        msgid "テスト"
        msgstr "Test"
        """)
        po_path = tmp_path / "en" / "LC_MESSAGES" / "aiagent.po"
        po_path.parent.mkdir(parents=True)
        po_path.write_text(po_content, encoding="utf-8")
        mod.compile_mo(po_path, po_path.with_suffix(".mo"))

        common = import_module_from_repo("i18n_common", _COMMON_PATH)
        monkeypatch.setattr(common, "CLI_LOCALES_DIR", tmp_path)
        monkeypatch.setenv("AIAGENT_LANG", "en")
        _ = common.setup_gettext()
        assert _("テスト") == "Test"

    def test_aiagent_lang_env(self, mod, tmp_path, monkeypatch):
        """AIAGENT_LANG 環境変数で言語が切り替わる"""
        common = import_module_from_repo("i18n_common", _COMMON_PATH)
        monkeypatch.setattr(common, "CLI_LOCALES_DIR", tmp_path / "nonexistent")
        monkeypatch.setenv("AIAGENT_LANG", "ja")
        _ = common.setup_gettext()
        # ja の場合はフォールバックで原文
        assert _("何か") == "何か"


# ===========================================================================
# TestCheckMode
# ===========================================================================

class TestCheckMode:
    def test_pot_up_to_date(self, mod, tmp_path):
        """ソースと .pot が一致"""
        src = tmp_path / "test.py"
        src.write_text('_ = lambda x: x\nprint(_("メッセージ"))\n')

        with patch.object(mod, "ROOT_DIR", tmp_path):
            entries = mod.extract_all(["test.py"])
            pot_text = mod.generate_pot(entries)

        pot_path = tmp_path / "test.pot"
        pot_path.write_text(pot_text, encoding="utf-8")

        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.check_pot_freshness(pot_path, ["test.py"])
        assert result is True

    def test_pot_outdated(self, mod, tmp_path):
        """ソース変更後に差分検出"""
        # 古い .pot
        pot_text = mod.generate_pot([mod.PotEntry(msgid="古いメッセージ", references=["t.py:1"])])
        pot_path = tmp_path / "test.pot"
        pot_path.write_text(pot_text, encoding="utf-8")

        # 新しいソース
        src = tmp_path / "test.py"
        src.write_text('_ = lambda x: x\nprint(_("新しいメッセージ"))\n')

        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.check_pot_freshness(pot_path, ["test.py"])
        assert result is False


# ===========================================================================
# TestGeneratePo
# ===========================================================================

class TestGeneratePo:
    def test_translations_inserted(self, mod):
        """翻訳が msgstr に埋め込まれる"""
        entries = [mod.PotEntry(msgid="テスト", references=["t.py:1"])]
        pot_text = mod.generate_pot(entries)
        translations = {"テスト": "Test"}
        po_text = mod.generate_po(pot_text, translations, "en")
        assert 'msgstr "Test"' in po_text

    def test_language_header_set(self, mod):
        """Language ヘッダが設定される"""
        pot_text = mod.generate_pot([])
        po_text = mod.generate_po(pot_text, {}, "es")
        assert '"Language: es\\n"' in po_text

    def test_missing_translation_empty_msgstr(self, mod):
        """翻訳がない場合は msgstr が空"""
        entries = [mod.PotEntry(msgid="未翻訳", references=["t.py:1"])]
        pot_text = mod.generate_pot(entries)
        po_text = mod.generate_po(pot_text, {}, "en")
        # msgid "未翻訳" の後に msgstr "" がある
        lines = po_text.split("\n")
        for i, line in enumerate(lines):
            if 'msgid' in line and '未翻訳' in line:
                assert lines[i + 1] == 'msgstr ""'
                break


# ===========================================================================
# TestTranslation (API モック)
# ===========================================================================

class TestTranslation:
    def test_translate_mock(self, mod):
        """Gemini API モックで翻訳が返る"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({"テスト": "Test", "保存": "Save"})
        mock_client.models.generate_content.return_value = mock_response

        entries = [
            mod.PotEntry(msgid="テスト", references=["t.py:1"]),
            mod.PotEntry(msgid="保存", references=["t.py:2"]),
        ]
        result = mod.translate_pot_entries(mock_client, entries, "en")
        assert result["テスト"] == "Test"
        assert result["保存"] == "Save"

    def test_preserves_format_placeholders(self, mod):
        """翻訳後も {key} が保持される"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({"保存: {key}": "Saved: {key}"})
        mock_client.models.generate_content.return_value = mock_response

        entries = [mod.PotEntry(msgid="保存: {key}", references=["t.py:1"])]
        result = mod.translate_pot_entries(mock_client, entries, "en")
        assert "{key}" in result["保存: {key}"]

"""tests for tools/i18n_qa.py — Phase 5: Unified QA runner"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import import_module_from_repo

_MOD_PATH = "tools/i18n_qa.py"
_COMMON_PATH = "tools/i18n_common.py"
_CHECK_PATH = "tools/i18n_check.py"
_CHECK_MD_PATH = "tools/i18n_check_md.py"


@pytest.fixture
def mod():
    import_module_from_repo("i18n_common", _COMMON_PATH)
    import_module_from_repo("i18n_check", _CHECK_PATH)
    import_module_from_repo("i18n_check_md", _CHECK_MD_PATH)
    return import_module_from_repo("i18n_qa", _MOD_PATH)


# ===========================================================================
# DomainResult
# ===========================================================================


class TestDomainResult:
    def test_to_dict_pass(self, mod):
        r = mod.DomainResult(domain="cli", passed=True, checks=[])
        d = r.to_dict()
        assert d["domain"] == "cli"
        assert d["passed"] is True
        assert "error" not in d

    def test_to_dict_with_error(self, mod):
        r = mod.DomainResult(domain="html", passed=False, error="broken")
        d = r.to_dict()
        assert d["passed"] is False
        assert d["error"] == "broken"


# ===========================================================================
# run_all — ドメインフィルタ
# ===========================================================================


class TestRunAll:
    def test_cli_only(self, mod):
        """domain=cli のみ実行"""
        with patch.object(mod, "run_cli_qa", return_value=mod.DomainResult(domain="cli")) as mock_cli:
            results = mod.run_all(["en"], domains=["cli"])
        assert len(results) == 1
        assert results[0].domain == "cli"
        mock_cli.assert_called_once()

    def test_md_only(self, mod):
        """domain=md のみ実行"""
        with patch.object(mod, "run_md_qa", return_value=mod.DomainResult(domain="md:en")) as mock_md:
            results = mod.run_all(["en"], domains=["md"])
        assert len(results) == 1
        mock_md.assert_called_once_with("en")

    def test_multiple_langs(self, mod):
        """複数言語で md 実行"""
        with patch.object(mod, "run_md_qa", return_value=mod.DomainResult(domain="md")) as mock_md:
            results = mod.run_all(["en", "es"], domains=["md"])
        assert len(results) == 2
        assert mock_md.call_count == 2

    def test_all_domains(self, mod):
        """domain 未指定で全ドメイン実行"""
        with (
            patch.object(mod, "run_html_qa", return_value=mod.DomainResult(domain="html")),
            patch.object(mod, "run_md_qa", return_value=mod.DomainResult(domain="md")),
            patch.object(mod, "run_cli_qa", return_value=mod.DomainResult(domain="cli")),
        ):
            results = mod.run_all(["en"])
        # html:en + md:en + cli = 3
        assert len(results) == 3


# ===========================================================================
# Exit code
# ===========================================================================


class TestExitCode:
    def test_all_pass_returns_zero(self, mod):
        """全ドメイン PASS → exit 0"""
        with (
            patch.object(mod, "run_cli_qa", return_value=mod.DomainResult(domain="cli", passed=True)),
        ):
            results = mod.run_all(["en"], domains=["cli"])
        assert all(r.passed for r in results)

    def test_any_fail_detected(self, mod):
        """1ドメイン FAIL → exit 1 相当"""
        with (
            patch.object(mod, "run_cli_qa", return_value=mod.DomainResult(domain="cli", passed=False)),
        ):
            results = mod.run_all(["en"], domains=["cli"])
        assert any(not r.passed for r in results)


# ===========================================================================
# run_cli_qa — 実際の動作
# ===========================================================================


class TestRunCliQa:
    def test_returns_domain_result(self, mod):
        """run_cli_qa は DomainResult を返す"""
        mock_check = MagicMock(return_value=True)
        mock_scan = MagicMock(return_value=[])
        with (
            patch.dict("sys.modules", {}),
            patch.object(mod, "run_cli_qa", wraps=mod.run_cli_qa),
        ):
            result = mod.run_cli_qa()
        assert isinstance(result, mod.DomainResult)
        assert result.domain == "cli"
        assert result.error is None
        assert len(result.checks) >= 1

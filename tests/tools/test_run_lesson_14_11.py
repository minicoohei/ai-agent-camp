"""Tests for tools/run_lesson_14_11.py - Notion lesson runner."""

from __future__ import annotations

import csv
import json
import sys
import types
from collections import Counter
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Stub the requests module so we can import without it installed
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _stub_requests(monkeypatch):
    stub = types.ModuleType("requests")
    stub.request = MagicMock()
    monkeypatch.setitem(sys.modules, "requests", stub)


@pytest.fixture
def mod(tmp_path):
    """Import the target module fresh each test, redirecting file paths to tmp."""
    from tests.conftest import import_module_from_repo
    m = import_module_from_repo("run_lesson_14_11", "tools/run_lesson_14_11.py")

    # Redirect all file paths to tmp_path
    pm_dir = tmp_path / "output" / "pm"
    pm_dir.mkdir(parents=True)
    results_dir = tmp_path / "output" / "test-results"
    results_dir.mkdir(parents=True)

    m.REPO_ROOT = tmp_path
    m.REQ_SPEC_PATH = tmp_path / "output" / "pm" / "requirements-spec.md"
    m.EXPORT_MD_PATH = pm_dir / "notion-export.md"
    m.EXPORT_CSV_PATH = pm_dir / "notion-export.csv"
    m.TRACKER_MD_PATH = pm_dir / "requirement-tracker.md"
    m.REPORT_PATH = results_dir / "start-14-11-report.json"
    return m


# ---------------------------------------------------------------------------
# Sample requirement spec content
# ---------------------------------------------------------------------------

SAMPLE_SPEC = """\
# Requirements

#### REQ-F-001: ユーザー認証
| 優先度 | P0（最重要） |
| 説明 | ログイン機能を提供する |
| 対象画面 | Login Screen |

#### REQ-F-002: ダッシュボード
| 優先度 | P1 |
| 要件 | データ可視化 |

#### REQ-NFR-P-001: パフォーマンス要件
| 優先度 | High |
| 説明 | 応答2秒以内 |

#### REQ-NFR-SC-001: スケーラビリティ
| 優先度 | Medium |
| 説明 | 水平スケーリング対応 |
"""


# ============================================================
# Helper functions
# ============================================================

class TestNowJst:
    def test_returns_datetime(self, mod):
        result = mod.now_jst()
        assert result is not None
        assert hasattr(result, "isoformat")


class TestEnvPresent:
    def test_present(self, mod, monkeypatch):
        monkeypatch.setenv("TEST_VAR_99", "value")
        assert mod.env_present("TEST_VAR_99") is True

    def test_absent(self, mod, monkeypatch):
        monkeypatch.delenv("TEST_VAR_99", raising=False)
        assert mod.env_present("TEST_VAR_99") is False

    def test_empty_string(self, mod, monkeypatch):
        monkeypatch.setenv("TEST_VAR_99", "")
        assert mod.env_present("TEST_VAR_99") is False


class TestNotionHeaders:
    def test_with_key(self, mod):
        h = mod.notion_headers("secret-key")
        assert h["Authorization"] == "Bearer secret-key"
        assert h["Notion-Version"] == "2022-06-28"

    def test_with_none(self, mod):
        h = mod.notion_headers(None)
        assert h["Authorization"] == "Bearer "


class TestSplitMarkdownRow:
    def test_normal(self, mod):
        assert mod.split_markdown_row("| a | b | c |") == ["a", "b", "c"]

    def test_empty_input(self, mod):
        assert mod.split_markdown_row("") == [""]

    def test_no_pipes(self, mod):
        assert mod.split_markdown_row("hello") == ["hello"]

    def test_unicode(self, mod):
        result = mod.split_markdown_row("| 日本語 | テスト |")
        assert result == ["日本語", "テスト"]


# ============================================================
# map_priority
# ============================================================

class TestMapPriority:
    def test_req_f_p0(self, mod):
        assert mod.map_priority("REQ-F-001", "P0") == "Must"

    def test_req_f_p1(self, mod):
        assert mod.map_priority("REQ-F-002", "P1") == "Should"

    def test_req_f_p2(self, mod):
        assert mod.map_priority("REQ-F-003", "P2") == "Could"

    def test_req_f_unknown_priority(self, mod):
        assert mod.map_priority("REQ-F-004", "X") == "Should"

    def test_req_f_phase2_release(self, mod):
        assert mod.map_priority("REQ-F-001", "P0", "Phase 2") == "Could"

    def test_nfr_must_list(self, mod):
        assert mod.map_priority("REQ-NFR-P-001", "") == "Must"
        assert mod.map_priority("REQ-NFR-S-001", "") == "Must"

    def test_nfr_sc_is_could(self, mod):
        assert mod.map_priority("REQ-NFR-SC-001", "") == "Could"

    def test_nfr_default_should(self, mod):
        assert mod.map_priority("REQ-NFR-X-999", "") == "Should"


# ============================================================
# parse_requirements
# ============================================================

class TestParseRequirements:
    def test_happy_path(self, mod, tmp_path):
        spec_file = tmp_path / "spec.md"
        spec_file.write_text(SAMPLE_SPEC, encoding="utf-8")
        rows = mod.parse_requirements(spec_file)
        assert len(rows) == 4
        assert rows[0]["requirement_id"] == "REQ-F-001"
        assert rows[0]["category"] == "機能"
        assert rows[0]["priority"] == "Must"
        assert rows[0]["screen"] == "Login Screen"

    def test_nfr_category(self, mod, tmp_path):
        spec_file = tmp_path / "spec.md"
        spec_file.write_text(SAMPLE_SPEC, encoding="utf-8")
        rows = mod.parse_requirements(spec_file)
        nfr = [r for r in rows if r["requirement_id"].startswith("REQ-NFR")]
        assert all(r["category"] == "非機能" for r in nfr)

    def test_empty_file_raises(self, mod, tmp_path):
        empty = tmp_path / "empty.md"
        empty.write_text("# No requirements\n", encoding="utf-8")
        with pytest.raises(ValueError, match="No requirement rows"):
            mod.parse_requirements(empty)

    def test_unicode_content(self, mod, tmp_path):
        content = "#### REQ-F-001: \u3042\u3044\u3046\u3048\u304a\n| \u8aac\u660e | \u30c6\u30b9\u30c8\u8aac\u660e |\n"
        spec_file = tmp_path / "unicode.md"
        spec_file.write_text(content, encoding="utf-8")
        rows = mod.parse_requirements(spec_file)
        assert len(rows) == 1
        assert rows[0]["notes"] == "テスト説明"


# ============================================================
# stats_for / pct
# ============================================================

class TestStatsFor:
    def test_basic(self, mod):
        rows = [
            {"status": "未着手", "priority": "Must", "category": "機能"},
            {"status": "未着手", "priority": "Should", "category": "非機能"},
        ]
        result = mod.stats_for(rows)
        assert result["status"]["未着手"] == 2
        assert result["priority"]["Must"] == 1


class TestPct:
    def test_normal(self, mod):
        assert mod.pct(1, 4) == "25.0%"

    def test_zero_total(self, mod):
        assert mod.pct(0, 0) == "0.0%"

    def test_full(self, mod):
        assert mod.pct(10, 10) == "100.0%"


# ============================================================
# write_markdown_export / write_csv_export / write_tracker
# ============================================================

class TestWriteMarkdownExport:
    def test_creates_file(self, mod, tmp_path):
        rows = [
            {"requirement_id": "REQ-F-001", "requirement_name": "Test",
             "category": "機能", "status": "未着手", "priority": "Must"},
        ]
        path = tmp_path / "export.md"
        mod.write_markdown_export(rows, path, "db123", "local", None, "note")
        text = path.read_text(encoding="utf-8")
        assert "REQ-F-001" in text
        assert "db123" in text


class TestWriteCsvExport:
    def test_creates_valid_csv(self, mod, tmp_path):
        rows = [
            {"requirement_id": "REQ-F-001", "requirement_name": "Auth",
             "category": "機能", "status": "未着手", "priority": "Must"},
        ]
        path = tmp_path / "export.csv"
        mod.write_csv_export(rows, path)
        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = list(reader)
        assert len(data) == 1
        assert data[0]["requirement_id"] == "REQ-F-001"


class TestWriteTracker:
    def test_creates_tracker(self, mod, tmp_path):
        rows = [
            {"requirement_id": "REQ-F-001", "requirement_name": "Auth",
             "category": "機能", "status": "未着手", "priority": "Must"},
        ]
        path = tmp_path / "tracker.md"
        mod.write_tracker(rows, path)
        text = path.read_text(encoding="utf-8")
        assert "REQ-F-001" in text
        assert "Requirement Tracker" in text


# ============================================================
# dns_probe
# ============================================================

class TestDnsProbe:
    def test_success(self, mod):
        with patch.object(mod.socket, "gethostbyname", return_value="1.2.3.4"):
            ok, detail = mod.dns_probe("example.com")
        assert ok is True
        assert detail == "1.2.3.4"

    def test_failure(self, mod):
        with patch.object(mod.socket, "gethostbyname", side_effect=OSError("fail")):
            ok, detail = mod.dns_probe("bad.host")
        assert ok is False
        assert "fail" in detail


# ============================================================
# notion_request
# ============================================================

class TestNotionRequest:
    def test_requests_none(self, mod, monkeypatch):
        monkeypatch.setattr(mod, "requests", None)
        ok, result = mod.notion_request("GET", "test", None)
        assert ok is False
        assert "not installed" in result

    def test_success(self, mod):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"id": "123"}
        mod.requests.request = MagicMock(return_value=mock_resp)
        ok, result = mod.notion_request("POST", "search", "key", {"q": "test"})
        assert ok is True
        assert result["status_code"] == 200

    def test_json_parse_error(self, mod):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.status_code = 200
        mock_resp.json.side_effect = ValueError("bad json")
        mock_resp.text = "not json"
        mod.requests.request = MagicMock(return_value=mock_resp)
        ok, result = mod.notion_request("GET", "ep", "key")
        assert ok is True
        assert result["body"]["text"] == "not json"

    def test_http_error(self, mod):
        mock_resp = MagicMock()
        mock_resp.ok = False
        mock_resp.status_code = 401
        mock_resp.json.return_value = {"message": "unauthorized"}
        mod.requests.request = MagicMock(return_value=mock_resp)
        ok, result = mod.notion_request("GET", "ep", "bad-key")
        assert ok is False
        assert result["status_code"] == 401


# ============================================================
# step1_verify_connection
# ============================================================

class TestStep1VerifyConnection:
    def test_all_present(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        monkeypatch.setenv("NOTION_DATABASE_ID", "db")
        monkeypatch.setenv("NOTION_PARENT_PAGE_ID", "page")
        with (
            patch.object(mod, "dns_probe", return_value=(True, "1.2.3.4")),
            patch.object(mod, "notion_request", return_value=(True, {"status_code": 200})),
        ):
            result = mod.step1_verify_connection()
        assert result.status == "success"

    def test_missing_key(self, mod, monkeypatch):
        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        monkeypatch.delenv("NOTION_DATABASE_ID", raising=False)
        monkeypatch.delenv("NOTION_PARENT_PAGE_ID", raising=False)
        with (
            patch.object(mod, "dns_probe", return_value=(False, "err")),
            patch.object(mod, "notion_request", return_value=(False, "err")),
        ):
            result = mod.step1_verify_connection()
        assert result.status == "failed"


# ============================================================
# step2_create_database
# ============================================================

class TestStep2CreateDatabase:
    def test_missing_api_key(self, mod, monkeypatch):
        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        monkeypatch.setenv("NOTION_PARENT_PAGE_ID", "page")
        result, db_id, db_url = mod.step2_create_database()
        assert result.status == "failed"
        assert db_id is None

    def test_missing_parent_page(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        monkeypatch.delenv("NOTION_PARENT_PAGE_ID", raising=False)
        result, db_id, db_url = mod.step2_create_database()
        assert result.status == "failed"

    def test_api_failure(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        monkeypatch.setenv("NOTION_PARENT_PAGE_ID", "page")
        with patch.object(mod, "notion_request", return_value=(False, "error")):
            result, db_id, db_url = mod.step2_create_database()
        assert result.status == "failed"
        assert db_id is None

    def test_success(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        monkeypatch.setenv("NOTION_PARENT_PAGE_ID", "page")
        response = {"status_code": 200, "body": {"id": "db-123", "url": "https://notion.so/db"}}
        with patch.object(mod, "notion_request", return_value=(True, response)):
            result, db_id, db_url = mod.step2_create_database()
        assert result.status == "success"
        assert db_id == "db-123"
        assert db_url == "https://notion.so/db"


# ============================================================
# notion_page_properties
# ============================================================

class TestNotionPageProperties:
    def test_creates_properties(self, mod):
        row = {
            "requirement_id": "REQ-F-001",
            "requirement_name": "Auth",
            "category": "機能",
            "status": "未着手",
            "priority": "Must",
        }
        props = mod.notion_page_properties(row)
        assert "要件名" in props
        assert props["要件ID"]["rich_text"][0]["text"]["content"] == "REQ-F-001"


# ============================================================
# step3_import_requirements
# ============================================================

class TestStep3ImportRequirements:
    def test_no_api_key(self, mod, monkeypatch):
        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        rows = [{"requirement_id": "R1"}]
        result = mod.step3_import_requirements(rows, "db-id")
        assert result.status == "partial"
        assert result.metrics["imported_to_notion"] == 0

    def test_no_database_id(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        result = mod.step3_import_requirements([{"x": "y"}], None)
        assert result.status == "partial"

    def test_all_success(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        rows = [
            {"requirement_id": "R1", "requirement_name": "A", "category": "機能",
             "status": "未着手", "priority": "Must"},
        ]
        response = {"status_code": 200, "body": {"id": "page-1"}}
        with patch.object(mod, "notion_request", return_value=(True, response)):
            result = mod.step3_import_requirements(rows, "db-id")
        assert result.status == "success"
        assert result.metrics["imported_to_notion"] == 1

    def test_partial_failure(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        rows = [
            {"requirement_id": "R1", "requirement_name": "A", "category": "機能",
             "status": "未着手", "priority": "Must"},
            {"requirement_id": "R2", "requirement_name": "B", "category": "機能",
             "status": "未着手", "priority": "Should"},
        ]
        with patch.object(mod, "notion_request", side_effect=[
            (True, {"status_code": 200, "body": {"id": "p1"}}),
            (False, "error"),
        ]):
            result = mod.step3_import_requirements(rows, "db-id")
        assert result.status == "partial"


# ============================================================
# parse_notion_page
# ============================================================

class TestParseNotionPage:
    def test_full_page(self, mod):
        page = {
            "properties": {
                "要件名": {"title": [{"plain_text": "Auth"}]},
                "要件ID": {"rich_text": [{"plain_text": "REQ-F-001"}]},
                "カテゴリ": {"select": {"name": "機能"}},
                "ステータス": {"select": {"name": "未着手"}},
                "優先度": {"select": {"name": "Must"}},
            }
        }
        result = mod.parse_notion_page(page)
        assert result["requirement_id"] == "REQ-F-001"
        assert result["requirement_name"] == "Auth"

    def test_empty_page(self, mod):
        result = mod.parse_notion_page({"properties": {}})
        assert result["requirement_id"] == ""
        assert result["requirement_name"] == ""

    def test_none_selects(self, mod):
        page = {
            "properties": {
                "要件名": {"title": []},
                "要件ID": {"rich_text": []},
                "カテゴリ": {"select": None},
                "ステータス": {"select": None},
                "優先度": {"select": None},
            }
        }
        result = mod.parse_notion_page(page)
        assert result["category"] == ""


# ============================================================
# step4_export
# ============================================================

class TestStep4Export:
    def test_no_api_key(self, mod, monkeypatch):
        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        rows = [
            {"requirement_id": "R1", "requirement_name": "A", "category": "機能",
             "status": "未着手", "priority": "Must"},
        ]
        result = mod.step4_export(rows, None, None)
        assert result.status == "partial"
        assert mod.EXPORT_MD_PATH.exists()
        assert mod.EXPORT_CSV_PATH.exists()

    def test_notion_success(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        rows = [
            {"requirement_id": "R1", "requirement_name": "A", "category": "機能",
             "status": "未着手", "priority": "Must"},
        ]
        notion_page = {
            "properties": {
                "要件名": {"title": [{"plain_text": "A"}]},
                "要件ID": {"rich_text": [{"plain_text": "R1"}]},
                "カテゴリ": {"select": {"name": "機能"}},
                "ステータス": {"select": {"name": "未着手"}},
                "優先度": {"select": {"name": "Must"}},
            }
        }
        response = {"status_code": 200, "body": {"results": [notion_page]}}
        with patch.object(mod, "notion_request", return_value=(True, response)):
            result = mod.step4_export(rows, "db-id", "https://notion.so/db")
        assert result.status == "success"
        assert result.metrics["source"] == "notion"

    def test_notion_query_failure(self, mod, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "key")
        rows = [
            {"requirement_id": "R1", "requirement_name": "A", "category": "機能",
             "status": "未着手", "priority": "Must"},
        ]
        with patch.object(mod, "notion_request", return_value=(False, "error")):
            result = mod.step4_export(rows, "db-id", None)
        assert result.status == "partial"


# ============================================================
# main()
# ============================================================

class TestMain:
    def test_missing_spec_file(self, mod, tmp_path, capsys):
        # REQ_SPEC_PATH does not exist
        result = mod.main()
        assert result == 1
        assert mod.REPORT_PATH.exists()

    def test_parse_failure(self, mod, tmp_path, capsys):
        mod.REQ_SPEC_PATH.write_text("# empty spec\n", encoding="utf-8")
        result = mod.main()
        assert result == 1

    def test_full_run_no_notion(self, mod, tmp_path, monkeypatch, capsys):
        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        monkeypatch.delenv("NOTION_DATABASE_ID", raising=False)
        monkeypatch.delenv("NOTION_PARENT_PAGE_ID", raising=False)
        mod.REQ_SPEC_PATH.write_text(SAMPLE_SPEC, encoding="utf-8")
        with (
            patch.object(mod, "dns_probe", return_value=(False, "err")),
            patch.object(mod, "notion_request", return_value=(False, "err")),
        ):
            result = mod.main()
        assert result == 0
        assert mod.REPORT_PATH.exists()
        report = json.loads(mod.REPORT_PATH.read_text())
        assert len(report["errors"]) > 0

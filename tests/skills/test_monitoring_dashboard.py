"""monitoring-dashboard/scripts/main.py の単体テスト"""
import json
import pytest
from pathlib import Path

from tests.conftest import import_module_from_repo


def _import_dashboard_main():
    return import_module_from_repo(
        "monitoring_dashboard_main",
        "skills/monitoring-dashboard/scripts/main.py",
    )


class TestImport:
    def test_import_module(self):
        mod = _import_dashboard_main()
        assert callable(mod.generate_progress_notebook)
        assert callable(mod.generate_test_notebook)
        assert callable(mod.generate_traceability_notebook)
        assert callable(mod.generate_integrated_notebook)
        assert mod.DASHBOARD_TYPES
        assert mod.GENERATORS

    def test_dashboard_types(self):
        DASHBOARD_TYPES = _import_dashboard_main().DASHBOARD_TYPES
        assert "progress" in DASHBOARD_TYPES
        assert "test" in DASHBOARD_TYPES
        assert "traceability" in DASHBOARD_TYPES
        assert "integrated" in DASHBOARD_TYPES
        assert len(DASHBOARD_TYPES) == 4

    def test_generators_mapping(self):
        mod = _import_dashboard_main()
        GENERATORS = mod.GENERATORS
        DASHBOARD_TYPES = mod.DASHBOARD_TYPES
        for dt in DASHBOARD_TYPES:
            assert dt in GENERATORS
            assert callable(GENERATORS[dt])


class TestGenerateProgressNotebook:
    def test_returns_string(self):
        generate_progress_notebook = _import_dashboard_main().generate_progress_notebook
        result = generate_progress_notebook("/tmp/data.json", "Test Dashboard")
        assert isinstance(result, str)

    def test_contains_marimo_import(self):
        generate_progress_notebook = _import_dashboard_main().generate_progress_notebook
        result = generate_progress_notebook("/tmp/data.json", "Progress")
        assert "import marimo" in result

    def test_contains_title(self):
        generate_progress_notebook = _import_dashboard_main().generate_progress_notebook
        result = generate_progress_notebook("/tmp/data.json", "My Title")
        assert "My Title" in result

    def test_contains_data_path(self):
        generate_progress_notebook = _import_dashboard_main().generate_progress_notebook
        result = generate_progress_notebook("/tmp/test-data.json", "Title")
        assert "/tmp/test-data.json" in result

    def test_contains_plotly(self):
        generate_progress_notebook = _import_dashboard_main().generate_progress_notebook
        result = generate_progress_notebook("/tmp/data.json", "Title")
        assert "plotly" in result

    def test_zero_division_guard(self):
        generate_progress_notebook = _import_dashboard_main().generate_progress_notebook
        result = generate_progress_notebook("/tmp/data.json", "Title")
        assert "total > 0" in result


class TestGenerateTestNotebook:
    def test_returns_string(self):
        generate_test_notebook = _import_dashboard_main().generate_test_notebook
        result = generate_test_notebook("/tmp/data.json", "Test Results")
        assert isinstance(result, str)

    def test_contains_test_metrics(self):
        generate_test_notebook = _import_dashboard_main().generate_test_notebook
        result = generate_test_notebook("/tmp/data.json", "Test")
        assert "passed" in result.lower()
        assert "failed" in result.lower()

    def test_contains_pie_chart(self):
        generate_test_notebook = _import_dashboard_main().generate_test_notebook
        result = generate_test_notebook("/tmp/data.json", "Test")
        assert "px.pie" in result

    def test_zero_division_guard(self):
        generate_test_notebook = _import_dashboard_main().generate_test_notebook
        result = generate_test_notebook("/tmp/data.json", "Title")
        assert "total > 0" in result


class TestGenerateTraceabilityNotebook:
    def test_returns_string(self):
        generate_traceability_notebook = _import_dashboard_main().generate_traceability_notebook
        result = generate_traceability_notebook("/tmp/data.json", "Traceability")
        assert isinstance(result, str)

    def test_contains_requirements_status(self):
        generate_traceability_notebook = _import_dashboard_main().generate_traceability_notebook
        result = generate_traceability_notebook("/tmp/data.json", "Trace")
        assert "status" in result
        assert "requirements" in result.lower()


class TestGenerateIntegratedNotebook:
    def test_returns_string(self):
        generate_integrated_notebook = _import_dashboard_main().generate_integrated_notebook
        result = generate_integrated_notebook("/tmp/data.json", "Integrated")
        assert isinstance(result, str)

    def test_contains_all_sections(self):
        generate_integrated_notebook = _import_dashboard_main().generate_integrated_notebook
        result = generate_integrated_notebook("/tmp/data.json", "Dashboard")
        assert "tasks" in result.lower()
        assert "tests" in result.lower()

    def test_contains_summary(self):
        generate_integrated_notebook = _import_dashboard_main().generate_integrated_notebook
        result = generate_integrated_notebook("/tmp/data.json", "Dashboard")
        assert "Summary" in result


class TestMainFunction:
    def test_main_exists(self):
        main = _import_dashboard_main().main
        assert callable(main)

    def test_default_output_path(self):
        DEFAULT_OUTPUT = _import_dashboard_main().DEFAULT_OUTPUT
        assert isinstance(DEFAULT_OUTPUT, Path)
        assert "output" in str(DEFAULT_OUTPUT)
        assert "dashboard.py" in str(DEFAULT_OUTPUT)

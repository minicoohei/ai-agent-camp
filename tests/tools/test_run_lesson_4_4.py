"""Tests for tools/run_lesson_4_4.py - lesson runner for data visualization."""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import pytest

# ---------------------------------------------------------------------------
# Helpers: stub heavy third-party modules before importing the target module
# ---------------------------------------------------------------------------

_STUBS: dict[str, types.ModuleType] = {}


def _ensure_stub(name: str) -> types.ModuleType:
    if name not in _STUBS:
        mod = types.ModuleType(name)
        _STUBS[name] = mod
    return _STUBS[name]


def _prepare_stubs():
    """Create lightweight stubs for numpy, pandas, matplotlib, seaborn, bigquery."""
    # numpy
    np = _ensure_stub("numpy")
    rng_mock = MagicMock()
    rng_mock.zipf.return_value = [1, 2, 3, 4, 5]
    np.random = MagicMock()
    np.random.default_rng = MagicMock(return_value=rng_mock)
    np.clip = MagicMock(side_effect=lambda x, a, b: x)

    # pandas
    from datetime import datetime as _dt
    pd = _ensure_stub("pandas")
    pd.DataFrame = MagicMock(side_effect=_make_dataframe)
    pd.date_range = MagicMock(return_value=[_dt(2021, 1, 1), _dt(2021, 1, 2)])
    pd.to_datetime = MagicMock(side_effect=lambda x: x)

    # matplotlib
    mpl = _ensure_stub("matplotlib")
    mpl.use = MagicMock()
    plt = _ensure_stub("matplotlib.pyplot")
    fig_mock = MagicMock()
    ax_mock = MagicMock()
    ax_mock.spines = {"top": MagicMock(), "right": MagicMock()}
    plt.subplots = MagicMock(return_value=(fig_mock, ax_mock))
    plt.tight_layout = MagicMock()
    plt.close = MagicMock()
    plt.rcParams = {}

    # seaborn
    sns = _ensure_stub("seaborn")
    sns.set_theme = MagicMock()
    sns.color_palette = MagicMock(return_value=["#000"] * 10)

    # google.cloud.bigquery
    gc = _ensure_stub("google")
    gc.cloud = _ensure_stub("google.cloud")
    bq = _ensure_stub("google.cloud.bigquery")
    bq.Client = MagicMock


def _make_dataframe(*args, **kwargs):
    """Return a lightweight mock DataFrame."""
    df = MagicMock()
    df.empty = False
    df.sort_values = MagicMock(return_value=df)
    df.iterrows = MagicMock(return_value=iter([]))
    df.__len__ = MagicMock(return_value=3)
    return df


@pytest.fixture(autouse=True)
def _stub_modules(monkeypatch, tmp_path):
    """Inject stubs and force the module to use tmp_path for output."""
    _prepare_stubs()
    for name, mod in _STUBS.items():
        monkeypatch.setitem(sys.modules, name, mod)

    # Also ensure tempfile.gettempdir returns tmp_path so module-level code works
    monkeypatch.setattr("tempfile.gettempdir", lambda: str(tmp_path))


@pytest.fixture
def mod(tmp_path):
    """Import the target module fresh."""
    from tests.conftest import import_module_from_repo
    m = import_module_from_repo("run_lesson_4_4", "tools/run_lesson_4_4.py")
    # Override OUTPUT_DIR and REPORT_PATH to tmp
    m.OUTPUT_DIR = tmp_path / "output"
    m.REPORT_PATH = m.OUTPUT_DIR / "lesson-4-4-run-report.json"
    return m


# ============================================================
# StepResult dataclass
# ============================================================

class TestStepResult:
    def test_create_basic(self, mod):
        sr = mod.StepResult(step="a", status="success")
        assert sr.step == "a"
        assert sr.status == "success"
        assert sr.output is None
        assert sr.source is None

    def test_create_with_all_fields(self, mod):
        sr = mod.StepResult(step="b", status="failed", output="/x", source="bq", details="err")
        assert sr.output == "/x"
        assert sr.details == "err"


# ============================================================
# prepare_matplotlib
# ============================================================

class TestPrepareMatplotlib:
    def test_runs_without_error(self, mod):
        mod.prepare_matplotlib()  # should not raise


# ============================================================
# maybe_build_bigquery_client
# ============================================================

class TestMaybeBuildBigqueryClient:
    def test_success(self, mod, monkeypatch):
        mock_client = MagicMock()
        bq_mod = sys.modules["google.cloud.bigquery"]
        monkeypatch.setattr(bq_mod, "Client", MagicMock(return_value=mock_client))
        monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
        client, err = mod.maybe_build_bigquery_client()
        assert client is mock_client
        assert err is None

    def test_credential_path_not_found(self, mod, monkeypatch, tmp_path):
        monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(tmp_path / "nope.json"))
        mock_client = MagicMock()
        bq_mod = sys.modules["google.cloud.bigquery"]
        monkeypatch.setattr(bq_mod, "Client", MagicMock(return_value=mock_client))
        client, err = mod.maybe_build_bigquery_client()
        assert client is mock_client

    def test_exception(self, mod, monkeypatch):
        monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
        bq_mod = sys.modules["google.cloud.bigquery"]
        monkeypatch.setattr(bq_mod, "Client", MagicMock(side_effect=RuntimeError("no project")))
        client, err = mod.maybe_build_bigquery_client()
        assert client is None
        assert "RuntimeError" in err


# ============================================================
# query_bigquery
# ============================================================

class TestQueryBigquery:
    def test_happy_path(self, mod):
        mock_client = MagicMock()
        row1 = MagicMock()
        row1.items.return_value = [("corpus", "hamlet"), ("count", 10)]
        mock_client.query.return_value.result.return_value = [row1]
        df = mod.query_bigquery(mock_client, "SELECT 1")
        # pd.DataFrame was called
        assert sys.modules["pandas"].DataFrame.called

    def test_timeout(self, mod):
        mock_client = MagicMock()
        mock_client.query.return_value.result.side_effect = TimeoutError("timeout")
        with pytest.raises(TimeoutError):
            mod.query_bigquery(mock_client, "SELECT 1", timeout=1)


# ============================================================
# Fallback data generators
# ============================================================

class TestFallbackData:
    def test_fallback_shakespeare(self, mod):
        result = mod.fallback_shakespeare_corpus()
        assert result is not None

    def test_fallback_ga4(self, mod):
        result = mod.fallback_ga4_daily()
        assert result is not None

    def test_fallback_histogram(self, mod):
        result = mod.fallback_histogram_data()
        assert result is not None


# ============================================================
# get_shakespeare_corpus / get_ga4_daily / get_histogram_data
# ============================================================

class TestGetShakespeareCorpus:
    def test_client_none_uses_fallback(self, mod):
        df, source, detail = mod.get_shakespeare_corpus(None)
        assert source == "fallback"
        assert detail == "BigQuery client unavailable"

    def test_client_query_success(self, mod):
        mock_client = MagicMock()
        with patch.object(mod, "query_bigquery", return_value=MagicMock()):
            df, source, detail = mod.get_shakespeare_corpus(mock_client)
        assert source == "bigquery"
        assert detail is None

    def test_client_query_failure(self, mod):
        mock_client = MagicMock()
        with patch.object(mod, "query_bigquery", side_effect=RuntimeError("fail")):
            df, source, detail = mod.get_shakespeare_corpus(mock_client)
        assert source == "fallback"
        assert "RuntimeError" in detail


class TestGetGa4Daily:
    def test_client_none(self, mod):
        df, source, detail = mod.get_ga4_daily(None)
        assert source == "fallback"

    def test_client_success_nonempty(self, mod):
        mock_client = MagicMock()
        mock_df = MagicMock()
        mock_df.empty = False
        with patch.object(mod, "query_bigquery", return_value=mock_df):
            df, source, detail = mod.get_ga4_daily(mock_client)
        assert source == "bigquery"

    def test_client_exception(self, mod):
        mock_client = MagicMock()
        with patch.object(mod, "query_bigquery", side_effect=ValueError("bad")):
            df, source, detail = mod.get_ga4_daily(mock_client)
        assert source == "fallback"


class TestGetHistogramData:
    def test_client_none(self, mod):
        df, source, detail = mod.get_histogram_data(None)
        assert source == "fallback"

    def test_client_query_error(self, mod):
        mock_client = MagicMock()
        with patch.object(mod, "query_bigquery", side_effect=OSError("err")):
            df, source, detail = mod.get_histogram_data(mock_client)
        assert source == "fallback"
        assert "OSError" in detail


# ============================================================
# Chart saving functions
# ============================================================

class TestSaveCharts:
    def _mock_df(self):
        df = MagicMock()
        df.sort_values.return_value = df
        df.__getitem__ = MagicMock(return_value=[1, 2, 3])
        df.iterrows.return_value = iter([])
        return df

    def test_save_bar_chart(self, mod, tmp_path):
        mod.save_bar_chart(self._mock_df(), tmp_path / "bar.png")

    def test_save_line_chart(self, mod, tmp_path):
        mod.save_line_chart(self._mock_df(), tmp_path / "line.png")

    def test_save_histogram(self, mod, tmp_path):
        df = MagicMock()
        df.__getitem__ = MagicMock(return_value=[1, 2, 3])
        mod.save_histogram(df, tmp_path / "hist.png")

    def test_save_scatter(self, mod, tmp_path):
        mod.save_scatter(self._mock_df(), tmp_path / "scatter.png")

    def test_save_dashboard(self, mod, tmp_path):
        plt_mod = sys.modules["matplotlib.pyplot"]
        fig_mock = MagicMock()
        axes = MagicMock()
        ax_mock = MagicMock()
        ax_mock.spines = {"top": MagicMock(), "right": MagicMock()}
        axes.__getitem__ = MagicMock(return_value=ax_mock)
        axes.flat = [ax_mock, ax_mock, ax_mock, ax_mock]
        plt_mod.subplots.return_value = (fig_mock, axes)

        mod.save_dashboard(
            self._mock_df(), self._mock_df(), self._mock_df(), tmp_path / "dash.png"
        )


# ============================================================
# run() integration
# ============================================================

class TestRun:
    def test_run_with_no_client(self, mod, tmp_path):
        mod.OUTPUT_DIR = tmp_path / "output"
        mod.REPORT_PATH = mod.OUTPUT_DIR / "report.json"
        with (
            patch.object(mod, "maybe_build_bigquery_client", return_value=(None, "no creds")),
            patch.object(mod, "save_bar_chart"),
            patch.object(mod, "save_line_chart"),
            patch.object(mod, "save_histogram"),
            patch.object(mod, "save_scatter"),
            patch.object(mod, "save_dashboard"),
        ):
            # Create fake output files so completion check passes
            mod.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            for name in [
                "chart-4-4-bar.png", "chart-4-4-line.png",
                "chart-4-4-hist.png", "chart-4-4-scatter.png", "dashboard-4-4.png"
            ]:
                (mod.OUTPUT_DIR / name).write_bytes(b"fake")

            result = mod.run()
        assert result == 0
        assert mod.REPORT_PATH.exists()
        report = json.loads(mod.REPORT_PATH.read_text())
        assert report["lesson"].startswith("Lesson 4-4")

    def test_run_with_client(self, mod, tmp_path):
        mod.OUTPUT_DIR = tmp_path / "output2"
        mod.REPORT_PATH = mod.OUTPUT_DIR / "report.json"
        mock_client = MagicMock()
        mock_client.project = "test-proj"
        with (
            patch.object(mod, "maybe_build_bigquery_client", return_value=(mock_client, None)),
            patch.object(mod, "get_shakespeare_corpus", return_value=(MagicMock(), "bigquery", None)),
            patch.object(mod, "get_ga4_daily", return_value=(MagicMock(), "bigquery", None)),
            patch.object(mod, "get_histogram_data", return_value=(MagicMock(), "bigquery", None)),
            patch.object(mod, "save_bar_chart"),
            patch.object(mod, "save_line_chart"),
            patch.object(mod, "save_histogram"),
            patch.object(mod, "save_scatter"),
            patch.object(mod, "save_dashboard"),
        ):
            mod.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            for name in [
                "chart-4-4-bar.png", "chart-4-4-line.png",
                "chart-4-4-hist.png", "chart-4-4-scatter.png", "dashboard-4-4.png"
            ]:
                (mod.OUTPUT_DIR / name).write_bytes(b"fake")
            result = mod.run()
        assert result == 0

    def test_run_missing_outputs(self, mod, tmp_path):
        mod.OUTPUT_DIR = tmp_path / "output3"
        mod.REPORT_PATH = mod.OUTPUT_DIR / "report.json"
        with (
            patch.object(mod, "maybe_build_bigquery_client", return_value=(None, "err")),
            patch.object(mod, "save_bar_chart"),
            patch.object(mod, "save_line_chart"),
            patch.object(mod, "save_histogram"),
            patch.object(mod, "save_scatter"),
            patch.object(mod, "save_dashboard"),
        ):
            mod.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            # Don't create output files -> completion_check should be "failed"
            result = mod.run()
        assert result == 0
        report = json.loads(mod.REPORT_PATH.read_text())
        completion = [r for r in report["results"] if r["step"] == "completion_check"]
        assert completion[0]["status"] == "failed"

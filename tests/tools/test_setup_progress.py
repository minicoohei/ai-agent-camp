"""setup_progress.py の単体テスト。

ファイルシステム操作をモックし、セットアップ進捗トラッキングロジックを検証する。
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))
import setup_progress as sp


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def progress_file(tmp_path):
    """tmp_path内に進捗ファイルを設定"""
    f = tmp_path / ".setup-progress.json"
    with patch.object(sp, "PROGRESS_FILE", f):
        yield f


@pytest.fixture
def init_data():
    """初期状態の進捗データ"""
    return sp._init_progress()


# ---------------------------------------------------------------------------
# _init_progress
# ---------------------------------------------------------------------------

class TestInitProgress:
    def test_has_version(self):
        data = sp._init_progress()
        assert data["version"] == 1

    def test_has_last_updated(self):
        data = sp._init_progress()
        assert "last_updated" in data
        datetime.fromisoformat(data["last_updated"])

    def test_all_steps_present(self):
        data = sp._init_progress()
        for entry in sp.SETUP_ORDER:
            assert entry["step"] in data["steps"]

    def test_all_steps_not_started(self):
        data = sp._init_progress()
        for step_data in data["steps"].values():
            assert step_data["status"] == "not_started"
            assert step_data["completed_at"] is None
            assert step_data["details"] == {}

    def test_step_count_matches_order(self):
        data = sp._init_progress()
        assert len(data["steps"]) == len(sp.SETUP_ORDER)


# ---------------------------------------------------------------------------
# _bar
# ---------------------------------------------------------------------------

class TestBar:
    def test_zero_total(self):
        result = sp._bar(0, 0)
        assert len(result) == 20
        assert "\u2588" not in result

    def test_all_done(self):
        result = sp._bar(10, 10)
        assert result == "\u2588" * 20

    def test_half_done(self):
        result = sp._bar(5, 10)
        assert result == "\u2588" * 10 + "\u2591" * 10

    def test_custom_width(self):
        result = sp._bar(5, 10, width=10)
        assert len(result) == 10
        assert result == "\u2588" * 5 + "\u2591" * 5

    def test_one_of_many(self):
        result = sp._bar(1, 100, width=100)
        assert result.count("\u2588") == 1
        assert result.count("\u2591") == 99

    def test_boundary_done_equals_total(self):
        result = sp._bar(1, 1, width=5)
        assert result == "\u2588" * 5

    def test_zero_done_nonzero_total(self):
        result = sp._bar(0, 10, width=10)
        assert result == "\u2591" * 10


# ---------------------------------------------------------------------------
# load_progress / save_progress
# ---------------------------------------------------------------------------

class TestLoadSaveProgress:
    def test_load_no_file_returns_init(self, progress_file):
        data = sp.load_progress()
        assert data["version"] == 1
        assert "steps" in data

    def test_save_and_load_roundtrip(self, progress_file):
        data = sp._init_progress()
        data["steps"]["setup-start"]["status"] = "completed"
        sp.save_progress(data)
        loaded = sp.load_progress()
        assert loaded["steps"]["setup-start"]["status"] == "completed"

    def test_corrupted_json_returns_init(self, progress_file):
        progress_file.write_text("not valid json{{{", encoding="utf-8")
        data = sp.load_progress()
        assert data["version"] == 1
        assert all(
            s["status"] == "not_started" for s in data["steps"].values()
        )

    def test_empty_file_returns_init(self, progress_file):
        progress_file.write_text("", encoding="utf-8")
        data = sp.load_progress()
        assert data["version"] == 1

    def test_save_updates_last_updated(self, progress_file):
        data = sp._init_progress()
        data["last_updated"] = "2000-01-01T00:00:00"
        sp.save_progress(data)
        loaded = sp.load_progress()
        assert loaded["last_updated"] != "2000-01-01T00:00:00"


# ---------------------------------------------------------------------------
# _get_next
# ---------------------------------------------------------------------------

class TestGetNext:
    def test_all_not_started(self, init_data):
        nxt = sp._get_next(init_data)
        assert nxt == sp.SETUP_ORDER[0]["step"]

    def test_first_completed(self, init_data):
        init_data["steps"][sp.SETUP_ORDER[0]["step"]]["status"] = "completed"
        nxt = sp._get_next(init_data)
        assert nxt == sp.SETUP_ORDER[1]["step"]

    def test_first_skipped(self, init_data):
        init_data["steps"][sp.SETUP_ORDER[0]["step"]]["status"] = "skipped"
        nxt = sp._get_next(init_data)
        assert nxt == sp.SETUP_ORDER[1]["step"]

    def test_all_completed(self, init_data):
        for step in sp.STEP_NAMES:
            init_data["steps"][step]["status"] = "completed"
        assert sp._get_next(init_data) is None

    def test_all_skipped(self, init_data):
        for step in sp.STEP_NAMES:
            init_data["steps"][step]["status"] = "skipped"
        assert sp._get_next(init_data) is None

    def test_middle_completed(self, init_data):
        for step in sp.STEP_NAMES[:2]:
            init_data["steps"][step]["status"] = "completed"
        assert sp._get_next(init_data) == sp.STEP_NAMES[2]


# ---------------------------------------------------------------------------
# mark_complete
# ---------------------------------------------------------------------------

class TestMarkComplete:
    def test_mark_valid_step(self, init_data):
        data = sp.mark_complete(init_data, "setup-start")
        assert data["steps"]["setup-start"]["status"] == "completed"
        assert data["steps"]["setup-start"]["completed_at"] is not None

    def test_mark_with_details(self, init_data):
        details = {"python": "3.12", "node": "20.0"}
        data = sp.mark_complete(init_data, "setup-start", details)
        assert data["steps"]["setup-start"]["details"] == details

    def test_mark_without_details(self, init_data):
        data = sp.mark_complete(init_data, "setup-start")
        assert data["steps"]["setup-start"]["details"] == {}

    def test_invalid_step_exits(self, init_data):
        with pytest.raises(SystemExit):
            sp.mark_complete(init_data, "nonexistent-step")

    def test_empty_step_name_exits(self, init_data):
        with pytest.raises(SystemExit):
            sp.mark_complete(init_data, "")

    def test_overwrite_existing_status(self, init_data):
        init_data["steps"]["setup-start"]["status"] = "skipped"
        data = sp.mark_complete(init_data, "setup-start")
        assert data["steps"]["setup-start"]["status"] == "completed"


# ---------------------------------------------------------------------------
# mark_skipped
# ---------------------------------------------------------------------------

class TestMarkSkipped:
    def test_mark_valid_step(self, init_data):
        data = sp.mark_skipped(init_data, "setup-slack", reason="後で設定する")
        assert data["steps"]["setup-slack"]["status"] == "skipped"
        assert data["steps"]["setup-slack"]["details"]["reason"] == "後で設定する"

    def test_mark_without_reason(self, init_data):
        data = sp.mark_skipped(init_data, "setup-slack")
        assert data["steps"]["setup-slack"]["details"]["reason"] == ""

    def test_invalid_step_exits(self, init_data):
        with pytest.raises(SystemExit):
            sp.mark_skipped(init_data, "nonexistent-step")

    def test_unicode_reason(self, init_data):
        data = sp.mark_skipped(init_data, "setup-slack", reason="理由：日本語テスト")
        assert "日本語テスト" in data["steps"]["setup-slack"]["details"]["reason"]


# ---------------------------------------------------------------------------
# get_step_status
# ---------------------------------------------------------------------------

class TestGetStepStatus:
    def test_existing_step(self, init_data):
        assert sp.get_step_status(init_data, "setup-start") == "not_started"

    def test_completed_step(self, init_data):
        init_data["steps"]["setup-start"]["status"] = "completed"
        assert sp.get_step_status(init_data, "setup-start") == "completed"

    def test_unknown_step(self, init_data):
        assert sp.get_step_status(init_data, "nonexistent") == "not_started"

    def test_empty_steps_dict(self):
        data = {"steps": {}}
        assert sp.get_step_status(data, "setup-start") == "not_started"


# ---------------------------------------------------------------------------
# show_progress
# ---------------------------------------------------------------------------

class TestShowProgress:
    def test_show_no_crash(self, init_data, capsys):
        sp.show_progress(init_data)
        captured = capsys.readouterr()
        assert "セットアップ進捗" in captured.out

    def test_show_with_current_step(self, init_data, capsys):
        sp.show_progress(init_data, current_step="setup-start")
        captured = capsys.readouterr()
        assert "今ここ" in captured.out

    def test_show_all_completed(self, init_data, capsys):
        for step in sp.STEP_NAMES:
            init_data["steps"][step]["status"] = "completed"
        sp.show_progress(init_data)
        captured = capsys.readouterr()
        assert "全完了" in captured.out

    def test_show_partial_progress(self, init_data, capsys):
        init_data["steps"]["setup-start"]["status"] = "completed"
        sp.show_progress(init_data)
        captured = capsys.readouterr()
        assert "次のステップ" in captured.out


# ---------------------------------------------------------------------------
# SETUP_ORDER / STEP_NAMES integrity
# ---------------------------------------------------------------------------

class TestSetupOrder:
    def test_step_names_match_order(self):
        assert sp.STEP_NAMES == [s["step"] for s in sp.SETUP_ORDER]

    def test_all_steps_have_required_keys(self):
        for entry in sp.SETUP_ORDER:
            assert "step" in entry
            assert "label" in entry
            assert "required" in entry
            assert "command" in entry
            assert "description" in entry

    def test_no_duplicate_steps(self):
        assert len(sp.STEP_NAMES) == len(set(sp.STEP_NAMES))

    def test_at_least_one_required(self):
        required = [s for s in sp.SETUP_ORDER if s["required"]]
        assert len(required) > 0


# ---------------------------------------------------------------------------
# main (CLI)
# ---------------------------------------------------------------------------

class TestMain:
    def test_no_command_exits(self):
        with patch("sys.argv", ["setup_progress.py"]):
            with pytest.raises(SystemExit):
                sp.main()

    def test_show_command(self, progress_file, capsys):
        with patch("sys.argv", ["setup_progress.py", "show"]):
            sp.main()
        captured = capsys.readouterr()
        assert "セットアップ進捗" in captured.out

    def test_next_command(self, progress_file, capsys):
        with patch("sys.argv", ["setup_progress.py", "next"]):
            sp.main()
        captured = capsys.readouterr()
        assert "次のステップ" in captured.out

    def test_status_command(self, progress_file, capsys):
        with patch("sys.argv", ["setup_progress.py", "status", "setup-start"]):
            sp.main()
        captured = capsys.readouterr()
        assert "setup-start" in captured.out

    def test_reset_command(self, progress_file, capsys):
        with patch("sys.argv", ["setup_progress.py", "reset"]):
            sp.main()
        captured = capsys.readouterr()
        assert "リセット" in captured.out

    def test_complete_command(self, progress_file, capsys):
        with patch("sys.argv", ["setup_progress.py", "complete", "setup-start"]):
            sp.main()
        captured = capsys.readouterr()
        assert "セットアップ進捗" in captured.out

    def test_complete_with_json_details(self, progress_file, capsys):
        with patch("sys.argv", [
            "setup_progress.py", "complete", "setup-start",
            "--details", '{"python":"3.12"}'
        ]):
            sp.main()
        data = json.loads(progress_file.read_text(encoding="utf-8"))
        assert data["steps"]["setup-start"]["details"]["python"] == "3.12"

    def test_complete_with_invalid_json_details(self, progress_file, capsys):
        with patch("sys.argv", [
            "setup_progress.py", "complete", "setup-start",
            "--details", "not-json"
        ]):
            sp.main()
        data = json.loads(progress_file.read_text(encoding="utf-8"))
        assert data["steps"]["setup-start"]["details"] == {}

    def test_skip_command(self, progress_file, capsys):
        with patch("sys.argv", [
            "setup_progress.py", "skip", "setup-slack",
            "--reason", "後で設定"
        ]):
            sp.main()
        data = json.loads(progress_file.read_text(encoding="utf-8"))
        assert data["steps"]["setup-slack"]["status"] == "skipped"

"""Unit tests for the lesson command/slide drift checker."""

import sys
from pathlib import Path

from tests.conftest import import_module_from_repo


drift_check = import_module_from_repo(
    "lesson_drift_check", "tools/lesson_drift_check/check.py"
)


def test_setup_m365cli_maps_to_module_19():
    assert drift_check.derive_module_id(Path("setup-m365cli.md")) == "module-19"


def test_unmapped_summary_uses_module_id(tmp_path, monkeypatch, capsys):
    commands = tmp_path / "commands"
    course = tmp_path / "course"
    commands.mkdir()
    course.mkdir()
    (commands / "check-setup.md").write_text("# Check setup\n", encoding="utf-8")

    csv_report = tmp_path / "lesson-drift.csv"
    md_report = tmp_path / "lesson-drift.md"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "check.py",
            "--commands",
            str(commands),
            "--course",
            str(course),
            "--csv",
            str(csv_report),
            "--md",
            str(md_report),
        ],
    )

    assert drift_check.main() == 0
    assert "Unmapped (filename does not encode a module): **1**" in md_report.read_text(
        encoding="utf-8"
    )
    assert "unmapped=1" in capsys.readouterr().out

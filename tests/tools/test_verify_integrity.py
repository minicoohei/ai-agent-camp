"""tools/scripts/verify_integrity.py の単体テスト。"""
from __future__ import annotations

import subprocess

import pytest

from tests.conftest import import_module_from_repo


vi = import_module_from_repo(
    "verify_integrity_under_test", "tools/scripts/verify_integrity.py"
)


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "git@github.com:Minicoohei/AI-Agent-Camp.git",
            "https://github.com/minicoohei/ai-agent-camp",
        ),
        (
            "HTTPS://GITHUB.COM/MINICOOHEI/AI-AGENT-CAMP.GIT",
            "https://github.com/minicoohei/ai-agent-camp",
        ),
    ],
)
def test_normalize_url(url, expected):
    assert vi._normalize_url(url) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "https://github.com/minicoohei/ai-agent-camp.git",
            ("ok", "https://github.com/minicoohei/ai-agent-camp.git", True),
        ),
        (
            "https://github.com/example/ai-agent-camp.git",
            ("fork", "https://github.com/example/ai-agent-camp.git", False),
        ),
        ("", ("missing-origin", "", False)),
    ],
)
def test_check_origin_branches(monkeypatch, raw, expected):
    monkeypatch.setattr(
        vi.subprocess,
        "run",
        lambda cmd, **_kwargs: subprocess.CompletedProcess(
            cmd, 0, stdout="true\n", stderr=""
        ),
    )
    monkeypatch.setattr(vi, "_run", lambda _cmd: raw)
    assert vi.check_origin() == expected


def test_check_origin_without_git_executable(monkeypatch):
    def no_git(*_args, **_kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(vi.subprocess, "run", no_git)
    assert vi.check_origin() == ("no-git", "", False)


def test_check_origin_outside_git_repository(monkeypatch):
    monkeypatch.setattr(
        vi.subprocess,
        "run",
        lambda cmd, **_kwargs: subprocess.CompletedProcess(
            cmd, 128, stdout="", stderr="not a git repository"
        ),
    )
    assert vi.check_origin() == ("no-git", "", False)


@pytest.mark.parametrize(
    ("diff_returncode", "status"),
    [(0, None), (1, "diff"), (128, "error")],
)
def test_check_upstream_drift_returncodes(monkeypatch, diff_returncode, status):
    def fake_run(cmd, **_kwargs):
        if cmd == ["git", "remote"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="upstream\n", stderr="")
        return subprocess.CompletedProcess(cmd, diff_returncode, stdout="", stderr="")

    monkeypatch.setattr(vi.subprocess, "run", fake_run)
    monkeypatch.setattr(vi, "INTEGRITY_TRACKED_FILES", ("tracked.txt",))

    result = vi.check_upstream_drift()

    if status is None:
        assert result == []
    else:
        assert result == [{"path": "tracked.txt", "status": status}]


def test_pre_commit_hook_is_active(monkeypatch, tmp_path):
    hooks_dir = tmp_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    hook = hooks_dir / "pre-commit"
    hook.write_text("#!/bin/sh\n", encoding="utf-8")
    hook.chmod(0o755)
    monkeypatch.setattr(vi, "_run", lambda _cmd: str(hooks_dir))

    assert vi.check_pre_commit_hook() == (True, str(hook))


@pytest.mark.parametrize("mode", [0o644, None])
def test_pre_commit_hook_is_inactive(monkeypatch, tmp_path, mode):
    hooks_dir = tmp_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True)
    hook = hooks_dir / "pre-commit"
    if mode is not None:
        hook.write_text("#!/bin/sh\n", encoding="utf-8")
        hook.chmod(mode)
    monkeypatch.setattr(vi, "_run", lambda _cmd: str(hooks_dir))

    assert vi.check_pre_commit_hook() == (False, str(hook))


def test_pre_commit_hook_uses_configured_hooks_path(monkeypatch, tmp_path):
    hooks_dir = tmp_path / "custom-hooks"
    hooks_dir.mkdir()
    hook = hooks_dir / "pre-commit"
    hook.write_text("#!/bin/sh\n", encoding="utf-8")
    hook.chmod(0o755)
    calls = []

    def fake_run(cmd):
        calls.append(cmd)
        return "custom-hooks"

    monkeypatch.setattr(vi, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(vi, "_run", fake_run)

    assert vi.check_pre_commit_hook() == (True, str(hook))
    assert calls == [["git", "rev-parse", "--git-path", "hooks"]]

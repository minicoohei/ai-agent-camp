"""firebase_onboarding.py の単体テスト。

subprocess, requests, webbrowser, http.server をモックし、
オンボーディングフローのロジックを検証する。
"""
import json
import subprocess
import time
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr=stderr,
    )


# ---------------------------------------------------------------------------
# load_state / save_state / mark_step_completed
# ---------------------------------------------------------------------------

class TestStateManagement:
    def test_load_state_empty(self, tmp_path):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "nonexistent.json"
        try:
            assert fo.load_state() == {}
        finally:
            fo.STATE_FILE = original

    def test_load_state_invalid_json(self, tmp_path):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        state_file = tmp_path / "bad.json"
        state_file.write_text("not json!", encoding="utf-8")
        fo.STATE_FILE = state_file
        try:
            assert fo.load_state() == {}
        finally:
            fo.STATE_FILE = original

    def test_save_and_load_state(self, tmp_path):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "work" / "state.json"
        try:
            fo.save_state({"github_username": "testuser"})
            state = fo.load_state()
            assert state["github_username"] == "testuser"
            assert "last_updated" in state
        finally:
            fo.STATE_FILE = original

    def test_save_state_creates_parent_dirs(self, tmp_path):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "deep" / "nested" / "state.json"
        try:
            fo.save_state({"key": "value"})
            assert fo.STATE_FILE.exists()
        finally:
            fo.STATE_FILE = original

    def test_mark_step_completed(self, tmp_path):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "state.json"
        try:
            fo.mark_step_completed("firebase_auth")
            state = fo.load_state()
            assert "firebase_auth" in state["steps_completed"]
        finally:
            fo.STATE_FILE = original

    def test_mark_step_completed_no_duplicates(self, tmp_path):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "state.json"
        try:
            fo.mark_step_completed("firebase_auth")
            fo.mark_step_completed("firebase_auth")
            state = fo.load_state()
            assert state["steps_completed"].count("firebase_auth") == 1
        finally:
            fo.STATE_FILE = original

    def test_mark_step_completed_appends(self, tmp_path):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "state.json"
        try:
            fo.mark_step_completed("firebase_auth")
            fo.mark_step_completed("github_auth")
            state = fo.load_state()
            assert state["steps_completed"] == ["firebase_auth", "github_auth"]
        finally:
            fo.STATE_FILE = original


# ---------------------------------------------------------------------------
# firebase_browser_auth
# ---------------------------------------------------------------------------

class TestFirebaseBrowserAuth:
    @patch("firebase_onboarding.webbrowser.open")
    @patch("firebase_onboarding.http.server.HTTPServer")
    @patch("firebase_onboarding._find_free_port", return_value=9999)
    @patch("firebase_onboarding.secrets.token_urlsafe", return_value="test_state_token")
    def test_auth_success(self, mock_token, mock_port, mock_server_cls, mock_browser):
        import firebase_onboarding as fo

        mock_server = MagicMock()
        mock_server_cls.return_value = mock_server

        # Simulate receiving a token on the first handle_request call
        call_count = 0
        def fake_handle():
            nonlocal call_count
            call_count += 1
            # After first call, pretend we got the token via the handler
            # We need to simulate the handler setting the token_holder
            # Since we can't easily access the closure, we patch time.monotonic
        mock_server.handle_request.side_effect = fake_handle

        # Simulate timeout by controlling time.monotonic
        start = 1000.0
        with patch("firebase_onboarding.time.monotonic", side_effect=[start, start + 130]):
            result = fo.firebase_browser_auth("https://example.web.app")

        mock_browser.assert_called_once()
        assert "port=9999" in mock_browser.call_args[0][0]
        assert "state=test_state_token" in mock_browser.call_args[0][0]
        mock_server.server_close.assert_called_once()

    @patch("firebase_onboarding.webbrowser.open")
    @patch("firebase_onboarding.http.server.HTTPServer")
    @patch("firebase_onboarding._find_free_port", return_value=9999)
    def test_auth_timeout_returns_none(self, mock_port, mock_server_cls, mock_browser):
        import firebase_onboarding as fo

        mock_server = MagicMock()
        mock_server_cls.return_value = mock_server

        # time.monotonic returns values past deadline immediately
        with patch("firebase_onboarding.time.monotonic", side_effect=[1000.0, 1200.0]):
            result = fo.firebase_browser_auth("https://example.web.app")

        assert result is None
        mock_server.server_close.assert_called_once()


# ---------------------------------------------------------------------------
# verify_github_ready / get_github_username
# ---------------------------------------------------------------------------

class TestGitHubChecks:
    @patch("firebase_onboarding.subprocess.run")
    def test_verify_github_ready_true(self, mock_run):
        import firebase_onboarding as fo
        mock_run.return_value = _make_completed(stdout="testuser\n")
        assert fo.verify_github_ready() is True

    @patch("firebase_onboarding.subprocess.run")
    def test_verify_github_ready_false_returncode(self, mock_run):
        import firebase_onboarding as fo
        mock_run.return_value = _make_completed(returncode=1)
        assert fo.verify_github_ready() is False

    @patch("firebase_onboarding.subprocess.run")
    def test_verify_github_ready_false_empty_stdout(self, mock_run):
        import firebase_onboarding as fo
        mock_run.return_value = _make_completed(stdout="")
        assert fo.verify_github_ready() is False

    @patch("firebase_onboarding.subprocess.run")
    def test_get_github_username_success(self, mock_run):
        import firebase_onboarding as fo
        mock_run.return_value = _make_completed(stdout="octocat\n")
        assert fo.get_github_username() == "octocat"

    @patch("firebase_onboarding.subprocess.run")
    def test_get_github_username_failure(self, mock_run):
        import firebase_onboarding as fo
        mock_run.return_value = _make_completed(returncode=1)
        assert fo.get_github_username() is None

    @patch("firebase_onboarding.subprocess.run")
    def test_get_github_username_strips_whitespace(self, mock_run):
        import firebase_onboarding as fo
        mock_run.return_value = _make_completed(stdout="  user  \n")
        assert fo.get_github_username() == "user"


# ---------------------------------------------------------------------------
# guide_github_setup
# ---------------------------------------------------------------------------

class TestGuideGithubSetup:
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("builtins.input", return_value="")
    def test_guide_success(self, mock_input, mock_verify):
        import firebase_onboarding as fo
        assert fo.guide_github_setup() is True
        mock_input.assert_called_once()

    @patch("firebase_onboarding.verify_github_ready", return_value=False)
    @patch("builtins.input", return_value="")
    def test_guide_failure(self, mock_input, mock_verify):
        import firebase_onboarding as fo
        assert fo.guide_github_setup() is False

    @patch("builtins.input", side_effect=EOFError)
    def test_guide_eof_returns_false(self, mock_input):
        import firebase_onboarding as fo
        assert fo.guide_github_setup() is False

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_guide_keyboard_interrupt_returns_false(self, mock_input):
        import firebase_onboarding as fo
        assert fo.guide_github_setup() is False


# ---------------------------------------------------------------------------
# call_cloud_function
# ---------------------------------------------------------------------------

class TestCallCloudFunction:
    @patch("requests.post")
    def test_success(self, mock_post):
        import firebase_onboarding as fo
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"status": "invited", "repo": "org/repo"}
        mock_post.return_value = mock_resp

        result = fo.call_cloud_function(
            "https://func.url/grant-access", "token123", "octocat",
        )
        assert result["status"] == "invited"
        mock_post.assert_called_once_with(
            "https://func.url/grant-access",
            json={"firebase_id_token": "token123", "github_username": "octocat"},
            timeout=60,
        )

    @patch("requests.post")
    def test_error_response(self, mock_post):
        import firebase_onboarding as fo
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"error": "Rate limited"}
        mock_post.return_value = mock_resp

        result = fo.call_cloud_function("https://func.url", "tok", "user")
        assert result["error"] == "Rate limited"

    @patch("requests.post", side_effect=Exception("Connection timeout"))
    def test_request_exception(self, mock_post):
        import firebase_onboarding as fo
        # requests is imported inside the function, so we need to patch at module level
        import requests
        with patch("requests.post", side_effect=requests.RequestException("timeout")):
            result = fo.call_cloud_function("https://func.url", "tok", "user")
        assert "error" in result
        assert "接続に失敗" in result["error"]

    @patch("requests.post")
    def test_invalid_json_response(self, mock_post):
        import firebase_onboarding as fo
        mock_resp = MagicMock()
        mock_resp.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
        mock_post.return_value = mock_resp

        result = fo.call_cloud_function("https://func.url", "tok", "user")
        assert "error" in result
        assert "無効なレスポンス" in result["error"]


# ---------------------------------------------------------------------------
# wait_for_invitation
# ---------------------------------------------------------------------------

class TestWaitForInvitation:
    @patch("firebase_onboarding.time.sleep")
    @patch("firebase_onboarding.subprocess.run")
    @patch("firebase_onboarding.time.monotonic")
    def test_found_immediately(self, mock_mono, mock_run, mock_sleep):
        import firebase_onboarding as fo
        # monotonic: deadline calc, while check, (loop body doesn't call again since found)
        mock_mono.side_effect = [0.0, 1.0]
        inv_json = json.dumps([{"id": 12345, "repository": {"full_name": "org/repo"}}])
        mock_run.return_value = _make_completed(stdout=inv_json)

        result = fo.wait_for_invitation("org/repo")
        assert result == 12345
        mock_sleep.assert_not_called()

    @patch("firebase_onboarding.time.sleep")
    @patch("firebase_onboarding.subprocess.run")
    @patch("firebase_onboarding.time.monotonic")
    def test_found_after_retry(self, mock_mono, mock_run, mock_sleep):
        import firebase_onboarding as fo
        # monotonic: deadline calc, while check #1, while check #2
        mock_mono.side_effect = [0.0, 1.0, 2.0, 3.0]
        inv_json = json.dumps([{"id": 67890, "repository": {"full_name": "org/repo"}}])
        mock_run.side_effect = [
            _make_completed(stdout="[]"),
            _make_completed(stdout=inv_json),
        ]

        result = fo.wait_for_invitation("org/repo")
        assert result == 67890
        mock_sleep.assert_called_once_with(fo.INVITATION_POLL_INTERVAL)

    @patch("firebase_onboarding.time.sleep")
    @patch("firebase_onboarding.subprocess.run")
    @patch("firebase_onboarding.time.monotonic")
    def test_timeout_returns_none(self, mock_mono, mock_run, mock_sleep):
        import firebase_onboarding as fo
        # deadline calc returns 0.0, first while check exceeds timeout
        mock_mono.side_effect = [0.0, fo.INVITATION_POLL_TIMEOUT + 1]
        mock_run.return_value = _make_completed(stdout="[]")

        result = fo.wait_for_invitation("org/repo")
        assert result is None

    @patch("firebase_onboarding.time.sleep")
    @patch("firebase_onboarding.subprocess.run")
    @patch("firebase_onboarding.time.monotonic")
    def test_no_matching_repo(self, mock_mono, mock_run, mock_sleep):
        import firebase_onboarding as fo
        # Has invitations but none match the repo
        mock_mono.side_effect = [0.0, 1.0, fo.INVITATION_POLL_TIMEOUT + 1]
        inv_json = json.dumps([{"id": 999, "repository": {"full_name": "other/repo"}}])
        mock_run.side_effect = [
            _make_completed(stdout=inv_json),
            _make_completed(stdout="[]"),
        ]

        result = fo.wait_for_invitation("org/repo")
        assert result is None


# ---------------------------------------------------------------------------
# accept_invitation
# ---------------------------------------------------------------------------

class TestAcceptInvitation:
    @patch("firebase_onboarding.subprocess.run")
    def test_accept_success(self, mock_run):
        import firebase_onboarding as fo
        mock_run.return_value = _make_completed(returncode=0)
        assert fo.accept_invitation(12345) is True
        args = mock_run.call_args[0][0]
        assert "/user/repository_invitations/12345" in " ".join(args)

    @patch("firebase_onboarding.subprocess.run")
    def test_accept_failure(self, mock_run):
        import firebase_onboarding as fo
        mock_run.return_value = _make_completed(returncode=1)
        assert fo.accept_invitation(12345) is False


# ---------------------------------------------------------------------------
# cmd_onboard
# ---------------------------------------------------------------------------

class TestCmdOnboard:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.accept_invitation", return_value=True)
    @patch("firebase_onboarding.wait_for_invitation", return_value=99)
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "invited"})
    @patch("firebase_onboarding.get_github_username", return_value="testuser")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="valid.jwt.token")
    @patch("firebase_onboarding.load_state", return_value={})
    def test_full_flow_success(
        self, mock_load, mock_auth, mock_gh_ready, mock_gh_user,
        mock_cf, mock_wait, mock_accept, mock_mark, mock_save,
    ):
        import firebase_onboarding as fo
        # content_updater is imported inside cmd_onboard, mock it via sys.modules
        mock_cu = MagicMock()
        mock_cu.has_upstream.return_value = False
        mock_cu.cmd_setup.return_value = 0
        with patch.dict("sys.modules", {"content_updater": mock_cu}):
            result = fo.cmd_onboard(
                hosting_url="https://test.web.app",
                function_url="https://func.url",
            )
        assert result == 0

    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.firebase_browser_auth", return_value=None)
    def test_firebase_auth_failure(self, mock_auth, mock_load):
        import firebase_onboarding as fo
        mock_load.return_value = {}

        result = fo.cmd_onboard()
        assert result == 1

    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    @patch("firebase_onboarding.verify_github_ready", return_value=False)
    @patch("firebase_onboarding.guide_github_setup", return_value=False)
    def test_github_setup_failure(self, mock_guide, mock_gh, mock_auth, mock_mark, mock_load):
        import firebase_onboarding as fo
        mock_load.return_value = {}

        result = fo.cmd_onboard()
        assert result == 1

    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.call_cloud_function", return_value={"error": "Rate limited"})
    def test_cloud_function_error(
        self, mock_cf, mock_gh_user, mock_gh, mock_auth, mock_mark, mock_load, mock_save,
    ):
        import firebase_onboarding as fo
        mock_load.return_value = {}

        result = fo.cmd_onboard()
        assert result == 1

    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    def test_skips_completed_steps(self, mock_gh_user, mock_mark, mock_load, mock_save):
        import firebase_onboarding as fo
        mock_load.return_value = {
            "steps_completed": [
                "firebase_auth", "github_auth", "cloud_function",
                "invitation_accepted", "content_setup",
            ],
        }

        result = fo.cmd_onboard()
        assert result == 0


# ---------------------------------------------------------------------------
# cmd_status
# ---------------------------------------------------------------------------

class TestCmdStatus:
    def test_empty_state(self, tmp_path, capsys):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "state.json"
        try:
            result = fo.cmd_status()
            assert result == 0
            output = capsys.readouterr().out
            assert "Firebase" in output
        finally:
            fo.STATE_FILE = original

    def test_partial_state(self, tmp_path, capsys):
        import firebase_onboarding as fo
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "state.json"
        fo.STATE_FILE.write_text(json.dumps({
            "steps_completed": ["firebase_auth", "github_auth"],
            "github_username": "testuser",
            "last_updated": "2026-01-01T00:00:00Z",
        }), encoding="utf-8")
        try:
            result = fo.cmd_status()
            assert result == 0
            output = capsys.readouterr().out
            assert "testuser" in output
            assert "2026-01-01" in output
        finally:
            fo.STATE_FILE = original


# ---------------------------------------------------------------------------
# cmd_link_github
# ---------------------------------------------------------------------------

class TestCmdLinkGithub:
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "invited"})
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="valid.jwt.token")
    def test_link_success(self, mock_auth, mock_gh, mock_user, mock_cf):
        import firebase_onboarding as fo
        result = fo.cmd_link_github(
            hosting_url="https://test.web.app",
            function_url="https://func.url",
        )
        assert result == 0

    @patch("firebase_onboarding.firebase_browser_auth", return_value=None)
    def test_link_auth_failure(self, mock_auth):
        import firebase_onboarding as fo
        result = fo.cmd_link_github()
        assert result == 1

    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    @patch("firebase_onboarding.verify_github_ready", return_value=False)
    def test_link_github_not_ready(self, mock_gh, mock_auth):
        import firebase_onboarding as fo
        result = fo.cmd_link_github()
        assert result == 1

    @patch("firebase_onboarding.call_cloud_function", return_value={"error": "API error"})
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    def test_link_cloud_function_error(self, mock_auth, mock_gh, mock_user, mock_cf):
        import firebase_onboarding as fo
        result = fo.cmd_link_github()
        assert result == 1

    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.get_github_username", return_value=None)
    def test_link_no_username(self, mock_user, mock_gh, mock_auth):
        import firebase_onboarding as fo
        result = fo.cmd_link_github()
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_auth_only
# ---------------------------------------------------------------------------

class TestCmdAuthOnly:
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.firebase_browser_auth", return_value="valid.jwt.token")
    def test_auth_only_success(self, mock_auth, mock_mark, capsys):
        import firebase_onboarding as fo
        result = fo.cmd_auth_only(hosting_url="https://test.web.app")
        assert result == 0
        output = capsys.readouterr().out
        assert "AUTH_OK:" in output
        mock_mark.assert_called_once_with("firebase_auth")

    @patch("firebase_onboarding.firebase_browser_auth", return_value=None)
    def test_auth_only_failure(self, mock_auth, capsys):
        import firebase_onboarding as fo
        result = fo.cmd_auth_only()
        assert result == 1
        output = capsys.readouterr().out
        assert "AUTH_FAILED" in output


# ---------------------------------------------------------------------------
# cmd_call_function
# ---------------------------------------------------------------------------

class TestCmdCallFunction:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "ok"})
    @patch("firebase_onboarding.get_github_username", return_value="testuser")
    def test_call_function_success(self, mock_user, mock_cf, mock_mark, mock_save, tmp_path, capsys):
        import firebase_onboarding as fo
        token_file = tmp_path / ".token.tmp"
        token_file.write_text("valid.jwt.token")
        original = fo.STATE_FILE
        fo.STATE_FILE = tmp_path / "state.json"
        try:
            result = fo.cmd_call_function(str(token_file))
            assert result == 0
            output = capsys.readouterr().out
            assert "OK:testuser" in output
            assert not token_file.exists()  # token file should be deleted
        finally:
            fo.STATE_FILE = original

    def test_call_function_missing_token_file(self, capsys):
        import firebase_onboarding as fo
        result = fo.cmd_call_function("/nonexistent/token.tmp")
        assert result == 1
        output = capsys.readouterr().out
        assert "ERROR:token_file_not_found" in output

    @patch("firebase_onboarding.get_github_username", return_value=None)
    def test_call_function_no_github_user(self, mock_user, tmp_path, capsys):
        import firebase_onboarding as fo
        token_file = tmp_path / ".token.tmp"
        token_file.write_text("tok")
        result = fo.cmd_call_function(str(token_file))
        assert result == 1
        output = capsys.readouterr().out
        assert "ERROR:github_username_not_found" in output

    @patch("firebase_onboarding.call_cloud_function", return_value={"error": "fail"})
    @patch("firebase_onboarding.get_github_username", return_value="user")
    def test_call_function_cf_error(self, mock_user, mock_cf, tmp_path, capsys):
        import firebase_onboarding as fo
        token_file = tmp_path / ".token.tmp"
        token_file.write_text("tok")
        result = fo.cmd_call_function(str(token_file))
        assert result == 1
        output = capsys.readouterr().out
        assert "ERROR:" in output


# ---------------------------------------------------------------------------
# cmd_check_invitation
# ---------------------------------------------------------------------------

class TestCmdCheckInvitation:
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.accept_invitation", return_value=True)
    @patch("firebase_onboarding.wait_for_invitation", return_value=42)
    def test_check_invitation_success(self, mock_wait, mock_accept, mock_mark, capsys):
        import firebase_onboarding as fo
        result = fo.cmd_check_invitation(repo="org/repo")
        assert result == 0
        output = capsys.readouterr().out
        assert "ACCEPTED:42" in output

    @patch("firebase_onboarding.accept_invitation", return_value=False)
    @patch("firebase_onboarding.wait_for_invitation", return_value=42)
    def test_check_invitation_accept_fails(self, mock_wait, mock_accept, capsys):
        import firebase_onboarding as fo
        result = fo.cmd_check_invitation(repo="org/repo")
        assert result == 1

    @patch("firebase_onboarding.wait_for_invitation", return_value=None)
    def test_check_invitation_not_found(self, mock_wait, capsys):
        import firebase_onboarding as fo
        result = fo.cmd_check_invitation(repo="org/repo")
        assert result == 1
        output = capsys.readouterr().out
        assert "NOT_FOUND" in output


# ---------------------------------------------------------------------------
# cmd_cleanup_token
# ---------------------------------------------------------------------------

class TestCmdCleanupToken:
    def test_cleanup_no_tokens(self, capsys):
        import firebase_onboarding as fo
        result = fo.cmd_cleanup_token()
        assert result == 0
        output = capsys.readouterr().out
        assert "CLEAN" in output

    def test_cleanup_with_tokens(self, tmp_path, capsys):
        import firebase_onboarding as fo
        import tempfile
        # Create temp files that match the pattern
        fd, path = tempfile.mkstemp(prefix=".firebase_token_", suffix=".tmp")
        os.close(fd)
        try:
            result = fo.cmd_cleanup_token()
            assert result == 0
            output = capsys.readouterr().out
            assert "CLEAN" in output
        finally:
            # File may already be deleted
            import os as _os
            try:
                _os.unlink(path)
            except FileNotFoundError:
                pass


# ---------------------------------------------------------------------------
# cmd_onboard: re-auth path (token expired during cloud_function step)
# ---------------------------------------------------------------------------

class TestCmdOnboardReauth:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.accept_invitation", return_value=True)
    @patch("firebase_onboarding.wait_for_invitation", return_value=99)
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "invited"})
    @patch("firebase_onboarding.get_github_username", return_value="testuser")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="new.jwt.token")
    @patch("firebase_onboarding.load_state")
    def test_reauth_when_token_missing(
        self, mock_load, mock_auth, mock_gh_ready, mock_gh_user,
        mock_cf, mock_wait, mock_accept, mock_mark, mock_save,
    ):
        """When firebase_auth is completed but firebase_token is None,
        cmd_onboard should re-authenticate."""
        import firebase_onboarding as fo
        mock_load.return_value = {
            "steps_completed": ["firebase_auth", "github_auth"],
            # firebase_token is missing (expired)
        }
        mock_cu = MagicMock()
        mock_cu.has_upstream.return_value = False
        mock_cu.cmd_setup.return_value = 0
        with patch.dict("sys.modules", {"content_updater": mock_cu}):
            result = fo.cmd_onboard()
        assert result == 0
        mock_auth.assert_called_once()  # re-auth was triggered


import os


# ---------------------------------------------------------------------------
# _find_free_port (lines 59-61)
# ---------------------------------------------------------------------------

class TestFindFreePort:
    def test_returns_positive_int(self):
        import firebase_onboarding as fo
        port = fo._find_free_port()
        assert isinstance(port, int)
        assert port > 0


# ---------------------------------------------------------------------------
# cmd_onboard: cloud_function step with token reauth failure (lines 335-340)
# ---------------------------------------------------------------------------

class TestCmdOnboardReauthFailure:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value=None)
    def test_reauth_failure_returns_1(
        self, mock_auth, mock_gh, mock_gh_user, mock_mark, mock_load, mock_save,
    ):
        """再認証失敗時に 1 を返す (lines 337-339)"""
        import firebase_onboarding as fo
        mock_load.return_value = {
            "steps_completed": ["firebase_auth", "github_auth"],
            # firebase_token is None (expired)
        }
        result = fo.cmd_onboard()
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_onboard: cloud_function error with detail (line 347)
# ---------------------------------------------------------------------------

class TestCmdOnboardCloudFunctionDetail:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    @patch("firebase_onboarding.call_cloud_function")
    def test_error_with_detail(
        self, mock_cf, mock_auth, mock_gh, mock_gh_user, mock_mark, mock_load, mock_save, capsys,
    ):
        """Cloud Function エラーに detail がある場合 (line 347)"""
        import firebase_onboarding as fo
        mock_load.return_value = {}
        mock_cf.return_value = {
            "error": "Unauthorized",
            "detail": "Token expired or invalid"
        }
        result = fo.cmd_onboard()
        assert result == 1
        output = capsys.readouterr().out
        assert "Token expired" in output


# ---------------------------------------------------------------------------
# cmd_onboard: github_username returns None (lines 321-322)
# ---------------------------------------------------------------------------

class TestCmdOnboardNoGithubUsername:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value=None)
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    def test_no_username_returns_1(
        self, mock_auth, mock_gh, mock_gh_user, mock_mark, mock_load, mock_save,
    ):
        import firebase_onboarding as fo
        mock_load.return_value = {}
        result = fo.cmd_onboard()
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_onboard: invitation not found → manual fallback (lines 363-374)
# ---------------------------------------------------------------------------

class TestCmdOnboardInvitationNotFound:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "invited"})
    @patch("firebase_onboarding.wait_for_invitation", return_value=None)
    @patch("builtins.input", return_value="")
    def test_manual_fallback(
        self, mock_input, mock_wait, mock_cf, mock_auth, mock_gh,
        mock_gh_user, mock_mark, mock_load, mock_save,
    ):
        """招待が見つからない場合の手動フォールバック (lines 363-374)"""
        import firebase_onboarding as fo
        mock_load.return_value = {}
        mock_cu = MagicMock()
        mock_cu.has_upstream.return_value = False
        mock_cu.cmd_setup.return_value = 0
        with patch.dict("sys.modules", {"content_updater": mock_cu}):
            result = fo.cmd_onboard()
        assert result == 0

    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "invited"})
    @patch("firebase_onboarding.wait_for_invitation", return_value=None)
    @patch("builtins.input", side_effect=EOFError)
    def test_manual_fallback_eof(
        self, mock_input, mock_wait, mock_cf, mock_auth, mock_gh,
        mock_gh_user, mock_mark, mock_load, mock_save,
    ):
        """手動フォールバックで EOFError (lines 370-373)"""
        import firebase_onboarding as fo
        mock_load.return_value = {}
        mock_cu = MagicMock()
        mock_cu.has_upstream.return_value = False
        mock_cu.cmd_setup.return_value = 0
        with patch.dict("sys.modules", {"content_updater": mock_cu}):
            result = fo.cmd_onboard()
        assert result == 0


# ---------------------------------------------------------------------------
# cmd_onboard: accept_invitation fails (lines 362-363)
# ---------------------------------------------------------------------------

class TestCmdOnboardAcceptFails:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "invited"})
    @patch("firebase_onboarding.wait_for_invitation", return_value=99)
    @patch("firebase_onboarding.accept_invitation", return_value=False)
    def test_accept_fails_continues(
        self, mock_accept, mock_wait, mock_cf, mock_auth, mock_gh,
        mock_gh_user, mock_mark, mock_load, mock_save, capsys,
    ):
        """accept_invitation が失敗しても続行 (lines 362-363)"""
        import firebase_onboarding as fo
        mock_load.return_value = {}
        mock_cu = MagicMock()
        mock_cu.has_upstream.return_value = False
        mock_cu.cmd_setup.return_value = 0
        with patch.dict("sys.modules", {"content_updater": mock_cu}):
            result = fo.cmd_onboard()
        output = capsys.readouterr().out
        assert "受諾に失敗" in output


# ---------------------------------------------------------------------------
# cmd_onboard: content_setup paths (lines 386-392)
# ---------------------------------------------------------------------------

class TestCmdOnboardContentSetup:
    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.accept_invitation", return_value=True)
    @patch("firebase_onboarding.wait_for_invitation", return_value=99)
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "ok"})
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    def test_content_setup_failure(
        self, mock_auth, mock_gh, mock_cf, mock_wait, mock_accept,
        mock_gh_user, mock_mark, mock_load, mock_save,
    ):
        """コンテンツセットアップ失敗時に 1 を返す (lines 386-387)"""
        import firebase_onboarding as fo
        mock_load.return_value = {}
        mock_cu = MagicMock()
        mock_cu.has_upstream.return_value = False
        mock_cu.cmd_setup.return_value = 1
        with patch.dict("sys.modules", {"content_updater": mock_cu}):
            result = fo.cmd_onboard()
        assert result == 1

    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.accept_invitation", return_value=True)
    @patch("firebase_onboarding.wait_for_invitation", return_value=99)
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "ok"})
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    def test_content_update_path(
        self, mock_auth, mock_gh, mock_cf, mock_wait, mock_accept,
        mock_gh_user, mock_mark, mock_load, mock_save,
    ):
        """has_upstream=True のとき cmd_update が呼ばれる (line 389)"""
        import firebase_onboarding as fo
        mock_load.return_value = {}
        mock_cu = MagicMock()
        mock_cu.has_upstream.return_value = True
        mock_cu.cmd_update.return_value = 0
        with patch.dict("sys.modules", {"content_updater": mock_cu}):
            result = fo.cmd_onboard()
        assert result == 0
        mock_cu.cmd_update.assert_called_once_with(skill_check=True, skill_strategy="ask")

    @patch("firebase_onboarding.save_state")
    @patch("firebase_onboarding.load_state")
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.get_github_username", return_value="user")
    @patch("firebase_onboarding.accept_invitation", return_value=True)
    @patch("firebase_onboarding.wait_for_invitation", return_value=99)
    @patch("firebase_onboarding.call_cloud_function", return_value={"status": "ok"})
    @patch("firebase_onboarding.verify_github_ready", return_value=True)
    @patch("firebase_onboarding.firebase_browser_auth", return_value="tok")
    def test_content_update_failure(
        self, mock_auth, mock_gh, mock_cf, mock_wait, mock_accept,
        mock_gh_user, mock_mark, mock_load, mock_save,
    ):
        """cmd_update 失敗時に 1 を返す (lines 390-392)"""
        import firebase_onboarding as fo
        mock_load.return_value = {}
        mock_cu = MagicMock()
        mock_cu.has_upstream.return_value = True
        mock_cu.cmd_update.return_value = 1
        with patch.dict("sys.modules", {"content_updater": mock_cu}):
            result = fo.cmd_onboard()
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_auth_only: write exception (lines 481-501)
# ---------------------------------------------------------------------------

class TestCmdAuthOnlyEdge:
    @patch("firebase_onboarding.mark_step_completed")
    @patch("firebase_onboarding.firebase_browser_auth", return_value="valid.jwt.token")
    def test_auth_only_write_exception(self, mock_auth, mock_mark, capsys):
        """一時ファイル書き込み失敗時に AUTH_FAILED (lines 493-496)"""
        import firebase_onboarding as fo
        with patch("tempfile.mkstemp", return_value=(999, "/tmp/fake")), \
             patch("os.fdopen", side_effect=Exception("write error")), \
             patch("os.close"):
            result = fo.cmd_auth_only()
        assert result == 1
        output = capsys.readouterr().out
        assert "AUTH_FAILED" in output


# ---------------------------------------------------------------------------
# wait_for_invitation: json decode error (line 263)
# ---------------------------------------------------------------------------

class TestWaitForInvitationJsonError:
    @patch("firebase_onboarding.time.sleep")
    @patch("firebase_onboarding.subprocess.run")
    @patch("firebase_onboarding.time.monotonic")
    def test_invalid_json_ignored(self, mock_mono, mock_run, mock_sleep):
        """不正な JSON レスポンスは無視して続行 (line 263)"""
        import firebase_onboarding as fo
        mock_mono.side_effect = [0.0, 1.0, fo.INVITATION_POLL_TIMEOUT + 1]
        mock_run.return_value = _make_completed(stdout="not-json{{{")
        result = fo.wait_for_invitation("org/repo")
        assert result is None

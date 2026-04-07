"""Tests for tools/ugc_factory.py - UGC pipeline orchestrator."""

from __future__ import annotations

import json
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Create stubs for all heavy dependencies before importing the target
# ---------------------------------------------------------------------------

@dataclass
class _MockVideoResult:
    video_path: str = "/fake/video.mp4"
    duration: float = 10.0
    cost: float = 0.5
    engine: str = "fabric"


def _build_stubs():
    """Create stub modules for all ugc_factory dependencies."""
    stubs = {}

    # runtime_env
    re_mod = types.ModuleType("runtime_env")
    re_mod.load_runtime_env = MagicMock()
    stubs["runtime_env"] = re_mod

    # ugc package
    ugc = types.ModuleType("ugc")
    ugc.generate_ugc_script = MagicMock(return_value="test script content")
    ugc.generate_speech = MagicMock()
    ugc.composite_video = MagicMock()
    stubs["ugc"] = ugc

    # ugc.prompts
    ugc_prompts = types.ModuleType("ugc.prompts")
    ugc_prompts.load_prompts = MagicMock(return_value={})
    stubs["ugc.prompts"] = ugc_prompts

    # ugc.audio_post
    audio_post = types.ModuleType("ugc.audio_post")
    audio_post.mux_audio = MagicMock()
    audio_post.remove_vocals_from_video = MagicMock()
    audio_post.apply_wav2lip = MagicMock()
    audio_post.apply_musetalk = MagicMock()
    audio_post.extract_audio = MagicMock()
    stubs["ugc.audio_post"] = audio_post

    # ugc.engines
    engines_mod = types.ModuleType("ugc.engines")
    mock_engine = MagicMock()
    mock_engine.requires_tts = True
    mock_engine.generate = MagicMock(
        return_value=_MockVideoResult()
    )
    engines_mod.get_engine = MagicMock(return_value=mock_engine)
    engines_mod.ENGINE_MAP = {"fabric": mock_engine, "veo": mock_engine, "heygen": mock_engine, "kling": mock_engine}
    engines_mod.VideoResult = _MockVideoResult
    stubs["ugc.engines"] = engines_mod

    # nanobanana
    nb = types.ModuleType("nanobanana")
    nb.generate_image = MagicMock()
    stubs["nanobanana"] = nb

    # bootcamp_utils
    bu = types.ModuleType("bootcamp_utils")
    bu.get_client = MagicMock(return_value=MagicMock())
    stubs["bootcamp_utils"] = bu

    return stubs


@pytest.fixture(autouse=True)
def _stub_deps(monkeypatch):
    stubs = _build_stubs()
    for name, mod in stubs.items():
        monkeypatch.setitem(sys.modules, name, mod)


@pytest.fixture
def mod(tmp_path):
    """Import the target module fresh."""
    from tests.conftest import import_module_from_repo
    m = import_module_from_repo("ugc_factory", "tools/ugc_factory.py")
    return m


# ============================================================
# create_output_dir
# ============================================================

class TestCreateOutputDir:
    def test_creates_directory(self, mod, tmp_path):
        base = str(tmp_path / "ugc_out")
        result = mod.create_output_dir(base)
        assert result.exists()
        assert result.is_dir()

    def test_timestamp_in_path(self, mod, tmp_path):
        base = str(tmp_path / "ugc_out")
        result = mod.create_output_dir(base)
        # Should have a timestamp directory
        assert len(result.name) > 0

    def test_nested_base_dir(self, mod, tmp_path):
        base = str(tmp_path / "a" / "b" / "c")
        result = mod.create_output_dir(base)
        assert result.exists()


# ============================================================
# generate_avatar
# ============================================================

class TestGenerateAvatar:
    def test_happy_path(self, mod, tmp_path):
        output_path = str(tmp_path / "avatar.png")
        result = mod.generate_avatar("test topic", output_path)
        assert result == output_path

    def test_no_client_raises(self, mod, tmp_path, monkeypatch):
        monkeypatch.setitem(sys.modules, "bootcamp_utils",
                           MagicMock(get_client=MagicMock(return_value=None)))
        # Re-import to pick up mocked bootcamp_utils
        from tests.conftest import import_module_from_repo
        m = import_module_from_repo("ugc_factory", "tools/ugc_factory.py")
        with pytest.raises(EnvironmentError, match="GEMINI_API_KEY"):
            m.generate_avatar("topic", str(tmp_path / "av.png"))

    def test_prompts_file_exists(self, mod, tmp_path, monkeypatch):
        # Create a fake prompts.json
        prompts_dir = tmp_path / "ugc"
        prompts_dir.mkdir()
        prompts_file = prompts_dir / "prompts.json"
        prompts_file.write_text(json.dumps({
            "avatar_prompts": {"default": "test prompt", "custom": "custom prompt"}
        }), encoding="utf-8")

        # Patch Path(__file__).parent to return tmp_path
        output_path = str(tmp_path / "avatar.png")
        with patch("pathlib.Path.__truediv__", side_effect=lambda self, other: prompts_dir / other if other == "prompts.json" else Path.__truediv__(self, other)):
            result = mod.generate_avatar("topic", output_path)
        assert result == output_path

    def test_custom_style(self, mod, tmp_path):
        output_path = str(tmp_path / "avatar.png")
        result = mod.generate_avatar("topic", output_path, style="custom")
        assert result == output_path


# ============================================================
# run_pipeline
# ============================================================

class TestRunPipeline:
    def _make_result(self, video_path="/fake/video.mp4"):
        return _MockVideoResult(video_path=video_path)

    def test_happy_path_tts_engine(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = True
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script text"),
            patch.object(mod, "generate_speech"),
            patch.object(mod, "composite_video"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="fabric", output_dir=output_dir,
            )
        assert result is not None

    def test_no_tts_engine_veo(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = False
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="veo", output_dir=output_dir,
                skip_avatar=True,
            )
        assert result is not None

    def test_no_tts_engine_kling(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = False
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="kling", output_dir=output_dir,
                skip_avatar=True, kling_duration=5,
            )
        assert result is not None

    def test_no_tts_engine_other(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = False
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="other_engine", output_dir=output_dir,
                skip_avatar=True,
            )
        assert result is not None

    def test_existing_avatar_path(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        avatar = tmp_path / "avatar.png"
        avatar.write_bytes(b"fake image")

        mock_engine = MagicMock()
        mock_engine.requires_tts = True
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch.object(mod, "generate_speech"),
            patch.object(mod, "composite_video"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="fabric", output_dir=output_dir,
                avatar_path=str(avatar),
            )
        assert result is not None

    def test_exception_returns_none(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch.object(mod, "generate_ugc_script", side_effect=RuntimeError("API down")):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="fabric", output_dir=output_dir,
                skip_avatar=True,
            )
        assert result is None

    def test_kling_post_audio(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = False
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch.object(mod, "generate_speech"),
            patch.object(mod, "mux_audio"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="kling", output_dir=output_dir,
                skip_avatar=True, post_audio=True,
            )
        assert result is not None

    def test_kling_post_audio_file(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        audio_file = tmp_path / "audio.mp3"
        audio_file.write_bytes(b"fake audio")

        mock_engine = MagicMock()
        mock_engine.requires_tts = False
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch.object(mod, "mux_audio"),
            patch("pathlib.Path.exists", return_value=True),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="kling", output_dir=output_dir,
                skip_avatar=True, post_audio_file=str(audio_file),
            )
        assert result is not None

    def test_kling_post_audio_file_not_found(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = False
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="kling", output_dir=output_dir,
                skip_avatar=True,
                post_audio_file="/nonexistent/audio.mp3",
            )
        # Exception caught -> returns None
        assert result is None

    def test_lipsync_wav2lip(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = True
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch.object(mod, "generate_speech"),
            patch.object(mod, "composite_video"),
            patch.object(mod, "extract_audio"),
            patch.object(mod, "apply_wav2lip"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="fabric", output_dir=output_dir,
                skip_avatar=True, lipsync=True, lipsync_engine="wav2lip",
            )
        assert result is not None

    def test_lipsync_musetalk(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = True
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch.object(mod, "generate_speech"),
            patch.object(mod, "composite_video"),
            patch.object(mod, "apply_musetalk"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="fabric", output_dir=output_dir,
                skip_avatar=True, lipsync=True, lipsync_engine="musetalk",
            )
        assert result is not None

    def test_remove_vocals(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = True
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch.object(mod, "generate_speech"),
            patch.object(mod, "composite_video"),
            patch.object(mod, "remove_vocals_from_video"),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="fabric", output_dir=output_dir,
                skip_avatar=True, remove_vocals=True,
            )
        assert result is not None

    def test_remove_vocals_error(self, mod, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_engine = MagicMock()
        mock_engine.requires_tts = True
        mock_engine.generate.return_value = self._make_result()

        with (
            patch.object(mod, "get_engine", return_value=mock_engine),
            patch.object(mod, "generate_ugc_script", return_value="script"),
            patch.object(mod, "generate_speech"),
            patch.object(mod, "composite_video"),
            patch.object(mod, "remove_vocals_from_video", side_effect=RuntimeError("demucs fail")),
            patch("pathlib.Path.exists", return_value=False),
        ):
            result = mod.run_pipeline(
                topic="test", screenshot_path="/fake/ss.png",
                engine_name="fabric", output_dir=output_dir,
                skip_avatar=True, remove_vocals=True,
            )
        # Should still succeed despite remove_vocals error
        assert result is not None


# ============================================================
# main() CLI
# ============================================================

class TestMain:
    def test_missing_screenshot_exits(self, mod, monkeypatch):
        monkeypatch.setattr("sys.argv", [
            "prog", "--topic", "test", "--screenshot", "/nonexistent/ss.png",
        ])
        with pytest.raises(SystemExit) as exc_info:
            mod.main()
        assert exc_info.value.code == 1

    def test_single_engine(self, mod, monkeypatch, tmp_path):
        ss = tmp_path / "screenshot.png"
        ss.write_bytes(b"fake png")
        monkeypatch.setattr("sys.argv", [
            "prog", "--topic", "test topic",
            "--screenshot", str(ss), "--engine", "fabric",
            "--output-dir", str(tmp_path / "ugc_output"),
        ])
        mock_result = _MockVideoResult()
        with patch.object(mod, "run_pipeline", return_value=mock_result):
            mod.main()

    def test_all_engines(self, mod, monkeypatch, tmp_path):
        ss = tmp_path / "screenshot.png"
        ss.write_bytes(b"fake png")
        monkeypatch.setattr("sys.argv", [
            "prog", "--topic", "test", "--screenshot", str(ss),
            "--engine", "all", "--output-dir", str(tmp_path / "ugc_output"),
        ])
        mock_result = _MockVideoResult()
        with patch.object(mod, "run_pipeline", return_value=mock_result):
            mod.main()

    def test_no_results(self, mod, monkeypatch, tmp_path):
        ss = tmp_path / "screenshot.png"
        ss.write_bytes(b"fake png")
        monkeypatch.setattr("sys.argv", [
            "prog", "--topic", "test", "--screenshot", str(ss),
            "--engine", "fabric", "--output-dir", str(tmp_path / "ugc_output"),
        ])
        with patch.object(mod, "run_pipeline", return_value=None):
            mod.main()

    def test_config_saved(self, mod, monkeypatch, tmp_path):
        ss = tmp_path / "screenshot.png"
        ss.write_bytes(b"fake png")
        monkeypatch.setattr("sys.argv", [
            "prog", "--topic", "my topic", "--screenshot", str(ss),
            "--engine", "fabric", "--output-dir", str(tmp_path / "ugc_output"),
            "--duration", "60", "--voice", "custom_voice",
        ])
        with patch.object(mod, "run_pipeline", return_value=None):
            mod.main()

        # Check config.json was written
        output_dirs = list((tmp_path / "ugc_output").iterdir())
        assert len(output_dirs) == 1
        config_path = output_dirs[0] / "config.json"
        assert config_path.exists()
        config = json.loads(config_path.read_text())
        assert config["topic"] == "my topic"
        assert config["duration"] == 60

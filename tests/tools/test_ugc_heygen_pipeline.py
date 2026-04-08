"""
heygen_pipeline.py のユニットテスト
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_video_result():
    vr = MagicMock()
    vr.video_path = "/tmp/out.mp4"
    vr.duration = 15.0
    vr.cost = 0.25
    return vr


def _edit_image_creates_file(*args, **kwargs):
    """Side effect that creates the output_path file."""
    out = kwargs.get("output_path")
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_bytes(b"\x89PNG_MOCK")
    return True


def _base_mods():
    heygen_engine = MagicMock()
    heygen_engine.generate.return_value = _make_video_result()

    return {
        "runtime_env": MagicMock(),
        "bootcamp_utils": MagicMock(
            get_client=MagicMock(return_value=MagicMock()),
            get_flash_model=MagicMock(return_value="m"),
            get_image_model=MagicMock(return_value="m"),
        ),
        "nanobanana": MagicMock(
            generate_image=MagicMock(), edit_image=MagicMock(side_effect=_edit_image_creates_file),
        ),
        "ugc": MagicMock(),
        "ugc.engines": MagicMock(),
        "ugc.engines.heygen": MagicMock(HeyGenEngine=MagicMock(return_value=heygen_engine)),
        "ugc.tts": MagicMock(generate_speech=MagicMock()),
        "ugc.script_generator": MagicMock(generate_ugc_script=MagicMock(return_value="Hello script")),
        "ugc.engines.longcat": MagicMock(),
    }


def _load(mods=None):
    if mods is None:
        mods = _base_mods()
    sys.modules.update(mods)

    # Load the module with __package__ set to "ugc" so relative imports work
    project_root = Path(__file__).parent.parent.parent
    module_path = project_root / "tools" / "ugc" / "heygen_pipeline.py"
    mod_name = "ugc.heygen_pipeline"

    sys.modules.pop(mod_name, None)
    spec = importlib.util.spec_from_file_location(
        mod_name, module_path,
        submodule_search_locations=[],
    )
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "ugc"
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# generate_avatar_with_screenshot
# ---------------------------------------------------------------------------


class TestGenerateAvatarWithScreenshot:

    def test_no_api_key(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mods = _base_mods()
        mods["bootcamp_utils"] = MagicMock(
            get_client=MagicMock(return_value=None),
            get_flash_model=MagicMock(), get_image_model=MagicMock(),
        )
        mod = _load(mods); mod._bootcamp_utils = None; mod._nanobanana = None
        with pytest.raises(EnvironmentError, match="GEMINI_API_KEY"):
            mod.generate_avatar_with_screenshot(screenshot_path=str(ss))

    def test_screenshot_missing(self):
        mod = _load(); mod._bootcamp_utils = None; mod._nanobanana = None
        with pytest.raises(FileNotFoundError):
            mod.generate_avatar_with_screenshot(screenshot_path="/no/file.png")

    def test_happy_path(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mod = _load(); mod._bootcamp_utils = None; mod._nanobanana = None
        r = mod.generate_avatar_with_screenshot(
            screenshot_path=str(ss), output_path=str(tmp_path / "av.png"))
        assert r == str(tmp_path / "av.png")

    def test_edit_image_failure(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mods = _base_mods()
        mods["nanobanana"] = MagicMock(edit_image=MagicMock(return_value=False), generate_image=MagicMock())
        mod = _load(mods); mod._bootcamp_utils = None; mod._nanobanana = None
        with pytest.raises(RuntimeError, match="画像生成に失敗"):
            mod.generate_avatar_with_screenshot(
                screenshot_path=str(ss), output_path=str(tmp_path / "av.png"))

    def test_custom_style(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mod = _load(); mod._bootcamp_utils = None; mod._nanobanana = None
        r = mod.generate_avatar_with_screenshot(
            screenshot_path=str(ss), avatar_style="robot", output_path=str(tmp_path / "av.png"))
        assert r == str(tmp_path / "av.png")

    def test_default_output(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mod = _load(); mod._bootcamp_utils = None; mod._nanobanana = None
        r = mod.generate_avatar_with_screenshot(screenshot_path=str(ss))
        assert "avatar_" in r


# ---------------------------------------------------------------------------
# generate_heygen_video
# ---------------------------------------------------------------------------


class TestGenerateHeygenVideo:

    def test_avatar_missing(self):
        mod = _load()
        with pytest.raises(FileNotFoundError):
            mod.generate_heygen_video(text="hi", avatar_image="/no/av.png")

    def test_happy_path(self, tmp_path):
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mod = _load()
        r = mod.generate_heygen_video(text="hello", avatar_image=str(av),
                                      output_path=str(tmp_path / "o.mp4"))
        assert r.video_path == "/tmp/out.mp4"

    def test_default_output(self, tmp_path):
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mod = _load()
        r = mod.generate_heygen_video(text="hi", avatar_image=str(av))
        assert r is not None


# ---------------------------------------------------------------------------
# full_pipeline
# ---------------------------------------------------------------------------


class TestFullPipeline:

    def test_happy_path(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mod = _load(); mod._bootcamp_utils = None; mod._nanobanana = None
        r = mod.full_pipeline(topic="AI", screenshot_path=str(ss),
                              output_path=str(tmp_path / "f.mp4"))
        assert r is not None

    def test_skip_avatar(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mod = _load(); mod._bootcamp_utils = None; mod._nanobanana = None
        r = mod.full_pipeline(topic="T", screenshot_path=str(ss),
                              skip_avatar_generation=True, existing_avatar=str(av),
                              output_path=str(tmp_path / "f.mp4"))
        assert r is not None

    def test_default_output(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mod = _load(); mod._bootcamp_utils = None; mod._nanobanana = None
        r = mod.full_pipeline(topic="T", screenshot_path=str(ss))
        assert r is not None


# ---------------------------------------------------------------------------
# Constants / main
# ---------------------------------------------------------------------------


class TestAvatarStyles:
    def test_presets(self):
        mod = _load()
        for k in ["friendly", "professional", "energetic", "casual"]:
            assert k in mod.AVATAR_STYLES


class TestMain:
    def test_no_command(self):
        mod = _load()
        with patch.object(sys, "argv", ["prog"]):
            with pytest.raises(SystemExit):
                mod.main()

    def test_avatar_cmd(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mod = _load(); mod._bootcamp_utils = None; mod._nanobanana = None
        with patch.object(sys, "argv", ["prog", "avatar", "--screenshot", str(ss),
                                        "--output", str(tmp_path / "av.png")]):
            mod.main()

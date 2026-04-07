"""
longcat_pipeline.py のユニットテスト
"""

import importlib.util
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_video_result():
    vr = MagicMock()
    vr.video_path = "/tmp/lc.mp4"
    vr.duration = 10.0
    vr.cost = 0.15
    return vr


def _base_mods():
    lc_inst = MagicMock()
    lc_inst.generate.return_value = _make_video_result()

    return {
        "runtime_env": MagicMock(),
        "nanobanana": MagicMock(generate_image=MagicMock(return_value="ok"),
                                edit_image=MagicMock(return_value=True)),
        "ugc": MagicMock(),
        "ugc.tts": MagicMock(generate_speech=MagicMock()),
        "ugc.engines": MagicMock(),
        "ugc.engines.longcat": MagicMock(LongCatEngine=MagicMock(return_value=lc_inst)),
    }


def _load(mods=None):
    if mods is None:
        mods = _base_mods()
    sys.modules.update(mods)

    project_root = Path(__file__).parent.parent.parent
    module_path = project_root / "tools" / "ugc" / "longcat_pipeline.py"
    mod_name = "ugc.longcat_pipeline"

    sys.modules.pop(mod_name, None)
    spec = importlib.util.spec_from_file_location(
        mod_name, module_path, submodule_search_locations=[],
    )
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "ugc"
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# generate_greenscreen_avatar
# ---------------------------------------------------------------------------


class TestGenerateGreenscreenAvatar:

    def test_happy(self, tmp_path):
        mod = _load(); mod._nanobanana = None
        r = mod.generate_greenscreen_avatar(output_path=str(tmp_path / "av.png"))
        assert r == str(tmp_path / "av.png")

    def test_default_output(self):
        mod = _load(); mod._nanobanana = None
        r = mod.generate_greenscreen_avatar()
        assert "avatar_greenscreen_" in r

    def test_custom_prompt(self, tmp_path):
        mod = _load(); mod._nanobanana = None
        r = mod.generate_greenscreen_avatar(output_path=str(tmp_path / "av.png"),
                                            custom_prompt="robot")
        assert r == str(tmp_path / "av.png")


# ---------------------------------------------------------------------------
# chromakey_composite
# ---------------------------------------------------------------------------


class TestChromakeyComposite:

    def test_happy(self, tmp_path):
        mod = _load()
        with patch("subprocess.run") as mr:
            mr.return_value = MagicMock(returncode=0)
            r = mod.chromakey_composite("/tmp/v.mp4", "/tmp/s.png", str(tmp_path / "o.mp4"))
        assert r == str(tmp_path / "o.mp4")

    def test_ffmpeg_fail(self, tmp_path):
        mod = _load()
        with patch("subprocess.run") as mr:
            mr.side_effect = subprocess.CalledProcessError(1, "ffmpeg", stderr="err")
            with pytest.raises(subprocess.CalledProcessError):
                mod.chromakey_composite("/tmp/v.mp4", "/tmp/s.png", str(tmp_path / "o.mp4"))

    def test_custom_params(self, tmp_path):
        mod = _load()
        with patch("subprocess.run") as mr:
            mr.return_value = MagicMock(returncode=0)
            r = mod.chromakey_composite("/tmp/v.mp4", "/tmp/s.png", str(tmp_path / "o.mp4"),
                                        similarity=0.5, blend=0.2)
        assert r == str(tmp_path / "o.mp4")
        cmd = " ".join(mr.call_args[0][0])
        assert "0.5" in cmd and "0.2" in cmd


# ---------------------------------------------------------------------------
# generate_longcat_video
# ---------------------------------------------------------------------------


class TestGenerateLongcatVideo:

    def test_happy(self, tmp_path):
        mod = _load()
        r = mod.generate_longcat_video("/tmp/av.png", "/tmp/a.mp3", str(tmp_path / "v.mp4"))
        assert r == "/tmp/lc.mp4"

    def test_custom_motion(self, tmp_path):
        mod = _load()
        r = mod.generate_longcat_video("/tmp/av.png", "/tmp/a.mp3", str(tmp_path / "v.mp4"),
                                       motion_prompt="Dancing")
        assert r is not None


# ---------------------------------------------------------------------------
# full_pipeline
# ---------------------------------------------------------------------------


class TestFullPipeline:

    def test_happy(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        out = tmp_path / "out" / "f.mp4"
        mod = _load(); mod._nanobanana = None
        with patch("subprocess.run") as mr:
            mr.return_value = MagicMock(returncode=0)
            r = mod.full_pipeline(text="Hello", screenshot_path=str(ss), output_path=str(out))
        assert r == str(out)

    def test_custom_avatar_prompt(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        out = tmp_path / "out" / "f.mp4"
        mod = _load(); mod._nanobanana = None
        with patch("subprocess.run") as mr:
            mr.return_value = MagicMock(returncode=0)
            r = mod.full_pipeline(text="Hi", screenshot_path=str(ss), output_path=str(out),
                                  avatar_prompt="robot")
        assert r == str(out)


# ---------------------------------------------------------------------------
# quick_generate
# ---------------------------------------------------------------------------


class TestQuickGenerate:

    def test_happy(self, tmp_path):
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mod = _load()
        r = mod.quick_generate(text="Hello", avatar_image=str(av),
                               output_path=str(tmp_path / "q.mp4"))
        assert r == str(tmp_path / "q.mp4")

    def test_custom_voice(self, tmp_path):
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mod = _load()
        r = mod.quick_generate(text="Hi", avatar_image=str(av),
                               output_path=str(tmp_path / "q.mp4"), voice="male")
        assert r == str(tmp_path / "q.mp4")


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


class TestMain:

    def test_no_command(self):
        mod = _load()
        with patch.object(sys, "argv", ["prog"]):
            mod.main()

    def test_quick(self, tmp_path):
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mod = _load()
        with patch.object(sys, "argv", ["p", "quick", "--text", "hi", "--image", str(av),
                                        "--output", str(tmp_path / "o.mp4")]):
            mod.main()

    def test_avatar(self, tmp_path):
        mod = _load(); mod._nanobanana = None
        with patch.object(sys, "argv", ["p", "avatar", "--output", str(tmp_path / "av.png")]):
            mod.main()

    def test_chromakey(self, tmp_path):
        mod = _load()
        with patch.object(sys, "argv", ["p", "chromakey", "--video", "/tmp/v.mp4",
                                        "--screenshot", "/tmp/s.png",
                                        "--output", str(tmp_path / "o.mp4")]):
            with patch("subprocess.run") as mr:
                mr.return_value = MagicMock(returncode=0)
                mod.main()

    def test_full(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mod = _load(); mod._nanobanana = None
        with patch.object(sys, "argv", ["p", "full", "--text", "hi",
                                        "--screenshot", str(ss),
                                        "--output", str(tmp_path / "o.mp4")]):
            with patch("subprocess.run") as mr:
                mr.return_value = MagicMock(returncode=0)
                mod.main()

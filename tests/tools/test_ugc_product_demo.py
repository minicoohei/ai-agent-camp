"""
product_demo_pipeline.py のユニットテスト
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _touch_copy(src, dst, *a, **kw):
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_bytes(b"\x00")


def _make_engine(requires_tts=True):
    e = MagicMock()
    e.requires_tts = requires_tts

    def _gen(**kw):
        out = kw.get("output_path", "")
        if out:
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            Path(out).write_bytes(b"\x00")
        r = MagicMock(); r.cost = 0.10; r.video_path = out; r.duration = 30.0
        return r

    e.generate.side_effect = _gen
    return e


def _touch_output(*args, **kwargs):
    if len(args) >= 2:
        Path(args[1]).parent.mkdir(parents=True, exist_ok=True)
        Path(args[1]).write_bytes(b"\x00")


def _base_mods(engine=None):
    if engine is None:
        engine = _make_engine()
    return {
        "runtime_env": MagicMock(),
        "bootcamp_utils": MagicMock(get_client=MagicMock(return_value=MagicMock())),
        "nanobanana": MagicMock(generate_image=MagicMock()),
        "ugc": MagicMock(
            generate_ugc_script=MagicMock(return_value="Script!"),
            generate_speech=MagicMock(),
            composite_video=MagicMock(),
        ),
        "ugc.engines": MagicMock(get_engine=MagicMock(return_value=engine)),
        "ugc.audio_post": MagicMock(mux_audio=MagicMock(), mix_bgm=MagicMock(side_effect=_touch_output)),
        "ugc.script_generator": MagicMock(),
        "ugc.tts": MagicMock(generate_speech=MagicMock()),
        "ugc.compositor": MagicMock(composite_video=MagicMock()),
    }


def _load(mods):
    sys.modules.update(mods)
    from tests.conftest import import_module_from_repo
    return import_module_from_repo("product_demo_pipeline", "tools/ugc/product_demo_pipeline.py")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRunProductDemo:

    def test_happy_existing_avatar(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     avatar_path=str(av), output_dir=str(tmp_path / "o"))
        assert r["product"] == "App" and "video_path" in r

    def test_auto_avatar(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     output_dir=str(tmp_path / "o"))
        assert r["product"] == "App"

    def test_no_gemini_key(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mods = _base_mods()
        mods["bootcamp_utils"] = MagicMock(get_client=MagicMock(return_value=None))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            with pytest.raises(EnvironmentError, match="GEMINI_API_KEY"):
                mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     output_dir=str(tmp_path / "o"))

    def test_avatar_gen_failure(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        mods = _base_mods()
        mods["nanobanana"] = MagicMock(generate_image=MagicMock(side_effect=RuntimeError("fail")))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            with pytest.raises(RuntimeError, match="アバター画像の生成に失敗"):
                mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     output_dir=str(tmp_path / "o"))

    def test_tts_skipped(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mods = _base_mods(engine=_make_engine(requires_tts=False))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     avatar_path=str(av), output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_composite_failure(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mods = _base_mods()
        mods["ugc"] = MagicMock(
            generate_ugc_script=MagicMock(return_value="S"),
            generate_speech=MagicMock(),
            composite_video=MagicMock(side_effect=RuntimeError("ffmpeg err")),
        )
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     avatar_path=str(av), output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_bgm_added(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        bgm = tmp_path / "b.mp3"; bgm.write_bytes(b"\x00")
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     avatar_path=str(av), bgm_path=str(bgm),
                                     output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_bgm_mix_fail(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        bgm = tmp_path / "b.mp3"; bgm.write_bytes(b"\x00")
        mods = _base_mods()
        mods["ugc.audio_post"] = MagicMock(mux_audio=MagicMock(),
                                           mix_bgm=MagicMock(side_effect=RuntimeError("fail")))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     avatar_path=str(av), bgm_path=str(bgm),
                                     output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_kling_clamp(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        engine = _make_engine()
        mods = _base_mods(engine=engine)
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     avatar_path=str(av), engine_name="kling",
                                     duration=60, output_dir=str(tmp_path / "o"))
        kw = engine.generate.call_args.kwargs
        assert kw["duration"] == 10

    def test_veo_clamp(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        engine = _make_engine()
        mods = _base_mods(engine=engine)
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_product_demo(product="App", screenshot_path=str(ss),
                                     avatar_path=str(av), engine_name="veo",
                                     duration=60, output_dir=str(tmp_path / "o"))
        kw = engine.generate.call_args.kwargs
        assert kw["duration"] == 8


class TestMain:
    def test_main(self, tmp_path):
        ss = tmp_path / "ss.png"; ss.write_bytes(b"\x89PNG")
        av = tmp_path / "av.png"; av.write_bytes(b"\x89PNG")
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            with patch.object(sys, "argv", ["p", "--product", "App", "--screenshot", str(ss),
                                            "--avatar", str(av), "--output-dir", str(tmp_path / "o")]):
                mod.main()

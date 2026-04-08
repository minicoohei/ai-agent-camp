"""
storyboard_anime_pipeline.py のユニットテスト
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _touch_output(*args, **kwargs):
    if len(args) >= 2:
        Path(args[1]).parent.mkdir(parents=True, exist_ok=True)
        Path(args[1]).write_bytes(b"\x00")


def _touch_copy(src, dst, *a, **kw):
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_bytes(b"\x00")


def _engine_generate(**kwargs):
    out = kwargs.get("output_path", "")
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_bytes(b"\x00")
    r = MagicMock(); r.cost = 0.08; r.video_path = out
    return r


def _make_client(text=None):
    c = MagicMock(); resp = MagicMock()
    if text is None:
        text = json.dumps([
            {"scene_number": 1, "description": "forest", "camera": "zoom_in",
             "mood": "calm", "is_key_scene": True},
            {"scene_number": 2, "description": "river", "camera": "pan_left",
             "mood": "dramatic", "is_key_scene": False},
        ])
    resp.text = text
    c.models.generate_content.return_value = resp
    return c


def _base_mods(client=None, engine_side_effect=None):
    if client is None:
        client = _make_client()
    engine = MagicMock()
    engine.generate.side_effect = engine_side_effect or (lambda **kw: _engine_generate(**kw))

    vc = MagicMock()
    vc.concat_simple.side_effect = _touch_output
    vc.concat_with_crossfade.side_effect = _touch_output

    return {
        "runtime_env": MagicMock(),
        "bootcamp_utils": MagicMock(get_client=MagicMock(return_value=client)),
        "nanobanana": MagicMock(generate_image=MagicMock()),
        "ugc": MagicMock(),
        "ugc.engines": MagicMock(get_engine=MagicMock(return_value=engine)),
        "ugc.video_concat": vc,
        "ugc.audio_post": MagicMock(mix_bgm=MagicMock(), mix_bgm_no_audio=MagicMock(side_effect=_touch_output)),
        "ugc.ken_burns": MagicMock(generate_broll=MagicMock(side_effect=_touch_output)),
    }


def _load(mods):
    sys.modules.update(mods)
    from tests.conftest import import_module_from_repo
    return import_module_from_repo("storyboard_anime_pipeline", "tools/ugc/storyboard_anime_pipeline.py")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRunStoryboardAnime:

    def test_no_client(self, tmp_path):
        mods = _base_mods()
        mods["bootcamp_utils"] = MagicMock(get_client=MagicMock(return_value=None))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            with pytest.raises(EnvironmentError, match="GEMINI_API_KEY"):
                mod.run_storyboard_anime(scenario="t", output_dir=str(tmp_path / "o"))

    def test_happy_full(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="girl", num_scenes=2, output_dir=str(tmp_path / "o"))
        assert r["num_scenes"] == 2 and "video_path" in r

    def test_cost_optimize(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=2, cost_optimize=True,
                                         aroll_count=1, output_dir=str(tmp_path / "o"))
        assert r["cost_optimize"] is True and r["broll_count"] == 1

    def test_json_failure(self, tmp_path):
        mods = _base_mods(client=_make_client("BAD"))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=3, output_dir=str(tmp_path / "o"))
        assert r["num_scenes"] == 3

    def test_code_fenced(self, tmp_path):
        d = [{"scene_number": 1, "description": "s", "camera": "static",
              "mood": "calm", "is_key_scene": True}]
        mods = _base_mods(client=_make_client("```json\n" + json.dumps(d) + "\n```"))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=1, output_dir=str(tmp_path / "o"))
        assert r["num_scenes"] == 1

    def test_engine_failure_ken_burns(self, tmp_path):
        def _fail(**kw):
            raise RuntimeError("API err")
        mods = _base_mods(engine_side_effect=_fail)
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=2, output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_bgm_exists(self, tmp_path):
        bgm = tmp_path / "b.mp3"; bgm.write_bytes(b"\x00")
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=2, bgm_path=str(bgm),
                                         output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_bgm_missing(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=2, bgm_path="/no.mp3",
                                         output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_single_clip(self, tmp_path):
        d = [{"scene_number": 1, "description": "s", "camera": "static",
              "mood": "calm", "is_key_scene": True}]
        mods = _base_mods(client=_make_client(json.dumps(d)))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=1, output_dir=str(tmp_path / "o"))
        assert r["num_scenes"] == 1

    def test_crossfade_fail(self, tmp_path):
        mods = _base_mods()
        vc = MagicMock()
        vc.concat_with_crossfade.side_effect = RuntimeError("xfade")
        vc.concat_simple.side_effect = _touch_output
        mods["ugc.video_concat"] = vc
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=2, output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_character_param(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", character="Red girl", num_scenes=2,
                                         output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_bgm_mix_failure(self, tmp_path):
        bgm = tmp_path / "b.mp3"; bgm.write_bytes(b"\x00")
        mods = _base_mods()
        mods["ugc.audio_post"] = MagicMock(
            mix_bgm=MagicMock(), mix_bgm_no_audio=MagicMock(side_effect=RuntimeError("fail")))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_storyboard_anime(scenario="t", num_scenes=2, bgm_path=str(bgm),
                                         output_dir=str(tmp_path / "o"))
        assert "video_path" in r


class TestMain:
    def test_main(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            with patch.object(sys, "argv", ["p", "--scenario", "t", "--num-scenes", "2",
                                            "--output-dir", str(tmp_path / "o")]):
                mod.main()

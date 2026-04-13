"""
mv_pipeline.py のユニットテスト
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
    r = MagicMock()
    r.cost = 0.05
    r.video_path = out
    r.engine = "kling"
    r.duration = 7.5
    return r


def _make_client(text=None):
    c = MagicMock(); resp = MagicMock()
    if text is None:
        text = json.dumps([
            {"scene_number": 1, "description": "field", "mood": "verse",
             "camera": "zoom_in", "is_key_scene": True, "visual_type": "narrative"},
            {"scene_number": 2, "description": "ocean", "mood": "chorus",
             "camera": "pan_left", "is_key_scene": False, "visual_type": "landscape"},
        ])
    resp.text = text
    c.models.generate_content.return_value = resp
    return c


def _base_mods(client=None):
    if client is None:
        client = _make_client()
    engine = MagicMock()
    engine.generate.side_effect = lambda **kw: _engine_generate(**kw)

    music_result = MagicMock(audio_path="/tmp/m.mp3", cost=0.50, lyrics="la")
    suno = MagicMock(); suno.generate_music.return_value = music_result

    analysis = MagicMock(tempo=120.0, beat_times=[0.5, 1.0], sections=["A"])
    ti = MagicMock(duration=7.5)
    beat = MagicMock()
    beat.analyze_beats.return_value = analysis
    beat.generate_beat_timeline.return_value = [ti, ti]
    beat.save_analysis = MagicMock(); beat.save_timeline = MagicMock()

    vc = MagicMock()
    vc.concat_simple.side_effect = _touch_output
    vc.concat_with_crossfade.side_effect = _touch_output

    return {
        "runtime_env": MagicMock(),
        "bootcamp_utils": MagicMock(get_client=MagicMock(return_value=client)),
        "nanobanana": MagicMock(generate_image=MagicMock()),
        "ugc": MagicMock(),
        "ugc.engines.suno": suno,
        "ugc.engines": MagicMock(
            get_engine=MagicMock(return_value=engine),
            generate_with_fallback=MagicMock(side_effect=lambda **kw: _engine_generate(**kw)),
        ),
        "ugc.ken_burns": MagicMock(generate_broll=MagicMock(side_effect=_touch_output)),
        "ugc.beat_sync": beat,
        "ugc.video_concat": vc,
        "ugc.audio_post": MagicMock(mix_bgm_no_audio=MagicMock(side_effect=_touch_output)),
        "ugc.video_qa": MagicMock(validate_video_output=MagicMock(return_value={"status": "PASS", "issues": []})),
        "ugc.narration_qa": MagicMock(qa_and_retry=MagicMock(return_value="/tmp/audio.mp3")),
    }


def _load(mods):
    sys.modules.update(mods)
    from tests.conftest import import_module_from_repo
    return import_module_from_repo("mv_pipeline", "tools/ugc/mv_pipeline.py")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRunMvPipeline:

    def test_raises_without_prompt_or_music(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            with pytest.raises(ValueError, match="--prompt または --music"):
                mod.run_mv_pipeline(prompt=None, music_path=None, output_dir=str(tmp_path / "o"))

    def test_raises_without_gemini_key(self, tmp_path):
        mods = _base_mods()
        mods["bootcamp_utils"] = MagicMock(get_client=MagicMock(return_value=None))
        with patch.dict(sys.modules, mods):
            mod = _load(mods)
            with pytest.raises(EnvironmentError, match="GEMINI_API_KEY"):
                mod.run_mv_pipeline(prompt="test", output_dir=str(tmp_path / "o"))

    def test_happy_path_with_prompt(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(prompt="pop", num_scenes=2, output_dir=str(tmp_path / "o"))
        assert r["num_scenes"] == 2
        assert "video_path" in r

    def test_existing_music(self, tmp_path):
        mf = tmp_path / "s.mp3"; mf.write_bytes(b"\x00" * 10)
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(music_path=str(mf), num_scenes=2, output_dir=str(tmp_path / "o"))
        assert r["music_path"] is not None

    def test_cost_optimize(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(prompt="t", num_scenes=2, cost_optimize=True, aroll_count=1,
                                    output_dir=str(tmp_path / "o"))
        assert r["cost_optimize"] is True

    def test_json_parse_failure(self, tmp_path):
        mods = _base_mods(client=_make_client("BAD"))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(prompt="t", num_scenes=3, output_dir=str(tmp_path / "o"))
        assert r["num_scenes"] == 3

    def test_code_fenced(self, tmp_path):
        d = [{"scene_number": 1, "description": "s", "mood": "verse",
              "camera": "static", "is_key_scene": True, "visual_type": "narrative"}]
        mods = _base_mods(client=_make_client("```json\n" + json.dumps(d) + "\n```"))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(prompt="t", num_scenes=1, output_dir=str(tmp_path / "o"))
        assert r["num_scenes"] == 1

    def test_music_gen_failure(self, tmp_path):
        mods = _base_mods()
        mods["ugc.engines.suno"] = MagicMock(generate_music=MagicMock(side_effect=RuntimeError("fail")))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(prompt="t", num_scenes=2, output_dir=str(tmp_path / "o"))
        assert r["music_path"] is None

    def test_beat_import_error(self, tmp_path):
        mods = _base_mods()
        mods["ugc.beat_sync"] = MagicMock(analyze_beats=MagicMock(side_effect=ImportError("no librosa")))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(prompt="t", num_scenes=2, output_dir=str(tmp_path / "o"))
        assert "video_path" in r

    def test_single_clip(self, tmp_path):
        d = [{"scene_number": 1, "description": "s", "mood": "verse",
              "camera": "static", "is_key_scene": True, "visual_type": "narrative"}]
        mods = _base_mods(client=_make_client(json.dumps(d)))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(prompt="t", num_scenes=1, output_dir=str(tmp_path / "o"))
        assert r["num_scenes"] == 1

    def test_crossfade_failure_fallback(self, tmp_path):
        mods = _base_mods()
        vc = MagicMock()
        vc.concat_with_crossfade.side_effect = RuntimeError("xfade fail")
        vc.concat_simple.side_effect = _touch_output
        mods["ugc.video_concat"] = vc
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_mv_pipeline(prompt="t", num_scenes=2, output_dir=str(tmp_path / "o"))
        assert "video_path" in r


class TestMain:
    def test_main(self, tmp_path):
        mods = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            with patch.object(sys, "argv", ["p", "--prompt", "t", "--num-scenes", "2",
                                            "--output-dir", str(tmp_path / "o")]):
                mod.main()

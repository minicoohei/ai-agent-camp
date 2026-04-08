"""
slide_narration_pipeline.py のユニットテスト
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers – make mocked functions create real files
# ---------------------------------------------------------------------------

def _touch_output(*args, **kwargs):
    """Side effect that creates the output file (2nd positional arg)."""
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
    r.cost = 0.10
    r.video_path = out
    return r


def _make_mock_client(text=None):
    client = MagicMock()
    resp = MagicMock()
    if text is None:
        text = json.dumps([
            {"section_title": "Intro", "narration": "Hello", "duration": 30, "visual_notes": ""}
        ])
    resp.text = text
    client.models.generate_content.return_value = resp
    return client


def _base_mods(client=None):
    if client is None:
        client = _make_mock_client()
    engine = MagicMock()
    engine.generate.side_effect = lambda **kw: _engine_generate(**kw)

    concat_mod = MagicMock()
    concat_mod.concat_simple.side_effect = _touch_output
    concat_mod.concat_with_crossfade.side_effect = _touch_output

    return {
        "runtime_env": MagicMock(),
        "bootcamp_utils": MagicMock(get_client=MagicMock(return_value=client)),
        "nanobanana": MagicMock(generate_image=MagicMock()),
        "ugc": MagicMock(),
        "ugc.tts": MagicMock(generate_speech=MagicMock()),
        "ugc.engines": MagicMock(get_engine=MagicMock(return_value=engine)),
        "ugc.video_concat": concat_mod,
        "ugc.ken_burns": MagicMock(generate_broll=MagicMock(side_effect=_touch_output)),
        "ugc.audio_post": MagicMock(mix_bgm=MagicMock(side_effect=_touch_output)),
        "html_parser": MagicMock(),
        "script_generator": MagicMock(),
    }, client, engine


def _load(mods):
    sys.modules.update(mods)
    from tests.conftest import import_module_from_repo
    return import_module_from_repo(
        "slide_narration_pipeline", "tools/ugc/slide_narration_pipeline.py",
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRunSlideNarration:

    def test_raises_when_no_html_or_slides(self, tmp_path):
        mods, _, _ = _base_mods()
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            with pytest.raises(ValueError, match="--html または --slides"):
                mod.run_slide_narration(html_path=None, slides_dir=None, output_dir=str(tmp_path / "o"))

    def test_script_only_with_slides(self, tmp_path):
        sd = tmp_path / "slides"; sd.mkdir()
        (sd / "s1.png").write_bytes(b"\x89PNG")

        mods, _, _ = _base_mods()
        with patch.dict(sys.modules, mods):
            mod = _load(mods)
            r = mod.run_slide_narration(slides_dir=str(sd), script_only=True, output_dir=str(tmp_path / "o"))
        assert "script_path" in r
        assert r["segments"] == 1

    def test_happy_path_slides_no_llm(self, tmp_path):
        sd = tmp_path / "slides"; sd.mkdir()
        (sd / "s1.png").write_bytes(b"\x89PNG")

        seg = MagicMock(section_title="S1", narration="Hi", duration=30, visual_notes="")
        sg = MagicMock(); sg.generate_script.return_value = MagicMock(segments=[seg])

        mods, _, _ = _base_mods()
        mods["script_generator"] = sg
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_slide_narration(slides_dir=str(sd), use_llm=False, output_dir=str(tmp_path / "o"))
        assert r["segments"] == 1
        assert "video_path" in r

    def test_happy_path_html_llm(self, tmp_path):
        html = tmp_path / "t.html"; html.write_text("<html></html>")
        hp = MagicMock()
        hp.parse_html.return_value = "c"
        hp.content_to_dict.return_value = {"title": "T", "sections": [{"title": "s", "text": "t", "duration": 30}]}

        mods, _, _ = _base_mods()
        mods["html_parser"] = hp
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_slide_narration(html_path=str(html), use_llm=True, output_dir=str(tmp_path / "o"))
        assert r["topic"] == "T"

    def test_llm_json_failure_fallback(self, tmp_path):
        sd = tmp_path / "slides"; sd.mkdir()
        (sd / "s1.png").write_bytes(b"\x89PNG")
        mods, _, _ = _base_mods(client=_make_mock_client("NOT JSON"))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_slide_narration(slides_dir=str(sd), use_llm=True, output_dir=str(tmp_path / "o"))
        assert r["segments"] == 1

    def test_code_fenced_response(self, tmp_path):
        sd = tmp_path / "slides"; sd.mkdir()
        (sd / "s1.png").write_bytes(b"\x89PNG")
        data = [{"section_title": "T", "narration": "N", "duration": 20, "visual_notes": ""}]
        fenced = "```json\n" + json.dumps(data) + "\n```"
        mods, _, _ = _base_mods(client=_make_mock_client(fenced))
        with patch.dict(sys.modules, mods):
            mod = _load(mods)
            r = mod.run_slide_narration(slides_dir=str(sd), script_only=True, output_dir=str(tmp_path / "o"))
        assert r["segments"] == 1

    def test_empty_slides_dir(self, tmp_path):
        sd = tmp_path / "slides"; sd.mkdir()
        mods, _, _ = _base_mods()
        with patch.dict(sys.modules, mods):
            mod = _load(mods)
            r = mod.run_slide_narration(slides_dir=str(sd), script_only=True, output_dir=str(tmp_path / "o"))
        assert r["segments"] == 1

    def test_tts_failure_continues(self, tmp_path):
        sd = tmp_path / "slides"; sd.mkdir()
        (sd / "s1.png").write_bytes(b"\x89PNG")
        mods, _, _ = _base_mods()
        mods["ugc.tts"] = MagicMock(generate_speech=MagicMock(side_effect=RuntimeError("TTS down")))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_slide_narration(slides_dir=str(sd), output_dir=str(tmp_path / "o"))
        assert "steps" in r

    def test_avatar_failure(self, tmp_path):
        sd = tmp_path / "slides"; sd.mkdir()
        (sd / "s1.png").write_bytes(b"\x89PNG")
        mods, _, _ = _base_mods()
        mods["nanobanana"] = MagicMock(generate_image=MagicMock(side_effect=RuntimeError("fail")))
        with patch.dict(sys.modules, mods), patch("shutil.copy2", side_effect=_touch_copy):
            mod = _load(mods)
            r = mod.run_slide_narration(slides_dir=str(sd), output_dir=str(tmp_path / "o"))
        assert r["presenter_clips"] == 0


class TestMain:
    def test_main_calls_run(self, tmp_path):
        sd = tmp_path / "slides"; sd.mkdir()
        (sd / "s1.png").write_bytes(b"\x89PNG")
        mods, _, _ = _base_mods()
        with patch.dict(sys.modules, mods):
            mod = _load(mods)
            with patch.object(sys, "argv", [
                "prog", "--slides", str(sd), "--script-only", "--output-dir", str(tmp_path / "o"),
            ]):
                mod.main()

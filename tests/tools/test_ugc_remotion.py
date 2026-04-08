"""tools/ugc/remotion_render.py の単体テスト"""
import json
import subprocess
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from tests.conftest import import_module_from_repo


@pytest.fixture
def remotion():
    mod = import_module_from_repo("remotion_render", "tools/ugc/remotion_render.py")
    yield mod


class TestTemplates:
    def test_all_templates_defined(self, remotion):
        expected = ["short", "quote", "summary", "blog", "training", "square"]
        for name in expected:
            assert name in remotion.TEMPLATES

    def test_template_fields(self, remotion):
        for name, tmpl in remotion.TEMPLATES.items():
            assert "composition" in tmpl
            assert "width" in tmpl
            assert "height" in tmpl
            assert "fps" in tmpl
            assert "description" in tmpl


class TestRenderVideo:
    def test_invalid_template_raises(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        input_json.write_text('{"clips": [], "session_dir": "/tmp/sess"}')
        with pytest.raises(ValueError, match="未対応"):
            remotion.render_video(input_json, "nonexistent_template")

    def test_missing_clip_id_raises(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        data = {"clips": [{"clip_id": "clip_01"}], "session_dir": str(tmp_path)}
        input_json.write_text(json.dumps(data))
        with pytest.raises(ValueError, match="clip_id"):
            remotion.render_video(input_json, "short", clip_id="nonexistent")

    def test_successful_render(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        data = {"clips": [{"clip_id": "c1"}], "session_dir": str(tmp_path)}
        input_json.write_text(json.dumps(data))
        output = tmp_path / "out.mp4"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = remotion.render_video(input_json, "short", output_path=output)
        assert result == output

    def test_render_fallback_to_ffmpeg(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        clip_path = tmp_path / "clip.mp4"
        clip_path.write_bytes(b"fakevideo")
        data = {
            "clips": [{"clip_id": "c1", "clip_path": str(clip_path), "summary": {"title": "Test"}}],
            "session_dir": str(tmp_path),
        }
        input_json.write_text(json.dumps(data))
        output = tmp_path / "out.mp4"

        # First call (remotion) fails, second call (ffmpeg fallback) succeeds
        def side_effect(*args, **kwargs):
            cmd = args[0] if args else kwargs.get("args", [])
            if "remotion" in str(cmd):
                return MagicMock(returncode=1, stderr="remotion not found")
            return MagicMock(returncode=0)

        with patch("subprocess.run", side_effect=side_effect):
            result = remotion.render_video(input_json, "short", output_path=output)
        assert result == output

    def test_auto_output_path(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        data = {"clips": [{"clip_id": "c1"}], "session_dir": str(tmp_path)}
        input_json.write_text(json.dumps(data))

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = remotion.render_video(input_json, "short")
        assert "marketing" in str(result)
        assert "short.mp4" in str(result)

    def test_clip_id_filter(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        data = {
            "clips": [
                {"clip_id": "c1", "text": "first"},
                {"clip_id": "c2", "text": "second"},
            ],
            "session_dir": str(tmp_path),
        }
        input_json.write_text(json.dumps(data))
        output = tmp_path / "out.mp4"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = remotion.render_video(input_json, "short", output_path=output, clip_id="c1")
        assert result == output

    def test_props_file_cleaned_up(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        data = {"clips": [], "session_dir": str(tmp_path)}
        input_json.write_text(json.dumps(data))
        output = tmp_path / "out.mp4"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            remotion.render_video(input_json, "short", output_path=output)
        # Props temp file should be cleaned up
        props_files = list(tmp_path.glob("_remotion_props_*.json"))
        assert len(props_files) == 0


class TestFfmpegFallback:
    def test_no_clips_raises(self, remotion):
        data = {"clips": []}
        tmpl = {"width": 1920, "height": 1080}
        with pytest.raises(RuntimeError, match="クリップ"):
            remotion.ffmpeg_fallback(data, "short", Path("/out.mp4"), tmpl)

    def test_missing_clip_file_raises(self, remotion):
        data = {"clips": [{"clip_path": "/nonexistent/clip.mp4", "summary": {}}]}
        tmpl = {"width": 1920, "height": 1080}
        with pytest.raises(FileNotFoundError):
            remotion.ffmpeg_fallback(data, "short", Path("/out.mp4"), tmpl)

    def test_ffmpeg_timeout_raises(self, remotion, tmp_path):
        clip_file = tmp_path / "clip.mp4"
        clip_file.write_bytes(b"fakevideo")
        data = {"clips": [{"clip_path": str(clip_file), "summary": {"title": "Test"}}]}
        tmpl = {"width": 1920, "height": 1080}

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("ffmpeg", 300)):
            with pytest.raises(RuntimeError, match="タイムアウト"):
                remotion.ffmpeg_fallback(data, "short", tmp_path / "out.mp4", tmpl)

    def test_ffmpeg_failure_raises(self, remotion, tmp_path):
        clip_file = tmp_path / "clip.mp4"
        clip_file.write_bytes(b"fake")
        data = {"clips": [{"clip_path": str(clip_file), "summary": {"title": "T"}}]}
        tmpl = {"width": 1920, "height": 1080}

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="encoding error")
            with pytest.raises(RuntimeError, match="FFmpegフォールバック失敗"):
                remotion.ffmpeg_fallback(data, "short", tmp_path / "out.mp4", tmpl)

    def test_no_title_no_drawtext(self, remotion, tmp_path):
        clip_file = tmp_path / "clip.mp4"
        clip_file.write_bytes(b"fake")
        data = {"clips": [{"clip_path": str(clip_file), "summary": {}}]}
        tmpl = {"width": 1920, "height": 1080}

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            remotion.ffmpeg_fallback(data, "short", tmp_path / "out.mp4", tmpl)
        cmd = mock_run.call_args[0][0]
        vf_idx = cmd.index("-vf")
        filter_str = cmd[vf_idx + 1]
        assert "drawtext" not in filter_str


class TestBatchRender:
    def test_batch_multiple_templates(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        data = {"clips": [], "session_dir": str(tmp_path)}
        input_json.write_text(json.dumps(data))

        with patch.object(remotion, "render_video") as mock_render:
            mock_render.return_value = tmp_path / "out.mp4"
            results = remotion.batch_render(input_json, ["short", "quote"])
        assert len(results) == 2
        assert all(r["status"] == "ok" for r in results)

    def test_batch_handles_errors(self, remotion, tmp_path):
        input_json = tmp_path / "input.json"
        data = {"clips": [], "session_dir": str(tmp_path)}
        input_json.write_text(json.dumps(data))

        with patch.object(remotion, "render_video", side_effect=ValueError("bad")):
            results = remotion.batch_render(input_json, ["short"])
        assert len(results) == 1
        assert results[0]["status"] == "error"
        assert "bad" in results[0]["error"]

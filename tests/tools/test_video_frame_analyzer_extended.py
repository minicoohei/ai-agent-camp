"""video_frame_analyzer.py の拡張テスト - カバレッジ向上"""
import json
import subprocess
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from tests.conftest import import_module_from_repo


@pytest.fixture
def vfa():
    """video_frame_analyzerをインポート"""
    with patch.dict("sys.modules", {
        "google": MagicMock(),
        "google.genai": MagicMock(),
    }):
        mod = import_module_from_repo("video_frame_analyzer", "tools/video_frame_analyzer.py")
        yield mod


class TestSampleIndicesExtended:
    def test_negative_max_returns_all(self, vfa):
        result = vfa.sample_indices(5, -1)
        assert result == [0, 1, 2, 3, 4]

    def test_single_total(self, vfa):
        result = vfa.sample_indices(1, 1)
        assert result == [0]

    def test_large_max_with_small_total(self, vfa):
        result = vfa.sample_indices(2, 10)
        assert result == [0, 1]

    def test_filler_needed(self, vfa):
        # When rounding creates duplicates, filler indices should be added
        result = vfa.sample_indices(5, 4)
        assert len(result) == 4
        assert all(0 <= i < 5 for i in result)
        assert result == sorted(result)

    def test_max_equals_total(self, vfa):
        result = vfa.sample_indices(3, 3)
        assert result == [0, 1, 2]

    def test_no_duplicates(self, vfa):
        result = vfa.sample_indices(20, 5)
        assert len(result) == len(set(result))

    def test_sorted_output(self, vfa):
        result = vfa.sample_indices(100, 10)
        assert result == sorted(result)


class TestParseJsonFromText:
    def test_valid_json(self, vfa):
        text = '{"summary": "test", "notable_elements": [], "potential_issues": [], "ui_changes": []}'
        result = vfa.parse_json_from_text(text)
        assert result["summary"] == "test"

    def test_json_in_code_block(self, vfa):
        text = '```json\n{"summary": "from block"}\n```'
        result = vfa.parse_json_from_text(text)
        assert result["summary"] == "from block"

    def test_invalid_json_returns_fallback(self, vfa):
        text = "This is not JSON at all, just plain text analysis"
        result = vfa.parse_json_from_text(text)
        assert "summary" in result
        assert result["notable_elements"] == []
        assert result["potential_issues"] == []
        assert result["ui_changes"] == []

    def test_empty_string(self, vfa):
        result = vfa.parse_json_from_text("")
        assert "summary" in result

    def test_long_text_truncated_in_summary(self, vfa):
        text = "A" * 1000
        result = vfa.parse_json_from_text(text)
        assert len(result["summary"]) <= 500

    def test_unicode_content(self, vfa):
        text = '{"summary": "analysis with special chars"}'
        result = vfa.parse_json_from_text(text)
        assert "special chars" in result["summary"]


class TestRunKeyframeExtraction:
    def test_successful_extraction(self, vfa, tmp_path):
        expected = {"files": ["f1.png", "f2.png"], "count": 2}
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout=json.dumps(expected),
                stderr="",
            )
            result = vfa.run_keyframe_extraction(
                video_path="video.mp4",
                output_dir=str(tmp_path),
                threshold=0.85,
                quality=30,
                scale=0.3,
            )
        assert result["files"] == ["f1.png", "f2.png"]

    def test_extraction_failure(self, vfa):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="extraction failed",
            )
            result = vfa.run_keyframe_extraction("v.mp4", None, 0.85, 30, 0.3)
        assert "error" in result

    def test_invalid_json_output(self, vfa):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="not json",
                stderr="",
            )
            result = vfa.run_keyframe_extraction("v.mp4", None, 0.85, 30, 0.3)
        assert "error" in result

    def test_empty_stderr_on_failure(self, vfa):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="",
            )
            result = vfa.run_keyframe_extraction("v.mp4", None, 0.85, 30, 0.3)
        assert "error" in result
        assert "キーフレーム抽出に失敗" in result["error"]

    def test_no_output_dir(self, vfa):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout='{"files": []}', stderr=""
            )
            result = vfa.run_keyframe_extraction("v.mp4", None, 0.85, 30, 0.3)
        # Check that -o flag is NOT in command when output_dir is None/empty
        cmd = mock_run.call_args[0][0]
        assert "-o" not in cmd

    def test_with_output_dir(self, vfa, tmp_path):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout='{"files": []}', stderr=""
            )
            result = vfa.run_keyframe_extraction("v.mp4", str(tmp_path), 0.85, 30, 0.3)
        cmd = mock_run.call_args[0][0]
        assert "-o" in cmd


class TestAnalyzeFrame:
    def test_analyzes_frame(self, vfa, tmp_path):
        from PIL import Image
        img = Image.new("RGB", (10, 10), color="blue")
        img_path = tmp_path / "frame.png"
        img.save(img_path)

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"summary": "blue frame", "notable_elements": [], "potential_issues": [], "ui_changes": []}'
        mock_client.models.generate_content.return_value = mock_response

        with patch("video_frame_analyzer.get_flash_model", return_value="test-model"):
            result = vfa.analyze_frame(mock_client, img_path, "describe this frame")
        assert result["summary"] == "blue frame"


class TestSummarizeResults:
    def test_summarizes(self, vfa):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"overall_summary": "test summary", "notable_changes": [], "issues": [], "recommendations": []}'
        mock_client.models.generate_content.return_value = mock_response

        frame_results = [
            {"frame_index": 0, "analysis": {"summary": "frame 0"}},
        ]
        with patch("video_frame_analyzer.get_flash_model", return_value="test-model"):
            result = vfa.summarize_results(mock_client, "test intent", frame_results)
        assert result["overall_summary"] == "test summary"

    def test_summarize_with_json_code_block(self, vfa):
        """レスポンスが ```json``` で囲まれている場合"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        inner = '{"overall_summary": "block", "notable_changes": [], "issues": [], "recommendations": []}'
        mock_response.text = f"```json\n{inner}\n```"
        mock_client.models.generate_content.return_value = mock_response

        with patch("video_frame_analyzer.get_flash_model", return_value="test-model"):
            result = vfa.summarize_results(mock_client, "intent", [])
        assert result["overall_summary"] == "block"

    def test_summarize_invalid_json(self, vfa):
        """不正なJSON のフォールバック"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "not valid json at all"
        mock_client.models.generate_content.return_value = mock_response

        with patch("video_frame_analyzer.get_flash_model", return_value="test-model"):
            result = vfa.summarize_results(mock_client, "intent", [])
        assert "summary" in result


class TestAnalyzeFrameExtended:
    """analyze_frame の追加テスト (lines 107-123)"""

    def test_analyze_frame_json_in_code_block(self, vfa, tmp_path):
        from PIL import Image
        img = Image.new("RGB", (10, 10), color="red")
        img_path = tmp_path / "frame.png"
        img.save(img_path)

        mock_client = MagicMock()
        inner = '{"summary": "red frame", "notable_elements": ["red"], "potential_issues": [], "ui_changes": []}'
        mock_response = MagicMock()
        mock_response.text = f"```json\n{inner}\n```"
        mock_client.models.generate_content.return_value = mock_response

        with patch("video_frame_analyzer.get_flash_model", return_value="test-model"):
            result = vfa.analyze_frame(mock_client, img_path, "describe")
        assert result["summary"] == "red frame"

    def test_analyze_frame_invalid_json(self, vfa, tmp_path):
        from PIL import Image
        img = Image.new("RGB", (10, 10), color="green")
        img_path = tmp_path / "frame.png"
        img.save(img_path)

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is plain text analysis, not JSON"
        mock_client.models.generate_content.return_value = mock_response

        with patch("video_frame_analyzer.get_flash_model", return_value="test-model"):
            result = vfa.analyze_frame(mock_client, img_path, "analyze")
        assert "summary" in result
        assert result["notable_elements"] == []


class TestMainFunction:
    """main() 関数のテスト (lines 152-225)"""

    def test_main_video_not_found(self, vfa, tmp_path, capsys):
        """動画ファイルが存在しない場合"""
        with patch("sys.argv", ["cmd", str(tmp_path / "nonexistent.mp4")]):
            with pytest.raises(SystemExit) as exc_info:
                vfa.main()
        assert exc_info.value.code == 1

    def test_main_extraction_error(self, vfa, tmp_path, capsys):
        """キーフレーム抽出がエラーの場合"""
        vid = tmp_path / "video.mp4"
        vid.write_bytes(b"fake video")

        with patch("sys.argv", ["cmd", str(vid)]):
            with patch.object(vfa, "run_keyframe_extraction", return_value={"error": "extraction failed"}):
                with pytest.raises(SystemExit) as exc_info:
                    vfa.main()
        assert exc_info.value.code == 1

    def test_main_no_analyze_mode(self, vfa, tmp_path, capsys):
        """--no-analyze モード"""
        vid = tmp_path / "video.mp4"
        vid.write_bytes(b"fake video")

        with patch("sys.argv", ["cmd", str(vid), "--no-analyze"]):
            with patch.object(vfa, "run_keyframe_extraction", return_value={"files": ["f1.png"]}):
                vfa.main()
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "extraction" in output

    def test_main_no_client(self, vfa, tmp_path, capsys):
        """Gemini API クライアントがない場合"""
        vid = tmp_path / "video.mp4"
        vid.write_bytes(b"fake video")

        with patch("sys.argv", ["cmd", str(vid)]):
            with patch.object(vfa, "run_keyframe_extraction", return_value={"files": ["f1.png"]}):
                with patch.object(vfa, "get_client", return_value=None):
                    with pytest.raises(SystemExit) as exc_info:
                        vfa.main()
        assert exc_info.value.code == 1

    def test_main_no_frame_files(self, vfa, tmp_path, capsys):
        """抽出フレームが空の場合"""
        vid = tmp_path / "video.mp4"
        vid.write_bytes(b"fake video")

        mock_client = MagicMock()

        with patch("sys.argv", ["cmd", str(vid)]):
            with patch.object(vfa, "run_keyframe_extraction", return_value={"files": []}):
                with patch.object(vfa, "get_client", return_value=mock_client):
                    with pytest.raises(SystemExit) as exc_info:
                        vfa.main()
        assert exc_info.value.code == 1

    def test_main_full_analysis(self, vfa, tmp_path, capsys):
        """完全な解析パイプライン"""
        vid = tmp_path / "video.mp4"
        vid.write_bytes(b"fake video")

        # Create dummy frame files
        frame1 = tmp_path / "frame1.png"
        frame2 = tmp_path / "frame2.png"
        from PIL import Image
        img = Image.new("RGB", (10, 10), "blue")
        img.save(frame1)
        img.save(frame2)

        mock_client = MagicMock()
        analyze_resp = MagicMock()
        analyze_resp.text = '{"summary": "test", "notable_elements": [], "potential_issues": [], "ui_changes": []}'
        summary_resp = MagicMock()
        summary_resp.text = '{"overall_summary": "all good", "notable_changes": [], "issues": [], "recommendations": []}'
        mock_client.models.generate_content.side_effect = [analyze_resp, analyze_resp, summary_resp]

        with patch("sys.argv", ["cmd", str(vid), "--max-frames", "2"]):
            with patch.object(vfa, "run_keyframe_extraction", return_value={"files": [str(frame1), str(frame2)]}):
                with patch.object(vfa, "get_client", return_value=mock_client):
                    with patch.object(vfa, "get_flash_model", return_value="test-model"):
                        vfa.main()

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "analysis" in output
        assert "summary" in output
        assert output["analysis"]["frame_count_analyzed"] == 2

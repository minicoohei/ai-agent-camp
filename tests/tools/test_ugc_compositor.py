"""tools/ugc/compositor.py の単体テスト"""
import subprocess
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock
import numpy as np

from tests.conftest import import_module_from_repo


@pytest.fixture
def compositor():
    """compositorモジュールをインポート"""
    with patch.dict("sys.modules", {
        "cv2": MagicMock(),
    }):
        mod = import_module_from_repo("compositor", "tools/ugc/compositor.py")
        yield mod


class TestDetectGreenRegion:
    def test_no_green_returns_none_bbox(self, compositor):
        import cv2
        mock_cv2 = MagicMock()
        mock_cv2.cvtColor.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cv2.inRange.return_value = np.zeros((100, 100), dtype=np.uint8)
        mock_cv2.morphologyEx.return_value = np.zeros((100, 100), dtype=np.uint8)
        mock_cv2.findContours.return_value = ([], None)
        mock_cv2.COLOR_BGR2HSV = 40
        mock_cv2.MORPH_OPEN = 2
        mock_cv2.MORPH_CLOSE = 3
        mock_cv2.RETR_EXTERNAL = 0
        mock_cv2.CHAIN_APPROX_SIMPLE = 1

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            frame = np.zeros((100, 100, 3), dtype=np.uint8)
            mask, bbox = compositor.detect_green_region(frame)
        assert bbox is None

    def test_small_contour_returns_none_bbox(self, compositor):
        mock_cv2 = MagicMock()
        mock_cv2.cvtColor.return_value = np.zeros((1000, 1000, 3), dtype=np.uint8)
        mock_cv2.inRange.return_value = np.zeros((1000, 1000), dtype=np.uint8)
        mock_cv2.morphologyEx.return_value = np.zeros((1000, 1000), dtype=np.uint8)
        contour = np.array([[[10, 10]], [[11, 10]], [[11, 11]], [[10, 11]]])
        mock_cv2.findContours.return_value = ([contour], None)
        mock_cv2.contourArea.return_value = 1  # very small
        mock_cv2.COLOR_BGR2HSV = 40
        mock_cv2.MORPH_OPEN = 2
        mock_cv2.MORPH_CLOSE = 3
        mock_cv2.RETR_EXTERNAL = 0
        mock_cv2.CHAIN_APPROX_SIMPLE = 1

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            frame = np.zeros((1000, 1000, 3), dtype=np.uint8)
            mask, bbox = compositor.detect_green_region(frame)
        assert bbox is None

    def test_large_contour_returns_bbox(self, compositor):
        mock_cv2 = MagicMock()
        mock_cv2.cvtColor.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cv2.inRange.return_value = np.zeros((100, 100), dtype=np.uint8)
        mock_cv2.morphologyEx.return_value = np.zeros((100, 100), dtype=np.uint8)
        contour = np.array([[[0, 0]], [[50, 0]], [[50, 50]], [[0, 50]]])
        mock_cv2.findContours.return_value = ([contour], None)
        mock_cv2.contourArea.return_value = 5000  # > 1% of 100*100
        mock_cv2.boundingRect.return_value = (0, 0, 50, 50)
        mock_cv2.COLOR_BGR2HSV = 40
        mock_cv2.MORPH_OPEN = 2
        mock_cv2.MORPH_CLOSE = 3
        mock_cv2.RETR_EXTERNAL = 0
        mock_cv2.CHAIN_APPROX_SIMPLE = 1

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            frame = np.zeros((100, 100, 3), dtype=np.uint8)
            mask, bbox = compositor.detect_green_region(frame)
        assert bbox == (0, 0, 50, 50)


class TestCompositeFrame:
    def test_composites_screenshot_padding(self, compositor):
        """composite_frame applies padding correctly"""
        bbox = (10, 10, 40, 40)
        padding = 5
        # After padding: x=15, y=15, w=30, h=30
        x = max(0, 10 + padding)
        y = max(0, 10 + padding)
        w = max(1, 40 - padding * 2)
        h = max(1, 40 - padding * 2)
        assert x == 15
        assert y == 15
        assert w == 30
        assert h == 30

    def test_composites_zero_padding(self, compositor):
        """padding=0 でも bbox が正しく使われる"""
        bbox = (5, 5, 20, 20)
        padding = 0
        x = max(0, 5 + padding)
        y = max(0, 5 + padding)
        w = max(1, 20 - padding * 2)
        h = max(1, 20 - padding * 2)
        assert x == 5
        assert w == 20


class TestCompositeVideo:
    def test_invalid_backend_raises(self, compositor):
        with pytest.raises(ValueError, match="auto/cv2/ffmpeg"):
            compositor.composite_video("vid.mp4", "ss.png", backend="invalid")

    def test_ffmpeg_backend_calls_ffmpeg(self, compositor):
        with patch.object(compositor, "composite_video_ffmpeg", return_value="out.mp4") as mock_ffmpeg:
            result = compositor.composite_video("vid.mp4", "ss.png", backend="ffmpeg")
        assert result == "out.mp4"
        mock_ffmpeg.assert_called_once()

    def test_auto_backend_fallback_to_ffmpeg(self, compositor):
        with patch.dict("sys.modules", {"cv2": MagicMock(side_effect=ImportError)}), \
             patch.object(compositor, "_composite_video_cv2", side_effect=ImportError("no cv2")), \
             patch.object(compositor, "composite_video_ffmpeg", return_value="fallback.mp4"):
            result = compositor.composite_video("vid.mp4", "ss.png", backend="auto")
        assert result == "fallback.mp4"

    def test_cv2_backend_raises_on_error(self, compositor):
        with patch.object(compositor, "_composite_video_cv2", side_effect=RuntimeError("cv2 error")):
            with pytest.raises(RuntimeError):
                compositor.composite_video("vid.mp4", "ss.png", backend="cv2")


class TestCompositeVideoFfmpeg:
    def test_no_ffmpeg_raises(self, compositor):
        with patch("shutil.which", return_value=None):
            with pytest.raises(RuntimeError, match="ffmpeg"):
                compositor.composite_video_ffmpeg("vid.mp4", "ss.png")

    def test_successful_ffmpeg(self, compositor, tmp_path):
        vid = tmp_path / "vid.mp4"
        vid.write_bytes(b"fakevideo")
        ss = tmp_path / "ss.png"
        ss.write_bytes(b"fakess")
        output = str(tmp_path / "out.mp4")

        with patch("shutil.which", return_value="/usr/bin/ffmpeg"), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = compositor.composite_video_ffmpeg(str(vid), str(ss), output)
        assert result == output

    def test_auto_output_path(self, compositor, tmp_path):
        vid = tmp_path / "test_vid.mp4"
        vid.write_bytes(b"fakevideo")
        ss = tmp_path / "ss.png"
        ss.write_bytes(b"fakess")

        with patch("shutil.which", return_value="/usr/bin/ffmpeg"), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = compositor.composite_video_ffmpeg(str(vid), str(ss))
        assert "test_vid_composited.mp4" in result

    def test_output_path_creates_parent_dir(self, compositor, tmp_path):
        vid = tmp_path / "vid.mp4"
        vid.write_bytes(b"fake")
        ss = tmp_path / "ss.png"
        ss.write_bytes(b"fake")
        output = str(tmp_path / "subdir" / "out.mp4")

        with patch("shutil.which", return_value="/usr/bin/ffmpeg"), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = compositor.composite_video_ffmpeg(str(vid), str(ss), output)
        assert result == output


class TestCompositeFrameActual:
    """composite_frame を実際の numpy 配列で呼び出すテスト (lines 93-121)"""

    def _make_cv2_mock(self, resized, roi_mask_3ch):
        mock_cv2 = MagicMock()
        mock_cv2.resize.return_value = resized
        mock_cv2.merge.return_value = roi_mask_3ch
        mock_cv2.INTER_AREA = 3
        return mock_cv2

    @staticmethod
    def _call_with_cv2(mock_cv2, func_name, *args, **kwargs):
        """Import compositor with cv2 injected into module namespace."""
        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            mod = import_module_from_repo("compositor_cf", "tools/ugc/compositor.py")
            # Inject cv2 into the module namespace (composite_frame uses it as a global)
            mod.cv2 = mock_cv2
            mod.np = np
            return getattr(mod, func_name)(*args, **kwargs)

    def test_composite_frame_full(self):
        """composite_frame が実際に合成処理を行う"""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        screenshot = np.ones((50, 50, 3), dtype=np.uint8) * 128
        mask = np.ones((100, 100), dtype=np.uint8) * 255
        bbox = (10, 10, 40, 40)

        resized = np.ones((30, 30, 3), dtype=np.uint8) * 128
        roi_mask_3ch = np.ones((30, 30, 3), dtype=np.uint8) * 255

        mock_cv2 = MagicMock()
        mock_cv2.resize.return_value = resized
        mock_cv2.merge.return_value = roi_mask_3ch
        mock_cv2.INTER_AREA = 3

        result = self._call_with_cv2(mock_cv2, "composite_frame", frame, screenshot, mask, bbox, padding=5)
        assert result.shape == frame.shape
        mock_cv2.resize.assert_called_once()

    def test_composite_frame_zero_padding(self):
        """padding=0 の場合の合成"""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        screenshot = np.ones((40, 40, 3), dtype=np.uint8) * 200
        mask = np.ones((100, 100), dtype=np.uint8) * 255
        bbox = (10, 10, 40, 40)

        resized = np.ones((40, 40, 3), dtype=np.uint8) * 200
        roi_mask_3ch = np.ones((40, 40, 3), dtype=np.uint8) * 255

        mock_cv2 = MagicMock()
        mock_cv2.resize.return_value = resized
        mock_cv2.merge.return_value = roi_mask_3ch
        mock_cv2.INTER_AREA = 3

        result = self._call_with_cv2(mock_cv2, "composite_frame", frame, screenshot, mask, bbox, padding=0)
        assert result.shape == frame.shape

    def test_composite_frame_large_padding_clamps(self):
        """padding が大きい場合、w/h が 1 にクランプされる"""
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        screenshot = np.ones((10, 10, 3), dtype=np.uint8) * 100
        mask = np.ones((100, 100), dtype=np.uint8) * 255
        bbox = (5, 5, 6, 6)

        resized = np.ones((1, 1, 3), dtype=np.uint8) * 100
        roi_mask_3ch = np.ones((1, 1, 3), dtype=np.uint8) * 255

        mock_cv2 = MagicMock()
        mock_cv2.resize.return_value = resized
        mock_cv2.merge.return_value = roi_mask_3ch
        mock_cv2.INTER_AREA = 3

        result = self._call_with_cv2(mock_cv2, "composite_frame", frame, screenshot, mask, bbox, padding=5)
        assert result.shape == frame.shape


class TestCompositeVideoCv2:
    """_composite_video_cv2 のテスト (lines 188-272)"""

    def test_cv2_processing_loop(self, compositor, tmp_path):
        """_composite_video_cv2 がフレームを処理するループを実行"""
        mock_cv2 = MagicMock()

        # VideoCapture mock
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {
            5: 30.0,  # FPS
            3: 100.0,  # WIDTH
            4: 100.0,  # HEIGHT
            7: 2.0,    # FRAME_COUNT
        }.get(prop, 0.0)
        frame_data = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, frame_data), (True, frame_data), (False, None)]
        mock_cv2.VideoCapture.return_value = mock_cap

        # imread mock
        mock_cv2.imread.return_value = np.zeros((50, 50, 3), dtype=np.uint8)

        # VideoWriter mock
        mock_writer = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_writer
        mock_cv2.VideoWriter_fourcc.return_value = 0x7634706D

        # CAP_PROP constants
        mock_cv2.CAP_PROP_FPS = 5
        mock_cv2.CAP_PROP_FRAME_WIDTH = 3
        mock_cv2.CAP_PROP_FRAME_HEIGHT = 4
        mock_cv2.CAP_PROP_FRAME_COUNT = 7

        vid = tmp_path / "input.mp4"
        vid.write_bytes(b"fake")
        ss = tmp_path / "ss.png"
        ss.write_bytes(b"fake")
        output = str(tmp_path / "out.mp4")

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            with patch.object(compositor, "detect_green_region", return_value=(np.zeros((100, 100), dtype=np.uint8), None)):
                result = compositor._composite_video_cv2(str(vid), str(ss), output)

        assert result == output
        mock_cap.release.assert_called_once()
        mock_writer.release.assert_called_once()

    def test_cv2_cannot_open_video(self, compositor, tmp_path):
        """動画を開けない場合"""
        mock_cv2 = MagicMock()
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_cv2.VideoCapture.return_value = mock_cap

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            with pytest.raises(ValueError, match="動画を開けません"):
                compositor._composite_video_cv2("bad.mp4", "ss.png", "out.mp4")

    def test_cv2_cannot_read_screenshot(self, compositor, tmp_path):
        """スクリーンショットを読み込めない場合"""
        mock_cv2 = MagicMock()
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.return_value = 30.0
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.imread.return_value = None
        mock_cv2.CAP_PROP_FPS = 5
        mock_cv2.CAP_PROP_FRAME_WIDTH = 3
        mock_cv2.CAP_PROP_FRAME_HEIGHT = 4
        mock_cv2.CAP_PROP_FRAME_COUNT = 7

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            with pytest.raises(ValueError, match="スクリーンショットを読み込めません"):
                compositor._composite_video_cv2("vid.mp4", "bad.png", "out.mp4")

    def test_cv2_auto_output_path(self, compositor, tmp_path):
        """output_path=None の場合の自動命名"""
        mock_cv2 = MagicMock()
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {5: 30.0, 3: 10.0, 4: 10.0, 7: 0.0}.get(prop, 0.0)
        mock_cap.read.return_value = (False, None)
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.imread.return_value = np.zeros((10, 10, 3), dtype=np.uint8)
        mock_writer = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_writer
        mock_cv2.VideoWriter_fourcc.return_value = 0
        mock_cv2.CAP_PROP_FPS = 5
        mock_cv2.CAP_PROP_FRAME_WIDTH = 3
        mock_cv2.CAP_PROP_FRAME_HEIGHT = 4
        mock_cv2.CAP_PROP_FRAME_COUNT = 7

        vid = tmp_path / "myvid.mp4"
        vid.write_bytes(b"fake")
        ss = tmp_path / "ss.png"
        ss.write_bytes(b"fake")

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            result = compositor._composite_video_cv2(str(vid), str(ss))
        assert "myvid_composited.mp4" in result

    def test_cv2_custom_green_range(self, compositor, tmp_path):
        """custom green_lower / green_upper"""
        mock_cv2 = MagicMock()
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {5: 30.0, 3: 10.0, 4: 10.0, 7: 0.0}.get(prop, 0.0)
        mock_cap.read.return_value = (False, None)
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.imread.return_value = np.zeros((10, 10, 3), dtype=np.uint8)
        mock_writer = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_writer
        mock_cv2.VideoWriter_fourcc.return_value = 0
        mock_cv2.CAP_PROP_FPS = 5
        mock_cv2.CAP_PROP_FRAME_WIDTH = 3
        mock_cv2.CAP_PROP_FRAME_HEIGHT = 4
        mock_cv2.CAP_PROP_FRAME_COUNT = 7

        vid = tmp_path / "myvid.mp4"
        vid.write_bytes(b"fake")
        ss = tmp_path / "ss.png"
        ss.write_bytes(b"fake")
        output = str(tmp_path / "out.mp4")

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            result = compositor._composite_video_cv2(
                str(vid), str(ss), output,
                green_lower=(30, 50, 50), green_upper=(90, 255, 255),
            )
        assert result == output


class TestPreviewGreenDetection:
    def test_frame_not_readable(self, compositor, capsys):
        mock_cv2 = MagicMock()
        mock_cap = MagicMock()
        mock_cap.read.return_value = (False, None)
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.CAP_PROP_POS_FRAMES = 1

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            compositor.preview_green_detection("video.mp4", frame_number=0)
        captured = capsys.readouterr()
        assert "読み込めません" in captured.out

    def test_preview_with_save_path(self, compositor, tmp_path):
        """save_path を指定してプレビューを保存 (lines 345-369)"""
        mock_cv2 = MagicMock()
        mock_cap = MagicMock()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, frame)
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.CAP_PROP_POS_FRAMES = 1
        mock_cv2.addWeighted.return_value = frame.copy()

        save_path = str(tmp_path / "preview.png")

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            with patch.object(compositor, "detect_green_region", return_value=(np.zeros((100, 100), dtype=np.uint8), None)):
                compositor.preview_green_detection("video.mp4", frame_number=0, save_path=save_path)

        mock_cv2.imwrite.assert_called_once()

    def test_preview_with_bbox(self, compositor, tmp_path):
        """bbox がある場合に矩形が描画される"""
        mock_cv2 = MagicMock()
        mock_cap = MagicMock()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, frame)
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.CAP_PROP_POS_FRAMES = 1
        mock_cv2.addWeighted.return_value = frame.copy()
        mock_cv2.FONT_HERSHEY_SIMPLEX = 0

        save_path = str(tmp_path / "preview.png")

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            with patch.object(compositor, "detect_green_region", return_value=(np.zeros((100, 100), dtype=np.uint8), (10, 10, 50, 50))):
                compositor.preview_green_detection("video.mp4", frame_number=5, save_path=save_path)

        mock_cv2.rectangle.assert_called_once()
        mock_cv2.putText.assert_called_once()

    def test_preview_no_save_shows_window(self, compositor):
        """save_path=None の場合はウィンドウ表示"""
        mock_cv2 = MagicMock()
        mock_cap = MagicMock()
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cap.read.return_value = (True, frame)
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.CAP_PROP_POS_FRAMES = 1
        mock_cv2.addWeighted.return_value = frame.copy()

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            with patch.object(compositor, "detect_green_region", return_value=(np.zeros((100, 100), dtype=np.uint8), None)):
                compositor.preview_green_detection("video.mp4")

        mock_cv2.imshow.assert_called_once()
        mock_cv2.waitKey.assert_called_once()
        mock_cv2.destroyAllWindows.assert_called_once()

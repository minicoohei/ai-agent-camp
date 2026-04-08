"""video_frame_analyzer.py の単体テスト"""
import pytest


class TestImport:
    def test_import_module(self):
        import video_frame_analyzer
        assert hasattr(video_frame_analyzer, 'sample_indices')


class TestSampleIndices:
    def test_small_total(self):
        from video_frame_analyzer import sample_indices
        result = sample_indices(3, 10)
        assert result == [0, 1, 2]

    def test_exact_match(self):
        from video_frame_analyzer import sample_indices
        result = sample_indices(5, 5)
        assert result == [0, 1, 2, 3, 4]

    def test_sample_subset(self):
        from video_frame_analyzer import sample_indices
        result = sample_indices(10, 3)
        assert len(result) == 3
        assert result[0] == 0
        assert result[-1] == 9

    def test_single_sample(self):
        from video_frame_analyzer import sample_indices
        result = sample_indices(10, 1)
        assert result == [0]

    def test_zero_max(self):
        from video_frame_analyzer import sample_indices
        result = sample_indices(5, 0)
        assert result == [0, 1, 2, 3, 4]

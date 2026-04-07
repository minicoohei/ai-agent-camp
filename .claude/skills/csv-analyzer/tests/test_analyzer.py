import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.analyzer import CSVAnalyzer


class TestCSVAnalyzer(unittest.TestCase):
    def setUp(self):
        """テスト用CSVファイルを作成"""
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5],
                "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
                "age": [25, 30, 35, None, 28],
                "score": [85.5, 90.0, 78.5, 82.0, 88.5],
            }
        )
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as file:
            df.to_csv(file, index=False)
            self.sample_csv = file.name

    def tearDown(self):
        Path(self.sample_csv).unlink(missing_ok=True)

    def test_analyze_basic(self):
        """基本的な分析テスト"""
        analyzer = CSVAnalyzer(self.sample_csv)
        result = analyzer.analyze()

        self.assertEqual(result["rows"], 5)
        self.assertEqual(result["columns"], 4)
        self.assertTrue(result["encoding"])
        self.assertIn("columns_info", result)

    def test_column_types(self):
        """列タイプの分析テスト"""
        analyzer = CSVAnalyzer(self.sample_csv)
        result = analyzer.analyze()

        col_names = [col["name"] for col in result["columns_info"]]
        self.assertIn("id", col_names)
        self.assertIn("name", col_names)

    def test_null_detection(self):
        """欠損値検出テスト"""
        analyzer = CSVAnalyzer(self.sample_csv)
        result = analyzer.analyze()

        age_col = next(col for col in result["columns_info"] if col["name"] == "age")
        self.assertEqual(age_col["null_count"], 1)

    def test_numeric_stats(self):
        """数値列の統計情報テスト"""
        analyzer = CSVAnalyzer(self.sample_csv)
        result = analyzer.analyze()

        score_col = next(col for col in result["columns_info"] if col["name"] == "score")
        self.assertEqual(score_col["stats"]["min"], 78.5)
        self.assertEqual(score_col["stats"]["max"], 90.0)

    def test_file_not_found(self):
        """ファイル未存在エラーテスト"""
        with self.assertRaises(FileNotFoundError):
            CSVAnalyzer("nonexistent.csv")


if __name__ == "__main__":
    unittest.main()

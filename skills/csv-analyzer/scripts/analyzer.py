import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

try:
    import chardet
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    chardet = None


class CSVAnalyzer:
    """CSVファイルを分析するクラス"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def detect_encoding(self) -> str:
        """先頭バイトから文字コードを推定する。"""
        if chardet is None:
            return "utf-8"

        raw = self.file_path.read_bytes()
        detected = chardet.detect(raw)
        return detected.get("encoding") or "utf-8"

    def analyze(self) -> Dict[str, Any]:
        """CSVファイルを分析する。"""
        encoding = self.detect_encoding()
        df = pd.read_csv(self.file_path, encoding=encoding)
        file_size_mb = self.file_path.stat().st_size / (1024 * 1024)

        return {
            "filename": self.file_path.name,
            "rows": len(df),
            "columns": len(df.columns),
            "encoding": encoding,
            "file_size_mb": round(file_size_mb, 2),
            "columns_info": self._analyze_columns(df),
        }

    def _analyze_columns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """各列を分析する。"""
        columns_info: List[Dict[str, Any]] = []
        for col in df.columns:
            col_data = df[col]
            col_info: Dict[str, Any] = {
                "name": col,
                "type": str(col_data.dtype),
                "null_count": int(col_data.isna().sum()),
                "unique_values": int(col_data.nunique(dropna=True)),
            }

            if pd.api.types.is_numeric_dtype(col_data):
                clean_data = col_data.dropna()
                col_info["stats"] = {
                    "min": float(clean_data.min()) if not clean_data.empty else None,
                    "max": float(clean_data.max()) if not clean_data.empty else None,
                    "mean": float(clean_data.mean()) if not clean_data.empty else None,
                }

            columns_info.append(col_info)
        return columns_info

    def to_json(self, output_path: str | None = None) -> str:
        """分析結果をJSON形式で返し、必要ならファイルに保存する。"""
        result = self.analyze()
        json_str = json.dumps(result, indent=2, ensure_ascii=False)

        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(json_str, encoding="utf-8")

        return json_str


def main() -> None:
    parser = argparse.ArgumentParser(description="CSVファイルを分析")
    parser.add_argument("--input", required=True, help="入力CSVファイルパス")
    parser.add_argument(
        "--output",
        help="出力JSONファイルパス（省略時は標準出力）",
    )
    args = parser.parse_args()

    analyzer = CSVAnalyzer(args.input)
    result = analyzer.to_json(args.output)

    if not args.output:
        print(result)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Video Frame Analyzer

動画からキーフレームを抽出し、Gemini Visionでフレーム解析を行う。
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any

from PIL import Image

# tools 配下のユーティリティを import できるようにする
sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env

load_runtime_env()

from bootcamp_utils import get_client, get_flash_model  # noqa: E402


def run_keyframe_extraction(
    video_path: str,
    output_dir: str,
    threshold: float,
    quality: int,
    scale: float,
) -> Dict[str, Any]:
    """video-frame-reader の抽出スクリプトを実行してJSONを返す。"""
    project_root = Path(__file__).resolve().parent.parent
    extract_script = project_root / "skills/video-frame-reader/extract_keyframes.py"

    cmd = [
        sys.executable,
        str(extract_script),
        video_path,
        "-t", str(threshold),
        "-q", str(quality),
        "-s", str(scale),
    ]
    if output_dir:
        cmd.extend(["-o", output_dir])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr.strip() or "キーフレーム抽出に失敗しました。"}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "キーフレーム抽出のJSON解析に失敗しました。"}


def sample_indices(total: int, max_frames: int) -> List[int]:
    """均等間隔でフレームをサンプリングする。"""
    if max_frames <= 0 or max_frames >= total:
        return list(range(total))
    if max_frames == 1:
        return [0]

    raw = [
        round(i * (total - 1) / (max_frames - 1))
        for i in range(max_frames)
    ]
    seen = set()
    indices = []
    for idx in raw:
        idx = max(0, min(total - 1, int(idx)))
        if idx not in seen:
            indices.append(idx)
            seen.add(idx)

    filler = 0
    while len(indices) < max_frames and filler < total:
        if filler not in seen:
            indices.append(filler)
            seen.add(filler)
        filler += 1

    return sorted(indices)


def parse_json_from_text(text: str) -> Dict[str, Any]:
    """Gemini出力からJSONを抽出して返す。"""
    content = text.strip()
    json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "summary": content[:500],
            "notable_elements": [],
            "potential_issues": [],
            "ui_changes": [],
        }


def analyze_frame(client, image_path: Path, intent: str) -> Dict[str, Any]:
    """単一フレームをGemini Visionで解析する。"""
    prompt = f"""
あなたは動画フレームのレビュー担当です。ユーザー意図: {intent}
このフレーム画像を解析し、以下のJSON形式で返してください。
{{
  "summary": "フレームの要約",
  "notable_elements": ["注目すべき要素"],
  "potential_issues": ["問題点・違和感があれば"],
  "ui_changes": ["UIの変化や遷移があれば"]
}}
JSONのみを出力してください。
"""
    image = Image.open(image_path)
    response = client.models.generate_content(
        model=get_flash_model(),
        contents=[prompt, image],
    )
    return parse_json_from_text(response.text)


def summarize_results(client, intent: str, frame_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """フレーム解析結果をまとめて要約する。"""
    prompt = f"""
以下は動画フレーム解析結果です。ユーザー意図: {intent}
結果を要約し、JSON形式で返してください。

解析結果:
{json.dumps(frame_results, ensure_ascii=False)}

出力JSON形式:
{{
  "overall_summary": "全体の要約",
  "notable_changes": ["重要な変化"],
  "issues": ["問題点"],
  "recommendations": ["次のアクション"]
}}
JSONのみを出力してください。
"""
    response = client.models.generate_content(
        model=get_flash_model(),
        contents=[prompt],
    )
    return parse_json_from_text(response.text)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="動画からキーフレームを抽出し、Geminiで解析します。"
    )
    parser.add_argument("video", help="入力動画ファイルパス")
    parser.add_argument("-o", "--output", default=None, help="出力ディレクトリ")
    parser.add_argument("-t", "--threshold", type=float, default=0.85, help="類似度閾値")
    parser.add_argument("-q", "--quality", type=int, default=30, help="JPEG品質")
    parser.add_argument("-s", "--scale", type=float, default=0.3, help="リサイズ倍率")
    parser.add_argument("--intent", default="動画の内容を要約し、重要なUI変化や問題点を特定してください。")
    parser.add_argument("--max-frames", type=int, default=12, help="解析する最大フレーム数")
    parser.add_argument("--no-analyze", action="store_true", help="解析をスキップして抽出のみ行う")

    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.exists():
        print(json.dumps({"error": f"動画ファイルが見つかりません: {video_path}"} , ensure_ascii=False))
        sys.exit(1)

    extract_result = run_keyframe_extraction(
        video_path=str(video_path),
        output_dir=args.output,
        threshold=args.threshold,
        quality=args.quality,
        scale=args.scale,
    )

    if extract_result.get("error"):
        print(json.dumps(extract_result, ensure_ascii=False, indent=2))
        sys.exit(1)

    output: Dict[str, Any] = {
        "extraction": extract_result,
    }

    if args.no_analyze:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    client = get_client()
    if not client:
        output["analysis_error"] = "Gemini APIキーが必要です。GEMINI_API_KEY または GOOGLE_API_KEY を設定してください。"
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(1)

    frame_files = extract_result.get("files", [])
    if not frame_files:
        output["analysis_error"] = "解析対象のフレームが見つかりません。"
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(1)

    indices = sample_indices(len(frame_files), args.max_frames)
    selected = [frame_files[i] for i in indices]

    frame_results = []
    for idx, frame_path in zip(indices, selected):
        analysis = analyze_frame(client, Path(frame_path), args.intent)
        frame_results.append(
            {
                "frame_index": idx,
                "file": frame_path,
                "analysis": analysis,
            }
        )

    output["analysis"] = {
        "intent": args.intent,
        "frame_count_analyzed": len(frame_results),
        "frames": frame_results,
    }

    output["summary"] = summarize_results(client, args.intent, frame_results)

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

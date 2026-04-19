"""
chapter_analyzer.py - AIセマンティックチャプター分析

字幕テキストをGemini Flashに送り、意味的なチャプター分割 + 要約 + スコアを生成。
"""

import json
import os
import sys
from pathlib import Path

import pysrt

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from bootcamp_utils import get_client, get_flash_model


def load_srt(srt_path: Path) -> list:
    """SRTファイルを読み込み、セグメントリストに変換"""
    subs = pysrt.open(str(srt_path), encoding="utf-8")
    segments = []
    for sub in subs:
        segments.append({
            "index": sub.index,
            "start": str(sub.start),
            "end": str(sub.end),
            "text": sub.text.replace("\n", " "),
        })
    return segments


def analyze_chapters(
    segments: list,
    video_title: str = "",
    video_duration: int = 0,
) -> list:
    """Gemini Flashでセマンティックチャプター分析

    Returns:
        list: [{"id": 1, "title": "...", "summary": "...", "start": "...",
                "end": "...", "keywords": [...], "highlight_score": 0.85}, ...]
    """
    client = get_client()
    if not client:
        raise RuntimeError("GEMINI_API_KEY が設定されていません")

    # 字幕テキスト全文を構築
    subtitle_text = "\n".join(
        f"[{seg['start']} - {seg['end']}] {seg['text']}"
        for seg in segments
    )

    # テキストが長すぎる場合は要約して送信
    if len(subtitle_text) > 100000:
        subtitle_text = subtitle_text[:100000] + "\n... (以下省略)"

    prompt = f"""以下は動画の字幕テキスト（タイムスタンプ付き）です。
動画タイトル: {video_title}
動画長さ: {video_duration}秒

この字幕を意味的なチャプターに分割してください。

ルール:
1. 各チャプターはトピックの自然な切れ目で分割すること
2. 各チャプターに日本語のタイトルと要約をつけること
3. highlight_score（0.0-1.0）をつけること。SNSでシェアしたくなる面白さ、有用性で評価
4. キーワード（日本語）を3-5個抽出すること
5. 結果はJSON配列で返すこと

出力形式（JSONのみ、他のテキストは不要）:
[
  {{
    "id": 1,
    "title": "チャプタータイトル",
    "summary": "このチャプターでは〜について解説している。具体的には...",
    "start": "00:00:00,000",
    "end": "00:05:30,000",
    "keywords": ["キーワード1", "キーワード2", "キーワード3"],
    "highlight_score": 0.85
  }}
]

字幕テキスト:
{subtitle_text}"""

    model = get_flash_model()
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API呼び出し失敗: {e}") from e

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        chapters = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Gemini応答のJSON解析失敗: {e}\n応答テキスト: {text[:500]}"
        ) from e

    # IDを正規化
    for i, ch in enumerate(chapters, 1):
        ch["id"] = i

    return chapters


def display_chapters(chapters: list) -> str:
    """チャプター一覧を表示用テキストに変換"""
    lines = []
    for ch in chapters:
        score = ch.get("highlight_score", 0)
        score_bar = "█" * int(score * 10)
        lines.append(
            f"  [{ch.get('id', 0):2d}] {ch.get('start', '??')[:8]} - {ch.get('end', '??')[:8]}  "
            f"★{score:.1f} {score_bar}\n"
            f"       {ch.get('title', '(無題)')}\n"
            f"       {ch.get('summary', '')[:80]}..."
        )
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="チャプター分析")
    parser.add_argument("srt", help="SRTファイル")
    parser.add_argument("--title", default="", help="動画タイトル")
    parser.add_argument("--duration", type=int, default=0, help="動画長さ（秒）")
    parser.add_argument("-o", "--output", default=None, help="JSON出力パス")
    args = parser.parse_args()

    segments = load_srt(Path(args.srt))
    chapters = analyze_chapters(segments, args.title, args.duration)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(
            json.dumps(chapters, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"出力: {args.output}")
    else:
        print(display_chapters(chapters))

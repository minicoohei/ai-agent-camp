"""
動画品質レビューモジュール

motion-review スキルのレンダー後品質チェックを Python モジュール化。
フレーム抽出 → Gemini Vision で各フレーム分析 → 品質判定を行う。
"""

import json
import os
from pathlib import Path
from typing import Optional

from ugc.video_qa import extract_qa_frames, validate_video_output


def review_rendered_video(
    mp4_path: str,
    expect_audio: bool = True,
    frame_count: int = 4,
    model: str = "gemini-2.5-flash",
) -> dict:
    """レンダー済み mp4 の品質チェック

    1. ffprobe でメタデータ検証 (audio/video stream, duration)
    2. 等間隔フレーム抽出
    3. Gemini Vision で各フレームの品質分析
    4. verdict 判定: PASS / FIX_RECOMMENDED / FIX_REQUIRED

    Args:
        mp4_path: レンダー済み動画のパス
        expect_audio: 音声ストリームを期待するか
        frame_count: 分析するフレーム数
        model: Gemini モデル

    Returns:
        {verdict, validation, frame_analysis, issues}
    """
    # Step 1: メタデータ検証
    validation = validate_video_output(mp4_path, expect_audio=expect_audio)

    issues = list(validation.get("issues", []))
    p1_count = len(issues)  # バリデーション失敗は P1 扱い

    # Step 2: フレーム抽出
    frames = []
    frame_analyses = []
    try:
        frames = extract_qa_frames(mp4_path, count=frame_count)
    except Exception as e:
        issues.append(f"フレーム抽出失敗: {e}")

    # Step 3: Gemini Vision 分析
    if frames:
        frame_analyses = _analyze_frames_with_gemini(frames, model)
        for fa in frame_analyses:
            if fa.get("issues"):
                issues.extend(fa["issues"])

    # Step 4: verdict 判定
    if p1_count > 0:
        verdict = "FIX_REQUIRED"
    elif len(issues) > p1_count:
        verdict = "FIX_RECOMMENDED"
    else:
        verdict = "PASS"

    result = {
        "verdict": verdict,
        "path": mp4_path,
        "validation": validation,
        "frame_analysis": frame_analyses,
        "issues": issues,
    }

    icon = {"PASS": "PASS", "FIX_RECOMMENDED": "WARN", "FIX_REQUIRED": "FAIL"}[verdict]
    print(f"  motion-review [{icon}]: {mp4_path}")
    if issues:
        for issue in issues[:5]:
            print(f"    - {issue}")

    return result


def _analyze_frames_with_gemini(
    frame_paths: list[str],
    model: str = "gemini-2.5-flash",
) -> list[dict]:
    """Gemini Vision でフレーム画像を分析する"""
    try:
        from google import genai
    except ImportError:
        print("  警告: google-genai パッケージ未インストール。フレーム分析をスキップします。")
        return []

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("  警告: GEMINI_API_KEY 未設定。フレーム分析をスキップします。")
        return []

    client = genai.Client(api_key=api_key)
    results = []

    prompt = (
        "この動画フレームを品質チェックしてください。以下の観点で分析し、JSON で回答してください:\n"
        '{"quality": "good"|"acceptable"|"poor", "issues": ["問題があれば記述"], '
        '"description": "フレームの内容を1行で"}\n\n'
        "チェック観点:\n"
        "- 黒フレーム/白フレームでないか\n"
        "- テキストが読める状態か（コントラスト、サイズ）\n"
        "- 画像が破損していないか\n"
        "- レイアウトが崩れていないか"
    )

    for i, frame_path in enumerate(frame_paths):
        try:
            uploaded = client.files.upload(file=frame_path)
            response = client.models.generate_content(
                model=model,
                contents=[prompt, uploaded],
            )
            text = response.text.strip()
            # JSON 抽出
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            analysis = json.loads(text)
            analysis["frame_index"] = i
            analysis["frame_path"] = frame_path
            results.append(analysis)
        except Exception as e:
            results.append({
                "frame_index": i,
                "frame_path": frame_path,
                "quality": "unknown",
                "issues": [f"分析失敗: {e}"],
                "description": "",
            })

    return results


def review_and_report(
    mp4_path: str,
    report_path: Optional[str] = None,
    expect_audio: bool = True,
) -> dict:
    """品質レビューを実行し、レポートを JSON で保存する

    Args:
        mp4_path: レンダー済み動画のパス
        report_path: レポート保存先（None の場合は動画と同じディレクトリ）
        expect_audio: 音声ストリームを期待するか

    Returns:
        レビュー結果 dict
    """
    result = review_rendered_video(mp4_path, expect_audio=expect_audio)

    if report_path is None:
        report_path = str(Path(mp4_path).parent / "motion_review.json")

    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"  motion-review レポート保存: {report_path}")
    return result

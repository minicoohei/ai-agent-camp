#!/usr/bin/env python3
"""
remotion_render.py - Python → Remotion CLI レンダリングラッパー

Clipper出力のremotion_input.jsonを受け取り、
Remotionテンプレートを適用してMP4を生成する。

Usage:
    python remotion_render.py --input remotion_input.json --template short
    python remotion_render.py --input remotion_input.json --template quote --clip-id clip_01
    python remotion_render.py --input remotion_input.json --batch short,quote,summary
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REMOTION_DIR = Path(__file__).resolve().parent / "remotion"
ROOT_DIR = Path(__file__).resolve().parents[2]

TEMPLATES = {
    "short": {
        "composition": "ShortClip",
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "description": "9:16 ショート動画（TikTok/Reels/Shorts）",
    },
    "quote": {
        "composition": "QuoteClip",
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "description": "16:9 引用クリップ（Twitter/X）",
    },
    "summary": {
        "composition": "SummaryVideo",
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "description": "16:9 まとめ動画（YouTube/ブログ）",
    },
    "blog": {
        "composition": "BlogEmbed",
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "description": "16:9 ブログ埋め込み用",
    },
    "training": {
        "composition": "TrainingClip",
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "description": "16:9 研修素材",
    },
    "square": {
        "composition": "ShortClip",
        "width": 1080,
        "height": 1080,
        "fps": 30,
        "description": "1:1 スクエア（Instagram Feed）",
    },
}


def render_video(
    input_json: Path,
    template: str,
    output_path: Path = None,
    clip_id: str = None,
    brand: str = "cursorbootcamp",
) -> Path:
    """Remotion CLIでレンダリング実行"""
    if template not in TEMPLATES:
        raise ValueError(f"テンプレート '{template}' は未対応。選択肢: {list(TEMPLATES.keys())}")

    tmpl = TEMPLATES[template]

    # 入力データ読み込み
    data = json.loads(input_json.read_text(encoding="utf-8"))

    # 特定クリップ指定の場合
    if clip_id:
        clips = [c for c in data.get("clips", []) if c["clip_id"] == clip_id]
        if not clips:
            raise ValueError(f"clip_id '{clip_id}' が見つかりません")
        data["clips"] = clips

    # 出力パス
    if output_path is None:
        session_dir = Path(data["session_dir"])
        output_dir = session_dir / "marketing"
        output_dir.mkdir(parents=True, exist_ok=True)
        clip_suffix = f"_{clip_id}" if clip_id else ""
        output_path = output_dir / f"{template}{clip_suffix}.mp4"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Remotion入力props
    props = {
        **data,
        "template": template,
        "brand": brand,
        "outputWidth": tmpl["width"],
        "outputHeight": tmpl["height"],
    }
    props_path = input_json.parent / f"_remotion_props_{template}.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    # Remotion CLI呼び出し
    cmd = [
        "npx", "remotion", "render",
        tmpl["composition"],
        str(output_path),
        "--props", str(props_path),
        "--width", str(tmpl["width"]),
        "--height", str(tmpl["height"]),
        "--fps", str(tmpl["fps"]),
    ]

    print(f"  Remotion レンダリング: {template} → {output_path}")
    result = subprocess.run(
        cmd,
        cwd=str(REMOTION_DIR),
        capture_output=True,
        text=True,
        timeout=600,
    )

    if result.returncode != 0:
        print(f"  警告: Remotionレンダリング失敗 ({template})")
        print(f"  stderr: {result.stderr[:300]}")
        # フォールバック: FFmpegでシンプルなオーバーレイ
        return ffmpeg_fallback(data, template, output_path, tmpl)

    # props一時ファイル削除
    props_path.unlink(missing_ok=True)

    return output_path


def ffmpeg_fallback(
    data: dict,
    template: str,
    output_path: Path,
    tmpl: dict,
) -> Path:
    """Remotion未初期化時のFFmpegフォールバック

    クリップに字幕とテキストオーバーレイを追加するシンプル版。
    """
    clips = data.get("clips", [])
    if not clips:
        raise RuntimeError("クリップが見つかりません")

    # 最初のクリップを使用
    clip = clips[0]
    clip_path = clip.get("clip_path")
    if not clip_path or not Path(clip_path).exists():
        raise FileNotFoundError(f"クリップファイルが見つかりません: {clip_path}")

    summary = clip.get("summary", {})
    title = summary.get("title", "")

    width = tmpl["width"]
    height = tmpl["height"]

    # FFmpegフィルタ構築
    filters = [f"scale={width}:{height}:force_original_aspect_ratio=decrease",
               f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black"]

    # テキストオーバーレイ（タイトル）
    if title:
        import re
        safe_title = re.sub(r"['\";:\\]", "", title)
        filters.append(
            f"drawtext=text='{safe_title}':fontsize=36:fontcolor=white:"
            f"x=(w-text_w)/2:y=h-100:box=1:boxcolor=black@0.6:boxborderw=10"
        )

    filter_str = ",".join(filters)

    cmd = [
        "ffmpeg", "-y",
        "-i", clip_path,
        "-vf", filter_str,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac",
        str(output_path),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        raise RuntimeError("FFmpegフォールバックがタイムアウトしました（300秒）")
    if result.returncode != 0:
        raise RuntimeError(f"FFmpegフォールバック失敗: {result.stderr[:300]}")

    print(f"  FFmpegフォールバック完了: {output_path}")
    return output_path


def batch_render(
    input_json: Path,
    templates: list,
    clip_id: str = None,
    brand: str = "cursorbootcamp",
) -> list:
    """複数テンプレートを順次レンダリング"""
    results = []
    for tmpl in templates:
        try:
            path = render_video(input_json, tmpl, clip_id=clip_id, brand=brand)
            results.append({"template": tmpl, "path": str(path), "status": "ok"})
        except Exception as e:
            results.append({"template": tmpl, "error": str(e), "status": "error"})
    return results


def main():
    parser = argparse.ArgumentParser(description="Remotion レンダリングラッパー")
    parser.add_argument("--input", required=True, help="remotion_input.json パス")
    parser.add_argument("--template", default=None, help="テンプレート (short/quote/summary/blog/training)")
    parser.add_argument("--batch", default=None, help="バッチレンダリング (short,quote,summary)")
    parser.add_argument("--clip-id", default=None, help="特定クリップID")
    parser.add_argument("--brand", default="cursorbootcamp", help="ブランドテーマ")
    parser.add_argument("-o", "--output", default=None, help="出力パス")
    parser.add_argument("--list-templates", action="store_true", help="テンプレート一覧")
    args = parser.parse_args()

    if args.list_templates:
        for name, t in TEMPLATES.items():
            print(f"  {name:10s}  {t['width']}x{t['height']}  {t['description']}")
        return

    input_json = Path(args.input).resolve()
    if not input_json.exists():
        print(f"エラー: {input_json} が見つかりません")
        sys.exit(1)

    if args.batch:
        templates = [t.strip() for t in args.batch.split(",")]
        results = batch_render(input_json, templates, args.clip_id, args.brand)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.template:
        output = Path(args.output) if args.output else None
        path = render_video(input_json, args.template, output, args.clip_id, args.brand)
        print(f"出力: {path}")
    else:
        print("--template または --batch を指定してください")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Nano Banana Pro 汎用画像生成・編集ツール

- テキストから画像生成（text-to-image）
- 画像＋指示で編集（image editing）

両方に対応しています。
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env
from bootcamp_utils import get_client, get_image_model

load_runtime_env()


# デフォルトの保存先
DEFAULT_OUTPUT_DIR = "docs/generated"


def get_aspect_ratio(width, height):
    """画像サイズからアスペクト比文字列を取得"""
    aspect_ratio = width / height
    if aspect_ratio > 1.9:
        return "21:9"
    elif aspect_ratio > 1.5:
        return "16:9"
    elif aspect_ratio > 1.2:
        return "4:3"
    elif aspect_ratio > 0.9:
        return "1:1"
    elif aspect_ratio > 0.7:
        return "3:4"
    else:
        return "9:16"


def sanitize_filename(name):
    """ファイル名に使用できない文字を置換"""
    # スペースをアンダースコアに
    name = name.replace(" ", "_")
    # ファイル名に使えない文字を除去
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # 長すぎる場合は切り詰め
    return name[:50]


def generate_image(client, prompt, output_path, aspect_ratio="16:9"):
    """
    Nano Banana Pro を使用してテキストから画像を生成する（text-to-image）
    """
    output_path = Path(output_path)
    print(f"Generating image with Nano Banana Pro...")
    print(f"Prompt: {prompt}")
    print(f"Aspect ratio: {aspect_ratio}")

    try:
        response = client.models.generate_content(
            model=get_image_model(),
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size="2K"
                )
            )
        )

        # response.candidates[0].content.parts からアクセス
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    result_image = types.Part.as_image(part)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    result_image.save(output_path)
                    print(f"\n✅ Generated image saved to: {output_path}")
                    return True
        
        print("No image data found in the response.")
        return False
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return False


def edit_image(client, input_image_paths, prompt, output_path, aspect_ratio="16:9", force_aspect_ratio=False):
    """
    Nano Banana Pro を使用して画像を編集する（複数画像入力対応）

    Args:
        force_aspect_ratio: Trueの場合、入力画像のアスペクト比を無視して指定値を使用
    """
    output_path = Path(output_path)
    input_images = []
    ar_str = aspect_ratio
    
    for i, input_image_path in enumerate(input_image_paths):
        print(f"Loading input image {i+1}: {input_image_path}")
        try:
            input_image = Image.open(input_image_path)
            width, height = input_image.size
            if i == 0 and not force_aspect_ratio:  # 強制モードでない場合のみ入力画像から取得
                ar_str = get_aspect_ratio(width, height)
            print(f"  Image size: {width}x{height}")
            input_images.append(input_image)
        except Exception as e:
            print(f"Error loading input image: {e}")
            sys.exit(1)
    
    if force_aspect_ratio:
        print(f"Aspect ratio: {ar_str} (FORCED)")
    else:
        print(f"Aspect ratio: {ar_str} (from input image)")
    print(f"Editing with {len(input_images)} reference image(s)...")
    print(f"Prompt: {prompt}")
    
    # プロンプトと画像を組み合わせてcontentsを作成
    contents = [prompt] + input_images
    
    try:
        response = client.models.generate_content(
            model=get_image_model(),
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=ar_str,
                    image_size="2K"
                )
            )
        )
        
        # response.candidates[0].content.parts からアクセス
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    result_image = types.Part.as_image(part)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    result_image.save(output_path)
                    print(f"\n✅ Edited image saved to: {output_path}")
                    return True
        
        print("No image data found in the response.")
        return False
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate or edit images using Nano Banana Pro (Gemini 3 Pro Image)."
    )
    parser.add_argument(
        "prompt",
        nargs='+',
        help="Generation/edit instruction (e.g., '富士山の風景画' or '背景をぼかす')."
    )
    parser.add_argument(
        "--input", "-i",
        action='append',
        help="Path to input image file(s). Can be specified multiple times for multiple reference images."
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path. Defaults to docs/generated/{timestamp}.png or {input_name}_edited.png"
    )
    parser.add_argument(
        "--aspect-ratio", "-ar",
        default="16:9",
        choices=["1:1", "4:3", "3:4", "16:9", "9:16", "21:9"],
        help="Aspect ratio for generation. Default: 16:9"
    )
    parser.add_argument(
        "--force-ar", "-far",
        action='store_true',
        help="Force aspect ratio even when editing (ignore input image's aspect ratio)"
    )
    parser.add_argument(
        "--session", "-s",
        help="Session/project name for organizing output (e.g., 'cursor_bootcamp_banner')"
    )

    args = parser.parse_args()
    
    # プロンプトの取得
    prompt = " ".join(args.prompt)
    if not prompt:
        print("Error: No prompt provided.")
        parser.print_help()
        sys.exit(1)
    
    client = get_client()
    
    if args.input:
        # 画像編集モード（複数画像対応）
        input_paths = []
        for input_file in args.input:
            input_path = Path(input_file)
            if not input_path.exists():
                print(f"Error: Input image not found: {input_file}")
                sys.exit(1)
            input_paths.append(input_path)
        
        # 出力パスの決定（最初の入力画像を基準）
        if args.output:
            output_path = Path(args.output)
        else:
            stem = input_paths[0].stem
            if stem.endswith("_edited"):
                output_name = f"{stem}_{datetime.now().strftime('%H%M%S')}.png"
            else:
                output_name = f"{stem}_edited.png"
            output_path = input_paths[0].parent / output_name
        
        edit_image(client, input_paths, prompt, output_path, args.aspect_ratio, args.force_ar)
    else:
        # テキストから画像生成モード
        if args.output:
            output_path = Path(args.output)
        else:
            date_str = datetime.now().strftime('%Y%m%d')
            timestamp = datetime.now().strftime('%H%M%S')
            
            if args.session:
                # セッション名をファイル名に使える形式に変換
                safe_session = sanitize_filename(args.session)
                output_dir = Path(DEFAULT_OUTPUT_DIR) / f"{date_str}_{safe_session}"
                output_name = f"{safe_session}_{timestamp}.png"
            else:
                output_dir = Path(DEFAULT_OUTPUT_DIR)
                output_name = f"generated_{date_str}_{timestamp}.png"
            
            output_path = output_dir / output_name
        
        generate_image(client, prompt, output_path, args.aspect_ratio)


if __name__ == "__main__":
    main()

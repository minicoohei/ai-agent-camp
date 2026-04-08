import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env
from bootcamp_utils import get_client, get_flash_model, get_image_model

load_runtime_env()


# デフォルトの保存先
DEFAULT_OUTPUT_DIR = "docs/manual_screenshots"


def refine_annotation_prompt(client, instruction, text_label, style):
    """
    Gemini 2.5 Flash を使用して、元画像を保持しつつ注釈を追加するための
    最適化されたプロンプトを生成する
    """
    print(f"Generating optimized annotation prompt...")
    print(f"  Instruction: {instruction}")
    print(f"  Text label: {text_label if text_label else '(none)'}")
    print(f"  Style: {style}")
    
    # スタイルごとの注釈ガイドライン
    style_guidelines = {
        "red_box": "Draw a bold red rectangular box (3-5px thick) around the target element. Add a red arrow pointing to the box from the left side.",
        "arrow": "Draw a prominent red arrow pointing directly to the target element. The arrow should be thick (8-12px) with a clear arrowhead.",
        "callout": "Add a speech bubble or callout box near the target element with the specified text inside. Use a white background with a red or black border.",
        "highlight": "Add a semi-transparent yellow highlight overlay on the target element, similar to a highlighter pen effect.",
        "circle": "Draw a bold red circle around the target element to draw attention to it.",
        "number": "Add a numbered marker (circled number) next to the target element to indicate step order."
    }
    
    style_instruction = style_guidelines.get(style, style_guidelines["red_box"])
    
    text_instruction = ""
    if text_label:
        text_instruction = f"""
        TEXT LABEL REQUIREMENT:
        - Add the following Japanese text label near the annotation: "{text_label}"
        - The text should be clearly readable, using a sans-serif font
        - Text color should be red or black for visibility
        - Position the text to the left of the arrow or near the callout
        """
    
    meta_prompt = f"""
    You are an expert at creating annotation overlays for technical manual screenshots.
    Your task is to generate a prompt for Gemini 3 Pro Image that will add annotations to a screenshot.

    ============================================================
    ABSOLUTELY CRITICAL - READ THIS CAREFULLY:
    ============================================================
    
    The original screenshot image MUST remain COMPLETELY UNCHANGED.
    
    - DO NOT modify, enhance, filter, blur, sharpen, or alter ANY pixel of the original image
    - DO NOT change colors, contrast, brightness, or any visual property of the original
    - DO NOT crop, resize, or transform the original image in any way
    - DO NOT add any effects or filters to the background/original image
    - The original screenshot must be preserved PIXEL-FOR-PIXEL, exactly as provided
    
    You are ONLY allowed to ADD annotation elements ON TOP of the original image:
    - Arrows
    - Boxes/rectangles
    - Circles
    - Text labels
    - Callout bubbles
    - Highlight overlays (semi-transparent)
    
    Think of it as placing transparent stickers on top of a photograph - 
    the photograph underneath must remain completely untouched.
    
    ============================================================
    
    USER'S ANNOTATION REQUEST:
    {instruction}
    
    ANNOTATION STYLE:
    {style_instruction}
    
    {text_instruction}
    
    OUTPUT REQUIREMENTS:
    - Generate a prompt that instructs the image model to:
      1. Keep the original screenshot as the base layer, completely unchanged
      2. Add ONLY the requested annotation elements as an overlay
      3. Ensure annotations are visually clear and professional
      4. Use bold, visible colors (primarily red) for annotations
      5. Maintain the exact same image dimensions
    
    Output ONLY the final prompt text in English, without any explanations or prefixes.
    The prompt should be detailed and specific about preserving the original image.
    """
    
    response = client.models.generate_content(
       model=get_flash_model(),
        contents=[meta_prompt]
    )
    
    refined_prompt = response.text.strip()
    print(f"\nRefined Prompt:\n{refined_prompt}\n")
    return refined_prompt


def annotate_image(client, input_image_path, prompt, output_path):
    """
    Nano Banana Pro (Gemini 3 Pro Image Preview) を使用して
    入力画像に注釈を追加し、保存する
    
    重要: 元画像は一切変更せず、注釈のみをオーバーレイする
    """
    print(f"Loading input image: {input_image_path}")
    
    try:
        # 入力画像を読み込み
        input_image = Image.open(input_image_path)
        width, height = input_image.size
        print(f"Image size: {width}x{height}")
        
        # アスペクト比を計算して最も近いものを選択
        aspect_ratio = width / height
        if aspect_ratio > 1.9:
            ar_str = "21:9"
        elif aspect_ratio > 1.5:
            ar_str = "16:9"
        elif aspect_ratio > 1.2:
            ar_str = "4:3"
        elif aspect_ratio > 0.9:
            ar_str = "1:1"
        elif aspect_ratio > 0.7:
            ar_str = "3:4"
        else:
            ar_str = "9:16"
        
        print(f"Using aspect ratio: {ar_str}")
        
    except Exception as e:
        print(f"Error loading input image: {e}")
        sys.exit(1)
    
    # プロンプトに元画像保持の強調を追加
    full_prompt = f"""
CRITICAL: The provided screenshot image MUST remain EXACTLY as-is. 
DO NOT modify ANY pixel of the original image.
ONLY add annotation overlays on top.

{prompt}
"""
    
    print(f"Generating annotated image with Nano Banana Pro...")
    
    try:
        response = client.models.generate_content(
            model=get_image_model(),
            contents=[full_prompt, input_image],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=ar_str,
                    image_size="2K"
                )
            )
        )
        
        for part in response.parts:
            if part.inline_data:
                result_image = types.Part.as_image(part)
                # ディレクトリが存在しない場合は作成
                output_path.parent.mkdir(parents=True, exist_ok=True)
                result_image.save(output_path)
                print(f"\n✅ Annotated image saved to: {output_path}")
                print(f"⚠️  Note: Original image at '{input_image_path}' was NOT modified.")
                return True
        
        print("No image data found in the response.")
        return False
        
    except Exception as e:
        print(f"Error generating annotated image: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Add annotations to screenshots using Nano Banana Pro (Gemini 3 Pro Image). "
                    "The original image is NEVER modified - annotations are added as overlays only."
    )
    parser.add_argument(
        "input", 
        help="Path to the input screenshot image."
    )
    parser.add_argument(
        "instruction", 
        nargs='*',
        help="Annotation instruction (e.g., '「保存」ボタンを赤枠で囲む'). Can be multiple words."
    )
    parser.add_argument(
        "--text", "-t",
        help="Optional text label to display near the annotation (e.g., 'ここをクリック')."
    )
    parser.add_argument(
        "--style", "-s",
        default="red_box",
        choices=["red_box", "arrow", "callout", "highlight", "circle", "number"],
        help="Annotation style. Default: red_box"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path. Defaults to {input_name}_annotated.png"
    )

    args = parser.parse_args()
    
    # 入力画像の存在確認
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input image not found: {args.input}")
        sys.exit(1)
    
    # 注釈指示の取得
    instruction = " ".join(args.instruction) if args.instruction else ""
    if not instruction:
        print("Error: No annotation instruction provided.")
        print("Example: python annotate_screenshot.py screenshot.png 「保存」ボタンを赤枠で囲む")
        parser.print_help()
        sys.exit(1)
    
    # 出力パスの決定
    if args.output:
        output_path = Path(args.output)
    else:
        # 入力ファイル名から _annotated.png を生成
        stem = input_path.stem
        # 既に _annotated が付いている場合は重複を避ける
        if stem.endswith("_annotated"):
            output_name = f"{stem}_{datetime.now().strftime('%H%M%S')}.png"
        else:
            output_name = f"{stem}_annotated.png"
        output_path = input_path.parent / output_name
    
    # 出力ファイルが入力ファイルと同じ場合はエラー
    if output_path.resolve() == input_path.resolve():
        print("Error: Output path cannot be the same as input path.")
        print("The original image must NOT be overwritten.")
        sys.exit(1)
    
    # 出力ファイルが既に存在する場合の警告
    if output_path.exists():
        print(f"Warning: Output file already exists: {output_path}")
        print("It will be overwritten.")
    
    client = get_client()
    
    # プロンプトの最適化
    refined_prompt = refine_annotation_prompt(
        client, 
        instruction, 
        args.text, 
        args.style
    )
    
    # 画像に注釈を追加
    annotate_image(client, input_path, refined_prompt, output_path)


if __name__ == "__main__":
    main()

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
DEFAULT_OUTPUT_DIR = "reports/visualizations"

def refine_prompt(client, topic, style):
    """
    Gemini 2.5 Flash を使用して、ユーザーのトピックから Nano Banana Pro に最適化された詳細な英語プロンプトを作成する
    """
    # トピックが長すぎる場合はプレビュー表示を制限
    preview_topic = topic[:50] + "..." if len(topic) > 50 else topic
    print(f"Generating optimized prompt for topic: '{preview_topic}' with style: '{style}'...")
    
    meta_prompt = f"""
    You are an expert prompt engineer for the Gemini 3 Pro Image model (Nano Banana Pro).
    Your task is to create a highly detailed and effective prompt for generating an infographic, diagram, or illustration based on the following input content.

    Input Content/Topic:
    {topic}

    Target Style: {style}

    Instructions:
    1. **Analyze the Input**: If the input is a long text or article, summarize the key concepts into a visual representation. Identify the main subject, relationships, and key data points to visualize.
    2. **Construct the Prompt**: According to the official Nano Banana Pro prompting guide, the prompt MUST include:
        - **Subject**: Clearly define who or what is in the image (e.g., "a flow chart illustrating...", "a detailed diagram of...").
        - **Composition**: Framing and perspective (e.g., "wide shot", "isometric view", "infographic layout").
        - **Action**: What is happening (if applicable).
        - **Location**: Setting or background (e.g., "on a clean white background", "in a futuristic lab").
        - **Style**: Aesthetic details (e.g., "3D animation", "watercolor", "photorealistic").
        - **Lighting**: Lighting setup (e.g., "studio lighting", "soft natural light").
        - **Text Integration**: Specify ANY important titles, labels, or keywords from the input text that should be rendered in the image.
        **CRITICAL**: If the input topic or request is in Japanese, or if the user specifically requests Japanese text, you MUST instruct the model to render the text in JAPANESE characters (Kanji, Hiragana, Katakana). Example: "The headline '光合成の仕組み' rendered in bold sans-serif font".

    Style Guidelines:
    - 'colorful_infographic': Focus on clear icons, vibrant colors, readable text labels, and an organized layout suitable for presentations.
    - 'sketch': Hand-drawn aesthetics, pencil/charcoal textures, schematic look, white background.
    - 'photorealistic': High-quality photo look, realistic textures, depth of field, cinematic lighting.
    - 'minimalist': Negative space, simple geometric shapes, limited color palette, clean design.
    - 'claymation': 3D clay texture, soft lighting, playful look.
    - 'pixel_art': Retro game style, blocky, limited color palette.

    Output ONLY the prompt text in English, without any explanations or prefixes. Ensure it is a single coherent paragraph or a structured list of visual descriptions.
    """
    
    response = client.models.generate_content(
        model=get_flash_model(),
        contents=[meta_prompt]
    )
    
    refined_prompt = response.text.strip()
    print(f"Refined Prompt: {refined_prompt}\n")
    return refined_prompt

def generate_image(client, prompt, output_path, aspect_ratio="16:9"):
    """
    Gemini 3 Pro Image Preview を使用して画像を生成し、保存する
    """
    print(f"Generating image with aspect ratio {aspect_ratio}...")
    
    try:
        response = client.models.generate_content(
            model=get_image_model(),
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size="2K"  # High resolution for professional use
                )
            )
        )
        
        for part in response.parts:
            if part.inline_data:
                image = types.Part.as_image(part)
                # ディレクトリが存在しない場合は作成
                output_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(output_path)
                print(f"Image saved to: {output_path}")
                return True
            
        print("No image data found in the response.")
        return False

    except Exception as e:
        print(f"Error generating image: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate an infographic or diagram using Gemini (Nano Banana Pro).")
    parser.add_argument("topic", nargs='*', help="The topic, description, or content to visualize. Can be multiple words.")
    parser.add_argument("--file", "-f", help="Path to a text file containing the content to visualize.")
    parser.add_argument("--style", default="colorful_infographic", 
                        choices=["colorful_infographic", "sketch", "photorealistic", "minimalist", "claymation", "pixel_art"],
                        help="The style of the generated image.")
    parser.add_argument("--output", help="Path to save the generated image. Defaults to reports/visualizations/.")
    parser.add_argument("--filename", help="Filename for the image. Defaults to topic_timestamp.png")
    parser.add_argument("--aspect_ratio", default="16:9", 
                        choices=["1:1", "16:9", "4:3", "3:4", "9:16", "21:9"],
                        help="Aspect ratio of the generated image.")

    args = parser.parse_args()

    # トピックの取得: ファイル指定があればファイルから、なければ引数から
    topic_text = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                topic_text = f.read()
        except Exception as e:
            print(f"Error reading file {args.file}: {e}")
            sys.exit(1)
    elif args.topic:
        topic_text = " ".join(args.topic)
    
    if not topic_text:
        print("Error: No topic or content provided. Use positional arguments or --file.")
        parser.print_help()
        sys.exit(1)

    client = get_client()

    # プロンプトの洗練
    refined_prompt = refine_prompt(client, topic_text, args.style)

    # 出力パスの決定
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # ファイル名に使えない文字を置換 (最初の30文字だけ使う)
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic_text])[:30]
        filename = args.filename if args.filename else f"{safe_topic}_{timestamp}.png"
        output_path = Path(DEFAULT_OUTPUT_DIR) / filename

    # 画像生成
    generate_image(client, refined_prompt, output_path, args.aspect_ratio)

if __name__ == "__main__":
    main()

"""
講義用スライド生成ツール

Gemini Flash でコンテンツを生成し、Nano Banana Pro でスライド画像を作成します。

デザイン仕様:
- 背景: 白
- メインカラー: 青 (#2563EB)
- サブカラー: 黄色 (#FBBF24)
- スタイル: フラットデザイン
- 文字サイズ: 14pt以上
- テキスト量: 少なめ（整頓されたイメージ）
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env
from bootcamp_utils import get_client, get_flash_model, get_image_model

from google import genai
from google.genai import types

load_runtime_env()


# デフォルトの保存先
DEFAULT_OUTPUT_DIR = "docs/slides"

# デザイン仕様の定数
DESIGN_SPEC = {
    "background": "white",
    "main_color": "#2563EB",  # 青
    "sub_color": "#FBBF24",   # 黄色
    "style": "flat design",
    "min_font_size": "14pt",
    "aspect_ratio": "16:9",
}


def get_client():
    """Google GenAI クライアントを初期化して返す"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def generate_slide_content(client, topic):
    """
    Gemini 2.5 Flash を使用して、トピックから講義内容を生成する
    """
    print(f"Generating slide content for topic: {topic}")
    
    content_prompt = f"""
    あなたは講義資料作成のエキスパートです。
    以下のトピックについて、1枚のスライドに収まる簡潔な講義内容を生成してください。

    トピック: {topic}

    出力要件:
    1. タイトル（15文字以内）
    2. サブタイトルまたは要約（30文字以内、省略可）
    3. 主要ポイント（3-5個、各20文字以内）
    4. 補足説明があれば1文（40文字以内、省略可）

    制約:
    - 文字数は最小限に抑える（スライドは見やすさが重要）
    - 専門用語は必要に応じて使用するが、可能な限り平易な表現を使う
    - 箇条書きは短く、インパクトのある表現を使う

    以下のJSON形式で出力してください:
    {{
        "title": "タイトル",
        "subtitle": "サブタイトル（省略可）",
        "points": ["ポイント1", "ポイント2", "ポイント3"],
        "note": "補足説明（省略可）"
    }}

    JSONのみを出力し、他の説明は不要です。
    """
    
    response = client.models.generate_content(
        model=get_flash_model(),
        contents=[content_prompt]
    )
    
    content = response.text.strip()
    # JSONブロックを抽出（```json ... ``` で囲まれている場合に対応）
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    
    print(f"\nGenerated Content:\n{content}\n")
    return content


def create_slide_prompt(client, topic, content, style):
    """
    Gemini 2.5 Flash を使用して、スライド生成用の最適化されたプロンプトを作成する
    """
    print(f"Creating optimized slide prompt...")
    print(f"  Topic: {topic}")
    print(f"  Style: {style}")
    
    # スタイルごとのレイアウトガイドライン
    style_guidelines = {
        "auto": """
            Analyze the content and choose the most appropriate layout:
            - If it's a main topic introduction, use a title slide layout
            - If it has multiple points, use a content slide layout with bullet points
            - If it explains a process or concept, use a diagram-style layout
            - If it summarizes key points, use a summary layout
        """,
        "title": """
            Create a TITLE SLIDE layout:
            - Large, bold title centered in the upper-middle area
            - Smaller subtitle below the title
            - Clean, minimal design with ample white space
            - Use the main blue color for the title
            - Optional: subtle accent line or shape using the yellow color
        """,
        "content": """
            Create a CONTENT SLIDE layout:
            - Title at the top (left-aligned or centered)
            - 3-5 bullet points with clear hierarchy
            - Use icons or simple shapes next to each bullet point
            - Consistent spacing between items
            - Use blue for headers/titles, yellow for accents or highlights
        """,
        "diagram": """
            Create a DIAGRAM SLIDE layout:
            - Title at the top
            - Visual representation of the concept (flowchart, process diagram, or concept map)
            - Use boxes, arrows, and simple icons
            - Clear visual hierarchy with numbered steps if applicable
            - Use blue for main elements, yellow for highlights or connectors
            - Minimal text, let the visuals tell the story
        """,
        "summary": """
            Create a SUMMARY SLIDE layout:
            - "Summary" or "Key Points" as the title
            - 3-5 key takeaways in a clean list format
            - Optional: checkmarks or numbered indicators
            - Use a subtle visual element to indicate completion/summary
            - Blue for main text, yellow for accents
        """
    }
    
    style_instruction = style_guidelines.get(style, style_guidelines["auto"])
    
    meta_prompt = f"""
    You are an expert at creating professional lecture slides.
    Your task is to generate a prompt for Gemini 3 Pro Image that will create a high-quality slide.

    ============================================================
    DESIGN SPECIFICATIONS (MUST FOLLOW EXACTLY):
    ============================================================
    
    1. BACKGROUND: Pure white (#FFFFFF)
    2. MAIN COLOR: Blue (#2563EB) - Use for titles, headers, important elements
    3. ACCENT COLOR: Yellow (#FBBF24) - Use sparingly for highlights, icons, decorative elements
    4. STYLE: Modern flat design - no gradients, no shadows, no 3D effects
    5. TYPOGRAPHY:
       - Clean sans-serif font (like Noto Sans, Helvetica, or similar)
       - Minimum font size: 14pt equivalent (ensure readability)
       - Title should be prominently larger than body text
    6. ASPECT RATIO: 16:9 (widescreen presentation format)
    7. TEXT AMOUNT: Minimal - prioritize clarity and visual impact over text density
    8. LANGUAGE: All text content should be in JAPANESE
    
    ============================================================
    SLIDE CONTENT:
    ============================================================
    
    Topic: {topic}
    
    Content (JSON):
    {content}
    
    ============================================================
    LAYOUT STYLE:
    ============================================================
    
    {style_instruction}
    
    ============================================================
    OUTPUT REQUIREMENTS:
    ============================================================
    
    Generate a detailed prompt that instructs the image model to:
    1. Create a professional lecture slide with the exact design specifications above
    2. Use the provided content appropriately placed on the slide
    3. Maintain visual hierarchy (title > subtitle > body > notes)
    4. Include subtle decorative elements using the accent color (geometric shapes, lines, etc.)
    5. Ensure the slide looks professional and suitable for corporate training
    6. All text must be in Japanese
    7. The overall impression should be clean, organized, and modern
    
    Output ONLY the final prompt text in English, without any explanations or prefixes.
    The prompt should be comprehensive and specific about the design requirements.
    """
    
    response = client.models.generate_content(
        model=get_flash_model(),
        contents=[meta_prompt]
    )
    
    refined_prompt = response.text.strip()
    print(f"\nRefined Prompt:\n{refined_prompt[:500]}...\n")
    return refined_prompt


def generate_slide_image(client, prompt, output_path):
    """
    Nano Banana Pro (Gemini 3 Pro Image Preview) を使用して
    スライド画像を生成し、保存する
    """
    print(f"Generating slide image with Nano Banana Pro...")
    
    # プロンプトにデザイン仕様の強調を追加
    full_prompt = f"""
Create a professional lecture slide image.

CRITICAL DESIGN REQUIREMENTS:
- Background: PURE WHITE only
- Main color: Blue (#2563EB)
- Accent color: Yellow (#FBBF24)
- Style: Modern FLAT DESIGN (no gradients, no shadows, no 3D effects)
- All text in JAPANESE
- Clean, minimal, professional appearance
- 16:9 aspect ratio presentation slide

{prompt}
"""
    
    try:
        response = client.models.generate_content(
            model=get_image_model(),
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
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
                print(f"\n✅ Slide image saved to: {output_path}")
                return True
        
        print("No image data found in the response.")
        return False
        
    except Exception as e:
        print(f"Error generating slide image: {e}")
        return False


def sanitize_filename(text, max_length=30):
    """
    ファイル名として使用できない文字を除去し、長さを制限する
    """
    # 使用できない文字を除去
    sanitized = re.sub(r'[<>:"/\\|?*]', '', text)
    # 空白をアンダースコアに置換
    sanitized = re.sub(r'\s+', '_', sanitized)
    # 長さを制限
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized


def main():
    parser = argparse.ArgumentParser(
        description="Generate professional lecture slides using Nano Banana Pro (Gemini 3 Pro Image). "
                    "Creates slides with a consistent design: white background, blue main color, yellow accents."
    )
    parser.add_argument(
        "topic",
        nargs='+',
        help="Topic for the slide (e.g., 'AI AgentのToolsの仕組み'). Can be multiple words."
    )
    parser.add_argument(
        "--style", "-s",
        default="auto",
        choices=["auto", "title", "content", "diagram", "summary"],
        help="Slide layout style. Default: auto (AI chooses based on content)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path. Defaults to docs/slides/{topic}_{timestamp}.png"
    )

    args = parser.parse_args()
    
    # トピックの取得
    topic = " ".join(args.topic)
    if not topic:
        print("Error: No topic provided.")
        print("Example: python generate_slide.py AI AgentのToolsの仕組み")
        parser.print_help()
        sys.exit(1)
    
    # 出力パスの決定
    if args.output:
        output_path = Path(args.output)
    else:
        # トピック名からファイル名を生成
        sanitized_topic = sanitize_filename(topic)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_name = f"{sanitized_topic}_{timestamp}.png"
        output_path = Path(DEFAULT_OUTPUT_DIR) / output_name
    
    # 出力ファイルが既に存在する場合の警告
    if output_path.exists():
        print(f"Warning: Output file already exists: {output_path}")
        print("It will be overwritten.")
    
    print("=" * 60)
    print("Lecture Slide Generator")
    print("=" * 60)
    print(f"Topic: {topic}")
    print(f"Style: {args.style}")
    print(f"Output: {output_path}")
    print("=" * 60)
    
    client = get_client()
    
    # Step 1: コンテンツ生成
    print("\n[Step 1/3] Generating slide content...")
    content = generate_slide_content(client, topic)
    
    # Step 2: プロンプト最適化
    print("\n[Step 2/3] Creating optimized prompt...")
    refined_prompt = create_slide_prompt(client, topic, content, args.style)
    
    # Step 3: スライド画像生成
    print("\n[Step 3/3] Generating slide image...")
    success = generate_slide_image(client, refined_prompt, output_path)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Slide generation completed successfully!")
        print(f"📁 Output: {output_path}")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Slide generation failed.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()

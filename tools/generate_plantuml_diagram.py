"""
PlantUML図解生成ツール

PlantUMLファイルを入力として、Visio Flowchartテンプレート風の
モダンなフローチャート画像をNano Banana Proで生成します。

デザイン仕様:
- レイアウト: 縦方向（トップダウン）、スイムレーン形式
- 背景: 淡いグレー (#F7F7F7)
- 一般プロセス: 白、角丸長方形、枠線 #4A90E2
- 内部処理: 淡いブルー (#E8F1FF)
- 受信/入力: 淡いグリーン (#E9F7EC)
- 条件分岐: 菱形、枠線 #7B61FF
- フォント: サンセリフ体
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
DEFAULT_OUTPUT_DIR = "docs/diagrams"

# デザイン仕様の定数
DESIGN_SPEC = """
============================================================
DESIGN SPECIFICATIONS (MUST FOLLOW EXACTLY):
============================================================

1. LAYOUT:
   - Top-down vertical flow direction
   - Swimlane layout: One vertical lane per "participant"
   - Swimlane borders: Light gray (#CCCCCC), white background
   - Each step placed in its corresponding participant's swimlane

2. SHAPE STYLES:
   - General Process: Rounded rectangle, white fill, border #4A90E2, light shadow
   - Internal Processing (self-calls): Light blue (#E8F1FF) rounded rectangle
   - Receiving/Input (from other participants): Light green (#E9F7EC) rounded rectangle
   - Conditional branches (alt/else/opt): Diamond shape, border #7B61FF

3. ARROWS (Flow Lines):
   - All straight lines or 90-degree angles only
   - Color: Dark gray (#555555)
   - Clear, visible arrowheads
   - Branches split left/right from diamond bottom with alt/else labels

4. ICONS:
   - Small flat icons in top-left of each shape
   - Icon line weight: 1.5-2px
   - Auto-assign icons based on participant name and process type
   - Examples: person icon for users, server icon for APIs, brain icon for AI

5. COLOR PALETTE:
   - Overall background: Light gray (#F7F7F7)
   - General process: White
   - Internal processing: Light blue (#E8F1FF)
   - Receiving/Input: Light green (#E9F7EC)
   - Branch labels: Dark gray (#444444)

6. TYPOGRAPHY:
   - Sans-serif font (Segoe UI, Helvetica, Noto Sans)
   - Shape text: ~18px
   - Labels (alt, else, opt): 14px
   - Center-aligned text in shapes

7. SPACING:
   - Vertical distance between shapes: 40-60px
   - Equal-width swimlanes
   - Proper margins, aligned shapes

8. OVERALL STYLE:
   - Modern, simple UI-style design
   - Minimal decorations, high readability
   - Very light shadows only, no heavy 3D effects
   - Balanced, well-aligned composition
   - Visio Flowchart template aesthetic
"""


def get_client():
    """Google GenAI クライアントを初期化して返す"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def parse_plantuml_structure(content):
    """
    PlantUMLの構造を解析して、participant数やステップ数を抽出する
    """
    # participant/actorの抽出
    participant_pattern = r'(?:participant|actor)\s+["\']?([^"\'"\s]+)["\']?(?:\s+as\s+(\w+))?'
    participants = re.findall(participant_pattern, content)
    
    # メッセージ（矢印）の数をカウント
    message_pattern = r'^\s*\w+\s*-+>+\s*\w+'
    messages = re.findall(message_pattern, content, re.MULTILINE)
    
    # alt/else/opt ブロックの数をカウント
    branch_pattern = r'\b(alt|else|opt|loop|group)\b'
    branches = re.findall(branch_pattern, content)
    
    return {
        "participant_count": len(participants),
        "message_count": len(messages),
        "branch_count": len(branches),
        "participants": participants
    }


def determine_aspect_ratio(structure):
    """
    PlantUMLの構造に基づいてアスペクト比を自動判定する
    """
    participant_count = structure["participant_count"]
    message_count = structure["message_count"]
    
    # participant数が多い場合は横長
    if participant_count >= 5:
        return "21:9"
    
    # シーケンスが長い場合は縦長
    if message_count >= 20:
        return "9:16"
    
    # participant数が3-4の場合
    if participant_count >= 3:
        return "16:9"
    
    # デフォルト
    return "16:9"


def create_diagram_prompt(client, plantuml_content, structure):
    """
    Gemini 2.5 Flash を使用して、PlantUMLから図解生成用の最適化されたプロンプトを作成する
    """
    print("Creating optimized diagram prompt from PlantUML...")
    
    meta_prompt = f"""
You are an expert at converting PlantUML sequence diagrams into visual specifications for image generation.
Your task is to analyze the PlantUML code and create a detailed prompt for generating a Visio-style flowchart image.

============================================================
INPUT PLANTUML CODE:
============================================================

{plantuml_content}

============================================================
PLANTUML STRUCTURE ANALYSIS:
============================================================

- Number of participants: {structure["participant_count"]}
- Number of messages/steps: {structure["message_count"]}
- Number of branches (alt/else/opt/loop): {structure["branch_count"]}

{DESIGN_SPEC}

============================================================
YOUR TASK:
============================================================

1. ANALYZE the PlantUML code and identify:
   - All participants and their roles (user, API, service, database, etc.)
   - The flow of messages between participants
   - Any conditional branches (alt/else), loops, or optional blocks
   - The logical grouping of steps

2. CONVERT to a visual description that includes:
   - Swimlane layout with participant names as headers
   - Each step as a shape in the correct swimlane
   - Proper shape types (process, internal, input, decision)
   - Arrow connections with labels
   - Appropriate icons for each participant type

3. OUTPUT a comprehensive image generation prompt that:
   - Describes the exact layout and positioning
   - Specifies all colors, shapes, and styles per the design spec
   - Includes all text labels in Japanese (preserve original Japanese text)
   - Creates a professional, Visio-like flowchart appearance

OUTPUT ONLY the final prompt text in English, without any explanations or prefixes.
The prompt should be comprehensive and specific about the visual layout.
Ensure all Japanese text from the PlantUML is preserved exactly in the output.
"""
    
    response = client.models.generate_content(
        model=get_flash_model(),
        contents=[meta_prompt]
    )
    
    refined_prompt = response.text.strip()
    print(f"\nRefined Prompt (preview):\n{refined_prompt[:500]}...\n")
    return refined_prompt


def generate_diagram_image(client, prompt, output_path, aspect_ratio):
    """
    Nano Banana Pro (Gemini 3 Pro Image Preview) を使用して
    図解画像を生成し、保存する
    """
    print(f"Generating diagram image with Nano Banana Pro (aspect ratio: {aspect_ratio})...")
    
    # プロンプトにデザイン仕様の強調を追加
    full_prompt = f"""
Create a professional Visio-style flowchart/sequence diagram image.

CRITICAL DESIGN REQUIREMENTS:
- Layout: Vertical top-down flow with swimlanes
- Background: Light gray (#F7F7F7)
- Process shapes: Rounded rectangles with light shadow
- Internal processing: Light blue (#E8F1FF)
- Input/receiving: Light green (#E9F7EC)
- Decision diamonds: Purple border (#7B61FF)
- Arrows: Dark gray (#555555), straight or 90-degree angles
- Small flat icons in top-left of shapes
- Sans-serif font, clear and readable
- Modern, clean, professional Visio Flowchart aesthetic
- All text in JAPANESE where applicable
- NO hand-drawn style, NO sketchy lines
- PRECISE alignment and spacing

{prompt}
"""
    
    try:
        response = client.models.generate_content(
            model=get_image_model(),
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
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
                print(f"\n✅ Diagram image saved to: {output_path}")
                return True
        
        print("No image data found in the response.")
        return False
        
    except Exception as e:
        print(f"Error generating diagram image: {e}")
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
        description="Generate Visio-style flowchart from PlantUML using Nano Banana Pro (Gemini 3 Pro Image). "
                    "Creates professional diagrams with swimlanes, modern styling, and consistent design."
    )
    parser.add_argument(
        "plantuml_path",
        help="Path to the PlantUML file (.puml)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path. Defaults to docs/diagrams/{filename}_{timestamp}.png"
    )
    parser.add_argument(
        "--aspect_ratio", "-a",
        default="auto",
        choices=["auto", "1:1", "16:9", "4:3", "3:4", "9:16", "21:9"],
        help="Aspect ratio of the generated image. 'auto' determines based on PlantUML structure."
    )

    args = parser.parse_args()
    
    # PlantUMLファイルの読み込み
    plantuml_path = Path(args.plantuml_path)
    if not plantuml_path.exists():
        print(f"Error: PlantUML file not found: {plantuml_path}")
        sys.exit(1)
    
    try:
        with open(plantuml_path, 'r', encoding='utf-8') as f:
            plantuml_content = f.read()
    except Exception as e:
        print(f"Error reading PlantUML file: {e}")
        sys.exit(1)
    
    if not plantuml_content.strip():
        print("Error: PlantUML file is empty.")
        sys.exit(1)
    
    # PlantUML構造の解析
    structure = parse_plantuml_structure(plantuml_content)
    print(f"PlantUML Structure:")
    print(f"  - Participants: {structure['participant_count']}")
    print(f"  - Messages: {structure['message_count']}")
    print(f"  - Branches: {structure['branch_count']}")
    
    # アスペクト比の決定
    if args.aspect_ratio == "auto":
        aspect_ratio = determine_aspect_ratio(structure)
        print(f"  - Auto-determined aspect ratio: {aspect_ratio}")
    else:
        aspect_ratio = args.aspect_ratio
    
    # 出力パスの決定
    if args.output:
        output_path = Path(args.output)
    else:
        # ファイル名から出力名を生成
        base_name = sanitize_filename(plantuml_path.stem)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_name = f"{base_name}_{timestamp}.png"
        output_path = Path(DEFAULT_OUTPUT_DIR) / output_name
    
    # 出力ファイルが既に存在する場合の警告
    if output_path.exists():
        print(f"Warning: Output file already exists: {output_path}")
        print("It will be overwritten.")
    
    print("=" * 60)
    print("PlantUML Diagram Generator")
    print("=" * 60)
    print(f"Input: {plantuml_path}")
    print(f"Aspect Ratio: {aspect_ratio}")
    print(f"Output: {output_path}")
    print("=" * 60)
    
    client = get_client()
    
    # Step 1: プロンプト生成
    print("\n[Step 1/2] Analyzing PlantUML and creating optimized prompt...")
    refined_prompt = create_diagram_prompt(client, plantuml_content, structure)
    
    # Step 2: 図解画像生成
    print("\n[Step 2/2] Generating diagram image...")
    success = generate_diagram_image(client, refined_prompt, output_path, aspect_ratio)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Diagram generation completed successfully!")
        print(f"📁 Output: {output_path}")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Diagram generation failed.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()

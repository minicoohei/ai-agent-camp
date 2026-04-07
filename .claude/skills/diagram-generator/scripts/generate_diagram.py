#!/usr/bin/env python3
"""
Diagram Generator - Generate infographics and visualizations from text using Gemini API.
"""
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# プロジェクトルートをパスに追加
_ROOT_DIR = Path(__file__).resolve().parents[3]
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from google import genai
from google.genai import types
from dotenv import load_dotenv

try:
    from tools.credential_manager import inject_to_environ
    inject_to_environ()
except ImportError:
    try:
        from credential_manager import inject_to_environ
        inject_to_environ()
    except ImportError:
        pass
load_dotenv()


FLASH_MODEL = os.environ.get("GEMINI_FLASH_MODEL", "gemini-3-flash-preview")
IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3-pro-preview")
DEFAULT_OUTPUT_DIR = Path("output/diagrams")

STYLE_GUIDELINES = {
    "colorful_infographic": "Clear icons, vibrant colors, readable text labels, organized layout for presentations.",
    "sketch": "Hand-drawn aesthetics, pencil/charcoal textures, schematic look, white background.",
    "photorealistic": "High-quality photo look, realistic textures, depth of field, cinematic lighting.",
    "minimalist": "Negative space, simple geometric shapes, limited color palette, clean design.",
    "claymation": "3D clay texture, soft lighting, playful look.",
    "pixel_art": "Retro game style, blocky, limited color palette."
}


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY required")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def refine_prompt(client, topic, style):
    """Generate optimized image generation prompt."""
    style_guide = STYLE_GUIDELINES.get(style, STYLE_GUIDELINES["colorful_infographic"])
    preview = topic[:100] + "..." if len(topic) > 100 else topic
    print(f"Generating prompt for: '{preview}' with style: '{style}'")
    
    meta_prompt = f"""Create a detailed image generation prompt for an infographic/diagram.

Input Topic: {topic}
Target Style: {style} - {style_guide}

Instructions:
1. Analyze input and identify key concepts to visualize
2. Create prompt with: Subject, Composition, Style, Lighting
3. If Japanese text requested, include Japanese characters in output
4. Focus on clarity and visual hierarchy

Output ONLY the prompt text in English."""

    response = client.models.generate_content(model=FLASH_MODEL, contents=[meta_prompt])
    return response.text.strip()


def generate_image(client, prompt, output_path, aspect_ratio="16:9"):
    """Generate image using Gemini Image API."""
    print(f"Generating image ({aspect_ratio})...")
    
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio=aspect_ratio, image_size="2K")
        )
    )
    
    for part in response.parts:
        if part.inline_data:
            result_image = types.Part.as_image(part)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            result_image.save(output_path)
            print(f"✅ Diagram saved: {output_path}")
            return True
    
    print("Error: No image generated")
    return False


def main():
    parser = argparse.ArgumentParser(description="Generate diagrams from text")
    parser.add_argument("topic", nargs='+', help="Topic or text to visualize")
    parser.add_argument("--style", "-s", default="colorful_infographic",
                       choices=list(STYLE_GUIDELINES.keys()))
    parser.add_argument("--aspect_ratio", "-a", default="16:9",
                       choices=["16:9", "1:1", "4:3", "3:4", "9:16", "21:9"])
    parser.add_argument("--output", "-o", help="Output path")
    args = parser.parse_args()
    
    topic = " ".join(args.topic)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if args.output:
        output_path = Path(args.output)
    else:
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c if c.isalnum() else "_" for c in topic[:30])
        output_path = DEFAULT_OUTPUT_DIR / f"diagram_{safe_name}_{timestamp}.png"
    
    client = get_client()
    prompt = refine_prompt(client, topic, args.style)
    generate_image(client, prompt, output_path, args.aspect_ratio)


if __name__ == "__main__":
    main()





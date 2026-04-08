#!/usr/bin/env python3
"""
Nano Banana Pro - Image generation and editing using Gemini Image API.
"""
import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.utils.path_validator import validate_path

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


IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "nano-banana-pro-preview")
DEFAULT_OUTPUT_DIR = Path("output/generated")


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY required")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def get_aspect_ratio(width, height):
    """Calculate aspect ratio string from dimensions."""
    ar = width / height
    if ar > 1.9: return "21:9"
    elif ar > 1.5: return "16:9"
    elif ar > 1.2: return "4:3"
    elif ar > 0.9: return "1:1"
    elif ar > 0.7: return "3:4"
    else: return "9:16"


def sanitize_filename(name):
    """Sanitize string for use in filename."""
    name = name.replace(" ", "_")
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name[:50]


def generate_image(client, prompt, output_path, aspect_ratio="16:9"):
    """Generate image from text prompt."""
    print(f"Generating image...")
    print(f"Prompt: {prompt}")
    
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
            print(f"✅ Generated: {output_path}")
            return True
    return False


def edit_image(client, input_paths, prompt, output_path, aspect_ratio="16:9", force_ar=False):
    """Edit image(s) with prompt."""
    input_images = []
    ar_str = aspect_ratio
    
    for i, path in enumerate(input_paths):
        print(f"Loading image {i+1}: {path}")
        img = Image.open(path)
        if i == 0 and not force_ar:
            ar_str = get_aspect_ratio(*img.size)
        input_images.append(img)
    
    print(f"Editing with {len(input_images)} image(s)...")
    print(f"Prompt: {prompt}")
    
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[prompt] + input_images,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio=ar_str, image_size="2K")
        )
    )
    
    for part in response.parts:
        if part.inline_data:
            result_image = types.Part.as_image(part)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            result_image.save(output_path)
            print(f"✅ Edited: {output_path}")
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Generate or edit images")
    parser.add_argument("prompt", nargs='+', help="Generation/edit instruction")
    parser.add_argument("--input", "-i", action='append', help="Input image(s)")
    parser.add_argument("--output", "-o", help="Output path")
    parser.add_argument("--aspect-ratio", "-ar", default="16:9",
                       choices=["1:1", "4:3", "3:4", "16:9", "9:16", "21:9"])
    parser.add_argument("--force-ar", "-far", action='store_true')
    parser.add_argument("--session", "-s", help="Session name")
    args = parser.parse_args()
    
    prompt = " ".join(args.prompt)
    client = get_client()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if args.input:
        # Edit mode
        input_paths = [
            validate_path(p, must_exist=True, must_be_file=True)
            for p in args.input
        ]
        
        output_path = (
            validate_path(args.output, must_exist=False)
            if args.output
            else validate_path(
                input_paths[0].parent / f"{input_paths[0].stem}_edited.png",
                must_exist=False,
            )
        )
        edit_image(client, input_paths, prompt, output_path, args.aspect_ratio, args.force_ar)
    else:
        # Generate mode
        if args.output:
            output_path = validate_path(args.output, must_exist=False)
        else:
            if args.session:
                safe_session = sanitize_filename(args.session)
                output_dir = DEFAULT_OUTPUT_DIR / f"{datetime.now().strftime('%Y%m%d')}_{safe_session}"
                output_path = output_dir / f"{safe_session}_{timestamp}.png"
            else:
                output_path = DEFAULT_OUTPUT_DIR / f"generated_{timestamp}.png"
            output_path = validate_path(output_path, must_exist=False)
        
        generate_image(client, prompt, output_path, args.aspect_ratio)


if __name__ == "__main__":
    main()





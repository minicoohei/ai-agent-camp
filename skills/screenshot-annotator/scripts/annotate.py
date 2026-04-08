#!/usr/bin/env python3
"""
Screenshot Annotator - Add annotations to screenshots using Gemini Vision API.
Original image is NEVER modified - annotations are overlays only.
"""
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

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


FLASH_MODEL = os.environ.get("GEMINI_FLASH_MODEL", "gemini-3-flash-preview")
IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "nano-banana-pro-preview")

STYLE_GUIDELINES = {
    "red_box": "Draw a bold red rectangular box (3-5px thick) around the target element. Add a red arrow pointing to the box.",
    "arrow": "Draw a prominent red arrow pointing directly to the target element. Thick (8-12px) with clear arrowhead.",
    "callout": "Add a speech bubble near the target element with the specified text. White background with red/black border.",
    "highlight": "Add a semi-transparent yellow highlight overlay on the target element.",
    "circle": "Draw a bold red circle around the target element.",
    "number": "Add a numbered marker (circled number) next to the target element."
}


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY required")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def refine_prompt(client, instruction, text_label, style):
    """Generate optimized prompt for annotation."""
    style_instruction = STYLE_GUIDELINES.get(style, STYLE_GUIDELINES["red_box"])
    text_instruction = f'Add text label "{text_label}" near the annotation in readable sans-serif font.' if text_label else ""
    
    meta_prompt = f"""Create a prompt for adding annotations to a screenshot.
    
CRITICAL: Original image MUST remain COMPLETELY UNCHANGED.
- DO NOT modify any pixel of the original image
- ONLY add annotation overlays on top

ANNOTATION REQUEST: {instruction}
STYLE: {style_instruction}
{text_instruction}

Output ONLY the final prompt text."""

    response = client.models.generate_content(model=FLASH_MODEL, contents=[meta_prompt])
    return response.text.strip()


def annotate_image(client, input_path, prompt, output_path):
    """Add annotations to image using Gemini Vision API."""
    input_image = Image.open(input_path)
    width, height = input_image.size
    
    # Calculate aspect ratio
    ar = width / height
    ar_str = "21:9" if ar > 1.9 else "16:9" if ar > 1.5 else "4:3" if ar > 1.2 else "1:1" if ar > 0.9 else "3:4" if ar > 0.7 else "9:16"
    
    full_prompt = f"CRITICAL: Keep original image EXACTLY as-is. ONLY add annotation overlays.\n\n{prompt}"
    
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[full_prompt, input_image],
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
            print(f"✅ Annotated image saved: {output_path}")
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Add annotations to screenshots")
    parser.add_argument("input", help="Path to screenshot")
    parser.add_argument("instruction", nargs='*', help="What to annotate")
    parser.add_argument("--text", "-t", help="Text label to add")
    parser.add_argument("--style", "-s", default="red_box", 
                       choices=["red_box", "arrow", "callout", "highlight", "circle", "number"])
    parser.add_argument("--output", "-o", help="Output path")
    args = parser.parse_args()
    
    input_path = validate_path(args.input, must_exist=True, must_be_file=True)
    
    instruction = " ".join(args.instruction) if args.instruction else ""
    if not instruction:
        print("Error: No annotation instruction provided")
        sys.exit(1)
    
    output_path = (
        validate_path(args.output, must_exist=False)
        if args.output
        else validate_path(input_path.parent / f"{input_path.stem}_annotated.png", must_exist=False)
    )
    
    if output_path.resolve() == input_path.resolve():
        print("Error: Output cannot be same as input")
        sys.exit(1)
    
    client = get_client()
    prompt = refine_prompt(client, instruction, args.text, args.style)
    annotate_image(client, input_path, prompt, output_path)


if __name__ == "__main__":
    main()





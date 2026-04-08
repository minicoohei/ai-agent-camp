#!/usr/bin/env python3
"""
Tutorial Generator - Generate operation tutorials from screenshots using Gemini Vision API.
"""
import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from google import genai
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


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY required")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def analyze_screenshot(client, image_path, context=""):
    """Analyze screenshot and generate tutorial steps."""
    image = Image.open(image_path)
    
    context_text = f"\nAdditional context: {context}" if context else ""
    
    prompt = f"""Analyze this screenshot and generate a step-by-step operation tutorial.
{context_text}

Output as JSON with this structure:
{{
  "title": "Screen/Page title",
  "overview": "Brief description of what this screen is for",
  "steps": [
    {{
      "step": 1,
      "action": "What to do (e.g., Click the Login button)",
      "location": "Where the element is (e.g., top-right corner)",
      "description": "Why/additional details"
    }}
  ],
  "tips": ["Helpful tips or warnings"]
}}

Focus on:
- Identify all interactive elements (buttons, inputs, links, menus)
- Determine logical operation order
- Use clear, actionable language
- Include element locations for clarity"""

    response = client.models.generate_content(model=FLASH_MODEL, contents=[prompt, image])
    text = response.text.strip()
    
    # Extract JSON from response
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        return json.loads(json_match.group())
    return {"title": "Tutorial", "overview": "", "steps": [], "tips": []}


def generate_html(tutorial_data, image_path, output_path):
    """Generate HTML tutorial from analyzed data."""
    image_b64 = base64.b64encode(Path(image_path).read_bytes()).decode()
    ext = Path(image_path).suffix.lower().replace('.', '')
    mime = f"image/{'jpeg' if ext in ['jpg', 'jpeg'] else ext}"
    
    steps_html = ""
    for step in tutorial_data.get("steps", []):
        steps_html += f"""
        <div class="step">
            <div class="step-number">{step.get('step', '')}</div>
            <div class="step-content">
                <h3>{step.get('action', '')}</h3>
                <p class="location">📍 {step.get('location', '')}</p>
                <p>{step.get('description', '')}</p>
            </div>
        </div>"""
    
    tips_html = "".join(f"<li>{tip}</li>" for tip in tutorial_data.get("tips", []))
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tutorial_data.get('title', 'Tutorial')}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; background: #f5f5f5; padding: 2rem; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 2rem; }}
        h1 {{ color: #333; margin-bottom: 0.5rem; }}
        .overview {{ color: #666; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #eee; }}
        .screenshot {{ text-align: center; margin: 2rem 0; }}
        .screenshot img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 8px; }}
        .steps {{ margin: 2rem 0; }}
        .step {{ display: flex; gap: 1rem; margin-bottom: 1.5rem; padding: 1rem; background: #f9f9f9; border-radius: 8px; }}
        .step-number {{ width: 40px; height: 40px; background: #4A90E2; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }}
        .step-content h3 {{ color: #333; margin-bottom: 0.5rem; }}
        .location {{ color: #888; font-size: 0.9rem; margin-bottom: 0.5rem; }}
        .tips {{ background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 1rem; margin-top: 2rem; }}
        .tips h3 {{ color: #856404; margin-bottom: 0.5rem; }}
        .tips ul {{ margin-left: 1.5rem; color: #856404; }}
        .generated {{ text-align: center; color: #999; font-size: 0.8rem; margin-top: 2rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{tutorial_data.get('title', 'Tutorial')}</h1>
        <p class="overview">{tutorial_data.get('overview', '')}</p>
        <div class="screenshot">
            <img src="data:{mime};base64,{image_b64}" alt="Screenshot">
        </div>
        <div class="steps">
            <h2>📋 操作手順</h2>
            {steps_html}
        </div>
        {"<div class='tips'><h3>💡 ヒント</h3><ul>" + tips_html + "</ul></div>" if tips_html else ""}
        <p class="generated">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
</body>
</html>"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ Tutorial saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate operation tutorial from screenshot")
    parser.add_argument("screenshot", help="Path to screenshot")
    parser.add_argument("--output", "-o", help="Output HTML path")
    parser.add_argument("--context", "-c", help="Additional context about the screen")
    args = parser.parse_args()
    
    image_path = validate_path(args.screenshot, must_exist=True, must_be_file=True)
    
    output_path = (
        validate_path(args.output, must_exist=False)
        if args.output
        else validate_path(image_path.parent / f"{image_path.stem}_tutorial.html", must_exist=False)
    )
    
    client = get_client()
    print(f"Analyzing screenshot: {image_path}")
    tutorial_data = analyze_screenshot(client, image_path, args.context or "")
    generate_html(tutorial_data, image_path, output_path)


if __name__ == "__main__":
    main()





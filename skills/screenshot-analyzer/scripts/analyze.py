#!/usr/bin/env python3
"""
Screenshot Analyzer - Analyze screenshots for error diagnosis or tutorial generation.
"""
import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google import genai
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


FLASH_MODEL = os.environ.get("GEMINI_FLASH_MODEL", "gemini-3-flash-preview")
DEFAULT_OUTPUT_DIR = Path("output/analysis")


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY required")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def analyze_for_errors(client, image_path):
    """Analyze screenshot for errors and solutions."""
    image = Image.open(image_path)
    
    prompt = """Analyze this screenshot for errors or issues.

Output JSON:
{
    "description": "What is shown in the image",
    "has_error": true/false,
    "error_details": {
        "error_message": "Error message if visible",
        "error_type": "Type of error",
        "location": "Where in the image",
        "cause": "Likely cause"
    },
    "suggestions": ["Solution 1", "Solution 2"],
    "next_steps": ["Step 1", "Step 2"]
}"""

    response = client.models.generate_content(model=FLASH_MODEL, contents=[prompt, image])
    text = response.text.strip()
    
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        return json.loads(json_match.group())
    return {"description": "Analysis failed", "has_error": False, "suggestions": []}


def analyze_for_tutorial(client, image_path):
    """Analyze screenshot for operation tutorial."""
    image = Image.open(image_path)
    
    prompt = """Analyze this screenshot and create operation tutorial steps.

Output JSON:
{
    "title": "Screen title",
    "overview": "What this screen is for",
    "steps": [
        {"step": 1, "action": "What to do", "location": "Where", "description": "Details"}
    ],
    "tips": ["Helpful tips"]
}"""

    response = client.models.generate_content(model=FLASH_MODEL, contents=[prompt, image])
    text = response.text.strip()
    
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        return json.loads(json_match.group())
    return {"title": "Tutorial", "overview": "", "steps": [], "tips": []}


def generate_analyze_html(data, image_path, output_path):
    """Generate HTML for error analysis."""
    image_b64 = base64.b64encode(Path(image_path).read_bytes()).decode()
    
    error_html = ""
    if data.get("has_error") and data.get("error_details"):
        ed = data["error_details"]
        error_html = f"""
        <div class="error-box">
            <h3>🚨 エラー検出</h3>
            <p><strong>メッセージ:</strong> {ed.get('error_message', 'N/A')}</p>
            <p><strong>種類:</strong> {ed.get('error_type', 'N/A')}</p>
            <p><strong>場所:</strong> {ed.get('location', 'N/A')}</p>
            <p><strong>原因:</strong> {ed.get('cause', 'N/A')}</p>
        </div>"""
    
    suggestions = "".join(f"<li>{s}</li>" for s in data.get("suggestions", []))
    next_steps = "".join(f"<li>{s}</li>" for s in data.get("next_steps", []))
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>スクリーンショット解析</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 2rem; background: #f5f5f5; }}
        .container {{ background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }}
        .screenshot {{ text-align: center; margin: 2rem 0; }}
        .screenshot img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 8px; }}
        .error-box {{ background: #fee; border: 1px solid #fcc; border-radius: 8px; padding: 1rem; margin: 1rem 0; }}
        .suggestions {{ background: #e8f5e9; border-radius: 8px; padding: 1rem; margin: 1rem 0; }}
        .next-steps {{ background: #e3f2fd; border-radius: 8px; padding: 1rem; margin: 1rem 0; }}
        ul {{ margin-left: 1.5rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 スクリーンショット解析</h1>
        <p>{data.get('description', '')}</p>
        <div class="screenshot"><img src="data:image/png;base64,{image_b64}" alt="Screenshot"></div>
        {error_html}
        {"<div class='suggestions'><h3>💡 解決策</h3><ul>" + suggestions + "</ul></div>" if suggestions else ""}
        {"<div class='next-steps'><h3>▶️ 次のステップ</h3><ul>" + next_steps + "</ul></div>" if next_steps else ""}
        <p style="color:#999;text-align:center;margin-top:2rem;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
</body>
</html>"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ Analysis saved: {output_path}")


def generate_tutorial_html(data, image_path, output_path):
    """Generate HTML for tutorial."""
    image_b64 = base64.b64encode(Path(image_path).read_bytes()).decode()
    
    steps_html = ""
    for step in data.get("steps", []):
        steps_html += f"""
        <div class="step">
            <div class="step-num">{step.get('step', '')}</div>
            <div class="step-content">
                <h3>{step.get('action', '')}</h3>
                <p class="location">📍 {step.get('location', '')}</p>
                <p>{step.get('description', '')}</p>
            </div>
        </div>"""
    
    tips = "".join(f"<li>{t}</li>" for t in data.get("tips", []))
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{data.get('title', 'Tutorial')}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 2rem; background: #f5f5f5; }}
        .container {{ background: white; border-radius: 12px; padding: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }}
        .overview {{ color: #666; border-bottom: 1px solid #eee; padding-bottom: 1rem; margin-bottom: 2rem; }}
        .screenshot {{ text-align: center; margin: 2rem 0; }}
        .screenshot img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 8px; }}
        .step {{ display: flex; gap: 1rem; margin: 1rem 0; padding: 1rem; background: #f9f9f9; border-radius: 8px; }}
        .step-num {{ width: 40px; height: 40px; background: #4A90E2; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }}
        .step-content h3 {{ margin: 0 0 0.5rem 0; color: #333; }}
        .location {{ color: #888; font-size: 0.9rem; }}
        .tips {{ background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 1rem; margin-top: 2rem; }}
        .tips ul {{ margin-left: 1.5rem; color: #856404; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{data.get('title', 'Tutorial')}</h1>
        <p class="overview">{data.get('overview', '')}</p>
        <div class="screenshot"><img src="data:image/png;base64,{image_b64}" alt="Screenshot"></div>
        <h2>📋 操作手順</h2>
        {steps_html}
        {"<div class='tips'><h3>💡 ヒント</h3><ul>" + tips + "</ul></div>" if tips else ""}
        <p style="color:#999;text-align:center;margin-top:2rem;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
</body>
</html>"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ Tutorial saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Analyze screenshots")
    parser.add_argument("screenshot", help="Path to screenshot")
    parser.add_argument("--mode", "-m", default="analyze", choices=["analyze", "tutorial"])
    parser.add_argument("--output", "-o", help="Output HTML path")
    parser.add_argument("--no-annotate", action="store_true", help="Skip annotation")
    args = parser.parse_args()
    
    image_path = validate_path(args.screenshot, must_exist=True, must_be_file=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = (
        validate_path(args.output, must_exist=False)
        if args.output
        else validate_path(DEFAULT_OUTPUT_DIR / f"{args.mode}_{timestamp}.html", must_exist=False)
    )
    
    client = get_client()
    print(f"Analyzing: {image_path} (mode: {args.mode})")
    
    if args.mode == "analyze":
        data = analyze_for_errors(client, image_path)
        generate_analyze_html(data, image_path, output_path)
    else:
        data = analyze_for_tutorial(client, image_path)
        generate_tutorial_html(data, image_path, output_path)


if __name__ == "__main__":
    main()





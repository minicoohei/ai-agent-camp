"""
Banner Creator - 広告バナー/クリエイティブ生成ツール

各種SNS・広告プラットフォーム向けのバナー/クリエイティブを生成します。
- プラットフォーム別プリセット（X, Facebook, Instagram, PRタイムズ, YouTube, LINE, Web広告）
- トーン・スタイル設定
- 参考画像検索/指定
- コピーテキスト同時生成

NOTE: This is a copy for Claude Skill. Main script is at tools/banner_creator.py
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
import requests

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.utils.path_validator import validate_path

# .envファイルを読み込む
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


# デフォルトの保存先
DEFAULT_OUTPUT_DIR = Path("docs/generated/banners")

# Gemini モデル設定
DEFAULT_FLASH_MODEL = "gemini-3-flash-preview"
DEFAULT_IMAGE_MODEL = "nano-banana-pro-preview"


def get_client():
    """Google GenAI クライアントを初期化して返す"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def get_flash_model() -> str:
    return os.environ.get("GEMINI_FLASH_MODEL", DEFAULT_FLASH_MODEL)


def get_image_model() -> str:
    return os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_IMAGE_MODEL)


# =============================================================================
# プラットフォーム別プリセット
# =============================================================================
PLATFORM_PRESETS: Dict[str, Dict] = {
    "x_post": {
        "name": "X (Twitter) - タイムライン投稿",
        "width": 1200, "height": 675, "aspect_ratio": "16:9",
        "description": "Xのタイムラインで最適に表示される横長バナー"
    },
    "x_card": {
        "name": "X (Twitter) - カード表示",
        "width": 800, "height": 418, "aspect_ratio": "16:9",
        "description": "リンクカードとして表示されるサイズ"
    },
    "facebook": {
        "name": "Facebook - リンク投稿",
        "width": 1200, "height": 630, "aspect_ratio": "16:9",
        "description": "Facebookのリンク投稿に最適なサイズ"
    },
    "facebook_story": {
        "name": "Facebook - ストーリーズ",
        "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "description": "Facebookストーリーズ向け縦長フォーマット"
    },
    "instagram_feed": {
        "name": "Instagram - フィード投稿",
        "width": 1080, "height": 1080, "aspect_ratio": "1:1",
        "description": "Instagramフィードの正方形投稿"
    },
    "instagram_story": {
        "name": "Instagram - ストーリーズ",
        "width": 1080, "height": 1920, "aspect_ratio": "9:16",
        "description": "Instagramストーリーズ向け縦長フォーマット"
    },
    "prtimes": {
        "name": "PRタイムズ - プレスリリース",
        "width": 1200, "height": 630, "aspect_ratio": "16:9",
        "description": "PRタイムズのプレスリリース用画像"
    },
    "youtube": {
        "name": "YouTube - サムネイル",
        "width": 1280, "height": 720, "aspect_ratio": "16:9",
        "description": "YouTubeサムネイル用の横長画像"
    },
    "line": {
        "name": "LINE - リッチメッセージ",
        "width": 1040, "height": 1040, "aspect_ratio": "1:1",
        "description": "LINE公式アカウントのリッチメッセージ用"
    },
    "web_horizontal": {
        "name": "Web広告 - 横長",
        "width": 1200, "height": 628, "aspect_ratio": "16:9",
        "description": "ディスプレイ広告向け横長バナー"
    },
    "web_vertical": {
        "name": "Web広告 - 縦長",
        "width": 300, "height": 600, "aspect_ratio": "9:16",
        "description": "サイドバー向け縦長バナー"
    },
}

# =============================================================================
# トーン・色味・フォント・優先度設定
# =============================================================================
TONE_PROMPTS: Dict[str, str] = {
    "professional": "ビジネス向けのプロフェッショナルで信頼感のあるデザイン。",
    "casual": "親しみやすくフレンドリーな雰囲気。",
    "pop": "明るく楽しいポップなデザイン。若者向けでエネルギッシュ。",
    "elegant": "高級感と洗練された印象を与えるエレガントなデザイン。",
    "urgent": "緊急感・限定感を演出。セール、キャンペーン向け。",
    "minimal": "シンプルで余白を活かしたミニマルデザイン。",
    "tech": "先進的でデジタル感のあるテックスタイル。",
    "natural": "自然でオーガニックな雰囲気。アースカラー基調。",
}

COLOR_SCHEME_PROMPTS: Dict[str, str] = {
    "warm": "赤、オレンジ、黄色など暖色系。",
    "cool": "青、緑、紫など寒色系。",
    "mono": "白、黒、グレーのモノトーン。",
    "pastel": "淡いパステルカラー。",
    "vivid": "鮮やかな原色。",
    "dark": "黒やダークグレー基調。",
    "auto": "AIが最適なカラースキームを自動選択。",
}

FONT_STYLE_PROMPTS: Dict[str, str] = {
    "gothic": "モダンで読みやすいゴシック体。",
    "mincho": "伝統的で格式高い明朝体。",
    "handwritten": "手書き風フォント。親しみやすい。",
    "bold": "太字でインパクトのあるフォント。",
    "script": "流れるようなスクリプト体。",
    "geometric": "幾何学的でモダンなフォント。",
    "auto": "AIが最適なフォントスタイルを自動選択。",
}

PRIORITY_PROMPTS: Dict[str, str] = {
    "ctr": "クリック率を最大化。目立つCTAボタン、視線誘導。",
    "brand": "ブランド認知を高める。ロゴや企業名を強調。",
    "info": "情報を正確に伝える。テキストの読みやすさ重視。",
    "emotion": "感情に訴えかける。共感や感動を呼ぶビジュアル。",
    "product": "商品を魅力的に見せる。商品画像を際立たせる。",
    "event": "イベント告知。日時・場所を明確に表示。",
}


def sanitize_filename(name: str) -> str:
    name = name.replace(" ", "_")
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name[:50]


def build_banner_prompt(
    message: str,
    platform: str,
    tone: str = "professional",
    color_scheme: str = "auto",
    font_style: str = "auto",
    priority: str = "ctr",
    sub_copy: Optional[str] = None,
    cta: Optional[str] = None,
    brand_name: Optional[str] = None,
) -> str:
    preset = PLATFORM_PRESETS.get(platform, PLATFORM_PRESETS["x_post"])
    tone_desc = TONE_PROMPTS.get(tone, TONE_PROMPTS["professional"])
    priority_desc = PRIORITY_PROMPTS.get(priority, PRIORITY_PROMPTS["ctr"])
    
    if color_scheme.startswith("#"):
        color_desc = f"ブランドカラー {color_scheme} を基調。"
    else:
        color_desc = COLOR_SCHEME_PROMPTS.get(color_scheme, COLOR_SCHEME_PROMPTS["auto"])
    
    font_desc = FONT_STYLE_PROMPTS.get(font_style, FONT_STYLE_PROMPTS["auto"])
    
    prompt_parts = [
        f"Create a professional advertising banner for {preset['name']}.",
        f"Size: {preset['width']}x{preset['height']} pixels, aspect ratio {preset['aspect_ratio']}.",
        "",
        "=== MAIN MESSAGE ===",
        f'Main headline (in Japanese): "{message}"',
    ]
    
    if sub_copy:
        prompt_parts.append(f'Sub-headline: "{sub_copy}"')
    if cta:
        prompt_parts.append(f'Call-to-action button: "{cta}"')
    if brand_name:
        prompt_parts.append(f'Brand name to display: "{brand_name}"')
    
    prompt_parts.extend([
        "",
        "=== DESIGN SPECIFICATIONS ===",
        f"Tone: {tone_desc}",
        f"Color scheme: {color_desc}",
        f"Font style: {font_desc}",
        f"Design priority: {priority_desc}",
        "",
        "=== IMPORTANT REQUIREMENTS ===",
        "- All text must be in Japanese",
        "- Text must be clearly readable (minimum 14pt equivalent)",
        "- Use clean, modern layout with proper spacing",
        "- The main message should be the most prominent element",
        "- Do NOT include any placeholder text",
    ])
    
    return "\n".join(prompt_parts)


def generate_copy_text(
    client,
    message: str,
    platform: str,
    tone: str = "professional",
    sub_copy: Optional[str] = None,
    cta: Optional[str] = None,
    brand_name: Optional[str] = None,
) -> Dict:
    preset = PLATFORM_PRESETS.get(platform, PLATFORM_PRESETS["x_post"])
    
    prompt = f"""
あなたは広告コピーライターです。以下の情報を元に、{preset['name']}向けの投稿テキストを生成してください。

【バナーの内容】
- メインメッセージ: {message}
- サブコピー: {sub_copy or "なし"}
- CTA: {cta or "なし"}
- ブランド名: {brand_name or "なし"}
- トーン: {tone}

【出力形式】
以下のJSON形式で出力してください（必ずJSONのみを出力）:
{{
    "post_texts": ["投稿文案1", "投稿文案2", "投稿文案3"],
    "hashtags": ["#ハッシュタグ1", "#ハッシュタグ2", "#ハッシュタグ3", "#ハッシュタグ4", "#ハッシュタグ5"],
    "cta_phrases": ["CTAフレーズ1", "CTAフレーズ2", "CTAフレーズ3"]
}}
"""

    try:
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=[prompt],
        )
        
        response_text = response.text.strip()
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {"post_texts": [message], "hashtags": [], "cta_phrases": []}
            
    except Exception as e:
        print(f"Warning: Failed to generate copy text: {e}")
        return {"post_texts": [message], "hashtags": [], "cta_phrases": []}


def save_copy_text(copy_data: Dict, output_path: Path) -> Path:
    copy_path = output_path.with_suffix('.md').parent / f"{output_path.stem}_copy.md"
    
    content_parts = [
        "# 投稿用コピーテキスト",
        "",
        f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 投稿文案",
        "",
    ]
    
    for i, text in enumerate(copy_data.get("post_texts", []), 1):
        content_parts.extend([f"### パターン{i}", "", text, ""])
    
    if copy_data.get("hashtags"):
        content_parts.extend(["## ハッシュタグ", "", " ".join(copy_data["hashtags"]), ""])
    
    if copy_data.get("cta_phrases"):
        content_parts.append("## CTAフレーズ")
        content_parts.append("")
        for phrase in copy_data["cta_phrases"]:
            content_parts.append(f"- {phrase}")
        content_parts.append("")
    
    copy_path.write_text("\n".join(content_parts), encoding="utf-8")
    return copy_path


def download_reference_image(url: str, output_dir: Path) -> Optional[Path]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        ext = ".jpg"
        if "png" in url.lower():
            ext = ".png"
        
        ref_path = output_dir / f"reference_{datetime.now().strftime('%H%M%S')}{ext}"
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_bytes(response.content)
        
        print(f"✅ Downloaded reference image: {ref_path}")
        return ref_path
        
    except Exception as e:
        print(f"Warning: Failed to download reference image: {e}")
        return None


def generate_banner(
    client,
    prompt: str,
    output_path: Path,
    aspect_ratio: str = "16:9",
    reference_image: Optional[Path] = None,
) -> bool:
    print(f"\n{'='*60}")
    print("Banner Creator - 広告バナー生成")
    print('='*60)
    print(f"\nGenerating banner with Nano Banana Pro...")
    print(f"Aspect ratio: {aspect_ratio}")
    
    try:
        contents = [prompt]
        
        if reference_image and reference_image.exists():
            ref_img = Image.open(reference_image)
            contents.append(ref_img)
            print("Using reference image for generation...")
        
        response = client.models.generate_content(
            model=get_image_model(),
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size="2K"
                )
            )
        )
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    result_image = types.Part.as_image(part)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    result_image.save(output_path)
                    print(f"\n✅ Banner saved to: {output_path}")
                    return True
        
        print("❌ No image data found in the response.")
        return False
        
    except Exception as e:
        print(f"❌ Error generating banner: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate advertising banners for various platforms."
    )
    
    parser.add_argument("--platform", "-p", required=True, choices=list(PLATFORM_PRESETS.keys()))
    parser.add_argument("--message", "-m", required=True)
    parser.add_argument("--sub-copy", "-sc")
    parser.add_argument("--cta", "-c")
    parser.add_argument("--tone", "-t", default="professional", choices=list(TONE_PROMPTS.keys()))
    parser.add_argument("--color-scheme", "-cs", default="auto")
    parser.add_argument("--font-style", "-fs", default="auto", choices=list(FONT_STYLE_PROMPTS.keys()))
    parser.add_argument("--priority", "-pr", default="ctr", choices=list(PRIORITY_PROMPTS.keys()))
    parser.add_argument("--brand-name", "-bn")
    parser.add_argument("--reference", "-r")
    parser.add_argument("--search-ref", "-sr")
    parser.add_argument("--session", "-s")
    parser.add_argument("--output", "-o")
    parser.add_argument("--with-copy", "-wc", action="store_true")
    parser.add_argument("--variants", "-v", type=int, default=1)
    
    args = parser.parse_args()
    
    client = get_client()
    if not client:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY not found.")
        sys.exit(1)
    
    preset = PLATFORM_PRESETS[args.platform]
    
    date_str = datetime.now().strftime('%Y%m%d')
    timestamp = datetime.now().strftime('%H%M%S')
    
    if args.output:
        output_path = validate_path(args.output, must_exist=False)
    else:
        if args.session:
            safe_session = sanitize_filename(args.session)
            output_dir = DEFAULT_OUTPUT_DIR / f"{date_str}_{safe_session}"
        else:
            output_dir = DEFAULT_OUTPUT_DIR / date_str
        
        output_name = f"{args.platform}_{timestamp}.png"
        output_path = output_dir / output_name
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    reference_image = None
    if args.reference:
        if args.reference.startswith("http"):
            reference_image = download_reference_image(args.reference, output_path.parent)
        else:
            reference_image = validate_path(args.reference, must_exist=True, must_be_file=True)
    
    for i in range(args.variants):
        if args.variants > 1:
            variant_output = output_path.parent / f"{output_path.stem}_v{i+1}.png"
        else:
            variant_output = output_path
        
        prompt = build_banner_prompt(
            message=args.message,
            platform=args.platform,
            tone=args.tone,
            color_scheme=args.color_scheme,
            font_style=args.font_style,
            priority=args.priority,
            sub_copy=args.sub_copy,
            cta=args.cta,
            brand_name=args.brand_name,
        )
        
        if args.variants > 1:
            print(f"\n--- Generating variant {i+1}/{args.variants} ---")
        
        generate_banner(
            client=client,
            prompt=prompt,
            output_path=variant_output,
            aspect_ratio=preset["aspect_ratio"],
            reference_image=reference_image,
        )
    
    if args.with_copy:
        print("\n--- Generating copy text ---")
        copy_data = generate_copy_text(
            client=client,
            message=args.message,
            platform=args.platform,
            tone=args.tone,
            sub_copy=args.sub_copy,
            cta=args.cta,
            brand_name=args.brand_name,
        )
        
        copy_path = save_copy_text(copy_data, output_path)
        print(f"\n✅ Copy text saved to: {copy_path}")
        
        print("\n" + "="*60)
        print("Generated Copy Text")
        print("="*60)
        
        print("\n📝 投稿文案:")
        for i, text in enumerate(copy_data.get("post_texts", []), 1):
            print(f"\n[パターン{i}]")
            print(text)
        
        if copy_data.get("hashtags"):
            print(f"\n#️⃣ ハッシュタグ: {' '.join(copy_data['hashtags'])}")
        
        if copy_data.get("cta_phrases"):
            print(f"\n🎯 CTAフレーズ: {', '.join(copy_data['cta_phrases'])}")
        
        print("\n" + "="*60)
    
    print("\n✨ Banner creation completed!")


if __name__ == "__main__":
    main()

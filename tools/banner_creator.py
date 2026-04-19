"""
Banner Creator - 広告バナー/クリエイティブ生成ツール

各種SNS・広告プラットフォーム向けのバナー/クリエイティブを生成します。
- プラットフォーム別プリセット（X, Facebook, Instagram, PRタイムズ, YouTube, LINE, Web広告）
- トーン・スタイル設定
- 参考画像検索/指定
- コピーテキスト同時生成
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from google import genai
from google.genai import types
from PIL import Image
import requests

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env
from bootcamp_utils import get_client, get_flash_model, get_image_model

load_runtime_env()

try:
    from i18n_common import setup_gettext
except ImportError:
    def setup_gettext():
        return lambda x: x

_ = setup_gettext()


# デフォルトの保存先
DEFAULT_OUTPUT_DIR = Path("docs/generated/banners")

# =============================================================================
# プラットフォーム別プリセット
# =============================================================================
PLATFORM_PRESETS: Dict[str, Dict] = {
    # X (Twitter)
    "x_post": {
        "name": "X (Twitter) - タイムライン投稿",
        "width": 1200,
        "height": 675,
        "aspect_ratio": "16:9",
        "description": "Xのタイムラインで最適に表示される横長バナー"
    },
    "x_card": {
        "name": "X (Twitter) - カード表示",
        "width": 800,
        "height": 418,
        "aspect_ratio": "16:9",  # 近似値
        "description": "リンクカードとして表示されるサイズ"
    },
    # Facebook
    "facebook": {
        "name": "Facebook - リンク投稿",
        "width": 1200,
        "height": 630,
        "aspect_ratio": "16:9",  # 近似値
        "description": "Facebookのリンク投稿に最適なサイズ"
    },
    "facebook_story": {
        "name": "Facebook - ストーリーズ",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "description": "Facebookストーリーズ向け縦長フォーマット"
    },
    # Instagram
    "instagram_feed": {
        "name": "Instagram - フィード投稿",
        "width": 1080,
        "height": 1080,
        "aspect_ratio": "1:1",
        "description": "Instagramフィードの正方形投稿"
    },
    "instagram_story": {
        "name": "Instagram - ストーリーズ",
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "description": "Instagramストーリーズ向け縦長フォーマット"
    },
    # その他プラットフォーム
    "prtimes": {
        "name": "PRタイムズ - プレスリリース",
        "width": 1200,
        "height": 630,
        "aspect_ratio": "16:9",
        "description": "PRタイムズのプレスリリース用画像"
    },
    "youtube": {
        "name": "YouTube - サムネイル",
        "width": 1280,
        "height": 720,
        "aspect_ratio": "16:9",
        "description": "YouTubeサムネイル用の横長画像"
    },
    "line": {
        "name": "LINE - リッチメッセージ",
        "width": 1040,
        "height": 1040,
        "aspect_ratio": "1:1",
        "description": "LINE公式アカウントのリッチメッセージ用"
    },
    "web_horizontal": {
        "name": "Web広告 - 横長",
        "width": 1200,
        "height": 628,
        "aspect_ratio": "16:9",
        "description": "ディスプレイ広告向け横長バナー"
    },
    "web_vertical": {
        "name": "Web広告 - 縦長",
        "width": 300,
        "height": 600,
        "aspect_ratio": "9:16",  # 近似値
        "description": "サイドバー向け縦長バナー"
    },
}

# =============================================================================
# トーン設定
# =============================================================================
TONE_PROMPTS: Dict[str, str] = {
    "professional": "ビジネス向けのプロフェッショナルで信頼感のあるデザイン。クリーンで洗練されたレイアウト。",
    "casual": "親しみやすくフレンドリーな雰囲気。リラックスした印象を与えるデザイン。",
    "pop": "明るく楽しいポップなデザイン。若者向けでエネルギッシュな印象。鮮やかな色使い。",
    "elegant": "高級感と洗練された印象を与えるエレガントなデザイン。上品な配色と余白の活用。",
    "urgent": "緊急感・限定感を演出するデザイン。セール、キャンペーン向け。目を引く配色とCTAの強調。",
    "minimal": "シンプルで余白を活かしたミニマルデザイン。必要最小限の要素で洗練された印象。",
    "tech": "先進的でデジタル感のあるテックスタイル。未来的なイメージ。グラデーションや幾何学的要素。",
    "natural": "自然でオーガニックな雰囲気。アースカラーを基調とした落ち着いたデザイン。",
}

# =============================================================================
# 色味設定
# =============================================================================
COLOR_SCHEME_PROMPTS: Dict[str, str] = {
    "warm": "赤、オレンジ、黄色など暖色系を基調としたカラースキーム。温かみのある印象。",
    "cool": "青、緑、紫など寒色系を基調としたカラースキーム。クールで知的な印象。",
    "mono": "白、黒、グレーのモノトーンカラースキーム。洗練されたシンプルな印象。",
    "pastel": "淡いパステルカラーを基調としたカラースキーム。優しく柔らかい印象。",
    "vivid": "鮮やかな原色を使ったビビッドなカラースキーム。インパクトのある目立つ配色。",
    "dark": "黒やダークグレーを基調としたダークカラースキーム。高級感とモダンな印象。",
    "auto": "内容に応じてAIが最適なカラースキームを自動選択。",
}

# =============================================================================
# フォントスタイル設定
# =============================================================================
FONT_STYLE_PROMPTS: Dict[str, str] = {
    "gothic": "モダンで読みやすいゴシック体フォント。クリーンで現代的な印象。",
    "mincho": "伝統的で格式高い明朝体フォント。フォーマルで高級感のある印象。",
    "handwritten": "手書き風のフォント。親しみやすく個性的な印象。人間味のあるデザイン。",
    "bold": "太字でインパクトのあるフォント。力強く目立つデザイン。見出しや強調に最適。",
    "script": "流れるようなスクリプト体フォント。エレガントで女性的な印象。",
    "geometric": "幾何学的でモダンなフォント。未来的でテック感のあるデザイン。",
    "auto": "内容とトーンに応じてAIが最適なフォントスタイルを自動選択。",
}

# =============================================================================
# 優先度（重要視する点）設定
# =============================================================================
PRIORITY_PROMPTS: Dict[str, str] = {
    "ctr": "クリック率を最大化するデザイン。目立つCTAボタン、視線を誘導するレイアウト、行動喚起を重視。",
    "brand": "ブランド認知を高めるデザイン。ロゴや企業名を目立たせ、ブランドカラーを効果的に使用。",
    "info": "情報を正確に伝えるデザイン。テキストの読みやすさ、情報の階層構造を重視。",
    "emotion": "感情に訴えかけるデザイン。共感や感動を呼ぶビジュアル、ストーリー性のある表現。",
    "product": "商品を魅力的に見せるデザイン。商品画像を際立たせ、特徴や価値を視覚的に伝える。",
    "event": "イベント告知に最適なデザイン。日時・場所を明確に表示、参加意欲を高める表現。",
}


def sanitize_filename(name: str) -> str:
    """ファイル名に使用できない文字を置換"""
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
    """バナー生成用のプロンプトを構築"""
    
    preset = PLATFORM_PRESETS.get(platform, PLATFORM_PRESETS["x_post"])
    tone_desc = TONE_PROMPTS.get(tone, TONE_PROMPTS["professional"])
    priority_desc = PRIORITY_PROMPTS.get(priority, PRIORITY_PROMPTS["ctr"])
    
    # 色味の処理（HEXコードの場合はそのまま使用）
    if color_scheme.startswith("#"):
        color_desc = f"ブランドカラー {color_scheme} を基調としたカラースキーム。この色をメインに使用。"
    else:
        color_desc = COLOR_SCHEME_PROMPTS.get(color_scheme, COLOR_SCHEME_PROMPTS["auto"])
    
    font_desc = FONT_STYLE_PROMPTS.get(font_style, FONT_STYLE_PROMPTS["auto"])
    
    # プロンプト構築
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
        "- Text must be clearly readable and properly sized (minimum 14pt equivalent)",
        "- Use clean, modern layout with proper spacing",
        "- The main message should be the most prominent element",
        "- Ensure visual hierarchy: headline > sub-copy > CTA > brand name",
        "- Do NOT include any placeholder text or lorem ipsum",
        "- The design should look professional and ready for immediate use",
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
    """投稿用コピーテキストを生成"""
    
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
    "post_texts": [
        "投稿文案1（最も推奨）",
        "投稿文案2（代替案）",
        "投稿文案3（代替案）"
    ],
    "hashtags": ["#ハッシュタグ1", "#ハッシュタグ2", "#ハッシュタグ3", "#ハッシュタグ4", "#ハッシュタグ5"],
    "cta_phrases": ["CTAフレーズ1", "CTAフレーズ2", "CTAフレーズ3"]
}}

【注意事項】
- 投稿文は{preset['name']}に適した長さと形式で
- ハッシュタグは関連性の高いものを5つ
- CTAフレーズは行動を促す短いフレーズを3つ
- 必ず有効なJSONのみを出力
"""

    try:
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=[prompt],
        )
        
        response_text = response.text.strip()
        
        # JSONを抽出
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {
                "post_texts": [f"{message}\n{sub_copy or ''}\n{cta or ''}"],
                "hashtags": [],
                "cta_phrases": [cta] if cta else []
            }
            
    except Exception as e:
        print(_("Warning: Failed to generate copy text: {err}").format(err=e))
        return {
            "post_texts": [message],
            "hashtags": [],
            "cta_phrases": []
        }


def save_copy_text(copy_data: Dict, output_path: Path) -> Path:
    """コピーテキストをMarkdownファイルとして保存"""
    
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
        content_parts.append(f"### パターン{i}")
        content_parts.append("")
        content_parts.append(text)
        content_parts.append("")
    
    if copy_data.get("hashtags"):
        content_parts.append("## ハッシュタグ")
        content_parts.append("")
        content_parts.append(" ".join(copy_data["hashtags"]))
        content_parts.append("")
    
    if copy_data.get("cta_phrases"):
        content_parts.append("## CTAフレーズ")
        content_parts.append("")
        for phrase in copy_data["cta_phrases"]:
            content_parts.append(f"- {phrase}")
        content_parts.append("")
    
    copy_path.write_text("\n".join(content_parts), encoding="utf-8")
    return copy_path


def download_reference_image(url: str, output_dir: Path) -> Optional[Path]:
    """URLから参考画像をダウンロード"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # ファイル名を生成
        ext = ".jpg"
        if "png" in url.lower():
            ext = ".png"
        elif "gif" in url.lower():
            ext = ".gif"
        
        ref_path = output_dir / f"reference_{datetime.now().strftime('%H%M%S')}{ext}"
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_bytes(response.content)
        
        print(_("✅ Downloaded reference image: {path}").format(path=ref_path))
        return ref_path

    except Exception as e:
        print(_("Warning: Failed to download reference image: {err}").format(err=e))
        return None


def generate_banner(
    client,
    prompt: str,
    output_path: Path,
    aspect_ratio: str = "16:9",
    reference_image: Optional[Path] = None,
) -> bool:
    """バナー画像を生成"""
    
    print(f"\n{'='*60}")
    print(_("Banner Creator - 広告バナー生成"))
    print('='*60)
    print(_("\nGenerating banner with Nano Banana Pro..."))
    print(_("Aspect ratio: {ratio}").format(ratio=aspect_ratio))

    if reference_image:
        print(_("Reference image: {path}").format(path=reference_image))
    
    try:
        contents = [prompt]
        
        # 参考画像がある場合は追加
        if reference_image and reference_image.exists():
            ref_img = Image.open(reference_image)
            contents.append(ref_img)
            print(_("Using reference image for generation..."))
        
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
        
        # 画像を保存
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    result_image = types.Part.as_image(part)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    result_image.save(output_path)
                    print(_("\n✅ Banner saved to: {path}").format(path=output_path))
                    return True

        print(_("❌ No image data found in the response."))
        return False

    except Exception as e:
        print(_("❌ Error generating banner: {err}").format(err=e))
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate advertising banners for various platforms using Nano Banana Pro."
    )
    
    # 必須引数
    parser.add_argument(
        "--platform", "-p",
        required=True,
        choices=list(PLATFORM_PRESETS.keys()),
        help="Target platform (e.g., x_post, instagram_feed, prtimes)"
    )
    parser.add_argument(
        "--message", "-m",
        required=True,
        help="Main headline/catchphrase for the banner"
    )
    
    # オプション引数
    parser.add_argument(
        "--sub-copy", "-sc",
        help="Sub-headline or additional text"
    )
    parser.add_argument(
        "--cta", "-c",
        help="Call-to-action text (e.g., '今すぐ登録')"
    )
    parser.add_argument(
        "--tone", "-t",
        default="professional",
        choices=list(TONE_PROMPTS.keys()),
        help="Banner tone/style (default: professional)"
    )
    parser.add_argument(
        "--color-scheme", "-cs",
        default="auto",
        help="Color scheme (warm, cool, mono, pastel, vivid, dark, auto, or HEX code like #FF5733)"
    )
    parser.add_argument(
        "--font-style", "-fs",
        default="auto",
        choices=list(FONT_STYLE_PROMPTS.keys()),
        help="Font style (default: auto)"
    )
    parser.add_argument(
        "--priority", "-pr",
        default="ctr",
        choices=list(PRIORITY_PROMPTS.keys()),
        help="Design priority (default: ctr)"
    )
    parser.add_argument(
        "--brand-name", "-bn",
        help="Brand or company name to display"
    )
    parser.add_argument(
        "--reference", "-r",
        help="Path or URL to reference image"
    )
    parser.add_argument(
        "--search-ref", "-sr",
        help="Keywords to search for reference images (not implemented in CLI, use in Cursor)"
    )
    parser.add_argument(
        "--session", "-s",
        help="Session name for organizing output"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    parser.add_argument(
        "--with-copy", "-wc",
        action="store_true",
        help="Also generate copy text (post texts, hashtags, CTAs)"
    )
    parser.add_argument(
        "--variants", "-v",
        type=int,
        default=1,
        help="Number of banner variations to generate (default: 1)"
    )
    
    args = parser.parse_args()
    
    # クライアント初期化
    client = get_client()
    if not client:
        print(_("Error: GEMINI_API_KEY or GOOGLE_API_KEY not found in environment."))
        sys.exit(1)
    
    # プリセット取得
    preset = PLATFORM_PRESETS[args.platform]
    
    # 出力パス決定
    date_str = datetime.now().strftime('%Y%m%d')
    timestamp = datetime.now().strftime('%H%M%S')
    
    if args.output:
        output_path = Path(args.output)
    else:
        if args.session:
            safe_session = sanitize_filename(args.session)
            output_dir = DEFAULT_OUTPUT_DIR / f"{date_str}_{safe_session}"
        else:
            output_dir = DEFAULT_OUTPUT_DIR / date_str
        
        output_name = f"{args.platform}_{timestamp}.png"
        output_path = output_dir / output_name
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 参考画像の処理
    reference_image = None
    if args.reference:
        if args.reference.startswith("http"):
            reference_image = download_reference_image(args.reference, output_path.parent)
        else:
            ref_path = Path(args.reference)
            if ref_path.exists():
                reference_image = ref_path
            else:
                print(_("Warning: Reference image not found: {path}").format(path=args.reference))
    
    # バナー生成
    for i in range(args.variants):
        if args.variants > 1:
            variant_output = output_path.parent / f"{output_path.stem}_v{i+1}.png"
        else:
            variant_output = output_path
        
        # プロンプト構築
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
            print(_("\n--- Generating variant {n}/{total} ---").format(n=i+1, total=args.variants))

        success = generate_banner(
            client=client,
            prompt=prompt,
            output_path=variant_output,
            aspect_ratio=preset["aspect_ratio"],
            reference_image=reference_image,
        )

        if not success:
            print(_("Failed to generate banner variant {n}").format(n=i+1))
    
    # コピーテキスト生成
    if args.with_copy:
        print(_("\n--- Generating copy text ---"))
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
        print(_("\n✅ Copy text saved to: {path}").format(path=copy_path))

        # コピーテキストをコンソールにも表示
        print("\n" + "="*60)
        print(_("Generated Copy Text"))
        print("="*60)

        print(_("\n📝 投稿文案:"))
        for i, text in enumerate(copy_data.get("post_texts", []), 1):
            print(_("\n[パターン{n}]").format(n=i))
            print(text)

        if copy_data.get("hashtags"):
            print(_("\n#️⃣ ハッシュタグ: {tags}").format(tags=' '.join(copy_data['hashtags'])))

        if copy_data.get("cta_phrases"):
            print(_("\n🎯 CTAフレーズ: {phrases}").format(phrases=', '.join(copy_data['cta_phrases'])))

        print("\n" + "="*60)

    print(_("\n✨ Banner creation completed!"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
バナー生成スクリプト（Final Example）

このスクリプトを実行すると、各プラットフォーム用のバナーを生成します。

必要条件:
- Gemini APIキー（環境変数 GEMINI_API_KEY）
- Python 3.9以上
- google-genai パッケージ

使用方法:
    python generate_banners.py --all
    python generate_banners.py --platform x_post --topic "AIで業務効率化"
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# プロジェクトルートのtoolsをインポートパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from tools.banner_creator import create_banner
    HAS_BANNER_CREATOR = True
except ImportError:
    HAS_BANNER_CREATOR = False
    print("Warning: banner_creator モジュールが見つかりません")

# プラットフォーム設定
PLATFORMS = {
    "x_post": {
        "size": (1200, 675),
        "description": "X（Twitter）投稿用",
        "aspect_ratio": "16:9"
    },
    "youtube_thumbnail": {
        "size": (1280, 720),
        "description": "YouTubeサムネイル",
        "aspect_ratio": "16:9"
    },
    "instagram_square": {
        "size": (1080, 1080),
        "description": "Instagram正方形",
        "aspect_ratio": "1:1"
    },
    "linkedin_cover": {
        "size": (1584, 396),
        "description": "LinkedInカバー",
        "aspect_ratio": "4:1"
    }
}

# サンプルトピック
SAMPLE_TOPICS = {
    "x_post": "AIエージェントで業務効率化を実現",
    "youtube_thumbnail": "【保存版】ChatGPT活用術10選",
    "instagram_square": "週末限定セール開催中",
    "linkedin_cover": "AIエージェント研修 - 2025"
}

# プロンプトテンプレート
PROMPT_TEMPLATES = {
    "x_post": """
X（Twitter）投稿用のバナー画像を生成してください。

トピック: {topic}
サイズ: 1200x675px (16:9)

デザイン要件:
- モダンでプロフェッショナルな印象
- 青と白を基調とした配色
- テキストは大きく読みやすく
- 背景にはテクノロジーを感じさせる抽象的なパターン
- 余白を適切に確保
""",
    
    "youtube_thumbnail": """
YouTubeサムネイル画像を生成してください。

トピック: {topic}
サイズ: 1280x720px (16:9)

デザイン要件:
- 目を引く鮮やかな配色
- 大きく太いフォントで視認性を確保
- 感嘆符やエフェクトで注目を集める
- 人物シルエットまたはアイコンを含める
- スマホでも読めるサイズのテキスト
""",
    
    "instagram_square": """
Instagram正方形投稿用の画像を生成してください。

トピック: {topic}
サイズ: 1080x1080px (1:1)

デザイン要件:
- クリーンでミニマルなデザイン
- パステルカラーまたはビビッドカラー
- 中央にメインビジュアル
- 日本語テキストは読みやすく
- トレンド感のあるスタイル
""",
    
    "linkedin_cover": """
LinkedInカバー画像を生成してください。

トピック: {topic}
サイズ: 1584x396px (4:1)

デザイン要件:
- ビジネスプロフェッショナルな印象
- 企業カラー（紺、グレー、白）
- シンプルで洗練されたデザイン
- 左側に余白を確保（プロフィール写真と重ならないよう）
- ロゴやアイコンは右寄せ
"""
}


def generate_banner(platform: str, topic: str, output_dir: Path) -> str:
    """バナーを生成"""
    if platform not in PLATFORMS:
        raise ValueError(f"Unknown platform: {platform}")
    
    config = PLATFORMS[platform]
    prompt = PROMPT_TEMPLATES[platform].format(topic=topic)
    
    output_path = output_dir / f"banner-{platform}.png"
    
    if HAS_BANNER_CREATOR:
        # 実際の生成
        result = create_banner(
            prompt=prompt,
            size=config["size"],
            output_path=str(output_path)
        )
        print(f"✅ 生成完了: {output_path}")
        return str(output_path)
    else:
        # プロンプトのみ出力（モック）
        prompt_file = output_dir / f"prompt-{platform}.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(f"# {config['description']} バナー生成プロンプト\n\n")
            f.write(f"サイズ: {config['size'][0]}x{config['size'][1]}px\n")
            f.write(f"アスペクト比: {config['aspect_ratio']}\n\n")
            f.write("---\n\n")
            f.write(prompt)
        
        print(f"📝 プロンプト保存: {prompt_file}")
        return str(prompt_file)


def generate_all(output_dir: Path):
    """全プラットフォームのバナーを生成"""
    print("=" * 50)
    print("バナー一括生成")
    print("=" * 50)
    
    results = []
    for platform, topic in SAMPLE_TOPICS.items():
        print(f"\n▶ {PLATFORMS[platform]['description']}")
        print(f"  トピック: {topic}")
        
        try:
            result = generate_banner(platform, topic, output_dir)
            results.append((platform, "成功", result))
        except Exception as e:
            results.append((platform, "失敗", str(e)))
            print(f"  ❌ エラー: {e}")
    
    print("\n" + "=" * 50)
    print("生成結果サマリー")
    print("=" * 50)
    for platform, status, path in results:
        print(f"  {platform}: {status}")
        if status == "成功":
            print(f"    → {path}")


def main():
    parser = argparse.ArgumentParser(description="バナー生成スクリプト")
    parser.add_argument("--all", action="store_true", help="全プラットフォームを生成")
    parser.add_argument("--platform", choices=PLATFORMS.keys(), help="プラットフォーム指定")
    parser.add_argument("--topic", type=str, help="トピック（--platform使用時）")
    parser.add_argument("--output", type=str, default=".", help="出力ディレクトリ")
    parser.add_argument("--list", action="store_true", help="利用可能なプラットフォームを表示")
    
    args = parser.parse_args()
    
    if args.list:
        print("利用可能なプラットフォーム:")
        for name, config in PLATFORMS.items():
            print(f"  {name}: {config['description']} ({config['size'][0]}x{config['size'][1]})")
        return
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.all:
        generate_all(output_dir)
    elif args.platform:
        topic = args.topic or SAMPLE_TOPICS.get(args.platform, "サンプルバナー")
        generate_banner(args.platform, topic, output_dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

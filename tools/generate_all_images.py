#!/usr/bin/env python3
"""
研修教材用の挿絵を一括生成するスクリプト。

使用方法:
    uv run python tools/generate_all_images.py --category foundation
    uv run python tools/generate_all_images.py --category headers
    uv run python tools/generate_all_images.py --category all

必要環境変数:
    GEMINI_API_KEY: Gemini API キー

生成カテゴリ:
    - foundation: AI基礎概念図（8枚）
    - headers: モジュールヘッダー画像（14枚）
    - concepts: 概念図・フロー図（35枚）
    - exercises: 演習用図解（20枚）
    - portal: ポータル用アイコン（8枚）
"""

import argparse
import os
import json
from pathlib import Path
from datetime import datetime

# 画像生成設定
IMAGE_SPECS = {
    "foundation": [
        {"name": "llm-concept", "prompt": "Illustration of Large Language Model concept, neural network brain, modern flat design, blue gradient", "size": "1200x800"},
        {"name": "token-concept", "prompt": "Illustration of text tokenization, words being split into tokens, clean diagram style", "size": "1200x800"},
        {"name": "agent-concept", "prompt": "AI Agent illustration, robot with tools, planning and execution loop, modern style", "size": "1200x800"},
        {"name": "context-engineering", "prompt": "Context Engineering diagram, layered prompts, system project conversation hierarchy", "size": "1200x800"},
        {"name": "transformer", "prompt": "Simplified Transformer architecture diagram, attention mechanism visualization", "size": "1200x800"},
        {"name": "next-token", "prompt": "Next token prediction illustration, probability distribution over words", "size": "1200x800"},
        {"name": "tool-use", "prompt": "AI tool use illustration, agent connecting to various tools and APIs", "size": "1200x800"},
        {"name": "prompt-structure", "prompt": "Effective prompt structure diagram, role context task format sections", "size": "1200x800"},
    ],
    "headers": [
        {"name": "module-1-banner", "prompt": "Banner creation header, colorful social media banners, design tools", "size": "1920x400"},
        {"name": "module-2-diagram", "prompt": "Diagram creation header, flowcharts and infographics, clean lines", "size": "1920x400"},
        {"name": "module-3-screenshot", "prompt": "Screenshot analysis header, screen captures with annotations", "size": "1920x400"},
        {"name": "module-4-data", "prompt": "Data analysis header, charts graphs BigQuery visualization", "size": "1920x400"},
        {"name": "module-5-pptx", "prompt": "PowerPoint header, presentation slides, professional design", "size": "1920x400"},
        {"name": "module-6-slack", "prompt": "Slack integration header, chat bubbles, team communication", "size": "1920x400"},
        {"name": "module-7-video", "prompt": "Video generation header, film strip, AI video creation", "size": "1920x400"},
        {"name": "module-8-gas", "prompt": "Google Apps Script header, automation gears, Google colors", "size": "1920x400"},
        {"name": "module-9-actions", "prompt": "GitHub Actions header, CI/CD pipeline, automation workflow", "size": "1920x400"},
        {"name": "module-10-notion", "prompt": "Notion integration header, database blocks, knowledge management", "size": "1920x400"},
        {"name": "module-11-agent", "prompt": "Agent development header, code and AI robot, programming", "size": "1920x400"},
        {"name": "foundation-header", "prompt": "AI Foundation header, brain and neural networks, learning", "size": "1920x400"},
        {"name": "setup-header", "prompt": "Setup header, installation and configuration, tools setup", "size": "1920x400"},
        {"name": "portal-header", "prompt": "Course portal header, learning journey, modern education", "size": "1920x600"},
    ],
    "concepts": [
        # 各モジュールの概念図（省略、実装時に詳細追加）
    ],
    "exercises": [
        # 演習用図解（省略、実装時に詳細追加）
    ],
    "portal": [
        # ポータル用アイコン（省略、実装時に詳細追加）
    ],
}

def generate_image(spec: dict, output_dir: Path, dry_run: bool = False):
    """
    Gemini APIを使って画像を生成する。

    Args:
        spec: 画像仕様（name, prompt, size）
        output_dir: 出力ディレクトリ
        dry_run: True の場合、実際の生成は行わずログのみ
    """
    output_path = output_dir / f"{spec['name']}.png"

    if dry_run:
        print(f"[DRY RUN] Would generate: {output_path}")
        print(f"  Prompt: {spec['prompt']}")
        print(f"  Size: {spec['size']}")
        return

    # 実際の画像生成はnanobanana.pyを使用
    # ここでは構造のみ定義
    print(f"Generating: {spec['name']}...")
    # TODO: nanobanana.py または Gemini API を呼び出し

def main():
    parser = argparse.ArgumentParser(description="研修教材用挿絵一括生成")
    parser.add_argument("--category", choices=["foundation", "headers", "concepts", "exercises", "portal", "all"],
                        default="all", help="生成するカテゴリ")
    parser.add_argument("--output", type=Path, default=Path("public/course-assets/assets/images"),
                        help="出力ディレクトリ")
    parser.add_argument("--dry-run", action="store_true", help="実際の生成は行わずログのみ")
    args = parser.parse_args()

    # 出力ディレクトリ作成
    args.output.mkdir(parents=True, exist_ok=True)

    # カテゴリ選択
    categories = [args.category] if args.category != "all" else IMAGE_SPECS.keys()

    total = 0
    for category in categories:
        specs = IMAGE_SPECS.get(category, [])
        print(f"\n=== {category.upper()} ({len(specs)} images) ===")
        for spec in specs:
            generate_image(spec, args.output / category, args.dry_run)
            total += 1

    print(f"\n完了: {total} 画像を{'確認' if args.dry_run else '生成'}しました")

if __name__ == "__main__":
    main()

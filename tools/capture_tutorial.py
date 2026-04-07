"""
Capture Tutorial - スクリーンショットから操作チュートリアルを生成

スクリーンショットを解析し、その画面で行うべき操作手順を示すチュートリアルを生成します。
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

from PIL import Image

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from bootcamp_utils import (
    get_client,
    get_flash_model,
    create_html_template,
    save_html_file,
    DEFAULT_OUTPUT_DIR,
)

# デフォルトの保存先
DEFAULT_TUTORIAL_DIR = DEFAULT_OUTPUT_DIR / "tutorials"


def add_step_annotations(image_path: Path, steps: list, output_dir: Path) -> List[Optional[str]]:
    """
    各ステップに対応する注釈画像を生成
    
    Args:
        image_path: 元画像のパス
        steps: ステップ情報のリスト
        output_dir: 出力ディレクトリ
        
    Returns:
        注釈付き画像パス（絶対パス）のリスト
    """
    annotated_paths = []
    annotate_script = Path(__file__).parent / "annotate_screenshot.py"
    
    print(f"\n🎨 注釈画像の生成を開始します（全{len(steps)}ステップ）...")
    
    for i, step in enumerate(steps):
        step_num = step.get("step", i + 1)
        action = step.get("action", "")
        location = step.get("location", "")
        
        # 注釈指示を作成
        instruction = f"{action}"
        if location:
            instruction += f" ({location})"
            
        output_filename = f"{image_path.stem}_step{step_num}_annotated.png"
        output_path = output_dir / output_filename
        
        print(f"  [{i+1}/{len(steps)}] ステップ{step_num}の注釈を生成中...")
        
        try:
            # annotate_screenshot.py を呼び出し
            cmd = [
                sys.executable,
                str(annotate_script),
                str(image_path),
                instruction,
                "--style", "red_box",
                "--output", str(output_path)
            ]
            
            # ステップ番号をテキストとして追加
            cmd.extend(["--text", str(step_num)])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and output_path.exists():
                print(f"    ✅ 生成成功: {output_filename}")
                annotated_paths.append(str(output_path.resolve()))
            else:
                print(f"    ⚠️ 生成失敗: {result.stderr}")
                annotated_paths.append(None)
                
        except Exception as e:
            print(f"    ⚠️ エラー: {e}")
            annotated_paths.append(None)
            
    return annotated_paths


def analyze_screen_for_tutorial(client, image_path: Path) -> dict:
    """
    Gemini Vision でスクリーンショットを解析し、操作チュートリアルを生成
    
    Args:
        client: Gemini APIクライアント
        image_path: 画像ファイルのパス
    
    Returns:
        解析結果の辞書
    """
    print(f"🔍 スクリーンショットを解析中: {image_path}")
    
    if not client:
        print("❌ エラー: Gemini APIキーが必要です。")
        return {
            "title": "APIキー未設定",
            "description": "Gemini APIキーを設定してください。",
            "steps": []
        }
    
    try:
        # 画像を読み込み
        image = Image.open(image_path)
        
        prompt = """
あなたはテクニカルライターです。ユーザーが提供したスクリーンショット（アプリケーションの画面）を基に、
この画面でユーザーが行うべき操作手順を分かりやすく説明するチュートリアルを作成してください。

以下の観点で分析してください：
1. **画面の目的**: この画面は何をするための画面か（例: ログイン、プロジェクト作成、設定変更）
2. **操作手順**: ユーザーがタスクを完了するために行うべき具体的な手順（クリック、入力など）
3. **重要な要素**: 注目すべきボタン、リンク、入力フィールド

以下のJSON形式で出力してください:
{
    "title": "画面のタイトルまたはタスク名",
    "description": "この画面の概要と目的の説明",
    "steps": [
        {
            "step": 1,
            "action": "具体的な操作（例: 「ログイン」ボタンをクリック）",
            "detail": "詳細な説明や補足（例: 右上の青いボタンです）",
            "location": "要素の場所（例: 画面右上、中央下など）"
        }
    ],
    "tips": ["操作時のヒントや注意点があれば記述"]
}

JSONのみを出力し、他の説明は不要です。
"""
        
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=[prompt, image]
        )
        
        content = response.text.strip()
        # JSONブロックを抽出
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        
        # JSONをパース
        try:
            result = json.loads(content)
            print("✅ 解析完了")
            return result
        except json.JSONDecodeError:
            print("⚠️ JSONパースエラー")
            return {
                "title": "解析エラー",
                "description": content[:500],
                "steps": [],
                "tips": []
            }
            
    except Exception as e:
        print(f"❌ 解析エラー: {e}")
        return {
            "title": "エラーが発生しました",
            "description": f"画像の読み込みまたは解析に失敗しました: {e}",
            "steps": [],
            "tips": []
        }


def build_tutorial_html(image_path: Path, result: dict, output_path: Path = None, annotated_paths: List[Optional[str]] = None) -> str:
    """
    チュートリアル用HTMLコンテンツを組み立て
    
    Args:
        image_path: 画像パス
        result: 解析結果
        output_path: 出力HTMLのパス（画像の相対パス計算用）
        annotated_paths: 注釈付き画像のパスリスト
    
    Returns:
        HTMLコンテンツ文字列
    """
    html_parts = []
    
    # タイトルと説明
    html_parts.append('<div class="info-box">')
    html_parts.append(f'<h2>🎯 {result.get("title", "チュートリアル")}</h2>')
    html_parts.append(f'<p>{result.get("description", "")}</p>')
    html_parts.append('</div>')
    
    # 画像パスを計算するヘルパー関数
    def get_rel_path(target_path_str):
        if not target_path_str:
            return ""
        target_path = Path(target_path_str).resolve()
        if output_path:
            output_dir = output_path.resolve().parent
            try:
                import os
                return os.path.relpath(target_path, output_dir)
            except ValueError:
                return str(target_path)
        else:
            try:
                return str(target_path.relative_to(Path.cwd()))
            except ValueError:
                return str(target_path)

    image_rel_path = get_rel_path(str(image_path))
    
    html_parts.append('<h2>🖼️ 画面プレビュー</h2>')
    html_parts.append(f'<div style="text-align: center;"><img src="{image_rel_path}" alt="スクリーンショット" style="max-height: 400px; border: 1px solid #ddd;"></div>')
    
    # 操作手順
    steps = result.get("steps", [])
    if steps:
        html_parts.append('<h2>👉 操作手順</h2>')
        for i, step in enumerate(steps):
            html_parts.append('<div class="step">')
            html_parts.append(f'<span class="step-number">{step.get("step", "?")}</span>')
            html_parts.append(f'<strong>{step.get("action", "")}</strong>')
            
            detail = step.get("detail")
            if detail:
                html_parts.append(f'<p style="margin-top: 5px; color: #555;">{detail}</p>')
                
            location = step.get("location")
            if location:
                html_parts.append(f'<div style="margin-top: 5px; font-size: 0.85em; color: #666;">📍 場所: {location}</div>')
            
            # 注釈付き画像がある場合は表示
            if annotated_paths and i < len(annotated_paths) and annotated_paths[i]:
                annotated_rel_path = get_rel_path(annotated_paths[i])
                html_parts.append(f'<div style="margin-top: 15px; text-align: center;"><img src="{annotated_rel_path}" alt="ステップ{i+1}の注釈" style="max-height: 300px; border: 1px solid #ddd; border-radius: 4px;"></div>')
            
            html_parts.append('</div>')
    
    # ヒント
    tips = result.get("tips", [])
    if tips:
        html_parts.append('<h2>💡 ヒント</h2>')
        html_parts.append('<ul>')
        for tip in tips:
            html_parts.append(f'<li>{tip}</li>')
        html_parts.append('</ul>')
        
    return "".join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description="スクリーンショットから操作チュートリアルを生成します。"
    )
    parser.add_argument(
        "screenshot",
        help="解析するスクリーンショット画像のパス"
    )
    parser.add_argument(
        "--output", "-o",
        help="出力ファイルパス（省略時は自動生成）"
    )
    parser.add_argument(
        "--no-annotate",
        action="store_true",
        help="注釈画像の生成をスキップする"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Capture Tutorial - スクリーンショットから操作チュートリアル生成")
    print("=" * 60)
    
    # 画像ファイルの存在確認
    image_path = Path(args.screenshot)
    if not image_path.exists():
        print(f"❌ エラー: 画像ファイルが見つかりません: {image_path}")
        sys.exit(1)
    
    # Gemini APIクライアントを取得
    client = get_client()
    if not client:
        print("❌ エラー: Gemini APIキーが必要です。")
        print("   GEMINI_API_KEY または GOOGLE_API_KEY を設定してください。")
        sys.exit(1)
    
    # スクリーンショットを解析
    result = analyze_screen_for_tutorial(client, image_path)
    
    # 出力パスを決定
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = DEFAULT_TUTORIAL_DIR / f"tutorial_{timestamp}.html"
    
    # 出力ディレクトリを作成（注釈画像の保存に必要）
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 注釈画像を追加（オプション）
    annotated_paths = []
    if not args.no_annotate and result.get("steps"):
        annotated_paths = add_step_annotations(
            image_path, 
            result["steps"], 
            output_path.parent
        )
    
    # HTMLコンテンツを組み立て
    html_content = build_tutorial_html(image_path, result, output_path, annotated_paths)
    
    # HTMLテンプレートでラップ
    title = f"チュートリアル: {result.get('title', 'Generated Tutorial')}"
    full_html = create_html_template(title, html_content)
    
    # ファイルを保存
    save_html_file(full_html, output_path, title)


if __name__ == "__main__":
    main()

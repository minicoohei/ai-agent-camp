"""
Screenshot Analyzer - スクリーンショット解析統合ツール

スクリーンショットを解析し、以下のモードで処理します：
- analyze: 状況診断・エラー検出・NextStep提案
- tutorial: 操作チュートリアル生成（ステップ注釈付き）

内部でannotate_screenshot.pyを呼び出して注釈画像を生成します。
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
DEFAULT_SCREENSHOT_DIR = DEFAULT_OUTPUT_DIR / "screenshots"


# =============================================================================
# 共通機能
# =============================================================================

def get_rel_path(target_path_str: str, output_path: Path = None) -> str:
    """画像パスを相対パスに変換"""
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


def add_annotations(image_path: Path, instruction: str, output_dir: Path, 
                   style: str = "red_box", text_label: str = None) -> Optional[str]:
    """
    annotate_screenshot.pyを呼び出して注釈を追加
    
    Args:
        image_path: 元画像のパス
        instruction: 注釈指示
        output_dir: 出力ディレクトリ
        style: 注釈スタイル
        text_label: テキストラベル
    
    Returns:
        注釈付き画像の絶対パス（失敗時はNone）
    """
    annotate_script = Path(__file__).parent / "annotate_screenshot.py"
    
    output_filename = f"{image_path.stem}_annotated.png"
    output_path = output_dir / output_filename
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        cmd = [
            sys.executable,
            str(annotate_script),
            str(image_path),
            instruction,
            "--style", style,
            "--output", str(output_path)
        ]
        
        if text_label:
            cmd.extend(["--text", text_label])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and output_path.exists():
            return str(output_path.resolve())
        else:
            print(f"⚠️ 注釈追加に失敗: {result.stderr}")
            return None
    except Exception as e:
        print(f"⚠️ 注釈追加エラー: {e}")
        return None


# =============================================================================
# Analyzeモード（旧 tutorial_from_screenshot）
# =============================================================================

def analyze_screenshot(client, image_path: Path) -> dict:
    """
    Gemini Vision でスクリーンショットを解析
    
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
            "description": "画像の内容を確認してください。",
            "has_error": False,
            "error_details": None,
            "suggestions": []
        }
    
    try:
        image = Image.open(image_path)
        
        analysis_prompt = """
以下のスクリーンショットを詳しく分析してください。

分析の観点:
1. 何が表示されているか（画面、Console、CLI、サーバーログなど）
2. エラーや問題が検出されるか
3. エラーがある場合、その原因は何か
4. 解決方法や次のステップは何か

以下のJSON形式で出力してください:
{
    "description": "画像に何が写っているかの説明",
    "has_error": true/false,
    "error_details": {
        "error_message": "エラーメッセージ（あれば）",
        "error_type": "エラーの種類",
        "possible_causes": ["原因1", "原因2"]
    },
    "suggestions": ["解決方法1", "解決方法2", "次のステップ"]
}

JSONのみを出力し、他の説明は不要です。
"""
        
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=[analysis_prompt, image]
        )
        
        content = response.text.strip()
        json_match = re.search(r'\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        
        try:
            result = json.loads(content)
            print("✅ 解析完了")
            return result
        except json.JSONDecodeError:
            print("⚠️ JSONパースエラー")
            has_error = "error" in content.lower() or "エラー" in content
            return {
                "description": content[:500] if content else "画像の内容を確認してください。",
                "has_error": has_error,
                "error_details": None,
                "suggestions": []
            }
    except Exception as e:
        print(f"❌ 解析エラー: {e}")
        return {
            "description": f"画像の読み込みに失敗しました: {e}",
            "has_error": False,
            "error_details": None,
            "suggestions": []
        }


def generate_next_steps(client, analysis: dict) -> dict:
    """NextStepを生成"""
    print("📋 NextStepを生成中...")
    
    if not client:
        suggestions = analysis.get("suggestions", [])
        return {
            "summary": "次のステップを実行してください。",
            "steps": suggestions if suggestions else ["状況を確認して次のアクションを決定"]
        }
    
    next_steps_prompt = f"""
以下の解析結果を基に、具体的なNextStepを生成してください。

解析結果:
- 説明: {analysis.get('description', '')}
- エラーあり: {analysis.get('has_error', False)}
- エラー詳細: {analysis.get('error_details', {})}
- 提案: {analysis.get('suggestions', [])}

以下のJSON形式で出力してください:
{{
    "summary": "NextStepの概要",
    "steps": [
        {{
            "step": "ステップ番号",
            "action": "具体的なアクション",
            "explanation": "なぜこのアクションが必要か"
        }}
    ],
    "expected_result": "この手順を実行すると何が達成されるか"
}}

JSONのみを出力し、他の説明は不要です。
"""
    
    try:
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=[next_steps_prompt]
        )
        
        content = response.text.strip()
        json_match = re.search(r'\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        
        try:
            result = json.loads(content)
            print("✅ NextStepを生成完了")
            return result
        except json.JSONDecodeError:
            suggestions = analysis.get("suggestions", [])
            return {
                "summary": "次のステップを実行してください。",
                "steps": [
                    {"step": str(i + 1), "action": suggestion, "explanation": ""}
                    for i, suggestion in enumerate(suggestions[:5])
                ] if suggestions else [{"step": "1", "action": "状況を確認", "explanation": ""}],
                "expected_result": "問題が解決される"
            }
    except Exception as e:
        print(f"⚠️ NextStep生成エラー: {e}")
        return {
            "summary": "次のステップを実行してください。",
            "steps": [{"step": "1", "action": "状況を確認", "explanation": ""}],
            "expected_result": "問題が解決される"
        }


def build_analyze_html(image_path: Path, analysis: dict, annotated_path: Optional[str], 
                       next_steps: dict, output_path: Path) -> str:
    """Analyzeモード用HTMLコンテンツを組み立て"""
    html_parts = []
    
    # 状況説明
    html_parts.append('<div class="info-box">')
    html_parts.append('<h2>📸 スクリーンショットの状況</h2>')
    html_parts.append(f'<p>{analysis.get("description", "画像の内容を確認してください。")}</p>')
    html_parts.append('</div>')
    
    # 元の画像
    image_rel_path = get_rel_path(str(image_path), output_path)
    html_parts.append('<h2>🖼️ 元のスクリーンショット</h2>')
    html_parts.append(f'<img src="{image_rel_path}" alt="元のスクリーンショット">')
    
    # エラー詳細
    if analysis.get("has_error"):
        html_parts.append('<h2>❌ 検出された問題</h2>')
        error_details = analysis.get("error_details", {})
        
        html_parts.append('<div class="warning-box">')
        if error_details and error_details.get("error_message"):
            html_parts.append(f'<p><strong>エラーメッセージ:</strong> {error_details["error_message"]}</p>')
        if error_details and error_details.get("error_type"):
            html_parts.append(f'<p><strong>エラーの種類:</strong> {error_details["error_type"]}</p>')
        
        causes = error_details.get("possible_causes", []) if error_details else []
        if causes:
            html_parts.append('<p><strong>考えられる原因:</strong></p>')
            html_parts.append('<ul>')
            for cause in causes:
                html_parts.append(f'<li>{cause}</li>')
            html_parts.append('</ul>')
        html_parts.append('</div>')
        
        # 注釈付き画像
        if annotated_path:
            annotated_rel_path = get_rel_path(annotated_path, output_path)
            html_parts.append('<h2>🎨 注釈付きスクリーンショット</h2>')
            html_parts.append(f'<img src="{annotated_rel_path}" alt="注釈付きスクリーンショット">')
    else:
        html_parts.append('<div class="success-box">')
        html_parts.append('<p>エラーや問題は検出されませんでした。</p>')
        html_parts.append('</div>')
    
    # 解決手順
    html_parts.append('<h2>🔧 解決手順</h2>')
    steps = next_steps.get("steps", [])
    if steps:
        for step_data in steps:
            html_parts.append('<div class="step">')
            step_num = step_data.get("step", "?") if isinstance(step_data, dict) else "?"
            action = step_data.get("action", step_data) if isinstance(step_data, dict) else step_data
            html_parts.append(f'<span class="step-number">{step_num}</span>')
            html_parts.append(f'<strong>{action}</strong>')
            if isinstance(step_data, dict) and step_data.get("explanation"):
                html_parts.append(f'<p>{step_data["explanation"]}</p>')
            html_parts.append('</div>')
    
    # NextStepのまとめ
    html_parts.append('<h2>✅ NextStepのまとめ</h2>')
    html_parts.append('<div class="success-box">')
    html_parts.append(f'<p><strong>{next_steps.get("summary", "次のステップを実行してください。")}</strong></p>')
    if next_steps.get("expected_result"):
        html_parts.append(f'<p>期待される結果: {next_steps["expected_result"]}</p>')
    html_parts.append('</div>')
    
    return "".join(html_parts)


# =============================================================================
# Tutorialモード（旧 capture_tutorial）
# =============================================================================

def analyze_for_tutorial(client, image_path: Path) -> dict:
    """
    Gemini Vision でスクリーンショットを解析し、操作チュートリアルを生成
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
        json_match = re.search(r'\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        
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


def add_step_annotations(image_path: Path, steps: list, output_dir: Path) -> List[Optional[str]]:
    """各ステップに対応する注釈画像を生成"""
    annotated_paths = []
    
    print(f"\n🎨 注釈画像の生成を開始します（全{len(steps)}ステップ）...")
    
    for i, step in enumerate(steps):
        step_num = step.get("step", i + 1)
        action = step.get("action", "")
        location = step.get("location", "")
        
        instruction = f"{action}"
        if location:
            instruction += f" ({location})"
            
        output_filename = f"{image_path.stem}_step{step_num}_annotated.png"
        output_path = output_dir / output_filename
        
        print(f"  [{i+1}/{len(steps)}] ステップ{step_num}の注釈を生成中...")
        
        result = add_annotations(
            image_path, 
            instruction, 
            output_dir, 
            style="red_box", 
            text_label=str(step_num)
        )
        
        if result:
            print(f"    ✅ 生成成功: {output_filename}")
            annotated_paths.append(result)
        else:
            annotated_paths.append(None)
            
    return annotated_paths


def build_tutorial_html(image_path: Path, result: dict, output_path: Path, 
                       annotated_paths: List[Optional[str]] = None) -> str:
    """Tutorialモード用HTMLコンテンツを組み立て"""
    html_parts = []
    
    # タイトルと説明
    html_parts.append('<div class="info-box">')
    html_parts.append(f'<h2>🎯 {result.get("title", "チュートリアル")}</h2>')
    html_parts.append(f'<p>{result.get("description", "")}</p>')
    html_parts.append('</div>')
    
    image_rel_path = get_rel_path(str(image_path), output_path)
    
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
            
            # 注釈付き画像
            if annotated_paths and i < len(annotated_paths) and annotated_paths[i]:
                annotated_rel_path = get_rel_path(annotated_paths[i], output_path)
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


# =============================================================================
# メイン処理
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="スクリーンショット解析統合ツール。エラー解析や操作チュートリアルを生成します。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # エラー解析モード（状況診断・NextStep提案）
  python screenshot_analyzer.py screenshot.png --mode analyze

  # 操作チュートリアルモード
  python screenshot_analyzer.py screenshot.png --mode tutorial

  # 注釈なしで解析のみ
  python screenshot_analyzer.py screenshot.png --mode analyze --no-annotate

  # 出力先を指定
  python screenshot_analyzer.py screenshot.png --mode tutorial --output docs/my_tutorial.html
        """
    )
    parser.add_argument(
        "screenshot",
        help="解析するスクリーンショット画像のパス"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["analyze", "tutorial"],
        default="analyze",
        help="処理モード: analyze=エラー解析・NextStep提案, tutorial=操作チュートリアル生成（デフォルト: analyze）"
    )
    parser.add_argument(
        "--no-annotate",
        action="store_true",
        help="注釈画像の生成をスキップする"
    )
    parser.add_argument(
        "--output", "-o",
        help="出力ファイルパス（省略時は自動生成）"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"Screenshot Analyzer - {args.mode.upper()}モード")
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
    
    # 出力パスを決定
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = DEFAULT_SCREENSHOT_DIR / f"{args.mode}_{timestamp}.html"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # モードに応じた処理
    if args.mode == "analyze":
        # Analyzeモード
        analysis = analyze_screenshot(client, image_path)
        
        # 注釈を追加（エラーがある場合）
        annotated_path = None
        if not args.no_annotate and analysis.get("has_error"):
            error_details = analysis.get("error_details", {})
            error_message = error_details.get("error_message", "") if error_details else ""
            if error_message:
                print("🎨 注釈を追加中...")
                instruction = f"エラーメッセージ '{error_message[:50]}' の部分を赤枠で囲んで矢印を追加"
                annotated_path = add_annotations(image_path, instruction, output_path.parent)
        
        # NextStepを生成
        next_steps = generate_next_steps(client, analysis)
        
        # HTMLを生成
        html_content = build_analyze_html(image_path, analysis, annotated_path, next_steps, output_path)
        title = f"スクリーンショット解析 - {image_path.stem}"
        
    else:
        # Tutorialモード
        result = analyze_for_tutorial(client, image_path)
        
        # 注釈画像を追加
        annotated_paths = []
        if not args.no_annotate and result.get("steps"):
            annotated_paths = add_step_annotations(image_path, result["steps"], output_path.parent)
        
        # HTMLを生成
        html_content = build_tutorial_html(image_path, result, output_path, annotated_paths)
        title = f"チュートリアル: {result.get('title', 'Generated Tutorial')}"
    
    # HTMLテンプレートでラップして保存
    full_html = create_html_template(title, html_content)
    save_html_file(full_html, output_path, title)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
スクリーンショット分析スクリプト（Final Example）

このスクリプトを実行すると、スクリーンショットを分析して
エラー診断や注釈を追加します。

必要条件:
- Gemini APIキー（環境変数 GEMINI_API_KEY）
- Python 3.9以上
- Pillow, google-genai

使用方法:
    python screenshot_analyzer.py --input screenshot.png --mode diagnose
    python screenshot_analyzer.py --input screenshot.png --mode annotate --prompt "エラー箇所を赤枠で囲んで"
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: Pillow がインストールされていません")

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    print("Warning: google-genai がインストールされていません")


# 分析モード
ANALYSIS_MODES = {
    "diagnose": {
        "description": "エラー診断",
        "prompt_template": """
このスクリーンショットを分析してください。

分析項目:
1. 画面に表示されているエラーや問題を特定
2. エラーの原因を推測
3. 解決方法を提案

出力形式（JSON）:
{{
    "errors": [
        {{
            "type": "エラータイプ",
            "message": "エラーメッセージ",
            "location": "画面上の位置",
            "cause": "推測される原因",
            "solution": "解決方法"
        }}
    ],
    "severity": "critical/high/medium/low",
    "summary": "全体サマリー"
}}
"""
    },
    "ui_review": {
        "description": "UI/UXレビュー",
        "prompt_template": """
このUIスクリーンショットをレビューしてください。

チェック項目:
1. レイアウトの問題点
2. 視認性（フォントサイズ、色のコントラスト）
3. 操作性（ボタン配置、導線）
4. アクセシビリティ
5. モバイル対応の観点

出力形式（JSON）:
{{
    "issues": [
        {{
            "category": "カテゴリ",
            "description": "問題の説明",
            "severity": "critical/major/minor",
            "suggestion": "改善提案"
        }}
    ],
    "positives": ["良い点1", "良い点2"],
    "overall_score": 1-10,
    "summary": "全体評価"
}}
"""
    },
    "annotate": {
        "description": "注釈追加",
        "prompt_template": """
このスクリーンショットに注釈を追加するための情報を提供してください。

{custom_prompt}

出力形式（JSON）:
{{
    "annotations": [
        {{
            "type": "box/arrow/text/highlight",
            "position": {{"x": 100, "y": 200, "width": 300, "height": 50}},
            "color": "red/green/blue/yellow",
            "text": "注釈テキスト"
        }}
    ]
}}
"""
    },
    "extract_text": {
        "description": "テキスト抽出（OCR）",
        "prompt_template": """
このスクリーンショットからテキストを抽出してください。

出力形式（JSON）:
{{
    "texts": [
        {{
            "content": "抽出テキスト",
            "type": "heading/paragraph/button/label/error",
            "position": "画面上の位置（上部/中央/下部など）"
        }}
    ],
    "language": "検出言語",
    "summary": "画面の概要"
}}
"""
    }
}


class ScreenshotAnalyzer:
    """スクリーンショット分析クラス"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if HAS_GENAI and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
    
    def analyze(self, image_path: str, mode: str, custom_prompt: str = None) -> Dict[str, Any]:
        """画像を分析"""
        if mode not in ANALYSIS_MODES:
            raise ValueError(f"Unknown mode: {mode}")
        
        config = ANALYSIS_MODES[mode]
        prompt = config["prompt_template"]
        
        if custom_prompt and mode == "annotate":
            prompt = prompt.format(custom_prompt=custom_prompt)
        
        if self.client and HAS_PIL:
            # 実際のAPI呼び出し
            image = Image.open(image_path)
            response = self.client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=[prompt, image]
            )
            
            # JSONを抽出
            try:
                result_text = response.text
                # JSONブロックを抽出
                if "```json" in result_text:
                    json_str = result_text.split("```json")[1].split("```")[0]
                elif "```" in result_text:
                    json_str = result_text.split("```")[1].split("```")[0]
                else:
                    json_str = result_text
                
                return json.loads(json_str)
            except:
                return {"raw_response": response.text}
        else:
            # モック結果
            return self._get_mock_result(mode)
    
    def _get_mock_result(self, mode: str) -> Dict[str, Any]:
        """モック結果を返す"""
        mock_results = {
            "diagnose": {
                "errors": [
                    {
                        "type": "HTTP Error",
                        "message": "404 Not Found",
                        "location": "中央のメインコンテンツエリア",
                        "cause": "リクエストされたURLが存在しない、またはリソースが削除された",
                        "solution": "1. URLのスペルを確認\n2. トップページから再度アクセス\n3. サイト管理者に連絡"
                    }
                ],
                "severity": "medium",
                "summary": "404エラーページが表示されています。リンク切れまたはURL入力ミスの可能性があります。"
            },
            "ui_review": {
                "issues": [
                    {
                        "category": "視認性",
                        "description": "ボタンのコントラストが低く、視認しにくい",
                        "severity": "major",
                        "suggestion": "背景色とボタン色のコントラスト比を4.5:1以上に"
                    },
                    {
                        "category": "レイアウト",
                        "description": "フォームの入力欄が狭すぎる",
                        "severity": "minor",
                        "suggestion": "最小高さを44pxに設定（タッチターゲット推奨サイズ）"
                    }
                ],
                "positives": ["ナビゲーションが明確", "ロゴの配置が適切"],
                "overall_score": 7,
                "summary": "基本的なUIは良好ですが、アクセシビリティの改善が必要です。"
            },
            "annotate": {
                "annotations": [
                    {
                        "type": "box",
                        "position": {"x": 100, "y": 200, "width": 300, "height": 50},
                        "color": "red",
                        "text": "エラーメッセージ"
                    },
                    {
                        "type": "arrow",
                        "position": {"x": 400, "y": 150, "width": 50, "height": 100},
                        "color": "blue",
                        "text": "ここをクリック"
                    }
                ]
            },
            "extract_text": {
                "texts": [
                    {"content": "ログイン", "type": "heading", "position": "上部"},
                    {"content": "メールアドレス", "type": "label", "position": "中央"},
                    {"content": "パスワード", "type": "label", "position": "中央"},
                    {"content": "ログインする", "type": "button", "position": "下部"}
                ],
                "language": "日本語",
                "summary": "ログインフォーム画面"
            }
        }
        return mock_results.get(mode, {})
    
    def add_annotations(self, image_path: str, annotations: List[Dict], output_path: str):
        """画像に注釈を追加"""
        if not HAS_PIL:
            print("Pillowがインストールされていないため、注釈を追加できません")
            return
        
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        # 色の定義
        colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "orange": (255, 165, 0)
        }
        
        for ann in annotations:
            pos = ann.get("position", {})
            color = colors.get(ann.get("color", "red"), (255, 0, 0))
            ann_type = ann.get("type", "box")
            
            x = pos.get("x", 0)
            y = pos.get("y", 0)
            w = pos.get("width", 100)
            h = pos.get("height", 50)
            
            if ann_type == "box":
                # 矩形を描画
                draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
            elif ann_type == "highlight":
                # 半透明のハイライト
                overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rectangle([x, y, x + w, y + h], fill=(*color, 64))
                image = Image.alpha_composite(image.convert('RGBA'), overlay)
                draw = ImageDraw.Draw(image)
            
            # テキストラベル
            text = ann.get("text", "")
            if text:
                draw.text((x, y - 20), text, fill=color)
        
        image.save(output_path)
        print(f"✅ 注釈追加完了: {output_path}")


def generate_report(analysis_result: Dict, output_path: str, mode: str):
    """分析レポートを生成"""
    report = f"""# スクリーンショット分析レポート

生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
分析モード: {ANALYSIS_MODES[mode]['description']}

---

"""
    
    if mode == "diagnose":
        report += "## エラー診断結果\n\n"
        report += f"**重要度**: {analysis_result.get('severity', 'N/A')}\n\n"
        report += f"**サマリー**: {analysis_result.get('summary', 'N/A')}\n\n"
        
        report += "### 検出されたエラー\n\n"
        for i, error in enumerate(analysis_result.get('errors', []), 1):
            report += f"#### エラー {i}: {error.get('type', 'Unknown')}\n\n"
            report += f"- **メッセージ**: {error.get('message', 'N/A')}\n"
            report += f"- **位置**: {error.get('location', 'N/A')}\n"
            report += f"- **原因**: {error.get('cause', 'N/A')}\n"
            report += f"- **解決策**: {error.get('solution', 'N/A')}\n\n"
    
    elif mode == "ui_review":
        report += "## UI/UXレビュー結果\n\n"
        report += f"**総合スコア**: {analysis_result.get('overall_score', 'N/A')}/10\n\n"
        report += f"**サマリー**: {analysis_result.get('summary', 'N/A')}\n\n"
        
        report += "### 検出された問題\n\n"
        for issue in analysis_result.get('issues', []):
            report += f"- **[{issue.get('severity', 'N/A')}]** {issue.get('category', '')}: "
            report += f"{issue.get('description', '')}\n"
            report += f"  - 提案: {issue.get('suggestion', '')}\n\n"
        
        report += "### 良い点\n\n"
        for positive in analysis_result.get('positives', []):
            report += f"- {positive}\n"
    
    elif mode == "extract_text":
        report += "## テキスト抽出結果\n\n"
        report += f"**検出言語**: {analysis_result.get('language', 'N/A')}\n\n"
        report += f"**画面概要**: {analysis_result.get('summary', 'N/A')}\n\n"
        
        report += "### 抽出テキスト\n\n"
        for text in analysis_result.get('texts', []):
            report += f"- **[{text.get('type', 'text')}]** {text.get('content', '')}\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📝 レポート生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="スクリーンショット分析スクリプト")
    parser.add_argument("--input", "-i", required=True, help="入力画像ファイル")
    parser.add_argument("--mode", "-m", choices=ANALYSIS_MODES.keys(), default="diagnose",
                        help="分析モード")
    parser.add_argument("--prompt", "-p", type=str, help="カスタムプロンプト（annotateモード用）")
    parser.add_argument("--output", "-o", type=str, help="出力ファイル")
    parser.add_argument("--format", choices=["json", "markdown", "annotated"], default="json",
                        help="出力形式")
    parser.add_argument("--list-modes", action="store_true", help="利用可能なモード一覧")
    
    args = parser.parse_args()
    
    if args.list_modes:
        print("利用可能な分析モード:")
        for mode, config in ANALYSIS_MODES.items():
            print(f"  {mode}: {config['description']}")
        return
    
    # 入力ファイル確認
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ ファイルが見つかりません: {input_path}")
        print("サンプル画像を使用してモック分析を実行します...")
    
    # 出力パス設定
    if args.output:
        output_path = Path(args.output)
    else:
        suffix = ".json" if args.format == "json" else ".md"
        output_path = input_path.with_suffix(f".analysis{suffix}")
    
    # 分析実行
    analyzer = ScreenshotAnalyzer()
    result = analyzer.analyze(str(input_path), args.mode, args.prompt)
    
    # 出力
    if args.format == "json":
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 分析完了: {output_path}")
    elif args.format == "markdown":
        generate_report(result, str(output_path), args.mode)
    elif args.format == "annotated":
        if args.mode == "annotate" and "annotations" in result:
            annotated_path = input_path.with_suffix(".annotated.png")
            analyzer.add_annotations(str(input_path), result["annotations"], str(annotated_path))
    
    # 結果表示
    print("\n分析結果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

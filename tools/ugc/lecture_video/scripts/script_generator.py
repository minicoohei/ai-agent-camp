#!/usr/bin/env python3
"""
Script Generator - 講義スクリプトを生成

HTMLから抽出したコンテンツを基に、自然な講義スクリプト（台本）を生成する。
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import sys

TOOLS_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TOOLS_DIR))
from runtime_env import load_runtime_env

load_runtime_env(TOOLS_DIR.parent)



@dataclass
class ScriptSegment:
    """講義スクリプトのセグメント"""
    section_title: str
    narration: str  # 読み上げるテキスト
    slide_type: str  # "title", "content", "diagram", "summary"
    duration: int  # 秒
    visual_notes: str = ""  # スライドに表示するメモ
    transition: str = "fade"  # トランジション効果


@dataclass
class LectureScript:
    """講義スクリプト全体"""
    title: str
    module_id: str
    segments: List[ScriptSegment] = field(default_factory=list)
    total_duration: int = 0
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "module_id": self.module_id,
            "total_duration": self.total_duration,
            "segments": [
                {
                    "section_title": s.section_title,
                    "narration": s.narration,
                    "slide_type": s.slide_type,
                    "duration": s.duration,
                    "visual_notes": s.visual_notes,
                    "transition": s.transition,
                }
                for s in self.segments
            ],
        }


def generate_script(content: dict, style: str = "friendly") -> LectureScript:
    """
    講義コンテンツからスクリプトを生成する
    
    Args:
        content: parse_htmlの出力（辞書形式）
        style: 話し方のスタイル ("friendly", "formal", "casual")
        
    Returns:
        LectureScript: 生成されたスクリプト
    """
    script = LectureScript(
        title=content["title"],
        module_id=content["module_id"],
    )
    
    # オープニング
    opening = _generate_opening(content, style)
    script.segments.append(opening)
    
    # 学習目標
    if content.get("learning_objectives"):
        objectives = _generate_objectives_segment(content["learning_objectives"], style)
        script.segments.append(objectives)
    
    # 各セクション
    for section in content.get("sections", []):
        segment = _generate_section_segment(section, style)
        script.segments.append(segment)
    
    # まとめ
    if content.get("summary_points"):
        summary = _generate_summary_segment(content["summary_points"], style)
        script.segments.append(summary)
    
    # クロージング
    closing = _generate_closing(content, style)
    script.segments.append(closing)
    
    # 合計時間を計算
    script.total_duration = sum(s.duration for s in script.segments)
    
    return script


def _generate_opening(content: dict, style: str) -> ScriptSegment:
    """オープニングセグメントを生成"""
    title = content["title"]
    
    if style == "friendly":
        narration = f"""
こんにちは！今日は「{title}」について学んでいきましょう。

このセッションでは、AIを活用する上で重要な基礎知識を、
わかりやすく説明していきます。

初めての方でも大丈夫。一緒にゆっくり進んでいきましょう。
        """.strip()
    elif style == "formal":
        narration = f"""
本日は「{title}」について解説いたします。

このセッションを通じて、
AIエージェントを活用するために必要な基礎知識を
体系的に理解していただけます。
        """.strip()
    else:  # casual
        narration = f"""
今日のテーマは「{title}」です！

難しそうに聞こえるかもしれませんが、
実はそんなに難しくありません。
一緒に見ていきましょう！
        """.strip()
    
    return ScriptSegment(
        section_title="オープニング",
        narration=narration,
        slide_type="title",
        duration=20,
        visual_notes=title,
        transition="fade",
    )


def _generate_objectives_segment(objectives: List[str], style: str) -> ScriptSegment:
    """学習目標セグメントを生成"""
    objectives_text = "\n".join(f"• {obj}" for obj in objectives)
    
    if style == "friendly":
        narration = f"""
まず、今日の学習目標を確認しておきましょう。

このセッションが終わるころには、次のことができるようになります。

{_format_list_for_narration(objectives)}

では、さっそく始めていきましょう！
        """.strip()
    else:
        narration = f"""
本セッションの学習目標は以下の通りです。

{_format_list_for_narration(objectives)}

順番に解説していきます。
        """.strip()
    
    return ScriptSegment(
        section_title="学習目標",
        narration=narration,
        slide_type="content",
        duration=30,
        visual_notes=objectives_text,
        transition="slide",
    )


def _generate_section_segment(section: dict, style: str) -> ScriptSegment:
    """コンテンツセクションのセグメントを生成"""
    title = section["title"]
    content_type = section.get("content_type", "concept")
    text_content = section.get("text_content", "")
    bullet_points = section.get("bullet_points", [])
    
    # コンテンツからナレーションを生成
    narration = _content_to_narration(
        title=title,
        text=text_content,
        bullets=bullet_points,
        style=style,
        content_type=content_type,
    )
    
    # スライドタイプを決定
    if section.get("plantuml_url"):
        slide_type = "diagram"
    elif content_type == "summary":
        slide_type = "summary"
    else:
        slide_type = "content"
    
    # ビジュアルノートを作成
    visual_notes = title
    if bullet_points:
        visual_notes += "\n" + "\n".join(f"• {b[:50]}..." if len(b) > 50 else f"• {b}" for b in bullet_points[:5])
    
    return ScriptSegment(
        section_title=title,
        narration=narration,
        slide_type=slide_type,
        duration=section.get("duration_estimate", 60),
        visual_notes=visual_notes,
        transition="slide",
    )


def _generate_summary_segment(summary_points: List[str], style: str) -> ScriptSegment:
    """まとめセグメントを生成"""
    if style == "friendly":
        narration = f"""
最後に、今日学んだことをおさらいしましょう。

大切なポイントは次の通りです。

{_format_list_for_narration(summary_points)}

これらのポイントを覚えておけば、
実際にAIを使う時に役立ちます。
        """.strip()
    else:
        narration = f"""
本セッションのまとめです。

{_format_list_for_narration(summary_points)}

以上が重要なポイントとなります。
        """.strip()
    
    return ScriptSegment(
        section_title="まとめ",
        narration=narration,
        slide_type="summary",
        duration=40,
        visual_notes="\n".join(f"• {p}" for p in summary_points),
        transition="fade",
    )


def _generate_closing(content: dict, style: str) -> ScriptSegment:
    """クロージングセグメントを生成"""
    title = content["title"]
    
    if style == "friendly":
        narration = f"""
お疲れさまでした！
「{title}」の解説は以上です。

わからないことがあれば、いつでも戻って復習してください。
それでは、次のセッションでお会いしましょう！
        """.strip()
    else:
        narration = f"""
以上で「{title}」の解説を終わります。

ご視聴ありがとうございました。
        """.strip()
    
    return ScriptSegment(
        section_title="クロージング",
        narration=narration,
        slide_type="title",
        duration=15,
        visual_notes="ありがとうございました",
        transition="fade",
    )


def _content_to_narration(
    title: str,
    text: str,
    bullets: List[str],
    style: str,
    content_type: str,
) -> str:
    """コンテンツをナレーションに変換"""
    
    # テキストを整形（HTMLタグ、余分な空白を除去）
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # たとえ話がある場合は強調
    has_analogy = "【たとえ話】" in text
    has_warning = "【注意事項】" in text
    
    # セクション導入
    intro = f"次に、「{title}」について見ていきましょう。\n\n"
    
    # メインコンテンツ
    if text:
        # 長すぎる場合は要約
        if len(text) > 500:
            main_text = _summarize_text(text, 500)
        else:
            main_text = text
    else:
        main_text = ""
    
    # 箇条書きを追加
    if bullets and len(bullets) > 0:
        bullets_text = "\n\nポイントをまとめると、\n"
        bullets_text += _format_list_for_narration(bullets[:5])
        main_text += bullets_text
    
    # スタイルに応じた調整
    if style == "friendly":
        # 親しみやすい表現に調整
        main_text = main_text.replace("である。", "です。")
        main_text = main_text.replace("だ。", "ですね。")
    
    return intro + main_text


def _format_list_for_narration(items: List[str]) -> str:
    """リストをナレーション用にフォーマット"""
    numbered = []
    ordinals = ["1つ目", "2つ目", "3つ目", "4つ目", "5つ目"]
    
    for i, item in enumerate(items[:5]):
        # 長すぎる項目は短縮
        if len(item) > 100:
            item = item[:97] + "..."
        
        if i < len(ordinals):
            numbered.append(f"{ordinals[i]}は、{item}")
        else:
            numbered.append(f"そして、{item}")
    
    return "\n".join(numbered)


def _summarize_text(text: str, max_length: int) -> str:
    """テキストを要約（簡易版）"""
    # 文で分割
    import re
    sentences = re.split(r'[。！？\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # 最初の数文を取得
    result = []
    current_length = 0
    
    for sentence in sentences:
        if current_length + len(sentence) > max_length:
            break
        result.append(sentence)
        current_length += len(sentence)
    
    return "。".join(result) + "。"


def generate_script_with_llm(content: dict, style: str = "friendly") -> LectureScript:
    """
    LLMを使用してより自然なスクリプトを生成する
    
    （オプション機能 - Gemini APIが必要）
    """
    try:
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ GEMINI_API_KEY が未設定。ルールベース生成にフォールバック")
            return generate_script(content, style)

        client = genai.Client(api_key=api_key)
        
        # プロンプトを構築
        prompt = f"""
以下の講義コンテンツを基に、自然な講義スクリプト（ナレーション）を生成してください。

## コンテンツ
{json.dumps(content, ensure_ascii=False, indent=2)}

## 要件
- スタイル: {style}（{"親しみやすく、初心者にもわかりやすい口調" if style == "friendly" else "丁寧で正式な口調"}）
- 各セクションに対して、読み上げ用のナレーションを作成
- 「です」「ます」調で統一
- 難しい用語には簡単な説明を追加
- 適度な間を入れる（「、」や改行で表現）

## 出力形式
JSON形式で出力してください。各セグメントは以下の形式:
{{
  "segments": [
    {{
      "section_title": "セクションタイトル",
      "narration": "読み上げるテキスト",
      "slide_type": "title/content/diagram/summary",
      "duration": 秒数
    }}
  ]
}}
"""
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[prompt],
        )
        result_text = response.text
        
        # JSONを抽出
        import re
        json_match = re.search(r'\{[\s\S]*\}', result_text)
        if json_match:
            result = json.loads(json_match.group())
            
            script = LectureScript(
                title=content["title"],
                module_id=content["module_id"],
            )
            
            for seg in result.get("segments", []):
                script.segments.append(ScriptSegment(
                    section_title=seg.get("section_title", ""),
                    narration=seg.get("narration", ""),
                    slide_type=seg.get("slide_type", "content"),
                    duration=seg.get("duration", 60),
                ))
            
            script.total_duration = sum(s.duration for s in script.segments)
            return script
        
    except Exception as e:
        print(f"⚠️ LLM生成エラー: {e}. ルールベース生成にフォールバック")
    
    return generate_script(content, style)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="講義スクリプトを生成")
    parser.add_argument("content_json", help="コンテンツJSONファイルのパス")
    parser.add_argument("--output", "-o", help="出力ファイルのパス")
    parser.add_argument("--style", "-s", default="friendly",
                       choices=["friendly", "formal", "casual"],
                       help="話し方のスタイル")
    parser.add_argument("--use-llm", action="store_true",
                       help="LLMを使用してより自然なスクリプトを生成")
    
    args = parser.parse_args()
    
    with open(args.content_json, "r", encoding="utf-8") as f:
        content = json.load(f)
    
    if args.use_llm:
        script = generate_script_with_llm(content, args.style)
    else:
        script = generate_script(content, args.style)
    
    result = script.to_dict()
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 出力: {args.output}")
        print(f"   セグメント数: {len(script.segments)}")
        print(f"   合計時間: {script.total_duration}秒 ({script.total_duration // 60}分{script.total_duration % 60}秒)")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

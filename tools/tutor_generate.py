"""
Tutor - 学習コンテンツ生成ツール
複数入力ソース対応: トピック / ファイル / テキスト / SpecStory
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from bootcamp_utils import (
    get_client,
    get_flash_model,
    get_latest_specstory_files,
    create_html_template,
    save_html_file,
    DEFAULT_OUTPUT_DIR,
    list_specstory_files_for_selection,
    print_specstory_file_list,
    get_selected_specstory_files,
    get_specstory_content_from_files,
    get_specstory_files_by_names,
    list_specstory_files_json,
    markdown_to_html,
    generate_plantuml_img_tag,
    build_referenced_files_html,
)

DEFAULT_TUTOR_DIR = DEFAULT_OUTPUT_DIR / "tutor"

def safe_parse_json(content: str) -> dict:
    """JSONを安全にパースする。壊れている場合は修復を試みる"""
    # ```json ... ``` ブロックを抽出（最後の```にマッチするようgreedyに）
    json_match = re.search(r'```json\s*(.*)\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1).strip()
    
    # まず直接パースを試みる
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
    # 壊れたJSONの修復を試みる
    try:
        # 最後の完全なオブジェクト/配列を見つける
        depth = 0
        last_valid = 0
        in_string = False
        escape = False
        
        for i, c in enumerate(content):
            if escape:
                escape = False
                continue
            if c == '\\':
                escape = True
                continue
            if c == '"' and not escape:
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == '{' or c == '[':
                depth += 1
            elif c == '}' or c == ']':
                depth -= 1
                if depth == 0:
                    last_valid = i + 1
        
        if last_valid > 0:
            return json.loads(content[:last_valid])
    except json.JSONDecodeError:
        pass
    
    return {}


def generate_topic_tutorial(client, topic: str) -> dict:
    """トピックからチュートリアルを生成"""
    print(f"📖 トピック「{topic}」のチュートリアルを生成中...")
    prompt = f"""
あなたは教育のエキスパートです。「{topic}」について、初心者向けのチュートリアルを作成してください。

以下のJSON形式で出力:
{{
    "title": "チュートリアルのタイトル",
    "introduction": "このトピックの概要と学ぶ意義",
    "sequence_flow": ["User -> System: 操作", "System -> User: 応答"],
    "prerequisites": ["前提知識1", "前提知識2"],
    "sections": [
        {{
            "title": "セクションタイトル",
            "content": "詳細な説明",
            "code_example": "コード例（あれば）",
            "tips": ["ポイント1", "ポイント2"]
        }}
    ],
    "common_mistakes": [
        {{"mistake": "よくある間違い", "correction": "正しい方法"}}
    ],
    "summary": ["まとめポイント1", "まとめポイント2"],
    "next_steps": ["次に学ぶべきこと"]
}}

重要:
- sequence_flowには、トピックに関連する処理の流れや相互作用を「A -> B: 動作」の形式で記述してください（該当しない場合は空配列）。

日本語で、JSONのみを出力してください。
"""
    if not client:
        return {
            "title": f"{topic} チュートリアル",
            "introduction": f"{topic}について学習しましょう。",
            "sequence_flow": [],
            "prerequisites": ["基礎知識"],
            "sections": [{"title": "基本", "content": f"{topic}の基本を理解しましょう。", "code_example": "", "tips": []}],
            "common_mistakes": [],
            "summary": [f"{topic}の基礎を理解する"],
            "next_steps": ["実践してみる"]
        }
    try:
        response = client.models.generate_content(model=get_flash_model(), contents=[prompt])
        content = response.text.strip()
        result = safe_parse_json(content)
        if result:
            print("✅ チュートリアル生成完了")
            return result
        else:
            print("⚠️ JSONパース失敗")
            return {"title": topic, "introduction": "", "sequence_flow": [], "prerequisites": [], "sections": [], "common_mistakes": [], "summary": [], "next_steps": []}
    except Exception as e:
        print(f"⚠️ 生成エラー: {e}")
        return {"title": topic, "introduction": "", "sequence_flow": [], "prerequisites": [], "sections": [], "common_mistakes": [], "summary": [], "next_steps": []}


def generate_file_tutorial(client, file_path: str) -> dict:
    """ファイルからマニュアルを生成"""
    print(f"📖 ファイル「{file_path}」のマニュアルを生成中...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()[:8000]
    except Exception as e:
        print(f"⚠️ ファイル読み込みエラー: {e}")
        return {"title": file_path, "introduction": "ファイルを読み込めませんでした。", "sequence_flow": [], "process_steps": [], "prerequisites": [], "sections": [], "common_mistakes": [], "summary": [], "next_steps": []}

    prompt = f"""
あなたは教育のエキスパートです。以下のコードファイルについて、使い方のマニュアルを作成してください。

ファイル: {file_path}
```
{file_content}
```

以下のJSON形式で出力:
{{
    "title": "ファイル名 - マニュアル",
    "introduction": "このファイルの目的と概要",
    "sequence_flow": ["User -> Tool: コマンド実行", "Tool -> API: 処理依頼", "API -> Tool: 結果返却"],
    "process_steps": ["手順1", "手順2", "手順3"],
    "prerequisites": ["前提知識1", "前提知識2"],
    "sections": [
        {{
            "title": "機能/関数名",
            "content": "詳細な説明",
            "code_example": "使用例",
            "tips": ["ポイント"]
        }}
    ],
    "common_mistakes": [
        {{"mistake": "よくある間違い", "correction": "正しい方法"}}
    ],
    "summary": ["まとめポイント"],
    "next_steps": ["関連ファイル", "次に学ぶべきこと"]
}}


重要:
- sequence_flowには、コンポーネント間のやり取りを「From -> To: メッセージ」形式の文字列配列で記述（例: ["User -> Tool: 実行", "Tool -> API: 依頼"]）
- process_stepsには、ユーザーが実行する操作手順を文字列配列で記述
日本語で、JSONのみを出力してください。
"""
    if not client:
        return {
            "title": f"{Path(file_path).name} マニュアル",
            "introduction": f"このファイルの使い方を説明します。",
            "sequence_flow": [],
            "process_steps": [],
            "prerequisites": [],
            "sections": [{"title": "概要", "content": file_content[:500], "code_example": "", "tips": []}],
            "common_mistakes": [],
            "summary": [],
            "next_steps": []
        }
    try:
        response = client.models.generate_content(model=get_flash_model(), contents=[prompt])
        content = response.text.strip()
        result = safe_parse_json(content)
        if result:
            print("✅ マニュアル生成完了")
            return result
        else:
            print("⚠️ JSONパース失敗")
            return {"title": file_path, "introduction": "", "sequence_flow": [], "process_steps": [], "prerequisites": [], "sections": [], "common_mistakes": [], "summary": [], "next_steps": []}
    except Exception as e:
        print(f"⚠️ 生成エラー: {e}")
        return {"title": file_path, "introduction": "", "sequence_flow": [], "process_steps": [], "prerequisites": [], "sections": [], "common_mistakes": [], "summary": [], "next_steps": []}


def generate_text_tutorial(client, text: str) -> dict:
    """テキストから解説を生成"""
    print("📖 入力テキストの解説を生成中...")
    prompt = f"""
あなたは教育のエキスパートです。以下のテキスト/コードについて、初心者向けの解説を作成してください。

```
{text[:8000]}
```

以下のJSON形式で出力:
{{
    "title": "解説のタイトル",
    "introduction": "このコード/テキストの概要",
    "sequence_flow": ["A -> B: 動作", "B -> A: 応答"],
    "prerequisites": ["前提知識1", "前提知識2"],
    "sections": [
        {{
            "title": "セクションタイトル",
            "content": "詳細な説明",
            "code_example": "関連コード例",
            "tips": ["ポイント"]
        }}
    ],
    "common_mistakes": [
        {{"mistake": "よくある間違い", "correction": "正しい方法"}}
    ],
    "summary": ["まとめポイント"],
    "next_steps": ["次に学ぶべきこと"]
}}

重要:
- sequence_flowには、テキスト内で説明されているプロセスや相互作用を「A -> B: 動作」の形式で記述してください（該当しない場合は空配列）。

日本語で、JSONのみを出力してください。
"""
    if not client:
        return {
            "title": "テキスト解説",
            "introduction": "入力されたテキストを解説します。",
            "sequence_flow": [],
            "prerequisites": [],
            "sections": [{"title": "内容", "content": text[:500], "code_example": "", "tips": []}],
            "common_mistakes": [],
            "summary": [],
            "next_steps": []
        }
    try:
        response = client.models.generate_content(model=get_flash_model(), contents=[prompt])
        content = response.text.strip()
        result = safe_parse_json(content)
        if result:
            print("✅ 解説生成完了")
            return result
        else:
            print("⚠️ JSONパース失敗")
            return {"title": "テキスト解説", "introduction": "", "sequence_flow": [], "prerequisites": [], "sections": [], "common_mistakes": [], "summary": [], "next_steps": []}
    except Exception as e:
        print(f"⚠️ 生成エラー: {e}")
        return {"title": "テキスト解説", "introduction": "", "sequence_flow": [], "prerequisites": [], "sections": [], "common_mistakes": [], "summary": [], "next_steps": []}


def analyze_learning_gaps(client, specstory_content: str) -> dict:
    """SpecStoryからユーザーがわかっていなそうな概念を抽出し、会話フローも生成"""
    print("📚 学習ギャップを分析中...")
    analysis_prompt = f"""
あなたは教育のエキスパートです。以下はCursor IDE（AIコーディングエディタ）での会話履歴です。

【Cursor IDEの特徴】
- @ファイルパス でファイルを直接参照・読み込み可能
- Agentモードではファイルの読み書き、シェルコマンド実行が可能
- AskQuestionツールでユーザーに選択肢を提示可能
- SpecStory拡張機能で会話履歴が自動保存される

上記のCursor機能を前提として、以下の2点を抽出してください:
1. ユーザーが理解していない概念（Cursorの基本機能は既知として扱う）
2. 会話における問題解決のフローや主要なやり取り

会話履歴:
{specstory_content[:8000]}

以下のJSON形式で出力:
{{
    "sequence_flow": ["User -> Assistant: 質問内容", "Assistant -> User: 回答内容", "User -> Tool: 操作"],
    "topics": [{{"topic": "トピック名", "reason": "なぜ必要か", "priority": "high/medium/low", "related_concepts": ["関連概念"]}}]
}}

重要:
- sequence_flowには、会話の主要なやり取りや問題解決の流れを「Actor -> Actor: メッセージ」形式で記述してください（該当しない場合は空配列）。
- Actorの例: User, Assistant, Tool, API, File, Database など

JSONのみを出力。
"""
    default_result = {"sequence_flow": [], "topics": [{"topic": "会話内容の理解", "reason": "履歴から学習が必要", "priority": "medium", "related_concepts": []}]}
    if not client:
        return default_result
    try:
        response = client.models.generate_content(model=get_flash_model(), contents=[analysis_prompt])
        content = response.text.strip()
        result = safe_parse_json(content)
        if result:
            topic_count = len(result.get("topics", []))
            flow_count = len(result.get("sequence_flow", []))
            print(f"✅ 分析完了: {topic_count}個のトピック, {flow_count}ステップのフローを抽出")
            return result
        else:
            print("⚠️ JSONパース失敗")
            return {"sequence_flow": [], "topics": []}
    except Exception as e:
        print(f"⚠️ 分析エラー: {e}")
        return {"sequence_flow": [], "topics": []}


def generate_learning_content(client, topic: str, reason: str, related_concepts: list) -> dict:
    """学習コンテンツを生成"""
    print(f"📖 学習コンテンツを生成中: {topic}")
    content_prompt = f"""
トピック「{topic}」について、初心者向けに説明してください。
学習が必要な理由: {reason}
関連概念: {', '.join(related_concepts) if related_concepts else 'なし'}

以下のJSON形式で出力:
{{"prerequisites": ["前提知識"], "concept": "概念の説明", "examples": [{{"title": "例", "description": "説明", "code": "コード例"}}], "common_mistakes": [{{"mistake": "間違い", "explanation": "正しい方法"}}], "summary": ["ポイント"]}}

日本語で、JSONのみを出力。
"""
    if not client:
        return {"prerequisites": ["基礎知識"], "concept": f"{topic}について学習しましょう。", "examples": [], "common_mistakes": [], "summary": [f"{topic}の基礎を理解する"]}
    try:
        response = client.models.generate_content(model=get_flash_model(), contents=[content_prompt])
        content = response.text.strip()
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        return json.loads(content)
    except Exception as e:
        print(f"⚠️ コンテンツ生成エラー: {e}")
        return {"prerequisites": ["基礎知識"], "concept": f"{topic}について学習しましょう。", "examples": [], "common_mistakes": [], "summary": [f"{topic}の基礎を理解する"]}


def create_svg_diagram(topic: str) -> str:
    """シンプルなSVG図解を生成"""
    return f"""
    <svg width="800" height="200" xmlns="http://www.w3.org/2000/svg" style="background: white; border-radius: 5px; margin: 20px 0;">
        <rect width="800" height="200" fill="white"/>
        <text x="400" y="40" font-family="sans-serif" font-size="20" font-weight="bold" fill="#2563EB" text-anchor="middle">{topic}</text>
        <circle cx="150" cy="120" r="50" fill="#dbeafe" stroke="#2563EB" stroke-width="2"/>
        <text x="150" y="125" font-family="sans-serif" font-size="14" fill="#1e40af" text-anchor="middle">概念</text>
        <path d="M 200 120 L 300 120" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow)"/>
        <circle cx="400" cy="120" r="50" fill="#fef3c7" stroke="#FBBF24" stroke-width="2"/>
        <text x="400" y="125" font-family="sans-serif" font-size="14" fill="#92400e" text-anchor="middle">実践</text>
        <path d="M 450 120 L 550 120" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow)"/>
        <circle cx="650" cy="120" r="50" fill="#d1fae5" stroke="#10b981" stroke-width="2"/>
        <text x="650" y="125" font-family="sans-serif" font-size="14" fill="#065f46" text-anchor="middle">理解</text>
        <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6" fill="#2563EB"/></marker></defs>
    </svg>"""


def sanitize_plantuml_text(text: str) -> str:
    """PlantUMLアクティビティ図用にテキストをサニタイズ"""
    # 括弧を全角に変換（PlantUMLの構文と衝突を防ぐ）
    text = text.replace('(', '（').replace(')', '）')
    # 山括弧をエスケープ
    text = text.replace('<', '＜').replace('>', '＞')
    # 改行をスペースに
    text = text.replace('\n', ' ')
    # セミコロンはPlantUMLの区切り文字なのでエスケープ
    text = text.replace(';', '；')
    return text

def build_sequence_plantuml(sequence_flow: list) -> str:
    """sequence_flowからPlantUMLシーケンス図を生成"""
    if not sequence_flow:
        return ""
    lines = [
        "@startuml",
        "skinparam backgroundColor white",
        "skinparam maxMessageSize 250",
        "skinparam wrapWidth 200",
        "skinparam responseMessageBelowArrow true",
        "skinparam sequenceMessageAlign center",
    ]# 参加者を順序保持で取得
    participants = []
    messages = []
    for item in sequence_flow:
        # "From -> To: message" 形式をパース
        if " -> " in item and ": " in item:
            parts = item.split(": ", 1)
            actors = parts[0].split(" -> ")
            if len(actors) == 2:
                from_actor, to_actor = actors[0].strip(), actors[1].strip()
                msg = parts[1] if len(parts) > 1 else ""
                if from_actor not in participants:
                    participants.append(from_actor)
                if to_actor not in participants:
                    participants.append(to_actor)
                messages.append((from_actor, to_actor, msg))
    for p in participants:
        lines.append(f'participant "{p}"')
    for from_actor, to_actor, msg in messages:
        lines.append(f'"{from_actor}" -> "{to_actor}": {msg}')
    lines.append("@enduml")
    return "\n".join(lines)


def build_tutorial_html(tutorial_data: dict, source_info: str = "") -> str:
    """チュートリアル形式のHTMLを組み立て"""
    html_parts = []
    
    if source_info:
        html_parts.append(f'<div class="info-box"><p><strong>📁 入力ソース:</strong> {source_info}</p></div>')
    
     # シーケンス図（処理フロー）
    sequence_flow = tutorial_data.get("sequence_flow", [])
    if sequence_flow and isinstance(sequence_flow, list) and len(sequence_flow) > 0:
        seq_plantuml = build_sequence_plantuml(sequence_flow)
        if seq_plantuml:
            html_parts.append('<h2>🔄 処理フロー（システム）</h2>')
            html_parts.append('<div class="flow-diagram">')
            html_parts.append(generate_plantuml_img_tag(seq_plantuml, "処理フロー"))
            html_parts.append('</div>')
    
    # アクティビティ図（手順フロー）
    process_steps = tutorial_data.get("process_steps", [])
    if process_steps and isinstance(process_steps, list) and len(process_steps) > 0:
        html_parts.append('<h2>📋 手順フロー（ユーザー操作）</h2>')
        html_parts.append('<div class="flow-diagram">')
        steps_plantuml = [
            "@startuml",
            "skinparam backgroundColor white",
            "skinparam wrapWidth 300",
            "skinparam ActivityFontSize 14",
            "start"
        ]
        for step in process_steps:
            sanitized_step = sanitize_plantuml_text(step)
            steps_plantuml.append(f":{sanitized_step};")
        steps_plantuml.append("stop")
        steps_plantuml.append("@enduml")
        flow_plantuml = "\n".join(steps_plantuml)
        html_parts.append(generate_plantuml_img_tag(flow_plantuml, "手順フロー"))
        html_parts.append('</div>')
    
    # イントロダクション
    if tutorial_data.get("introduction"):
        html_parts.append('<div class="info-box">')
        html_parts.append('<h2>📚 概要</h2>')
        html_parts.append(f'<p>{tutorial_data["introduction"]}</p>')
        html_parts.append('</div>')
    
    # 前提知識
    if tutorial_data.get("prerequisites"):
        html_parts.append('<h2>📋 前提知識</h2>')
        html_parts.append('<ul>')
        for prereq in tutorial_data["prerequisites"]:
            html_parts.append(f'<li>{prereq}</li>')
        html_parts.append('</ul>')
    
    # セクション
    sections = tutorial_data.get("sections", [])
    for idx, section in enumerate(sections, 1):
        html_parts.append(f'<div class="step">')
        html_parts.append(f'<h2><span class="step-number">{idx}</span>{section.get("title", "セクション")}</h2>')
        
        if section.get("content"):
            html_parts.append(f'<p>{section["content"]}</p>')
        
        if section.get("code_example"):
            code_content = section["code_example"]
            if isinstance(code_content, (dict, list)):
                code_str = json.dumps(code_content, indent=2, ensure_ascii=False)
            else:
                code_str = str(code_content)
            code = code_str.replace('<', '&lt;').replace('>', '&gt;')
            html_parts.append(f'<pre><code>{code}</code></pre>')
        
        if section.get("tips"):
            html_parts.append('<div class="info-box"><strong>💡 ポイント:</strong><ul>')
            for tip in section["tips"]:
                html_parts.append(f'<li>{tip}</li>')
            html_parts.append('</ul></div>')
        
        html_parts.append('</div>')
    
    # よくある間違い
    if tutorial_data.get("common_mistakes"):
        html_parts.append('<h2>⚠️ よくある間違い</h2>')
        for mistake in tutorial_data["common_mistakes"]:
            html_parts.append('<div class="warning-box">')
            html_parts.append(f'<p><strong>❌ {mistake.get("mistake", "")}</strong></p>')
            html_parts.append(f'<p>✅ {mistake.get("correction", mistake.get("explanation", ""))}</p>')
            html_parts.append('</div>')
    
    # まとめ
    if tutorial_data.get("summary"):
        html_parts.append('<h2>✅ まとめ</h2>')
        html_parts.append('<div class="success-box"><ul>')
        for point in tutorial_data["summary"]:
            html_parts.append(f'<li>{point}</li>')
        html_parts.append('</ul></div>')
    
    # 次のステップ
    if tutorial_data.get("next_steps"):
        html_parts.append('<h2>🚀 次のステップ</h2>')
        html_parts.append('<ul>')
        for step in tutorial_data["next_steps"]:
            html_parts.append(f'<li>{step}</li>')
        html_parts.append('</ul>')
    
    return "".join(html_parts)


def build_specstory_html(topics_data: dict, client, referenced_files: list) -> str:
    """SpecStory分析のHTMLを組み立て（動的フロー図対応）"""
    html_parts = []
    html_parts.append(build_referenced_files_html(referenced_files))
    
    # 動的シーケンス図（会話フロー）
    sequence_flow = topics_data.get("sequence_flow", []) if isinstance(topics_data, dict) else []
    if sequence_flow and isinstance(sequence_flow, list) and len(sequence_flow) > 0:
        seq_plantuml = build_sequence_plantuml(sequence_flow)
        if seq_plantuml:
            html_parts.append('<h2>🔄 会話フロー</h2>')
            html_parts.append('<div class="flow-diagram">')
            html_parts.append(generate_plantuml_img_tag(seq_plantuml, "会話フロー"))
            html_parts.append('</div>')
    
    html_parts.append('<div class="info-box">')
    html_parts.append('<h2>📚 学習ガイド</h2>')
    html_parts.append('<p>このページは、あなたの会話履歴から抽出された学習が必要なトピックをまとめています。</p>')
    html_parts.append('</div>')

    try:
        topics_json = topics_data if isinstance(topics_data, dict) else json.loads(topics_data)
        topics = topics_json.get("topics", [])
    except:
        topics = []

    if not topics:
        html_parts.append('<div class="warning-box"><p>学習トピックが見つかりませんでした。</p></div>')
        return "".join(html_parts)

    for idx, topic_data in enumerate(topics, 1):
        topic = topic_data.get("topic", "不明なトピック")
        reason = topic_data.get("reason", "")
        related = topic_data.get("related_concepts", [])

        html_parts.append(f'<div class="step">')
        html_parts.append(f'<h2><span class="step-number">{idx}</span>{topic}</h2>')
        if reason:
            html_parts.append(f'<p><strong>なぜ学ぶか:</strong> {reason}</p>')
        if related:
            html_parts.append(f'<p><strong>関連概念:</strong> {", ".join(related)}</p>')

        content = generate_learning_content(client, topic, reason, related)

        if content.get("prerequisites"):
            html_parts.append('<h3>📋 前提知識</h3><ul>')
            for prereq in content["prerequisites"]:
                html_parts.append(f'<li>{prereq}</li>')
            html_parts.append('</ul>')

        if content.get("concept"):
            html_parts.append('<h3>💡 概念の説明</h3>')
            html_parts.append(f'<p>{content["concept"]}</p>')

        html_parts.append(create_svg_diagram(topic))

        if content.get("examples"):
            html_parts.append('<h3>📝 具体例</h3>')
            for example in content["examples"]:
                html_parts.append(f'<h4>{example.get("title", "例")}</h4>')
                html_parts.append(f'<p>{example.get("description", "")}</p>')
                if example.get("code"):
                    code_content = example["code"]
                    if isinstance(code_content, (dict, list)):
                        code_str = json.dumps(code_content, indent=2, ensure_ascii=False)
                    else:
                        code_str = str(code_content)
                    code = code_str.replace('<', '&lt;').replace('>', '&gt;')
                    html_parts.append(f'<pre><code>{code}</code></pre>')

        if content.get("common_mistakes"):
            html_parts.append('<h3>⚠️ よくある間違い</h3>')
            for mistake in content["common_mistakes"]:
                html_parts.append('<div class="warning-box">')
                html_parts.append(f'<p><strong>❌ {mistake.get("mistake", "")}</strong></p>')
                html_parts.append(f'<p>✅ {mistake.get("explanation", "")}</p>')
                html_parts.append('</div>')

        if content.get("summary"):
            html_parts.append('<h3>✅ まとめ</h3><ul>')
            for point in content["summary"]:
                html_parts.append(f'<li>{point}</li>')
            html_parts.append('</ul>')

        html_parts.append('</div>')

    return "".join(html_parts)


def main():
    parser = argparse.ArgumentParser(description="学習コンテンツ生成ツール")
    
    # 入力ソースオプション
    parser.add_argument("--topic", "-t", help="トピックを指定してチュートリアル生成")
    parser.add_argument("--file", help="ファイルパスを指定してマニュアル生成")
    parser.add_argument("--text", help="テキストを指定して解説生成")
    parser.add_argument("--specstory", action="store_true", help="SpecStory履歴から学習ギャップ分析")
    
    # SpecStory関連オプション
    parser.add_argument("--files", "-f", type=int, default=1, help="分析するSpecStoryファイル数")
    parser.add_argument("--list", "-l", action="store_true", help="SpecStoryファイル一覧を表示")
    parser.add_argument("--json", "-j", action="store_true", help="JSON形式で出力（--listと併用）")
    parser.add_argument("--select", "-s", help="ファイルを番号で指定（例: 1,2,3）")
    parser.add_argument("--names", "-n", help="ファイル名で指定（カンマ区切り）")
    
    # 出力オプション
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    
    args = parser.parse_args()

    print("=" * 60)
    print("Tutor - 学習コンテンツ生成")
    print("=" * 60)

    # ファイル一覧表示
    if args.list:
        files_info = list_specstory_files_for_selection(10)
        if not files_info:
            print("❌ SpecStory履歴が見つかりません。")
            sys.exit(1)
        if args.json:
            print(list_specstory_files_json(10))
        else:
            print_specstory_file_list(files_info)
        sys.exit(0)

    client = get_client()
    if not client:
        print("⚠️ Gemini APIキーが未設定。基本コンテンツのみ生成します。")

    html_content = ""
    title = "学習ガイド - Tutor"

    # トピックモード
    if args.topic:
        print(f"📝 モード: トピック指定")
        tutorial_data = generate_topic_tutorial(client, args.topic)
        title = tutorial_data.get("title", f"{args.topic} チュートリアル")
        html_content = build_tutorial_html(tutorial_data, f"トピック: {args.topic}")
    
    # ファイルモード
    elif args.file:
        print(f"📝 モード: ファイル指定")
        tutorial_data = generate_file_tutorial(client, args.file)
        title = tutorial_data.get("title", f"{Path(args.file).name} マニュアル")
        html_content = build_tutorial_html(tutorial_data, f"ファイル: {args.file}")
    
    # テキストモード
    elif args.text:
        print(f"📝 モード: テキスト指定")
        tutorial_data = generate_text_tutorial(client, args.text)
        title = tutorial_data.get("title", "テキスト解説")
        html_content = build_tutorial_html(tutorial_data, "入力テキスト")
    
    # SpecStoryモード（デフォルト）
    else:
        print(f"📝 モード: SpecStory分析")
        referenced_files = []
        
        if args.names:
            filenames = [f.strip() for f in args.names.split(',')]
            selected_files = get_specstory_files_by_names(filenames)
            if not selected_files:
                print("❌ 有効なファイルが見つかりません。--list で確認してください。")
                sys.exit(1)
            specstory_content, referenced_files = get_specstory_content_from_files(selected_files)
            print(f"📁 選択された {len(selected_files)} 個のファイルを分析します")
        elif args.select:
            files_info = list_specstory_files_for_selection(10)
            if not files_info:
                print("❌ SpecStory履歴が見つかりません。")
                sys.exit(1)
            selected_files = get_selected_specstory_files(args.select, files_info)
            if not selected_files:
                print("❌ 有効なファイルが選択されていません。--list で確認してください。")
                sys.exit(1)
            specstory_content, referenced_files = get_specstory_content_from_files(selected_files)
            print(f"📁 選択された {len(selected_files)} 個のファイルを分析します")
        else:
            files = get_latest_specstory_files(args.files)
            if not files:
                print("❌ SpecStory履歴が見つかりません。")
                sys.exit(1)
            specstory_content, referenced_files = get_specstory_content_from_files(files)
            print(f"📁 最新 {len(files)} 個のファイルを分析します")

        for f in referenced_files:
            print(f"   - {f}")

        topics_data = analyze_learning_gaps(client, specstory_content)
        html_content = build_specstory_html(topics_data, client, referenced_files)

    # 出力
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = DEFAULT_TUTOR_DIR / f"tutor_{timestamp}.html"

    full_html = create_html_template(title, html_content)
    save_html_file(full_html, output_path, title)


if __name__ == "__main__":
    main()

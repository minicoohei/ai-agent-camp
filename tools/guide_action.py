"""
Guide - 次のアクション提示ツール
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

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
    build_referenced_files_html,
)

DEFAULT_GUIDE_DIR = DEFAULT_OUTPUT_DIR / "guide"


def analyze_current_situation(client, specstory_content: str) -> dict:
    """現在の状況を分析"""
    print("現在の状況を分析中...")
    analysis_prompt = f"""
    あなたはプロジェクト管理のエキスパートです。以下の会話履歴を分析してください。

会話履歴:
{specstory_content[:8000]}

以下のJSON形式で出力:
{{"current_task": "現在の作業内容", "progress": "進捗状況", "challenges": ["課題1"], "next_steps": ["次のステップ1"], "context": "全体の文脈"}}

JSONのみを出力。
"""
    if not client:
        return {"current_task": "会話履歴の分析", "progress": "確認中", "challenges": [], "next_steps": ["次のアクションを決定"], "context": "SpecStory履歴から状況を把握"}
    try:
        response = client.models.generate_content(model=get_flash_model(), contents=[analysis_prompt])
        content = response.text.strip()
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        result = json.loads(content)
        print("分析完了")
        return result
    except Exception as e:
        print(f"分析エラー: {e}")
        return {"current_task": "会話履歴の分析", "progress": "確認中", "challenges": [], "next_steps": ["次のアクションを決定"], "context": "SpecStory履歴から状況を把握"}


def generate_background_explanation(client, situation: dict, specstory_content: str) -> str:
    """背景説明を生成"""
    print("背景説明を生成中...")
    background_prompt = f"""
以下の状況を基に、なぜこの作業が必要か説明してください。

現在の作業: {situation.get('current_task', '')}
進捗: {situation.get('progress', '')}
次のステップ: {', '.join(situation.get('next_steps', []))}

会話履歴:
{specstory_content[:4000]}

わかりやすく説明してください。Markdown記法は使わないでください。
"""
    if not client:
        return f"この作業は、{situation.get('current_task', '現在のタスク')}を進めるためのものです。"
    try:
        response = client.models.generate_content(model=get_flash_model(), contents=[background_prompt])
        print("背景説明を生成完了")
        return response.text.strip()
    except Exception as e:
        print(f"背景説明生成エラー: {e}")
        return f"この作業は、{situation.get('current_task', '現在のタスク')}を進めるためのものです。"


def generate_prompt_example(client, situation: dict, background: str) -> str:
    """プロンプト例を生成"""
    print("プロンプト例を生成中...")
    prompt_prompt = f"""
以下の状況を基に、新しいAgentに入力するプロンプト例を生成してください。

作業内容: {situation.get('current_task', '')}
進捗: {situation.get('progress', '')}
次のステップ: {', '.join(situation.get('next_steps', []))}

プロンプト例のみを出力してください。
"""
    if not client:
        next_step = situation.get('next_steps', ['次のアクションを実行'])[0] if situation.get('next_steps') else '次のアクションを実行'
        return f"{situation.get('current_task', '現在のタスク')}を進めています。\n次のステップとして、{next_step}を実行してください。"
    try:
        response = client.models.generate_content(model=get_flash_model(), contents=[prompt_prompt])
        print("プロンプト例を生成完了")
        return response.text.strip()
    except Exception as e:
        print(f"プロンプト生成エラー: {e}")
        return f"{situation.get('current_task', '現在のタスク')}を進めてください。"


def build_html_content(situation: dict, background: str, prompt_example: str, referenced_files: list) -> str:
    """HTMLコンテンツを組み立て"""
    html_parts = []
    html_parts.append(build_referenced_files_html(referenced_files))
    html_parts.append('<div class="info-box">')
    html_parts.append('<h2>現在の状況</h2>')
    html_parts.append(f'<p><strong>作業内容:</strong> {situation.get("current_task", "不明")}</p>')
    html_parts.append(f'<p><strong>進捗:</strong> {situation.get("progress", "確認中")}</p>')
    challenges = situation.get("challenges", [])
    if challenges:
        html_parts.append('<p><strong>課題:</strong></p><ul>')
        for c in challenges:
            html_parts.append(f'<li>{c}</li>')
        html_parts.append('</ul>')
    html_parts.append('</div>')
    html_parts.append('<h2>背景・文脈</h2>')
    html_parts.append('<div class="step">')
    html_parts.append(markdown_to_html(background))
    html_parts.append('</div>')
    html_parts.append('<h2>次のアクション</h2>')
    next_steps = situation.get("next_steps", [])
    if next_steps:
        for idx, step in enumerate(next_steps, 1):
            html_parts.append(f'<div class="step"><span class="step-number">{idx}</span><strong>{step}</strong></div>')
    else:
        html_parts.append('<div class="warning-box"><p>次のアクションが特定できませんでした。</p></div>')
    html_parts.append('<h2>次のAgentで使うプロンプト例</h2>')
    html_parts.append(f'<div class="prompt-box">{prompt_example}</div>')
    html_parts.append('<div class="info-box"><p><strong>使い方:</strong> 上記のプロンプトをコピーして、新しいAgentに入力してください。</p></div>')
    html_parts.append('<h2>期待される結果</h2>')
    html_parts.append('<div class="success-box"><p>このアクションで以下が達成されます:</p><ul>')
    for step in next_steps[:3]:
        html_parts.append(f'<li>{step}が完了する</li>')
    html_parts.append('</ul></div>')
    return "".join(html_parts)


def main():
    parser = argparse.ArgumentParser(description="SpecStory履歴から次のアクションを提示")
    parser.add_argument("--files", "-f", type=int, default=3, help="分析するファイル数")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument("--list", "-l", action="store_true", help="ファイル一覧を表示")
    parser.add_argument("--json", "-j", action="store_true", help="JSON形式で出力（--listと併用）")
    parser.add_argument("--select", "-s", help="ファイルを番号で指定（例: 1,2,3）")
    parser.add_argument("--names", "-n", help="ファイル名で指定（カンマ区切り）")
    args = parser.parse_args()

    print("=" * 60)
    print("Guide - 次のアクション提示")
    print("=" * 60)

    if args.list:
        files_info = list_specstory_files_for_selection(10)
        if not files_info:
            print("SpecStory履歴が見つかりません。")
            sys.exit(1)
        if args.json:
            print(list_specstory_files_json(10))
        else:
            print_specstory_file_list(files_info)
        sys.exit(0)

    referenced_files = []
    if args.names:
        filenames = [f.strip() for f in args.names.split(',')]
        selected_files = get_specstory_files_by_names(filenames)
        if not selected_files:
            print("有効なファイルが見つかりません。--list で確認してください。")
            sys.exit(1)
        specstory_content, referenced_files = get_specstory_content_from_files(selected_files)
        print(f"選択された {len(selected_files)} 個のファイルを分析します")
    elif args.select:
        files_info = list_specstory_files_for_selection(10)
        if not files_info:
            print("SpecStory履歴が見つかりません。")
            sys.exit(1)
        selected_files = get_selected_specstory_files(args.select, files_info)
        if not selected_files:
            print("有効なファイルが選択されていません。--list で確認してください。")
            sys.exit(1)
        specstory_content, referenced_files = get_specstory_content_from_files(selected_files)
        print(f"選択された {len(selected_files)} 個のファイルを分析します")
    else:
        files = get_latest_specstory_files(args.files)
        if not files:
            print("SpecStory履歴が見つかりません。")
            sys.exit(1)
        specstory_content, referenced_files = get_specstory_content_from_files(files)
        print(f"最新 {len(files)} 個のファイルを分析します")

    for f in referenced_files:
        print(f"   - {f}")

    client = get_client()
    if not client:
        print("Gemini APIキーが未設定。基本分析のみ実行します。")

    situation = analyze_current_situation(client, specstory_content)
    background = generate_background_explanation(client, situation, specstory_content)
    prompt_example = generate_prompt_example(client, situation, background)
    html_content = build_html_content(situation, background, prompt_example, referenced_files)

    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = DEFAULT_GUIDE_DIR / f"guide_{timestamp}.html"

    full_html = create_html_template("次のアクション - Guide", html_content)
    save_html_file(full_html, output_path, "次のアクション - Guide")


if __name__ == "__main__":
    main()

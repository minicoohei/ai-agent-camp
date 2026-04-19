"""
Cursor Bootcamp 共通ユーティリティ

SpecStory履歴の取得・パース、HTMLテンプレート生成、Gemini APIクライアント初期化を提供
"""

import base64
import json
import os
import re
import sys
import urllib.request
import zlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runtime_env import load_runtime_env

SPECSTORY_DIR = Path(".specstory/history")
DEFAULT_OUTPUT_DIR = Path("docs/bootcamp")
PLANTUML_SERVER = "https://www.plantuml.com/plantuml/svg/"

# Gemini モデル設定（.env で上書き可能）
DEFAULT_FLASH_MODEL = "gemini-3-flash-preview"
DEFAULT_IMAGE_MODEL = "nano-banana-pro-preview"

load_runtime_env()



def get_client():
    """Google GenAI クライアントを初期化して返す"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    from google import genai
    return genai.Client(api_key=api_key)


def get_flash_model() -> str:
    """テキスト処理用Flashモデル名を取得（.env で GEMINI_FLASH_MODEL を設定可能）"""
    return os.environ.get("GEMINI_FLASH_MODEL", DEFAULT_FLASH_MODEL)


def get_image_model() -> str:
    """画像生成用モデル名を取得（.env で GEMINI_IMAGE_MODEL を設定可能）"""
    return os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_IMAGE_MODEL)




def get_latest_specstory_files(limit: int = 10) -> List[Path]:
    """SpecStory履歴から最新のファイルを取得"""
    if not SPECSTORY_DIR.exists():
        return []
    files = sorted(SPECSTORY_DIR.glob("*.md"), key=lambda p: p.name, reverse=True)
    return files[:limit]


def parse_specstory_file(file_path: Path) -> Dict:
    """SpecStoryファイルをパースして構造化データを返す"""
    content = file_path.read_text(encoding="utf-8")
    title_match = re.search(r'^# (.+?)\s*\(', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file_path.stem
    session_match = re.search(r'cursor Session ([a-f0-9-]+)', content)
    session_id = session_match.group(1) if session_match else ""
    timestamp_match = re.search(r'\((\d{4}-\d{2}-\d{2} \d{2}:\d{2}Z)\)', content)
    timestamp = timestamp_match.group(1) if timestamp_match else ""
    user_pattern = r'_\*\*User\*\*_\s*\n\n(.*?)(?=\n---\n|_\*\*Agent|$)'
    user_matches = re.findall(user_pattern, content, re.DOTALL)
    user_messages = [m.strip() for m in user_matches if m.strip()]
    agent_pattern = r'_\*\*Agent[^_]*_\*\*_\s*\n\n(.*?)(?=\n---\n|_\*\*User|$)'
    agent_matches = re.findall(agent_pattern, content, re.DOTALL)
    agent_messages = [m.strip() for m in agent_matches if m.strip()]
    return {
        "title": title,
        "session_id": session_id,
        "timestamp": timestamp,
        "user_messages": user_messages,
        "agent_messages": agent_messages,
        "raw_content": content
    }


def get_recent_specstory_content(limit: int = 5) -> str:
    """最近のSpecStory履歴の内容を結合して返す"""
    files = get_latest_specstory_files(limit)
    if not files:
        return ""
    contents = []
    for file_path in files:
        parsed = parse_specstory_file(file_path)
        contents.append(f"# {parsed['title']} ({parsed['timestamp']})\n\n")
        contents.append("## User Messages\n")
        for msg in parsed['user_messages']:
            contents.append(f"{msg}\n\n")
        contents.append("## Agent Messages\n")
        for msg in parsed['agent_messages']:
            contents.append(f"{msg}\n\n")
        contents.append("---\n\n")
    return "".join(contents)


def extract_title_from_filename(filename: str) -> str:
    """SpecStoryファイル名からタイトルを抽出"""
    match = re.match(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}Z-(.+)\.md$', filename)
    if match:
        return match.group(1).replace('-', ' ').title()
    return filename


def extract_timestamp_from_filename(filename: str) -> str:
    """SpecStoryファイル名からタイムスタンプを抽出"""
    match = re.match(r'(\d{4}-\d{2}-\d{2})_(\d{2})-(\d{2})Z', filename)
    if match:
        return f"{match.group(1)} {match.group(2)}:{match.group(3)}Z"
    return ""


def list_specstory_files_for_selection(limit: int = 10) -> List[Dict]:
    """選択用にSpecStoryファイル一覧を整形して返す"""
    files = get_latest_specstory_files(limit)
    result = []
    for idx, f in enumerate(files, 1):
        parsed = parse_specstory_file(f)
        result.append({
            "index": idx,
            "filename": f.name,
            "path": f,
            "title": parsed.get("title", extract_title_from_filename(f.name)),
            "timestamp": extract_timestamp_from_filename(f.name)
        })
    return result


def print_specstory_file_list(files_info: List[Dict]) -> None:
    """SpecStoryファイル一覧をコンソールに表示"""
    print("\n" + "=" * 70)
    print("SpecStory履歴ファイル一覧")
    print("=" * 70)
    for info in files_info:
        print(f"  [{info['index']:2d}] {info['timestamp']} - {info['title']}")
        print(f"       ファイル: {info['filename']}")
    print("=" * 70)
    print("使用方法: --select 1,2,3 で番号指定、または --files N で最新N件")
    print("=" * 70 + "\n")


def get_selected_specstory_files(selection: str, available_files: List[Dict]) -> List[Path]:
    """選択文字列からSpecStoryファイルのパスリストを取得"""
    selected_paths = []
    parts = selection.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part and not part.startswith('-'):
            try:
                start, end = map(int, part.split('-'))
                for idx in range(start, end + 1):
                    if 1 <= idx <= len(available_files):
                        selected_paths.append(available_files[idx - 1]['path'])
            except ValueError:
                continue
        else:
            try:
                idx = int(part)
                if 1 <= idx <= len(available_files):
                    selected_paths.append(available_files[idx - 1]['path'])
            except ValueError:
                continue
    return selected_paths


def get_specstory_files_by_names(filenames: List[str]) -> List[Path]:
    """ファイル名リストからSpecStoryファイルのパスリストを取得"""
    if not SPECSTORY_DIR.exists():
        return []
    selected_paths = []
    for filename in filenames:
        filename = filename.strip()
        file_path = SPECSTORY_DIR / filename
        if file_path.exists():
            selected_paths.append(file_path)
    return selected_paths


def list_specstory_files_json(limit: int = 10) -> str:
    """AskQuestion用にSpecStoryファイル一覧をJSON形式で返す"""
    files_info = list_specstory_files_for_selection(limit)
    json_output = []
    for info in files_info:
        json_output.append({
            "id": info['filename'],
            "label": f"{info['timestamp']} - {info['title']}"
        })
    return json.dumps(json_output, ensure_ascii=False, indent=2)


def get_specstory_content_from_files(files: List[Path]) -> Tuple[str, List[str]]:
    """指定されたSpecStoryファイルから内容を取得"""
    contents = []
    filenames = []
    for file_path in files:
        if file_path.exists():
            parsed = parse_specstory_file(file_path)
            contents.append(f"# {parsed['title']} ({parsed['timestamp']})\n\n")
            contents.append("## User Messages\n")
            for msg in parsed['user_messages']:
                contents.append(f"{msg}\n\n")
            contents.append("## Agent Messages\n")
            for msg in parsed['agent_messages']:
                contents.append(f"{msg}\n\n")
            contents.append("---\n\n")
            filenames.append(file_path.name)
    return "".join(contents), filenames


def markdown_to_html(text: str) -> str:
    """Markdown記法をHTMLに変換"""
    if not text:
        return ""
    html = text
    
    # コードブロックを保護
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks) - 1}__"
    
    code_block_pattern = r'```[^\n]*\n.*?\n```'
    html = re.sub(code_block_pattern, save_code_block, html, flags=re.DOTALL)
    
    # 見出し
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 太字・斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', html)
    
    # インラインコード
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 水平線
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)
    
    # 番号付きリスト
    def convert_numbered_list(match):
        items = match.group(0).strip().split('\n')
        list_html = '<ol>\n'
        for item in items:
            item_match = re.match(r'\d+\.\s+(.+)', item)
            if item_match:
                list_html += f'  <li>{item_match.group(1)}</li>\n'
        list_html += '</ol>'
        return list_html
    
    html = re.sub(r'(^\d+\.\s+.+$\n?)+', convert_numbered_list, html, flags=re.MULTILINE)
    
    # 箇条書きリスト
    def convert_bullet_list(match):
        items = match.group(0).strip().split('\n')
        list_html = '<ul>\n'
        for item in items:
            item_match = re.match(r'^[-*]\s+(.+)', item)
            if item_match:
                list_html += f'  <li>{item_match.group(1)}</li>\n'
        list_html += '</ul>'
        return list_html
    
    html = re.sub(r'(^[-*]\s+.+$\n?)+', convert_bullet_list, html, flags=re.MULTILINE)
    
    # 段落処理
    paragraphs = html.split('\n\n')
    processed_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if re.match(r'^<(h[1-6]|ul|ol|hr|div|pre|p)', p):
            processed_paragraphs.append(p)
        elif p.startswith('__CODE_BLOCK_'):
            processed_paragraphs.append(p)
        else:
            p = p.replace('\n', '<br>\n')
            processed_paragraphs.append(f'<p>{p}</p>')
    
    html = '\n\n'.join(processed_paragraphs)
    
    # コードブロック復元
    for idx, code_block in enumerate(code_blocks):
        code_match = re.match(r'```(\w*)\n(.*)\n```', code_block, re.DOTALL)
        if code_match:
            lang = code_match.group(1)
            code = code_match.group(2).replace('<', '&lt;').replace('>', '&gt;')
            replacement = f'<pre><code class="language-{lang}">{code}</code></pre>'
        else:
            code_content = code_block.replace('```', '').strip()
            code_content = code_content.replace('<', '&lt;').replace('>', '&gt;')
            replacement = f'<pre><code>{code_content}</code></pre>'
        html = html.replace(f'__CODE_BLOCK_{idx}__', replacement)
    
    return html


def plantuml_encode(text: str) -> str:
    """PlantUMLテキストをURLエンコード（正しいDeflate + Base64変換）"""
    utf8_encoded = text.encode('utf-8')
    
    # 正しいDeflate圧縮（wbits=-15でヘッダーなし）
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(utf8_encoded) + compressor.flush()
    
    # 標準Base64 → PlantUML文字セットへ変換
    base64_encoded = base64.b64encode(compressed).decode('utf-8')
    standard_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    plantuml_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    return base64_encoded.translate(str.maketrans(standard_chars, plantuml_chars))



def generate_plantuml_url(plantuml_code: str) -> str:
    """PlantUMLコードからSVG画像のURLを生成"""
    encoded = plantuml_encode(plantuml_code)
    return f"{PLANTUML_SERVER}{encoded}"


def validate_plantuml_url(url: str, timeout: int = 5) -> bool:
    """PlantUML URLが有効かどうかを確認"""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False



def generate_plantuml_img_tag(plantuml_code: str, alt_text: str = "処理フロー図", validate: bool = False) -> str:
    """
    PlantUMLコードからimgタグを生成。生成失敗やURL無効時はコードブロックにフォールバック。

    Args:
        plantuml_code (str): PlantUMLのコード
        alt_text (str): 画像のalt属性
        validate (bool): TrueでURLの有効性を検証

    Returns:
        str: imgタグまたはコードブロック付き警告HTML
    """
    url = generate_plantuml_url(plantuml_code)
    is_valid = True
    if validate:
        is_valid = validate_plantuml_url(url, timeout=10)
    if is_valid:
        return f'<img src="{url}" alt="{alt_text}" style="max-width: 100%; margin: 20px 0;">'
    else:
        escaped = (
            plantuml_code
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
        )
        return f'<div class="warning-box"><p>図の生成に失敗しました</p><pre><code>{escaped}</code></pre></div>'


def build_referenced_files_html(filenames: List[str]) -> str:
    """参照したSpecStoryファイル一覧のHTMLを生成"""
    if not filenames:
        return ""
    html_parts = ['<div class="info-box">', '<h3>参照したSpecStoryファイル</h3>', '<ul>']
    for filename in filenames:
        title = extract_title_from_filename(filename)
        timestamp = extract_timestamp_from_filename(filename)
        html_parts.append(f'<li><strong>{title}</strong> ({timestamp})<br><code>{filename}</code></li>')
    html_parts.extend(['</ul>', '</div>'])
    return '\n'.join(html_parts)


def create_html_template(title: str, content: str, css_extra: str = "") -> str:
    """共通HTMLテンプレートを生成"""
    css = f"""
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #2563EB; border-bottom: 3px solid #2563EB; padding-bottom: 10px; margin-bottom: 30px; }}
        h2 {{ color: #1e40af; margin-top: 30px; margin-bottom: 15px; padding-left: 10px; border-left: 4px solid #2563EB; }}
        h3 {{ color: #3b82f6; margin-top: 20px; margin-bottom: 10px; }}
        p {{ margin-bottom: 15px; }}
        ul, ol {{ margin-left: 20px; margin-bottom: 15px; }}
        li {{ margin-bottom: 8px; }}
        code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 3px; font-family: "Courier New", monospace; font-size: 0.9em; }}
        pre {{ background: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 5px; overflow-x: auto; margin-bottom: 20px; }}
        pre code {{ background: none; padding: 0; color: inherit; }}
        .info-box {{ background: #dbeafe; border-left: 4px solid #2563EB; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        .warning-box {{ background: #fef3c7; border-left: 4px solid #FBBF24; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        .success-box {{ background: #d1fae5; border-left: 4px solid #10b981; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        img {{ max-width: 100%; height: auto; border-radius: 5px; margin: 20px 0; }}
        .step {{ background: #f8fafc; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #2563EB; }}
        .step-number {{ display: inline-block; background: #2563EB; color: white; width: 30px; height: 30px; line-height: 30px; text-align: center; border-radius: 50%; margin-right: 10px; font-weight: bold; }}
        .prompt-box {{ background: #1e293b; color: #e2e8f0; padding: 20px; border-radius: 5px; margin: 20px 0; font-family: "Courier New", monospace; white-space: pre-wrap; border-left: 4px solid #2563EB; }}
        .flow-diagram {{ text-align: center; margin: 30px 0; padding: 20px; background: #fafafa; border-radius: 8px; }}
        {css_extra}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad: true}});</script>
    """
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {css}
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        {content}
    </div>
</body>
</html>"""


def save_html_file(html_content: str, output_path: Path, title: str = "Document"):
    """HTMLファイルを保存"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
    abs_path = output_path.resolve()
    file_url = f"file://{abs_path}"
    
    print("\n" + "=" * 60)
    print(f"HTMLファイルを生成しました")
    print("=" * 60)
    print(f"\nファイルパス（絶対パス）:")
    print(f"   {abs_path}")
    print(f"\nブラウザで開く:")
    print(f"   {file_url}")
    print(f"\nターミナルから開く（コピペでOK）:")
    print(f"   open \"{abs_path}\"")
    print("=" * 60 + "\n")

#!/usr/bin/env python3
"""
Article Writer - テーマからMarkdown記事を自動生成するCLIツール。

Gemini APIを使い、テーマ→アウトライン→セクション執筆→挿絵マーカー挿入の
ワークフローで一貫性のある記事を生成する。
文体プロファイル（YAML）によるトーン統一に対応。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from tools.credential_manager import inject_to_environ
    inject_to_environ()
except ImportError:
    try:
        from credential_manager import inject_to_environ
        inject_to_environ()
    except ImportError:
        pass
load_dotenv()



# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_FLASH_MODEL = "gemini-3-flash-preview"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "output"
DEFAULT_WORD_COUNT = 3000
DEFAULT_ILLUSTRATIONS = "auto"


# ---------------------------------------------------------------------------
# Gemini client helpers
# ---------------------------------------------------------------------------

def get_client():
    """Google GenAI クライアントを初期化して返す。"""
    try:
        from google import genai
    except ImportError:
        raise ImportError(
            "google-genai パッケージが必要です。"
            " `pip install google-genai` でインストールしてください。"
        ) from None
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def get_model() -> str:
    """テキスト生成用モデル名を取得。"""
    return os.environ.get("GEMINI_FLASH_MODEL", DEFAULT_FLASH_MODEL)


def call_gemini(client, prompt: str, model: str | None = None) -> str:
    """Gemini APIを呼び出してテキストレスポンスを返す。リトライ付き。"""
    from google.genai import types
    mdl = model or get_model()
    max_retries = 2
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=mdl,
                contents=[
                    {"role": "user", "parts": [{"text": prompt}]}
                ],
            )
            return response.text
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"[article-writer] API error (attempt {attempt + 1}): {e}, retrying...",
                      file=sys.stderr)
                continue

    raise RuntimeError(f"Gemini API呼び出しに失敗しました ({max_retries}回試行): {last_error}")


# ---------------------------------------------------------------------------
# Style profile
# ---------------------------------------------------------------------------

def load_style_profile(path: str) -> dict:
    """YAML形式のスタイルプロファイルを読み込む。"""
    p = Path(path)
    if not p.exists():
        print(f"[article-writer] Warning: style profile not found: {p}", file=sys.stderr)
        return {}
    with open(p, "r", encoding="utf-8") as f:
        profile = yaml.safe_load(f) or {}
    print(f"[article-writer] Style profile loaded: {p}")
    return profile


def style_instructions(profile: dict) -> str:
    """スタイルプロファイルからプロンプト用の指示文を生成する。"""
    if not profile:
        return ""

    lines = ["\n## 文体指示（以下に厳密に従うこと）"]

    mapping = {
        "tone": "トーン",
        "formality": "フォーマリティ",
        "sentence_ending": "語尾スタイル",
        "vocabulary_level": "語彙レベル",
        "paragraph_length": "段落の長さ",
        "target_audience": "対象読者",
        "brand_voice": "ブランドボイス",
    }

    for key, label in mapping.items():
        if key in profile:
            lines.append(f"- {label}: {profile[key]}")

    if profile.get("use_examples"):
        lines.append("- 具体例を積極的に使用する")
    if profile.get("use_metaphors"):
        lines.append("- 比喩表現を活用する")
    elif profile.get("use_metaphors") is False:
        lines.append("- 比喩表現は使わない")

    if profile.get("avoid_words"):
        words = ", ".join(profile["avoid_words"])
        lines.append(f"- 以下の語は使用禁止: {words}")

    if profile.get("preferred_expressions"):
        words = ", ".join(profile["preferred_expressions"])
        lines.append(f"- 優先的に使う表現: {words}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Outline generation
# ---------------------------------------------------------------------------

def generate_outline(client, theme: str, sections: str, word_count: int,
                     audience: str, profile: dict) -> dict:
    """テーマからアウトラインをJSON形式で生成する。"""
    section_instruction = (
        f"セクション数は {sections} 個にしてください。"
        if sections != "auto"
        else "セクション数はテーマの性質に応じて4〜8個で自動決定してください。"
    )

    audience_instruction = (
        f"\n想定読者: {audience}" if audience else ""
    )

    prompt = f"""あなたはプロのライター・編集者です。
以下のテーマについて記事のアウトラインをJSON形式で生成してください。

## テーマ
{theme}

## 条件
- 目標文字数: 約{word_count}文字
- {section_instruction}{audience_instruction}
{style_instructions(profile)}

## 出力形式（JSONのみ、他のテキスト不要）

```json
{{
  "title": "記事タイトル",
  "lead": "リード文（2〜3文の導入・要約）",
  "sections": [
    {{
      "heading": "セクション見出し（H2）",
      "key_points": ["ポイント1", "ポイント2", "ポイント3"],
      "subsections": [
        {{
          "heading": "サブセクション見出し（H3）（任意）",
          "key_points": ["ポイント"]
        }}
      ],
      "illustration_hint": "このセクションに適した図表や画像の説明（不要ならnull）"
    }}
  ],
  "conclusion_points": ["まとめポイント1", "まとめポイント2"]
}}
```

## ルール
1. タイトルは読者の興味を引く具体的なものにする
2. セクション構成は論理的な流れを持たせる
3. key_points は各セクションで3〜5個
4. illustration_hint は具体的に記述する（「フロー図: ...」「写真: ...」など）
5. JSONブロック以外のテキストは出力しない
"""

    text = call_gemini(client, prompt)
    return _parse_json_response(text)


def _parse_json_response(text: str) -> dict:
    """Geminiのレスポンスからjsonブロックを抽出してパースする。"""
    # Try to extract json code block
    match = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        json_text = match.group(1)
    else:
        json_text = text.strip()

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as err:
        # Attempt to find JSON-like structure
        match2 = re.search(r"\{.*\}", text, re.DOTALL)
        if match2:
            return json.loads(match2.group(0))
        raise ValueError(f"JSONパースに失敗しました。レスポンス:\n{text[:500]}") from err


# ---------------------------------------------------------------------------
# Section drafting
# ---------------------------------------------------------------------------

def draft_section(client, theme: str, section: dict, word_target: int,
                  profile: dict, audience: str) -> str:
    """アウトラインの1セクションを執筆する。"""
    key_points_str = "\n".join(f"  - {p}" for p in section.get("key_points", []))

    subsections_str = ""
    if section.get("subsections"):
        for sub in section["subsections"]:
            sub_points = "\n".join(f"    - {p}" for p in sub.get("key_points", []))
            subsections_str += f"\n### {sub['heading']}\nキーポイント:\n{sub_points}\n"

    audience_line = f"\n想定読者: {audience}" if audience else ""

    prompt = f"""あなたはプロのライターです。以下の指示に従って記事の1セクションを執筆してください。

## 記事テーマ
{theme}

## 執筆するセクション
見出し: {section['heading']}
キーポイント:
{key_points_str}
{subsections_str}

## 条件
- このセクションの目標文字数: 約{word_target}文字
- Markdown形式で出力{audience_line}
- セクション見出し（## ）から書き始める
- 具体例や説明を含め、読みやすい文章にする
- サブセクションがある場合は ### で見出しを付ける
{style_instructions(profile)}

## 出力
Markdownテキストのみ（余計な説明不要）
"""

    return call_gemini(client, prompt)


# ---------------------------------------------------------------------------
# Illustration markers
# ---------------------------------------------------------------------------

def insert_illustration_markers(section_text: str, hint: str | None,
                                mode: str) -> str:
    """セクションテキストに挿絵マーカーを挿入する。"""
    if mode == "none" or not hint:
        return section_text

    # Determine illustration type from hint
    ill_type = "image"
    hint_lower = hint.lower() if hint else ""
    if any(w in hint_lower for w in ["フロー", "図", "diagram", "構成", "アーキテクチャ",
                                      "シーケンス", "uml", "プロセス"]):
        ill_type = "diagram"
    elif any(w in hint_lower for w in ["グラフ", "chart", "データ", "推移", "比較"]):
        ill_type = "chart"
    elif any(w in hint_lower for w in ["スクリーンショット", "screenshot", "画面", "UI"]):
        ill_type = "screenshot"

    marker = f'\n\n<!-- illustration: type={ill_type} description="{hint}" -->\n'

    if mode == "manual":
        # manual mode: marker at end of section
        return section_text.rstrip() + marker
    else:
        # auto mode: try to insert after first paragraph break
        paragraphs = section_text.split("\n\n")
        if len(paragraphs) >= 3:
            # Insert after the second paragraph
            insert_idx = 2
            paragraphs.insert(insert_idx, marker.strip())
            return "\n\n".join(paragraphs)
        else:
            return section_text.rstrip() + marker


# ---------------------------------------------------------------------------
# Article assembly
# ---------------------------------------------------------------------------

def build_toc(outline: dict) -> str:
    """アウトラインから目次を生成する。"""
    lines = ["## 目次\n"]
    for section in outline.get("sections", []):
        heading = section["heading"]
        anchor = heading.lower().replace(" ", "-")
        # Simple anchor: remove special chars
        anchor = re.sub(r"[^a-z0-9\u3040-\u9fff\-]", "", anchor)
        lines.append(f"- [{heading}](#{anchor})")
    lines.append("- [まとめ](#まとめ)")
    return "\n".join(lines)


def assemble_article(outline: dict, section_texts: list[str]) -> str:
    """アウトラインとセクションテキストを組み合わせて最終記事を生成する。"""
    parts = []

    # Title
    parts.append(f"# {outline['title']}\n")

    # Lead
    if outline.get("lead"):
        parts.append(f"> {outline['lead']}\n")

    # TOC
    parts.append(build_toc(outline))
    parts.append("")

    # Sections
    for text in section_texts:
        cleaned = text.strip()
        # Remove any stray code fences that Gemini might have added
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:markdown)?\s*\n", "", cleaned)
            cleaned = re.sub(r"\n```\s*$", "", cleaned)
        parts.append(cleaned)
        parts.append("")

    # Conclusion
    if outline.get("conclusion_points"):
        parts.append("## まとめ\n")
        for point in outline["conclusion_points"]:
            parts.append(f"- {point}")
        parts.append("")

    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Test mode
# ---------------------------------------------------------------------------

SAMPLE_ARTICLE = """# AIエージェントの活用法 - ビジネスを変える5つのアプローチ

> AIエージェントは単なるチャットボットではありません。業務プロセスを自律的に遂行し、人間の生産性を飛躍的に向上させるパートナーです。本記事では、ビジネスシーンで即実践できる5つの活用法を解説します。

## 目次

- [AIエージェントとは](#aiエージェントとは)
- [活用法1: ドキュメント作成の自動化](#活用法1-ドキュメント作成の自動化)
- [活用法2: データ分析の効率化](#活用法2-データ分析の効率化)
- [まとめ](#まとめ)

## AIエージェントとは

AIエージェントとは、大規模言語モデル（LLM）を核として、ツール操作やファイル処理を自律的に行うシステムです。従来のAIアシスタントが「質問に答える」だけだったのに対し、AIエージェントは「タスクを完遂する」ことができます。

具体的には、以下のような特徴があります。

- **自律的な判断**: 与えられた目標に向けて、必要なステップを自分で計画・実行する
- **ツール連携**: ファイル操作、Web検索、API呼び出しなどの外部ツールを活用する
- **反復改善**: 実行結果を評価し、必要に応じてアプローチを修正する

<!-- illustration: type=diagram description="フロー図: AIエージェントの処理ループ（目標設定→計画→実行→評価→改善）" -->

## 活用法1: ドキュメント作成の自動化

ビジネスにおけるドキュメント作成は多大な時間を消費します。AIエージェントを活用すれば、会議メモからの議事録作成、報告書のドラフト生成、プレゼン資料の構成案作成を自動化できます。

例えば、Claude Codeを使った場合、「先週の営業会議の議事録から、今月の売上レポートを作成して」と指示するだけで、データの収集からフォーマットの整形まで一気通貫で処理されます。

<!-- illustration: type=image description="デスクでAIエージェントにドキュメント作成を指示するビジネスパーソン" -->

## 活用法2: データ分析の効率化

データ分析においても、AIエージェントは強力なパートナーになります。CSVファイルの読み込みからグラフの作成、異常値の検出、レポートの出力まで、一連の分析フローを自動で実行します。

BigQueryやスプレッドシートのデータに接続し、自然言語で「先月と今月の売上を比較して、トレンドをグラフで可視化して」と指示するだけで、適切な分析コードを生成・実行します。

<!-- illustration: type=chart description="棒グラフ: 月別売上推移とAIエージェント導入前後の分析時間比較" -->

## まとめ

- AIエージェントは「質問応答」を超え、「タスク完遂」ができる次世代ツールである
- ドキュメント作成、データ分析など、日常業務の多くの場面で活用できる
- 小さなタスクから始めて、段階的に活用範囲を広げることが成功のカギ
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Article Writer - テーマからMarkdown記事を自動生成"
    )
    parser.add_argument("--theme", type=str, help="記事のテーマ・トピック")
    parser.add_argument("--style", type=str, default=None,
                        help="文体プロファイルYAMLファイルのパス")
    parser.add_argument("--audience", type=str, default=None,
                        help="想定読者（例: '非エンジニアのビジネスパーソン'）")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="出力ファイルパス")
    parser.add_argument("--word-count", type=int, default=DEFAULT_WORD_COUNT,
                        help=f"目標文字数（デフォルト: {DEFAULT_WORD_COUNT}）")
    parser.add_argument("--sections", type=str, default="auto",
                        help="セクション数（デフォルト: auto）")
    parser.add_argument("--illustrations", type=str, default=DEFAULT_ILLUSTRATIONS,
                        choices=["auto", "manual", "none"],
                        help="挿絵マーカー: auto/manual/none")
    parser.add_argument("--test", action="store_true",
                        help="テストモード（API呼び出しなしでサンプル出力）")
    args = parser.parse_args()

    # --- Test mode ---
    if args.test:
        output_path = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR / "article_test.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(SAMPLE_ARTICLE.strip() + "\n", encoding="utf-8")
        print(f"[article-writer] Test article generated: {output_path.resolve()}")
        return

    # --- Validate args ---
    if not args.theme:
        parser.error("--theme is required (or use --test for test mode)")

    # --- Init client ---
    client = get_client()
    if client is None:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY が未設定です。", file=sys.stderr)
        print("  export GEMINI_API_KEY='your-key' を実行してください。", file=sys.stderr)
        sys.exit(1)

    # --- Load style profile ---
    profile = {}
    if args.style:
        profile = load_style_profile(args.style)

    # --- Step 1: Generate outline ---
    print(f"[article-writer] テーマ: {args.theme}")
    print(f"[article-writer] 目標文字数: {args.word_count}")
    print("[article-writer] Step 1/4: アウトライン生成中...")

    outline = generate_outline(
        client, args.theme, args.sections, args.word_count,
        args.audience or "", profile
    )

    num_sections = len(outline.get("sections", []))
    print(f"[article-writer] アウトライン完成: {outline.get('title', 'Untitled')} "
          f"({num_sections}セクション)")

    # --- Step 2: Draft each section ---
    print("[article-writer] Step 2/4: セクション執筆中...")
    section_texts = []
    words_per_section = max(200, args.word_count // max(num_sections, 1))

    for i, section in enumerate(outline.get("sections", []), 1):
        print(f"  [{i}/{num_sections}] {section['heading']}...")
        text = draft_section(
            client, args.theme, section, words_per_section,
            profile, args.audience or ""
        )
        section_texts.append(text)

    # --- Step 3: Insert illustration markers ---
    print("[article-writer] Step 3/4: 挿絵マーカー挿入中...")
    for i, section in enumerate(outline.get("sections", [])):
        hint = section.get("illustration_hint")
        section_texts[i] = insert_illustration_markers(
            section_texts[i], hint, args.illustrations
        )

    # --- Step 4: Assemble ---
    print("[article-writer] Step 4/4: 記事組み立て中...")
    article = assemble_article(outline, section_texts)

    # --- Write output ---
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = DEFAULT_OUTPUT_DIR / f"article_{timestamp}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(article.strip() + "\n", encoding="utf-8")

    # --- Summary ---
    char_count = len(article)
    print("\n[article-writer] 記事生成完了!")
    print(f"  タイトル: {outline.get('title', 'Untitled')}")
    print(f"  セクション数: {num_sections}")
    print(f"  文字数: {char_count}")
    print(f"  出力先: {output_path.resolve()}")


if __name__ == "__main__":
    main()

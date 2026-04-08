#!/usr/bin/env python3
"""
Proofreading Agent - 日本語記事校閲エージェント

日本語記事を体系的に校閲し、インライン注釈付きのレビュー結果を出力する。
Five Sweeps（正確性・文法・一貫性・読みやすさ・構成）で多角的にレビュー。
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
load_dotenv(ROOT_DIR / ".env")


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SWEEP_NAMES = {
    "accuracy": "正確性チェック",
    "grammar": "文法チェック",
    "consistency": "一貫性チェック",
    "readability": "読みやすさチェック",
    "structure": "構成チェック",
}

ALL_SWEEPS = list(SWEEP_NAMES.keys())

SEVERITY_LEVELS = {"low": 1, "medium": 2, "high": 3}

DEFAULT_OUTPUT_DIR = ROOT_DIR / "output" / "reviews"

DEFAULT_MODEL = "gemini-3-flash-preview"

SAMPLE_TEXT = """\
# AIエージェントの活用方法

## はじめに

近年、AI技術の発展に伴い、AIエージェントを業務に活用する企業が増加してます。
本記事では、AIエージェントの基本的な概念から、実践的な活用方法までを解説します。

## AIエージェントとは

AIエージェントは、人工知能を搭載したソフトウエアであり、ユーザーの指示に基づいて
自律的にタスクを実行することができるシステムです。従来のチャットボットと異なり、
AIエージェントは複数のツールを使用して、複雑なタスクをこなす事ができます。

主な特徴としては以下の通りです：

1. 自律的な意思決定が可能
2. 複数のツールやAPIとの連携
3. コンテキストを理解した対話
4. タスクの計画と実行

## 活用シーン

AIエージェントは様々な場面で活用する事ができます。例えば、カスタマーサポートでは
顧客からの問い合わせに対して、適切な回答を自動的に生成することができます。
また、データ分析の分野においても、大量のデーターを処理し、レポートを
自動作成するといった使い方が可能です。

マーケティングの領域では、SNS投稿の作成やキャンペーンの企画立案を
サポートすることができます。さらに、開発の現場でも、コードレビューやテスト
自動化などの用途で活用されています。

## 導入に際しての注意点

AIエージェントを導入するにあたっては、いくつかの注意点があります。
まず、セキュリティーの観点から、機密情報の取り扱いには十分注意する必要があります。
また、AIの判断が常に正しいとは限らないため、重要な意思決定においては
人間によるレビューを挟むことが推奨されます。

コストの面でも、API利用料金が発生するため、利用頻度と効果を見極めた上で
導入を進めることが大事です。

## まとめ

AIエージェントは、適切に活用すれば業務効率を大幅に向上させることが可能です。
ただし、導入にあたっては、セキュリティやコストの面を十分に検討した上で、
段階的に進めていく事が重要です。
"""

# ---------------------------------------------------------------------------
# Sweep Prompts
# ---------------------------------------------------------------------------


def _build_accuracy_prompt() -> str:
    return """あなたは日本語校閲の専門家です。以下の日本語記事の「正確性」をチェックしてください。

## チェック項目
- 誤字脱字（漢字の変換ミス、タイプミス）
- 送り仮名の誤り（例：「行なう」→「行う」）
- 同音異義語の誤用（例：「以外」と「意外」）
- 固有名詞の表記ミス

## 出力形式（JSON配列）
各問題を以下の形式で出力してください。問題がない場合は空配列 [] を返してください。

```json
[
  {
    "line": 行番号（1始まり）,
    "original": "問題のある原文テキスト",
    "suggestion": "修正後のテキスト",
    "reason": "修正理由の簡潔な説明",
    "severity": "high/medium/low"
  }
]
```

重要：JSON配列のみを出力してください。説明文や前置きは不要です。"""


def _build_grammar_prompt() -> str:
    return """あなたは日本語校閲の専門家です。以下の日本語記事の「文法」をチェックしてください。

## チェック項目
- 主述のねじれ（主語と述語の不一致）
- 助詞の誤用（「は」と「が」、「に」と「へ」の使い分け）
- 敬語の統一（尊敬語・謙譲語・丁寧語の混在）
- 係り受けの誤り（修飾語と被修飾語の関係）
- 時制の不一致（過去形と現在形の混在）

## 出力形式（JSON配列）
各問題を以下の形式で出力してください。問題がない場合は空配列 [] を返してください。

```json
[
  {
    "line": 行番号（1始まり）,
    "original": "問題のある原文テキスト",
    "suggestion": "修正後のテキスト",
    "reason": "修正理由の簡潔な説明",
    "severity": "high/medium/low"
  }
]
```

重要：JSON配列のみを出力してください。説明文や前置きは不要です。"""


def _build_consistency_prompt(style_config: Optional[Dict] = None) -> str:
    style_rules = ""
    if style_config:
        if "tone" in style_config:
            style_rules += f"\n- 文体: 「{style_config['tone']}」調で統一されているか確認"
        if "terminology" in style_config:
            preferred = style_config["terminology"].get("preferred", [])
            if preferred:
                rules = []
                for entry in preferred:
                    rejects = "、".join(entry.get("reject", []))
                    rules.append(f"  - 「{entry['term']}」を使用（「{rejects}」は不可）")
                style_rules += "\n- 用語統一ルール:\n" + "\n".join(rules)
        if "rules" in style_config:
            rules = style_config["rules"]
            if "punctuation" in rules:
                style_rules += f"\n- 句読点: 「{rules['punctuation']}」を使用"
            if "number_style" in rules:
                style_rules += f"\n- 数字表記: {rules['number_style']}を使用"

    extra = f"\n## 追加スタイルルール\n{style_rules}" if style_rules else ""

    return f"""あなたは日本語校閲の専門家です。以下の日本語記事の「一貫性」をチェックしてください。

## チェック項目
- 表記揺れ（例：「サーバー」と「サーバ」、「ユーザー」と「ユーザ」）
- 語尾の統一（「です・ます」調と「だ・である」調の混在）
- 数字表記（全角と半角の混在、「3つ」と「三つ」）
- 記号の統一（括弧の種類、句読点）
- 略語の統一（初出でのフルスペル表記）
{extra}

## 出力形式（JSON配列）
各問題を以下の形式で出力してください。問題がない場合は空配列 [] を返してください。

```json
[
  {{
    "line": 行番号（1始まり）,
    "original": "問題のある原文テキスト",
    "suggestion": "修正後のテキスト",
    "reason": "修正理由の簡潔な説明",
    "severity": "high/medium/low"
  }}
]
```

重要：JSON配列のみを出力してください。説明文や前置きは不要です。"""


def _build_readability_prompt(max_sentence_length: int = 80) -> str:
    return f"""あなたは日本語校閲の専門家です。以下の日本語記事の「読みやすさ」をチェックしてください。

## チェック項目
- 一文が{max_sentence_length}文字を超える箇所
- 難読漢字（一般読者に難しい漢字の使用）
- 冗長表現（例：「することができる」→「できる」）
- 二重否定（例：「ないわけではない」→「ある」）
- 受身形の多用（能動態への書き換え提案）
- カタカナ語の乱用（日本語で十分伝わる箇所）

## 出力形式（JSON配列）
各問題を以下の形式で出力してください。問題がない場合は空配列 [] を返してください。

```json
[
  {{
    "line": 行番号（1始まり）,
    "original": "問題のある原文テキスト",
    "suggestion": "修正後のテキスト",
    "reason": "修正理由の簡潔な説明",
    "severity": "high/medium/low"
  }}
]
```

重要：JSON配列のみを出力してください。説明文や前置きは不要です。"""


def _build_structure_prompt() -> str:
    return """あなたは日本語校閲の専門家です。以下の日本語記事の「構成」をチェックしてください。

## チェック項目
- 段落の論理的つながり（前後の段落間の接続）
- 重複内容（同じ情報の不要な繰り返し）
- 情報の過不足（説明不足の箇所、不要な情報）
- 見出しの階層（見出しレベルの適切さ）
- 導入と結論の整合性（冒頭の問題提起と結論の対応）

## 出力形式（JSON配列）
各問題を以下の形式で出力してください。問題がない場合は空配列 [] を返してください。

```json
[
  {
    "line": 行番号（1始まり、段落や見出しの先頭行）,
    "original": "問題のある箇所（段落冒頭や見出し等）",
    "suggestion": "改善案の説明",
    "reason": "修正理由の簡潔な説明",
    "severity": "high/medium/low"
  }
]
```

重要：JSON配列のみを出力してください。説明文や前置きは不要です。"""


# ---------------------------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------------------------


def get_client():
    """Google GenAI クライアントを初期化して返す."""
    try:
        from google import genai
    except ImportError:
        print("Error: google-genai パッケージが必要です。")
        print("  pip install google-genai")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY が必要です。")
        print("  export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def get_model() -> str:
    """テキスト処理用モデル名を取得."""
    return os.environ.get("GEMINI_FLASH_MODEL", DEFAULT_MODEL)


# ---------------------------------------------------------------------------
# Core Functions
# ---------------------------------------------------------------------------


def load_article(path: Path) -> str:
    """記事ファイルを読み込む."""
    if not path.exists():
        print(f"Error: ファイルが見つかりません: {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def load_style_profile(path: Path) -> Optional[Dict]:
    """スタイルプロファイルを読み込む."""
    if not path.exists():
        print(f"Warning: スタイルプロファイルが見つかりません: {path}")
        return None
    try:
        import yaml
    except ImportError:
        print("Warning: pyyaml パッケージが必要です。スタイルプロファイルをスキップします。")
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def call_gemini(client, model: str, system_prompt: str, article: str) -> List[Dict]:
    """Gemini API を呼び出して校閲結果を取得する."""
    from google.genai import types

    numbered_lines = []
    for i, line in enumerate(article.split("\n"), 1):
        numbered_lines.append(f"L{i}: {line}")
    numbered_article = "\n".join(numbered_lines)

    user_prompt = f"以下の記事を校閲してください:\n\n{numbered_article}"

    try:
        response = client.models.generate_content(
            model=model,
            contents=[user_prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
            ),
        )
    except Exception as e:
        print(f"  API Error: {e}")
        return []

    text = response.text.strip()

    # Extract JSON from response (handle markdown code blocks)
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if json_match:
        text = json_match.group(1).strip()

    # Try to parse JSON
    try:
        issues = json.loads(text)
        if isinstance(issues, list):
            return issues
    except json.JSONDecodeError:
        # Try to find JSON array in text
        array_match = re.search(r"\[.*\]", text, re.DOTALL)
        if array_match:
            try:
                issues = json.loads(array_match.group(0))
                if isinstance(issues, list):
                    return issues
            except json.JSONDecodeError:
                pass
        print("  Warning: JSON解析に失敗しました。レスポンスをスキップします。")
    return []


def run_sweep(
    client, model: str, sweep: str, article: str,
    style_config: Optional[Dict] = None,
) -> List[Dict]:
    """指定されたスイープを実行し、問題リストを返す."""
    print(f"  [{SWEEP_NAMES[sweep]}] 実行中...")

    if sweep == "accuracy":
        prompt = _build_accuracy_prompt()
    elif sweep == "grammar":
        prompt = _build_grammar_prompt()
    elif sweep == "consistency":
        prompt = _build_consistency_prompt(style_config)
    elif sweep == "readability":
        max_len = 80
        if style_config and "rules" in style_config:
            max_len = style_config["rules"].get("max_sentence_length", 80)
        prompt = _build_readability_prompt(max_len)
    elif sweep == "structure":
        prompt = _build_structure_prompt()
    else:
        print(f"  Unknown sweep: {sweep}")
        return []

    issues = call_gemini(client, model, prompt, article)

    # Tag each issue with its sweep category
    for issue in issues:
        issue["category"] = sweep

    count = len(issues)
    print(f"  [{SWEEP_NAMES[sweep]}] {count} 件検出")
    return issues


# ---------------------------------------------------------------------------
# Readability Score
# ---------------------------------------------------------------------------


def compute_readability_score(article: str, issues: List[Dict]) -> Dict[str, Any]:
    """読みやすさスコアを算出する."""
    lines = article.split("\n")
    # Filter out empty lines, headings, and code blocks for sentence analysis
    text_lines = []
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped and not stripped.startswith("#"):
            text_lines.append(stripped)

    full_text = "".join(text_lines)

    # Split into sentences (approximate)
    sentences = re.split(r"[。！？\n]", full_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 1. Average sentence length (30 points)
    avg_len = sum(len(s) for s in sentences) / max(len(sentences), 1)
    if avg_len <= 40:
        length_score = 30
    elif avg_len <= 60:
        length_score = 20
    elif avg_len <= 80:
        length_score = 10
    else:
        length_score = 0

    # 2. Kanji ratio (20 points)
    total_chars = len(full_text)
    kanji_count = sum(
        1 for ch in full_text
        if unicodedata.name(ch, "").startswith("CJK UNIFIED")
    )
    kanji_ratio = kanji_count / max(total_chars, 1)
    if 0.20 <= kanji_ratio <= 0.35:
        kanji_score = 20
    elif 0.35 < kanji_ratio <= 0.45:
        kanji_score = 15
    else:
        kanji_score = 10

    # 3. Verbose expression ratio (20 points)
    readability_issues = [
        i for i in issues if i.get("category") == "readability"
    ]
    verbose_count = len(readability_issues)
    verbose_ratio = verbose_count / max(len(sentences), 1)
    verbose_score = max(0, int(20 * (1 - verbose_ratio * 5)))

    # 4. Paragraph appropriateness (15 points)
    paragraphs = re.split(r"\n\s*\n", article)
    paragraphs = [p for p in paragraphs if p.strip() and not p.strip().startswith("#")]
    if paragraphs:
        avg_sents_per_para = len(sentences) / max(len(paragraphs), 1)
        if 3 <= avg_sents_per_para <= 5:
            para_score = 15
        elif 2 <= avg_sents_per_para <= 7:
            para_score = 10
        else:
            para_score = 5
    else:
        para_score = 10

    # 5. Connector appropriateness (15 points)
    connectors = [
        "また", "さらに", "しかし", "一方", "そのため", "したがって",
        "例えば", "つまり", "なお", "ただし", "そして", "このように",
    ]
    connector_count = sum(full_text.count(c) for c in connectors)
    connector_ratio = connector_count / max(len(paragraphs), 1)
    if 0.5 <= connector_ratio <= 2.0:
        connector_score = 15
    elif connector_ratio > 0:
        connector_score = 10
    else:
        connector_score = 5

    total_score = length_score + kanji_score + verbose_score + para_score + connector_score

    return {
        "total": min(100, total_score),
        "avg_sentence_length": round(avg_len, 1),
        "kanji_ratio": round(kanji_ratio * 100, 1),
        "verbose_expressions": verbose_count,
        "details": {
            "length_score": length_score,
            "kanji_score": kanji_score,
            "verbose_score": verbose_score,
            "paragraph_score": para_score,
            "connector_score": connector_score,
        },
    }


# ---------------------------------------------------------------------------
# Annotated Output
# ---------------------------------------------------------------------------


def generate_annotated_article(article: str, issues: List[Dict]) -> str:
    """原文にインライン注釈を挿入した記事を生成する."""
    lines = article.split("\n")

    # Group issues by line number
    issues_by_line: Dict[int, List[Dict]] = {}
    for issue in issues:
        line_num = issue.get("line", 0)
        if line_num not in issues_by_line:
            issues_by_line[line_num] = []
        issues_by_line[line_num].append(issue)

    annotated_lines = []
    for i, line in enumerate(lines, 1):
        if i in issues_by_line:
            annotated_line = line
            for issue in issues_by_line[i]:
                original = issue.get("original", "")
                suggestion = issue.get("suggestion", "")
                reason = issue.get("reason", "")
                severity = issue.get("severity", "medium").upper()
                category = SWEEP_NAMES.get(issue.get("category", ""), "")

                annotation = (
                    f"[校閲({severity}): "
                    f"「{original}」→「{suggestion}」"
                    f"（理由: {reason}）"
                    f"【{category}】]"
                )

                # Try to insert annotation after the original text
                if original and original in annotated_line:
                    annotated_line = annotated_line.replace(
                        original,
                        f"{original}{annotation}",
                        1,
                    )
                else:
                    # Append annotation at end of line
                    annotated_line = f"{annotated_line}  {annotation}"

            annotated_lines.append(annotated_line)
        else:
            annotated_lines.append(line)

    return "\n".join(annotated_lines)


def generate_summary(
    issues: List[Dict],
    readability: Dict[str, Any],
    severity_threshold: int,
) -> str:
    """校閲サマリーレポートを生成する."""
    sections = []
    sections.append("\n---\n## 校閲サマリー\n")

    # Issue counts by category
    category_counts: Dict[str, int] = {}
    for sweep in ALL_SWEEPS:
        category_counts[sweep] = 0
    for issue in issues:
        cat = issue.get("category", "unknown")
        if cat in category_counts:
            category_counts[cat] += 1

    total = sum(category_counts.values())

    sections.append("### 検出件数\n")
    sections.append("| カテゴリ | 件数 |")
    sections.append("|---------|------|")
    for sweep in ALL_SWEEPS:
        sections.append(f"| {SWEEP_NAMES[sweep]} | {category_counts[sweep]} |")
    sections.append(f"| **合計** | **{total}** |")
    sections.append("")

    # Readability score
    sections.append(f"### 読みやすさスコア: {readability['total']}/100\n")
    sections.append(f"- 平均文長: {readability['avg_sentence_length']}文字")
    sections.append(f"- 漢字含有率: {readability['kanji_ratio']}%")
    sections.append(f"- 冗長表現: {readability['verbose_expressions']}箇所")
    sections.append("")

    # Severity breakdown
    severity_counts = {"high": 0, "medium": 0, "low": 0}
    for issue in issues:
        sev = issue.get("severity", "medium").lower()
        if sev in severity_counts:
            severity_counts[sev] += 1

    sections.append("### 重要度別\n")
    sections.append("| 重要度 | 件数 |")
    sections.append("|--------|------|")
    for sev in ["high", "medium", "low"]:
        sections.append(f"| {sev.upper()} | {severity_counts[sev]} |")
    sections.append("")

    # Top 5 critical fixes
    filtered = [
        i for i in issues
        if SEVERITY_LEVELS.get(i.get("severity", "medium").lower(), 2) >= severity_threshold
    ]
    sorted_issues = sorted(
        filtered,
        key=lambda x: SEVERITY_LEVELS.get(x.get("severity", "medium").lower(), 2),
        reverse=True,
    )
    top5 = sorted_issues[:5]

    if top5:
        sections.append("### 最重要修正 Top 5\n")
        for idx, issue in enumerate(top5, 1):
            sev = issue.get("severity", "medium").upper()
            line = issue.get("line", "?")
            original = issue.get("original", "")
            suggestion = issue.get("suggestion", "")
            reason = issue.get("reason", "")
            if original and suggestion:
                sections.append(
                    f"{idx}. [{sev}] L{line}: 「{original}」→「{suggestion}」（{reason}）"
                )
            else:
                sections.append(f"{idx}. [{sev}] L{line}: {reason}")
        sections.append("")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Test Mode
# ---------------------------------------------------------------------------


def run_test_mode() -> str:
    """テストモード: API を使わずサンプルテキストで校閲結果を生成する."""
    print("=== テストモード（API不要）===\n")
    print("サンプルテキストを使用して校閲結果を生成します。\n")

    article = SAMPLE_TEXT

    # Simulated issues for demonstration
    test_issues = [
        {
            "line": 5,
            "original": "増加してます",
            "suggestion": "増加しています",
            "reason": "「い」の脱落（脱字）",
            "severity": "high",
            "category": "accuracy",
        },
        {
            "line": 10,
            "original": "ソフトウエア",
            "suggestion": "ソフトウェア",
            "reason": "一般的な表記は「ソフトウェア」",
            "severity": "medium",
            "category": "accuracy",
        },
        {
            "line": 11,
            "original": "実行することができるシステム",
            "suggestion": "実行できるシステム",
            "reason": "冗長表現「することができる」→「できる」",
            "severity": "medium",
            "category": "readability",
        },
        {
            "line": 13,
            "original": "こなす事ができます",
            "suggestion": "こなすことができます",
            "reason": "「事」→「こと」（形式名詞はひらがな表記が一般的）",
            "severity": "medium",
            "category": "accuracy",
        },
        {
            "line": 20,
            "original": "活用する事ができます",
            "suggestion": "活用できます",
            "reason": "冗長表現＋「事」→「こと」",
            "severity": "medium",
            "category": "readability",
        },
        {
            "line": 21,
            "original": "生成することができます",
            "suggestion": "生成できます",
            "reason": "冗長表現「することができる」→「できる」",
            "severity": "low",
            "category": "readability",
        },
        {
            "line": 23,
            "original": "データー",
            "suggestion": "データ",
            "reason": "表記揺れ。一般的には「データ」を使用",
            "severity": "medium",
            "category": "consistency",
        },
        {
            "line": 32,
            "original": "セキュリティー",
            "suggestion": "セキュリティ",
            "reason": "長音符の統一。JIS規格では3音以上の語は長音を省略",
            "severity": "low",
            "category": "consistency",
        },
        {
            "line": 37,
            "original": "大事です",
            "suggestion": "重要です",
            "reason": "文体の統一。記事全体で「重要」を使用しており「大事」は口語的",
            "severity": "low",
            "category": "consistency",
        },
        {
            "line": 40,
            "original": "進めていく事が重要です",
            "suggestion": "進めていくことが重要です",
            "reason": "「事」→「こと」（形式名詞はひらがな表記が一般的）",
            "severity": "medium",
            "category": "accuracy",
        },
        {
            "line": 20,
            "original": "AIエージェントは様々な場面で活用する事ができます。例えば、カスタマーサポートでは顧客からの問い合わせに対して、適切な回答を自動的に生成することができます。",
            "suggestion": "文を分割するか、80文字以内に収める",
            "reason": "一文が80文字を超えている（約90文字）",
            "severity": "low",
            "category": "readability",
        },
        {
            "line": 5,
            "original": "AIエージェントの基本的な概念から、実践的な活用方法までを解説します。",
            "suggestion": "（構成に対応する結論あり）",
            "reason": "導入の問題提起とまとめの結論が適切に対応している（良い点）",
            "severity": "low",
            "category": "structure",
        },
    ]

    readability = compute_readability_score(article, test_issues)
    annotated = generate_annotated_article(article, test_issues)
    summary = generate_summary(
        test_issues,
        readability,
        severity_threshold=SEVERITY_LEVELS["low"],
    )

    output = f"# 校閲結果（テストモード）\n\n{annotated}\n{summary}"

    # Write to file
    output_dir = DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"review_test_{timestamp}.md"
    output_path.write_text(output, encoding="utf-8")
    print(f"\n出力ファイル: {output_path}")
    print(f"検出件数: {len(test_issues)} 件")
    print(f"読みやすさスコア: {readability['total']}/100")

    return str(output_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Proofreading Agent - 日本語記事校閲エージェント",
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        help="校閲対象のファイルパス（Markdown/テキスト）",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="校閲結果の出力先（デフォルト: output/reviews/review_{timestamp}.md）",
    )
    parser.add_argument(
        "--sweep", "-s",
        type=str,
        default="all",
        choices=["all"] + ALL_SWEEPS,
        help="実行するスイープ（デフォルト: all）",
    )
    parser.add_argument(
        "--style",
        type=str,
        default=None,
        help="スタイルプロファイル（YAML）のパス",
    )
    parser.add_argument(
        "--severity",
        type=str,
        default="medium",
        choices=["low", "medium", "high"],
        help="表示する最低重要度（デフォルト: medium）",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="テストモード（サンプルテキストで API 不要の動作確認）",
    )

    args = parser.parse_args()

    # Test mode
    if args.test:
        run_test_mode()
        return

    # Validate input
    if not args.input:
        print("Error: --input オプションでファイルを指定してください（または --test でテスト実行）")
        sys.exit(1)

    input_path = Path(args.input).resolve()
    article = load_article(input_path)

    # Load style profile
    style_config = None
    if args.style:
        style_config = load_style_profile(Path(args.style).resolve())

    # Determine output path
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = DEFAULT_OUTPUT_DIR / f"review_{timestamp}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine sweeps to run
    if args.sweep == "all":
        sweeps = ALL_SWEEPS
    else:
        sweeps = [args.sweep]

    severity_threshold = SEVERITY_LEVELS[args.severity]

    # Initialize client
    client = get_client()
    model = get_model()

    print(f"校閲対象: {input_path}")
    print(f"モデル: {model}")
    print(f"スイープ: {', '.join(SWEEP_NAMES[s] for s in sweeps)}")
    print(f"重要度フィルタ: {args.severity} 以上")
    if style_config:
        print(f"スタイル: {style_config.get('name', 'カスタム')}")
    print()

    # Run sweeps
    all_issues: List[Dict] = []
    for sweep in sweeps:
        issues = run_sweep(client, model, sweep, article, style_config)
        all_issues.extend(issues)

    # Filter by severity
    filtered_issues = [
        i for i in all_issues
        if SEVERITY_LEVELS.get(i.get("severity", "medium").lower(), 2) >= severity_threshold
    ]

    # Compute readability score
    readability = compute_readability_score(article, all_issues)

    # Generate output
    annotated = generate_annotated_article(article, filtered_issues)
    summary = generate_summary(all_issues, readability, severity_threshold)

    output_content = "# 校閲結果\n\n"
    output_content += f"- 対象ファイル: `{input_path.name}`\n"
    output_content += f"- 校閲日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    output_content += f"- スイープ: {', '.join(SWEEP_NAMES[s] for s in sweeps)}\n"
    if style_config:
        output_content += f"- スタイル: {style_config.get('name', 'カスタム')}\n"
    output_content += "\n---\n\n"
    output_content += annotated
    output_content += f"\n{summary}"

    output_path.write_text(output_content, encoding="utf-8")

    print(f"\n{'='*50}")
    print("校閲完了")
    print(f"  検出件数: {len(all_issues)} 件（表示: {len(filtered_issues)} 件）")
    print(f"  読みやすさスコア: {readability['total']}/100")
    print(f"  出力ファイル: {output_path}")


if __name__ == "__main__":
    main()

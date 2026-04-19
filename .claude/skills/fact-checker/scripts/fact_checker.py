#!/usr/bin/env python3
"""
Fact Checker - 記事内の事実主張を抽出し、Web検索で裏付け確認する。

Usage:
    python fact_checker.py --input article.md
    python fact_checker.py --input article.md --category numbers --depth thorough
    python fact_checker.py --test
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

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

CATEGORY_LABELS = {
    "numbers": "数値・統計",
    "dates": "日付・時系列",
    "names": "固有名詞",
    "causation": "因果関係",
    "citations": "引用・出典",
}

VERDICT_LABELS = {
    "verified": "✅ 確認済",
    "needs_review": "⚠️ 要確認",
    "discrepancy": "❌ 不一致",
    "unverifiable": "ℹ️ 検証不能",
}

GEMINI_MODEL = os.environ.get("GEMINI_FACT_CHECK_MODEL", "gemini-3-flash-preview")

DEFAULT_OUTPUT_DIR = ROOT_DIR / "output"

# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------


def get_client():
    """Initialize and return a google.genai Client."""
    from google import genai  # noqa: delayed import

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY が環境変数に設定されていません。")
        print("  export GEMINI_API_KEY=your_key  または .env に記載してください。")
        sys.exit(1)
    return genai.Client(api_key=api_key)


# ---------------------------------------------------------------------------
# Claim extraction
# ---------------------------------------------------------------------------

EXTRACT_PROMPT_TEMPLATE = """\
あなたは事実検証（ファクトチェック）の専門家です。
以下の記事から、検証可能な事実主張（Factual Claims）を抽出してください。

## 抽出対象カテゴリ
{categories}

## 出力形式
必ず以下のJSON配列形式で出力してください。JSON以外のテキストは含めないでください。
```json
[
  {{
    "id": 1,
    "claim": "主張のテキスト（記事からの引用）",
    "category": "numbers|dates|names|causation|citations",
    "search_query": "この主張を検証するための最適な検索クエリ（日本語または英語）"
  }}
]
```

## ルール
1. 主観的な意見や推測は除外し、客観的に検証可能な事実のみを抽出する
2. 1つの文に複数の事実が含まれる場合は分割する
3. search_query は具体的で検証に有効なキーワードを含める
4. 最大20件まで抽出する（重要度の高い順）

## 記事
{article}
"""


def build_category_description(category: str) -> str:
    """Build the category description section for the extraction prompt."""
    if category == "all":
        lines = []
        for key, label in CATEGORY_LABELS.items():
            lines.append(f"- **{label}** ({key})")
        return "\n".join(lines)
    label = CATEGORY_LABELS.get(category, category)
    return f"- **{label}** ({category}) のみを対象としてください。他のカテゴリは無視してください。"


def extract_claims(client, article_text: str, category: str) -> list[dict]:
    """Use Gemini to extract factual claims from the article."""
    from google.genai import types  # noqa: delayed import

    prompt = EXTRACT_PROMPT_TEMPLATE.format(
        categories=build_category_description(category),
        article=article_text,
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )

    raw = response.text.strip()

    # Parse JSON -- handle possible markdown fences
    if raw.startswith("```"):
        lines = raw.split("\n")
        # Remove first and last fence lines
        lines = [line for line in lines if not line.strip().startswith("```")]
        raw = "\n".join(lines)

    try:
        claims = json.loads(raw)
    except json.JSONDecodeError:
        print("Warning: Gemini の応答を JSON としてパースできませんでした。")
        print(f"Raw response:\n{raw[:500]}")
        claims = []

    if not isinstance(claims, list):
        claims = []

    return claims


# ---------------------------------------------------------------------------
# Claim verification
# ---------------------------------------------------------------------------

VERIFY_PROMPT_TEMPLATE = """\
あなたは事実検証（ファクトチェック）の専門家です。
以下の主張が正確かどうかを、あなたの知識に基づいて検証してください。

## 検証対象の主張
「{claim}」

## カテゴリ
{category}

## 検索結果・参考情報
{search_context}

## 出力形式
必ず以下のJSON形式で出力してください。JSON以外のテキストは含めないでください。
```json
{{
  "verdict": "verified|needs_review|discrepancy|unverifiable",
  "confidence": 0-100,
  "reason": "判定理由の説明（日本語、1-3文）",
  "sources": ["参考にした情報源やURL（わかる範囲で）"]
}}
```

## 判定基準
- **verified**: 複数の信頼できる情報源で裏付けられる
- **needs_review**: 部分的に一致するが、数値の差異や情報の古さがある
- **discrepancy**: 信頼できる情報源と明確に矛盾する
- **unverifiable**: 公開情報として確認できない
"""


def verify_claim_with_grounding(client, claim: dict, depth: str) -> dict:
    """Verify a single claim using Gemini with Google Search grounding."""
    from google.genai import types  # noqa: delayed import

    search_query = claim.get("search_query", claim.get("claim", ""))
    category_label = CATEGORY_LABELS.get(claim.get("category", ""), claim.get("category", ""))

    # Step 1: Use Google Search grounding to gather context
    try:
        search_tool = types.Tool(google_search=types.GoogleSearch())
        search_response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[f"以下について、最新の正確な情報を調べてください: {search_query}"],
            config=types.GenerateContentConfig(
                tools=[search_tool],
                temperature=0.1,
            ),
        )
        search_context = search_response.text.strip() if search_response.text else "検索結果なし"

        # Extract grounding sources if available
        grounding_sources = []
        if hasattr(search_response, "candidates") and search_response.candidates:
            candidate = search_response.candidates[0]
            if hasattr(candidate, "grounding_metadata") and candidate.grounding_metadata:
                metadata = candidate.grounding_metadata
                if hasattr(metadata, "grounding_chunks") and metadata.grounding_chunks:
                    for chunk in metadata.grounding_chunks:
                        if hasattr(chunk, "web") and chunk.web:
                            url = getattr(chunk.web, "uri", "")
                            title = getattr(chunk.web, "title", "")
                            if url:
                                grounding_sources.append(f"[{title or url}]({url})")
    except Exception as e:
        search_context = f"検索エラー: {e}"
        grounding_sources = []

    # Step 2: Verify the claim using the gathered context
    verify_prompt = VERIFY_PROMPT_TEMPLATE.format(
        claim=claim.get("claim", ""),
        category=category_label,
        search_context=search_context,
    )

    try:
        verify_response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[verify_prompt],
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
            ),
        )
        raw = verify_response.text.strip()

        # Parse JSON
        if raw.startswith("```"):
            lines = raw.split("\n")
            lines = [line for line in lines if not line.strip().startswith("```")]
            raw = "\n".join(lines)

        result = json.loads(raw)
    except (json.JSONDecodeError, Exception) as e:
        result = {
            "verdict": "unverifiable",
            "confidence": 0,
            "reason": f"検証処理中にエラーが発生: {e}",
            "sources": [],
        }

    # Merge grounding sources into the result
    existing_sources = result.get("sources", [])
    if grounding_sources:
        existing_sources.extend(grounding_sources)
    result["sources"] = existing_sources

    return result


def verify_claim_quick(client, claim: dict) -> dict:
    """Quick verification using Gemini without grounding (faster)."""
    from google.genai import types  # noqa: delayed import

    category_label = CATEGORY_LABELS.get(claim.get("category", ""), claim.get("category", ""))

    verify_prompt = VERIFY_PROMPT_TEMPLATE.format(
        claim=claim.get("claim", ""),
        category=category_label,
        search_context="(クイックモード: Web検索なし。あなたの学習データに基づいて判断してください。情報の確度が低い場合は needs_review としてください。)",
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[verify_prompt],
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
            ),
        )
        raw = response.text.strip()

        if raw.startswith("```"):
            lines = raw.split("\n")
            lines = [line for line in lines if not line.strip().startswith("```")]
            raw = "\n".join(lines)

        result = json.loads(raw)
    except (json.JSONDecodeError, Exception) as e:
        result = {
            "verdict": "unverifiable",
            "confidence": 0,
            "reason": f"検証処理中にエラーが発生: {e}",
            "sources": [],
        }

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def generate_report(
    claims: list[dict],
    results: list[dict],
    input_path: str,
    depth: str,
) -> str:
    """Generate a Markdown fact-check report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Count verdicts
    counts = {"verified": 0, "needs_review": 0, "discrepancy": 0, "unverifiable": 0}
    for r in results:
        v = r.get("verdict", "unverifiable")
        if v in counts:
            counts[v] += 1
        else:
            counts["unverifiable"] += 1

    total = len(claims)

    lines = [
        "# ファクトチェックレポート",
        "",
        f"**対象ファイル**: {input_path}",
        f"**検証日時**: {now}",
        f"**検証深度**: {depth}",
        "",
        "## サマリー",
        "",
        f"- 検出した主張: **{total}件**",
        f"- ✅ 確認済: **{counts['verified']}件**",
        f"- ⚠️ 要確認: **{counts['needs_review']}件**",
        f"- ❌ 不一致: **{counts['discrepancy']}件**",
        f"- ℹ️ 検証不能: **{counts['unverifiable']}件**",
        "",
        "---",
        "",
        "## 詳細",
        "",
    ]

    for i, (claim, result) in enumerate(zip(claims, results), 1):
        claim_text = claim.get("claim", "(不明)")
        category_key = claim.get("category", "")
        category_label = CATEGORY_LABELS.get(category_key, category_key)
        verdict = result.get("verdict", "unverifiable")
        verdict_label = VERDICT_LABELS.get(verdict, verdict)
        confidence = result.get("confidence", 0)
        reason = result.get("reason", "")
        sources = result.get("sources", [])

        lines.append(f"### 主張{i}: 「{claim_text}」")
        lines.append("")
        lines.append(f"- **カテゴリ**: {category_label}")
        lines.append(f"- **判定**: {verdict_label}")
        lines.append(f"- **信頼度**: {confidence}%")
        lines.append(f"- **理由**: {reason}")

        if sources:
            lines.append("- **出典**:")
            for src in sources:
                lines.append(f"  - {src}")

        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"*このレポートは Fact Checker スキルにより自動生成されました（{now}）*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Test mode
# ---------------------------------------------------------------------------

SAMPLE_ARTICLE = """\
# AIの最新動向

OpenAIは2015年12月にサンフランシスコで設立された非営利のAI研究所です。
共同創設者にはサム・アルトマンとイーロン・マスクが含まれます。

2024年のAI市場規模は約1840億ドルに達し、前年比で約37%の成長を記録しました。
Gartnerの予測によると、2027年までにAI市場は5000億ドルを超えるとされています。

日本では2023年にAI戦略会議が設置され、政府はAI関連予算として
約2000億円を計上しました。経済産業省の報告によれば、
日本企業のAI導入率は2024年時点で約35%です。

GPT-4は2023年3月14日に公開され、大規模マルチモーダルモデルとして
テキストと画像の両方を処理できます。

Anthropicは2021年にDario AmodeとDaniela Amodeiによって設立されました。
"""


def run_test_mode():
    """Run in test mode with hardcoded sample data, no API needed."""
    print("=" * 60)
    print("  Fact Checker - テストモード")
    print("=" * 60)
    print()
    print("サンプル記事を使用してテストを実行します（APIは使用しません）。")
    print()

    # Simulated claims extraction
    sample_claims = [
        {
            "id": 1,
            "claim": "OpenAIは2015年12月にサンフランシスコで設立された",
            "category": "dates",
            "search_query": "OpenAI founding date San Francisco 2015",
        },
        {
            "id": 2,
            "claim": "共同創設者にはサム・アルトマンとイーロン・マスクが含まれる",
            "category": "names",
            "search_query": "OpenAI co-founders Sam Altman Elon Musk",
        },
        {
            "id": 3,
            "claim": "2024年のAI市場規模は約1840億ドル",
            "category": "numbers",
            "search_query": "AI market size 2024 billion dollars",
        },
        {
            "id": 4,
            "claim": "Gartnerの予測では2027年までにAI市場は5000億ドルを超える",
            "category": "citations",
            "search_query": "Gartner AI market forecast 2027 500 billion",
        },
        {
            "id": 5,
            "claim": "GPT-4は2023年3月14日に公開された",
            "category": "dates",
            "search_query": "GPT-4 release date March 2023",
        },
        {
            "id": 6,
            "claim": "Anthropicは2021年にDario AmodeとDaniela Amodeiによって設立された",
            "category": "names",
            "search_query": "Anthropic founded 2021 Dario Daniela Amodei",
        },
    ]

    # Simulated verification results
    sample_results = [
        {
            "verdict": "verified",
            "confidence": 95,
            "reason": "OpenAIは2015年12月に設立。サンフランシスコを拠点としていることも複数ソースで確認済み。",
            "sources": ["https://en.wikipedia.org/wiki/OpenAI"],
        },
        {
            "verdict": "verified",
            "confidence": 90,
            "reason": "サム・アルトマンとイーロン・マスクはともにOpenAIの共同創設者として広く知られている。",
            "sources": ["https://openai.com/about"],
        },
        {
            "verdict": "needs_review",
            "confidence": 60,
            "reason": "AI市場規模の推定値はソースにより異なる。1840億ドルはいくつかのレポートに近い数値だが、異なる定義を使うソースもある。",
            "sources": ["https://www.statista.com/statistics/ai-market-size/"],
        },
        {
            "verdict": "needs_review",
            "confidence": 50,
            "reason": "Gartnerは様々なAI市場予測を発表しているが、5000億ドルという具体的な数値の出典を特定できない。予測値は報告書のバージョンにより変動する。",
            "sources": [],
        },
        {
            "verdict": "verified",
            "confidence": 98,
            "reason": "GPT-4は2023年3月14日にOpenAIから公開された。これは広く報道された事実。",
            "sources": ["https://openai.com/research/gpt-4"],
        },
        {
            "verdict": "discrepancy",
            "confidence": 85,
            "reason": "Anthropicは2021年設立で正しいが、共同創設者の名前は「Dario Amodei」であり、記事中の「Dario Amode」はスペルミスの可能性がある。",
            "sources": ["https://en.wikipedia.org/wiki/Anthropic"],
        },
    ]

    print("--- 抽出された主張 ---")
    for c in sample_claims:
        cat = CATEGORY_LABELS.get(c["category"], c["category"])
        print(f"  [{c['id']}] ({cat}) {c['claim']}")
    print()

    report = generate_report(sample_claims, sample_results, "sample_article.md", "test")
    print(report)

    # Write test report
    output_dir = DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "fact_report_test.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"\nテストレポートを保存しました: {output_path}")


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------


def run_fact_check(input_path: str, output_path: str, category: str, depth: str):
    """Run the full fact-checking workflow."""
    # 1. Load article
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: 入力ファイルが見つかりません: {input_path}")
        sys.exit(1)

    article_text = input_file.read_text(encoding="utf-8")
    if not article_text.strip():
        print(f"Error: 入力ファイルが空です: {input_path}")
        sys.exit(1)

    print("=" * 60)
    print("  Fact Checker - ファクトチェック実行")
    print("=" * 60)
    print(f"  入力: {input_path}")
    print(f"  カテゴリ: {category}")
    print(f"  検証深度: {depth}")
    print()

    # 2. Initialize Gemini client
    client = get_client()

    # 3. Extract claims
    print("📋 記事から事実主張を抽出中...")
    claims = extract_claims(client, article_text, category)

    if not claims:
        print("主張が見つかりませんでした。記事の内容を確認してください。")
        sys.exit(0)

    print(f"  → {len(claims)}件の主張を検出しました。")
    print()

    for c in claims:
        cat = CATEGORY_LABELS.get(c.get("category", ""), c.get("category", ""))
        print(f"  [{c.get('id', '?')}] ({cat}) {c.get('claim', '')}")
    print()

    # 4. Verify each claim
    print("🔍 各主張を検証中...")
    results = []
    for i, claim in enumerate(claims, 1):
        claim_text = claim.get("claim", "")
        print(f"  [{i}/{len(claims)}] 検証中: {claim_text[:60]}...")

        if depth == "thorough":
            result = verify_claim_with_grounding(client, claim, depth)
        else:
            result = verify_claim_quick(client, claim)

        verdict_label = VERDICT_LABELS.get(result.get("verdict", ""), "?")
        confidence = result.get("confidence", 0)
        print(f"           → {verdict_label} (信頼度: {confidence}%)")
        results.append(result)

    print()

    # 5. Generate report
    print("📝 レポートを生成中...")
    report = generate_report(claims, results, input_path, depth)

    # 6. Write output
    if output_path:
        out = Path(output_path)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = DEFAULT_OUTPUT_DIR / f"fact_report_{timestamp}.md"

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")

    # Summary
    counts = {"verified": 0, "needs_review": 0, "discrepancy": 0, "unverifiable": 0}
    for r in results:
        v = r.get("verdict", "unverifiable")
        if v in counts:
            counts[v] += 1

    print()
    print("=" * 60)
    print("  ファクトチェック完了")
    print("=" * 60)
    print(f"  レポート: {out}")
    print()
    print("  --- サマリー ---")
    print(f"  検出した主張:   {len(claims)}件")
    print(f"  ✅ 確認済:      {counts['verified']}件")
    print(f"  ⚠️ 要確認:      {counts['needs_review']}件")
    print(f"  ❌ 不一致:      {counts['discrepancy']}件")
    print(f"  ℹ️ 検証不能:    {counts['unverifiable']}件")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Fact Checker - 記事内の事実主張を抽出し、Web検索で裏付け確認する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
例:
  python fact_checker.py --input article.md
  python fact_checker.py --input article.md --category numbers --depth thorough
  python fact_checker.py --input article.md --output report.md
  python fact_checker.py --test
""",
    )

    parser.add_argument(
        "--input", "-i",
        type=str,
        help="入力ファイルパス（Markdown/テキスト）",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="出力レポートのパス（デフォルト: output/fact_report_{timestamp}.md）",
    )
    parser.add_argument(
        "--category", "-c",
        type=str,
        default="all",
        choices=["all", "numbers", "dates", "names", "causation", "citations"],
        help="チェック対象カテゴリ（デフォルト: all）",
    )
    parser.add_argument(
        "--depth", "-d",
        type=str,
        default="quick",
        choices=["quick", "thorough"],
        help="検証深度: quick（高速）/ thorough（詳細、Google Search grounding使用）",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="テストモード（API不要、サンプル記事で動作確認）",
    )

    args = parser.parse_args()

    if args.test:
        run_test_mode()
        return

    if not args.input:
        parser.error("--input は必須です（--test モード以外）")

    run_fact_check(args.input, args.output, args.category, args.depth)


if __name__ == "__main__":
    main()

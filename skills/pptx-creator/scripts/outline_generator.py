"""
outline_generator.py — Gemini Flash でトピックから構造化アウトライン(YAML)を生成

bootcamp_utils.py の get_client() / get_flash_model() を再利用。
"""

import sys
import re
from pathlib import Path

import yaml

# bootcamp_utils を tools/ から import
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from bootcamp_utils import get_client, get_flash_model


# ---------------------------------------------------------------------------
# Supported slide types
# ---------------------------------------------------------------------------
VALID_SLIDE_TYPES = {
    "title", "section", "content", "key_message", "two_column",
    "comparison", "agenda", "closing",
    "kpi_dashboard", "process_flow", "table",
}

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

def _build_system_prompt(slides_count, audience, language):
    lang_label = "日本語" if language == "ja" else "English"
    return f"""あなたはプレゼンテーション構成のプロフェッショナルです。
与えられたトピックから、{slides_count}枚構成のスライドアウトラインをYAML形式で生成してください。

## 出力言語
{lang_label}

## 対象聴衆
{audience}

## スライドタイプ一覧（slide_type フィールドに使用）

| slide_type | 説明 | 必須フィールド |
|------------|------|---------------|
| title | タイトルスライド（最初のスライド） | title, subtitle |
| section | セクション区切り | title, subtitle |
| content | 通常コンテンツ（箇条書き） | title, bullets (list of strings) |
| key_message | 1つの主要メッセージ | title, body (string) |
| two_column | 2列レイアウト | title, left_body, right_body |
| comparison | 比較（左右ブロック） | title, left (title + items list), right (title + items list) |
| agenda | アジェンダ・目次 | title, bullets |
| closing | 締めスライド（最後） | title, subtitle |
| kpi_dashboard | KPIカード表示（3-4個） | title, kpis (list of {{label, value, unit, change}}) |
| process_flow | プロセスフロー（3-5ステップ） | title, steps (list of {{title, description}}) |
| table | テーブル表示 | title, table_data ({{headers: list, rows: list of lists}}) |

## ルール
1. slide_number は 1 から連番
2. 最初のスライドは必ず slide_type: title
3. 最後のスライドは必ず slide_type: closing
4. 全体で {slides_count} 枚
5. kpi_dashboard の kpis は 3〜4 個
6. process_flow の steps は 3〜5 個
7. table の rows は各行が headers と同じ列数
8. content の bullets は 3〜5 個（6個以上は禁止、情報過多になる）
9. 多様な slide_type を活用すること（全部 content にしない）
10. YAMLブロック以外のテキストは出力しない

## プロフェッショナル品質ガイドライン（コンサルファーム水準）
- 1スライド1メッセージの原則を厳守
- タイトルは結論・主張を示す（「売上状況」ではなく「売上は前年比120%で好調推移」）
- 箇条書きは具体的かつ簡潔に（1行15〜25文字目安）
- agenda スライドを title の直後に配置（3枚以上の場合）
- key_message, kpi_dashboard, process_flow, comparison 等を積極的に活用
- closing にはNext Steps / CTA / 連絡先を含める

## 出力形式

```yaml
title: "プレゼンタイトル"
slides:
  - slide_number: 1
    slide_type: title
    title: "タイトルテキスト"
    subtitle: "サブタイトルテキスト"
  - slide_number: 2
    slide_type: agenda
    title: "アジェンダ"
    bullets:
      - "項目1"
      - "項目2"
      - "項目3"
  - slide_number: 3
    slide_type: kpi_dashboard
    title: "主要KPI"
    kpis:
      - {{label: "売上", value: "150", unit: "億円", change: "+12%"}}
      - {{label: "顧客数", value: "5,000", unit: "社", change: "+8%"}}
      - {{label: "満足度", value: "92", unit: "%", change: "+3%"}}
  - slide_number: 4
    slide_type: content
    title: "コンテンツ例"
    bullets:
      - "ポイント1の説明"
      - "ポイント2の説明"
      - "ポイント3の説明"
  - slide_number: 5
    slide_type: process_flow
    title: "導入プロセス"
    steps:
      - {{title: "計画", description: "要件定義と目標設定"}}
      - {{title: "実行", description: "パイロット導入"}}
      - {{title: "評価", description: "効果測定"}}
  - slide_number: 6
    slide_type: closing
    title: "ご清聴ありがとうございました"
    subtitle: "お問い合わせ先: example@co.jp"
```
"""


def _parse_gemini_response(text):
    """```yaml``` ブロックを抽出して YAML パース"""
    # Try to extract yaml code block
    match = re.search(r"```(?:yaml)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        yaml_text = match.group(1)
    else:
        # Assume entire response is YAML
        yaml_text = text.strip()

    return yaml.safe_load(yaml_text)


def _validate_outline(outline, slides_count):
    """slide_type 検証、不明→content フォールバック、連番振り直し"""
    if not isinstance(outline, dict) or "slides" not in outline:
        raise ValueError("Outline must have a 'slides' key")

    slides = outline["slides"]
    if not isinstance(slides, list) or len(slides) == 0:
        raise ValueError("Outline must have at least one slide")

    validated = []
    for i, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        st = slide.get("slide_type", "content")
        if st not in VALID_SLIDE_TYPES:
            print(f"[outline] Warning: unknown slide_type '{st}' at slide {i+1}, falling back to 'content'", file=sys.stderr)
            slide["slide_type"] = "content"
            if "bullets" not in slide:
                slide["bullets"] = [slide.get("body", "内容を追加してください")]
        slide["slide_number"] = i + 1
        validated.append(slide)

    # Ensure first is title, last is closing
    if validated and validated[0].get("slide_type") != "title":
        validated[0]["slide_type"] = "title"
    if validated and validated[-1].get("slide_type") != "closing":
        validated[-1]["slide_type"] = "closing"

    outline["slides"] = validated
    return outline


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_outline(topic, slides_count=8, audience="business", language="ja"):
    """
    Gemini Flash でトピックからアウトライン生成。

    Args:
        topic: プレゼンのトピック
        slides_count: スライド枚数
        audience: 対象聴衆
        language: 出力言語 ("ja" or "en")

    Returns:
        dict: アウトライン (title, slides)

    Raises:
        RuntimeError: Gemini API エラーまたは YAML パース失敗
    """
    client = get_client()
    if client is None:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY が未設定です。", file=sys.stderr)
        print("  export GEMINI_API_KEY='your-key' を実行してください。", file=sys.stderr)
        sys.exit(1)

    model = get_flash_model()
    system_prompt = _build_system_prompt(slides_count, audience, language)
    user_prompt = f"トピック: {topic}\n\n上記トピックで {slides_count} 枚構成のプレゼンテーションアウトラインをYAMLで生成してください。"

    max_retries = 2
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    {"role": "user", "parts": [{"text": system_prompt + "\n\n" + user_prompt}]}
                ],
            )
            text = response.text
            outline = _parse_gemini_response(text)
            outline = _validate_outline(outline, slides_count)
            return outline

        except yaml.YAMLError as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"[outline] YAML parse failed (attempt {attempt+1}), retrying...", file=sys.stderr)
                continue
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"[outline] API error (attempt {attempt+1}): {e}, retrying...", file=sys.stderr)
                continue

    raise RuntimeError(f"アウトライン生成に失敗しました ({max_retries}回試行): {last_error}")


def save_outline(outline, path):
    """アウトラインをYAMLファイルに保存"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        yaml.dump(outline, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"[outline] Saved: {p.resolve()}")


def load_outline(path):
    """YAMLファイルからアウトラインを読み込み"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Outline file not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        outline = yaml.safe_load(f)
    return _validate_outline(outline, len(outline.get("slides", [])))

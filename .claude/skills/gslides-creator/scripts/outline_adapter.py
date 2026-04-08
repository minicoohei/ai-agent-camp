"""
outline_adapter.py — Gemini アウトライン YAML → GAS slideSpecs 変換

pptx-creator の outline_generator.py と同じアウトライン YAML を受け取り、
deckSlides.js の createDeck() が受け付ける slideSpecs 形式に変換する。
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# bootcamp_utils を tools/ から import
_TOOLS_DIR = str(Path(__file__).resolve().parents[3] / "tools")
sys.path.insert(0, _TOOLS_DIR)

try:
    from bootcamp_utils import get_client, get_flash_model
except ImportError:
    def get_client():
        return None
    def get_flash_model() -> str:
        return "gemini-3-flash-preview"


# ─── スタイル定義 ──────────────────────────────────────────────

STYLES = {
    "corporate": {
        "primary_color": "#2563EB",
        "secondary_color": "#1E40AF",
        "accent_color": "#FBBF24",
        "text_color": "#1F2D3D",
        "bg_color": "#FFFFFF",
        "title_font": "Noto Sans JP",
        "body_font": "Noto Sans JP",
        "title_size": 36,
        "subtitle_size": 20,
        "heading_size": 28,
        "body_size": 16,
    },
    "minimal": {
        "primary_color": "#111827",
        "secondary_color": "#374151",
        "accent_color": "#EF4444",
        "text_color": "#111827",
        "bg_color": "#FFFFFF",
        "title_font": "Noto Sans JP",
        "body_font": "Noto Sans JP",
        "title_size": 32,
        "subtitle_size": 18,
        "heading_size": 26,
        "body_size": 14,
    },
}

# ─── スライドレイアウト寸法 (pt) ────────────────────────────────

SLIDE_W = 720   # 10 inches
SLIDE_H = 405   # 5.625 inches
MARGIN = 40


# ─── Gemini アウトライン生成 ──────────────────────────────────

def generate_outline(
    topic: str,
    slides_count: int = 10,
    audience: str = "ビジネスパーソン",
    language: str = "ja",
) -> dict:
    """Gemini でアウトライン YAML を生成"""
    client = get_client()
    if client is None:
        raise RuntimeError("Gemini client が利用できません。GEMINI_API_KEY を設定してください。")

    system_prompt = _build_system_prompt(slides_count, audience, language)
    user_prompt = f"トピック: {topic}"

    response = client.models.generate_content(
        model=get_flash_model(),
        contents=user_prompt,
        config={
            "system_instruction": system_prompt,
            "temperature": 0.7,
        },
    )

    text = response.text.strip()
    # YAML ブロック抽出
    import re
    yaml_match = re.search(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL)
    if yaml_match:
        text = yaml_match.group(1)
    elif "```" in text:
        generic_match = re.search(r"```\s*\n(.*?)```", text, re.DOTALL)
        if generic_match:
            text = generic_match.group(1)

    outline = yaml.safe_load(text)
    return outline


def _build_system_prompt(slides_count: int, audience: str, language: str) -> str:
    lang_label = "日本語" if language == "ja" else "English"
    return f"""あなたはプレゼンテーション構成のプロフェッショナルです。
与えられたトピックから、{slides_count}枚構成のスライドアウトラインをYAML形式で生成してください。

## 出力言語
{lang_label}

## 対象聴衆
{audience}

## スライドタイプ一覧

| slide_type | 説明 | 必須フィールド |
|------------|------|---------------|
| title | タイトルスライド（最初のスライド） | title, subtitle |
| section | セクション区切り | title, subtitle |
| content | 通常コンテンツ（箇条書き） | title, bullets (list of strings) |
| key_message | 1つの主要メッセージ | title, body (string) |
| two_column | 2列レイアウト | title, left_body, right_body |
| comparison | 比較 | title, left (title + items list), right (title + items list) |
| agenda | アジェンダ・目次 | title, bullets |
| closing | 締めスライド（最後） | title, subtitle |
| kpi_dashboard | KPIカード表示 | title, kpis (list of {{label, value, unit, change}}) |
| process_flow | プロセスフロー | title, steps (list of {{title, description}}) |
| table | テーブル表示 | title, table_data ({{headers: list, rows: list of lists}}) |

## ルール
1. slide_number は 1 から連番
2. 最初のスライドは必ず slide_type: title
3. 最後のスライドは必ず slide_type: closing
4. 全体で {slides_count} 枚
5. 多様な slide_type を活用すること
6. YAMLブロック以外のテキストは出力しない

## 出力形式

```yaml
title: "プレゼンタイトル"
slides:
  - slide_number: 1
    slide_type: title
    title: "タイトルテキスト"
    subtitle: "サブタイトルテキスト"
```"""


# ─── アウトライン → GAS slideSpecs 変換 ───────────────────────

def outline_to_slide_specs(
    outline: dict,
    style_name: str = "corporate",
) -> list:
    """
    アウトライン YAML → GAS createDeck() の slideSpecs 形式に変換

    Returns:
        list of { layout, elements: [{ type, value, position, style }] }
    """
    style = STYLES.get(style_name, STYLES["corporate"])
    slides = outline.get("slides", [])
    specs = []

    for slide in slides:
        slide_type = slide.get("slide_type", "content")
        converter = _CONVERTERS.get(slide_type, _convert_content)
        spec = converter(slide, style)
        specs.append(spec)

    return specs


# ─── スライドタイプ別コンバーター ─────────────────────────────

def _convert_title(slide: dict, style: dict) -> dict:
    return {
        "layout": "BLANK",
        "elements": [
            {
                "type": "textbox",
                "value": slide.get("title", ""),
                "position": {"left": MARGIN, "top": 120, "width": SLIDE_W - MARGIN * 2, "height": 80},
                "style": {
                    "font": style["title_font"],
                    "size": style["title_size"],
                    "bold": True,
                    "color": style["primary_color"],
                    "align": "center",
                },
            },
            {
                "type": "textbox",
                "value": slide.get("subtitle", ""),
                "position": {"left": MARGIN + 60, "top": 220, "width": SLIDE_W - MARGIN * 2 - 120, "height": 50},
                "style": {
                    "font": style["body_font"],
                    "size": style["subtitle_size"],
                    "color": style["text_color"],
                    "align": "center",
                },
            },
        ],
    }


def _convert_section(slide: dict, style: dict) -> dict:
    return {
        "layout": "BLANK",
        "elements": [
            {
                "type": "shape",
                "shape_type": "RECTANGLE",
                "position": {"left": 0, "top": 0, "width": SLIDE_W, "height": SLIDE_H},
                "fill_color": style["primary_color"],
            },
            {
                "type": "textbox",
                "value": slide.get("title", ""),
                "position": {"left": MARGIN + 40, "top": 140, "width": SLIDE_W - MARGIN * 2 - 80, "height": 70},
                "style": {
                    "font": style["title_font"],
                    "size": style["heading_size"],
                    "bold": True,
                    "color": "#FFFFFF",
                    "align": "center",
                },
            },
            {
                "type": "textbox",
                "value": slide.get("subtitle", ""),
                "position": {"left": MARGIN + 80, "top": 220, "width": SLIDE_W - MARGIN * 2 - 160, "height": 40},
                "style": {
                    "font": style["body_font"],
                    "size": style["body_size"],
                    "color": "#E5E7EB",
                    "align": "center",
                },
            },
        ],
    }


def _convert_content(slide: dict, style: dict) -> dict:
    bullets = slide.get("bullets", [])
    bullet_text = "\n".join(f"  {b}" for b in bullets)

    return {
        "layout": "BLANK",
        "elements": [
            {
                "type": "textbox",
                "value": slide.get("title", ""),
                "position": {"left": MARGIN, "top": 30, "width": SLIDE_W - MARGIN * 2, "height": 50},
                "style": {
                    "font": style["title_font"],
                    "size": style["heading_size"],
                    "bold": True,
                    "color": style["primary_color"],
                },
            },
            {
                "type": "textbox",
                "value": bullet_text,
                "position": {"left": MARGIN + 20, "top": 100, "width": SLIDE_W - MARGIN * 2 - 40, "height": 270},
                "style": {
                    "font": style["body_font"],
                    "size": style["body_size"],
                    "color": style["text_color"],
                },
            },
        ],
    }


def _convert_key_message(slide: dict, style: dict) -> dict:
    return {
        "layout": "BLANK",
        "elements": [
            {
                "type": "textbox",
                "value": slide.get("title", ""),
                "position": {"left": MARGIN, "top": 30, "width": SLIDE_W - MARGIN * 2, "height": 50},
                "style": {
                    "font": style["title_font"],
                    "size": style["heading_size"],
                    "bold": True,
                    "color": style["primary_color"],
                },
            },
            {
                "type": "textbox",
                "value": slide.get("body", ""),
                "position": {"left": MARGIN + 40, "top": 130, "width": SLIDE_W - MARGIN * 2 - 80, "height": 200},
                "style": {
                    "font": style["body_font"],
                    "size": 22,
                    "color": style["text_color"],
                    "align": "center",
                },
            },
        ],
    }


def _convert_two_column(slide: dict, style: dict) -> dict:
    col_w = (SLIDE_W - MARGIN * 3) // 2
    return {
        "layout": "BLANK",
        "elements": [
            {
                "type": "textbox",
                "value": slide.get("title", ""),
                "position": {"left": MARGIN, "top": 30, "width": SLIDE_W - MARGIN * 2, "height": 50},
                "style": {
                    "font": style["title_font"],
                    "size": style["heading_size"],
                    "bold": True,
                    "color": style["primary_color"],
                },
            },
            {
                "type": "textbox",
                "value": slide.get("left_body", ""),
                "position": {"left": MARGIN, "top": 100, "width": col_w, "height": 270},
                "style": {"font": style["body_font"], "size": style["body_size"], "color": style["text_color"]},
            },
            {
                "type": "textbox",
                "value": slide.get("right_body", ""),
                "position": {"left": MARGIN * 2 + col_w, "top": 100, "width": col_w, "height": 270},
                "style": {"font": style["body_font"], "size": style["body_size"], "color": style["text_color"]},
            },
        ],
    }


def _convert_comparison(slide: dict, style: dict) -> dict:
    left = slide.get("left", {})
    right = slide.get("right", {})
    col_w = (SLIDE_W - MARGIN * 3) // 2

    left_text = left.get("title", "") + "\n\n" + "\n".join(f"  {i}" for i in left.get("items", []))
    right_text = right.get("title", "") + "\n\n" + "\n".join(f"  {i}" for i in right.get("items", []))

    return {
        "layout": "BLANK",
        "elements": [
            {
                "type": "textbox",
                "value": slide.get("title", ""),
                "position": {"left": MARGIN, "top": 30, "width": SLIDE_W - MARGIN * 2, "height": 50},
                "style": {
                    "font": style["title_font"],
                    "size": style["heading_size"],
                    "bold": True,
                    "color": style["primary_color"],
                },
            },
            {
                "type": "shape",
                "shape_type": "ROUND_RECTANGLE",
                "value": left_text,
                "position": {"left": MARGIN, "top": 100, "width": col_w, "height": 270},
                "fill_color": "#F0F4F8",
                "style": {"font": style["body_font"], "size": style["body_size"], "color": style["text_color"]},
            },
            {
                "type": "shape",
                "shape_type": "ROUND_RECTANGLE",
                "value": right_text,
                "position": {"left": MARGIN * 2 + col_w, "top": 100, "width": col_w, "height": 270},
                "fill_color": "#F0F4F8",
                "style": {"font": style["body_font"], "size": style["body_size"], "color": style["text_color"]},
            },
        ],
    }


def _convert_kpi_dashboard(slide: dict, style: dict) -> dict:
    kpis = slide.get("kpis", [])
    n = len(kpis)
    if n == 0:
        return _convert_content(slide, style)

    card_w = (SLIDE_W - MARGIN * 2 - 20 * (n - 1)) // n
    elements = [
        {
            "type": "textbox",
            "value": slide.get("title", ""),
            "position": {"left": MARGIN, "top": 30, "width": SLIDE_W - MARGIN * 2, "height": 50},
            "style": {
                "font": style["title_font"],
                "size": style["heading_size"],
                "bold": True,
                "color": style["primary_color"],
            },
        },
    ]

    for idx, kpi in enumerate(kpis):
        left = MARGIN + idx * (card_w + 20)
        label = kpi.get("label", "")
        value = kpi.get("value", "")
        unit = kpi.get("unit", "")
        change = kpi.get("change", "")
        card_text = f"{label}\n\n{value} {unit}\n{change}"
        elements.append({
            "type": "shape",
            "shape_type": "ROUND_RECTANGLE",
            "value": card_text,
            "position": {"left": left, "top": 110, "width": card_w, "height": 200},
            "fill_color": "#F0F4F8",
            "style": {
                "font": style["body_font"],
                "size": 14,
                "color": style["text_color"],
                "align": "center",
            },
        })

    return {"layout": "BLANK", "elements": elements}


def _convert_process_flow(slide: dict, style: dict) -> dict:
    steps = slide.get("steps", [])
    n = len(steps)
    if n == 0:
        return _convert_content(slide, style)

    step_w = (SLIDE_W - MARGIN * 2 - 15 * (n - 1)) // n
    elements = [
        {
            "type": "textbox",
            "value": slide.get("title", ""),
            "position": {"left": MARGIN, "top": 30, "width": SLIDE_W - MARGIN * 2, "height": 50},
            "style": {
                "font": style["title_font"],
                "size": style["heading_size"],
                "bold": True,
                "color": style["primary_color"],
            },
        },
    ]

    for idx, step in enumerate(steps):
        left = MARGIN + idx * (step_w + 15)
        step_title = step.get("title", f"Step {idx + 1}")
        step_desc = step.get("description", "")
        step_text = f"{idx + 1}. {step_title}\n\n{step_desc}"
        elements.append({
            "type": "shape",
            "shape_type": "ROUND_RECTANGLE",
            "value": step_text,
            "position": {"left": left, "top": 110, "width": step_w, "height": 240},
            "fill_color": style["primary_color"] if idx == 0 else "#F0F4F8",
            "style": {
                "font": style["body_font"],
                "size": 12,
                "color": "#FFFFFF" if idx == 0 else style["text_color"],
            },
        })

    return {"layout": "BLANK", "elements": elements}


def _convert_table(slide: dict, style: dict) -> dict:
    table_data = slide.get("table_data", {})
    headers = table_data.get("headers", [])
    rows = table_data.get("rows", [])

    value = [headers] + rows if headers else rows

    return {
        "layout": "BLANK",
        "elements": [
            {
                "type": "textbox",
                "value": slide.get("title", ""),
                "position": {"left": MARGIN, "top": 30, "width": SLIDE_W - MARGIN * 2, "height": 50},
                "style": {
                    "font": style["title_font"],
                    "size": style["heading_size"],
                    "bold": True,
                    "color": style["primary_color"],
                },
            },
            {
                "type": "table",
                "value": value,
                "position": {"left": MARGIN, "top": 100, "width": SLIDE_W - MARGIN * 2, "height": 270},
                "header_style": {"bold": True, "size": 12, "color": "#FFFFFF"},
            },
        ],
    }


def _convert_closing(slide: dict, style: dict) -> dict:
    return {
        "layout": "BLANK",
        "elements": [
            {
                "type": "textbox",
                "value": slide.get("title", "Thank You"),
                "position": {"left": MARGIN, "top": 130, "width": SLIDE_W - MARGIN * 2, "height": 80},
                "style": {
                    "font": style["title_font"],
                    "size": style["title_size"],
                    "bold": True,
                    "color": style["primary_color"],
                    "align": "center",
                },
            },
            {
                "type": "textbox",
                "value": slide.get("subtitle", ""),
                "position": {"left": MARGIN + 60, "top": 230, "width": SLIDE_W - MARGIN * 2 - 120, "height": 40},
                "style": {
                    "font": style["body_font"],
                    "size": style["subtitle_size"],
                    "color": style["text_color"],
                    "align": "center",
                },
            },
        ],
    }


# コンバーターマップ
_CONVERTERS = {
    "title": _convert_title,
    "section": _convert_section,
    "content": _convert_content,
    "key_message": _convert_key_message,
    "two_column": _convert_two_column,
    "comparison": _convert_comparison,
    "agenda": _convert_content,  # agenda は content と同じレイアウト
    "closing": _convert_closing,
    "kpi_dashboard": _convert_kpi_dashboard,
    "process_flow": _convert_process_flow,
    "table": _convert_table,
}

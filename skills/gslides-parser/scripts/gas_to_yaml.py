"""
gas_to_yaml.py — GAS パース結果(JSON) → pptx-converter互換 マッピングYAML 変換

GAS の parsePresentation() が返すJSON構造を、
pptx-converter の mapper.py と同等のセマンティック解析 + プレースホルダー付与を行い
マッピング YAML に変換する。
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# pptx-converter の mapper.py からロール定義を再利用
_TOOLS_DIR = str(Path(__file__).resolve().parents[3] / "tools")
sys.path.insert(0, _TOOLS_DIR)

try:
    from bootcamp_utils import get_client, get_flash_model
except ImportError:
    def get_client():
        return None
    def get_flash_model() -> str:
        return "gemini-3-flash-preview"


# ─── ロール定義 ──────────────────────────────────────────────

ROLE_CATEGORIES = {
    "text": [
        "title", "subtitle", "heading", "body", "caption",
        "label", "footnote", "page_number", "bullet_list",
    ],
    "image": [
        "hero_image", "logo", "icon", "photo", "decorative", "background",
    ],
    "table": [
        "data_table", "comparison_table", "schedule_table",
    ],
    "chart": [
        "revenue_chart", "trend_chart", "comparison_chart",
    ],
    "shape": [
        "accent_decoration", "callout", "divider", "background_shape",
    ],
    "group": [
        "process_flow", "feature_cards", "step_diagram",
    ],
}

_DECORATIVE_ROLES = frozenset({
    "decorative", "background", "background_shape",
    "divider", "accent_decoration",
})


# ─── メイン変換関数 ──────────────────────────────────────────

def convert_gas_to_mapping(gas_data: dict, use_gemini: bool = True) -> dict:
    """
    GAS parsePresentation() 出力 → マッピング YAML 辞書

    Args:
        gas_data: GAS が返した JSON 辞書
        use_gemini: Gemini セマンティック解析を使うか

    Returns:
        pptx-converter 互換のマッピング辞書
    """
    mapping = {
        "source": gas_data.get("source", "Google Slides"),
        "presentation_id": gas_data.get("presentation_id", ""),
        "presentation_url": gas_data.get("presentation_url", ""),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "slide_width_pt": gas_data.get("slide_width_pt", 0),
        "slide_height_pt": gas_data.get("slide_height_pt", 0),
        "slides": [],
        "placeholders": [],
    }

    all_placeholders = []

    for slide_data in gas_data.get("slides", []):
        slide_num = slide_data.get("slide_number", 0)
        elements = slide_data.get("elements", [])

        # セマンティック解析
        analyzed = _analyze_elements(elements, slide_num, use_gemini)

        # プレースホルダー付与
        with_ph = _assign_placeholders(analyzed, slide_num)

        # マッピング構築
        slide_elements = []
        for elem in with_ph:
            entry = _build_entry(elem)
            slide_elements.append(entry)

            if entry.get("placeholder"):
                all_placeholders.append({
                    "key": entry["placeholder"],
                    "type": entry.get("type", ""),
                    "role": entry.get("role", ""),
                    "current": _extract_current(entry),
                })

        mapping["slides"].append({
            "slide_number": slide_num,
            "object_id": slide_data.get("object_id", ""),
            "layout": slide_data.get("layout", ""),
            "elements": slide_elements,
        })

    mapping["placeholders"] = all_placeholders
    return mapping


def save_yaml(mapping: dict, output_path: str) -> None:
    """マッピングを YAML ファイルに保存"""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        yaml.dump(
            mapping, f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=120,
        )
    print(f"[yaml] Saved: {out.resolve()}")


# ─── セマンティック解析 ──────────────────────────────────────

def _analyze_elements(
    elements: list, slide_number: int, use_gemini: bool
) -> list:
    """要素に role / hint を付与"""
    result = []
    for elem in elements:
        elem = dict(elem)  # コピー

        if use_gemini:
            # TODO: Gemini 解析の実装（将来）
            pass

        # ヒューリスティック
        _apply_heuristic(elem, slide_number)

        # グループ子要素も再帰的に処理
        if elem.get("type") == "group" and "children" in elem:
            elem["children"] = _analyze_elements(
                elem["children"], slide_number, use_gemini
            )

        result.append(elem)
    return result


def _apply_heuristic(elem: dict, slide_number: int) -> None:
    """ヒューリスティックで role / hint を付与"""
    etype = elem.get("type", "")
    value = elem.get("value", "")
    if isinstance(value, (list, dict)):
        value = ""
    value = str(value) if value else ""

    style = elem.get("style", {}) or {}
    font_size = style.get("size", 0) or 0
    bold = style.get("bold", False)
    shape_type = (elem.get("shape_type", "") or "").upper()
    is_ph = elem.get("is_placeholder", False)
    ph_type = (elem.get("placeholder_type", "") or "").upper()

    role = ""
    hint = ""

    if etype == "text":
        role, hint = _heuristic_text(value, font_size, bold, is_ph, ph_type, slide_number)
    elif etype == "shape":
        role, hint = _heuristic_shape(value, shape_type)
    elif etype == "image":
        role, hint = _heuristic_image(elem)
    elif etype == "table":
        role, hint = _heuristic_table(elem)
    elif etype == "chart":
        role, hint = "trend_chart", "チャート。Sheets連携。"
    elif etype == "group":
        children = elem.get("children", [])
        role = "step_diagram"
        hint = f"グループ要素。子要素{len(children)}個。"
    elif etype == "line":
        role = "divider"
        hint = ""
    elif etype == "wordart":
        role = "title" if font_size >= 24 else "label"
        hint = "ワードアート。"
    elif etype == "video":
        role = "decorative"
        hint = "動画要素。"
    else:
        role = etype or "unknown"
        hint = ""

    elem["role"] = role
    elem["hint"] = hint


def _heuristic_text(
    text: str, font_size: int, bold: bool,
    is_placeholder: bool, ph_type: str, slide_number: int
) -> Tuple[str, str]:
    """テキスト要素のロール判定"""
    # プレースホルダータイプベース
    if is_placeholder:
        if "TITLE" in ph_type or "CENTER_TITLE" in ph_type:
            return "title", "メインタイトル。"
        if "SUBTITLE" in ph_type:
            return "subtitle", "サブタイトル。"
        if "BODY" in ph_type:
            return "body", "本文テキスト。"
        if "SLIDE_NUMBER" in ph_type:
            return "page_number", "スライド番号。"

    # ページ番号判定
    if text.strip().isdigit() and len(text.strip()) <= 3:
        return "page_number", "ページ番号。"

    # フォントサイズベース
    if font_size >= 28:
        return "title", f"タイトル。{max(10, 40 - int(font_size))}〜{40 - int(font_size) + 15}文字程度。"
    if font_size >= 20 and bold:
        return "heading", "見出し。"
    if font_size >= 18:
        return "subtitle", "サブタイトル。"

    # 箇条書き判定
    bullet_chars = ["・", "●", "•", "-", "※", "→"]
    if text and ("\n" in text or any(text.lstrip().startswith(c) for c in bullet_chars)):
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return "bullet_list", f"箇条書き。{len(lines)}項目。"

    # 短いテキスト = ラベル
    if text and len(text.strip()) <= 10:
        return "label", "ラベル。短いテキスト。"

    return "body", "本文テキスト。"


def _heuristic_shape(text: str, shape_type: str) -> Tuple[str, str]:
    """Shape 要素のロール判定"""
    if text and text.strip():
        if len(text.strip()) <= 15:
            return "label", "ラベル。"
        return "callout", f"シェイプ内テキスト。{len(text.strip())}文字程度。"

    # テキストなしの図形
    if "RECTANGLE" in shape_type or "ROUND" in shape_type:
        return "accent_decoration", ""
    if "ELLIPSE" in shape_type:
        return "accent_decoration", ""

    return "accent_decoration", ""


def _heuristic_image(elem: dict) -> Tuple[str, str]:
    """画像要素のロール判定"""
    pos = elem.get("position", {})
    width = pos.get("width", 0)
    height = pos.get("height", 0)

    if width > 0 and height > 0:
        if width < 50 and height < 50:
            return "icon", "小さなアイコン。"
        if width > 500:
            return "hero_image", "メインビジュアル。"

    return "photo", "画像。"


def _heuristic_table(elem: dict) -> Tuple[str, str]:
    """テーブル要素のロール判定"""
    config = elem.get("table_config", {})
    rows = config.get("rows", 0)
    cols = config.get("cols", 0)
    return "data_table", f"データテーブル。{rows}行x{cols}列。"


# ─── プレースホルダー付与 ────────────────────────────────────

def _assign_placeholders(elements: list, slide_number: int) -> list:
    """各要素にプレースホルダーキーを付与"""
    type_counters: Dict[str, int] = {}
    role_counters: Dict[str, int] = {}

    result = []
    for elem in elements:
        elem = dict(elem)
        role = elem.get("role", "")

        # デコレーション系はスキップ
        if role in _DECORATIVE_ROLES:
            elem["placeholder"] = None
            result.append(elem)
            continue

        etype = elem.get("type", "")

        if etype in ("chart", "table", "image"):
            key = f"slide_{slide_number}_{etype}"
            count = type_counters.get(key, 0)
            type_counters[key] = count + 1
            if count == 0:
                elem["placeholder"] = "{{" + key + "}}"
            else:
                elem["placeholder"] = "{{" + f"{key}_{count + 1}" + "}}"
        elif etype in ("text", "shape", "wordart"):
            if etype == "shape" and not (elem.get("value") or "").strip():
                elem["placeholder"] = None
            else:
                key = f"slide_{slide_number}_{role or 'element'}"
                count = role_counters.get(key, 0)
                role_counters[key] = count + 1
                if count == 0:
                    elem["placeholder"] = "{{" + key + "}}"
                else:
                    elem["placeholder"] = "{{" + f"{key}_{count + 1}" + "}}"
        elif etype == "group":
            key = f"slide_{slide_number}_{role or 'group'}"
            count = role_counters.get(key, 0)
            role_counters[key] = count + 1
            elem["placeholder"] = "{{" + key + "}}" if count == 0 else "{{" + f"{key}_{count + 1}" + "}}"

            # 子要素にもプレースホルダー付与
            if "children" in elem:
                group_id = elem.get("id", "grp")
                for idx, child in enumerate(elem["children"]):
                    child = dict(child)
                    child_text = child.get("value", "")
                    if isinstance(child_text, str) and child_text.strip():
                        child_role = child.get("role", "step")
                        child["placeholder"] = "{{" + f"group_{group_id}_{child_role}_{idx + 1}" + "}}"
                    else:
                        child["placeholder"] = None
                    elem["children"][idx] = child
        else:
            elem["placeholder"] = None

        result.append(elem)
    return result


# ─── エントリ構築 ────────────────────────────────────────────

def _build_entry(elem: dict) -> dict:
    """マッピングYAML用のエントリを構築"""
    entry = {
        "id": elem.get("id", ""),
        "type": elem.get("type", ""),
        "role": elem.get("role", ""),
        "hint": elem.get("hint", ""),
        "position": elem.get("position", {}),
    }

    etype = elem.get("type", "")

    if etype in ("text", "wordart"):
        entry["style"] = elem.get("style", {})
        entry["value"] = elem.get("value", "")
        if elem.get("is_placeholder"):
            entry["is_placeholder"] = True
            entry["placeholder_type"] = elem.get("placeholder_type", "")
    elif etype == "shape":
        entry["shape_type"] = elem.get("shape_type", "")
        if elem.get("value"):
            entry["value"] = elem["value"]
        if elem.get("fill_color"):
            entry["fill_color"] = elem["fill_color"]
        if elem.get("style"):
            entry["style"] = elem["style"]
    elif etype == "image":
        entry["image_info"] = elem.get("image_info", {})
    elif etype == "table":
        entry["table_config"] = elem.get("table_config", {})
        entry["value"] = elem.get("value", [])
        if elem.get("cell_styles"):
            entry["cell_styles"] = elem["cell_styles"]
    elif etype == "chart":
        entry["chart_info"] = elem.get("chart_info", {})
    elif etype == "group":
        if "children" in elem:
            entry["children"] = [_build_entry(c) for c in elem["children"]]
    elif etype == "line":
        if elem.get("line_type"):
            entry["line_type"] = elem["line_type"]
        if elem.get("line_style"):
            entry["line_style"] = elem["line_style"]

    entry["placeholder"] = elem.get("placeholder")
    return entry


def _extract_current(entry: dict) -> str:
    """エントリから現在値を文字列で取得"""
    etype = entry.get("type", "")
    value = entry.get("value", "")

    if etype in ("text", "shape", "wordart"):
        return str(value)[:100] if value else ""
    if etype == "table":
        if isinstance(value, list):
            return f"table({len(value)} rows)"
        return "table"
    if etype == "chart":
        return "chart(Sheets連携)"
    if etype == "image":
        return "image"

    return str(value)[:100] if value else ""

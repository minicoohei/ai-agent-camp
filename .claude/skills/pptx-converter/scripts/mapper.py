"""
PPTX Mapper - マッピングYAML生成 & Geminiセマンティック解析モジュール

PPTXExtractor の出力を受け取り、各要素にセマンティックロール・置換ヒント・
プレースホルダーキーを付与した YAML マッピングファイルを生成する。

使い方:
    from mapper import PPTXMapper
    mapper = PPTXMapper(extracted_data)
    mapping = mapper.generate_mapping()
    mapper.save_yaml(mapping, "mapping.yaml")
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# ─── Gemini クライアントの読み込み ─────────────────────────────────
# tools/bootcamp_utils.py から get_client / get_flash_model を取得
_TOOLS_DIR = str(Path(__file__).resolve().parent.parent.parent.parent / "tools")
sys.path.insert(0, _TOOLS_DIR)

try:
    from bootcamp_utils import get_client, get_flash_model
except ImportError:
    # bootcamp_utils が見つからない場合のフォールバック
    def get_client():
        return None

    def get_flash_model() -> str:
        return "gemini-3-flash-preview"


# ─── ロールカテゴリ定義 ──────────────────────────────────────────
# 各要素タイプに対応するセマンティックロールの候補一覧
ROLE_CATEGORIES: Dict[str, List[str]] = {
    "text": [
        "title", "subtitle", "heading", "body", "caption",
        "label", "footnote", "page_number", "bullet_list",
    ],
    "chart": [
        "revenue_chart", "trend_chart", "comparison_chart",
        "distribution_chart", "progress_chart",
    ],
    "table": [
        "data_table", "comparison_table", "schedule_table",
        "specs_table", "pricing_table",
    ],
    "image": [
        "hero_image", "logo", "icon", "photo",
        "diagram_image", "decorative", "background",
    ],
    "shape": [
        "accent_decoration", "callout", "flowchart_step",
        "connector", "icon_container", "background_shape", "divider",
    ],
    "group": [
        "process_flow", "timeline", "feature_cards",
        "org_chart", "step_diagram",
    ],
    "smartart": [
        "organization_chart", "process_diagram", "cycle_diagram",
        "hierarchy", "matrix",
    ],
}

# デコレーション系ロール（プレースホルダーを付与しない）
_DECORATIVE_ROLES = frozenset({
    "decorative", "background", "background_shape",
    "connector", "divider", "accent_decoration",
})


# =====================================================================
# PPTXMapper クラス
# =====================================================================
class PPTXMapper:
    """PPTXExtractor の出力からマッピング YAML を生成するクラス。"""

    def __init__(self, extracted_data: dict):
        """
        Args:
            extracted_data: PPTXExtractor.extract_all() の出力辞書。
                期待する構造:
                    {
                        "source": "file.pptx",
                        "slide_width": int,
                        "slide_height": int,
                        "slides": [
                            {
                                "slide_number": int,
                                "layout": str,
                                "elements": [ ... ]
                            },
                            ...
                        ]
                    }
        """
        self._data = extracted_data
        self._client = None  # 遅延初期化
        self._gemini_available: Optional[bool] = None

    # ── Gemini クライアント ─────────────────────────────────────
    def _ensure_client(self) -> bool:
        """Gemini クライアントを初期化し、利用可否を返す。"""
        if self._gemini_available is not None:
            return self._gemini_available
        try:
            self._client = get_client()
            self._gemini_available = self._client is not None
        except Exception:
            self._client = None
            self._gemini_available = False
        return self._gemini_available

    # ================================================================
    # パブリック API
    # ================================================================
    def generate_mapping(self) -> dict:
        """全スライドのマッピング情報を生成して返す。

        Returns:
            マッピング辞書（YAML 出力用）。
        """
        source = self._data.get("source", "unknown.pptx")
        slide_width = self._data.get("slide_width", 0)
        slide_height = self._data.get("slide_height", 0)

        slides_mapping: List[dict] = []
        all_placeholders: List[dict] = []
        warnings: List[dict] = []

        for slide_data in self._data.get("slides", []):
            slide_num = slide_data.get("slide_number", 0)
            layout = slide_data.get("layout", "")
            elements = slide_data.get("elements", [])

            # セマンティック解析（Gemini or ヒューリスティック）
            analyzed = self.analyze_semantics(elements, slide_num)

            # プレースホルダー生成
            with_placeholders = self.generate_placeholders(analyzed, slide_num)

            # スライドマッピング組み立て
            slide_elements: List[dict] = []
            for elem in with_placeholders:
                entry = self._build_element_entry(elem)
                slide_elements.append(entry)

                # プレースホルダー集約
                if entry.get("placeholder"):
                    all_placeholders.append({
                        "key": entry["placeholder"],
                        "type": entry["type"],
                        "role": entry.get("role", ""),
                        "current": _extract_current_value(entry),
                    })

                # 警告の収集
                warn = self._check_warnings(elem, slide_num)
                if warn:
                    warnings.append(warn)

            slides_mapping.append({
                "slide_number": slide_num,
                "layout": layout,
                "elements": slide_elements,
            })

        mapping: dict = {
            "source": source,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "slide_width": slide_width,
            "slide_height": slide_height,
            "slides": slides_mapping,
            "placeholders": all_placeholders,
        }
        if warnings:
            mapping["warnings"] = warnings
        return mapping

    # ── セマンティック解析 ──────────────────────────────────────
    def analyze_semantics(
        self, slide_elements: list, slide_number: int
    ) -> list:
        """各要素にセマンティック role と hint を付与する。

        Gemini Flash が利用可能なら LLM 解析、不可ならヒューリスティック。

        Args:
            slide_elements: 1スライド分の要素リスト。
            slide_number: スライド番号。

        Returns:
            role / hint が追加された要素リスト（元リストのコピー）。
        """
        if not slide_elements:
            return []

        elements = [_deep_copy_element(e) for e in slide_elements]

        if self._ensure_client():
            try:
                return self._analyze_with_gemini(elements, slide_number)
            except Exception as exc:
                # Gemini 失敗時はフォールバック
                print(f"[mapper] Gemini 解析失敗 (slide {slide_number}): {exc}")

        # フォールバック: ヒューリスティック
        return self._analyze_heuristic(elements, slide_number)

    # ── プレースホルダー生成 ─────────────────────────────────────
    def generate_placeholders(
        self, elements: list, slide_number: int
    ) -> list:
        """各要素にプレースホルダーキーを付与する。

        命名規則:
            - テキスト: {{slide_{N}_{role}}}
            - チャート: {{slide_{N}_chart}} (複数なら _1, _2 ...)
            - テーブル: {{slide_{N}_table}} (同上)
            - 画像: {{slide_{N}_image}} (同上)
            - シェイプ(テキスト付き): {{slide_{N}_{role}}}
            - グループ子要素: {{group_{group_id}_{child_role}}} / {{flow_step_{idx}}}
            - SmartArt: {{smartart_{id}_node_{idx}}}
            - デコレーション/コネクタ: 付与しない

        Args:
            elements: analyze_semantics() の出力。
            slide_number: スライド番号。

        Returns:
            placeholder キーが追加された要素リスト。
        """
        # タイプ別カウンタ（重複時に連番を付けるため）
        type_counters: Dict[str, int] = {}
        # ロール別カウンタ（同一ロール重複検出用）
        role_counters: Dict[str, int] = {}

        result = []
        for elem in elements:
            elem = _deep_copy_element(elem)
            etype = elem.get("type", "")
            role = elem.get("role", "")
            elem_id = elem.get("id", "")

            # デコレーション系はスキップ
            if role in _DECORATIVE_ROLES:
                elem["placeholder"] = None
                result.append(elem)
                continue

            placeholder = self._compute_placeholder(
                elem, slide_number, type_counters, role_counters,
            )
            elem["placeholder"] = placeholder

            # グループ内子要素にもプレースホルダーを付与
            if etype == "group" and "children" in elem:
                elem["children"] = self._assign_group_child_placeholders(
                    elem["children"], elem_id, slide_number,
                )

            # SmartArt テキストノード
            if etype == "smartart" and "text_nodes" in elem:
                elem["text_nodes"] = self._assign_smartart_placeholders(
                    elem["text_nodes"], elem_id,
                )

            result.append(elem)
        return result

    # ── YAML 保存 ───────────────────────────────────────────────
    def save_yaml(self, mapping: dict, output_path: str) -> None:
        """マッピング辞書を YAML ファイルとして保存する。

        Args:
            mapping: generate_mapping() の返り値。
            output_path: 出力ファイルパス。
        """
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            yaml.dump(
                mapping,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                width=120,
            )
        print(f"[mapper] YAML マッピングを保存しました: {out.resolve()}")

    # ── アセット保存 ────────────────────────────────────────────
    def save_assets(self, extracted_data: dict, assets_dir: str) -> None:
        """抽出済み画像ファイルを assets_dir へコピー/保存する。

        extracted_data 内の各画像要素が持つ image_info.extracted_path
        を参照して、指定ディレクトリへ保存する。

        Args:
            extracted_data: PPTXExtractor.extract_all() の出力。
            assets_dir: 保存先ディレクトリパス。
        """
        dest = Path(assets_dir)
        dest.mkdir(parents=True, exist_ok=True)

        saved_count = 0
        for slide in extracted_data.get("slides", []):
            for elem in slide.get("elements", []):
                if elem.get("type") != "image":
                    continue
                img_info = elem.get("image_info", {})
                src_path = img_info.get("extracted_path", "")
                if not src_path:
                    continue
                src = Path(src_path)
                if not src.exists():
                    # バイトデータが直接格納されている場合
                    raw = img_info.get("data")
                    if raw and isinstance(raw, (bytes, bytearray)):
                        ext = _guess_extension(img_info.get("content_type", ""))
                        slide_num = slide.get("slide_number", 0)
                        fname = f"slide{slide_num}_pic{saved_count + 1}{ext}"
                        (dest / fname).write_bytes(raw)
                        saved_count += 1
                    continue
                dst = dest / src.name
                shutil.copy2(str(src), str(dst))
                saved_count += 1

        print(f"[mapper] {saved_count} 件のアセットを {dest.resolve()} に保存しました")

    # ================================================================
    # 内部メソッド: Gemini 解析
    # ================================================================
    def _analyze_with_gemini(
        self, elements: list, slide_number: int
    ) -> list:
        """Gemini Flash を使ってセマンティック解析を実行する。"""
        prompt = self._build_gemini_prompt(elements, slide_number)
        response = self._client.models.generate_content(
            model=get_flash_model(),
            contents=[prompt],
        )

        # レスポンスから JSON を抽出
        raw_text = response.text if hasattr(response, "text") else str(response)
        parsed = _extract_json_from_response(raw_text)

        if not parsed or not isinstance(parsed, list):
            raise ValueError("Gemini から有効な JSON 配列を取得できませんでした")

        # 解析結果を要素に反映
        result_map: Dict[str, dict] = {}
        for item in parsed:
            eid = str(item.get("id", ""))
            if eid:
                result_map[eid] = item

        for elem in elements:
            eid = str(elem.get("id", ""))
            if eid in result_map:
                elem["role"] = result_map[eid].get("role", elem.get("role", ""))
                elem["hint"] = result_map[eid].get("hint", "")
            else:
                # Gemini が返さなかった要素にはヒューリスティック適用
                self._apply_heuristic_single(elem, slide_number)

        return elements

    def _build_gemini_prompt(
        self, elements: list, slide_number: int
    ) -> str:
        """Gemini に送信するプロンプトを構築する。"""
        # 要素サマリーを作成（必要最小限の情報のみ送る）
        summaries = []
        for elem in elements:
            summary: Dict[str, Any] = {
                "id": elem.get("id", ""),
                "type": elem.get("type", ""),
            }
            # 位置情報
            pos = elem.get("position")
            if pos:
                summary["position"] = pos
            # テキストプレビュー（先頭80文字）
            text = elem.get("text", "") or elem.get("value", "")
            if isinstance(text, str) and text:
                summary["text_preview"] = text[:80]
            # チャートタイプ
            if elem.get("chart_type"):
                summary["chart_type"] = elem["chart_type"]
            # テーブル行数・列数
            if elem.get("type") == "table":
                rows = elem.get("rows", [])
                if rows:
                    summary["table_rows"] = len(rows)
                    summary["table_cols"] = len(rows[0]) if rows else 0
            # スタイル情報
            style = elem.get("style", {})
            if style:
                if style.get("size"):
                    summary["font_size"] = style["size"]
                if style.get("bold"):
                    summary["bold"] = True
            # 名前
            name = elem.get("name", "")
            if name:
                summary["name"] = name
            summaries.append(summary)

        elements_json = json.dumps(summaries, ensure_ascii=False, indent=2)

        # 利用可能なロール一覧を整形
        roles_desc = ""
        for category, roles in ROLE_CATEGORIES.items():
            roles_desc += f"  {category}: {', '.join(roles)}\n"

        prompt = (
            f"あなたはPowerPointスライドの要素を分析するエキスパートです。\n\n"
            f"以下はスライド {slide_number} の要素一覧です。各要素に対して:\n"
            f"1. `role` - セマンティックロール（以下のカテゴリから最も適切なものを選択）\n"
            f"2. `hint` - 日本語での置換ヒント（AIが内容を差し替える際の制約・ガイダンス）\n\n"
            f"を JSON 配列で返してください。\n\n"
            f"利用可能なロール:\n{roles_desc}\n"
            f"要素一覧:\n{elements_json}\n\n"
            f"回答は以下の形式の JSON 配列のみで返してください（説明文は不要）:\n"
            f"```json\n"
            f'[{{"id": "要素ID", "role": "ロール名", "hint": "日本語のヒント"}}, ...]\n'
            f"```\n\n"
            f"ヒントの例:\n"
            f'- title: "メインタイトル。15-25文字。"\n'
            f'- subtitle: "サブタイトル。簡潔に1行で。"\n'
            f'- body: "本文テキスト。箇条書き3-5項目を維持。"\n'
            f'- chart: "四半期推移。カテゴリ4つ、シリーズ2つを維持。"\n'
            f'- table: "比較表。行数・列数を維持。"\n'
            f'- image: "メインビジュアル。16:9推奨。"\n'
            f'- callout: "強調テキスト。20文字以内。"\n'
            f'- footnote: "注釈。1行で簡潔に。"\n'
        )
        return prompt

    # ================================================================
    # 内部メソッド: ヒューリスティック解析（フォールバック）
    # ================================================================
    def _analyze_heuristic(
        self, elements: list, slide_number: int
    ) -> list:
        """Gemini 不使用時のヒューリスティックロール判定。"""
        for elem in elements:
            self._apply_heuristic_single(elem, slide_number)
        return elements

    def _apply_heuristic_single(self, elem: dict, slide_number: int) -> None:
        """単一要素にヒューリスティックで role / hint を付与する。"""
        etype = elem.get("type", "")
        name = (elem.get("name", "") or "").lower()
        text = elem.get("text", "") or elem.get("value", "")
        if isinstance(text, dict):
            text = ""
        style = elem.get("style", {}) or {}
        font_size = style.get("size", 0) or 0
        bold = style.get("bold", False)

        role = ""
        hint = ""

        # ── テキスト要素 ─────────────────────────────────────
        if etype == "text":
            role, hint = self._heuristic_text_role(
                name, str(text), font_size, bold, slide_number,
            )

        # ── チャート要素 ──────────────────────────────────────
        elif etype == "chart":
            chart_type = elem.get("chart_type", "")
            role, hint = self._heuristic_chart_role(chart_type, elem)

        # ── テーブル要素 ──────────────────────────────────────
        elif etype == "table":
            role, hint = self._heuristic_table_role(elem)

        # ── 画像要素 ──────────────────────────────────────────
        elif etype == "image":
            role, hint = self._heuristic_image_role(name, elem)

        # ── シェイプ要素 ──────────────────────────────────────
        elif etype == "shape":
            role, hint = self._heuristic_shape_role(name, str(text))

        # ── グループ要素 ──────────────────────────────────────
        elif etype == "group":
            role, hint = self._heuristic_group_role(elem)

        # ── SmartArt 要素 ─────────────────────────────────────
        elif etype == "smartart":
            role, hint = self._heuristic_smartart_role(elem)

        # ── 不明 ─────────────────────────────────────────────
        else:
            role = etype or "unknown"
            hint = "要素タイプ不明。手動で確認してください。"

        elem["role"] = role
        elem["hint"] = hint

    # ── テキストのヒューリスティック ──────────────────────────
    def _heuristic_text_role(
        self, name: str, text: str, font_size: int, bold: bool,
        slide_number: int,
    ) -> Tuple[str, str]:
        """テキスト要素のロール・ヒントをヒューリスティックで判定。"""
        # 名前ベース判定
        if "title" in name:
            return "title", "メインタイトル。15-25文字。"
        if "subtitle" in name:
            return "subtitle", "サブタイトル。簡潔に1行で。"
        if "footer" in name or "footnote" in name:
            return "footnote", "注釈・脚注。1行で簡潔に。"
        if "page" in name and "number" in name:
            return "page_number", "ページ番号。自動更新。"
        if "caption" in name:
            return "caption", "キャプション。図表の説明を簡潔に。"

        # ページ番号パターン（数字のみ、短い）
        if text.strip().isdigit() and len(text.strip()) <= 3:
            return "page_number", "ページ番号。"

        # フォントサイズベース判定
        if font_size >= 28:
            return "title", f"タイトル。{max(10, 40 - font_size)}〜{40 - font_size + 15}文字程度。"
        if font_size >= 20 and bold:
            return "heading", "見出し。簡潔に。"
        if font_size >= 18:
            return "subtitle", "サブタイトルまたは見出し。簡潔に1行で。"

        # 箇条書き判定（改行 + 記号）
        bullet_chars = ["・", "●", "•", "-", "※"]
        if text and ("\n" in text or any(text.lstrip().startswith(c) for c in bullet_chars)):
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            return "bullet_list", f"箇条書き。{len(lines)}項目を維持。"

        # ラベル（短いテキスト）
        if text and len(text.strip()) <= 10:
            return "label", "ラベル。短いテキスト。"

        # デフォルト: body
        return "body", "本文テキスト。内容を適切に置換。"

    # ── チャートのヒューリスティック ──────────────────────────
    def _heuristic_chart_role(
        self, chart_type: str, elem: dict
    ) -> Tuple[str, str]:
        """チャート要素のロール・ヒントをヒューリスティックで判定。"""
        ct = (chart_type or "").upper()
        value = elem.get("value", {})

        # カテゴリ数・シリーズ数を抽出
        cats = value.get("categories", []) if isinstance(value, dict) else []
        series = value.get("series", []) if isinstance(value, dict) else []
        cat_count = len(cats)
        series_count = len(series)

        constraint = ""
        if cat_count > 0 or series_count > 0:
            constraint = f"カテゴリ{cat_count}つ、シリーズ{series_count}つを維持。"

        if "PIE" in ct or "DOUGHNUT" in ct:
            return "distribution_chart", f"構成比チャート。{constraint}"
        if "LINE" in ct:
            return "trend_chart", f"推移チャート。{constraint}"
        if "BAR" in ct:
            return "comparison_chart", f"比較チャート（横棒）。{constraint}"
        if "COLUMN" in ct:
            return "revenue_chart", f"棒グラフ。{constraint}"
        if "AREA" in ct:
            return "trend_chart", f"面グラフ推移。{constraint}"
        if "RADAR" in ct:
            return "comparison_chart", f"レーダーチャート。{constraint}"

        if constraint:
            return "trend_chart", f"チャート。{constraint}"
        return "trend_chart", "チャート。データ構造を維持。"

    # ── テーブルのヒューリスティック ──────────────────────────
    def _heuristic_table_role(self, elem: dict) -> Tuple[str, str]:
        """テーブル要素のロール・ヒント。"""
        rows = elem.get("rows", elem.get("value", []))
        if isinstance(rows, list):
            row_count = len(rows)
            col_count = len(rows[0]) if rows else 0
        else:
            row_count = 0
            col_count = 0
        return "data_table", f"データテーブル。{row_count}行x{col_count}列を維持。"

    # ── 画像のヒューリスティック ──────────────────────────────
    def _heuristic_image_role(
        self, name: str, elem: dict
    ) -> Tuple[str, str]:
        """画像要素のロール・ヒント。"""
        if "logo" in name:
            return "logo", "ロゴ画像。差し替え時はアスペクト比を維持。"
        if "icon" in name:
            return "icon", "アイコン。正方形推奨。"
        if "background" in name or "bg" in name:
            return "background", "背景画像。"

        # サイズで判定
        pos = elem.get("position", {})
        width = pos.get("width", 0)
        height = pos.get("height", 0)

        # 小さい画像はアイコン/ロゴと推定
        if width > 0 and height > 0:
            if width < 500000 and height < 500000:
                return "icon", "小さな画像。アイコンまたはロゴ。"
            if width > 8000000:
                return "hero_image", "メインビジュアル。16:9推奨。"

        return "photo", "写真画像。適切なサイズで差し替え。"

    # ── シェイプのヒューリスティック ──────────────────────────
    def _heuristic_shape_role(
        self, name: str, text: str
    ) -> Tuple[str, str]:
        """シェイプ要素のロール・ヒント。"""
        if "callout" in name:
            return "callout", "吹き出し・強調テキスト。20文字以内。"
        if "arrow" in name or "connector" in name:
            return "connector", ""
        if "line" in name or "divider" in name:
            return "divider", ""

        # テキストがある場合
        if text and text.strip():
            if len(text.strip()) <= 15:
                return "label", "ラベル。短いテキスト。"
            return "callout", f"シェイプ内テキスト。{len(text.strip())}文字程度。"

        # テキストなしの図形
        return "accent_decoration", ""

    # ── グループのヒューリスティック ──────────────────────────
    def _heuristic_group_role(self, elem: dict) -> Tuple[str, str]:
        """グループ要素のロール・ヒント。"""
        children = elem.get("children", [])
        child_count = len(children)
        name = (elem.get("name", "") or "").lower()

        if "flow" in name or "process" in name:
            return "process_flow", f"プロセスフロー。{child_count}ステップ。"
        if "timeline" in name:
            return "timeline", f"タイムライン。{child_count}項目。"
        if "card" in name:
            return "feature_cards", f"カード群。{child_count}枚。"
        if "org" in name:
            return "org_chart", f"組織図。{child_count}要素。"

        return "step_diagram", f"グループ要素。子要素{child_count}個。"

    # ── SmartArt のヒューリスティック ─────────────────────────
    def _heuristic_smartart_role(self, elem: dict) -> Tuple[str, str]:
        """SmartArt 要素のロール・ヒント。"""
        name = (elem.get("name", "") or "").lower()
        text_nodes = elem.get("text_nodes", [])
        node_count = len(text_nodes)

        if "org" in name or "hierarchy" in name:
            return "organization_chart", f"組織図SmartArt。ノード{node_count}個。テキストのみ差し替え可能。"
        if "process" in name or "flow" in name:
            return "process_diagram", f"プロセス図SmartArt。ノード{node_count}個。テキストのみ差し替え可能。"
        if "cycle" in name:
            return "cycle_diagram", f"サイクル図SmartArt。ノード{node_count}個。テキストのみ差し替え可能。"
        if "matrix" in name:
            return "matrix", f"マトリクスSmartArt。ノード{node_count}個。テキストのみ差し替え可能。"

        return "process_diagram", f"SmartArt。ノード{node_count}個。テキストのみ差し替え可能。"

    # ================================================================
    # 内部メソッド: プレースホルダー生成
    # ================================================================
    def _compute_placeholder(
        self,
        elem: dict,
        slide_number: int,
        type_counters: Dict[str, int],
        role_counters: Dict[str, int],
    ) -> Optional[str]:
        """要素のプレースホルダーキーを計算する。"""
        etype = elem.get("type", "")
        role = elem.get("role", "")

        # デコレーション系はプレースホルダーなし
        if role in _DECORATIVE_ROLES:
            return None

        # タイプ別の処理
        if etype in ("chart", "table", "image"):
            return self._indexed_placeholder(
                slide_number, etype, type_counters,
            )

        if etype == "text":
            return self._role_placeholder(
                slide_number, role, role_counters,
            )

        if etype == "shape":
            # テキスト付きシェイプのみ
            text = elem.get("text", "") or elem.get("value", "")
            if isinstance(text, str) and text.strip():
                return self._role_placeholder(
                    slide_number, role, role_counters,
                )
            return None

        if etype == "group":
            return self._role_placeholder(
                slide_number, role, role_counters,
            )

        if etype == "smartart":
            return self._role_placeholder(
                slide_number, role, role_counters,
            )

        # その他
        return self._role_placeholder(
            slide_number, role or etype, role_counters,
        )

    def _indexed_placeholder(
        self, slide_number: int, etype: str, counters: Dict[str, int]
    ) -> str:
        """chart/table/image 用の連番付きプレースホルダー。"""
        key = f"slide_{slide_number}_{etype}"
        count = counters.get(key, 0)
        counters[key] = count + 1
        if count == 0:
            return "{{" + f"slide_{slide_number}_{etype}" + "}}"
        return "{{" + f"slide_{slide_number}_{etype}_{count + 1}" + "}}"

    def _role_placeholder(
        self, slide_number: int, role: str, counters: Dict[str, int]
    ) -> str:
        """ロールベースのプレースホルダー（重複時に連番付与）。"""
        if not role:
            role = "element"
        key = f"slide_{slide_number}_{role}"
        count = counters.get(key, 0)
        counters[key] = count + 1
        if count == 0:
            return "{{" + f"slide_{slide_number}_{role}" + "}}"
        return "{{" + f"slide_{slide_number}_{role}_{count + 1}" + "}}"

    def _assign_group_child_placeholders(
        self, children: list, group_id: Any, slide_number: int
    ) -> list:
        """グループの子要素にプレースホルダーを付与する。"""
        result = []
        for idx, child in enumerate(children):
            child = _deep_copy_element(child)
            child_role = child.get("role", "step")
            text = child.get("text", "") or child.get("value", "")

            # テキストを持つ子要素のみ
            if isinstance(text, str) and text.strip():
                child["placeholder"] = "{{" + f"group_{group_id}_{child_role}_{idx + 1}" + "}}"
            else:
                child["placeholder"] = None
            result.append(child)
        return result

    def _assign_smartart_placeholders(
        self, text_nodes: list, smartart_id: Any
    ) -> list:
        """SmartArt テキストノードにプレースホルダーを付与する。"""
        result = []
        for idx, node in enumerate(text_nodes):
            node = _deep_copy_element(node) if isinstance(node, dict) else {"text": str(node)}
            node["placeholder"] = "{{" + f"smartart_{smartart_id}_node_{idx + 1}" + "}}"
            result.append(node)
        return result

    # ================================================================
    # 内部メソッド: マッピングエントリ構築
    # ================================================================
    def _build_element_entry(self, elem: dict) -> dict:
        """1要素分のマッピングエントリを構築する。"""
        entry: dict = {}
        etype = elem.get("type", "")

        # 基本フィールド
        entry["id"] = elem.get("id", "")
        if elem.get("name"):
            entry["name"] = elem["name"]
        entry["type"] = etype
        entry["role"] = elem.get("role", "")
        entry["hint"] = elem.get("hint", "")

        # 位置情報
        if elem.get("position"):
            entry["position"] = elem["position"]

        # スタイル情報（テキスト）
        if etype == "text" and elem.get("style"):
            entry["style"] = elem["style"]

        # 値（テキスト / チャート / テーブル）
        if etype == "text":
            text = elem.get("text", "") or elem.get("value", "")
            entry["value"] = text if isinstance(text, str) else str(text)
        elif etype == "chart":
            entry["chart_type"] = elem.get("chart_type", "")
            if elem.get("chart_config"):
                entry["chart_config"] = elem["chart_config"]
            entry["value"] = elem.get("value", {})
        elif etype == "table":
            entry["value"] = elem.get("value", elem.get("rows", []))
        elif etype == "image":
            entry["image_info"] = elem.get("image_info", {})
            entry["replace_mode"] = elem.get("replace_mode", "keep")
        elif etype == "shape":
            text = elem.get("text", "") or elem.get("value", "")
            if isinstance(text, str) and text.strip():
                entry["value"] = text

        # グループ子要素
        if etype == "group" and "children" in elem:
            entry["children"] = elem["children"]

        # SmartArt テキストノード
        if etype == "smartart" and "text_nodes" in elem:
            entry["text_nodes"] = elem["text_nodes"]

        # プレースホルダー
        entry["placeholder"] = elem.get("placeholder")

        return entry

    # ── 警告チェック ────────────────────────────────────────────
    def _check_warnings(self, elem: dict, slide_number: int) -> Optional[dict]:
        """要素に関する警告を生成する（必要な場合のみ）。"""
        etype = elem.get("type", "")
        name = elem.get("name", "")

        if etype == "smartart":
            return {
                "slide": slide_number,
                "element": name or f"SmartArt_{elem.get('id', '')}",
                "type": "smartart",
                "message": "SmartArtのテキストノードのみ差し替え可能。レイアウト変更は不可。",
            }

        if etype == "group":
            children = elem.get("children", [])
            if len(children) > 10:
                return {
                    "slide": slide_number,
                    "element": name or f"Group_{elem.get('id', '')}",
                    "type": "group",
                    "message": f"グループ内の子要素が{len(children)}個あります。個別の差し替えを確認してください。",
                }

        if etype == "chart":
            chart_type = (elem.get("chart_type", "") or "").upper()
            if "3D" in chart_type:
                return {
                    "slide": slide_number,
                    "element": name or f"Chart_{elem.get('id', '')}",
                    "type": "chart",
                    "message": "3Dチャートのデータ差し替えは視覚的な崩れが起きる場合があります。",
                }

        return None


# =====================================================================
# ユーティリティ関数
# =====================================================================
def _deep_copy_element(elem: dict) -> dict:
    """要素辞書のシャローコピー（子リストは新リスト参照にする）。"""
    copied = dict(elem)
    if "children" in copied and isinstance(copied["children"], list):
        copied["children"] = [dict(c) if isinstance(c, dict) else c for c in copied["children"]]
    if "text_nodes" in copied and isinstance(copied["text_nodes"], list):
        copied["text_nodes"] = [dict(n) if isinstance(n, dict) else n for n in copied["text_nodes"]]
    return copied


def _extract_json_from_response(text: str) -> Optional[list]:
    """Gemini レスポンスから JSON 配列を抽出する。

    ```json ... ``` ブロックや生のJSON配列に対応。
    """
    if not text:
        return None

    # ```json ... ``` ブロックを探す
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    json_str = match.group(1).strip() if match else text.strip()

    # JSON 配列部分を抽出（先頭の [ を探す）
    bracket_match = re.search(r"\[.*\]", json_str, re.DOTALL)
    if bracket_match:
        json_str = bracket_match.group(0)

    try:
        parsed = json.loads(json_str)
        return parsed if isinstance(parsed, list) else None
    except json.JSONDecodeError:
        return None


def _extract_current_value(entry: dict) -> str:
    """マッピングエントリから現在値を文字列で取得する。"""
    etype = entry.get("type", "")
    value = entry.get("value", "")

    if etype == "text" or etype == "shape":
        return str(value)[:100] if value else ""

    if etype == "chart":
        if isinstance(value, dict):
            cats = value.get("categories", [])
            return f"chart({len(cats)} categories)"
        return "chart"

    if etype == "table":
        if isinstance(value, list):
            return f"table({len(value)} rows)"
        return "table"

    if etype == "image":
        img_info = entry.get("image_info", {})
        return img_info.get("extracted_path", "image")

    return str(value)[:100] if value else ""


def _guess_extension(content_type: str) -> str:
    """MIMEタイプからファイル拡張子を推定する。"""
    ext_map = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/gif": ".gif",
        "image/svg+xml": ".svg",
        "image/bmp": ".bmp",
        "image/tiff": ".tiff",
        "image/webp": ".webp",
        "image/emf": ".emf",
        "image/wmf": ".wmf",
    }
    return ext_map.get(content_type, ".png")


# =====================================================================
# CLI エントリーポイント（単体テスト・デバッグ用）
# =====================================================================
def main():
    """コマンドライン実行用エントリーポイント。

    使い方:
        python mapper.py --input extracted.json --output mapping.yaml [--assets-dir extracted_assets]
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="PPTX マッピング YAML 生成ツール",
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="PPTXExtractor の出力 JSON ファイルパス",
    )
    parser.add_argument(
        "--output", "-o", default="mapping.yaml",
        help="出力 YAML ファイルパス (デフォルト: mapping.yaml)",
    )
    parser.add_argument(
        "--assets-dir",
        help="画像アセットの保存先ディレクトリ",
    )
    parser.add_argument(
        "--no-gemini", action="store_true",
        help="Gemini 解析を無効にし、ヒューリスティックのみ使用",
    )
    args = parser.parse_args()

    # 入力 JSON 読み込み
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[mapper] エラー: 入力ファイルが見つかりません: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        extracted_data = json.load(f)

    print(f"[mapper] 入力ファイル読み込み完了: {input_path}")
    slide_count = len(extracted_data.get("slides", []))
    print(f"[mapper] スライド数: {slide_count}")

    # マッパー初期化
    mapper = PPTXMapper(extracted_data)

    # Gemini 無効化
    if args.no_gemini:
        mapper._gemini_available = False
        mapper._client = None
        print("[mapper] Gemini 解析を無効にしました（ヒューリスティックモード）")

    # マッピング生成
    mapping = mapper.generate_mapping()

    # YAML 保存
    mapper.save_yaml(mapping, args.output)

    # アセット保存
    if args.assets_dir:
        mapper.save_assets(extracted_data, args.assets_dir)

    # サマリー表示
    total_elements = sum(len(s.get("elements", [])) for s in mapping.get("slides", []))
    total_placeholders = len(mapping.get("placeholders", []))
    total_warnings = len(mapping.get("warnings", []))

    print(f"\n[mapper] === マッピング生成完了 ===")
    print(f"[mapper]   スライド数: {len(mapping.get('slides', []))}")
    print(f"[mapper]   要素数: {total_elements}")
    print(f"[mapper]   プレースホルダー数: {total_placeholders}")
    if total_warnings:
        print(f"[mapper]   警告数: {total_warnings}")
    print(f"[mapper]   出力: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()

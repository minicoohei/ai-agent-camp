#!/usr/bin/env python3
"""
HTML Parser - HTMLから講義コンテンツを抽出

課程のHTMLファイルからセクション、キーポイント、図解などを抽出し、
構造化されたデータとして出力する。
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup


@dataclass
class ContentSection:
    """講義セクション"""
    title: str
    content_type: str  # "title", "concept", "example", "diagram", "quiz", "summary"
    text_content: str
    bullet_points: List[str] = field(default_factory=list)
    code_blocks: List[str] = field(default_factory=list)
    plantuml_url: Optional[str] = None
    diagram_title: Optional[str] = None
    duration_estimate: int = 30  # 秒単位の推定時間


@dataclass
class LectureContent:
    """講義コンテンツ全体"""
    title: str
    module_id: str
    sections: List[ContentSection] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    summary_points: List[str] = field(default_factory=list)
    total_duration: int = 0  # 秒


def parse_html(html_path: str) -> LectureContent:
    """
    HTMLファイルから講義コンテンツを抽出する
    
    Args:
        html_path: HTMLファイルのパス
        
    Returns:
        LectureContent: 抽出された講義コンテンツ
    """
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    
    # タイトルを取得
    title_elem = soup.find("h1")
    title = title_elem.get_text(strip=True) if title_elem else "無題"
    
    # モジュールIDを推測
    module_id = Path(html_path).stem
    
    lecture = LectureContent(title=title, module_id=module_id)
    
    # 学習目標を抽出（key-point クラスの最初のもの）
    key_points = soup.find_all(class_="key-point")
    if key_points:
        first_key_point = key_points[0]
        objectives = first_key_point.find_all("li")
        lecture.learning_objectives = [li.get_text(strip=True) for li in objectives]
    
    # 各カード（セクション）を抽出
    cards = soup.find_all("section", class_="card")
    
    for card in cards:
        section = _parse_card(card)
        if section:
            lecture.sections.append(section)
    
    # まとめセクションを抽出
    summary_card = soup.find("section", class_=lambda x: x and "border-primary" in x)
    if summary_card:
        summary_items = summary_card.find_all("li")
        lecture.summary_points = [li.get_text(strip=True) for li in summary_items]
    
    # 合計時間を計算
    lecture.total_duration = sum(s.duration_estimate for s in lecture.sections)
    
    return lecture


def _parse_card(card) -> Optional[ContentSection]:
    """カードセクションをパースする"""
    # ヘッダーからタイトルを取得
    header = card.find(class_="card-header")
    if not header:
        return None
    
    title = header.get_text(strip=True)
    
    # コンテンツタイプを判定
    content_type = _detect_content_type(card, title)
    
    # 本文テキストを取得
    body = card.find(class_="card-body")
    if not body:
        return None
    
    # 段落テキストを取得
    paragraphs = body.find_all("p", recursive=False)
    text_content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    
    # 箇条書きを取得
    bullet_points = []
    for ul in body.find_all("ul"):
        for li in ul.find_all("li", recursive=False):
            bullet_points.append(li.get_text(strip=True))
    
    # コードブロックを取得
    code_blocks = []
    for code in body.find_all("code"):
        code_text = code.get_text(strip=True)
        if code_text and len(code_text) > 10:
            code_blocks.append(code_text)
    
    # PlantUMLを取得
    plantuml_url = None
    diagram_title = None
    plantuml_container = body.find(class_="plantuml-container")
    if plantuml_container:
        img = plantuml_container.find("img")
        if img and img.get("src"):
            plantuml_url = img.get("src")
        title_elem = plantuml_container.find(class_="diagram-title")
        if title_elem:
            diagram_title = title_elem.get_text(strip=True)
    
    # たとえ話（analogy-box）を取得
    analogy = body.find(class_="analogy-box")
    analogy_text = ""
    if analogy:
        analogy_text = analogy.get_text(strip=True)
    
    # 注意事項（common-mistake）を取得
    mistake = body.find(class_="common-mistake")
    mistake_text = ""
    if mistake:
        mistake_text = mistake.get_text(strip=True)
    
    # 全テキストを結合
    full_text = text_content
    if analogy_text:
        full_text += f"\n\n【たとえ話】\n{analogy_text}"
    if mistake_text:
        full_text += f"\n\n【注意事項】\n{mistake_text}"
    
    # 時間を推定
    duration = _estimate_duration(full_text, bullet_points, code_blocks, plantuml_url)
    
    return ContentSection(
        title=title,
        content_type=content_type,
        text_content=full_text,
        bullet_points=bullet_points,
        code_blocks=code_blocks,
        plantuml_url=plantuml_url,
        diagram_title=diagram_title,
        duration_estimate=duration,
    )


def _detect_content_type(card, title: str) -> str:
    """コンテンツタイプを判定"""
    title_lower = title.lower()
    
    if "まとめ" in title or "summary" in title_lower:
        return "summary"
    if "理解度チェック" in title or "quiz" in title_lower:
        return "quiz"
    if "例" in title or "example" in title_lower:
        return "example"
    if "ワークフロー" in title or "フロー" in title:
        return "diagram"
    
    # PlantUMLがある場合
    if card.find(class_="plantuml-container"):
        return "diagram"
    
    return "concept"


def _estimate_duration(text: str, bullets: List[str], codes: List[str], has_diagram: bool) -> int:
    """セクションの推定時間（秒）を計算"""
    # 基本時間: 10秒
    duration = 10
    
    # テキストの長さに基づく時間（100文字あたり15秒）
    text_length = len(text)
    duration += (text_length // 100) * 15
    
    # 箇条書き（1項目あたり5秒）
    duration += len(bullets) * 5
    
    # コードブロック（1ブロックあたり10秒）
    duration += len(codes) * 10
    
    # 図解（20秒追加）
    if has_diagram:
        duration += 20
    
    # 最小30秒、最大180秒
    return max(30, min(180, duration))


def content_to_dict(content: LectureContent) -> dict:
    """LectureContentを辞書に変換"""
    return {
        "title": content.title,
        "module_id": content.module_id,
        "learning_objectives": content.learning_objectives,
        "summary_points": content.summary_points,
        "total_duration": content.total_duration,
        "sections": [
            {
                "title": s.title,
                "content_type": s.content_type,
                "text_content": s.text_content,
                "bullet_points": s.bullet_points,
                "code_blocks": s.code_blocks,
                "plantuml_url": s.plantuml_url,
                "diagram_title": s.diagram_title,
                "duration_estimate": s.duration_estimate,
            }
            for s in content.sections
        ],
    }


if __name__ == "__main__":
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="HTMLから講義コンテンツを抽出")
    parser.add_argument("html_path", help="HTMLファイルのパス")
    parser.add_argument("--output", "-o", help="出力JSONファイルのパス")
    
    args = parser.parse_args()
    
    content = parse_html(args.html_path)
    result = content_to_dict(content)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 出力: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

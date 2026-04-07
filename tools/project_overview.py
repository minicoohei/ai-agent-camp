"""
Project Overview - プロジェクト構造可視化ツール

- 指定ディレクトリ配下の構造を走査し、概要をHTMLで出力します。
- Gemini APIキーがあれば、主要ファイル断片から「モジュール」「実装済み機能」「不足機能」等を要約します。
- PlantUML形式で構造図を生成し、PlantUML公式サーバー経由でSVG画像として表示します。
- ファイル一覧、関数一覧、簡単な説明を表示します。

NOTE:
- serena MCP を Python から直接呼び出すのは前提にしません（HTML内で“深掘り用プロンプト”として案内します）。
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import os
import re
import sys
import zlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# tools 配下の bootcamp_utils.py を import できるようにする
sys.path.insert(0, str(Path(__file__).parent))

from bootcamp_utils import (  # noqa: E402
    DEFAULT_OUTPUT_DIR,
    create_html_template,
    get_client,
    get_flash_model,
    save_html_file,
)

DEFAULT_OVERVIEW_DIR = DEFAULT_OUTPUT_DIR / "overview"

EXCLUDE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    ".cursor",
    ".specstory",
    ".serena",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".pytest_cache",
}


def walk_tree(root: Path, max_code_files: int = 4000) -> Tuple[Dict[str, Any], List[Path]]:
    structure: Dict[str, Any] = {}
    code_files: List[Path] = []
    count = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]

        try:
            rel_dir = str(Path(dirpath).relative_to(root))
        except ValueError:
            # root外のパスが含まれる場合のフォールバック
            rel_dir = str(Path(dirpath))
        
        rel_dir = "(root)" if rel_dir == "." else rel_dir

        keep_files = []
        for f in filenames:
            if f.startswith("."):
                continue
            if f.endswith(
                (
                    ".py",
                    ".ts",
                    ".tsx",
                    ".js",
                    ".jsx",
                    ".md",
                    ".yml",
                    ".yaml",
                    ".json",
                    ".toml",
                    ".txt",
                    ".html",
                    ".css",
                    ".puml",
                    ".pu",
                )
            ):
                keep_files.append(f)
        keep_files = sorted(keep_files)[:80]

        structure[rel_dir] = {"subdirs": sorted(dirnames)[:80], "files": keep_files}

        for f in filenames:
            if f.startswith("."):
                continue
            p = Path(dirpath) / f
            if p.suffix in {".py", ".ts", ".tsx", ".js", ".jsx"}:
                code_files.append(p)
                count += 1
                if count >= max_code_files:
                    return structure, code_files

    return structure, code_files


def collect_targets(root: Path, files: List[str]) -> Tuple[Dict[str, Any], List[Path]]:
    """
    ディレクトリ走査結果と指定ファイルを統合します。
    指定されたファイルは優先的にリストの先頭に配置されます。
    """
    structure, dir_files = walk_tree(root)

    if not files:
        return structure, dir_files

    priority_files: List[Path] = []
    for f in files:
        p = Path(f).resolve()
        if p.exists() and p.is_file():
            priority_files.append(p)
        else:
            print(f"⚠️ 指定されたファイルが見つかりません: {f}")

    # 重複排除しつつ、priority_files を先頭に
    seen = {f.resolve() for f in priority_files}
    final_files = priority_files + [f for f in dir_files if f.resolve() not in seen]

    return structure, final_files


def read_head(path: Path, limit_chars: int = 2500) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit_chars]
    except Exception:
        return ""


def read_text_limited(path: Path, limit_chars: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit_chars]
    except Exception:
        return ""


def find_html_files(root: Path, max_files: int = 300) -> List[Path]:
    htmls: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for f in filenames:
            if f.startswith("."):
                continue
            if f.lower().endswith(".html"):
                htmls.append(Path(dirpath) / f)
                if len(htmls) >= max_files:
                    return sorted(htmls)
    return sorted(htmls)


def extract_links(html: str) -> List[str]:
    # href / src をざっくり抽出（厳密なHTMLパースではない）
    # 例: href="assets/style.css" / src='./main.js'
    pat = re.compile(r"""(?:href|src)\s*=\s*["']([^"' >]+)["']""", re.IGNORECASE)
    return [m.group(1).strip() for m in pat.finditer(html) if m.group(1).strip()]


def normalize_link(link: str) -> str:
    # query / fragment を落としてパスだけにする
    link = link.split("#", 1)[0]
    link = link.split("?", 1)[0]
    return link.strip()


def is_external_link(link: str) -> bool:
    l = link.lower()
    return (
        l.startswith("http://")
        or l.startswith("https://")
        or l.startswith("mailto:")
        or l.startswith("tel:")
        or l.startswith("data:")
        or l.startswith("javascript:")
        or l.startswith("//")
    )


def check_links(root: Path, html_files: List[Path]) -> Tuple[List[Dict[str, str]], List[Tuple[str, str]]]:
    """
    Returns:
      issues: [{source, link, resolved, reason}]
      edges:  [(src_rel, dst_rel)] (HTML内リンクがroot配下のhtmlに解決できたもの)
    """
    root = root.resolve()
    html_set = {p.resolve() for p in html_files}
    issues: List[Dict[str, str]] = []
    edges: List[Tuple[str, str]] = []

    for src in html_files:
        content = read_text_limited(src)
        for raw in extract_links(content):
            link = normalize_link(raw)
            if not link or link == "/":
                continue
            if is_external_link(link) or link.startswith("#"):
                continue

            # 絶対パス風 "/assets/..." は root 起点として扱う（静的サイト想定）
            if link.startswith("/"):
                target = (root / link.lstrip("/")).resolve()
            else:
                target = (src.parent / link).resolve()

            exists = target.exists()
            if not exists and link.endswith("/"):
                # "dir/" なら dir/index.html も試す
                target2 = (target / "index.html").resolve()
                if target2.exists():
                    target = target2
                    exists = True

            if exists:
                if target.suffix.lower() == ".html" and target in html_set:
                    try:
                        edges.append(
                            (
                                str(src.relative_to(root)),
                                str(target.relative_to(root)),
                            )
                        )
                    except ValueError:
                        pass # root外の場合はスキップ
                continue

            try:
                src_rel = str(src.relative_to(root))
            except ValueError:
                src_rel = str(src)

            issues.append(
                {
                    "source": src_rel,
                    "link": raw,
                    "resolved": str(target),
                    "reason": "not found",
                }
            )

    # 重複を軽く除去
    uniq_edges = sorted(set(edges))
    uniq_issues_key = {(i["source"], i["link"], i["resolved"]): i for i in issues}
    uniq_issues = list(uniq_issues_key.values())
    uniq_issues.sort(key=lambda x: (x["source"], x["link"]))
    return uniq_issues, uniq_edges


def structure_to_text(structure: Dict[str, Any], max_dirs: int = 250) -> str:
    lines: List[str] = []
    for i, key in enumerate(sorted(structure.keys())):
        if i >= max_dirs:
            lines.append("... (省略)")
            break
        entry = structure.get(key) or {}
        subdirs = entry.get("subdirs") or []
        files = entry.get("files") or []
        lines.append(f"- {key}/")
        if subdirs:
            lines.append(f"  - subdirs: {', '.join(map(str, subdirs[:20]))}" + (" ..." if len(subdirs) > 20 else ""))
        if files:
            lines.append(f"  - files : {', '.join(map(str, files[:30]))}" + (" ..." if len(files) > 30 else ""))
    return "\n".join(lines)


def fallback_modules_from_pages(pages: List[Path], edges: List[Tuple[str, str]], root: Path) -> List[Dict[str, Any]]:
    # ざっくり「ページ（=モジュール）」として扱う
    deps_map: Dict[str, List[str]] = {}
    for src, dst in edges:
        deps_map.setdefault(src, []).append(dst)

    modules: List[Dict[str, Any]] = []
    for p in pages:
        try:
            rel = str(p.relative_to(root))
        except ValueError:
            rel = str(p)
        modules.append(
            {
                "name": rel,
                "path": rel,
                "purpose": "HTMLページ",
                "dependencies": sorted(set(deps_map.get(rel, [])))[:20],
                "features": ["ページ表示"],
            }
        )
    return modules


def gemini_analyze(client: Any, root: Path, structure: Dict[str, Any], code_files: List[Path]) -> Dict[str, Any]:
    if not client:
        return {"modules": [], "files_summary": [], "implemented_features": [], "missing_features": [], "recommendations": []}

    samples = []
    # 優先ファイル（code_filesの先頭）を含めて12ファイルまで
    for p in code_files[:12]:
        try:
            rel = p.relative_to(root)
        except ValueError:
            rel = p.name # root外の場合はファイル名のみ
        
        head = read_head(p)
        if head.strip():
            samples.append(f"## {rel}\n{head}\n")

    prompt = f"""
あなたはソフトウェア設計とドキュメント作成のエキスパートです。
以下のリポジトリ構造と主要ファイル断片を見て、プロジェクトの構造を要約してください。
特に、**階層的な機能分解（WBS）** ができるように、モジュールごとの機能を抽出してください。
また、各ファイルの概要と主要な関数/クラスを抽出してください。

制約:
- 推測は最小限。根拠のない断定はしない
- 初学者にも分かる言葉を優先

入力:
- root: {root.name}
- tree(抜粋):
{json.dumps(structure, ensure_ascii=False)[:6000]}

- code samples(抜粋):
{''.join(samples)[:9000]}

出力はJSONのみ:
{{
  "modules": [
    {{"name":"モジュール名","path":"パス","purpose":"役割","features":["機能1", "機能2", ...],"dependencies":["依存(推定可)"]}}
  ],
  "files_summary": [
    {{"path":"ファイルパス","description":"ファイルの説明（1-2文）","functions":["関数名1", "関数名2", ...]}}
  ],
  "implemented_features": ["実装済み機能（全体）"],
  "missing_features": ["不足/曖昧な点"],
  "recommendations": ["次にやると良いこと"]
}}
"""

    resp = client.models.generate_content(model=get_flash_model(), contents=[prompt])
    text = (resp.text or "").strip()
    
    def extract_json_blob(s: str) -> str:
        s = (s or "").strip()
        fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", s, re.IGNORECASE)
        if fence:
            return fence.group(1).strip()
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            return s[start : end + 1].strip()
        return s

    blob = extract_json_blob(text)
    try:
        return json.loads(blob)
    except Exception:
        return {
            "modules": [],
            "files_summary": [],
            "implemented_features": [],
            "missing_features": [],
            "recommendations": ["Geminiの出力がJSONとして解析できませんでした。"],
        }


def encode_plantuml(plantuml_text: str) -> str:
    """
    PlantUML公式サーバー用のURLエンコード文字列を生成します。
    ref: https://plantuml.com/text-encoding
    """

    def encode6bit(b: int) -> str:
        if b < 10:
            return chr(48 + b)
        b -= 10
        if b < 26:
            return chr(65 + b)
        b -= 26
        if b < 26:
            return chr(97 + b)
        b -= 26
        if b == 0:
            return "-"
        if b == 1:
            return "_"
        return "?"

    def append3bytes(b1: int, b2: int, b3: int) -> str:
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        return f"{encode6bit(c1)}{encode6bit(c2)}{encode6bit(c3)}{encode6bit(c4)}"

    data = plantuml_text.encode("utf-8")
    compressed = zlib.compress(data)[2:-4]  # raw DEFLATE
    res: List[str] = []
    i = 0
    while i < len(compressed):
        b1 = compressed[i]
        b2 = compressed[i + 1] if i + 1 < len(compressed) else 0
        b3 = compressed[i + 2] if i + 2 < len(compressed) else 0
        res.append(append3bytes(b1, b2, b3))
        i += 3
    return "".join(res)


def plantuml(modules: List[Dict[str, Any]]) -> str:
    # 横に長くなりすぎないよう、縦方向レイアウトを優先
    lines = ["@startuml", "", "top to bottom direction", ""]
    if not modules:
        lines += ["note as N", "  モジュール情報がありません。", "end note", "@enduml"]
        return "\n".join(lines)

    def node(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9_]", "_", name.strip() or "Unknown")

    for mod in modules:
        name = str(mod.get("name", "Unknown")).strip() or "Unknown"
        nid = node(name)
        purpose = str(mod.get("purpose", "")).replace("\n", " ")
        lines.append(f'package "{name}" as {nid} {{}}')
        if purpose:
            lines.append(f"note right of {nid} : {purpose[:60]}")
        lines.append("")

    name_to_node = {str(m.get("name", "Unknown")).strip(): node(str(m.get("name", "Unknown"))) for m in modules}
    for mod in modules:
        src_name = str(mod.get("name", "Unknown")).strip()
        src_node = name_to_node.get(src_name)
        for dep in (mod.get("dependencies") or []):
            dep_name = str(dep).strip()
            dep_node = name_to_node.get(dep_name)
            if src_node and dep_node and dep_node != src_node:
                lines.append(f"{dep_node} --> {src_node}")

    lines.append("@enduml")
    return "\n".join(lines)


def plantuml_wbs(modules: List[Dict[str, Any]], root_name: str) -> str:
    # WBSだと横に広がりすぎるため、MindMap形式（右方向展開）を採用して
    # 縦スクロールで見やすくする
    lines = ["@startmindmap", f"* {root_name}"]
    if not modules:
        lines.append("** モジュール情報なし")
        lines.append("@endmindmap")
        return "\n".join(lines)

    for mod in modules:
        name = mod.get("name", "Unknown")
        lines.append(f"** {name}")
        features = mod.get("features") or []
        for feat in features:
             # 見やすくするため、長すぎる機能名は省略
             feat_str = str(feat).replace("\n", " ")[:40]
             lines.append(f"*** {feat_str}")

    lines.append("@endmindmap")
    return "\n".join(lines)


def structure_to_plantuml_mindmap(structure: Dict[str, Any], root_name: str, max_depth: int = 6) -> str:
    """
    ディレクトリ構造から直接PlantUML MindMapを生成します。
    Geminiの要約に依存せず、実際のファイルシステム構造を反映します。
    
    Args:
        structure: walk_tree()で取得したディレクトリ構造
        root_name: ルートディレクトリ名
        max_depth: 最大深さ（デフォルト6）
    
    Returns:
        PlantUML MindMap形式の文字列
    """
    # ツリー構造を構築
    tree: Dict[str, Any] = {"_files": [], "_dirs": {}}
    
    for rel_dir, entry in structure.items():
        if rel_dir == "(root)":
            # ルート直下のファイル
            tree["_files"] = entry.get("files", [])
            for subdir in entry.get("subdirs", []):
                if subdir not in tree["_dirs"]:
                    tree["_dirs"][subdir] = {"_files": [], "_dirs": {}}
        else:
            # サブディレクトリのパスを分解
            parts = rel_dir.split("/") if "/" in rel_dir else [rel_dir]
            current = tree
            for part in parts:
                if part not in current["_dirs"]:
                    current["_dirs"][part] = {"_files": [], "_dirs": {}}
                current = current["_dirs"][part]
            current["_files"] = entry.get("files", [])
            for subdir in entry.get("subdirs", []):
                if subdir not in current["_dirs"]:
                    current["_dirs"][subdir] = {"_files": [], "_dirs": {}}
    
    lines = ["@startmindmap", f"* {root_name}"]
    
    def add_node(node: Dict[str, Any], depth: int) -> None:
        if depth > max_depth:
            return
        
        prefix = "*" * (depth + 1)
        
        # サブディレクトリを先に追加
        for dir_name in sorted(node.get("_dirs", {}).keys()):
            # ディレクトリ名をエスケープ（特殊文字対策）
            safe_name = dir_name.replace(":", "_").replace("<", "_").replace(">", "_")
            lines.append(f"{prefix} 📁 {safe_name}")
            add_node(node["_dirs"][dir_name], depth + 1)
        
        # ファイルを追加
        files = node.get("_files", [])
        for f in files:
            if depth + 1 <= max_depth:
                # ファイル名をエスケープ
                safe_f = str(f).replace(":", "_").replace("<", "_").replace(">", "_")
                # 拡張子によるアイコン
                if safe_f.endswith(".py"):
                    icon = "🐍"
                elif safe_f.endswith((".ts", ".tsx", ".js", ".jsx")):
                    icon = "📜"
                elif safe_f.endswith(".md"):
                    icon = "📝"
                elif safe_f.endswith((".yml", ".yaml")):
                    icon = "⚙️"
                elif safe_f.endswith(".json"):
                    icon = "📊"
                elif safe_f.endswith(".html"):
                    icon = "🌐"
                elif safe_f.endswith((".puml", ".pu")):
                    icon = "📐"
                else:
                    icon = "📄"
                lines.append(f"{prefix}_ {icon} {safe_f}")
    
    add_node(tree, 1)
    
    lines.append("@endmindmap")
    return "\n".join(lines)




def build_html(analysis: Dict[str, Any], plantuml_code: str, wbs_code: str, file_tree_code: str, root: Path) -> str:
    modules = analysis.get("modules") or []
    files_summary = analysis.get("files_summary") or []
    impl = analysis.get("implemented_features") or []
    missing = analysis.get("missing_features") or []
    recs = analysis.get("recommendations") or []
    structure_text = analysis.get("structure_text") or ""
    pages = analysis.get("pages") or []
    link_issues = analysis.get("link_issues") or []

    parts: List[str] = []

    parts.append('<div class="info-box">')
    parts.append("<h2>プロジェクト概要</h2>")
    parts.append(f"<p><strong>対象:</strong> {root}</p>")
    parts.append("</div>")

    if structure_text:
        parts.append("<h2>ディレクトリ構造（テキスト）</h2>")
        parts.append("<details><summary>テキスト形式で表示</summary>")
        parts.append("<pre><code>")
        parts.append(structure_text)
        parts.append("</code></pre>")
        parts.append("</details>")

    # ファイル階層図（PlantUML MindMap）
    if file_tree_code:
        parts.append("<h2>📂 ファイル階層図</h2>")
        encoded_tree = encode_plantuml(file_tree_code)
        parts.append('<div class="step" style="overflow-x: auto;">')
        parts.append(f'<img src="https://www.plantuml.com/plantuml/svg/{encoded_tree}" alt="File Tree Diagram" style="max-width: 100%; min-width: 600px;" />')
        parts.append("</div>")
        parts.append("<details><summary>PlantUMLソースコードを表示</summary>")
        parts.append("<pre><code>")
        parts.append(html_lib.escape(file_tree_code))
        parts.append("</code></pre>")
        parts.append("</details>")

    if pages:
        parts.append("<h2>HTMLページ一覧</h2><ul>")
        for p in pages[:300]:
            file_url = f"file://{(root / p).resolve()}" if isinstance(p, str) else f"file://{p.resolve()}"
            label = str(p)
            parts.append(f'<li><a href="{file_url}">{label}</a></li>')
        parts.append("</ul>")

    if link_issues:
        parts.append('<h2>リンク/参照の欠落（要修正）</h2><div class="warning-box">')
        parts.append("<p>HTML内の <code>href</code>/<code>src</code> を解決できなかったものです。</p>")
        parts.append("<ul>")
        for i in link_issues[:200]:
            parts.append(f"<li><strong>{i.get('source')}</strong>: {i.get('link')} → {i.get('resolved')}</li>")
        if len(link_issues) > 200:
            parts.append("<li>...（省略）</li>")
        parts.append("</ul></div>")

    # ファイル一覧と関数
    if files_summary:
        parts.append("<h2>ファイル一覧と関数</h2>")
        parts.append('<table class="file-table" style="width:100%; border-collapse: collapse; margin-bottom: 20px;">')
        parts.append('<thead><tr style="background-color: #f0f0f0;">')
        parts.append('<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">ファイル</th>')
        parts.append('<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">説明</th>')
        parts.append('<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">関数/クラス</th>')
        parts.append('</tr></thead><tbody>')
        for f in files_summary:
            path = html_lib.escape(str(f.get("path", "")))
            desc = html_lib.escape(str(f.get("description", "")))
            funcs = f.get("functions") or []
            funcs_str = ", ".join([html_lib.escape(str(fn)) for fn in funcs[:10]])
            if len(funcs) > 10:
                funcs_str += " ..."
            parts.append('<tr>')
            parts.append(f'<td style="border: 1px solid #ddd; padding: 8px; font-family: monospace;">{path}</td>')
            parts.append(f'<td style="border: 1px solid #ddd; padding: 8px;">{desc}</td>')
            parts.append(f'<td style="border: 1px solid #ddd; padding: 8px; font-family: monospace; font-size: 0.9em;">{funcs_str}</td>')
            parts.append('</tr>')
        parts.append('</tbody></table>')

    if modules:
        parts.append("<h2>モジュール</h2>")
        for m in modules:
            parts.append('<div class="step">')
            parts.append(f"<h3>{m.get('name','Unknown')}</h3>")
            if m.get("path"):
                parts.append(f"<p><strong>path:</strong> {m.get('path')}</p>")
            if m.get("purpose"):
                parts.append(f"<p><strong>purpose:</strong> {m.get('purpose')}</p>")
            
            feats = m.get("features") or []
            if feats:
                parts.append("<p><strong>features:</strong></p><ul>")
                for f in feats:
                    parts.append(f"<li>{f}</li>")
                parts.append("</ul>")

            deps = m.get("dependencies") or []
            if deps:
                parts.append(f"<p><strong>dependencies:</strong> {', '.join(map(str, deps))}</p>")
            parts.append("</div>")

    parts.append("<h2>構造図（PlantUML）</h2>")
    
    # PlantUML (Component)
    if plantuml_code:
        parts.append("<h3>コンポーネント図</h3>")
        encoded = encode_plantuml(plantuml_code)
        parts.append('<div class="step">')
        parts.append(f'<img src="https://www.plantuml.com/plantuml/svg/{encoded}" alt="PlantUML Diagram" style="max-width: 100%;" />')
        parts.append("</div>")
        parts.append("<details><summary>ソースコードを表示</summary>")
        parts.append("<pre><code>")
        parts.append(html_lib.escape(plantuml_code))
        parts.append("</code></pre>")
        parts.append("</details>")

    # PlantUML (WBS/MindMap)
    if wbs_code:
        parts.append("<h3>マインドマップ（WBS）</h3>")
        encoded_wbs = encode_plantuml(wbs_code)
        parts.append('<div class="step">')
        parts.append(f'<img src="https://www.plantuml.com/plantuml/svg/{encoded_wbs}" alt="PlantUML WBS" style="max-width: 100%;" />')
        parts.append("</div>")
        parts.append("<details><summary>ソースコードを表示</summary>")
        parts.append("<pre><code>")
        parts.append(html_lib.escape(wbs_code))
        parts.append("</code></pre>")
        parts.append("</details>")

    if impl:
        parts.append("<h2>実装済み機能</h2><ul>")
        parts += [f"<li>{x}</li>" for x in impl]
        parts.append("</ul>")

    if missing:
        parts.append('<h2>不足/要確認</h2><div class="warning-box"><ul>')
        parts += [f"<li>{x}</li>" for x in missing]
        parts.append("</ul></div>")

    if recs:
        parts.append('<h2>推奨</h2><div class="success-box"><ul>')
        parts += [f"<li>{x}</li>" for x in recs]
        parts.append("</ul></div>")

    parts.append("<h2>serena MCPで深掘りする場合</h2>")
    parts.append('<div class="info-box">')
    parts.append("<p>より厳密に「どのファイルで何をしているか」を追うなら、serena MCPでの解析がおすすめです。</p>")
    parts.append(
        "<pre><code>"
        "serena MCPを使って、このプロジェクトの構造とどのファイルで何をしているかを明確化して、"
        "PlantUMLでアクティビティ図を作って現状不足しているもの抽出して。"
        "</code></pre>"
    )
    parts.append("</div>")

    return "".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="プロジェクト構造を可視化し、HTMLで出力します")
    parser.add_argument("--directory", "-d", default=".", help="分析対象ディレクトリ（デフォルト: .）")
    parser.add_argument("--files", "-F", nargs="*", default=[], help="分析対象ファイル（複数指定可、ディレクトリと併用可）")
    parser.add_argument("--format", "-f", choices=["plantuml", "wbs", "all"], default="all", help="出力形式（plantuml/wbs/all）")
    parser.add_argument("--output", "-o", default="", help="出力HTMLパス（省略可）")
    args = parser.parse_args()

    # ディレクトリ処理
    user_root = Path(args.directory).resolve()
    
    # --files が指定されていて、--directory がデフォルト(.)の場合、
    # ユーザーの意図としては「ファイル周辺」を見たい可能性がある。
    # ただし、基本は user_root を起点にする。
    
    if not user_root.exists() or not user_root.is_dir():
        print(f"❌ ディレクトリが見つかりません: {user_root}")
        sys.exit(1)

    client = get_client()
    
    # ファイル収集
    structure, code_files = collect_targets(user_root, args.files)
    
    # 分析
    analysis = gemini_analyze(client, user_root, structure, code_files)

    # 静的サイト/教材のように「コードファイルが少ない」ケースでも最低限の有用情報を出す
    pages = find_html_files(user_root)
    issues, edges = check_links(user_root, pages)
    analysis["structure_text"] = structure_to_text(structure)
    analysis["pages"] = [str(p.relative_to(user_root)) if p.is_relative_to(user_root) else str(p) for p in pages]
    analysis["link_issues"] = issues

    if not (analysis.get("modules") or []):
        analysis["modules"] = fallback_modules_from_pages(pages, edges, user_root)
        analysis.setdefault("implemented_features", [])
        analysis.setdefault("missing_features", [])
        analysis.setdefault("recommendations", [])
        if pages:
            analysis["implemented_features"] = list(analysis["implemented_features"]) + [f"HTMLページ: {len(pages)}件"]
        if issues:
            analysis["missing_features"] = list(analysis["missing_features"]) + [f"リンク/参照欠落: {len(issues)}件（修正推奨）"]
        if not issues:
            analysis["recommendations"] = list(analysis["recommendations"]) + ["内部リンクの解決に問題は見つかりませんでした。"]

    modules = analysis.get("modules") or []
    
    # PlantUMLコード生成
    gen_all = (args.format == "all")
    
    plantuml_code = plantuml(modules) if gen_all or args.format == "plantuml" else ""
    wbs_code = plantuml_wbs(modules, user_root.name) if gen_all or args.format in {"plantuml", "wbs"} else ""
    
    # ファイル階層図を直接生成（Geminiに依存しない全量表示）
    file_tree_code = structure_to_plantuml_mindmap(structure, user_root.name) if gen_all or args.format in {"plantuml", "wbs"} else ""

    body = build_html(analysis, plantuml_code, wbs_code, file_tree_code, user_root)
    title = f"Overview - {user_root.name}"
    html = create_html_template(title, body)

    if args.output:
        out = Path(args.output)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = DEFAULT_OVERVIEW_DIR / f"overview_{ts}.html"

    save_html_file(html, out, title)


if __name__ == "__main__":
    main()

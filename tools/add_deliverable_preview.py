#!/usr/bin/env python3
"""
Add 📋 成果物プレビュー sections to lesson command files.
Inserts a hybrid preview block (expected output + verification commands)
before the completion check section in each lesson file.

Usage:
    uv run python tools/add_deliverable_preview.py --dry-run   # Preview changes
    uv run python tools/add_deliverable_preview.py --execute    # Apply changes
    uv run python tools/add_deliverable_preview.py --execute --sync  # Apply + sync to .cursor/
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Module → Type mapping ──────────────────────────────────────────────

MODULE_TYPE_MAP = {
    1: "A",   # Banner PNG images
    2: "A",   # Diagram PNG images
    3: "A",   # Screenshot PNG images
    4: "D",   # gogcli CLI output
    5: "E",   # PPTX files
    6: "B",   # Agent dev / code files
    7: "G",   # Skill/Command files
    8: "D",   # BigQuery terminal output
    9: "D",   # Slack search terminal output
    10: "J",  # GAS scripts
    11: "F",  # GitHub Actions YAML
    # 12: excluded (Notion, no local files)
    13: "C",  # HTML LP files
    14: "B",  # Markdown articles
    15: "H",  # Video MP4 + JSON
    16: "C",  # HTML email
    17: "A",  # Marketing PNG + text
    18: "B",  # PM docs (with overrides)
}

# Modules to skip entirely
SKIP_MODULES = {0, 12, 19, 20}

# ── Default output paths per module ────────────────────────────────────

DEFAULT_OUTPUT = {
    1:  ("docs/generated/banners/", "banner-{テーマ名}.png", "バナー画像 (1200x630px)"),
    2:  ("output/diagrams/", "flow-{テーマ名}.png", "フロー図 (PNG)"),
    3:  ("output/screenshots/", "analyzed-{対象名}.png", "分析済みスクリーンショット"),
    4:  ("", "", ""),  # CLI output, no file
    5:  ("output/", "presentation.pptx", "PowerPointプレゼンテーション"),
    6:  ("output/", "{プロジェクト名}/", "エージェント/コード成果物"),
    7:  ("skills/{skill_name}/", "SKILL.md", "スキル定義ファイル"),
    8:  ("", "", ""),  # CLI output
    9:  ("", "", ""),  # CLI output
    10: ("output/gas/", "Code.gs", "GASスクリプト"),
    11: (".github/workflows/", "{workflow}.yml", "GitHub Actionsワークフロー"),
    13: ("output/lp/", "index.html", "ランディングページ"),
    14: ("output/", "article-{N}-{L}-*.md", "記事ドキュメント"),
    15: ("output/ugc/", "*.mp4 + metadata.json", "動画 + メタデータ"),
    16: ("output/email/", "index.html", "HTMLメール"),
    17: ("output/marketing/", "banner-*.png", "マーケティング素材"),
    18: ("output/pm/", "*.md", "PMドキュメント"),
}

# ── Module 18 per-lesson overrides ─────────────────────────────────────

MODULE_18_OVERRIDES = {
    "18-1":  ("output/pm/stakeholder-map.md", "ステークホルダーマップ"),
    "18-2":  ("output/pm/customer-needs.md", "顧客ニーズ分析"),
    "18-3":  ("output/pm/prd.md", "プロダクト要件定義書"),
    "18-4":  ("output/pm/review-*.md", "レビュードキュメント群"),
    "18-5":  ("output/pm/requirements-spec.md", "要件仕様書"),
    "18-6":  ("output/pm/usecases.md", "ユースケース定義"),
    "18-7":  ("output/pm/wbs.md", "WBS (Work Breakdown Structure)"),
    "18-8":  ("output/pm/er-diagram.puml", "ER図 (PlantUML)"),
    "18-9":  ("output/pm/system-architecture.puml", "システムアーキテクチャ図"),
    "18-10": ("output/pm/test-plan.md", "テスト計画書"),
    "18-11": ("output/pm/test-cases.md", "テストケース一覧"),
    "18-12": ("output/pm/e2e-test-code/", "E2Eテストコード"),
    "18-13": ("output/pm/integration-test-evidence/", "結合テストエビデンス"),
    "18-14": ("output/pm/deployment-plan.md", "デプロイ計画"),
    "18-15": ("output/pm/test-cases.md", "テストケース"),
    "18-16": ("output/pm/unit-test-code/", "単体テストコード"),
    "18-17": ("output/pm/operation-manual.md", "運用マニュアル"),
    "18-18": ("output/pm/retrospective.md", "振り返りレポート"),
    "18-19": ("output/pm/presentation.md", "プレゼン資料"),
    "18-20": ("output/pm/project-summary.md", "プロジェクト総括"),
}

# ── Filename pattern ───────────────────────────────────────────────────

FILE_PATTERN = re.compile(r"^start-(\d+)-(\d+)\.md$")


# ── Templates ──────────────────────────────────────────────────────────

def template_A(output_dir, filename, desc):
    """Image files (PNG)"""
    return f"""
---

## 📋 成果物プレビュー

### 期待される出力
```
📁 {output_dir}
├── {filename}
└── (バリエーション)
```
> 形式: PNG | サイズ: 自動設定

### 確認コマンド
```bash
# ファイル一覧
ls -la {output_dir}

# 画像を開く（macOS: open / Linux: xdg-open）
open {output_dir}
```

> 💡 **Claude Code**: Read ツールでファイルパスを指定するとチャット内で画像プレビューできます
> 💡 **Cursor**: ファイルエクスプローラーで画像をクリックしてプレビュー
"""


def template_B(output_dir, filename, desc):
    """Text/Markdown files"""
    path = f"{output_dir}{filename}" if not filename.startswith("*") else f"{output_dir}"
    return f"""
---

## 📋 成果物プレビュー

### 期待される出力
```
📁 {output_dir}
└── {filename}  ({desc})
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh {path}

# 冒頭を確認（最初の30行）
head -30 {path}
```

> 💡 全文を確認: `cat {path}` で全文表示できます
"""


def template_C(output_dir, filename, desc):
    """HTML files"""
    path = f"{output_dir}{filename}"
    return f"""
---

## 📋 成果物プレビュー

### 期待される出力
```
📁 {output_dir}
├── {filename}  ({desc})
├── style.css
└── assets/
```

### 確認コマンド
```bash
# ファイル一覧
ls -lh {output_dir}

# ブラウザで開く（macOS: open / Linux: xdg-open）
open {path}
```

> 💡 HTMLの構造確認: `head -30 {path}`
"""


def template_D(output_dir, filename, desc):
    """CLI/Terminal output"""
    return """
---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```
┌─────────────────────────────────────┐
│  コマンド実行結果                      │
│  ステータス: ✅ 成功                   │
│  処理件数: N件                        │
└─────────────────────────────────────┘
```

> 💡 出力をファイルに保存するには、コマンド末尾に ` > output/result.txt` を追加
"""


def template_E(output_dir, filename, desc):
    """PPTX files"""
    path = f"{output_dir}{filename}"
    return f"""
---

## 📋 成果物プレビュー

### 期待される出力
```
📁 {output_dir}
└── {filename}  ({desc})
    スライド数: N枚
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh {path}

# PowerPointで開く（macOS: open / Linux: xdg-open）
open {path}
```

> 💡 スライド数確認: `python3 -c "from pptx import Presentation; p=Presentation('{path}'); print(f'スライド数: {{len(p.slides)}}')"`
"""


def template_F(output_dir, filename, desc):
    """YAML workflow files"""
    return f"""
---

## 📋 成果物プレビュー

### 期待される出力
```
📁 {output_dir}
└── {filename}  ({desc})
```

### 確認コマンド
```bash
# ワークフローファイルの一覧
ls -la {output_dir}

# ファイル内容を確認
cat {output_dir}{filename}

# GitHub上の実行状況を確認
gh run list --limit 5
```
"""


def template_G(output_dir, filename, desc):
    """Skill/Command files"""
    return f"""
---

## 📋 成果物プレビュー

### 期待される出力
```
📁 {output_dir}
├── {filename}  (スキル定義)
├── scripts/    (実行スクリプト)
└── tests/      (テストファイル)
```

### 確認コマンド
```bash
# スキルのディレクトリ構造を確認
tree {output_dir} 2>/dev/null || find {output_dir} -maxdepth 2 -type f | head -15

# SKILL.md の冒頭を確認
head -30 {output_dir}{filename}
```
"""


def template_H(output_dir, filename, desc):
    """Video/UGC output"""
    return f"""
---

## 📋 成果物プレビュー

### 期待される出力
```
📁 {output_dir}
├── *.mp4           (動画ファイル)
├── metadata.json   (メタデータ)
└── thumbnails/     (サムネイル)
```

### 確認コマンド
```bash
# 出力ファイルの一覧とサイズ
ls -lh {output_dir}

# メタデータを確認
cat {output_dir}*metadata*.json 2>/dev/null | head -20

# 動画を再生（macOS: open / Linux: xdg-open）
open {output_dir}*.mp4
```
"""


def template_J(output_dir, filename, desc):
    """GAS scripts"""
    return f"""
---

## 📋 成果物プレビュー

### 期待される出力
```
📁 {output_dir}
└── {filename}  ({desc})
```

### 確認コマンド
```bash
# ローカルのスクリプトファイルを確認
ls -la {output_dir}

# スクリプト内容の冒頭を確認
head -30 {output_dir}{filename}

# GASエディタで確認
clasp open
```
"""


TEMPLATE_MAP = {
    "A": template_A,
    "B": template_B,
    "C": template_C,
    "D": template_D,
    "E": template_E,
    "F": template_F,
    "G": template_G,
    "H": template_H,
    "J": template_J,
}


# ── Core logic ─────────────────────────────────────────────────────────

def find_insertion_point(lines: list[str]) -> int | None:
    """Find insertion point: before ## ✅ 完了チェック or ## ➡️ 次のステップ."""
    completion_line = None
    next_step_line = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "## ✅ 完了チェック":
            completion_line = i
            break
        if stripped.startswith("## ➡️"):
            next_step_line = i

    target = completion_line or next_step_line
    if target is None:
        return None

    # Find the --- separator before target (within 5 lines)
    for j in range(target - 1, max(target - 5, 0), -1):
        if lines[j].strip() == "---":
            return j
    return target


def get_preview_block(module_num: int, lesson_id: str) -> str | None:
    """Generate preview block for a lesson."""
    if module_num in SKIP_MODULES:
        return None

    dtype = MODULE_TYPE_MAP.get(module_num)
    if dtype is None:
        return None

    template_fn = TEMPLATE_MAP[dtype]

    # Module 18 overrides
    if module_num == 18 and lesson_id in MODULE_18_OVERRIDES:
        output_path, desc = MODULE_18_OVERRIDES[lesson_id]
        if "/" in output_path and not output_path.endswith("/"):
            parts = output_path.rsplit("/", 1)
            output_dir = parts[0] + "/"
            filename = parts[1]
        else:
            output_dir = output_path
            filename = ""
        return template_fn(output_dir, filename, desc)

    # Default output info
    info = DEFAULT_OUTPUT.get(module_num)
    if info is None:
        return None

    output_dir, filename, desc = info

    # Substitute {N} and {L} placeholders
    lesson_parts = lesson_id.split("-")
    if len(lesson_parts) == 2:
        filename = filename.replace("{N}", lesson_parts[0]).replace("{L}", lesson_parts[1])

    return template_fn(output_dir, filename, desc)


def process_file(filepath: Path, dry_run: bool = True) -> str:
    """Process a single lesson file. Returns status string."""
    filename = filepath.name
    match = FILE_PATTERN.match(filename)
    if not match:
        return f"[SKIP] {filename}: non-numeric pattern"

    module_num = int(match.group(1))
    lesson_num = match.group(2)
    lesson_id = f"{module_num}-{lesson_num}"

    if module_num in SKIP_MODULES:
        return f"[SKIP] {filename}: module {module_num} excluded"

    content = filepath.read_text(encoding="utf-8")

    # Idempotency check
    if "## 📋 成果物プレビュー" in content:
        return f"[SKIP] {filename}: preview already exists"

    lines = content.split("\n")
    insertion_point = find_insertion_point(lines)
    if insertion_point is None:
        return f"[WARN] {filename}: no anchor found (no 完了チェック or 次のステップ)"

    # Get preview block
    preview = get_preview_block(module_num, lesson_id)
    if preview is None:
        return f"[SKIP] {filename}: no template for module {module_num}"

    # Insert preview block
    preview_lines = preview.rstrip("\n").split("\n")

    new_lines = lines[:insertion_point] + preview_lines + [""] + lines[insertion_point:]
    new_content = "\n".join(new_lines)

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")

    dtype = MODULE_TYPE_MAP.get(module_num, "?")
    return f"[{'DRY' if dry_run else 'OK'}] {filename}: type={dtype}, insert@line {insertion_point}, +{len(preview_lines)} lines"


def main():
    dry_run = "--execute" not in sys.argv
    do_sync = "--sync" in sys.argv

    if dry_run:
        print("=" * 60)
        print("DRY RUN MODE - No changes will be made")
        print("Run with --execute to apply changes")
        print("=" * 60)
    else:
        print("=" * 60)
        print("EXECUTING - Changes will be applied!")
        print("=" * 60)

    claude_dir = ROOT / ".claude" / "commands" / "lesson"
    cursor_dir = ROOT / ".cursor" / "commands" / "lesson"

    if not claude_dir.exists():
        print(f"ERROR: {claude_dir} does not exist")
        sys.exit(1)

    # Process all start-*.md files
    files = sorted(claude_dir.glob("start-*.md"))
    print(f"\nFound {len(files)} start-*.md files\n")

    stats = {"OK": 0, "DRY": 0, "SKIP": 0, "WARN": 0}

    for f in files:
        result = process_file(f, dry_run)
        print(f"  {result}")

        for key in stats:
            if f"[{key}]" in result:
                stats[key] += 1
                break

    print(f"\n{'─' * 40}")
    action_key = "DRY" if dry_run else "OK"
    print(f"  Modified: {stats[action_key]}")
    print(f"  Skipped:  {stats['SKIP']}")
    print(f"  Warnings: {stats['WARN']}")

    # Sync to .cursor/
    if do_sync and not dry_run:
        print(f"\n{'─' * 40}")
        print("Syncing to .cursor/commands/lesson/...")

        # Check for pre-existing diffs
        diff_result = subprocess.run(
            ["diff", "-rq", str(claude_dir), str(cursor_dir)],
            capture_output=True, text=True
        )

        if diff_result.returncode != 0:
            # There are diffs - this is expected after our modifications
            pass

        # Copy modified files
        for f in claude_dir.glob("start-*.md"):
            target = cursor_dir / f.name
            if target.exists():
                shutil.copy2(f, target)
            else:
                print(f"  [WARN] {f.name} not found in .cursor/, skipping")

        print("  Sync complete.")

        # Verify sync
        verify = subprocess.run(
            ["diff", "-rq", str(claude_dir), str(cursor_dir)],
            capture_output=True, text=True
        )
        if verify.stdout.strip():
            print(f"  [WARN] Post-sync diffs remain:\n{verify.stdout[:500]}")
        else:
            print("  [OK] .claude/ and .cursor/ are in sync")

    if dry_run:
        print(f"\n{'=' * 60}")
        print("DRY RUN COMPLETE - Run with --execute --sync to apply")
        print("=" * 60)


if __name__ == "__main__":
    main()

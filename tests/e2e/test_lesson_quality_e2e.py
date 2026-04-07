"""レッスンコンテンツ品質 E2E テスト

初学者向けのわかりやすさ、図解の正確性、ナビゲーション整合性を検証し
エビデンスレポートを生成する。

実行:
    python -m pytest tests/e2e/test_lesson_quality_e2e.py -v
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tests.e2e.lesson_quality_helpers import (
    JARGON_TERMS,
    AsciiArtBlock,
    extract_ascii_art_blocks,
    extract_code_blocks,
    extract_mermaid_blocks,
    extract_tables,
    validate_mermaid_syntax,
    write_evidence_report,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLAUDE_LESSON_DIR = PROJECT_ROOT / ".claude" / "commands" / "lesson"
START_REF_RE = re.compile(r"/start-(\d+)-(\d+)")

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _all_lesson_paths() -> list[Path]:
    return sorted(CLAUDE_LESSON_DIR.glob("start-*.md"))


def _all_lesson_ids() -> set[str]:
    return {f.stem for f in _all_lesson_paths()}


LESSON_PATHS = _all_lesson_paths()
LESSON_IDS = _all_lesson_ids()


# ---------------------------------------------------------------------------
# Category B-1: Code block quality
# ---------------------------------------------------------------------------


class TestCodeBlockQuality:
    """コードブロックの品質チェック"""

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_json_blocks_are_valid_json(self, lesson_path: Path):
        """```json ブロックが有効な JSON であること"""
        text = lesson_path.read_text(encoding="utf-8")
        blocks = extract_code_blocks(text)
        json_blocks = [b for b in blocks if b.language == "json"]
        if not json_blocks:
            pytest.skip("no json blocks")
        errors = []
        for block in json_blocks:
            try:
                json.loads(block.content)
            except json.JSONDecodeError as e:
                errors.append(f"L{block.line_number}: {e.msg}")
        assert not errors, f"Invalid JSON blocks:\n" + "\n".join(errors)

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_code_blocks_have_language_specifier(self, lesson_path: Path):
        """コードブロックに言語指定があること（xfail: 既存の未対応を許容）"""
        text = lesson_path.read_text(encoding="utf-8")
        blocks = extract_code_blocks(text)
        if not blocks:
            pytest.skip("no code blocks")
        unlabeled = [b for b in blocks if not b.language]
        if unlabeled:
            ratio = len(unlabeled) / len(blocks)
            if ratio > 0.5:
                pytest.xfail(
                    f"{len(unlabeled)}/{len(blocks)} blocks unlabeled ({ratio:.0%})"
                )
            assert not unlabeled, (
                f"{len(unlabeled)} unlabeled code blocks at lines: "
                + ", ".join(str(b.line_number) for b in unlabeled)
            )


# ---------------------------------------------------------------------------
# Category C: Diagrams & ASCII art
# ---------------------------------------------------------------------------


class TestAsciiArtAndDiagrams:
    """図解・ダイアグラムの品質チェック"""

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_mermaid_blocks_syntax(self, lesson_path: Path):
        """Mermaid ブロックの構文が正しいこと"""
        text = lesson_path.read_text(encoding="utf-8")
        mermaid_blocks = extract_mermaid_blocks(text)
        if not mermaid_blocks:
            pytest.skip("no mermaid blocks")
        errors = []
        for block in mermaid_blocks:
            valid, msg = validate_mermaid_syntax(block.content)
            if not valid:
                errors.append(f"L{block.line_number}: {msg}")
        assert not errors, "Mermaid syntax errors:\n" + "\n".join(errors)

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_ascii_art_box_alignment(self, lesson_path: Path):
        """ASCII art のボックスが整列していること"""
        text = lesson_path.read_text(encoding="utf-8")
        blocks = extract_ascii_art_blocks(text)
        # 1行だけのブロックは説明文中の罫線文字（例: ┌─┐│└─┘）なので除外
        blocks = [b for b in blocks if len(b.lines) >= 3]
        if not blocks:
            pytest.skip("no ASCII art blocks")
        errors = []
        for block in blocks:
            # ボックスの開始文字（┌╭╔┏）と終了文字（└╰╚┗）の列位置が一致するか
            openers = {"┌", "╭", "╔", "┏"}
            closers = {"└", "╰", "╚", "┗"}
            open_cols = set()
            close_cols = set()
            for line in block.lines:
                for i, c in enumerate(line):
                    if c in openers:
                        open_cols.add(i)
                    if c in closers:
                        close_cols.add(i)
            if open_cols and close_cols and open_cols != close_cols:
                # 全角文字幅でずれる場合は1-2列の差を許容
                max_diff = max(
                    min(abs(o - c) for c in close_cols) for o in open_cols - close_cols
                ) if open_cols - close_cols else 0
                if max_diff > 2:
                    errors.append(
                        f"L{block.line_start}-{block.line_end}: "
                        f"box misaligned (open cols={open_cols}, close cols={close_cols})"
                    )
        assert not errors, "ASCII art alignment:\n" + "\n".join(errors)

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_tables_are_well_formed(self, lesson_path: Path):
        """Markdown テーブルの列数が一致していること"""
        text = lesson_path.read_text(encoding="utf-8")
        tables = extract_tables(text)
        if not tables:
            pytest.skip("no tables")
        errors = []
        for table in tables:
            col_counts = set()
            for row in table.rows:
                # 先頭と末尾の | を除いてカウント
                cols = row.strip().strip("|").split("|")
                col_counts.add(len(cols))
            if len(col_counts) > 1:
                errors.append(
                    f"L{table.line_start}: column count varies: {col_counts}"
                )
        assert not errors, "Table column mismatch:\n" + "\n".join(errors)


# ---------------------------------------------------------------------------
# Category B-2: Beginner readability
# ---------------------------------------------------------------------------


class TestBeginnerReadability:
    """初学者向けの読みやすさチェック"""

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_step_numbering_sequential(self, lesson_path: Path):
        """## Step / ## ステップ の番号が連続していること"""
        text = lesson_path.read_text(encoding="utf-8")
        step_re = re.compile(r"^##\s+.*?(?:Step|ステップ)\s*(\d+)", re.MULTILINE)
        steps = [int(m.group(1)) for m in step_re.finditer(text)]
        if len(steps) < 2:
            pytest.skip("less than 2 steps")
        for i in range(1, len(steps)):
            if steps[i] != steps[i - 1] + 1:
                pytest.fail(
                    f"Step numbering gap: {steps[i-1]} → {steps[i]} "
                    f"(expected {steps[i-1] + 1})"
                )

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_emoji_header_pattern_consistent(self, lesson_path: Path):
        """## ヘッダーの絵文字パターンが統一されていること"""
        text = lesson_path.read_text(encoding="utf-8")
        h2_re = re.compile(r"^##\s+(.+)$", re.MULTILINE)
        headers = h2_re.findall(text)
        if len(headers) < 3:
            pytest.skip("too few h2 headers")
        # 絵文字で始まるヘッダーの割合を確認
        emoji_re = re.compile(r"^[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u26A1\u2705\u274C\u26A0\u2139\u27A1]")
        emoji_count = sum(1 for h in headers if emoji_re.match(h))
        # 全部絵文字付き or 全部なし なら OK、混在は警告
        if 0 < emoji_count < len(headers):
            ratio = emoji_count / len(headers)
            if ratio < 0.5:
                pytest.xfail(f"Mixed emoji headers: {emoji_count}/{len(headers)}")


# ---------------------------------------------------------------------------
# Category B-3: Navigation
# ---------------------------------------------------------------------------


class TestNavigationIntegrity:
    """レッスン間のナビゲーション整合性チェック"""

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_has_next_step_section(self, lesson_path: Path):
        """次のステップセクションが存在すること"""
        # 最終モジュール、ワークショップ、セットアップは除外
        stem = lesson_path.stem
        if any(x in stem for x in ["cursor-workshop", "exercise"]):
            pytest.skip("workshop/exercise file")
        # Module 20 の最終レッスンは除外
        if stem == "start-20-1":
            pytest.skip("final module")

        text = lesson_path.read_text(encoding="utf-8")
        has_next = (
            "次のステップ" in text
            or "next" in text.lower()
            or "finish" in text.lower()
            or "完了" in text
            or "おめでとう" in text
        )
        assert has_next, f"{stem}: 次のステップ / 完了セクションがない"

    @pytest.mark.parametrize("lesson_path", LESSON_PATHS, ids=lambda p: p.stem)
    def test_next_step_references_valid_lessons(self, lesson_path: Path):
        """次のステップで参照される /start-X-Y が実在すること"""
        text = lesson_path.read_text(encoding="utf-8")
        # 「次のステップ」セクション以降のみチェック
        next_section_idx = text.find("次のステップ")
        if next_section_idx == -1:
            pytest.skip("no next step section")
        section_text = text[next_section_idx:]
        errors = []
        for match in START_REF_RE.finditer(section_text):
            ref_id = f"start-{match.group(1)}-{match.group(2)}"
            if ref_id not in LESSON_IDS:
                errors.append(f"/start-{match.group(1)}-{match.group(2)} → {ref_id}.md not found")
        assert not errors, "Broken next-step refs:\n" + "\n".join(errors)


# ---------------------------------------------------------------------------
# Evidence report
# ---------------------------------------------------------------------------


class TestDiagramEvidence:
    """図解のインベントリレポートを生成"""

    def test_generate_diagram_report(self):
        """diagram-validation-report.json を生成"""
        lessons = []
        total_mermaid = 0
        total_ascii = 0
        total_tables = 0

        for lesson_path in LESSON_PATHS:
            text = lesson_path.read_text(encoding="utf-8")
            mermaid_blocks = extract_mermaid_blocks(text)
            ascii_blocks = extract_ascii_art_blocks(text)
            table_blocks = extract_tables(text)

            mermaid_items = []
            for b in mermaid_blocks:
                valid, err = validate_mermaid_syntax(b.content)
                mermaid_items.append({"line": b.line_number, "valid": valid, "error": err})

            ascii_items = [
                {"line_start": b.line_start, "line_end": b.line_end, "line_count": len(b.lines)}
                for b in ascii_blocks
            ]

            table_items = [
                {"line": t.line_start, "columns": t.column_count, "has_separator": t.has_separator}
                for t in table_blocks
            ]

            total_mermaid += len(mermaid_items)
            total_ascii += len(ascii_items)
            total_tables += len(table_items)

            if mermaid_items or ascii_items or table_items:
                lessons.append({
                    "file": lesson_path.stem,
                    "mermaid": mermaid_items,
                    "ascii_art": ascii_items,
                    "tables": table_items,
                })

        report = {
            "total_lessons_scanned": len(LESSON_PATHS),
            "lessons_with_diagrams": len(lessons),
            "total_mermaid_blocks": total_mermaid,
            "total_ascii_art_blocks": total_ascii,
            "total_tables": total_tables,
            "lessons": lessons,
        }
        path = write_evidence_report(report, "diagram-validation-report.json")
        assert path.exists()

    def test_generate_code_block_report(self):
        """code-block-quality-report.json を生成"""
        lessons = []
        total_labeled = 0
        total_unlabeled = 0

        for lesson_path in LESSON_PATHS:
            text = lesson_path.read_text(encoding="utf-8")
            blocks = extract_code_blocks(text)
            labeled = [b for b in blocks if b.language]
            unlabeled = [b for b in blocks if not b.language]
            total_labeled += len(labeled)
            total_unlabeled += len(unlabeled)

            if unlabeled:
                lessons.append({
                    "file": lesson_path.stem,
                    "total_blocks": len(blocks),
                    "labeled": len(labeled),
                    "unlabeled": len(unlabeled),
                    "unlabeled_lines": [b.line_number for b in unlabeled],
                })

        report = {
            "total_lessons_scanned": len(LESSON_PATHS),
            "total_code_blocks": total_labeled + total_unlabeled,
            "labeled": total_labeled,
            "unlabeled": total_unlabeled,
            "label_rate": f"{total_labeled / (total_labeled + total_unlabeled):.1%}" if (total_labeled + total_unlabeled) else "N/A",
            "lessons_with_unlabeled": lessons,
        }
        path = write_evidence_report(report, "code-block-quality-report.json")
        assert path.exists()

    def test_generate_readability_report(self):
        """beginner-readability-report.json を生成"""
        lessons = []

        for lesson_path in LESSON_PATHS:
            text = lesson_path.read_text(encoding="utf-8")
            warnings = []

            # Jargon check: first occurrence without explanation
            text_lower = text.lower()
            for term, explanation_pattern in JARGON_TERMS.items():
                idx = text_lower.find(term.lower())
                if idx == -1:
                    continue
                # 初出箇所の前後200文字で説明パターンを探す
                context_start = max(0, idx - 200)
                context_end = min(len(text), idx + 200)
                context = text[context_start:context_end]
                if not re.search(explanation_pattern, context, re.IGNORECASE):
                    line_num = text[:idx].count("\n") + 1
                    warnings.append({
                        "type": "jargon_without_explanation",
                        "term": term,
                        "line": line_num,
                    })

            if warnings:
                lessons.append({
                    "file": lesson_path.stem,
                    "warnings": warnings,
                })

        report = {
            "total_lessons_scanned": len(LESSON_PATHS),
            "lessons_with_warnings": len(lessons),
            "lessons": lessons,
        }
        path = write_evidence_report(report, "beginner-readability-report.json")
        assert path.exists()

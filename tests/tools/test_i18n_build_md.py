"""tests for tools/i18n_build_md.py — Phase 2: MD ビルド"""

import json
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import import_module_from_repo

_EXTRACT_MOD_PATH = "tools/i18n_extract_md.py"
_MOD_PATH = "tools/i18n_build_md.py"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_MD = textwrap.dedent("""\
---
description: "Module 0 Lesson 0-1: 環境セットアップ確認"
duration: "約15分"
prerequisites: ["Cursor をインストール済み", "ai-agent-camp フォルダを開いている"]
level: "beginner"
tags: ["setup", "environment"]
---

# Lesson 0-1: 環境セットアップ確認

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

| 項目 | 内容 |
|------|------|
| ゴール | 環境確認 |
| 所要時間 | 約15分 |

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」と入力してください。

- OS の判定（Mac / Windows）
- Python / Node.js の確認

教材ページは [こちら](https://ai-agent.camp/ja/course/module-0) を参照。

**AskQuestionの設定:**
```json
{
  "title": "Step 1: セットアップ開始",
  "questions": [{
    "id": "action",
    "prompt": "環境のセットアップを始めましょう。何をしますか？",
    "options": [
      {"id": "run_setup", "label": "セットアップを始める"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

通常のコードブロック:
```python
print("hello")
```

![セットアップ画面](images/setup.png)
""")

SAMPLE_TRANSLATIONS = {
    "frontmatter.description": "Module 0 Lesson 0-1: Environment Setup Check",
    "frontmatter.duration": "About 15 minutes",
    "frontmatter.prerequisites.0": "Cursor installed",
    "frontmatter.prerequisites.1": "ai-agent-camp folder is open",
    "body.h1.0": "Lesson 0-1: Environment Setup Check",
    "body.h2.0": "Check Setup Progress",
    "body.p.0": "**AI auto-runs:** {{code_0}} to show current setup progress.",
    "body.table.0.r0.c0": "Item",
    "body.table.0.r0.c1": "Details",
    "body.table.0.r1.c0": "Goal",
    "body.table.0.r1.c1": "Environment check",
    "body.table.0.r2.c0": "Duration",
    "body.table.0.r2.c1": "About 15 minutes",
    "body.blockquote.0": "**Hint**: If AI stops responding, type 'show more'.",
    "body.li.0": "OS detection (Mac / Windows)",
    "body.li.1": "Python / Node.js verification",
    "body.p.1": "See course page [here](https://ai-agent.camp/en/course/module-0).",
    "body.askq.0.title": "Step 1: Start Setup",
    "body.askq.0.questions.0.prompt": "Let's start environment setup. What would you like to do?",
    "body.askq.0.questions.0.options.0.label": "Start setup",
    "body.askq.0.questions.0.options.1.label": "Skip",
    "body.img_alt.0": "Setup screen",
    "body.p.2": "**AskQuestion settings:**",
    "body.p.3": "Normal code block:",
}


@pytest.fixture
def build_mod():
    # i18n_build_md は i18n_extract_md に依存するため先にロード
    import_module_from_repo("i18n_extract_md", _EXTRACT_MOD_PATH)
    return import_module_from_repo("i18n_build_md", _MOD_PATH)


@pytest.fixture
def locale_dir(tmp_path):
    d = tmp_path / "locales" / "md"
    d.mkdir(parents=True)
    return d


# ===========================================================================
# TestApplyTranslations — 中心テスト群
# ===========================================================================

class TestApplyTranslations:
    """apply_translations_to_md のテスト"""

    def test_frontmatter_description_replaced(self, build_mod):
        result, applied, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert 'Module 0 Lesson 0-1: Environment Setup Check' in result

    def test_frontmatter_duration_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "About 15 minutes" in result

    def test_frontmatter_prerequisites_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "Cursor installed" in result
        assert "ai-agent-camp folder is open" in result

    def test_heading_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "# Lesson 0-1: Environment Setup Check" in result
        assert "## Check Setup Progress" in result

    def test_paragraph_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "**AI auto-runs:**" in result

    def test_table_cells_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "Goal" in result
        assert "Environment check" in result
        assert "Item" in result

    def test_blockquote_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "**Hint**: If AI stops responding" in result

    def test_list_items_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "OS detection (Mac / Windows)" in result
        assert "Python / Node.js verification" in result

    def test_askq_json_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert '"Step 1: Start Setup"' in result
        assert "Let's start environment setup" in result
        assert '"Start setup"' in result
        assert '"Skip"' in result

    def test_askq_json_structure_preserved(self, build_mod):
        """AskQuestion JSON の id フィールドは変更されない"""
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert '"id": "action"' in result
        assert '"id": "run_setup"' in result
        assert '"id": "skip"' in result

    def test_code_fence_untouched(self, build_mod):
        """通常のコードフェンス内は変更されない"""
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert 'print("hello")' in result

    def test_inline_code_restored(self, build_mod):
        """翻訳後にインラインコードが復元される"""
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "`uv run python tools/setup_progress.py show`" in result

    def test_url_ja_rewritten(self, build_mod):
        """URL 内の /ja/ が /en/ に書き換え"""
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "/en/course/module-0" in result
        assert "/ja/course/" not in result

    def test_image_alt_replaced(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "![Setup screen]" in result

    def test_missing_key_fallback(self, build_mod):
        """翻訳キーが欠損 → 日本語ソースのまま"""
        partial = {"body.h1.0": "Translated heading"}
        result, applied, missing = build_mod.apply_translations_to_md(
            SAMPLE_MD, partial, "en"
        )
        assert "# Translated heading" in result
        assert applied >= 1
        assert missing > 0
        # 未翻訳の見出しは日本語のまま
        assert "セットアップ進捗の確認" in result

    def test_applied_and_missing_counts(self, build_mod):
        _, applied, missing = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        # SAMPLE_TRANSLATIONS は全キーをカバー — 具体値で検証
        assert applied == len(SAMPLE_TRANSLATIONS)
        assert missing == 0

    def test_horizontal_rule_preserved(self, build_mod):
        result, _, _ = build_mod.apply_translations_to_md(
            SAMPLE_MD, SAMPLE_TRANSLATIONS, "en"
        )
        assert "---" in result


class TestAskqSchemaB:
    """Schema B の AskQuestion JSON テスト"""

    def test_schema_b_replaced(self, build_mod):
        md = textwrap.dedent("""\
        ---
        description: test
        ---

        Setup:
        ```json
        {
          "type": "AskQuestion",
          "question": "何をしますか？",
          "hint": "ヒントテキスト",
          "options": [
            {"id": "a", "label": "選択A"},
            {"id": "b", "label": "選択B"}
          ]
        }
        ```
        """)
        translations = {
            "body.askq.0.question": "What do you want to do?",
            "body.askq.0.hint": "Hint text",
            "body.askq.0.options.0.label": "Option A",
            "body.askq.0.options.1.label": "Option B",
        }
        result, applied, _ = build_mod.apply_translations_to_md(md, translations, "en")
        assert "What do you want to do?" in result
        assert "Hint text" in result
        assert "Option A" in result
        assert "Option B" in result
        assert '"id": "a"' in result  # id は不変


class TestCheckboxList:
    """チェックボックスリストの置換テスト"""

    def test_checkbox_preserved(self, build_mod):
        md = textwrap.dedent("""\
        ---
        description: test
        ---

        - [ ] タスクA
        - [x] タスクB
        """)
        translations = {
            "body.li.0": "Task A",
            "body.li.1": "Task B",
        }
        result, _, _ = build_mod.apply_translations_to_md(md, translations, "en")
        assert "- [ ] Task A" in result
        assert "- [x] Task B" in result


class TestNoFrontmatter:
    """frontmatter なしの MD"""

    def test_body_only(self, build_mod):
        md = "# 見出し\n\n段落テキスト。\n"
        translations = {
            "body.h1.0": "Heading",
            "body.p.0": "Paragraph text.",
        }
        result, applied, _ = build_mod.apply_translations_to_md(md, translations, "en")
        assert "# Heading" in result
        assert "Paragraph text." in result
        assert applied == 2


# ===========================================================================
# TestReplaceAskqJson — 単体テスト
# ===========================================================================

class TestReplaceAskqJson:
    def test_schema_a(self, build_mod):
        json_text = json.dumps({
            "title": "タイトル",
            "questions": [{"id": "q1", "prompt": "質問", "options": [{"id": "o1", "label": "ラベル"}]}],
        }, ensure_ascii=False)
        translations = {
            "body.askq.0.title": "Title",
            "body.askq.0.questions.0.prompt": "Question",
            "body.askq.0.questions.0.options.0.label": "Label",
        }
        result, count = build_mod._replace_askq_json(json_text, translations, "body.askq.0")
        data = json.loads(result)
        assert data["title"] == "Title"
        assert data["questions"][0]["prompt"] == "Question"
        assert data["questions"][0]["options"][0]["label"] == "Label"
        assert data["questions"][0]["id"] == "q1"  # id 不変
        assert count == 3

    def test_malformed_json(self, build_mod):
        result, count = build_mod._replace_askq_json("{broken", {}, "body.askq.0")
        assert result == "{broken"
        assert count == 0

    def test_no_matching_keys(self, build_mod):
        json_text = json.dumps({"title": "タイトル", "questions": []}, ensure_ascii=False)
        result, count = build_mod._replace_askq_json(json_text, {}, "body.askq.0")
        # 翻訳なし → 元の JSON がそのまま返る
        assert result == json_text
        assert count == 0


# ===========================================================================
# TestReplaceFrontmatter
# ===========================================================================

class TestReplaceFrontmatter:
    def test_string_field(self, build_mod):
        fm = ['description: "元の説明"', 'level: beginner']
        result = build_mod._replace_frontmatter(fm, {"frontmatter.description": "New description"})
        assert any("New description" in line for line in result)
        assert any("beginner" in line for line in result)

    def test_list_field_inline(self, build_mod):
        fm = ['prerequisites: ["前提A", "前提B"]']
        result = build_mod._replace_frontmatter(fm, {
            "frontmatter.prerequisites.0": "Prereq A",
            "frontmatter.prerequisites.1": "Prereq B",
        })
        joined = " ".join(result)
        assert "Prereq A" in joined
        assert "Prereq B" in joined

    def test_no_translation_keeps_original(self, build_mod):
        fm = ['description: "元の説明"']
        result = build_mod._replace_frontmatter(fm, {})
        assert result == fm

    def test_double_quote_escaped(self, build_mod):
        """P1-3: 翻訳テキスト内のダブルクォートがエスケープされる"""
        fm = ['description: "元の説明"']
        result = build_mod._replace_frontmatter(fm, {
            "frontmatter.description": 'He said "hello" to me',
        })
        assert result == ['description: "He said \\"hello\\" to me"']  # json.dumps 出力


# ===========================================================================
# TestBuildLang — 統合テスト
# ===========================================================================

class TestBuildLang:
    def test_output_dir_structure(self, build_mod, tmp_path):
        """dist/en/ にソースと同じ構造で出力される"""
        # ソースファイル作成
        src = tmp_path / ".cursor" / "commands" / "lesson" / "start-0-1.md"
        src.parent.mkdir(parents=True)
        src.write_text("# テスト\n\n段落。\n", encoding="utf-8")

        rel = ".cursor/commands/lesson/start-0-1.md"
        ja_data = {rel: {"body.h1.0": "テスト", "body.p.0": "段落。"}}
        en_data = {rel: {"body.h1.0": "Test", "body.p.0": "Paragraph."}}

        with patch.object(build_mod, "ROOT_DIR", tmp_path), \
             patch.object(build_mod, "DIST_DIR_ROOT", tmp_path / "dist"):
            built, applied, missing, skipped = build_mod.build_lang(
                "en", ja_data, en_data, verbose=True
            )

        assert built == 1
        assert applied > 0
        out = tmp_path / "dist" / "en" / rel
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert "# Test" in content
        assert "Paragraph." in content

    def test_skip_missing_translations(self, build_mod, tmp_path):
        src = tmp_path / "test.md"
        src.write_text("# テスト\n", encoding="utf-8")

        ja_data = {"test.md": {"body.h1.0": "テスト"}}
        en_data = {}  # 翻訳なし

        with patch.object(build_mod, "ROOT_DIR", tmp_path), \
             patch.object(build_mod, "DIST_DIR_ROOT", tmp_path / "dist"):
            built, applied, missing, skipped = build_mod.build_lang(
                "en", ja_data, en_data, verbose=True
            )

        assert skipped == 1
        assert built == 0

    def test_dry_run_no_write(self, build_mod, tmp_path):
        src = tmp_path / "test.md"
        src.write_text("# テスト\n", encoding="utf-8")

        ja_data = {"test.md": {"body.h1.0": "テスト"}}
        en_data = {"test.md": {"body.h1.0": "Test"}}

        with patch.object(build_mod, "ROOT_DIR", tmp_path), \
             patch.object(build_mod, "DIST_DIR_ROOT", tmp_path / "dist"):
            built, _, _, _ = build_mod.build_lang(
                "en", ja_data, en_data, dry_run=True
            )

        assert built == 1
        assert not (tmp_path / "dist" / "en" / "test.md").exists()

    def test_clean_removes_old(self, build_mod, tmp_path):
        src = tmp_path / "test.md"
        src.write_text("# テスト\n", encoding="utf-8")

        old_file = tmp_path / "dist" / "en" / "old.md"
        old_file.parent.mkdir(parents=True)
        old_file.write_text("old content")

        ja_data = {"test.md": {"body.h1.0": "テスト"}}
        en_data = {"test.md": {"body.h1.0": "Test"}}

        with patch.object(build_mod, "ROOT_DIR", tmp_path), \
             patch.object(build_mod, "DIST_DIR_ROOT", tmp_path / "dist"):
            build_mod.build_lang("en", ja_data, en_data, clean=True)

        assert not old_file.exists()
        assert (tmp_path / "dist" / "en" / "test.md").exists()


# ===========================================================================
# TestLoadLocale
# ===========================================================================

class TestLoadLocale:
    def test_loads_existing(self, build_mod, tmp_path):
        data = {"file.md": {"body.h1.0": "test"}}
        path = tmp_path / "locales" / "md" / "en.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(data), encoding="utf-8")

        with patch.object(build_mod, "MD_LOCALES_DIR", tmp_path / "locales" / "md"):
            result = build_mod.load_locale("en")
        assert result == data

    def test_missing_returns_empty(self, build_mod, tmp_path):
        with patch.object(build_mod, "MD_LOCALES_DIR", tmp_path / "locales" / "md"):
            result = build_mod.load_locale("xx")
        assert result == {}

    def test_malformed_json_returns_empty(self, build_mod, tmp_path):
        path = tmp_path / "locales" / "md" / "bad.json"
        path.parent.mkdir(parents=True)
        path.write_text("{broken json", encoding="utf-8")

        with patch.object(build_mod, "MD_LOCALES_DIR", tmp_path / "locales" / "md"):
            result = build_mod.load_locale("bad")
        assert result == {}


# ===========================================================================
# TestUrlRewrite
# ===========================================================================

class TestUrlRewrite:
    def test_ja_url_in_frontmatter(self, build_mod):
        md = textwrap.dedent("""\
        ---
        description: "https://ai-agent.camp/ja/course/module-0"
        ---

        テスト。
        """)
        translations = {
            "frontmatter.description": "https://ai-agent.camp/ja/course/module-0",
        }
        result, _, _ = build_mod.apply_translations_to_md(md, translations, "en")
        assert "/en/course/module-0" in result
        assert "/ja/" not in result

    def test_ja_url_in_body(self, build_mod):
        md = textwrap.dedent("""\
        ---
        description: test
        ---

        Visit https://ai-agent.camp/ja/course/module-0 for details.
        """)
        translations = {
            "body.p.0": "Visit https://ai-agent.camp/ja/course/module-0 for details.",
        }
        result, _, _ = build_mod.apply_translations_to_md(md, translations, "es")
        assert "/es/course/module-0" in result


# ===========================================================================
# TestE2eRoundtrip — 抽出→ビルドのラウンドトリップ
# ===========================================================================

class TestE2eRoundtrip:
    def test_extract_then_build(self, build_mod, tmp_path):
        """抽出した ja.json をそのまま翻訳として使うと元と同じ構造になる"""
        from tools.i18n_extract_md import extract_texts_from_md

        keys = extract_texts_from_md(SAMPLE_MD)
        # ja キーをそのまま翻訳として使用（置換テスト）
        result, applied, missing = build_mod.apply_translations_to_md(
            SAMPLE_MD, keys, "ja"
        )
        # 適用数がキー数に近い（完全一致ではなく、構造保持確認）
        assert applied > 0
        # 見出しが存在
        assert "環境セットアップ確認" in result
        # コードフェンスが壊れていない
        assert '```json' in result
        assert '```python' in result
        assert 'print("hello")' in result

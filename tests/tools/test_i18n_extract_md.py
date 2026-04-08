"""
tests for tools/i18n_extract_md.py

MD テキスト抽出・翻訳のユニットテスト。
Codex sandbox 対応: API呼び出しテストは @pytest.mark.smoke で分離。
"""

import json
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import import_module_from_repo

# fresh import するために毎テストクラスで使う
_MOD_PATH = "tools/i18n_extract_md.py"


@pytest.fixture
def mod():
    return import_module_from_repo("i18n_extract_md", _MOD_PATH)


# ---------------------------------------------------------------------------
# テスト用 MD コンテンツ
# ---------------------------------------------------------------------------

SAMPLE_COMMAND_MD = textwrap.dedent("""\
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

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」と入力すると再開します。

- OS の判定（Mac / Windows）
- 不足しているツールがあればURLを案内

**AskQuestionの設定:**
```json
{
  "title": "Step 1: セットアップ開始",
  "questions": [{
    "id": "action",
    "prompt": "環境のセットアップを始めましょう。何をしますか？",
    "options": [
      {"id": "run_setup", "label": "セットアップを始める"},
      {"id": "already_done", "label": "既にセットアップ済み"}
    ]
  }]
}
```

### Step 2: 確認

通常の段落テキスト。
""")

SAMPLE_SKILL_MD = textwrap.dedent("""\
---
name: test-skill
description: Test skill for unit testing
version: 1.0.0
author: Test
dependencies: []
---

## トリガーワード
「テスト」「検証」

# Test Skill

## Workflow
1. Read `README.md`.
2. 短い説明を返す。
""")

SAMPLE_SIMPLE_MD = textwrap.dedent("""\
# シンプルな見出し

これはテスト段落です。

- リスト項目1
- リスト項目2
""")

SAMPLE_NO_FM_MD = textwrap.dedent("""\
# Frontmatterなし

本文テキスト。
""")

SAMPLE_EDGE_MD = textwrap.dedent("""\
---
description: "エッジケーステスト"
---

# 見出し

```python
# このコードは翻訳されない
print("hello")
```

通常テキスト

```json
{"not_askq": "これはAskQuestionではない"}
```

![代替テキスト](image.png)

- [ ] チェックボックス付きタスク
""")


# =============================================================================
# TestMdParser: ステートマシンのユニットテスト
# =============================================================================

class TestMdParser:
    """MD パーサーのステートマシンテスト"""

    def test_frontmatter_extraction(self, mod):
        """YAML frontmatter から description/duration/prerequisites を抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        assert "frontmatter.description" in keys
        assert "frontmatter.duration" in keys
        assert "frontmatter.prerequisites.0" in keys
        assert "frontmatter.prerequisites.1" in keys
        assert keys["frontmatter.duration"] == "約15分"

    def test_frontmatter_skips_non_translatable(self, mod):
        """name, tags, level, chapter はスキップ"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        # level, tags は frontmatter にあるがスキップされる
        assert not any(k.startswith("frontmatter.level") for k in keys)
        assert not any(k.startswith("frontmatter.tags") for k in keys)

    def test_no_frontmatter(self, mod):
        """frontmatter なしの MD も正常にパース"""
        keys = mod.extract_texts_from_md(SAMPLE_NO_FM_MD)
        assert "body.h1.0" in keys
        assert "body.p.0" in keys

    def test_heading_extraction(self, mod):
        """# H1, ## H2 のテキスト抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        assert "body.h1.0" in keys
        assert "Lesson 0-1" in keys["body.h1.0"]
        assert "body.h2.0" in keys

    def test_paragraph_extraction(self, mod):
        """段落テキストの抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        # "**AIが自動実行:**" を含む段落
        p_keys = [k for k in keys if k.startswith("body.p.")]
        assert len(p_keys) >= 1

    def test_list_item_extraction(self, mod):
        """- item の抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        li_keys = [k for k in keys if k.startswith("body.li.")]
        assert len(li_keys) >= 2

    def test_table_cell_extraction(self, mod):
        """| cell | の抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        table_keys = [k for k in keys if k.startswith("body.table.")]
        assert len(table_keys) >= 2  # 項目, 内容, ゴール, 環境確認

    def test_table_separator_skipped(self, mod):
        """テーブルセパレータ行 |---|---| はスキップ"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        # セパレータの "---" がキーとして出ていないことを確認
        for v in keys.values():
            assert v != "------"

    def test_blockquote_extraction(self, mod):
        """> テキスト の抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        bq_keys = [k for k in keys if k.startswith("body.blockquote.")]
        assert len(bq_keys) >= 1
        assert "ヒント" in keys[bq_keys[0]]

    def test_image_alt_extraction(self, mod):
        """![alt](url) から alt のみ抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_EDGE_MD)
        alt_keys = [k for k in keys if k.startswith("body.img_alt.")]
        assert len(alt_keys) >= 1
        assert keys[alt_keys[0]] == "代替テキスト"

    def test_code_fence_skipped(self, mod):
        """```python ... ``` 内はスキップ"""
        keys = mod.extract_texts_from_md(SAMPLE_EDGE_MD)
        # "print" や "hello" がキーの値に含まれないことを確認
        all_values = " ".join(keys.values())
        assert 'print("hello")' not in all_values

    def test_non_askq_json_skipped(self, mod):
        """AskQuestion でない JSON コードフェンスはスキップ"""
        keys = mod.extract_texts_from_md(SAMPLE_EDGE_MD)
        # "not_askq" がキーに含まれないことを確認
        all_values = " ".join(keys.values())
        assert "not_askq" not in all_values

    def test_askq_json_label_extracted(self, mod):
        """AskQuestion JSON の label を抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        askq_keys = [k for k in keys if "options" in k and "label" in k]
        assert len(askq_keys) >= 2
        labels = [keys[k] for k in askq_keys]
        assert "セットアップを始める" in labels

    def test_askq_json_prompt_extracted(self, mod):
        """AskQuestion JSON の prompt を抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        prompt_keys = [k for k in keys if ".prompt" in k and "askq" in k]
        assert len(prompt_keys) >= 1

    def test_askq_json_title_extracted(self, mod):
        """AskQuestion JSON の title を抽出"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        title_keys = [k for k in keys if ".title" in k and "askq" in k]
        assert len(title_keys) >= 1

    def test_askq_preserves_id(self, mod):
        """AskQuestion JSON の id はスキップ"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        # id フィールドは抽出されない
        assert not any(".id" in k for k in keys if "askq" in k)

    def test_askq_schema_b_extracted(self, mod):
        """Schema B: {"type":"AskQuestion", "question":..., "options":[...]}"""
        md = textwrap.dedent("""\
        ## 準備チェック

        ```json
        {
          "type": "AskQuestion",
          "question": "このレッスンの準備確認",
          "description": "開始前の条件チェック",
          "options": [
            {"label": "準備完了", "value": "ready"},
            {"label": "見直したい", "value": "review"}
          ]
        }
        ```
        """)
        keys = mod.extract_texts_from_md(md)
        askq_keys = {k: v for k, v in keys.items() if "askq" in k}
        assert any("question" in k for k in askq_keys), f"Missing question key in {askq_keys}"
        assert any("description" in k for k in askq_keys), f"Missing description key in {askq_keys}"
        labels = [v for k, v in askq_keys.items() if "label" in k]
        assert "準備完了" in labels
        assert "見直したい" in labels

    def test_askq_schema_b_hint_helptext_context(self, mod):
        """Schema B: hint, helpText, context フィールドも抽出"""
        md = textwrap.dedent("""\
        ```json
        {
          "type": "AskQuestion",
          "question": "質問テキスト",
          "hint": "ヒントテキスト",
          "helpText": "ヘルプテキスト",
          "context": "コンテキストテキスト",
          "options": [{"label": "選択肢", "value": "a"}]
        }
        ```
        """)
        keys = mod.extract_texts_from_md(md)
        askq_keys = {k: v for k, v in keys.items() if "askq" in k}
        assert any(k.endswith(".hint") for k in askq_keys), f"Missing hint: {askq_keys}"
        assert any(k.endswith(".helpText") for k in askq_keys), f"Missing helpText: {askq_keys}"
        assert any(k.endswith(".context") for k in askq_keys), f"Missing context: {askq_keys}"

    def test_askq_blank_line_before_json(self, mod):
        """ヒント行と ```json の間に空行があっても検出される"""
        md = textwrap.dedent("""\
        **AskQuestionの設定:**

        ```json
        {
          "title": "テスト",
          "questions": [{
            "id": "q1",
            "prompt": "質問テキスト",
            "options": [{"id": "a", "label": "選択肢A"}]
          }]
        }
        ```
        """)
        keys = mod.extract_texts_from_md(md)
        askq_keys = [k for k in keys if "askq" in k]
        assert len(askq_keys) >= 2, f"Expected AskQ keys but got: {askq_keys}"

    def test_askq_no_hint_but_detected_by_content(self, mod):
        """ヒント行なしでもJSON内容からAskQuestionを自動検出"""
        md = textwrap.dedent("""\
        ```json
        {
          "type": "AskQuestion",
          "question": "自動検出テスト",
          "options": [{"label": "はい", "value": "yes"}]
        }
        ```
        """)
        keys = mod.extract_texts_from_md(md)
        askq_keys = [k for k in keys if "askq" in k]
        assert len(askq_keys) >= 2

    def test_askq_malformed_json(self, mod):
        """不正 JSON は安全にスキップ"""
        md = textwrap.dedent("""\
        **AskQuestionの設定:**
        ```json
        { invalid json here
        ```
        """)
        keys = mod.extract_texts_from_md(md)
        askq_keys = [k for k in keys if "askq" in k]
        assert len(askq_keys) == 0

    def test_horizontal_rule_skipped(self, mod):
        """--- 水平線はスキップ"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        for v in keys.values():
            assert v != "---"

    def test_checkbox_list_item(self, mod):
        """- [ ] チェックボックス付きリスト"""
        keys = mod.extract_texts_from_md(SAMPLE_EDGE_MD)
        li_keys = [k for k in keys if k.startswith("body.li.")]
        li_values = [keys[k] for k in li_keys]
        assert any("チェックボックス" in v for v in li_values)
        # チェックボックスマーカー自体は含まれない
        assert not any(v.startswith("[ ]") for v in li_values)


# =============================================================================
# TestInlineCode: インラインコード保護
# =============================================================================

class TestInlineCode:
    """インラインコードのプレースホルダー変換テスト"""

    def test_inline_code_placeholder(self, mod):
        """``code`` → {{code_0}} 変換"""
        text = "Run `uv run python test.py` now"
        protected, codes = mod._protect_inline_code(text)
        assert "{{code_0}}" in protected
        assert "`uv run python test.py`" in codes.values()

    def test_multiple_inline_codes(self, mod):
        """1行に複数の ``code`` がある場合"""
        text = "Use `cmd1` and `cmd2` together"
        protected, codes = mod._protect_inline_code(text)
        assert "{{code_0}}" in protected
        assert "{{code_1}}" in protected
        assert len(codes) == 2

    def test_placeholder_roundtrip(self, mod):
        """{{code_N}} → 元の ``code`` に復元可能"""
        original = "Run `uv run python test.py` and `echo hello`"
        protected, codes = mod._protect_inline_code(original)
        restored = mod._restore_inline_code(protected, codes)
        assert restored == original

    def test_no_inline_code(self, mod):
        """インラインコードなしのテキスト"""
        text = "No inline code here"
        protected, codes = mod._protect_inline_code(text)
        assert protected == text
        assert len(codes) == 0

    def test_paragraph_has_placeholder(self, mod):
        """抽出されたキーにプレースホルダーが含まれる"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        # "**AIが自動実行:** `...` を実行して" → {{code_0}} を含むはず
        p_values = [keys[k] for k in keys if k.startswith("body.p.")]
        has_placeholder = any("{{code_" in v for v in p_values)
        assert has_placeholder


# =============================================================================
# TestKeyGeneration: キー生成
# =============================================================================

class TestKeyGeneration:

    def test_key_format(self, mod):
        """キーが frontmatter.X / body.tag.N 形式"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        for key in keys:
            assert key.startswith("frontmatter.") or key.startswith("body."), f"Unexpected key: {key}"

    def test_key_uniqueness(self, mod):
        """同一ファイル内でキーが重複しない"""
        keys = mod.extract_texts_from_md(SAMPLE_COMMAND_MD)
        key_list = list(keys.keys())
        assert len(key_list) == len(set(key_list))

    def test_real_file_extraction(self, mod):
        """start-0-1.md を実際にパースしてキーが抽出される"""
        from i18n_common import COMMANDS_DIR
        real_file = COMMANDS_DIR / "lesson" / "start-0-1.md"
        if not real_file.exists():
            pytest.skip("start-0-1.md not found")
        content = real_file.read_text(encoding="utf-8")
        keys = mod.extract_texts_from_md(content)
        # 最低限のキーが抽出される
        assert len(keys) >= 20
        assert "frontmatter.description" in keys

    def test_skill_extraction(self, mod):
        """SKILL.md からキーが抽出される"""
        keys = mod.extract_texts_from_md(SAMPLE_SKILL_MD)
        assert "frontmatter.description" in keys
        assert "body.h2.0" in keys  # トリガーワード
        assert "body.h1.0" in keys  # Test Skill


# =============================================================================
# TestExtractAll: 一括抽出
# =============================================================================

class TestExtractAll:

    def test_extract_all_with_files(self, mod, tmp_path):
        """複数ファイルの一括抽出"""
        (tmp_path / "a.md").write_text(SAMPLE_SIMPLE_MD, encoding="utf-8")
        (tmp_path / "b.md").write_text(SAMPLE_SKILL_MD, encoding="utf-8")

        files = [tmp_path / "a.md", tmp_path / "b.md"]
        data = mod.extract_all(files)
        assert len(data) == 2

    def test_extract_all_empty(self, mod):
        """空リストでも正常"""
        data = mod.extract_all([])
        assert data == {}

    def test_extract_all_skips_unreadable(self, mod, tmp_path):
        """読み取れないファイルはスキップ"""
        nonexistent = tmp_path / "ghost.md"
        data = mod.extract_all([nonexistent])
        assert data == {}


# =============================================================================
# TestTranslateMd: 翻訳（API モック）
# =============================================================================

class TestTranslateMd:

    def test_translate_batch(self, mod, mock_gemini_response):
        """バッチ翻訳が正しい JSON を返す"""
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.text = '{"body.h1.0": "Environment Setup Check"}'
        mock_client.models.generate_content.return_value = mock_resp

        result = mod.translate_batch(mock_client, {"body.h1.0": "環境セットアップ確認"}, "en", "gemini-2.0-flash")
        assert result["body.h1.0"] == "Environment Setup Check"

    def test_translate_batch_fallback(self, mod):
        """翻訳失敗時にフォールバック"""
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.text = "invalid json"
        mock_client.models.generate_content.return_value = mock_resp

        original = {"body.h1.0": "テスト"}
        result = mod.translate_batch(mock_client, original, "en", "gemini-2.0-flash")
        assert result == original

    def test_translate_file_texts_batching(self, mod):
        """バッチ分割が正しく動作"""
        mock_client = MagicMock()
        mock_resp = MagicMock()

        texts = {f"key{i}": f"テスト{i}" for i in range(5)}

        def side_effect(*args, **kwargs):
            prompt = args[1][0] if len(args) > 1 else kwargs.get("contents", [[""]])[0]
            # バッチサイズ2で3回呼ばれるはず
            resp = MagicMock()
            resp.text = json.dumps({f"key{i}": f"test{i}" for i in range(5)})
            return resp

        mock_client.models.generate_content.side_effect = side_effect

        with patch("i18n_extract_md.time"):
            result = mod.translate_file_texts(mock_client, texts, "en", "gemini-2.0-flash", batch_size=2)

        assert mock_client.models.generate_content.call_count == 3

    def test_translate_prompt_preserves_placeholders(self, mod):
        """翻訳プロンプトに {{code_N}} 保持ルールが含まれる"""
        prompt = mod._build_md_translation_prompt(
            {"body.p.0": "Run {{code_0}} now"}, "en", "English"
        )
        assert "{{code_N}}" in prompt or "code_0" in prompt


# =============================================================================
# TestScopeFilter: スコープフィルタ
# =============================================================================

class TestScopeFilter:

    def test_scope_commands(self, mod):
        """--scope commands で skills を除外"""
        files = mod._get_files("commands")
        for f in files:
            assert "skills" not in str(f) or ".cursor" in str(f) or ".claude" in str(f)

    def test_scope_skills(self, mod):
        """--scope skills で commands を除外"""
        files = mod._get_files("skills")
        for f in files:
            assert "SKILL.md" in f.name

    def test_scope_none(self, mod):
        """scope なしで全ファイル"""
        all_files = mod._get_files(None)
        cmd_files = mod._get_files("commands")
        skill_files = mod._get_files("skills")
        assert len(all_files) == len(cmd_files) + len(skill_files)


# =============================================================================
# TestCheckDrift: --check モード
# =============================================================================

class TestCheckDrift:

    def test_check_no_ja_json(self, mod, tmp_path, monkeypatch):
        """ja.json 不存在で exit 1"""
        monkeypatch.setattr(mod, "MD_LOCALES_DIR", tmp_path)
        result = mod.check_drift({"file.md": {"key": "val"}})
        assert result == 1

    def test_check_up_to_date(self, mod, tmp_path, monkeypatch):
        """ja.json が最新なら exit 0"""
        monkeypatch.setattr(mod, "MD_LOCALES_DIR", tmp_path)
        data = {"file.md": {"body.h1.0": "テスト"}}
        (tmp_path / "ja.json").write_text(json.dumps(data), encoding="utf-8")
        result = mod.check_drift(data)
        assert result == 0

    def test_check_drift_detected(self, mod, tmp_path, monkeypatch):
        """差分があれば exit 1"""
        monkeypatch.setattr(mod, "MD_LOCALES_DIR", tmp_path)
        old_data = {"file.md": {"body.h1.0": "古いテキスト"}}
        new_data = {"file.md": {"body.h1.0": "新しいテキスト"}}
        (tmp_path / "ja.json").write_text(json.dumps(old_data), encoding="utf-8")
        result = mod.check_drift(new_data)
        assert result == 1

    def test_check_new_file_detected(self, mod, tmp_path, monkeypatch):
        """新規ファイルが検出される"""
        monkeypatch.setattr(mod, "MD_LOCALES_DIR", tmp_path)
        old_data = {"file.md": {"body.h1.0": "テスト"}}
        new_data = {"file.md": {"body.h1.0": "テスト"}, "new.md": {"body.h1.0": "新規"}}
        (tmp_path / "ja.json").write_text(json.dumps(old_data), encoding="utf-8")
        result = mod.check_drift(new_data)
        assert result == 1

    def test_check_scoped_ignores_other_scope(self, mod, tmp_path, monkeypatch):
        """--check --scope: 他スコープのファイルは removed 扱いしない"""
        monkeypatch.setattr(mod, "MD_LOCALES_DIR", tmp_path)
        full_data = {
            ".cursor/commands/a.md": {"body.h1.0": "コマンド"},
            "skills/b/SKILL.md": {"body.h1.0": "スキル"},
        }
        (tmp_path / "ja.json").write_text(json.dumps(full_data), encoding="utf-8")
        # commands だけスコープ → skills が消えても OK
        scoped_data = {".cursor/commands/a.md": {"body.h1.0": "コマンド"}}
        result = mod.check_drift(scoped_data, scoped=True)
        assert result == 0

    def test_check_scoped_detects_deleted_in_scope(self, mod, tmp_path, monkeypatch):
        """--check --scope: スコープ内で削除されたファイルを検出"""
        monkeypatch.setattr(mod, "MD_LOCALES_DIR", tmp_path)
        full_data = {
            ".cursor/commands/a.md": {"body.h1.0": "A"},
            ".cursor/commands/deleted.md": {"body.h1.0": "削除済み"},
            "skills/b/SKILL.md": {"body.h1.0": "スキル"},
        }
        (tmp_path / "ja.json").write_text(json.dumps(full_data), encoding="utf-8")
        # commands スコープで deleted.md がなくなった
        scoped_data = {".cursor/commands/a.md": {"body.h1.0": "A"}}
        result = mod.check_drift(scoped_data, scoped=True)
        assert result == 1  # drift detected


# =============================================================================
# TestPrintStats: 統計表示
# =============================================================================

class TestMergeLocaleData:

    def test_merge_new_file(self, mod, tmp_path):
        """既存 JSON に新ファイルが追加される"""
        existing = {"a.md": {"key": "val"}}
        path = tmp_path / "test.json"
        path.write_text(json.dumps(existing), encoding="utf-8")
        new_data = {"b.md": {"key2": "val2"}}
        merged = mod._merge_locale_data(path, new_data)
        assert "a.md" in merged
        assert "b.md" in merged

    def test_merge_overwrites_existing(self, mod, tmp_path):
        """既存エントリが上書きされる"""
        existing = {"a.md": {"key": "old"}}
        path = tmp_path / "test.json"
        path.write_text(json.dumps(existing), encoding="utf-8")
        new_data = {"a.md": {"key": "new"}}
        merged = mod._merge_locale_data(path, new_data)
        assert merged["a.md"]["key"] == "new"

    def test_merge_no_existing_file(self, mod, tmp_path):
        """既存ファイルなし → new_data そのまま"""
        path = tmp_path / "nonexistent.json"
        new_data = {".cursor/commands/a.md": {"key": "val"}}
        merged = mod._merge_locale_data(path, new_data)
        assert merged == new_data

    def test_merge_purges_deleted_in_scope(self, mod, tmp_path):
        """スコープ内で削除されたファイルがパージされる"""
        existing = {
            ".cursor/commands/a.md": {"key": "A"},
            ".cursor/commands/deleted.md": {"key": "削除"},
            "skills/b/SKILL.md": {"key": "スキル"},
        }
        path = tmp_path / "test.json"
        path.write_text(json.dumps(existing), encoding="utf-8")
        # commands スコープで a.md だけ
        new_data = {".cursor/commands/a.md": {"key": "A-new"}}
        merged = mod._merge_locale_data(path, new_data)
        assert ".cursor/commands/a.md" in merged
        assert ".cursor/commands/deleted.md" not in merged  # パージ
        assert "skills/b/SKILL.md" in merged  # 他スコープは維持


class TestPrintStats:

    def test_print_stats_no_error(self, mod, capsys):
        """統計表示がエラーなく完了"""
        data = {
            "file.md": {
                "frontmatter.description": "desc",
                "body.h1.0": "heading",
                "body.p.0": "paragraph",
                "body.table.0.r0.c0": "cell",
                "body.li.0": "list",
                "body.blockquote.0": "quote",
                "body.askq.0.title": "title",
            }
        }
        mod.print_stats(data)
        captured = capsys.readouterr()
        assert "Files: 1" in captured.out
        assert "Total keys: 7" in captured.out

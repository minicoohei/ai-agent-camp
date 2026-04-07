"""verify_commands.py の拡張ユニットテスト - カバレッジ向上"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestValidateFileStructureExtended:
    def test_missing_required_sections(self, tmp_path):
        from verify_commands import validate_file_structure
        content = '''---
description: "test"
---

## Some random section
Nothing relevant.
'''
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        result = validate_file_structure(f)
        assert len(result["errors"]) > 0

    def test_missing_frontmatter_description(self, tmp_path):
        from verify_commands import validate_file_structure
        content = '''---
title: "no description"
---

## 📍 今あなたがやっていること
## 🚀 Step 1
```
code
```
## ✅ チェックポイント
## ➡️ 次のステップ
`/start-1-2`
'''
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        result = validate_file_structure(f)
        assert any("frontmatter" in e.lower() for e in result["errors"])

    def test_step_without_code_block_warning(self, tmp_path):
        from verify_commands import validate_file_structure
        content = '''---
description: "test lesson"
---

## 📍 今あなたがやっていること
test

## 🚀 Step 1
No code block here, just text.

## 🚀 Step 2
Also no code block.

## ✅ チェックポイント
done

## ➡️ 次のステップ
`/start-1-2`
'''
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        result = validate_file_structure(f)
        assert any("code block" in w.lower() for w in result["warnings"])

    def test_missing_optional_section_warning(self, tmp_path):
        from verify_commands import validate_file_structure
        content = '''---
description: "test lesson"
---

## 📍 今あなたがやっていること
test

## 🚀 Step 1
```
code
```

## ✅ チェックポイント
done

## ➡️ 次のステップ
`/start-1-2`
'''
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        result = validate_file_structure(f)
        assert any("optional" in w.lower() for w in result["warnings"])

    def test_missing_next_step_reference(self, tmp_path):
        from verify_commands import validate_file_structure
        content = '''---
description: "test lesson"
---

## 📍 今あなたがやっていること
test

## 🚀 Step 1
```
code
```

## ✅ チェックポイント
done

## ➡️ 次のステップ
No reference here.
'''
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        result = validate_file_structure(f)
        assert any("next step" in w.lower() for w in result["warnings"])

    def test_troubleshooting_few_items(self, tmp_path):
        from verify_commands import validate_file_structure
        content = '''---
description: "test lesson"
---

## 📍 今あなたがやっていること
test

## 🚀 Step 1
```
code
```

## ⚠️ よくあるトラブルと解決方法
### トラブル1: エラーA
Fix A

## ✅ チェックポイント
done

## ➡️ 次のステップ
`/start-1-2`
'''
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        result = validate_file_structure(f)
        assert any("troubleshooting" in w.lower() for w in result["warnings"])

    def test_read_error(self, tmp_path):
        from verify_commands import validate_file_structure
        f = tmp_path / "nonexistent.md"
        result = validate_file_structure(f)
        assert len(result["errors"]) > 0
        assert "Failed to read" in result["errors"][0]


class TestValidateLinkReferences:
    def test_valid_tool_reference(self, tmp_path):
        from verify_commands import validate_link_references
        content = "Run `python tools/verify_commands.py` to check."
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        with patch("verify_commands.PROJECT_ROOT", tmp_path):
            # Create the referenced tool
            tools_dir = tmp_path / "tools"
            tools_dir.mkdir()
            (tools_dir / "verify_commands.py").write_text("pass")
            result = validate_link_references(f)
        assert len(result["errors"]) == 0

    def test_missing_tool_reference(self, tmp_path):
        from verify_commands import validate_link_references
        content = "Run `python tools/nonexistent_tool.py` to check."
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        with patch("verify_commands.PROJECT_ROOT", tmp_path):
            result = validate_link_references(f)
        assert len(result["errors"]) > 0
        assert "nonexistent_tool.py" in result["errors"][0]

    def test_no_references(self, tmp_path):
        from verify_commands import validate_link_references
        content = "Just a plain text lesson with no tool references."
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        with patch("verify_commands.PROJECT_ROOT", tmp_path):
            result = validate_link_references(f)
        assert len(result["errors"]) == 0

    def test_read_error(self, tmp_path):
        from verify_commands import validate_link_references
        f = tmp_path / "nonexistent.md"
        result = validate_link_references(f)
        assert len(result["errors"]) > 0


class TestValidateAllCommands:
    def test_runs_without_files(self, tmp_path):
        from verify_commands import validate_all_commands
        cmd_dir = tmp_path / ".cursor" / "commands" / "lesson"
        cmd_dir.mkdir(parents=True)
        with patch("verify_commands.COMMANDS_DIRS", [cmd_dir]):
            results = validate_all_commands()
        assert results["total_files"] == 0
        assert results["passed"] == 0
        assert results["failed"] == 0

    def test_with_valid_command_file(self, tmp_path):
        from verify_commands import validate_all_commands
        cmd_dir = tmp_path / "commands"
        cmd_dir.mkdir()
        content = '''---
description: "Lesson 0-1"
---

## 📍 今あなたがやっていること
test

## 🚀 Step 1
```
code
```

## ⚠️ よくあるトラブル
### トラブル1: A
### トラブル2: B
### トラブル3: C

## ✅ チェックポイント
done

## ➡️ 次のステップ
`/start-0-2`
'''
        (cmd_dir / "start-0-1.md").write_text(content, encoding="utf-8")
        with patch("verify_commands.COMMANDS_DIRS", [cmd_dir]):
            results = validate_all_commands()
        assert results["total_files"] >= 1

    def test_with_failing_file(self, tmp_path):
        from verify_commands import validate_all_commands
        cmd_dir = tmp_path / "commands"
        cmd_dir.mkdir()
        (cmd_dir / "start-0-1.md").write_text("bad content", encoding="utf-8")
        with patch("verify_commands.COMMANDS_DIRS", [cmd_dir]):
            results = validate_all_commands()
        if results["total_files"] > 0:
            assert results["failed"] >= 1


class TestValidateLinkReferencesExtended:
    """validate_link_references の追加テスト (lines 86-108)"""

    def test_skill_reference_exists(self, tmp_path):
        from verify_commands import validate_link_references
        content = "Use the check-inboxスキル to process email."
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        with patch("verify_commands.PROJECT_ROOT", tmp_path):
            skill_dir = tmp_path / ".claude" / "skills" / "check-inbox"
            skill_dir.mkdir(parents=True)
            result = validate_link_references(f)
        assert len(result["errors"]) == 0

    def test_skill_reference_missing(self, tmp_path):
        from verify_commands import validate_link_references
        content = "Use the missing-skillスキル to do something."
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        with patch("verify_commands.PROJECT_ROOT", tmp_path):
            result = validate_link_references(f)
        assert any("missing-skill" in e for e in result["errors"])


class TestValidateAllCommandsExtended:
    """validate_all_commands の追加テスト (lines 122-186)"""

    def test_module_mapping_coverage(self, tmp_path):
        """各モジュールのマッピングが正しく動作する"""
        from verify_commands import validate_all_commands
        cmd_dir = tmp_path / "commands"
        cmd_dir.mkdir()

        # Create files for multiple modules to exercise different branches
        content = '''---
description: "Test lesson"
---

## 📍 今あなたがやっていること
test

## 🚀 Step 1
```
code
```

## ✅ チェックポイント
done

## ➡️ 次のステップ
`/start-0-2`
'''
        for m in range(12):
            for l in range(1, 3):
                (cmd_dir / f"start-{m}-{l}.md").write_text(content, encoding="utf-8")

        with patch("verify_commands.COMMANDS_DIRS", [cmd_dir]):
            results = validate_all_commands()
        assert results["total_files"] > 0
        assert results["passed"] > 0

    def test_validate_all_commands_multiple_dirs(self, tmp_path):
        """複数のコマンドディレクトリをスキャン"""
        from verify_commands import validate_all_commands
        dir1 = tmp_path / "cursor_commands"
        dir1.mkdir()
        dir2 = tmp_path / "claude_commands"
        dir2.mkdir()

        content = '''---
description: "Test"
---

## 📍 今あなたがやっていること
test

## 🚀 Step 1
```code```

## ✅ チェック
done

## ➡️ 次
`/start-0-2`
'''
        # File in first dir
        (dir1 / "start-0-1.md").write_text(content, encoding="utf-8")

        with patch("verify_commands.COMMANDS_DIRS", [dir1, dir2]):
            results = validate_all_commands()
        assert results["total_files"] >= 1


class TestMainFunction:
    """main() 関数のテスト (lines 230-248)"""

    def test_main_runs(self, tmp_path):
        from verify_commands import main
        cmd_dir = tmp_path / "commands"
        cmd_dir.mkdir()

        with patch("verify_commands.COMMANDS_DIRS", [cmd_dir]), \
             patch("verify_commands.RESULTS_DIR", tmp_path):
            result = main()
        assert result == 0  # 0 failures

    def test_main_with_failures(self, tmp_path):
        from verify_commands import main
        cmd_dir = tmp_path / "commands"
        cmd_dir.mkdir()
        (cmd_dir / "start-0-1.md").write_text("bad content", encoding="utf-8")

        with patch("verify_commands.COMMANDS_DIRS", [cmd_dir]), \
             patch("verify_commands.RESULTS_DIR", tmp_path):
            result = main()
        assert result >= 1


class TestGenerateReportExtended:
    """generate_report の追加テスト (lines 191-225)"""

    def test_report_with_warnings(self, tmp_path):
        from verify_commands import generate_report
        results = {
            "timestamp": "2024-01-01T00:00:00",
            "total_files": 1,
            "passed": 1,
            "failed": 0,
            "files": {
                "start-0-1": {
                    "status": "PASSED",
                    "errors": [],
                    "warnings": ["Warning 1", "Warning 2"],
                },
            },
        }
        with patch("verify_commands.RESULTS_DIR", tmp_path):
            json_file, summary_file = generate_report(results)
        content = summary_file.read_text()
        assert "FAILURES" not in content  # No failures section

    def test_report_multiple_failures(self, tmp_path):
        from verify_commands import generate_report
        results = {
            "timestamp": "2024-01-01T00:00:00",
            "total_files": 3,
            "passed": 1,
            "failed": 2,
            "files": {
                "start-0-1": {
                    "status": "PASSED",
                    "errors": [],
                    "warnings": [],
                },
                "start-0-2": {
                    "status": "FAILED",
                    "errors": ["Missing section A"],
                    "warnings": ["Warning"],
                },
                "start-0-3": {
                    "status": "FAILED",
                    "errors": ["Missing section B", "Missing section C"],
                    "warnings": [],
                },
            },
        }
        with patch("verify_commands.RESULTS_DIR", tmp_path):
            json_file, summary_file = generate_report(results)
        content = summary_file.read_text()
        assert "start-0-2" in content
        assert "start-0-3" in content
        assert "Missing section B" in content


class TestGenerateReport:
    def test_generates_files(self, tmp_path):
        from verify_commands import generate_report
        results = {
            "timestamp": "2024-01-01T00:00:00",
            "total_files": 2,
            "passed": 1,
            "failed": 1,
            "files": {
                "start-0-1": {
                    "status": "PASSED",
                    "errors": [],
                    "warnings": ["minor warning"],
                },
                "start-0-2": {
                    "status": "FAILED",
                    "errors": ["Missing section"],
                    "warnings": [],
                },
            },
        }
        with patch("verify_commands.RESULTS_DIR", tmp_path):
            json_file, summary_file = generate_report(results)
        assert json_file.exists()
        assert summary_file.exists()
        summary_content = summary_file.read_text()
        assert "Passed" in summary_content
        assert "FAILURES" in summary_content

    def test_report_with_no_failures(self, tmp_path):
        from verify_commands import generate_report
        results = {
            "timestamp": "2024-01-01T00:00:00",
            "total_files": 1,
            "passed": 1,
            "failed": 0,
            "files": {
                "start-0-1": {
                    "status": "PASSED",
                    "errors": [],
                    "warnings": [],
                },
            },
        }
        with patch("verify_commands.RESULTS_DIR", tmp_path):
            json_file, summary_file = generate_report(results)
        assert json_file.exists()
        json_data = json.loads(json_file.read_text())
        assert json_data["passed"] == 1

"""verify_commands.py の単体テスト"""
import pytest
from pathlib import Path


class TestImport:
    def test_import_module(self):
        import verify_commands
        assert hasattr(verify_commands, 'validate_file_structure')
        assert hasattr(verify_commands, 'validate_link_references')


class TestValidateFileStructure:
    def test_valid_file(self, tmp_path):
        from verify_commands import validate_file_structure
        content = '''---
description: "テストレッスン"
---

## 📍 今あなたがやっていること
テスト中です

## 🚀 Step 1
```
python test.py
```

## ⚠️ よくあるトラブルと解決方法
### トラブル1: エラーA
### トラブル2: エラーB
### トラブル3: エラーC

## ✅ チェックポイント
- [ ] 完了

## ➡️ 次のステップ
`/start-1-2` に進む
'''
        test_file = tmp_path / "start-1-1.md"
        test_file.write_text(content, encoding="utf-8")
        result = validate_file_structure(test_file)
        assert len(result["errors"]) == 0

    def test_missing_frontmatter(self, tmp_path):
        from verify_commands import validate_file_structure
        content = "# No frontmatter"
        test_file = tmp_path / "bad.md"
        test_file.write_text(content, encoding="utf-8")
        result = validate_file_structure(test_file)
        assert len(result["errors"]) > 0

    def test_nonexistent_file(self, tmp_path):
        from verify_commands import validate_file_structure
        result = validate_file_structure(tmp_path / "nonexistent.md")
        assert len(result["errors"]) > 0

    @pytest.mark.parametrize(
        ("suffix", "headings"),
        [
            (
                ".en.md",
                """## What You'll Do
### Step 1: Run the check
## Checkpoint
## Next Steps""",
            ),
            (
                ".es.md",
                """## Lo que hará en esta sesión
### Paso 1: Ejecutar la verificación
## Punto de verificación
## Siguientes pasos""",
            ),
        ],
    )
    def test_localized_required_sections(self, tmp_path, suffix, headings):
        from verify_commands import validate_file_structure

        test_file = tmp_path / f"start-1-1{suffix}"
        test_file.write_text(
            f'''---
description: "Localized lesson"
---

{headings}
''',
            encoding="utf-8",
        )

        result = validate_file_structure(test_file)

        assert result["errors"] == []

    @pytest.mark.parametrize(
        ("filename", "headings", "expected_layout"),
        [
            (
                "start-99-42.en.md",
                "## What You'll Do\n## Prerequisites\n## Goals\n## Next Steps",
                "compact",
            ),
            (
                "start-88-7.es.md",
                "## Qué cubre esta lección\n## Cómo avanzar\n## Pistas\n## Enlaces de referencia",
                "reference",
            ),
        ],
    )
    def test_layout_profiles_are_detected_without_known_lesson_ids(
        self, tmp_path, filename, headings, expected_layout
    ):
        from verify_commands import layout_for_content, locale_for_path, validate_file_structure

        test_file = tmp_path / filename
        test_file.write_text(
            f'---\ndescription: "Profiled lesson"\n---\n\n{headings}\n',
            encoding="utf-8",
        )

        assert layout_for_content(headings, locale_for_path(test_file)) == expected_layout
        assert validate_file_structure(test_file)["errors"] == []

    def test_broken_reference_keeps_reference_profile(self, tmp_path):
        from verify_commands import layout_for_content, validate_file_structure

        headings = "## What this lesson covers\n## How to proceed"
        test_file = tmp_path / "start-99-99.en.md"
        test_file.write_text(
            f'---\ndescription: "Broken future reference"\n---\n\n{headings}\n',
            encoding="utf-8",
        )

        assert layout_for_content(headings, "en") == "reference"
        assert any("Reference" in error for error in validate_file_structure(test_file)["errors"])

    def test_full_layout_does_not_fall_back_when_checkpoint_is_missing(self, tmp_path):
        from verify_commands import validate_file_structure

        test_file = tmp_path / "start-1-1.en.md"
        test_file.write_text(
            '---\ndescription: "Broken full lesson"\n---\n\n'
            "## Step 1: Do work\n## Next Steps\n",
            encoding="utf-8",
        )

        assert validate_file_structure(test_file)["errors"]

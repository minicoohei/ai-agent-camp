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

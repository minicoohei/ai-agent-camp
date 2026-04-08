"""generate_all_images.py の単体テスト。

画像仕様データ構造、generate_image関数、CLIパース、dry-runモードを検証する。
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    return import_module_from_repo("generate_all_images", "tools/generate_all_images.py")


# ===========================================================================
# IMAGE_SPECS
# ===========================================================================

class TestImageSpecs:
    def test_foundation_has_specs(self, mod):
        assert "foundation" in mod.IMAGE_SPECS
        assert len(mod.IMAGE_SPECS["foundation"]) == 8

    def test_headers_has_specs(self, mod):
        assert "headers" in mod.IMAGE_SPECS
        assert len(mod.IMAGE_SPECS["headers"]) == 14

    def test_all_categories_exist(self, mod):
        expected = {"foundation", "headers", "concepts", "exercises", "portal"}
        assert set(mod.IMAGE_SPECS.keys()) == expected

    def test_spec_structure(self, mod):
        """各specが name, prompt, size を持つ"""
        for category, specs in mod.IMAGE_SPECS.items():
            for spec in specs:
                assert "name" in spec, f"{category} spec missing name"
                assert "prompt" in spec, f"{category}/{spec.get('name', '?')} missing prompt"
                assert "size" in spec, f"{category}/{spec.get('name', '?')} missing size"

    def test_unique_names_per_category(self, mod):
        """同一カテゴリ内で名前が重複しない"""
        for category, specs in mod.IMAGE_SPECS.items():
            names = [s["name"] for s in specs]
            assert len(names) == len(set(names)), f"Duplicate names in {category}"

    def test_size_format(self, mod):
        """sizeが 'WxH' 形式"""
        for category, specs in mod.IMAGE_SPECS.items():
            for spec in specs:
                parts = spec["size"].split("x")
                assert len(parts) == 2, f"Bad size format: {spec['size']}"
                assert parts[0].isdigit() and parts[1].isdigit()

    def test_prompt_not_empty(self, mod):
        for category, specs in mod.IMAGE_SPECS.items():
            for spec in specs:
                assert len(spec["prompt"]) > 10, f"Prompt too short: {spec['name']}"


# ===========================================================================
# generate_image
# ===========================================================================

class TestGenerateImage:
    def test_dry_run(self, mod, tmp_path, capsys):
        spec = {"name": "test-img", "prompt": "test prompt", "size": "100x100"}
        mod.generate_image(spec, tmp_path, dry_run=True)
        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out
        assert "test-img" in captured.out
        # ファイルは作成されない
        assert not (tmp_path / "test-img.png").exists()

    def test_non_dry_run(self, mod, tmp_path, capsys):
        spec = {"name": "real-img", "prompt": "generate this", "size": "200x200"}
        mod.generate_image(spec, tmp_path, dry_run=False)
        captured = capsys.readouterr()
        assert "Generating: real-img" in captured.out

    def test_output_path_construction(self, mod, tmp_path, capsys):
        spec = {"name": "my-image", "prompt": "test", "size": "100x100"}
        mod.generate_image(spec, tmp_path, dry_run=True)
        captured = capsys.readouterr()
        expected_path = str(tmp_path / "my-image.png")
        assert expected_path in captured.out

    def test_special_characters_in_name(self, mod, tmp_path, capsys):
        spec = {"name": "image-with-dashes_and_underscores", "prompt": "test", "size": "100x100"}
        mod.generate_image(spec, tmp_path, dry_run=True)
        captured = capsys.readouterr()
        assert "image-with-dashes_and_underscores" in captured.out


# ===========================================================================
# main (CLI)
# ===========================================================================

class TestMain:
    def test_dry_run_foundation(self, mod, tmp_path, capsys):
        with patch("sys.argv", ["prog", "--category", "foundation", "--output", str(tmp_path), "--dry-run"]):
            mod.main()
        captured = capsys.readouterr()
        assert "FOUNDATION" in captured.out
        assert "8 images" in captured.out
        assert "確認" in captured.out

    def test_dry_run_headers(self, mod, tmp_path, capsys):
        with patch("sys.argv", ["prog", "--category", "headers", "--output", str(tmp_path), "--dry-run"]):
            mod.main()
        captured = capsys.readouterr()
        assert "HEADERS" in captured.out
        assert "14 images" in captured.out

    def test_dry_run_all(self, mod, tmp_path, capsys):
        with patch("sys.argv", ["prog", "--category", "all", "--output", str(tmp_path), "--dry-run"]):
            mod.main()
        captured = capsys.readouterr()
        assert "FOUNDATION" in captured.out
        assert "HEADERS" in captured.out

    def test_empty_category(self, mod, tmp_path, capsys):
        """空のカテゴリ (concepts, exercises, portal)"""
        with patch("sys.argv", ["prog", "--category", "concepts", "--output", str(tmp_path), "--dry-run"]):
            mod.main()
        captured = capsys.readouterr()
        assert "CONCEPTS (0 images)" in captured.out

    def test_output_dir_created(self, mod, tmp_path):
        out_dir = tmp_path / "new_dir"
        with patch("sys.argv", ["prog", "--category", "foundation", "--output", str(out_dir), "--dry-run"]):
            mod.main()
        assert out_dir.exists()

    def test_total_count(self, mod, tmp_path, capsys):
        with patch("sys.argv", ["prog", "--category", "foundation", "--output", str(tmp_path), "--dry-run"]):
            mod.main()
        captured = capsys.readouterr()
        assert "8" in captured.out


# ===========================================================================
# Boundary
# ===========================================================================

class TestBoundary:
    def test_nonexistent_category_in_specs(self, mod):
        """IMAGE_SPECSに存在しないカテゴリ"""
        result = mod.IMAGE_SPECS.get("nonexistent", [])
        assert result == []

    def test_all_foundation_images_distinct_prompts(self, mod):
        """foundationの全画像が異なるプロンプトを持つ"""
        prompts = [s["prompt"] for s in mod.IMAGE_SPECS["foundation"]]
        assert len(prompts) == len(set(prompts))

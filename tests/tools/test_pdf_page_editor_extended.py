"""pdf_page_editor.py の拡張テスト - カバレッジ向上"""
import json
import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
from PIL import Image


@pytest.fixture
def pdf_module():
    """外部依存をモックしてモジュールをインポート"""
    with patch.dict("sys.modules", {
        "google": MagicMock(),
        "google.genai": MagicMock(),
        "google.genai.types": MagicMock(),
    }):
        from tests.conftest import import_module_from_repo
        mod = import_module_from_repo("pdf_page_editor", "tools/pdf_page_editor.py")
        yield mod


@pytest.fixture
def workspace(tmp_path):
    """テスト用ワークスペース"""
    ws = tmp_path / "doc_workspace"
    pages_dir = ws / "pages"
    pages_dir.mkdir(parents=True)
    edited_dir = ws / "edited"
    edited_dir.mkdir()

    for i in range(1, 4):
        img = Image.new("RGB", (1920, 1080), color=(255, 255, 255))
        img.save(pages_dir / f"page_{i:03d}.png", "PNG")

    analysis = {
        "document": {
            "source": "test.pdf",
            "total_pages": 3,
            "workspace": str(ws),
        },
        "pages": [
            {
                "page_number": 1,
                "image_path": str(pages_dir / "page_001.png"),
                "layout": "title_slide",
                "elements": [
                    {"type": "title", "content": "A very long title that is more than forty characters long here"},
                ],
            },
            {
                "page_number": 2,
                "image_path": str(pages_dir / "page_002.png"),
                "layout": "content",
                "elements": [
                    {"type": "heading", "content": "Chapter 1"},
                    {"type": "bullet_list", "items": ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6"]},
                ],
                "diagrams": [
                    {"type": "flowchart", "description": "Flow", "labels": ["A", "B", "C", "D", "E", "F"]},
                ],
            },
            {
                "page_number": 3,
                "image_path": str(pages_dir / "page_003.png"),
                "layout": "content",
                "elements": [{"type": "text", "content": "Last page"}],
            },
        ],
    }

    yaml_path = ws / "analysis.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(analysis, f, allow_unicode=True)
    return ws


class TestGetWorkspacePathEdgeCases:
    def test_special_characters(self, pdf_module):
        result = pdf_module.get_workspace_path(Path("/path/to/my doc (2).pdf"))
        assert result == Path("/path/to/my doc (2)_workspace")

    def test_no_extension(self, pdf_module):
        result = pdf_module.get_workspace_path(Path("/path/to/myfile"))
        assert result == Path("/path/to/myfile_workspace")


class TestImageToBytes:
    def test_rgba_image(self, pdf_module):
        img = Image.new("RGBA", (10, 10), color=(255, 0, 0, 128))
        data = pdf_module.image_to_bytes(img)
        assert isinstance(data, bytes)
        assert data[:4] == b"\x89PNG"

    def test_single_pixel(self, pdf_module):
        img = Image.new("RGB", (1, 1), color="black")
        data = pdf_module.image_to_bytes(img)
        assert len(data) > 0


class TestParseJsonResponseEdgeCases:
    def test_nested_json(self, pdf_module):
        text = '{"layout": "content", "elements": [{"type": "title", "content": "Test"}]}'
        result = pdf_module.parse_json_response(text)
        assert len(result["elements"]) == 1

    def test_code_block_with_invalid_inner_json(self, pdf_module):
        text = '```json\n{invalid json}\n```'
        result = pdf_module.parse_json_response(text)
        assert result["layout"] == "unknown"

    def test_json_with_extra_text(self, pdf_module):
        text = 'Some text before ```json\n{"layout": "test"}\n``` and after'
        result = pdf_module.parse_json_response(text)
        assert result["layout"] == "test"


class TestCmdShowExtended:
    def test_show_page_with_bullet_list(self, pdf_module, workspace, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 2
        pdf_module.cmd_show(args)
        captured = capsys.readouterr()
        assert "Item 1" in captured.out
        # Items beyond 5 should show count
        assert "more items" in captured.out

    def test_show_page_with_long_title(self, pdf_module, workspace, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        pdf_module.cmd_show(args)
        captured = capsys.readouterr()
        # Title should be displayed (may or may not be truncated depending on length)
        assert "title" in captured.out.lower() or "A very long" in captured.out

    def test_show_page_with_diagram_labels(self, pdf_module, workspace, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 2
        pdf_module.cmd_show(args)
        captured = capsys.readouterr()
        assert "ラベル" in captured.out

    def test_show_page_with_edited_path(self, pdf_module, workspace, capsys):
        yaml_path = workspace / "analysis.yaml"
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        data["pages"][0]["edited_path"] = str(workspace / "edited" / "page_001_edited.png")
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        pdf_module.cmd_show(args)
        captured = capsys.readouterr()
        assert "edited" in captured.out.lower() or "編集済み" in captured.out


class TestCmdEditExtended:
    def test_edit_with_replace(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = ["old text", "new text"]
        args.delete = None
        args.prompt = None
        args.overlay = None

        mock_types = MagicMock()
        mock_result_image = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mock_types.Part.as_image.return_value = MagicMock()
            mock_types.Part.as_image.return_value.save = MagicMock()
            result = pdf_module.cmd_edit(args)
        assert result is True

    def test_edit_with_delete(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = "text to delete"
        args.prompt = None
        args.overlay = None

        mock_types = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mock_types.Part.as_image.return_value = MagicMock()
            mock_types.Part.as_image.return_value.save = MagicMock()
            result = pdf_module.cmd_edit(args)
        assert result is True

    def test_edit_with_prompt(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = "Remove the logo"
        args.overlay = None

        mock_types = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mock_types.Part.as_image.return_value = MagicMock()
            mock_types.Part.as_image.return_value.save = MagicMock()
            result = pdf_module.cmd_edit(args)
        assert result is True

    def test_edit_with_overlay(self, pdf_module, workspace, tmp_path):
        overlay = tmp_path / "logo.png"
        Image.new("RGBA", (50, 50), color="red").save(overlay)

        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = "Add logo"
        args.overlay = str(overlay)

        mock_types = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mock_types.Part.as_image.return_value = MagicMock()
            mock_types.Part.as_image.return_value.save = MagicMock()
            result = pdf_module.cmd_edit(args)
        assert result is True

    def test_edit_nonexistent_overlay(self, pdf_module, workspace, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = "Edit"
        args.overlay = "/nonexistent/logo.png"

        mock_types = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mock_types.Part.as_image.return_value = MagicMock()
            mock_types.Part.as_image.return_value.save = MagicMock()
            result = pdf_module.cmd_edit(args)
        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_edit_no_image_in_response(self, pdf_module, workspace, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = "Edit"
        args.overlay = None

        mock_types = MagicMock()
        mock_response = MagicMock()
        mock_response.parts = []  # No image data

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            result = pdf_module.cmd_edit(args)
        assert result is False

    def test_edit_api_error(self, pdf_module, workspace, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = "Edit"
        args.overlay = None

        mock_types = MagicMock()
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("API Error")

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            result = pdf_module.cmd_edit(args)
        assert result is False

    def test_edit_uses_edited_image_if_exists(self, pdf_module, workspace):
        """連鎖編集: edited_pathが存在する場合そちらを使う"""
        edited_dir = workspace / "edited"
        edited_img = edited_dir / "page_001_edited.png"
        Image.new("RGB", (1920, 1080), color="gray").save(edited_img)

        yaml_path = workspace / "analysis.yaml"
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        data["pages"][0]["edited_path"] = str(edited_img)
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = "Change it"
        args.overlay = None

        mock_types = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mock_types.Part.as_image.return_value = MagicMock()
            mock_types.Part.as_image.return_value.save = MagicMock()
            result = pdf_module.cmd_edit(args)
        assert result is True

    def test_edit_aspect_ratio_variations(self, pdf_module, workspace):
        """異なるアスペクト比の画像でのテスト"""
        pages_dir = workspace / "pages"
        # 21:9 ultra-wide
        Image.new("RGB", (2520, 1080), color="white").save(pages_dir / "page_001.png")

        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = "Test"
        args.overlay = None

        mock_types = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mock_types.Part.as_image.return_value = MagicMock()
            mock_types.Part.as_image.return_value.save = MagicMock()
            result = pdf_module.cmd_edit(args)
        assert result is True


class TestCmdRebuildExtended:
    def test_rebuild_with_edited_pages(self, pdf_module, workspace, tmp_path):
        # Create an edited page
        edited_dir = workspace / "edited"
        Image.new("RGB", (1920, 1080), color="red").save(edited_dir / "page_002_edited.png")

        mock_img2pdf = MagicMock()
        mock_img2pdf.convert = MagicMock(return_value=b"pdfdata")
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            args = MagicMock()
            args.workspace = str(workspace)
            args.output = str(tmp_path / "output.pdf")
            result = pdf_module.cmd_rebuild(args)
        assert result is True

    def test_rebuild_auto_output(self, pdf_module, workspace):
        mock_img2pdf = MagicMock()
        mock_img2pdf.convert = MagicMock(return_value=b"pdfdata")
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            args = MagicMock()
            args.workspace = str(workspace)
            args.output = None
            result = pdf_module.cmd_rebuild(args)
        assert result is True

    def test_rebuild_rgba_image(self, pdf_module, workspace, tmp_path):
        """RGBA/P mode画像をRGBに変換するパスをテスト"""
        pages_dir = workspace / "pages"
        Image.new("RGBA", (100, 100), color=(255, 0, 0, 128)).save(pages_dir / "page_001.png")
        Image.new("P", (100, 100)).save(pages_dir / "page_002.png")
        Image.new("LA", (100, 100)).save(pages_dir / "page_003.png")

        mock_img2pdf = MagicMock()
        mock_img2pdf.convert = MagicMock(return_value=b"pdfdata")
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            args = MagicMock()
            args.workspace = str(workspace)
            args.output = str(tmp_path / "output.pdf")
            result = pdf_module.cmd_rebuild(args)
        assert result is True

    def test_rebuild_img2pdf_error(self, pdf_module, workspace, capsys):
        mock_img2pdf = MagicMock()
        mock_img2pdf.convert.side_effect = RuntimeError("conversion failed")
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            args = MagicMock()
            args.workspace = str(workspace)
            args.output = None
            result = pdf_module.cmd_rebuild(args)
        assert result is False

    def test_rebuild_missing_page_skipped(self, pdf_module, workspace, tmp_path, capsys):
        # Delete one page image
        (workspace / "pages" / "page_002.png").unlink()

        mock_img2pdf = MagicMock()
        mock_img2pdf.convert = MagicMock(return_value=b"pdfdata")
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            args = MagicMock()
            args.workspace = str(workspace)
            args.output = str(tmp_path / "output.pdf")
            result = pdf_module.cmd_rebuild(args)
        captured = capsys.readouterr()
        assert "Warning" in captured.out


class TestCmdInsertExtended:
    def test_insert_with_edited_pages(self, pdf_module, workspace, tmp_path):
        """edited_pathがあるページの後に挿入"""
        edited_dir = workspace / "edited"
        Image.new("RGB", (100, 100), "red").save(edited_dir / "page_002_edited.png")

        yaml_path = workspace / "analysis.yaml"
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        data["pages"][1]["edited_path"] = str(edited_dir / "page_002_edited.png")
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

        insert_img = tmp_path / "new.png"
        Image.new("RGB", (100, 100), "blue").save(insert_img)

        args = MagicMock()
        args.workspace = str(workspace)
        args.after_page = 1
        args.image = str(insert_img)
        args.title = "Inserted"
        result = pdf_module.cmd_insert(args)
        assert result is True

        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        assert data["document"]["total_pages"] == 4


class TestCmdOverlayExtended:
    def test_overlay_nonexistent_workspace(self, pdf_module, tmp_path):
        args = MagicMock()
        args.workspace = str(tmp_path / "nope")
        args.image = "/logo.png"
        with pytest.raises(SystemExit):
            pdf_module.cmd_overlay(args)

    def test_overlay_no_yaml(self, pdf_module, tmp_path):
        ws = tmp_path / "ws"
        ws.mkdir()
        args = MagicMock()
        args.workspace = str(ws)
        args.image = "/logo.png"
        with pytest.raises(SystemExit):
            pdf_module.cmd_overlay(args)


class TestCmdCompress:
    def test_compress_nonexistent_pdf(self, pdf_module, tmp_path):
        mock_img2pdf = MagicMock()
        mock_pdf2image = MagicMock()
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf, "pdf2image": mock_pdf2image}):
            args = MagicMock()
            args.pdf = str(tmp_path / "nope.pdf")
            with pytest.raises(SystemExit):
                pdf_module.cmd_compress(args)

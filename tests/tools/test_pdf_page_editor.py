"""pdf_page_editor.py の単体テスト"""
import json
import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

import importlib.util

try:
    from PIL import Image
except ImportError:
    Image = None

_pdf2image_available = importlib.util.find_spec("pdf2image") is not None

pytestmark = pytest.mark.skipif(
    Image is None or not _pdf2image_available,
    reason="Pillow or pdf2image not installed",
)


# ---------------------------------------------------------------------------
# Helper: import with mocked dependencies
# ---------------------------------------------------------------------------

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
    """テスト用ワークスペース構造を作成"""
    ws = tmp_path / "doc_workspace"
    pages_dir = ws / "pages"
    pages_dir.mkdir(parents=True)
    edited_dir = ws / "edited"
    edited_dir.mkdir()

    # ダミー画像を3ページ分作成
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
                "elements": [{"type": "title", "content": "Title Page"}],
            },
            {
                "page_number": 2,
                "image_path": str(pages_dir / "page_002.png"),
                "layout": "content",
                "elements": [
                    {"type": "heading", "content": "Chapter 1"},
                    {"type": "text", "content": "Some text here"},
                ],
                "diagrams": [
                    {"type": "flowchart", "description": "Flow", "labels": ["A", "B"]},
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


@pytest.fixture
def overlay_image(tmp_path):
    """テスト用オーバーレイ画像"""
    img = Image.new("RGBA", (100, 50), color=(255, 0, 0, 128))
    path = tmp_path / "logo.png"
    img.save(path, "PNG")
    return path


@pytest.fixture
def insert_image(tmp_path):
    """挿入用ダミー画像"""
    img = Image.new("RGB", (1920, 1080), color=(0, 0, 255))
    path = tmp_path / "new_page.png"
    img.save(path, "PNG")
    return path


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------

class TestImport:
    def test_import(self, pdf_module):
        assert hasattr(pdf_module, "main")
        assert hasattr(pdf_module, "parse_json_response")


# ---------------------------------------------------------------------------
# get_workspace_path
# ---------------------------------------------------------------------------

class TestGetWorkspacePath:
    def test_basic(self, pdf_module):
        result = pdf_module.get_workspace_path(Path("/path/to/doc.pdf"))
        assert result == Path("/path/to/doc_workspace")

    def test_with_spaces(self, pdf_module):
        result = pdf_module.get_workspace_path(Path("/path/to/my doc.pdf"))
        assert result == Path("/path/to/my doc_workspace")


# ---------------------------------------------------------------------------
# image_to_bytes
# ---------------------------------------------------------------------------

class TestImageToBytes:
    def test_basic(self, pdf_module):
        img = Image.new("RGB", (10, 10), color="red")
        data = pdf_module.image_to_bytes(img)
        assert isinstance(data, bytes)
        assert len(data) > 0
        # PNG magic bytes
        assert data[:4] == b"\x89PNG"


# ---------------------------------------------------------------------------
# parse_json_response
# ---------------------------------------------------------------------------

class TestParseJsonResponse:
    def test_valid_json(self, pdf_module):
        result = pdf_module.parse_json_response('{"layout": "content", "elements": []}')
        assert result["layout"] == "content"

    def test_json_in_code_block(self, pdf_module):
        text = '```json\n{"layout": "title", "elements": []}\n```'
        result = pdf_module.parse_json_response(text)
        assert result["layout"] == "title"

    def test_json_in_plain_code_block(self, pdf_module):
        text = '```\n{"layout": "doc"}\n```'
        result = pdf_module.parse_json_response(text)
        assert result["layout"] == "doc"

    def test_invalid_json(self, pdf_module):
        result = pdf_module.parse_json_response("not json at all")
        assert result["layout"] == "unknown"
        assert "raw_response" in result

    def test_empty_string(self, pdf_module):
        result = pdf_module.parse_json_response("")
        assert result["layout"] == "unknown"

    def test_partial_json(self, pdf_module):
        result = pdf_module.parse_json_response('{"layout": "content"')
        # Invalid JSON without code block -> fallback
        assert result["layout"] == "unknown"

    def test_unicode_content(self, pdf_module):
        text = '{"layout": "content", "elements": [{"type": "title", "content": "日本語テスト"}]}'
        result = pdf_module.parse_json_response(text)
        assert result["elements"][0]["content"] == "日本語テスト"


# ---------------------------------------------------------------------------
# cmd_show
# ---------------------------------------------------------------------------

class TestCmdShow:
    def test_show_page(self, pdf_module, workspace, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        pdf_module.cmd_show(args)
        captured = capsys.readouterr()
        assert "Title Page" in captured.out

    def test_show_page_with_diagrams(self, pdf_module, workspace, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 2
        pdf_module.cmd_show(args)
        captured = capsys.readouterr()
        assert "Chapter 1" in captured.out
        assert "flowchart" in captured.out

    def test_show_invalid_page_zero(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 0
        with pytest.raises(SystemExit):
            pdf_module.cmd_show(args)

    def test_show_invalid_page_over(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 999
        with pytest.raises(SystemExit):
            pdf_module.cmd_show(args)

    def test_show_nonexistent_workspace(self, pdf_module, tmp_path):
        args = MagicMock()
        args.workspace = str(tmp_path / "nope")
        args.page = 1
        with pytest.raises(SystemExit):
            pdf_module.cmd_show(args)


# ---------------------------------------------------------------------------
# cmd_insert
# ---------------------------------------------------------------------------

class TestCmdInsert:
    def test_insert_after_page_1(self, pdf_module, workspace, insert_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.after_page = 1
        args.image = str(insert_image)
        args.title = "New Page"

        result = pdf_module.cmd_insert(args)
        assert result is True

        # analysis.yamlが更新されていることを確認
        yaml_path = workspace / "analysis.yaml"
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        assert data["document"]["total_pages"] == 4

    def test_insert_at_beginning(self, pdf_module, workspace, insert_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.after_page = 0
        args.image = str(insert_image)
        args.title = None

        result = pdf_module.cmd_insert(args)
        assert result is True

    def test_insert_at_end(self, pdf_module, workspace, insert_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.after_page = 3
        args.image = str(insert_image)
        args.title = "Last"

        result = pdf_module.cmd_insert(args)
        assert result is True

    def test_insert_invalid_after_page(self, pdf_module, workspace, insert_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.after_page = 99
        args.image = str(insert_image)
        args.title = None

        with pytest.raises(SystemExit):
            pdf_module.cmd_insert(args)

    def test_insert_negative_after_page(self, pdf_module, workspace, insert_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.after_page = -1
        args.image = str(insert_image)
        args.title = None

        with pytest.raises(SystemExit):
            pdf_module.cmd_insert(args)

    def test_insert_nonexistent_image(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.after_page = 1
        args.image = "/no/such/image.png"
        args.title = None

        with pytest.raises(SystemExit):
            pdf_module.cmd_insert(args)

    def test_insert_nonexistent_workspace(self, pdf_module, tmp_path, insert_image):
        args = MagicMock()
        args.workspace = str(tmp_path / "nope")
        args.after_page = 0
        args.image = str(insert_image)
        args.title = None

        with pytest.raises(SystemExit):
            pdf_module.cmd_insert(args)


# ---------------------------------------------------------------------------
# cmd_overlay
# ---------------------------------------------------------------------------

class TestCmdOverlay:
    def test_overlay_all_pages(self, pdf_module, workspace, overlay_image, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.image = str(overlay_image)
        args.pages = None
        args.width = None
        args.position = "bottom-right"
        args.margin_x = 30
        args.margin_y = 20
        args.clear_background = False
        args.clear_padding = 10

        pdf_module.cmd_overlay(args)
        captured = capsys.readouterr()
        assert "page_001_edited.png" in captured.out

    def test_overlay_specific_pages(self, pdf_module, workspace, overlay_image, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.image = str(overlay_image)
        args.pages = "1,3"
        args.width = 50
        args.position = "top-left"
        args.margin_x = 10
        args.margin_y = 10
        args.clear_background = False
        args.clear_padding = 10

        pdf_module.cmd_overlay(args)
        captured = capsys.readouterr()
        assert "page_001_edited.png" in captured.out
        assert "page_003_edited.png" in captured.out

    def test_overlay_center_position(self, pdf_module, workspace, overlay_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.image = str(overlay_image)
        args.pages = "1"
        args.width = None
        args.position = "center"
        args.margin_x = 0
        args.margin_y = 0
        args.clear_background = False
        args.clear_padding = 10

        pdf_module.cmd_overlay(args)

    def test_overlay_custom_position(self, pdf_module, workspace, overlay_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.image = str(overlay_image)
        args.pages = "1"
        args.width = None
        args.position = "100,200"
        args.margin_x = 0
        args.margin_y = 0
        args.clear_background = False
        args.clear_padding = 10

        pdf_module.cmd_overlay(args)

    def test_overlay_invalid_position(self, pdf_module, workspace, overlay_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.image = str(overlay_image)
        args.pages = "1"
        args.width = None
        args.position = "invalid"
        args.margin_x = 0
        args.margin_y = 0
        args.clear_background = False
        args.clear_padding = 10

        with pytest.raises(SystemExit):
            pdf_module.cmd_overlay(args)

    def test_overlay_with_clear_background(self, pdf_module, workspace, overlay_image):
        args = MagicMock()
        args.workspace = str(workspace)
        args.image = str(overlay_image)
        args.pages = "1"
        args.width = None
        args.position = "bottom-right"
        args.margin_x = 30
        args.margin_y = 20
        args.clear_background = True
        args.clear_padding = 10

        pdf_module.cmd_overlay(args)

    def test_overlay_all_positions(self, pdf_module, workspace, overlay_image):
        """全position指定をテスト"""
        for position in ["bottom-right", "bottom-left", "top-right", "top-left", "center"]:
            args = MagicMock()
            args.workspace = str(workspace)
            args.image = str(overlay_image)
            args.pages = "1"
            args.width = None
            args.position = position
            args.margin_x = 30
            args.margin_y = 20
            args.clear_background = False
            args.clear_padding = 10

            pdf_module.cmd_overlay(args)

    def test_overlay_out_of_range_page(self, pdf_module, workspace, overlay_image, capsys):
        args = MagicMock()
        args.workspace = str(workspace)
        args.image = str(overlay_image)
        args.pages = "99"
        args.width = None
        args.position = "center"
        args.margin_x = 0
        args.margin_y = 0
        args.clear_background = False
        args.clear_padding = 10

        pdf_module.cmd_overlay(args)
        captured = capsys.readouterr()
        assert "スキップ" in captured.out

    def test_overlay_nonexistent_image(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.image = "/no/logo.png"
        with pytest.raises(SystemExit):
            pdf_module.cmd_overlay(args)


# ---------------------------------------------------------------------------
# cmd_rebuild (mocked img2pdf)
# ---------------------------------------------------------------------------

class TestCmdRebuild:
    def test_rebuild_basic(self, pdf_module, workspace, tmp_path):
        mock_img2pdf = MagicMock()
        mock_img2pdf.convert = MagicMock(return_value=b"pdfdata")
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            args = MagicMock()
            args.workspace = str(workspace)
            args.output = str(tmp_path / "output.pdf")

            result = pdf_module.cmd_rebuild(args)
            assert result is True
            assert Path(tmp_path / "output.pdf").exists()

    def test_rebuild_nonexistent_workspace(self, pdf_module, tmp_path):
        mock_img2pdf = MagicMock()
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            args = MagicMock()
            args.workspace = str(tmp_path / "nope")
            args.output = None

            with pytest.raises(SystemExit):
                pdf_module.cmd_rebuild(args)

    def test_rebuild_no_yaml(self, pdf_module, tmp_path):
        mock_img2pdf = MagicMock()
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            ws = tmp_path / "ws"
            ws.mkdir()
            args = MagicMock()
            args.workspace = str(ws)
            args.output = None

            with pytest.raises(SystemExit):
                pdf_module.cmd_rebuild(args)


# ---------------------------------------------------------------------------
# cmd_edit (API mocked)
# ---------------------------------------------------------------------------

class TestCmdEdit:
    def test_edit_nonexistent_workspace(self, pdf_module, tmp_path):
        args = MagicMock()
        args.workspace = str(tmp_path / "nope")
        args.page = 1
        with pytest.raises(SystemExit):
            pdf_module.cmd_edit(args)

    def test_edit_invalid_page(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 0
        args.replace = None
        args.delete = None
        args.prompt = None
        with pytest.raises(SystemExit):
            pdf_module.cmd_edit(args)

    def test_edit_no_instruction(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = None
        args.overlay = None
        with pytest.raises(SystemExit):
            pdf_module.cmd_edit(args)

    def test_edit_page_over_total(self, pdf_module, workspace):
        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 999
        args.replace = None
        args.delete = None
        args.prompt = None
        with pytest.raises(SystemExit):
            pdf_module.cmd_edit(args)


# ---------------------------------------------------------------------------
# cmd_analyze (heavily mocked)
# ---------------------------------------------------------------------------

class TestCmdAnalyze:
    def test_nonexistent_pdf(self, pdf_module, tmp_path):
        args = MagicMock()
        args.pdf = str(tmp_path / "nope.pdf")
        args.dpi = 150
        with pytest.raises(SystemExit):
            pdf_module.cmd_analyze(args)

    def test_analyze_success(self, pdf_module, tmp_path):
        """cmd_analyze の正常系テスト (lines 105-186)"""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 dummy")

        mock_img = Image.new("RGB", (800, 600), "white")

        # Mock pdf2image module with convert_from_path
        mock_pdf2image = MagicMock()
        mock_pdf2image.convert_from_path = MagicMock(return_value=[mock_img, mock_img])

        # Mock tqdm to just pass through the iterable
        mock_tqdm = MagicMock()
        mock_tqdm.tqdm = lambda iterable, **kwargs: iterable
        mock_tqdm.tqdm.write = MagicMock()

        mock_types = MagicMock()

        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "layout": "content",
            "elements": [{"type": "title", "content": "A very long title that exceeds forty characters in length definitely"}],
        })

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {
                 "pdf2image": mock_pdf2image,
                 "google.genai.types": mock_types,
                 "tqdm": mock_tqdm,
                 "tqdm.auto": mock_tqdm,
             }):
            args = MagicMock()
            args.pdf = str(pdf_file)
            args.dpi = 150
            result = pdf_module.cmd_analyze(args)
            assert result is not None
            assert result["document"]["total_pages"] == 2

    def test_analyze_api_error(self, pdf_module, tmp_path):
        """cmd_analyze でAPI呼び出し失敗時 (line 138-139)"""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 dummy")

        mock_img = Image.new("RGB", (800, 600), "white")

        mock_pdf2image = MagicMock()
        mock_pdf2image.convert_from_path.return_value = [mock_img]

        mock_tqdm_cls = MagicMock(side_effect=lambda iterable, **kwargs: iterable)
        mock_tqdm_cls.write = MagicMock()

        mock_types = MagicMock()
        mock_types.Part.from_bytes.return_value = MagicMock()
        mock_types.GenerateContentConfig.return_value = MagicMock()

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("API Error")

        with patch.object(pdf_module, "get_client", return_value=mock_client), \
             patch.dict("sys.modules", {
                 "pdf2image": mock_pdf2image,
                 "tqdm": MagicMock(tqdm=mock_tqdm_cls),
                 "tqdm.auto": MagicMock(tqdm=mock_tqdm_cls),
                 "google.genai.types": mock_types,
             }):
            args = MagicMock()
            args.pdf = str(pdf_file)
            args.dpi = 150
            result = pdf_module.cmd_analyze(args)
            assert result is not None
            assert result["pages"][0].get("error") is not None


# ---------------------------------------------------------------------------
# get_client
# ---------------------------------------------------------------------------

class TestGetClient:
    def test_no_api_key(self, pdf_module):
        """GEMINI_API_KEY が未設定の場合 (lines 65-69)"""
        with patch.object(pdf_module, "GEMINI_API_KEY", None):
            with pytest.raises(SystemExit):
                pdf_module.get_client()

    def test_with_api_key(self, pdf_module):
        """GEMINI_API_KEY が設定済みの場合"""
        mock_genai = MagicMock()
        mock_genai.Client.return_value = MagicMock()
        with patch.object(pdf_module, "GEMINI_API_KEY", "test-key"), \
             patch.dict("sys.modules", {"google": MagicMock(genai=mock_genai), "google.genai": mock_genai}):
            client = pdf_module.get_client()
            assert client is not None


# ---------------------------------------------------------------------------
# cmd_compress (lines 684-762)
# ---------------------------------------------------------------------------

class TestCmdCompressExtended:
    def test_compress_success(self, pdf_module, tmp_path):
        """cmd_compress 正常系テスト"""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF" + b"\x00" * 10000)

        mock_img = Image.new("RGB", (2000, 1500), "white")
        mock_pdf2image = MagicMock()
        mock_pdf2image.convert_from_path.return_value = [mock_img]

        mock_img2pdf = MagicMock()
        mock_img2pdf.convert.return_value = b"pdfdata"

        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf, "pdf2image": mock_pdf2image}):
            args = MagicMock()
            args.pdf = str(pdf_file)
            args.output = str(tmp_path / "output.pdf")
            args.width = 1920
            args.quality = 85
            args.dpi = 150
            result = pdf_module.cmd_compress(args)
        assert result is True
        assert (tmp_path / "output.pdf").exists()

    def test_compress_auto_output(self, pdf_module, tmp_path):
        """output 未指定時の自動ファイル名"""
        pdf_file = tmp_path / "document.pdf"
        pdf_file.write_bytes(b"%PDF" + b"\x00" * 10000)

        mock_img = Image.new("RGB", (800, 600), "white")
        mock_pdf2image = MagicMock()
        mock_pdf2image.convert_from_path.return_value = [mock_img]

        mock_img2pdf = MagicMock()
        mock_img2pdf.convert.return_value = b"pdfdata"

        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf, "pdf2image": mock_pdf2image}):
            args = MagicMock()
            args.pdf = str(pdf_file)
            args.output = None
            args.width = None
            args.quality = None
            args.dpi = None
            result = pdf_module.cmd_compress(args)
        assert result is True

    def test_compress_rgba_image(self, pdf_module, tmp_path):
        """RGBA画像のRGB変換パス (lines 731-737)"""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF" + b"\x00" * 10000)

        mock_img = Image.new("RGBA", (2000, 1500), (255, 0, 0, 128))
        mock_pdf2image = MagicMock()
        mock_pdf2image.convert_from_path.return_value = [mock_img]

        mock_img2pdf = MagicMock()
        mock_img2pdf.convert.return_value = b"pdfdata"

        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf, "pdf2image": mock_pdf2image}):
            args = MagicMock()
            args.pdf = str(pdf_file)
            args.output = str(tmp_path / "out.pdf")
            args.width = 1920
            args.quality = 85
            args.dpi = 150
            result = pdf_module.cmd_compress(args)
        assert result is True


# ---------------------------------------------------------------------------
# cmd_edit: yaml missing (line 200-201)
# ---------------------------------------------------------------------------

class TestCmdEditYamlMissing:
    def test_edit_missing_yaml(self, pdf_module, tmp_path):
        """workspace は存在するが analysis.yaml がない場合"""
        ws = tmp_path / "ws"
        ws.mkdir()
        args = MagicMock()
        args.workspace = str(ws)
        args.page = 1
        with pytest.raises(SystemExit):
            pdf_module.cmd_edit(args)


# ---------------------------------------------------------------------------
# cmd_edit: missing page image (lines 222-224)
# ---------------------------------------------------------------------------

class TestCmdEditMissingImage:
    def test_edit_missing_page_image(self, pdf_module, workspace):
        """ページ画像ファイルが存在しない場合"""
        # ページ画像を削除
        pages_dir = workspace / "pages"
        (pages_dir / "page_001.png").unlink()

        yaml_path = workspace / "analysis.yaml"
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        # edited_pathもクリア
        if data["pages"][0].get("edited_path"):
            del data["pages"][0]["edited_path"]
        # image_pathを壊れたパスに
        data["pages"][0]["image_path"] = str(pages_dir / "page_001.png")
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

        args = MagicMock()
        args.workspace = str(workspace)
        args.page = 1
        args.replace = None
        args.delete = None
        args.prompt = "test"
        args.overlay = None

        with pytest.raises(SystemExit):
            pdf_module.cmd_edit(args)


# ---------------------------------------------------------------------------
# cmd_show: nonexistent yaml (line 410-412)
# ---------------------------------------------------------------------------

class TestCmdShowMissingYaml:
    def test_show_missing_yaml(self, pdf_module, tmp_path):
        """workspace は存在するが analysis.yaml がない場合"""
        ws = tmp_path / "ws"
        ws.mkdir()
        args = MagicMock()
        args.workspace = str(ws)
        args.page = 1
        with pytest.raises(SystemExit):
            pdf_module.cmd_show(args)


# ---------------------------------------------------------------------------
# cmd_rebuild: no images found (lines 352-354)
# ---------------------------------------------------------------------------

class TestCmdRebuildNoImages:
    def test_rebuild_empty_pages(self, pdf_module, tmp_path):
        """全ページ画像がない場合"""
        ws = tmp_path / "ws"
        ws.mkdir()
        pages_dir = ws / "pages"
        pages_dir.mkdir()

        analysis = {
            "document": {"source": "test.pdf", "total_pages": 2, "workspace": str(ws)},
            "pages": [
                {"page_number": 1, "image_path": str(pages_dir / "page_001.png")},
                {"page_number": 2, "image_path": str(pages_dir / "page_002.png")},
            ],
        }
        yaml_path = ws / "analysis.yaml"
        with open(yaml_path, "w") as f:
            yaml.dump(analysis, f)

        mock_img2pdf = MagicMock()
        with patch.dict("sys.modules", {"img2pdf": mock_img2pdf}):
            args = MagicMock()
            args.workspace = str(ws)
            args.output = None
            with pytest.raises(SystemExit):
                pdf_module.cmd_rebuild(args)

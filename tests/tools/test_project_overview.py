"""project_overview.py の単体テスト"""
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestImport:
    def test_import_module(self):
        import project_overview
        assert hasattr(project_overview, 'walk_tree')
        assert hasattr(project_overview, 'EXCLUDE_DIRS')


class TestWalkTree:
    def test_basic_walk(self, tmp_path):
        from project_overview import walk_tree
        # Create a simple structure
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("def hello(): pass", encoding="utf-8")
        (tmp_path / "README.md").write_text("# Test", encoding="utf-8")
        _structure, code_files = walk_tree(tmp_path)
        assert len(code_files) >= 1

    def test_excludes_git(self, tmp_path):
        from project_overview import walk_tree
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "config").write_text("test", encoding="utf-8")
        (tmp_path / "main.py").write_text("test", encoding="utf-8")
        _structure, code_files = walk_tree(tmp_path)
        assert not any(".git" in str(f) for f in code_files)

    def test_excludes_node_modules(self, tmp_path):
        from project_overview import walk_tree
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "test.js").write_text("test", encoding="utf-8")
        (tmp_path / "app.js").write_text("test", encoding="utf-8")
        _structure, code_files = walk_tree(tmp_path)
        # Check relative paths to avoid false positives from tmp_path dir name
        rel_paths = [str(f.relative_to(tmp_path)) for f in code_files]
        assert not any("node_modules" in rp for rp in rel_paths)

    def test_empty_dir(self, tmp_path):
        from project_overview import walk_tree
        _structure, code_files = walk_tree(tmp_path)
        assert len(code_files) == 0

    def test_max_code_files_limit(self, tmp_path):
        """max_code_files 制限のテスト"""
        from project_overview import walk_tree
        for i in range(10):
            (tmp_path / f"file{i}.py").write_text(f"# file {i}", encoding="utf-8")
        _structure, code_files = walk_tree(tmp_path, max_code_files=3)
        assert len(code_files) <= 3

    def test_structure_keys(self, tmp_path):
        """構造辞書のキーを確認"""
        from project_overview import walk_tree
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("pass", encoding="utf-8")
        structure, _ = walk_tree(tmp_path)
        assert "(root)" in structure
        assert "src" in structure

    def test_structure_contains_files(self, tmp_path):
        """構造辞書にファイル一覧が含まれる"""
        from project_overview import walk_tree
        (tmp_path / "app.py").write_text("pass", encoding="utf-8")
        (tmp_path / "config.json").write_text("{}", encoding="utf-8")
        structure, _ = walk_tree(tmp_path)
        root_files = structure["(root)"]["files"]
        assert "app.py" in root_files
        assert "config.json" in root_files

    def test_excludes_dotfiles(self, tmp_path):
        """ドットファイルは除外される"""
        from project_overview import walk_tree
        (tmp_path / ".hidden.py").write_text("pass", encoding="utf-8")
        (tmp_path / "visible.py").write_text("pass", encoding="utf-8")
        structure, code_files = walk_tree(tmp_path)
        root_files = structure["(root)"]["files"]
        assert ".hidden.py" not in root_files
        assert "visible.py" in root_files

    def test_includes_multiple_extensions(self, tmp_path):
        """複数の拡張子がサポートされる"""
        from project_overview import walk_tree
        for ext in [".py", ".ts", ".js", ".md", ".yml", ".json"]:
            (tmp_path / f"test{ext}").write_text("test", encoding="utf-8")
        structure, _ = walk_tree(tmp_path)
        root_files = structure["(root)"]["files"]
        assert len(root_files) == 6


class TestCollectTargets:
    def test_no_extra_files(self, tmp_path):
        from project_overview import collect_targets
        (tmp_path / "main.py").write_text("pass", encoding="utf-8")
        structure, files = collect_targets(tmp_path, [])
        assert len(files) >= 1

    def test_with_priority_files(self, tmp_path):
        from project_overview import collect_targets
        (tmp_path / "main.py").write_text("pass", encoding="utf-8")
        extra = tmp_path / "extra.py"
        extra.write_text("pass", encoding="utf-8")
        structure, files = collect_targets(tmp_path, [str(extra)])
        # priority file should be first
        assert files[0].resolve() == extra.resolve()

    def test_nonexistent_file_ignored(self, tmp_path):
        from project_overview import collect_targets
        (tmp_path / "main.py").write_text("pass", encoding="utf-8")
        structure, files = collect_targets(tmp_path, ["/nonexistent/file.py"])
        # Should not crash, just warn


class TestReadHead:
    def test_reads_content(self, tmp_path):
        from project_overview import read_head
        f = tmp_path / "test.py"
        f.write_text("hello world", encoding="utf-8")
        assert read_head(f) == "hello world"

    def test_limit_chars(self, tmp_path):
        from project_overview import read_head
        f = tmp_path / "test.py"
        f.write_text("A" * 5000, encoding="utf-8")
        result = read_head(f, limit_chars=100)
        assert len(result) == 100

    def test_nonexistent_file(self):
        from project_overview import read_head
        result = read_head(Path("/nonexistent/file.py"))
        assert result == ""


class TestExtractLinks:
    def test_extracts_href(self):
        from project_overview import extract_links
        html = '<a href="page.html">Link</a>'
        links = extract_links(html)
        assert "page.html" in links

    def test_extracts_src(self):
        from project_overview import extract_links
        html = '<img src="image.png">'
        links = extract_links(html)
        assert "image.png" in links

    def test_no_links(self):
        from project_overview import extract_links
        html = '<p>No links here</p>'
        links = extract_links(html)
        assert links == []

    def test_single_quotes(self):
        from project_overview import extract_links
        html = "<a href='page.html'>Link</a>"
        links = extract_links(html)
        assert "page.html" in links


class TestNormalizeLink:
    def test_removes_fragment(self):
        from project_overview import normalize_link
        assert normalize_link("page.html#section") == "page.html"

    def test_removes_query(self):
        from project_overview import normalize_link
        assert normalize_link("page.html?v=1") == "page.html"

    def test_removes_both(self):
        from project_overview import normalize_link
        assert normalize_link("page.html?v=1#top") == "page.html"

    def test_plain_link(self):
        from project_overview import normalize_link
        assert normalize_link("page.html") == "page.html"


class TestIsExternalLink:
    def test_http(self):
        from project_overview import is_external_link
        assert is_external_link("http://example.com") is True

    def test_https(self):
        from project_overview import is_external_link
        assert is_external_link("https://example.com") is True

    def test_mailto(self):
        from project_overview import is_external_link
        assert is_external_link("mailto:user@example.com") is True

    def test_data(self):
        from project_overview import is_external_link
        assert is_external_link("data:text/html,<h1>Hello</h1>") is True

    def test_relative_link(self):
        from project_overview import is_external_link
        assert is_external_link("page.html") is False

    def test_protocol_relative(self):
        from project_overview import is_external_link
        assert is_external_link("//cdn.example.com/file.js") is True


class TestStructureToText:
    def test_basic(self):
        from project_overview import structure_to_text
        structure = {
            "(root)": {"subdirs": ["src"], "files": ["main.py"]},
            "src": {"subdirs": [], "files": ["app.py"]},
        }
        text = structure_to_text(structure)
        assert "(root)/" in text
        assert "main.py" in text
        assert "src/" in text

    def test_empty_structure(self):
        from project_overview import structure_to_text
        text = structure_to_text({})
        assert text == ""

    def test_max_dirs(self):
        from project_overview import structure_to_text
        structure = {f"dir{i}": {"subdirs": [], "files": []} for i in range(300)}
        text = structure_to_text(structure, max_dirs=5)
        assert "省略" in text


class TestCheckLinks:
    def test_no_issues(self, tmp_path):
        from project_overview import check_links
        f = tmp_path / "index.html"
        f.write_text('<a href="other.html">Link</a>', encoding="utf-8")
        other = tmp_path / "other.html"
        other.write_text("<html></html>", encoding="utf-8")
        issues, edges = check_links(tmp_path, [f, other])
        assert len(issues) == 0
        assert len(edges) == 1

    def test_broken_link(self, tmp_path):
        from project_overview import check_links
        f = tmp_path / "index.html"
        f.write_text('<a href="missing.html">Link</a>', encoding="utf-8")
        issues, edges = check_links(tmp_path, [f])
        assert len(issues) == 1
        assert issues[0]["reason"] == "not found"


class TestFindHtmlFiles:
    def test_finds_html(self, tmp_path):
        from project_overview import find_html_files
        (tmp_path / "index.html").write_text("<html></html>", encoding="utf-8")
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "page.html").write_text("<html></html>", encoding="utf-8")
        files = find_html_files(tmp_path)
        assert len(files) == 2

    def test_excludes_dotdirs(self, tmp_path):
        from project_overview import find_html_files
        (tmp_path / ".hidden").mkdir()
        (tmp_path / ".hidden" / "secret.html").write_text("<html></html>", encoding="utf-8")
        files = find_html_files(tmp_path)
        assert len(files) == 0

    def test_max_files(self, tmp_path):
        from project_overview import find_html_files
        for i in range(10):
            (tmp_path / f"page{i}.html").write_text("<html></html>", encoding="utf-8")
        files = find_html_files(tmp_path, max_files=3)
        assert len(files) == 3


class TestEncodePlantuml:
    def test_basic_encode(self):
        from project_overview import encode_plantuml
        result = encode_plantuml("@startuml\nA -> B\n@enduml")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_empty_input(self):
        from project_overview import encode_plantuml
        result = encode_plantuml("")
        assert isinstance(result, str)


class TestPlantuml:
    def test_no_modules(self):
        from project_overview import plantuml
        result = plantuml([])
        assert "@startuml" in result
        assert "モジュール情報がありません" in result
        assert "@enduml" in result

    def test_with_modules(self):
        from project_overview import plantuml
        modules = [
            {"name": "ModA", "purpose": "Test module", "dependencies": []},
            {"name": "ModB", "purpose": "Another", "dependencies": ["ModA"]},
        ]
        result = plantuml(modules)
        assert "ModA" in result
        assert "ModB" in result
        assert "@startuml" in result


class TestPlantumlWbs:
    def test_no_modules(self):
        from project_overview import plantuml_wbs
        result = plantuml_wbs([], "test-project")
        assert "@startmindmap" in result
        assert "test-project" in result
        assert "モジュール情報なし" in result

    def test_with_modules_and_features(self):
        from project_overview import plantuml_wbs
        modules = [
            {"name": "Core", "features": ["Feature1", "Feature2"]},
        ]
        result = plantuml_wbs(modules, "root")
        assert "Core" in result
        assert "Feature1" in result


class TestStructureToPlantumlMindmap:
    def test_basic_structure(self):
        from project_overview import structure_to_plantuml_mindmap
        structure = {
            "(root)": {"subdirs": ["src"], "files": ["main.py"]},
            "src": {"subdirs": [], "files": ["app.py"]},
        }
        result = structure_to_plantuml_mindmap(structure, "test-project")
        assert "@startmindmap" in result
        assert "test-project" in result
        assert "main.py" in result

    def test_empty_structure(self):
        from project_overview import structure_to_plantuml_mindmap
        result = structure_to_plantuml_mindmap({}, "empty")
        assert "@startmindmap" in result
        assert "@endmindmap" in result


class TestGeminiAnalyze:
    def test_no_client(self):
        from project_overview import gemini_analyze
        result = gemini_analyze(None, Path("/tmp"), {}, [])
        assert result["modules"] == []
        assert result["files_summary"] == []

    def test_with_mock_client(self, tmp_path):
        from project_overview import gemini_analyze
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "modules": [{"name": "TestMod", "path": "test.py", "purpose": "Testing", "features": [], "dependencies": []}],
            "files_summary": [],
            "implemented_features": ["Feature A"],
            "missing_features": [],
            "recommendations": [],
        })
        mock_client.models.generate_content.return_value = mock_response

        # Create a sample file
        code_file = tmp_path / "test.py"
        code_file.write_text("def hello(): pass", encoding="utf-8")

        with patch("project_overview.get_flash_model", return_value="test-model"):
            result = gemini_analyze(mock_client, tmp_path, {}, [code_file])
        assert len(result["modules"]) == 1
        assert result["modules"][0]["name"] == "TestMod"

    def test_gemini_invalid_json(self, tmp_path):
        from project_overview import gemini_analyze
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "not valid json at all"
        mock_client.models.generate_content.return_value = mock_response

        with patch("project_overview.get_flash_model", return_value="test-model"):
            result = gemini_analyze(mock_client, tmp_path, {}, [])
        # Should fall back gracefully
        assert "recommendations" in result

    def test_gemini_json_in_code_fence(self, tmp_path):
        from project_overview import gemini_analyze
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '```json\n{"modules": [], "files_summary": [], "implemented_features": [], "missing_features": [], "recommendations": ["test"]}\n```'
        mock_client.models.generate_content.return_value = mock_response

        with patch("project_overview.get_flash_model", return_value="test-model"):
            result = gemini_analyze(mock_client, tmp_path, {}, [])
        assert result["recommendations"] == ["test"]


class TestFallbackModulesFromPages:
    def test_empty_pages(self):
        from project_overview import fallback_modules_from_pages
        result = fallback_modules_from_pages([], [], Path("/tmp"))
        assert result == []

    def test_with_pages(self, tmp_path):
        from project_overview import fallback_modules_from_pages
        pages = [tmp_path / "index.html", tmp_path / "about.html"]
        edges = [("index.html", "about.html")]
        result = fallback_modules_from_pages(pages, edges, tmp_path)
        assert len(result) == 2
        assert result[0]["purpose"] == "HTMLページ"


class TestBuildHtml:
    def test_basic_output(self):
        from project_overview import build_html
        analysis = {
            "modules": [],
            "files_summary": [],
            "implemented_features": [],
            "missing_features": [],
            "recommendations": [],
            "structure_text": "",
            "pages": [],
            "link_issues": [],
        }
        html = build_html(analysis, "", "", "", Path("/tmp"))
        assert "プロジェクト概要" in html

    def test_with_modules(self):
        from project_overview import build_html
        analysis = {
            "modules": [{"name": "TestMod", "path": "test.py", "purpose": "Testing", "features": ["F1"], "dependencies": ["dep1"]}],
            "files_summary": [{"path": "test.py", "description": "A test file", "functions": ["hello", "world"]}],
            "implemented_features": ["Feature A"],
            "missing_features": ["Missing B"],
            "recommendations": ["Do C"],
            "structure_text": "- (root)/\n  - files: test.py",
            "pages": [],
            "link_issues": [],
        }
        html = build_html(analysis, "@startuml\n@enduml", "@startmindmap\n@endmindmap", "", Path("/tmp"))
        assert "TestMod" in html
        assert "Feature A" in html
        assert "Missing B" in html
        assert "Do C" in html

    def test_with_link_issues(self):
        from project_overview import build_html
        analysis = {
            "modules": [],
            "files_summary": [],
            "implemented_features": [],
            "missing_features": [],
            "recommendations": [],
            "structure_text": "",
            "pages": ["index.html"],
            "link_issues": [{"source": "index.html", "link": "broken.css", "resolved": "/tmp/broken.css"}],
        }
        html = build_html(analysis, "", "", "", Path("/tmp"))
        assert "broken.css" in html
        assert "リンク/参照の欠落" in html

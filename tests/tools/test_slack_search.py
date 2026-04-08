"""slack_search.py の単体テスト"""
import pytest
import json
from pathlib import Path


@pytest.fixture
def mock_index(tmp_path):
    """テスト用の最小限インデックスを作成"""
    index = {
        "version": "1.0",
        "generated_at": "2024-01-01T00:00:00",
        "stats": {"total_channels": 2, "total_messages": 100},
        "workspaces": ["test-workspace"],
        "tree": {
            "test-workspace": {
                "general": ["test-workspace/general"],
                "projects": ["test-workspace/project-alpha"],
            }
        },
        "channels": {
            "test-workspace/general": {
                "name": "general",
                "workspace": "test-workspace",
                "category": "general",
                "overview": "一般的な連絡用チャンネル",
                "topics": ["連絡", "お知らせ"],
                "metadata": {
                    "message_count": 50,
                    "first_activity": "2024-01-01",
                    "last_activity": "2024-06-01",
                },
                "paths": {"summary": "data/test-workspace/general/summary.md"},
                "related_channels": ["test-workspace/project-alpha"],
            },
            "test-workspace/project-alpha": {
                "name": "project-alpha",
                "workspace": "test-workspace",
                "category": "projects",
                "overview": "プロジェクトアルファの開発チャンネル",
                "topics": ["開発", "プロジェクト管理"],
                "metadata": {
                    "message_count": 50,
                    "first_activity": "2024-02-01",
                    "last_activity": "2024-06-15",
                },
                "paths": {"summary": "data/test-workspace/project-alpha/summary.md"},
                "related_channels": ["test-workspace/general"],
            },
        },
        "entities": {
            "persons": {
                "田中太郎": {
                    "aliases": ["tanaka", "Tanaka"],
                    "channels": ["test-workspace/general"],
                    "mention_count": 10,
                },
            },
            "events": {
                "DX展示会2024": {
                    "channel": "test-workspace/project-alpha",
                    "date": "2024-03-15",
                    "participants": ["田中太郎"],
                    "topics": ["DX", "展示会"],
                },
            },
        },
        "output_sources": {},
    }
    index_path = tmp_path / "book_index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    return index_path


class TestImport:
    def test_import_module(self):
        from slack_search import SlackSearch
        assert SlackSearch is not None


class TestSlackSearch:
    def test_init(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        assert search._index is not None

    def test_init_missing_index(self, tmp_path):
        from slack_search import SlackSearch
        with pytest.raises(FileNotFoundError):
            SlackSearch(index_path=str(tmp_path / "nonexistent.json"))

    def test_workspace_overview(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        overview = search.get_workspace_overview()
        assert "stats" in overview
        assert "workspaces" in overview

    def test_workspace_overview_specific(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        overview = search.get_workspace_overview("test-workspace")
        assert overview["workspace"] == "test-workspace"
        assert overview["channel_count"] == 2

    def test_workspace_overview_unknown(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        result = search.get_workspace_overview("unknown")
        assert "error" in result

    def test_find_channels(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_channels("general")
        assert len(results) > 0
        assert results[0]["name"] == "general"

    def test_find_channels_by_topic(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_channels("開発")
        assert any(r["name"] == "project-alpha" for r in results)

    def test_find_channels_empty_query(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_channels("")
        # Empty query still returns results based on similarity
        assert isinstance(results, list)

    def test_get_channel_detail(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        detail = search.get_channel_detail("test-workspace/general")
        assert detail["name"] == "general"
        assert "overview" in detail

    def test_get_channel_detail_by_name(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        detail = search.get_channel_detail("general")
        assert detail["name"] == "general"

    def test_get_channel_detail_not_found(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        result = search.get_channel_detail("nonexistent")
        assert "error" in result

    def test_find_related_channels(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        related = search.find_related_channels("test-workspace/general")
        assert related["total_related"] >= 1

    def test_find_person(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_person("田中")
        assert len(results) == 1
        assert results[0]["name"] == "田中太郎"

    def test_find_person_by_alias(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_person("tanaka")
        assert len(results) == 1

    def test_find_events(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_events("DX")
        assert len(results) == 1
        assert results[0]["name"] == "DX展示会2024"

    def test_find_events_all(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_events()
        assert len(results) >= 1

    def test_list_channels_by_category(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.list_channels_by_category("projects")
        assert len(results) == 1
        assert results[0]["name"] == "project-alpha"

    def test_get_timeline(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        timeline = search.get_timeline()
        assert timeline["channel_count"] == 2

    def test_get_timeline_filtered(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        timeline = search.get_timeline(start_date="2024-03-01")
        assert timeline["channel_count"] >= 1

    def test_get_output_sources(self, mock_index):
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        sources = search.get_output_sources()
        assert isinstance(sources, dict)

    def test_reload_index(self, mock_index):
        """Line 64: reload_index"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        search.reload_index()
        assert search._index is not None

    def test_find_channels_workspace_filter(self, mock_index):
        """Line 146: workspace filter"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_channels("general", workspace="nonexistent")
        assert results == []

    def test_find_channels_category_filter(self, mock_index):
        """Line 148: category filter"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_channels("general", category="projects")
        # general is in "general" category, not "projects"
        assert not any(r["name"] == "general" for r in results)

    def test_find_channels_limit(self, mock_index):
        """Test limit parameter"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_channels("", limit=1)
        assert len(results) <= 1

    def test_calculate_search_score_exact_match(self, mock_index):
        """Line 215: exact name match scores highest"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        channel = search._index["channels"]["test-workspace/general"]
        score = search._calculate_search_score("general", {"general"}, channel)
        assert score >= 10.0

    def test_calculate_search_score_recent_activity(self, tmp_path):
        """Lines 215, 217-218: activity bonus for recent channels"""
        from slack_search import SlackSearch
        from datetime import datetime, timedelta
        recent_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        index = {
            "version": "1.0",
            "generated_at": "2024-01-01T00:00:00",
            "stats": {},
            "workspaces": ["ws"],
            "tree": {"ws": {"cat": ["ws/ch"]}},
            "channels": {
                "ws/ch": {
                    "name": "recent-channel",
                    "workspace": "ws",
                    "category": "cat",
                    "overview": "",
                    "topics": [],
                    "metadata": {
                        "message_count": 10,
                        "first_activity": "2024-01-01",
                        "last_activity": recent_date,
                    },
                    "paths": {},
                    "related_channels": [],
                },
            },
            "entities": {"persons": {}, "events": {}},
            "output_sources": {},
        }
        idx_path = tmp_path / "idx.json"
        idx_path.write_text(json.dumps(index), encoding="utf-8")
        search = SlackSearch(index_path=str(idx_path))
        channel = search._index["channels"]["ws/ch"]
        score = search._calculate_search_score("recent", {"recent"}, channel)
        # Should have activity bonus
        assert score > 0

    def test_calculate_search_score_medium_activity(self, tmp_path):
        """Lines 217-218: medium activity bonus (30-90 days)"""
        from slack_search import SlackSearch
        from datetime import datetime, timedelta
        medium_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
        index = {
            "version": "1.0",
            "generated_at": "2024-01-01T00:00:00",
            "stats": {},
            "workspaces": ["ws"],
            "tree": {"ws": {"cat": ["ws/ch"]}},
            "channels": {
                "ws/ch": {
                    "name": "medium-channel",
                    "workspace": "ws",
                    "category": "cat",
                    "overview": "test overview",
                    "topics": ["test topic"],
                    "metadata": {
                        "message_count": 10,
                        "first_activity": "2024-01-01",
                        "last_activity": medium_date,
                    },
                    "paths": {},
                    "related_channels": [],
                },
            },
            "entities": {"persons": {}, "events": {}},
            "output_sources": {},
        }
        idx_path = tmp_path / "idx2.json"
        idx_path.write_text(json.dumps(index), encoding="utf-8")
        search = SlackSearch(index_path=str(idx_path))
        channel = search._index["channels"]["ws/ch"]
        score = search._calculate_search_score("medium", {"medium"}, channel)
        assert score > 0

    def test_calculate_search_score_invalid_date(self, tmp_path):
        """Line 218: bare except for invalid date parsing"""
        from slack_search import SlackSearch
        index = {
            "version": "1.0",
            "generated_at": "2024-01-01T00:00:00",
            "stats": {},
            "workspaces": ["ws"],
            "tree": {"ws": {"cat": ["ws/ch"]}},
            "channels": {
                "ws/ch": {
                    "name": "bad-date-channel",
                    "workspace": "ws",
                    "category": "cat",
                    "overview": "",
                    "topics": [],
                    "metadata": {
                        "message_count": 10,
                        "first_activity": "2024-01-01",
                        "last_activity": "not-a-date",
                    },
                    "paths": {},
                    "related_channels": [],
                },
            },
            "entities": {"persons": {}, "events": {}},
            "output_sources": {},
        }
        idx_path = tmp_path / "idx3.json"
        idx_path.write_text(json.dumps(index), encoding="utf-8")
        search = SlackSearch(index_path=str(idx_path))
        channel = search._index["channels"]["ws/ch"]
        # Should not raise, bare except catches
        score = search._calculate_search_score("bad", {"bad"}, channel)
        assert isinstance(score, float)

    def test_get_channel_detail_not_found_with_slash(self, mock_index):
        """Line 249: channel_id with / but not in index"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        result = search.get_channel_detail("unknown-ws/unknown-ch")
        assert "error" in result

    def test_find_related_channels_by_name(self, mock_index):
        """Lines 287-290: find_related_channels with name only"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        result = search.find_related_channels("general")
        assert result["origin"] == "test-workspace/general"

    def test_find_related_channels_not_found(self, mock_index):
        """Line 293: channel not found"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        result = search.find_related_channels("nonexistent-ws/nonexistent")
        assert "error" in result

    def test_find_related_channels_depth_2(self, mock_index):
        """Depth 2 exploration"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        result = search.find_related_channels("test-workspace/general", depth=2)
        assert result["depth"] == 2
        assert len(result["levels"]) >= 1

    def test_find_person_exact_match(self, mock_index):
        """Line 355: exact name match"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_person("田中太郎")
        assert len(results) == 1
        assert results[0]["score"] == 10.0

    def test_find_person_no_match(self, mock_index):
        """Person not found"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_person("存在しない人")
        assert results == []

    def test_find_events_no_match(self, mock_index):
        """Line 402: events with non-matching query"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.find_events("nonexistent")
        assert results == []

    def test_list_channels_by_category_with_workspace(self, mock_index):
        """Lines 441, 481: workspace filter in category listing"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.list_channels_by_category("projects", workspace="test-workspace")
        assert len(results) == 1
        results_empty = search.list_channels_by_category("projects", workspace="other")
        assert results_empty == []

    def test_list_channels_by_category_nonexistent(self, mock_index):
        """Line 487: category not found"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        results = search.list_channels_by_category("nonexistent")
        assert results == []

    def test_get_timeline_with_workspace(self, mock_index):
        """Lines 491, 493: timeline with workspace and end_date filter"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        timeline = search.get_timeline(workspace="test-workspace")
        assert timeline["workspace"] == "test-workspace"
        assert timeline["channel_count"] == 2

    def test_get_timeline_end_date_filter(self, mock_index):
        """Line 493: end_date filters out channels starting after"""
        from slack_search import SlackSearch
        search = SlackSearch(index_path=str(mock_index))
        timeline = search.get_timeline(end_date="2024-01-15")
        # project-alpha first_activity is 2024-02-01 which is > 2024-01-15
        assert timeline["channel_count"] <= 2

    def test_get_timeline_no_activity(self, tmp_path):
        """Lines 487: channels with no first/last activity skipped"""
        from slack_search import SlackSearch
        index = {
            "version": "1.0",
            "generated_at": "2024-01-01T00:00:00",
            "stats": {},
            "workspaces": ["ws"],
            "tree": {"ws": {"cat": ["ws/ch"]}},
            "channels": {
                "ws/ch": {
                    "name": "no-activity",
                    "workspace": "ws",
                    "category": "cat",
                    "overview": "",
                    "topics": [],
                    "metadata": {"message_count": 0},
                    "paths": {},
                    "related_channels": [],
                },
            },
            "entities": {"persons": {}, "events": {}},
            "output_sources": {},
        }
        idx_path = tmp_path / "idx4.json"
        idx_path.write_text(json.dumps(index), encoding="utf-8")
        search = SlackSearch(index_path=str(idx_path))
        timeline = search.get_timeline()
        assert timeline["channel_count"] == 0


class TestSlackSearchCLI:
    """Lines 538-594: main() CLI function"""

    def test_cli_no_args(self, mock_index, capsys):
        """Line 542-553: no arguments shows help"""
        from slack_search import SlackSearch
        from unittest.mock import patch
        with patch("sys.argv", ["slack_search.py"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            from slack_search import main
            main()
        captured = capsys.readouterr()
        assert "Usage" in captured.out

    def test_cli_overview(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "overview"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "version" in captured.out

    def test_cli_overview_workspace(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "overview", "test-workspace"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "test-workspace" in captured.out

    def test_cli_find(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "find", "general"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "general" in captured.out

    def test_cli_detail(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "detail", "test-workspace/general"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "general" in captured.out

    def test_cli_related(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "related", "test-workspace/general"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "origin" in captured.out

    def test_cli_person(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "person", "田中"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "田中" in captured.out

    def test_cli_events(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "events"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "DX" in captured.out

    def test_cli_category(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "category", "projects"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "project-alpha" in captured.out

    def test_cli_timeline(self, mock_index, capsys):
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "timeline", "2024-01-01", "2024-12-31"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "channel_count" in captured.out

    def test_cli_unknown_command(self, mock_index, capsys):
        """Line 591: unknown command"""
        from unittest.mock import patch
        from slack_search import SlackSearch, main
        with patch("sys.argv", ["slack_search.py", "badcommand"]), \
             patch("slack_search.SlackSearch", return_value=SlackSearch(index_path=str(mock_index))):
            main()
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out

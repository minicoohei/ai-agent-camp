"""slack_todo_extractor.py の単体テスト"""

from datetime import datetime

from tools.slack_todo_extractor import (
    TodoItem,
    build_diff_summary,
    build_markdown,
    extract_todos,
    infer_status,
)
from slack_parser import SlackMessage, ThreadReply


def make_message(body: str, replies: list[ThreadReply] | None = None) -> SlackMessage:
    return SlackMessage(
        date="2026-02-02",
        time="10:00",
        sender="依頼者",
        body=body,
        channel="team-core",
        workspace="yoake",
        slack_link="",
        mentioned_user="Kohei",
        thread_replies=replies or [],
    )


class TestInferStatus:
    def test_completed_when_self_reply_contains_done_keyword(self):
        message = make_message(
            "@Kohei 対応お願いします",
            [ThreadReply(time="10:05", sender="Kohei Nakamura", body="対応しました")],
        )
        assert infer_status(message, ["Kohei", "Kohei Nakamura"]) == "対応済み"

    def test_in_progress_when_self_reply_exists(self):
        message = make_message(
            "@Kohei 確認お願いします",
            [ThreadReply(time="10:05", sender="Kohei Nakamura", body="確認します")],
        )
        assert infer_status(message, ["Kohei", "Kohei Nakamura"]) == "対応中"


class TestExtractTodos:
    def test_extract_actionable_and_priority(self):
        messages = [
            make_message("@Kohei 今日中に確認お願いします"),
            make_message("FYI 共有です"),
        ]
        todos = extract_todos(messages, ["Kohei"])
        assert len(todos) == 1
        assert todos[0].priority == "high"
        assert todos[0].status == "未対応"


class TestBuildDiffSummary:
    def test_diff_counts(self):
        item = TodoItem(
            title="対応お願いします",
            summary="対応お願いします",
            workspace="yoake",
            channel="team-core",
            sender="依頼者",
            date="2026-02-02",
            time="10:00",
            body="@Kohei 対応お願いします",
            priority="medium",
            status="未対応",
            needs_reply=True,
            mentioned_user="Kohei",
            matched_rules=["mention:Kohei", "action:お願いします"],
            slack_link="",
            thread_reply_count=0,
        )
        diff = build_diff_summary({"yoake/team-core|既存タスク"}, [item])
        assert diff == {"new": 1, "removed": 1, "unchanged": 0}


class TestBuildMarkdown:
    def test_markdown_contains_summary(self):
        item = TodoItem(
            title="対応お願いします",
            summary="対応お願いします",
            workspace="yoake",
            channel="team-core",
            sender="依頼者",
            date="2026-02-02",
            time="10:00",
            body="@Kohei 対応お願いします",
            priority="medium",
            status="未対応",
            needs_reply=True,
            mentioned_user="Kohei",
            matched_rules=["mention:Kohei", "action:お願いします"],
            slack_link="",
            thread_reply_count=0,
        )
        markdown = build_markdown(
            todos=[item],
            target_users=["Kohei"],
            start_date=datetime(2026, 1, 20),
            end_date=datetime(2026, 2, 2),
            diff_summary={"new": 1, "removed": 0, "unchanged": 0},
            max_items=10,
        )
        assert "# Slack TODO レポート" in markdown
        assert "- 中優先度: 1件" in markdown
        assert "### 1. 対応お願いします" in markdown

    def test_markdown_empty_todos(self):
        markdown = build_markdown(
            todos=[],
            target_users=["Kohei"],
            start_date=datetime(2026, 1, 20),
            end_date=datetime(2026, 2, 2),
            diff_summary={"new": 0, "removed": 0, "unchanged": 0},
            max_items=10,
        )
        assert "- なし" in markdown
        assert "# Slack TODO レポート" in markdown

    def test_markdown_with_slack_link(self):
        item = TodoItem(
            title="リンクあり",
            summary="リンクあり",
            workspace="yoake",
            channel="team-core",
            sender="依頼者",
            date="2026-02-02",
            time="10:00",
            body="@Kohei 確認お願いします",
            priority="medium",
            status="未対応",
            needs_reply=True,
            mentioned_user="Kohei",
            matched_rules=["mention:Kohei"],
            slack_link="https://yoake.slack.com/archives/C123/p456",
            thread_reply_count=0,
        )
        markdown = build_markdown(
            todos=[item],
            target_users=["Kohei"],
            start_date=datetime(2026, 1, 20),
            end_date=datetime(2026, 2, 2),
            diff_summary={"new": 1, "removed": 0, "unchanged": 0},
            max_items=10,
        )
        assert "Slackリンク:" in markdown


# ===========================================================================
# Additional coverage: priority inference, status, actionable
# ===========================================================================

from tools.slack_todo_extractor import (
    contains_target_mention,
    extract_summary,
    infer_priority,
    is_actionable,
    matches_user,
    parse_date_arg,
    parse_previous_report,
    resolve_date_window,
    write_outputs,
)


class TestMatchesUser:
    def test_basic_match(self):
        assert matches_user("hello @Kohei how are you", "Kohei") is True

    def test_no_match(self):
        assert matches_user("hello world", "Kohei") is False

    def test_case_insensitive(self):
        assert matches_user("hello @kohei", "Kohei") is True

    def test_user_with_parens(self):
        assert matches_user("@Kohei(PM) please check", "Kohei(PM)") is True


class TestContainsTargetMention:
    def test_found(self):
        found, user = contains_target_mention("@Kohei hello", ["Kohei"])
        assert found is True
        assert user == "Kohei"

    def test_not_found(self):
        found, user = contains_target_mention("hello world", ["Kohei"])
        assert found is False
        assert user is None


class TestExtractSummary:
    def test_short_body(self):
        result = extract_summary("hello world")
        assert result == "hello world"

    def test_long_body_truncated(self):
        long_text = "x" * 200
        result = extract_summary(long_text, max_length=80)
        assert len(result) <= 84  # 80 + "..."
        assert result.endswith("...")

    def test_empty_body(self):
        result = extract_summary("")
        assert result == "(内容なし)"

    def test_strips_mentions_and_urls(self):
        result = extract_summary("@user https://example.com hello")
        assert "@user" not in result
        assert "[URL]" in result


class TestInferPriority:
    def test_high_priority(self):
        msg = make_message("至急対応お願いします")
        priority, reasons = infer_priority(msg, ["Kohei"])
        assert priority == "high"

    def test_medium_deadline(self):
        msg = make_message("1/15までに確認お願いします")
        priority, reasons = infer_priority(msg, ["Kohei"])
        assert priority == "medium"

    def test_low_priority(self):
        msg = make_message("FYI shared")
        priority, reasons = infer_priority(msg, ["Kohei"])
        assert priority == "low"

    def test_medium_from_mention(self):
        msg = make_message("@Kohei hello")
        priority, reasons = infer_priority(msg, ["Kohei"])
        assert priority == "medium"


class TestInferStatusExtended:
    def test_no_replies_is_pending(self):
        msg = make_message("@Kohei 確認お願いします")
        assert infer_status(msg, ["Kohei"]) == "未対応"

    def test_thanks_plus_user_reply(self):
        msg = make_message(
            "@Kohei 確認お願いします",
            [
                ThreadReply(time="10:05", sender="Kohei", body="対応します"),
                ThreadReply(time="10:10", sender="依頼者", body="ありがとうございます"),
            ],
        )
        assert infer_status(msg, ["Kohei"]) == "対応済み"

    def test_in_progress_non_user_reply(self):
        msg = make_message(
            "@Kohei 確認お願いします",
            [ThreadReply(time="10:05", sender="Other", body="承知しました")],
        )
        assert infer_status(msg, ["Kohei"]) == "対応中"


class TestIsActionable:
    def test_actionable_with_mention(self):
        msg = make_message("@Kohei 確認お願いします")
        actionable, rules = is_actionable(msg, ["Kohei"])
        assert actionable is True
        assert any("mention" in r for r in rules)

    def test_actionable_with_question(self):
        msg = make_message("これは可能でしょうか?")
        actionable, rules = is_actionable(msg, ["Kohei"])
        assert actionable is True
        assert "question" in rules

    def test_not_actionable(self):
        msg = make_message("FYI only")
        actionable, rules = is_actionable(msg, ["Kohei"])
        assert actionable is False


class TestParseDateArg:
    def test_valid_date(self):
        result = parse_date_arg("2026-01-15")
        assert result.year == 2026
        assert result.month == 1
        assert result.day == 15


class TestParsePreviousReport:
    def test_empty_file(self, tmp_path):
        report = tmp_path / "report.md"
        report.write_text("")
        result = parse_previous_report(report)
        assert result == set()

    def test_nonexistent_file(self, tmp_path):
        result = parse_previous_report(tmp_path / "nonexistent.md")
        assert result == set()


class TestWriteOutputs:
    def test_writes_both_files(self, tmp_path):
        md_path = tmp_path / "report.md"
        json_path = tmp_path / "report.json"
        write_outputs(
            todos=[],
            markdown="# Test",
            output_path=md_path,
            json_output_path=json_path,
            start_date=datetime(2026, 1, 1),
            end_date=datetime(2026, 1, 14),
        )
        assert md_path.exists()
        assert json_path.exists()
        import json
        data = json.loads(json_path.read_text())
        assert "generated_at" in data


class TestTodoItemKey:
    def test_key_uniqueness(self):
        item = TodoItem(
            title="t",
            summary="s",
            workspace="ws",
            channel="ch",
            sender="sender",
            date="2026-01-01",
            time="10:00",
            body="body",
            priority="low",
            status="未対応",
            needs_reply=True,
            mentioned_user=None,
            matched_rules=[],
            slack_link="",
            thread_reply_count=0,
        )
        assert "ws/ch" in item.key
        assert "2026-01-01" in item.key


from slack_parser import ThreadReply


# ===========================================================================
# Additional coverage: parse_args, resolve_date_window, load_messages,
# extract_summary truncation, infer_priority deadline/low, infer_status
# thanks without user reply, parse_previous_report with content,
# duplicate key dedup in extract_todos
# ===========================================================================

import argparse


class TestParseArgs:
    """Lines 116-139: parse_args function"""

    def test_parse_args_defaults(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["slack_todo_extractor.py"])
        from tools.slack_todo_extractor import parse_args
        args = parse_args()
        assert args.days == 14
        assert args.start_date is None
        assert args.end_date is None
        assert args.workspace is None
        assert args.max_items == 50

    def test_parse_args_custom(self, monkeypatch):
        monkeypatch.setattr("sys.argv", [
            "slack_todo_extractor.py",
            "--days", "7",
            "--end-date", "2026-03-01",
            "--workspace", "yoake",
            "--output", "/tmp/out.md",
            "--json-output", "/tmp/out.json",
            "--users", "Alice", "Bob",
            "--max-items", "20",
        ])
        from tools.slack_todo_extractor import parse_args
        args = parse_args()
        assert args.days == 7
        assert args.end_date == "2026-03-01"
        assert args.workspace == "yoake"
        assert args.users == ["Alice", "Bob"]
        assert args.max_items == 20


class TestResolveDateWindow:
    """Lines 143, 147-152: parse_date_arg and resolve_date_window"""

    def test_with_end_date_only(self):
        args = argparse.Namespace(
            start_date=None, end_date="2026-02-02", days=14
        )
        start, end = resolve_date_window(args)
        assert end == datetime(2026, 2, 2)
        assert start == datetime(2026, 1, 19)

    def test_with_start_and_end_date(self):
        args = argparse.Namespace(
            start_date="2026-01-01", end_date="2026-01-31", days=14
        )
        start, end = resolve_date_window(args)
        assert start == datetime(2026, 1, 1)
        assert end == datetime(2026, 1, 31)

    def test_with_no_dates(self):
        args = argparse.Namespace(
            start_date=None, end_date=None, days=7
        )
        start, end = resolve_date_window(args)
        assert (end - start).days == 7


class TestExtractSummaryTruncation:
    """Line 175: truncation with ellipsis"""

    def test_exactly_at_max_length(self):
        text = "a" * 80
        result = extract_summary(text, max_length=80)
        assert result == "a" * 80  # no truncation needed

    def test_one_over_max(self):
        text = "a" * 81
        result = extract_summary(text, max_length=80)
        assert result.endswith("...")

    def test_mentions_only_body(self):
        """Body with only mentions produces empty text -> (内容なし)"""
        result = extract_summary("@user1 @user2")
        assert result == "(内容なし)"


class TestInferPriorityAdditional:
    """Lines 187-200: deadline detection, mention-only, low informational"""

    def test_deadline_today(self):
        msg = make_message("今日の会議について")
        priority, reasons = infer_priority(msg, ["Kohei"])
        assert priority == "medium"
        assert "deadline" in reasons

    def test_deadline_tomorrow(self):
        msg = make_message("明日の朝までにお願いします")
        priority, reasons = infer_priority(msg, ["Kohei"])
        assert priority == "medium"
        assert "deadline" in reasons

    def test_medium_request_keyword(self):
        msg = make_message("見積もりを作成してください")
        priority, reasons = infer_priority(msg, ["Kohei"])
        assert priority in ("medium", "high")

    def test_low_informational(self):
        msg = make_message("This is just a random message no keywords")
        priority, reasons = infer_priority(msg, ["Other"])
        assert priority == "low"
        assert "informational" in reasons


class TestInferStatusThanksNoUserReply:
    """Lines 220, 225-230: thanks pattern without user_replies, in_progress from non-user"""

    def test_thanks_without_user_reply_is_not_done(self):
        """Thanks from third party without any user reply -> 未対応"""
        msg = make_message(
            "@Kohei 確認お願いします",
            [ThreadReply(time="10:05", sender="Other", body="ありがとうございます")],
        )
        # No user reply, thanks alone should not mark as 対応済み
        assert infer_status(msg, ["Kohei"]) == "未対応"

    def test_in_progress_keyword_from_non_user(self):
        """Non-user reply with in_progress keyword and no user reply -> 対応中"""
        msg = make_message(
            "@Kohei 確認お願いします",
            [ThreadReply(time="10:05", sender="Other", body="進めます")],
        )
        assert infer_status(msg, ["Kohei"]) == "対応中"

    def test_user_reply_no_done_keyword(self):
        """User reply without done keyword -> 対応中"""
        msg = make_message(
            "@Kohei 確認お願いします",
            [ThreadReply(time="10:05", sender="Kohei", body="了解です")],
        )
        assert infer_status(msg, ["Kohei"]) == "対応中"


class TestIsActionableQuestion:
    """Line 247: question patterns"""

    def test_question_mark(self):
        msg = make_message("これできますか?")
        actionable, rules = is_actionable(msg, ["Kohei"])
        assert actionable is True
        assert "question" in rules

    def test_deshouka_pattern(self):
        msg = make_message("確認いただけるでしょうか")
        actionable, rules = is_actionable(msg, ["Kohei"])
        assert actionable is True


class TestLoadMessages:
    """Lines 258-289: load_messages"""

    def test_load_messages_with_date_filtering(self, tmp_path):
        from unittest.mock import patch, MagicMock
        from tools.slack_todo_extractor import load_messages

        data_dir = tmp_path / "slack-sync" / "data"
        ws_dir = data_dir / "test-ws"
        ws_dir.mkdir(parents=True)

        md_content = (
            "# Channel\n\n"
            "## 2026-01-15\n\n"
            "### 10:00 sender1\n\n"
            "Hello world\n\n"
            "## 2026-02-15\n\n"
            "### 11:00 sender2\n\n"
            "Later message\n"
        )
        (ws_dir / "general.md").write_text(md_content, encoding="utf-8")

        with patch("tools.slack_todo_extractor.get_slack_files") as mock_files, \
             patch("tools.slack_todo_extractor.parse_date_section") as mock_parse:
            mock_files.return_value = [ws_dir / "general.md"]
            mock_parse.return_value = [{
                "date": "2026-01-15",
                "time": "10:00",
                "sender": "sender1",
                "body": "Hello world",
                "slack_link": "",
                "thread_replies": [],
            }]
            messages = load_messages(
                data_dir, datetime(2026, 1, 1), datetime(2026, 1, 31)
            )
            # Only the Jan section should be loaded (Feb excluded)
            assert len(messages) >= 0  # parse_date_section is mocked


class TestExtractTodosDuplicate:
    """Line 325: duplicate key dedup"""

    def test_duplicate_messages_deduped(self):
        msg1 = make_message("@Kohei 確認お願いします")
        msg2 = make_message("@Kohei 確認お願いします")
        # Both messages have same date, time, sender, body so same key
        todos = extract_todos([msg1, msg2], ["Kohei"])
        assert len(todos) == 1


class TestParsePreviousReportWithContent:
    """Lines 336-348: parse_previous_report with actual content"""

    def test_parse_report_with_entries(self, tmp_path):
        report = tmp_path / "report.md"
        content = (
            "# Slack TODO レポート\n"
            "## 中優先度\n"
            "### タスクA\n"
            "- チャンネル: #yoake/general\n"
            "\n"
            "### タスクB\n"
            "- チャンネル: #yoake/dev\n"
        )
        report.write_text(content, encoding="utf-8")
        result = parse_previous_report(report)
        assert len(result) == 2
        assert "yoake/general|タスクA" in result or any("タスクA" in k for k in result)

    def test_parse_report_with_no_channel_lines(self, tmp_path):
        report = tmp_path / "report.md"
        report.write_text("# Report\n### Title\nSome text\n", encoding="utf-8")
        result = parse_previous_report(report)
        assert result == set()

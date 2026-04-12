"""check-inbox/scripts/slack_parser.py の単体テスト"""
import pytest


class TestImport:
    def test_import_module(self):
        import slack_parser
        assert hasattr(slack_parser, 'parse_date_section')
        assert hasattr(slack_parser, 'extract_task_summary')
        assert hasattr(slack_parser, 'has_reply_from_user')
        assert hasattr(slack_parser, 'SlackMessage')


class TestParseDateSection:
    def test_basic_message(self):
        from slack_parser import parse_date_section
        content = """### 10:30 - Tanaka [[Slack]](https://slack.com/link1)
こんにちは @TestUser、タスクの確認お願いします。
"""
        messages = parse_date_section(content, "2026-01-15")
        assert len(messages) == 1
        assert messages[0]["time"] == "10:30"
        assert messages[0]["sender"] == "Tanaka"
        assert messages[0]["date"] == "2026-01-15"
        assert "タスクの確認" in messages[0]["body"]

    def test_multiple_messages(self):
        from slack_parser import parse_date_section
        content = """### 09:00 - Alice [[Slack]](https://slack.com/a)
Morning message

### 14:00 - Bob [[Slack]](https://slack.com/b)
Afternoon message
"""
        messages = parse_date_section(content, "2026-01-15")
        assert len(messages) == 2
        assert messages[0]["sender"] == "Alice"
        assert messages[1]["sender"] == "Bob"

    def test_empty_content(self):
        from slack_parser import parse_date_section
        messages = parse_date_section("", "2026-01-15")
        assert messages == []

    def test_no_slack_link(self):
        from slack_parser import parse_date_section
        content = """### 10:00 - NoLink
メッセージ本文
"""
        messages = parse_date_section(content, "2026-01-15")
        assert len(messages) == 1
        assert messages[0]["slack_link"] == ""


class TestExtractTaskSummary:
    def test_basic(self):
        from slack_parser import extract_task_summary
        result = extract_task_summary("@TestUser タスクをお願いします")
        assert "タスクをお願いします" in result
        assert "@TestUser" not in result

    def test_url_replaced(self):
        from slack_parser import extract_task_summary
        result = extract_task_summary("Check https://example.com/path please")
        assert "[URL]" in result
        assert "https://example.com" not in result

    def test_truncation(self):
        from slack_parser import extract_task_summary
        result = extract_task_summary("あ" * 200, max_length=50)
        assert len(result) <= 54  # 50 + "..."

    def test_newlines_converted(self):
        from slack_parser import extract_task_summary
        result = extract_task_summary("line1\nline2\nline3")
        assert "\n" not in result


class TestHasReplyFromUser:
    def test_has_reply(self):
        from slack_parser import has_reply_from_user, SlackMessage, ThreadReply
        msg = SlackMessage(
            date="2026-01-15", time="10:00", sender="Alice",
            body="test", channel="general", workspace="ws",
            slack_link="", mentioned_user="TestUser",
            thread_replies=[
                ThreadReply(time="10:05", sender="TestUser", body="ok")
            ]
        )
        assert has_reply_from_user(msg, ["TestUser"]) is True

    def test_no_reply(self):
        from slack_parser import has_reply_from_user, SlackMessage, ThreadReply
        msg = SlackMessage(
            date="2026-01-15", time="10:00", sender="Alice",
            body="test", channel="general", workspace="ws",
            slack_link="", mentioned_user="TestUser",
            thread_replies=[
                ThreadReply(time="10:05", sender="Bob", body="ok")
            ]
        )
        assert has_reply_from_user(msg, ["TestUser"]) is False

    def test_empty_replies(self):
        from slack_parser import has_reply_from_user, SlackMessage
        msg = SlackMessage(
            date="2026-01-15", time="10:00", sender="Alice",
            body="test", channel="general", workspace="ws",
            slack_link="", mentioned_user="TestUser",
            thread_replies=[]
        )
        assert has_reply_from_user(msg, ["TestUser"]) is False

    def test_case_insensitive(self):
        from slack_parser import has_reply_from_user, SlackMessage, ThreadReply
        msg = SlackMessage(
            date="2026-01-15", time="10:00", sender="Alice",
            body="test", channel="general", workspace="ws",
            slack_link="", mentioned_user="testuser",
            thread_replies=[
                ThreadReply(time="10:05", sender="TESTUSER", body="replied")
            ]
        )
        assert has_reply_from_user(msg, ["testuser"]) is True

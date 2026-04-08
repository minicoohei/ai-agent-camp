"""check-inbox/scripts/common.py の単体テスト"""
import pytest
from datetime import datetime, timedelta


class TestImport:
    def test_import_module(self):
        import common
        assert hasattr(common, 'get_date_range')
        assert hasattr(common, 'TaskItem')
        assert hasattr(common, 'format_task_markdown')
        assert hasattr(common, 'generate_output_markdown')


class TestGetDateRange:
    def test_basic(self):
        from common import get_date_range
        start, end = get_date_range(3)
        assert start < end
        diff = end - start
        assert diff.days >= 2

    def test_one_day(self):
        from common import get_date_range
        start, end = get_date_range(1)
        assert start.date() == end.date()

    def test_start_at_midnight(self):
        from common import get_date_range
        start, _ = get_date_range(5)
        assert start.hour == 0
        assert start.minute == 0
        assert start.second == 0

    def test_zero_days_raises(self):
        from common import get_date_range
        with pytest.raises(ValueError):
            get_date_range(0)

    def test_negative_days_raises(self):
        from common import get_date_range
        with pytest.raises(ValueError):
            get_date_range(-1)


class TestFormatTaskMarkdown:
    def test_email_task(self):
        from common import TaskItem, format_task_markdown
        task = TaskItem(
            source="email",
            title="重要なメール",
            content="本文テスト",
            sender="田中太郎",
            date="2026-01-01",
            time="10:00",
            priority="high",
            reason="返信必要",
            draft_reply="承知しました",
            link="https://example.com",
        )
        md = format_task_markdown(task)
        assert "重要なメール" in md
        assert "田中太郎" in md
        assert "返信必要" in md
        assert "承知しました" in md
        assert "https://example.com" in md

    def test_slack_task(self):
        from common import TaskItem, format_task_markdown
        task = TaskItem(
            source="slack",
            title="Slack通知",
            content="テスト内容",
            sender="佐藤次郎",
            date="2026-01-01",
            time="14:30",
            priority="medium",
            reason="メンションあり",
            draft_reply="確認します",
            channel="general",
        )
        md = format_task_markdown(task)
        assert "general" in md
        assert "佐藤次郎" in md
        assert "テスト内容" in md

    def test_slack_long_content_truncated(self):
        from common import TaskItem, format_task_markdown
        task = TaskItem(
            source="slack",
            title="長い内容",
            content="あ" * 200,
            sender="sender",
            date="2026-01-01",
            time="12:00",
            priority="low",
            reason="test",
            draft_reply="ok",
            channel="ch",
        )
        md = format_task_markdown(task)
        assert "..." in md

    def test_no_link(self):
        from common import TaskItem, format_task_markdown
        task = TaskItem(
            source="email",
            title="No Link",
            content="body",
            sender="sender",
            date="2026-01-01",
            time="10:00",
            priority="low",
            reason="test",
            draft_reply="ok",
            link="",
        )
        md = format_task_markdown(task)
        assert "リンク" not in md


class TestGenerateOutputMarkdown:
    def test_empty_tasks(self):
        from common import generate_output_markdown
        now = datetime.now()
        md = generate_output_markdown([], now - timedelta(days=3), now)
        assert "対応が必要なタスクはありません" in md

    def test_with_tasks(self):
        from common import TaskItem, generate_output_markdown
        now = datetime.now()
        task = TaskItem(
            source="email",
            title="Test",
            content="body",
            sender="sender",
            date="2026-01-01",
            time="10:00",
            priority="high",
            reason="urgent",
            draft_reply="reply",
        )
        md = generate_output_markdown([task], now - timedelta(days=1), now, email_count=5)
        assert "高優先度" in md
        assert "メール件数: 5件" in md

    def test_priority_grouping(self):
        from common import TaskItem, generate_output_markdown
        now = datetime.now()
        tasks = [
            TaskItem(source="email", title="H", content="", sender="s",
                     date="2026-01-01", time="10:00", priority="high",
                     reason="r", draft_reply="d"),
            TaskItem(source="slack", title="L", content="", sender="s",
                     date="2026-01-01", time="10:00", priority="low",
                     reason="r", draft_reply="d", channel="ch"),
        ]
        md = generate_output_markdown(tasks, now - timedelta(days=1), now)
        assert "高優先度" in md
        assert "低優先度" in md

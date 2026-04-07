"""check-inbox/scripts/email_parser.py の単体テスト"""
import pytest
from datetime import datetime


class TestImport:
    def test_import_module(self):
        import email_parser
        assert hasattr(email_parser, 'parse_sender')
        assert hasattr(email_parser, 'parse_date')
        assert hasattr(email_parser, 'Email')


class TestParseSender:
    def test_name_and_email(self):
        from email_parser import parse_sender
        name, email = parse_sender('John Doe <john@example.com>')
        assert name == "John Doe"
        assert email == "john@example.com"

    def test_quoted_name(self):
        from email_parser import parse_sender
        name, email = parse_sender('"Jane Smith" <jane@example.com>')
        assert name == "Jane Smith"
        assert email == "jane@example.com"

    def test_email_only(self):
        from email_parser import parse_sender
        name, email = parse_sender('user@example.com')
        assert name == "user@example.com"
        assert email == "user@example.com"

    def test_unknown_format(self):
        from email_parser import parse_sender
        name, email = parse_sender('Unknown Sender')
        assert name == "Unknown Sender"
        assert email == ""

    def test_whitespace_stripped(self):
        from email_parser import parse_sender
        name, email = parse_sender('  Bob  <bob@test.com>  ')
        assert name == "Bob"
        assert email == "bob@test.com"


class TestParseDate:
    def test_rfc2822(self):
        from email_parser import parse_date
        result = parse_date("Wed, 15 Jan 2026 10:30:00 +0900")
        assert result is not None
        assert result.year == 2026
        assert result.month == 1
        assert result.day == 15

    def test_iso_date(self):
        from email_parser import parse_date
        result = parse_date("2026-01-15")
        assert result is not None
        assert result.year == 2026

    def test_invalid_date(self):
        from email_parser import parse_date
        result = parse_date("not a date")
        assert result is None

    def test_empty_string(self):
        from email_parser import parse_date
        result = parse_date("")
        assert result is None


class TestNormalizeIdentifier:
    def test_lowercase(self):
        from email_parser import normalize_identifier
        assert normalize_identifier("John DOE") == "john doe"

    def test_strip_whitespace(self):
        from email_parser import normalize_identifier
        assert normalize_identifier("  hello  world  ") == "hello world"


class TestNormalizeBodyText:
    def test_removes_quotes(self):
        from email_parser import normalize_body_text
        result = normalize_body_text("> quoted line\nnormal line")
        assert "quoted" not in result
        assert "normal" in result

    def test_removes_markdown(self):
        from email_parser import normalize_body_text
        result = normalize_body_text("# Heading\n**bold** `code`")
        assert "#" not in result
        assert "*" not in result
        assert "`" not in result


class TestIsLowContentEmail:
    def test_low_content(self):
        from email_parser import is_low_content_email, Email
        email = Email(
            id="1", subject="", sender="", sender_email="",
            date=datetime.now(), body="", file_path=""
        )
        assert is_low_content_email(email) is True

    def test_normal_content(self):
        from email_parser import is_low_content_email, Email
        email = Email(
            id="1", subject="Important Meeting", sender="Boss",
            sender_email="boss@co.jp", date=datetime.now(),
            body="Please join the meeting at 3pm.", file_path=""
        )
        assert is_low_content_email(email) is False


class TestIsLikelyMarketingEmail:
    def test_noreply_sender(self):
        from email_parser import is_likely_marketing_email, Email
        email = Email(
            id="1", subject="News", sender="Company",
            sender_email="noreply@company.com", date=datetime.now(),
            body="Check out our new features", file_path=""
        )
        assert is_likely_marketing_email(email) is True

    def test_newsletter_keywords(self):
        from email_parser import is_likely_marketing_email, Email
        email = Email(
            id="1", subject="Weekly Newsletter", sender="Company",
            sender_email="team@company.com", date=datetime.now(),
            body="Unsubscribe from this newsletter", file_path=""
        )
        assert is_likely_marketing_email(email) is True

    def test_human_email(self):
        from email_parser import is_likely_marketing_email, Email
        email = Email(
            id="1", subject="Meeting tomorrow", sender="Bob",
            sender_email="bob@company.com", date=datetime.now(),
            body="Hi, can we meet tomorrow?", file_path=""
        )
        assert is_likely_marketing_email(email) is False

    def test_very_long_email(self):
        from email_parser import is_likely_marketing_email, Email
        email = Email(
            id="1", subject="Promo", sender="Company",
            sender_email="sales@company.com", date=datetime.now(),
            body="a" * 3500, file_path=""
        )
        assert is_likely_marketing_email(email) is True


class TestFilterHumanEmails:
    def test_filters_marketing(self):
        from email_parser import filter_human_emails, Email
        emails = [
            Email(id="1", subject="Meeting", sender="Bob",
                  sender_email="bob@company.com", date=datetime.now(),
                  body="Hi", file_path=""),
            Email(id="2", subject="Sale!", sender="Shop",
                  sender_email="noreply@shop.com", date=datetime.now(),
                  body="Big sale unsubscribe", file_path=""),
        ]
        filtered = filter_human_emails(emails)
        assert len(filtered) == 1
        assert filtered[0].id == "1"

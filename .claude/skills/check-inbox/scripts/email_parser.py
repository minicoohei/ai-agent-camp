#!/usr/bin/env python3
"""
メールパーサーモジュール

/output/gmail/ 配下のMarkdownファイルからメールを抽出
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from email.utils import parsedate_to_datetime


@dataclass
class Email:
    """メールデータ"""
    id: str
    subject: str
    sender: str
    sender_email: str
    date: datetime
    body: str
    file_path: str


def parse_sender(from_field: str) -> tuple[str, str]:
    """
    送信者フィールドをパース

    Args:
        from_field: "Name <email@example.com>" 形式の文字列

    Returns:
        (送信者名, メールアドレス) のタプル
    """
    # "Name" <email@example.com> または Name <email@example.com>
    match = re.match(r'^"?([^"<]+)"?\s*<([^>]+)>$', from_field.strip())
    if match:
        return match.group(1).strip(), match.group(2).strip()

    # email@example.com のみ
    if "@" in from_field and "<" not in from_field:
        return from_field.strip(), from_field.strip()

    return from_field.strip(), ""


def parse_date(date_str: str) -> Optional[datetime]:
    """
    日付文字列をパース

    Args:
        date_str: RFC 2822形式等の日付文字列

    Returns:
        datetimeオブジェクト、パース失敗時はNone
    """
    try:
        return parsedate_to_datetime(date_str)
    except (ValueError, TypeError):
        pass

    # 手動でパース試行
    patterns = [
        r"(\w{3}, \d{1,2} \w{3} \d{4} \d{2}:\d{2}:\d{2})",
        r"(\d{4}-\d{2}-\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, date_str)
        if match:
            try:
                return datetime.strptime(match.group(1), "%a, %d %b %Y %H:%M:%S")
            except ValueError:
                try:
                    return datetime.strptime(match.group(1), "%Y-%m-%d")
                except ValueError:
                    pass

    return None


def parse_email_file(file_path: Path) -> list[Email]:
    """
    メールファイルをパース

    Args:
        file_path: Markdownファイルのパス

    Returns:
        Emailオブジェクトのリスト
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    emails = []

    # --- で区切られたブロックを抽出
    # パターン: ---\nid: ...\nsubject: ...\nfrom: ...\ndate: ...\n---\n本文
    blocks = re.split(r"^---$", content, flags=re.MULTILINE)

    i = 0
    while i < len(blocks):
        block = blocks[i].strip()

        # フロントマター（YAMLメタデータ）をチェック
        if block.startswith("id:"):
            metadata = {}
            for line in block.split("\n"):
                if ":" in line:
                    key, _, value = line.partition(":")
                    metadata[key.strip()] = value.strip()

            # 次のブロックが本文
            body = ""
            if i + 1 < len(blocks):
                body = blocks[i + 1].strip()
                # 次のフロントマターまでを本文とする
                # ただし次のフロントマターの直前の --- は除外済み

            if "id" in metadata and "subject" in metadata:
                sender_name, sender_email = parse_sender(metadata.get("from", ""))
                date = parse_date(metadata.get("date", ""))

                # date が None の場合はスキップ（Email.date は datetime を期待）
                if date is None:
                    continue

                emails.append(Email(
                    id=metadata["id"],
                    subject=metadata["subject"],
                    sender=sender_name,
                    sender_email=sender_email,
                    date=date,
                    body=body,
                    file_path=str(file_path)
                ))

        i += 1

    return emails


def get_email_files(
    base_dir: Path,
    start_date: datetime,
    end_date: datetime
) -> list[Path]:
    """
    指定期間のメールファイルを取得

    Args:
        base_dir: /output/gmail/ ディレクトリ
        start_date: 開始日
        end_date: 終了日

    Returns:
        ファイルパスのリスト
    """
    files = []

    def add_date_dir_files(date_dir: Path):
        """日付ディレクトリ内のファイルを追加"""
        match = re.match(r"(\d{4}-\d{2}-\d{2})$", date_dir.name)
        if match:
            file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
            if start_date.date() <= file_date.date() <= end_date.date():
                for md_file in date_dir.glob("*.md"):
                    # index.md は除外
                    if md_file.name != "index.md":
                        files.append(md_file)

    # パターン1: base_dir 直下の日付ディレクトリ
    # 例: output/gmail/2026-01-27/*.md
    for dir_path in base_dir.iterdir():
        if dir_path.is_dir():
            if re.match(r"^\d{4}-\d{2}-\d{2}$", dir_path.name):
                add_date_dir_files(dir_path)

    # パターン2: アカウント別サブディレクトリ内の日付ディレクトリ
    # 例: output/gmail/my-account/2026-01-27/*.md
    for account_dir in base_dir.iterdir():
        if account_dir.is_dir() and not re.match(r"^\d{4}-\d{2}-\d{2}$", account_dir.name):
            for date_dir in account_dir.iterdir():
                if date_dir.is_dir():
                    add_date_dir_files(date_dir)

    # パターン3: YYYY-MM-DD_emails.md パターン（古い形式）
    for md_file in base_dir.glob("*_emails.md"):
        match = re.match(r"(\d{4}-\d{2}-\d{2})_emails\.md", md_file.name)
        if match:
            file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
            if start_date.date() <= file_date.date() <= end_date.date():
                files.append(md_file)

    return sorted(set(files))  # 重複除去してソート


def find_email_data_dir() -> Optional[Path]:
    """
    メールデータディレクトリを探す

    Returns:
        見つかったディレクトリのパス、見つからない場合は None
    """
    candidates = [
        Path.cwd() / "output" / "gmail",
        Path.home() / "output" / "gmail",
        Path(__file__).parent.parent.parent.parent.parent / "output" / "gmail",
        Path.home() / "githubactions_fordata" / "output" / "gmail",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate

    return None


def load_emails(
    gmail_dir: Path,
    start_date: datetime,
    end_date: datetime
) -> list[Email]:
    """
    指定期間のメールを読み込み

    Args:
        gmail_dir: /output/gmail/ ディレクトリ（Noneの場合は自動検出）
        start_date: 開始日
        end_date: 終了日

    Returns:
        Emailオブジェクトのリスト
    """
    if gmail_dir is None:
        gmail_dir = find_email_data_dir()
        if gmail_dir is None:
            raise FileNotFoundError(
                "メールデータディレクトリが見つかりません。\n"
                "以下のいずれかにデータを配置してください:\n"
                "  - ./output/gmail/\n"
                "  - ~/output/gmail/"
            )

    all_emails = []

    files = get_email_files(gmail_dir, start_date, end_date)

    for file_path in files:
        try:
            emails = parse_email_file(file_path)
            all_emails.extend(emails)
        except Exception as e:
            print(f"  ⚠️ ファイル読み込みエラー: {file_path}: {e}")

    return all_emails


# マーケティング・自動メール判定用のパターン
MARKETING_DOMAINS = [
    "mail.capcut.com",
    "no_reply@",
    "noreply@",
    "no-reply@",
    "notification@",
    "notifications@",
    "newsletter@",
    "marketing@",
    "promo@",
    "info@",
    "hello@",
    "team@",
    "support@",
    "updates@",
    "news@",
    "events@",
    "learn.",
    "mail.",
    "email.",
    "list-manage.com",
    "customer.io",
    "sendgrid.net",
    "mailchimp.com",
    "hubspot.com",
    "intercom.io",
    "mailgun.org",
    "amazonses.com",
]

MARKETING_KEYWORDS = [
    "unsubscribe",
    "配信停止",
    "メール配信",
    "ニュースレター",
    "newsletter",
    "black friday",
    "セール",
    "sale",
    "discount",
    "割引",
    "キャンペーン",
    "campaign",
    "promo",
    "offer",
    "save up to",
    "free trial",
    "limited time",
    "don't miss",
    "act now",
    "view this email in your browser",
]


# デフォルトの自分の名前リスト
# 自分の名前に書き換えてください
# 例: ["Taro Yamada", "taro.yamada", "taro"]
DEFAULT_SELF_NAMES = os.environ.get(
    "CHECK_INBOX_SELF_NAMES", ""
).split(",") if os.environ.get("CHECK_INBOX_SELF_NAMES") else []


def normalize_identifier(value: str) -> str:
    return " ".join(value.strip().lower().split())


def get_self_filters() -> tuple[set[str], set[str]]:
    emails = set()
    names = set()

    raw_emails = os.getenv("INBOX_SELF_EMAILS", "")
    raw_names = os.getenv("INBOX_SELF_NAMES", "")

    if raw_emails:
        emails.update(
            normalize_identifier(v)
            for v in raw_emails.split(",")
            if v.strip()
        )

    if raw_names:
        names.update(
            normalize_identifier(v)
            for v in raw_names.split(",")
            if v.strip()
        )

    if not names:
        names.update(normalize_identifier(v) for v in DEFAULT_SELF_NAMES)

    return emails, names


def is_self_email(email: Email) -> bool:
    self_emails, self_names = get_self_filters()
    sender_email = normalize_identifier(email.sender_email)
    sender_name = normalize_identifier(email.sender)

    if sender_email and sender_email in self_emails:
        return True
    if sender_name and sender_name in self_names:
        return True

    return False


def normalize_body_text(body: str) -> str:
    lines = []
    for line in body.splitlines():
        if line.strip().startswith(">"):
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"[#*`>\-]", "", cleaned)
    return " ".join(cleaned.split()).strip()


def is_low_content_email(email: Email) -> bool:
    subject = normalize_body_text(email.subject)
    body = normalize_body_text(email.body)
    return len(subject) <= 2 and len(body) <= 4


def is_likely_marketing_email(email: Email) -> bool:
    """
    マーケティング/自動メールかどうかを判定

    Args:
        email: Emailオブジェクト

    Returns:
        マーケティングメールの可能性が高い場合True
    """
    email_lower = email.sender_email.lower()
    body_lower = email.body.lower()
    subject_lower = email.subject.lower()

    # ドメイン/メールアドレスパターンチェック
    for pattern in MARKETING_DOMAINS:
        if pattern in email_lower:
            return True

    # キーワードチェック（本文）
    keyword_count = 0
    for keyword in MARKETING_KEYWORDS:
        if keyword in body_lower or keyword in subject_lower:
            keyword_count += 1
            if keyword_count >= 2:
                return True

    # 長いメールはマーケティングの可能性が高い
    if len(email.body) > 3000:
        return True

    return False


def filter_human_emails(emails: list[Email]) -> list[Email]:
    """
    人からのメールのみをフィルタリング

    Args:
        emails: Emailオブジェクトのリスト

    Returns:
        人からのメールのみのリスト
    """
    return [
        e for e in emails
        if (
            not is_likely_marketing_email(e)
            and not is_self_email(e)
            and not is_low_content_email(e)
        )
    ]


if __name__ == "__main__":
    # テスト用
    import sys

    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        emails = parse_email_file(file_path)
        print(f"📧 {len(emails)} 件のメールを検出")
        for email in emails[:5]:
            print(f"  - [{email.subject[:50]}...] from: {email.sender}")
    else:
        print("Usage: python email_parser.py <email_file.md>")

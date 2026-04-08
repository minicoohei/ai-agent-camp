"""Shared logging utility with sensitive data filtering."""

import logging
import os
import re


class SensitiveDataFilter(logging.Filter):
    """Masks API keys, tokens, and credentials in log messages."""

    _PATTERNS = re.compile(
        r"AIza[0-9A-Za-z\-_]{35,}"          # Google API key
        r"|sk-[a-zA-Z0-9_\-]{20,}"          # OpenAI (sk-*, sk-proj-*, sk-admin-*)
        r"|ghp_[a-zA-Z0-9_]{36,}"           # GitHub PAT (classic)
        r"|github_pat_[a-zA-Z0-9_]{20,}"    # GitHub fine-grained PAT
        r"|gh[osur]_[a-zA-Z0-9_]{20,}"      # GitHub OAuth/user/server/refresh tokens
        r"|xox[abps]-[0-9A-Za-z\-]{10,}"    # Slack token families
        r"|://[^@\s/:]+(:[^@\s/:]+)?@"       # basic auth (user:pass@) or token-only (@) in URLs
        r"|(?<![a-zA-Z0-9/])[0-9a-fA-F]{32,}(?![a-zA-Z0-9/])"  # 32+ hex token
    )
    _REDACTED = "***REDACTED***"

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self._PATTERNS.sub(self._REDACTED, record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: (self._PATTERNS.sub(self._REDACTED, v) if isinstance(v, str) else v)
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    self._PATTERNS.sub(self._REDACTED, a) if isinstance(a, str) else a
                    for a in record.args
                )
        return True


def setup_logger(name: str) -> logging.Logger:
    """Return a configured logger that reads level from LOGLEVEL env var."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        level = os.environ.get("LOGLEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, level, logging.INFO))
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addFilter(SensitiveDataFilter())
        logger.addHandler(handler)
    return logger

# i18n共通ユーティリティ - extract/build/check/images 間で共有する定数・関数
"""
i18n共通ユーティリティ

i18nツール（extract, build, check, images）間で共有する定数・関数。
HTML教材 + MD (commands/skills) + CLI (gettext) の3系統をサポート。
"""
import gettext as _gettext_mod
import os
import sys
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).resolve().parents[1]

# --- HTML教材 (既存) ---
COURSE_DIR = ROOT_DIR / "course"
LOCALES_DIR = COURSE_DIR / "locales"
DIST_DIR = COURSE_DIR / "dist"

# --- MD (commands / skills) ---
COMMANDS_DIR = ROOT_DIR / ".cursor" / "commands"  # ソースオブトゥルース
CLAUDE_CMD_DIR = ROOT_DIR / ".claude" / "commands"
SKILLS_DIR = ROOT_DIR / "skills"
MD_LOCALES_DIR = ROOT_DIR / "locales" / "md"
CLI_LOCALES_DIR = ROOT_DIR / "locales" / "cli"
DIST_DIR_ROOT = ROOT_DIR / "dist"
ZIP_DIST_DIR = ROOT_DIR / "dist" / "zip"

EXCLUDE_DIRS = {"dist", "locales", "_templates"}
SKIP_SKILLS = {"_template"}

LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "ko": "Korean",
    "zh": "Chinese (Simplified)",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "it": "Italian",
    "vi": "Vietnamese",
    "th": "Thai",
    "ru": "Russian",
    "ar": "Arabic",
    "id": "Indonesian",
    "ms": "Malay",
}


def get_language_name(lang_code: str) -> str:
    """言語コードから表示名を取得"""
    return LANGUAGE_NAMES.get(lang_code, lang_code)


def is_excluded(path: Path) -> bool:
    """除外ディレクトリ配下かどうかを判定"""
    parts = path.relative_to(COURSE_DIR).parts
    return any(part in EXCLUDE_DIRS for part in parts)


def find_html_files() -> List[Path]:
    """course/ 配下のHTMLファイルを列挙（除外ディレクトリを除く）"""
    files = sorted(COURSE_DIR.rglob("*.html"))
    return [f for f in files if not is_excluded(f)]


def find_command_md_files() -> List[Path]:
    """commands/ 配下の全 .md ファイルを列挙（.cursor + .claude 両方）"""
    files: List[Path] = []
    for base in (COMMANDS_DIR, CLAUDE_CMD_DIR):
        if base.exists():
            files.extend(sorted(base.rglob("*.md")))
    return files


def find_skill_md_files() -> List[Path]:
    """skills/*/SKILL.md を列挙"""
    files: List[Path] = []
    if SKILLS_DIR.exists():
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if skill_dir.is_dir() and skill_dir.name not in SKIP_SKILLS:
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    files.append(skill_md)
    return files


def find_all_md_sources() -> dict:
    """commands と skills の MD ファイルをまとめて返す"""
    return {
        "commands": find_command_md_files(),
        "skills": find_skill_md_files(),
    }


def setup_gettext(domain: str = "aiagent") -> callable:
    """CLI ツール用 gettext セットアップ。AIAGENT_LANG 環境変数で言語切替。"""
    lang = os.environ.get("AIAGENT_LANG", "ja")
    localedir = CLI_LOCALES_DIR if CLI_LOCALES_DIR.exists() else None
    t = _gettext_mod.translation(
        domain, localedir=str(localedir) if localedir else None,
        languages=[lang], fallback=True,
    )
    return t.gettext


def require_gemini_client():
    """Gemini APIクライアントを取得。未設定の場合はsys.exit(1)"""
    sys.path.insert(0, str(Path(__file__).parent))
    from bootcamp_utils import get_client
    client = get_client()
    if client is None:
        print(
            "[ERROR] GEMINI_API_KEY または GOOGLE_API_KEY が"
            " 設定されていません。いずれかの環境変数を設定してください。",
            file=sys.stderr,
        )
        sys.exit(1)
    return client

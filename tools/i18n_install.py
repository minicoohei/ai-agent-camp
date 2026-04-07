"""
i18n Install Tool

dist/{lang}/ からワーキングツリーに翻訳ファイルをコピーする。
git clone ユーザー向けのヘルパー。

使い方:
  uv run python tools/i18n_install.py --lang en
  uv run python tools/i18n_install.py --lang en --backup --verbose
  uv run python tools/i18n_install.py --lang en --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Dict

_LANG_RE = re.compile(r"^[A-Za-z]{2,3}(?:[_-][A-Za-z0-9]+)?$")

_tools_dir = str(Path(__file__).resolve().parent)
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

try:
    from i18n_common import ROOT_DIR, DIST_DIR_ROOT, get_language_name
except ImportError:
    from tools.i18n_common import ROOT_DIR, DIST_DIR_ROOT, get_language_name


def install_lang(
    lang: str,
    backup: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
) -> Dict:
    """dist/{lang}/ からワーキングツリーにコピー。

    Returns:
        {"copied": int, "backed_up": int, "skipped": int}
    """
    if not _LANG_RE.match(lang):
        print(f"[ERROR] 不正な言語コード: {lang}", file=sys.stderr)
        return {"copied": 0, "backed_up": 0, "skipped": 0}

    lang_dist = DIST_DIR_ROOT / lang
    lang_name = get_language_name(lang)

    if not lang_dist.exists():
        print(f"[ERROR] dist/{lang}/ が見つかりません。先に i18n_build_md.py を実行してください。",
              file=sys.stderr)
        return {"copied": 0, "backed_up": 0, "skipped": 0}

    print(f"\n=== Installing {lang_name} ({lang}) ===")

    copied = 0
    backed_up = 0
    skipped = 0

    for src in sorted(lang_dist.rglob("*")):
        if not src.is_file():
            continue

        rel = src.relative_to(lang_dist)
        dest = ROOT_DIR / rel

        if dry_run:
            status = "[BACKUP+COPY]" if backup and dest.exists() else "[COPY]"
            if verbose:
                print(f"  {status} {rel}")
            copied += 1
            if backup and dest.exists():
                backed_up += 1
            continue

        # バックアップ
        if backup and dest.exists():
            bak_path = dest.with_suffix(dest.suffix + ".bak")
            shutil.copy2(dest, bak_path)
            backed_up += 1
            if verbose:
                print(f"  [BACKUP] {rel} → {rel}.bak")

        # コピー
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied += 1
        if verbose:
            print(f"  [COPY] {rel}")

    # .aiagent-lang マーカー
    lang_marker = ROOT_DIR / ".aiagent-lang"
    if not dry_run:
        lang_marker.write_text(lang, encoding="utf-8")
    if verbose:
        print(f"  [MARKER] .aiagent-lang = {lang}")

    mode = "[DRY RUN] " if dry_run else ""
    print(f"\n{mode}--- {lang_name} ({lang}) Summary ---")
    print(f"  Copied: {copied} files")
    if backup:
        print(f"  Backed up: {backed_up} files")

    return {"copied": copied, "backed_up": backed_up, "skipped": skipped}


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Install translated files from dist/{lang}/ to working tree"
    )
    parser.add_argument("--lang", required=True,
                        help="Target language (e.g. en)")
    parser.add_argument("--backup", action="store_true",
                        help="Create .bak files before overwriting")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be copied without making changes")
    parser.add_argument("--verbose", action="store_true",
                        help="Show per-file details")
    args = parser.parse_args()

    install_lang(
        args.lang,
        backup=args.backup,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()

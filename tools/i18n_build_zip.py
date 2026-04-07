"""
i18n Build Zip Tool

翻訳済みファイルを zip にパッケージングして配布する。
- dist/{lang}/ の翻訳済み MD ファイル
- locales/cli/{lang}/LC_MESSAGES/aiagent.mo (gettext)
- .aiagent-lang マーカーファイル

使い方:
  uv run python tools/i18n_build_zip.py --lang en es
  uv run python tools/i18n_build_zip.py --lang en --dry-run --verbose
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple

_LANG_RE = re.compile(r"^[A-Za-z]{2,3}(?:[_-][A-Za-z0-9]+)?$")

_tools_dir = str(Path(__file__).resolve().parent)
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

try:
    from i18n_common import ROOT_DIR, DIST_DIR_ROOT, ZIP_DIST_DIR, CLI_LOCALES_DIR, get_language_name
except ImportError:
    from tools.i18n_common import ROOT_DIR, DIST_DIR_ROOT, ZIP_DIST_DIR, CLI_LOCALES_DIR, get_language_name


def _collect_dist_files(lang: str) -> List[Tuple[Path, str]]:
    """dist/{lang}/ 配下のファイルを収集。(実パス, zip内パス) のリスト。"""
    lang_dist = DIST_DIR_ROOT / lang
    if not lang_dist.exists():
        return []

    files = []
    for f in sorted(lang_dist.rglob("*")):
        if f.is_file():
            # dist/{lang}/ プレフィックスを除去
            arcname = str(f.relative_to(lang_dist))
            files.append((f, arcname))
    return files


def _collect_mo_file(lang: str) -> List[Tuple[Path, str]]:
    """locales/cli/{lang}/LC_MESSAGES/aiagent.mo を収集。"""
    mo_path = CLI_LOCALES_DIR / lang / "LC_MESSAGES" / "aiagent.mo"
    if mo_path.exists():
        arcname = f"locales/cli/{lang}/LC_MESSAGES/aiagent.mo"
        return [(mo_path, arcname)]
    return []


def build_zip(
    lang: str,
    dry_run: bool = False,
    verbose: bool = False,
) -> Dict:
    """1言語分の zip を作成。

    Returns:
        {"files": int, "size_bytes": int, "path": str}
    """
    if not _LANG_RE.match(lang):
        print(f"[ERROR] 不正な言語コード: {lang}", file=sys.stderr)
        return {"files": 0, "size_bytes": 0, "path": ""}

    lang_name = get_language_name(lang)
    lang_dist = DIST_DIR_ROOT / lang

    if not lang_dist.exists():
        print(f"[SKIP] dist/{lang}/ が見つかりません。先に i18n_build_md.py を実行してください。",
              file=sys.stderr)
        return {"files": 0, "size_bytes": 0, "path": ""}

    print(f"\n=== Building zip for {lang_name} ({lang}) ===")

    # ファイル収集
    dist_files = _collect_dist_files(lang)
    mo_files = _collect_mo_file(lang)
    all_files = dist_files + mo_files

    # .aiagent-lang は writestr で追加するので +1
    total_count = len(all_files) + 1

    if verbose or dry_run:
        print(f"  .aiagent-lang (marker)")
        for _, arcname in all_files:
            print(f"  {arcname}")
        print(f"  Total: {total_count} files")

    if dry_run:
        return {"files": total_count, "size_bytes": 0, "path": ""}

    # zip 作成
    ZIP_DIST_DIR.mkdir(parents=True, exist_ok=True)
    zip_name = f"aiagent-base-{lang}.zip"
    zip_path = ZIP_DIST_DIR / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # .aiagent-lang マーカー
        zf.writestr(".aiagent-lang", lang)

        # 翻訳ファイル
        for file_path, arcname in all_files:
            zf.write(file_path, arcname)

    size = zip_path.stat().st_size
    print(f"  Created: {zip_path} ({total_count} files, {size:,} bytes)")

    return {"files": total_count, "size_bytes": size, "path": str(zip_path)}


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Build distributable zip files from translated content"
    )
    parser.add_argument("--lang", nargs="+", required=True,
                        help="Target languages (e.g. en es)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be included without creating zip")
    parser.add_argument("--verbose", action="store_true",
                        help="Show per-file details")
    args = parser.parse_args()

    for lang in args.lang:
        result = build_zip(lang, dry_run=args.dry_run, verbose=args.verbose)
        if args.dry_run and result["files"] > 0:
            print(f"\n[DRY RUN] {lang}: {result['files']} files would be included")


if __name__ == "__main__":
    main()

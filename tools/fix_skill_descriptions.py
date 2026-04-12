#!/usr/bin/env python3
"""SKILL.md の description: | (YAML block scalar) を単行 description: "..." に変換する。

tools/skill_manager.py のパーサーが行ごとに : で分割するため、
multiline block scalar が正しくパースされない問題を修正する。
"""

import glob
import re
import sys


def fix_skill_md(path: str) -> bool:
    """SKILL.md を読み込み、description: | を単行に変換する。

    Returns:
        True if file was modified, False otherwise.
    """
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # frontmatter を抽出
    m = re.match(r"^(---\n)(.*?\n)(---)", content, re.DOTALL)
    if not m:
        return False

    prefix = m.group(1)   # "---\n"
    fm_body = m.group(2)  # frontmatter 本体
    suffix = m.group(3)   # "---"
    rest = content[m.end():]  # frontmatter 以降の本文

    # description: | パターンを検出
    # description: | の後、2スペースインデントの行が続く
    pattern = re.compile(
        r"^(description:\s*)\|\s*\n((?:[ \t]+[^\n]*\n)+)",
        re.MULTILINE,
    )
    match = pattern.search(fm_body)
    if not match:
        return False

    # インデントされた行を収集して結合
    indented_block = match.group(2)
    lines = []
    for line in indented_block.splitlines():
        stripped = line.strip()
        if stripped:
            lines.append(stripped)

    # 結合して1行にする
    single_line = " ".join(lines)

    # ダブルクォートをエスケープ
    single_line = single_line.replace("\\", "\\\\").replace('"', '\\"')

    # 置換
    replacement = f'description: "{single_line}"\n'
    new_fm_body = fm_body[: match.start()] + replacement + fm_body[match.end():]

    new_content = prefix + new_fm_body + suffix + rest

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    files = sorted(glob.glob("skills/*/SKILL.md"))
    fixed = 0
    skipped = 0
    errors = []

    for path in files:
        try:
            if fix_skill_md(path):
                fixed += 1
                print(f"  FIXED: {path}")
            else:
                skipped += 1
        except Exception as e:
            errors.append((path, str(e)))
            print(f"  ERROR: {path}: {e}", file=sys.stderr)

    print(f"\n=== 結果 ===")
    print(f"  対象ファイル: {len(files)}")
    print(f"  修正済み:     {fixed}")
    print(f"  スキップ:     {skipped}")
    if errors:
        print(f"  エラー:       {len(errors)}")
        for p, e in errors:
            print(f"    {p}: {e}")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

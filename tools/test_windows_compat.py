#!/usr/bin/env python3
"""Windows互換性テストスクリプト

全Python/bashスクリプトを静的解析し、Windows非互換な箇所を検出する。
GitHub Actions (windows-latest) でも実行可能。

Usage:
    uv run python tools/test_windows_compat.py [--report output/test-results/windows-compatibility-report.md]
"""

import argparse
import ast
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 検出パターン定義
MACOS_COMMANDS = ["open ", "pbcopy", "pbpaste", "brew ", "diskutil", "osascript"]
POSIX_COMMANDS = ["mktemp", "sed ", "awk ", "wc -l", "chmod ", "chown "]
HARDCODED_UNIX_PATHS = [r'"/tmp/', r"'/tmp/", r'Path\("/tmp', r'Path\(\'/tmp']
BASH_SHEBANGS = ["#!/usr/bin/env bash", "#!/bin/bash", "#!/usr/bin/env sh", "#!/bin/sh"]


def check_python_imports(py_files: list[Path]) -> list[dict]:
    """Python ファイルの import が構文的に正しいかチェック"""
    issues = []
    for f in py_files:
        try:
            source = f.read_text(encoding="utf-8")
            ast.parse(source)
        except SyntaxError as e:
            issues.append({
                "file": str(f.relative_to(BASE_DIR)),
                "line": e.lineno or 0,
                "type": "syntax_error",
                "severity": "high",
                "detail": f"SyntaxError: {e.msg}",
            })
        except UnicodeDecodeError:
            issues.append({
                "file": str(f.relative_to(BASE_DIR)),
                "line": 0,
                "type": "encoding",
                "severity": "high",
                "detail": "Non-UTF-8 encoding detected",
            })
    return issues


def check_hardcoded_paths(files: list[Path]) -> list[dict]:
    """ハードコードされた Unix パスを検出"""
    self_path = Path(__file__).resolve()
    issues = []
    for f in files:
        # 自分自身は検査対象外（パターン定義が誤検知される）
        if f.resolve() == self_path:
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            # /tmp/ ハードコード
            for pattern in HARDCODED_UNIX_PATHS:
                if re.search(pattern, line):
                    issues.append({
                        "file": str(f.relative_to(BASE_DIR)),
                        "line": i,
                        "type": "hardcoded_tmp",
                        "severity": "high",
                        "detail": f"Hardcoded /tmp/ path: {line.strip()[:100]}",
                    })
            # /Users/ ハードコード（コメント・ドキュメント除外）
            stripped = line.strip()
            if "/Users/" in line and not stripped.startswith("#") and not stripped.startswith("//"):
                if f.suffix == ".py":
                    issues.append({
                        "file": str(f.relative_to(BASE_DIR)),
                        "line": i,
                        "type": "hardcoded_users",
                        "severity": "medium",
                        "detail": f"Hardcoded /Users/ path: {stripped[:100]}",
                    })
    return issues


def check_macos_commands(files: list[Path]) -> list[dict]:
    """macOS 固有コマンドの使用を検出"""
    issues = []
    for f in files:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for cmd in MACOS_COMMANDS:
                if cmd in line:
                    # subprocess.run(["open", ...]) や os.system("open ...") のパターン
                    if f.suffix == ".py" and cmd == "open ":
                        if "subprocess" in line or "os.system" in line or "os.popen" in line:
                            issues.append({
                                "file": str(f.relative_to(BASE_DIR)),
                                "line": i,
                                "type": "macos_command",
                                "severity": "high",
                                "detail": f"macOS 'open' command in code: {stripped[:100]}",
                            })
                    elif f.suffix in (".sh", ".bash"):
                        issues.append({
                            "file": str(f.relative_to(BASE_DIR)),
                            "line": i,
                            "type": "macos_command",
                            "severity": "high",
                            "detail": f"macOS command '{cmd.strip()}': {stripped[:100]}",
                        })
                    elif f.suffix == ".json" and cmd == "open ":
                        # process.platform 分岐でクロスプラットフォーム対応済みなら除外
                        if "process.platform" not in line:
                            issues.append({
                                "file": str(f.relative_to(BASE_DIR)),
                                "line": i,
                                "type": "macos_command",
                                "severity": "high",
                                "detail": f"macOS 'open' in config: {stripped[:100]}",
                            })
    return issues


def check_bash_scripts(sh_files: list[Path]) -> list[dict]:
    """bash スクリプトの Windows 非互換性を検出"""
    issues = []
    for f in sh_files:
        issues.append({
            "file": str(f.relative_to(BASE_DIR)),
            "line": 1,
            "type": "bash_script",
            "severity": "high",
            "detail": f"Bash script not executable on native Windows: {f.name}",
        })
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for i, line in enumerate(content.splitlines(), 1):
            for cmd in POSIX_COMMANDS:
                if cmd in line and not line.strip().startswith("#"):
                    issues.append({
                        "file": str(f.relative_to(BASE_DIR)),
                        "line": i,
                        "type": "posix_command",
                        "severity": "medium",
                        "detail": f"POSIX command '{cmd.strip()}': {line.strip()[:100]}",
                    })
    return issues


def check_symlinks(base: Path) -> list[dict]:
    """symlink の残存を検出"""
    issues = []
    skills_dir = base / ".claude" / "skills"
    if not skills_dir.exists():
        return issues
    for item in skills_dir.iterdir():
        if item.is_symlink():
            target = os.readlink(item)
            issues.append({
                "file": str(item.relative_to(base)),
                "line": 0,
                "type": "symlink",
                "severity": "high",
                "detail": f"Symlink to {target} — Windows may not resolve",
            })
    return issues


def check_package_json(base: Path) -> list[dict]:
    """package.json の OS 固有コマンドを検出"""
    issues = []
    pkg = base / "package.json"
    if not pkg.exists():
        return issues
    lines = pkg.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines, 1):
        if '"open ' in line or "'open " in line:
            # process.platform 分岐でクロスプラットフォーム対応済みなら除外
            if "process.platform" in line:
                continue
            issues.append({
                "file": "package.json",
                "line": i,
                "type": "macos_command",
                "severity": "high",
                "detail": f"macOS 'open' in package.json scripts: {line.strip()[:100]}",
            })
    return issues


def generate_report(issues: list[dict], output_path: Path) -> str:
    """Markdown レポート生成"""
    high = [i for i in issues if i["severity"] == "high"]
    medium = [i for i in issues if i["severity"] == "medium"]
    low = [i for i in issues if i["severity"] == "low"]

    lines = [
        "# Windows 互換性レポート",
        "",
        f"生成日時: {__import__('datetime').datetime.now().isoformat()[:19]}",
        "",
        "## サマリー",
        "",
        f"| 優先度 | 件数 |",
        f"|--------|------|",
        f"| 高 | {len(high)} |",
        f"| 中 | {len(medium)} |",
        f"| 低 | {len(low)} |",
        f"| **合計** | **{len(issues)}** |",
        "",
    ]

    # カテゴリ別集計
    categories: dict[str, list[dict]] = {}
    for issue in issues:
        cat = issue["type"]
        categories.setdefault(cat, []).append(issue)

    lines.append("## カテゴリ別集計")
    lines.append("")
    lines.append("| カテゴリ | 件数 | 説明 |")
    lines.append("|---------|------|------|")
    category_desc = {
        "bash_script": "bashスクリプト（Windows非実行）",
        "posix_command": "POSIXコマンド使用",
        "macos_command": "macOS固有コマンド",
        "hardcoded_tmp": "/tmp/ ハードコード",
        "hardcoded_users": "/Users/ ハードコード",
        "symlink": "symlink残存",
        "syntax_error": "Python構文エラー",
        "encoding": "非UTF-8エンコーディング",
    }
    for cat, items in sorted(categories.items()):
        desc = category_desc.get(cat, cat)
        lines.append(f"| {cat} | {len(items)} | {desc} |")
    lines.append("")

    # 高優先度の詳細
    if high:
        lines.append("## 高優先度の問題")
        lines.append("")
        lines.append("| ファイル | 行 | 種別 | 詳細 |")
        lines.append("|---------|-----|------|------|")
        for issue in high:
            lines.append(
                f"| `{issue['file']}` | {issue['line']} | {issue['type']} | {issue['detail'][:80]} |"
            )
        lines.append("")

    # 中優先度の詳細
    if medium:
        lines.append("## 中優先度の問題")
        lines.append("")
        lines.append("| ファイル | 行 | 種別 | 詳細 |")
        lines.append("|---------|-----|------|------|")
        for issue in medium[:50]:  # 上限50件
            lines.append(
                f"| `{issue['file']}` | {issue['line']} | {issue['type']} | {issue['detail'][:80]} |"
            )
        if len(medium) > 50:
            lines.append(f"| ... | ... | ... | 他 {len(medium) - 50} 件 |")
        lines.append("")

    # 推奨対応
    lines.extend([
        "## 推奨対応",
        "",
        "### WSL2 前提の場合",
        "- すべてのbashスクリプトはWSL2環境で実行可能",
        "- `/tmp/` パスもWSL2内で有効",
        "- 追加対応不要",
        "",
        "### ネイティブWindows対応が必要な場合",
        "1. `/tmp/` → `tempfile.gettempdir()` に変更",
        "2. `open` → `start` (Windows) / `xdg-open` (Linux) の分岐",
        "3. bashスクリプト → PowerShell版作成 or Python化",
        "4. symlink → 実体コピー（#277 で対応済み）",
        "",
    ])

    report = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description="Windows互換性チェック")
    parser.add_argument(
        "--report",
        default="output/test-results/windows-compatibility-report.md",
        help="レポート出力先",
    )
    args = parser.parse_args()

    all_issues: list[dict] = []

    # venv/node_modules 除外フィルタ
    def exclude_vendored(files: list[Path]) -> list[Path]:
        excludes = {"venv", ".venv", "node_modules", "__pycache__", ".git", "site-packages"}
        return [f for f in files if not any(ex in f.parts for ex in excludes)]

    # Python ファイル収集（venv除外）
    py_files = exclude_vendored(list((BASE_DIR / "tools").glob("**/*.py")))
    py_files += exclude_vendored(list((BASE_DIR / "skills").glob("**/*.py")))
    py_files += exclude_vendored(list((BASE_DIR / ".claude" / "skills").glob("**/*.py")))
    py_files += list((BASE_DIR / ".claude" / "hooks").glob("*.py"))

    # bash ファイル収集
    sh_files = list((BASE_DIR / "tools").glob("**/*.sh"))
    sh_files += list((BASE_DIR / "scripts").glob("**/*.sh")) if (BASE_DIR / "scripts").exists() else []
    sh_files += list((BASE_DIR / ".claude" / "hooks").glob("*.sh"))
    sh_files += list((BASE_DIR / ".claude" / "scripts").glob("*.sh"))
    sh_files += exclude_vendored(list((BASE_DIR / "skills").glob("**/*.sh")))

    # 全テキストファイル（パスチェック用）
    check_files = py_files + list((BASE_DIR / "tools").glob("**/*.json"))

    print(f"Checking {len(py_files)} Python files, {len(sh_files)} bash files...")

    # 各チェック実行
    all_issues += check_python_imports(py_files)
    all_issues += check_hardcoded_paths(py_files)
    all_issues += check_macos_commands(py_files + sh_files)
    all_issues += check_bash_scripts(sh_files)
    all_issues += check_symlinks(BASE_DIR)
    all_issues += check_package_json(BASE_DIR)

    # レポート生成
    report_path = BASE_DIR / args.report
    report = generate_report(all_issues, report_path)

    # サマリー出力
    high = sum(1 for i in all_issues if i["severity"] == "high")
    medium = sum(1 for i in all_issues if i["severity"] == "medium")
    print(f"\nResults: {len(all_issues)} issues found (high={high}, medium={medium})")
    print(f"Report saved to: {report_path}")

    # 高優先度があれば exit code 1
    sys.exit(1 if high > 0 else 0)


if __name__ == "__main__":
    main()

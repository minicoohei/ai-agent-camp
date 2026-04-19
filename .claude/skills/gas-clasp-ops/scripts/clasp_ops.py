#!/usr/bin/env python3
"""
GAS clasp 操作スクリプト
.clasp.json を持つプロジェクトを検出し、push/deploy/run を一括実行
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


def find_clasp_projects(base_dir: Path) -> list[Path]:
    """
    .clasp.json を持つプロジェクトディレクトリを検出
    """
    projects = []
    for clasp_file in base_dir.rglob(".clasp.json"):
        projects.append(clasp_file.parent)
    return sorted(projects)


def run_clasp_command(
    project_dir: Path,
    command: str,
    function_name: Optional[str] = None,
    dry_run: bool = False,
) -> tuple[bool, str]:
    """
    clasp コマンドを実行
    Returns: (success, output)
    """
    cmd = ["clasp", command]
    
    if command == "run" and function_name:
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", function_name):
            raise ValueError(f"Invalid function name: {function_name}")
        cmd.append(function_name)
    
    if dry_run:
        return True, f"[DRY-RUN] Would execute: {' '.join(cmd)} in {project_dir}"
    
    try:
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout + result.stderr
        success = result.returncode == 0
        return success, output.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out after 120 seconds"
    except Exception as e:
        return False, f"Error: {e}"


def get_project_info(project_dir: Path) -> dict:
    """
    .clasp.json から設定情報を取得
    """
    clasp_file = project_dir / ".clasp.json"
    if clasp_file.exists():
        with open(clasp_file, encoding="utf-8") as f:
            return json.load(f)
    return {}


def main():
    parser = argparse.ArgumentParser(
        description="GAS clasp 操作ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s push                           # 全プロジェクトを push
  %(prog)s push deploy                    # 全プロジェクトを push → deploy
  %(prog)s push --project work/10.X-Calendar-GAS  # 特定プロジェクトのみ
  %(prog)s run --project work/10.X-Calendar-GAS --function myFunction
  %(prog)s status --dry-run               # 実行せず確認
        """,
    )
    
    parser.add_argument(
        "commands",
        nargs="*",
        help="実行するコマンド: push, deploy, run, status, open（複数指定可、デフォルト: push）",
    )
    parser.add_argument(
        "--project", "-p",
        action="append",
        dest="projects",
        help="対象プロジェクトパス（複数指定可）",
    )
    parser.add_argument(
        "--function", "-f",
        help="実行する関数名（run コマンド時必須）",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="実行せず確認のみ",
    )
    parser.add_argument(
        "--base-dir", "-b",
        type=Path,
        default=Path.cwd(),
        help="検索ベースディレクトリ（デフォルト: カレントディレクトリ）",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="検出プロジェクト一覧を表示",
    )
    
    args = parser.parse_args()
    
    # デフォルトコマンド
    if not args.commands:
        args.commands = ["push"]
    
    # コマンドのバリデーション
    valid_commands = {"push", "deploy", "run", "status", "open"}
    invalid_commands = set(args.commands) - valid_commands
    if invalid_commands:
        parser.error(f"無効なコマンド: {', '.join(invalid_commands)} (有効: {', '.join(valid_commands)})")
    
    # run コマンドには --function が必須
    if "run" in args.commands and not args.function:
        parser.error("run コマンドには --function オプションが必須です")
    
    # プロジェクト検出
    all_projects = find_clasp_projects(args.base_dir)
    
    if not all_projects:
        print(f"❌ .clasp.json が見つかりません: {args.base_dir}")
        sys.exit(1)
    
    # --list オプション
    if args.list:
        print(f"📂 検出されたプロジェクト ({len(all_projects)} 件):")
        for p in all_projects:
            info = get_project_info(p)
            script_id = info.get("scriptId", "N/A")[:20] + "..."
            print(f"  - {p.relative_to(args.base_dir)} (scriptId: {script_id})")
        sys.exit(0)
    
    # 対象プロジェクト決定
    if args.projects:
        target_projects = []
        for proj_path in args.projects:
            proj = Path(proj_path)
            if not proj.is_absolute():
                proj = args.base_dir / proj
            if proj.exists() and (proj / ".clasp.json").exists():
                target_projects.append(proj)
            else:
                print(f"⚠️  スキップ: {proj_path} (.clasp.json なし)")
    else:
        target_projects = all_projects
    
    if not target_projects:
        print("❌ 対象プロジェクトがありません")
        sys.exit(1)
    
    # 実行
    print(f"🚀 対象: {len(target_projects)} プロジェクト")
    print(f"📋 コマンド: {', '.join(args.commands)}")
    if args.dry_run:
        print("🔍 DRY-RUN モード")
    print("-" * 50)
    
    results = []
    
    for project in target_projects:
        rel_path = project.relative_to(args.base_dir) if project.is_relative_to(args.base_dir) else project
        print(f"\n📁 {rel_path}")
        
        project_results = {"project": str(rel_path), "commands": []}
        
        for cmd in args.commands:
            success, output = run_clasp_command(
                project,
                cmd,
                function_name=args.function if cmd == "run" else None,
                dry_run=args.dry_run,
            )
            
            status = "✅" if success else "❌"
            print(f"  {status} {cmd}: {output[:100]}{'...' if len(output) > 100 else ''}")
            
            project_results["commands"].append({
                "command": cmd,
                "success": success,
                "output": output,
            })
            
            # 失敗したら次のコマンドはスキップ（同一プロジェクト内）
            if not success and not args.dry_run:
                print(f"  ⚠️  エラーのため残りのコマンドをスキップ")
                break
        
        results.append(project_results)
    
    # サマリー
    print("\n" + "=" * 50)
    print("📊 サマリー")
    
    success_count = sum(
        1 for r in results
        if all(c["success"] for c in r["commands"])
    )
    fail_count = len(results) - success_count
    
    print(f"  成功: {success_count} / 失敗: {fail_count}")
    
    if fail_count > 0:
        print("\n❌ 失敗したプロジェクト:")
        for r in results:
            failed_cmds = [c for c in r["commands"] if not c["success"]]
            if failed_cmds:
                print(f"  - {r['project']}")
                for c in failed_cmds:
                    print(f"      {c['command']}: {c['output'][:80]}")
    
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()

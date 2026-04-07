#!/usr/bin/env python3
"""
gslides_parser.py — Google Slides パーサー メインCLI

GAS (parseSlides.js) を clasp 経由で実行し、
プレゼンテーション構造をパースしてマッピング YAML を出力する。

サブコマンド:
  analyze:  プレゼンテーションをパース → YAML 出力
  json:     GAS パース結果の JSON だけ出力（YAML 変換なし）
  setup:    GAS プロジェクト初期設定（clasp create）

使用例:
  python gslides_parser.py analyze 1ZVAI8Cjts1N44lYXgoCoZXfb0gz7BAx7A1A5-bhapvQ -o mapping.yaml
  python gslides_parser.py json 1ZVAI8Cjts1N44lYXgoCoZXfb0gz7BAx7A1A5-bhapvQ
  python gslides_parser.py setup
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

# ─── パス設定 ─────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_GAS_DIR = _SCRIPT_DIR.parent / "gas"
_TOOLS_DIR = _SCRIPT_DIR.parent.parent.parent / "tools"
sys.path.insert(0, str(_SCRIPT_DIR))
sys.path.insert(0, str(_TOOLS_DIR))

from gas_to_yaml import convert_gas_to_mapping, save_yaml


# ─── clasp 実行ヘルパー ───────────────────────────────────────

def _run_clasp(args: list[str], cwd: Path, timeout: int = 180) -> tuple[bool, str]:
    """clasp コマンドを実行して結果を返す"""
    cmd = ["npx", "@google/clasp"] + args
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, f"タイムアウト ({timeout}秒)"
    except FileNotFoundError:
        return False, "npx が見つかりません。Node.js をインストールしてください。"


def _check_clasp_project() -> bool:
    """GAS プロジェクト設定 (.clasp.json) が存在するか確認"""
    return (_GAS_DIR / ".clasp.json").exists()


def _get_script_id() -> Optional[str]:
    """.clasp.json から scriptId を取得"""
    clasp_file = _GAS_DIR / ".clasp.json"
    if clasp_file.exists():
        with open(clasp_file, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("scriptId")
    return None


# ─── clasp run 出力パーサー ────────────────────────────────────

def _parse_clasp_run_output(raw_output: str) -> Optional[dict]:
    """
    clasp run の出力から JSON データを抽出する。

    clasp run の出力パターン:
      1) 直接 JSON が返る
      2) "Running in dev mode." + ログ行 + JSON
      3) "{ ... }" がどこかに含まれる
    """
    lines = raw_output.strip().split("\n")

    # パターン1: 最後の行から JSON を探す（逆順）
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line.startswith("{"):
            # この行から末尾まで結合して JSON パース試行
            json_candidate = "\n".join(l.strip() for l in lines[i:])
            try:
                return json.loads(json_candidate)
            except json.JSONDecodeError:
                pass

    # パターン2: 全体を JSON として試す
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        pass

    # パターン3: JSON ブロックを正規表現で探す
    match = re.search(r'\{[\s\S]*\}', raw_output)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return None


# ─── メインコマンド ────────────────────────────────────────────

def cmd_setup(args: argparse.Namespace) -> int:
    """GAS プロジェクト初期設定"""
    if _check_clasp_project():
        script_id = _get_script_id()
        print(f"[setup] GAS プロジェクトは設定済みです (scriptId: {script_id})")
        print(f"[setup] 再作成する場合は {_GAS_DIR / '.clasp.json'} を削除してください。")
        return 0

    print("[setup] GAS プロジェクトを作成します...")

    # clasp login チェック
    ok, out = _run_clasp(["login", "--status"], cwd=_GAS_DIR, timeout=10)
    if not ok or "Not logged in" in out:
        print("[setup] clasp にログインしてください:")
        print("  npx @google/clasp login")
        return 1

    # clasp create
    title = args.title or "gslides-parser"
    ok, out = _run_clasp(
        ["create", "--type", "standalone", "--title", title, "--rootDir", "."],
        cwd=_GAS_DIR,
    )
    if not ok:
        print(f"[setup] プロジェクト作成に失敗しました:\n{out}")
        return 1

    print(f"[setup] GAS プロジェクト作成完了: {title}")
    print(f"[setup] scriptId: {_get_script_id()}")

    # push
    ok, out = _run_clasp(["push", "--force"], cwd=_GAS_DIR)
    if ok:
        print("[setup] コード push 完了")
    else:
        print(f"[setup] push 失敗: {out}")

    print("\n[setup] 次のステップ:")
    print("  1. GAS エディタで実行権限を付与")
    print("     npx @google/clasp open --cwd " + str(_GAS_DIR))
    print("  2. Google Apps Script API を有効化")
    print("     https://script.google.com/home/usersettings")
    print("  3. analyze コマンドでパース実行:")
    print("     python gslides_parser.py analyze <PRESENTATION_ID>")

    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    """プレゼンテーションをパース → YAML 出力"""
    presentation_id = args.presentation_id

    # GAS プロジェクト確認
    if not _check_clasp_project():
        print("[error] GAS プロジェクトが未設定です。先に setup を実行してください:")
        print("  python gslides_parser.py setup")
        return 1

    # ステップ1: push（最新コードを反映）
    if not args.skip_push:
        print("[1/3] GAS コードを push 中...")
        ok, out = _run_clasp(["push", "--force"], cwd=_GAS_DIR)
        if not ok:
            print(f"[error] push 失敗:\n{out}")
            return 1
        print("[1/3] push 完了")

    # ステップ2: clasp run で parsePresentation を実行
    print(f"[2/3] parsePresentation 実行中 (ID: {presentation_id})...")
    params_json = json.dumps([presentation_id])
    ok, out = _run_clasp(
        ["run", "parsePresentation", "--params", params_json],
        cwd=_GAS_DIR,
        timeout=300,
    )

    if not ok:
        print(f"[error] GAS 実行失敗:\n{out}")
        _print_troubleshooting(out)
        return 1

    # ステップ3: JSON パース
    gas_data = _parse_clasp_run_output(out)
    if gas_data is None:
        print("[error] GAS 出力の JSON パースに失敗しました。")
        print("[debug] 生出力:")
        print(out[:2000])
        return 1

    slide_count = len(gas_data.get("slides", []))
    print(f"[2/3] パース完了: {slide_count} スライド")

    # ステップ4: YAML 変換
    print("[3/3] YAML 変換中...")
    mapping = convert_gas_to_mapping(gas_data, use_gemini=not args.no_gemini)

    # 出力
    output_path = args.output
    if not output_path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"output/slides/gslides_{presentation_id[:8]}_{ts}.yaml"

    save_yaml(mapping, output_path)
    print(f"[3/3] 完了: {output_path}")

    # サマリー
    ph_count = len(mapping.get("placeholders", []))
    print(f"\n[summary] スライド: {slide_count}, プレースホルダー: {ph_count}")
    print(f"[summary] URL: {mapping.get('presentation_url', '')}")

    return 0


def cmd_json(args: argparse.Namespace) -> int:
    """GAS パース結果の JSON だけ出力"""
    presentation_id = args.presentation_id

    if not _check_clasp_project():
        print("[error] GAS プロジェクトが未設定です。", file=sys.stderr)
        return 1

    # push
    if not args.skip_push:
        ok, out = _run_clasp(["push", "--force"], cwd=_GAS_DIR)
        if not ok:
            print(f"[error] push 失敗:\n{out}", file=sys.stderr)
            return 1

    # run
    params_json = json.dumps([presentation_id])
    ok, out = _run_clasp(
        ["run", "parsePresentation", "--params", params_json],
        cwd=_GAS_DIR,
        timeout=300,
    )

    if not ok:
        print(f"[error] GAS 実行失敗:\n{out}", file=sys.stderr)
        return 1

    gas_data = _parse_clasp_run_output(out)
    if gas_data is None:
        print("[error] JSON パース失敗", file=sys.stderr)
        return 1

    # 出力
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(gas_data, f, ensure_ascii=False, indent=2)
        print(f"[json] Saved: {out_path}", file=sys.stderr)
    else:
        print(json.dumps(gas_data, ensure_ascii=False, indent=2))

    return 0


# ─── トラブルシューティング ─────────────────────────────────────

def _print_troubleshooting(error_output: str):
    """エラー内容に応じたトラブルシューティングを表示"""
    if "Not logged in" in error_output:
        print("\n[hint] clasp にログインしてください:")
        print("  npx @google/clasp login")
    elif "Script API" in error_output or "scriptApi" in error_output:
        print("\n[hint] Google Apps Script API を有効化してください:")
        print("  https://script.google.com/home/usersettings")
    elif "PERMISSION_DENIED" in error_output or "permission" in error_output.lower():
        print("\n[hint] GAS エディタで一度手動実行して権限を付与してください:")
        print(f"  npx @google/clasp open --cwd {_GAS_DIR}")
    elif "Function not found" in error_output:
        print("\n[hint] push が完了しているか確認してください:")
        print(f"  npx @google/clasp push --force --cwd {_GAS_DIR}")
    elif "timed out" in error_output.lower():
        print("\n[hint] タイムアウトしました。大きなプレゼンの場合は GAS エディタから実行してください:")
        print(f"  npx @google/clasp open --cwd {_GAS_DIR}")


# ─── CLI ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Google Slides パーサー — GAS 経由でスライド構造をパース → YAML 変換",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s setup                                          # GAS プロジェクト初期設定
  %(prog)s analyze 1ZVAI8Cjts... -o mapping.yaml         # パース → YAML
  %(prog)s analyze 1ZVAI8Cjts... --no-gemini             # Gemini なしでパース
  %(prog)s json 1ZVAI8Cjts... -o raw.json                # JSON のみ出力
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # setup
    p_setup = subparsers.add_parser("setup", help="GAS プロジェクト初期設定")
    p_setup.add_argument("--title", default="gslides-parser", help="GAS プロジェクト名")

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="プレゼンテーションをパース → YAML")
    p_analyze.add_argument("presentation_id", help="Google Slides プレゼンテーション ID")
    p_analyze.add_argument("-o", "--output", help="出力 YAML パス")
    p_analyze.add_argument("--no-gemini", action="store_true", help="Gemini セマンティック解析を無効化")
    p_analyze.add_argument("--skip-push", action="store_true", help="clasp push をスキップ")

    # json
    p_json = subparsers.add_parser("json", help="GAS パース結果の JSON を出力")
    p_json.add_argument("presentation_id", help="Google Slides プレゼンテーション ID")
    p_json.add_argument("-o", "--output", help="出力 JSON パス")
    p_json.add_argument("--skip-push", action="store_true", help="clasp push をスキップ")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "setup": cmd_setup,
        "analyze": cmd_analyze,
        "json": cmd_json,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())

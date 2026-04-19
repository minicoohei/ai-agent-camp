#!/usr/bin/env python3
"""
gslides_creator.py — Google Slides クリエーター メインCLI

テンプレートから Google Slides を作成する。3つのサブコマンド:
  convert: テンプレートコピー → Gemini で新コンテンツ生成 → replaceAllText
  build:   テンプレートコピー → マッピング YAML + データで精密書き換え
  deck:    ゼロから or テンプレートベースでデッキ生成

使用例:
  python gslides_creator.py convert TEMPLATE_ID --topic "新トピック" --title "新タイトル"
  python gslides_creator.py build TEMPLATE_ID --data data.yaml --title "新タイトル"
  python gslides_creator.py deck --topic "AI活用提案" --slides 10 --style corporate
  python gslides_creator.py setup
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

import yaml

# ─── パス設定 ─────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_GAS_DIR = _SCRIPT_DIR.parent / "gas"
_PARSER_DIR = _SCRIPT_DIR.parent.parent / "gslides-parser" / "scripts"
_TOOLS_DIR = _SCRIPT_DIR.parent.parent.parent / "tools"
sys.path.insert(0, str(_SCRIPT_DIR))
sys.path.insert(0, str(_TOOLS_DIR))

from outline_adapter import generate_outline, outline_to_slide_specs, STYLES

try:
    from bootcamp_utils import get_client, get_flash_model
except ImportError:
    def get_client():
        return None
    def get_flash_model() -> str:
        return "gemini-3-flash-preview"


# ─── clasp 実行ヘルパー ───────────────────────────────────────

def _run_clasp(args: list[str], cwd: Path, timeout: int = 300) -> tuple[bool, str]:
    """clasp コマンドを実行"""
    cmd = ["npx", "@google/clasp"] + args
    try:
        result = subprocess.run(
            cmd, cwd=cwd,
            capture_output=True, text=True,
            timeout=timeout,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, f"タイムアウト ({timeout}秒)"
    except FileNotFoundError:
        return False, "npx が見つかりません"


def _check_clasp_project() -> bool:
    return (_GAS_DIR / ".clasp.json").exists()


def _parse_clasp_run_output(raw_output: str) -> Optional[dict]:
    """clasp run の出力から JSON を抽出"""
    lines = raw_output.strip().split("\n")
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line.startswith("{"):
            json_candidate = "\n".join(l.strip() for l in lines[i:])
            try:
                return json.loads(json_candidate)
            except json.JSONDecodeError:
                pass
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        pass
    match = re.search(r'\{[\s\S]*\}', raw_output)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


def _push_gas() -> bool:
    """GAS コードを push"""
    print("[push] GAS コードを push 中...")
    ok, out = _run_clasp(["push", "--force"], cwd=_GAS_DIR)
    if not ok:
        print(f"[error] push 失敗:\n{out}")
    else:
        print("[push] 完了")
    return ok


# ─── setup ────────────────────────────────────────────────────

def cmd_setup(args: argparse.Namespace) -> int:
    """GAS プロジェクト初期設定"""
    if _check_clasp_project():
        print("[setup] GAS プロジェクトは設定済みです。")
        return 0

    print("[setup] GAS プロジェクトを作成します...")
    title = args.title or "gslides-creator"
    ok, out = _run_clasp(
        ["create", "--type", "standalone", "--title", title, "--rootDir", "."],
        cwd=_GAS_DIR,
    )
    if not ok:
        print(f"[setup] 作成失敗:\n{out}")
        return 1

    ok, out = _run_clasp(["push", "--force"], cwd=_GAS_DIR)
    print("[setup] GAS プロジェクト作成完了")
    print(f"  npx @google/clasp open --cwd {_GAS_DIR}")
    return 0


# ─── convert ──────────────────────────────────────────────────

def cmd_convert(args: argparse.Namespace) -> int:
    """テンプレートコピー → Gemini 新コンテンツ → replaceAllText"""
    template_id = args.template_id
    topic = args.topic
    title = args.title or topic

    if not _check_clasp_project():
        print("[error] GAS プロジェクト未設定。先に setup を実行してください。")
        return 1

    # ステップ1: gslides-parser でテンプレート構造を取得
    print(f"[1/4] テンプレートの構造を解析中 (ID: {template_id})...")
    mapping = _get_template_mapping(template_id)
    if not mapping:
        print("[error] テンプレート解析に失敗。gslides-parser が設定されていない可能性があります。")
        print("[hint] まず gslides-parser の setup を実行してください。")
        return 1

    placeholders = mapping.get("placeholders", [])
    if not placeholders:
        print("[warn] プレースホルダーが見つかりません。replaceAllText は実行されません。")

    # ステップ2: Gemini で新コンテンツ生成
    print(f"[2/4] Gemini で新コンテンツ生成中 (topic: {topic})...")
    replacements = _generate_replacements(placeholders, topic)
    print(f"[2/4] {len(replacements)} 個の置換データ生成完了")

    # ステップ3: push
    if not args.skip_push and not _push_gas():
        return 1

    # ステップ4: convertPresentation 実行
    print(f"[3/4] テンプレートコピー + 置換実行中...")
    params = json.dumps([template_id, title, replacements])
    ok, out = _run_clasp(
        ["run", "convertPresentation", "--params", params],
        cwd=_GAS_DIR,
    )

    if not ok:
        print(f"[error] GAS 実行失敗:\n{out}")
        return 1

    result = _parse_clasp_run_output(out)
    if not result:
        print("[error] 結果の JSON パースに失敗")
        return 1

    url = result.get("url", "")
    print(f"[4/4] 完了!")
    print(f"\n  URL: {url}")
    print(f"  ID:  {result.get('presentation_id', '')}")
    print(f"  置換: {result.get('replaced_count', 0)}/{result.get('total_placeholders', 0)}")

    return 0


def _get_template_mapping(template_id: str) -> Optional[dict]:
    """gslides-parser を使ってテンプレートの構造を取得"""
    parser_script = _PARSER_DIR / "gslides_parser.py"
    if not parser_script.exists():
        return None

    try:
        result = subprocess.run(
            [sys.executable, str(parser_script), "json", template_id, "--skip-push"],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode != 0:
            return None

        gas_data = json.loads(result.stdout)

        # gas_to_yaml でマッピング変換
        sys.path.insert(0, str(_PARSER_DIR))
        from gas_to_yaml import convert_gas_to_mapping
        return convert_gas_to_mapping(gas_data, use_gemini=False)
    except Exception:
        return None


def _generate_replacements(placeholders: list, topic: str) -> dict:
    """Gemini でプレースホルダーの新コンテンツを生成"""
    client = get_client()
    if not client or not placeholders:
        return {}

    ph_list = "\n".join(
        f"- {p['key']}: type={p.get('type','')}, role={p.get('role','')}, current=\"{p.get('current','')[:60]}\""
        for p in placeholders
    )

    prompt = f"""以下のプレースホルダーに対して、新しいトピック「{topic}」に合わせた新しいコンテンツを生成してください。

## プレースホルダー一覧
{ph_list}

## ルール
1. 各プレースホルダーの role に適したコンテンツを生成
2. current の文字数を参考に、同程度の長さで生成
3. 日本語で生成
4. JSON 形式で出力: {{"{{placeholder_key}}": "new value", ...}}
5. JSON 以外のテキストは出力しない"""

    try:
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=prompt,
            config={"temperature": 0.7},
        )
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text)
    except Exception:
        return {}


# ─── build ────────────────────────────────────────────────────

def cmd_build(args: argparse.Namespace) -> int:
    """テンプレートコピー → マッピング + データで精密書き換え"""
    template_id = args.template_id
    data_path = Path(args.data)
    title = args.title or "Built Presentation"

    if not data_path.exists():
        print(f"[error] データファイルが見つかりません: {data_path}")
        return 1

    if not _check_clasp_project():
        print("[error] GAS プロジェクト未設定。")
        return 1

    # データ YAML 読み込み
    with open(data_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    slide_updates = data.get("slides", data) if isinstance(data, dict) else data
    if not isinstance(slide_updates, list):
        print("[error] データは slides リスト形式が必要です。")
        return 1

    # push
    if not args.skip_push and not _push_gas():
        return 1

    # buildPresentation 実行
    print(f"[build] テンプレートコピー + 要素書き換え中...")
    params = json.dumps([template_id, title, slide_updates])
    ok, out = _run_clasp(
        ["run", "buildPresentation", "--params", params],
        cwd=_GAS_DIR,
    )

    if not ok:
        print(f"[error] GAS 実行失敗:\n{out}")
        return 1

    result = _parse_clasp_run_output(out)
    if not result:
        print("[error] 結果パース失敗")
        return 1

    url = result.get("url", "")
    print(f"[build] 完了!")
    print(f"\n  URL: {url}")
    print(f"  スライド更新: {result.get('slides_updated', 0)}")

    return 0


# ─── deck ─────────────────────────────────────────────────────

def cmd_deck(args: argparse.Namespace) -> int:
    """ゼロから or テンプレートベースでデッキ生成"""
    topic = args.topic
    title = args.title or topic
    slides_count = args.slides
    style_name = args.style
    template_id = args.template

    if not _check_clasp_project():
        print("[error] GAS プロジェクト未設定。")
        return 1

    # ステップ1: Gemini でアウトライン生成
    print(f"[1/3] Gemini でアウトライン生成中 (topic: {topic}, {slides_count}枚)...")
    try:
        outline = generate_outline(
            topic=topic,
            slides_count=slides_count,
            audience=args.audience or "ビジネスパーソン",
            language="ja",
        )
    except Exception as e:
        print(f"[error] アウトライン生成失敗: {e}")
        return 1

    actual_slides = len(outline.get("slides", []))
    print(f"[1/3] アウトライン生成完了: {actual_slides} スライド")

    # ステップ2: アウトライン → GAS slideSpecs 変換
    print(f"[2/3] slideSpecs 変換中 (style: {style_name})...")
    slide_specs = outline_to_slide_specs(outline, style_name=style_name)

    # push
    if not args.skip_push and not _push_gas():
        return 1

    # ステップ3: GAS でデッキ生成
    print(f"[3/3] Google Slides デッキ生成中...")

    if template_id:
        func_name = "createDeckFromTemplate"
        params = json.dumps([template_id, title, slide_specs])
    else:
        func_name = "createDeck"
        params = json.dumps([title, slide_specs])

    ok, out = _run_clasp(
        ["run", func_name, "--params", params],
        cwd=_GAS_DIR,
    )

    if not ok:
        print(f"[error] GAS 実行失敗:\n{out}")
        return 1

    result = _parse_clasp_run_output(out)
    if not result:
        print("[error] 結果パース失敗")
        return 1

    url = result.get("url", "")
    print(f"\n[done] デッキ生成完了!")
    print(f"  URL:    {url}")
    print(f"  ID:     {result.get('presentation_id', '')}")
    print(f"  スライド: {result.get('slides_count', 0)} 枚")

    # アウトライン YAML 保存（オプション）
    if args.save_outline:
        outline_path = Path(args.save_outline)
        outline_path.parent.mkdir(parents=True, exist_ok=True)
        with open(outline_path, "w", encoding="utf-8") as f:
            yaml.dump(outline, f, allow_unicode=True, default_flow_style=False)
        print(f"  アウトライン: {outline_path}")

    return 0


# ─── CLI ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Google Slides クリエーター — テンプレートから新スライドを作成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s setup
  %(prog)s convert TEMPLATE_ID --topic "新トピック" --title "新タイトル"
  %(prog)s build TEMPLATE_ID --data data.yaml --title "新タイトル"
  %(prog)s deck --topic "AI活用提案" --slides 10 --style corporate
  %(prog)s deck --topic "Q1報告" --template TEMPLATE_ID --style minimal
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")

    # setup
    p_setup = subparsers.add_parser("setup", help="GAS プロジェクト初期設定")
    p_setup.add_argument("--title", default="gslides-creator", help="GAS プロジェクト名")

    # convert
    p_convert = subparsers.add_parser("convert", help="テンプレートコピー → Gemini 書き換え")
    p_convert.add_argument("template_id", help="テンプレートのプレゼンテーション ID")
    p_convert.add_argument("--topic", required=True, help="新しいトピック")
    p_convert.add_argument("--title", help="新しいタイトル (デフォルト: topic)")
    p_convert.add_argument("--skip-push", action="store_true")

    # build
    p_build = subparsers.add_parser("build", help="テンプレートコピー → YAML データで書き換え")
    p_build.add_argument("template_id", help="テンプレートのプレゼンテーション ID")
    p_build.add_argument("--data", required=True, help="データ YAML パス")
    p_build.add_argument("--title", default="Built Presentation", help="新タイトル")
    p_build.add_argument("--skip-push", action="store_true")

    # deck
    p_deck = subparsers.add_parser("deck", help="ゼロからデッキ生成")
    p_deck.add_argument("--topic", required=True, help="トピック")
    p_deck.add_argument("--title", help="タイトル (デフォルト: topic)")
    p_deck.add_argument("--slides", type=int, default=10, help="スライド数 (デフォルト: 10)")
    p_deck.add_argument("--style", default="corporate", choices=list(STYLES.keys()), help="スタイル")
    p_deck.add_argument("--template", help="テンプレート ID (テーマを継承)")
    p_deck.add_argument("--audience", default="ビジネスパーソン", help="対象聴衆")
    p_deck.add_argument("--save-outline", help="アウトライン YAML 保存パス")
    p_deck.add_argument("--skip-push", action="store_true")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "setup": cmd_setup,
        "convert": cmd_convert,
        "build": cmd_build,
        "deck": cmd_deck,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())

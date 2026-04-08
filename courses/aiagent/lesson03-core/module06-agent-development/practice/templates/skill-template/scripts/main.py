#!/usr/bin/env python3
"""
{スキル名} - {スキルの説明}

使い方:
    python main.py --param1 value1 --param2 value2
"""

import argparse
import json
import os
import sys


def parse_args():
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(description="{スキルの説明}")
    parser.add_argument("--param1", required=True, help="{パラメータ1の説明}")
    parser.add_argument("--param2", default="{デフォルト値}", help="{パラメータ2の説明}")
    parser.add_argument("--output", "-o", default=None, help="出力先パス")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細出力")
    return parser.parse_args()


def validate_environment():
    """環境変数をチェック"""
    required_vars = []  # 例: ["API_KEY", "SECRET"]
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        print(f"Error: 以下の環境変数が未設定です: {', '.join(missing)}")
        sys.exit(1)


def main():
    """メイン処理"""
    args = parse_args()
    validate_environment()

    if args.verbose:
        print(f"パラメータ1: {args.param1}")
        print(f"パラメータ2: {args.param2}")

    # TODO: メイン処理を実装
    result = {
        "status": "success",
        "param1": args.param1,
        "param2": args.param2,
    }

    # 出力
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"出力完了: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()

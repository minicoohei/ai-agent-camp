#!/usr/bin/env python3
"""
main.py - YouTube Clipper スキル エントリーポイント

スキル規約に準拠したCLIエントリーポイント。
内部でclipper.pyのrun_clipperを呼び出す。
"""

import sys
from pathlib import Path

# スクリプトディレクトリをパスに追加
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from clipper import main

if __name__ == "__main__":
    main()

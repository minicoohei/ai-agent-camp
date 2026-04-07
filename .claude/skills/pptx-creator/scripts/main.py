#!/usr/bin/env python3
"""
main.py — pptx-creator スキルエントリポイント

pptx_creator.py の main() に委譲。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pptx_creator import main

if __name__ == "__main__":
    main()

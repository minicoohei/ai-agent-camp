#!/usr/bin/env python3
"""簡易静的サイトジェネレーター

Lesson 11-5 の演習テンプレート。
受講者はこのスクリプトを GitHub Actions ワークフローから呼び出し、
GitHub Pages / Vercel へのデプロイを自動化する。
"""
import json
import os
from datetime import datetime


def build():
    os.makedirs("dist", exist_ok=True)

    # index.html 生成
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>AI Agent Camp — ビルド成果物</title>
  <style>
    body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
    .meta {{ color: #666; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <h1>AI Agent Camp</h1>
  <p class="meta">ビルド日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  <p>GitHub Actions で自動生成されたページです。</p>
</body>
</html>"""

    with open("dist/index.html", "w") as f:
        f.write(html)

    # build-info.json 生成
    info = {
        "built_at": datetime.utcnow().isoformat(),
        "commit": os.environ.get("GITHUB_SHA", "local"),
        "ref": os.environ.get("GITHUB_REF", "local"),
    }
    with open("dist/build-info.json", "w") as f:
        json.dump(info, f, indent=2)

    print("ビルド完了: dist/ ディレクトリに成果物を生成しました")


if __name__ == "__main__":
    build()

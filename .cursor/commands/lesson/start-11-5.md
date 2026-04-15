---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
duration: "約25分"
prerequisites: ["start-11-1"]
level: "intermediate"
tags: ["github-actions", "deploy", "artifact", "release", "vercel", "github-pages"]
---

# 🎓 Lesson 11-5: GitHub Actions でデプロイ・ファイル生成

## 📍 このセッションでやること

**Lesson 11-5: GitHub Actions でデプロイ・ファイル生成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GitHub Actions でビルド成果物の生成、GitHub Pages / Vercel へのデプロイ、リリースノート自動生成を行う |
| 所要時間 | 約25分 |
| 使うスキル | GitHub Actions, GitHub Pages, Vercel CLI, gh CLI |
| 前提条件 | Lesson 11-1 完了（ワークフロー基本の理解） |

**このセッションの流れ:**
1. ビルド成果物の生成スクリプト
2. artifact としてのアップロード・保存
3. GitHub Pages へのデプロイ
4. Vercel 自動デプロイ
5. リリースノート自動生成

セッション終了時には、ビルド→デプロイ→リリースの自動化パイプラインが構築されています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## 🎯 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → Lesson 11-1 完了確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: ビルド成果物の生成

```json
{
  "title": "🚀 Step 1: ビルド成果物生成",
  "questions": [{
    "id": "step_action",
    "prompt": "Python / Node スクリプトで静的ファイルを生成するステップを作成します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "ビルド成果物の種類を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`scripts/build_site.py` を作成（簡単な静的サイトジェネレーター）:

```python
#!/usr/bin/env python3
"""簡易静的サイトジェネレーター"""
import os
import json
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
```

```bash
python scripts/build_site.py && ls -la dist/
```

**期待される結果**: `dist/` ディレクトリに `index.html` と `build-info.json` が生成される。

---

## 🚀 Step 2: artifact のアップロード・保存

```json
{
  "title": "🚀 Step 2: artifact 管理",
  "questions": [{
    "id": "step_action",
    "prompt": "ビルド成果物を GitHub Actions artifact として保存するワークフローを作成します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "artifact の仕組みを確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`.github/workflows/build-and-deploy.yml` を作成:

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build site
        run: python scripts/build_site.py

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: site-build-${{ github.run_number }}
          path: dist/
          retention-days: 30

      - name: Build summary
        run: |
          echo "## ビルド成果物" >> $GITHUB_STEP_SUMMARY
          echo "| ファイル | サイズ |" >> $GITHUB_STEP_SUMMARY
          echo "|---------|-------|" >> $GITHUB_STEP_SUMMARY
          for f in dist/*; do
            SIZE=$(wc -c < "$f" | tr -d ' ')
            echo "| $(basename $f) | ${SIZE} bytes |" >> $GITHUB_STEP_SUMMARY
          done
```

**ポイント:**
- `actions/upload-artifact@v4` でビルド成果物を保存
- `retention-days` で保持期間を指定（デフォルト90日）
- `$GITHUB_STEP_SUMMARY` でワークフローサマリにビルド情報を表示

**期待される結果**: ワークフロー実行後、Actions タブの Summary に artifact ダウンロードリンクが表示される。

---

## 🚀 Step 3: GitHub Pages へのデプロイ

```json
{
  "title": "🚀 Step 3: GitHub Pages デプロイ",
  "questions": [{
    "id": "step_action",
    "prompt": "ビルド成果物を GitHub Pages にデプロイします。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "GitHub Pages の設定方法を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

ワークフローに Pages デプロイジョブを追加:

```yaml
  deploy-pages:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build site
        run: python scripts/build_site.py

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist/

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**事前設定:**
1. リポジトリの Settings → Pages
2. Source: 「GitHub Actions」を選択

**期待される結果**: `https://<owner>.github.io/<repo>/` でサイトが公開される。

---

## 🚀 Step 4: Vercel 自動デプロイ

```json
{
  "title": "🚀 Step 4: Vercel デプロイ",
  "questions": [{
    "id": "step_action",
    "prompt": "Vercel CLI を使って GitHub Actions からデプロイします。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "Vercel の設定方法を確認"},
      {"id": "skip", "label": "スキップ（GitHub Pages のみ使う）"}
    ]
  }]
}
```

**選択後の案内（例）**:

`.github/workflows/vercel-deploy.yml` を作成:

```yaml
name: Vercel Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build
        run: python scripts/build_site.py

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Deploy to Vercel
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
        run: |
          vercel deploy dist/ --prod --token=$VERCEL_TOKEN \
            --yes --cwd .
```

**Secrets に設定する値:**
- `VERCEL_TOKEN`: Vercel ダッシュボード → Settings → Tokens で生成
- `VERCEL_ORG_ID`: `vercel link` 実行後に `.vercel/project.json` から取得
- `VERCEL_PROJECT_ID`: 同上

**期待される結果**: push のたびに Vercel にデプロイされ、プレビュー URL が発行される。

---

## 🚀 Step 5: リリースノート自動生成

```json
{
  "title": "🚀 Step 5: リリースノート自動生成",
  "questions": [{
    "id": "step_action",
    "prompt": "タグ push をトリガーにリリースノートを自動生成します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "gh release の使い方を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`.github/workflows/release.yml` を作成（または既存を拡張）:

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build
        run: python scripts/build_site.py

      - name: Create release archive
        run: |
          cd dist && tar czf ../release-${{ github.ref_name }}.tar.gz .
          cd .. && zip -r release-${{ github.ref_name }}.zip dist/

      - name: Generate release notes
        run: |
          # 前のタグから今回のタグまでのコミットログを取得
          PREV_TAG=$(git tag --sort=-creatordate | head -2 | tail -1)
          echo "## 変更内容" > release_notes.md
          echo "" >> release_notes.md
          git log ${PREV_TAG}..HEAD --pretty=format:"- %s (%h)" >> release_notes.md

      - name: Create GitHub Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release create ${{ github.ref_name }} \
            --title "Release ${{ github.ref_name }}" \
            --notes-file release_notes.md \
            release-${{ github.ref_name }}.tar.gz \
            release-${{ github.ref_name }}.zip
```

**テスト手順:**
```bash
# タグを作成して push
git tag v1.0.0
git push origin v1.0.0

# リリースを確認
gh release list
```

**期待される結果**: タグ push でリリースが自動作成され、ビルド成果物が添付される。

---

## ⚠️ よくあるトラブルと解決方法

```json
{
  "title": "⚠️ トラブルシューティング",
  "questions": [{
    "id": "trouble",
    "prompt": "問題が発生しましたか？",
    "options": [
      {"id": "trouble_1", "label": "GitHub Pages のデプロイに失敗"},
      {"id": "trouble_2", "label": "Vercel デプロイのエラー"},
      {"id": "trouble_3", "label": "artifact がダウンロードできない"},
      {"id": "trouble_4", "label": "リリースが作成されない"}
    ]
  }]
}
```

### トラブル1: 「GitHub Pages のデプロイに失敗」
**原因**: Pages の Source が「GitHub Actions」に設定されていない、または permissions が不足。
**解決プロンプト**:
```
リポジトリの Settings → Pages → Source で「GitHub Actions」が選択されているか確認してください。ワークフローに pages: write と id-token: write の permissions があるか確認してください。
```

### トラブル2: 「Vercel デプロイのエラー」
**原因**: `VERCEL_TOKEN` が無効、またはプロジェクトが未リンク。
**解決プロンプト**:
```
ローカルで vercel link を実行してプロジェクトをリンクしてください。.vercel/project.json から ORG_ID と PROJECT_ID を取得して Secrets に設定してください。
```

### トラブル3: 「artifact がダウンロードできない」
**原因**: `retention-days` の期限切れ、またはパスの指定ミス。
**解決プロンプト**:
```
ワークフローのログで upload-artifact ステップの出力を確認してください。path で指定したディレクトリにファイルが存在するか確認してください。
```

### トラブル4: 「リリースが作成されない」
**原因**: タグの形式が `v*` にマッチしていない、または permissions: contents: write がない。
**解決プロンプト**:
```
git tag の形式が v1.0.0 のように v で始まるか確認してください。gh release create コマンドをローカルで試して、エラーメッセージを確認してください。
```

---

## ✅ チェックポイント

- [ ] `scripts/build_site.py` で `dist/` にファイルが生成される
- [ ] artifact として成果物がアップロードされる
- [ ] GitHub Pages または Vercel にデプロイできる
- [ ] タグ push でリリースが自動作成される
- [ ] リリースにビルド成果物が添付されている

---

## 📋 成果物プレビュー

**作成されるファイル:**
```
scripts/
└── build_site.py              # 静的サイトジェネレーター

.github/workflows/
├── build-and-deploy.yml       # ビルド + Pages デプロイ
├── vercel-deploy.yml          # Vercel デプロイ（オプション）
└── release.yml                # リリースノート自動生成

dist/                          # ビルド成果物（実行時生成）
├── index.html
└── build-info.json
```

---

## ➡️ 次のステップ

```json
{
  "title": "➡️ 次のステップ",
  "questions": [{
    "id": "next_step",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_auto", "label": "Module 12（Notion連携）に進む → /start-12-1"},
      {"id": "review_module", "label": "Module 11 の成果物を振り返りたい"},
      {"id": "finish", "label": "今日はここまで"}
    ]
  }]
}
```

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "約20分"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["slide", "pptx", "demo"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 29-1: slide-forge APIキー不要デモ

## 📍 このセッションでやること

**Lesson 29-1: slide-forge APIキー不要デモ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | OpenAI APIキーなしで、同梱サンプルから PPTX / HTML の出力を確認する |
| 所要時間 | 約20分 |
| 使うスキル | slide-forge, build-only, PPTX確認 |
| 前提条件 | Lesson 0-3 |
| 教材ページ | [Module 29: slide-forge](https://ai-agent.camp/ja/course/module-29?slideId=first-run) を並行参照 |

**このセッションの流れ:**
1. 作業場所と依存を確認
2. slide-forge を取得
3. APIキー不要デモを実行
4. PPTX / HTML 出力を確認

セッション終了時には、APIキーを使わずに slide-forge の固定 chrome デッキを確認できています。

> **💡 ヒント**: 秘密情報や API キーをチャットに貼らないでください。このレッスンでは OpenAI API キーは不要です。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "APIキー不要デモを始める準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → Python 3.11+、Node.js、ImageMagick、Poppler の確認を案内)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: 作業場所と依存を確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 作業場所と依存を確認",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
slide-forge の APIキー不要デモを実行する前に、作業場所と依存を確認してください。

確認項目:
1. 既存の slide-forge ディレクトリがある場合は勝手に上書きしない
2. Python 3.11+ が使える
3. Node.js が使える
4. ImageMagick の magick が使える
5. Poppler の pdfinfo / pdftoppm が使える
6. macOS: brew install imagemagick poppler ／ Windows・Linux は各パッケージマネージャで ImageMagick と Poppler を導入

秘密情報や API キーの値は表示しないでください。
```

**期待される結果**: 作業場所と依存の不足が一覧化されます。

---

## 🚀 Step 2: slide-forge を取得

未取得の場合は、公式リポジトリから取得します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: slide-forge を取得",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
slide-forge が未取得なら、次の手順で取得してください。
既存ディレクトリや既存 checkout がある場合は上書きせず、後続手順でも .env / config.yaml を上書きしないでください。

git clone --depth 1 --branch v0.1.0 https://github.com/minicoohei/slide-forge.git
cd slide-forge

検証済みバージョンを固定して使う（供給網対策）。
```

**期待される結果**: slide-forge リポジトリのルートに移動できます。

---

## 🚀 Step 3: APIキー不要デモを実行

同梱サンプル画像を使って、OpenAI API キーなしで PPTX / HTML を生成します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: APIキー不要デモを実行",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
依存をインストールし、APIキー不要デモを実行してください。

pip install -r requirements.txt
cd pipeline/lib && npm ci && npx playwright install chromium && cd ../..
cp -n .env.example .env
cp -n config.default.yaml config.yaml
python cli.py build-only --manifest examples/sample_manifest.json \
  --tastes lime --formats pptx html --no-regen --out examples/sample

注意:
- 既存の .env / config.yaml は cp -n により上書きしません
- オフラインデモは --out examples/sample --tastes lime 固定です
- 値を変えると本文画像が無い空デッキになり、missing_bodies が出ます
- OpenAI API キーは不要です
```

**期待される結果**: `examples/sample/lime/deck.pptx` と `examples/sample/lime/deck.html` が生成されます。

---

## 🚀 Step 4: PPTX / HTML 出力を確認

生成されたファイルを開いて、固定 chrome の見え方を確認します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: PPTX / HTML 出力を確認",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
生成された PPTX と HTML を確認してください。

open examples/sample/lime/deck.pptx

確認観点:
1. 見出し・リード・フッターが編集可能テキストとして載っている
2. 固定 chrome が全ページで同じ座標に揃っている
3. 本文図解だけが画像として配置されている
4. HTML でも deck.html を開いて同じ内容を確認できる
```

**期待される結果**: PPTX / HTML の両方でサンプルデッキを確認できます。

---

## ⚠️ よくあるトラブルと解決方法

AskUserQuestion（AskQuestion）でトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "missing_bodies が出る"},
      {"id": "trouble_2", "label": "magick / pdfinfo が無い"},
      {"id": "trouble_3", "label": "Playwright の Chromium が無い"},
      {"id": "trouble_4", "label": "PPTX が開けない"}
    ]
  }]
}
```

### トラブル1: `missing_bodies` が出る
**原因**: `--out examples/sample --tastes lime` 以外で実行している
**解決プロンプト**:
```
slide-forge の APIキー不要デモを --out examples/sample --tastes lime 固定で再実行してください。
なぜこの値が固定なのかも説明してください。
```

### トラブル2: `magick` / `pdfinfo` が無い
**原因**: ImageMagick または Poppler が未インストール
**解決プロンプト**:
```
macOS で ImageMagick と Poppler をインストールし、magick / pdfinfo / pdftoppm を確認する手順を案内してください。
```

### トラブル3: Playwright の Chromium が無い
**原因**: `npx playwright install chromium` が未実行
**解決プロンプト**:
```
slide-forge の pipeline/lib で Chromium をインストールし直す手順を案内してください。
```

### トラブル4: PPTX が開けない
**原因**: 生成途中で失敗したか、空デッキを開いている
**解決プロンプト**:
```
deck.pptx の存在、ファイルサイズ、build-only の JSON 出力を確認し、失敗箇所を切り分けてください。
```

---

## ✅ チェックポイント
- [ ] slide-forge の作業ディレクトリを確認した
- [ ] Python 3.11+ / Node.js / ImageMagick / Poppler を確認した
- [ ] APIキー不要デモを `--out examples/sample --tastes lime` 固定で実行した
- [ ] `examples/sample/lime/deck.pptx` を開いた
- [ ] `examples/sample/lime/deck.html` を確認した
- [ ] 秘密情報や API キーをチャットに貼っていない

---

## 📚 成果物プレビュー

このレッスンの成果物は API キーなしで生成したサンプルデッキです。

### 期待される出力
```
examples/sample/lime/deck.pptx
examples/sample/lime/deck.html
```

> 💡 PDF / PNG も確認する場合は `--formats pdf png` で追加生成できます。

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: examples/sample/lime/deck.pptx と deck.html が生成され、固定 chrome と編集可能テキストを確認できたか判定してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。次のセクションを始めるか、新しいウィンドウを開いて、新しいセクションを開始してください。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-29-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-29-2
- finish → 終了

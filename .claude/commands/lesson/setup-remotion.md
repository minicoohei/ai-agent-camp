---
description: "Remotion セットアップ（npm install + 動作確認ガイド付き）"
duration: "約10分"
prerequisites: ["Node.js 18以上がインストール済み"]
level: "beginner"
tags: ["setup", "remotion", "video", "react", "npm"]
---

# Remotion セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-remotion` を実行して進捗を表示
2. 既存の環境を自動検出:
   - `node --version` で Node.js のバージョン確認（18以上が必要）
   - `mv-composer/node_modules/remotion` が存在するか確認
   - 既にセットアップ済みの場合、Step 3（動作テスト）のみ実行して完了にできる

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Remotion（React ベースの動画生成フレームワーク）を mv-composer/ にセットアップし、Remotion Studio が起動できる状態にする |
| 所要時間 | 約10分 |
| 前提条件 | Node.js 18 以上がインストール済みであること |
| 操作レベル | すべてAIが自動実行（確認のみ） |

**Remotion とは:**
React コンポーネントで動画を作成できるフレームワークです。プログラマブルにアニメーション動画を生成でき、プロモーションMV、TikTok/YouTube Shorts、プロダクト紹介動画などの制作に使います。

**料金について:**
Remotion はオープンソースで、ローカルレンダリングは無料です。Remotion Lambda（クラウドレンダリング）を使う場合のみ別途ライセンスが必要ですが、研修では使用しません。

**このセッションの流れ:**
1. Node.js バージョン確認
2. npm install で依存パッケージをインストール
3. Remotion Studio の起動テスト
4. テストレンダリング（任意）

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "セッション開始前の確認",
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
(check_prereq → 「Node.js 18以上が必要です。`node --version` で確認できます。未インストールの場合は https://nodejs.org からインストールしてください」と案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: Node.js の確認

**AIが実行すること:**
1. Node.js のバージョンを確認する:

```bash
node --version
```

2. npm のバージョンを確認する:

```bash
npm --version
```

**判定基準:**
- Node.js 18.x 以上 → OK、Step 2 へ
- Node.js 未インストール or 18未満 → インストール案内

**Node.js がインストールされていない場合の案内:**

```text
Node.js 18以上が必要です。以下からインストールしてください:
  https://nodejs.org （LTS版を推奨）

Mac の場合は Homebrew でもインストールできます:
  brew install node
```

**ブラウザ起動コマンド:**
```bash
# Mac:
open https://nodejs.org
# Windows:
start https://nodejs.org
# Linux:
xdg-open https://nodejs.org
```

インストール後、「完了しました」と入力してもらい、再度 `node --version` で確認する。

---

## Step 2: Remotion のインストール

**AIが実行すること:**
1. mv-composer ディレクトリに移動して npm install を実行:

```bash
cd mv-composer && npm install
```

2. インストール結果を確認:

```bash
ls mv-composer/node_modules/remotion/package.json && echo "Remotion installed OK"
```

**期待される結果:**
- `added XX packages` のメッセージが表示される
- `Remotion installed OK` と表示される

**トラブルシューティング:**
- `EACCES` エラー → `sudo` は使わない。`npm config set prefix ~/.npm-global` で回避
- `ERESOLVE` エラー → `npm install --legacy-peer-deps` を試す
- ネットワークエラー → プロキシ設定を確認

---

## Step 3: Remotion Studio の起動テスト

**AIが実行すること:**
1. Remotion Studio を起動する:

```bash
cd mv-composer && npx remotion studio
```

**期待される結果:**
- ブラウザが自動で開き、Remotion Studio が表示される
- コンポジション一覧（ScreenExplainer 等）が左パネルに表示される
- プレビュー画面で動画がレンダリングされる

**ユーザーへの案内:**
```text
ブラウザに Remotion Studio が表示されましたか？
左パネルにコンポジション一覧が表示されていれば成功です。

確認できたら Ctrl+C でサーバーを停止してください。
```

**AskQuestionの設定:**
```json
{
  "title": "Remotion Studio 確認",
  "questions": [{
    "id": "studio_check",
    "prompt": "Remotion Studio はブラウザに表示されましたか？",
    "options": [
      {"id": "success", "label": "表示された！"},
      {"id": "no_browser", "label": "ブラウザが開かない"},
      {"id": "error", "label": "エラーが出た"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

(success → Step 4へ)
(no_browser → `http://localhost:3000` を手動でブラウザに入力するよう案内)
(error → エラーメッセージを貼ってもらい、トラブルシューティング)
(skip → Step 4へ)

---

## Step 4: テストレンダリング（任意）

**AskQuestionの設定:**
```json
{
  "title": "テストレンダリング",
  "questions": [{
    "id": "render_test",
    "prompt": "テストレンダリングを試しますか？（約30秒〜1分）",
    "options": [
      {"id": "yes", "label": "試す"},
      {"id": "no", "label": "スキップして完了する"}
    ]
  }]
}
```

(yes → テストレンダリングを実行)
(no → 完了チェックへ)

**AIが実行すること（yesの場合）:**
1. 短いコンポジションをレンダリングする:

```bash
cd mv-composer && npx remotion render src/index.ts ScreenExplainer --frames=0-30 --codec h264 out/test_render.mp4
```

2. 出力ファイルの確認:

```bash
ls -lh mv-composer/out/test_render.mp4
```

**期待される結果:**
- `out/test_render.mp4` が生成される
- ファイルサイズが 0 より大きい

**レンダリング後の案内:**
```text
テストレンダリングが完了しました。
out/test_render.mp4 が生成されています。

動画を確認するには:
  open mv-composer/out/test_render.mp4  (Mac)
  start mv-composer\out\test_render.mp4  (Windows)
```

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestionの設定:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "npm install が失敗する"},
      {"id": "trouble_2", "label": "Remotion Studio が開かない"},
      {"id": "trouble_3", "label": "レンダリングが失敗する"},
      {"id": "trouble_4", "label": "TypeScript エラーが出る"}
    ]
  }]
}
```

### トラブル1: 「npm install が失敗する」
**原因**: Node.js バージョン不足、ネットワーク問題
**解決プロンプト:**
```text
以下を順に確認してください:
1. node --version が 18.x 以上か
2. npm cache clean --force を実行してリトライ
3. npm install --legacy-peer-deps を試す
```

### トラブル2: 「Remotion Studio が開かない」
**原因**: ポート競合、ブラウザ設定
**解決プロンプト:**
```text
1. http://localhost:3000 をブラウザに直接入力
2. ポート変更: npx remotion studio --port 3001
3. ファイアウォール設定を確認
```

### トラブル3: 「レンダリングが失敗する」
**原因**: FFmpeg 未インストール、メモリ不足
**解決プロンプト:**
```text
Remotion は内蔵 FFmpeg を使うため、通常は追加インストール不要です。
エラーメッセージを確認してください。
メモリ不足の場合: --concurrency=1 オプションを追加
```

### トラブル4: 「TypeScript エラーが出る」
**原因**: 型定義の不一致
**解決プロンプト:**
```text
1. node_modules を削除して再インストール:
   rm -rf mv-composer/node_modules && cd mv-composer && npm install
2. TypeScript バージョン確認:
   npx tsc --version
```

---

## ✅ チェックポイント
- [ ] Node.js 18 以上がインストールされている
- [ ] mv-composer/node_modules/remotion が存在する
- [ ] Remotion Studio がブラウザで表示できた
- [ ] （任意）テストレンダリングが成功した

---

## ✅ 完了チェック

**AIが実行すること:**
```bash
# Node.js バージョン確認
node --version

# Remotion インストール確認
ls mv-composer/node_modules/remotion/package.json && echo "OK: Remotion installed"

# セットアップ進捗を完了に
uv run python tools/setup_progress.py complete setup-remotion
```

---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```text
┌─────────────────────────────────────┐
│  Remotion セットアップ完了            │
│  Node.js: v18.x.x ✅               │
│  Remotion: 4.0.434 ✅               │
│  Studio: 起動確認済み ✅             │
└─────────────────────────────────────┘
```

---

## ➡️ 次のステップ

Remotion のセットアップが完了しました。動画制作レッスンに進めます。

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "lesson_15_8", "label": "Lesson 15-8: Remotion でマーケ素材を自動生成"},
      {"id": "mv_composer", "label": "MV Composer で動画を作る"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内:**
- lesson_15_8 → /start-15-8
- mv_composer → 「MV動画を作って」と入力すると mv-composer スキルが起動します
- finish → 終了

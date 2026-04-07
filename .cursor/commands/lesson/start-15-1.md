---
description: "When the user says /start-15-1 — Module 15 Lesson 15-1: 動画からキーフレームを抽出して分析"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "約30分"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["video", "keyframe", "analysis", "ffmpeg"]
---

# 🎓 Lesson 15-1: 動画フレーム分析

## 📍 このセッションでやること

**Lesson 15-1: 動画フレーム分析** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 動画からキーフレームを抽出し、内容を分析して要約レポートを作成する |
| 所要時間 | 約30分 |
| 使うスキル | video-frame-reader (FFmpeg, Gemini Vision API) |
| 前提条件 | FFmpeg・Python 3.9以上・Gemini APIキー設定済み |
| 教材ページ | [Module 15: 動画生成](https://ai-agent.camp/ja/course/module-15) を並行参照 |

**このセッションの流れ:**
1. 環境の確認
2. サンプル動画の準備
3. キーフレームの抽出と分析
4. 動画の要約レポート作成

セッション終了時には、動画のキーフレームと要約が outputs に保存されています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

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
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 前提条件の確認を実行)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 0: テスト用動画の準備

同梱サンプル動画を優先して使います。手元に動画がない場合のみ、FFmpeg で練習用動画を追加します。

```bash
# lesson 配下の data ディレクトリを作成（なければ）
mkdir -p courses/aiagent/lesson03-core/module15-video/practice/data/videos

# テスト用動画を FFmpeg で生成（10秒、640x480、30fps）:
ffmpeg -f lavfi -i testsrc=duration=10:size=640x480:rate=30 -pix_fmt yuv420p courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4
```

> **注意**: FFmpeg がインストールされていない場合は、Step 1 の環境確認で案内します。

---

## 🚀 Step 1: 環境の確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 環境の確認",
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
動画フレーム抽出に必要な環境を確認してください：
- FFmpegがインストールされているか
- Python 3.9以上がインストールされているか
- video-frame-readerスキルが利用可能か

インストールされていないものがあれば、インストール手順を教えてください。
```

**期待される結果**: 必要な環境が確認され、不足があればインストール手順が表示されます。

---

## 🚀 Step 2: サンプル動画の準備

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: サンプル動画の準備",
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
動画フレーム抽出のテスト用に、以下を確認してください：
1. `courses/aiagent/lesson03-core/module15-video/practice/data/videos/` フォルダがあること
2. デフォルトの公式サンプルとして `data/videos/module7-lesson1-frame-lab-sample.mp4` または `courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4` が使えること

別の動画で試す場合のみ、30秒以内の MP4 を `courses/aiagent/lesson03-core/module15-video/practice/data/videos/` に追加で配置してよい。
```

**期待される結果**: `data/videos/module7-lesson1-frame-lab-sample.mp4` を含むテスト用動画が揃い、パスが確認できる。

---

## 🚀 Step 3: キーフレームの抽出

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: キーフレームの抽出",
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
data/videos/module7-lesson1-frame-lab-sample.mp4 または
courses/aiagent/lesson03-core/module15-video/practice/data/videos/module15-lesson1-sample.mp4 から
キーフレームを抽出してください（video-frame-reader の extract_keyframes.py を使用）。

設定:
- 抽出間隔: 5秒ごと（またはスキルのデフォルト）
- 出力形式: スキルに従う（PNG 等）
- 出力先: data/frames/ など分かりやすいパス

抽出後、生成されたフレーム画像の一覧を表示してください。
```

**期待される結果**: 指定間隔でキーフレームがPNG形式で保存されます。

---

## 🚀 Step 4: 抽出フレームの分析

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 抽出フレームの分析",
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
抽出されたフレーム画像を分析してください：

data/frames/ 内の各画像について、
- シーンの内容説明
- 検出されたオブジェクト
- テキストがあればOCR結果
- 前のフレームとの違い

を教えてください。
```

**期待される結果**: 各フレームの内容が説明されます。

---

## 🚀 Step 5: 動画の要約レポート作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 動画の要約レポート作成",
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
フレーム分析結果を基に、動画の要約レポートを作成してください。

レポート内容:
- 動画の概要（1-2文）
- 主要なシーンのリスト
- タイムライン形式の内容説明
- 特徴的なポイント

出力: output/video_summary.md
```

**期待される結果**: 動画の内容がMarkdown形式で要約されます。

---

## 🚀 Step 6: シーン変化の検出

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 6: シーン変化の検出",
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
動画のシーン変化を自動検出してください。

検出方法:
- フレーム間の色分布の変化を分析
- 大きな変化があった時点をシーン境界として記録
- 各シーンの開始時間と終了時間を特定

結果をJSON形式で保存してください：
出力: output/scene_detection.json
```

> **注意**: シーン変化検出は将来の拡張機能です。現在はキーフレーム抽出のみ対応しています。
> このステップでは、FFmpeg の `select='gt(scene,0.3)'` フィルタや、フレーム間差分の手動比較で代替できます。

**期待される結果**: シーン変化のタイムスタンプがJSON形式で保存されます。

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
      {"id": "trouble_1", "label": "FFmpegが見つからない"},
      {"id": "trouble_2", "label": "動画が読み込めない"},
      {"id": "trouble_3", "label": "メモリ不足エラー"},
      {"id": "trouble_4", "label": "フレーム画像が真っ黒"}
    ]
  }]
}
```


### トラブル1: 「FFmpegが見つからない」
**原因**: FFmpegがインストールされていない
**解決プロンプト**:
```
FFmpegをインストールしてください。
macOSの場合: brew install ffmpeg
Windowsの場合: winget install ffmpeg または https://ffmpeg.org/download.html からダウンロード
インストール後、ffmpeg -version で確認してください。
```

### トラブル2: 「動画が読み込めない」
**原因**: 動画形式がサポートされていない、またはコーデックの問題
**解決プロンプト**:
```
動画ファイルの形式を確認してください。
ffprobe でコーデック情報を取得して、
サポートされている形式（MP4/H.264）への変換方法を教えてください。
```

### トラブル3: 「メモリ不足エラー」
**原因**: 動画が長い、または解像度が高い
**解決プロンプト**:
```
メモリ不足エラーを解決する方法を教えてください：
- 抽出間隔を長くする（例: 30秒ごと）
- 動画の解像度を下げる
- バッチ処理で分割して処理
```

### トラブル4: 「フレーム画像が真っ黒」
**原因**: 動画の最初がフェードインしている、またはコーデックの問題
**解決プロンプト**:
```
抽出されたフレームが黒い画像です。
- 開始位置を数秒後にずらす
- 別のフレーム抽出方法を試す
方法を教えてください。
```

---

## ✅ チェックポイント
- [ ] FFmpegがインストールできた
- [ ] テスト用動画を準備できた
- [ ] キーフレームを抽出できた
- [ ] 抽出された画像が正しく保存された
- [ ] フレーム内容を分析できた
- [ ] 動画の要約レポートを作成できた


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/ugc/
├── *.mp4           (動画ファイル)
├── metadata.json   (メタデータ)
└── thumbnails/     (サムネイル)
```

### 確認コマンド
```bash
# 出力ファイルの一覧とサイズ
ls -lh output/ugc/

# メタデータを確認
cat output/ugc/*metadata*.json 2>/dev/null | head -20

# 動画を再生（macOS: open / Linux: xdg-open）
open output/ugc/*.mp4
```

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-15-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-15-2
- finish → 終了

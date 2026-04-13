---
description: "When the user says /start-15-2 — Module 15 Lesson 15-2: Remotion でスライドシュート風テキストアニメーションを作る"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "約40分"
prerequisites: ["setup-remotion"]
level: "intermediate"
tags: ["video", "remotion", "animation", "text", "slide-shoot"]
---

# Lesson 15-2: Remotion アニメーション基礎 — スライドシュート風テキストアニメ

## 学習目標

Remotion の `spring` / `interpolate` を使い、テキストがかっこよくスライドインする動画を自作します。

| 項目 | 内容 |
|------|------|
| ゴール | spring / interpolate を使ったスライドシュート風テキストアニメーション動画を自作する |
| 所要時間 | 約40分 |
| 使うツール | Remotion (React + FFmpeg ローカルレンダリング) |
| 前提条件 | Node.js 18+・setup-remotion 完了 |
| コスト | **$0**（完全ローカル、外部APIなし） |
| 教材ページ | [Module 15: 動画生成](https://ai-agent.camp/ja/course/module-15) を並行参照 |

**セッションの流れ:**
1. Remotion の基本概念を理解する
2. `useCurrentFrame` / `spring` / `interpolate` の使い方を学ぶ
3. スライドシュート風テキストアニメを実装する
4. 複数行テキストのスタガー演出を追加する
5. 動画をレンダリングして確認する

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
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → `setup-remotion` の確認を案内)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: Remotion の基本概念

AskUserQuestion で「このまま進める / 例だけ確認 / スキップ」を選べます。

**説明内容:**

Remotion は **React で動画を作る** フレームワークです:

- **フレームベースアニメーション**: `useCurrentFrame()` で現在のフレーム番号を取得し、スタイルを計算
- **spring()**: バネのような自然な動き。`damping`（減衰）、`mass`（質量）、`stiffness`（硬さ）で制御
- **interpolate()**: フレーム番号→値のマッピング（例: フレーム 0→30 を opacity 0→1 に変換）
- **レンダリング**: ローカルの FFmpeg で MP4 に書き出し。API不要、コスト$0

```tsx
// Remotion の基本パターン
import { useCurrentFrame, spring, interpolate, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// spring: 0 → 1 にバネ的に変化
const progress = spring({ frame, fps, config: { damping: 16, mass: 0.5, stiffness: 120 } });

// interpolate: progress を translateX に変換
const translateX = interpolate(progress, [0, 1], [200, 0]);
const opacity = interpolate(progress, [0, 1], [0, 1]);
```

---

## Step 2: 最小限のスライドインテキストを作る

入力内容:
```
mv-composer ディレクトリに以下の仕様でスライドインテキストのコンポーネントを作成してください。

■ ファイル名: src/components/scenes/SlideShootText.tsx

■ 仕様:
- 背景は黒 (#000000)
- テキストが右から左にスライドインしながらフェードイン
- spring 設定: damping: 16, mass: 0.5, stiffness: 120
- フォント: 白、太字、60px
- 1行のテキストを props で受け取る

■ 参考パターン（mv-composer/src/components/scenes/CinematicTextHook.tsx）:
- WordReveal の spring + interpolate パターンを参考にする
- translateX: 200px → 0px のスライドイン
- opacity: 0 → 1 のフェードイン
```

**期待される結果**: 1行テキストがスライドインする基本コンポーネントが作成されます。

---

## Step 3: スタガー演出を追加する（複数行テキスト）

入力内容:
```
Step 2 で作った SlideShootText を拡張して、複数行のスタガーアニメーションを作ってください。

■ 仕様:
- 複数行のテキストを配列で受け取る（例: ["AI Agent Camp", "動画を作る時代へ", "完全無料で始めよう"]）
- 各行が順番にスライドインする（スタガー: 各行の開始を 15 フレームずつずらす）
- 行ごとに delayFrames を設定可能にする
- 最終行は少しゆっくり表示する（stiffness を下げる）
- 全行表示完了後、2秒間保持してからフェードアウト

■ 参考パターン:
- CinematicTextHook.tsx の lineOffsets 計算ロジック
- spring の config を行ごとに変えるテクニック

■ Root.tsx に Composition として登録:
- id: "SlideShootDemo"
- durationInFrames: 150 (5秒 @30fps)
- fps: 30
- width: 1920, height: 1080
```

**期待される結果**: 複数行テキストが順番にスライドインするアニメーションが動作します。

---

## Step 4: 演出のバリエーション

入力内容:
```
SlideShootText にアニメーションバリエーションを追加してください。

■ 追加バリエーション（direction prop で切り替え）:
1. "right" — 右からスライドイン（デフォルト）
2. "left" — 左からスライドイン
3. "bottom" — 下からスライドアップ
4. "scale" — 中央で拡大しながらフェードイン（scale 0.5 → 1.0）

■ 追加演出（オプション）:
- textShadow で発光感を追加
- 背景にアンビエントオーブ（浮遊する光の玉）を追加
  → CinematicTextHook.tsx の orbDrift パターンを参考

■ 複数の Composition を Root.tsx に追加:
- "SlideShoot-Right", "SlideShoot-Left", "SlideShoot-Bottom", "SlideShoot-Scale"
```

**期待される結果**: 4種類のスライドイン方向が Remotion Studio でプレビューできます。

---

## Step 5: 動画のレンダリング

入力内容:
```
作成した SlideShootDemo をレンダリングしてください。

cd mv-composer
npx remotion render src/index.ts SlideShootDemo out/slide-shoot-demo.mp4

バリエーションも一括レンダリング:
npx remotion render src/index.ts SlideShoot-Right out/slide-shoot-right.mp4
npx remotion render src/index.ts SlideShoot-Left out/slide-shoot-left.mp4
npx remotion render src/index.ts SlideShoot-Bottom out/slide-shoot-bottom.mp4
npx remotion render src/index.ts SlideShoot-Scale out/slide-shoot-scale.mp4

出力された MP4 を再生して確認してください。
```

---

## Step 5.5: /motion-review で品質チェック

**レンダリング後、必ず品質レビューを実行してください。**

入力内容:
```
/motion-review

レンダリングした SlideShootText コンポーネントの品質をチェックしてください。

■ チェック対象:
- src/components/scenes/SlideShootText.tsx
- out/slide-shoot-demo.mp4

■ 特に確認したい項目:
- トランジション: 黒フレームがないか、フェードが自然か
- モーション品質: spring の振動が残っていないか
- テロップ: フォントサイズ・視認性が十分か
- 全体的な完成度
```

`/motion-review` は26項目のチェックリストでRemotionの品質を自動レビューします。
P1（致命的）/ P2（重要）/ P3（改善推奨）の3段階で問題を報告し、修正提案も出してくれます。

**P1/P2 の指摘があった場合**: 指摘に従って修正し、再レンダリング → 再レビューしてください。

---

## Step 6（発展）: 自分のテーマでテキストアニメを作る

入力内容:
```
自分のテーマでオリジナルのスライドシュート動画を作ってください。

■ お題例:
- 自己紹介動画（名前 → 肩書き → メッセージ）
- プロダクト紹介（サービス名 → キャッチコピー → URL）
- イベント告知（日時 → 場所 → タイトル）

■ カスタマイズポイント:
- テキスト内容の変更
- spring の設定調整（damping / stiffness で動きの「味」を変える）
- フォントサイズ・色の変更
- 背景色やアンビエント効果のカスタマイズ
```

---

## ⚠️ よくあるトラブルと解決方法

### 「Remotion Studio が起動しない」
**原因**: Node.js バージョン or 依存パッケージの問題
```
確認: node --version が 18 以上か / npm install が完了しているか
```

### 「レンダリングでエラー」
**原因**: FFmpeg 未インストール or Composition ID の不一致
```
確認: ffmpeg -version が実行できるか / Root.tsx の id とコマンドの id が一致しているか
```

### 「アニメーションがカクつく」
**原因**: spring 設定が過敏 or フレームレート不足
```
調整: damping を 14-20 に / stiffness を 100-150 に / fps を 30 以上に
```

### 「日本語フォントが表示されない」
**原因**: フォント未設定
```
fontFamily に "Noto Sans JP", "Hiragino Sans", sans-serif を指定
```

---

## ✅ チェックポイント
- [ ] Remotion の useCurrentFrame / spring / interpolate を理解した
- [ ] 単一テキストのスライドインが動作した
- [ ] 複数行のスタガーアニメーションが動作した
- [ ] 4方向のバリエーションを試した
- [ ] MP4 にレンダリングできた

---

## 📋 成果物プレビュー

### 期待される出力
```
📁 out/
├── slide-shoot-demo.mp4     (メインデモ)
├── slide-shoot-right.mp4    (右からスライドイン)
├── slide-shoot-left.mp4     (左からスライドイン)
├── slide-shoot-bottom.mp4   (下からスライドアップ)
└── slide-shoot-scale.mp4    (拡大フェードイン)
```

### 確認コマンド
```bash
ls -lh out/slide-shoot*.mp4
open out/slide-shoot-demo.mp4
```

---

## ➡️ 次のステップ

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-15-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

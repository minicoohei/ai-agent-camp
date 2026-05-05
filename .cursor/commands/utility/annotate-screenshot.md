---
nonInteractiveMode: compliant
---

# Annotate Screenshot with Nano Banana Pro

このコマンドは、`tools/annotate_screenshot.py` を使用して、スクリーンショットにマニュアル用の注釈（赤枠・矢印・吹き出し・テキスト）を追加します。

## 重要な原則

**元のスクリーンショットは絶対に変更されません。**

- 入力画像のピクセルは一切修正されない
- 注釈は元画像の上にオーバーレイとして追加される
- 出力は必ず別ファイルとして保存される
- マニュアル用途のため、実画面をそのまま保持することを徹底

## 実行手順

1. **パラメータの抽出**:
   ユーザーの入力から以下の情報を抽出してください。
   - **入力画像パス**: 注釈を追加したいスクリーンショット（必須）
   - **注釈指示**: どこに何を追加するか（必須）例: 「保存ボタンを赤枠で囲む」
   - **テキストラベル**: 矢印や吹き出しに表示するテキスト（任意）
   - **スタイル**: `red_box` (default), `arrow`, `callout`, `highlight`, `circle`, `number`
   - **出力パス**: 省略時は `{元ファイル名}_annotated.png`

2. **ツールの実行**:
   以下の形式でコマンドを実行してください。
   ```bash
   uv run python tools/annotate_screenshot.py "{入力画像パス}" "{注釈指示}" --style "{スタイル}" --text "{テキストラベル}" --output "{出力パス}"
   ```

3. **結果の確認**:
   - 生成された注釈付き画像のパスを確認し、ユーザーに報告してください。
   - **元画像が変更されていないことを明示**してください。
   - エラーが発生した場合は、エラーメッセージを表示してください。

## スタイル一覧

| スタイル | 説明 |
|----------|------|
| `red_box` | 赤い矩形枠で要素を囲み、矢印を追加（デフォルト） |
| `arrow` | 赤い矢印で要素を指し示す |
| `callout` | 吹き出し（コメントバルーン）を追加 |
| `highlight` | 蛍光ペン風の半透明ハイライト |
| `circle` | 赤い丸で要素を囲む |
| `number` | 番号付きマーカーを追加（手順の順序表示用） |

## 使用例

### 基本的な使用（赤枠 + 矢印）
```
/annotate-screenshot docs/manual_screenshots/login.png 「ログイン」ボタンを赤枠で囲んで矢印を追加
```

### テキストラベル付き
```
/annotate-screenshot settings.png 右上の「設定」アイコン --text "ここをクリック"
```

### 吹き出しスタイル
```
/annotate-screenshot dashboard.png メニューバー --style callout --text "この領域から操作します"
```

### 蛍光ペン風ハイライト
```
/annotate-screenshot form.png 入力フィールド --style highlight
```

### 出力先を指定
```
/annotate-screenshot original.png 「送信」ボタン --output docs/manual_screenshots/step3_annotated.png
```

### 複数の注釈を順番に追加（番号付きマーカー）
```
/annotate-screenshot workflow.png 最初の入力欄 --style number --text "1"
/annotate-screenshot workflow_annotated.png 次のドロップダウン --style number --text "2" --output workflow_step2.png
```

## 注意事項

- 実行には `GEMINI_API_KEY` または `GOOGLE_API_KEY` が環境変数（または `.env`）に設定されている必要があります。
- 出力ファイルパスが入力ファイルパスと同じ場合は、安全のためエラーになります。
- Nano Banana Pro（Gemini 3 Pro Image Preview）を使用するため、プロンプトで元画像の保持を強く指示していますが、AI生成の特性上、微細な差異が生じる可能性があります。厳密なピクセルパーフェクトが必要な場合は、従来の `src/gemini_annotate.py`（Pillow描画版）の使用を検討してください。

















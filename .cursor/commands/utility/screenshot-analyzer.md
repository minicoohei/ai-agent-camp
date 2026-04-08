# Screenshot Analyzer - スクリーンショット解析統合ツール

このコマンドは、`tools/screenshot_analyzer.py` を使用して、スクリーンショットを解析し、エラー診断や操作チュートリアル生成を行います。

## 機能

- **Analyzeモード**: 画像内のエラーを検出し、原因と解決策（NextStep）を提示します。
- **Tutorialモード**: 画像内の操作手順を解析し、ステップごとの注釈付きチュートリアルを生成します。
- **注釈追加**: エラー箇所や操作ステップに、赤枠や矢印などの注釈を自動で追加します。

## 実行手順

1. **パラメータの抽出**:
   ユーザーの入力から以下の情報を抽出してください。
   - **入力画像パス**: 解析したいスクリーンショット（必須）
   - **モード**: `analyze`（エラー解析）または `tutorial`（操作手順）（オプション、デフォルト: `analyze`）
   - **出力パス**: 省略時は `docs/bootcamp/screenshots/{mode}_{timestamp}.html`

2. **ツールの実行**:
   以下の形式でコマンドを実行してください。

   ```bash
   # エラー解析モード（デフォルト）
   uv run python tools/screenshot_analyzer.py "{入力画像パス}" --mode analyze

   # 操作チュートリアルモード
   uv run python tools/screenshot_analyzer.py "{入力画像パス}" --mode tutorial
   ```

3. **結果の確認**:
   - 生成されたHTMLファイルのパスを確認し、ユーザーに報告してください。
   - Live Serverで開く方法を案内してください。
   - エラーが発生した場合は、エラーメッセージを表示してください。

## 使用例

### エラー解析（Analyzeモード）
```
/screenshot-analyzer error.png
```
または
```
/screenshot-analyzer error.png --mode analyze
```

### 操作チュートリアル生成（Tutorialモード）
```
/screenshot-analyzer menu.png --mode tutorial
```

### 注釈なしで実行
```
/screenshot-analyzer error.png --no-annotate
```

### 出力先を指定
```
/screenshot-analyzer error.png --output docs/report/error_analysis.html
```

## 注意事項

- 実行には `GEMINI_API_KEY` または `GOOGLE_API_KEY` が必要です。
- Tutorialモードでは、ステップごとに注釈画像が生成されるため、処理に時間がかかる場合があります。
- 元の画像ファイルは変更されません（注釈付き画像は別ファイルとして保存されます）。

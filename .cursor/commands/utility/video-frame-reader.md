# Video Frame Reader - 動画キーフレーム抽出

このコマンドは、動画からキーフレームを抽出し、必要に応じてGemini Visionでフレーム解析を行い、結果をJSONで出力します。

## 前提条件
- `ffmpeg` がインストール済み
- Python3 + `Pillow` + `numpy`
- Gemini APIキー（解析を行う場合）

## 実行手順

1. **パラメータの抽出**:
   ユーザーの入力から以下の情報を抽出してください。
   - **動画ファイルパス**（必須）
   - **出力ディレクトリ**（任意。省略時は `{動画名}_keyframes`）
   - **threshold**（任意、デフォルト: 0.85）
   - **quality**（任意、デフォルト: 30）
   - **scale**（任意、デフォルト: 0.3）
   - **intent**（任意、解析観点）
   - **max-frames**（任意、解析最大フレーム数。デフォルト: 12）

2. **初回のみ venv 準備**（未実施の場合）:
   ```bash
   cd .cursor/skills/video-frame-reader
   python3 -m venv venv          # Windowsでは python -m venv venv
   source venv/bin/activate      # Windowsでは venv\Scripts\activate
   pip install Pillow numpy --quiet
   ```

3. **抽出 + 解析**:
   ```bash
   uv run python tools/video_frame_analyzer.py "{動画パス}" -o "{出力ディレクトリ}" -t {threshold} -q {quality} -s {scale} --intent "{intent}" --max-frames {max_frames}
   ```

4. **結果の確認**:
   - JSON出力に `extraction` と `analysis` が含まれていることを確認
   - 解析を不要にする場合は `--no-analyze` を付ける
   - エラー時は `error` をそのまま表示

## 使用例

### 基本
```
/video-frame-reader /path/to/video.mp4
```

### トークン削減を強める
```
/video-frame-reader /path/to/video.mp4 -t 0.75 -q 20 -s 0.2
```

### 解析観点を指定
```
/video-frame-reader /path/to/video.mp4 --intent "ボタン操作後の画面遷移に違和感がないか確認"
```

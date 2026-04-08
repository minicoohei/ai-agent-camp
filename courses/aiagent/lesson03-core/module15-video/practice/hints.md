# ヒント: 動画生成・解析

## FFmpeg コマンドのヒント

### インストール確認
```bash
ffmpeg -version
# バージョン情報が表示されればOK
```

### macOS でのインストール
```bash
brew install ffmpeg
```

### 基本的な動画情報の取得
```bash
# 動画のメタ情報を確認
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

### フレーム抽出の手動実行
```bash
# 1秒ごとにフレームを抽出
ffmpeg -i input.mp4 -vf "fps=1" output_%04d.jpg

# キーフレームのみ抽出
ffmpeg -i input.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr keyframe_%04d.jpg
```

## video-frame-reader のヒント

### パラメータ調整のコツ

| パラメータ | 推奨値 | 説明 |
|-----------|--------|------|
| threshold | 0.85 | デフォルト。類似度が高いフレームを除外 |
| threshold | 0.75 | 動きの少ない動画向け。より多くのフレームを統合 |
| threshold | 0.95 | アニメーション等。ほぼ全フレームを保持 |
| quality | 30 | トークン節約。分析には十分な品質 |
| scale | 0.3 | トークン節約。UI分析には0.5推奨 |

### トークンコスト削減のコツ
- `threshold` を下げると類似フレームがまとめられ、枚数が減る
- `quality` を下げるとファイルサイズが小さくなる
- `scale` を下げると画像サイズが小さくなる
- まず低コスト設定で概要把握 → 気になる部分を高品質で再抽出

## storyboard-generator のヒント

### モード選択
- **sheet モード（推奨）**: 1枚のシートとして全フレームを一括生成。キャラクター一貫性が高い
- **individual モード**: 1フレームずつ生成。キャラの見た目がブレやすいが、個別にリトライ可能

### シナリオ記述のコツ
1. 各シーンの「場所」「人物の動作」「画面テキスト」を明確に書く
2. カメラアングルやライティングの指定があると品質が上がる
3. シーン間の「変化」を意識する（暗→明、問題→解決）

### キャラクター設定のコツ
- 服装・髪型・年齢を具体的に書く
- 「ビジネスカジュアルの30代男性」より「ネイビージャケットに白シャツ、黒髪短髪の30代男性」の方が一貫性が高い

### scenes.json の motion_type について
| タイプ | 説明 | 使い所 |
|--------|------|--------|
| static | 静止画のまま使用 | テキスト主体のシーン |
| ken_burns | ズーム/パン効果 | 風景、静的構図 |
| motion_graphics | Remotionでアニメーション | UI遷移、テキストアニメ |
| i2v | Image-to-Video変換 | 人物動作、表情変化 |

## fal.ai（動画生成）のヒント

### API キー設定
```bash
export FAL_KEY="your-fal-api-key"
```

### コスト意識
- i2v 変換は1クリップあたり数セントのコストがかかる
- まず短い動画（5秒）で品質を確認してから長尺（10秒）に挑戦
- `motion_type` が `static` や `ken_burns` のシーンは i2v 不要（コスト節約）

### カメラワークの指定
- `--camera-motion` オプションでカメラの動きを指定可能
- 例: "zoom in slowly", "pan left to right", "static"

## トラブルシューティング

### よくあるエラー

| エラー | 原因 | 対処 |
|--------|------|------|
| `ffmpeg: command not found` | FFmpeg未インストール | `brew install ffmpeg` |
| `GEMINI_API_KEY not set` | 環境変数未設定 | `.env` に追加 |
| `FAL_KEY not set` | fal.ai キー未設定 | `export FAL_KEY=...` |
| `Pillow not found` | パッケージ未インストール | `pip install Pillow` |
| 絵コンテが真っ白 | プロンプトが不適切 | シナリオをより具体的に |
| 動画が生成されない | API 制限超過 | しばらく待って再実行 |

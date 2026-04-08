# 講義動画生成パイプライン

Remotion + Veo3/Fabric/Viduを組み合わせて、AIエージェント研修用の講義動画を自動生成するパイプライン。

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────────┐
│                     講義動画生成パイプライン                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   コンテンツ   │ ──▶ │   スクリプト   │ ──▶ │    TTS     │       │
│  │   (HTML)     │     │   生成       │     │   (音声)    │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│                                                  │              │
│                                                  ▼              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │   Remotion   │     │   Veo3 /     │ ◀── │   アバター   │       │
│  │   (スライド)  │     │   Fabric     │     │   画像      │       │
│  └──────┬──────┘     └──────┬──────┘     └─────────────┘       │
│         │                    │                                  │
│         ▼                    ▼                                  │
│  ┌──────────────────────────────────────────┐                  │
│  │            最終合成 (FFmpeg)              │                  │
│  │   スライド動画 + プレゼンター動画           │                  │
│  └──────────────────────────────────────────┘                  │
│                          │                                      │
│                          ▼                                      │
│                   ┌─────────────┐                               │
│                   │  最終動画    │                               │
│                   │  (MP4)      │                               │
│                   └─────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

## コンポーネント

### 1. Remotion (スライド動画)
- ReactでスライドをレンダリングしてMP4に変換
- テキスト、画像、PlantUML図解のアニメーション
- トランジション効果（フェード、スライド等）

### 2. Veo3 (プレゼンター動画)
- Google Veo 3.1を使用
- プロンプトからアバター動画を生成
- 音声も同時に生成（TTS不要）
- 最大8秒/セグメント

### 3. Fabric (リップシンク動画)
- VEED Fabric 1.0を使用
- 画像 + 音声 → リップシンク動画
- より自然な口の動き

### 4. Vidu (追加予定)
- 高品質な動画生成エンジン
- 長尺動画のサポート

## 使用方法

### 準備

```bash
# 依存関係のインストール
cd tools/ugc/lecture_video
npm install

# 環境変数の設定
export FAL_KEY=your_fal_api_key
export ELEVEN_LABS_API_KEY=your_eleven_labs_key
export GEMINI_API_KEY=your_gemini_key
```

### スクリプト生成

```bash
python generate_lecture.py \
  --html course/foundation/llm-basics.html \
  --output output/lecture/llm-basics/
```

### 動画生成

```bash
# Fabricエンジンで生成
python generate_lecture.py \
  --html course/foundation/llm-basics.html \
  --engine fabric \
  --output output/lecture/llm-basics/

# Veo3で生成
python generate_lecture.py \
  --html course/foundation/llm-basics.html \
  --engine veo \
  --output output/lecture/llm-basics/
```

## ディレクトリ構造

```
lecture_video/
├── README.md
├── package.json
├── remotion/
│   ├── src/
│   │   ├── LectureVideo.tsx
│   │   ├── components/
│   │   │   ├── TitleSlide.tsx
│   │   │   ├── ContentSlide.tsx
│   │   │   └── DiagramSlide.tsx
│   │   └── styles/
│   │       └── lecture.css
│   └── remotion.config.ts
├── scripts/
│   ├── html_parser.py      # HTMLからコンテンツを抽出
│   ├── script_generator.py # 講義スクリプトを生成
│   └── video_composer.py   # 最終動画を合成
└── templates/
    └── lecture_prompt.json # スクリプト生成用プロンプト
```

## 生成フロー

1. **コンテンツ抽出**: HTMLから章、セクション、キーポイントを抽出
2. **スクリプト生成**: 各セクションの講義スクリプトを生成
3. **TTS生成**: スクリプトを音声に変換
4. **スライド動画生成**: Remotionでスライドをレンダリング
5. **プレゼンター動画生成**: Veo3/Fabricでアバター動画を生成
6. **最終合成**: スライドとプレゼンターを合成

## 設定オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--engine` | 動画生成エンジン (fabric/veo/vidu) | fabric |
| `--voice` | TTSの声 | default |
| `--avatar` | アバター画像のパス | 自動生成 |
| `--fps` | フレームレート | 30 |
| `--resolution` | 解像度 (720p/1080p) | 720p |
| `--presenter-position` | プレゼンター位置 (left/right/bottom) | right |

## 料金目安

| エンジン | 料金目安 | 特徴 |
|---------|---------|------|
| Fabric | $0.15/秒 (720p) | リップシンク精度高 |
| Veo3 | $8/8秒 (720p) | 音声自動生成 |
| Vidu | TBD | 長尺対応 |

30分の講義動画の場合:
- Fabric: 約$270 (1800秒 × $0.15)
- Veo3: 約$1800 (225セグメント × $8)

## 注意事項

- Veo3は1セグメント最大8秒のため、長い講義は複数セグメントに分割されます
- 本番環境での使用前に必ずテスト生成を行ってください
- APIキーの使用量に注意してください

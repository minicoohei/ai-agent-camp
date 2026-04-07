# Module 7: 動画生成 - 成果物（Final）

動画フレーム分析、絵コンテ生成、動画合成の例です。

## 学習目標
- 動画からキーフレームを抽出できる
- 絵コンテ（Storyboard）を作成できる
- 複数素材を組み合わせて動画を生成できる

## 成果物一覧

| ファイル | 種類 | 内容 |
|---------|------|------|
| `keyframes/` | 画像 | 抽出キーフレーム |
| `storyboard.md` | Markdown | 絵コンテ |
| `narration_script.txt` | テキスト | ナレーション台本 |
| `final_video.mp4` | 動画 | 最終出力動画 |
| `generation_config.json` | JSON | 生成設定 |

## 動画生成パイプライン

```
┌─────────────────────────────────────────────────────────┐
│  動画生成パイプライン                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 企画・構成                                          │
│     │                                                   │
│     ├─ 動画の目的定義                                   │
│     ├─ ターゲット視聴者                                 │
│     └─ 尺・形式の決定                                   │
│                                                         │
│  2. 絵コンテ作成                                        │
│     │                                                   │
│     ├─ シーン分割                                       │
│     ├─ カット構成                                       │
│     └─ トランジション指定                               │
│                                                         │
│  3. 素材準備                                            │
│     │                                                   │
│     ├─ 画像・映像素材                                   │
│     ├─ BGM・SE                                         │
│     └─ ナレーション音声                                 │
│                                                         │
│  4. 合成・編集                                          │
│     │                                                   │
│     ├─ タイムライン構築                                 │
│     ├─ エフェクト適用                                   │
│     └─ 音声同期                                         │
│                                                         │
│  5. 出力                                                │
│     │                                                   │
│     ├─ エンコード                                       │
│     └─ 品質確認                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 実行コマンド例

### キーフレーム抽出
```bash
uv run python tools/video_frame_analyzer.py extract \
  --input data/videos/source.mp4 \
  --output examples/final/module-07-video/keyframes/ \
  --interval 30 \
  --format png
```

### 絵コンテ生成
```bash
uv run python tools/ugc/script_generator.py \
  --topic "AIエージェント研修紹介動画" \
  --duration 60 \
  --style "professional" \
  --output examples/final/module-07-video/storyboard.md
```

### ナレーション生成（TTS）
```bash
uv run python tools/ugc/tts.py \
  --script examples/final/module-07-video/narration_script.txt \
  --voice "ja-JP-Standard-A" \
  --output examples/final/module-07-video/narration.mp3
```

### 動画合成
```bash
uv run python tools/ugc_factory.py compose \
  --config examples/final/module-07-video/generation_config.json \
  --output examples/final/module-07-video/final_video.mp4
```

## 絵コンテ形式

```markdown
# 絵コンテ: AIエージェント研修紹介

## 基本情報
- 尺: 60秒
- 形式: 1080p (1920x1080)
- スタイル: プロフェッショナル、明るい

---

## シーン1: オープニング (0:00-0:05)

**映像**: 
- ロゴアニメーション
- グラデーション背景（紺→白）

**テキスト**:
"AIエージェント研修"

**音声**:
BGM開始（明るいテクノ系）

**トランジション**: フェードイン

---

## シーン2: 問題提起 (0:05-0:15)

**映像**:
- オフィスで作業する人のイメージ
- 書類の山、忙しそうな様子

**ナレーション**:
「毎日の業務に追われていませんか？」

**テキスト**:
- "業務効率化の課題"

**トランジション**: スライド左

---

## シーン3: 解決策提示 (0:15-0:30)

**映像**:
- AIアシスタントのイメージ
- スムーズに作業が進むアニメーション

**ナレーション**:
「AIエージェントが、あなたの業務をサポートします」

**テキスト**:
- "AIエージェントで解決"
- 機能リスト（3項目）

**トランジション**: ズームイン

---

## シーン4: 機能紹介 (0:30-0:50)

**映像**:
- 機能デモ画面（4分割）
  1. バナー生成
  2. データ分析
  3. 文書作成
  4. タスク管理

**ナレーション**:
「バナー生成からデータ分析まで、
様々な業務を自動化できます」

**トランジション**: グリッド分割

---

## シーン5: CTA (0:50-0:60)

**映像**:
- ロゴ + QRコード
- 申し込みURL表示

**ナレーション**:
「今すぐ始めましょう」

**テキスト**:
- "無料トライアル実施中"
- URL: example.com/trial

**トランジション**: フェードアウト

---

## 技術仕様

| 項目 | 値 |
|------|-----|
| 解像度 | 1920x1080 (1080p) |
| フレームレート | 30fps |
| コーデック | H.264 |
| ビットレート | 8Mbps |
| 音声 | AAC 192kbps |
```

## 生成設定JSON例

```json
{
  "project": {
    "name": "ai-agent-intro",
    "duration": 60,
    "resolution": "1920x1080",
    "fps": 30
  },
  "scenes": [
    {
      "id": 1,
      "start": 0,
      "end": 5,
      "type": "title",
      "content": {
        "title": "AIエージェント研修",
        "background": "gradient",
        "animation": "fade_in"
      }
    },
    {
      "id": 2,
      "start": 5,
      "end": 15,
      "type": "narration",
      "content": {
        "video": "assets/office.mp4",
        "audio": "narration_scene2.mp3",
        "overlay_text": "業務効率化の課題"
      }
    }
  ],
  "audio": {
    "bgm": {
      "file": "assets/bgm_upbeat.mp3",
      "volume": 0.3,
      "fade_out": 3
    },
    "narration": {
      "voice": "ja-JP-Standard-A",
      "speed": 1.0
    }
  },
  "output": {
    "format": "mp4",
    "codec": "h264",
    "bitrate": "8M"
  }
}
```

## 利用可能なエンジン

| エンジン | 特徴 | 用途 |
|---------|------|------|
| **Veo3** | Google製、高品質、プロンプトベース | プレゼンター動画 |
| **Fabric** | 画像+音声からリップシンク | アバター動画 |
| **Remotion** | React/TypeScriptベース | スライド動画 |
| **FFmpeg** | 汎用動画処理 | 最終合成 |

## チェックリスト

- [ ] キーフレームが正しく抽出される
- [ ] 絵コンテが構造化されている
- [ ] ナレーションが自然に聞こえる
- [ ] シーン間のトランジションがスムーズ
- [ ] 音声と映像が同期している
- [ ] 出力品質が適切

## 関連レッスン

- `/start-7-1`: 動画フレーム分析
- `/start-7-2`: 絵コンテ生成
- `/start-7-3`: ナレーション作成
- `/start-7-4`: 素材準備
- `/start-7-5`: 動画合成
- `/start-7-6`: 最終出力

## 参考リンク

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Google Text-to-Speech](https://cloud.google.com/text-to-speech)
- [Remotion](https://www.remotion.dev/)

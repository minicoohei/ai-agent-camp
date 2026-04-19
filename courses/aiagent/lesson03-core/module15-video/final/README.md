# module15-video 完成例

## 概要

このディレクトリには、動画生成・解析演習の完成例が含まれています。
AIエージェント研修プロモーション動画（30秒、5シーン）の絵コンテを生成しました。

## 成果物一覧

### 絵コンテ画像（output/storyboard/）

| ファイル | シーン | 内容 |
|----------|--------|------|
| `scene_01_problem.png` | 問題提起 | 大量の作業に疲れたビジネスパーソン |
| `scene_02_discovery.png` | 出会い | Claude Code を発見する瞬間 |
| `scene_03_training.png` | 実践中 | 研修で AI ツールを操作する参加者たち |
| `scene_04_results.png` | 成果発表 | チームで成果を見せ合う場面 |
| `scene_05_cta.png` | CTA | CursorBootcamp のクロージング画面 |

## 使用ツール

- **nanobanana**: 各シーンの絵コンテ画像生成（Gemini Image Generation API）
- **storyboard-generator**: 実際の制作ではこちらのシートモードを推奨

## 再現手順

```bash
# シーン画像の個別生成（nanobanana使用）
uv run python tools/nanobanana.py "<プロンプト>" --output output/storyboard/scene_XX.png --aspect-ratio 9:16

# 絵コンテ一括生成（storyboard-generator使用、推奨）
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "AIエージェント研修プロモーション動画のシナリオ" \
    --character "30代の日本人男性、ネイビージャケットに白シャツ" \
    --aspect-ratio 9:16 \
    --num-frames 8 \
    --mode sheet \
    --session "promo_video"
```

## 学習ポイント

1. **シナリオ設計**: 30秒動画を5シーンに分割し、起承転結+CTAの構成
2. **キャラクター一貫性**: 詳細なキャラクター設定で全シーンの一貫性を確保
3. **motion_type 判定**: 各シーンに適切な動画化方式を選択（コスト最適化）
4. **ナレーション連携**: 画面テキストとナレーション台本を同期

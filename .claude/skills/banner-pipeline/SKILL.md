---
name: banner-pipeline
description: "バナー自動生成パイプライン — サイズ×訴求でバッチ生成→Gemini Vision品質スコアリング→自動選定→レビューHTML。banner-creator の発展版。「バナーをまとめて作って」「複数サイズでバナー生成」「バナーのバリエーション」で発動。"
triggers:
  - banner-pipeline
  - バナーパイプライン
  - バナーをまとめて作って
  - 複数サイズでバナー生成
  - バナーのバリエーション
  - バッチバナー
---

# Banner Pipeline - バナー自動生成パイプライン

`banner-creator` の発展版スキル。1枚ずつ手動で作る代わりに、**サイズ × 訴求を一括生成 → AI品質採点 → ベスト自動選定**まで全自動で実行します。

## banner-creator との違い

| 項目 | banner-creator | banner-pipeline |
|------|---------------|-----------------|
| 生成方式 | 1枚ずつ指定 | サイズ×訴求のクロス積で一括 |
| 品質判定 | なし（目視） | Gemini Vision で4軸100点採点 |
| 選定 | 手動 | スコア上位K枚を自動選定 |
| レビュー | なし | スコア付きHTMLダッシュボード |
| ロゴ合成 | なし | オプションで自動合成 |

## Usage

```bash
# 基本: 3サイズ × 3訴求 = 9枚 → 各サイズTop2を選定
uv run python tools/banner_pipeline.py \
  --sizes "1200x675,1080x1080,300x250" \
  --appeals "AIエージェント研修,業務効率3倍,非エンジニアでもできる" \
  --brand "AI Agent Camp" --price "月額12,800円" \
  --session my_campaign --top-k 2

# ロゴ合成あり
uv run python tools/banner_pipeline.py \
  --sizes "240x120,200x120" \
  --appeals "Claude Code実践講座,AIを武器にする" \
  --logo assets/logo.png \
  --session with_logo --top-k 1

# スコアリングをスキップ（テスト用）
uv run python tools/banner_pipeline.py \
  --sizes "300x250" --appeals "テスト訴求" \
  --session quick_test --skip-scoring
```

## パラメータ

| パラメータ | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--sizes` | Yes | カンマ区切りの WxH | - |
| `--appeals` | Yes | カンマ区切りの訴求ヘッドライン | - |
| `--logo` | No | ロゴPNGパス（指定時に合成） | なし |
| `--brand` | No | ブランド名 | `AI Agent Camp` |
| `--price` | No | 価格テキスト | `月額12,800円` |
| `--session` | No | セッション名 | `default` |
| `--top-k` | No | サイズ毎の選定枚数 | `3` |
| `--output-dir` | No | 出力ベースディレクトリ | `output/banners` |
| `--skip-scoring` | No | Vision スコアリングをスキップ | `false` |

## パイプライン

1. **Generate** — Gemini Image で2x解像度生成→ダウンスケール
2. **Logo Overlay** (任意) — 上部白帯にロゴ自動合成
3. **Vision Scoring** — Gemini 2.0 Flash で4軸採点
4. **Auto-Select** — スコア上位K枚を `approved/` にコピー
5. **Review HTML** — スコア付きカードUIでレビューページ生成

## 出力

```
output/banners/{session}/
  generated/          ← 全生成画像
  approved/           ← 自動選定されたトップK
  review.html         ← レビューHTML（ブラウザで開く）
  results.json        ← スコア・verdict一覧
  vision_cache.json   ← スコアキャッシュ
```

## 前提条件

- `GEMINI_API_KEY` が設定済み
- `google-genai`, `Pillow`, `python-dotenv`

## 関連スキル

- `banner-creator` — 単発バナー生成（プラットフォーム別プリセット）
- `media-generator` — 汎用メディア生成

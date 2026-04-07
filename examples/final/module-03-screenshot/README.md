# Module 3: スクリーンショット分析 - 成果物（Final）

スクリーンショットの分析、注釈追加、チュートリアル生成の例です。

## 学習目標
- screenshot-analyzerでエラーを自動診断できる
- screenshot-annotatorで注釈を追加できる
- tutorial-generatorでステップバイステップガイドを作成できる

## 成果物一覧

| ファイル | 種類 | 内容 |
|---------|------|------|
| `error-404-analyzed.png` | エラー診断 | 404エラーの原因分析・解決策 |
| `form-validation-annotated.png` | 注釈付き | フォームバリデーションエラーの説明 |
| `ui-improvement.png` | UI分析 | UI改善提案のマーキング |
| `tutorial-steps/` | チュートリアル | 操作手順の連続画像 |
| `analysis-report.json` | レポート | 分析結果のJSON出力 |

## スクリーンショット分析の種類

```
┌─────────────────────────────────────────────────────────┐
│  スクリーンショット分析タイプ                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. エラー診断                                          │
│     ├─ エラーメッセージの解読                           │
│     ├─ 原因の特定                                      │
│     └─ 解決策の提案                                    │
│                                                         │
│  2. UI/UX分析                                          │
│     ├─ レイアウトの問題点                              │
│     ├─ アクセシビリティの課題                          │
│     └─ 改善提案                                        │
│                                                         │
│  3. チュートリアル生成                                  │
│     ├─ 操作手順の抽出                                  │
│     ├─ ステップ番号の追加                              │
│     └─ 説明テキストの生成                              │
│                                                         │
│  4. 比較分析                                            │
│     ├─ Before/After比較                                │
│     ├─ 差分の可視化                                    │
│     └─ 変更点のハイライト                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 実行コマンド例

### エラー診断
```bash
uv run python tools/screenshot_analyzer.py \
  --input data/screenshots/error-screen.png \
  --mode diagnose \
  --output examples/final/module-03-screenshot/error-404-analyzed.png
```

### 注釈追加
```bash
uv run python tools/annotate_screenshot.py \
  --input data/screenshots/form-error.png \
  --prompt "バリデーションエラーの箇所を赤枠で囲み、正しい入力例を注釈で追加" \
  --output examples/final/module-03-screenshot/form-validation-annotated.png
```

### UI改善分析
```bash
uv run python tools/screenshot_analyzer.py \
  --input data/screenshots/dashboard.png \
  --mode ui_review \
  --prompt "このダッシュボードのUI/UXの問題点を指摘し、改善案を提案" \
  --output examples/final/module-03-screenshot/ui-improvement.png
```

### チュートリアル生成
```bash
uv run python tools/capture_tutorial.py \
  --input data/screenshots/tutorial-recording/ \
  --output examples/final/module-03-screenshot/tutorial-steps/ \
  --format numbered
```

## 注釈の種類

### 1. マーキング
```
┌─────────────────────────────────────┐
│  赤枠: エラー・問題箇所             │
│  緑枠: 正解・推奨箇所               │
│  黄枠: 注意・警告箇所               │
│  青枠: 情報・補足説明               │
└─────────────────────────────────────┘
```

### 2. 矢印・線
```
→  指示・フロー方向
⟶  長い矢印（離れた要素間）
↺  循環・繰り返し
```

### 3. 番号・ラベル
```
①②③  手順番号
A B C  グループ分け
★☆   重要度
```

## 分析レポート形式（JSON）

```json
{
  "analysis_type": "error_diagnosis",
  "timestamp": "2025-02-03T12:00:00Z",
  "source_image": "error-screen.png",
  "findings": [
    {
      "type": "error",
      "location": {"x": 150, "y": 200, "width": 400, "height": 50},
      "description": "404 Not Found エラー",
      "cause": "リクエストされたURLが存在しない",
      "solution": "URLのスペルを確認、またはリダイレクト設定を確認"
    }
  ],
  "severity": "medium",
  "recommendations": [
    "カスタム404ページの実装",
    "壊れたリンクのチェック",
    "適切なリダイレクトの設定"
  ]
}
```

## プロンプトのコツ

### エラー診断
```markdown
# 良いプロンプト ✅
「このスクリーンショットを分析してください:
1. エラーメッセージの内容を特定
2. 考えられる原因を3つ挙げる
3. それぞれの解決方法を具体的に説明
4. エラー箇所を赤枠でマーキング」

# 悪いプロンプト ❌
「エラーを直して」
```

### UI分析
```markdown
# 良いプロンプト ✅
「このUIの問題点を分析:
- ボタンの配置と視認性
- フォントサイズと読みやすさ
- 色のコントラスト
- モバイル対応の観点
それぞれの改善案も提案してください」
```

## 期待される出力例

### エラー診断結果（画像に含まれる注釈）

```
┌─────────────────────────────────────────────────────────┐
│  ┌───────────────────────────────────────────────┐     │
│  │  404 Not Found                                │     │
│  │  The requested URL was not found.             │     │
│  └───────────────────────────────────────────────┘     │
│         ↑                                              │
│    ┌────┴────────────────────────────────────┐        │
│    │ 🔴 エラー: リクエストしたページが存在しません │        │
│    │                                          │        │
│    │ 原因:                                    │        │
│    │ • URLのスペルミス                         │        │
│    │ • ページが削除された                      │        │
│    │ • サーバー設定の問題                      │        │
│    │                                          │        │
│    │ 解決策:                                   │        │
│    │ 1. URLを確認して再入力                    │        │
│    │ 2. トップページから再度アクセス            │        │
│    │ 3. 管理者に連絡                          │        │
│    └──────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

## チェックリスト

- [ ] エラーの原因が正確に特定されている
- [ ] 解決策が具体的で実行可能
- [ ] 注釈が見やすく配置されている
- [ ] 色のコントラストが適切
- [ ] 重要な情報が強調されている

## 関連レッスン

- `/start-3-1`: スクショ分析基礎
- `/start-3-2`: エラー診断
- `/start-3-3`: UI分析
- `/start-3-4`: チュートリアル作成
- `/start-3-5`: バッチ処理
- `/start-3-6`: レポート生成

## 参考リンク

- [Gemini Vision API](https://ai.google.dev/gemini-api/docs/vision)
- [画像注釈のベストプラクティス](https://www.nngroup.com/articles/screenshots-software-tutorials/)

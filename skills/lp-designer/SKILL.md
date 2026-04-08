---
name: lp-designer
description: LP/HP作成ワークフロー。ヒアリング→訴求整理→WF→Pencilデザイン→HTML実装→Vercelデプロイの全フローをガイド。「LPを作って」「ランディングページ作成」「HPデザイン」「Webページ制作」で発動。
---

# LP/HP Designer - ランディングページ・ホームページ制作スキル

LP（ランディングページ）/ HP（ホームページ）をゼロから制作するための統合ワークフロースキル。
AskQuestionToolによるヒアリングからVercelデプロイまで、6つのフェーズで完結する。

## トリガーフレーズ

- 「LPを作って」「ランディングページを作成」
- 「HPを作りたい」「ホームページ制作」
- 「Webページを作って」「サイトを作りたい」
- 「Pencilでデザインして実装」

## 前提条件

- Cursor IDE で ai-agent-camp を開いていること
- Pencil MCP が有効（.pen ファイル操作用）
- Node.js 18+ がインストール済み（Vercelデプロイ用）
- Gemini API キーが設定済み（diagram-generator 用）

## ワークフロー概要

```
Phase 1: ヒアリング（AskQuestion）
    ↓ サービス概要・ターゲット・訴求軸
Phase 2: 訴求整理
    ↓ ペルソナ・ベネフィット・コピー
Phase 3: WF作成
    ↓ ASCII WF + ビジュアルWF
Phase 4: Pencilデザイン
    ↓ .pen デザインファイル
Phase 5: コード実装
    ↓ HTML/CSS(Tailwind)/JS
Phase 6: Vercelデプロイ
    ↓ 公開URL
```

---

## Phase 1: ヒアリング（AskQuestion）

最初にAskQuestionToolを使って、制作するLP/HPの要件を構造的に収集する。

### Step 1-1: プロジェクト種別の確認

```json
{
  "title": "LP/HP制作ヒアリング",
  "questions": [{
    "id": "project_type",
    "prompt": "どのタイプのページを作成しますか？",
    "options": [
      {"id": "lp", "label": "LP（ランディングページ）- 1つのCTAに集中"},
      {"id": "hp", "label": "HP（ホームページ）- 複数セクション・ナビ付き"},
      {"id": "product", "label": "プロダクトページ - 機能紹介中心"},
      {"id": "event", "label": "イベント/キャンペーンページ"}
    ]
  }]
}
```

### Step 1-2: サービス/プロダクト情報

```json
{
  "title": "サービス情報",
  "questions": [
    {
      "id": "service_category",
      "prompt": "サービスのカテゴリを選んでください",
      "options": [
        {"id": "saas", "label": "SaaS / Webサービス"},
        {"id": "ec", "label": "ECサイト / 物販"},
        {"id": "consulting", "label": "コンサルティング / 士業"},
        {"id": "education", "label": "教育 / スクール"},
        {"id": "event", "label": "イベント / セミナー"},
        {"id": "portfolio", "label": "ポートフォリオ / 個人"},
        {"id": "other", "label": "その他"}
      ]
    },
    {
      "id": "design_tone",
      "prompt": "デザインのトーンを選んでください",
      "options": [
        {"id": "professional", "label": "プロフェッショナル・信頼感"},
        {"id": "modern", "label": "モダン・スタイリッシュ"},
        {"id": "playful", "label": "ポップ・親しみやすい"},
        {"id": "luxury", "label": "高級感・エレガント"},
        {"id": "minimal", "label": "ミニマル・シンプル"},
        {"id": "tech", "label": "テック・先進的"}
      ]
    }
  ]
}
```

### Step 1-3: 追加ヒアリング（自由入力）

AskQuestion の後、以下を自由入力で確認する:

- **サービス名**: 正式名称
- **キャッチコピー案**: あれば（なければ生成）
- **ターゲット**: 誰に向けたページか
- **主な訴求ポイント**: 3つ程度
- **参考サイト**: あればURL
- **CTAの目的**: 問い合わせ / 申し込み / 資料請求 / 購入 など

---

## Phase 2: 訴求整理

Phase 1 のヒアリング結果をもとに、以下のドキュメントを生成する。

### 出力: `output/lp-brief.md`

```markdown
# LP ブリーフ

## ペルソナ
- 名前: {例: 田中太郎}
- 年齢: {例: 35歳}
- 職種: {例: マーケティングマネージャー}
- 課題: {例: LP制作に時間がかかりすぎる}

## 訴求軸（ベネフィット3点）
1. {メインベネフィット}
2. {サブベネフィット1}
3. {サブベネフィット2}

## コピー
- ヘッドライン: {例: AIで、LP制作を10倍速く}
- サブヘッドライン: {例: ヒアリングからデプロイまで、すべてをAIがサポート}
- CTA文言: {例: 無料で始める}

## セクション構成
1. Hero（ヘッドライン + CTA）
2. Pain Points（課題提起）
3. Solution（ソリューション紹介）
4. Features（機能 / 特徴 3-4点）
5. Social Proof（実績 / お客様の声）
6. Pricing / Plan（料金・プラン）※オプション
7. FAQ（よくある質問）
8. Final CTA（最終アクション）
```

---

## Phase 3: WF（ワイヤーフレーム）作成

### Step 3-1: ASCII ワイヤーフレーム

テキストベースで各セクションの構造を設計する:

```
┌─────────────────────────────────┐
│           HEADER / NAV          │
├─────────────────────────────────┤
│                                 │
│     [Hero Image / Video]        │
│                                 │
│     ヘッドライン（H1）            │
│     サブヘッドライン              │
│     [ CTA ボタン ]              │
│                                 │
├─────────────────────────────────┤
│     Pain Points セクション       │
│   ┌─────┐ ┌─────┐ ┌─────┐     │
│   │課題1│ │課題2│ │課題3│     │
│   └─────┘ └─────┘ └─────┘     │
├─────────────────────────────────┤
│     Solution セクション          │
│   [画像]  説明テキスト           │
├─────────────────────────────────┤
│     Features セクション          │
│   ┌──────┐ ┌──────┐            │
│   │機能1 │ │機能2 │            │
│   └──────┘ └──────┘            │
│   ┌──────┐ ┌──────┐            │
│   │機能3 │ │機能4 │            │
│   └──────┘ └──────┘            │
├─────────────────────────────────┤
│     Social Proof                │
│     ★★★★★ お客様の声           │
├─────────────────────────────────┤
│     FAQ                         │
│     Q1 / A1                     │
│     Q2 / A2                     │
├─────────────────────────────────┤
│     Final CTA                   │
│     [ CTA ボタン ]              │
├─────────────────────────────────┤
│           FOOTER                │
└─────────────────────────────────┘
```

### Step 3-2: ビジュアルWF生成

diagram-generator を使ってビジュアルワイヤーフレームを生成:

```bash
uv run python tools/generate_diagram.py --topic "LP wireframe: {セクション構成}" --style minimalist
```

出力先: `output/images/lp-wireframe.png`

---

## Phase 4: Pencilデザイン

Pencil MCP を使って .pen デザインファイルを作成する。
.pen ファイルは暗号化されているため、Read/Grep ではなく必ず Pencil MCP ツールを使うこと。

### Step 4-0: Pencil エディターを開く

まず現在のエディター状態を確認する。ファイルが開いていなければ新規作成する。

```
# 1) エディター状態を確認
CallMcpTool: user-pencil / get_editor_state
  arguments: {}

# → ファイルが開いていない場合エラーが返る
# → 既にファイルが開いている場合はノード一覧が返る

# 2-A) 新規ドキュメントを作成する場合
CallMcpTool: user-pencil / open_document
  arguments: { "filePathOrTemplate": "new" }

# 2-B) 既存の .pen ファイルを開く場合
CallMcpTool: user-pencil / open_document
  arguments: { "filePathOrTemplate": "path/to/design.pen" }

# 3) 開いた後、再度 get_editor_state でノード構造を確認
CallMcpTool: user-pencil / get_editor_state
  arguments: {}
```

**重要**: `open_document` は Pencil アプリ内で対象ファイルを開く操作。
Cursor の MCP 設定で `user-pencil` が有効になっている必要がある。

### Step 4-1: LPデザインガイドライン取得

LP 特化のデザインルール（セクション構成、ヒーロー設計、フッター設計等）を取得する:

```
CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "landing-page" }
```

このガイドラインには以下が含まれる:
- SaaS/LP の推奨セクション構成（Hero → Features → Social Proof → Pricing → FAQ → CTA → Footer）
- ヒーローセクションのベストプラクティス
- コンテンツ→ビジュアルの順序原則
- batch_design でのページコンテナ作成例

### Step 4-2: スタイルガイド取得

デザインのトーンに合ったスタイルガイドを取得する:

```
# 1) 使えるタグ一覧を確認
CallMcpTool: user-pencil / get_style_guide_tags
  arguments: {}

# → minimal, modern, clean, warm, tech, brutalist 等のタグが返る

# 2) ヒアリング結果のトーンに合うタグを選択して取得
CallMcpTool: user-pencil / get_style_guide
  arguments: { "tags": ["minimal", "clean", "whitespace", "website"] }
```

スタイルガイドには以下が含まれる:
- カラーシステム（背景色、テキスト色、アクセント色）
- タイポグラフィ（フォント、サイズ、ウェイト）
- スペーシング・角丸・シャドウの設定値
- コンポーネントパターン（ボタン、カード、ナビ等）

### Step 4-3: ページコンテナ作成

LP全体を包むフレームを `batch_design` で作成する:

```
# batch_design の operations はスクリプト形式で記述
CallMcpTool: user-pencil / batch_design
  arguments: {
    "operations": "page=I(document, {type: \"frame\", name: \"Landing Page\", placeholder: true, layout: \"vertical\", width: 1440, height: \"fit_content(4000)\", fill: \"#FFFFFF\", clip: true})"
  }
```

**batch_design 操作の基本構文:**

| 操作 | 構文 | 説明 |
|------|------|------|
| Insert | `foo=I("parentId", {...})` | 親ノードに子を挿入 |
| Copy | `bar=C("nodeId", "parentId", {...})` | ノードをコピー |
| Update | `U("nodeId", {...})` | プロパティ更新 |
| Replace | `R("nodeId", {...})` | ノードを置換 |
| Delete | `D("nodeId")` | ノード削除 |
| Move | `M("nodeId", "parentId", index)` | ノード移動 |
| Image | `G("nodeId", "ai", "prompt")` | AI画像生成 |

**重要ルール:**
- `placeholder: true` を作業中のフレームに必ず設定し、完了時に `false` にする
- テキストには必ず `fill` を設定する（デフォルトは透明で見えない）
- 1回の batch_design は最大 25 操作まで
- flexbox の子要素では `x`, `y` は無視される（`fill_container` / `fit_content` を使う）
- 画像ノード型は存在しない。フレームに `G()` で画像を適用する

### Step 4-4: セクションを順に作成

`batch_design` を使い、以下のセクションを1〜2セクションずつ作成する:

1. **Header**: ロゴ + ナビリンク + CTAボタン（横配置 `space_between`）
2. **Hero セクション**: バッジ、ヘッドライン、サブヘッドライン、CTAボタン（中央揃え）
3. **Features**: セクションヘッダー + 3カラムのカード（アイコン + タイトル + 説明）
4. **How It Works**: 番号付きの3ステップ（丸数字 + タイトル + 説明）
5. **Stats/Social Proof**: ダーク背景の実績数字 + 顧客の声カード
6. **Final CTA**: アクセントカラー背景 + ヘッドライン + CTAボタン
7. **Footer**: ダーク背景 + リンクカラム + コピーライト

各セクションの作成例（Hero）:

```
CallMcpTool: user-pencil / batch_design
  arguments: {
    "operations": "hero=I(\"pageId\", {type: \"frame\", name: \"Hero\", layout: \"vertical\", width: \"fill_container\", height: \"fit_content(600)\", padding: [100, 120], gap: 32, alignItems: \"center\", fill: \"#FFFFFF\"})\nheadline=I(hero, {type: \"text\", content: \"メインコピー\", fontFamily: \"Outfit\", fontSize: 56, fontWeight: \"700\", fill: \"#1A1918\", letterSpacing: -1, textAlign: \"center\", lineHeight: 1.2, textGrowth: \"fixed-width\", width: 800})\nsubline=I(hero, {type: \"text\", content: \"サブコピーの説明文\", fontFamily: \"Outfit\", fontSize: 18, fill: \"#6D6C6A\", textAlign: \"center\"})"
  }
```

### Step 4-5: デザイン確認・微調整

各セクション追加後にスクリーンショットで視覚確認する:

```
# ページ全体を確認
CallMcpTool: user-pencil / get_screenshot
  arguments: { "nodeId": "pageId" }

# 特定セクションを拡大確認
CallMcpTool: user-pencil / get_screenshot
  arguments: { "nodeId": "heroId" }

# レイアウト構造を数値で確認（位置ズレの検出に有効）
CallMcpTool: user-pencil / snapshot_layout
  arguments: { "parentId": "pageId", "maxDepth": 3 }
```

問題があれば `batch_design` の `U()` で修正する。
すべてのセクションが完成したら、placeholder を解除する:

```
CallMcpTool: user-pencil / batch_design
  arguments: { "operations": "U(\"pageId\", {placeholder: false})" }
```

---

## Phase 5: コード実装

Pencilデザインを実際に動くHTML/CSS/JSに変換する。

### Step 5-1: コード化ガイドライン取得

```
CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "code" }

CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "tailwind" }
```

### Step 5-2: プロジェクト構造

```
lp-project/
├── index.html          # メインHTML
├── css/
│   └── style.css       # カスタムCSS（Tailwind CDN使用）
├── js/
│   └── main.js         # インタラクション
├── images/             # 画像アセット
└── package.json        # Vercelデプロイ用
```

### Step 5-3: 実装のポイント

- **Tailwind CSS CDN**: `<script src="https://cdn.tailwindcss.com"></script>` で即座に利用
- **レスポンシブ**: モバイルファーストで実装（sm: / md: / lg: ブレークポイント）
- **アニメーション**: スクロールで要素がフェードインする Intersection Observer
- **フォーム**: Formspree や Netlify Forms 等の外部サービス連携

### Step 5-4: ブラウザ確認

cursor-ide-browser MCP を使って表示確認:

```
CallMcpTool: cursor-ide-browser / browser_navigate
  arguments: { "url": "file:///path/to/lp-project/index.html" }
```

---

## Phase 6: Vercelデプロイ

### Step 6-1: Vercel CLI インストール

```bash
npm i -g vercel
```

### Step 6-2: プレビューデプロイ

```bash
vercel lp-project
```

初回はログイン・プロジェクト設定が求められる。

### Step 6-3: 本番デプロイ

```bash
vercel --prod
```

### Step 6-4: カスタムドメイン（オプション）

```bash
vercel domains add your-domain.com
```

---

## 3段階の体験

このスキルは3つのレベルで活用できる:

### Stage 1: テキストベースLP（初級）
- AskQuestion でヒアリング
- ASCII WF で構造設計
- HTML/CSS を直接生成（Pencilなし）
- ローカルで確認

### Stage 2: HP制作（中級）
- 複数ページ構成（トップ + サブページ）
- ナビゲーション実装
- diagram-generator でビジュアルWF
- レスポンシブ対応

### Stage 3: Pencilデザイン → LP（上級）
- Pencil MCP でプロのデザイン作成
- デザイン→コード変換
- アニメーション・インタラクション
- Vercelデプロイで公開

---

## 関連スキル

- **diagram-generator**: WF・構造図の生成
- **nanobanana**: Hero画像・OGP画像の生成
- **banner-creator**: SNS告知用バナー作成
- **screenshot-annotator**: デザインレビュー用注釈追加

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "30分"
category: "lesson"
prerequisites: ["start-18-11", "output/pm/wireframes.md"]
level: "intermediate"
tags: ["pm", "ui", "design", "pencil-mcp"]
---

# 🎓 Lesson 18-12: UIデザイン（Pencil MCP）

| 項目 | 内容 |
|------|------|
| ゴール | Pencil MCPを使ってTaskFlowの主要画面（ダッシュボード、タスク一覧、タスク詳細）をデザインする |
| 所要時間 | 約30分 |
| 使うスキル | Pencil MCP |
| 前提条件 | Lesson 18-11 完了、output/pm/wireframes.md が存在する。Pencil MCPがCursorに接続済み |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

> **💡 ツール情報**: このレッスンでは Pencil MCP を使用します。現在のワークスペース、Claude Code（CLI/デスクトップ）のいずれでも利用可能です。Codex CLI 等の一部環境では `request_user_input is not supported` エラーが出る場合があります。その場合は「代替ワークフロー」セクションを参照してください。

## 📍 Step 1: デザインシステムの定義

まず Pencil MCP でデザインファイルをプロジェクト内に作成します:
```bash
mkdir -p output/pm/ui-design
open_document("output/pm/ui-design/taskflow-ui.pen")
```
> **保存先**: `output/pm/ui-design/taskflow-ui.pen`

デザインの基本となるカラーパレット、タイポグラフィ、スペーシング、シャドウスタイルを定義します。これらはすべての画面で統一的に使用される要素です。

```json
{
  "type": "AskQuestion",
  "question": "TaskFlowのデザイントーンを選んでください",
  "options": [
    {
      "label": "プロフェッショナル（青系）",
      "value": "professional",
      "description": "ビジネス向け。信頼感と安定感を重視。主色：青（#0066CC）、副色：グレー"
    },
    {
      "label": "モダン（紫系）",
      "value": "modern",
      "description": "先進的で洗練。イノベーション感を重視。主色：紫（#7C3AED）、副色：インディゴ"
    },
    {
      "label": "フレンドリー（緑系）",
      "value": "friendly",
      "description": "親しみやすく穏やか。ユーザー親和性を重視。主色：緑（#10B981）、副色：エメラルド"
    },
    {
      "label": "カスタム",
      "value": "custom",
      "description": "独自のカラーパレットを指定"
    }
  ],
  "required": true,
  "hint": "デザインの全体トーンを決めるため、プロジェクトのポジショニングに合わせて選択してください"
}
```

### 🚀 デザインシステム定義タスク

選択したトーンに基づいて、以下の要素を定義します：

#### カラーパレット
- **Primary Color**: メインアクション、重要要素に使用
- **Secondary Color**: サポート要素、予備的アクションに使用
- **Accent Color**: 警告、成功、情報など状態表現に使用
- **Background Colors**: メイン背景、サブ背景（コンテナ用）
- **Text Colors**: 本文、見出し、補足テキスト

#### タイポグラフィ
- **見出し**: フォントサイズ 28px/24px/20px、ウェイト Bold/SemiBold
- **本文**: フォントサイズ 16px/14px、ウェイト Regular
- **補足**: フォントサイズ 12px、ウェイト Regular、opacity 70%
- **推奨フォント**: Inter, Segoe UI, または SF Pro Display

#### スペーシング規則
- **基本単位**: 4px
- **一般間隔**: 8px, 12px, 16px, 24px, 32px
- **コンポーネント内**: 12px 〜 16px
- **セクション間**: 24px 〜 32px
- **ページマージン**: 16px（モバイル）/ 24px（デスクトップ）

#### ボーダーと角丸
- **Border Radius**: 4px（小）/ 8px（中）/ 16px（大）
- **Border Color**: neutral-200 / neutral-300
- **Border Width**: 1px 標準

#### シャドウスタイル
- **Soft Shadow**: `0 1px 3px rgba(0,0,0,0.1)`
- **Medium Shadow**: `0 4px 12px rgba(0,0,0,0.15)`
- **Elevated Shadow**: `0 10px 30px rgba(0,0,0,0.2)`

---

## 📍 Step 2: ダッシュボード画面のデザイン

TaskFlowのメイン画面となるダッシュボードをデザインします。ユーザーが最初に目にする画面として、直感的で情報構造が明確である必要があります。

```json
{
  "type": "AskQuestion",
  "question": "ダッシュボードのレイアウトを選んでください",
  "options": [
    {
      "label": "カード型（統計+タスク一覧）",
      "value": "card_layout",
      "description": "統計カード + タスクリスト。バランス型で最も一般的"
    },
    {
      "label": "カンバン型（ステータス列）",
      "value": "kanban_layout",
      "description": "タスクをステータス別の列で表示。ビジュアルで進捗管理が容易"
    },
    {
      "label": "タイムライン型",
      "value": "timeline_layout",
      "description": "時系列でタスクを表示。スケジュール管理向け"
    },
    {
      "label": "AIに提案してもらう",
      "value": "ai_suggest",
      "description": "プロジェクト規模と用途から最適レイアウトを提案"
    }
  ],
  "required": true,
  "hint": "プロジェクトのタスク数と管理スタイルを考慮して選択してください"
}
```

### 🚀 ダッシュボードのデザイン要素

#### ヘッダーエリア（Height: 56px / 64px）
- ロゴ/ブランド名（左）
- ページタイトル「ダッシュボード」
- ユーザーメニュー/通知（右）
- デバイス対応: スマートフォンでは縮小表示

#### サイドバー（Width: 256px / 200px）
- ナビゲーションメニュー
  - ダッシュボード（現在地）
  - タスク一覧
  - プロジェクト
  - チーム
  - 設定
- 折りたたみ機能（モバイル対応）

#### メインコンテンツエリア
**統計カード群（グリッド: 4列 → 2列 → 1列）**
- 今日のタスク：🎯 数値 + バー
- 完了率：📊 パーセンテージ + サークルプログレス
- 期限切れタスク：⚠️ 数値 + 警告色
- チームアクティビティ：👥 活動数

**「今日のタスク」セクション（Height: 320px）**
- フィルター/ソートコントロール（上部）
- タスクリスト（スクロール可能）
  - 優先度インジケーター
  - タスクタイトル
  - 担当者アバター
  - 期限表示
  - ステータスバッジ
- 「すべてを見る」ボタン

**最近のアクティビティセクション（Height: 240px）**
- タイムラインビュー
- アクティビティアイテム
  - アクション種別アイコン
  - 実行者情報
  - タイムスタンプ（相対時間）

---

## 📍 Step 3: タスク一覧/詳細画面のデザイン

タスク管理の中核となる画面をデザインします。大量のタスク情報を効率的に表示し、ユーザーが必要な情報に素早くアクセスできる必要があります。

```json
{
  "type": "AskQuestion",
  "question": "タスク一覧の表示形式を選んでください",
  "options": [
    {
      "label": "テーブル型",
      "value": "table_view",
      "description": "表形式。多くのカラム情報を一度に表示。大量データ向け"
    },
    {
      "label": "カード型",
      "value": "card_view",
      "description": "カード形式。タスク情報を視覚的に。情報量は限定的"
    },
    {
      "label": "カンバン型",
      "value": "kanban_view",
      "description": "ステータス別の列。ドラッグアンドドロップで状態変更可能"
    },
    {
      "label": "リスト+カード切替",
      "value": "hybrid_view",
      "description": "リストビューと詳細パネルを並行表示。柔軟で高機能"
    }
  ],
  "required": true,
  "hint": "ユーザーがタスクをどのように管理したいかを考えて選択してください"
}
```

### 🚀 タスク一覧画面のデザイン

#### 上部操作バー（Height: 56px）
- タイトル「タスク一覧」
- 検索ボックス
  - プレースホルダー: "タスク検索"
  - 検索アイコン
- フィルターボタン
  - ステータス
  - 優先度
  - 担当者
  - 期限
- ソートメニュー
  - 日付（新しい順・古い順）
  - 優先度
  - 名前（A-Z）
- 新規作成ボタン（Primary Button）

#### フィルター・ソートパネル（展開時）
- タブ: フィルター / ソート
- チェックボックスリスト
- リセットボタン
- 適用ボタン

#### タスクリスト要素（選択した形式に応じて）

**テーブル型の場合:**
- カラムヘッダー: ☑️ | タスク名 | 優先度 | 担当者 | 期限 | ステータス | アクション
- 行高: 48px
- ホバー効果: 背景色変更 + アクションメニュー表示
- 選択機能: チェックボックス
- ソート可能なカラムに↑↓アイコン

**カード型の場合:**
- グリッドレイアウト（3列 → 2列 → 1列）
- カード内容:
  - タスク名（太字）
  - 説明（1-2行）
  - タグ/ラベル
  - 優先度バッジ
  - 担当者アバター
  - 期限日時
  - ステータスバッジ
  - ホバー時: クイックアクション（編集・削除・共有）

**カンバン型の場合:**
- ステータスカラム（未割り当て / 予定 / 進行中 / レビュー / 完了）
- 各カラムヘッダー: ステータス名 + タスク数
- ドラッグアンドドロップ領域
- カード表示（カード型と同じ）
- 「新規追加」ボタン（カラム下部）

**リスト+カード切替の場合:**
- 左パネル: タスクリスト（狭い表示）
- 右パネル: 選択タスクの詳細表示
- リサイザー（パネル幅調整）
- 左パネルのアイテム選択でリアルタイム更新

#### ページネーション（底部）
- ページ情報表示（例: 1-25 of 127）
- ページ数選択
- 前へ / 次へ ボタン

---

### 📍 タスク詳細画面のデザイン

#### レイアウト
- **フルページ表示**: ブラウザ全体を使用（大画面）
- **モーダル/サイドパネル**: 既存リストの上に表示（小〜中画面）

#### ヘッダーセクション（Height: 72px）
- タスク名（編集可能）
- 優先度バッジ
- ステータスドロップダウン
- 「×」閉じるボタン / 戻るボタン

#### メインコンテンツ（スクロール可能）

**基本情報セクション**
- タスク名
- 説明/メモ（マークダウン対応）
- 優先度セレクター
- ステータス
- 割り当て先
- 期限日時

**詳細情報セクション**
- プロジェクト
- ラベル/タグ
- 推定工数
- 完了率
- 親タスク（ある場合）
- 関連タスク

**添付ファイルセクション**
- アップロードエリア
- ファイル一覧

**アクティビティ/コメントセクション**
- タイムラインビュー
- コメント入力フィールド
- 既存コメント表示

#### サイドバー（右側）
- チェックリスト（サブタスク）
- アサイニー情報
- タイムトラッキング
- 関連リンク

#### 下部アクションバー
- 削除ボタン
- キャンセルボタン
- 保存ボタン（Primary）

---

## 📍 Step 4: デザインレビュー

作成したデザインが要件を満たし、高品質であることを確認します。

```json
{
  "type": "AskQuestion",
  "question": "デザインレビューの観点を選んでください",
  "options": [
    {
      "label": "UIの一貫性",
      "value": "consistency",
      "description": "カラー、タイポグラフィ、コンポーネント形状の統一性を確認"
    },
    {
      "label": "アクセシビリティ",
      "value": "accessibility",
      "description": "色覚異常対応、コントラスト比、キーボード操作を確認"
    },
    {
      "label": "ユーザビリティ",
      "value": "usability",
      "description": "操作のしやすさ、情報探索性、タスクフロー効率を確認"
    },
    {
      "label": "すべて",
      "value": "all",
      "description": "上記3つの観点をすべて確認（最も推奨）"
    }
  ],
  "required": true,
  "hint": "完成度を高めるため『すべて』の選択を推奨します"
}
```

### 🚀 UIの一貫性チェックリスト

- [ ] カラーパレットが全画面で統一されている
  - Primary Color の使用箇所（ボタン、強調要素）
  - Secondary Color の使用箇所（背景、補助要素）
  - 警告/エラー/成功の色が標準化されている
- [ ] フォント指定が統一されている
  - 見出しは常にBold/SemiBold
  - 本文は常にRegular
  - サイズが標準の 28/24/20/16/14/12px を使用
- [ ] 間隔（マージン/パディング）が 4px の倍数
  - コンポーネント内: 12px / 16px
  - セクション間: 24px / 32px
- [ ] コンポーネント形状が統一されている
  - ボタン: 同じ高さ（44px / 40px）、同じ角丸（8px）
  - カード: 同じ角丸（8px）、同じシャドウ
  - 入力フィールド: 同じ高さ（40px）、同じ枠線スタイル
- [ ] アイコンが統一されている
  - 同じアイコンセット（Material Icons / Heroicons など）
  - 同じサイズ（16px / 20px / 24px）
  - 同じストロークウェイト

### ⚠️ アクセシビリティチェックリスト

- [ ] コントラスト比が WCAG AA 基準を満たす
  - テキスト: 最小 4.5:1（通常テキスト）/ 3:1（大きいテキスト）
  - グラフィック要素: 最小 3:1
  - 特に背景色とテキスト色の組み合わせを確認
- [ ] 色だけで情報を伝えていない
  - 優先度: 色 + アイコン + テキスト
  - ステータス: 色 + バッジ + ラベル
  - エラー: 色 + アイコン + メッセージテキスト
- [ ] フォーカス状態が明確である
  - ボタンのホバー/フォーカス状態が視認可能
  - フォーカスインジケーターが明確（アウトラインなど）
- [ ] テキストサイズが十分である
  - 本文: 最小 14px
  - キャプション: 最小 12px（ただし避けるべき）
- [ ] インタラクティブ要素のターゲットサイズが十分
  - ボタン: 最小 44px × 44px（タッチターゲット）
  - リンク: 最小 16px 高さ

### ✅ ユーザビリティチェックリスト

- [ ] 主要なユーザータスクが効率的に実行できる
  - タスク検索: 3クリック以内
  - タスク作成: 4ステップ以内
  - タスク編集: 直接インライン編集可能
  - ステータス変更: ワンクリック（カンバン）
- [ ] 情報階層が明確である
  - 最重要情報（タスク名、ステータス）が目に入りやすい
  - セカンダリ情報（期限、担当者）は適切な大きさ
  - 補足情報（作成日時など）は目立たない
- [ ] アクション（ボタン）の配置が論理的
  - Primary アクション（保存・作成）は右下または目立つ位置
  - Destructive アクション（削除）は警告色 + 確認ダイアログ
  - Secondary アクション（キャンセル）は左側
- [ ] エラーハンドリングが明確である
  - バリデーションエラーは入力フィールド直下に表示
  - エラーメッセージは具体的で解決策を含む
  - 色 + アイコン + テキストで表現
- [ ] 応答性フィードバックが即座である
  - ボタンクリック: ビジュアル変化（色、アニメーション）
  - データ送信: ローディング状態表示
  - エラー: 警告表示（300ms 以内）
- [ ] ワイヤーフレームとの整合性
  - ダッシュボード構成が wireframes.md と一致している
  - タスク一覧のレイアウトが仕様を満たしている
  - 必須要素（フィルター、検索など）がすべて含まれている

---

## ✅ 成果物

このレッスンで作成するファイルと形式：

### .pen ファイル（Pencil MCP で管理）
- `dashboard.pen` - ダッシュボード画面デザイン
- `task-list.pen` - タスク一覧画面デザイン
- `task-detail.pen` - タスク詳細画面デザイン
- `design-system.pen` - デザインシステム（カラー、タイポグラフィ、コンポーネント）

### ドキュメント（参考用）
- `output/pm/design-system.md` - デザインシステム仕様書
  - カラーパレット定義（HEX/RGB コード）
  - タイポグラフィ規則
  - スペーシング規則
  - コンポーネント設計仕様
  - アクセシビリティガイドライン

---

## 🚀 実装手順

### 1. Pencil MCP の接続確認
```bash
cursor /pencil status
```
- Status: Connected
- Version: 1.0+

### 2. デザインシステムの作成
```bash
cursor /pencil create-system \
  --name "TaskFlow" \
  --primary "#0066CC" \
  --secondary "#F3F4F6" \
  --accent "#EF4444"
```

### 3. 各画面デザインの作成
- ダッシュボード: `/pencil design-screen dashboard --layout card_layout`
- タスク一覧: `/pencil design-screen task-list --layout table_view`
- タスク詳細: `/pencil design-screen task-detail --layout full-page`

### 4. コンポーネント設計（再利用可能要素）
- Button（Primary / Secondary / Danger）
- Input Field
- Card
- Badge
- Avatar
- Dialog / Modal
- Dropdown
- Tabs

### 5. エクスポート
```bash
cursor /pencil export --format png --output output/pm/designs/
cursor /pencil export --format figma --output output/pm/designs/figma-link
```

---

## 🔄 代替ワークフロー（非GUI環境向け）

Pencil MCP が利用できない環境（Claude Code、Codex CLI、SSH等）では、HTML + Tailwind CSS で直接 UI モックアップを作成します。

1. `output/pm/wireframes.md` を参照してデザイン要件を確認
2. Step 1 のデザインシステム定義は `output/pm/design-system.md` に Markdown で記述
3. 各画面（ダッシュボード、タスク一覧、タスク詳細）を HTML + Tailwind CSS CDN で実装:
   ```bash
   mkdir -p output/pm/designs
   ```
4. `output/pm/designs/dashboard.html`、`task-list.html`、`task-detail.html` を作成
5. Playwright でスクリーンショットを取得し PNG として保存:
   ```bash
   npx playwright screenshot output/pm/designs/dashboard.html output/pm/designs/dashboard.png
   ```
6. Step 4 のデザインレビューチェックリストはそのまま適用可能

> .pen ファイルの代わりに HTML ファイルが成果物となります。Lesson 18-13 へはそのまま進めます。

---

## ⚠️ よくあるトラブルシューティング

### Pencil MCP が接続されていない
**原因**: Cursor の拡張機能がロードされていない

**解決策**:
1. Cursor 設定で MCP を確認: Settings > Extensions > Pencil MCP
2. 再起動: `cursor restart`
3. 接続テスト: `cursor /pencil status`

### デザインの修正方法がわからない
**参考手順**:
1. Pencil で該当コンポーネントを右クリック
2. 「Edit」を選択
3. プロパティパネルで色/サイズ/配置を調整
4. プレビューで確認
5. Save（Ctrl+S）

### カラーパレットの選び方
**判断基準**:
- **プロフェッショナル**: B2B/エンタープライズ向け、金融系、ビジネス管理ツール
- **モダン**: SaaS、スタートアップ、イノベーション重視
- **フレンドリー**: コンシューマー向け、学習/教育、ヘルスケア
- **カスタム**: 既存ブランドカラーがある場合

### ワイヤーフレームとの差異
**確認ポイント**:
- `output/pm/wireframes.md` を開く
- 各セクションのレイアウトがデザインと一致しているか確認
- 不一致がある場合は、ワイヤーフレームを優先して修正

### コンポーネントの再利用
**推奨方法**:
1. Pencil で「Library」を開く
2. 作成済みコンポーネント（ボタン、カードなど）をドラッグ
3. 複数の画面で同じコンポーネントを使用
4. コンポーネント更新時に全画面が自動更新される

---

## 📍 チェックポイント

以下を完了したら、このレッスンは完了です：

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "title": "デザインシステム定義済み",
      "description": "カラーパレット、タイポグラフィ、スペーシング規則が .pen に保存されている",
      "verification": "cursor /pencil list-components | grep 'design-system'"
    },
    {
      "title": "ダッシュボード画面デザイン完了",
      "description": "ヘッダー、サイドバー、統計カード、タスクリスト、アクティビティセクションが含まれている",
      "verification": "ls output/pm/designs/dashboard.png"
    },
    {
      "title": "タスク一覧画面デザイン完了",
      "description": "フィルター、ソート、タスク表示（選択形式）、ページネーションが含まれている",
      "verification": "ls output/pm/designs/task-list.png"
    },
    {
      "title": "タスク詳細画面デザイン完了",
      "description": "タスク情報、アクティビティ/コメント、サイドバー、アクションが含まれている",
      "verification": "ls output/pm/designs/task-detail.png"
    },
    {
      "title": ".pen ファイル保存済み",
      "description": "dashboard.pen, task-list.pen, task-detail.pen, design-system.pen がすべて Pencil MCP に保存されている",
      "verification": "cursor /pencil list-files | wc -l >= 4"
    }
  ]
}
```


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/ui-design/
├── taskflow-ui.pen       ← Pencil デザインファイル（本体）
├── dashboard.png         ← ダッシュボード画面のスクリーンショット
├── task-list.png         ← タスク一覧画面のスクリーンショット
└── task-detail.png       ← タスク詳細画面のスクリーンショット
```

### 確認コマンド
```bash
# .pen ファイルとスクリーンショットの確認
ls -lh output/pm/ui-design/

# 画像を開く（macOS: open / Linux: xdg-open）
open output/pm/ui-design/
```

> 💡 **Claude Code**: `Read output/pm/ui-design/dashboard.png` でチャット内プレビュー
> 💡 **Cursor**: ファイルエクスプローラーで画像をクリックしてプレビュー
> 💡 **.pen ファイル**: Pencil MCP の `batch_get` や `get_screenshot` で中身を確認できます

---

## ➡️ 次のステップ

このレッスンを完了したら、**Lesson 18-13: HTML + Tailwind CSS プロトタイプ**に進みます。

Pencil MCP で作成したデザインを元に、実際のコードに変換します：

- HTML 構造の作成
- Tailwind CSS による スタイリング
- レスポンシブ対応（モバイル / タブレット / デスクトップ）
- インタラクション実装（ホバー、クリック、アニメーション）

**開始**: `cursor /lesson start-18-13`

---

## 📚 参考資料

- [Pencil MCP ドキュメント](https://pencil.dev/docs)
- [デザインシステム ベストプラクティス](https://www.designsystems.com/)
- [WCAG 2.1 アクセシビリティガイドライン](https://www.w3.org/WAI/WCAG21/quickref/)
- [Tailwind CSS コンポーネント集](https://tailwindui.com/)
- [Material Design 3 ガイドライン](https://m3.material.io/)

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "25分"
category: "lesson"
prerequisites: ["start-18-10", "output/pm/wbs.md", "output/pm/requirements-spec.md"]
level: "intermediate"
tags: ["pm", "notion", "tracker", "collaboration"]
---

# 🎓 Lesson 18-11: Notion連携

| 項目 | 内容 |
|------|------|
| ゴール | Notionに要件トラッカーDBを作成し、TaskFlowの要件をデータベース管理する |
| 所要時間 | 約25分 |
| 使うスキル | notion-db スキル |
| 前提条件 | Lesson 18-10 完了、output/pm/requirements-spec.md が存在する。Notion APIキーが設定済み |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

---

## 📍 Step 1: Notion API接続の確認

### 🚀 実施内容

Notion APIの接続状況を確認し、必要に応じてAPIキーを設定します。

```json
{
  "type": "AskQuestion",
  "question": "Notion APIの準備はどのような状況ですか？",
  "options": [
    {
      "label": "設定済み",
      "value": "ready",
      "description": "Notion APIキーが環境変数に設定されています"
    },
    {
      "label": "これから設定する",
      "value": "setup_now",
      "description": "APIキーを今から取得・設定します"
    },
    {
      "label": "Notion連携をスキップしたい",
      "value": "skip",
      "description": "マークダウンベースのトラッカーで代替します"
    },
    {
      "label": "トラブルがある",
      "value": "troubleshoot",
      "description": "接続設定に問題があります"
    }
  ],
  "conditional": {
    "setup_now": "🔧 Notion API キーの取得方法\n\n1. Notion公式サイト（https://www.notion.so）にログイン\n2. Settings → Developer → My integrations → New integration\n3. Name: 'TaskFlow PM Tracker' と入力\n4. Capabilities: Read content, Update content, Insert content を選択\n5. Associated workspace: 対象ワークスペースを選択\n6. Show API key をクリック\n7. 以下を環境変数に設定:\n   - NOTION_API_KEY=YOUR_NOTION_SECRET_HERE\n   - NOTION_DATABASE_ID=xxxxxxxx... (DBを作成後に設定)",
    "skip": "✅ Notionをスキップする場合\n\n以下の代替案を使用します:\n- マークダウン形式の要件トラッカー\n- タイプ: output/pm/requirement-tracker.md\n- 手動更新が必要\n\nただし、このレッスンのチェックポイントは実装されません。",
    "troubleshoot": "⚠️ トラブルシューティング\n\n【エラー】\"NOTION_API_KEY not found\"\n→ 環境変数が未設定です。上記のAPI キー取得方法を参照してください。\n\n【エラー】\"Unauthorized\"\n→ APIキーが正しいか確認してください。show API key から再度取得してください。\n\n【エラー】\"Rate limit exceeded\"\n→ 15秒待機してから再度実行してください。\n\n詳細は docs/setup-guides/ を参照"
  }
}
```

### ⚠️ 確認項目

- [ ] Notion APIキーが環境変数に設定されている
- [ ] Notion APIキーが有効か確認済み
- [ ] 対象ワークスペースの権限がある
- [ ] Node.js環境でAPIライブラリがインストール可能

---

## 📍 Step 2: 要件トラッカーDBの作成

### 🚀 実施内容

Notionに要件管理用のデータベースを作成します。カラム構成を選択してください。

```json
{
  "type": "AskQuestion",
  "question": "トラッカーのカラム構成を選んでください",
  "options": [
    {
      "label": "シンプル（5カラム）",
      "value": "simple",
      "description": "基本情報のみ: ID / 名前 / カテゴリ / ステータス / 優先度"
    },
    {
      "label": "標準（8カラム）",
      "value": "standard",
      "description": "シンプル + 担当者 / 関連ユースケース / 備考"
    },
    {
      "label": "詳細（12カラム）",
      "value": "detailed",
      "description": "標準 + テストケースID / 完了予定日 / 関連ドキュメント / 技術スタック"
    },
    {
      "label": "カスタム",
      "value": "custom",
      "description": "自由にカラムを組み合わせる"
    }
  ]
}
```

### 📋 データベーススキーマ

#### シンプル構成（5カラム）

| カラム名 | 型 | 説明 | 必須 |
|---------|----|----|------|
| 要件ID | Text | REQ-001, REQ-002 など | Yes |
| 要件名 | Title | 要件の名前 | Yes |
| カテゴリ | Select | 機能 / 非機能 / その他 | Yes |
| ステータス | Select | 未着手 / 設計中 / 実装中 / テスト中 / 完了 | Yes |
| 優先度 | Select | Must / Should / Could / Won't | Yes |

#### 標準構成（8カラム）

シンプル構成に加えて:

| カラム名 | 型 | 説明 | 必須 |
|---------|----|----|------|
| 担当者 | People | このタスクの担当者 | No |
| 関連ユースケース | Relation | UC-XXX へのリンク | No |
| 備考 | Text | 追加情報やメモ | No |

#### 詳細構成（12カラム）

標準構成に加えて:

| カラム名 | 型 | 説明 | 必須 |
|---------|----|----|------|
| テストケースID | Text | TC-001 など | No |
| 完了予定日 | Date | 目標完了日 | No |
| 関連ドキュメント | URL | 仕様書やリンク | No |
| 技術スタック | Multi-select | React / Node.js など | No |

### 🚀 実行手順

```bash
# 1. notion-db スキルで DB を作成
/notion-db create \
  --db-name "TaskFlow Requirements Tracker" \
  --workspace-name "TaskFlow PM" \
  --icon "📋" \
  --columns-template "standard"

# 出力例:
# ✓ Database created
# Database ID: abc123def456...
# URL: https://notion.so/abc123def456...
# 環境変数 NOTION_DATABASE_ID を設定してください
```

### ✅ 成功確認

- [ ] Notion上にデータベースが作成されている
- [ ] URL: `https://notion.so/{DATABASE_ID}` にアクセス可能
- [ ] すべてのカラムが正しく作成されている
- [ ] 環境変数 `NOTION_DATABASE_ID` が設定されている

---

## 📍 Step 3: 要件データの投入

### 🚀 実施内容

requirements-spec.md から要件を抽出し、Notion DBに投入します。

```json
{
  "type": "AskQuestion",
  "question": "データの投入方法を選んでください",
  "options": [
    {
      "label": "requirements-spec.mdから自動抽出",
      "value": "auto_extract",
      "description": "既存の仕様書から要件を自動解析して投入（推奨）"
    },
    {
      "label": "手動で1件ずつ",
      "value": "manual",
      "description": "フォーム入力で1件ずつ追加"
    },
    {
      "label": "サンプルデータで一括投入",
      "value": "sample",
      "description": "テスト用のサンプル要件15件を一括投入"
    }
  ]
}
```

### 📋 自動抽出の手順

```bash
# 1. requirements-spec.md を読み込む
/notion-db import \
  --source-file "output/pm/requirements-spec.md" \
  --database-id "${NOTION_DATABASE_ID}" \
  --parse-mode "markdown" \
  --map-config '{
    "title": "requirement_name",
    "id": "requirement_id",
    "category": "category_field",
    "priority": "priority_field",
    "status": "initial_status:未着手"
  }'

# 2. インポート結果の確認
# 投入件数: 10-15件
# 成功件数: XX件
# エラー件数: 0件
```

### 📋 サンプルデータの例

```markdown
| 要件ID | 要件名 | カテゴリ | ステータス | 優先度 | 関連ユースケース | 備考 |
|--------|--------|---------|----------|--------|---------------|------|
| REQ-001 | ユーザー登録機能 | 機能 | 未着手 | Must | UC-01 | メール認証を含む |
| REQ-002 | ログイン機能 | 機能 | 未着手 | Must | UC-02 | パスワードリセット機能 |
| REQ-003 | ダッシュボード表示 | 機能 | 未着手 | Must | UC-05 | リアルタイム更新不要 |
| REQ-004 | タスク一覧表示 | 機能 | 未着手 | Must | UC-06 | フィルタリング機能を含む |
| REQ-005 | タスク作成・編集 | 機能 | 未着手 | Must | UC-07 | 複数の優先度レベル対応 |
| REQ-006 | タスク削除機能 | 機能 | 未着手 | Should | UC-08 | 論理削除を実装 |
| REQ-007 | 通知機能 | 機能 | 未着手 | Should | UC-09 | メール/プッシュ対応 |
| REQ-008 | 期限アラート | 機能 | 未着手 | Should | UC-10 | 24時間前に通知 |
| REQ-009 | レスポンシブ対応 | 非機能 | 未着手 | Must | UC-11 | Mobile/Tablet/Desktop |
| REQ-010 | ページロード時間 | 非機能 | 未着手 | Should | N/A | 3秒以内 |
| REQ-011 | セキュリティ（暗号化） | 非機能 | 未着手 | Must | N/A | SSL/TLS必須 |
| REQ-012 | データベース最適化 | 非機能 | 未着手 | Could | N/A | インデックス設定 |
```

### ✅ 投入確認

- [ ] 要件が10件以上Notion DBに投入されている
- [ ] すべての必須フィールド（ID/名前/カテゴリ/ステータス）が入力されている
- [ ] 優先度が適切に設定されている（Must: 40-50%, Should: 30-40%, Could: 10-20%）
- [ ] Notionで実際に表示・検索・フィルタリングが可能

---

## 📍 Step 4: Markdownエクスポート

### 🚀 実施内容

Notion DBの内容をマークダウン形式でエクスポートし、ドキュメント化します。

```json
{
  "type": "AskQuestion",
  "question": "エクスポート形式を選んでください",
  "options": [
    {
      "label": "Markdown表形式",
      "value": "markdown_table",
      "description": "表形式のマークダウンでエクスポート（推奨）"
    },
    {
      "label": "CSV",
      "value": "csv",
      "description": "CSVファイルでエクスポート"
    },
    {
      "label": "JSON",
      "value": "json",
      "description": "構造化されたJSONでエクスポート"
    },
    {
      "label": "すべて",
      "value": "all",
      "description": "Markdown + CSV + JSON の3形式を生成"
    }
  ]
}
```

### 🚀 エクスポート実行

```bash
# 1. Notion DB をエクスポート
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "markdown" \
  --output-file "output/pm/notion-export.md" \
  --include-metadata true \
  --include-stats true

# 2. CSV形式でもエクスポート（推奨）
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "csv" \
  --output-file "output/pm/notion-export.csv"

# 3. JSON形式でエクスポート
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "json" \
  --output-file "output/pm/notion-export.json"
```

### 📋 エクスポート形式の例

```markdown
# TaskFlow Requirements Tracker - Export

**エクスポート日時**: 2024-01-15 14:30:00 JST
**データベースID**: abc123def456...
**URL**: https://notion.so/abc123def456...

## 📊 統計情報

| 項目 | 件数 |
|------|------|
| 総要件数 | 15 |
| 未着手 | 15 |
| 設計中 | 0 |
| 実装中 | 0 |
| テスト中 | 0 |
| 完了 | 0 |

### 優先度別

| 優先度 | 件数 | 割合 |
|--------|------|------|
| Must | 7 | 46.7% |
| Should | 6 | 40.0% |
| Could | 2 | 13.3% |
| Won't | 0 | 0.0% |

### カテゴリ別

| カテゴリ | 件数 | 割合 |
|---------|------|------|
| 機能 | 12 | 80% |
| 非機能 | 3 | 20% |

## 📋 要件一覧

| 要件ID | 要件名 | カテゴリ | ステータス | 優先度 | 関連UC | 備考 |
|--------|--------|---------|----------|--------|--------|------|
| REQ-001 | ユーザー登録機能 | 機能 | 未着手 | Must | UC-01 | メール認証を含む |
| REQ-002 | ログイン機能 | 機能 | 未着手 | Must | UC-02 | パスワードリセット機能 |
| ... | ... | ... | ... | ... | ... | ... |

---

**Generated by TaskFlow PM Training Platform**
```

### ✅ エクスポート確認

- [ ] output/pm/notion-export.md ファイルが生成されている
- [ ] 統計情報が含まれている（要件数、ステータス分布、優先度分布）
- [ ] すべての要件が表形式で表示されている
- [ ] 表のフォーマットが正しい（Markdownパーサーで読み込み可能）
- [ ] 必要に応じてCSVもエクスポート済み

---

## 🎯 成果物チェックリスト

### 必須ファイル・データ

```json
{
  "type": "AskQuestion",
  "question": "以下の成果物が完成していますか？ すべてに✓をつけてください",
  "options": [
    {
      "label": "✓ Notion側の準備（API接続確認完了）",
      "value": "step1_done"
    },
    {
      "label": "✓ 要件トラッカーDB作成完了",
      "value": "step2_done"
    },
    {
      "label": "✓ 要件データ投入完了（10件以上）",
      "value": "step3_done"
    },
    {
      "label": "✓ Markdownエクスポート完了",
      "value": "step4_done"
    },
    {
      "label": "✓ output/pm/notion-export.md ファイル生成済み",
      "value": "export_done"
    }
  ]
}
```

### ✅ 成功指標

- **Notion API接続**: 環境変数 `NOTION_API_KEY`, `NOTION_DATABASE_ID` が正しく設定されている
- **DB作成**: Notionダッシュボードで要件トラッカーDBが表示・アクセス可能
- **データ投入**: 最低10件、理想的には15件の要件がDBに存在
- **ステータス分布**: 初期状態では全て「未着手」
- **優先度分布**: Must 40-50%, Should 30-40%, Could 10-20% 程度
- **エクスポート完了**: output/pm/notion-export.md が生成され、統計情報と全要件リストが含まれている

---

## ⚠️ トラブルシューティング

### エラー: "NOTION_API_KEY not found"

```text
原因: 環境変数が設定されていない
解決策:
1. Notion APIキーを取得（https://www.notion.so/settings/integrations）
2. 以下を実行:
   export NOTION_API_KEY="YOUR_NOTION_SECRET_HERE"          # Mac/Linux/WSL
3. 再度実行
```

### エラー: "Unauthorized - Invalid API key"

```text
原因: APIキーが無効または期限切れ
解決策:
1. Notion settings から新しいAPIキーを生成
2. 環境変数を更新
3. 再度実行
```

### エラー: "Database not found"

```text
原因: NOTION_DATABASE_ID が正しくない、またはDBにアクセス権がない
解決策:
1. Notion DBのURLから正しいIDを確認
   https://notion.so/[32文字のID] から ID を抽出
2. 環境変数を修正
3. Integration に DB へのアクセス権があるか確認
```

### エラー: "Rate limit exceeded"

```text
原因: APIリクエストの頻度が高すぎる
解決策:
1. 15秒待機
2. 再度実行
3. 大量データ投入時は --delay フラグを使用
```

### エラー: "Markdown パース失敗"

```text
原因: requirements-spec.md の形式が正しくない
解決策:
1. requirements-spec.md の形式を確認
2. 手動で1件ずつ投入する（manual mode）
3. またはサンプルデータで試す
```

### ファイルが生成されない

```text
原因: output/pm/ ディレクトリがない、または権限不足
解決策:
1. ディレクトリ作成: mkdir -p output/pm
2. 権限確認: ls -la output/
3. 再度実行
```


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── test-cases.md  (テストケース一覧)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/test-cases.md

# 冒頭を確認（最初の30行）
head -30 output/pm/test-cases.md
```

> 💡 全文を確認: `cat output/pm/test-cases.md` で全文表示できます

---

## ➡️ 次のステップ

### 🎓 Lesson 18-12: UIデザイン

**フェーズ進捗**: Phase B（要件定義・設計）が完了！

次のレッスンではPhase C（デザイン・実装）に進みます。

- TaskFlowのUIプロトタイプ作成
- ワイヤーフレーム設計
- デザインシステムの定義
- フロントエンド実装の準備

**所要時間**: 約30分
**使うスキル**: figma-design / wireframe スキル

---

## 📚 参考リソース

### Notion API ドキュメント
- [Notion API Documentation](https://developers.notion.com/)
- [Database API Reference](https://developers.notion.com/reference/database)
- [Query Database](https://developers.notion.com/reference/post-database-query)

### TaskFlow PM モジュール
- Module 18: システム要件定義（企画〜要件定義〜設計〜実装〜テスト〜総括）

### 関連レッスン
- Lesson 18-10: 要件仕様書作成（要件分析）
- Lesson 18-12: UIデザイン（デザイン・実装フェーズ）
- Lesson 18-13: 実装計画書作成（実装フェーズ）

---

**Created**: 2024-01-15
**Last Updated**: 2024-01-15
**Module**: 14-PM-System Definition
**Level**: Intermediate

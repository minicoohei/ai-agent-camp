---
description: "When the user says /start-18-2 — Module 18 Lesson 18-2: PM - 要求資料の作成"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "25分"
category: "lesson"
prerequisites: ["start-18-1", "output/pm/customer-needs.md"]
level: "intermediate"
tags: ["pm", "requirements", "moscow"]
---

# 🎓 Lesson 18-2: 要求資料の作成

## 📍 このセッションでやること

**Lesson 18-2: 要求資料の作成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowの機能要求/非機能要求を整理し、要求資料（MoSCoW法）を作成する |
| 所要時間 | 約25分 |
| 使うスキル | pm-toolkit スキル |
| 前提条件 | Lesson 18-1 完了、output/pm/customer-needs.md が存在する |
| 教材ページ | [Module 18: PM & システム要件定義](https://ai-agent.camp/ja/course/module-18) を並行参照 |

**このセッションの流れ:**
1. customer-needs.md を読み込み、要求を抽出
2. 機能要求の洗い出し（MoSCoW法で優先順位付け）
3. 非機能要求の定義（性能、セキュリティ、可用性）
4. requirements-brief.md の生成

セッション終了時には、TaskFlowの要求資料が完成しています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。ツールによって応答が途中で止まることがありますが、故障ではありません。

---

## 🎯 準備チェック

16-1 を終えて、要求資料作成の準備ができていますか？確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "Lesson 18-1 が完了しているか確認したい"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 前提条件の確認を実行)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: 顧客ニーズの読み込み

前のレッスンで作成した customer-needs.md から、要求の種類を抽出する準備をしましょう。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 顧客ニーズの確認",
  "questions": [{
    "id": "needs_status",
    "prompt": "customer-needs.md は準備できていますか？",
    "options": [
      {"id": "ready", "label": "ファイルがある、進める"},
      {"id": "missing", "label": "ファイルがない"},
      {"id": "show_me", "label": "ファイルの内容を確認したい"}
    ]
  }]
}
```

(ready → Step 2へ)
(missing → Lesson 18-1 へ誘導)
(show_me → ファイル内容を表示)

**期待される結果**: customer-needs.md が確認され、内容が整理できます。

---

## 🚀 Step 2: 機能要求の洗い出し

customer-needs.md のニーズをもとに、TaskFlowの機能要求を列挙し、MoSCoW法で優先順位を付けます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 機能要求のカテゴリを選択",
  "questions": [{
    "id": "functional_category",
    "prompt": "機能要求のカテゴリを1つ選んで、その機能を詳しく洗い出しましょう",
    "options": [
      {"id": "task_basics", "label": "タスク管理基本機能"},
      {"id": "team_collab", "label": "チームコラボレーション"},
      {"id": "analytics", "label": "分析・レポート機能"},
      {"id": "notification", "label": "通知・アラート機能"},
      {"id": "all_categories", "label": "全てのカテゴリを一度に整理（AIにお任せ）"}
    ]
  }]
}
```

**各カテゴリの機能要求例（AIが提案）:**

```text
【タスク管理基本機能】
- タスク作成・編集・削除
- タスクの優先度設定
- 期限設定とリマインダー
- ステータス管理（未開始→進行中→完了）
- タスク検索・フィルター

【チームコラボレーション】
- タスクの割り当て
- チームメンバー間のコメント・議論
- ファイル添付機能
- 担当者の変更・委譲
- チーム権限管理

【分析・レポート機能】
- プロジェクト進捗ダッシュボード
- 個人・チーム別の生産性分析
- 期限超過タスクの可視化
- 週別・月別レポート生成

【通知・アラート機能】
- 期限前通知
- タスク割り当て通知
- コメント通知
- メール/Slack 統合
```

**AskQuestionの設定例（MoSCoW分類）:**
```json
{
  "title": "🚀 Step 2-2: 機能をMoSCoW法で分類",
  "questions": [{
    "id": "moscow_classification",
    "prompt": "抽出した機能を以下のカテゴリに分類してください",
    "options": [
      {"id": "must_have", "label": "Must Have（絶対必要）: MVP に必須"},
      {"id": "should_have", "label": "Should Have（重要）: 1～2か月後に必要"},
      {"id": "could_have", "label": "Could Have（できたら良い）: 将来的に検討"},
      {"id": "wont_have", "label": "Won't Have（不要）: 今回は実装しない"},
      {"id": "auto_classify", "label": "AIに自動分類させて"}
    ]
  }]
}
```

**MoSCoW分類のガイドライン:**
```text
Must Have の判定基準:
  ✓ ユーザーの80%が使う機能
  ✓ 「これがないと困る」と複数の顧客が言及
  ✓ 競合他社の標準機能
  → 例：タスク作成・優先度・期限設定

Should Have の判定基準:
  ✓ ユーザーの50%以上が使う機能
  ✓ 「できたら嬉しい」という意見
  ✓ MVP の次フェーズで実装可能
  → 例：生産性ダッシュボード、Slack 連携

Could Have の判定基準:
  ✓ ニッチな使用例
  ✓ 実装コスト高い
  ✓ 後から追加可能
  → 例：AI による優先度提案、高度な分析

Won't Have の判定基準:
  ✓ スコープ外
  ✓ 運用困難
  ✓ 需要不明確
  → 例：携帯アプリ（Web のみ）、高度なカスタマイズ
```

**期待される結果**: 機能要求が Must Have ～ Won't Have に分類されます。

---

## 🚀 Step 3: 非機能要求の定義

品質・性能・セキュリティなど、機能以外の要求を定義します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 非機能要求の観点を選択",
  "questions": [{
    "id": "nonfunctional_aspect",
    "prompt": "非機能要求の観点を1つ選んで、具体的な目標値を決めましょう",
    "options": [
      {"id": "performance", "label": "性能要件（レスポンス時間、処理速度）"},
      {"id": "security", "label": "セキュリティ要件"},
      {"id": "availability", "label": "可用性要件（アップタイム、冗長性）"},
      {"id": "usability", "label": "ユーザビリティ要件"},
      {"id": "all_aspects", "label": "全ての観点を一度に（AIにお任せ）"}
    ]
  }]
}
```

**各観点の具体例：**

```text
【性能要件】
- ページロード時間: < 3秒
- API レスポンス時間: < 500ms
- 同時接続ユーザー: 1,000 人
- データベースクエリ: < 1秒

【セキュリティ要件】
- SSL/TLS で通信暗号化
- 認証: Email + パスワード（2要素認証オプション）
- 権限管理: ロールベース（Admin, Manager, Member）
- パスワードポリシー: 最小8文字、大文字・数字を含む
- 監査ログ: 全操作を記録

【可用性要件】
- サービス稼働率: 99.5% 以上
- 月次メンテナンス: 最大4時間（月1回）
- バックアップ: 日次自動バックアップ
- 災害復旧: RPO=1日、RTO=4時間

【ユーザビリティ要件】
- 対応ブラウザ: Chrome, Firefox, Safari 最新版
- レスポンシブ: モバイル・タブレット対応
- アクセシビリティ: WCAG 2.1 AA 準拠
- サポート言語: 日本語（英語は将来）
- ヘルプ・チュートリアル: 初回ユーザー向けガイド完備
```

**AskQuestionの設定例（数値目標設定）:**
```json
{
  "title": "🚀 Step 3-2: 非機能要求の数値目標",
  "questions": [
    {
      "id": "perf_targets",
      "prompt": "性能目標を選択または入力してください",
      "options": [
        {"id": "fast", "label": "高速（ページロード<2s、API<300ms）"},
        {"id": "normal", "label": "標準（ページロード<3s、API<500ms）"},
        {"id": "custom", "label": "カスタム入力"}
      ]
    },
    {
      "id": "security_level",
      "prompt": "セキュリティレベルを選択してください",
      "options": [
        {"id": "standard", "label": "標準（パスワード認証、HTTPS）"},
        {"id": "high", "label": "高（2要素認証、監査ログ）"},
        {"id": "custom", "label": "カスタム"}
      ]
    }
  ]
}
```

**期待される結果**: 各非機能要件の数値目標が設定されます。

---

## 🚀 Step 4: requirements-brief.md の生成

Step 2, 3 で整理した機能要求・非機能要求をドキュメント化します。

**生成するドキュメント:**
```text
以下の内容で output/pm/requirements-brief.md を生成してください:

# TaskFlow 要求資料（要件定義書）

## 1. ドキュメント情報
- プロジェクト名: TaskFlow
- バージョン: 1.0
- 作成日: {今日の日付}
- 対象版: MVP（Minimum Viable Product）

## 2. 概要
TaskFlow は、社員数 10～100 名の中小企業向けのタスク管理 Web アプリケーションです。
チーム全員の「今日やること」が一目でわかり、AI が優先度を提案し、タスクの見落としを防ぎます。

## 3. 機能要求（MoSCoW 法で分類）

### 3.1 Must Have（MVP に必須）
| # | 機能 | 説明 | 優先度 |
|---|------|------|--------|
| 1 | タスク作成 | テキストと期限を指定してタスクを作成 | P0 |
| 2 | タスク一覧表示 | 自分のタスク・チームのタスクを一覧表示 | P0 |
| ... | ... | ... | ... |

### 3.2 Should Have（フェーズ 2 で実装）
| # | 機能 | 説明 | 優先度 |
|---|------|------|--------|
| 1 | プロジェクト単位の管理 | 複数プロジェクトに対応 | P1 |
| ... | ... | ... | ... |

### 3.3 Could Have（検討対象）
| # | 機能 | 説明 |
|---|------|------|
| 1 | AI による優先度提案 | 自然言語から優先度を自動判定 |
| ... | ... | ... |

### 3.4 Won't Have（スコープ外）
- モバイルネイティブアプリ（将来検討）
- 高度なカスタマイズ機能（運用困難なため）

## 4. 非機能要求

### 4.1 性能要件
- ページロード時間: < 3秒
- API レスポンス時間: < 500ms
- 同時接続ユーザー: 最大 1,000 人

### 4.2 セキュリティ要件
- 認証: Email + パスワード（初版）
- 通信: TLS 1.2 以上で暗号化
- 権限管理: ロールベース（Admin, Manager, Member）
- 監査ログ: 全操作を記録・保持

### 4.3 可用性・信頼性
- サービス稼働率: 99.5% 以上（月当たりダウン時間 < 3.6 時間）
- バックアップ: 日次自動バックアップ（リテンション 30 日）
- 災害復旧: RTO 4 時間、RPO 1 日

### 4.4 ユーザビリティ
- 対応ブラウザ: Chrome, Firefox, Safari 最新版
- レスポンシブデザイン: モバイル・タブレット対応
- サポート言語: 日本語
- ヘルプ: チュートリアル + FAQ完備

## 5. 制約条件
- 開発期間: 8 週間（MVP）
- チーム規模: エンジニア 3 人、PM/デザイナー各 1 人
- 予算: {顧客から聞いた予算枠}
- 技術スタック: フロント（React）、バック（Node.js + PostgreSQL）

## 6. 前提条件・リスク

### 前提条件
- 顧客が定期的にフィードバックを提供できる
- デザイン・ブランドガイドラインが事前に準備されている

### リスク
1. API 仕様の頻繁な変更 → 週 1 回のデザインレビューで軽減
2. スケーラビリティ → 負荷テスト実施（フェーズ 2）

## 7. 次のステップ
- Lesson 18-3: PRD（Product Requirements Document）作成

mkdir -p output/pm && ファイルを output/pm/requirements-brief.md に保存
```

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 生成内容の確認",
  "questions": [{
    "id": "doc_generation",
    "prompt": "requirements-brief.md を生成してもいいですか？",
    "options": [
      {"id": "generate", "label": "生成する"},
      {"id": "review", "label": "内容を確認してから生成"},
      {"id": "custom", "label": "カスタマイズして生成"}
    ]
  }]
}
```

(generate → ドキュメント生成)
(review → 内容をプレビュー表示)
(custom → カスタマイズオプション表示)

**期待される結果**: `output/pm/requirements-brief.md` が生成されます。

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "MoSCoW分類で機能の優先度が判断できない"},
      {"id": "trouble_2", "label": "非機能要求の数値目標がわからない"},
      {"id": "trouble_3", "label": "customer-needs.md がない"},
      {"id": "trouble_4", "label": "出力ファイルが生成されない"}
    ]
  }]
}
```

### トラブル1: MoSCoW分類で優先度が判断できない
**解決策**: 以下の問いを自分に問いかけてください:
- 「ユーザーの80%が使う機能か？」→ Yes なら Must Have
- 「複数の顧客が『これがないと困る』と言及したか？」→ Yes なら Must Have
- 「競合他社（Trello, Asana）の標準機能か？」→ Yes なら Should Have
- 「1～2か月後に必要な機能か？」→ Yes なら Should Have
- 「やってみて反応を見たい機能か？」→ Yes なら Could Have
- 「今回のスコープではやらない機能か？」→ Yes なら Won't Have

### トラブル2: 非機能要求の数値目標がわからない
**解決策**: 業界標準値を参考にしてください:

| 項目 | 標準値 | 高速 |
|------|--------|------|
| ページロード時間 | < 3秒 | < 2秒 |
| API レスポンス | < 500ms | < 300ms |
| サイト稼働率 | 99.5% | 99.99% |
| バックアップ頻度 | 日次 | 時間単位 |

わからなければ「標準」を選び、運用開始後に改善します。

### トラブル3: customer-needs.md がない
**解決策**: Lesson 18-1 から開始してください。または、簡易版として以下を作成:
```markdown
# 顧客ニーズ分析（簡易版）

## ペルソナ
- 名前: 太郎（仮名）
- 職種: プロジェクトマネージャー
- 課題: Excel でのタスク管理が煩雑

## ニーズ
1. チーム全員のタスクが見える
2. 期限超過を自動で警告
3. Slack と連携して通知が欲しい
```

### トラブル4: 出力ファイルが生成されない
**解決策**: `output/pm/` ディレクトリが存在するか確認:
```bash
mkdir -p output/pm
# その後、ドキュメント生成を再度実行
```

---

## ✅ チェックポイント
- [ ] Lesson 18-1 を完了している
- [ ] customer-needs.md を読み込んだ
- [ ] 機能要求が Must Have ～ Won't Have に分類されている
- [ ] Must Have が 5～10 個に絞られている（多すぎないか確認）
- [ ] 非機能要求に具体的な数値目標が設定されている
- [ ] output/pm/requirements-brief.md が生成されている
- [ ] ドキュメントの内容が正確（タイプミス、矛盾がないか）


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── customer-needs.md  (顧客ニーズ分析)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/customer-needs.md

# 冒頭を確認（最初の30行）
head -30 output/pm/customer-needs.md
```

> 💡 全文を確認: `cat output/pm/customer-needs.md` で全文表示できます

---

## ✅ 完了チェック
以下をCodexのチャットに入力して、完了状況を確認してください:

```text
output/pm/requirements-brief.md の内容を確認してください：

1. 機能要求が Must Have / Should Have / Could Have / Won't Have に分類されているか
2. 各カテゴリで最低1つ以上の機能が定義されているか
3. 非機能要求（性能・セキュリティ・可用性）に具体的な数値が記載されているか
4. 制約条件と前提条件が明記されているか

確認後、「完了」と返答してください。
```

**期待される結果**: ドキュメントの完成度が確認されます。

---

## ➡️ 次のステップ

これでLesson 18-2は完了です。次は要求資料をもとに PRD（Product Requirements Document）を作成します。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のレッスン（PRD作成）を開始"},
      {"id": "next_window", "label": "新しいウィンドウで /start-18-3 を開始"},
      {"id": "review", "label": "もう一度要求資料を見直す"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- next_auto → /start-18-3 を実行
- next_window → 新しいウィンドウで /start-18-3
- review → requirements-brief.md を再表示
- finish → 終了

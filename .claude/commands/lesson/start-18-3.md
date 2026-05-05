---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "30分"
category: "lesson"
prerequisites: ["start-18-2", "output/pm/requirements-brief.md"]
level: "intermediate"
tags: ["pm", "prd", "working-backwards"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-3: PRD作成（Working Backwards方式）

## 📍 このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Amazon Working Backwards方式でTaskFlowのPRDを作成する |
| 所要時間 | 約30分 |
| 使うスキル | pm-toolkit スキル |
| 前提条件 | Lesson 18-2 完了、output/pm/requirements-brief.md が存在する |
| 教材ページ | [Module 18: PM & システム要件定義](https://ai-agent.camp/ja/course/module-18) を並行参照 |

**このセッションの流れ:**
1. Working Backwards方式の解説
2. プレスリリース形式でのPRD起草
3. FAQ・ユーザーストーリーの追記
4. prd.md の生成・整形

成果物: `output/pm/prd.md`

---

## 🎯 準備チェック - readiness check

```json
{
  "type": "AskQuestion",
  "question": "このレッスンを開始するための準備確認",
  "description": "16-3を開始する前に、必要な条件をチェックします。",
  "options": [
    {
      "label": "準備完了。Lesson 18-2を完了済み、requirements-brief.mdが存在する",
      "value": "ready",
      "next_action": "continue"
    },
    {
      "label": "Lesson 18-2を見直したい",
      "value": "review_previous",
      "next_action": "view_html",
      "url": "../../start-18-2"
    },
    {
      "label": "現在のファイル構成を確認したい",
      "value": "check_structure",
      "next_action": "bash",
      "command": "ls -la output/pm/ 2>/dev/null || echo 'Directory not found'"
    },
    {
      "label": "Module 18を最初から学びたい",
      "value": "start_module",
      "next_action": "view_html",
      "url": "https://ai-agent.camp/ja/course/module-18"
    }
  ]
}
```

**確認項目:**
- ✓ Lesson 18-2（要件定義ブリーフ）が完了している
- ✓ `output/pm/requirements-brief.md` が存在する
- ✓ プロジェクト背景を理解している

---

## 🚀 Step 1: Working Backwards方式の理解と準備

```json
{
  "type": "AskQuestion",
  "question": "Amazon Working Backwards方式についてどの程度知っていますか？",
  "description": "Working Backwards方式は、Amazonが採用している革新的なプロダクト開発手法です。この手法の習熟度を確認して、説明レベルを調整します。",
  "options": [
    {
      "label": "詳しく知っている（Amazonの事例や書籍で学んだ）",
      "value": "expert",
      "next_action": "continue"
    },
    {
      "label": "概要だけ知っている（顧客視点で開発する、という程度）",
      "value": "intermediate",
      "next_action": "continue"
    },
    {
      "label": "初めて聞く、または何それ？という状態",
      "value": "beginner",
      "next_action": "continue"
    }
  ]
}
```

### Working Backwards方式とは

Working Backwards方式は、**「顧客の視点から逆算してプロダクトを定義する」**というAmazonの開発手法です。

**従来の開発手法との違い:**

| 従来手法 | Working Backwards |
|--------|-----------------|
| 技術仕様から始まる | **顧客体験から始まる** |
| 完成後に利用方法を考える | **プレスリリースを最初に書く** |
| 社内視点での要件定義 | **顧客からの質問(FAQ)を先に書く** |

**Working Backwards の 5 ステップ:**

1. **プレスリリース(Press Release)** - 製品発表を顧客向けに書く
2. **FAQ(Frequently Asked Questions)** - 顧客とステークホルダーの質問に答える
3. **ユーザーストーリー(User Stories)** - 利用シーンを具体化する
4. **スコープ定義(Scope)** - MVPと将来版の区分
5. **成功指標(Success Metrics)** - KPIの定義

**TaskFlowに適用する場合:**
- 誰が「タスク管理に困っているのか」を明確にする
- 「どう変わると嬉しいのか」をプレスリリースで表現する
- 「なぜそれが必要か」をFAQで説明する

### 準備: 前回のドキュメントを確認

```json
{
  "type": "AskQuestion",
  "question": "requirements-brief.md の内容を確認しますか？",
  "description": "Step 2でプレスリリースを作成する際に、前回のRequirements Briefが参照材料になります。事前に内容を確認しておくことをお勧めします。",
  "options": [
    {
      "label": "内容を確認する（ファイルを表示）",
      "value": "view",
      "next_action": "bash",
      "command": "cat output/pm/requirements-brief.md || echo 'File not found'"
    },
    {
      "label": "確認済み、次のステップに進む",
      "value": "skip",
      "next_action": "continue"
    },
    {
      "label": "ファイルが見つからない、ヘルプが必要",
      "value": "help",
      "next_action": "bash",
      "command": "find . -name 'requirements-brief.md' -o -name '*requirement*' 2>/dev/null | head -10"
    }
  ]
}
```

---

## 🚀 Step 2: プレスリリース形式でのPRD起草

プレスリリース形式でPRDを書くことで、**顧客メリットが明確**で、**社内の技術者にも理解しやすい**ドキュメントができます。

```json
{
  "type": "AskQuestion",
  "question": "プレスリリースのトーンと対象をどう設定しますか？",
  "description": "Working Backwards方式では、プレスリリースの書き方が重要です。ターゲット読者に応じて、トーンと内容を調整します。",
  "options": [
    {
      "label": "ビジネス向け（フォーマル、株主・投資家を想定）",
      "value": "formal",
      "next_action": "continue"
    },
    {
      "label": "スタートアップ向け（カジュアル、ユーザーコミュニティを想定）",
      "value": "casual",
      "next_action": "continue"
    },
    {
      "label": "社内向け（実用的、エンジニア向け）",
      "value": "internal",
      "next_action": "continue"
    },
    {
      "label": "投資家向け（数字重視、成長性を強調）",
      "value": "investor",
      "next_action": "continue"
    }
  ]
}
```

### プレスリリースのテンプレート

Working Backwards方式のプレスリリースには、以下のセクションが必須です：

**必須セクション:**

```text
# [HEADLINE: 簡潔で力強いタイトル]

## サマリー
[一段落で製品の本質を説明]

## 問題
[対象顧客がどんな課題を持っているか]

## ソリューション
[TaskFlowがどう解決するか、3-5点を箇条書き]

## カスタマーメリット
[顧客にとっての具体的な利点]

## 提供開始時期 / 価格
[可用性と価格戦略]

## 詳細情報
[ウェブサイト、ドキュメント、お問い合わせ先]

---

## お客様からの声（トーク）
"[顧客の言葉で、期待する効果を表現]" - [顧客企業 役職]
```

### Step 2 の実行

```json
{
  "type": "AskQuestion",
  "question": "プレスリリース（draft）をAIに作成させますか、それとも手動で作成しますか？",
  "description": "Step 2では、requirements-brief.mdを読み込んで、AIがプレスリリースのドラフトを自動生成するか、あるいは自分で作成するかを選べます。",
  "options": [
    {
      "label": "AIに生成してもらう（pm-toolkitで自動生成）",
      "value": "ai_generate",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-pressrelease --tone-mode {tone_option} --input-file output/pm/requirements-brief.md"
    },
    {
      "label": "手動で作成する（AIはレビュー補助のみ）",
      "value": "manual",
      "next_action": "continue"
    },
    {
      "label": "AIの案を見てから調整したい",
      "value": "hybrid",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-pressrelease-draft --tone-mode {tone_option} --input-file output/pm/requirements-brief.md"
    }
  ]
}
```

**もし手動で作成する場合のステップ:**

1. エディタを開く: `output/pm/prd-draft.md`
2. 上記テンプレートを貼り付け
3. Requirements-briefを参考に、各セクションを記入
4. 社内レビューに出す前に、「顧客メリット」が明確になっているか確認

**プレスリリースの品質チェックリスト:**
- [ ] ヘッドラインは一目で「何が変わるのか」を表現している
- [ ] 問題セクションに、顧客の苦労がリアルに書かれている
- [ ] ソリューションセクションは「How」ではなく「What/Why」に焦点を当てている
- [ ] 顧客の声（トーク）がビジネス価値を具体的に表現している
- [ ] 専門用語は最小限、誰でも理解できる言葉を使っている

---

## 🚀 Step 3: FAQ・ユーザーストーリーの追記

プレスリリースが完成したら、**FAQ（よくある質問）**と**ユーザーストーリー**を追加して、PRDをより詳細にします。

### 3-1: FAQ（よくある質問）の作成

```json
{
  "type": "AskQuestion",
  "question": "FAQでカバーする観点を選んでください",
  "description": "FAQには2種類の質問が必要です。（1）エンドユーザーからの質問、（2）ステークホルダー（経営層・エンジニア）からの質問。どれを優先的に書きますか？",
  "options": [
    {
      "label": "ユーザー向けFAQ（使い方、機能、サポート）",
      "value": "user_faq",
      "next_action": "continue"
    },
    {
      "label": "ステークホルダー向けFAQ（ビジネス価値、技術、スケーラビリティ）",
      "value": "stakeholder_faq",
      "next_action": "continue"
    },
    {
      "label": "ユーザーストーリー（具体的な使用シーン）",
      "value": "user_stories",
      "next_action": "continue"
    },
    {
      "label": "全部（ユーザーFAQ + ステークホルダーFAQ + ユーザーストーリー）",
      "value": "all",
      "next_action": "continue"
    }
  ]
}
```

**ユーザー向けFAQ の例:**

```markdown
## FAQ - ユーザー向け

### Q1: TaskFlowはどのくらいの数のタスクを管理できますか？
A: TaskFlowは数千のタスクの同時管理をサポートしています。...

### Q2: 既存のツール（Notion, Asanaなど）からの移行はできますか？
A: はい、CSV/JSON形式のインポート機能で一括移行できます。...

### Q3: モバイルアプリはありますか？
A: MVP版ではWebアプリを提供します。モバイルアプリはv2での予定です。...

### Q4: オフラインでも使えますか？
A: はい、オフラインモードで基本機能を使用できます。...

### Q5: チーム内での権限管理はどの程度細かく設定できますか？
A: オーナー、メンバー、ビューアの3レベルの権限を提供しています。...
```

**ステークホルダー向けFAQ の例:**

```markdown
## FAQ - ステークホルダー向け

### Q1: TaskFlowのターゲットマーケットはどのぐらいの大きさですか？
A: グローバルなプロジェクト管理市場は年間 XX 億ドルで、成長率は Y% です。...

### Q2: 競合製品（Jira, Monday.comなど）との違いは何ですか？
A: TaskFlowは「シンプルさ」と「チームコラボレーション」に特化しています。...

### Q3: 売上モデルは何ですか？
A: SaaS型のサブスクリプション（フリーミアム + 有料プラン）を採用します。...

### Q4: 技術的なスケーラビリティは大丈夫ですか？
A: クラウドネイティブアーキテクチャで、数百万ユーザーまでのスケールを想定しています。...

### Q5: セキュリティやコンプライアンスは？
A: SOC 2 Type II認証を取得し、GDPR/個人情報保護法に準拠しています。...
```

### 3-2: ユーザーストーリーの定義

```json
{
  "type": "AskQuestion",
  "question": "ユーザーストーリーの優先度付けをどうしますか？",
  "description": "ユーザーストーリーは、実装優先度によってMust/Should/Couldに分類します。各レベルでいくつのストーリーを書きますか？",
  "options": [
    {
      "label": "Must（MVP必須）に絞る：3～5個",
      "value": "must_only",
      "next_action": "continue"
    },
    {
      "label": "Must + Should：合計8～10個",
      "value": "must_should",
      "next_action": "continue"
    },
    {
      "label": "フルセット（Must/Should/Could）：15個以上",
      "value": "full_set",
      "next_action": "continue"
    },
    {
      "label": "AIに自動生成させる",
      "value": "ai_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-user-stories --input-file output/pm/requirements-brief.md --count 10"
    }
  ]
}
```

**ユーザーストーリーのテンプレート:**

```text
As a [ロール], I want [機能/アクション], so that [ビジネス価値/メリット]

例1) As a busy project manager, I want to set recurring tasks, so that I don't have to manually recreate them every week.

例2) As a team lead, I want to see real-time progress on all projects, so that I can identify blockers immediately.

例3) As a new user, I want a guided onboarding tutorial, so that I can set up my first project in under 5 minutes.
```

**MoSCoWプライオリティ:**

```text
## ユーザーストーリー（優先度付け）

### MUST（MVP必須）
- [ ] US-1: As a user, I want to create tasks with title and description
- [ ] US-2: As a team lead, I want to assign tasks to team members
- [ ] US-3: As a user, I want to mark tasks as complete/incomplete

### SHOULD（v1で実装したい）
- [ ] US-4: As a user, I want to set due dates and reminders
- [ ] US-5: As a user, I want to organize tasks into projects/folders

### COULD（将来版での実装）
- [ ] US-6: As a user, I want to integrate with Slack notifications
- [ ] US-7: As a user, I want to generate reports on productivity metrics
```

---

## 🚀 Step 4: スコープ定義と成功指標の設定

最後に、**何をやるのか/やらないのか**を明確にして、**成功をどう測るのか**を定義します。

### 4-1: In Scope (MVP) vs Out of Scope (将来版)

```json
{
  "type": "AskQuestion",
  "question": "スコープ定義をどう進めますか？",
  "description": "「何を入れる/入れない」を決めることで、開発工数や期間が大きく変わります。以下の方法から選んでください。",
  "options": [
    {
      "label": "AIに提案してもらう（requirements-briefから自動抽出）",
      "value": "ai_suggest",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-scope-definition --input-file output/pm/requirements-brief.md"
    },
    {
      "label": "自分で決める（テンプレートを使って手動入力）",
      "value": "manual",
      "next_action": "continue"
    },
    {
      "label": "ハイブリッド（AIの案をレビューして調整）",
      "value": "hybrid",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-scope-definition-draft --input-file output/pm/requirements-brief.md"
    }
  ]
}
```

**スコープ定義テンプレート:**

```text
## In Scope (MVP v1.0)

### Core Features
- Task creation, editing, deletion
- Task assignment to team members
- Due date and priority setting
- Project/folder organization
- Basic filtering and search
- Team collaboration (comments on tasks)
- Email notifications

### Technical
- Web application (responsive design for desktop, tablet)
- SQLite/PostgreSQL database
- REST API for future mobile app
- Basic authentication

## Out of Scope (v2+)

### Future Features
- Mobile native apps (iOS/Android)
- Advanced reporting and analytics
- Integration with Slack/Teams
- Time tracking and estimation
- Resource allocation algorithms
- Advanced permission management

### Not Planned
- Desktop client (will use web)
- Complex workflow automation
- AI-powered task recommendations (future AI phase)
```

### 4-2: 成功指標（Success Metrics / KPIs）の定義

```json
{
  "type": "AskQuestion",
  "question": "成功指標（KPI）をどのフレームワークで定義しますか？",
  "description": "ProductのSuccess Metricsは、ビジネス目標に直結した測定可能な指標です。一般的には AARRR (Acquisition, Activation, Retention, Revenue, Referral)を使用します。",
  "options": [
    {
      "label": "AARRR（Pirate Metrics）で定義",
      "value": "aarrr",
      "next_action": "continue"
    },
    {
      "label": "OKR（Objectives & Key Results）で定義",
      "value": "okr",
      "next_action": "continue"
    },
    {
      "label": "一般的なSaaS KPIで定義",
      "value": "saas_kpi",
      "next_action": "continue"
    },
    {
      "label": "AIに全て生成させる",
      "value": "ai_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-success-metrics --input-file output/pm/requirements-brief.md --framework aarrr"
    }
  ]
}
```

**AARRR フレームワークでのKPI定義例:**

```text
## Success Metrics (KPIs)

### Acquisition（獲得）
- Monthly signup rate: 目標 500 users/month (by end of v1)
- Organic traffic rate: 目標 30% (vs paid marketing)
- Sign-up conversion rate: 目標 3% (from landing page)

### Activation（有効化）
- First project creation rate: 目標 70% (within 7 days of signup)
- First task creation rate: 目標 85% (within 24 hours)
- Tutorial completion rate: 目標 60%

### Retention（継続利用）
- Monthly active users (MAU): 目標 80% of signups
- Weekly active users (WAU): 目標 50% of signups
- Churn rate: 目標 < 5% per month (for paid users)

### Revenue（収益）
- Conversion to paid: 目標 10% of free users
- Average revenue per account (ARPA): 目標 $50/month
- Customer lifetime value (LTV): 目標 $2,400

### Referral（紹介）
- Viral coefficient: 目標 1.2 (each user brings 1.2 new users)
- Referral signup rate: 目標 15% of new users
```

---

## 🚀 Step 5: PRD完成と出力

最後に、すべてのセクションを統合して、最終的なPRD（`prd.md`）を生成します。

```json
{
  "type": "AskQuestion",
  "question": "PRD（prd.md）の生成方法を選んでください",
  "description": "これまでのすべてのセクション（プレスリリース、FAQ、ユーザーストーリー、スコープ、KPI）を統合して、最終的なPRDを生成します。",
  "options": [
    {
      "label": "AIに全部統合・生成させる（pm-toolkitで自動生成）",
      "value": "full_auto",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-full-prd --input-files output/pm/requirements-brief.md,output/pm/prd-draft.md --output output/pm/prd.md"
    },
    {
      "label": "手動で各セクションを組み立てる",
      "value": "manual_assembly",
      "next_action": "continue"
    },
    {
      "label": "AIのドラフトをレビューしてから確定",
      "value": "review_then_finalize",
      "next_action": "skill",
      "skill_name": "pm-toolkit",
      "skill_args": "generate-prd-draft --input-files output/pm/requirements-brief.md,output/pm/prd-draft.md"
    }
  ]
}
```

**最終PRDの構成:**

```text
# Product Requirements Document (PRD)
## TaskFlow v1.0

---

## Executive Summary
[プレスリリースの内容を短縮したサマリー]

---

## Press Release
[Step 2で作成したプレスリリース全文]

---

## FAQ

### ユーザー向け FAQ
[Step 3で作成したユーザーFAQ]

### ステークホルダー向け FAQ
[Step 3で作成したステークホルダーFAQ]

---

## User Stories

### MUST (MVP v1.0)
[優先度付けされたユーザーストーリー]

### SHOULD (将来版)
[...]

### COULD (さらに将来)
[...]

---

## Scope Definition

### In Scope (MVP v1.0)
- Core Features
- Technical Requirements
- Design Scope

### Out of Scope (v2+)
- Future Features
- Not Planned

---

## Success Metrics (KPIs)

### AARRR Framework
- Acquisition: ...
- Activation: ...
- Retention: ...
- Revenue: ...
- Referral: ...

---

## Dependencies & Risks

### Dependencies
- 既存システムとの統合
- 外部サービスの利用可能性

### Risk & Mitigation
- リスク要因と対応策

---

## Timeline & Milestones
- Kick-off: ...
- Soft launch: ...
- GA: ...
```

### 出力ファイルの確認

```json
{
  "type": "AskQuestion",
  "question": "生成されたPRDを確認しますか？",
  "description": "prd.md が正しく生成されたかを確認します。",
  "options": [
    {
      "label": "ファイルの内容を表示（確認）",
      "value": "view",
      "next_action": "bash",
      "command": "cat output/pm/prd.md | head -100"
    },
    {
      "label": "ファイルサイズと生成日時を確認",
      "value": "check_meta",
      "next_action": "bash",
      "command": "ls -lh output/pm/prd.md && wc -l output/pm/prd.md"
    },
    {
      "label": "最後のセクション（KPI）を確認",
      "value": "view_end",
      "next_action": "bash",
      "command": "tail -50 output/pm/prd.md"
    }
  ]
}
```

---

## ⚠️ よくあるトラブルと解決方法

### Trouble 1: プレスリリースのヘッドラインが思いつかない

**症状:** ヘッドラインを何度も書き直してしまう、または「TaskFlow」という単語だけになっている

**原因:** ヘッドラインは「製品名」ではなく「顧客メリット」を伝える必要がある

**解決方法:**

```json
{
  "type": "AskQuestion",
  "question": "ヘッドラインの作成で困っていますか？",
  "options": [
    {
      "label": "はい、テンプレートが欲しい",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "いいえ、大丈夫",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**テンプレート:**

```text
パターン1) [ターゲット] の [課題] を [解決方法] で解決する
  例: 「忙しいチームリーダーのタスク管理負荷を、リアルタイム可視化で軽減する」

パターン2) [ビジネス成果] を実現する [製品名]
  例: 「プロジェクト完了までの時間を 30% 短縮する、TaskFlow」

パターン3) [定性的メリット] な [新アプローチ]
  例: 「シンプルなのに、パワフル。TaskFlowが変えるタスク管理」

ポイント:
- 専門用語を避ける（「可視化」「最適化」などの行政的な言葉は NG）
- 「Why」に焦点（「どのような機能」ではなく「どんな効果」）
```

---

### Trouble 2: スコープが広すぎて、MVPの定義が曖昧

**症状:** In Scopeに20個以上の機能が列挙されている、または「全部MVP」という状態

**原因:** 「できたらいいな」と「必須」が区別できていない

**解決方法:**

```json
{
  "type": "AskQuestion",
  "question": "スコープが広すぎると感じていますか？",
  "options": [
    {
      "label": "はい、絞り込みたい",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "いいえ、大丈夫",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**MVPの定義方法:**

```text
**MVP = 最小化されたスコープで、1つのペインポイントを完全に解決するセット**

Taskflow MVPの例:
  ✓ MVP に含める：Task作成・編集・削除 + チーム割り当て + 期限設定
  ✗ MVP から外す：統計・分析、Slack統合、時間追跡、高度な権限管理

判断基準:
- 「ユーザーがこれなしで価値を感じられるか？」→ Yes ⇒ MVP必須
- 「ハッキング・ワークアラウンドで対応できるか？」→ Yes ⇒ v2以降でOK
- 「競合他社がやっているから」→ それだけでは理由にならない ✗
```

---

### Trouble 3: KPIの設定がわからない

**症状:** KPIが「ユーザー数を増やす」だけ、または数字の根拠がない

**原因:** ビジネスモデルと測定指標の関係が明確になっていない

**解決方法:**

```json
{
  "type": "AskQuestion",
  "question": "KPI設定で困っていますか？",
  "options": [
    {
      "label": "はい、フレームワークを教えて",
      "value": "help",
      "next_action": "continue"
    },
    {
      "label": "いいえ、大丈夫",
      "value": "skip",
      "next_action": "continue"
    }
  ]
}
```

**AARRR フレームワークの実装例:**

```text
### Acquisition（どうユーザーを獲得するか）
- KPI例: Monthly signup rate, Cost per acquisition (CPA), Sign-up conversion rate
- TaskFlowの例: Product Hunt で launch ⇒ 目標 1000 signups

### Activation（ユーザーが価値を感じるまでの時間）
- KPI例: % users who complete onboarding, Time to first action, Feature adoption rate
- TaskFlowの例: 7日以内に最初のプロジェクトを作成したユーザーが 70% 以上

### Retention（継続利用）
- KPI例: Monthly/Weekly active users (MAU/WAU), Churn rate, Engagement score
- TaskFlowの例: 月間でアクティブなユーザーが 80% 以上

### Revenue（収益化）
- KPI例: ARPU (Average Revenue Per User), Conversion to paid, LTV (Life Time Value)
- TaskFlowの例: Freemium ⇒ 有料プラン転換率 10% 以上 ⇒ LTV $2400

### Referral（ウイルス成長）
- KPI例: Viral coefficient, Referral rate, NPS (Net Promoter Score)
- TaskFlowの例: 各ユーザーが平均 0.5人の新規ユーザーを招待
```

---

### Trouble 4: requirements-brief.md が見つからない

**症状:** エラー「File not found」、または `/output/pm/` ディレクトリが存在しない

**原因:** 16-2 を完了していない、またはファイルが別の場所に保存されている

**解決方法:**

```json
{
  "type": "AskQuestion",
  "question": "requirements-brief.md が見つかりませんか？",
  "options": [
    {
      "label": "見つからない。Lesson 18-2 をやり直したい",
      "value": "redo_lesson",
      "next_action": "view_html",
      "url": "../../start-18-2"
    },
    {
      "label": "別の場所にあるかもしれない（検索してほしい）",
      "value": "search",
      "next_action": "bash",
      "command": "find . -name 'requirements-brief*' -o -name '*brief*' 2>/dev/null"
    },
    {
      "label": "新規作成したい（テンプレートが欲しい）",
      "value": "create_new",
      "next_action": "continue"
    }
  ]
}
```

---

## ✅ チェックポイント

このセッションを完了したら、以下のすべてのボックスにチェックが入っていることを確認してください：

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "label": "Working Backwards方式を理解した",
      "required": true
    },
    {
      "label": "プレスリリース形式のPRDが起草されている",
      "required": true
    },
    {
      "label": "FAQ（ユーザー向け + ステークホルダー向け）が 5個以上含まれている",
      "required": true
    },
    {
      "label": "ユーザーストーリーが 3個以上定義されている（MUST優先度）",
      "required": true
    },
    {
      "label": "スコープ（In Scope / Out of Scope）が明確に定義されている",
      "required": true
    },
    {
      "label": "成功指標（KPI）が AARRR フレームワークで設定されている",
      "required": true
    },
    {
      "label": "ファイル `output/pm/prd.md` が生成されている",
      "required": true
    },
    {
      "label": "prd.md が 300行以上ある（十分な詳細度がある）",
      "required": false,
      "hint": "推奨：300～500行程度"
    }
  ]
}
```

**最終確認コマンド:**

```bash
# ファイルが存在するか確認
ls -lh output/pm/prd.md

# 行数を確認
wc -l output/pm/prd.md

# 内容をプレビュー
head -50 output/pm/prd.md
```


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── prd.md  (プロダクト要件定義書)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/prd.md

# 冒頭を確認（最初の30行）
head -30 output/pm/prd.md
```

> 💡 全文を確認: `cat output/pm/prd.md` で全文表示できます

---

## ➡️ 次のステップ

Lesson 18-3 が完了したら、次のレッスンに進みます：

```json
{
  "type": "NextStep",
  "next_lesson": "start-18-4",
  "title": "16-4: 3種レビュー（ビジネス/UX/テック）",
  "description": "作成したPRDを、3つの観点（ビジネス、ユーザー体験、技術実現性）からレビューし、最終版を完成させます。",
  "estimated_duration": "約25分",
  "what_you_will_do": [
    "PRDの論理的一貫性をチェック（ビジネスレビュー）",
    "ユーザー体験の実現可能性を評価（UXレビュー）",
    "技術的な実現可能性を確認（テックレビュー）",
    "フィードバックを統合して最終PRDを完成",
    "PRDのサイン・バージョン管理"
  ],
  "button_label": "16-4 に進む",
  "button_action": "open_lesson",
  "button_target": "start-18-4"
}
```

---

## 📌 補足資料

### Reference: Amazon Working Backwards の公式情報

Working Backwards方式について、さらに詳しく学びたい場合は、以下のリソースを参照してください：

- **書籍:** "Working Backwards" by Colin Bryar & Bill Carr (Amazon の VP Product が著）
- **Amazonの公式ガイド:** Leadership Principles の一つ "Customer Obsession"
- **ケーススタディ:** Kindle開発の例（会見資料）

### Reference: PARDフレームワーク（拡張版）

Working Backwards 以外の PRD フレームワークとして、以下も有用です：

```text
## PARD Framework
- P (Purpose): なぜこれを作るのか
- A (Approach): どのアプローチで解決するのか
- R (Result): 期待される成果
- D (Dependency): 依存性・リスク
```

### Reference: PRD Template Variations

業界・ステージによって、PRD テンプレートが異なります：

| テンプレート | 適用 | 特徴 |
|---------|------|------|
| **Lean PRD** | スタートアップ初期 | 1～3ページ、俊敏 |
| **Working Backwards** | アマゾン流 | プレスリリース中心 |
| **Full PRD** | 大企業・既成企業 | 100ページ以上、詳細 |
| **One-Pager** | Executive層向け | 1ページにまとめる |

**TaskFlow では Working Backwards (Lean版) を採用しています。**

---

## 🎓 振り返りクイズ

このレッスンで学んだ内容を振り返るために、簡単なクイズを用意しています：

```json
{
  "type": "AskQuestion",
  "question": "Working Backwards方式の特徴として、正しいものはどれですか？（複数選択可）",
  "options": [
    {
      "label": "顧客の視点から始まる",
      "value": "correct_1",
      "is_correct": true
    },
    {
      "label": "プレスリリースを最初に書く",
      "value": "correct_2",
      "is_correct": true
    },
    {
      "label": "技術仕様書から始まる",
      "value": "incorrect_1",
      "is_correct": false
    },
    {
      "label": "完成後に利用方法を考える",
      "value": "incorrect_2",
      "is_correct": false
    }
  ]
}
```

```json
{
  "type": "AskQuestion",
  "question": "MVP（Minimum Viable Product）の定義として、最適なものは？",
  "options": [
    {
      "label": "できるだけ多くの機能を詰め込んだ最初の版",
      "value": "wrong",
      "is_correct": false
    },
    {
      "label": "顧客に価値を提供できる最小限の機能セット",
      "value": "correct",
      "is_correct": true
    },
    {
      "label": "全ての計画された機能を含む版",
      "value": "wrong2",
      "is_correct": false
    }
  ]
}
```

```json
{
  "type": "AskQuestion",
  "question": "AAARRRフレームワークの「R」3つを挙げてください。（記述問題）",
  "hint": "Retention, Revenue, Referral",
  "expected_answer": "Retention（継続利用）, Revenue（収益）, Referral（紹介）"
}
```

---

**おめでとうございます！Lesson 18-3（PRD作成）が完了しました！**

次は Lesson 18-4 で、作成したPRDを複数の観点からレビューして、最終版を完成させます。

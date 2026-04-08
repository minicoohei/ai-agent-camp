---
description: "When the user says /start-16-8 — Module 16 Lesson 16-8: Resend Sequence & CLI でドリップキャンペーン自動化"
category: "lesson"
duration: "30分"
prerequisites: ["start-16-6", "start-16-7"]
level: "intermediate"
tags: ["email", "resend", "resend-cli", "sequences", "drip-campaign", "automation"]
---

# 🎓 Lesson 16-8: Resend Sequence & CLI でドリップキャンペーン

## 📍 このセッションでやること

**Lesson 16-8: Resend Sequence でドリップキャンペーン** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Resend Sequences でウェルカムシーケンスを作成し、CLI でコンタクト管理を自動化する |
| 所要時間 | 約30分 |
| 使うツール | Resend CLI (`resend-cli`), Resend Dashboard, email-sequence スキル |
| 前提条件 | Lesson 16-6 & Lesson 16-7 完了（ドメイン検証 & APIキー作成済み）|
| 教材ページ | [Module 16: メール自動化](https://ai-agent.camp/ja/course/module-16) を並行参照 |

**このセッションの流れ:**
1. シーケンスの概念と設計パターン
2. Resend Dashboard でシーケンスを作成
3. Resend CLI でコンタクト・Audience を管理
4. email-sequence スキルでテンプレート生成

セッション終了時には、自動化されたメールシーケンスが構築されています。

> **💡 ヒント**: Resend CLI でコンタクト管理を自動化すれば、新規登録ユーザーを自動的にシーケンスに追加できます。

---

## 🎯 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "previous_lesson", "label": "Lesson 16-7 をまずやりたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

---

## 🚀 Step 1: シーケンスの基本概念

**シーケンスとは？**
特定のトリガーをきっかけに、あらかじめ設定した間隔でメールを自動送信する仕組み。

**ウェルカムシーケンスの例:**
| メール | タイミング | 件名 | 目的 |
|--------|-----------|------|------|
| 1通目 | Day 0（即時） | ようこそ！始め方ガイド | 第一印象・サービス概要 |
| 2通目 | Day 3 | 使いこなしのコツ3選 | 主要機能の紹介 |
| 3通目 | Day 7 | 〇〇さんの活用事例 | 社会的証明 |
| 4通目 | Day 14 | フィードバックをお聞かせください | エンゲージメント |

**AskQuestion:**
```json
{
  "title": "📋 シーケンスタイプを選択",
  "questions": [{
    "id": "sequence_type",
    "prompt": "どのタイプのシーケンスを作りますか？",
    "options": [
      {"id": "welcome", "label": "ウェルカムシーケンス（新規登録者向け）"},
      {"id": "onboarding", "label": "オンボーディング（利用開始支援）"},
      {"id": "nurture", "label": "リードナーチャリング（見込み顧客育成）"},
      {"id": "custom", "label": "カスタム（自分で条件を指定）"}
    ]
  }]
}
```

---

## 🚀 Step 2: Resend Dashboard でシーケンスを作成

1. Resend ダッシュボード → **Sequences** → Create Sequence
2. シーケンス名を入力（例: "Welcome Series"）
3. トリガー条件を設定（例: Audience に追加された時）
4. メールステップを追加（件名、本文、送信間隔）

**email-sequence スキルでテンプレートを生成:**
```text
email-sequence スキルを使って、SaaS のウェルカムシーケンスを設計してください。

条件:
- 対象: 新規無料登録ユーザー
- メール数: 4通
- 期間: 14日間
- ゴール: プロダクトの定着と有料プランへの誘導
- トーン: フレンドリーで親しみやすい
```

---

## 🚀 Step 3: Resend CLI でコンタクト・Audience 管理

**Audience の作成:**
```bash
resend audiences create --name "Welcome Series"
```

**コンタクトの追加:**
```bash
resend contacts create \
  --audience-id <audience-id> \
  --email "user@example.com" \
  --first-name "Taro"
```

**コンタクト一覧の確認:**
```bash
resend contacts list --audience-id <audience-id>
```

**JSON 出力（自動化/スクリプト用）:**
```bash
resend contacts list --audience-id <audience-id> --json
```

> **💡 自動化のポイント**: 新規ユーザー登録時に Webhook → Resend CLI でコンタクトを自動追加すれば、シーケンスが自動的にスタートします。

---

## 🚀 Step 4: テスト送信とモニタリング

**テストコンタクトでシーケンスを実行:**
1. 自分のメールアドレスをコンタクトとして追加
2. シーケンスの初回メールが届くか確認
3. Resend ダッシュボードで配信状況をモニタリング

**配信メトリクスの確認ポイント:**
- 配信率（Delivery Rate）
- 開封率（Open Rate）
- クリック率（Click Rate）
- 配信停止率（Unsubscribe Rate）

---

## ⚠️ よくあるトラブルと解決方法

| トラブル | 解決策 |
|---------|--------|
| シーケンスが開始されない | Audience にコンタクトが正しく追加されているか確認 |
| メールが届かない | ドメイン検証を再確認。SPF/DKIM の設定をチェック |
| CLI で Audience が見つからない | `resend audiences list` で ID を確認 |
| テンプレートが意図通りにならない | email-sequence スキルに詳細な条件を追加して再生成 |

---

## ✅ チェックポイント

- [ ] シーケンスの設計パターンを理解した
- [ ] Resend Dashboard でシーケンスを作成した
- [ ] Resend CLI で Audience とコンタクトを管理できた
- [ ] テスト送信でシーケンスの動作を確認した


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/email/
├── index.html  (HTMLメール)
├── style.css
└── assets/
```

### 確認コマンド
```bash
# ファイル一覧
ls -lh output/email/

# ブラウザで開く（macOS: open / Linux: xdg-open）
open output/email/index.html
```

> 💡 HTMLの構造確認: `head -30 output/email/index.html`

---

## ✅ 完了チェック

```bash
uv run python tools/lesson_progress.py --check start-16-8
```

---

## ➡️ 次のステップ

**AskQuestion:**
```json
{
  "title": "🎉 Lesson 16-8 完了！",
  "questions": [{
    "id": "next_action",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-17-1）"},
      {"id": "practice", "label": "別のシーケンスも作ってみたい"},
      {"id": "review", "label": "Module 16 の概要を確認"},
      {"id": "end", "label": "今日はここまで"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-17-1
- practice → 別のシーケンスで実践
- review → Module 16 の振り返り
- end → 終了

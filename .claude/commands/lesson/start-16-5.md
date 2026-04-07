---
description: "When the user says /start-16-5 — Module 16 Lesson 16-5: メール自動化ワークフロー - GitHub Actions & 総合演習"
category: "lesson"
duration: "30分"
prerequisites: ["start-16-1", "start-16-2", "start-16-3"]
level: "advanced"
tags: ["email", "gmail", "gogcli", "github-actions", "automation"]
---

# 🎓 Lesson 16-5: メール自動化ワークフロー

## 📍 このセッションでやること

**Lesson 16-5: メール自動化ワークフロー** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GitHub Actions で定期メール送信を自動化し、Slack 連携通知を設定する |
| 所要時間 | 約30分 |
| 使うツール | gogcli (gog), check-inbox, GitHub Actions |
| 前提条件 | Lesson 16-1〜Lesson 16-3 完了 |
| 教材ページ | [Module 16: メール自動化](https://ai-agent.camp/ja/course/module-16) を並行参照 |

**このセッションの流れ:**
1. メール自動化の全体像を設計
2. GitHub Actions ワークフローを作成
3. Slack 連携通知を設定
4. 総合演習（全スキル統合）

セッション終了時には、メール業務の自動化パイプラインが構築されています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

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
      {"id": "previous_lesson", "label": "前のレッスンをまずやりたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

---

## 🚀 Step 1: メール自動化の全体像

GitHub Actions + gogcli で構築する自動化パイプライン:

```text
┌─────────────────────────────────────────┐
│         GitHub Actions (cron)           │
│  ┌─────────────┐  ┌─────────────────┐  │
│  │ google-sync  │→│  check-inbox    │  │
│  │ メール同期   │  │  タスク抽出     │  │
│  └─────────────┘  └──────┬──────────┘  │
│                          │              │
│  ┌─────────────┐  ┌──────▼──────────┐  │
│  │ gog send    │←│  返信ドラフト    │  │
│  │ メール送信   │  │  レビュー・承認  │  │
│  └──────┬──────┘  └─────────────────┘  │
│         │                               │
│  ┌──────▼──────────────────────────┐   │
│  │ Slack 通知（処理結果サマリー）    │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 🚀 Step 2: GitHub Actions ワークフローの設計

**ワークフロー例を設計:**

```text
以下の要件で GitHub Actions ワークフローを設計してください:

1. トリガー: 毎朝9時（JST）に実行
2. ステップ:
   a. google-sync でメール同期
   b. check-inbox でタスク抽出
   c. 結果をサマリーとして出力
   d. Slack に通知
3. 環境変数: GOOGLE_CREDENTIALS（Secret）
```

**AskQuestion:**
```json
{
  "title": "📋 ワークフローのカスタマイズ",
  "questions": [{
    "id": "workflow_type",
    "prompt": "どのタイプの自動化を構築しますか？",
    "options": [
      {"id": "daily_check", "label": "毎朝のメールチェック & タスク抽出"},
      {"id": "auto_reply", "label": "特定条件でのメール自動返信"},
      {"id": "report", "label": "週次メールレポートの自動送信"},
      {"id": "custom", "label": "カスタムワークフロー（条件を指定）"}
    ]
  }]
}
```

---

## 🚀 Step 3: Slack 連携通知の設定

メール処理の結果を Slack に通知します。

**Slack Webhook の設定:**
1. Slack App の Incoming Webhook を設定
2. Webhook URL を GitHub Secrets に保存
3. ワークフロー内で `curl` で通知を送信

**通知メッセージの例:**
```json
{
  "text": "📧 メール日次レポート\n- 未読: 5通\n- 要返信: 2通\n- タスク: 3件\n\n詳細: <URL>"
}
```

---

## 🚀 Step 4: 総合演習

Module 16 で学んだすべてのスキルを統合した演習です。

**演習課題:**

```text
以下のメール業務自動化パイプラインを構築してください:

1. gogcli で受信メールを取得
2. check-inbox でタスクを抽出し、優先度を判定
3. 高優先度のメールに対して返信ドラフトを生成
4. --dry-run で送信内容を確認
5. 確認後、gogcli で返信を送信
6. 処理結果を Slack に通知
```

**AskQuestion:**
```json
{
  "title": "🏆 総合演習の進め方",
  "questions": [{
    "id": "exercise_approach",
    "prompt": "総合演習をどのように進めますか？",
    "options": [
      {"id": "guided", "label": "ガイド付きで一緒に進める"},
      {"id": "independent", "label": "自分で挑戦してみる"},
      {"id": "skip", "label": "演習をスキップして振り返りへ"},
      {"id": "partial", "label": "一部だけ試したい"}
    ]
  }]
}
```

---

## ⚠️ よくあるトラブルと解決方法

| トラブル | 解決策 |
|---------|--------|
| GitHub Actions でクレデンシャルエラー | Secrets に正しい値が設定されているか確認 |
| cron が実行されない | cron 構文を確認（UTC注意: JST 9:00 = UTC 0:00） |
| Slack 通知が届かない | Webhook URL が正しいか確認 |
| gogcli がCI環境で動かない | `gog` のバイナリが PATH に含まれているか確認 |

---

## ✅ チェックポイント

- [ ] メール自動化のワークフローを設計できた
- [ ] GitHub Actions の YAML ファイルが作成できた
- [ ] Slack 通知の仕組みを理解した
- [ ] 総合演習で全スキルを統合的に使用できた


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
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

---

## ➡️ 次のステップ

**AskQuestion:**
```json
{
  "title": "🎉 Module 16 全レッスン完了！",
  "questions": [{
    "id": "next_action",
    "prompt": "おめでとうございます！次に何をしますか？",
    "options": [
      {"id": "next_module", "label": "Module 14 へ → 記事作成"},
      {"id": "review_all", "label": "Module 16 を振り返りたい"},
      {"id": "home", "label": "ホームに戻る"},
      {"id": "end", "label": "今日はここまで"}
    ]
  }]
}
```

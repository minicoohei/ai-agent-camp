---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
duration: "約20分"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["lp", "copywriting", "persona", "brief"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 13-1: 訴求の整理（ヒアリング & コピーライティング）

## 📍 このセッションでやること

**Lesson 13-1: 訴求の整理** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | AskQuestionでヒアリングし、ペルソナ・訴求軸・コピーを整理してLP制作の土台を作る |
| 所要時間 | 約20分 |
| 使うスキル | 選択肢付きの対話フロー, lp-designer スキル |
| 前提条件 | Lesson 0-1 完了、ai-agent-camp を開いている |
| 教材ページ | [Module 13: LP/HP制作](https://ai-agent.camp/ja/course/module-13) を並行参照 |

**このセッションの流れ:**
1. LP/HPの種別とサービス情報のヒアリング
2. ターゲットペルソナの定義
3. ベネフィット・コピーの生成
4. セクション構成案の策定

セッション終了時には、LP制作に必要な訴求ブリーフが完成しています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。ツールによって応答が途中で止まることがありますが、故障ではありません。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

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

## 🚀 Step 1: プロジェクト種別のヒアリング

まずはどんなページを作るか決めましょう。AskQuestionToolでヒアリングします。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: どんなページを作りますか？",
  "questions": [
    {
      "id": "project_type",
      "prompt": "作成するページの種類を選んでください",
      "options": [
        {"id": "lp", "label": "LP（ランディングページ）- 1つのCTAに集中"},
        {"id": "hp", "label": "HP（ホームページ）- 複数セクション構成"},
        {"id": "product", "label": "プロダクトページ - 機能紹介中心"},
        {"id": "event", "label": "イベント/キャンペーンページ"}
      ]
    },
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
    }
  ]
}
```

**選択後**: ユーザーの選択に基づいて、具体的なサービス情報を自由入力で確認します。

以下の情報を入力してください:
```text
作成するLP/HPについて教えてください：

1. サービス名（正式名称）:
2. サービスの概要（1-2文で）:
3. 一番伝えたいこと:
4. 参考にしたいサイトのURL（あれば）:
```

**期待される結果**: サービスの基本情報が収集されます。

---

## 🚀 Step 2: ターゲットペルソナの定義

次に、誰に向けたページかを明確にします。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: ターゲットペルソナ",
  "questions": [
    {
      "id": "target_age",
      "prompt": "メインターゲットの年齢層は？",
      "options": [
        {"id": "20s", "label": "20代"},
        {"id": "30s", "label": "30代"},
        {"id": "40s", "label": "40代"},
        {"id": "50plus", "label": "50代以上"},
        {"id": "all", "label": "幅広い年齢層"}
      ]
    },
    {
      "id": "target_role",
      "prompt": "ターゲットの主な職種・立場は？",
      "options": [
        {"id": "executive", "label": "経営者・役員"},
        {"id": "manager", "label": "部長・マネージャー"},
        {"id": "marketer", "label": "マーケター・広報"},
        {"id": "engineer", "label": "エンジニア・技術者"},
        {"id": "sales", "label": "営業・セールス"},
        {"id": "individual", "label": "個人・一般消費者"},
        {"id": "other", "label": "その他"}
      ]
    },
    {
      "id": "cta_goal",
      "prompt": "CTAの目的は？（ユーザーにしてほしいアクション）",
      "options": [
        {"id": "signup", "label": "無料登録・アカウント作成"},
        {"id": "inquiry", "label": "問い合わせ・相談"},
        {"id": "download", "label": "資料ダウンロード"},
        {"id": "purchase", "label": "購入・申し込み"},
        {"id": "trial", "label": "無料トライアル開始"},
        {"id": "event", "label": "イベント参加申し込み"}
      ]
    }
  ]
}
```

**選択後**: ペルソナの課題（ペインポイント）を確認します。

追加で入力してください:
```text
ターゲットが抱えている課題を3つ挙げてください:

1. 一番大きな課題:
2. 日常的に感じている不満:
3. 解決したいけど諦めていること:
```

**期待される結果**: 明確なペルソナ像が定義されます。

---

## 🚀 Step 3: ベネフィット・コピーの生成

ヒアリング結果をもとに、訴求コピーを生成します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: デザインのトーン選択",
  "questions": [{
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
  }]
}
```

**選択後の案内**:

AIが以下を自動生成します:
```text
Step 1〜2 のヒアリング結果をもとに、以下を生成してください:

## ベネフィット3点
1. メインベネフィット（最大の価値）
2. サブベネフィット1（効率化・時短）
3. サブベネフィット2（安心感・サポート）

## コピー案
- ヘッドライン（H1）: 15文字以内のインパクトあるコピー
- サブヘッドライン: 30文字以内の補足説明
- CTA文言: 7文字以内のアクション文言
- CTA補足: CTAボタン下の安心テキスト（例: 無料・クレカ不要）

3パターン生成してください。
```

**期待される結果**: 3パターンのコピー案が生成されます。

---

## 🚀 Step 4: セクション構成案の策定

コピーをもとに、LPのセクション構成を決定します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: セクション構成",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
ここまでのヒアリング結果（サービス情報、ペルソナ、ベネフィット、コピー）を
output/lp-brief.md にまとめてください。

以下のフォーマットで出力:

# LP ブリーフ: {サービス名}

## ペルソナ
- 名前: {仮名}
- 年齢: {年齢}
- 職種: {職種}
- 課題: {課題3点}

## 訴求軸
1. {メインベネフィット}
2. {サブベネフィット1}
3. {サブベネフィット2}

## コピー（採用案）
- ヘッドライン: {選択したコピー}
- サブヘッドライン: {選択したコピー}
- CTA: {選択したCTA}

## セクション構成
1. Hero - ヘッドライン + CTA
2. Pain Points - 課題提起 3点
3. Solution - ソリューション紹介
4. Features - 機能/特徴 3-4点
5. Social Proof - 実績/お客様の声
6. FAQ - よくある質問 3-5個
7. Final CTA - 最終アクション

## デザイントーン
{選択したトーン}
```

**期待される結果**: `output/lp-brief.md` にブリーフが保存されます。

---

## ⚠️ よくあるトラブルと解決方法

Codex では通常チャットで選択肢を提示しながらでトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "何を入力すればいいかわからない"},
      {"id": "trouble_2", "label": "コピーがしっくりこない"},
      {"id": "trouble_3", "label": "セクション構成に迷う"},
      {"id": "trouble_4", "label": "出力ファイルが生成されない"}
    ]
  }]
}
```

### トラブル1: 何を入力すればいいかわからない
**解決策**: 架空のサービスでOKです。「AIを使ったLP自動生成サービス」など、身近な例で進めましょう。

### トラブル2: コピーがしっくりこない
**解決策**: 「もっとカジュアルに」「数字を入れて」「緊急感を出して」と指示すると再生成できます。

### トラブル3: セクション構成に迷う
**解決策**: 基本構成（Hero → Pain → Solution → Features → Proof → CTA）から始めて、後で追加・削除できます。

### トラブル4: 出力ファイルが生成されない
**解決策**: `output/` ディレクトリが存在するか確認してください。なければ `mkdir -p output` で作成します。

---

## ✅ チェックポイント
- [ ] サービスの種別・カテゴリが決まっている
- [ ] ターゲットペルソナが定義されている
- [ ] ベネフィット3点が明確
- [ ] ヘッドライン・CTA文言が決まっている
- [ ] セクション構成案がある
- [ ] `output/lp-brief.md` が生成されている


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/
└── lp-brief.md  (LP企画ブリーフ)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/lp-brief.md

# 冒頭を確認（最初の30行）
head -30 output/lp-brief.md
```

> 💡 全文を確認: `cat output/lp-brief.md` で全文表示できます

---

## ✅ 完了チェック
以下をCodexのチャットに入力して、完了状況を確認してください:

```text
output/lp-brief.md の内容を確認し、ペルソナ・訴求軸・コピー・セクション構成が
すべて埋まっているかチェックしてください。
```

**期待される結果**: ブリーフの完成度が確認されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。次のセクションを始めるか、新しいウィンドウを開いて、新しいセクションを開始してください。

Codex では通常チャットで選択肢を提示しながらで選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクション（WF作成）を開始"},
      {"id": "next_window", "label": "新しいウィンドウで /start-13-2 を開始"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-13-2 を実行
- next_window → 新しいウィンドウで /start-13-2
- finish → 終了

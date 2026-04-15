---
description: "Lesson command"
category: "lesson"
chapter: "courses/aiagent/lesson03-core/module19-outlook-windows"
duration: "約35分"
prerequisites: ["start-19-1"]
level: "intermediate"
tags: ["outlook", "microsoft365", "rules", "folders", "categories"]
---

# 🎓 Lesson 19-2: フォルダ・ルール・カテゴリ

## 📍 このセッションでやること

**Lesson 19-2: フォルダ・ルール・カテゴリ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Outlook のフォルダ設計・ルール・カテゴリを使ってメール整理を自動化する |
| 所要時間 | 約35分 |
| 使うスキル | Outlook ルール設定、カテゴリ管理、m365 CLI |
| 前提条件 | Lesson 19-1 完了（m365 CLI 認証セットアップ済み） |
| 教材ページ | [Module 19: Outlook](https://ai-agent.camp/ja/course/module-19) を並行参照 |

> **💡 ツール情報**: このレッスンでは m365 CLI を使用します。Cursor IDE、Claude Code（CLI/デスクトップ）のいずれでも利用可能です。Codex CLI 等の一部環境では `request_user_input is not supported` エラーが出る場合があります。その場合は「代替ワークフロー」セクションを参照してください。

**このセッションの流れ:**
1. 受信トレイに留めすぎないフォルダ設計を学ぶ
2. ルールの条件と処理（移動・カテゴリ付与など）を設定する
3. カテゴリで横断的にタグ付けする方法を理解する
4. 整理ルールを適用した後、m365 CLI でメール一覧・送信を自動化する
5. 設定結果を output/outlook/ に記録・保存する

セッション終了時には、Outlook のフォルダ・ルール・カテゴリを活用した受信トレイの整理と、m365 CLI による自動化ができるようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

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

## 🚀 Step 1: 受信トレイに留めすぎないフォルダ設計

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: フォルダ設計の基本",
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
```
Outlook のフォルダ設計のベストプラクティスを教えてください。以下の内容を説明してください：

1. フォルダ設計の基本方針:
   - 受信トレイはゼロを目指す（Inbox Zero）
   - 階層は2段階まで（深すぎると管理困難）
   - アクション軸とプロジェクト軸の使い分け

2. 推奨フォルダ構成の例:
   - 📁 01_アクション必要（要対応メール）
   - 📁 02_待ち（返信待ち・承認待ち）
   - 📁 03_参照（読むだけ・情報メール）
   - 📁 04_プロジェクト/（プロジェクト別サブフォルダ）
   - 📁 05_アーカイブ/（月別・年別）

3. m365 CLI でフォルダ一覧を取得:
   m365 outlook mail folder list
```

**期待される結果**: フォルダ設計の方針を理解し、現在のフォルダ構成を確認できます。

---

## 🚀 Step 2: ルールの条件と処理（移動・カテゴリ付与）

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: ルールの条件と処理",
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
```
Outlook のルール設定方法を教えてください。以下の内容を説明してください：

1. ルールの基本構成:
   - 条件（Condition）: いつルールが発動するか
   - 処理（Action）: 条件に合致した時に何をするか
   - 例外（Exception）: ルールを適用しない場合

2. よく使う条件:
   - 差出人（from）で振り分け
   - 件名（subject）にキーワードを含む
   - 宛先（to/cc）で自分がCCの場合
   - ドメイン別（@company.com など）

3. よく使う処理:
   - 特定フォルダへ移動
   - カテゴリを付与
   - 重要度を変更
   - フラグを付ける
   - 通知を表示

4. 実践: 以下のルールを Outlook で作成
   - ルール1: 社内メール（@自社ドメイン）→ 「社内」カテゴリ付与
   - ルール2: ニュースレター → 「03_参照」フォルダへ移動
   - ルール3: 上司からのメール → 重要度「高」に設定

5. 設定結果を output/outlook/rules-config.json に記録
```

**期待される結果**: Outlook にルールが3つ作成され、条件に応じた自動振り分けが設定されます。

---

## 🚀 Step 3: カテゴリで横断的にタグ付け

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: カテゴリで横断的にタグ付け",
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
```
Outlook のカテゴリ機能を使った横断的なタグ付けを設定してください。

手順:
1. カテゴリの基本概念:
   - フォルダ = 1つのメールは1つのフォルダにしか入れない
   - カテゴリ = 1つのメールに複数のタグを付けられる
   - フォルダで「場所」、カテゴリで「性質」を管理

2. カテゴリの設計例:
   - 🔴 緊急（赤）: 今日中に対応が必要
   - 🟡 今週（黄）: 今週中に対応
   - 🟢 情報（緑）: 読むだけ
   - 🔵 プロジェクトA（青）: プロジェクトA関連
   - 🟣 プロジェクトB（紫）: プロジェクトB関連

3. m365 CLI でカテゴリ一覧を確認:
   m365 outlook mail list --top 10 --query "categories/any(c:c eq '緊急')"

4. カテゴリとフォルダの組み合わせルールを設計
5. 設定結果を output/outlook/categories-config.json に記録
```

**期待される結果**: カテゴリが設定され、フォルダとの組み合わせで効率的なメール管理体制が構築されます。

---

## 🚀 Step 4: m365 CLI でメール一覧・送信の自動化

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: m365 CLI で一覧・送信自動化",
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
```
m365 CLI を使って、整理後のメール一覧取得と送信を自動化してください。

手順:
1. mkdir -p output/outlook

2. フォルダ別メール一覧の取得:
   # 受信トレイのメール一覧
   m365 outlook mail list --top 20 --output json > output/outlook/inbox-list.json

   # 特定フォルダのメール一覧
   m365 outlook mail folder list --output json

3. フィルタ付き取得:
   # 未読メールのみ
   m365 outlook mail list --filter "isRead eq false" --output json

   # 特定カテゴリのメール
   m365 outlook mail list --filter "categories/any(c:c eq '緊急')" --output json

4. メール送信の自動化:
   m365 outlook mail send \
     --to "colleague@example.com" \
     --subject "週次レポート" \
     --bodyContents "今週のレポートを添付します。" \
     --bodyContentType Text

5. 結果を output/outlook/automation-result.json に保存
```

**期待される結果**: m365 CLI でメール一覧取得と送信が自動化され、output/outlook/ に結果が保存されます。

---

## 🚀 Step 5: 設定結果の確認と記録

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 設定結果の確認と記録",
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
```
これまでの設定結果を確認し、まとめを作成してください。

手順:
1. 作成したフォルダ構成を一覧表示
2. 設定したルールの一覧と各ルールの条件・処理を確認
3. カテゴリの設計と運用ルールを確認
4. 以下の内容を output/outlook/summary.md にまとめる:
   - フォルダ構成
   - ルール設定（条件 → 処理）
   - カテゴリ設計
   - m365 CLI 自動化コマンド一覧
5. 今後の運用改善ポイントを3つ提示
```

**期待される結果**: output/outlook/ にフォルダ・ルール・カテゴリの設定まとめが保存されます。

---

## ⚠️ よくあるトラブルと解決方法

AskUserQuestion（AskQuestion）でトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "m365 CLI の認証が切れた"},
      {"id": "trouble_2", "label": "ルールが期待通りに動作しない"},
      {"id": "trouble_3", "label": "カテゴリが表示されない"},
      {"id": "trouble_4", "label": "メール送信でエラーが出る"}
    ]
  }]
}
```


### トラブル1: 「m365 CLI の認証が切れた」
**原因**: アクセストークンの有効期限切れ
**解決プロンプト**:
```
m365 login コマンドで再認証してください。
m365 status で現在の認証状態を確認できます。
トークンが期限切れの場合は再度ブラウザ認証が必要です。
```

### トラブル2: 「ルールが期待通りに動作しない」
**原因**: ルールの条件設定が不正、またはルールの優先順位の問題
**解決プロンプト**:
```
Outlook のルール設定画面で条件と処理を再確認してください。
ルールは上から順に適用されるため、優先順位を確認してください。
「処理後にルールの処理を中止する」オプションが有効になっているか確認してください。
```

### トラブル3: 「カテゴリが表示されない」
**原因**: カテゴリが作成されていない、またはフィルタのクエリが不正
**解決プロンプト**:
```
Outlook の設定 → カテゴリ管理でカテゴリが作成されているか確認してください。
m365 CLI のフィルタ構文が正しいか確認してください。
カテゴリ名は完全一致で指定する必要があります。
```

### トラブル4: 「メール送信でエラーが出る」
**原因**: 権限不足、または送信パラメータの不正
**解決プロンプト**:
```
m365 CLI に Mail.Send 権限が付与されているか確認してください。
--to パラメータに有効なメールアドレスを指定しているか確認してください。
--bodyContentType は Text または HTML を指定できます。
```

---

## ✅ チェックポイント
- [ ] フォルダ設計の方針を理解し、フォルダ構成を確認できた
- [ ] ルールの条件と処理を設定し、自動振り分けができた
- [ ] カテゴリで横断的にタグ付けする方法を理解できた
- [ ] m365 CLI でメール一覧取得と送信を自動化できた
- [ ] output/outlook/ に設定結果が保存された


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/outlook/
├── inbox-list.json            ← 受信トレイメール一覧
├── rules-config.json          ← ルール設定の記録
├── categories-config.json     ← カテゴリ設定の記録
├── automation-result.json     ← m365 CLI 自動化結果
└── summary.md                 ← 設定まとめ
```
> 形式: JSON / Markdown

### 確認コマンド
```bash
# 出力ファイルの確認
ls -lh output/outlook/

# メール一覧の確認
cat output/outlook/inbox-list.json | jq '.[:3]'

# まとめの確認
cat output/outlook/summary.md
```

> 💡 **Claude Code**: `Read output/outlook/summary.md` でチャット内プレビュー
> 💡 **Cursor**: ファイルエクスプローラーでファイルをクリックしてプレビュー

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_module", "label": "Module 20 に進む（/start-20-1）"},
      {"id": "review_module", "label": "Module 19を復習する"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_module → /start-20-1 で Module 20 へ
- review_module → Module 19の各レッスンを振り返る
- finish → 終了

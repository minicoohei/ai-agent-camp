---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "約30分"
prerequisites: ["start-17-4"]
level: "intermediate"
tags: ["marketing", "typefully", "x", "threads", "sns", "api"]
---

# 🎓 Lesson 17-5: Typefully で X/Threads 投稿自動化

## 📍 このセッションでやること

**Lesson 17-5: Typefully で X/Threads 投稿自動化** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Typefully API v2 を使って X（Twitter）と Threads への投稿を自動化する |
| 所要時間 | 約30分 |
| 使うスキル | Typefully API v2（social set 取得・ドラフト作成・スケジュール・スレッド投稿） |
| 前提条件 | Typefully アカウント作成済み、APIキー取得済み |
| 教材ページ | [Module 17: マーケティング](https://ai-agent.camp/ja/course/module-17) を並行参照 |

> **💡 ツール情報**: このレッスンでは Typefully API v2 を使用します。Cursor IDE、Claude Code（CLI/デスクトップ）のいずれでも利用可能です。Codex CLI 等の一部環境では `request_user_input is not supported` エラーが出る場合があります。その場合は「代替ワークフロー」セクションを参照してください。

> **⚠️ API バージョン**: 2025年以降、Typefully API は v2 に移行しました。v1 の `x-api-key` ヘッダーと `/v1/drafts/` エンドポイントは非推奨です。このレッスンでは v2（`Authorization: Bearer` ヘッダー + `/v2/social-sets/{id}/drafts` エンドポイント）を使います。

**このセッションの流れ:**
1. Typefully API の概要を理解し、アカウント・APIキー・social_set_id を取得する
2. ドラフトを作成し、スケジュール投稿を設定する
3. X（Twitter）と Threads への同時投稿を試す
4. スレッド形式の連続投稿を自動化する
5. 投稿結果を確認し、output/typefully/ に記録を保存する

セッション終了時には、Typefully API v2 経由でドラフト作成・スケジュール投稿・スレッド自動投稿ができるようになっています。

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

## 🚀 Step 1: Typefully API v2 の概要とアカウント設定

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Typefully API v2 の概要とアカウント設定",
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
Typefully API v2 の概要を教えてください。以下の内容を説明してください：

1. Typefully とは — X（Twitter）/ Threads の投稿管理・スケジュールツール
2. API v2 でできること — social set 取得、ドラフト作成、スケジュール設定、スレッド投稿、プラットフォーム別投稿
3. アカウント設定手順:
   a. https://typefully.com でアカウントを作成
   b. X（Twitter）アカウントを連携
   c. Threads アカウントを連携（対応している場合）
4. APIキーの取得:
   a. Typefully の Settings → Integrations → API & Integrations
   b. API Key を生成してコピー
5. APIキーを環境変数に設定:
   export TYPEFULLY_API_KEY="your-api-key-here"
6. social_set_id の取得（v2 では必須）:

curl -X GET "https://api.typefully.com/v2/social-sets" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY"

   レスポンスから使いたい social set の id を控えてください:
   export TYPEFULLY_SOCIAL_SET_ID="取得した値"
```

**期待される結果**: Typefully の概要を理解し、API キーと social_set_id の設定が完了します。

---

## 🚀 Step 2: ドラフト作成・スケジュール設定

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: ドラフト作成・スケジュール設定",
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
Typefully API v2 を使ってドラフトを作成し、スケジュール投稿を設定してください。

手順:
1. mkdir -p output/typefully
2. 以下の curl コマンドでドラフトを作成（v2 エンドポイント）:

curl -X POST "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/drafts" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "x": {
        "enabled": true,
        "posts": [
          {"text": "AIエージェントで業務効率が劇的に変わる！\n\n非エンジニアでも使える実践テクニックを公開中。\n\n#AIAgent #業務効率化"}
        ]
      }
    },
    "publish_at": "next-free-slot"
  }'

3. レスポンスの draft ID を記録
4. スケジュール設定の確認（publish_at: "next-free-slot" / ISO8601 形式の日時指定）
5. 結果を output/typefully/draft-result.json に保存
```

**期待される結果**: Typefully にドラフトが作成され、スケジュールが設定されます。

---

## 🚀 Step 3: X（Twitter）と Threads への同時投稿

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: X と Threads への同時投稿",
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
Typefully API v2 で X（Twitter）と Threads の両方に同時投稿するドラフトを作成してください。

手順:
1. platforms.x と platforms.threads を両方 enabled にして投稿先を指定:

curl -X POST "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/drafts" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "x": {
        "enabled": true,
        "posts": [
          {"text": "Typefully API v2 から自動投稿テスト！\n\nX と Threads に同時配信しています。\n\n#自動投稿 #TypefullyAPI"}
        ]
      },
      "threads": {
        "enabled": true,
        "posts": [
          {"text": "Typefully API v2 から自動投稿テスト！\n\nX と Threads に同時配信しています。\n\n#自動投稿 #TypefullyAPI"}
        ]
      }
    },
    "publish_at": "next-free-slot"
  }'

2. Typefully ダッシュボードで投稿先（X / Threads）を確認
3. 同時投稿の結果を output/typefully/multi-post-result.json に保存
4. 投稿先ごとの文字数制限やフォーマットの違いを確認（X: 280文字、Threads: 500文字）
```

**期待される結果**: X と Threads の両方に同時投稿するドラフトが作成されます。

---

## 🚀 Step 4: スレッド形式の連続投稿自動化

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: スレッド形式の連続投稿自動化",
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
Typefully API v2 でスレッド形式の連続投稿を作成してください。

手順:
1. v2 では posts 配列に複数エントリを並べるとスレッドになります（v1 の threadify + 改行4つの仕様は廃止）:

curl -X POST "https://api.typefully.com/v2/social-sets/$TYPEFULLY_SOCIAL_SET_ID/drafts" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": {
      "x": {
        "enabled": true,
        "posts": [
          {"text": "【AIエージェント活用ガイド 1/3】\n\nAIエージェントとは、指示に基づいて自律的にタスクを実行するAIです。"},
          {"text": "【2/3】\n\n具体的な活用例:\n- メール自動返信\n- スケジュール管理\n- データ分析レポート作成"},
          {"text": "【3/3】\n\n始め方は簡単！\nまずは1つの業務から試してみましょう。\n\n詳しくはプロフィールのリンクから👇"}
        ]
      }
    },
    "publish_at": "next-free-slot"
  }'

2. スレッドの各ツイートが posts 配列の順で分割されているか確認
3. 結果を output/typefully/thread-result.json に保存
```

**期待される結果**: 3つのツイートからなるスレッドがドラフトとして作成されます。

---

## 🚀 Step 5: 投稿結果の確認と記録

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 投稿結果の確認と記録",
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
これまでの投稿結果を確認し、まとめを作成してください。

手順:
1. Typefully ダッシュボードで作成済みドラフト一覧を確認
2. 各ドラフトのステータス（下書き / スケジュール済み / 投稿済み）を確認
3. 以下の内容を output/typefully/summary.md にまとめる:
   - 作成したドラフト数
   - スケジュール設定の内容（publish_at）
   - 投稿先（platforms.x / platforms.threads）
   - スレッド投稿の構成（posts 配列の要素数）
4. 今後の自動化に向けた改善ポイントを3つ提示
```

**期待される結果**: output/typefully/ に投稿結果のまとめが保存されます。

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
      {"id": "trouble_1", "label": "APIキーが認証エラーになる"},
      {"id": "trouble_2", "label": "social_set_id がわからない"},
      {"id": "trouble_3", "label": "ドラフト作成でエラーが出る"},
      {"id": "trouble_4", "label": "スレッドが正しく分割されない"},
      {"id": "trouble_5", "label": "Threads への投稿が反映されない"}
    ]
  }]
}
```


### トラブル1: 「APIキーが認証エラーになる」
**原因**: APIキーが無効、または v2 では `Authorization: Bearer` ヘッダー形式を使う必要がある（v1 の `x-api-key` は非推奨）
**解決プロンプト**:
```
環境変数 TYPEFULLY_API_KEY が正しく設定されているか確認してください。
[[ -n "$TYPEFULLY_API_KEY" ]] && echo "設定済み" || echo "未設定" で存在を確認し、
Typefully の Settings → API & Integrations で有効なキーか照合してください。
v2 では "Authorization: Bearer $TYPEFULLY_API_KEY" の形式を必ず使ってください。
```

### トラブル2: 「social_set_id がわからない」
**原因**: v2 エンドポイントは social_set_id が URL パスに必要
**解決プロンプト**:
```
以下のコマンドで利用可能な social set 一覧を取得してください:

curl -X GET "https://api.typefully.com/v2/social-sets" \
  -H "Authorization: Bearer $TYPEFULLY_API_KEY"

レスポンスの中から使いたい social set の id を控え、
export TYPEFULLY_SOCIAL_SET_ID="取得した値" で環境変数に設定してください。
```

### トラブル3: 「ドラフト作成でエラーが出る」
**原因**: リクエストボディの JSON 形式が不正、または v2 の必須フィールド（platforms）が不足
**解決プロンプト**:
```
curl コマンドの JSON ボディを確認してください。
v2 では platforms.{x|threads}.{enabled, posts} が必須です。
posts は配列で、各要素に text フィールドが必要です。
Content-Type: application/json ヘッダーが含まれているか確認してください。
jq でレスポンスを整形すると原因が特定しやすくなります。
```

### トラブル4: 「スレッドが正しく分割されない」
**原因**: v2 では posts 配列で分割する（v1 の改行4つ / threadify は廃止）
**解決プロンプト**:
```
v2 ではスレッドは posts 配列の要素数で決まります。
{"posts": [{"text": "1つ目"}, {"text": "2つ目"}]} のように並べてください。
v1 の threadify パラメータや改行4つ（\n\n\n\n）の区切り仕様は v2 では動作しません。
```

### トラブル5: 「Threads への投稿が反映されない」
**原因**: Threads アカウントが Typefully に連携されていない、または platforms.threads.enabled が false
**解決プロンプト**:
```
Typefully の Settings → Accounts で Threads アカウントが
連携されているか確認してください。
リクエストボディで platforms.threads.enabled: true と
platforms.threads.posts に最低1件の投稿が含まれているか確認してください。
Threads の API 対応状況はTypefullyの最新ドキュメントも確認してください。
```

---

## ✅ チェックポイント
- [ ] Typefully API v2 の概要を理解し、APIキーと social_set_id を設定できた
- [ ] ドラフトを作成し、スケジュール投稿を設定できた
- [ ] X（Twitter）と Threads への同時投稿を試せた
- [ ] スレッド形式の連続投稿を自動化できた（posts 配列）
- [ ] output/typefully/ に投稿結果が保存された


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/typefully/
├── draft-result.json          ← 単発ドラフト作成結果
├── multi-post-result.json     ← X/Threads 同時投稿結果
├── thread-result.json         ← スレッド投稿結果
└── summary.md                 ← 投稿結果まとめ
```
> 形式: JSON / Markdown

### 確認コマンド
```bash
# 出力ファイルの確認
ls -lh output/typefully/

# ドラフト結果の確認
cat output/typefully/draft-result.json | jq .

# まとめの確認
cat output/typefully/summary.md
```

> 💡 **Claude Code**: `Read output/typefully/summary.md` でチャット内プレビュー
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

これでModule 17: マーケティングの全レッスンが完了です！

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_module", "label": "次のモジュールを開始（/start-18-1）"},
      {"id": "review_module", "label": "Module 17を復習する"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_module → /start-18-1 で 要件定義/システム開発モジュールへ
- review_module → Module 17の各レッスンを振り返る
- finish → 終了

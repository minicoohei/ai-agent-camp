---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
duration: "約25分"
prerequisites: ["start-12-4"]
level: "intermediate"
tags: ["notion", "ncli", "update", "write"]
---

# 🎓 Lesson 12-5: 書き込みと更新

## 📍 このセッションでやること

**Lesson 12-5: 書き込みと更新** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | ncli で既存のNotionページ・DBエントリを更新し、ページの移動・編集を行う |
| 所要時間 | 約25分 |
| 使うスキル | ncli (Notion CLI) |
| 前提条件 | Lesson 12-4 完了（ページ・DB作成ができる状態） |

**このセッションの流れ:**
1. サンドボックスページの準備
2. プロパティの更新
3. 本文の追記・編集
4. ページの移動
5. 変更の検証

セッション終了時には、既存のNotionコンテンツを自由に更新・編集できるようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

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
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → Lesson 12-4 で作成したページ・DBが存在するか確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: サンドボックスページの準備

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: サンドボックスページの準備",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする（既存ページを使う）"}
    ]
  }]
}
```

**AIが実行すること:**

1. 更新テスト用のサンドボックスページを作成:
   ```bash
   ncli page create --title "更新テスト用サンドボックス" --body "# 初期コンテンツ

このページは ncli の更新テスト用です。

## セクション1
- 項目A
- 項目B

## セクション2
ここに追記していきます。"
   ```

2. 作成されたページのIDとURLを記録する。

3. テスト用のサブページも作成（移動テスト用）:
   ```bash
   ncli page create --title "移動テスト用ページ" --body "このページを別の場所に移動するテストです。"
   ```

4. Lesson 12-4 で作成したタスク管理DBのURLも確認:
   ```bash
   ncli search "タスク管理"
   ```

**期待される結果**: サンドボックスページとサブページが作成され、テスト準備が完了する。

---

## 🚀 Step 2: プロパティの更新（ncli page update）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: プロパティの更新",
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

**AIが実行すること:**

1. まず更新前の状態を確認:
   ```bash
   ncli fetch <タスクページID>
   ```

2. タスク管理DBのエントリを更新（ステータス変更）:
   ```bash
   ncli page update <タスクページID> --prop "Status=Done"
   ```

3. 複数プロパティを同時に更新:
   ```bash
   ncli page update <タスクページID> --prop "Status=InProgress" --prop "Priority=High"
   ```

4. 更新後の状態を確認して変更前後を比較:
   ```bash
   ncli fetch <タスクページID>
   ```

5. 変更前後の比較結果を表示:

   | プロパティ | 変更前 | 変更後 |
   |-----------|--------|--------|
   | Status | Open | InProgress |
   | Priority | Medium | High |

**期待される結果**: プロパティが正しく更新され、変更前後の差分が確認できる。

---

## 🚀 Step 3: 本文の追記・編集

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 本文の追記・編集",
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

**AIが実行すること:**

1. サンドボックスページに本文を追記:
   ```bash
   ncli page update <サンドボックスページID> --body "## 追記セクション

以下は ncli page update で追記した内容です。

- 追記項目1: $(date +%Y-%m-%d_%H:%M)
- 追記項目2: 更新テスト完了"
   ```

2. 追記後の内容を確認:
   ```bash
   ncli fetch <サンドボックスページID>
   ```

3. タイトルの変更も試す:
   ```bash
   ncli page update <サンドボックスページID> --title "更新テスト用サンドボックス（編集済み）"
   ```

4. パイプ入力で長文を追記:
   ```bash
   echo "## 自動生成セクション

このセクションはパイプ経由で追記されました。
更新日時: $(date)" | ncli page update <サンドボックスページID> --body -
   ```

5. 最終的な状態を確認し、変更履歴を整理して表示する。

**期待される結果**: ページの本文が追記・編集され、タイトルも変更できる。

---

## 🚀 Step 4: ページの移動（ncli page move）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: ページの移動",
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

**AIが実行すること:**

1. 移動前のページの親を確認:
   ```bash
   ncli fetch <移動テスト用ページID> --json
   ```

2. ページを別の場所に移動:
   ```bash
   ncli page move <移動テスト用ページID> --to <サンドボックスページURL>
   ```

3. 移動後の状態を確認:
   ```bash
   ncli fetch <移動テスト用ページID> --json
   ```

4. 移動結果を報告:
   - 移動前の親ページ
   - 移動後の親ページ
   - ページのURLが変わったかどうか

5. Notionブラウザでサイドバーを確認し、ページが正しい場所に移動したか確認するよう案内する。

**補足**: ページを移動すると、そのページの子ページも一緒に移動します。重要なページを移動する前は、元の位置を記録しておくことをお勧めします。

**期待される結果**: ページが指定した親ページの下に移動する。

---

## 🚀 Step 5: 変更の検証（ncli fetch で確認）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 変更の検証",
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

**AIが実行すること:**

1. このレッスンで行った全変更を一覧で確認:
   ```bash
   ncli fetch <サンドボックスページURL>
   ```

2. タスク管理DBの最新状態を取得:
   ```bash
   ncli db query <タスク管理DB-URL>
   ```

3. 変更サマリーレポートを作成:
   ```markdown
   # 変更サマリー

   ## ページ更新
   - サンドボックスページ: タイトル変更、本文追記
   - 移動テスト用ページ: 親ページ変更

   ## DB更新
   - タスク1: Status Open → InProgress, Priority Medium → High
   - タスク2: （変更内容）

   ## ファイル操作
   - 追記: X回
   - 移動: X回
   ```

4. サマリーを `output/notion_update_summary.md` に保存する。

5. 受講者にNotionブラウザでの確認を案内し、CLIとブラウザの表示が一致するか確認してもらう。

**期待される結果**: 全変更が正しく反映され、サマリーレポートが生成される。

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
      {"id": "trouble_1", "label": "page update でプロパティが更新されない"},
      {"id": "trouble_2", "label": "本文の追記が上書きになってしまう"},
      {"id": "trouble_3", "label": "page move で Permission denied エラー"},
      {"id": "trouble_4", "label": "更新後に fetch しても変更が反映されない"}
    ]
  }]
}
```

### トラブル1: page update でプロパティが更新されない
**原因**: プロパティ名または値の指定が間違っている
**解決方法**:
```text
以下を確認してください：
1. ncli fetch <ページID> でプロパティ名を正確に確認
2. --prop の値がプロパティの型に合っているか確認
3. Select の場合、選択肢に存在する値を指定しているか確認
```

### トラブル2: 本文の追記が上書きになってしまう
**原因**: --body オプションの動作がページ全体の置換になっている場合がある
**解決方法**:
```text
以下を試してください：
1. まず ncli fetch で現在の内容を取得
2. 既存内容 + 追記内容を結合してから --body で更新
3. REST API を使って特定のブロックだけ追加することも可能:
   ncli rest PATCH /v1/blocks/<block-id>/children '{"children":[...]}'
```

### トラブル3: page move で Permission denied エラー
**原因**: 移動先のページに書き込み権限がない
**解決方法**:
```text
以下を確認してください：
1. 移動先のページにアクセスできるか ncli fetch で確認
2. 自分が作成したページ同士で試す
3. ワークスペースの権限設定を確認
```

### トラブル4: 更新後に fetch しても変更が反映されない
**原因**: キャッシュまたはAPIの伝播遅延
**解決方法**:
```text
以下を試してください：
1. 数秒待ってから再度 ncli fetch を実行
2. --json オプションを付けて詳細データを取得
3. Notionブラウザで直接確認して、API側の反映を待つ
```

---

## ✅ チェックポイント
- [ ] サンドボックスページが作成されている
- [ ] `ncli page update` でプロパティが更新できる
- [ ] 本文の追記・編集ができる
- [ ] `ncli page move` でページが移動できる
- [ ] `ncli fetch` で変更が正しく反映されていることを確認できる

---

## 📋 成果物プレビュー

このレッスンで得られる成果物:

| 成果物 | 説明 |
|--------|------|
| 編集済みサンドボックスページ | タイトル変更・本文追記済み |
| 移動済みページ | 親ページが変更されたページ |
| 更新済みDBエントリ | プロパティが変更されたタスク |
| `output/notion_update_summary.md` | 変更サマリーレポート |

---

## ➡️ 次のステップ

これで書き込みと更新は完了です。次のレッスンでは、要約の作成とコメントの返信を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-12-6）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内:**
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-12-6
- finish → 終了

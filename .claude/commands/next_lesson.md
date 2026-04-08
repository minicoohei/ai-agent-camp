---
description: "完了チェックして次のレッスンへ進む"
---

# /next_lesson

## ✅ 完了チェックと次のレッスン
完了状況を確認し、次のレッスンを自動で案内します。

AskUserQuestion（AskQuestion）で進め方を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のレッスンへ進む",
  "questions": [{
    "id": "next_action",
    "prompt": "どの操作を行いますか？",
    "options": [
      {"id": "check_next", "label": "完了チェックして次へ進む"},
      {"id": "mark_done", "label": "手動で完了登録して次へ進む"},
      {"id": "list_lessons", "label": "レッスン一覧を確認する"}
    ]
  }]
}
```

## 実行内容

### 1) 完了チェックして次へ進む
```
uv run python tools/lesson_progress.py --next
```

### 2) 手動で完了登録して次へ進む
```
uv run python tools/lesson_progress.py --mark <現在のレッスンID>
uv run python tools/lesson_progress.py --next
```
> `<現在のレッスンID>` は直前に実施したレッスン（例: `start-1-1`, `start-3-2` など）に置き換えてください。

### 3) レッスン一覧を確認する
```
uv run python tools/lesson_progress.py --list
```

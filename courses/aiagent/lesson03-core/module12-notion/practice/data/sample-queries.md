# Notion API クエリ例

## クエリ 1: 未完了タスクの取得

ステータスが「完了」以外の全タスクを取得します。

```json
{
  "filter": {
    "property": "ステータス",
    "select": {
      "does_not_equal": "完了"
    }
  },
  "sorts": [
    {
      "property": "期限",
      "direction": "ascending"
    }
  ]
}
```

## クエリ 2: 担当者別タスク一覧

特定の担当者に割り当てられたタスクを取得します。

```json
{
  "filter": {
    "property": "担当者",
    "select": {
      "equals": "鈴木一郎"
    }
  }
}
```

## クエリ 3: 今週期限のタスク

今週中に期限が来るタスクを取得します。

```json
{
  "filter": {
    "property": "期限",
    "date": {
      "this_week": {}
    }
  },
  "sorts": [
    {
      "property": "優先度",
      "direction": "ascending"
    }
  ]
}
```

## クエリ 4: 高優先度 かつ 未着手のタスク

優先度が「高」で、まだ着手していないタスクを取得します。

```json
{
  "filter": {
    "and": [
      {
        "property": "優先度",
        "select": {
          "equals": "高"
        }
      },
      {
        "property": "ステータス",
        "select": {
          "equals": "未着手"
        }
      }
    ]
  }
}
```

## クエリ 5: カテゴリ検索（開発 または バグ修正）

カテゴリに「開発」または「バグ修正」が含まれるタスクを取得します。

```json
{
  "filter": {
    "or": [
      {
        "property": "カテゴリ",
        "multi_select": {
          "contains": "開発"
        }
      },
      {
        "property": "カテゴリ",
        "multi_select": {
          "contains": "バグ修正"
        }
      }
    ]
  },
  "sorts": [
    {
      "property": "期限",
      "direction": "ascending"
    }
  ]
}
```

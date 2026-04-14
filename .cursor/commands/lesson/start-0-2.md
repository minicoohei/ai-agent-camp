---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch02-extensions"
duration: "約5分"
prerequisites: ["Lesson 0-1 完了"]
level: "beginner"
tags: ["setup", "extensions"]
---

# Lesson 0-2: 拡張機能インストール

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | AIエージェント開発に必要な拡張機能を確認・インストールし、開発効率を高める |
| 所要時間 | 約5分 |
| 前提条件 | Lesson 0-1 完了（Cursor が動作すること） |
| 教材ページ | [コース教材トップ](https://ai-agent.camp/ja/course/module-0) を並行参照 |

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## 拡張機能の自動インストール

このレッスンでは `/setup-extensions` を実行するだけで完了します。
**ターミナルの操作は一切不要です。全てAIが自動で実行します。**
もしAIが「ターミナルで実行してください」と案内した場合は [ターミナル入門ガイド](../../../docs/terminal-guide.md) を参照してください。

### AIが自動で行うこと

1. 現在インストール済みの拡張機能を確認
2. 不足している必須拡張機能（Python, Marp, Draw.io, PlantUML 等）を特定
3. 不足分を自動でインストール
4. インストール結果をレポート表示

**AskQuestionの設定:**
```json
{
  "title": "拡張機能セットアップ",
  "questions": [{
    "id": "action",
    "prompt": "拡張機能の自動インストールを始めますか？",
    "options": [
      {"id": "run", "label": "自動インストールを開始する（/setup-extensions を実行）"},
      {"id": "already_done", "label": "既にインストール済み"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(run → `/setup-extensions` の内容を実行する)
(already_done → チェックポイントへ)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 実行コマンド

```text
/setup-extensions
```

## 期待される出力例

```text
拡張機能チェック結果:
- Marp for VS Code: インストール済み ✓
- Draw.io Integration: 新規インストール ✓
- PlantUML: 新規インストール ✓
全ての必須拡張機能が揃いました！
```

## よくあるトラブル
- インストールが進まない → Cursor を再起動して再実行
- `cursor --list-extensions` が見つからない → コマンドパレットから手動インストール

---

## 拡張機能 Extension ID 一覧

| 拡張機能 | Extension ID | 必須/推奨 |
|---------|-------------|---------|
| Python | ms-python.python | 必須 |
| Marp | marp-team.marp-vscode | 推奨 |
| Draw.io | hediet.vscode-drawio | 推奨 |
| PlantUML | jebbs.plantuml | 推奨 |

## チェックポイント
- [ ] Python 拡張機能がインストール済み
- [ ] Marp 拡張機能がインストール済み
- [ ] Draw.io 拡張機能がインストール済み
- [ ] PlantUML 拡張機能がインストール済み
- [ ] 構文ハイライトが機能している

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next", "label": "Gemini APIを設定する（/start-0-3）"},
      {"id": "check", "label": "環境チェックをする（/check-setup）"},
      {"id": "back", "label": "環境確認に戻る（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(next → /start-0-3 を案内)
(check → /check-setup の内容を実行する)
(back → /start-0-1 を案内)
(finish → 終了)

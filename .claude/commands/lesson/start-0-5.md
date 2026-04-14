---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "約5分"
prerequisites: ["start-0-1", "start-0-2", "start-0-3", "start-0-4"]
level: "beginner"
tags: ["setup", "security"]
---

# Lesson 0-5: セキュリティ設定確認

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | .gitignore と pre-commit フックを設定し、APIキーの漏洩を防止する。Module 0 を安全に完了する |
| 所要時間 | 約5分 |
| 前提条件 | Lesson 0-1〜Lesson 0-4 完了、.env に API キーを設定済み |
| 教材ページ | [コース教材トップ](https://ai-agent.camp/ja/course/module-0) を並行参照 |

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## セキュリティ設定の自動セットアップ

このレッスンでは `/setup-security` を実行するだけで完了します。
**ターミナルの操作は一切不要です。全てAIが自動で実行します。**

### AIが自動で行うこと

1. `.gitignore` の確認・不足エントリの自動追加（.env, credentials/, *.key, *.pem 等）
2. `pre-commit` フックの自動設定（.envファイルの誤コミットをブロック）
3. 現状の安全性チェック（.envがGit追跡対象になっていないか、過去にコミットされていないか）
4. 問題が見つかった場合は自動修復を提案

**AskQuestionの設定:**
```json
{
  "title": "セキュリティ設定",
  "questions": [{
    "id": "action",
    "prompt": "セキュリティ設定を始めますか？",
    "options": [
      {"id": "run", "label": "自動設定を開始する（/setup-security を実行）"},
      {"id": "already_done", "label": "既にセキュリティ設定済み"},
      {"id": "more_info", "label": "なぜセキュリティ設定が必要なのか知りたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(run → `/setup-security` の内容を実行する)
(already_done → 完了チェックへ)
(more_info → 「APIキーがGitHubに公開されると、不正利用や高額請求のリスクがあります。このコマンドで自動的に防止策を設定します」と説明した上で再度選択)
(different_lesson → モジュール一覧を表示)

---

## 実行コマンド

```text
/setup-security
```

## 期待される出力例

```text
セキュリティ設定完了:
- .gitignore: .env, credentials/, *.key, *.pem を追加 ✓
- pre-commit フック: 設定済み ✓
- .env ファイル: Git追跡対象外 ✓
```

## よくあるトラブル
- pre-commitフックがコミットをブロックする → AIに「コミット内容を確認して」と依頼
- .env がGitに追跡されている → AIに「.envをGitの追跡から外して」と依頼

---

## チェックポイント
- [ ] .gitignore に .env が含まれている
- [ ] .gitignore に credentials/ が含まれている
- [ ] pre-commit フックが設定されている
- [ ] .env ファイルが Git の追跡対象になっていない
- [ ] Git 履歴に機密情報が含まれていない

---

## Module 0 完了！

セキュリティ設定が完了したら、Module 0 は全て完了です。

最終確認として `/check-setup` を実行すると、全項目の状態をレポート表示できます。

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "Module 0 完了！次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "おめでとうございます！Module 0 が完了しました。次に何をしますか？",
    "options": [
      {"id": "start_lesson", "label": "最初のレッスンを始める（/start-1-1: バナー生成）"},
      {"id": "final_check", "label": "最終チェックをする（/check-setup）"},
      {"id": "overview", "label": "プロジェクト全体を確認する（/overview）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(start_lesson → /start-1-1 を案内)
(final_check → /check-setup の内容を実行する)
(overview → /overview を案内)
(finish → 「お疲れさまでした。いつでも /start-1-1 で最初のレッスンを始められます」と表示)

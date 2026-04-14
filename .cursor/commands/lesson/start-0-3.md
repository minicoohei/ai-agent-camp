---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "約10分"
prerequisites: ["start-0-1", "start-0-2"]
level: "beginner"
tags: ["setup", "gemini", "api"]
---

# Lesson 0-3: Gemini API設定

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Google AI Studio で Gemini API キーを取得し、.env に設定して画像生成などのAI機能を使えるようにする |
| 所要時間 | 約10分 |
| 前提条件 | Lesson 0-1・Lesson 0-2 完了、ブラウザで Google アカウントにログイン可能 |
| 教材ページ | [コース教材トップ](https://ai-agent.camp/ja/course/module-0) を並行参照 |

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## Gemini APIの自動セットアップ

このレッスンでは `/setup-gemini` を実行するだけで完了します。
**ターミナルの操作は一切不要です。全てAIが自動で実行します。**

### AIが自動で行うこと

1. ブラウザで Google AI Studio を自動起動（AIがOSに応じて `open` / `start` を実行）
2. ブラウザ上でのAPIキー取得手順をステップバイステップで案内
3. `.env` ファイルを自動作成（`.env.example` をコピー + `.gitignore` 確認）
4. ユーザーが `.env` ファイルにAPIキーを直接入力（Cursorのエディタで編集）
5. Gemini APIへのテストリクエストを自動実行して動作確認

**重要**: APIキーはチャットに貼り付けないでください。`.env` ファイルに直接入力する方式です。

**AskQuestionの設定:**
```json
{
  "title": "Gemini API セットアップ",
  "questions": [{
    "id": "action",
    "prompt": "Gemini APIの設定を始めますか？",
    "options": [
      {"id": "run", "label": "セットアップを開始する（/setup-gemini を実行）"},
      {"id": "already_done", "label": "既にGemini APIを設定済み"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(run → `/setup-gemini` の内容を実行する)
(already_done → チェックポイントへ)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 実行コマンド

```text
/setup-gemini
```

## 期待される出力例

```text
Gemini API テスト結果:
API応答: こんにちは！お手伝いできることはありますか？
```

> **注意**: 応答テキストはモデルにより異なります。エラーが出なければ接続成功です。

## よくあるトラブル
- ブラウザが開かない → AIに「Google AI Studioを開いて」と依頼
- APIテストが失敗する → .env ファイルのキーを確認し `/setup-gemini` を再実行

---

## チェックポイント
- [ ] Google AI StudioでAPIキーを取得した
- [ ] .envファイルに GEMINI_API_KEY が設定されている
- [ ] .envファイルが .gitignore で除外されている
- [ ] APIテストが成功した（Gemini APIからの応答を受信できた）

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
      {"id": "next", "label": "Slack APIを設定する（/start-0-4）"},
      {"id": "try_banner", "label": "さっそくバナーを作ってみる（/start-1-1）"},
      {"id": "check", "label": "環境チェックをする（/check-setup）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(next → /start-0-4 を案内)
(try_banner → /start-1-1 を案内)
(check → /check-setup の内容を実行する)
(finish → 終了)

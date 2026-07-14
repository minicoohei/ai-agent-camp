---
description: "Lesson command — 教材コンテンツの初回セットアップ"
duration: "約3分"
prerequisites: ["ai-agent-camp フォルダを Cursor / Codex / Claude Code で開いている", "git が使える状態"]
level: "beginner"
nonInteractiveMode: deferred
tags: ["setup", "content", "module-0"]
---

# /setup-content -- 教材コンテンツの初回セットアップ

> aiagent-course Module 0 の S45 (`HowToUpdateContent`) スライドが参照するコマンド。学習者が教材を最新化できる状態に環境を整えるための初回セットアップ手順をまとめる。

## このコマンドの役割

`/setup-content` は **「これから教材を更新できる状態にする」** ための一回限りの準備。実際の最新化はこのあと `git fetch origin && git log HEAD..origin/main --oneline  # 上流との差分を確認` などで継続的に行う想定。

## AI が裏で行うこと

1. リポジトリの sparse-checkout 設定を確認（必要なら有効化）
2. `git status` でクリーンな状態かチェック（commit していない作業がないか）
3. `git fetch origin` で最新の参照を取得
4. the upstream sync helper の存在を確認:
   - 存在する場合 → `python -c "import pathlib; print('ok' if pathlib.Path('.git').exists() else 'missing')"` で疎通確認
   - 存在しない場合 → 「先に upstream の最新を pull してください」と案内し、`git pull` の手順を提示して終了
5. 「次は `git fetch origin && git log HEAD..origin/main --oneline  # 上流との差分を確認` で更新差分を確認できます」とユーザーに告知

## 確認方法

正常に終了したら、続けて以下を実行:

```bash
git fetch origin && git log HEAD..origin/main --oneline  # 上流との差分を確認
```

## 非対話モード（claude -p / cursor-agent --print）での挙動

`nonInteractiveMode: deferred` です。

- Step 1〜3（git fetch / status 等の read-only 操作）は実行する
- the upstream sync helper の有無確認まで進める
- 該当ツールが無い、または何かしらの確認入力が必要な場合は **`setup-resume.md`** に「対話モードで `/setup-content` を再実行」と書いて終了する

## 関連

- aiagent-course Module 0 S45 (`HowToUpdateContent`) — 教材の更新方法スライド
- 共通仕様: [`_lib/non-interactive.md`](../_lib/non-interactive.md)

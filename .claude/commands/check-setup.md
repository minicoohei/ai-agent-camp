---
description: "Top-level alias — see lesson/check-setup.md for the full body."
duration: "約2分"
level: "beginner"
nonInteractiveMode: deferred
tags: ["setup", "check", "alias"]
---

# /check-setup -- 環境の自動チェック（top-level alias）

## このファイルの役割

サブディレクトリ命名空間 (`/lesson:check-setup`) を覚えなくても **`/check-setup`** で同じレッスンが起動できるようにする薄いラッパー。本体のロジックはすべて [`lesson/check-setup.md`](./lesson/check-setup.md) にある。

## AI への指示

1. このコマンドが呼ばれたら、まず `.claude/commands/lesson/check-setup.md` を **Read** して、その指示にそのまま従う。
2. 非対話モード（`claude -p` / `cursor-agent --print` 経由など、stdin が TTY ではない、または `CLAUDE_CODE_NON_INTERACTIVE=1` 等の env が立っている）で呼び出された場合は **deferred モード**で動作する:
   - 環境チェック自体は実行する（read-only コマンドのみ）。
   - レポートを Markdown で出力する。
   - 末尾に `AskQuestion` ブロックがある場合は、ユーザーに尋ねず **「次に対話モードで `/check-setup` を再度実行してください」** とだけ表示して終了する。
3. 対話モードで呼ばれた場合は、本体ファイルの AskQuestion ブロックをそのまま提示する。

## 非対話モード判定の擬似コード

```python
import os, sys
non_interactive = (
    not sys.stdin.isatty()
    or os.environ.get("CLAUDE_CODE_NON_INTERACTIVE") == "1"
    or os.environ.get("CURSOR_AGENT_PRINT") == "1"
)
```

## 関連ドキュメント

- 非対話モード共通仕様: [`_lib/non-interactive.md`](./_lib/non-interactive.md)
- 多言語版: [`check-setup.en.md`](./check-setup.en.md), [`check-setup.es.md`](./check-setup.es.md)

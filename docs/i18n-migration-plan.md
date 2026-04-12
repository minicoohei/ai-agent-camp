# i18n Migration Plan: Full Multi-Language Build System

## Purpose

ai-agent-camp リポジトリの全コンテンツ（コマンド、スキル、マニフェスト）を en/ja/es の3言語でリリースビルドできるようにする。
リリースビルドは各言語ごとにダウンロードし、upstream として設定する方式で配布する。

---

## Current State

| 対象 | 現状 | 言語 | ファイル数 |
|------|------|------|-----------|
| `courses/aiagent/*.yaml` | 既に3言語対応 | ja/en/es | 43 pairs (86 files) |
| `docs/i18n-glossary.md` | 用語集・スタイルガイド完備 | ja/en/es | 1 file (14.6KB) |
| `README.md` / `.ja.md` / `.es.md` | 完了済み（本セッション） | en/ja/es | 3 files |
| `.claude/commands/lesson/*.md` | 日本語のみ | ja | 134 files |
| `.cursor/commands/lesson/*.md` | 日本語のみ（.claude と同一） | ja | 134 files |
| `.cursor/commands/utility/*.md` | 日本語のみ | ja | 32 files |
| `.claude/commands/*.md` (non-lesson) | 日本語のみ | ja | 11 files |
| `skills/*/SKILL.md` | 日本語 + 英語混在 | ja (partial en) | 101 files |
| `courses/lessons.manifest.yaml` | 日本語のみ | ja | 1 file (134 entries) |

**翻訳が必要な総ファイル数**: 約 280 ファイル × 2言語 = 約 560 翻訳タスク

---

## Architecture Design

### Option A: File Suffix 方式（推奨）

courses/ で既に採用されている `*.en.yaml` / `*.es.yaml` パターンを全体に拡張する。

```
skills/banner-creator/
├── SKILL.md          # ja（デフォルト / source of truth）
├── SKILL.en.md       # en
└── SKILL.es.md       # es

.claude/commands/lesson/
├── start-1-1.md      # ja（デフォルト）
├── start-1-1.en.md   # en
└── start-1-1.es.md   # es
```

**メリット**: 既存の courses/ パターンと一貫性がある、diff が取りやすい
**デメリット**: ファイル数が3倍になる

### Option B: ディレクトリ分離方式

```
.claude/commands/
├── ja/lesson/start-1-1.md
├── en/lesson/start-1-1.md
└── es/lesson/start-1-1.md
```

**メリット**: 言語ごとにクリーンなビルドが可能
**デメリット**: 既存パスが変わる、Cursor/Claude のコマンド解決パスに影響

### Option C: ビルドスクリプト + テンプレート方式

```
# Source (single file with i18n keys)
.claude/commands/lesson/start-1-1.md  # {{t.title}}, {{t.description}} 等

# Generated
dist/ja/.claude/commands/lesson/start-1-1.md
dist/en/.claude/commands/lesson/start-1-1.md
dist/es/.claude/commands/lesson/start-1-1.md
```

**メリット**: 構造的な変更箇所を1ファイルで管理、翻訳漏れを検出しやすい
**デメリット**: ビルドツールの開発が必要、テンプレート構文の学習コスト

### 推奨: Option A（File Suffix 方式）

理由:
1. courses/ で既に動作実績がある
2. ビルドツール不要で即座に開始可能
3. 各ファイルが独立しているため並列翻訳が容易
4. リリースビルド時は言語 suffix でフィルタリングするだけ

---

## Implementation Plan

### Phase 1: Infrastructure（1セッション）

1. **リリースビルドスクリプト作成** (`tools/build_release.py`)
   - 引数: `--lang ja|en|es`
   - 処理: 指定言語のファイルを収集し、suffix を除去して `dist/{lang}/` に配置
   - `.claude/commands/`, `.cursor/commands/`, `skills/` を対象
   - `courses/` は既存の `*.{lang}.yaml` をそのままコピー

2. **翻訳差分検出スクリプト作成** (`tools/check_translations.py`)
   - source（ja）と翻訳ファイルの対応チェック
   - 欠落ファイル、更新日時の差分を検出
   - CI で実行可能にする

3. **lessons.manifest の多言語化**
   - `courses/lessons.manifest.yaml` → デフォルト（ja）
   - `courses/lessons.manifest.en.yaml` → 英語版
   - `courses/lessons.manifest.es.yaml` → スペイン語版

### Phase 2: Commands 翻訳（2-3セッション）

翻訳ルール:
- `docs/i18n-glossary.md` の用語集に厳密に従う
- 技術用語（Claude Code, Cursor, Gemini, LLM, API 等）は翻訳しない
- frontmatter の `description:` フィールドも翻訳する
- Markdown 構造（見出し、リスト、コードブロック）は保持する

対象:
```
# Lesson commands: 134 files × 2 languages = 268 files
.claude/commands/lesson/start-*.md → start-*.en.md, start-*.es.md
.cursor/commands/lesson/ → 同上（.claude と同期）

# Utility commands: 32 files × 2 = 64 files
.cursor/commands/utility/*.md → *.en.md, *.es.md

# Non-lesson commands: 11 files × 2 = 22 files
.claude/commands/module-18-*.md → *.en.md, *.es.md
```

並列化戦略:
- 5エージェントで module ごとにバッチ分割
- 各エージェントに i18n-glossary.md と翻訳元ファイルを渡す
- .claude と .cursor は同一内容なので .claude を先に翻訳し cp で同期

### Phase 3: Skills 翻訳（1-2セッション）

```
# 101 skills × 2 languages = 202 files
skills/*/SKILL.md → SKILL.en.md, SKILL.es.md
```

翻訳対象:
- frontmatter: `name`, `description`, `triggers` を翻訳
- body: 見出し、説明文、テーブル、トラブルシューティングを翻訳
- コードブロック内のコメントは翻訳するがコードは翻訳しない

### Phase 4: CI/CD + 検証（1セッション）

1. **GitHub Actions ワークフロー**
   - `check_translations.py` を PR 時に自動実行
   - 翻訳漏れがあれば Warning を出す

2. **リリースビルド自動化**
   - tag push 時に3言語のビルドを生成
   - GitHub Releases にアーティファクトとして添付

3. **品質チェック**
   - `i18n-glossary.md` の regex パターンで残留日本語を検出
   - 各言語のリンク整合性チェック

---

## Glossary Reference

翻訳時は必ず `docs/i18n-glossary.md` を参照すること。主要ルール:

- **翻訳しない用語**: Claude Code, Cursor, Codex, Gemini, BigQuery, MCP, LLM, API, Git, GitHub, Slack, Notion, PPTX, GAS
- **日本語 → 英語**: 「〜してください」→ imperative form, 「〜しましょう」→ "Let's..."
- **日本語 → スペイン語**: 「〜してください」→ imperativo formal (usted), 敬称は tú ではなく usted

---

## Session Kickoff Prompt

以下のプロンプトを新しいセッションで使用してください:

```
docs/i18n-migration-plan.md を読んで、Phase 1（Infrastructure）から実装を開始してください。

現状:
- README は en/ja/es 対応済み
- courses/aiagent/ は .en.yaml/.es.yaml 対応済み
- commands と skills は日本語のみ

目標:
- リリースビルドスクリプト (tools/build_release.py) を作成
- 翻訳差分検出スクリプト (tools/check_translations.py) を作成
- lessons.manifest の多言語版を作成

翻訳ルールは docs/i18n-glossary.md に定義済みです。
```

Phase 2 以降は以下のように開始:

```
docs/i18n-migration-plan.md の Phase 2 を実行してください。
Phase 1 のビルドスクリプトは完了済みです。

.claude/commands/lesson/ の134ファイルを英語・スペイン語に翻訳してください。
翻訳ルールは docs/i18n-glossary.md に従ってください。
File Suffix 方式（*.en.md, *.es.md）で作成してください。
```

---

## Estimated Effort

| Phase | セッション数 | 翻訳ファイル数 | 備考 |
|-------|-------------|--------------|------|
| Phase 1: Infrastructure | 1 | 3 (manifest) | スクリプト2本 + manifest翻訳 |
| Phase 2: Commands | 2-3 | 354 | 5エージェント並列で1セッション約150ファイル |
| Phase 3: Skills | 1-2 | 202 | 5エージェント並列 |
| Phase 4: CI/CD | 1 | 0 | GitHub Actions + 検証 |
| **合計** | **5-7** | **559** | |

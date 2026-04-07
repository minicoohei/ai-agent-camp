# i18n 用語集 / i18n Glossary

> このドキュメントは ai-agent-camp プロジェクトの多言語翻訳における用語の標準化ガイドです。
> 翻訳作業時・レビュー時の参照資料として使用してください。
>
> This document is the terminology standardization guide for multilingual translation
> in the ai-agent-camp project. Use as a reference during translation and review.

**対象ロケール / Target Locales:** 日本語 (ja), English (en), Español (es)

**ロケールファイル / Locale Files:**
- `course/locales/ja.json` (10847 keys)
- `course/locales/en.json` (10846 keys)
- `course/locales/es.json` (10846 keys)

---

## 1. コア用語 / Core Terms

日本語の原文に対する英語・スペイン語の **標準訳** です。
翻訳時はこの表に従い、表記ゆれを防いでください。

### Brand / Course Structure

| 日本語 (JA) | English (EN) | Español (ES) | 出現数 | 備考 / Notes |
|---|---|---|---:|---|
| 研修 | Training | Capacitación | 197 | Use 'course' only when referring to course materials specifically. ES: Do not use 'entrenamiento' or 'formación' |
| AIエージェント研修 | AI Agent Training | Capacitación de Agentes de IA | 175 | BRAND NAME. Must be identical across all pages. ES: always 'IA' not 'AI' |

### Navigation

| 日本語 (JA) | English (EN) | Español (ES) | 出現数 | 備考 / Notes |
|---|---|---|---:|---|
| モジュール | Module | Módulo | 129 |  |
| ホーム | Home | Inicio | 76 |  |
| レッスン | Lesson | Lección | 75 |  |
| 戻る | Back | Volver | 53 |  |
| 次へ | Next | Siguiente | 44 |  |
| 前へ | Previous | Anterior | 37 | Do not use 'Previo' |
| モジュール概要 | Module Overview | Resumen del módulo | 37 | ES: lowercase 'módulo' per Spanish capitalization rules |
| 全体像を見る | See the big picture | Ver la visión general | 16 | EN: Do not use 'View Overview' |

### Course Structure

| 日本語 (JA) | English (EN) | Español (ES) | 出現数 | 備考 / Notes |
|---|---|---|---:|---|
| 演習 | Exercise | Ejercicio | 101 |  |
| 実践 | Hands-on practice | Práctica | 77 |  |
| 基礎 | Foundation | Fundamentos | 37 |  |
| 目標 | Goal | Objetivo | 35 | In lesson context: 'Learning objective' |
| まとめ | Summary | Resumen | 32 |  |
| 前提条件 | Prerequisites | Requisitos previos | 20 |  |
| 理解度チェック | Comprehension Check | Verificación de comprensión | 6 | EN: Do not use 'Understanding Check' |
| カリキュラム | Curriculum | Plan de estudios | 2 |  |

### Actions

| 日本語 (JA) | English (EN) | Español (ES) | 出現数 | 備考 / Notes |
|---|---|---|---:|---|
| 生成 | Generate | Generar | 434 |  |
| 実行 | Run | Ejecutar | 389 | EN: 'Run' preferred over 'Execute' (more natural). 'Run in Cursor chat:' is the standard phrasing. |
| 作成 | Create | Crear | 358 |  |
| 設定 | Settings / Setup | Configuración | 311 | EN: 'Settings' for noun (config page), 'Setup' for process |
| 確認 | Verify / Confirm | Verificar | 288 | EN: 'Verify' for checking correctness, 'Confirm' for user action buttons. ES: 'verificar' for technical checks, 'confirmar' only for user confirmation buttons. |
| 検索 | Search | Buscar | 172 |  |
| 分析 | Analyze | Analizar | 166 | EN: American spelling 'Analyze' (not 'Analyse') |
| 操作 | Steps | Pasos | 115 | EN: 'Steps' preferred over 'Operation' (more natural as a label). Do not use 'Operation:' in headings. |
| 追加 | Add | Agregar | 91 | ES: 'Agregar' preferred over 'Añadir' |
| 表示 | Display / View | Mostrar / Ver | 80 |  |
| 編集 | Edit | Editar | 58 |  |
| 保存 | Save | Guardar | 48 |  |
| 削除 | Delete | Eliminar | 15 |  |

### UI Elements

| 日本語 (JA) | English (EN) | Español (ES) | 出現数 | 備考 / Notes |
|---|---|---|---:|---|
| 重要 | Important | Importante | 67 |  |
| 注意 | Note | Nota | 37 | For stronger warnings: EN 'Warning' / ES 'Advertencia' |
| ヒント | Tip | Consejo | 24 |  |
| プロンプトを入力 | Enter this prompt in Cursor | Ingrese este prompt en Cursor | 4 | EN: Do not use 'Prompt to enter in Cursor' (awkward). ES: Use 'usted' form. |
| Cursorのチャットで実行 | Run in Cursor chat: | Ejecutar en el chat de Cursor: | 0 | EN: Always 'Run' (not 'Execute'). Lowercase 'chat'. |
| 期待される出力 | Expected output | Resultado esperado | 0 |  |

### Technical Concepts

| 日本語 (JA) | English (EN) | Español (ES) | 出現数 | 備考 / Notes |
|---|---|---|---:|---|
| エージェント | Agent | Agente | 402 | Always capitalized when referring to AI Agent |
| スキル | Skill | Skill | 227 | When referring to Claude Code plugin: do NOT translate. ES: Do not use 'habilidad' for technical skills. Only 'habilidad' for human competencies. |
| コマンド | Command | Comando | 157 |  |
| ツール | Tool | Herramienta | 138 |  |
| プロンプト | Prompt | Prompt | 125 | Do not translate. Keep as 'Prompt' in all languages. |
| コンテキスト | Context | Contexto | 97 |  |
| 認証 | Authentication | Autenticación | 80 |  |
| ワークフロー | Workflow | Flujo de trabajo | 75 |  |
| テンプレート | Template | Plantilla | 61 |  |
| ダッシュボード | Dashboard | Panel de control | 45 | ES: 'Dashboard' also acceptable in technical context |
| デプロイ | Deploy | Desplegar / Deploy | 42 | ES: 'Desplegar' as verb, 'deploy' acceptable in technical context |
| 環境変数 | Environment variable | Variable de entorno | 15 |  |
| 依存関係 | Dependencies | Dependencias | 14 |  |

### 三大原則 / Golden Rules (Boilerplate)

各モジュールページで繰り返される「三大原則」は、全ページで同一の訳文を使用すること。

| # | 日本語 (JA) | English (EN) | Español (ES) |
|---|---|---|---|
| 1 | Plan Modeではじめること | Start in Plan Mode | Comience en modo Plan |
| 2 | AskUserQuestionsで曖昧さをゼロにすること | Eliminate Ambiguity with AskUserQuestions | Elimine la ambigüedad con AskUserQuestions |
| 3 | 新しいエージェントで始める。コンテキストは綺麗に保つ | Start with a new agent. Keep the context clean | Comience con un nuevo agente. Mantenga el contexto limpio |

**EN boilerplate for Golden Rule explanation:**

> When conversations get long, the context gets cluttered, reducing the agent's accuracy.
> Start a new chat for each task and always keep the context clean.

---

## 2. 翻訳しない用語 / Technical Terms (Never Translate)

以下の用語は **原語のまま** 使用し、翻訳しないこと。
These terms must be kept in their **original form** and never translated.

### AI / ML Products

`Claude Code`, `Claude`, `Cursor`, `Gemini`, `GPT-4o`, `ChatGPT`, `Copilot`, `Devin`

### Acronyms / Concepts

`LLM`, `AI`, `API`, `MCP`, `RAG`, `EDA`, `PRD`, `WBS`, `E2E`, `UML`, `CRUD`, `CI/CD`, `SDK`, `CLI`, `IDE`

### Cloud / Infrastructure

`BigQuery`, `GitHub Actions`, `GitHub`, `Docker`, `Vercel`, `Google Cloud`, `GCP`, `GAS`

### File Formats

`PPTX`, `PDF`, `CSV`, `JSON`, `HTML`, `CSS`, `YAML`, `Markdown`

### Languages / Runtimes

`JavaScript`, `TypeScript`, `Python`, `Node.js`

### Tools / Libraries

`Git`, `npm`, `pip`, `PlantUML`, `Tailwind`, `Bootstrap`, `Playwright`, `marimo`, `gogcli`, `clasp`

### Project-Specific

`Nano Banana`, `NotebookLM`, `AGENTS.md`, `SKILL.md`, `CLAUDE.md`

### Modes / Features

`Plan Mode`, `Agent Mode`, `Ask Mode`, `Debug Mode`, `Max Mode`, `SubAgent`

**例外 / Exceptions:**

| 用語 | EN | ES | 備考 |
|---|---|---|---|
| AI | AI | **IA** | ES では 'IA' (Inteligencia Artificial) を使用。ただし製品名の一部 ('AI Agent') はそのまま。 |
| スキル (技術的) | Skill | **Skill** | Claude Code プラグインとしての 'スキル' は翻訳しない。人間の能力を指す場合のみ ES: 'habilidad' |
| コンピュータ | Computer | **Computadora** | ES: 'ordenador' (スペイン) ではなく 'computadora' (中南米・中立) を使用 |

---

## 3. スタイルガイド / Style Guide

### English (EN)

| 項目 | ガイドライン |
|---|---|
| **Tone** | Professional but accessible, instructional. Suitable for corporate training. |
| **Formality** | Use "Do not" (not "Don't"). Avoid contractions in instructional text. |
| **Voice** | Active voice preferred. Address the reader directly ("you"). |
| **Spelling** | American English: "analyze" (not "analyse"), "color" (not "colour"). |
| **Capitalization** | Title Case for headings: "Create a New Banner". Sentence case for descriptions. |
| **Oxford comma** | Use it: "images, diagrams, and charts". |
| **Numbers** | Spell out one through nine. Use digits for 10+. |
| **Brand name** | "AI Agent Training" (always this form). |

### Español (ES)

| 項目 | ガイドライン |
|---|---|
| **Tone** | Profesional y accesible. Tono instructivo para capacitación corporativa. |
| **Formality** | Siempre **usted** (forma formal). No usar **tú**. |
| **Register** | "Haga clic" (not "Haz clic"), "puede" (not "puedes"), "su" (not "tu"). |
| **AI vs IA** | Usar **IA** (Inteligencia Artificial), no "AI". Excepción: nombres propios en inglés. |
| **Regional** | Español neutro (no regional). "computadora" (not "ordenador"), "clic" (not "click"). |
| **Capitalization** | Solo la primera palabra de un título: "Resumen del módulo" (not "Resumen del Módulo"). |
| **Brand name** | "Capacitación de Agentes de IA" (always this form). |
| **Calques** | Avoid literal translations of Japanese patterns. "es posible" → use direct verbs: "permite", "se puede". |

### 日本語 (JA) - 原文のルール

| 項目 | ガイドライン |
|---|---|
| **ブランド名** | 「AIエージェント研修」（常にこの表記） |
| **敬体** | です・ます体を基本とする |
| **カタカナ** | 外来語はカタカナ表記（エージェント、プロンプト、スキル） |
| **括弧** | 強調は「」、補足は（）を使用 |

---

## 4. 約物・記号の変換ルール / Punctuation Rules

日本語の約物は、英語・スペイン語では以下のように置き換えること。
翻訳後に日本語固有の約物が残っている場合はバグとして修正すること。

| 日本語 | English | Español | 例 (JA → EN) |
|---|---|---|---|
| 「」 | "" (double quotes) | "" (double quotes) or « » | 「Go Live」 → "Go Live" |
| ※ | Note: | Nota: | ※注意 → Note: ... |
| （） | () | () | MCP（詳細） → MCP (details) |
| 〜 | – (en-dash) | – (en-dash) | モジュール1〜13 → Modules 1–13 |
| ・ | / or , | / or , | 読み取り・書き込み → Read / Write |
| 。 | . (period) | . (period) | 実行します。 → Run the command. |
| 、 | , (comma) | , (comma) | 計画、実行、確認 → Plan, run, verify |
| … | ... | ... | 読み込み中… → Loading... |
| ： | : | : | 配置場所： → Location: |

### 残存チェック用正規表現 / Regex for Residual Detection

翻訳後のファイルに日本語約物が残っていないか検出するための正規表現:

```
# Japanese brackets (should not appear in EN/ES)
[「」『』【】]

# Full-width parentheses
[（）]

# Japanese note marker
※

# Wave dash (range)
〜

# Full-width colon/semicolon
[：；]
```

---

## 5. 共通パターン / Common Translation Patterns

### UI ラベルの標準訳

| 日本語パターン | English | Español |
|---|---|---|
| "○○を作成する" | "Create ○○" | "Crear ○○" |
| "○○の設定" | "○○ Settings" | "Configuración de ○○" |
| "○○を確認する" | "Verify ○○" | "Verificar ○○" |
| "○○が可能" | "Can ○○" / "Supports ○○" | "Permite ○○" / "Se puede ○○" |
| "○○について" | "About ○○" | "Acerca de ○○" |
| "以下の○○" | "The following ○○" | "Los siguientes ○○" (or omit) |

### ナビゲーションリンク

| 用途 | JA | EN | ES |
|---|---|---|---|
| Home link (main pages) | ホーム | Home | Inicio |
| Back to module (from sub-page) | モジュール概要に戻る | Back to Module Overview | Volver al resumen del módulo |
| Next lesson button | 次へ: ○○ | Next: ○○ | Siguiente: ○○ |
| Previous lesson button | 前へ: ○○ | Previous: ○○ | Anterior: ○○ |
| Footer | AIエージェント研修 - ai-agent-camp | AI Agent Training - ai-agent-camp | Capacitación de Agentes de IA - ai-agent-camp |

### Cursor 操作の指示文

| JA | EN (standardized) | ES (standardized) |
|---|---|---|
| Cursorのチャットで実行: | Run in Cursor chat: | Ejecutar en el chat de Cursor: |
| Cursorに入力するプロンプト | Enter this prompt in Cursor | Ingrese este prompt en Cursor |
| 操作: | Steps: | Pasos: |

---

## 6. 既知の問題と対応方針 / Known Issues from Native Reviews

2026-02-22 のネイティブレビュー結果に基づく主要な指摘事項:

### English

| ID | Severity | Issue | Resolution |
|---|---|---|---|
| T-02 | Medium | "Execute in Cursor chat" has 5 variants | Standardize to "Run in Cursor chat:" |
| T-04 | Medium | "Prompt to enter in Cursor" is awkward | Standardize to "Enter this prompt in Cursor" |
| T-03 | Medium | "Operation:" label is unnatural | Standardize to "Steps:" |
| P-01 | High | 22 instances of Japanese brackets 「」 | Replace with double quotes |
| P-02 | High | 5 instances of ※ marker | Replace with "Note:" |
| P-03 | High | 7 instances of full-width （） | Replace with standard () |
| P-04 | High | 1 instance of wave dash 〜 | Replace with en-dash – |

### Español

| ID | Severity | Issue | Resolution |
|---|---|---|---|
| TERM-001 | Critical | Brand name has 20 variants | Standardize to "Capacitación de Agentes de IA" |
| TERM-002 | Important | Inconsistent AI vs IA (349 vs 321) | Standardize to IA |
| TERM-005 | Minor | スキル translated as "habilidad" (215x) | Keep "Skill" for technical context |
| FORM-001 | Important | tú/usted mixed in 16 pages | Standardize to usted |
| PUNCT-001 | Critical | 40 instances of 「」 | Replace with "" or « » |
| PUNCT-002 | Important | 54 instances of （） | Replace with standard () |
| EXPR-001 | Critical | 13 empty 「 」 brackets | Recover content from HTML source |
| EXPR-002 | Important | 18 literal "es posible" calques | Rephrase with direct verbs |

---

## 変更履歴 / Changelog

| Date | Version | Description |
|---|---|---|
| 2026-02-22 | 1.0.0 | Initial glossary created from native review analysis |

---

*Generated by `create_glossary.py` from locale files and native review reports.*

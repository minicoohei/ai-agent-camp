---
name: course-editor
version: 1.0.0
author: ai-agent-camp team
description: |
  コース教材の管理ガイドラインスキル。
  教材ページは外部サイト（https://ai-agent.camp/）でホスト。
  ai-agent-camp 側ではレッスンコマンドとYAMLメタデータを管理する。
dependencies: none  # ガイドラインスキルのため実行スクリプトなし
triggers:
  - 教材を編集
  - 教材を作成
  - モジュールHTMLを更新
  - コース教材を作成
  - レッスンページを追加
  - セクションを書き換え
  - 教材リライト
---

# course-editor - HTML教材エディター

HTML教材（`course/`）の効率的な編集・新規作成をガイドするスキル。

## 目次

- [クイックスタート](#クイックスタート)
- [1. CSSフレームワーク情報](#1-cssフレームワーク情報)
- [2. テンプレート構造（3種類）](#2-テンプレート構造3種類)
- [3. 相対パス規則](#3-相対パス規則)
- [4. セクション単位編集ガイド](#4-セクション単位編集ガイド)
- [5. 新規ページ作成手順](#5-新規ページ作成手順)
- [6. 検証チェックリスト](#6-検証チェックリスト)

## クイックスタート

教材ページは外部サイト `https://ai-agent.camp/` で管理されています。

ai-agent-camp での作業:
1. `courses/aiagent/lesson03-core/` に chapter YAML を追加
2. `courses/lessons.manifest.yaml` にレッスンエントリを追加
3. `.claude/commands/lesson/` と `.cursor/commands/lesson/` にコマンドファイルを作成
4. 教材ページリンクは `https://ai-agent.camp/ja/course/module-{N}` を使用

---

## 1. CSSフレームワーク情報

教材HTMLは以下のフレームワークで統一されている。**エージェントが個別に確認する必要はない。**

### CDN（全ページ共通）

```html
<!-- Bootstrap 5.3.8 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">

<!-- Bootstrap Icons 1.11.1 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
```

### カスタムCSS

| ファイル | 用途 |
|---------|------|
| `course/assets/css/bootcamp.css` | メインデザインシステム（1534行） |
| `course/assets/style.css` | 追加スタイル（一部ページで使用） |
| `course/assets/css/deliverable-preview.css` | 成果物プレビュー用（モジュールindexで使用） |

### CSS変数（主要のみ抜粋。全変数は bootcamp.css 参照）

```css
/* Primary Colors */
--primary-navy: #1a365d;
--primary-navy-dark: #0f2744;

/* Accent Colors */
--accent-blue: #4299e1;
--accent-orange: #ed8936;
--accent-green: #48bb78;
--accent-purple: #9f7aea;
--accent-red: #f56565;

/* Typography */
--font-sans: 'Hiragino Sans', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', Consolas, Monaco, monospace;
```

### 主要CSSクラス

| クラス | 用途 | 例 |
|--------|------|-----|
| `.hero` | ヒーローセクション（ページ上部の目立つ帯） | モジュールタイトル表示 |
| `.section-title` | セクション見出し | `<h2 class="section-title">` |
| `.golden-rule-callout` | 3原則セクション（黄色い帯） | モジュールindex必須 |
| `.alert-box info/success/warning` | アラートボックス | ヒント、注意、成功メッセージ |
| `.card` + `.card-header navy/blue/green/purple` | カード | コンテンツカード |
| `.code-block` | コードブロック（コピーボタン対応） | コマンド表示 |
| `.exercise-card` | 演習カード | ハンズオン演習 |
| `.prompt-template` | プロンプトテンプレート | Cursor入力例 |
| `.deliverable-preview` | 成果物プレビュー | 演習の期待出力 |
| `.sidebar` + `.sidebar-nav` | サイドバーナビ | マニュアル用 |
| `.step-number` | ステップ番号バッジ | レッスン番号表示 |
| `.navbar-gradient` | ナビバー背景グラデーション | 全ページ共通 |
| `.page-wrapper` | bodyクラス（manual/slides用レイアウト調整） | `<body class="page-wrapper">` |

---

## 2. テンプレート構造（3種類）

教材HTMLは3つのテンプレートに分類される。テンプレートファイルは `course/_templates/` にある。

### A. Module Index（モジュール概要ページ）

**外部URL**: `https://ai-agent.camp/ja/course/module-{N}`
**テンプレート**: `course/_templates/module-index.html`（外部サイト用）

```text
┌─────────────────────────────────────┐
│  <head> + CDN + CSS                 │ ← 共通ボイラープレート（15行）
├─────────────────────────────────────┤
│  <nav> ナビゲーション               │ ← 共通（リンク先のみ変更）
├─────────────────────────────────────┤
│  <section class="hero">             │ ← 編集対象：タイトル、バッジ
│    Module番号、タイトル、説明        │
├─────────────────────────────────────┤
│  <section> 3原則（golden-rule）      │ ← 共通テンプレート（変更不要）
├─────────────────────────────────────┤
│  <section> モジュール概要            │ ← ★ 編集対象（メインコンテンツ）
├─────────────────────────────────────┤
│  <section> レッスン一覧              │ ← ★ 編集対象
├─────────────────────────────────────┤
│  <section> ハンズオン演習            │ ← ★ 編集対象
├─────────────────────────────────────┤
│  <section> リソース                  │ ← ★ 編集対象
├─────────────────────────────────────┤
│  フッターナビゲーション              │ ← 共通（リンク先のみ変更）
├─────────────────────────────────────┤
│  <footer> + Bootstrap JS + copyCode │ ← 共通ボイラープレート（30行）
└─────────────────────────────────────┘
```

### B. Manual（実践マニュアル）

**外部URL**: `https://ai-agent.camp/ja/course/module-{N}`
**テンプレート**: `course/_templates/manual.html`（外部サイト用）

```text
┌─────────────────────────────────────┐
│  <head> + CDN + CSS                 │ ← 共通ボイラープレート（10行）
├─────────────────────────────────────┤
│  <nav> ナビゲーション               │ ← 共通（リンク先のみ変更）
├─────────────────────────────────────┤
│  <div class="layout-container">     │
│    ┌───────┬───────────────────┐    │
│    │Sidebar│ Main Content      │    │
│    │（目次）│                   │    │
│    │       │ ★ 編集対象        │    │
│    │       │ セクション群       │    │
│    │       │ フッターナビ       │    │
│    └───────┴───────────────────┘    │
├─────────────────────────────────────┤
│  <footer> + Bootstrap JS + copyCode│ ← 共通ボイラープレート（40行）
└─────────────────────────────────────┘
```

### C. Slides（プレゼンテーション）

**外部URL**: `https://ai-agent.camp/ja/course/module-{N}`
**テンプレート**: `course/_templates/slides.html`（外部サイト用）

```text
┌─────────────────────────────────────┐
│  <head> + CDN + CSS + スライドCSS   │ ← 共通ボイラープレート（150行）
├─────────────────────────────────────┤
│  <div class="slide-header">         │ ← 共通（タイトルのみ変更）
├─────────────────────────────────────┤
│  <div class="slides-container">     │
│    ┌───────┬───────────────────┐    │
│    │Slide  │ Slide Content     │    │
│    │List   │                   │    │
│    │       │ ★ 各スライド      │    │
│    └───────┴───────────────────┘    │
├─────────────────────────────────────┤
│  <div class="slide-controls">       │ ← 共通ボイラープレート
├─────────────────────────────────────┤
│  スライド制御JavaScript              │ ← 共通ボイラープレート（50行）
└─────────────────────────────────────┘
```

---

## 3. 相対パス規則

HTMLファイルの階層に応じて、アセットや他ページへの相対パスが変わる。

| ファイルの場所 | index.htmlへのパス | assets/へのパス |
|---------------|-------------------|----------------|
| `course/setup/*.html` | `../index.html` | `../assets/` |
| `course/foundation/*.html` | `../index.html` | `../assets/` |
| 教材ページ（外部） | `https://ai-agent.camp/ja/course/module-{N}` | 外部サイトで管理 |

### 画像パス規約

画像は `course/assets/images/` に配置。

| カテゴリ | パス | 用途 |
|---------|------|------|
| モジュール別 | `course/assets/images/module{N}/` | 各モジュールの画像 |
| Foundation | `course/assets/images/{topic}/` | 基礎教材（llm-basics/, agents/ 等） |
| 共通 | `course/assets/images/common/` | サイト共通アイコン等 |

---

## 4. セクション単位編集ガイド

### 並列リライト時の手順

複数のHTMLファイルを並列エージェントでリライトする場合、以下の手順でコンテキスト消費を最小化する。

#### Step 1: 編集対象セクションの特定

ファイル全体を読み込む前に、まず行数を確認してセクション範囲を特定する。

```text
Read tool で offset/limit を使い、編集対象セクションのみ読む。
例: "概要セクション（行50-100）のみリライトする"
```

#### Step 2: エージェントへの指示テンプレート

並列エージェントに渡すプロンプトには、以下の情報を含める：

```markdown
## 編集対象
- 対象: https://ai-agent.camp/ja/course/module-X（外部サイト）
- 編集範囲: 行XX〜行YY（○○セクション）
- 変更しないこと: nav, footer, golden-rule-callout, Bootstrap CDN/JS

## CSSフレームワーク（参照のみ）
- Bootstrap 5.3.8 + Bootstrap Icons 1.11.1
- カスタムCSS: bootcamp.css
- 主要クラス: .section-title, .alert-box, .card, .code-block, .exercise-card

## 編集内容
[具体的な変更指示をここに記載]
```

#### Step 3: Edit toolでセクション単位の編集

Read toolで対象セクションを読み、Edit toolで差分のみ変更する。ファイル全体のWrite は避ける。

### 注意事項

- **3原則セクション（golden-rule-callout）は編集しない**: 全モジュールindexで共通のため
- **copyCode関数は変更しない**: フッターのJavaScriptは全ページ共通
- **CDN URLは変更しない**: integrity ハッシュが一致しなくなる

---

## 5. 新規ページ作成手順

### テンプレートからの作成

1. `course/_templates/` から適切なテンプレートをコピー
2. プレースホルダー（`{{MODULE_NUMBER}}` 等）を置換
3. メインコンテンツセクションを記述
4. 画像を `course/assets/images/module{N}/` に配置

### プレースホルダー一覧

| プレースホルダー | 置換先 | 例 |
|-----------------|--------|-----|
| `{{MODULE_NUMBER}}` | モジュール番号 | `1` |
| `{{MODULE_TITLE}}` | モジュールタイトル | `バナー・画像生成` |
| `{{MODULE_ICON}}` | Bootstrap Iconクラス | `bi-image` |
| `{{MODULE_DURATION}}` | 所要時間 | `約90分` |
| `{{MODULE_LESSONS}}` | レッスン数 | `3レッスン` |
| `{{MODULE_LEAD}}` | リード文 | `banner-creatorと...` |
| `{{SKILLS_USED}}` | 使用スキル | `banner-creator / nanobanana` |
| `{{PREV_MODULE_LINK}}` | 前モジュールリンク | `../../index.html` |
| `{{NEXT_MODULE_NUMBER}}` | 次モジュール番号 | `2` |
| `{{NEXT_MODULE_LINK}}` | 次モジュールリンク | `../2-diagram/index.html` |
| `{{NEXT_MODULE_TITLE}}` | 次モジュール名 | `Module 2 - 図表・フロー作成` |
| `{{CONTENT}}` | メインコンテンツ（Manual用） | HTML記述 |
| `{{CONTENT_OVERVIEW}}` | モジュール概要（Index用） | HTML記述 |
| `{{CONTENT_LESSONS}}` | レッスン一覧（Index用） | HTML記述 |
| `{{CONTENT_EXERCISES}}` | ハンズオン演習（Index用） | HTML記述 |
| `{{CONTENT_RESOURCES}}` | リソース（Index用） | HTML記述 |
| `{{PREV_MODULE_TITLE}}` | 前モジュール名 | `ホーム` |
| `{{SIDEBAR_ITEMS}}` | サイドバー項目（Manual用） | `<li>` 要素群 |
| `{{SLIDE_SUBTITLE}}` | スライド副題（Slides用） | `スキルと活用法` |
| `{{SLIDE_INTRO}}` | スライド導入文（Slides用） | テキスト |
| `{{SLIDE_CONTENT}}` | スライドHTML（Slides用） | `<div class="slide">` 群 |
| `{{SLIDE_DATA}}` | スライドデータ（Slides用） | JS オブジェクト配列 |

---

## 6. 検証チェックリスト

教材HTMLを編集・作成した後は以下を確認:

- [ ] Bootstrap CDN（CSS + JS）が正しく読み込まれている
- [ ] bootcamp.css が正しい相対パスで読み込まれている
- [ ] ナビゲーションリンクが正しい相対パスになっている
- [ ] 画像パスが `course/assets/images/` 規約に従っている
- [ ] モジュールindexには3原則セクション（golden-rule-callout）が含まれている
- [ ] フッターナビゲーションのリンク先が正しい
- [ ] copyCode関数が含まれている（コードブロック使用時）
- [ ] HTMLが valid（閉じタグ忘れがない）

---

最終更新: 2026-02-17 17:42:00 JST

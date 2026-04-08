---
description: "When the user says /start-18-13 — Module 18 Lesson 18-13: PM - HTML + Tailwind CSS プロトタイプ実装"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "30分"
category: "lesson"
prerequisites: ["start-18-12"]
level: "intermediate"
tags: ["pm", "ui", "prototype", "html", "tailwind"]
---

# 🎓 Lesson 18-13: HTML + Tailwind CSS プロトタイプ

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowのPencilデザインをHTML + Tailwind CSSで実装し、動くプロトタイプを作成する |
| 所要時間 | 約30分 |
| 使うスキル | - |
| 前提条件 | Lesson 18-12 完了、Pencilデザインが存在する |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

---

## 📍 何を学ぶのか

このレッスンでは、Pencilで作成したPM向けダッシュボードデザインを、実際に動作するHTMLプロトタイプに変換します。Tailwind CSSを使い、レスポンシブ対応した実装を目指します。

**学習ポイント：**
- Tailwind CDNによる高速プロトタイピング
- HTML構造とコンポーネント設計
- CSSフレームワークの効率的な活用
- レスポンシブデザイン実装

---

## 🚀 Step 1: プロジェクト初期化（HTML + Tailwind CDN）

### 1-1. 構成方法の選択

```json
{
  "type": "AskQuestion",
  "question": "プロトタイプの構成を選んでください",
  "hint": "CDN版は素早く始められます。ビルド版は本番に近い環境です。",
  "options": [
    {
      "label": "単一HTML（CDN版）",
      "description": "index.htmlのみで完結。最も簡単。",
      "value": "single-html"
    },
    {
      "label": "マルチページ（CDN版）",
      "description": "複数HTMLファイル。ページ遷移を含める。",
      "value": "multi-page"
    },
    {
      "label": "Vite + Tailwind（ビルドあり）",
      "description": "npm、ビルドプロセス付き。本番環境に近い。",
      "value": "vite-build"
    },
    {
      "label": "AIに最適な構成を提案してもらう",
      "description": "コースの目的に合わせた提案を受ける。",
      "value": "ai-suggest"
    }
  ]
}
```

### 1-2. プロジェクト構造を作成

```text
output/pm/prototype/
├── index.html          # ダッシュボード画面
├── tasks.html          # タスク管理画面
├── task-detail.html    # タスク詳細画面
├── styles.css          # カスタムスタイル（必要に応じて）
└── app.js              # JavaScriptロジック（CRUD選択時）
```

**実行コマンド：**
```bash
mkdir -p output/pm/prototype
```

### 1-3. index.html の基本構造

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TaskFlow - PM Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    /* Custom styles */
  </style>
</head>
<body class="bg-gray-50">
  <!-- Header -->
  <header class="bg-white border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <h1 class="text-2xl font-bold text-gray-900">TaskFlow</h1>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Dashboard sections will be added here -->
  </main>

  <script src="app.js"></script>
</body>
</html>
```

---

## 📍 Step 2: ダッシュボード画面の実装

### 2-1. 実装アプローチの選択

```json
{
  "type": "AskQuestion",
  "question": "実装の進め方を選んでください",
  "hint": "Pencilデザインをどの程度参考にするかで効率が変わります。",
  "options": [
    {
      "label": "Pencilデザインから自動変換",
      "description": "AIが設計図を読み込んで変換（ツール利用）",
      "value": "auto-convert"
    },
    {
      "label": "セクションごとに手動実装",
      "description": "デザイン仕様を見ながら手で書く。学習効果高。",
      "value": "manual-section"
    },
    {
      "label": "AIに一括生成してもらう",
      "description": "Pencilファイルをアップロードしてコード生成",
      "value": "ai-generate"
    }
  ]
}
```

### 2-2. ダッシュボード構成要素

**必須要素：**
- ヘッダー（ユーザー情報、ナビゲーション）
- サイドバー（メニュー）
- 統計カード（タスク数、完了率等）
- タスクリスト（今日のタスク）
- プロジェクト一覧
- アクティビティフィード

### 2-3. 実装サンプル（セクションごと）

**ヘッダー実装：**
```html
<header class="bg-white shadow sticky top-0 z-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
    <div class="flex items-center">
      <h1 class="text-2xl font-bold text-blue-600">TaskFlow</h1>
    </div>
    <div class="flex items-center gap-4">
      <button class="p-2 hover:bg-gray-100 rounded-lg">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
        </svg>
      </button>
      <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-bold">
        PM
      </div>
    </div>
  </div>
</header>
```

**統計カード実装：**
```html
<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
  <!-- Total Tasks Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">全タスク数</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">24</p>
      </div>
      <div class="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
      </div>
    </div>
  </div>

  <!-- Completed Tasks Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">完了したタスク</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">16</p>
      </div>
      <div class="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center">
        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
    </div>
  </div>

  <!-- In Progress Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">進行中</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">5</p>
      </div>
      <div class="w-12 h-12 rounded-lg bg-yellow-100 flex items-center justify-center">
        <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
      </div>
    </div>
  </div>

  <!-- Completion Rate Card -->
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-gray-600 text-sm font-medium">完了率</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">67%</p>
      </div>
      <div class="w-12 h-12 rounded-lg bg-purple-100 flex items-center justify-center">
        <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
      </div>
    </div>
  </div>
</div>
```

**タスクリスト実装：**
```html
<div class="bg-white rounded-lg shadow overflow-hidden">
  <div class="px-6 py-4 border-b border-gray-200">
    <h2 class="text-lg font-semibold text-gray-900">今日のタスク</h2>
  </div>
  <div class="divide-y divide-gray-200">
    <!-- Task Item -->
    <div class="px-6 py-4 hover:bg-gray-50 transition cursor-pointer flex items-center gap-4">
      <input type="checkbox" class="w-5 h-5 text-blue-600 rounded cursor-pointer">
      <div class="flex-1">
        <p class="font-medium text-gray-900">ユーザー認証機能の実装</p>
        <p class="text-sm text-gray-600 mt-1">Backend Team</p>
      </div>
      <span class="px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">高優先度</span>
      <span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full">進行中</span>
    </div>

    <!-- More task items -->
    <div class="px-6 py-4 hover:bg-gray-50 transition cursor-pointer flex items-center gap-4">
      <input type="checkbox" class="w-5 h-5 text-blue-600 rounded cursor-pointer">
      <div class="flex-1">
        <p class="font-medium text-gray-900">データベース設計レビュー</p>
        <p class="text-sm text-gray-600 mt-1">Database Team</p>
      </div>
      <span class="px-3 py-1 bg-green-100 text-green-700 text-sm font-medium rounded-full">中優先度</span>
      <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-full">未開始</span>
    </div>
  </div>
</div>
```

---

## 📍 Step 3: タスクCRUD画面の実装

### 3-1. 機能レベルの選択

```json
{
  "type": "AskQuestion",
  "question": "タスク画面の機能レベルを選んでください",
  "hint": "JavaScriptなし（静的）が最もシンプル。LocalStorageなら保存されます。",
  "options": [
    {
      "label": "表示のみ（静的HTML）",
      "description": "HTMLの表示とCSSのみ。インタラクションなし。",
      "value": "static-only"
    },
    {
      "label": "簡易インタラクション（JS付き）",
      "description": "モーダル表示、フォーム入力等。ただしメモリ内のみ。",
      "value": "js-interaction"
    },
    {
      "label": "フルCRUD（LocalStorage使用）",
      "description": "Create/Read/Update/Delete全機能。ブラウザに保存。",
      "value": "localstorage-crud"
    }
  ]
}
```

### 3-2. tasks.html - タスク一覧ページ

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TaskFlow - Tasks</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <!-- Header -->
  <header class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
      <a href="index.html" class="text-2xl font-bold text-blue-600">TaskFlow</a>
      <a href="index.html" class="text-gray-600 hover:text-gray-900">← ダッシュボードに戻る</a>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Title and Action -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">タスク管理</h1>
      <button id="newTaskBtn" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        + 新しいタスク
      </button>
    </div>

    <!-- Filter Tabs -->
    <div class="flex gap-2 mb-6 border-b border-gray-200">
      <button class="px-4 py-2 text-gray-900 font-medium border-b-2 border-blue-600">全て</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">進行中</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">完了</button>
      <button class="px-4 py-2 text-gray-600 hover:text-gray-900">期限超過</button>
    </div>

    <!-- Task Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">タスク名</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">チーム</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">優先度</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">ステータス</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">期限</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">アクション</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <!-- Task rows will be generated here -->
          <tr class="hover:bg-gray-50 transition">
            <td class="px-6 py-4"><a href="task-detail.html" class="text-blue-600 hover:underline font-medium">ユーザー認証実装</a></td>
            <td class="px-6 py-4 text-gray-900">Backend</td>
            <td class="px-6 py-4"><span class="px-3 py-1 bg-red-100 text-red-700 text-sm font-medium rounded-full">高</span></td>
            <td class="px-6 py-4"><span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full">進行中</span></td>
            <td class="px-6 py-4 text-gray-900">2024-01-25</td>
            <td class="px-6 py-4 text-right">
              <button class="text-blue-600 hover:text-blue-900 mr-3">編集</button>
              <button class="text-red-600 hover:text-red-900">削除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>

  <!-- New Task Modal -->
  <div id="taskModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full mx-4 p-6">
      <h2 class="text-xl font-bold mb-4">新しいタスク</h2>
      <form>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">タスク名</label>
          <input type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">説明</label>
          <textarea class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" rows="3"></textarea>
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">優先度</label>
          <select class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option>低</option>
            <option>中</option>
            <option selected>高</option>
          </select>
        </div>
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">期限</label>
          <input type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        <div class="flex gap-3">
          <button type="button" id="closeModalBtn" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">キャンセル</button>
          <button type="submit" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">作成</button>
        </div>
      </form>
    </div>
  </div>

  <script src="app.js"></script>
</body>
</html>
```

### 3-3. task-detail.html - タスク詳細ページ

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TaskFlow - Task Detail</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <!-- Header -->
  <header class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
      <a href="index.html" class="text-2xl font-bold text-blue-600">TaskFlow</a>
      <a href="tasks.html" class="text-gray-600 hover:text-gray-900">← タスク一覧に戻る</a>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="grid grid-cols-3 gap-8">
      <!-- Main Content -->
      <div class="col-span-2">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex justify-between items-start mb-6">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">ユーザー認証機能の実装</h1>
              <p class="text-gray-600 mt-2">タスクID: #2401</p>
            </div>
            <button class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">編集</button>
          </div>

          <!-- Description -->
          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-2">説明</h2>
            <p class="text-gray-700">ユーザーの認証機能を実装する。OAuth2.0を使用し、Google、GitHub、Microsoft アカウントでのログインに対応する必要がある。</p>
          </div>

          <!-- Details Grid -->
          <div class="grid grid-cols-2 gap-6 mb-6">
            <div>
              <p class="text-sm font-medium text-gray-600">チーム</p>
              <p class="text-gray-900 mt-1">Backend</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">担当者</p>
              <p class="text-gray-900 mt-1">山田太郎</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">優先度</p>
              <span class="inline-block px-3 py-1 bg-red-100 text-red-700 text-sm font-medium rounded-full mt-1">高</span>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-600">ステータス</p>
              <span class="inline-block px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-medium rounded-full mt-1">進行中</span>
            </div>
          </div>

          <!-- Checklist -->
          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">チェックリスト</h2>
            <div class="space-y-2">
              <label class="flex items-center">
                <input type="checkbox" checked class="w-4 h-4 text-green-600 rounded">
                <span class="ml-3 text-gray-700">OAuth2.0の調査と設計</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" checked class="w-4 h-4 text-green-600 rounded">
                <span class="ml-3 text-gray-700">認証ライブラリの選定</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" class="w-4 h-4 text-blue-600 rounded">
                <span class="ml-3 text-gray-700">実装とテスト</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" class="w-4 h-4 text-blue-600 rounded">
                <span class="ml-3 text-gray-700">本番環境へのデプロイ</span>
              </label>
            </div>
          </div>

          <!-- Comments Section -->
          <div>
            <h2 class="text-lg font-semibold text-gray-900 mb-4">コメント</h2>
            <div class="space-y-4">
              <div class="border-t pt-4">
                <p class="font-medium text-gray-900">山田太郎</p>
                <p class="text-sm text-gray-600">2024-01-20</p>
                <p class="text-gray-700 mt-2">Google認証は完了しました。次はGitHub認証に取り組みます。</p>
              </div>
            </div>
            <div class="mt-4">
              <input type="text" placeholder="コメントを入力..." class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div>
        <div class="bg-white rounded-lg shadow p-6 sticky top-20">
          <h3 class="font-semibold text-gray-900 mb-4">プロジェクト情報</h3>
          <div class="space-y-4">
            <div>
              <p class="text-sm text-gray-600">開始日</p>
              <p class="text-gray-900 font-medium">2024-01-15</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">期限</p>
              <p class="text-gray-900 font-medium">2024-01-25</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">進捗</p>
              <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div class="bg-blue-600 h-2 rounded-full" style="width: 60%"></div>
              </div>
              <p class="text-sm text-gray-600 mt-1">60% 完了</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</body>
</html>
```

---

## 📍 Step 4: レスポンシブ対応・動作確認

### 4-1. 確認方法の選択

```json
{
  "type": "AskQuestion",
  "question": "確認方法を選んでください",
  "hint": "手動確認で実感できます。チェックリストで漏らしなく確認できます。",
  "options": [
    {
      "label": "ブラウザで手動確認",
      "description": "複数デバイスで開いて見た目を確認する。",
      "value": "manual-browser"
    },
    {
      "label": "レスポンシブチェックリストで確認",
      "description": "提供されたチェックリスト項目に沿って確認。",
      "value": "checklist-verification"
    },
    {
      "label": "AIにコードレビューしてもらう",
      "description": "HTMLとCSSをAIが検査し、改善案を提示。",
      "value": "ai-review"
    }
  ]
}
```

### 4-2. レスポンシブ確認チェックリスト

**モバイル表示（320px～480px）**
- [ ] ヘッダーのナビゲーションが折り畳まれている
- [ ] タスクカードが1列で積み重ねられている
- [ ] ボタンのサイズが大きく、タップしやすい（48px×48px以上）
- [ ] テキストが読みやすいサイズ（16px以上）
- [ ] 横スクロールが発生していない

**タブレット表示（768px～1024px）**
- [ ] 統計カードが2列～3列で表示されている
- [ ] サイドバーとメインコンテンツが並んで表示
- [ ] テーブルが見やすく表示されている

**デスクトップ表示（1024px以上）**
- [ ] レイアウトが最大幅（max-w-7xl）に制限されている
- [ ] 統計カードが4列で表示
- [ ] ホバー効果が正常に動作している
- [ ] 全ての機能が期待通りに表示

### 4-3. Tailwind CSSのレスポンシブクラス

```html
<!-- 例：異なるスクリーンサイズで異なるグリッドを使う -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  <!-- モバイル: 1列、タブレット: 2列、デスクトップ: 4列 -->
</div>
```

**Tailwindの主なブレークポイント：**
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

---

## ⚠️ トラブルシューティング

### Tailwind CDNが読み込まれない
- ブラウザの開発者ツール（F12）で「Network」タブを確認
- CDNのステータスが200番台か確認
- キャッシュをクリアして再読み込み（Ctrl+Shift+Delete）

### レイアウトが崩れる
- `max-w-` クラスが親要素に適用されているか確認
- パディング・マージン設定を確認（`px-`, `py-` など）
- ネストの深さを確認（過度にネストしていないか）

### Pencilデザインとの差異
- Pencilファイルと実装を並べて確認
- 色コード（HEX値）が正確か確認
- フォントサイズが一致しているか確認（Tailwind のサイズ定義）
- 要素の配置（flexbox/grid）が設計通りか確認

### JavaScriptが動作しない
- `app.js` が正しくロードされているか確認（F12で確認）
- ブラウザコンソールでエラーを確認（F12 → Console）
- イベントリスナーが正しく登録されているか確認

---

## ✅ チェックポイント

プロトタイプ完成の確認項目：

```json
{
  "type": "AskQuestion",
  "question": "全て完了しましたか？",
  "hint": "下記の項目を全てチェックしてから次に進んでください。",
  "checkpoints": [
    {
      "item": "prototype/index.html が存在する",
      "checked": false
    },
    {
      "item": "ダッシュボード画面が表示される",
      "checked": false
    },
    {
      "item": "タスク一覧画面が表示される",
      "checked": false
    },
    {
      "item": "タスク詳細画面が表示される",
      "checked": false
    },
    {
      "item": "レスポンシブ対応済み（モバイル/タブレット/デスクトップで確認）",
      "checked": false
    },
    {
      "item": "ブラウザで動作確認済み（エラーなし）",
      "checked": false
    },
    {
      "item": "Pencilデザインとの見た目が一致している",
      "checked": false
    },
    {
      "item": "JavaScriptインタラクション（選択した場合）が動作している",
      "checked": false
    }
  ]
}
```


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/integration-test-evidence/
└──   (結合テストエビデンス)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/integration-test-evidence/

# 冒頭を確認（最初の30行）
head -30 output/pm/integration-test-evidence/
```

> 💡 全文を確認: `cat output/pm/integration-test-evidence/` で全文表示できます

---

## ➡️ 次のステップ

✅ このレッスンを完了したら、以下に進みます：

**[Lesson 18-14: Playwright E2Eテスト](./start-18-14.md)**
- プロトタイプの自動テストを実装
- ページ遷移、フォーム入力、ボタンクリックなど主要機能をテスト
- CI/CD統合の基礎

---

## 📚 参考資料

- [Tailwind CSS 公式ドキュメント](https://tailwindcss.com/docs)
- [MDN - HTML セマンティック要素](https://developer.mozilla.org/ja/docs/Glossary/Semantics)
- [Flexbox & Grid - CSS-Tricks](https://css-tricks.com/)
- [アクセシビリティ入門 - WAI](https://www.w3.org/WAI/fundamentals/accessibility-intro/ja)

---

**Created with Claude Code - PM Training Course**

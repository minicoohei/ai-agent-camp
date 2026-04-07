---
description: "When the user says /start-18-14 — Module 18 Lesson 18-14: PM - Playwright E2Eテスト"
duration: "25分"
category: "lesson"
prerequisites: ["start-18-13", "output/pm/prototype/"]
level: "intermediate"
tags: ["pm", "test", "e2e", "playwright"]
---

# 🎓 Lesson 18-14: Playwright E2Eテスト

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowプロトタイプに対するPlaywright E2Eテストコードを生成し、実行する |
| 所要時間 | 約25分 |
| 使うスキル | test-planner スキル |
| 前提条件 | Lesson 18-13 完了、output/pm/prototype/ にHTMLプロトタイプが存在する |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

---

## 📍 Step 1: Playwright環境セットアップ

Playwrightはブラウザの自動テストを実行するためのツールです。このステップでは、TaskFlowプロトタイプをテストするための環境を整備します。

### 環境セットアップの流れ

1. npm init playwright@latest で新規プロジェクトを初期化
2. playwright.config.ts で基本設定を実施
3. ブラウザドライバーをインストール
4. テスト実行環境の確認

```json
{
  "type": "AskQuestion",
  "question": "Playwrightの経験はありますか？",
  "options": [
    {
      "id": "beginner",
      "label": "初めて使う",
      "value": "beginner",
      "description": "詳細なセットアップガイダンスを提供"
    },
    {
      "id": "intermediate",
      "label": "基本は知っている",
      "value": "intermediate",
      "description": "標準的なセットアップ手順を提供"
    },
    {
      "id": "advanced",
      "label": "実務経験あり",
      "value": "advanced",
      "description": "最小限のガイダンスで進行"
    },
    {
      "id": "setup_only",
      "label": "セットアップだけ手伝って",
      "value": "setup_only",
      "description": "セットアップスクリプトを実行"
    }
  ],
  "required": true,
  "helpText": "経験レベルに応じて、セットアップガイダンスの詳しさが変わります"
}
```

### セットアップコマンド

**選択肢: 初めて使う / 基本は知っている**

```bash
# プロジェクトディレクトリに移動（プロトタイプのあるディレクトリ）
cd output/pm

# Playwright初期化（対話形式）
npm init playwright@latest

# または明示的なセットアップ
npm install -D @playwright/test
npx playwright install
```

**playwright.config.ts の基本設定**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e-tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npx serve . -l 8080',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
  },
});
```

✅ **チェックポイント: Playwright環境構築済み**

```bash
npx playwright --version  # v1.40.0 以上で確認
ls -la playwright.config.ts  # 設定ファイル確認
```

---

## 📍 Step 2: E2Eテストシナリオの設計

TaskFlowプロトタイプに対するテストシナリオを設計します。16-6で定義したユースケースをベースに、主要なユーザーフローをカバーするシナリオを選定します。

### テストシナリオの選定

```json
{
  "type": "AskQuestion",
  "question": "テストシナリオの範囲を選んでください",
  "options": [
    {
      "id": "minimal",
      "label": "基本3シナリオ（最小限）",
      "value": "minimal",
      "description": "主要フローのみをカバーする最小限のテスト"
    },
    {
      "id": "standard",
      "label": "標準5シナリオ（推奨）",
      "value": "standard",
      "description": "主要フロー＋エッジケースをカバー"
    },
    {
      "id": "comprehensive",
      "label": "網羅的（8シナリオ以上）",
      "value": "comprehensive",
      "description": "全ユースケースを網羅的にテスト"
    },
    {
      "id": "ai_suggest",
      "label": "AIに提案してもらう",
      "value": "ai_suggest",
      "description": "AIがプロトタイプを分析し最適なシナリオを提案"
    }
  ],
  "required": true,
  "helpText": "プロトタイプの品質保証範囲に応じて選択してください。推奨は標準5シナリオです"
}
```

### シナリオ定義

**基本3シナリオ（最小限）**

| # | シナリオ名 | テスト対象 | 検証項目 |
|----|----------|----------|--------|
| 1 | ページ読み込み確認 | トップページ表示 | タイトル表示、ヘッダー描画、初期フォーム表示 |
| 2 | タスク作成フロー | メインユースケース | フォーム入力、送信ボタン、完了画面表示 |
| 3 | ナビゲーション確認 | メニュー・ページ遷移 | メニュークリック、ページURL変更、戻るボタン動作 |

**標準5シナリオ（推奨）**

| # | シナリオ名 | テスト対象 | 検証項目 |
|----|----------|----------|--------|
| 1 | ページ読み込み確認 | トップページ表示 | タイトル表示、ヘッダー描画、初期フォーム表示 |
| 2 | タスク作成フロー | メインユースケース | フォーム入力、送信ボタン、完了画面表示 |
| 3 | ナビゲーション確認 | メニュー・ページ遷移 | メニュークリック、ページURL変更、戻るボタン動作 |
| 4 | レスポンシブ表示確認 | モバイル・タブレット | 画面サイズ変更時のレイアウト、タッチ操作 |
| 5 | エラーハンドリング確認 | 入力値検証 | 必須項目空白時のエラー表示、エラーメッセージ確認 |

**網羅的（8シナリオ以上）**

上記5シナリオに加え：

| # | シナリオ名 | テスト対象 | 検証項目 |
|----|----------|----------|--------|
| 6 | ローカルストレージ確認 | データ永続化 | 入力データの保存、ページリロード後の復元 |
| 7 | 複数タスク管理 | リスト機能 | タスク追加・削除・編集、タスク一覧表示 |
| 8 | API連携確認 | バックエンド通信 | API呼び出し、レスポンス処理、ネットワークエラーハンドリング |
| 9 | パフォーマンス確認 | 読み込み速度 | LCP(Largest Contentful Paint)測定、スクロール性能 |

### シナリオマッピング

各シナリオは16-6で定義したユースケースにマッピングされます：

```text
UC-1: タスク作成 → シナリオ#2（標準）
UC-2: タスク一覧表示 → シナリオ#7（網羅的）
UC-3: タスク更新 → シナリオ#7（網羅的）
UC-4: ナビゲーション → シナリオ#3（基本）
UC-5: エラーハンドリング → シナリオ#5（標準）
```

✅ **チェックポイント: テストシナリオ3つ以上設計**

```bash
# テストシナリオドキュメントの作成
cat > output/pm/e2e-tests/SCENARIOS.md << 'EOF'
# E2E Test Scenarios

## Selected Scenarios
- [x] ページ読み込み確認
- [x] タスク作成フロー
- [x] ナビゲーション確認
- [x] (オプション) レスポンシブ表示確認
- [x] (オプション) エラーハンドリング確認
EOF
```

---

## 📍 Step 3: テストコードの自動生成

test-plannerスキルを使用して、設計したシナリオに基づくテストコードを自動生成します。

### テストコード生成方法の選択

```json
{
  "type": "AskQuestion",
  "question": "テストコードの生成方法を選んでください",
  "options": [
    {
      "id": "auto_generate",
      "label": "test-plannerスキルで自動生成",
      "value": "auto_generate",
      "description": "AIがシナリオに基づいてテストコードを一括生成"
    },
    {
      "id": "from_template",
      "label": "テンプレートから修正",
      "value": "from_template",
      "description": "テンプレートをベースにカスタマイズ"
    },
    {
      "id": "interactive",
      "label": "1つずつ対話的に作成",
      "value": "interactive",
      "description": "AIと対話しながら1テストずつ作成"
    },
    {
      "id": "import_existing",
      "label": "既存テストファイルをインポート",
      "value": "import_existing",
      "description": "既存のテストファイルを読み込んで拡張"
    }
  ],
  "required": true,
  "helpText": "効率重視の場合はスキル自動生成、カスタマイズ重視の場合は対話的作成を選択してください"
}
```

### 自動生成（推奨）

```bash
# test-planner スキルを実行
# AIがシナリオに基づいて .spec.ts ファイルを生成します
```

### テストファイル構造

生成されるテストファイルは以下の構造を持ちます：

**01-page-load.spec.ts - ページ読み込み確認**

```typescript
import { test, expect } from '@playwright/test';

test.describe('ページ読み込み確認', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('タイトルが正しく表示される', async ({ page }) => {
    const title = page.locator('h1');
    await expect(title).toContainText('TaskFlow');
  });

  test('ヘッダーが描画される', async ({ page }) => {
    const header = page.locator('header');
    await expect(header).toBeVisible();
  });

  test('初期フォームが表示される', async ({ page }) => {
    const form = page.locator('form');
    await expect(form).toBeVisible();
  });
});
```

**02-task-creation.spec.ts - タスク作成フロー**

```typescript
import { test, expect } from '@playwright/test';

test.describe('タスク作成フロー', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('タスクを作成できる', async ({ page }) => {
    // フォーム入力
    await page.locator('input[name="taskName"]').fill('テストタスク');
    await page.locator('input[name="dueDate"]').fill('2025-12-31');

    // 送信
    await page.locator('button[type="submit"]').click();

    // 完了確認
    const successMessage = page.locator('.success-message');
    await expect(successMessage).toContainText('作成されました');
  });

  test('フォーム送信後、リダイレクトする', async ({ page }) => {
    await page.locator('input[name="taskName"]').fill('テストタスク');
    await page.locator('button[type="submit"]').click();

    // ページがリダイレクトされることを確認
    await page.waitForURL('/tasks');
    expect(page.url()).toContain('/tasks');
  });
});
```

**03-navigation.spec.ts - ナビゲーション確認**

```typescript
import { test, expect } from '@playwright/test';

test.describe('ナビゲーション確認', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('メニューをクリックしてページ遷移', async ({ page }) => {
    await page.locator('a[href="/tasks"]').click();
    await expect(page).toHaveURL('/tasks');
  });

  test('戻るボタンで前のページに戻る', async ({ page }) => {
    await page.goto('/tasks');
    await page.goBack();
    await expect(page).toHaveURL('/');
  });
});
```

**04-responsive.spec.ts - レスポンシブ表示（オプション）**

```typescript
import { test, expect, devices } from '@playwright/test';

test.describe('レスポンシブ表示確認', () => {
  test('モバイル表示でレイアウトが崩れない', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 12'],
    });
    const page = await context.newPage();
    await page.goto('/');

    const header = page.locator('header');
    await expect(header).toBeVisible();

    await context.close();
  });
});
```

**05-error-handling.spec.ts - エラーハンドリング（オプション）**

```typescript
import { test, expect } from '@playwright/test';

test.describe('エラーハンドリング確認', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('必須項目が空の場合、エラーが表示される', async ({ page }) => {
    await page.locator('button[type="submit"]').click();

    const errorMessage = page.locator('.error-message');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('必須項目');
  });

  test('無効な日付形式でエラーが表示される', async ({ page }) => {
    await page.locator('input[name="dueDate"]').fill('invalid-date');
    await page.locator('button[type="submit"]').click();

    const errorMessage = page.locator('.error-message');
    await expect(errorMessage).toContainText('日付形式が正しくありません');
  });
});
```

### ファイル配置

生成されたテストファイルは以下の構造で配置されます：

```text
output/pm/
├── e2e-tests/
│   ├── 01-page-load.spec.ts
│   ├── 02-task-creation.spec.ts
│   ├── 03-navigation.spec.ts
│   ├── 04-responsive.spec.ts (オプション)
│   ├── 05-error-handling.spec.ts (オプション)
│   ├── SCENARIOS.md
│   └── fixtures/ (必要に応じて)
├── playwright.config.ts
└── package.json
```

✅ **チェックポイント: テストコード(.spec.ts)生成済み**

```bash
# テストファイルの確認
ls -la output/pm/e2e-tests/*.spec.ts

# テストコードの構文チェック
npx tsc --noEmit e2e-tests/*.spec.ts
```

---

## 🚀 Step 4: テスト実行 & レポート確認

生成したテストコードを実行し、結果を確認します。

### テスト実行方法の選択

```json
{
  "type": "AskQuestion",
  "question": "テストの実行方法を選んでください",
  "options": [
    {
      "id": "run_all",
      "label": "全テスト実行（推奨）",
      "value": "run_all",
      "description": "全テストスイートを一括実行しレポート生成"
    },
    {
      "id": "headless",
      "label": "ヘッドレスモード（速い）",
      "value": "headless",
      "description": "ブラウザ非表示で高速実行"
    },
    {
      "id": "ui_mode",
      "label": "UIモード（ブラウザ表示）",
      "value": "ui_mode",
      "description": "ブラウザを表示して動作を目視確認"
    },
    {
      "id": "one_by_one",
      "label": "1テストずつ確認",
      "value": "one_by_one",
      "description": "テストを1つずつ実行して結果を確認"
    }
  ],
  "required": true,
  "helpText": "初回はUIモードで動作確認、以降はヘッドレスで高速実行することをお勧めします"
}
```

### 全テスト実行

```bash
# プロトタイプサーバーが起動していることを確認
# （playwright.config.ts の webServer 設定で自動起動）

# テスト実行
npx playwright test

# または個別実行
npx playwright test 01-page-load.spec.ts
npx playwright test 02-task-creation.spec.ts
```

### ヘッドレスモード実行（高速）

```bash
npx playwright test --headed=false

# CI環境向け
CI=true npx playwright test
```

### UIモード実行（ブラウザ表示）

```bash
npx playwright test --ui

# または特定のテストをUIモードで実行
npx playwright test 02-task-creation.spec.ts --ui
```

### 1テストずつ確認

```bash
# デバッグモードで実行
npx playwright test --debug

# または Playwright Inspector を使用
PWDEBUG=1 npx playwright test 02-task-creation.spec.ts
```

### レポート確認

```bash
# HTMLレポートを生成・表示
npx playwright show-report

# レポート生成のみ（表示しない）
npx playwright test --reporter=html
```

生成されるレポートには以下の情報が含まれます：

- ✅ **成功したテスト**: チェックマーク、実行時間
- ❌ **失敗したテスト**: スタックトレース、スクリーンショット
- ⚠️ **スキップされたテスト**: スキップ理由
- 📊 **統計**: 合計実行数、成功数、失敗数、スキップ数
- 📸 **スクリーンショット**: failure-on-error で自動キャプチャ

### トラブルシューティング

| 問題 | 原因と対処法 |
|------|----------|
| **Playwrightインストールエラー** | `npm install` 後に `npx playwright install` を実行 |
| **ブラウザが起動しない** | `npx playwright install chromium` でブラウザドライバー再インストール |
| **セレクタが見つからない** | `npx playwright test --debug` でDOM構造を確認し、セレクタを修正 |
| **テストがタイムアウト** | `timeout: 30000` を playwright.config.ts で指定、または `test.setTimeout(30000)` |
| **webServer が起動しない** | package.json の `dev` スクリプトを確認、ポート競合を確認 |

✅ **チェックポイント: テスト実行成功**

```bash
# テスト結果確認
# 実行結果が "X passed" で終了することを確認
npx playwright test

# レポート確認
npx playwright show-report
```

---

## ✅ 完了確認

以下の項目が完了していることを確認してください：

- ✅ Playwright環境構築済み
  - `npx playwright --version` で v1.40.0 以上
  - playwright.config.ts が設定済み

- ✅ テストシナリオ3つ以上設計
  - output/pm/e2e-tests/SCENARIOS.md に記載
  - 16-6 のユースケースとマッピング完了

- ✅ テストコード(.spec.ts)生成済み
  - output/pm/e2e-tests/ に *.spec.ts ファイルが存在
  - 各ファイルが test.describe, test.beforeEach, 複数の test() を含む

- ✅ テスト実行成功
  - `npx playwright test` で "X passed" を確認
  - 失敗がないこと（または既知の失敗のみ）

- ✅ レポート確認済み
  - `npx playwright show-report` でHTMLレポート表示
  - 各テストの詳細が確認できること

---

## ⚠️ 注意事項

- **ブラウザドライバー**: 初回セットアップ時は `npx playwright install` で各ブラウザをインストール（約500MB）
- **ローカルサーバー**: WebServer設定がない場合は別ターミナルで `npm run dev` を実行
- **セレクタメンテナンス**: プロトタイプUIが変更される場合、テストコードのセレクタも修正が必要
- **CI/CD統合**: GitHub Actions や GitLab CI を使用する場合は、runner に Playwright dependencies のインストールステップを追加


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── deployment-plan.md  (デプロイ計画)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/deployment-plan.md

# 冒頭を確認（最初の30行）
head -30 output/pm/deployment-plan.md
```

> 💡 全文を確認: `cat output/pm/deployment-plan.md` で全文表示できます

---

## ➡️ 次のステップ

**→ Lesson 18-15: テスト計画書 & テストケース生成**

次のレッスンでは、以下を実施します：

- テスト計画書（Test Plan）の作成
- 詳細なテストケース（Test Cases）の生成
- テスト結果レポートの自動作成

**注記**: Phase C（デザイン・実装）が完了しました！
次のLesson 18-15からPhase D（テスト・運用）に進みます。

---

## 📚 関連リソース

- [Playwright Official Documentation](https://playwright.dev/)
- [Playwright Test API Reference](https://playwright.dev/docs/api/class-test)
- [Best Practices for E2E Testing](https://playwright.dev/docs/best-practices)
- [前のレッスン: Lesson 18-13](./start-18-13.md)
- [モジュールトップ: Module 18 PM System Definition](https://ai-agent.camp/ja/course/module-18)

---

**作成日**: 2025年02月
**コース**: TaskFlow PM Training Course
**フェーズ**: Phase C - Design & Implementation (最終段階)

---
name: test-planner
description: "テスト計画書・テストケース・テストレポートの生成に使用。 「テスト計画を作って」「テストケースを生成して」「E2Eテストを書いて」等で発動。"
triggers:
  - テスト計画を作って
  - テストケースを生成
  - E2Eテストを書いて
  - テスト結果サマリー
  - テスト観点を分析
  - test-planner
  - Playwright テスト
---

# Test Planner - テスト計画・実行支援ツール

ユースケースからテスト計画書、テストケース、テストコードを自動生成します。

## Workflow

1. ユースケース記述（usecases.md）を入力として受け取る
2. テスト観点を分析（正常系/異常系/境界値/セキュリティ）
3. テスト計画書・テストケースを構造化して出力
4. 必要に応じてPlaywright E2Eテストコードを生成

## Templates

### テスト計画書テンプレート

```markdown
# テスト計画書: {システム名}

## 1. テスト概要
### 1.1 テスト目的
### 1.2 テスト範囲
### 1.3 テスト環境

## 2. テスト方針
### 2.1 テストレベル
| レベル | 対象 | 手法 | ツール |
|--------|------|------|-------|
| 単体テスト | 個別関数・メソッド | ホワイトボックス | pytest |
| 結合テスト | API間連携 | グレーボックス | pytest + requests |
| E2Eテスト | 画面操作フロー | ブラックボックス | Playwright |

### 2.2 テスト観点
- 機能テスト（正常系・異常系）
- 境界値テスト
- セキュリティテスト（認証・認可）
- 性能テスト（レスポンスタイム）
- ユーザビリティテスト

## 3. テストスケジュール
| フェーズ | 期間 | 担当 | 成果物 |
|---------|------|------|--------|

## 4. 合否判定基準
- 全テストケース実行率: 100%
- 重大バグ（Severity: Critical/High）: 0件
- テストカバレッジ: 80%以上
```

### テストケーステンプレート

```markdown
# テストケース一覧

## TC-{番号}: {テスト名}
- **テストレベル:** 単体 / 結合 / E2E
- **対応ユースケース:** UC-{番号}
- **前提条件:**
- **テスト手順:**
  1. {手順1}
  2. {手順2}
  3. {手順3}
- **期待結果:**
- **テストデータ:**
- **優先度:** High / Medium / Low
- **結果:** ⬜ 未実施 / ✅ 成功 / ❌ 失敗
```

### Playwright E2Eテストテンプレート

```typescript
import { test, expect } from '@playwright/test';

test.describe('{機能名}', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('{テスト名}', async ({ page }) => {
    // Arrange
    // Act
    // Assert
    await expect(page.locator('{selector}')).toBeVisible();
  });
});
```

### テストエビデンステンプレート

```markdown
# テストエビデンス: {テストケースID}

## 実行情報
- 実行日時: {datetime}
- 実行者: {name}
- 環境: {environment}

## 結果
- ステータス: ✅ 成功 / ❌ 失敗
- スクリーンショット: {path}
- ログ: {path}

## 備考
```

### テスト結果サマリーテンプレート

```markdown
# テスト結果サマリー

## 概要
| 項目 | 値 |
|------|-----|
| 総テストケース数 | {total} |
| 実行済み | {executed} |
| 成功 | {passed} |
| 失敗 | {failed} |
| スキップ | {skipped} |
| 成功率 | {rate}% |

## 失敗テスト一覧
| TC-ID | テスト名 | 失敗理由 | 重要度 | 対応状況 |
|-------|---------|---------|--------|---------|

## 品質判定
- [ ] 合否判定基準を満たしている
- [ ] 重大バグが0件である
- [ ] テストカバレッジが80%以上
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| input | Yes | - | ユースケース記述ファイルのパス |
| type | No | all | テスト種別（unit/integration/e2e/all） |
| output_dir | No | output/pm/ | 出力ディレクトリ |
| format | No | markdown | 出力形式（markdown/playwright） |

## Output Format

- テスト計画書 → `output/pm/test-plan.md`
- テストケース → `output/pm/test-cases.md`
- E2Eテストコード → `output/pm/e2e-tests/*.spec.ts`
- テストエビデンス → `output/pm/unit-test-evidence/`, `output/pm/integration-test-evidence/`
- テスト結果サマリー → `output/pm/test-summary.md`

## Example

```
test-plannerスキルを使って、usecases.mdからテスト計画書とテストケースを生成してください。
→ output/pm/test-plan.md, output/pm/test-cases.md が生成される
```

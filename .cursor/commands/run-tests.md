---
description: "プロジェクトのテストを実行"
---

# テスト実行

プロジェクトのテストを実行するコマンドです。

## Python テスト

### 全テスト実行
```bash
pytest tests/ -v
```

### カバレッジ付きテスト
```bash
pytest tests/ -v --cov=src/ --cov-report=term-missing
```

### 特定のテストファイル実行
```bash
pytest tests/test_specific.py -v
```

## JavaScript テスト（Node.js）

### npm テスト
```bash
npm test
```

### 特定のテストファイル
```bash
npx jest tests/specific.test.js
```

## テスト結果の解釈

- ✅ PASSED: テスト成功
- ❌ FAILED: テスト失敗（エラー内容を確認）
- ⚠️ SKIPPED: スキップされたテスト
- 📊 Coverage: カバレッジ率（目標: 80%以上）

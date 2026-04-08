# ヒント: GitHub Actions

## YAML 基本構文

### インデント
```yaml
# 常に半角スペース2つ
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Step name
        run: echo "hello"
```

### 複数行コマンド
```yaml
- name: Multiple commands
  run: |
    echo "Line 1"
    echo "Line 2"
    npm install
```

### 環境変数
```yaml
# ワークフローレベル
env:
  NODE_ENV: production

# ジョブレベル
jobs:
  build:
    env:
      CI: true

# ステップレベル
steps:
  - run: echo $MY_VAR
    env:
      MY_VAR: hello
```

## よく使うアクション

### チェックアウト
```yaml
- uses: actions/checkout@v4
```

### Node.js セットアップ
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

### Python セットアップ
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
```

### アーティファクトのアップロード/ダウンロード
```yaml
# アップロード
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/

# ダウンロード
- uses: actions/download-artifact@v4
  with:
    name: build-output
```

## cron 式の書き方

```
┌───────── 分 (0-59)
│ ┌───────── 時 (0-23, UTC)
│ │ ┌───────── 日 (1-31)
│ │ │ ┌───────── 月 (1-12)
│ │ │ │ ┌───────── 曜日 (0-6, 0=日曜)
│ │ │ │ │
* * * * *
```

### よく使うパターン
| cron 式 | 説明 |
|---------|------|
| `0 0 * * *` | 毎日 UTC 0:00（JST 9:00） |
| `0 1 * * 1-5` | 平日 UTC 1:00（JST 10:00） |
| `30 23 * * *` | 毎日 UTC 23:30（JST 翌8:30） |
| `0 */6 * * *` | 6時間ごと |
| `0 0 * * 0` | 毎週日曜 UTC 0:00 |

**注意**: GitHub Actions の cron は UTC 基準です。JST = UTC + 9 時間。

## ジョブの依存関係

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]

  build:
    needs: test  # test 完了後に実行
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    needs: [test, build]  # 両方完了後に実行
    runs-on: ubuntu-latest
    steps: [...]
```

## 条件分岐

```yaml
# ブランチ限定
deploy:
  if: github.ref == 'refs/heads/main'

# PRイベントのみ
review:
  if: github.event_name == 'pull_request'

# 前のジョブが成功した場合のみ
notify:
  if: success()

# 前のジョブが失敗した場合のみ
alert:
  if: failure()
```

## Secrets の使い方

### 設定方法
1. リポジトリの Settings → Secrets and variables → Actions
2. 「New repository secret」をクリック
3. Name と Value を入力して保存

### 参照方法
```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: ./deploy.sh
```

## ローカルテスト（act）

```bash
# インストール
brew install act

# ワークフロー一覧
act -l

# push イベントをシミュレート
act push

# 特定のジョブのみ実行
act -j test

# 環境変数を指定
act --env-file .env
```

## トラブルシューティング

| 問題 | 原因 | 対処 |
|------|------|------|
| ワークフローが実行されない | YAML構文エラー | `yamllint` で検証 |
| `Permission denied` | GITHUB_TOKEN 権限不足 | permissions を追加 |
| cron が実行されない | UTC/JST の変換ミス | UTC で指定しているか確認 |
| キャッシュが効かない | キーのミスマッチ | hashFiles のパスを確認 |
| ジョブがスキップされる | if 条件が false | `${{ toJSON(github) }}` で値を確認 |

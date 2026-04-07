# module11-github-actions 完成例

## 概要

GitHub Actions を使った3種類のワークフローの完成例です。CI/CD、定期実行、PR自動レビューという実務でよく使うパターンをカバーしています。

## 成果物一覧

| ファイル | 説明 |
|----------|------|
| `output/workflows/ci.yml` | CI/CD パイプライン（テスト→ビルド→デプロイ） |
| `output/workflows/scheduled-sync.yml` | 毎日 JST 9:00 のデータ同期 |
| `output/workflows/pr-review.yml` | PR 自動ラベル付与・テンプレートチェック・サイズ警告 |

## 各ワークフローの詳細

### ci.yml
- **トリガー**: push(main/develop), pull_request(main)
- **test ジョブ**: Node.js 18/20 マトリックスでテスト実行
- **build ジョブ**: test 成功後にビルド、アーティファクトアップロード
- **deploy ジョブ**: main push 時のみ、production 環境にデプロイ

### scheduled-sync.yml
- **トリガー**: cron(UTC 0:00 = JST 9:00), workflow_dispatch
- **手動トリガー**: 同期対象（all/slack/google）を選択可能
- **自動コミット**: 変更がある場合のみコミット＆プッシュ
- **Slack 通知**: 成功/失敗に応じた通知

### pr-review.yml
- **ラベル自動付与**: ファイルパスに基づく（docs, frontend, backend, test, ci/cd）
- **テンプレートチェック**: 概要・テスト計画セクションの有無を確認
- **サイズチェック**: 500行超の場合に警告コメントと large-pr ラベル付与

## 使用ツール

- GitHub Actions（YAML ワークフロー定義）
- GitHub CLI（`gh`）

## 学習ポイント

1. **マトリックスビルド**: 複数バージョンでの並列テスト
2. **ジョブ依存関係**: `needs` による実行順序制御
3. **条件分岐**: `if` による環境・イベント判定
4. **cron スケジュール**: UTC/JST 変換の注意点
5. **GitHub CLI (gh)**: ワークフロー内での PR 操作
6. **Secrets 管理**: 機密情報の安全な取り扱い

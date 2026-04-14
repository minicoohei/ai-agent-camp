---
name: gas-clasp-ops
description: "Google Apps Script (GAS) プロジェクトを clasp 経由で操作するスキル。 「GASをデプロイして」「claspでpush」「GAS関数をテスト」等のリクエストで発動。 push / deploy / run を一括または個別に実行。複数プロジェクト管理に対応。"
triggers:
  - gas-clasp-ops
  - GASデプロイ
  - clasp push
  - Apps Script
  - GASテスト
  - スクリプト反映
  - clasp
---

# GAS clasp 操作スキル

Google Apps Script プロジェクトを clasp CLI で一括操作するためのスキル。

## 前提条件

```bash
# clasp は npx 経由で実行（インストール不要）
# Google アカウントでログイン（初回のみ）
npx -y @google/clasp login
```

## クイックスタート

```bash
# 全プロジェクトを push
python skills/gas-clasp-ops/scripts/clasp_ops.py push

# 特定プロジェクトを push → deploy
python skills/gas-clasp-ops/scripts/clasp_ops.py push deploy --project work/10.X-Calendar-GAS

# 関数を実行（テスト）
python skills/gas-clasp-ops/scripts/clasp_ops.py run --project work/10.X-Calendar-GAS --function myFunction

# dry-run で確認
python skills/gas-clasp-ops/scripts/clasp_ops.py push --dry-run
```

## コマンド

| コマンド | 説明 |
|---------|------|
| `push` | ローカルコードを GAS に反映 |
| `deploy` | 新しいバージョンをデプロイ |
| `run` | 指定した関数を実行（`--function` 必須） |
| `status` | デプロイ一覧を表示 |
| `open` | GAS エディタをブラウザで開く |

## オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--project PATH` | 対象プロジェクト（複数指定可） | 全プロジェクト |
| `--function NAME` | 実行する関数名（run 時必須） | - |
| `--dry-run` | 実行せず確認のみ | false |
| `--base-dir PATH` | 検索ベースディレクトリ | ワークスペースルート |

## 検出対象

`.clasp.json` を含むディレクトリを自動検出:

- `work/10.X-Calendar-GAS/`
- `work/03.AiTutor/session_workshop/03.gas/samples/clasp-slides-generator/`
- `work/03.AiTutor/session_workshop/03.gas/samples/clasp-weather-recorder/`

## 実行例

### プロジェクト一覧を確認

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py --list
```

出力例:
```
📂 検出されたプロジェクト (3 件):
  - work/03.AiTutor/.../clasp-slides-generator (scriptId: 1uIfFp1vuV...)
  - work/03.AiTutor/.../clasp-weather-recorder (scriptId: 1O6SBnHgY-...)
  - work/10.X-Calendar-GAS (scriptId: 1qLnnrFfzX...)
```

### 全プロジェクトを push → deploy

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py push deploy
```

### 特定プロジェクトで関数実行（テスト）

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py run \
  --project work/10.X-Calendar-GAS \
  --function processUnreadTweets
```

## トラブルシューティング

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `Not logged in` | clasp 未ログイン | `npx -y @google/clasp login` を実行 |
| `Script API disabled` | GAS API 無効 | [GAS API](https://script.google.com/home/usersettings) で有効化 |
| `Permission denied` | OAuth スコープ不足 | `appsscript.json` に必要なスコープを追加 |
| `Function not found` | 関数名が不正 | GAS エディタで関数名を確認 |

## 注意事項

- `clasp run` は GAS API を有効化し、OAuth スコープの設定が必要
- デプロイ前に必ず `push` でコードを反映すること
- エラー発生時は対象ごとにログを出力し、処理は継続
- タイムアウトは 120 秒に設定（長時間処理は GAS エディタから実行推奨）

## Overview

Google Apps Script (GAS) プロジェクトを clasp CLI 経由で一括操作するスキルです。`.clasp.json` を持つプロジェクトを自動検出し、push・deploy・run を効率的に実行します。

## Success Criteria

- [ ] 対象プロジェクトへの push/deploy がエラーなく完了している
- [ ] `--function` 指定時に関数が正常に実行されている
- [ ] 複数プロジェクト一括操作時に全プロジェクトの結果がログ出力されている

## Usage

上記「クイックスタート」セクションを参照。基本例:

```bash
# 全プロジェクトを push
python skills/gas-clasp-ops/scripts/clasp_ops.py push

# 特定プロジェクトで関数実行
python skills/gas-clasp-ops/scripts/clasp_ops.py run --project work/10.X-Calendar-GAS --function myFunction
```

## Troubleshooting

上記「トラブルシューティング」セクションを参照。

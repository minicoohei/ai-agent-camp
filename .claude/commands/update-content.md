---
description: 教材コンテンツを最新版に安全に更新する（ユーザーファイルは保持）
---

# 教材コンテンツの更新

upstream リポジトリから最新の教材を取得し、コンテンツファイルのみを更新します。
ユーザーファイル（.env, output/, work/ 等）には一切触れません。

## 実行手順

### 1. 更新可能な差分を確認（ドライラン）
```bash
uv run python tools/content_updater.py --dry-run
```

### 2. 更新を実行（スキルコンフリクト検出付き）
```bash
uv run python tools/content_updater.py
```

スキルをカスタマイズしている場合、upstream との差分が検出されると選択肢が表示されます:
- `keep_mine` — 自分のバージョンを維持
- `take_upstream` — upstream を採用（自分のをバックアップ）
- `keep_both` — 両方保持（自分のを -custom にリネーム）

コンフリクト検出を無効化する場合:
```bash
uv run python tools/content_updater.py --no-skill-check
```

### 3. 問題があった場合のロールバック
```bash
uv run python tools/content_updater.py --rollback
```

## 初回セットアップ（upstream 未設定の場合）

`gh auth login` で GitHub 認証済みであることが前提です。
コンテンツリポジトリへのコラボレーター招待を受諾後に実行してください。

```bash
uv run python tools/content_updater.py --setup
```

## 注意事項

- **前提**: `gh auth login` 済み + コラボレーター招待受諾済み
- **更新対象**: course/, skills/, tools/, commands/ 等のコンテンツファイル
- **保護対象**: .env, output/, work/, .setup-progress.json 等のユーザーファイル
- **バックアップ**: course/exercises/ 内の変更は自動バックアップされます（work/.backup/）
- **依存関係**: requirements.txt が更新された場合、pip install が自動実行されます

## アクセス権限管理（講師向け）

受講者のアクセス権限は `access-control/users.yaml` で管理します。

```bash
# ユーザー追加（3ヶ月有効）
python access-control/manage_access.py add github-username --months 3

# ユーザー削除
python access-control/manage_access.py remove github-username

# 状態確認
python access-control/manage_access.py list

# 期限切れチェック
python access-control/manage_access.py check
```

GitHub Actions が日次で期限切れを自動チェック・削除します。

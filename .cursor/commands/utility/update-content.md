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

### 2. 更新を実行
```bash
uv run python tools/content_updater.py
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

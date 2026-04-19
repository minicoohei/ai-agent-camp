---
description: "開発環境の状態をチェック"
---

# 環境チェック

開発環境の状態を確認するコマンドです。

## チェック項目

以下のコマンドを実行して環境を確認してください：

### 1. Node.js バージョン確認
```bash
node --version
```
期待値: v18.x 以上

### 2. Python バージョン確認
```bash
python3 --version    # Windowsでは python --version
```
期待値: Python 3.9 以上

### 3. Git 設定確認
```bash
git config user.name
git config user.email
```

### 4. npm パッケージ確認
```bash
npm list -g --depth=0
```

### 5. uv パッケージ確認
```bash
uv pip list | head -20
```

## トラブルシューティング
問題がある場合は `/start-0-1` でセットアップを確認してください。

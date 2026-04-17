# トラブルシューティング: 環境セットアップ

## 1. `command not found: node`

**原因**: Node.js が PATH に含まれていない

**対処（macOS）**:
```bash
# Homebrew で再インストール
brew install node

# パスを確認
which node
echo $PATH
```

**対処（WSL/Ubuntu）**:
```bash
# nvm で再インストール
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install --lts
```

---

## 2. `command not found: python3`

**原因**: Python が未インストールまたは PATH 未設定

**対処（macOS）**:
```bash
brew install python
```

**対処（WSL/Ubuntu）**:
```bash
sudo apt install -y python3 python3-pip python3-venv
```

---

## 3. `uv add` で Permission denied

**原因**: システム Python に書き込み権限がない

**対処**:
```bash
# ユーザーインストール
uv add --user <package>

# または仮想環境を使用
# uv で依存関係をインストール
uv add <package>
```

---

## 4. `git clone` で認証エラー

**原因**: GitHub の認証情報が設定されていない

**対処**:
```bash
# SSH キーを生成（未作成の場合）
ssh-keygen -t ed25519 -C "your.email@example.com"

# 公開鍵を表示してGitHubに登録
cat ~/.ssh/id_ed25519.pub

# または HTTPS + Personal Access Token を使用
git clone https://<token>@github.com/owner/repo.git
```

---

## 5. `claude` / `codex` コマンドが動かない

**原因**: 使っている CLI が正しくインストールされていない

**対処**:
```bash
# Claude Code
npm install -g @anthropic-ai/claude-code

# Codex
npm install -g @openai/codex

# パス確認
which claude
which codex
```

---

## 6. Cursor が起動しない / 拡張機能が読み込めない

**原因**: キャッシュの破損

**対処**:
```bash
# macOS: キャッシュクリア
rm -rf ~/Library/Application\ Support/Cursor/Cache
rm -rf ~/Library/Application\ Support/Cursor/CachedData

# Windows (Cursor は Windows ネイティブ側で動作): %APPDATA%\Cursor\Cache を削除
#   エクスプローラーで %APPDATA%\Cursor を開き、Cache / CachedData フォルダを削除する
```

> WSL2 側の Cursor Server（`~/.cursor-server/`）が原因と思われる場合は、WSL ターミナル内で `rm -rf ~/.cursor-server/data/CachedData` を試してください。

---

## 7. `brew install` が遅い / エラーになる

**原因**: Homebrew の更新が必要

**対処**:
```bash
brew update
brew doctor
brew install <package>
```

---

## 8. FFmpeg のインストールエラー（WSL/Ubuntu）

**原因**: パッケージが未インストール

**対処**:
```bash
sudo apt update && sudo apt install -y ffmpeg
ffmpeg -version
```

---

## 9. `npm install` で EACCES エラー

**原因**: npm グローバルディレクトリの権限問題

**対処**:
```bash
# npm のグローバルディレクトリを変更
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# PATH に追加（.bashrc or .zshrc）
export PATH=~/.npm-global/bin:$PATH
source ~/.zshrc
```

---

## 10. SSL/TLS 証明書エラー

**原因**: 企業プロキシやセキュリティソフトの干渉

**対処**:
```bash
# Git の SSL 検証を一時無効化（テスト用のみ）
git config --global http.sslVerify false

# npm のレジストリを HTTP に変更（テスト用のみ）
npm config set registry http://registry.npmjs.org/

# 根本対処: プロキシ設定
git config --global http.proxy http://proxy:port
npm config set proxy http://proxy:port
```

**注意**: SSL 検証の無効化はセキュリティリスクがあるため、問題解決後は元に戻してください。

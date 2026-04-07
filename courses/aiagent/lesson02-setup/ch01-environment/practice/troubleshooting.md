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

**対処（Windows）**:
- Node.js インストーラーを再実行し、「Add to PATH」にチェック
- ターミナルを再起動

---

## 2. `command not found: python3`

**原因**: Python が未インストールまたは PATH 未設定

**対処（macOS）**:
```bash
brew install python
```

**対処（Windows）**:
- Python インストーラーで「Add Python to PATH」にチェックして再インストール
- `python` コマンド（`python3` ではなく）で試す

---

## 3. `pip install` で Permission denied

**原因**: システム Python に書き込み権限がない

**対処**:
```bash
# ユーザーインストール
pip3 install --user <package>

# または仮想環境を使用
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
pip install <package>
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

# Windows: %APPDATA%\Cursor\Cache を削除
```

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

## 8. FFmpeg のインストールエラー（Windows）

**原因**: PATH の設定が正しくない

**対処**:
1. FFmpeg を C:\ffmpeg に展開
2. 「システム環境変数」→「Path」に `C:\ffmpeg\bin` を追加
3. ターミナルを再起動
4. `ffmpeg -version` で確認

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

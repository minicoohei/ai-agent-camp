# 環境セットアップ チェックリスト

以下の各項目を確認し、全てにチェックが入れば環境構築完了です。

## 基本ツール

- [ ] **Git**: `git --version` → バージョンが表示される
  ```bash
  git --version
  # 期待: git version 2.x.x
  ```

- [ ] **Node.js**: `node --version` → v18 以上
  ```bash
  node --version
  # 期待: v18.x.x 以上
  ```

- [ ] **npm**: `npm --version` → バージョンが表示される
  ```bash
  npm --version
  # 期待: 9.x.x 以上
  ```

- [ ] **Python**: `python3 --version` → 3.8 以上
  ```bash
  python3 --version
  # 期待: Python 3.8.x 以上
  ```

- [ ] **pip**: `pip3 --version` → バージョンが表示される
  ```bash
  pip3 --version
  # 期待: pip 2x.x.x
  ```

## エディタ

- [ ] **Cursor**: アプリケーションが起動する
  ```bash
  cursor --version  # CLI が使える場合
  ```

- [ ] **Claude Code**: `claude --version` → バージョンが表示される
  ```bash
  claude --version
  ```

- [ ] **Codex**: `codex --version` → バージョンが表示される
  ```bash
  codex --version
  ```

## Git 設定

- [ ] **ユーザー名**: `git config --global user.name` → 名前が表示される
  ```bash
  git config --global user.name
  ```

- [ ] **メールアドレス**: `git config --global user.email` → メールが表示される
  ```bash
  git config --global user.email
  ```

## オプションツール

- [ ] **FFmpeg**: `ffmpeg -version` → バージョンが表示される
  ```bash
  ffmpeg -version
  # 動画処理をしない場合はスキップ可
  ```

- [ ] **clasp**: `clasp --version` → バージョンが表示される
  ```bash
  npx @google/clasp --version
  # GAS を使わない場合はスキップ可
  ```

## リポジトリ

- [ ] **クローン完了**: `ls aiagent-base/` → ファイル一覧が表示される

- [ ] **Python 依存関係**: `pip list | grep Pillow` → Pillow が表示される
  ```bash
  pip3 install -r requirements.txt
  pip3 list | grep Pillow
  ```

- [ ] **Node.js 依存関係**: `ls node_modules/` → ディレクトリが存在する
  ```bash
  npm install
  ls node_modules/
  ```

## 確認スクリプト

全項目を一括チェックする場合:
```bash
# Cursor: /check-setup
# Codex: aiagent-check-setup skill
```

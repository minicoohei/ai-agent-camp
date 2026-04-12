---
description: 元リポジトリ（upstream）から最新の教材を取り込む
---

# 教材を最新版に更新

## 使い方
```
/update-material
```

## 概要
Import repository または clone + push で作成した自分用リポジトリ（例: 自分の GitHub の ai-agent-camp）に、大元のリポジトリ（aibrainpartners/ai-agent-camp）の最新の教材変更を取り込みます。

## 実行手順

以下の順で実行してください。

### 1. upstream の有無を確認
```bash
git remote -v
```
`upstream` が表示されていなければ、次のステップで追加します。

### 2. upstream が未設定の場合のみ追加
```bash
git remote add upstream https://github.com/aibrainpartners/ai-agent-camp.git
```
既に `upstream` がある場合はこのステップは不要です。

### 3. 最新を取得
```bash
git fetch upstream
```

### 4. 現在のブランチにマージ
```bash
# 現在のブランチを確認（多くの場合は main）
git branch --show-current

# 元リポジトリの main を取り込む
git merge upstream/main
```
ブランチ名が `master` の場合は `git merge upstream/main` のまま（upstream 側は main を前提）で問題ありません。

## コンフリクトが発生した場合
自分で変更を加えているファイルが元リポジトリでも更新されていると、コンフリクトが発生することがあります。その場合は以下を案内してください。

- コンフリクト箇所をエディタで開き、`<<<<<<<` / `=======` / `>>>>>>>` を確認して手動で解決する
- 解決後: `git add <ファイル>` → `git commit` でマージを完了する
- 解決が難しい場合は、該当ファイルを退避してから `git checkout --theirs -- <パス>` で元リポジトリ版を採用する方法もある

## 注意事項
- **対象**: 自分用にコピーしたリポジトリ（Import / clone+push）向けです。Fork している場合も同様に利用できます。
- **安全**: `git push --force` は実行しません。merge のみ行い、必要に応じてユーザーが自分で `git push origin main` などでプッシュしてください。

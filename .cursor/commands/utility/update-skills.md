---
description: upstream からスキルの最新版を取り込む
category: utility
---

# スキルを最新版に更新

## 使い方
```text
/update-skills
```

## 概要
元リポジトリ（TokenPocket/ai-agent-camp）から最新のスキル更新を取り込みます。
内部的には `git fetch upstream` + `git merge upstream/main` を実行します。
`/update-material` と同様の仕組みですが、スキル更新に特化した案内を行います。

## 実行手順

以下のコマンドを実行してください。

```bash
uv run python tools/skill_manager.py update-upstream
```

スクリプトが以下を自動的に行います:

1. `upstream` リモートの有無を確認（未設定なら追加）
2. `git fetch upstream` で最新を取得
3. `git merge upstream/main` で現在のブランチにマージ

## コンフリクトが発生した場合
自分で変更を加えているスキルが元リポジトリでも更新されていると、コンフリクトが発生することがあります。その場合:

- コンフリクト箇所をエディタで開き、`<<<<<<<` / `=======` / `>>>>>>>` を確認して手動で解決する
- 解決後: `git add <ファイル>` → `git commit` でマージを完了する

## 更新後の確認

```bash
# 現在のスキル一覧を確認
uv run python tools/skill_manager.py list
```

## 注意事項
- **対象**: 自分用にコピーしたリポジトリ（Import / clone+push）向けです
- **安全**: `git push --force` は実行しません。merge のみ行います
- 必要に応じて `git push origin main` でリモートに反映してください

# Google Workspace（gog）用 OAuth クライアント

## 受講者向け（最短）

**推奨:** 教材どおり、エディタのチャットで **`/module-18-gcp-quick`** を実行してください。エージェントが gog の確認と OAuth の手順を進めます。ターミナルに手入力する必要はありません。

1. リポジトリのルートで `credentials/google-workspace-desktop-oauth.json` に、**運営が配布したデスクトップアプリ用 OAuth クライアント JSON** を置く（またはこのファイルの `REPLACE_*` を実値に差し替える）。
2. 上記のスラッシュコマンドをチャットで実行し、エージェントの案内に従う。
3. **トークンや `.env.local` の秘密は Git にコミットしない。**

### 補足（自分で切り分けたい場合のみ）

エージェントを使わず状況だけ確認したいときは、リポジトリルートで次を実行できます。

```bash
command -v gog || echo "gog: not found in PATH"
gog --version
gog auth --help
gog auth list
```

- `gog` が見つからない → 教材 **Module 15-1** などで gogcli（gog）をインストールしてから続行。
- 手動で OAuth を進める場合は、上記確認のあと `gog auth credentials set credentials/google-workspace-desktop-oauth.json` と `gog auth add <あなたのGoogleメール>` を実行し、同意後に `gog auth list` で登録を確認。

## 運営向け（メンテナンス）

- Google Cloud Console で **デスクトップアプリ** の OAuth クライアントを作成し、ダウンロードした JSON をこのパスに配置する（または受講者が上書きできるよう配布チャネルを別に用意）。
- Gmail / Drive 等のスコープを使う場合、**OAuth 同意画面の公開ステータスと Google の検証要件**に従う。テストユーザーのみの運用と本番公開では手続きが異なる。
- 利用が増えたら **API クォータ**をコンソールで監視する。デスクトップ型クライアント ID の濫用はクォータを消費しうる。

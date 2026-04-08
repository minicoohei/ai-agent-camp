---
description: "When the user says /start-13-5 — Module 13 Lesson 13-5: LP制作 - Vercelデプロイ"
prerequisites: ["start-13-4"]
duration: "約15分"
level: "intermediate"
tags: ["lp", "vercel", "deploy", "hosting"]
---

# 🎓 Lesson 13-5: Vercelデプロイ

## 📍 このセッションでやること

**Lesson 13-5: Vercelデプロイ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 作成したLP/HPをVercelにデプロイし、公開URLを取得する |
| 所要時間 | 約15分 |
| 使うスキル | lp-designer, Vercel CLI |
| 前提条件 | Lesson 13-4 完了（`output/lp-project/` が存在すること）。未完了の場合はフォールバックでサンプルプロジェクトを生成します |
| 教材ページ | [Module 13: LP/HP制作](https://ai-agent.camp/ja/course/module-13) を並行参照 |

> **⚠️ 非対話環境（Codex, CI等）での注意**: `vercel login` はブラウザ認証が必要なため、非対話環境では実行できません。その場合は `VERCEL_TOKEN` 環境変数によるトークン認証を使用するか、デプロイステップをスキップしてください。

**このセッションの流れ:**
1. プロジェクト存在チェック（なければサンプル生成）
2. Vercel CLI のインストール・認証
3. プレビューデプロイ
4. ブラウザで確認
5. 本番デプロイ

セッション終了時には、LPが世界中からアクセス可能なURLで公開されています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 0へ)
(check_prereq → Node.js, npm の存在確認 + Lesson 13-4 完了確認)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🔍 Step 0: プロジェクト存在チェック

13-4 の成果物（`output/lp-project/`）が存在するか確認します。

**確認手順:**
```bash
# output/lp-project ディレクトリの存在チェック
ls output/lp-project/index.html 2>/dev/null && echo "OK: プロジェクトが存在します" || echo "NOT FOUND: プロジェクトが見つかりません"
```

**プロジェクトが存在しない場合のフォールバック:**

`output/lp-project/` が存在しない場合は、13-4 を先に実施するか、以下の最小限サンプルプロジェクトで代替できます。

```bash
# サンプルプロジェクトを生成
mkdir -p output/lp-project
cat > output/lp-project/index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>サンプルLP - Vercelデプロイ練習用</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <header class="bg-blue-600 text-white py-16 text-center">
    <h1 class="text-4xl font-bold mb-4">サンプルLP</h1>
    <p class="text-xl">Vercelデプロイの練習用ページです</p>
  </header>
  <main class="max-w-3xl mx-auto py-12 px-4">
    <section class="bg-white rounded-lg shadow p-8 mb-8">
      <h2 class="text-2xl font-bold mb-4">このページについて</h2>
      <p class="text-gray-700">13-5 のVercelデプロイ練習用に自動生成されたサンプルページです。13-4 を完了すると、実際に作成したLPをデプロイできます。</p>
    </section>
  </main>
  <footer class="bg-gray-800 text-gray-400 py-6 text-center">
    <p>&copy; 2026 AIエージェント研修</p>
  </footer>
</body>
</html>
HTMLEOF
echo "サンプルプロジェクトを output/lp-project/ に生成しました"
```

> **推奨**: 本来は 13-4 (`/start-13-4`) で作成したLPを使うのがベストです。サンプルはデプロイ手順の練習用です。

**期待される結果**: `output/lp-project/index.html` が存在する状態になります。

---

## 🚀 Step 1: Vercel CLI インストール・認証

Vercel CLI をインストールしてログインします。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Vercel CLI セットアップ",
  "questions": [{
    "id": "vercel_status",
    "prompt": "Vercel CLI の状態は？",
    "options": [
      {"id": "not_installed", "label": "まだインストールしていない"},
      {"id": "installed", "label": "インストール済み（ログインも済み）"},
      {"id": "installed_no_login", "label": "インストール済み（未ログイン）"},
      {"id": "no_account", "label": "Vercelアカウントを持っていない"}
    ]
  }]
}
```

**選択後の案内（not_installed の場合）**:
入力内容:
```text
Vercel CLI をインストールしてログインしてください。

手順:
1. インストール
   npm i -g vercel

2. バージョン確認
   vercel --version

3. ログイン（方法A: ブラウザ認証 ※対話環境のみ）
   vercel login

   ブラウザが開くので、Vercelアカウントでログインしてください。
   アカウントがなければ https://vercel.com/signup で無料作成できます。

4. ログイン確認
   vercel whoami
```

**選択後の案内（installed_no_login の場合）**:

> **⚠️ 非対話環境（Codex, CI, SSH等）の場合**: `vercel login` はブラウザが必要なため実行できません。以下の「方法B: トークン認証」を使ってください。

入力内容:
```text
■ 方法A: ブラウザ認証（ローカル環境）
  vercel login
  → ブラウザが開くので認証してください

■ 方法B: トークン認証（非対話環境・CI対応）
  1. https://vercel.com/account/tokens にアクセス
  2. 「Create Token」でトークンを発行（名前は任意、例: "aiagent-deploy"）
  3. 環境変数に設定:
     export VERCEL_TOKEN="発行されたトークン"

  4. .env に追記して永続化（任意）:
     テキストエディタで .env ファイルを直接開き、VERCEL_TOKEN=発行されたトークン を追記してください。

     > **セキュリティ注意**: `echo 'VERCEL_TOKEN=...' >> .env` のようにコマンドで追記すると、シェル履歴にトークンが残るリスクがあります。テキストエディタでの直接編集を推奨します。

  5. トークン認証でデプロイする場合は以下のように実行:
     vercel --token "$VERCEL_TOKEN"
     vercel --prod --token "$VERCEL_TOKEN"

■ ログイン確認:
  vercel whoami
  # トークン認証の場合: vercel whoami --token "$VERCEL_TOKEN"
```

**選択後の案内（no_account の場合）**:
```text
Vercelアカウントを作成してください:

1. https://vercel.com/signup にアクセス
2. GitHubアカウントまたはメールで登録（無料プラン）
3. 登録後、ターミナルで vercel login を実行
   （非対話環境の場合は https://vercel.com/account/tokens でトークンを発行）
```

**期待される結果**: Vercel CLI がインストール・認証されます。

---

## 🚀 Step 2: プレビューデプロイ

まずプレビュー環境にデプロイして確認します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: プレビューデプロイ",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
LP プロジェクトを Vercel にプレビューデプロイしてください。

■ 方法A: 対話形式（ローカル環境）
1. プロジェクトディレクトリに移動
   cd output/lp-project

2. Vercel デプロイ実行
   vercel

   対話形式で以下を設定:
   - Set up and deploy? → Y
   - Which scope? → 自分のアカウントを選択
   - Link to existing project? → N
   - Project name? → my-lp（任意の名前）
   - In which directory is your code located? → ./
   - Override settings? → N

3. デプロイ完了後、プレビューURLが表示されます
   例: https://my-lp-xxxxx.vercel.app

■ 方法B: 非対話モード（CI/Codex環境、またはトークン認証の場合）
1. プロジェクトディレクトリに移動
   cd output/lp-project

2. --yes フラグで対話をスキップしてデプロイ
   vercel --yes --token "$VERCEL_TOKEN"

   ※ VERCEL_TOKEN が未設定の場合はStep 1のトークン認証手順を参照

3. デプロイ完了後、プレビューURLが表示されます

表示されたプレビューURLを記録してください。
```

> **⚠️ `~/.vercel` が存在しないエラーが出る場合**: 初回デプロイ時に自動作成されます。エラーが続く場合は `mkdir -p ~/.vercel` を実行してください。

**期待される結果**: プレビューURLが取得されます。

---

## 🚀 Step 3: ブラウザで確認

プレビューURLをブラウザで確認します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: プレビュー確認",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
プレビューURLをブラウザで開いて確認してください。

確認項目:
1. ページが正しく表示されるか
2. 画像・フォントが読み込まれるか
3. レスポンシブが正しく動くか（ブラウザの幅を変えてみる）
4. アニメーションが動作するか
5. リンク・ボタンが機能するか

cursor-ide-browser MCPを使って確認:
browser_navigate でプレビューURLを開き、
browser_snapshot でスクリーンショットを取得してください。

問題があればコードを修正し、再度 vercel でデプロイできます。
```

**期待される結果**: プレビュー環境でLPが正しく表示されることを確認します。

---

## 🚀 Step 4: 本番デプロイ

問題なければ本番環境にデプロイします。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 本番デプロイ",
  "questions": [{
    "id": "deploy_action",
    "prompt": "本番デプロイしますか？",
    "options": [
      {"id": "deploy_prod", "label": "本番デプロイする"},
      {"id": "fix_first", "label": "まず修正してから本番デプロイ"},
      {"id": "skip_prod", "label": "プレビューのみで終了"},
      {"id": "custom_domain", "label": "カスタムドメインも設定したい"}
    ]
  }]
}
```

**選択後の案内（deploy_prod の場合）**:
入力内容:
```text
本番環境にデプロイしてください。

手順:
1. 本番デプロイ実行
   cd output/lp-project
   vercel --prod
   # トークン認証の場合: vercel --prod --token "$VERCEL_TOKEN"

2. 本番URLが表示されます
   例: https://my-lp.vercel.app

3. 本番URLでの最終確認
   - ページ表示速度
   - OGP画像（SNS共有時のプレビュー）
   - モバイル表示

本番URLを記録してください。
```

**選択後の案内（custom_domain の場合）**:

> **注意**: カスタムドメインの設定は任意です。独自ドメインを所有している場合のみ実施してください。Vercelの無料サブドメイン（*.vercel.app）でも公開は可能です。

入力内容:
```text
カスタムドメインを設定してください（独自ドメインを所有している場合のみ）。

手順:
1. ドメインの追加
   vercel domains add your-domain.com

2. DNS設定（ドメインプロバイダ側で設定）
   - タイプ: CNAME
   - 名前: @ または www
   - 値: cname.vercel-dns.com

3. SSL証明書（自動発行）
   Vercelが自動でLet's Encrypt証明書を発行します。

4. 設定確認
   vercel domains inspect your-domain.com
```

**期待される結果**: LPが本番URLで公開されます。

---

## ⚠️ よくあるトラブルと解決方法

AskUserQuestion（AskQuestion）でトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "vercel コマンドが見つからない"},
      {"id": "trouble_2", "label": "ログインできない"},
      {"id": "trouble_3", "label": "デプロイがエラーになる"},
      {"id": "trouble_4", "label": "ページが真っ白になる"}
    ]
  }]
}
```

### トラブル1: vercel コマンドが見つからない
**解決策**: `npm i -g vercel` でグローバルインストール。それでもダメなら `npx vercel` で実行。

### トラブル2: ログインできない
**解決策**: `vercel login --token <token>` でトークンベースのログインを試してください。トークンは https://vercel.com/account/tokens で発行できます。

### トラブル3: デプロイがエラーになる
**解決策**: エラーメッセージを確認してください。よくある原因:
- ファイルサイズ上限超過 → 画像を圧縮
- package.json の構文エラー → JSON形式を確認
- ビルドエラー → ローカルで動作するか再確認

### トラブル4: ページが真っ白になる
**解決策**: デプロイ先のルートディレクトリ設定を確認。`vercel` コマンド実行時に `In which directory is your code located?` で `./` を指定しているか確認。

---

## ✅ チェックポイント
- [ ] `output/lp-project/` にデプロイ対象のプロジェクトが存在する
- [ ] Vercel CLI がインストールされている
- [ ] Vercel にログイン済み（ブラウザ認証 or トークン認証）
- [ ] プレビューデプロイが成功している
- [ ] プレビューURLでLPが正しく表示される
- [ ] 本番デプロイが完了している（オプション）


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/lp/
├── index.html  (ランディングページ)
├── style.css
└── assets/
```

### 確認コマンド
```bash
# ファイル一覧
ls -lh output/lp/

# ブラウザで開く（macOS: open / Linux: xdg-open）
open output/lp/index.html
```

> 💡 HTMLの構造確認: `head -30 output/lp/index.html`

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```bash
vercel ls で現在のデプロイ一覧を表示し、
最新のデプロイのURL・状態・作成日時を確認してください。
# トークン認証の場合: vercel ls --token "$VERCEL_TOKEN"
```

**期待される結果**: デプロイの一覧とURLが表示されます。

---

## 🎉 おめでとうございます！

Module 13 のすべてのレッスンを完了しました！

### 習得したスキル
1. **訴求設計**: ペルソナ定義、ベネフィット整理、コピーライティング
2. **ワイヤーフレーム**: ASCII WF、ビジュアルWF、情報設計
3. **Pencilデザイン**: MCP を使ったプロ品質のデザイン作成
4. **フロントエンド実装**: HTML/CSS(Tailwind)/JS によるLP構築
5. **デプロイ**: Vercel を使った即座の公開

### 3段階の体験まとめ
- **Stage 1**: テキスト → HTML で直接LP作成（13-1, 13-2, 13-4）
- **Stage 2**: より複雑なHP構築（応用演習で実践）
- **Stage 3**: Pencil → コード変換（13-3 → 13-4）

---

## ➡️ 次のステップ

これで全セクション完了です。次にやることを選んでください。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-14-1）"},
      {"id": "course_top", "label": "コーストップを開く（ai-agent.camp）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-14-1
- course_top → ブラウザで https://ai-agent.camp/ja/course を開く
- finish → 終了

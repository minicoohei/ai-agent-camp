---
description: "When the user says /start-16-6 — Module 16 Lesson 16-6: Resend 登録 & ドメイン設定 - Vercel DNS 自動設定"
category: "lesson"
duration: "30分"
prerequisites: ["start-13-1"]
level: "beginner"
tags: ["email", "resend", "domain", "dns", "vercel", "spf", "dkim"]
---

# 🎓 Lesson 16-6: Resend 登録 & ドメイン設定

## 📍 このセッションでやること

**Lesson 16-6: Resend 登録 & ドメイン設定** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Resend アカウントを作成し、Vercel ドメインの DNS 設定（SPF, DKIM）を完了する |
| 所要時間 | 約30分 |
| 使うツール | Resend CLI (`resend-cli`), Vercel Dashboard |
| 前提条件 | Vercel でドメインが管理されていること |
| 教材ページ | [Module 16: メール自動化](https://ai-agent.camp/ja/course/module-16) を並行参照 |

**このセッションの流れ:**
1. Resend アカウント登録
2. Resend CLI のインストールと認証
3. ドメインの追加と Vercel DNS 自動設定
4. ドメイン検証の確認

セッション終了時には、Resend でメール送信できるドメインが設定されています。

> **💡 ヒント**: Vercel で LP やウェブサイトをデプロイ済みなら、そのドメインをそのまま Resend で使えます。

---

## 🎯 準備チェック

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
      {"id": "previous_lesson", "label": "13-3 をまずやりたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

---

## 🚀 Step 1: Resend アカウント登録

1. [resend.com](https://resend.com) にアクセスし、アカウントを作成
2. 組織情報（会社名、住所等）を入力
3. メール認証を完了

**完了したら次のステップへ進みましょう。**

---

## 🚀 Step 2: Resend CLI のインストールと認証

**Resend CLI をインストール:**

```bash
# npm でインストール
npm install -g resend-cli

# または Homebrew（Mac）
brew install resend/cli/resend
```

**インストール確認:**
```bash
resend --version
```

**認証（APIキーの設定）:**
Resend ダッシュボードで API Key を作成し、CLI に設定します。
（APIキーの詳細な作成手順は 13-5 で行います。まずはデフォルトキーを使用）

---

## 🚀 Step 3: ドメインの追加と Vercel DNS 自動設定

**Resend CLI でドメインを追加:**
```bash
resend domains create --name your-domain.com --region ap-northeast-1
```

**Vercel Dashboard で DNS 自動設定:**
1. Resend ダッシュボード → Domains → 追加したドメイン → Records タブ
2. 「Auto configure」ボタンをクリック
3. Vercel の DNS に MX, SPF, DKIM レコードが自動追加される

**CLI でドメイン一覧を確認:**
```bash
resend domains list
```

**AskQuestion:**
```json
{
  "title": "📋 ドメイン設定の確認",
  "questions": [{
    "id": "domain_status",
    "prompt": "ドメインの設定状況は？",
    "options": [
      {"id": "auto_done", "label": "Auto configure で設定完了 → 検証へ"},
      {"id": "manual", "label": "手動で DNS レコードを設定したい"},
      {"id": "no_vercel", "label": "Vercel 以外の DNS を使っている"},
      {"id": "error", "label": "エラーが出た → トラブルシューティング"}
    ]
  }]
}
```

---

## 🚀 Step 4: ドメイン検証

**CLI でドメイン検証を実行:**
```bash
resend domains verify --domain-id <domain-id>
```

**検証ステータスの確認:**
```bash
resend domains list
```

DNS レコードの反映には数分〜数時間かかる場合があります。ステータスが `verified` になれば完了です。

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestion:**
```json
{
  "title": "⚠️ トラブルはありましたか？",
  "questions": [{
    "id": "trouble",
    "prompt": "何か問題がありましたか？",
    "options": [
      {"id": "none", "label": "問題なし → チェックポイントへ"},
      {"id": "dns_pending", "label": "DNS 検証が完了しない"},
      {"id": "auto_config_fail", "label": "Auto configure が動かない"},
      {"id": "other", "label": "その他のエラー"}
    ]
  }]
}
```

| トラブル | 解決策 |
|---------|--------|
| DNS 検証が完了しない | DNS 反映に数時間かかる場合があります。`resend domains verify` で再チェック |
| Auto configure が動かない | Vercel でドメインが正しく設定されているか確認。手動で TXT/MX レコードを追加 |
| resend CLI が見つからない | `npm install -g resend-cli` で再インストール |

---

## ✅ チェックポイント

- [ ] Resend アカウントを作成した
- [ ] Resend CLI をインストールし、認証した
- [ ] ドメインを追加し、DNS レコード（SPF, DKIM）を設定した
- [ ] ドメイン検証が完了した（`verified` ステータス）


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/email/
├── index.html  (HTMLメール)
├── style.css
└── assets/
```

### 確認コマンド
```bash
# ファイル一覧
ls -lh output/email/

# ブラウザで開く（macOS: open / Linux: xdg-open）
open output/email/index.html
```

> 💡 HTMLの構造確認: `head -30 output/email/index.html`

---

## ✅ 完了チェック

```bash
uv run python tools/lesson_progress.py --check start-16-6
```

---

## ➡️ 次のステップ

**AskQuestion:**
```json
{
  "title": "🎉 Lesson 16-6 完了！",
  "questions": [{
    "id": "next_action",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_lesson", "label": "Lesson 16-7 へ → APIキー作成 & 初回送信"},
      {"id": "practice", "label": "DNS 設定をもう少し確認したい"},
      {"id": "review", "label": "Module 16 の概要を確認"},
      {"id": "end", "label": "今日はここまで"}
    ]
  }]
}
```

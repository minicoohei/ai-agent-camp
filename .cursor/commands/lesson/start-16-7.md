---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "25分"
prerequisites: ["start-16-6"]
level: "beginner"
tags: ["email", "resend", "api-key", "resend-cli", "send"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 16-7: APIキー作成 & 初回メール送信

## 📍 このセッションでやること

**Lesson 16-7: APIキー作成 & 初回メール送信** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Resend APIキーを作成し、CLI と SDK の両方でメールを送信する |
| 所要時間 | 約25分 |
| 使うツール | Resend CLI (`resend-cli`), Resend SDK (TypeScript) |
| 前提条件 | Lesson 16-6 完了（ドメイン検証済み）|
| 教材ページ | [Module 16: メール自動化](https://ai-agent.camp/ja/course/module-16) を並行参照 |

**このセッションの流れ:**
1. APIキーの作成とパーミッション設定
2. Resend CLI でメール送信
3. Resend SDK（TypeScript）で送信
4. .env でAPIキーを安全に管理

セッション終了時には、Resend 経由でメールが送信できるようになっています。

> **⚠️ 重要**: APIキーは一度しか表示されません。必ず .env に保存し、Git にコミットしないでください。

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
      {"id": "previous_lesson", "label": "13-4 をまずやりたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

---

## 🚀 Step 1: APIキーの作成

**Resend ダッシュボードで作成:**
1. Settings → API Keys → Create API Key
2. Name: 任意（例: `dev-key`）
3. Permission: `Full access`（開発用）または `Sending access`（本番用）
4. Domain: 検証済みドメインを選択

**パーミッションの違い:**
| パーミッション | できること | 推奨用途 |
|--------------|----------|---------|
| Full access | メール送信 + ドメイン管理 + Audience 管理 | 開発・テスト |
| Sending access | メール送信のみ | 本番環境（最小権限の原則）|

**APIキーを .env に保存:**
```bash
echo "RESEND_API_KEY=re_xxxxxxxx" >> .env
```

---

## 🚀 Step 2: Resend CLI でメール送信

**CLI でテスト送信:**
```bash
resend emails send \
  --from "noreply@your-domain.com" \
  --to "your-email@gmail.com" \
  --subject "Resend CLI テスト送信" \
  --html "<p>Resend CLI からのテスト送信です！</p>"
```

**送信結果の確認:**
```bash
resend emails list
```

**スケジュール送信（自然言語対応）:**
```bash
resend emails send \
  --from "noreply@your-domain.com" \
  --to "your-email@gmail.com" \
  --subject "スケジュール送信テスト" \
  --html "<p>1時間後に届くメールです</p>" \
  --scheduled-at "in 1 hour"
```

**AskQuestion:**
```json
{
  "title": "📋 CLI 送信の結果",
  "questions": [{
    "id": "cli_result",
    "prompt": "CLI でのメール送信は成功しましたか？",
    "options": [
      {"id": "success", "label": "送信成功 → SDK 送信に進む"},
      {"id": "auth_error", "label": "認証エラーが出た"},
      {"id": "domain_error", "label": "ドメインエラーが出た"},
      {"id": "other", "label": "その他のエラー"}
    ]
  }]
}
```

---

## 🚀 Step 3: Resend SDK で送信

**SDK のインストール:**
```bash
npm install resend
```

**TypeScript でメール送信:**
```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send({
  from: 'noreply@your-domain.com',
  to: 'your-email@gmail.com',
  subject: 'Resend SDK テスト送信',
  html: '<p>Resend SDK からのテスト送信です！</p>',
});

if (error) {
  console.error('送信エラー:', error);
} else {
  console.log('送信成功:', data);
}
```

---

## 🚀 Step 4: .env でAPIキーを安全に管理

**.gitignore に .env を追加:**
```bash
echo ".env" >> .gitignore
```

**確認:**
```bash
cat .gitignore | grep .env
```

---

## ⚠️ よくあるトラブルと解決方法

| トラブル | 解決策 |
|---------|--------|
| `API key is invalid` | APIキーが正しくコピーされているか確認。再作成が必要な場合もある |
| `Domain not verified` | 13-4 に戻り、ドメイン検証を完了する |
| `The from address is not verified` | from アドレスのドメインが検証済みか確認 |
| メールが届かない | 迷惑メールフォルダを確認。SPF/DKIM 設定を再チェック |

---

## ✅ チェックポイント

- [ ] APIキーを作成し、.env に保存した
- [ ] Resend CLI でテストメールを送信できた
- [ ] Resend SDK（TypeScript）でメールを送信できた
- [ ] .gitignore に .env が含まれている


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
uv run python tools/lesson_progress.py --check start-16-7
```

---

## ➡️ 次のステップ

**AskQuestion:**
```json
{
  "title": "🎉 Lesson 16-7 完了！",
  "questions": [{
    "id": "next_action",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_lesson", "label": "Lesson 16-8 へ → Resend Sequence でドリップキャンペーン"},
      {"id": "practice", "label": "もっとメール送信を試したい"},
      {"id": "review", "label": "Module 16 の概要を確認"},
      {"id": "end", "label": "今日はここまで"}
    ]
  }]
}
```

---
description: "Lesson command — line-harness-oss を Cloudflare 無料枠にデプロイ"
duration: "約75分"
prerequisites: ["LINE 公式アカウント / Developers アカウント", "Cloudflare アカウント", "Node 20+ / pnpm 9+"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "line", "mcp", "cloudflare", "module-23"]
---

# /setup-line-harness -- line-harness-oss + Cloudflare デプロイ

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | line-harness-oss を Cloudflare 無料枠（Workers + D1 + R2）に自前デプロイし、Claude Code から `line-harness` MCP 経由で全機能を操作可能にする |
| 所要時間 | 約 75 分（ブラウザ操作 15 分、CLI 30 分、待ち時間 30 分） |
| 前提 | LINE Messaging API + LINE Login の 2 チャネルが作成可能 / Cloudflare アカウント / Node 20+ |
| つながる先 | aiagent-course Module 23 のスライド内容と一致 |

> ⚠️ **非対話モードでは完走不可** (`nonInteractiveMode: incompatible`)。 LINE Developers Console / Cloudflare ダッシュボードでの**ブラウザ認証**が複数回必要なため、`claude -p` / `cursor-agent --print` で実行された場合は冒頭で停止し、対話モードへ誘導します。

---

## Step 0: 進捗確認 + 既存検出

**AI が裏で実行する内容:**

1. `<project>/.mcp.json` または `~/.claude/mcp_settings.json` に `line-harness` エントリがあるか
2. `wrangler --version` で wrangler CLI のインストール確認
3. `~/work/line-marketing` または同等のリポジトリディレクトリの存在
4. macOS Keychain に `LINE_HARNESS_API_KEY` があるか（値は表示しない）

すべて揃っているなら **Step 6（接続テスト）にスキップ**。

---

## Step 1: LINE Developers Console で 2 チャネル作成

ブラウザで <https://developers.line.biz/console/> を開く。

**Provider** を 1 つ作り、その中で:

1. **Messaging API チャネル** を作成 → `LINE_CHANNEL_SECRET` と `LINE_CHANNEL_ACCESS_TOKEN` を控える
2. **LINE Login チャネル** も作成（**必須**）→ `LINE_LOGIN_CHANNEL_ID` と `LINE_LOGIN_CHANNEL_SECRET` を控える

> ⚠️ **LINE Login チャネルが無いと UUID が取れず、マルチアカウント統合と流入元追跡が機能しません**。あとから作っても、それまでに登録された友だちは UUID 紐付けからやり直しになります。

---

## Step 2: リポジトリ取得

```bash
git clone https://github.com/Shudesu/line-harness-oss.git
cd line-harness-oss
pnpm install   # Node 20+ / pnpm 9+ が必要
```

---

## Step 3: Cloudflare D1 + Worker のプロビジョニング

```bash
npx wrangler login                     # 1 回目: ブラウザでログイン
npx wrangler d1 create line-crm        # 出てきた database_id を apps/worker/wrangler.toml に貼る
npx wrangler d1 execute line-crm \
  --file=packages/db/schema.sql        # 42 テーブルを一気に作成
```

---

## Step 4: 5 種のシークレット登録

```bash
npx wrangler secret put LINE_CHANNEL_SECRET
npx wrangler secret put LINE_CHANNEL_ACCESS_TOKEN
npx wrangler secret put LINE_LOGIN_CHANNEL_ID
npx wrangler secret put LINE_LOGIN_CHANNEL_SECRET
npx wrangler secret put API_KEY                  # 自分で決めたランダム値
```

---

## Step 5: デプロイと Webhook 接続

```bash
# 重要: pnpm run deploy を必ず使う（npx wrangler deploy だけでは Vite ビルドが走らない）
pnpm run deploy
```

LINE Developers Console → Messaging API → **Webhook URL** を以下に設定:

```
https://<your-worker>.workers.dev/webhook
```

「Verify」ボタンで 200 が返れば疎通完了。

---

## Step 6: line-harness MCP を Claude Code に追加

`.mcp.json`（プロジェクトローカルか `~/.claude/mcp_settings.json`）に:

```jsonc
{
  "mcpServers": {
    "line-harness": {
      "type": "http",
      "url": "https://<your-worker>.workers.dev",
      "env": {
        "LINE_HARNESS_API_KEY": "***"  // wrangler secret put で入れた値
      }
    }
  }
}
```

`.gitignore` に `.mcp.json` を必ず追加。

Claude Code を再起動して `/mcp` を実行 → `line-harness (http): ... ✓ connected` が出れば OK。

---

## Step 7: 主要 8 ツールの確認

| ツール | 用途 |
|---|---|
| `manage_auto_replies` | キーワード自動応答 |
| `manage_scenarios` | ステップ配信シナリオ |
| `manage_broadcasts` | ブロードキャスト送信 |
| `manage_rich_menus` | リッチメニュー管理 |
| `manage_tags` | タグ |
| `manage_friends` | 友だちリスト |
| `upload_image` | R2 経由で公開 URL 取得 |
| `account_summary` | サマリ・perAccount 別友だち数 |

---

## つまずきポイント（aiagent-course Module 23 と同じ）

| 症状 | 原因 | 対処 |
|---|---|---|
| 既存フォロワーのメッセージが silent drop | LINE API は follow event 以外で取れない | webhook で `getOrCreateFriendFromMessage` ヘルパー |
| `wrangler deploy` でコード変更が反映されない | Vite ビルドが走らない | 必ず `pnpm run deploy` |
| Cloudflare WAF (1010) で画像アップロード拒否 | Mozilla 系 UA でない | `requests` に Mozilla UA を付ける |
| UUID が取れない | LINE Login チャネル未作成 | 2 チャネルを最初から作る |
| Flex carousel の `size: giga` が効かない | carousel の bubble は mega まで | mega を使う |
| `account_summary` の合計が合わない | per-account 重複含む | `perAccount` 配列を見る |
| API Key が git に上がる | `.mcp.json` がデフォで gitignore されない | `.gitignore` に追加 |
| Pillow で絵文字 □ になる | Unicode 絵文字未対応 | ★ ✦ ◆ で代用 |
| 自動応答 keyword が競合 | matchType=contains の部分一致 | 既存 id を update |
| ボタン label が切れる | LINE は label ≤ 20 文字 | 短くして body に移す |

---

## 非対話モード（claude -p / cursor-agent --print）での挙動

このコマンドは `nonInteractiveMode: incompatible` です。-p 実行時の AI への指示:

冒頭で次のメッセージだけ出力して即座に exit する:

> このコマンドは Cloudflare ログイン (`wrangler login`) と LINE Developers Console
> でのブラウザ操作が必須なため、`claude -p` / `cursor-agent --print` では完走できません。
> 対話モードで Claude Code または Cursor を起動し直してから `/setup-line-harness` を実行してください。

`setup-resume.md` の生成は不要（最初から対話モードで実行する想定）。

---

## 関連

- スライド本体: aiagent-course Module 23
- line-harness-oss: <https://github.com/Shudesu/line-harness-oss>
- Wiki: <https://github.com/Shudesu/line-harness-oss/wiki>
- 体験 LINE: <https://shudesu.github.io/line-harness-oss/>
- Module 22 (Discord) との比較: `/setup-discord`

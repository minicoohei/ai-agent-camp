---
description: "Lesson command — deploy line-harness-oss to Cloudflare's free tier"
duration: "~75 min"
prerequisites: ["LINE OA / Developers account", "Cloudflare account", "Node 20+ / pnpm 9+"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "line", "mcp", "cloudflare", "module-23"]
---

# /setup-line-harness -- self-host line-harness-oss on Cloudflare

## Goal

Self-deploy `line-harness-oss` (Cloudflare Workers + D1 + R2) and wire the
`line-harness` MCP into Claude Code. Mirrors aiagent-course Module 23.

> ⚠️ **Cannot complete under non-interactive mode** (`nonInteractiveMode: incompatible`).
> Cloudflare login (`wrangler login`) and LINE Developers Console actions both
> require a browser. Under `claude -p` / `cursor-agent --print` the AI emits a
> short notice and stops — re-run in interactive mode.

---

## Step 0: detect existing setup

The AI checks:

1. `.mcp.json` / `~/.claude/mcp_settings.json` for a `line-harness` entry.
2. `wrangler --version` reachable.
3. A local clone of line-harness-oss (e.g. `~/work/line-marketing`).
4. `LINE_HARNESS_API_KEY` in Keychain (do NOT print the value).

If all set, skip to **Step 6**.

---

## Step 1: create two LINE channels

Open <https://developers.line.biz/console/>. In one Provider:

1. Create a **Messaging API channel** → grab `LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN`.
2. Create a **LINE Login channel** (required) → grab `LINE_LOGIN_CHANNEL_ID` and `LINE_LOGIN_CHANNEL_SECRET`.

> Without the LINE Login channel, UUID issuance breaks → multi-account merge and
> traffic-source attribution stop working. Friends added before you fix this need
> to be re-linked manually.

---

## Step 2: clone and install

```bash
git clone https://github.com/Shudesu/line-harness-oss.git
cd line-harness-oss
pnpm install   # Node 20+ / pnpm 9+
```

---

## Step 3: provision Cloudflare D1 + Worker

```bash
npx wrangler login                        # browser login (one-time)
npx wrangler d1 create line-crm           # paste database_id into apps/worker/wrangler.toml
npx wrangler d1 execute line-crm \
  --file=packages/db/schema.sql           # creates 42 tables
```

---

## Step 4: register five secrets

```bash
npx wrangler secret put LINE_CHANNEL_SECRET
npx wrangler secret put LINE_CHANNEL_ACCESS_TOKEN
npx wrangler secret put LINE_LOGIN_CHANNEL_ID
npx wrangler secret put LINE_LOGIN_CHANNEL_SECRET
npx wrangler secret put API_KEY                  # your own random value
```

---

## Step 5: deploy and wire the webhook

```bash
# Important: use pnpm run deploy. `npx wrangler deploy` alone won't run Vite.
pnpm run deploy
```

LINE Developers Console → Messaging API → **Webhook URL**:

```
https://<your-worker>.workers.dev/webhook
```

Hit Verify → expect 200.

---

## Step 6: connect the line-harness MCP

```jsonc
// .mcp.json  (also add this file to .gitignore)
{
  "mcpServers": {
    "line-harness": {
      "type": "http",
      "url": "https://<your-worker>.workers.dev",
      "env": { "LINE_HARNESS_API_KEY": "***" }
    }
  }
}
```

Restart Claude Code → `/mcp` → expect `line-harness (http): ... ✓ connected`.

---

## Step 7: confirm the eight core tools

| Tool | Purpose |
|---|---|
| `manage_auto_replies` | Keyword auto-replies |
| `manage_scenarios` | Step-delivery scenarios |
| `manage_broadcasts` | Broadcast send / send_to_segment |
| `manage_rich_menus` | Rich-menu image + areas + default |
| `manage_tags` | Tags |
| `manage_friends` | Friends list / tag updates |
| `upload_image` | base64 → R2 public URL |
| `account_summary` | perAccount friend counts |

---

## Top 10 gotchas (mirrors Module 23)

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | Existing followers' messages silently dropped | LINE API can't enumerate followers outside follow events | webhook helper `getOrCreateFriendFromMessage` |
| 2 | `wrangler deploy` doesn't ship | Vite build never runs | always `pnpm run deploy` |
| 3 | WAF (1010) blocks image upload | Non-Mozilla UA | set Mozilla-style UA on `requests` |
| 4 | No UUIDs | LINE Login channel missing | create both channels up front |
| 5 | Flex carousel ignores `size: giga` | carousel bubbles cap at mega | use mega |
| 6 | `account_summary.totalDbRecords` mismatch | per-account sum (with dupes) | read `perAccount` array |
| 7 | API key committed | `.mcp.json` not gitignored | add it; use `***` placeholder |
| 8 | Emoji render as □ on banners | Pillow lacks emoji glyphs | use ★ ✦ ◆ symbols |
| 9 | Auto-reply keyword collisions | All matchType=contains | look up id, update instead of create |
| 10 | Button label cut off | LINE caps labels at 20 chars | shorten label, push copy to body |

---

## Non-interactive behavior

`nonInteractiveMode: incompatible`. Under `-p` the AI prints:

> This command needs `wrangler login` and LINE Developers Console browser actions,
> so it can't run under `claude -p` / `cursor-agent --print`. Restart in interactive
> mode and run `/setup-line-harness` again.

…and exits without writing `setup-resume.md`.

---

## See also

- aiagent-course Module 23 slides
- <https://github.com/Shudesu/line-harness-oss>
- Wiki: <https://github.com/Shudesu/line-harness-oss/wiki>
- `/setup-discord` (Module 22 counterpart)

---
description: "Lesson command — desplegar line-harness-oss en el plan gratuito de Cloudflare"
duration: "~75 min"
prerequisites: ["Cuenta LINE OA / Developers", "Cuenta Cloudflare", "Node 20+ / pnpm 9+"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "line", "mcp", "cloudflare", "module-23"]
---

# /setup-line-harness -- auto-hospedaje de line-harness-oss en Cloudflare

## Objetivo

Desplegar `line-harness-oss` (Cloudflare Workers + D1 + R2) y conectar el MCP
`line-harness` a Claude Code. Refleja el módulo 23 de aiagent-course.

> ⚠️ **No completable en modo no interactivo** (`nonInteractiveMode: incompatible`).
> `wrangler login` y las acciones en LINE Developers Console requieren navegador.
> Bajo `claude -p` / `cursor-agent --print` la IA emite un aviso corto y sale —
> reanuda en modo interactivo.

---

## Paso 0: detectar configuración existente

La IA comprueba:

1. `.mcp.json` / `~/.claude/mcp_settings.json` con entrada `line-harness`.
2. `wrangler --version` accesible.
3. Clon local de line-harness-oss (p. ej. `~/work/line-marketing`).
4. `LINE_HARNESS_API_KEY` en Keychain (NO imprimir el valor).

Si todo está, saltar al **Paso 6**.

---

## Paso 1: dos canales LINE

Abre <https://developers.line.biz/console/>. En un Provider:

1. **Messaging API channel** → toma `LINE_CHANNEL_SECRET` y `LINE_CHANNEL_ACCESS_TOKEN`.
2. **LINE Login channel** (obligatorio) → toma `LINE_LOGIN_CHANNEL_ID` y `LINE_LOGIN_CHANNEL_SECRET`.

> Sin LINE Login se rompe la emisión de UUID → multi-cuenta y atribución de
> origen dejan de funcionar.

---

## Paso 2: clonar e instalar

```bash
git clone https://github.com/Shudesu/line-harness-oss.git
cd line-harness-oss
pnpm install
```

---

## Paso 3: provisionar Cloudflare

```bash
npx wrangler login                        # navegador
npx wrangler d1 create line-crm           # pega database_id en wrangler.toml
npx wrangler d1 execute line-crm \
  --file=packages/db/schema.sql
```

---

## Paso 4: cinco secrets

```bash
npx wrangler secret put LINE_CHANNEL_SECRET
npx wrangler secret put LINE_CHANNEL_ACCESS_TOKEN
npx wrangler secret put LINE_LOGIN_CHANNEL_ID
npx wrangler secret put LINE_LOGIN_CHANNEL_SECRET
npx wrangler secret put API_KEY
```

---

## Paso 5: desplegar y conectar webhook

```bash
# Importante: pnpm run deploy (npx wrangler deploy solo no corre Vite)
pnpm run deploy
```

LINE Developers Console → Messaging API → **Webhook URL**:
`https://<tu-worker>.workers.dev/webhook` → Verify (200 = OK).

---

## Paso 6: MCP en Claude Code

```jsonc
// .mcp.json  (añadir a .gitignore)
{
  "mcpServers": {
    "line-harness": {
      "type": "http",
      "url": "https://<tu-worker>.workers.dev",
      "env": { "LINE_HARNESS_API_KEY": "***" }
    }
  }
}
```

Reinicia Claude Code → `/mcp` → espera `line-harness (http): ... ✓ connected`.

---

## Paso 7: las ocho herramientas

| Herramienta | Uso |
|---|---|
| `manage_auto_replies` | respuestas automáticas |
| `manage_scenarios` | escenarios por pasos |
| `manage_broadcasts` | broadcast / send_to_segment |
| `manage_rich_menus` | rich menu |
| `manage_tags` | tags |
| `manage_friends` | amigos |
| `upload_image` | base64 → URL pública R2 |
| `account_summary` | conteo por sub-cuenta |

---

## 10 tropiezos (igual que módulo 23)

| # | Síntoma | Causa | Solución |
|---|---|---|---|
| 1 | Mensajes de seguidores antiguos descartados | LINE API no enumera fuera de follow | helper `getOrCreateFriendFromMessage` |
| 2 | `wrangler deploy` no aplica | Vite no corre | siempre `pnpm run deploy` |
| 3 | WAF 1010 bloquea subida | UA no Mozilla | UA estilo Mozilla en `requests` |
| 4 | Sin UUIDs | falta LINE Login | crear ambos canales desde el inicio |
| 5 | Flex carousel ignora `size: giga` | bubbles llegan a mega | usar mega |
| 6 | `totalDbRecords` no coincide | suma por sub-cuenta con duplicados | leer `perAccount` |
| 7 | API key en repo | `.mcp.json` no gitignored | añadirlo; usar `***` |
| 8 | Emoji como □ | Pillow no soporta | usar ★ ✦ ◆ |
| 9 | Keywords colisionan | matchType=contains | actualizar id existente |
| 10 | Label cortado | LINE limita 20 chars | acortar y mover copy al body |

---

## Comportamiento no interactivo

`nonInteractiveMode: incompatible`. Bajo `-p` la IA imprime:

> Esta comando necesita `wrangler login` y acciones del navegador en LINE
> Developers Console, así que no termina bajo `claude -p` / `cursor-agent
> --print`. Reinicia en modo interactivo y ejecuta `/setup-line-harness` de nuevo.

…y sale sin escribir `setup-resume.md`.

---

## Ver también

- Slides del módulo 23 en aiagent-course
- <https://github.com/Shudesu/line-harness-oss>
- Wiki: <https://github.com/Shudesu/line-harness-oss/wiki>
- `/setup-discord` (contraparte del módulo 22)

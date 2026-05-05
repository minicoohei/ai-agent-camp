---
description: "Lesson command — configuración del Bot de Discord + claude-channel-discord MCP"
duration: "~30 min"
prerequisites: ["Cuenta de Discord", "Bun o Node.js 18+"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "discord", "mcp", "module-22"]
---

# /setup-discord -- Bot de Discord + claude-channel-discord MCP

## Objetivo

Crear un Bot de Discord en el Developer Portal y conectarlo a Claude Code vía
el MCP `claude-channel-discord`. Refleja el módulo 22 de aiagent-course.

> **Modo no interactivo**: requiere navegador y pegado de token. Bajo `claude -p`
> / `cursor-agent --print` no termina — `nonInteractiveMode: deferred` indica a
> la IA que emita un `setup-resume.md` y se detenga.

---

## Paso 0: detectar configuración existente

La IA debe:

1. Comprobar `~/.claude/mcp_settings.json` y `<project>/.mcp.json` por una entrada `discord`.
2. Verificar `bunx claude-channel-discord@0.0.4 --version` (o `npx ...`).
3. Confirmar `DISCORD_BOT_TOKEN` en Keychain con `security find-generic-password
   -s DISCORD_BOT_TOKEN 2>&1 | head -3` (NO imprimir el valor).

Si todo está, saltar al **Paso 5 (prueba)**.

---

## Paso 1: crear el bot

Abre <https://discord.com/developers/applications>.

1. **New Application** → ponle nombre (p. ej. `AI Agent Camp Demo`) → **Create**.
2. Sidebar **Bot** → **Reset Token** → copia el token al gestor de contraseñas.
3. Activa los dos **Privileged Gateway Intents**: `SERVER MEMBERS INTENT` y `MESSAGE CONTENT INTENT`.

---

## Paso 2: invitar el bot

OAuth2 → URL Generator → scopes `bot` + `applications.commands` → permisos
(Read / Send Messages, Add Reactions, Manage Messages) → abre la URL → elige tu servidor.

---

## Paso 3: guardar el token en Keychain

```bash
security add-generic-password -a "$USER" -s DISCORD_BOT_TOKEN -w '<paste-token>'
echo 'export DISCORD_BOT_TOKEN="$(security find-generic-password -s DISCORD_BOT_TOKEN -w 2>/dev/null)"' >> ~/.zshrc
```

---

## Paso 4: registrar el MCP

```bash
bun install -g claude-channel-discord@0.0.4
claude mcp add --transport stdio discord -- bun x claude-channel-discord@0.0.4
claude mcp list
```

Esperado: `discord (stdio): ... ✓ connected`.

---

## Paso 5: política de acceso

```bash
/discord:access set --dm-policy allowlist
/discord:access approve <tu-discord-user-id>
/discord:access list
```

---

## Paso 6: prueba

En Claude Code: `Mándame un DM "Hello from MCP" en Discord`. Si llega, listo.

---

## Tropiezos comunes (igual que slide del módulo 22)

| Síntoma | Causa | Solución |
|---|---|---|
| Token deja de funcionar | Token viejo tras Reset | Reset y actualiza Keychain |
| No lee mensajes | `MESSAGE CONTENT INTENT` apagado | Activar y reiniciar MCP |
| DMs ajenos no visibles | Límite del API | Canales de ticket privados |
| No puedo iniciar DM | Sin canal DM previo | El usuario debe escribirle al bot primero |

---

## Comportamiento no interactivo

`nonInteractiveMode: deferred` — bajo `-p` sólo corre el Paso 0; el resto
queda en `setup-resume.md` para retomar en interactivo. Ver `_lib/non-interactive.md`.

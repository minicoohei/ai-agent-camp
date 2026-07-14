---
description: "Lesson command — configuración del Bot de Discord + plugin oficial de Claude Code Channels"
duration: "~30 min"
prerequisites: ["Cuenta de Discord", "Claude Code", "Bun"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "discord", "plugin", "module-22"]
---

# /setup-discord -- Bot de Discord + plugin oficial de Claude Code Channels

## Objetivo

Crear un Bot de Discord en el Developer Portal y lanzarlo como Channel de Claude
Code con el plugin oficial `discord@claude-plugins-official`. Refleja el módulo
22 de aiagent-course.

> **Modo no interactivo**: requiere navegador, pegado de token y comandos de
> plugin dentro de Claude Code. Bajo `claude -p` / `cursor-agent --print` no
> termina; `nonInteractiveMode: deferred` indica a la IA que emita un
> `setup-resume.md` y se detenga.

---

## Paso 0: detectar configuración existente

La IA debe:

1. Guiar al alumno para comprobar si `discord@claude-plugins-official` está instalado en Claude Code.
2. Confirmar que `~/.claude/channels/discord/.env` contiene `DISCORD_BOT_TOKEN` sin imprimir el valor.
3. Pedir que ejecute `/discord:access` dentro de Claude Code para revisar el estado de acceso.

Si todo está listo, saltar al **Paso 6 (prueba)**.

---

## Paso 1: crear el bot

Abre <https://discord.com/developers/applications>.

1. **New Application** → ponle nombre (por ejemplo, `AI Agent Camp Demo`) → **Create**.
2. Sidebar **Bot** → **Reset Token** → copia el token inmediatamente al gestor de contraseñas.
3. En **Privileged Gateway Intents**, activa sólo `MESSAGE CONTENT INTENT`.

MESSAGE CONTENT INTENT es necesario para que el bot pueda leer el texto de los mensajes.

---

## Paso 2: invitar el bot

1. Abre **OAuth2** → **URL Generator**.
2. Selecciona el scope `bot`.
3. En **Bot Permissions**, selecciona los permisos mínimos:
   - `View Channels`
   - `Send Messages`
   - `Send Messages in Threads`
   - `Read Message History`
   - `Attach Files`
4. Define **Integration type** como **Guild Install**.
5. Abre la URL generada y agrega el bot a tu servidor.

---

## Paso 3: instalar el plugin oficial de Discord

Inicia Claude Code y ejecuta estos comandos dentro de Claude Code:

```text
/plugin install discord@claude-plugins-official
/reload-plugins
```

Después de recargar plugins, configura el token del bot en la misma sesión de Claude Code:

```text
/discord:configure <paste-bot-token>
```

Esto escribe `DISCORD_BOT_TOKEN` en `~/.claude/channels/discord/.env`. No pegues
el token en chats normales ni logs.

---

## Paso 4: lanzar Claude Code con Channels

Sal de Claude Code y arráncalo desde la terminal:

```bash
claude --channels plugin:discord@claude-plugins-official
```

El channel de Discord no se inicia con un registro normal de servidor. Lanza
siempre con `--channels plugin:discord@claude-plugins-official`.

---

## Paso 5: configurar control de acceso

El pairing captura tu ID de usuario de Discord. Mantén Claude Code corriendo con
el comando del Paso 4 y envía un DM al bot desde Discord. Cuando el bot responda
con un código de 6 caracteres, ejecuta dentro de Claude Code:

```text
/discord:access pair <code>
/discord:access policy allowlist
/discord:access
```

Si ya conoces el snowflake de Discord de un usuario, agrégalo manualmente:

```text
/discord:access allow <snowflake>
/discord:access
```

Para producción, cambia a `allowlist` después de agregar los usuarios necesarios
para que emisores desconocidos no reciban códigos de pairing.

---

## Paso 6: prueba

Con Claude Code corriendo como:

```bash
claude --channels plugin:discord@claude-plugins-official
```

Envía un DM al bot desde Discord y confirma que la notificación llega a Claude
Code y que el bot puede responder. Si no pasa nada, ejecuta `/discord:access`
para revisar allowlist y pairings pendientes.

---

## Tropiezos comunes (igual que slide del módulo 22)

| Síntoma | Causa | Solución |
|---|---|---|
| Token deja de funcionar | Token viejo tras `Reset Token` | Haz Reset otra vez y ejecuta `/discord:configure <paste-bot-token>` |
| No lee mensajes | `MESSAGE CONTENT INTENT` apagado | Actívalo y relanza con `--channels` |
| El bot no reacciona a DMs | Claude Code se lanzó sin `--channels` | Inicia con `claude --channels plugin:discord@claude-plugins-official` |
| No está claro qué pasa con usuarios desconocidos | Política de acceso / allowlist sin revisar | Ejecuta `/discord:access`, luego usa `pair` o `allow` según haga falta |

---

## Comportamiento no interactivo

`nonInteractiveMode: deferred` — bajo `-p`, sólo puede correr el Paso 0. Las
acciones de navegador, pegado de token y comandos de plugin de Claude Code se
escriben en `setup-resume.md` para retomar en modo interactivo. Ver
`_lib/non-interactive.md`.

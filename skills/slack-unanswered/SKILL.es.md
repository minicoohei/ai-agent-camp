---
name: slack-unanswered
description: "Habilidad que detecta mensajes sin responder en Slack y genera borradores de respuesta. Se activa con solicitudes como 'Mensajes sin responder', 'Mensajes que no he respondido', 'Verificar Slack'."
triggers:
  - Mensajes sin responder
  - Mensajes que no he respondido
  - Verificar Slack
  - Menciones no leídas
  - Mensajes que necesitan respuesta
  - slack-unanswered
  - unanswered messages
---

## Palabras clave de activación
"Mensajes sin responder", "Mensajes que no he respondido", "Verificar Slack", "Menciones no leídas"

# Buscador de mensajes sin responder en Slack

Esta habilidad encuentra mensajes de Slack que necesitan su atención y le ayuda a responderlos.

## Directorio objetivo

Todas las búsquedas se realizan en: `slack-sync/data/`

## Sus identificadores

> Reemplace lo siguiente con su propio nombre de visualización y nombre de usuario de Slack.

Buscar estos nombres (sin distinción de mayúsculas):
- `@{SU_NOMBRE_DE_VISUALIZACIÓN}`
- `@{SU_NOMBRE_COMPLETO}`
- `@{SU_USUARIO_SLACK}`
- Mensajes publicados por: `{SU_NOMBRE_COMPLETO}`, `{SU_USUARIO_SLACK}`

Configuración: Reemplace los marcadores de posición anteriores con su información, o especifique mediante la opción `--users`.

---

## Flujo de trabajo

### Paso 1: Encontrar mensajes sin responder

Buscar mensajes que contengan sus identificadores:

```bash
grep -rn -B2 -A10 -E "@{SU_NOMBRE_DE_VISUALIZACIÓN}|@{SU_USUARIO_SLACK}|{SU_NOMBRE_COMPLETO}" slack-sync/data/
```

### Paso 2: Identificar mensajes sin responder

Un mensaje está **sin responder** si:
1. Contiene una mención de su nombre (o usted lo publicó)
2. Termina con una pregunta (`?`) o contiene una solicitud
3. NO hay líneas que comiencen con `> ####` inmediatamente después (antes del siguiente `###` o `---`)

Enfocarse en mensajes recientes (últimos 7 días). Excluir mensajes de bots (Sentry, Vercel, etc.).

### Paso 3: Presentar hallazgos

Para cada mensaje sin responder, proporcionar:
- Nombre del canal
- Fecha/Hora
- Remitente
- Resumen del contenido
- Enlace de Slack
- Si necesita respuesta o es un seguimiento

### Paso 4: Generar borrador de respuesta

Para mensajes que necesitan respuestas, genere un borrador de respuesta en japonés. Pida al usuario que revise y edite.

### Paso 5: Enviar respuesta (con confirmación)

**IMPORTANTE: ¡Siempre obtenga confirmación del usuario antes de enviar!**

El flujo de respuesta es:
1. Mostrar el borrador de respuesta al usuario
2. Preguntar: "¿Está bien enviar con este contenido? (Avíseme si tiene ediciones)"
3. Esperar la confirmación o ediciones del usuario
4. Solo después de la aprobación explícita, usar el script de respuesta

---

## Responder a mensajes

### Ubicación del script de respuesta

```
slack-sync/scripts/reply_slack.py
```

### Uso

```bash
# Ejecución en seco (vista previa sin enviar)
python slack-sync/scripts/reply_slack.py \
  --url "https://xxx.slack.com/archives/CHANNEL/pTIMESTAMP" \
  --message "Contenido de respuesta" \
  --dry-run

# Enviar realmente (¡solo después de que el usuario confirme!)
python slack-sync/scripts/reply_slack.py \
  --url "https://xxx.slack.com/archives/CHANNEL/pTIMESTAMP" \
  --message "Contenido de respuesta"
```

### Variable de entorno requerida

```
SLACK_USER_TOKEN=xoxp-...
```

Este token necesita el scope `chat:write`. Consulte las instrucciones de configuración a continuación.

---

## Configuración: Agregar scope chat:write

Para habilitar la funcionalidad de respuesta:

1. Vaya a [Slack API Apps](https://api.slack.com/apps)
2. Seleccione su aplicación (ej., "Message Archiver")
3. Navegue a **OAuth & Permissions**
4. En **User Token Scopes**, agregue:
   - `chat:write` - Publicar mensajes
5. Haga clic en **Reinstall to Workspace**
6. Copie el nuevo token `xoxp-...`
7. Actualice `SLACK_USER_TOKEN` en su entorno/GitHub Secrets

---

## Referencia de formato de mensajes

Mensajes en archivos markdown:
- **Mensaje principal**: `### HH:MM - Nombre del remitente [[Slack]](url)`
- **Respuesta**: Líneas que comienzan con `> ####`

---

## Gestión de archivo TODO

### Ubicación del archivo TODO

```
slack-sync/TODO.md
```

### Flujo de trabajo con TODO

1. **Durante la búsqueda**: Agregar mensajes sin responder encontrados a TODO.md
2. **Al responder**: Cambiar la casilla de verificación a `[x]`
3. **Al completar**: Mover a la sección "Mensajes completados"

---

## Comandos rápidos

### Encontrar menciones en archivos recientes:
```bash
grep -rn -B2 -A10 "@{SU_NOMBRE_DE_VISUALIZACIÓN}" slack-sync/data/ | head -200
```

### Encontrar sus publicaciones:
```bash
grep -rn "### [0-9:]* - {SU_NOMBRE_DE_VISUALIZACIÓN}" slack-sync/data/ | head -100
```

### Encontrar preguntas dirigidas a usted:
```bash
grep -rn -A5 "@{SU_NOMBRE_DE_VISUALIZACIÓN}" slack-sync/data/ | grep -E "\?$|por favor|podría|puede"
```

### Ver TODO actual:
```bash
cat slack-sync/TODO.md
```

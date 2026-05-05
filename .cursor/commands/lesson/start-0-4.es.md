---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "~15 min"
prerequisites: ["start-0-1", "start-0-2", "start-0-3"]
level: "beginner"
tags: ["setup", "slack", "api"]
nonInteractiveMode: deferred
---
# Lección 0-4: Configuración de Slack API

## Verificar progreso de configuración

**Ejecución automática por IA:** Ejecute `uv run python tools/setup_progress.py show` para mostrar el progreso actual de la configuración.

---

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Crear una Slack App, obtener un Bot Token, configurarlo en .env y habilitar las funciones de integración con Slack |
| Duración | ~15 min |
| Requisitos previos | Lección 0-1 a Lección 0-3 completadas; acceso de administrador (o permiso de creación de Apps) en un espacio de trabajo de Slack |
| Página del curso | Consulte [Página principal del curso](https://ai-agent.camp/es/course/module-0) en paralelo |

> **Consejo**: Si la IA deja de responder, escriba "por favor continua" o "se detuvo" para reanudar.

---

## Configuración automática de Slack API

En esta lección, solo ejecute `/setup-slack` y habrá terminado.
**No se requieren operaciones de terminal. La IA se encarga de todo automáticamente.**

### Lo que la IA hace automáticamente

1. Abrir automáticamente la página de administración de Slack App en el navegador
2. Guiarlo paso a paso en la creación de una Slack App
3. Guiarlo en la configuración de Bot Token Scopes (channels:history, channels:read, chat:write, users:read)
4. Guiarlo en la instalación al espacio de trabajo y obtención del token
5. Agregar automáticamente la línea del token al archivo `.env`
6. Usted ingresa el token directamente en el archivo `.env`
7. Ejecutar automáticamente una solicitud de prueba a Slack API para verificar el funcionamiento

**Importante**: No pegue el token en el chat. Puede guardarlo de forma segura con el siguiente comando:

```bash
uv run python tools/credential_manager.py store SLACK_BOT_TOKEN
```

Al ejecutarlo, aparecerá un indicador de entrada de contraseña. El valor ingresado no se muestra en pantalla y se almacena de forma segura en el Credential Store del sistema operativo (macOS Keychain, etc.).

> **Nota**: También puede escribir directamente en el archivo `.env`, pero en Claude Code esto puede ser bloqueado por el guardia de seguridad (write_guard). Usar `credential_manager.py` es el método más seguro y confiable.

**Configuración de AskQuestion:**
```json
{
  "title": "Configuracion de Slack API",
  "questions": [{
    "id": "action",
    "prompt": "Desea iniciar la configuracion de Slack API?",
    "options": [
      {"id": "run", "label": "Iniciar configuracion (ejecutar /setup-slack)"},
      {"id": "already_done", "label": "Slack API ya esta configurada"},
      {"id": "no_slack", "label": "No tengo un espacio de trabajo de Slack"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(run -> Ejecutar el contenido de `/setup-slack`)
(already_done -> Ir al punto de verificación)
(no_slack -> Guiar: "Puede crear un espacio de trabajo de Slack gratis. Cree un espacio de trabajo de prueba en https://slack.com/create y luego reinicie esta configuración.")
(different_lesson -> Mostrar lista de modulos)

---

## Comandos a ejecutar

```text
/setup-slack
```

## Ejemplo de salida esperada

```text
Resultado de prueba de Slack API:
Conexion: OK
Espacio de trabajo: your-workspace
Nombre del Bot: AIAgent Bootcamp
```

## Solución de problemas comunes
- El navegador no se abre -> Abra manualmente `https://api.slack.com/apps`
- Error `not_authed` -> Verifique en .env que el token se haya copiado correctamente
- Error `missing_scope` -> Agregue los scopes en la página de administración de Slack, luego haga clic en "Reinstall to Workspace"

---

## Punto de verificación
- [ ] Creó una Slack App llamada "AIAgent Bootcamp"
- [ ] Configuró los Bot Token Scopes necesarios
- [ ] Instaló la App en el espacio de trabajo
- [ ] SLACK_BOT_TOKEN está configurado en .env
- [ ] La prueba de API fue exitosa

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next", "label": "Configurar ajustes de seguridad (/start-0-5)"},
      {"id": "try_slack", "label": "Probar busqueda en Slack (/start-6-1)"},
      {"id": "check", "label": "Verificar el entorno (/check-setup)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

(next -> Guiar a /start-0-5)
(try_slack -> Guiar a /start-6-1)
(check -> Ejecutar el contenido de /check-setup)
(finish -> Fin)

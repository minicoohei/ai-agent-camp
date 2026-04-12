---
description: "When the user says /start-0-3 — Módulo 0 Lección 0-3: Configuración de Gemini API"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "~10 min"
prerequisites: ["start-0-1", "start-0-2"]
level: "beginner"
tags: ["setup", "gemini", "api"]
---

# Lección 0-3: Configuración de Gemini API

## Verificar progreso de configuración

**Ejecución automática por IA:** Ejecute `uv run python tools/setup_progress.py show` para mostrar el progreso actual de la configuración.

---

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Obtener una clave de Gemini API desde Google AI Studio y configurarla en .env para poder usar funciones de IA como la generación de imagenes |
| Duración | ~10 min |
| Requisitos previos | Lección 0-1 y Lección 0-2 completadas; poder iniciar sesión en una cuenta de Google desde el navegador |
| Página del curso | Consulte [Página principal del curso](https://ai-agent.camp/es/course/module-0) en paralelo |

> **Consejo**: Si la IA deja de responder, escriba "por favor continua" o "se detuvo" para reanudar.

---

## Configuración automática de Gemini API

En esta lección, solo ejecute `/setup-gemini` y habrá terminado.
**No se requieren operaciones de terminal. La IA se encarga de todo automáticamente.**

### Lo que la IA hace automáticamente

1. Abrir automáticamente Google AI Studio en el navegador (la IA ejecuta `open` / `start` según su sistema operativo)
2. Guiarlo paso a paso en el proceso de obtención de la clave API en el navegador
3. Crear automáticamente el archivo `.env` (copiar de `.env.example` + verificar `.gitignore`)
4. Usted ingresa la clave API directamente en el archivo `.env` (editar en el editor de Cursor)
5. Ejecutar automáticamente una solicitud de prueba a Gemini API para verificar el funcionamiento

**Importante**: No pegue la clave API en el chat. Este proceso utiliza la entrada directa en el archivo `.env`.

**Configuración de AskQuestion:**
```json
{
  "title": "Configuracion de Gemini API",
  "questions": [{
    "id": "action",
    "prompt": "Desea iniciar la configuracion de Gemini API?",
    "options": [
      {"id": "run", "label": "Iniciar configuracion (ejecutar /setup-gemini)"},
      {"id": "already_done", "label": "Gemini API ya esta configurada"},
      {"id": "view_html", "label": "Ver la pagina del curso primero"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(run -> Ejecutar el contenido de `/setup-gemini`)
(already_done -> Ir al punto de verificación)
(view_html -> Proporcionar la URL de la página del curso)
(different_lesson -> Mostrar lista de modulos)

---

## Comandos a ejecutar

```text
/setup-gemini
```

## Ejemplo de salida esperada

```text
Resultado de prueba de Gemini API:
Respuesta de API: Hola! En que puedo ayudarle?
```

> **Nota**: El texto de respuesta varia según el modelo. Si no se produce ningún error, la conexión fue exitosa.

## Solución de problemas comunes
- El navegador no se abre -> Pida a la IA que "abra Google AI Studio"
- La prueba de API falla -> Verifique la clave en .env y vuelva a ejecutar `/setup-gemini`

---

## Punto de verificación
- [ ] Obtuvo una clave API de Google AI Studio
- [ ] GEMINI_API_KEY está configurada en .env
- [ ] El archivo .env está excluido por .gitignore
- [ ] La prueba de API fue exitosa (se recibio una respuesta de Gemini API)

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
      {"id": "next", "label": "Configurar Slack API (/start-0-4)"},
      {"id": "try_banner", "label": "Intentar crear un banner ahora mismo (/start-1-1)"},
      {"id": "check", "label": "Verificar el entorno (/check-setup)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

(next -> Guiar a /start-0-4)
(try_banner -> Guiar a /start-1-1)
(check -> Ejecutar el contenido de /check-setup)
(finish -> Fin)

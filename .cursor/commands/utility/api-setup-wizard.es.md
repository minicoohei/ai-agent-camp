---
description: "Guía unificada de configuración de API (lista de configuraciones de servicios)"
aliases: ["api-setup", "setup-api"]
category: "setup"
duration: "Aproximadamente 5 minutos"
prerequisites: ["Cursor está instalado", "La carpeta ai-agent-camp está abierta"]
level: "beginner"
tags: ["setup", "api", "guide"]
---

# API Setup Wizard - Guía de configuración unificada

Gestione de forma centralizada la configuración de varias API (Google, Notion, Slack, Fal.AI, Gemini, etc.).

## Configuración rápida (recomendada)

Simplemente ingrese los siguientes comandos en el campo de chat de Cursor, y la IA le guiará a través de la configuración de forma interactiva.

| Comando | Servicio objetivo | Descripción |
|---------|-------------------|-------------|
| `/setup-gemini` | Gemini API | Necesario para generación de imágenes/texto (obligatorio) |
| `/setup-github` | GitHub | Necesario para operaciones de repositorio y Actions (recomendado) |
| `/setup-slack` | Slack API | Necesario para búsqueda en Slack y gestión de tareas |
| `/check-setup` | Verificación general | Verificar todas las configuraciones de API de una vez |

## Servicios compatibles

| Servicio | Descripción | Método de configuración |
|----------|-------------|------------------------|
| `gemini` | IA generativa Google Gemini | Ejecute `/setup-gemini` |
| `google` | Gmail, Calendar, Drive, Sheets, Slides | Ejecute `/setup-google-api` |
| `notion` | Páginas y bases de datos de Notion | Ingrese `NOTION_API_KEY` directamente en `.env` |
| `slack` | Espacio de trabajo de Slack | Ejecute `/setup-slack` |
| `fal` | Generación de imágenes/video Fal.AI | Ingrese `FAL_KEY` directamente en `.env` |
| `heygen` | Videos con avatar de IA HeyGen | Ingrese `HEYGEN_API_KEY` directamente en `.env` |
| `elevenlabs` | ElevenLabs TTS (texto a voz) | Ingrese `ELEVENLABS_API_KEY` directamente en `.env` |
| `typefully` | Gestión de publicaciones Typefully X (antes Twitter) | Ingrese `TYPEFULLY_API_KEY` directamente en `.env` |

## Verificar el estado de la configuración

Para verificar todas las configuraciones de API, ingrese lo siguiente en el campo de chat de Cursor:

```text
/check-setup
```

La IA verificará automáticamente todos los elementos y mostrará un informe indicando qué API están configuradas y cuáles no.

## Comandos relacionados

- `/setup-gemini` - Configuración de Gemini API (la IA abre el navegador para guiarle)
- `/setup-slack` - Configuración de Slack API (la IA abre el navegador para guiarle)
- `/setup-github` - Configuración de autenticación de GitHub
- `/check-setup` - Verificación integral del entorno
- `/setup-google-api` - Configuración dedicada de Google API (flujo de autenticación OAuth)
- `/gmail-account-setup` - Configuración de múltiples cuentas de Gmail

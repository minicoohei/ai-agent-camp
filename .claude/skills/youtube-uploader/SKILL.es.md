---
name: youtube-uploader
description: "Habilidad de carga de video usando YouTube Data API v3. Soporta detección automática de Shorts, inserción automática de enlaces UTM y publicación programada. Se activa con 'Publicar en YouTube', 'Subir video', 'Publicar Shorts', etc."
status: draft
triggers:
  - Publicar en YouTube
  - Subir video
  - Publicar Shorts
  - Publicar video de YouTube
  - Configurar publicación programada
  - youtube-uploader
  - YouTube upload
---

# Habilidad de Carga a YouTube

Carga de video mediante YouTube Data API v3. Soporta detección automática de Shorts e inserción automática de enlaces UTM.

## Palabras de Activación
- YouTube, publicación de YouTube, carga de video, publicación de Shorts, YouTube Shorts

## Estado de Implementación

> **Borrador:** El script de carga no está incluido. No se proporciona ningún comando de ejecución hasta que se agregue la implementación.

## Características Planificadas

- **Detección Automática de Shorts**: Vertical (h>w) y 60 segundos o menos -> tratado automáticamente como Shorts
- **Inserción Automática de Enlace UTM**: Si la descripción no contiene enlace ai-agent.camp, se agrega automáticamente
- **Carga Resumible**: Carga estable en fragmentos de 10MB
- **Guardado de Logs**: `output/gtm/youtube/upload_YYYYMMDD_HHMMSS.json`

## Dependencias

- `google-api-python-client`, `google-auth` (para carga)
- `ffprobe` (para detección de Shorts, opcional)

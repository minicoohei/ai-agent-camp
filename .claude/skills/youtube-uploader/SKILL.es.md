---
name: youtube-uploader
description: "Habilidad de carga de video usando YouTube Data API v3. Soporta detección automática de Shorts, inserción automática de enlaces UTM y publicación programada. Se activa con 'Publicar en YouTube', 'Subir video', 'Publicar Shorts', etc."
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

## Uso

```bash
# Carga básica (dry-run)
python scripts/gtm/upload_youtube.py --file video.mp4 --title "Título" --description "Descripción" --dry-run

# Publicación de Shorts
python scripts/gtm/upload_youtube.py --file short.mp4 --title "Consejos de IA" --shorts --dry-run

# Publicación programada
python scripts/gtm/upload_youtube.py --file video.mp4 --title "..." --schedule "2026-03-20T09:00:00Z" --dry-run

# Con etiquetas
python scripts/gtm/upload_youtube.py --file video.mp4 --title "..." --tags "IA,agente,sin-código" --dry-run
```

## Argumentos

| Argumento | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| `--file` | Sí | - | Ruta del archivo de video |
| `--title` | Sí | - | Título del video |
| `--description` | No | - | Descripción (enlace UTM agregado automáticamente) |
| `--tags` | No | - | Etiquetas separadas por coma |
| `--category` | No | 27 | ID de categoría (27=Educación) |
| `--privacy` | No | private | private/unlisted/public |
| `--shorts` | No | false | Forzar modo Shorts |
| `--language` | No | ja | Idioma del video |
| `--schedule` | No | - | Publicación programada (ISO 8601) |
| `--credentials` | No | env | Ruta del JSON de autenticación de YouTube |
| `--dry-run` | No | false | No subir |

## Características

- **Detección Automática de Shorts**: Vertical (h>w) y 60 segundos o menos -> tratado automáticamente como Shorts
- **Inserción Automática de Enlace UTM**: Si la descripción no contiene enlace ai-agent.camp, se agrega automáticamente
- **Carga Resumible**: Carga estable en fragmentos de 10MB
- **Guardado de Logs**: `output/gtm/youtube/upload_YYYYMMDD_HHMMSS.json`

## Dependencias

- `google-api-python-client`, `google-auth` (para carga)
- `ffprobe` (para detección de Shorts, opcional)

---
name: youtube-clipper
description: "Habilidad para extraer momentos destacados de videos de YouTube/múltiples plataformas usando IA y generar clips con subtítulos bilingües. Se activa con 'Recortar del video', 'Extraer momentos destacados', 'Clips con subtítulos', etc."
triggers:
  - Recortar del video
  - Extraer momentos destacados
  - Crear clips con subtítulos
  - Clip de YouTube
  - Cortar mejores momentos del video
  - youtube-clipper
  - clip highlight
---

# /youtube-clipper - Extracción de Momentos Destacados y Generación de Clips

## Punto de Entrada

```bash
python skills/youtube-clipper/scripts/main.py --url "https://..."
```

## Descripción General

Analiza semánticamente los momentos destacados de videos de YouTube/Vimeo/X usando IA,
y genera automáticamente clips con subtítulos bilingües.

## Inicio Rápido

```bash
# Extraer clips de un video de YouTube
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=xxxxx"

# También soporta videos locales
python skills/youtube-clipper/scripts/clipper.py \
  --file /path/to/local.mp4

# Modo de selección automática (extraer capítulos con puntuación > 0.8)
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://..." --auto-select "score>0.8"
```

## Flujo de Trabajo

```text
Entrada (URL o archivo local)
  |
Paso 1: Descarga de video + obtención de subtítulos (sin subtítulos -> reconocimiento de voz Gemini)
  |
Paso 2: Análisis de capítulos con IA (segmentación semántica + resumen + puntuación)
  |
Paso 3: El usuario selecciona momentos destacados (número/lenguaje natural/filtro de puntuación)
  |
Paso 4: Extracción de clip + traducción de subtítulos + incrustación
  |
Salida: clips/ + chapters.json + resumen para redes sociales
```

## Parámetros

| Parámetro | Predeterminado | Descripción |
|-----------|----------------|-------------|
| `--url` | - | URL de YouTube/Vimeo/X, etc. |
| `--file` | - | Archivo de video local |
| `--output` | `output/clips/` | Directorio de salida |
| `--resolution` | `1080` | Calidad de video (720/1080/best) |
| `--target-lang` | `ja` | Idioma de traducción objetivo |
| `--burn-subtitles` | false | Incrustar subtítulos en el video |
| `--auto-select` | - | Criterios de selección automática (`score>0.8`, `all`) |
| `--chapters-only` | false | Solo análisis de capítulos (sin extracción de clips) |

## Estructura de Salida

```text
output/clips/YYYYMMDD_HHMMSS_{video_id}/
+-- metadata.json
+-- chapters.json
+-- subtitles/
|   +-- original.srt
|   +-- translated_ja.srt
+-- clips/
|   +-- clip_01/
|   |   +-- clip_01.mp4
|   |   +-- clip_01_subtitled.mp4
|   |   +-- original.srt
|   |   +-- translated_ja.srt
|   |   +-- bilingual.srt
|   |   +-- summary.json
|   +-- ...
+-- remotion_input.json
```

## Plataformas Soportadas

YouTube, Vimeo, X/Twitter, Niconico, Dailymotion, etc. (rango soportado por yt-dlp)

## Videos Sin Subtítulos

Cuando los subtítulos no están disponibles, se extrae el audio con FFmpeg,
y Gemini 3.0 Flash Preview realiza la transcripción + generación de marcas de tiempo.

## Estimación de Costos

| Proceso | Costo |
|---------|-------|
| Descarga de video | $0 |
| Transcripción Gemini (video de 10 min) | ~$0.02 |
| Análisis de capítulos | ~$0.01 |
| Traducción de subtítulos | ~$0.005 |
| **Total** | **~$0.035/video** |

## Solución de Problemas

### La Descarga de YouTube Falla

Los servidores headless pueden ser bloqueados por la detección de bots de YouTube.
Configure un archivo de cookies:

```bash
# Método 1: Especificar archivo de cookies
export YTDLP_COOKIES=/path/to/cookies.txt    # Mac/Linux/WSL

# Método 2: Obtener cookies del navegador (para PC local)
export YTDLP_COOKIES_FROM_BROWSER=chrome    # Mac/Linux/WSL
```

Cómo obtener el archivo de cookies:
1. Exportar cookies de YouTube usando extensión de navegador "Get cookies.txt LOCALLY" o similar
2. Subir el cookies.txt en formato Netscape al servidor
3. Establecer la ruta en la variable de entorno `YTDLP_COOKIES`

### yt-dlp No Encontrado

```bash
uv add yt-dlp
```

### FFmpeg No Encontrado

```bash
sudo apt-get install -y ffmpeg    # Ubuntu/Debian
# macOS: brew install ffmpeg
# Windows: winget install ffmpeg
```

### Se Requiere deno (Runtime JS)

El extractor de YouTube de yt-dlp puede requerir el runtime JS deno.

> ⚠️ **Aviso de seguridad**: `curl ... | sh` ejecuta scripts remotos sin verificación.
> Prefiere estas alternativas:
> - macOS: `brew install deno`
> - Windows: `winget install DenoLand.Deno`
> - Manual: revisa la [guía oficial de instalación de Deno](https://docs.deno.com/runtime/manual/getting_started/installation)

```bash
# Solo después de asumir el riesgo de pipe-to-shell
curl -fsSL https://deno.land/install.sh | sh    # Mac/Linux/WSL
export PATH="$HOME/.deno/bin:$PATH"    # Mac/Linux/WSL
```

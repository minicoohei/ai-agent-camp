---
description: "When the user says /start-15-7 — Module 15 Lesson 15-7: YouTube Clipper para extracción de momentos destacados de video"
chapter: "courses/aiagent/lesson03-core/module15-video/chapter.yaml"
duration: 40 min
prerequisites: ["FFmpeg", "yt-dlp", "Gemini API key"]
level: intermediate
tags: ["video", "clipper", "subtitles", "ai-analysis"]
---

# Lección 15-7: YouTube Clipper -- Extracción de Momentos Destacados

## Objetivos de Aprendizaje

En esta lección, aprendera a extraer automáticamente momentos destacados de videos de YouTube (u otras plataformas) usando IA.

1. Descarga de video y obtención de subtítulos
2. División semántica de capítulos con IA
3. Selección de momentos destacados con lenguaje natural
4. Extracción de clips + generación de subtítulos bilingües
5. Reconocimiento de voz con Gemini para videos sin subtítulos

---

## Paso 1: Verificación del Entorno

Primero verifique que las herramientas necesarias están instaladas.

```bash
yt-dlp --version
ffmpeg -version | head -1
python3 -c "import pysrt; print('pysrt OK')"    # En Windows reemplace python3 por python
```

Si no están instaladas:
```bash
pip install yt-dlp pysrt
apt-get install ffmpeg    # Ubuntu/Debian
# macOS: brew install ffmpeg
# Windows: winget install ffmpeg o descargue de https://ffmpeg.org/download.html
```

---

## Paso 2: Verificar Información del Video

Prepare la URL de un video de YouTube de su elección.
Primero verifique la información del video:

```bash
python skills/youtube-clipper/scripts/downloader.py \
  "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --subs-only
```

Verifique en la salida:
- `subtitles_available`: Idiomas de subtítulos manuales
- `auto_subtitles_available`: Idiomas de subtítulos automáticos
- `duration`: Duración del video

---

## Paso 3: Análisis de Capítulos con Clipper

Ejecute solo el análisis de capítulos:

```bash
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --chapters-only
```

La IA dividirá el video en capítulos semanticos, asignando a cada uno un título, resumen y highlight_score.

---

## Paso 4: Extracción de Clips de Momentos Destacados

Extraiga como clips los capítulos con puntuaciones altas:

```bash
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --auto-select "score>0.7" \
  --burn-subtitles
```

En el directorio `output/clips/` se generan:
- MP4 de cada clip
- Subtítulos originales + subtítulos traducidos
- SRT bilingüe
- Resumen para publicación en redes sociales (JSON)

---

## Paso 5: Transcripción de Videos sin Subtítulos (Avanzado)

Incluso para videos sin subtítulos, puede usar el reconocimiento de voz de Gemini:

```bash
# Probar con un archivo de video local
python skills/youtube-clipper/scripts/clipper.py \
  --file /path/to/video_without_subs.mp4
```

Internamente, se extrae el audio con FFmpeg y se transcribe con Gemini 3.0 Flash Preview.

---

## Ejercicios

1. **Básico**: Seleccione un video de YouTube de su elección (5-15 minutos) y extraiga al menos 3 clips
2. **Aplicado**: Grabe subtítulos bilingües en los clips de un video en inglés
3. **Avanzado**: Pruebe el reconocimiento de voz de Gemini con un video sin subtítulos y verifique la precisión

---

## Siguientes Pasos

En la Lección 15-8, aprendera a convertir los clips extraidos en materiales de marketing para redes sociales con Remotion.

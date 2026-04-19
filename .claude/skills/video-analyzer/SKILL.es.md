---
name: video-analyzer
description: "Habilidad para analizar videos de TikTok/YouTube y convertirlos en plantillas. Descarga video, extrae fotogramas, ejecuta STT, analiza composición y genera JSON de plantilla. Se usa para análisis de competidores y aprendizaje de estructuras de videos populares. Se activa con 'Analizar video', 'Análisis de TikTok', 'Análisis de YouTube', etc."
triggers:
  - Analizar video
  - Análisis de TikTok
  - Analizar video de YouTube
  - Analizar video de competidor
  - Convertir video a plantilla
  - video-analyzer
  - Aprender composición de video
---

# Analizador de Video

Descarga, analiza y convierte videos de TikTok/YouTube/Instagram en plantillas.

## Plataformas Soportadas

- **TikTok** -- `https://www.tiktok.com/@user/video/...` / `https://vt.tiktok.com/...`
- **YouTube** -- `https://www.youtube.com/watch?v=...` / `https://youtu.be/...`
- **YouTube Shorts** -- `https://youtube.com/shorts/...`
- **Instagram Reels** -- `https://www.instagram.com/reel/...`
- Otras plataformas soportadas por yt-dlp

## Inicio Rápido

```bash
# Analizar un video de TikTok
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://www.tiktok.com/@user/video/123456" \
  --output output/templates/

# Analizar un video de YouTube
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://www.youtube.com/watch?v=XXXXX" \
  --output output/templates/

# Analizar YouTube Shorts
python skills/video-analyzer/scripts/analyze_video.py \
  --url "https://youtube.com/shorts/XXXXX" \
  --output output/templates/
```

## Pipeline

```
URL -> yt-dlp -> Archivo de video (soporta TikTok/YouTube/Instagram, etc.)
  -> ffmpeg -> Extracción de fotogramas (1fps)
  -> Whisper API -> STT (texto + marcas de tiempo)
  -> Vision IA -> Análisis de fotogramas (posición de subtítulos, diseño, composición)
  -> JSON de plantilla (compatible con scenes.json)
```

## Salida: template.json

```json
{
  "source_url": "https://...",
  "duration": 32.5,
  "resolution": "1080x1920",
  "scenes": [
    {
      "frame_number": 1,
      "timestamp": "0:00-0:03",
      "duration": 3.0,
      "narration": "Texto extraído del STT",
      "text_overlay": {
        "text": "Subtítulo en pantalla",
        "position": "center",
        "style": "bold",
        "color": "#FFFFFF",
        "has_stroke": true
      },
      "visual": {
        "shot_type": "close_up | medium | wide | overhead",
        "subject": "Persona sosteniendo un producto",
        "transition_to_next": "cut | fade | swipe"
      },
      "motion_type": "i2v",
      "energy": "high | medium | low"
    }
  ],
  "summary": {
    "total_scenes": 8,
    "avg_scene_duration": 4.1,
    "full_transcript": "...",
    "category": "tutorial",
    "caption_style": "Texto blanco negrita, trazo negro, centro inferior de pantalla",
    "structure": "gancho -> problema -> solución -> demostración -> CTA",
    "pacing": "fast | medium | slow",
    "key_techniques": ["técnica1", "técnica2"]
  }
}
```

## Uso

### 1. Análisis Individual
```bash
python analyze_video.py --url "URL"
```

### 2. Análisis por Lotes (Múltiples URLs)
```bash
python analyze_video.py --urls-file urls.txt --output output/templates/
```

### 3. Acumulación de Playbook (Habilidad Separada)
Pase los resultados de análisis template.json a la habilidad `video-playbook` para acumular conocimientos por tipo:
```bash
python skills/video-playbook/scripts/manage_playbook.py --add -t output/templates/template.json
```

### 4. Generar Nuevo Video desde Plantilla
Pase los resultados de análisis template.json al storyboard-generator para recrear con su propio contenido:
```bash
python generate_storyboard.py --template output/templates/template.json --topic "Nombre de su producto"
```

## Dependencias
- yt-dlp (`.bin/yt-dlp`)
- ffmpeg (`.bin/ffmpeg`)
- OpenAI Whisper API (STT)
- Gemini Vision API (Análisis de fotogramas)

## Variables de Entorno
- `OPENAI_API_KEY` -- Para Whisper STT
- `GEMINI_API_KEY` -- Para análisis de Vision

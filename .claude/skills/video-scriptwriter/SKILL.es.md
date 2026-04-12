---
name: video-scriptwriter
description: "Habilidad de generación automática de guiones de video para TikTok/YouTube. Especifique un tema + formato + duración para generar scenes.json (compatible con storyboard/audio/editor). Referencia automáticamente los conocimientos del Playbook para una estructura óptima. Se activa con 'Crear un guión', 'Generar guión', 'Crear un plan', etc."
triggers:
  - Crear un guión de video
  - Generar guión
  - Crear un plan de video
  - Guión para TikTok
  - Generar scenes.json
  - video-scriptwriter
  - Propuesta de estructura de video
---

# Guionista de Video

Genera automáticamente tema -> plan -> scenes.json.

## 6 Formatos

| Formato | Descripción | Aptitud para Producción Masiva |
|---------|-------------|-------------------------------|
| `split_screen_teaching` | Mitad superior texto+TTS / mitad inferior metraje de gameplay | 5/5 |
| `ranking_list` | Formato ranking TOP 5 | 4/5 |
| `reddit_story` | Lectura de Reddit/2ch + video de fondo | 5/5 |
| `dark_facts` | Formato de trivia "Cosas aterradoras que no sabías sobre X" | 4/5 |
| `standard_teaching` | Formato educativo/explicativo estándar | 4/5 |
| `product_intro` | Formato de introducción/reseña de producto | 3/5 |

## Inicio Rápido

```bash
# Básico
python3 skills/video-scriptwriter/scripts/generate_script.py \
  --topic "5 formas de mejorar la calidad del sueño" \
  --format ranking_list \
  --duration 30s

# Educativo en pantalla dividida
python3 skills/video-scriptwriter/scripts/generate_script.py \
  --topic "Qué es la computación cuántica" \
  --format split_screen_teaching \
  --duration 30s \
  --hook shocking

# Listar formatos
python3 skills/video-scriptwriter/scripts/generate_script.py --list-formats
```

## Opciones

| Opción | Predeterminado | Descripción |
|--------|----------------|-------------|
| `--topic` | (requerido) | Tema/tópico del video |
| `--format` | standard_teaching | Formato |
| `--duration` | 30s | Duración del video (15s/30s/60s) |
| `--language` | ja | Idioma |
| `--hook` | question | Estilo de gancho (question/shocking/pov/wait/ranking/dark/nobody/comparison) |
| `--output` | auto | Directorio de salida |
| `--instructions` | - | Texto de instrucciones adicionales |

## Salida: scenes.json

Formato compatible con storyboard-generator / video-audio / video-editor:

```json
{
  "title": "Título del video",
  "format": "split_screen_teaching",
  "scenes": [
    {
      "frame_number": 1,
      "timestamp": "0:00-0:03",
      "duration": 3.0,
      "scene_type": "hook",
      "narration": "Narración",
      "text_overlay": { "main_text": "Subtítulo" },
      "visual_prompt": "Prompt en inglés para generación de imagen...",
      "motion_type": "i2v"
    }
  ],
  "metadata": {
    "target_audience": "...",
    "estimated_retention_hooks": ["técnica de gancho", "divulgación progresiva de información"]
  }
}
```

## Integración de Pipeline

```
scriptwriter (tema -> scenes.json)
  |
storyboard-generator (scenes.json -> imágenes con IA)
  |
video-audio (scenes.json -> audio TTS)
  |
video-editor (imágenes + audio -> video final)
```

## Integración con Playbook

Referencia automáticamente los conocimientos acumulados en `video-playbook`:
- Duración promedio de escena, ritmo
- Patrones de estructura
- Estilo de subtítulos
- Técnicas efectivas

## Dependencias
- Gemini API (`GEMINI_API_KEY`)
- video-playbook (opcional, para referencia de conocimientos)

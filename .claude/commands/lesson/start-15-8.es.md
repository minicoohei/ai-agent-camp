---
description: "When the user says /start-15-8 — Module 15 Lesson 15-8: Clipper x Remotion para generación automática de materiales de marketing"
chapter: "courses/aiagent/lesson03-core/module15-video/chapter.yaml"
duration: 45 min
prerequisites: ["start-15-7"]
level: intermediate
tags: ["video", "remotion", "marketing", "sns"]
---

# Lección 15-8: Clipper x Remotion -- Generación Automática de Materiales de Marketing

## Objetivos de Aprendizaje

Aprenda a convertir los clips extraidos en la Lección 15-7 en materiales de marketing para redes sociales usando Remotion.

1. Concepto básico de Remotion (React + video = video programable)
2. Comprender las plantillas (ShortClip, QuoteClip, SummaryVideo)
3. Conversión de clips a videos para publicación en redes sociales
4. Salida simultanea en multiples formatos
5. Personalización con la marca CursorBootcamp

---

## Qué es Remotion?

Remotion es un framework para **crear videos programables con React**.

- Defina el diseño del video con HTML y CSS
- Controle las animaciones con componentes React
- Renderizado local con FFmpeg (sin API, costo $0)
- Una vez creada la plantilla, puede producir en masa cambiando solo los datos

---

## Paso 1: Ejecución del Pipeline Integrado

Combine con Clipper de la Lección 15-7 para una ejecución de extremo a extremo:

```bash
uv run python tools/ugc/clipper_marketing_pipeline.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --auto-select "score>0.8" \
  --batch-render short,quote
```

Esto realiza:
1. Descarga de video -> Análisis con IA -> Extracción de momentos destacados
2. Renderizado de cada clip en formatos "short(9:16)" y "quote(16:9)"
3. Generación automática de borradores de publicación para redes sociales (texto + hashtags)

---

## Paso 2: Comprender los Tipos de Plantillas

Lista de plantillas disponibles:

```bash
uv run python tools/ugc/remotion_render.py --list-templates
```

| Plantilla | Tamaño | Uso |
|-----------|--------|-----|
| `short` | 1080x1920 (9:16) | TikTok / Reels / Shorts |
| `quote` | 1920x1080 (16:9) | Twitter/X / LinkedIn |
| `summary` | 1920x1080 (16:9) | YouTube / Blog |
| `blog` | 1920x1080 (16:9) | Incrustación en blog |
| `training` | 1920x1080 (16:9) | Material de capacitación |
| `square` | 1080x1080 (1:1) | Feed de Instagram |

---

## Paso 3: Renderizado Individual

Renderice un clip específico con una plantilla específica:

```bash
uv run python tools/ugc/remotion_render.py \
  --input output/clips/SESSION_DIR/remotion_input.json \
  --template short \
  --clip-id clip_01
```

---

## Paso 4: Renderizado por Lotes

Genere todos los formatos de un solo clip en una sola ejecución:

```bash
uv run python tools/ugc/remotion_render.py \
  --input output/clips/SESSION_DIR/remotion_input.json \
  --batch short,quote,summary,square
```

---

## Paso 5: Verificar Borradores de Publicación para Redes Sociales

Revise el `post_drafts.json` generado después de la ejecución del pipeline:

```bash
cat output/clips/SESSION_DIR/post_drafts.json | python3 -m json.tool
```

Contiene texto, hashtags y rutas de video para cada plataforma.

---

## Ejercicios

1. **Básico**: Seleccione 3 momentos destacados de un video de su elección y genere videos cortos (9:16)
2. **Aplicado**: Genere 3 tipos simultaneamente (short, quote, square) del mismo clip
3. **Avanzado**: Usando el post_drafts.json generado, complete un texto de publicación real para redes sociales

---

## Referencia de Costos

| Proceso | Costo |
|---------|-------|
| Clipper (descarga + análisis + traducción) | ~$0.035/video |
| Renderizado con Remotion | $0 (local) |
| **Total** | **~$0.035/video** |

---

## Resumen

- YouTube Clipper detecta automáticamente las "mejores partes" de un video con IA
- Remotion las inyecta en plantillas para producir materiales para redes sociales en masa
- Genere materiales para multiples plataformas simultaneamente a partir de un solo video
- El costo es practicamente cero (Gemini API ~$0.035 + renderizado local)

---

## Vista Previa de Entregables

### Salida esperada
```text
output/ugc/
  *.mp4           (archivos de video)
  metadata.json   (metadatos)
  thumbnails/     (miniaturas)
```

### Comandos de verificación
```bash
# Lista y tamano de archivos de salida
ls -lh output/ugc/

# Verificar metadatos
cat output/ugc/*metadata*.json 2>/dev/null | head -20

# Reproducir video (macOS: open / Linux: xdg-open)
open output/ugc/*.mp4
```

---

## Siguientes Pasos

Esto completa el Module 15 (Producción de Video).

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente accion",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-16-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

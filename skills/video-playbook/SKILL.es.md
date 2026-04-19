---
name: video-playbook
description: "Habilidad para acumular y utilizar conocimientos en Playbooks por tipo a partir de resultados de análisis de video. Usa la salida template.json del video-analyzer como entrada. Se activa con 'Actualizar Playbook', 'Conocimientos por tipo de video', 'Verificar Playbook', etc."
triggers:
  - Actualizar Playbook
  - Conocimientos por tipo de video
  - Verificar Playbook
  - Directrices de producción de video
  - Acumular resultados de análisis
  - video-playbook
---

# Video Playbook

Determina el tipo de video a partir de resultados de análisis (template.json) y acumula conocimientos de producción en Playbooks específicos por tipo.

## Tipos de Video (7 tipos)

| Tipo | Descripción |
|------|-------------|
| `intro` | Introducción/Reseña (intro de producto, intro de servicio, intro de persona) |
| `teaching` | Enseñanza/Explicación (cómo hacer, compartir conocimiento, consejos, know-how) |
| `template` | Plantilla/Tendencia (formatos de moda, sincronización de sonido, desafíos) |
| `meme` | Meme/Comedia (enfocado en remate, humor, parodia) |
| `dance` | Baile/Actuación (coreografía, sincronización BPM, covers) |
| `mv` | MV/Cinemático (video musical, efectos intensivos, producción cinematográfica) |
| `clip` | Clip/Destacado (largo a corto, mejores momentos, clips de streaming) |

## Inicio Rápido

```bash
# Agregar conocimientos al Playbook después de analizar con video-analyzer
python skills/video-playbook/scripts/manage_playbook.py \
  --add -t output/templates/video_001/template.json

# Listar Playbooks por tipo
python skills/video-playbook/scripts/manage_playbook.py --list

# Mostrar Playbook para tipo específico
python skills/video-playbook/scripts/manage_playbook.py --show teaching

# Exportar en formato Markdown
python skills/video-playbook/scripts/manage_playbook.py --export teaching
```

## Flujo de Trabajo

```
1. Analizar video con video-analyzer -> template.json
2. manage_playbook.py --add -t template.json
   -> Detección automática del tipo de video
   -> Extracción de conocimientos sobre timing, estructura, subtítulos, etc.
   -> Agregar al JSON de playbook por tipo
   -> Actualización automática de datos agregados
3. manage_playbook.py --show TIPO para revisar conocimientos acumulados
4. Consultar Playbook al crear nuevos videos
```

## Cómo Funciona la Acumulación del Playbook

Los siguientes conocimientos se extraen de cada resultado de análisis y se acumulan por tipo:

- **Timing**: Duración promedio de escena, ritmo, longitud del gancho
- **Estructura**: Patrones de composición (gancho->problema->solución, etc.), técnicas utilizadas
- **Subtítulos**: Estilo, ubicación, color, densidad
- **Visual**: Tipos de toma, variedad, resolución
- **Audio**: Presencia de narración, densidad, caracteres por escena

A medida que se acumulan más muestras, los datos agregados se vuelven más precisos, y las directrices de producción sobre "cómo hacer este tipo de video" se generan automáticamente.

## Aprovechamiento para Creación de Contenido

Al crear nuevos videos usando los conocimientos del Playbook:

1. Use `--show TIPO` para revisar conocimientos del tipo objetivo
2. Use `--export TIPO` para generar un resumen en Markdown
3. Incluya el resumen en prompts de LLM para generar guiones y propuestas de estructura
4. Refleje los conocimientos del Playbook en storyboard-generator

## Ubicación de Almacenamiento de Datos

```
skills/video-playbook/playbooks/
  +-- teaching.json    # Conocimientos de enseñanza
  +-- intro.json       # Conocimientos de introducción
  +-- meme.json        # Conocimientos de meme
  +-- ...
```

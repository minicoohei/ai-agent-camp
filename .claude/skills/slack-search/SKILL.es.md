---
name: slack-search
description: "Habilidad para búsqueda semántica de canales y mensajes de Slack. Se activa con solicitudes como 'Buscar en Slack', 'Encontrar canales', 'Buscar mensajes'."
triggers:
  - Buscar en Slack
  - Encontrar canales
  - Buscar mensajes
  - Canales relacionados
  - Buscar eventos
  - slack-search
  - Slack search
---

# Habilidad de búsqueda en Slack

Búsqueda semántica de Slack utilizando indexación jerárquica basada en BookRAG.

## Inicio rápido

```python
import sys
from pathlib import Path
# Agregar directorio tools/ de la raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools"))
from slack_search import SlackSearch

search = SlackSearch()

# Resumen del workspace
overview = search.get_workspace_overview()

# Búsqueda de canales (búsqueda semántica)
results = search.find_channels("exhibición DX")

# Detalles del canal
detail = search.get_channel_detail("my-workspace/example-channel")

# Exploración de canales relacionados
related = search.find_related_channels("my-workspace/example-channel")

# Búsqueda de personas
persons = search.find_person("Shimizu")

# Búsqueda de eventos
events = search.find_events("DX")

# Búsqueda por línea de tiempo
timeline = search.get_timeline("2025-12-01", "2025-12-31")
```

## Funciones de búsqueda disponibles

### 1. Resumen del workspace (`get_workspace_overview`)
Obtener estadísticas generales y estructura de categorías.

### 2. Búsqueda de canales (`find_channels`)
Búsqueda semántica en nombres de canales, temas y resúmenes.

### 3. Detalles del canal (`get_channel_detail`)
Obtener información detallada de un canal específico incluyendo resumen, temas, participantes, período de actividad, rutas de archivos y canales relacionados.

### 4. Exploración de canales relacionados (`find_related_channels`)
Explorar canales relacionados basándose en estructura de grafo. Soporta parámetro de profundidad para relaciones indirectas.

### 5. Búsqueda de personas (`find_person`)
Buscar personas por nombre de emisor o menciones. Devuelve nombre, alias, cantidad de canales y lista de canales.

### 6. Búsqueda de eventos (`find_events`)
Buscar exhibiciones, reuniones y otros eventos.

### 7. Listado por categoría (`list_channels_by_category`)
Listar canales por categoría (cafe, project, product, sales, notify, partner, event, external).

### 8. Búsqueda por línea de tiempo (`get_timeline`)
Buscar actividad por rango de fechas.

### 9. Fuentes de salida (`get_output_sources`)
Estadísticas para salidas de calendario, gmail, drive y notas de voz.

## Comandos CLI

```bash
# Resumen del workspace
uv run python tools/slack_search.py overview [workspace]

# Búsqueda de canales
uv run python tools/slack_search.py find "consulta"

# Detalles del canal
uv run python tools/slack_search.py detail "channel_id"

# Canales relacionados
uv run python tools/slack_search.py related "channel_id"

# Búsqueda de personas
uv run python tools/slack_search.py person "nombre"

# Búsqueda de eventos
uv run python tools/slack_search.py events [consulta]

# Por categoría
uv run python tools/slack_search.py category "nombre_categoría"

# Línea de tiempo
uv run python tools/slack_search.py timeline "fecha_inicio" "fecha_fin"
```

## Actualización del índice

El índice se actualiza automáticamente a diario mediante GitHub Actions.
Actualización manual:

```bash
python3 slack-sync/scripts/build_book_index.py
```

## Descripción general

Habilidad que utiliza indexación jerárquica basada en BookRAG para búsqueda semántica de canales y mensajes de Slack. Soporta búsqueda de canales, búsqueda de personas, búsqueda de eventos y búsqueda por línea de tiempo.

## Solución de problemas

| Error | Solución |
|-------|----------|
| Index file not found | Reconstruya el índice con `python3 slack-sync/scripts/build_book_index.py` |
| No results found | Cambie las palabras clave de la consulta o verifique las categorías disponibles con `get_workspace_overview()` |

## Criterios de éxito

- [ ] Se devuelven canales o mensajes relacionados para la consulta de búsqueda
- [ ] Los resultados de búsqueda incluyen nombre del canal, resumen y relevancia
- [ ] Se completa sin errores

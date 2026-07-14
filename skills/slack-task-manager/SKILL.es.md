---
name: slack-task-manager
description: "Sub-agente para búsqueda en Slack, extracción de TODOs y gestión de tareas. Extrae tareas de múltiples fuentes de datos y las prioriza. Se activa con solicitudes como 'Buscar en Slack', 'Extraer tareas', 'Verificar TODOs', 'Verificar menciones'."
triggers:
  - Buscar en Slack
  - Búsqueda en Slack
  - Encontrar canales
  - Verificar menciones
  - Extraer TODOs
  - Extraer tareas
  - Lista de tareas
  - Tareas pendientes
  - Solicitudes
---

# Sub-agente de Slack/Gestión de tareas

Sub-agente que ejecuta búsqueda en Slack, extracción de TODOs y gestión de tareas en un contexto dedicado.

## Propósito

Separa los datos de Slack y la gestión de tareas del contexto del agente principal para:
- Buscar eficientemente grandes volúmenes de mensajes de Slack
- Integrar la extracción de tareas de múltiples fuentes de datos
- Devolver solo resúmenes de resultados de búsqueda

## Lista de funcionalidades

| Funcionalidad | Script | Descripción |
|---------------|--------|-------------|
| Búsqueda en Slack | `slack_search.py` | Búsqueda semántica basada en BookRAG |
| Extracción de TODOs | `extract_todos.py` | Extracción de TODOs de menciones con determinación de estado |
| Extracción de tareas | `extract_tasks.py` | Extracción de tareas de múltiples fuentes |

## 1. Búsqueda en Slack (`tools/slack_search.py`)

Búsqueda semántica utilizando indexación jerárquica basada en BookRAG.

### Funcionalidades

| Método | Descripción |
|--------|-------------|
| `get_workspace_overview()` | Resumen del workspace |
| `find_channels(query)` | Búsqueda de canales |
| `get_channel_detail(channel_id)` | Detalles del canal |
| `find_related_channels(channel_id)` | Búsqueda de canales relacionados |
| `find_person(name)` | Búsqueda de personas |

## 2. Extracción de TODOs (`skills/slack-todo-extractor/scripts/extract_todos.py`)

Extrae tareas de menciones en Slack y determina su estado.

### Uso

```bash
# Básico (basado en palabras clave)
python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "SuNombre,su-usuario" \
  --period "2026-01-06:2026-01-08"

# Basado en LLM (alta precisión, requiere GEMINI_API_KEY)
python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "SuNombre,su-usuario" \
  --period "1/6:8" \
  --use-llm

# Salida JSON
python skills/slack-todo-extractor/scripts/extract_todos.py \
  -u "SuNombre" -p "1/6:8" --use-llm -o json
```

### Determinación de estado

| Estado | Condición |
|--------|-----------|
| Completado | El usuario objetivo respondió "hecho" etc. / El solicitante respondió "gracias" etc. |
| En progreso | El usuario objetivo respondió "entendido", "lo haré" etc. |
| Pendiente | Sin respuesta |

## 3. Extracción de tareas (`tools/extract_tasks.py`)

Extrae y prioriza automáticamente tareas de múltiples fuentes de datos.

### Fuentes de datos

| Fuente | Descripción |
|--------|-------------|
| Git | Archivos modificados, trabajo sin confirmar |
| Activity Logger | Actividad reciente |
| SpecStory | Tareas en progreso |
| Slack-sync | Solicitudes, menciones |
| Output | Calendario, Gmail, notas de voz |
| Notion | Bases de datos/páginas |

### Uso

```bash
# Extraer tareas de todas las fuentes
uv run python tools/extract_tasks.py

# Solo fuentes específicas
uv run python tools/extract_tasks.py --sources git,slack

# Con generación de HowToDo
uv run python tools/extract_tasks.py --with-howtodo

# Salida HTML
uv run python tools/extract_tasks.py --format html --output tasks.html
```

## Prerrequisitos

- La sincronización de Slack en `slack-sync/` debe estar completada
- Las respuestas en hilos requieren sincronización previa si es necesario

```bash
# Sincronización de Slack
python data/slack-sync/scripts/fetch_slack.py --workspace my-workspace

# También obtener respuestas en hilos
python data/slack-sync/scripts/fetch_slack.py --workspace my-workspace --refresh-threads
```

## Dependencias

```txt
python-dotenv>=1.0.0
google-generativeai>=0.3.0  # Al usar modo LLM
```

## Variables de entorno

```bash
# Al usar modo LLM
GEMINI_API_KEY=su_clave_api

# Al usar integración con Notion
NOTION_TOKEN=su_token
```

## Casos de uso

1. **Búsqueda de canales**: Encontrar canales relacionados con proyectos
2. **Verificación de TODOs**: Extraer tareas de menciones dirigidas a usted
3. **Integración de tareas**: Listar tareas de múltiples fuentes
4. **Priorización**: Organizar tareas por fecha límite e importancia

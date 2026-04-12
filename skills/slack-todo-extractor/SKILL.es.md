---
name: slack-todo-extractor
description: "Habilidad que busca datos sincronizados de Slack para menciones y extrae TODOs/tareas con determinación de estado. Se activa con solicitudes como 'Extraer tareas de Slack', 'Verificar TODOs', 'Verificar menciones'."
triggers:
  - Extraer tareas de Slack
  - Verificar TODOs
  - Verificar menciones
  - Tareas para mí
  - Tareas pendientes de Slack
  - slack-todo-extractor
  - Slack TODO
---

# Habilidad de extracción de TODOs de Slack

## Descripción general

Habilidad que busca en los datos sincronizados de Slack (`slack-sync/data/`) menciones dirigidas a un usuario específico, y extrae TODOs/tareas con determinación de estado incluyendo respuestas en hilos.

## Inicio rápido

```bash
# Básico (basado en palabras clave)
uv run python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "SuNombre,su-usuario" \
  --period "2026-01-06:2026-01-08"

# Basado en LLM (alta precisión, requiere GEMINI_API_KEY)
uv run python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "SuNombre,su-usuario" \
  --period "1/6:8" \
  --use-llm
```

## Parámetros de entrada

| Parámetro | Requerido | Descripción | Ejemplo |
|-----------|-----------|-------------|---------|
| `--users`, `-u` | Sí | Nombres de usuario objetivo (separados por coma) | `SuNombre, su-usuario` |
| `--period`, `-p` | Sí | Período de búsqueda | `2026-01-06:2026-01-08` o `1/6:8` |
| `--workspace`, `-w` | No | Workspace (todos si se omite) | `my-workspace`, `my-workspace-2` |
| `--use-llm` | No | Usar LLM (Gemini 2.0 Flash) para determinación | - |
| `--output`, `-o` | No | Formato de salida | `markdown` (por defecto) o `json` |

## Flujo de procesamiento

### Paso 1: Búsqueda de menciones
Buscar en `slack-sync/data/{workspace}/*.md` mensajes que contengan `@nombre_usuario`

### Paso 2: Verificación de respuestas en hilos
Para cada mención:
- Extraer respuestas en hilos (formato `> ####`)
- Verificar mensajes posteriores del canal en el mismo día

### Paso 3: Determinación de estado

#### Basado en palabras clave (sin `--use-llm`)
| Condición | Estado |
|-----------|--------|
| El usuario objetivo respondió "hecho", "completado" etc. | completado |
| El solicitante respondió "gracias", "lo verificaré" etc. | completado |
| El usuario objetivo respondió "entendido", "lo haré" etc. | en_progreso |
| Sin respuesta | pendiente |

#### Basado en LLM (con `--use-llm`)
Gemini 2.0 Flash comprende el contexto:
- "Entendido" es aceptación, no finalización
- Si se establece una fecha límite, el estado es en_progreso antes de esa fecha
- La respuesta de confirmación del solicitante determina la finalización

## Configuración del entorno

### GEMINI_API_KEY (al usar modo LLM)

Almacenar en Credential Store:
```bash
uv run python tools/credential_manager.py store GEMINI_API_KEY
```

## Prerrequisitos

- La sincronización de Slack en `slack-sync/` debe estar completada (consulte `data/slack-sync/`)

## Habilidades relacionadas

- `slack-search`: Búsqueda de texto completo en mensajes de Slack
- `slack-task-manager`: Gestión integrada de tareas

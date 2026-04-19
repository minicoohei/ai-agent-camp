---
description: "Verificar finalización y pasar a la siguiente lección"
---

# /next_lesson

## ✅ Verificación de finalización y siguiente lección
Verificar el estado de finalización y guiar automáticamente a la siguiente lección.

Puede elegir cómo proceder usando AskUserQuestion (AskQuestion).

**Ejemplo de AskQuestion:**
```json
{
  "title": "Pasar a la siguiente lección",
  "questions": [{
    "id": "next_action",
    "prompt": "¿Qué desea hacer?",
    "options": [
      {"id": "check_next", "label": "Verificar finalización y continuar"},
      {"id": "mark_done", "label": "Marcar manualmente como completa y continuar"},
      {"id": "list_lessons", "label": "Ver lista de lecciones"}
    ]
  }]
}
```

## Acciones

### 1) Verificar finalización y continuar
```
uv run python tools/lesson_progress.py --next
```

### 2) Marcar manualmente como completa y continuar
```
uv run python tools/lesson_progress.py --mark <id-de-lección-actual>
uv run python tools/lesson_progress.py --next
```
> Reemplace `<id-de-lección-actual>` con la lección que acaba de completar (ej.: `start-1-1`, `start-3-2`).

### 3) Ver lista de lecciones
```
uv run python tools/lesson_progress.py --list
```

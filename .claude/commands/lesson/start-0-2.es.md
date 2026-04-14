---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch02-extensions"
duration: "~5 min"
prerequisites: ["Lección 0-1 completada"]
level: "beginner"
tags: ["setup", "extensions"]
---

# Lección 0-2: Instalación de extensiones

## Verificar progreso de configuración

**Ejecución automática por IA:** Ejecute `uv run python tools/setup_progress.py show` para mostrar el progreso actual de la configuración.

---

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Verificar e instalar las extensiones necesarias para el desarrollo de agentes de IA y mejorar la eficiencia del desarrollo |
| Duración | ~5 min |
| Requisitos previos | Lección 0-1 completada (Cursor funciona correctamente) |
| Página del curso | Consulte [Página principal del curso](https://ai-agent.camp/es/course/module-0) en paralelo |

> **Consejo**: Si la IA deja de responder, escriba "por favor continua" o "se detuvo" para reanudar.

---

## Instalación automática de extensiones

En esta lección, solo ejecute `/setup-extensions` y habrá terminado.
**No se requieren operaciones de terminal. La IA se encarga de todo automáticamente.**

### Lo que la IA hace automáticamente

1. Verificar las extensiones actualmente instaladas
2. Identificar extensiones obligatorias faltantes (Python, Marp, Draw.io, PlantUML, etc.)
3. Instalar automáticamente las faltantes
4. Mostrar un informe de resultados de instalación

**Configuración de AskQuestion:**
```json
{
  "title": "Configuracion de extensiones",
  "questions": [{
    "id": "action",
    "prompt": "Desea iniciar la instalacion automatica de extensiones?",
    "options": [
      {"id": "run", "label": "Iniciar instalacion automatica (ejecutar /setup-extensions)"},
      {"id": "already_done", "label": "Ya estan instaladas"},
      {"id": "view_html", "label": "Ver la pagina del curso primero"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(run -> Ejecutar el contenido de `/setup-extensions`)
(already_done -> Ir al punto de verificación)
(view_html -> Proporcionar la URL de la página del curso)
(different_lesson -> Mostrar lista de modulos)

---

## Comandos a ejecutar

```text
/setup-extensions
```

## Ejemplo de salida esperada

```text
Resultados de verificacion de extensiones:
- Marp for VS Code: Ya instalada ✓
- Draw.io Integration: Recien instalada ✓
- PlantUML: Recien instalada ✓
Todas las extensiones obligatorias estan listas!
```

## Solución de problemas comunes
- La instalación no avanza -> Reinicie Cursor y vuelva a ejecutar
- `cursor --list-extensions` no encontrado -> Instale manualmente desde la Paleta de Comandos

---

## Lista de Extensión ID

| Extensión | Extensión ID | Obligatoria/Recomendada |
|-----------|-------------|------------------------|
| Python | ms-python.python | Obligatoria |
| Marp | marp-team.marp-vscode | Recomendada |
| Draw.io | hediet.vscode-drawio | Recomendada |
| PlantUML | jebbs.plantuml | Recomendada |

## Punto de verificación
- [ ] La extensión Python está instalada
- [ ] La extensión Marp está instalada
- [ ] La extensión Draw.io está instalada
- [ ] La extensión PlantUML está instalada
- [ ] El resaltado de sintaxis funciona correctamente

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next", "label": "Configurar Gemini API (/start-0-3)"},
      {"id": "check", "label": "Verificar el entorno (/check-setup)"},
      {"id": "back", "label": "Volver a la verificacion del entorno (/start-0-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

(next -> Guiar a /start-0-3)
(check -> Ejecutar el contenido de /check-setup)
(back -> Guiar a /start-0-1)
(finish -> Fin)

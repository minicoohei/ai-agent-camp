---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "~5 min"
prerequisites: ["start-0-1", "start-0-2", "start-0-3", "start-0-4"]
level: "beginner"
tags: ["setup", "security"]
---

# Lección 0-5: Verificación de configuración de seguridad

## Verificar progreso de configuración

**Ejecución automática por IA:** Ejecute `uv run python tools/setup_progress.py show` para mostrar el progreso actual de la configuración.

---

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Configurar .gitignore y hooks de pre-commit para prevenir la filtración de claves API. Completar el Módulo 0 de forma segura |
| Duración | ~5 min |
| Requisitos previos | Lección 0-1 a Lección 0-4 completadas; claves API configuradas en .env |
| Página del curso | Consulte [Página principal del curso](https://ai-agent.camp/es/course/module-0) en paralelo |

> **Consejo**: Si la IA deja de responder, escriba "por favor continua" o "se detuvo" para reanudar.

---

## Configuración automática de seguridad

En esta lección, solo ejecute `/setup-security` y habrá terminado.
**No se requieren operaciones de terminal. La IA se encarga de todo automáticamente.**

### Lo que la IA hace automáticamente

1. Verificar `.gitignore` y agregar automáticamente entradas faltantes (.env, credentials/, *.key, *.pem, etc.)
2. Configurar automáticamente hooks de `pre-commit` (bloquear commits accidentales de archivos .env)
3. Ejecutar una verificación de seguridad actual (verificar que .env no este rastreado por Git, ni haya sido commiteado anteriormente)
4. Si se encuentran problemas, sugerir correcciones automáticas

**Configuración de AskQuestion:**
```json
{
  "title": "Configuracion de seguridad",
  "questions": [{
    "id": "action",
    "prompt": "Desea iniciar la configuracion de seguridad?",
    "options": [
      {"id": "run", "label": "Iniciar configuracion automatica (ejecutar /setup-security)"},
      {"id": "already_done", "label": "La seguridad ya esta configurada"},
      {"id": "more_info", "label": "Por que es necesaria la configuracion de seguridad?"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(run -> Ejecutar el contenido de `/setup-security`)
(already_done -> Ir a la verificación de finalización)
(more_info -> Explicar: "Si las claves API se exponen en GitHub, existe riesgo de uso no autorizado y cargos elevados. Este comando configura automáticamente medidas preventivas." Luego volver a preguntar.)
(different_lesson -> Mostrar lista de modulos)

---

## Comandos a ejecutar

```text
/setup-security
```

## Ejemplo de salida esperada

```text
Configuracion de seguridad completada:
- .gitignore: Se agregaron .env, credentials/, *.key, *.pem ✓
- Hook de pre-commit: Configurado ✓
- Archivo .env: No rastreado por Git ✓
```

## Solución de problemas comunes
- El hook de pre-commit bloquea un commit -> Pida a la IA que "verifique el contenido del commit"
- .env está rastreado por Git -> Pida a la IA que "elimine .env del rastreo de Git"

---

## Punto de verificación
- [ ] .gitignore incluye .env
- [ ] .gitignore incluye credentials/
- [ ] El hook de pre-commit está configurado
- [ ] El archivo .env no está rastreado por Git
- [ ] El historial de Git no contiene información confidencial

---

## Módulo 0 completado!

Una vez que la configuración de seguridad esté completa, el Módulo 0 estará totalmente terminado.

Como verificación final, ejecute `/check-setup` para mostrar un informe de todos los elementos.

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Modulo 0 completado! Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Felicitaciones! El Modulo 0 esta completo. Que desea hacer a continuacion?",
    "options": [
      {"id": "start_lesson", "label": "Comenzar la primera leccion (/start-1-1: Generacion de banners)"},
      {"id": "final_check", "label": "Ejecutar verificacion final (/check-setup)"},
      {"id": "overview", "label": "Revisar la vista general del proyecto (/overview)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

(start_lesson -> Guiar a /start-1-1)
(final_check -> Ejecutar el contenido de /check-setup)
(overview -> Guiar a /overview)
(finish -> Mostrar "Excelente trabajo! Puede comenzar la primera lección en cualquier momento con /start-1-1")

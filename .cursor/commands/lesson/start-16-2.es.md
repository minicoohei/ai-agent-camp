---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "30 min"
prerequisites: ["start-16-1"]
level: "beginner"
tags: ["email", "gmail", "check-inbox", "task-extraction"]
nonInteractiveMode: deferred
---
# Lección 16-2: Análisis de Correos Recibidos y Extracción de Tareas

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 16-2: Análisis de Correos Recibidos y Extracción de Tareas**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Extraer TODOs de correos, determinar prioridad y generar borradores de respuesta con la habilidad check-inbox |
| Duración | ~30 min |
| Habilidades utilizadas | check-inbox |
| Requisitos previos | Lección 16-1 completada (gogcli autenticado), clave API de Gemini configurada |
| Página del curso | Consulte [Module 16: Automatización de Correo](https://ai-agent.camp/es/course/module-16) en paralelo |

**Flujo de la sesión:**
1. Comprender el funcionamiento de check-inbox
2. Preparar los datos de correo (sincronización con google-sync)
3. Ejecutar el análisis de correo con check-inbox
4. Verificar la lista de tareas priorizadas y los borradores de respuesta

> **Consejo**: Si la respuesta de la IA se detiene a mitad, escriba "por favor continue" para reanudar.

---

## Verificación de Preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "previous_lesson", "label": "Quiero hacer la leccion 16-1 primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra leccion"}
    ]
  }]
}
```

---

## Paso 1: Comprender el Funcionamiento de check-inbox

check-inbox funciona con el siguiente flujo:

```text
Sincronizar correos con google-sync -> Guardar como archivos Markdown
    |
check-inbox lee los archivos locales
    |
Analizar contenido con Gemini API
    |
Determinacion de prioridad + generacion de borradores de respuesta
```

**Punto clave:**
- No consulta la API de Gmail en tiempo real, sino que analiza datos locales sincronizados previamente
- Determinación rápida de contexto con Gemini 3.0 Flash

---

## Paso 2: Preparar los Datos de Correo

**Verificar la existencia de datos:**
```bash
ls output/gmail/ 2>/dev/null && echo "Datos disponibles" || echo "Sin datos"
```

Si no hay datos, exporte directamente con gogcli:
```bash
gog gmail search "is:inbox newer_than:7d" --account <su-email@gmail.com> --max 20 --format json
```

---

## Paso 3: Ejecutar el Análisis de Correo con check-inbox

**Ejecute el siguiente prompt en Cursor / Claude Code:**
```text
Revise la bandeja de entrada y liste los correos que requieren respuesta.
Asigne prioridades y cree borradores de respuesta.
```

**Salida esperada:**
- Lista de correos que requieren respuesta (con prioridad)
- Resumen de cada correo
- Propuestas de borradores de respuesta

---

## Paso 4: Verificar y Utilizar los Resultados

**Configuración de AskQuestion:**
```json
{
  "title": "Uso de los resultados del analisis",
  "questions": [{
    "id": "usage",
    "prompt": "Como desea utilizar los resultados del analisis?",
    "options": [
      {"id": "reply", "label": "Quiero usar los borradores para responder correos -> Ir a 16-3"},
      {"id": "review", "label": "Quiero verificar y organizar la lista de tareas"},
      {"id": "retry", "label": "Quiero re-analizar con un filtro diferente"},
      {"id": "next", "label": "Quiero avanzar a la siguiente leccion"}
    ]
  }]
}
```

---

## Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| Error de `GEMINI_API_KEY` | Configure la clave API de Gemini en `.env` o ejecute `/setup-gemini` |
| Datos de correo no encontrados | Verifique la existencia del directorio `output/gmail/` |
| Los resultados del análisis están vacios | Verifique el formato de los datos de correo (Markdown + YAML front matter) |

---

## Punto de Control

- [ ] El análisis de correo con check-inbox se ejecuto correctamente
- [ ] Se género una lista de tareas priorizadas
- [ ] Se propusieron borradores de respuesta

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Leccion 16-2 completada!",
  "questions": [{
    "id": "next_action",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_lesson", "label": "Ir a 16-3 -> Envio de correo con gogcli"},
      {"id": "practice", "label": "Quiero probar mas analisis"},
      {"id": "review", "label": "Revisar la descripcion general del Module 16"},
      {"id": "end", "label": "Terminar por hoy"}
    ]
  }]
}
```

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-14-4"]
level: "intermediate"
tags: ["article", "proofreading"]
---

# 🎓 Lección 14-5: Corrección - Revisión con agente de corrección

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 14-5: Corrección - Revisión con agente de corrección**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Revisar el artículo desde 5 perspectivas usando el agente de corrección y aplicar las correcciones |
| Duración | ~30 min |
| Habilidades utilizadas | proofreading-agent |
| Requisitos previos | Clave API de Gemini configurada, Lección 14-4 (borrador con ilustraciones) completada |
| Página del curso | Consulte [Módulo 14: Redacción de artículos](https://ai-agent.camp/es/course/module-14) en paralelo |

**Flujo de la sesión:**
1. Comprender los 5 Sweeps de corrección (perspectivas)
2. Ejecutar todos los Sweeps con proofreading-agent
3. Revisar los resultados y aplicar las correcciones

Al finalizar la sesión, un borrador del artículo corregido desde 5 perspectivas estará completó.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" o "se detuvo" para reanudar. Las respuestas pueden pausarse dependiendo de la herramienta, pero no es un error.

---

## 🎯 Verificación de preparación

Primero, confirmemos que todo está listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver la página del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Paso 1)
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar la ruta de la página del curso)
(different_lesson → Mostrar lista de módulos)

---

## 🚀 Paso 1: Comprender los 5 Sweeps de corrección

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Comprender las 5 perspectivas de corrección",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Explique los 5 Sweeps (perspectivas de revisión) que usa el agente de corrección.

1. Sweep de precisión: Exactitud de hechos, datos y nombres propios
2. Sweep de gramática: Detección de errores gramaticales, puntuación y erratas
3. Sweep de consistencia: Unificación de terminología, variaciones de notación y consistencia de estilo
4. Sweep de legibilidad: Longitud de oraciones, complejidad estructural y uso excesivo de términos técnicos
5. Sweep de estructura: Flujo lógico, longitud de párrafos y balance entre introducción y conclusión

Explique los elementos de verificación específicos y los patrones de observaciones comunes para cada Sweep.
```

**Resultado esperado**: Se explican los elementos de verificación detallados de los 5 Sweeps y ejemplos comunes de observaciones.

---

## 🚀 Paso 2: Ejecutar todos los Sweeps con proofreading-agent

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Ejecutar corrección",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Use la habilidad proofreading-agent para corregir el borrador del artículo.

Comando de ejecución:
python skills/proofreading-agent/scripts/proofreading_agent.py --input output/article-14-4-with-images.md --output output/article-14-5-review.json

Archivo objetivo: output/article-14-4-with-images.md

Ejecute los 5 Sweeps:
1. Sweep de precisión
2. Sweep de gramática
3. Sweep de consistencia
4. Sweep de legibilidad
5. Sweep de estructura

Para cada hallazgo, genere lo siguiente:
- Ubicación (número de línea y texto)
- Tipo de problema (nombre del Sweep)
- Severidad (Alta/Media/Baja)
- Corrección sugerida

Guarde los resultados en output/article-14-5-review.json.
```

**Resultado esperado**: Los resultados de corrección de los 5 Sweeps se generan en formato JSON, con todos los hallazgos listados.

---

## 🚀 Paso 3: Revisar resultados y aplicar correcciones

En Codex, normalmente se selecciona entre opciones en el chat para elegir el método de corrección.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Aplicar correcciones",
  "questions": [{
    "id": "apply_method",
    "prompt": "¿Cómo desea aplicar las correcciones?",
    "options": [
      {"id": "auto_all", "label": "Aplicar todas las correcciones automáticamente"},
      {"id": "one_by_one", "label": "Revisar y aplicar una por una"},
      {"id": "summary_only", "label": "Solo revisar el resumen"}
    ]
  }]
}
```

**Si selecciona "Aplicar todas las correcciones automáticamente":**
Entrada:
```text
Aplique todos los hallazgos de output/article-14-5-review.json al artículo.

Archivo objetivo: output/article-14-4-with-images.md
Archivo corregido: output/article-14-5-proofread.md

También genere un resumen de correcciones:
- Número de correcciones (por Sweep)
- Desglose por severidad
- Principales correcciones realizadas
```

**Si selecciona "Revisar y aplicar una por una":**
```text
Muestre los hallazgos de output/article-14-5-review.json uno por uno en orden de severidad.
Permita elegir "Aplicar/Omitir/Modificar corrección" para cada hallazgo.
```

**Si selecciona "Solo revisar el resumen":**
```text
Muestre el resumen de resultados de corrección de output/article-14-5-review.json.
Muestre el número de hallazgos por Sweep y liste solo los hallazgos de severidad "Alta".
```

**Resultado esperado**: Las correcciones de la revisión se aplican al artículo y se guarda el borrador corregido.

---

## ⚠️ Problemas comunes y soluciones

En Codex, normalmente se presentan opciones en el chat para que el usuario seleccione su problema y reciba orientación al instante.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "Demasiados hallazgos para manejar"},
      {"id": "trouble_2", "label": "Hallazgos irrelevantes"},
      {"id": "trouble_3", "label": "El texto quedó poco natural después de las correcciones"},
      {"id": "trouble_4", "label": "No se genera el archivo de resultados de revisión"}
    ]
  }]
}
```


### Problema 1: "Demasiados hallazgos para manejar"
**Causa**: La calidad del borrador es baja o los estándares de corrección son demasiado estrictos
**Prompt de solución**:
```text
Comience abordando solo los hallazgos de severidad "Alta".
Maneje los de severidad "Media" y "Baja" en la siguiente iteración.
Filtre y muestre solo los hallazgos de severidad "Alta".
```

### Problema 2: "Hallazgos irrelevantes"
**Causa**: Verificación mecánica sin considerar el contexto
**Prompt de solución**:
```text
Puede ignorar los hallazgos irrelevantes.
Seleccione "Omitir" y pase al siguiente hallazgo.
Las expresiones intencionales (características de estilo, expresiones retóricas) están excluidas de la corrección.
```

### Problema 3: "El texto quedó poco natural después de las correcciones"
**Causa**: Correcciones locales que ignoran el contexto
**Prompt de solución**:
```text
Si el texto corregido es poco natural, reajuste incluyendo el contexto circundante.
También puede volver al texto original:
Consulte output/article-14-4-with-images.md (antes de las correcciones).
```

### Problema 4: "No se genera el archivo de resultados de revisión"
**Causa**: No se encuentra el archivo de entrada
**Prompt de solución**:
```bash
Verifique la ruta del archivo de entrada:
ls output/article-14-4-with-images.md
Si el archivo no existe, complete primero la Lección 14-4 (/start-14-4).
```

---

## ✅ Punto de control
- [ ] Se comprendieron los 5 Sweeps de corrección (precisión/gramática/consistencia/legibilidad/estructura)
- [ ] Se ejecutaron todos los Sweeps con proofreading-agent
- [ ] Se revisaron los hallazgos y se decidió el enfoque de corrección
- [ ] Se guardó el borrador corregido con las correcciones en output/

---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/
└── article-14-5-*.md  (documentos del artículo)
```

### Comandos de verificación
```bash
# Verificar existencia y tamaño de archivos
ls -lh output/article-14-5-*.md

# Verificar el inicio (primeras 30 líneas)
head -30 output/article-14-5-*.md
```

> 💡 Ver texto completó: `cat output/article-14-5-*.md` para mostrar el archivo completó

---

## ✅ Verificación de finalización
Ingrese lo siguiente en el chat de Codex para verificar la finalización:

```bash
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Se muestra el estado de finalización/incompleto y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar.

En Codex, normalmente puede seleccionar entre opciones en el chat.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione qué hacer a continuación",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/next_lesson)"},
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-14-6)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir /start-14-6 en una nueva ventana
- finish → Finalizar

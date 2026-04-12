---
description: "When the user says /start-14-6 — Module 14 Lesson 14-6: Redacción de artículos - Agente de verificación de hechos"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-14-5"]
level: "intermediate"
tags: ["article", "factcheck"]
---

# 🎓 Lección 14-6: Verificación de hechos - Agente de verificación de hechos

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 14-6: Verificación de hechos - Agente de verificación de hechos**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Verificar las afirmaciones factuales del artículo con el agente de verificación de hechos y agregar citas |
| Duración | ~30 min |
| Habilidades utilizadas | fact-checker |
| Requisitos previos | Clave API de Gemini configurada, Lección 14-5 (borrador corregido) completada |
| Página del curso | Consulte [Módulo 14: Redacción de artículos](https://ai-agent.camp/es/course/module-14) en paralelo |

**Flujo de la sesión:**
1. Comprender las categorías objetivo de verificación de hechos
2. Ejecutar la verificación de hechos con fact-checker
3. Revisar los resultados de verificación y agregar citas al artículo

Al finalizar la sesión, un artículo verificado con citas estará completó.

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

## 🚀 Paso 1: Comprender las categorías de verificación de hechos

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Comprender las categorías de verificación de hechos",
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
Explique las 5 categorías que verifica el agente de verificación de hechos.

1. Números y estadísticas: Exactitud de valores como "X%", "X veces", "X mil millones"
2. Fechas y cronologías: Exactitud de fechas como "comenzó en el año X", "lanzado en el mes X"
3. Nombres propios: Ortografía y nombres oficiales de empresas, productos y personas
4. Relaciones causales: Validez de afirmaciones como "X causó Y"
5. Citas y referencias: Verificación de fuentes para afirmaciones como "según X", "un estudio de X muestra"

Explique los métodos de verificación específicos y los patrones de errores comunes para cada categoría.
```

**Resultado esperado**: Se explican los detalles de las 5 categorías de verificación y los patrones de errores comunes.

---

## 🚀 Paso 2: Ejecutar verificación de hechos con fact-checker

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Ejecutar verificación de hechos",
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
Use la habilidad fact-checker para verificar los hechos del artículo corregido.

Comando de ejecución:
python skills/fact-checker/scripts/fact_checker.py --input output/article-14-5-proofread.md --output output/article-14-6-factcheck.json

Archivo objetivo: output/article-14-5-proofread.md

Verifique en las 5 categorías:
1. Números y estadísticas
2. Fechas y cronologías
3. Nombres propios
4. Relaciones causales
5. Citas y referencias

Para cada afirmación, genere lo siguiente:
- Texto relevante (con número de línea)
- Categoría
- Resultado de verificación: Verificado / Requiere revisión / Error / Fuente desconocida
- Información correcta (si hay error)
- URL de fuente recomendada (si está disponible)

Guarde los resultados en output/article-14-6-factcheck.json.
```

**Resultado esperado**: Todas las afirmaciones factuales del artículo se verifican en las 5 categorías, con resultados generados en formato JSON.

---

## 🚀 Paso 3: Revisar resultados y agregar citas

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Agregar citas",
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
Con base en los resultados de verificación de output/article-14-6-factcheck.json,
aplique las siguientes correcciones al artículo.

1. Afirmaciones con "Error": Corregir con información precisa
2. Afirmaciones con "Requiere revisión": Cambiar a expresión cautelosa (por ejemplo, "se dice que...")
3. Citas con "Fuente desconocida": Agregar fuentes o eliminar la cita
4. Afirmaciones "Verificadas": Agregar fuentes como notas al pie

Coloque todas las citas al final del artículo:
## Referencias
1. [Título de la fuente](URL) - Descripción de la sección referenciada
2. ...

Guarde el resultado en output/article-14-6-factchecked.md.
```

**Resultado esperado**: Las correcciones de verificación de hechos se aplican y se guarda el artículo con citas.

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
      {"id": "trouble_1", "label": "La mayoría de las afirmaciones marcadas como 'Requiere revisión'"},
      {"id": "trouble_2", "label": "No se encuentran URLs de fuentes"},
      {"id": "trouble_3", "label": "La verificación de hechos es demasiado estricta"},
      {"id": "trouble_4", "label": "No se genera el archivo de resultados de verificación"}
    ]
  }]
}
```


### Problema 1: "La mayoría de las afirmaciones marcadas cómo 'Requiere revisión'"
**Causa**: Muchas afirmaciones en el artículo carecen de fuentes
**Prompt de solución**:
```text
Considere los siguientes enfoques:
1. Cambiar hechos generales (información ampliamente conocida) de "Requiere revisión" a "Verificado"
2. Cambiar afirmaciones sin datos específicos a expresiones cautelosas como "se considera generalmente que..."
3. Agregar fuentes oficiales (gobierno, artículos académicos, sitios oficiales) para afirmaciones importantes
```

### Problema 2: "No se encuentran URLs de fuentes"
**Causa**: Información de nicho o fuentes primarias no publicadas
**Prompt de solución**:
```text
Cuando no se encuentran fuentes:
1. Cambiar la expresión a "en la experiencia del autor" o "generalmente"
2. Usar fuentes de información similares (informes de la industria, artículos de noticias) como citas alternativas
3. Eliminar la afirmación (las afirmaciones sin evidencia erosionan la confianza del lector)
```

### Problema 3: "La verificación de hechos es demasiado estricta"
**Causa**: Se aplica verificación de nivel académico a un artículo de blog
**Prompt de solución**:
```text
Ajuste el nivel de verificación según el tipo de artículo:
- Artículos de blog: Enfocarse en la exactitud de números y nombres propios
- Artículos explicativos: Enfocarse en relaciones causales y exactitud de citas
- Artículos técnicos: Enfocarse en exactitud de comandos, información de versión y procedimientos
Las opiniones y consejos están excluidos de la verificación.
```

### Problema 4: "No se genera el archivo de resultados de verificación"
**Causa**: No se encuentra el archivo de entrada
**Prompt de solución**:
```bash
Verifique la ruta del archivo de entrada:
ls output/article-14-5-proofread.md
Si el archivo no existe, complete primero la Lección 14-5 (/start-14-5).
```

---

## ✅ Punto de control
- [ ] Se comprendieron las 5 categorías de verificación de hechos (números/fechas/nombres propios/relaciones causales/citas)
- [ ] Se ejecutó la verificación en todas las categorías con fact-checker
- [ ] Se revisaron los resultados de verificación y se corrigieron los errores
- [ ] Se guardó el artículo con citas agregadas en output/

---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/
└── article-14-6-*.md  (documentos del artículo)
```

### Comandos de verificación
```bash
# Verificar existencia y tamaño de archivos
ls -lh output/article-14-6-*.md

# Verificar el inicio (primeras 30 líneas)
head -30 output/article-14-6-*.md
```

> 💡 Ver texto completó: `cat output/article-14-6-*.md` para mostrar el archivo completó

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
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-14-7)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir /start-14-7 en una nueva ventana
- finish → Finalizar

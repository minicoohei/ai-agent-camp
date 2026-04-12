---
description: "When the user says /start-14-7 — Module 14 Lesson 14-7: Redacción de artículos - Ejecución paralela y finalización"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~40 min"
prerequisites: ["start-14-1", "start-14-2", "start-14-3", "start-14-4", "start-14-5", "start-14-6"]
level: "advanced"
tags: ["article", "parallel"]
---

# 🎓 Lección 14-7: Ejecución paralela y finalización - Procesamiento por lotes de múltiples artículos

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 14-7: Ejecución paralela y finalización - Procesamiento por lotes de múltiples artículos**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Aprender a generar artículos en paralelo con múltiples temas y ejecutar todo el flujo de trabajo en lote |
| Duración | ~40 min |
| Habilidades utilizadas | article-writer, style-analyzer, proofreading-agent, fact-checker, nanobanana, diagram-generator |
| Requisitos previos | Lecciones 14-1 a 14-6 completadas (comprensión de todas las etapas) |
| Página del curso | Consulte [Módulo 14: Redacción de artículos](https://ai-agent.camp/es/course/module-14) en paralelo |

**Flujo de la sesión:**
1. Configurar múltiples temas
2. Demostrar la generación paralela de artículos usando la herramienta Task
3. Ejecutar corrección y verificación de hechos en paralelo para cada artículo
4. Revisión final y salida de todos los artículos

Al finalizar la sesión, los artículos de múltiples temas estarán completados en paralelo y habrá dominado el patrón de ejecución por lotes de todo el flujo de trabajo.

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

## 🚀 Paso 1: Configurar múltiples temas

En Codex, normalmente se selecciona entre opciones en el chat para elegir el número de temas.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Elegir número de temas",
  "questions": [{
    "id": "theme_count",
    "prompt": "Seleccione el número de temas para la generación paralela",
    "options": [
      {"id": "two", "label": "2 temas (para principiantes, tiempo de procesamiento más corto)"},
      {"id": "three", "label": "3 temas (estándar, experimentar el efecto del procesamiento paralelo)"},
      {"id": "custom", "label": "Especificar temas manualmente"}
    ]
  }]
}
```

**Si selecciona "2 temas":**
Entrada:
```text
Generaremos artículos en paralelo para los siguientes 2 temas.

Tema A: "5 consejos para aumentar la productividad en el trabajo remoto"
- Audiencia: Profesionales de negocios que trabajan desde casa
- Tipo de artículo: Artículo de blog
- Extensión estimada: 2500-3000 caracteres

Tema B: "Habilidades necesarias en la era de la IA"
- Audiencia: Personas de 20 a 30 años que buscan avance profesional
- Tipo de artículo: Artículo explicativo
- Extensión estimada: 3000-3500 caracteres

Guarde el esquema de cada tema en output/batch/theme-a-outline.md y theme-b-outline.md.
```

**Si selecciona "3 temas":**
```text
Generaremos artículos en paralelo para los siguientes 3 temas.

Tema A: "5 consejos para aumentar la productividad en el trabajo remoto"
Tema B: "Habilidades necesarias en la era de la IA"
Tema C: "Técnicas de comunicación para mejorar la eficiencia del equipo"

Guarde el esquema de cada tema en output/batch/.
```

**Resultado esperado**: Se generan esquemas para múltiples temas en output/batch/.

---

## 🚀 Paso 2: Generación paralela de artículos usando la herramienta Task

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Ejecutar generación paralela de artículos",
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
Use la herramienta Task para generar artículos de múltiples temas en paralelo.

Ejecute las siguientes etapas en paralelo para cada tema:
1. Esquema → generación de borrador (article-writer + style-analyzer)
2. Detección de marcadores de ilustración y generación de imágenes (nanobanana / diagram-generator)
3. Inserción de imágenes

Patrón de ejecución paralela:
- Task 1: Generación del artículo del Tema A (output/batch/theme-a-draft.md)
- Task 2: Generación del artículo del Tema B (output/batch/theme-b-draft.md)
(Agregue Task 3 para 3 temas)

Use el perfil de estilo compartido output/style_profile.yaml para todos los temas.
Guarde todos los resultados en output/batch/ después de completar todas las tareas.
```

**Resultado esperado**: Los borradores de artículos de múltiples temas se generan en paralelo, con un tiempo de procesamiento menor que la ejecución secuencial.

---

## 🚀 Paso 3: Corrección y verificación de hechos en paralelo

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Ejecutar corrección y verificación de hechos en paralelo",
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
Ejecute la corrección y verificación de hechos en paralelo para cada artículo.

Patrón de ejecución paralela:
- Task 1: Corrección del Tema A (proofreading-agent)
- Task 2: Corrección del Tema B (proofreading-agent)
- Task 3: Verificación de hechos del Tema A (fact-checker) *después de completar la corrección
- Task 4: Verificación de hechos del Tema B (fact-checker) *después de completar la corrección

Resultados de cada tarea:
- output/batch/theme-a-proofread.md
- output/batch/theme-b-proofread.md
- output/batch/theme-a-final.md
- output/batch/theme-b-final.md

Flujo: Corrección → Verificación de hechos → Adición de citas → Guardar versión final
```

**Resultado esperado**: La corrección y verificación de hechos de todos los artículos se completan en paralelo y se guardan las versiones finales.

---

## 🚀 Paso 4: Revisión final y salida de todos los artículos

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Revisión final y salida",
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
Cree un informe final para todos los artículos en output/batch/.

Contenido del informe:
1. Resumen de cada artículo
   - Tema, extensión, número de ilustraciones, número de citas
2. Puntuación de calidad
   - Tasa de corrección de revisión
   - Tasa de aprobación de verificación de hechos
3. Eficiencia del procesamiento paralelo
   - Comparación de tiempo con ejecución secuencial (estimado)
   - Tiempo ahorrado por procesamiento paralelo
4. Lista de todos los artículos (con rutas de archivo)

Guarde el informe en output/batch/batch-report.md.

También muestre un resumen que revise todo el contenido de aprendizaje del Módulo 14:
- Lección 14-1: Configuración de tema y esquema
- Lección 14-2: Perfil de estilo
- Lección 14-3: Borrador con estilo aplicado
- Lección 14-4: Generación de ilustraciones
- Lección 14-5: Corrección
- Lección 14-6: Verificación de hechos
- Lección 14-7: Ejecución paralela (esta lección)
```

**Resultado esperado**: Se genera un informe final de todos los artículos y un resumen de aprendizaje del Módulo 14.

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
      {"id": "trouble_1", "label": "Algunas tareas paralelas fallan"},
      {"id": "trouble_2", "label": "El tiempo de procesamiento es demasiado largo"},
      {"id": "trouble_3", "label": "Los estilos son inconsistentes entre artículos"},
      {"id": "trouble_4", "label": "No se encuentran archivos en output/batch/"}
    ]
  }]
}
```


### Problema 1: "Algunas tareas paralelas fallan"
**Causa**: Límites de tasa de API o el error de una tarea afecta a otras
**Prompt de solución**:
```text
Re-ejecute solo las tareas fallidas.
Si es por límites de tasa de API, espere 30 segundos antes de re-ejecutar.
Los resultados de las tareas exitosas se preservan.
Verifique las rutas de archivo de los temas fallidos: ls output/batch/
```

### Problema 2: "El tiempo de procesamiento es demasiado largo"
**Causa**: Demasiados temas o la extensión del artículo es muy alta
**Prompt de solución**:
```text
Puede reducir el tiempo de procesamiento:
1. Reducir el número de temas a 2
2. Establecer la extensión estimada de cada artículo a menos de 2000 caracteres
3. Omitir la generación de ilustraciones (se pueden agregar después)
4. Limitar la corrección y verificación de hechos a "Solo severidad alta"
```

### Problema 3: "Los estilos son inconsistentes entre artículos"
**Causa**: Cada tarea interpreta el estilo de forma independiente
**Prompt de solución**:
```text
Especifique explícitamente el mismo perfil de estilo (output/style_profile.yaml)
para todos los artículos.
Asegúrese de que la opción --style de cada tarea incluya la ruta del perfil.
También puede ejecutar una verificación adicional de consistencia de estilo después de la generación.
```

### Problema 4: "No se encuentran archivos en output/batch/"
**Causa**: El directorio no existe
**Prompt de solución**:
```bash
Cree el directorio y vuelva a ejecutar:
mkdir -p ~/ai-agent-camp/output/batch
```

---

## ✅ Punto de control
- [ ] Se configuraron esquemas para múltiples temas (2-3 artículos)
- [ ] Se generaron borradores de artículos en paralelo con la herramienta Task
- [ ] Se ejecutaron corrección y verificación de hechos en paralelo
- [ ] Se guardaron las versiones finales de todos los artículos en output/batch/
- [ ] Se verificó la calidad y eficiencia con el informe por lotes

---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/
└── article-14-7-*.md  (documentos del artículo)
```

### Comandos de verificación
```bash
# Verificar existencia y tamaño de archivos
ls -lh output/article-14-7-*.md

# Verificar el inicio (primeras 30 líneas)
head -30 output/article-14-7-*.md
```

> 💡 Ver texto completó: `cat output/article-14-7-*.md` para mostrar el archivo completó

---

## ✅ Verificación de finalización
Ingrese lo siguiente en el chat de Codex para verificar la finalización:

```bash
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Se muestra el estado de finalización/incompleto y los elementos faltantes.

---

## ➡️ Siguientes pasos

Se completaron todas las lecciones del Módulo 14: Redacción de artículos.

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
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-15-1)"},
      {"id": "review_module", "label": "Revisar el Módulo 14"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir /start-15-1 en una nueva ventana
- review_module → Revisar cada lección del Módulo 14
- finish → Finalizar

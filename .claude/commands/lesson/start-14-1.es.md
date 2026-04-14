---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~25 min"
prerequisites: []
level: "beginner"
tags: ["article", "planning"]
---

# 🎓 Lección 14-1: Planificación de artículos - Selección de tema y generación de esquema

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 14-1: Planificación de artículos - Selección de tema y generación de esquema**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Determinar el tema del artículo, definir la audiencia objetivo y generar un esquema del artículo |
| Duración | ~25 min |
| Habilidades utilizadas | article-writer |
| Requisitos previos | Clave API de Gemini configurada |
| Página del curso | Consulte [Módulo 14: Redacción de artículos](https://ai-agent.camp/es/course/module-14) en paralelo |

**Flujo de la sesión:**
1. Establecer el tema del artículo y la audiencia objetivo
2. Generar automáticamente un esquema con la habilidad article-writer
3. Revisar y ajustar la estructura del esquema

Al finalizar la sesión, el tema del artículo, la audiencia objetivo y el esquema (estructura de títulos) estarán definidos.

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

## 🚀 Paso 1: Establecer el tema y la audiencia objetivo

En Codex, normalmente se selecciona entre opciones en el chat para elegir el tipo de artículo.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Elegir el tipo de artículo",
  "questions": [{
    "id": "article_type",
    "prompt": "¿Qué tipo de artículo va a escribir?",
    "options": [
      {"id": "blog", "label": "Artículo de blog (casual, enfocado en legibilidad)"},
      {"id": "explainer", "label": "Artículo explicativo (explicación de conceptos y mecanismos)"},
      {"id": "technical", "label": "Artículo técnico (procedimientos y detalles de implementación)"},
      {"id": "free_theme", "label": "Tema libre (especificar manualmente)"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Establezca el tema del artículo y la audiencia objetivo con las siguientes condiciones.

Tipo de artículo: Artículo de blog
Tema candidato: Mejora de la eficiencia laboral con herramientas de IA
Audiencia objetivo: Profesionales de negocios de 30 a 40 años, nivel intermedio de conocimientos informáticos

Genere lo siguiente:
1. Propuestas de título del artículo (3 candidatos)
2. Persona del lector objetivo (edad, ocupación, desafíos, metas)
3. Propósito del artículo (qué acción incentivar en los lectores)
4. Extensión estimada
5. Candidatos de palabras clave (para SEO, 3 a 5 palabras clave)

Guarde los resultados en output/article-14-1-theme.md.
```

**Resultado esperado**: Los candidatos de tema, la persona objetivo y el propósito del artículo se organizan y guardan cómo un archivo Markdown.

---

## 🚀 Paso 2: Generar esquema con la habilidad article-writer

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Generar esquema",
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
Use la habilidad article-writer para generar un esquema de artículo con el siguiente tema.

Tema: Mejora de la eficiencia laboral con herramientas de IA
Audiencia: Profesionales de negocios de 30 a 40 años
Tipo de artículo: Artículo de blog
Extensión estimada: 3000-4000 caracteres

Cree un esquema que incluya:
1. Introducción (gancho + resumen del artículo)
2. Estructura de títulos del cuerpo (nivel H2/H3)
3. Notas de puntos clave por sección (2-3 líneas)
4. Posiciones candidatas para ilustraciones (formato <!-- illustration: type=image/diagram, description="..." -->)
5. Resumen y CTA

Guarde los resultados en output/article-14-1-outline.md.
```

**Resultado esperado**: Se genera un esquema con la estructura de títulos, puntos clave por sección y marcadores de ilustración.

---

## 🚀 Paso 3: Revisar y ajustar el esquema

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Revisar y ajustar el esquema",
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
Revise el esquema en output/article-14-1-outline.md.

Proporcione comentarios desde las siguientes perspectivas:
1. Flujo lógico: ¿Las conexiones entre secciones son naturales?
2. Exhaustividad: ¿Responde a las preguntas del lector objetivo?
3. Legibilidad: ¿El balance de longitud entre secciones es apropiado?
4. Ubicación de ilustraciones: ¿Los puntos de inserción de figuras e imágenes son efectivos?

Si se necesitan mejoras, proponga una versión revisada y
guarde la versión final en output/article-14-1-outline-final.md.
```

**Resultado esperado**: Se muestran los resultados de la revisión del esquema y las propuestas de mejora, y se guarda el esquema final.

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
      {"id": "trouble_1", "label": "No puedo decidir el tema / el tema es demasiado amplio"},
      {"id": "trouble_2", "label": "El esquema es superficial / carece de especificidad"},
      {"id": "trouble_3", "label": "No se generan los marcadores de ilustración"},
      {"id": "trouble_4", "label": "El archivo no se guarda"}
    ]
  }]
}
```


### Problema 1: "No puedo decidir el tema / el tema es demasiado amplio"
**Causa**: La granularidad del tema es demasiado grande y carece de enfoque
**Prompt de solución**:
```text
Para delimitar el tema, responda las siguientes 3 preguntas:
1. ¿Qué es lo que el lector más quiere saber? (solo una cosa)
2. ¿Qué quiere que el lector haga después de leer este artículo?
3. ¿Cuál es el punto de diferenciación respecto a artículos similares?
Use estas respuestas para redefinir el tema.
```

### Problema 2: "El esquema es superficial / carece de especificidad"
**Causa**: Información insuficiente sobre el tema o el público objetivo
**Prompt de solución**:
```text
Para hacer el esquema más específico, agregue lo siguiente a cada sección:
- Al menos un ejemplo concreto o dato
- Una pregunta al lector
- Un elemento de acción
```

### Problema 3: "No se generan los marcadores de ilustración"
**Causa**: No se especificó el formato de marcadores de ilustración en el prompt
**Prompt de solución**:
```text
Agregue marcadores de ilustración al esquema.
Formato: <!-- illustration: type=image|diagram, description="texto descriptivo" -->
Coloque al menos un marcador de ilustración en cada sección H2.
```

### Problema 4: "El archivo no se guarda"
**Causa**: El directorio output no existe
**Prompt de solución**:
```bash
Verifique si el directorio output existe y créelo si no existe.
mkdir -p ~/ai-agent-camp/output
```

---

## ✅ Punto de control
- [ ] Se determinó el tema del artículo y las propuestas de título
- [ ] Se estableció la persona del lector objetivo
- [ ] Se generó un esquema con la habilidad article-writer
- [ ] Se revisó el esquema y se guardó la versión final en output/

---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/
└── article-14-1-*.md  (documentos del artículo)
```

### Comandos de verificación
```bash
# Verificar existencia y tamaño de archivos
ls -lh output/article-14-1-*.md

# Verificar el inicio (primeras 30 líneas)
head -30 output/article-14-1-*.md
```

> 💡 Ver texto completó: `cat output/article-14-1-*.md` para mostrar el archivo completó

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
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-14-2)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir /start-14-2 en una nueva ventana
- finish → Finalizar

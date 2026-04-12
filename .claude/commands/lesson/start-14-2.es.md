---
description: "When the user says /start-14-2 — Module 14 Lesson 14-2: Redacción de artículos - Aprendizaje de estilo y creación de perfil de estilo"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-14-1"]
level: "beginner"
tags: ["article", "style"]
---

# 🎓 Lección 14-2: Aprendizaje de estilo - Creación de perfil de estilo

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 14-2: Aprendizaje de estilo - Creación de perfil de estilo**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Analizar múltiples muestras de escritura para identificar características de estilo y crear un perfil de estilo |
| Duración | ~30 min |
| Habilidades utilizadas | style-analyzer |
| Requisitos previos | Lección 14-1 completada, clave API de Gemini configurada, muestras de escritura para análisis (3-5 recomendadas) |
| Página del curso | Consulte [Módulo 14: Redacción de artículos](https://ai-agent.camp/es/course/module-14) en paralelo |

**Flujo de la sesión:**
1. Preparar sus muestras de escritura (3-5 recomendadas)
2. Ejecutar el análisis de estilo con style-analyzer
3. Revisar y comprender el perfil de estilo generado

Al finalizar la sesión, un perfil de estilo (formato YAML) que cuantifica las características de su escritura estará completó.

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

## 🚀 Paso 1: Preparar muestras de escritura

En Codex, normalmente se selecciona entre opciones en el chat para indicar el estado de preparación de las muestras.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Preparar muestras de escritura",
  "questions": [{
    "id": "sample_status",
    "prompt": "¿Tiene muestras de escritura para el análisis?",
    "options": [
      {"id": "ready", "label": "Muestras listas (especificar ruta del archivo)"},
      {"id": "write_now", "label": "Escribir texto de muestra ahora"},
      {"id": "use_demo", "label": "Usar muestras de demostración"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:

**Si selecciona "Muestras listas":**
```text
Proporcione las rutas de los archivos de muestras de escritura para el análisis.
Lo ideal son 3-5 archivos Markdown o de texto.
Ejemplo: output/samples/sample1.md, output/samples/sample2.md
```

**Si selecciona "Escribir texto de muestra ahora":**
```text
Vamos a crear muestras de escritura en el directorio output/samples/.
Usando la plantilla a continuación, escriba 3 textos cortos (300-500 caracteres cada uno):

Ejemplos de temas:
1. Algo que aprendió recientemente
2. Recomendación de una herramienta
3. Consejos y trucos de trabajo

Guarde cada archivo como output/samples/sample1.md, sample2.md, sample3.md.
```

**Si selecciona "Usar muestras de demostración":**
```text
Se generarán 3 textos de muestra de demostración y se guardarán en output/samples/.
Se incluirán muestras con diferentes patrones de estilo (casual/formal/técnico).
```

**Resultado esperado**: 3-5 muestras de escritura para análisis preparadas en output/samples/.

---

## 🚀 Paso 2: Ejecutar análisis de estilo con style-analyzer

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Ejecutar análisis de estilo",
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
Use la habilidad style-analyzer para ejecutar un análisis de estilo en las siguientes muestras de escritura.

Archivos de entrada:
- output/samples/sample1.md
- output/samples/sample2.md
- output/samples/sample3.md

Elementos de análisis:
1. Patrones de terminación de oraciones (forma cortés, forma llana, mixto)
2. Longitud promedio de oraciones (caracteres por oración)
3. Proporción kanji/hiragana/katakana
4. Características del tono (cortesía, amabilidad, tecnicismo)
5. Tendencias de conjunciones (frecuencia, conjunciones más usadas)
6. Patrones de estructura de párrafos (oraciones por párrafo, frecuencia de saltos de línea)

Guarde los resultados en output/style_profile.yaml.

Comando de ejecución:
python skills/style-analyzer/scripts/style_analyzer.py --input output/samples/sample1.md --input output/samples/sample2.md --input output/samples/sample3.md --output output/style_profile.yaml
```

**Resultado esperado**: Las características del estilo de escritura se cuantifican, estructuran y guardan cómo un perfil de estilo en formato YAML.

---

## 🚀 Paso 3: Revisar y explicar los resultados del perfil

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Revisar los resultados del perfil",
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
Lea el contenido de output/style_profile.yaml y explique lo siguiente:

1. Resumen de las características de mi estilo de escritura (3-5 líneas)
2. Significado e interpretación de los valores de cada elemento de análisis
3. Tipos de artículos adecuados para este estilo de escritura (blog/explicativo/técnico, etc.)
4. Fortalezas del estilo de escritura (puntos que causan buena impresión en los lectores)
5. Sugerencias de mejora (propuestas para mejorar la legibilidad)

Este perfil se usará en la Lección 14-3 para generar artículos,
así que comprendamos bien su contenido.
```

**Resultado esperado**: Se proporcionan explicaciones de cada elemento del perfil de estilo y las características, fortalezas y puntos de mejora del estilo de escritura.

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
      {"id": "trouble_1", "label": "Pocas muestras, baja precisión del análisis"},
      {"id": "trouble_2", "label": "Los valores del perfil de estilo son extremos"},
      {"id": "trouble_3", "label": "Error con style-analyzer"},
      {"id": "trouble_4", "label": "El archivo no se guarda"}
    ]
  }]
}
```


### Problema 1: "Pocas muestras, baja precisión del análisis"
**Causa**: Con solo 1-2 muestras, las tendencias de estilo no se pueden capturar con precisión
**Prompt de solución**:
```text
Para aumentar la cantidad de muestras, intente lo siguiente:
- Extraiga texto de correos electrónicos, chats o informes anteriores
- Incluso textos cortos pueden revelar tendencias básicas con 3 o más muestras
- Si no puede preparar muestras, practique con "muestras de demostración" primero,
  y luego re-analice con sus propias muestras más adelante
```

### Problema 2: "Los valores del perfil de estilo son extremos"
**Causa**: Los estilos varían mucho entre las muestras (por ejemplo, mezcla de escritura laboral y personal)
**Prompt de solución**:
```text
Verifique si los estilos de escritura de las muestras son consistentes.
Recomendamos separar por propósito (negocios/casual) y
crear perfiles separados para cada uno:
- output/style_profile_business.yaml
- output/style_profile_casual.yaml
```

### Problema 3: "Error con style-analyzer"
**Causa**: Ruta de archivo incorrecta o formato de archivo no compatible
**Prompt de solución**:
```text
Verifique lo siguiente:
1. ¿La ruta del archivo es correcta? (especifique ruta absoluta)
2. ¿El formato del archivo es .md o .txt?
3. ¿El archivo no está vacío?
4. ¿La codificación de caracteres es UTF-8?
```

### Problema 4: "El archivo no se guarda"
**Causa**: El directorio output no existe
**Prompt de solución**:
```bash
Verifique si el directorio output existe y créelo si no existe.
mkdir -p ~/ai-agent-camp/output/samples
```

---

## ✅ Punto de control
- [ ] Se prepararon 3 o más muestras de escritura
- [ ] Se ejecutó el análisis de estilo con style-analyzer
- [ ] Se guardó el perfil de estilo (formato YAML) en output/
- [ ] Se comprendió el significado de cada elemento del perfil

---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/
└── article-14-2-*.md  (documentos del artículo)
```

### Comandos de verificación
```bash
# Verificar existencia y tamaño de archivos
ls -lh output/article-14-2-*.md

# Verificar el inicio (primeras 30 líneas)
head -30 output/article-14-2-*.md
```

> 💡 Ver texto completó: `cat output/article-14-2-*.md` para mostrar el archivo completó

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
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-14-3)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir /start-14-3 en una nueva ventana
- finish → Finalizar

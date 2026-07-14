---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~40 min"
prerequisites: ["start-14-3"]
level: "intermediate"
tags: ["article", "illustration"]
nonInteractiveMode: deferred
---
# 🎓 Lección 14-4: Planificación y generación de ilustraciones - nanobanana + PlantUML

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 14-4: Planificación y generación de ilustraciones - nanobanana + PlantUML**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Detectar marcadores de ilustración en el artículo y generar automáticamente ilustraciones con nanobanana y PlantUML |
| Duración | ~40 min |
| Habilidades utilizadas | nanobanana, diagram-generator |
| Requisitos previos | Clave API de Gemini configurada, Lección 14-3 (borrador) completada |
| Página del curso | Consulte [Módulo 14: Redacción de artículos](https://ai-agent.camp/es/course/module-14) en paralelo |

**Flujo de la sesión:**
1. Verificar los marcadores de ilustración (`<!-- illustration: ... -->`) en el borrador
2. Para marcadores type=diagram → generar diagramas con PlantUML
3. Para marcadores type=image → generar imágenes con nanobanana
4. Insertar las imágenes generadas en Markdown

Al finalizar la sesión, un borrador del artículo con ilustraciones estará completó.

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

## 🚀 Paso 1: Verificar los marcadores de ilustración en el borrador

En Codex, normalmente se selecciona entre opciones en el chat para elegir el método de detección de marcadores.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Verificar marcadores de ilustración",
  "questions": [{
    "id": "marker_method",
    "prompt": "¿Cómo desea detectar los marcadores de ilustración?",
    "options": [
      {"id": "auto_detect", "label": "Detectar marcadores automáticamente"},
      {"id": "manual_specify", "label": "Especificar manualmente las ubicaciones de ilustraciones"}
    ]
  }]
}
```

**Si selecciona "Detectar marcadores automáticamente":**
Entrada:
```text
Lea output/article-14-3-draft-final.md y
extraiga todos los marcadores de ilustración (<!-- illustration: ... -->).

Liste lo siguiente para cada marcador:
1. Número de línea
2. Tipo (image / diagram)
3. Texto de descripción
4. Contexto circundante (a qué sección pertenece)

Si faltan marcadores, sugiera ubicaciones donde deberían agregarse.
```

**Si selecciona "Especificar manualmente las ubicaciones":**
```text
Muestre el contenido de output/article-14-3-draft-final.md.
Especifique dónde desea insertar ilustraciones y se agregarán los marcadores.
```

**Resultado esperado**: Todos los marcadores de ilustración del borrador están listados y se establece un plan de generación.

---

## 🚀 Paso 2: Generar diagramas con PlantUML (type=diagram)

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Generar diagramas con PlantUML",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir (si no hay marcadores de diagrama)"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Use la habilidad diagram-generator para generar diagramas para los siguientes marcadores de ilustración.

Marcador objetivo:
<!-- illustration: type=diagram, description="Diagrama de flujo de mejora de eficiencia laboral" -->

Condiciones de generación:
- Formato: PlantUML → imagen PNG
- Estilo: Esquema de colores simple y fácil de leer
- Salida: output/images/article-14-4-diagram-1.png

Comando de ejecución:
uv run python tools/generate_diagram.py --type flowchart --topic "Flujo de mejora de eficiencia laboral" --output output/images/article-14-4-diagram-1.png

Genere imágenes para todos los marcadores de diagrama.
```

**Resultado esperado**: Se generan imágenes de diagramas basados en PlantUML en output/images/.

---

## 🚀 Paso 3: Generar imágenes con nanobanana (type=image)

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Generar imágenes con nanobanana",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir (si no hay marcadores de imagen)"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Use la habilidad nanobanana para generar imágenes para los siguientes marcadores de ilustración.

Marcador objetivo:
<!-- illustration: type=image, description="Profesional de negocios trabajando con herramientas de IA" -->

Condiciones de generación:
- Estilo: Ilustración moderna y limpia
- Tamaño: Relación de aspecto adecuada para ilustraciones de artículos (16:9 o 4:3)
- Salida: output/images/article-14-4-image-1.png

Comando de ejecución:
uv run python tools/nanobanana.py --prompt "Profesional de negocios trabajando con herramientas de IA, estilo de ilustración moderna" --output output/images/article-14-4-image-1.png

Genere imágenes para todos los marcadores de imagen.
```

**Resultado esperado**: Se guardan las imágenes de ilustración generadas con nanobanana en output/images/.

---

## 🚀 Paso 4: Insertar las imágenes generadas en Markdown

En Codex, normalmente se selecciona entre opciones en el chat: "Continuar / Solo revisar ejemplos / Omitir".

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Insertar imágenes en Markdown",
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
Reemplace los marcadores de ilustración en output/article-14-3-draft-final.md
con la sintaxis de imagen Markdown de las imágenes generadas.

Reglas de reemplazo:
- <!-- illustration: type=diagram, description="..." -->
  → ![Descripción](images/article-14-4-diagram-N.png)
- <!-- illustration: type=image, description="..." -->
  → ![Descripción](images/article-14-4-image-N.png)

Agregue texto alternativo (descripción) y un pie de imagen (*Figura N: Descripción*) a cada imagen.

Guarde el resultado en output/article-14-4-with-images.md.
```

**Resultado esperado**: Los marcadores de ilustración se reemplazan con referencias de imagen reales y se guarda el borrador completó del artículo.

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
      {"id": "trouble_1", "label": "Los diagramas PlantUML no se generan correctamente"},
      {"id": "trouble_2", "label": "Las imágenes de nanobanana no coinciden con lo esperado"},
      {"id": "trouble_3", "label": "No se encuentran los marcadores de ilustración"},
      {"id": "trouble_4", "label": "Las rutas de inserción de imágenes están rotas"}
    ]
  }]
}
```


### Problema 1: "Los diagramas PlantUML no se generan correctamente"
**Causa**: Error de sintaxis PlantUML o problema con el entorno Java
**Prompt de solución**:
```text
Verifique la sintaxis de PlantUML.
Primero verifique el funcionamiento con un diagrama simple, luego agregue elementos gradualmente.
Si se necesita un entorno Java: verifique con java -version.
Alternativa: También puede generar diagramas directamente con la API de generación de imágenes de Gemini.
```

### Problema 2: "Las imágenes de nanobanana no coinciden con lo esperado"
**Causa**: El prompt no es lo suficientemente específico
**Prompt de solución**:
```text
Haga el prompt de generación de imágenes más específico:
- Especificación de estilo: "ilustración de diseño plano", "estilo fotorrealista", "estilo acuarela"
- Especificación de color: "tonos azules tranquilos"
- Especificación de composición: "objeto principal centrado, fondo simple"
Intente regenerar y comparar los resultados.
```

### Problema 3: "No se encuentran los marcadores de ilustración"
**Causa**: Los marcadores no se insertaron en la Lección 14-1/14-3
**Prompt de solución**:
```text
Agregue marcadores de ilustración al borrador.
Inserte al inicio o final de cada sección H2 en este formato:
<!-- illustration: type=image|diagram, description="Descripción del contenido de la sección" -->
```

### Problema 4: "Las rutas de inserción de imágenes están rotas"
**Causa**: Discrepancia entre rutas relativas y absolutas
**Prompt de solución**:
```bash
Use rutas relativas desde el archivo del artículo para las rutas de imágenes en Markdown.
Si el artículo está en output/: ![alt](images/filename.png)
Verifique que las imágenes estén en output/images/: ls output/images/
```

---

## ✅ Punto de control
- [ ] Se detectaron y confirmaron todos los marcadores de ilustración en el borrador
- [ ] Se generaron diagramas PlantUML para los marcadores type=diagram
- [ ] Se generaron imágenes nanobanana para los marcadores type=image
- [ ] Se guardó el artículo con todas las ilustraciones insertadas en Markdown en output/

---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/
└── article-14-4-*.md  (documentos del artículo)
```

### Comandos de verificación
```bash
# Verificar existencia y tamaño de archivos
ls -lh output/article-14-4-*.md

# Verificar el inicio (primeras 30 líneas)
head -30 output/article-14-4-*.md
```

> 💡 Ver texto completó: `cat output/article-14-4-*.md` para mostrar el archivo completó

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
      {"id": "next_window", "label": "Abrir en nueva ventana (/start-14-5)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir /start-14-5 en una nueva ventana
- finish → Finalizar

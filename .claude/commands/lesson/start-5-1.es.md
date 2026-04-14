---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module05-pptx"
duration: "~25 min"
prerequisites: ["start-0-1"]
level: "beginner"
tags: ["pptx", "analysis", "document"]
---

# 🎓 Lesson 5-1: Analisis de PPTX

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 5-1: Analisis de PPTX**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Analizar estructuras de archivos PPTX y extraer informacion de diapositivas, disenos y texto |
| Duracion | ~25 min |
| Skills utilizados | pptx-analyzer, document-processor |
| Requisitos previos | Entorno Python configurado, se recomienda tener un archivo PPTX de muestra |
| Pagina del curso | [Module 5: PPTX](https://ai-agent.camp/es/course/module-5) en paralelo |

**Flujo de la sesion:**
1. Verificar la estructura del archivo PPTX
2. Extraer diapositivas, texto y formas
3. Obtener informacion de la plantilla

Al finalizar esta sesion, podra manejar estructuras PPTX programaticamente.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificacion de preparacion

Verifiquemos que todo esta listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Confirmación antes de iniciar la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo/a?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver primero la página del curso"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Verificar instalacion de bibliotecas requeridas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Verificar instalación de bibliotecas requeridas",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Verifique si python-pptx está instalado.
Si no está instalado, ejecute pip install python-pptx.
```

**Resultado esperado**: python-pptx esta instalado y se muestra la version.

---

## 🚀 Step 2: Preparar archivo PPTX de muestra

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Preparar archivo PPTX de muestra",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Verifique si tiene un archivo de PowerPoint de muestra.
Si no, cree un archivo PPTX de prueba simple (aproximadamente 3 diapositivas).
```

> **Nota**: Es posible que no existan archivos PPTX de muestra en el directorio `data/`. Use cualquier archivo `.pptx` que tenga a mano, o pida a la IA que genere un archivo PPTX de prueba en `output/`.

**Resultado esperado**: Se prepara un archivo PPTX de muestra.

---

## 🚀 Step 3: Extraer informacion basica del PPTX

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Extraer información básica del PPTX",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cargue el archivo PPTX en ~/ai-agent-camp/data/ y proporcione la siguiente información:
- Número total de diapositivas
- Nombre del diseño de cada diapositiva
- Número de formas en cada diapositiva
- Lista de fuentes utilizadas
```

**Resultado esperado**: La informacion de estructura del archivo PPTX se muestra en formato JSON.

---

## 🚀 Step 4: Analisis detallado por diapositiva

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Análisis detallado por diapositiva",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Realice un análisis detallado de cada diapositiva del archivo PPTX:
- Contenido de texto (incluyendo viñetas)
- Tamaño y posición de la imagen si está presente
- Número de filas y columnas si hay una tabla
Guarde los resultados como archivo JSON en ~/ai-agent-camp/output/pptx-analysis.json.
```

**Resultado esperado**: Los resultados detallados del analisis se guardan como archivo JSON.

---

## 🚀 Step 5: Extraer informacion de plantilla

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Extraer información de plantilla",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Extraiga la información del patrón de diapositivas y diseño del archivo PPTX:
- Lista de diseños disponibles
- Información de marcadores de posición para cada diseño
- Configuración de colores del tema
Organice estos como información de plantilla reutilizable.
```

**Resultado esperado**: Se extrae la informacion de la plantilla y las opciones de diseno quedan claras.

---

## ⚠️ Problemas comunes y soluciones

Use AskUserQuestion (AskQuestion) para seleccionar su problema y recibir asistencia guiada.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione la opción que corresponda",
    "options": [
      {"id": "trouble_1", "label": "No se puede abrir el archivo PPTX"},
      {"id": "trouble_2", "label": "Ocurren problemas de codificación de caracteres"},
      {"id": "trouble_3", "label": "No se puede obtener la información de la imagen"}
    ]
  }]
}
```


### Problema 1: "No se puede abrir el archivo PPTX"
**Causa**: La ruta del archivo es incorrecta, o el archivo esta danado
**Prompt de solucion**:
```
Verifique si el archivo PPTX se puede cargar correctamente.
Si ocurre un error, identifique la causa y la solución.
```

### Problema 2: "Ocurren problemas de codificacion de caracteres"
**Causa**: Problema de codificacion
**Prompt de solucion**:
```
El texto en japonés del PPTX tiene problemas de codificación de caracteres.
Explique cómo guardar correctamente con codificación UTF-8.
```

### Problema 3: "No se puede obtener la informacion de la imagen"
**Causa**: La imagen no esta correctamente incrustada dentro de la forma
**Prompt de solucion**:
```
No se puede obtener la información de la imagen del PPTX.
Verifique el método de verificación hasattr(shape, 'image').
```

---

## ✅ Punto de control
- [ ] Pudo instalar python-pptx
- [ ] Pudo cargar un archivo PPTX
- [ ] Pudo obtener informacion basica de diapositivas
- [ ] Pudo extraer informacion de texto y formas
- [ ] Pudo obtener informacion de diseno y marcadores de posicion
- [ ] Pudo guardar los resultados del analisis como JSON


---

## 📋 Vista previa de resultados

### Salida esperada
```
📁 output/
└── presentation.pptx  (Presentación de PowerPoint)
    Número de diapositivas: N
```

### Comandos de verificacion
```bash
# Verificar existencia y tamano del archivo
ls -lh output/presentation.pptx

# Abrir en PowerPoint (macOS: open / Linux: xdg-open)
open output/presentation.pptx
```

> 💡 Verificar numero de diapositivas: `python3 -c "from pptx import Presentation; p=Presentation('output/presentation.pptx'); print(f'Numero de diapositivas: {len(p.slides)}')"`

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Cursor para verificar la finalizacion:

```
# Verificación de finalización: Verifique que se hayan generado los archivos de salida esperados en la carpeta output/.
```

**Resultado esperado**: Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Use AskUserQuestion (AskQuestion) para elegir.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-5-2)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-5-2
- finish → Finalizar

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module05-pptx"
prerequisites: ["start-5-1"]
duration: "~30 min"
level: "intermediate"
tags: ["pptx", "generation", "automation", "document"]
---

# 🎓 Lesson 5-2: Edicion y generacion automatica de PPTX

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 5-2: Edicion y generacion automatica de PPTX**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear nuevas diapositivas, editar texto y agregar formas, tablas e imagenes usando python-pptx |
| Duracion | ~30 min |
| Skills utilizados | pptx_ops, generate_slide, document-processor |
| Requisitos previos | Leccion 5-1 completada, entorno Python configurado |
| Pagina del curso | [Module 5: PPTX](https://ai-agent.camp/es/course/module-5) en paralelo |

**Flujo de la sesion:**
1. Agregar nuevas diapositivas y editar texto
2. Agregar formas, tablas e imagenes
3. Generar automaticamente diapositivas desde plantillas

Al finalizar esta sesion, podra editar y generar archivos PPTX programaticamente.

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

## 🚀 Step 1: Crear nueva presentacion

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Crear nueva presentación",
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
Cree una nueva presentación 16:9 usando python-pptx.
Agregue una diapositiva de título con el título "Curso de agentes de IA",
subtítulo "Febrero 2026",
y guarde como ~/ai-agent-camp/output/new_presentation.pptx.
```

**Resultado esperado**: Se crea un nuevo archivo PPTX que contiene una diapositiva de titulo.

---

## 🚀 Step 2: Agregar diapositivas de contenido

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Agregar diapositivas de contenido",
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
Agregue diapositivas de contenido al PPTX que acaba de crear con el siguiente contenido:

Diapositiva 2:
- Título: "Agenda de hoy"
- Viñetas:
  1. ¿Qué son los agentes de IA?
  2. Cómo usar Claude Code
  3. Taller práctico
  4. Preguntas y respuestas

Diapositiva 3:
- Título: "¿Qué son los agentes de IA?"
- Viñetas:
  1. IA que ejecuta tareas de forma autónoma
  2. Comprende instrucciones del usuario y actúa
  3. Puede combinar múltiples herramientas
```

**Resultado esperado**: Se agrega una diapositiva con formato de vinaetas.

---

## 🚀 Step 3: Agregar tablas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Agregar tablas",
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
Agregue una nueva diapositiva al PPTX y cree una tabla con los siguientes datos:

Título: "Tabla de comparación de funciones"

| Función | Claude Code | Herramientas tradicionales |
|---------|------------|---------------------------|
| Lenguaje natural | ◯ | △ |
| Generación de código | ◯ | × |
| Operaciones de archivos | ◯ | △ |
| Curva de aprendizaje | Baja | Alta |

Aplique negrita a la fila de encabezado con un estilo legible.
```

**Resultado esperado**: Se agrega una diapositiva que contiene una tabla.

---

## 🚀 Step 4: Agregar formas y elementos de diseno

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Agregar formas y elementos de diseño",
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
Agregue una nueva diapositiva al PPTX y añada los siguientes elementos de diseño:

- Título: "Flujo de trabajo"
- 3 rectángulos dispuestos horizontalmente
- Texto "Entrada" "Proceso" "Salida" en cada rectángulo
- Flechas colocadas entre los rectángulos
- Fondo: Degradado en tonos azules

Cree un diseño de diagrama de flujo profesional.
```

**Resultado esperado**: Se crea un diagrama de flujo usando formas.

---

## 🚀 Step 5: Generar automaticamente desde plantilla

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Generación automática desde plantilla",
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
Genere automáticamente una presentación a partir de los siguientes datos JSON:

{
  "title": "Reporte trimestral",
  "subtitle": "2026 Q1",
  "author": "Departamento de ventas",
  "slides": [
    {
      "type": "content",
      "title": "Resultados de ventas",
      "points": ["Logro del objetivo: 115%", "Interanual: +20%", "Nuevos clientes: 50"]
    },
    {
      "type": "content",
      "title": "Planes futuros",
      "points": ["Lanzamiento de nuevos productos", "Expansión global", "Promoción de DX"]
    }
  ]
}

Salida: ~/ai-agent-camp/output/quarterly_report.pptx
```

**Resultado esperado**: Se genera automaticamente una presentacion a partir de datos JSON.

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
      {"id": "trouble_1", "label": "Índice de diseño fuera de rango"},
      {"id": "trouble_2", "label": "Las fuentes japonesas no se muestran"},
      {"id": "trouble_3", "label": "La relación de aspecto de la imagen está distorsionada"},
      {"id": "trouble_4", "label": "Los anchos de las celdas de la tabla no son iguales"}
    ]
  }]
}
```


### Problema 1: "Indice de diseno fuera de rango"
**Causa**: El diseno que intenta usar no existe
**Prompt de solucion**:
```
Muestre todos los diseños disponibles y sus índices.
Quiero verificar la lista de prs.slide_layouts.
```

### Problema 2: "Las fuentes japonesas no se muestran"
**Causa**: Problema de especificacion de fuente
**Prompt de solucion**:
```
Aplique la fuente japonesa "Meiryo" al texto de la diapositiva.
Muestre cómo configurar paragraph.font.name = "Meiryo".
```

### Problema 3: "La relacion de aspecto de la imagen esta distorsionada"
**Causa**: Se especifican tanto el ancho como la altura
**Prompt de solucion**:
```
Al insertar una imagen, muestre cómo insertar manteniendo la relación de aspecto.
Use el método de especificar solo el ancho.
```

### Problema 4: "Los anchos de las celdas no son iguales"
**Causa**: Los anchos de columna se calculan automaticamente
**Prompt de solucion**:
```
Muestre cómo establecer explícitamente el ancho de cada columna de la tabla.
Use la configuración table.columns[i].width.
```

---

## ✅ Punto de control
- [ ] Pudo crear una nueva presentacion
- [ ] Pudo agregar una diapositiva de titulo
- [ ] Pudo agregar contenido con vinaetas
- [ ] Pudo crear y colocar una tabla
- [ ] Pudo colocar formas (rectangulos, flechas)
- [ ] Pudo generar automaticamente a partir de datos JSON
- [ ] Pudo guardar el archivo correctamente


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-6-1)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-6-1
- finish → Finalizar

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "~25 min"
level: "intermediate"
tags: ["screenshot", "annotation", "manual"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 3-4: Configuracion de monitoreo de panel de control

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 3-4: Configuracion de monitoreo de panel de control**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Agregar flechas, marcos, numeros y texto usando el skill screenshot-annotator para crear imagenes de manual |
| Duracion | ~25 min |
| Skills utilizados | screenshot-annotator (Gemini Vision API) |
| Requisitos previos | Lesson 3-1 completada, clave de Gemini API configurada |
| Pagina del curso | [Module 3: Analisis de capturas](https://ai-agent.camp/es/course/module-3) en paralelo |

**Flujo de la sesion:**
1. Resaltar botones con marcos rojos
2. Agregar flechas y globos de texto
3. Crear imagenes anotadas con numeros de paso

Al finalizar esta sesion, las imagenes anotadas para manuales estaran guardadas en outputs.

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

## 🚀 Step 1: Capturar capturas de pantalla del panel de control

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Resaltar botones con marcos rojos",
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
Utilice el skill screenshot-annotator para resaltar el boton de ayuda del panel de control.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/dashboard.png
Salida: output/screenshots/help-button-annotated.png

Anotaciones:
- Enmarque el boton de ayuda en la esquina superior derecha con un recuadro rojo
- Senale con una flecha diciendo "Haga clic aqui"
- Estilo: red_box
```

**Resultado esperado**: Se genera una imagen con el boton de ayuda enmarcado en rojo y flechas con texto explicativo agregado.

---

## 🚀 Step 2: Analizar metricas y KPI

Agregue explicaciones al formulario de busqueda:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Agregar explicaciones con globos de texto",
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
Agregue explicaciones con globos de texto al formulario de busqueda.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/search-form.png
Salida: output/screenshots/search-annotated.png

Anotaciones:
- Identifique el formulario de busqueda
- Estilo: callout (globo de texto)
- Texto: "Ingrese una palabra clave y presione la tecla Enter"
```

**Resultado esperado**: Se agrega un globo de texto al formulario de busqueda explicando como usarlo.

---

## 🚀 Step 3: Generar reporte de monitoreo

Agregue numeros a los pasos de operacion:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Agregar numeros de paso",
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
Agregue numeros a los pasos de operacion del menu.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/menu-operation.png
Salida: output/screenshots/menu-steps-annotated.png

Anotaciones (agregar en orden):
1. Icono de menu en la esquina superior izquierda -> Agregar "1" (estilo circulo)
2. Elemento del menu de configuracion -> Agregar "2"
3. Configuracion de perfil -> Agregar "3"

Encierre cada numero en un circulo rojo para aclarar el orden de las operaciones.
```

**Resultado esperado**: Se genera una imagen con pasos numerados 1, 2, 3 en circulos rojos.

---

## 🚀 Step 4: Revisar estilos de anotacion

Revisemos los estilos de anotacion disponibles:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Revisar estilos de anotacion",
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
Indiqueme todos los estilos de anotacion disponibles en screenshot-annotator.

Para cada estilo, explique lo siguiente:
- Nombre del estilo
- Descripcion visual
- Casos de uso adecuados
- Ejemplo de uso
```

**Resultado esperado**: Se muestra una lista de estilos como red_box, arrow, callout, highlight, circle, number, etc.

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
      {"id": "trouble_1", "label": "Las anotaciones no se muestran"},
      {"id": "trouble_2", "label": "La posicion de la anotacion es incorrecta"},
      {"id": "trouble_3", "label": "La direccion de la flecha esta invertida"},
      {"id": "trouble_4", "label": "El texto es dificil de leer"}
    ]
  }]
}
```


### Problema 1: "Las anotaciones no se muestran"
**Causa**: El elemento especificado no esta incluido en la captura de pantalla
**Prompt de solucion**:
```
Analice los elementos de la interfaz de usuario contenidos en la captura de pantalla.
Indiqueme a cuales elementos se les pueden agregar anotaciones, en una lista.
```

### Problema 2: "La posicion de la anotacion es incorrecta"
**Causa**: La descripcion del elemento es inexacta
**Prompt de solucion**:
```
Quiero especificar la posicion del elemento a anotar con mas precision.
Es posible especificar por coordenadas, como
"El boton a aproximadamente 100px desde la izquierda y 50px desde la parte superior de la pantalla"?
```

### Problema 3: "La direccion de la flecha esta invertida"
**Causa**: Los puntos de inicio y fin de la flecha son ambiguos
**Prompt de solucion**:
```
Ajuste la direccion de la flecha.
Indiqueme como especificar explicitamente los puntos de inicio y fin.
```

### Problema 4: "El texto es dificil de leer"
**Causa**: Bajo contraste con el color de fondo
**Prompt de solucion**:
```
Mejore la visibilidad del texto de anotacion.
Indiqueme como ajustar el color de fondo, el tamano de fuente y el color del texto.
```

---

## ✅ Punto de control
- [ ] Puede resaltar botones con el estilo red_box
- [ ] Puede agregar explicaciones con globos de texto usando el estilo callout
- [ ] Puede agregar numeros de paso con el estilo number/circle
- [ ] Puede agregar anotaciones a multiples elementos simultaneamente
- [ ] Puede colocar anotaciones que guien correctamente la mirada del usuario


---

## 📋 Vista previa de resultados

### Salida esperada
```
📁 output/screenshots/
├── analyzed-{nombre-del-objetivo}.png
└── (variaciones)
```
> Formato: PNG | Tamano: Configuracion automatica

### Comandos de verificacion
```bash
# Lista de archivos
ls -la output/screenshots/

# Abrir imagen (macOS: open / Linux: xdg-open)
open output/screenshots/
```

> 💡 **Claude Code**: Especifique la ruta del archivo con la herramienta Read para previsualizar imagenes en el chat
> 💡 **Cursor**: Haga clic en la imagen en el explorador de archivos para previsualizar

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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-3-5)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-3-5
- finish → Finalizar

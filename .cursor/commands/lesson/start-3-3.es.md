---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "~25 min"
level: "intermediate"
tags: ["screenshot", "tutorial", "documentation"]
---

# 🎓 Lesson 3-3: Generacion automatica de tutoriales

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 3-3: Generacion automatica de tutoriales**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Generar automaticamente tutoriales de operacion a partir de capturas de pantalla usando el skill tutorial-generator |
| Duracion | ~25 min |
| Skills utilizados | tutorial-generator (Gemini Vision API) |
| Requisitos previos | Lesson 3-1 completada, clave de Gemini API configurada |
| Pagina del curso | [Module 3: Analisis de capturas](https://ai-agent.camp/es/course/module-3) en paralelo |

**Flujo de la sesion:**
1. Generar tutorial de pantalla de inicio de sesion
2. Crear tutoriales de multiples pasos
3. Salida en formato de manual

Al finalizar esta sesion, podra generar manuales de operacion y documentos de incorporacion.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 📁 Preparar imagenes de muestra

Esta leccion utiliza capturas de pantalla como entrada. Prepare los siguientes materiales en `courses/aiagent/lesson03-core/module03-screenshot/practice/data/`:

- **login-screen.png** — Una captura de pantalla de cualquier pantalla de inicio de sesion
- **signup-form.png** — Una captura de pantalla de cualquier formulario de registro
- **purchase-step1~4.png** — Capturas de pantalla de cada paso del flujo de compra de un sitio de comercio electronico (4 imagenes)

> **Consejo**: Si no tiene capturas de pantalla disponibles, preparelas utilizando uno de los siguientes metodos:
> - Tome capturas de pantalla de cualquier sitio web y guardelas en `practice/data/tutorial-samples/` (macOS: `Cmd+Shift+4`, Windows: `Win+Shift+S`)
> - Generar automaticamente imagenes de muestra usando el skill nanobanana:
>   ```bash
>   uv run python tools/nanobanana.py --prompt "Captura de pantalla de formulario de inicio de sesion con campos de correo y contrasena y boton de inicio de sesion" --output courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login-screen.png
>   uv run python tools/nanobanana.py --prompt "Formulario de registro con campos de nombre, correo y contrasena" --output courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/signup-form.png
>   ```
> - Tambien puede usar imagenes existentes en `practice/data/screenshots/` (`dashboard.png`, `ui-issue.png`, etc.) como alternativas
> - Los activos que no estan en `practice/` pero se necesitan para la capacitacion no deben eliminarse; muevanse como materiales oficiales al directorio `practice/` o `final/` de la leccion correspondiente

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

## 🚀 Step 1: Generar tutorial de pantalla de inicio de sesion

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Generar tutorial de pantalla de inicio de sesion",
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
Utilice el skill tutorial-generator para generar un tutorial de la pantalla de inicio de sesion.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login-screen.png
Salida: output/tutorials/login-tutorial.html

Publico objetivo: Principiantes
Proposito: Explicar el procedimiento de inicio de sesion
Formato de salida: HTML
```

> **Nota**: Al ejecutar scripts, configure PYTHONPATH como `PYTHONPATH=. python skills/tutorial-generator/scripts/generate_tutorial.py ...`.

**Resultado esperado**: Se genera un tutorial de inicio de sesion paso a paso en formato HTML.

---

## 🚀 Step 2: Tutorial con informacion de contexto adicional

Agregue informacion de contexto para explicaciones mas detalladas:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Tutorial con informacion de contexto agregada",
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
Genere un tutorial de la pantalla de registro de usuario.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/signup-form.png
Salida: output/tutorials/signup-tutorial.html

Informacion de contexto:
- Esta es una pantalla de registro de nuevo usuario
- Ingrese correo electronico, contrasena y nombre para registrarse
- La contrasena debe tener 8+ caracteres
- Se requiere verificacion por correo electronico

Cree un tutorial detallado que refleje esta informacion.
```

**Resultado esperado**: Se genera un tutorial con explicaciones detalladas que reflejan la informacion de contexto.

---

## 🚀 Step 3: Generar flujo de operacion de multiples pasos

Genere tutoriales que abarcan multiples pantallas, como flujos de compra de comercio electronico:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Generar un flujo de operacion de multiples pasos",
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
Cree un tutorial del flujo de compra.

Procese en el siguiente orden de pantallas:
1. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step1.png - Seleccion de producto
2. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step2.png - Confirmacion del carrito
3. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step3.png - Entrada de direccion de envio
4. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step4.png - Pago completado

Salida: output/tutorials/purchase-tutorial.html

Explique las operaciones de cada paso en detalle
y compile todo en un unico documento HTML.
```

**Resultado esperado**: Se genera un documento de tutorial con 4 pasos consecutivos.

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
      {"id": "trouble_1", "label": "El tutorial no se genera"},
      {"id": "trouble_2", "label": "La explicacion de la IA es inexacta"},
      {"id": "trouble_3", "label": "Los caracteres japoneses aparecen ilegibles"},
      {"id": "trouble_4", "label": "El procesamiento se detiene a mitad de camino con multiples archivos"}
    ]
  }]
}
```


### Problema 1: "El tutorial no se genera"
**Causa**: El formato del archivo de captura de pantalla no es compatible
**Prompt de solucion**:
```
Indiqueme los formatos de archivo de imagen compatibles.
Ademas, verifique el formato de la captura de pantalla actual.
```

### Problema 2: "Las explicaciones de la IA son inexactas"
**Causa**: La informacion de contexto es insuficiente
**Prompt de solucion**:
```
Que informacion de contexto se debe agregar
para mejorar la precision del tutorial?
Por favor, explique con ejemplos especificos.
```

### Problema 3: "El texto en japones tiene problemas de codificacion"
**Causa**: Problema de codificacion
**Prompt de solucion**:
```
Verifique la codificacion de caracteres del archivo HTML generado.
Verifique que este guardado correctamente en UTF-8 y corrija cualquier problema.
```

### Problema 4: "El procesamiento de multiples archivos se detiene"
**Causa**: Archivo no encontrado o tiempo de espera agotado
**Prompt de solucion**:
```
Verifique que todos los archivos especificados existan.
Genere el tutorial utilizando solo los archivos que existen.
```

---

## ✅ Punto de control
- [ ] Puede generar automaticamente tutoriales a partir de capturas de pantalla
- [ ] Puede generar explicaciones detalladas utilizando informacion de contexto
- [ ] Puede cubrir todo el flujo de operacion de multiples pasos
- [ ] Los tutoriales en formato HTML se muestran correctamente
- [ ] Se generan tutoriales apropiados en japones


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-3-4)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-3-4
- finish → Finalizar

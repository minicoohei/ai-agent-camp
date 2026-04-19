---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
duration: "~25 min"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["screenshot", "analysis", "gemini-vision"]
---

# 🎓 Lesson 3-1: Fundamentos de analisis de capturas de pantalla

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 3-1: Introduccion al analisis de capturas de pantalla**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Analizar automaticamente errores en pantalla y sugerir soluciones usando el Skill screenshot-analyzer |
| Duracion | ~25 min |
| Skills utilizados | screenshot-analyzer (Gemini Vision API) |
| Requisitos previos | Clave de Gemini API configurada, entorno Python configurado |
| Pagina del curso | Consulte [Module 3: Analisis de capturas](https://ai-agent.camp/es/course/module-3) en paralelo |

**Flujo de la sesion:**
1. Preparar capturas de pantalla
2. Analizar pantallas de error y obtener soluciones
3. Aplicar los resultados del analisis

Al finalizar esta sesion, podra obtener resultados de diagnostico de errores y sugerencias de solucion.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificacion de preparacion

Verifiquemos que todo esta listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Esta listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Preparar capturas de pantalla

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Preparar capturas de pantalla",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Verifique si existen imagenes de muestra en courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/.
Si no existen, muestreme como agregar imagenes de capacitacion al mismo directorio
y como mover activos temporales personales a materiales oficiales de la leccion.
```

**Resultado esperado**: Se confirma el estado de la carpeta de entradas y se proporcionan instrucciones para preparar imagenes de prueba segun sea necesario.

---

## 🚀 Step 2: Ejecutar analisis basico de errores

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Ejecutar analisis basico de errores",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Use el Skill screenshot-analyzer para analizar errores de una captura de pantalla.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/error-screenshot.png
Salida: output/screenshots/analyzed-error.png

Analisis:
- Identificar la causa del error
- Sugerir soluciones
- Marcar areas importantes
```

**Resultado esperado**: Las areas de error se marcan con bordes rojos y se genera una imagen con anotaciones de solucion.

---

## 🚀 Step 3: Identificar problemas de interfaz de usuario

Analicemos los problemas de diseno de interfaz de usuario:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Identificar problemas de interfaz de usuario",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Analice los problemas de interfaz de usuario en esta captura de pantalla.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/ui-issue.png
Salida: output/screenshots/ui-issue-annotated.png

Criterios de analisis:
- Ubicacion de botones
- Tamano de fuente
- Contraste de colores
- Usabilidad

Agregue anotaciones a las areas problematicas y presente sugerencias de mejora.
```

**Resultado esperado**: Los problemas de interfaz de usuario se marcan visualmente y se agregan sugerencias de mejora como anotaciones.

---

## ⚠️ Problemas comunes y soluciones

Use AskUserQuestion (AskQuestion) para seleccionar su problema y recibir asistencia guiada.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "Archivo de captura de pantalla no encontrado"},
      {"id": "trouble_2", "label": "Los resultados del analisis son inexactos"},
      {"id": "trouble_3", "label": "Las anotaciones no se muestran"},
      {"id": "trouble_4", "label": "Error de Gemini API"}
    ]
  }]
}
```


### Problema 1: "Archivo de captura de pantalla no encontrado"
**Causa**: La ruta del archivo es incorrecta o el archivo no existe
**Prompt de solucion**:
```
Verifique el contenido de courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/.
Liste los archivos de imagen (.png, .jpg) encontrados alli.
```

### Problema 2: "Los resultados del analisis son inexactos"
**Causa**: La calidad de la captura de pantalla es baja o la informacion es insuficiente
**Prompt de solucion**:
```
Indiqueme que informacion adicional se debe proporcionar
para hacer el analisis de la captura de pantalla mas preciso.
```

### Problema 3: "Las anotaciones no se muestran"
**Causa**: La carpeta de salida no existe
**Prompt de solucion**:
```
Cree la carpeta output/screenshots/.
Si no existe, creela. Si existe, verifique su contenido.
```

### Problema 4: "Error de Gemini API"
**Causa**: La clave de API no esta configurada
**Prompt de solucion**:
```
Verifique si la variable de entorno GEMINI_API_KEY esta configurada.
Si no lo esta, muestreme como configurarla.
```

---

## ✅ Punto de control
- [ ] Puede identificar problemas a partir de capturas de pantalla
- [ ] Puede interpretar correctamente los mensajes de error
- [ ] Puede marcar visualmente las areas problematicas
- [ ] Puede sugerir soluciones especificas
- [ ] Los resultados del analisis se guardaron en la carpeta de salida


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
# Listado de archivos
ls -la output/screenshots/

# Abrir imagenes (macOS: open / Linux: xdg-open)
open output/screenshots/
```

> 💡 **Claude Code**: Especifique la ruta del archivo con la herramienta Read para previsualizar imagenes en el chat
> 💡 **Cursor**: Haga clic en la imagen en el explorador de archivos para previsualizar

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Cursor para verificar la finalizacion:

```
# Verificacion de finalizacion: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Use AskUserQuestion (AskQuestion) para elegir.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccionar siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija su siguiente accion",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-3-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-3-2
- finish → Finalizar

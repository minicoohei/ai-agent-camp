---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "~25 min"
level: "intermediate"
tags: ["screenshot", "error-diagnosis", "analysis"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 3-2: Diagnostico avanzado de errores

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 3-2: Diagnostico avanzado de errores**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Analizar pantallas de error complejas, determinar niveles de prioridad y proponer soluciones |
| Duracion | ~25 min |
| Skills utilizados | screenshot-analyzer (avanzado) |
| Requisitos previos | Lesson 3-1 completada, clave de Gemini API configurada |
| Pagina del curso | [Module 3: Analisis de capturas](https://ai-agent.camp/es/course/module-3) en paralelo |

**Flujo de la sesion:**
1. Analizar errores de respuesta de API
2. Priorizar errores compuestos y determinar soluciones
3. Aplicar a casos de uso del mundo real

Al finalizar esta sesion, podra realizar diagnosticos de errores a nivel de produccion.

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

## 🚀 Step 1: Analizar errores de respuesta API

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Analizar errores de respuesta de API",
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
Utilice el skill screenshot-analyzer para analizar el error de respuesta de la API.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/api-error-response.png
Salida: output/screenshots/api-error-analysis.html

Contenido del analisis:
- Significado de los codigos de error
- Estimacion de la causa raiz
- Determinacion de prioridad (Alta/Media/Baja)
- Pasos de resolucion especificos
```

**Resultado esperado**: Se genera un analisis detallado del error en formato HTML con niveles de prioridad y pasos de resolucion claramente documentados.

---

## 🚀 Step 2: Priorizar multiples errores

Analice pantallas donde ocurren multiples errores simultaneamente:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Priorizar múltiples errores",
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
Analice la captura de pantalla que muestra multiples errores.

Entrada: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/multiple-errors.png
Salida: output/screenshots/error-priority.png

Clasifique los errores por gravedad:
- [Alta] Marco rojo: Accion inmediata requerida
- [Media] Marco amarillo: Accion temprana preferible
- [Baja] Marco azul: Atender cuando haya tiempo

Numere cada error y aclare el orden de respuesta.
```

**Resultado esperado**: Se genera una imagen donde cada error esta codificado por colores, haciendo que la prioridad de respuesta sea clara de un vistazo.

---

## 🚀 Step 3: Diagnosticar patrones de error comunes

Practiquemos el diagnostico de errores HTTP comunes:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Diagnosticar patrones de error comunes",
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
Para los siguientes patrones de error, proponga diagnosticos y soluciones
incluso sin capturas de pantalla:

1. 502 Bad Gateway
2. 503 Service Unavailable
3. 401 Unauthorized
4. Error CORS

Resuma la causa y solucion de cada uno en formato de tabla.
```

**Resultado esperado**: Se muestra una tabla que resume la causa y solucion de cada error.

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
      {"id": "trouble_1", "label": "Los resultados del análisis son demasiado abstractos"},
      {"id": "trouble_2", "label": "No se puede entender la relacion entre multiples errores"},
      {"id": "trouble_3", "label": "No se puede entender los criterios de prioridad"},
      {"id": "trouble_4", "label": "La salida HTML tiene problemas de codificación"}
    ]
  }]
}
```


### Problema 1: "Los resultados del analisis son demasiado abstractos"
**Causa**: Informacion insuficiente en la captura de pantalla
**Prompt de solucion**:
```
Indiqueme que informacion adicional se necesita para un analisis de errores mas preciso.
Tambien sugiera elementos que deben incluirse en la captura de pantalla (registro de consola, pestana de red, etc.).
```

### Problema 2: "No se puede entender la relacion entre multiples errores"
**Causa**: La relacion de cadena de errores es compleja
**Prompt de solucion**:
```
En esta pantalla de error, analice cual es el error raiz
y cuales son los errores derivados.
Diagrame las relaciones causales entre los errores.
```

### Problema 3: "No se puede entender los criterios de prioridad"
**Causa**: Los criterios de evaluacion no son claros
**Prompt de solucion**:
```
Indiqueme los criterios para determinar la prioridad de los errores.
Explique desde las siguientes perspectivas:
- Impacto en el usuario
- Impacto en el negocio
- Gravedad tecnica
- Urgencia de respuesta
```

### Problema 4: "La salida HTML tiene problemas de codificacion"
**Causa**: Problema de codificacion de caracteres
**Prompt de solucion**:
```
El archivo HTML generado tiene problemas de codificacion de caracteres.
Por favor, regenere con codificacion UTF-8.
```

---

## ✅ Punto de control
- [ ] Puede analizar automaticamente capturas de pantalla de errores
- [ ] Puede distinguir entre causas raiz y problemas derivados
- [ ] Puede determinar el orden de respuesta segun la prioridad
- [ ] Puede generar reportes de analisis en formato HTML
- [ ] Puede codificar por colores y visualizar multiples errores


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-3-3)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-3-3
- finish → Finalizar

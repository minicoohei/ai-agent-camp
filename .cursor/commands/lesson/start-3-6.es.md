---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1", "start-3-2", "start-3-3", "start-3-4", "start-3-5"]
duration: "~40 min"
level: "intermediate"
tags: ["screenshot", "capstone", "manual"]
---

# 🎓 Lesson 3-6: Ejercicio resumen de analisis de capturas de pantalla

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 3-6: Ejercicio resumen de analisis de capturas de pantalla**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Integrar todos los skills del Module 3 y completar el proyecto de generacion de manual de operaciones |
| Duracion | ~40 min |
| Skills utilizados | Uso integral de screenshot-analyzer, tutorial-generator y screenshot-annotator |
| Requisitos previos | Lecciones 3-1 a 3-5 completadas, clave de Gemini API configurada |
| Pagina del curso | [Module 3: Analisis de capturas](https://ai-agent.camp/es/course/module-3) en paralelo |

**Flujo de la sesion:**
1. Seleccionar proyecto y organizar requisitos
2. Ejecutar el flujo de trabajo de analisis, tutorial y anotacion
3. Revisar el producto terminado y reflexionar sobre el Module 3

Al finalizar esta sesion, un manual de operaciones practico estara completo y el Module 3 habra finalizado.

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

## 🚀 Step 1: Seleccionar un tema de analisis

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Seleccionar un proyecto",
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
Elija uno de los siguientes proyectos de ejercicio:

[Principiante] Manual de aplicacion web (30-40 min)
- Objetivo: Aplicacion web con aproximadamente 5 funciones
- Entregables: Manual de usuario en formato HTML

[Intermedio] Reporte de diagnostico de errores (40-50 min)
- Objetivo: Multiples pantallas de error
- Entregables: Reporte de diagnostico con prioridades + guia de resolucion

[Avanzado] Soporte multiplataforma (60-90 min)
- Objetivo: Version PC + version movil
- Entregables: Manual completo para ambas plataformas

Por favor, elija que proyecto desea realizar.
Una vez seleccionado, se proporcionaran los pasos detallados para ese proyecto.
```

**Resultado esperado**: Se presentan los pasos detallados de implementacion del proyecto seleccionado.

---

## 🚀 Step 2: Analisis integral de multiples capturas de pantalla

Este es un ejemplo del proyecto principiante:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: [Principiante] Crear un manual de aplicacion web",
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
Crearemos un manual de usuario de Gmail.

Publico objetivo: Principiantes (personas mayores de 60 anos)
Funciones principales:
1. Inicio de sesion
2. Recepcion y lectura de correos
3. Composicion y envio de correos
4. Gestion de etiquetas
5. Busqueda de correos

Requisitos de entregables:
- Manual HTML: Cubrir las 5+ funciones
- Capturas de pantalla: 15+ imagenes
- Resolucion de problemas: 3+ elementos

Asumiendo que las capturas de pantalla de Gmail se han colocado como materiales oficiales en
courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/,
comience a crear el manual.
```

**Resultado esperado**: Se crea un manual de Gmail detallado para personas mayores.

---

## 🚀 Step 3: Crear reporte de analisis y materiales de presentacion

Este es un ejemplo del proyecto intermedio:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: [Intermedio] Crear un reporte de diagnostico de errores",
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
Cree un reporte de diagnostico a partir de multiples pantallas de error del sistema.

Entrada: Todas las imagenes de error en courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/
Salida: output/error-report/

Contenido del reporte:
1. Tabla de lista de errores (prioridad, causa, solucion)
2. Analisis detallado de cada error
3. Diagrama de flujo de respuesta
4. Propuestas de medidas preventivas

Formato de salida:
- Reporte de diagnostico en formato HTML
- Imagenes de error codificadas por color segun prioridad
- Lista de verificacion de respuesta (Markdown)
```

**Resultado esperado**: Se crea un reporte sistematico de diagnostico de errores.

---

## 🚀 Step 4: Revisar entregables y exportar

Revisemos los entregables creados:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Revisar entregables y exportar",
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
Verifique la calidad del manual/reporte creado.

Lista de verificacion:
- [ ] Todas las imagenes se muestran correctamente
- [ ] Sin problemas de codificacion de caracteres
- [ ] Los enlaces funcionan correctamente
- [ ] Legible en dispositivos moviles
- [ ] Lenguaje comprensible para principiantes

Si hay problemas, corrijalos y guarde la version final en output/final/.
```

**Resultado esperado**: La verificacion de calidad esta completa y la version final se ha guardado.

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
      {"id": "trouble_1", "label": "No se puede completar dentro del limite de tiempo"},
      {"id": "trouble_2", "label": "La calidad es insuficiente"},
      {"id": "trouble_3", "label": "La estructura de archivos esta desorganizada"}
    ]
  }]
}
```


- No se puede completar dentro del limite de tiempo
- La calidad es insuficiente
- La estructura de archivos esta desorganizada

### Problema 1: "No se puede completar dentro del limite de tiempo"
**Causa**: El alcance es demasiado grande
**Prompt de solucion**:
```
Verifique el estado de progreso actual.
Reduzca el alcance a lo que se pueda completar en el tiempo restante
y complete solo las partes de alta prioridad.
```

### Problema 2: "La calidad es insuficiente"
**Causa**: Revision insuficiente
**Prompt de solucion**:
```
Para mejorar la calidad del manual,
revise desde las siguientes perspectivas:
- Claridad
- Precision
- Consistencia
- Diseno

Si hay areas de mejora, proporcione sugerencias especificas.
```

### Problema 3: "La estructura de archivos esta desorganizada"
**Causa**: El destino de salida no esta organizado
**Prompt de solucion**:
```
Organice la estructura de archivos del proyecto.

Estructura recomendada:
project-output/
├── README.md
├── screenshots/
├── tutorials/
├── manual/
├── annotations/
└── scripts/

Mueva los archivos para que coincidan con esta estructura.
```

---

## ✅ Punto de control

### Lista de verificacion de finalizacion del Module 3

### Habilidades tecnicas
- [ ] Utilizo screenshot-analyzer 3 o mas veces
- [ ] Utilizo tutorial-generator 3 o mas veces
- [ ] Utilizo screenshot-annotator 5 o mas veces
- [ ] Implemento automatizacion con scripts personalizados
- [ ] Creo un documento HTML integrado

### Entregables
- [ ] Completo un manual de usuario practico
- [ ] Tiene un documento HTML integrado
- [ ] Creo capturas de pantalla anotadas
- [ ] Basado en casos de uso reales

---

## 🎉 Module 3 Completado！

Felicitaciones! Ha dominado las siguientes habilidades:
- Diagnosticar automaticamente las causas de errores a partir de capturas de pantalla
- Generar tutoriales paso a paso
- Ilustrar interfaces de usuario usando anotaciones
- Crear manuales de usuario practicos
- Automatizar procesos complejos


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-4-1)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-4-1
- finish → Finalizar

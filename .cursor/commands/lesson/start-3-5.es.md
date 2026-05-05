---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1", "start-3-2", "start-3-3", "start-3-4"]
duration: "~30 min"
level: "intermediate"
tags: ["screenshot", "batch-processing", "manual"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 3-5: Analisis de resultados de pruebas A/B

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 3-5: Analisis de resultados de pruebas A/B**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Procesar por lotes multiples capturas de pantalla y crear un manual de usuario integrado |
| Duracion | ~30 min |
| Skills utilizados | Integracion de screenshot-analyzer, tutorial-generator y screenshot-annotator |
| Requisitos previos | Lecciones 3-1 a 3-4 completadas, clave de Gemini API configurada |
| Pagina del curso | [Module 3: Analisis de capturas](https://ai-agent.camp/es/course/module-3) en paralelo |

**Flujo de la sesion:**
1. Definir requisitos de creacion del manual
2. Analisis por lotes de multiples capturas de pantalla y diseno de estructura
3. Generar el manual integrado

Al finalizar esta sesion, podra crear manuales de operacion de nivel profesional.

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

## 🚀 Step 1: Analizar pantallas de pruebas A/B

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Definir requisitos de creacion del manual",
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
Crearemos un manual de usuario de la aplicacion web.

Funciones objetivo:
1. Inicio de sesion
2. Panel de control
3. Entrada de datos
4. Generacion de reportes
5. Configuracion de usuario

Las capturas de pantalla de cada funcion se colocan como materiales oficiales en `courses/aiagent/lesson03-core/module03-screenshot/practice/data/`.
Los recursos que no estan en `practice/` pero son necesarios para la capacitacion deben moverse al directorio `practice/` o `final/` correspondiente antes de usarlos.

Cree un plan de creacion del manual:
- Numero de capturas de pantalla necesarias para cada funcion
- Orden de generacion de tutoriales
- Metodo de integracion
```

**Resultado esperado**: Se presenta un plan detallado de creacion del manual.

---

## 🚀 Step 2: Evaluacion de significancia estadistica

Genere tutoriales por lotes a partir de multiples capturas de pantalla:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Generar tutoriales por lotes",
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
Genere tutoriales por lotes a partir de las siguientes capturas de pantalla.

Archivos de entrada:
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/dashboard.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/data-input.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/report.png

Salida: output/manual/

Para cada archivo:
1. Generar tutorial con tutorial-generator
2. Agregar anotaciones a las areas clave con screenshot-annotator
3. Guardar en formato HTML

Informe el progreso durante la ejecucion.
```

**Resultado esperado**: Se generan tutoriales para cada captura de pantalla y se reporta el progreso.

---

## 🚀 Step 3: Generar reporte de analisis

Aplique estilos de anotacion consistentes a todas las imagenes:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Agregar anotaciones por lotes",
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
Para las imagenes PNG en courses/aiagent/lesson03-core/module03-screenshot/practice/data/,
resalte los botones de accion importantes con marcos rojos.

Salida: output/annotated/

Para cada imagen:
- Detectar automaticamente los botones de accion principales
- Resaltar con estilo red_box
- Agregar descripciones de operacion con globos de texto

Muestre la lista de imagenes procesadas.
```

**Resultado esperado**: Se agregan anotaciones a todas las imagenes con un estilo consistente.

---

## 🚀 Step 4: Integrar en un manual HTML

Integre el contenido generado en un solo documento HTML:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Integrar en un manual HTML",
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
Integre los tutoriales generados y las imagenes anotadas
en un unico manual HTML.

Archivos a integrar:
- output/manual/*.html (tutoriales)
- output/annotated/*.png (imagenes anotadas)

Salida: output/complete-manual.html

Estructura:
1. Tabla de contenidos (enlaces a cada funcion)
2. Tutorial de cada funcion
3. Seccion de resolucion de problemas
4. Preguntas frecuentes

Cree con un lenguaje accesible para principiantes.
```

**Resultado esperado**: Se genera un manual HTML completo con tabla de contenidos.

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
      {"id": "trouble_1", "label": "Se produce un error durante el procesamiento por lotes"},
      {"id": "trouble_2", "label": "El manual es demasiado largo"},
      {"id": "trouble_3", "label": "El HTML no se muestra correctamente"},
      {"id": "trouble_4", "label": "Las imagenes no se muestran"}
    ]
  }]
}
```


### Problema 1: "Se produce un error durante el procesamiento por lotes"
**Causa**: Algunas rutas de archivo son incorrectas
**Prompt de solucion**:
```
Verifique la lista de archivos a procesar.
Si algun archivo no existe, informelo
y continue el procesamiento solo con los archivos existentes.
```

### Problema 2: "El manual es demasiado largo"
**Causa**: Demasiada informacion lo hace dificil de leer
**Prompt de solucion**:
```
Divida el manual de la siguiente manera:
- Basico (solo operaciones esenciales)
- Avanzado (configuracion detallada)
- Administrador (funciones de gestion)

Genere cada parte como un archivo HTML separado.
```

### Problema 3: "El HTML no se muestra correctamente"
**Causa**: Error de estructura de etiquetas HTML
**Prompt de solucion**:
```
Valide la estructura del archivo HTML generado.
Si hay errores, corrijalos y regenere en formato HTML5 correcto.
```

### Problema 4: "Las imagenes no se muestran"
**Causa**: Las rutas de imagen son relativas y no se resuelven correctamente
**Prompt de solucion**:
```
Verifique las rutas de las imagenes en el manual HTML.
Verifique que todas las imagenes esten referenciadas correctamente
y corrija las rutas segun sea necesario.
```

---

## ✅ Punto de control
- [ ] Puede definir los requisitos de creacion del manual
- [ ] Puede procesar multiples archivos por lotes
- [ ] Puede combinar eficientemente la generacion automatica con la edicion manual
- [ ] Puede integrar en un documento HTML
- [ ] Puede crear un manual con tabla de contenidos y estructura


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-3-6)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-3-6
- finish → Finalizar

---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
prerequisites: ["start-12-1"]
duration: "~30 min"
level: "intermediate"
tags: ["notion", "database", "automation"]
---

# 🎓 Lesson 12-2: Operaciones de base de datos de Notion

## 📍 Lo que hara en esta sesion

**Lección 12-2: Operaciones de base de datos de Notion**!

| Elemento | Contenido |
|------|------|
| Objetivo | Automatizar la creacion, consulta y actualizacion de bases de datos de Notion, y operar la gestion de tareas desde Claude Code |
| Duracion | ~30 min |
| Habilidades utilizadas | Notion API (bases de datos) |
| Requisitos previos | Leccion 12-1 completada, integracion de Notion creada |
| Pagina del curso | [Module 12: Notion](https://ai-agent.camp/es/course/module-12)  como referencia paralela |

**Flujo de la sesion:**
1. Crear una base de datos de gestión de tareas
2. Consultas y filtros
3. Añadir, actualizar y eliminar registros

Al final de esta sesion, podra gestionar tareas y proyectos de Notion desde codigo.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un mal funcionamiento.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
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

## 🚀 Step 1: Create Task Management Database

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Crear base de datos de gestión de tareas",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, cree la siguiente base de datos en Notion:

Nombre de la base de datos: Tareas del proyecto

Propiedades:
1. Nombre de la tarea (Title)
2. Estado (Select)
   - No iniciado (gris)
   - En progreso (azul)
   - En revisión (amarillo)
   - Completado (verde)
3. Fecha límite (Date)
4. Prioridad (Select)
   - Urgente (rojo)
   - Alta (naranja)
   - Media (amarillo)
   - Baja (gris)
5. Horas estimadas (Number) - en horas
6. Categoría (Multi-select)
   - Desarrollo
   - Diseño
   - Planificación
   - Documentación
```

**Resultado esperado:** Se crea una base de datos con propiedades en Notion.

---

## 🚀 Step 2: Add Sample Tasks

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Añadir tareas de ejemplo",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, añada las siguientes tareas a la base de datos "Tareas del proyecto":

1. Nombre de la tarea: Crear documentación API
   - Estado: No iniciado
   - Fecha límite: Próximo viernes
   - Prioridad: Alta
   - Horas estimadas: 4
   - Categoría: Documentación

2. Nombre de la tarea: Implementar autenticación de usuario
   - Estado: En progreso
   - Fecha límite: 3 días después
   - Prioridad: Urgente
   - Horas estimadas: 8
   - Categoría: Desarrollo

3. Nombre de la tarea: Crear mockup de interfaz
   - Estado: No iniciado
   - Fecha límite: 5 días después
   - Prioridad: Media
   - Horas estimadas: 6
   - Categoría: Diseño

Después de añadir, muestre el contenido de la base de datos.
```

**Resultado esperado:** Se anaden 3 tareas a la base de datos.

---

## 🚀 Step 3: Data Retrieval and Filtering

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Obtención de datos y filtrado",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, obtenga tareas de la base de datos "Tareas del proyecto" con las siguientes condiciones:

Consulta 1: Obtener todas las tareas
- Obtener y mostrar todas las tareas

Consulta 2: Solo tareas incompletas
- Obtener tareas cuyo estado no sea "Completado"

Consulta 3: Tareas de alta prioridad
- Obtener tareas con prioridad "Urgente" o "Alta"
- Ordenar por fecha límite

Muestre cada resultado en formato de tabla.
```

**Resultado esperado:** Se obtienen y muestran las tareas que coinciden con las condiciones.

---

## 🚀 Step 4: Update Tasks

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Actualizar tareas",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, realice las siguientes actualizaciones en la base de datos "Tareas del proyecto":

1. Tarea "Crear documentación API"
   - Cambiar estado a "En progreso"

2. Tarea "Implementar autenticación de usuario"
   - Cambiar estado a "En revisión"
   - Actualizar horas estimadas a 10 (el tiempo real aumentó)

Después de actualizar, muestre el estado de todas las tareas.
```

**Resultado esperado:** Los estados de las tareas se actualizan.

---

## 🚀 Step 5: Aggregation and Report

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Agregación e informe",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, cree un informe de agregación de la base de datos "Tareas del proyecto":

Contenido de la agregación:
1. Cantidad de tareas por estado
   - No iniciado: X elementos
   - En progreso: X elementos
   - En revisión: X elementos
   - Completado: X elementos

2. Total de horas estimadas por categoría
   - Desarrollo: X horas
   - Diseño: X horas
   - Planificación: X horas
   - Documentación: X horas

3. Tasa de finalización
   - Tareas completadas / Total de tareas = X%

4. Lista de tareas con fecha límite esta semana
   - Mostrar nombre de la tarea, prioridad, estado

Por favor, genere el informe en un formato legible.
```

**Resultado esperado:** Las estadisticas de la base de datos se generan en formato de informe.

---

## ⚠️ Problemas comunes y soluciones

Utilice AskQuestion para seleccionar el problema y luego siga las indicaciones.

**Configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "Database not found"},
      {"id": "trouble_2", "label": "No se pueden crear propiedades"},
      {"id": "trouble_3", "label": "Los filtros no funcionan"},
      {"id": "trouble_4", "label": "La especificación de fecha no funciona"}
    ]
  }]
}
```


### Problema 1: "Database not found"
**Causa:** El ID de la base de datos es incorrecto o no hay permisos de acceso
**Prompt de solucion:**
```
Por favor, verifique lo siguiente:
1. La integración se ha añadido a la página donde existe la base de datos
2. El nombre de la base de datos es correcto
3. La integración se ha añadido a la página principal
```

### Problema 2: No se pueden crear propiedades
**Causa:** La especificacion del tipo de propiedad es incorrecta
**Prompt de solucion:**
```
Por favor, verifique los tipos de propiedad soportados por la API de Notion:
- title, rich_text, number, select, multi_select, date, people, checkbox, etc.
Las opciones de Select/Multi-select deben definirse previamente.
```

### Problema 3: Los filtros no funcionan
**Causa:** La sintaxis del filtro es incorrecta
**Prompt de solucion:**
```
Por favor, verifique la sintaxis de filtros de la API de Notion:
- Condición única: {"property": "Status", "select": {"equals": "Completado"}}
- Múltiples condiciones: {"and": [condición1, condición2]}
```

### Problema 4: La especificacion de fecha no funciona correctamente
**Causa:** El formato de fecha es incorrecto
**Prompt de solucion:**
```
Por favor, especifique las fechas de la API de Notion en formato ISO 8601:
- Solo fecha: "2024-01-15"
- Fecha y hora: "2024-01-15T09:00:00"
También considere la zona horaria.
```

---

## ✅ Punto de control
- [ ] Se puede crear la base de datos
- [ ] Se pueden añadir tareas
- [ ] El filtrado funciona
- [ ] Se pueden actualizar tareas
- [ ] Se puede generar el informe de agregación

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado:** Se muestran el estado completado/incompleto y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Utilice AskQuestion para elegir.

**Configuracion de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-6-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-6-1
- finish → Finalizar

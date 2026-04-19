---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
prerequisites: ["start-9-1"]
duration: "~25 min"
level: "intermediate"
tags: ["slack", "task", "todo", "extraction"]
---

# 🎓 Lesson 9-2: Resumen y reporte de canales de Slack

## 📍 Lo que hara en esta sesion

**Lesson 9-2: Extraccion de tareas de Slack** !

| Elemento | Contenido |
|------|------|
| Objetivo | Extraer TODOs/tareas de Slack, determinar prioridades y generar informes de tareas |
| Duracion | ~25 min |
| Habilidades utilizadas | slack-task-manager, check-inbox |
| Requisitos previos | Lesson 9-1 completada, API de Slack configurada |
| Pagina del curso | [Module 9: Busqueda en Slack](https://ai-agent.camp/es/course/module-9) como referencia paralela |

**Flujo de la sesion:**
1. Detectar menciones y elementos de accion
2. Determinar prioridad y generar lista de tareas
3. Generar y utilizar informes de tareas

Al final de esta sesion, podra rastrear automaticamente las respuestas pendientes y los TODOs de Slack.

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

## 🚀 Step 1: Check Mentions to Yourself

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Verificar menciones dirigidas a usted",
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
Por favor, busque las menciones dirigidas a usted en Slack.
Busque usando los siguientes patrones de nombre de usuario:
- @YourName (reemplace con su nombre de usuario)
- @SuNombreParaMostrar

Resuma las menciones de la última semana por canal.
```

**Resultado esperado:** Se muestra una lista de menciones dirigidas a usted.

---

## 🚀 Step 2: Extract Action Items

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Extraer elementos de acción",
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
Por favor, extraiga TODOs de los mensajes de Slack usando los siguientes patrones:

Patrones de búsqueda:
- "por favor haga ~" "le solicito ~"
- "por favor confirme" "por favor revise"
- "por favor atienda" "urgente"
- Mensajes de solicitud con menciones a usted

Dirija la búsqueda a los de las últimas 2 semanas.
```

**Resultado esperado:** Se extraen los mensajes que contienen elementos de accion.

---

## 🚀 Step 3: Priority Assessment

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Evaluación de prioridad",
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
Por favor, evalúe la prioridad de los TODOs extraídos usando los siguientes criterios:

Prioridad alta:
- Contiene "urgente" "hoy" "ASAP" "emergencia"
- Menciones de ejecutivos o supervisores

Prioridad media:
- Plazo explícitamente indicado
- Contiene "esta semana" "para la próxima semana"

Prioridad baja:
- Sin plazo
- Solo información compartida

Muestre la cantidad y el contenido por cada nivel de prioridad.
```

**Resultado esperado:** Los TODOs se clasifican por prioridad.

---

## 🚀 Step 4: Check Thread Replies

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Verificar respuestas del hilo",
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
Por favor, verifique el hilo de cada TODO extraído:

Elementos a verificar:
- Si ha sido atendido (respuestas con "completado" "gestionado" etc.)
- Si hay solicitudes adicionales
- Si ha quedado sin respuesta

Clasifique los TODOs por estado de respuesta:
- Atendido
- En progreso
- No atendido
```

**Resultado esperado:** Se determina el estado de los TODOs.

---

## 🚀 Step 5: Generate Task Report

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Generar informe de tareas",
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
Por favor, compile los TODOs extraídos en un informe Markdown con el siguiente formato:

# Informe de TODOs de Slack
Fecha de generación: (fecha/hora actual)

## Resumen
- Prioridad alta: X elementos
- Prioridad media: X elementos
- Prioridad baja: X elementos
- No atendidos: X elementos

## Prioridad alta (Detalles)
### 1. (Nombre de la tarea)
- Canal: #...
- Solicitante: @...
- Fecha/hora: ...
- Contenido: ...
- Estado: No atendido/En progreso/Completado

(continúa a continuación)

Salida: ~/ai-agent-camp/output/slack_todo_report.md
```

**Resultado esperado:** La lista de TODOs se guarda como un informe Markdown.

---

## 🚀 Step 6: Automate Periodic Reports

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 6: Automatizar informes periódicos",
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
Por favor, cree un script de Python para generar automáticamente
un informe de TODOs cada lunes.

Funcionalidades:
- Extraer TODOs de los datos de sincronización de Slack
- Evaluación de prioridad y verificación de estado
- Generación de informe Markdown
- Mostrar diferencias con informes anteriores

Salida: ~/ai-agent-camp/tools/slack_todo_extractor.py
```

**Resultado esperado:** Se crea un script Python para automatizacion.

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
      {"id": "trouble_1", "label": "Mentions not detected"},
      {"id": "trouble_2", "label": "Japanese pattern not working"},
      {"id": "trouble_3", "label": "Cannot retrieve thread information"},
      {"id": "trouble_4", "label": "There are many TODOs"}
    ]
  }]
}
```


### Problema 1: "No se detectan las menciones"
**Causa:** El formato del ID de usuario de Slack es diferente
**Prompt de solucion:**
```
Por favor, verifique el formato de mención de Slack.
Muestre cómo buscar tanto el formato de User ID como <@U12345678>
como el formato @NombreMostrado.
```

### Problema 2: "Los patrones en japones no funcionan"
**Causa:** Problema de codificacion de expresiones regulares
**Prompt de solucion:**
```
Los patrones de expresiones regulares en japonés no funcionan.
Por favor, muestre cómo buscar usando el flag re.UNICODE.
```

### Problema 3: "No se puede obtener la informacion del hilo"
**Causa:** La sincronizacion de hilos esta deshabilitada
**Prompt de solucion:**
```
Por favor, muestre cómo obtener información de hilos de Slack.
También muestre cómo habilitar threads en la configuración de slack-sync.
```

### Problema 4: "Demasiados TODOs"
**Causa:** El filtrado es insuficiente
**Prompt de solucion:**
```
Hay demasiados TODOs para gestionar.
Por favor, añada los siguientes filtros:
- Reducir el rango de fechas (últimos 3 días)
- Mostrar solo prioridad alta
- Dirigirse solo a canales específicos
```

---

## ✅ Punto de control
- [ ] Se detectaron menciones dirigidas a mi
- [ ] Se extrajeron mensajes con patrones TODO
- [ ] Se determinaron las prioridades
- [ ] Se confirmo el estado de respuestas del hilo
- [ ] Se genero el informe Markdown
- [ ] Se identificaron las tareas sin resolver


---

## 📋 Vista previa de entregables

Los entregables de esta leccion son salidas de terminal.

### Ejemplo de salida esperada
```
┌─────────────────────────────────────┐
│  Resultado de la ejecución               │
│  Estado: ✅ Éxito                        │
│  Registros procesados: N                 │
└─────────────────────────────────────┘
```

> 💡 Para guardar la salida en un archivo, agregue ` > output/result.txt` al final del comando

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado:** Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-10-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-10-1
- finish → Finalizar

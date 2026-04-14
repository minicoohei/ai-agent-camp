---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
prerequisites: ["start-0-4"]
duration: "~25 min"
level: "intermediate"
tags: ["slack", "search", "bookrag"]
---

# 🎓 Lesson 9-1: Busqueda en Slack

## 📍 Lo que hara en esta sesion

**Lesson 9-1: Busqueda extendida por palabras clave en Slack** !

| Elemento | Contenido |
|------|------|
| Objetivo | Realizar busqueda extendida por palabras clave en canales y mensajes con slack-search |
| Duracion | ~25 min |
| Habilidades utilizadas | slack-search (BookRAG) |
| Requisitos previos | API de Slack configurada (Lesson 0-4), es recomendable tener datos en data/slack-sync |
| Pagina del curso | [Module 9: Busqueda en Slack](https://ai-agent.camp/es/course/module-9) como referencia paralela |

**Flujo de la sesion:**
1. Fundamentos de busqueda en Slack y verificacion de indices
2. Ejecutar busquedas por palabras clave y semanticas
3. Utilizar los resultados de busqueda

Al final de esta sesion, podra buscar conversaciones de Slack usando busqueda extendida por palabras clave (busqueda de similitud basada en SequenceMatcher).

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

## 🚀 Step 1: Verify Slack Sync Data

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Verificar datos sincronizados de Slack",
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
Por favor, verifique la carpeta ~/ai-agent-camp/data/slack-sync/data/.
Proporcione la siguiente información:
- Lista de canales sincronizados
- Número total de archivos de mensajes
- Fecha/hora de la última sincronización
```

**Resultado esperado:** Se muestra el estado de sincronizacion de datos de Slack. Si no esta sincronizado, se requiere configuracion.

---

## 🚀 Step 2: Run Keyword Search

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Ejecutar búsqueda por palabras clave",
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
Por favor, busque mensajes que contengan la palabra clave "progreso del proyecto" en Slack.
Muestre los de la última semana en el siguiente formato:
- Nombre del canal
- Fecha/hora
- Autor
- Contenido del mensaje (hasta 100 caracteres)
```

**Resultado esperado:** Se muestra una lista de mensajes coincidentes.

---

## 🚀 Step 3: Channel-Specific Search

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Búsqueda por canal específico",
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
Por favor, busque en un canal específico de Slack:
- Canal: #general (o un nombre de canal existente)
- Palabras clave: reunión OR conferencia
- Período: Últimas 2 semanas

Organice los mensajes encontrados cronológicamente.
```

**Resultado esperado:** Se muestran los resultados de busqueda del canal especificado.

---

## 🚀 Step 4: User-Specific Search

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Búsqueda por usuario",
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
Por favor, busque mensajes de un usuario específico en Slack:
- Usuario objetivo: @YourName (reemplace con su nombre de usuario)
- Palabras clave de búsqueda: revisión OR confirmación
- Período: Último mes

Ordene los resultados por importancia.
```

**Resultado esperado:** Se extraen los mensajes del usuario especificado.

---

## 🚀 Step 5: Using Extended Keyword Search

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Uso de búsqueda extendida por palabras clave",
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
Por favor, realice una búsqueda extendida por palabras clave de mensajes relacionados con "retroalimentación de clientes" en Slack.

Incluya también los siguientes sinónimos en la búsqueda:
- retroalimentación, opiniones, solicitudes, quejas, impresiones
- clientes, consumidores

Clasifique los resultados de búsqueda por categoría (positivo/negativo/neutral).
```

**Resultado esperado:** Los mensajes semanticamente relacionados se clasifican y muestran.

---

## 🚀 Step 6: Convert Search Results to Report

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 6: Convertir resultados de búsqueda en informe",
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
Por favor, compile los resultados de búsqueda anteriores en un informe Markdown.

Utilice el siguiente formato:
# Informe de búsqueda de Slack
Fecha de generación: (fecha/hora actual)

## Criterios de búsqueda
- Palabras clave: ...
- Período: ...

## Resumen de resultados
- Total de registros: ...
- Desglose por canal: ...

## Detalles
(Lista de mensajes)

Salida: ~/ai-agent-camp/output/slack_search_report.md
```

**Resultado esperado:** Los resultados de busqueda se compilan en un informe Markdown.

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
      {"id": "trouble_1", "label": "Sync data not found"},
      {"id": "trouble_2", "label": "Search results are few"},
      {"id": "trouble_3", "label": "Japanese search not working well"},
      {"id": "trouble_4", "label": "Don't know the specific user's ID"}
    ]
  }]
}
```


### Problema 1: "No se encuentran datos sincronizados"
**Causa:** La configuracion de slack-sync no esta completa
**Prompt de solucion:**
```
Por favor, verifique el estado de configuración de slack-sync.
Explique la estructura y los archivos necesarios en la carpeta ~/ai-agent-camp/data/slack-sync/.
```

### Problema 2: "Muy pocos resultados de busqueda"
**Causa:** Las condiciones de busqueda son demasiado estrictas
**Prompt de solucion:**
```
Para aumentar los resultados de búsqueda, intente lo siguiente:
- Ampliar el período de búsqueda a 1 mes
- Cambiar las palabras clave a unas más generales
- Eliminar la especificación de canal
```

### Problema 3: "La busqueda en japones no funciona bien"
**Causa:** Problema de codificacion o tokenizacion
**Prompt de solucion:**
```
La búsqueda con palabras clave en japonés no funciona bien.
Intente lo siguiente:
- Buscar usando tanto hiragana como katakana
- Dividir las palabras clave en segmentos más cortos
- Usar búsqueda de coincidencia parcial
```

### Problema 4: "No se el ID del usuario especifico"
**Causa:** Es necesario identificar el ID de usuario de Slack
**Prompt de solucion:**
```
Por favor, muestre cómo verificar el Slack User ID.
Busque su User ID en el archivo users.json.
```

---

## ✅ Punto de control
- [ ] Se confirmo la ubicacion de los datos sincronizados de Slack
- [ ] Se ejecuto exitosamente la busqueda por palabras clave
- [ ] Se busco exitosamente por canal especificado
- [ ] Se busco exitosamente por usuario
- [ ] Se utilizo exitosamente la busqueda expandida por palabras clave
- [ ] Se compilaron exitosamente los resultados de busqueda en un informe


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-9-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-9-2
- finish → Finalizar

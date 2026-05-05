---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module10-gas"
duration: "~25 min"
prerequisites: ["start-10-1"]
level: "intermediate"
tags: ["gas", "gmail", "sheets", "automation", "clasp"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 10-4: Busqueda y extraccion de correos con GmailApp → Organizacion en hoja de calculo

## 📍 Lo que hara en esta sesion

**Lesson 10-4: Busqueda y extraccion de correos con GmailApp → Organizacion en hoja de calculo**!

| Elemento | Contenido |
|------|------|
| Objetivo | Buscar y extraer correos con GmailApp de GAS y organizarlos automaticamente en una hoja de calculo |
| Duracion | ~25 min |
| Habilidades utilizadas | GAS (GmailApp, SpreadsheetApp), clasp |
| Requisitos previos | Lesson 10-1 completada (clasp autenticado) |

**Flujo de la sesion:**
1. Agregar scope de Gmail a appsscript.json
2. Buscar correos con GmailApp.search()
3. Extraer informacion de hilos/mensajes
4. Escribir datos en hoja de calculo con SpreadsheetApp
5. Configurar trigger de ejecucion periodica

Al final de esta sesion, tendra un script de GAS completo que busca y extrae correos automaticamente y los organiza en una hoja de calculo.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar.

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
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Verificar que Lesson 10-1 este completada. Verificar estado de autenticacion con `clasp login --status`)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Agregar scope de Gmail a appsscript.json

```json
{
  "title": "🚀 Step 1: Agregar scope de Gmail",
  "questions": [{
    "id": "step_action",
    "prompt": "Se agregara el scope de lectura de Gmail a appsscript.json.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Ver el appsscript.json actual"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**

Agregar lo siguiente a `oauthScopes` en `gas-example/appsscript.json`:

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/script.scriptapp"
  ]
}
```

Despues de agregar, desplegar con `clasp push`:

```bash
cd gas-example && npx -y @google/clasp push
```

**Resultado esperado**: El scope `gmail.readonly` se agrega a `appsscript.json` y el push se realiza correctamente.

---

## 🚀 Step 2: Buscar correos con GmailApp.search()

```json
{
  "title": "🚀 Step 2: Busqueda de correos",
  "questions": [{
    "id": "step_action",
    "prompt": "Se creara una funcion para buscar correos usando GmailApp.search().",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Ver sintaxis de consultas de busqueda de Gmail"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**

Crear la funcion `searchEmails` en `gas-example/Gmail.gs`:

```javascript
function searchEmails(query, maxResults) {
  query = query || "is:unread newer_than:7d";
  maxResults = maxResults || 50;
  var threads = GmailApp.search(query, 0, maxResults);
  Logger.log("Resultados de busqueda: " + threads.length + " hilos");
  return threads;
}
```

**Ejemplos de consultas de busqueda de Gmail:**

| Consulta | Significado |
|--------|------|
| `is:unread` | Correos no leidos |
| `newer_than:7d` | Ultimos 7 dias |
| `from:example@company.com` | Remitente especifico |
| `subject:reunion` | Asunto que contiene "reunion" |
| `has:attachment` | Con archivo adjunto |
| `is:unread newer_than:3d` | Condicion compuesta |

`clasp push` → `clasp open` para abrir el editor de GAS, ejecutar `searchEmails` y verificar los logs.

**Resultado esperado**: Se muestra en los logs el numero de hilos encontrados.

---

## 🚀 Step 3: Extraccion de informacion de correos

```json
{
  "title": "🚀 Step 3: Extraccion de informacion de correos",
  "questions": [{
    "id": "step_action",
    "prompt": "Se extraera informacion de los hilos (remitente, asunto, fecha, cuerpo).",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Ver la API de GmailMessage"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**

Agregar la funcion `extractEmailData`:

```javascript
function extractEmailData(threads) {
  var data = [];
  threads.forEach(function(thread) {
    var messages = thread.getMessages();
    var lastMessage = messages[messages.length - 1];
    data.push({
      subject: lastMessage.getSubject(),
      from: lastMessage.getFrom(),
      date: lastMessage.getDate(),
      body: lastMessage.getPlainBody().substring(0, 200),
      isUnread: lastMessage.isUnread(),
      messageCount: messages.length
    });
  });
  return data;
}
```

**Metodos principales:**

| Metodo | Contenido obtenido |
|---------|---------|
| `getSubject()` | Asunto |
| `getFrom()` | Remitente |
| `getDate()` | Fecha y hora |
| `getPlainBody()` | Cuerpo (texto) |
| `isUnread()` | Si esta no leido |
| `getMessages().length` | Numero de mensajes en el hilo |

**Resultado esperado**: La informacion de correos se extrae como un array de objetos.

---

## 🚀 Step 4: Escribir datos en hoja de calculo

```json
{
  "title": "🚀 Step 4: Escribir en la hoja",
  "questions": [{
    "id": "step_action",
    "prompt": "Se escribiran los datos de correos extraidos en una hoja de calculo.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Ver la API de SpreadsheetApp"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**

Agregar la funcion `writeToSheet` y la funcion principal `extractAndOrganizeEmails`:

```javascript
function writeToSheet(data, sheetName) {
  sheetName = sheetName || "Lista_correos_" + Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyy-MM-dd");
  var ss = SpreadsheetApp.create(sheetName);
  var sheet = ss.getActiveSheet();

  // Fila de encabezado
  var headers = ["Asunto", "Remitente", "Fecha", "Cuerpo (primeros 200 caracteres)", "Estado", "N. de mensajes"];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");

  // Filas de datos
  if (data.length > 0) {
    var rows = data.map(function(item) {
      return [
        item.subject, item.from,
        Utilities.formatDate(item.date, "Asia/Tokyo", "yyyy-MM-dd HH:mm"),
        item.body, item.isUnread ? "No leido" : "Leido", item.messageCount
      ];
    });
    sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
  }

  Logger.log("Hoja creada: " + ss.getUrl());
  return ss.getUrl();
}

function extractAndOrganizeEmails() {
  var threads = searchEmails("is:unread newer_than:7d", 50);
  var data = extractEmailData(threads);
  var url = writeToSheet(data);
  Logger.log("Proceso completado: " + data.length + " correos organizados en la hoja");
}
```

`clasp push` → `clasp open` para ejecutar `extractAndOrganizeEmails`.

**Resultado esperado**: Se crea en Google Drive una hoja de calculo llamada "Lista_correos_YYYY-MM-DD" con la informacion de correos organizada.

---

## 🚀 Step 5: Configuracion de trigger de ejecucion periodica

```json
{
  "title": "🚀 Step 5: Configuracion de trigger",
  "questions": [{
    "id": "step_action",
    "prompt": "Se configurara un trigger para ejecutar automaticamente la organizacion de correos todos los dias a las 9:00.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Ver especificaciones de ScriptApp.newTrigger"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**

```javascript
function setEmailExtractTrigger() {
  // Eliminar triggers existentes
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    if (trigger.getHandlerFunction() === "extractAndOrganizeEmails") {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Crear nuevo trigger
  ScriptApp.newTrigger("extractAndOrganizeEmails")
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();

  Logger.log("Trigger configurado para las 9:00 todos los dias");
}
```

`clasp push` → `clasp open` para ejecutar `setEmailExtractTrigger`.

**Resultado esperado**: En la pantalla "Triggers" del editor de GAS se muestra un trigger de tipo temporal para las 9:00 diarias.

---

## ⚠️ Problemas comunes y soluciones

```json
{
  "title": "⚠️ Solucion de problemas",
  "questions": [{
    "id": "trouble",
    "prompt": "Ha ocurrido algun problema?",
    "options": [
      {"id": "trouble_1", "label": "Error de permisos de Gmail"},
      {"id": "trouble_2", "label": "No se crea la hoja de calculo"},
      {"id": "trouble_3", "label": "Caracteres incorrectos en japones"},
      {"id": "trouble_4", "label": "El trigger no funciona"}
    ]
  }]
}
```

### Problema 1: "Error de permisos de Gmail"
**Causa**: El scope `gmail.readonly` no se ha agregado a `appsscript.json`, o la autorizacion de la primera ejecucion no se ha completado.
**Prompt de solucion**:
```text
Verifique que "https://www.googleapis.com/auth/gmail.readonly" este incluido en oauthScopes de appsscript.json. Si no esta, agreguelo y ejecute clasp push. En la primera ejecucion, ejecute la funcion en el editor de GAS y complete el dialogo de autorizacion de permisos.
```

### Problema 2: "No se crea la hoja de calculo"
**Causa**: Falta el scope `spreadsheets`, o los resultados de busqueda de correos son 0.
**Prompt de solucion**:
```text
Verifique que "https://www.googleapis.com/auth/spreadsheets" este en oauthScopes. Tambien intente ampliar el rango de la consulta de busqueda de searchEmails a "newer_than:30d" y vuelva a ejecutar.
```

### Problema 3: "Caracteres incorrectos en japones"
**Causa**: Problema de codificacion de `getPlainBody()`.
**Prompt de solucion**:
```text
En lugar de getPlainBody(), use getBody() y agregue una funcion auxiliar para eliminar las etiquetas HTML.
```

### Problema 4: "El trigger no funciona"
**Causa**: Permisos insuficientes para el trigger, o hay un error en el script.
**Prompt de solucion**:
```text
Verifique los logs de error en la pantalla "Ejecuciones" del editor de GAS. Tambien verifique que el scope de ScriptApp este incluido en appsscript.json.
```

---

## ✅ Punto de control

- [ ] Se ha agregado el scope de Gmail a `appsscript.json`
- [ ] La funcion `searchEmails` puede buscar correos
- [ ] La funcion `extractEmailData` puede extraer remitente, asunto, fecha y cuerpo
- [ ] `extractAndOrganizeEmails` genera una hoja de calculo
- [ ] Se ha configurado el trigger de ejecucion periodica

---

## 📋 Vista previa de entregables

**Archivos creados:**
```text
gas-example/
├── appsscript.json   # Con scope de Gmail agregado
├── Calendar.gs       # Entregable de Lesson 10-2
├── Sheets.gs         # Entregable de Lesson 10-3
└── Gmail.gs          # Entregable de esta leccion (5 funciones)
```

**Hoja de calculo generada:**

| Asunto | Remitente | Fecha | Cuerpo (primeros 200 caracteres) | Estado | N. de mensajes |
|------|--------|------|---------------------|------|-------------|
| Informe semanal | alice@co.com | 2026-04-14 10:30 | Buen trabajo. Esta semana... | No leido | 3 |
| Acta de reunion | bob@co.com | 2026-04-13 15:00 | La reunion de hoy... | Leido | 1 |

---

## ➡️ Siguientes pasos

```json
{
  "title": "➡️ Siguientes pasos",
  "questions": [{
    "id": "next_step",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_auto", "label": "Avanzar a Module 11 (GitHub Actions) → /start-11-1"},
      {"id": "review_module", "label": "Revisar los entregables de Module 10"},
      {"id": "finish", "label": "Terminar por hoy"}
    ]
  }]
}
```

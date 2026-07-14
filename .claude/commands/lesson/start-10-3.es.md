---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module10-gas"
prerequisites: ["start-10-1", "start-10-2"]
duration: "~30 min"
level: "intermediate"
tags: ["gas", "sheets", "google", "automation"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 10-3: Ejecucion programada y configuracion de triggers

## 📍 Lo que hara en esta sesion

**Lección 10-3: Integración de GAS con Google Sheets**!

| Elemento | Contenido |
|------|------|
| Objetivo | Automatizar la lectura/escritura de hojas de calculo, procesamiento de datos y generacion de informes desde GAS |
| Duracion | ~30 min |
| Habilidades utilizadas | gas-clasp-ops, Google Sheets API, gogcli |
| Requisitos previos | Lesson 10-1 y 10-2 completadas, proyecto GAS creado |
| Pagina del curso | [Module 10: GAS](https://ai-agent.camp/es/course/module-10)  como referencia paralela |

**Flujo de la sesion:**
1. Acceso a hoja de cálculo
2. Funcionalidad de lectura de datos
3. Funcionalidad de escritura de datos
4. Funcionalidad de generación de informes
5. Flujo de trabajo de automatización

Al final de esta sesion, podra automatizar la integracion con Sheets.

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

## 🚀 Step 1: Spreadsheet Access

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Acceso a hoja de cálculo",
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
Por favor, cree un archivo Sheets.gs en el directorio gas-example con el siguiente contenido:

function getActiveSpreadsheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    Logger.log("No hay hoja de cálculo activa. Por favor, cree una nueva.");
    return null;
  }
  Logger.log("Hoja de cálculo: " + ss.getName());
  Logger.log("ID de la hoja de cálculo: " + ss.getId());
  return ss;
}

function getAllSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) return [];

  const sheets = ss.getSheets();
  Logger.log("Total de hojas: " + sheets.length);

  sheets.forEach(sheet => {
    Logger.log("- " + sheet.getName() + " (" + sheet.getLastRow() + " filas)");
  });

  return sheets;
}

Por favor, sincronice con clasp push.
```

**Resultado esperado:** Sheets.gs se sincroniza con Google Drive.

---

## 🚀 Step 2: Data Reading Functions

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Funciones de lectura de datos",
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
Por favor, añada las siguientes funciones de lectura de datos a Sheets.gs:

function getDataRange(sheetName, range) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("Hoja no encontrada: " + sheetName);
    return [];
  }

  const data = sheet.getRange(range).getValues();
  Logger.log("Datos obtenidos: " + range + " (" + data.length + " filas)");
  return data;
}

function getAllData(sheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return [];

  const lastRow = sheet.getLastRow();
  const lastColumn = sheet.getLastColumn();

  if (lastRow < 1) {
    Logger.log("No hay datos disponibles");
    return [];
  }

  return sheet.getRange(1, 1, lastRow, lastColumn).getValues();
}

Por favor, sincronice con clasp push.
```

**Resultado esperado:** Se agrega una funcion para leer datos de la hoja de calculo.

---

## 🚀 Step 3: Data Writing Functions

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Funciones de escritura de datos",
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
Por favor, añada las siguientes funciones de escritura de datos a Sheets.gs:

function writeSingleCell(sheetName, cell, value) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("Hoja no encontrada: " + sheetName);
    return false;
  }

  sheet.getRange(cell).setValue(value);
  Logger.log("Escritura en celda: " + cell + " = " + value);
  return true;
}

function appendRow(sheetName, rowData) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("Hoja no encontrada: " + sheetName);
    return false;
  }

  sheet.appendRow(rowData);
  Logger.log("Fila añadida: " + rowData.join(", "));
  return true;
}

function writeDataRange(sheetName, startCell, data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return false;

  const rows = data.length;
  const cols = data[0].length;
  const range = sheet.getRange(startCell).offset(0, 0, rows, cols);
  range.setValues(data);

  Logger.log("Escritura de rango completada: " + rows + " filas x " + cols + " columnas");
  return true;
}

Por favor, sincronice con clasp push.
```

**Resultado esperado:** Se agrega una funcion para escribir datos en la hoja de calculo.

---

## 🚀 Step 4: Report Generation Function

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Función de generación de informes",
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
Por favor, añada las siguientes funciones de generación de informes a Sheets.gs:

function generateSummaryReport(sourceSheetName, reportSheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sourceSheet = ss.getSheetByName(sourceSheetName);
  let reportSheet = ss.getSheetByName(reportSheetName);

  // Crear hoja de informe si no existe
  if (!reportSheet) {
    reportSheet = ss.insertSheet(reportSheetName);
  }

  // Limpiar la hoja de informe
  reportSheet.clearContents();

  // Encabezado del informe
  reportSheet.getRange("A1").setValue("=== Informe resumido ===");
  reportSheet.getRange("A1").setFontSize(14).setFontWeight("bold");
  reportSheet.getRange("A2").setValue("Fecha de generación: " + new Date().toLocaleString("es-ES"));

  // Estadísticas de datos
  const lastRow = sourceSheet.getLastRow();
  const lastCol = sourceSheet.getLastColumn();

  reportSheet.getRange("A4").setValue("Total de registros:");
  reportSheet.getRange("B4").setValue(lastRow - 1); // Excluyendo encabezado

  reportSheet.getRange("A5").setValue("Total de columnas:");
  reportSheet.getRange("B5").setValue(lastCol);

  Logger.log("Generación de informe resumido completada");
}

function createTestData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("TestData");

  if (!sheet) {
    sheet = ss.insertSheet("TestData");
  }

  // Encabezado
  sheet.getRange("A1:D1").setValues([["Fecha", "Producto", "Cantidad", "Monto"]]);

  // Datos de ejemplo
  const testData = [
    ["2024-01-01", "Producto A", 10, 1000],
    ["2024-01-02", "Producto B", 5, 500],
    ["2024-01-03", "Producto A", 15, 1500],
    ["2024-01-04", "Producto C", 8, 800],
    ["2024-01-05", "Producto B", 12, 1200]
  ];

  sheet.getRange(2, 1, testData.length, 4).setValues(testData);
  Logger.log("Creación de datos de prueba completada");
}

Por favor, ejecute clasp push, primero ejecute createTestData, luego ejecute generateSummaryReport("TestData", "Report").
```

**Resultado esperado:** Se generan automaticamente datos de prueba e informes de resumen.

---

## 🚀 Step 5: Automation Workflow

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Flujo de trabajo de automatización",
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
Por favor, añada las siguientes funciones de flujo de trabajo automatizado a Sheets.gs:

function dailyReportTask() {
  Logger.log("===== Inicio de generación de informe diario =====");

  try {
    // Generar informe
    generateSummaryReport("TestData", "DailyReport");

    // Notificación de finalización (enviar correo)
    const userEmail = Session.getActiveUser().getEmail();
    if (userEmail) {
      GmailApp.sendEmail(
        userEmail,
        "Informe diario completado " + new Date().toLocaleDateString("es-ES"),
        "Se ha generado el informe diario. Verifique la hoja DailyReport en la hoja de cálculo."
      );
    }

    Logger.log("Informe diario completado");
  } catch (error) {
    Logger.log("Error: " + error);
  }
}

function setDailyReportTrigger() {
  // Eliminar triggers existentes con el mismo nombre
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === "dailyReportTask") {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Crear un trigger para ejecutar diariamente a las 10:00
  ScriptApp.newTrigger("dailyReportTask")
    .timeBased()
    .everyDays(1)
    .atHour(10)
    .create();

  Logger.log("Se ha configurado el trigger de generación de informes diario a las 10:00");
}

Por favor, sincronice con clasp push.
```

**Resultado esperado:** La generacion automatica de informes diarios y la configuracion de disparadores estan listas.

---

## 🚀 Step 6: gogcli x GAS x clasp deploy - Email Aggregation Pipeline

> **Punto clave**: Construya un pipeline E2E: obtener correos con gogcli -> agregar con GAS -> exportar a Sheets -> desplegar en producción con clasp deploy. Es un flujo de trabajo práctico que combina una CLI local (gogcli) con un entorno de ejecución en la nube (GAS).

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 6: gogcli x GAS x clasp deploy",
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
Construya un pipeline para obtener correos con gogcli, agregar en GAS y generar salida en una hoja de cálculo.

### Step 6-1: Obtener correos no leídos con gogcli

gog gmail search "is:unread" --json > ~/ai-agent-camp/gas-example/unread_emails.json

Por favor, verifique el contenido del JSON obtenido (remitente, asunto, fecha, etc.).

### Step 6-2: Crear script de agregación de correos en GAS

Por favor, añada la siguiente función a Sheets.gs:

function aggregateEmailStats() {
  // Agregar estadísticas de correo con GmailApp y generar salida en la hoja
  const threads = GmailApp.search("is:unread", 0, 50);
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Resumen de correos");

  if (!sheet) {
    sheet = ss.insertSheet("Resumen de correos");
  }

  sheet.clearContents();

  // Encabezado
  sheet.getRange("A1:E1").setValues([["Remitente", "Asunto", "Fecha de recepción", "Etiqueta", "Hilos"]]);
  sheet.getRange("A1:E1").setFontWeight("bold");

  // Datos de correo
  const data = threads.map(thread => {
    const msg = thread.getMessages()[0];
    return [
      msg.getFrom(),
      msg.getSubject(),
      msg.getDate().toLocaleString("ja-JP"),
      thread.getLabels().map(l => l.getName()).join(", "),
      thread.getMessageCount()
    ];
  });

  if (data.length > 0) {
    sheet.getRange(2, 1, data.length, 5).setValues(data);
  }

  // Resumen de agregación
  const summaryRow = data.length + 3;
  sheet.getRange("A" + summaryRow).setValue("Fecha de agregación:");
  sheet.getRange("B" + summaryRow).setValue(new Date().toLocaleString("ja-JP"));
  sheet.getRange("A" + (summaryRow + 1)).setValue("Correos no leídos:");
  sheet.getRange("B" + (summaryRow + 1)).setValue(data.length);

  Logger.log("Agregación de correos completada: " + data.length + " elementos");
}

Por favor, sincronice con clasp push.

### Step 6-3: Despliegue a producción con clasp deploy

cd ~/ai-agent-camp/gas-example
clasp push
clasp deploy --description "Agregación de correos v1"

Verifique que se muestre el ID de despliegue.
Ejecute aggregateEmailStats en el editor de GAS y verifique que la salida aparezca en la hoja de cálculo.
```

**Resultado esperado:** Puede verificar datos de correo localmente con gogcli, GAS agrega los mismos datos en una hoja de calculo y el despliegue en produccion se completa con clasp deploy.

**Ejercicio práctico: Obtener correos con gogcli -> Agregar con GAS -> Exportar a Sheets -> clasp deploy**

Practiquemos el siguiente flujo de trabajo:
1. Obtener la lista de correos no leídos localmente con `gog gmail search "is:unread" --json`
2. Ejecutar `aggregateEmailStats()` de GAS para agregar en la hoja de cálculo
3. Comparar la salida de gogcli con la salida de GAS para verificar la consistencia de datos
4. Desplegar en producción con `clasp push && clasp deploy --description "email-aggregation-v1"`
5. Configurar un trigger en el script desplegado para ejecución automática cada mañana

> **Consejo**: Este pipeline es un patrón muy utilizado en la práctica.
> - **gogcli**: Verificar y depurar datos rápidamente de forma local
> - **GAS**: Ejecución programada y automatización en la nube
> - **clasp**: Flujo CI/CD de desarrollo local -> despliegue en la nube

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
      {"id": "trouble_1", "label": "Sheet not found"},
      {"id": "trouble_2", "label": "Invalid range"},
      {"id": "trouble_3", "label": "Permission denied for Gmail"},
      {"id": "trouble_4", "label": "No se pueden escribir datos"},
      {"id": "trouble_5", "label": "clasp deploy falla"},
      {"id": "trouble_6", "label": "Error de autenticación de gogcli (gog gmail search falla)"}
    ]
  }]
}
```


### Problema 1: "Sheet not found"
**Causa:** El nombre de la hoja no existe
**Prompt de solucion:**
```
Por favor, ejecute getAllSheets() para verificar los nombres de hojas existentes.
Verifique que la ortografía del nombre de la hoja sea correcta.
```

### Problema 2: "Invalid range"
**Causa:** El formato de especificacion de rango es invalido
**Prompt de solucion:**
```
Por favor, verifique la especificación de rango en formato A1:C10.
Verifique el rango válido con getLastRow() y getLastColumn().
```

### Problema 3: "Permission denied for Gmail"
**Causa:** No hay permisos de la API de Gmail
**Prompt de solucion:**
```
Por favor, habilite la API de Gmail en el editor de GAS.
Muestre cómo añadir los scopes de Gmail a appsscript.json.
```

### Problema 4: No se pueden escribir datos
**Causa:** La hoja esta protegida o el tamano de la matriz no coincide
**Prompt de solucion:**
```
Por favor, verifique la configuración de protección de la hoja.
Verifique que la cantidad de filas y columnas del array de datos a escribir sea correcta.
```

### Problema 5: clasp deploy falla
**Causa:** No hay permisos de despliegue o la configuracion de appsscript.json esta incompleta
**Prompt de solucion:**
```
Por favor, verifique los despliegues existentes con clasp deployments.
Verifique que los oauthScopes necesarios estén configurados en appsscript.json.
Verifique el estado de autenticación con clasp login --status.
```

### Problema 6: Error de autenticacion de gogcli
**Causa:** La autenticacion de gogcli no esta completa o el token ha expirado
**Prompt de solucion:**
```
Por favor, verifique el estado de autenticación con gog auth status.
Si la autenticación ha expirado, vuelva a autenticarse con gog auth login.
Consulte 4-1 para completar la configuración de gogcli.
```

---

## ✅ Punto de control
- [ ] Se puede acceder a la hoja de cálculo
- [ ] Se pueden leer datos
- [ ] Se pueden escribir datos
- [ ] La generación de informes funciona
- [ ] Se puede configurar el trigger de automatización
- [ ] Se envían notificaciones por correo
- [ ] Se pueden obtener datos de correo con gogcli (`gog gmail search "is:unread" --json`)
- [ ] La agregación de correos de GAS se exporta a la hoja de cálculo
- [ ] El despliegue en producción tiene éxito con `clasp deploy`


---

## 📋 Vista previa de entregables

### Salida esperada
```
📁 output/gas/
└── Code.gs  (script GAS)
```

### Comandos de verificacion
```bash
# Verificar archivos de script locales
ls -la output/gas/

# Verificar el inicio del contenido del script
head -30 output/gas/Code.gs

# Verificar en el editor de GAS
clasp open
```

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```
# Verificación de finalización: Verifique que se hayan creado los datos de prueba y las hojas de informe en Google Sheets, que las funciones GAS (después de clasp push) funcionen correctamente y que clasp deploy haya tenido éxito.
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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-11-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-11-1
- finish → Finalizar

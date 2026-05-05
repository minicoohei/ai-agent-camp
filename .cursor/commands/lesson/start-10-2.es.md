---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module10-gas"
prerequisites: ["start-10-1"]
duration: "~30 min"
level: "intermediate"
tags: ["gas", "calendar", "google", "automation"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 10-2: Automatizacion de hojas de calculo con GAS

## 📍 Lo que hara en esta sesion

**Lección 10-2: Integración de GAS con Google Calendar**!

| Elemento | Contenido |
|------|------|
| Objetivo | Automatizar operaciones de eventos con la API de Google Calendar desde GAS |
| Duracion | ~30 min |
| Habilidades utilizadas | gas-clasp-ops, Google Calendar API, gogcli |
| Requisitos previos | Lesson 10-1 completada, proyecto GAS creado, Apps Script API habilitada |
| Pagina del curso | [Module 10: GAS](https://ai-agent.camp/es/course/module-10)  como referencia paralela |

**Flujo de la sesion:**
1. Crear un script de obtención de calendario
2. Crear, actualizar y eliminar eventos
3. Configurar triggers y notificaciones

Al final de esta sesion, podra automatizar la integracion del calendario.

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

## 🚀 Step 1: Calendar Retrieval Script

**Verificación de requisitos previos (ejecución automática):**
Verifique lo siguiente antes de continuar:

1. **Verificar `.clasp.json`**: Verificar que `gas-example/.clasp.json` existe. Si no, complete primero 4-1.
2. **Verificar que Apps Script API está habilitada**: Verificar que "Google Apps Script API" está ON en https://script.google.com/home/usersettings.
3. **Configuración de oauthScopes en `appsscript.json`**: Añadir los siguientes alcances a `gas-example/appsscript.json` para usar la Calendar API:

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/script.external_request"
  ]
}
```

> **Importante**: Si no se configuran los oauthScopes, se producirá un error "Permission denied" al llamar a la Calendar API.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Script de obtención de calendario",
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
Por favor, cree un archivo Calendar.gs en el directorio gas-example con el siguiente contenido:

function getDefaultCalendar() {
  const calendar = CalendarApp.getDefaultCalendar();
  Logger.log("Nombre del calendario: " + calendar.getName());
  Logger.log("ID del calendario: " + calendar.getId());
  return calendar;
}

function getAllCalendars() {
  const calendars = CalendarApp.getAllCalendars();
  Logger.log("Total de calendarios: " + calendars.length);
  calendars.forEach(calendar => {
    Logger.log("- " + calendar.getName());
  });
  return calendars;
}

Por favor, sincronice con clasp push.
```

**Resultado esperado:** Calendar.gs se sincroniza con Google Drive y puede recuperar la lista de calendarios.

---

## 🚀 Step 2: Event Creation Function

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Función de creación de eventos",
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
Por favor, añada la siguiente función de creación de eventos a Calendar.gs:

function createSimpleEvent(title, startTime, endTime) {
  const calendar = CalendarApp.getDefaultCalendar();
  const event = calendar.createEvent(title, startTime, endTime);
  Logger.log("Evento creado: " + title);
  Logger.log("ID del evento: " + event.getId());
  return event.getId();
}

function createTomorrowEvent() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  const startTime = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 14, 0, 0);
  const endTime = new Date(startTime.getTime() + 60 * 60 * 1000);

  return createSimpleEvent("Evento de prueba", startTime, endTime);
}

Por favor, ejecute clasp push y luego createTomorrowEvent en el editor de GAS.
```

**Resultado esperado:** Se agrega un "Evento de prueba" al calendario por 1 hora a partir de las 14:00 de manana.

---

## 🚀 Step 3: Get Event List

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Obtener lista de eventos",
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
Por favor, añada la siguiente función de obtención de eventos a Calendar.gs:

function getTodayEvents() {
  const calendar = CalendarApp.getDefaultCalendar();
  const today = new Date();
  const dayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 0, 0, 0);
  const dayEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59, 59);

  const events = calendar.getEvents(dayStart, dayEnd);
  Logger.log("Eventos de hoy: " + events.length);

  events.forEach(event => {
    Logger.log("- " + event.getTitle() + " (" + event.getStartTime().toLocaleString() + ")");
  });

  return events;
}

Por favor, ejecute clasp push y luego ejecútelo.
```

**Resultado esperado:** Los eventos del calendario de hoy se muestran en el registro.

---

## 🚀 Step 4: Scheduled Trigger Setup

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Configuración de trigger de ejecución programada",
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
Por favor, añada la siguiente función de configuración de triggers a Calendar.gs:

function dailyMorningTask() {
  const events = getTodayEvents();
  Logger.log("Verificación de eventos de hoy: " + events.length + " elementos");
  // Añadir procesamiento de notificación por correo aquí
}

function createDailyTrigger() {
  // Eliminar triggers existentes
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));

  // Crear un trigger para ejecutar diariamente a las 9:00
  ScriptApp.newTrigger("dailyMorningTask")
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();

  Logger.log("Se ha configurado el trigger diario a las 9:00");
}

Por favor, ejecute clasp push y luego createDailyTrigger.
```

**Resultado esperado:** Se configura un disparador para ejecutarse automaticamente todos los dias a las 9:00.

---

## 🚀 Step 5: gogcli x GAS Integration - Calendar Data Retrieval and Transcription

> **Punto clave**: Usando gogcli configurado en 4-1, experimentará un flujo de trabajo de obtener datos de calendario localmente y transferirlos automáticamente a una hoja de cálculo con GAS. Al combinar gogcli (CLI local) y GAS (ejecución en la nube), puede construir pipelines de datos flexibles.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Integración gogcli x GAS",
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
Integre gogcli con GAS para transferir automáticamente la información del calendario a una hoja de cálculo.

### Step 5-1: Obtener datos del calendario con gogcli

gog calendar list --days 7 --json > ~/ai-agent-camp/gas-example/calendar_data.json

Por favor, verifique el contenido del archivo JSON obtenido.

### Step 5-2: Cargar datos del calendario en GAS y transferir a la hoja

Por favor, añada la siguiente función a Calendar.gs:

function importCalendarDataToSheet() {
  // Imagen de transferir datos JSON obtenidos con gogcli a una hoja de cálculo
  // En la práctica, hay dos patrones: obtener directamente a través de CalendarApp desde GAS vinculado a una hoja de cálculo,
  // o pegar manual/automáticamente la salida de gogcli en la hoja

  const calendar = CalendarApp.getDefaultCalendar();
  const now = new Date();
  const weekLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  const events = calendar.getEvents(now, weekLater);

  // Escribir en la hoja de cálculo
  const ss = SpreadsheetApp.create("Informe semanal del calendario");
  const sheet = ss.getActiveSheet();

  // Encabezado
  sheet.getRange("A1:E1").setValues([["Título", "Fecha de inicio", "Fecha de fin", "Lugar", "Descripción"]]);

  // Datos de eventos
  const data = events.map(event => [
    event.getTitle(),
    event.getStartTime().toLocaleString("ja-JP"),
    event.getEndTime().toLocaleString("ja-JP"),
    event.getLocation() || "",
    event.getDescription() || ""
  ]);

  if (data.length > 0) {
    sheet.getRange(2, 1, data.length, 5).setValues(data);
  }

  Logger.log("Transferencia de datos del calendario completada: " + data.length + " elementos");
  Logger.log("URL de la hoja de cálculo: " + ss.getUrl());
  return ss.getUrl();
}

Por favor, ejecute clasp push y luego importCalendarDataToSheet en el editor de GAS.
```

**Resultado esperado:** Puede recuperar JSON del calendario localmente con gogcli, y GAS puede transcribir los mismos datos del calendario a una hoja de calculo.

**Ejercicio práctico: Transferir automáticamente datos de calendario obtenidos con gogcli a una hoja de cálculo usando GAS**

Practiquemos el siguiente flujo de trabajo:
1. Obtener las citas de esta semana con `gog calendar list --days 7 --json`
2. Verificar la estructura del JSON de salida (título, fecha/hora, lugar, etc.)
3. Ejecutar `importCalendarDataToSheet()` de GAS para transferir los mismos datos a la hoja de cálculo
4. Comparar la salida de gogcli con la salida de GAS para verificar la consistencia de datos

> **Consejo**: gogcli es una CLI local, lo que facilita la integración con CI/CD y scripts. Por otro lado, GAS puede ejecutarse periódicamente (mediante triggers) en la nube. Al combinar ambos, se puede lograr un flujo de desarrollo de verificación local -> automatización en la nube.

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
      {"id": "trouble_1", "label": "Calendar not found"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Event not found"},
      {"id": "trouble_4", "label": "El disparador no funciona"},
      {"id": "trouble_5", "label": "Apps Script API has not been used / is not enabled"},
      {"id": "trouble_6", "label": "Error de autenticación de gogcli (gog calendar list falla)"}
    ]
  }]
}
```


### Problema 1: "Calendar not found"
**Causa:** El ID del calendario es invalido o no tiene permisos de acceso
**Prompt de solucion:**
```
Por favor, ejecute getAllCalendars() y verifique la lista de calendarios accesibles.
Verifique que el ID del calendario sea correcto.
```

### Problema 2: "Permission denied"
**Causa:** No se han otorgado permisos de la API de Calendar
**Prompt de solucion:**
```
Por favor, añada la API de Google Calendar desde "Servicios" en el editor de GAS.
También muestre cómo añadir oauthScopes a appsscript.json.
```

### Problema 3: "Event not found"
**Causa:** El ID del evento no existe o ha sido eliminado
**Prompt de solucion:**
```
Por favor, añada una verificación null antes de getEventById e implemente el manejo de errores para cuando el evento no exista.
```

### Problema 4: El disparador no funciona
**Causa:** No hay permisos de ejecucion para el disparador
**Prompt de solucion:**
```
Por favor, verifique el estado de los triggers desde el menú "Triggers" en el editor de GAS.
Si hay registros de errores, proporcione los detalles.
```

### Problema 5: "Apps Script API has not been used in project / User has not enabled the Apps Script API"
**Causa:** Google Apps Script API esta deshabilitada
**Pasos de resolución**:
1. Acceder a https://script.google.com/home/usersettings
2. Cambiar el interruptor de "Google Apps Script API" a **ON**
3. Después del cambio, repetir desde `clasp login`

> Esta configuración es por cuenta de Google. Una vez habilitada, se puede usar para todos los proyectos GAS posteriores.

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
- [ ] La obtención de calendarios funciona
- [ ] La creación de eventos funciona
- [ ] La obtención de la lista de eventos funciona
- [ ] El trigger ha sido configurado
- [ ] La ejecución programada funciona
- [ ] Se pueden obtener datos de calendario con gogcli (`gog calendar list --days 7 --json`)
- [ ] GAS puede transferir datos de calendario a la hoja de cálculo


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
# Verificación de finalización: Verifique lo siguiente.
# 1. gas-example/Calendar.gs existe
# 2. appsscript.json tiene oauthScopes (calendar, script.external_request) configurados
# 3. clasp push tiene éxito (ejecutar en el directorio gas-example)
# 4. Ejecutar getDefaultCalendar() en el editor de GAS muestra el nombre del calendario
# 5. createTomorrowEvent() crea un evento en el calendario
```

**Resultado esperado:** Todos los elementos pasan y las operaciones de eventos usando la API de Google Calendar desde GAS estan listas.

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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-10-3)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-10-3
- finish → Finalizar

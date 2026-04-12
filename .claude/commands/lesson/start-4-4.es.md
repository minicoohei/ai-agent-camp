---
description: "When the user says /start-4-4 — Module 4 Lesson 4-4: Registro y gestion de eventos de Google Calendar"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-4-3"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "calendar", "event-management"]
---

# 🎓 Lesson 4-4: Registro y gestion de eventos de Google Calendar

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 4-4: Registro y gestion de eventos de Google Calendar**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear, gestionar asistentes, configurar recurrencia y eliminar eventos del calendario usando gogcli |
| Duracion | ~30 min |
| Skills utilizados | gogcli calendar create / delete |
| Requisitos previos | Conceptos basicos de Google Calendar completados (start-4-3 finalizado) |

**Flujo de la sesion:**
1. Crear un evento simple
2. Crear eventos con asistentes y Google Meet
3. Configurar eventos recurrentes (reglas de recurrencia)
4. Eliminar y gestionar eventos
5. Ejercicio practico: registrar por lotes un horario semanal

Al finalizar esta sesion, podra crear y gestionar libremente eventos del calendario usando gogcli.

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
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → `gog auth list`  para verificar estado de autenticacion、start-4-3 verificar finalizacion)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Creacion de eventos simples

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Creación de evento simple",
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

Creemos un evento basico:

```bash
# Creacion simple de evento (solo titulo, inicio y fin)
gog calendar create primary --account your-email@gmail.com \
  --summary "Sesion de estudio de IA" \
  --from "2026-03-20T14:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00"

# Creacion de evento con descripcion y ubicacion
gog calendar create primary --account your-email@gmail.com \
  --summary "Sesion de estudio de IA" \
  --from "2026-03-20T14:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00" \
  --description "Sesión de estudio sobre el uso de Claude Code. Materiales compartidos previamente." \
  --location "Sala de conferencias B"
```

**Resultado esperado**: Se crean eventos y se reflejan en Google Calendar. Se devuelven los IDs de los eventos.

> **⚠️ Advertencia**: Especifique fechas y horas en formato RFC3339 (`YYYY-MM-DDTHH:MM:SS+09:00`). Incluya siempre el desplazamiento de zona horaria (por ejemplo, `+09:00`).

---

## 🚀 Step 2: Eventos con participantes y Google Meet

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Eventos con participantes y Google Meet",
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

Cree eventos que inviten a asistentes y generen automaticamente enlaces de Google Meet:

```bash
# Evento con participantes y Google Meet
gog calendar create primary --account your-email@gmail.com \
  --summary "Reunion de equipo" \
  --from "2026-03-20T10:00:00+09:00" \
  --to "2026-03-20T11:00:00+09:00" \
  --attendees "colleague@company.com" \
  --with-meet

# Especificar multiples participantes separados por comas
gog calendar create primary --account your-email@gmail.com \
  --summary "Inicio del proyecto" \
  --from "2026-03-21T13:00:00+09:00" \
  --to "2026-03-21T14:30:00+09:00" \
  --attendees "member1@company.com,member2@company.com,member3@company.com" \
  --with-meet \
  --description "Reunión de inicio del nuevo proyecto" \
  --location "En línea"

# Con configuracion de visibilidad y opciones de notificacion
gog calendar create primary --account your-email@gmail.com \
  --summary "Reunión general" \
  --from "2026-03-22T15:00:00+09:00" \
  --to "2026-03-22T16:00:00+09:00" \
  --attendees "team@company.com" \
  --with-meet \
  --visibility public \
  --send-updates all
```

**Resultado esperado**: Se crean eventos, se envian correos de invitacion a los asistentes y se generan automaticamente enlaces de Google Meet.

> **💡 Consejo**: La opcion `--send-updates` controla quien recibe notificaciones de invitacion (`all`=todos, `externalOnly`=solo externos, `none`=sin notificaciones).

---

## 🚀 Step 3: Eventos recurrentes (reglas de recurrencia)

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Eventos recurrentes (reglas de recurrencia)",
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

Use la opcion `--rrule` para especificar reglas de recurrencia (RFC 5545 RRULE):

```bash
# Evento recurrente semanal los lunes (12 veces)
gog calendar create primary --account your-email@gmail.com \
  --summary "Standup semanal" \
  --from "2026-03-23T10:00:00+09:00" \
  --to "2026-03-23T11:00:00+09:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=12"

# Revision mensual el primer lunes (6 veces)
gog calendar create primary --account your-email@gmail.com \
  --summary "Revisión mensual" \
  --from "2026-04-06T14:00:00+09:00" \
  --to "2026-04-06T15:30:00+09:00" \
  --rrule "RRULE:FREQ=MONTHLY;BYDAY=1MO;COUNT=6" \
  --attendees "manager@company.com" \
  --with-meet

# Evento de dia completo (opcion --all-day)
gog calendar create primary --account your-email@gmail.com \
  --summary "Retiro del equipo" \
  --from "2026-04-10" \
  --to "2026-04-11" \
  --all-day \
  --description "Retiro del equipo Q2 (2 días / 1 noche)"
```

**Patrones RRULE comunes:**

| Patron | RRULE | Descripcion |
|---------|-------|------|
| Cada lunes | `FREQ=WEEKLY;BYDAY=MO;COUNT=12` | 12 semanas |
| Cada mar/jue | `FREQ=WEEKLY;BYDAY=TU,TH;COUNT=24` | 12 semanas (2 veces/semana) |
| 1ro de cada mes | `FREQ=MONTHLY;BYMONTHDAY=1;COUNT=6` | 6 meses |
| 2do mie de cada mes | `FREQ=MONTHLY;BYDAY=2WE;COUNT=6` | 6 meses |
| Cada dia laborable | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=20` | 4 semanas |

> **💡 Consejo**: `COUNT` especifica el numero de repeticiones y `UNTIL` especifica la fecha de finalizacion. Si se omite `COUNT`, el evento se repite indefinidamente, asi que tenga cuidado.

---

## 🚀 Step 4: Eliminacion y gestion de eventos

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Eliminación y gestión de eventos",
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

Gestione y elimine eventos creados:

```bash
# Eliminar evento (eventId devuelto durante la creacion)
gog calendar delete primary <eventId> --account your-email@gmail.com --force

# Verificar ID de la lista de eventos y eliminar
gog calendar list --account your-email@gmail.com --days 7
# Eliminar usando el ID del evento mostrado arriba
```

**Opciones utiles al crear eventos:**

```bash
# Especificar color del evento (numero 1-11)
gog calendar create primary --account your-email@gmail.com \
  --summary "Tarea importante" \
  --from "2026-03-20T09:00:00+09:00" \
  --to "2026-03-20T10:00:00+09:00" \
  --event-color 11

# Tiempo de concentracion (trabajo profundo)
gog calendar create primary --account your-email@gmail.com \
  --summary "Tiempo de concentración" \
  --from "2026-03-20T13:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00" \
  --event-type focus-time

# Configuracion de ausencia (Out of Office)
gog calendar create primary --account your-email@gmail.com \
  --summary "Vacaciones" \
  --from "2026-03-25T00:00:00+09:00" \
  --to "2026-03-26T00:00:00+09:00" \
  --event-type out-of-office
```

**Referencia de numeros de color de eventos:**

| Numero | Color | Ejemplo de uso |
|------|-----|-------|
| 1 | Lavanda | Personal |
| 2 | Salvia | Aprendizaje |
| 4 | Flamingo | Importante |
| 5 | Banana | Precaucion |
| 9 | Arandano | Reunion |
| 11 | Tomate | Urgente |

> **💡 Consejo**: El indicador `--force` elimina sin confirmacion. Tenga en cuenta que eliminar un evento recurrente elimina toda la serie.

---

## 🚀 Step 5: Ejercicio practico (registrar horario semanal en lote)

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Ejercicio práctico",
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

Combinemos las funciones que ha aprendido para registrar por lotes un horario semanal. Ingrese el siguiente prompt en Cursor:

```text
Use el comando gog calendar create para crear el siguiente horario semanal:

1. Cada mañana 9:00-9:15 "Standup matutino" (lun-vie, con --with-meet, usando --rrule)
2. Lunes 10:00-12:00 "Tiempo de concentración" (--event-type focus-time)
3. Martes 14:00-15:00 "Reunión 1 a 1" (participante: manager@company.com, con --with-meet)
4. Miércoles 15:00-16:00 "Sesión de estudio del equipo" (--description "Compartir casos de uso de IA", --event-color 2)
5. Viernes 17:00-17:30 "Retrospectiva semanal" (--attendees "team@company.com", con --with-meet)

Cuenta: your-email@gmail.com
Fecha de inicio: próximo lunes
Agregue también descripciones apropiadas a cada evento.
```

**Ejemplo de comandos generados por la IA:**
```bash
# 1. Standup matutino (recurrente)
gog calendar create primary --account your-email@gmail.com \
  --summary "Standup matutino" \
  --from "2026-03-23T09:00:00+09:00" \
  --to "2026-03-23T09:15:00+09:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=5" \
  --with-meet \
  --description "Informe diario de progreso (15 min)"

# 2. Tiempo de concentracion
gog calendar create primary --account your-email@gmail.com \
  --summary "Tiempo de concentración" \
  --from "2026-03-23T10:00:00+09:00" \
  --to "2026-03-23T12:00:00+09:00" \
  --event-type focus-time \
  --description "Tiempo de trabajo concentrado. Configurar Slack en no molestar."

# 3. Reunion 1 a 1
gog calendar create primary --account your-email@gmail.com \
  --summary "Reunión 1 a 1" \
  --from "2026-03-24T14:00:00+09:00" \
  --to "2026-03-24T15:00:00+09:00" \
  --attendees "manager@company.com" \
  --with-meet \
  --description "1 a 1 con el gerente"

# 4. Sesion de estudio del equipo
gog calendar create primary --account your-email@gmail.com \
  --summary "Sesión de estudio del equipo" \
  --from "2026-03-25T15:00:00+09:00" \
  --to "2026-03-25T16:00:00+09:00" \
  --event-color 2 \
  --description "Compartir casos de uso de IA"

# 5. Retrospectiva semanal
gog calendar create primary --account your-email@gmail.com \
  --summary "Retrospectiva semanal" \
  --from "2026-03-27T17:00:00+09:00" \
  --to "2026-03-27T17:30:00+09:00" \
  --attendees "team@company.com" \
  --with-meet \
  --description "Compartir los resultados de esta semana y los planes de la próxima"
```

**Resultado esperado**: Se registran 5 tipos de eventos en el calendario. Verifiquelos en Google Calendar.

> **💡 Consejo**: Al delegar a la IA, incluso las configuraciones de horarios complejas se pueden automatizar facilmente.

---

## ⚠️ Problemas comunes y soluciones

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione la opción que corresponda",
    "options": [
      {"id": "trouble_1", "label": "Los eventos no se crean"},
      {"id": "trouble_2", "label": "Las notificaciones no llegan a los participantes"},
      {"id": "trouble_3", "label": "Las reglas de recurrencia no funcionan correctamente"},
      {"id": "trouble_4", "label": "El enlace de Google Meet no se genera"}
    ]
  }]
}
```

### Problema 1: "Los eventos no se crean"
**Causa**: Especificacion incorrecta de calendarId, o error de formato de fecha/hora
**Prompt de solucion**:
```text
Verifique que calendarId sea correcto (normalmente "primary").
Especifique fechas/horas en formato RFC3339 ("YYYY-MM-DDTHH:MM:SS+09:00").
Puede verificar los IDs de calendario con gog calendar calendars --account your-email@gmail.com
```

### Problema 2: "Las notificaciones no llegan a los participantes"
**Causa**: La opcion --send-updates no esta especificada
**Prompt de solucion**:
```text
Agregue --send-updates all.
De forma predeterminada, es posible que no se envíen notificaciones.
Ejemplo: gog calendar create primary --account ... --attendees "..." --send-updates all
```

### Problema 3: "Las reglas de recurrencia no funcionan correctamente"
**Causa**: Error de sintaxis RRULE
**Prompt de solucion**:
```text
Verifique la sintaxis RRULE:
- Se requiere el prefijo "RRULE:"
- FREQ es obligatorio (WEEKLY, MONTHLY, DAILY, etc.)
- BYDAY usa códigos de día de 2 letras (MO, TU, WE, TH, FR, SA, SU)
- Especifique condiciones de finalización con COUNT o UNTIL
Ejemplo correcto: "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=12"
```

### Problema 4: "El enlace de Google Meet no se genera"
**Causa**: El indicador --with-meet no esta especificado
**Prompt de solucion**:
```text
Agregue el indicador --with-meet.
Ejemplo: gog calendar create primary --account ... --summary "Reunión" --with-meet
Si no está usando una cuenta de Google Workspace, la generación de enlaces de Meet puede estar restringida.
```

---

## ✅ Punto de control
- [ ] Creo exitosamente un evento simple
- [ ] Creo exitosamente eventos con asistentes y Meet
- [ ] Configuro exitosamente eventos recurrentes
- [ ] Elimino exitosamente eventos
- [ ] Completo el registro por lotes de un horario semanal


---

## 📋 Vista previa de resultados

El entregable de esta leccion es la salida de la terminal.

### Salida esperada
```text
┌─────────────────────────────────────┐
│  Resultado de ejecución del comando    │
│  Estado: ✅ Éxito                       │
│  Elementos procesados: N               │
└─────────────────────────────────────┘
```

> Consejo: Para guardar la salida en un archivo, agregue ` > output/result.txt` al final del comando

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Codex para verificar la finalizacion:

```text
Ejecute los siguientes comandos para verificar que el registro y gestión de eventos del Calendar funcione correctamente:
1. gog calendar list --account <su-correo> --days 7
2. Verifique que los eventos creados en esta lección aparezcan en los resultados anteriores
3. Verifique que los eventos recurrentes estén configurados correctamente
Confirme que todo funcione correctamente.
```

**Resultado esperado**: Los eventos creados (simples, con asistentes, recurrentes, tiempo de enfoque, etc.) se muestran en el listado.

---

## 🎉 Siguientes pasos

La gestion y registro de eventos de Google Calendar esta completa. En la siguiente leccion, aprendera las operaciones de Google Drive.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/start-4-5)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-4-5)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /start-4-5（Operaciones de Google Drive)
- next_window → Abrir nueva ventana con /start-4-5
- finish → Finalizar

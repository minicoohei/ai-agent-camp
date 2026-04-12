---
description: "When the user says /start-4-3 — Module 4 Lesson 4-3: Operaciones de Google Calendar"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~25 min"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "calendar"]
---

# 🎓 Lesson 4-3: Operaciones de Google Calendar

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 4-3: Operaciones de Google Calendar**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Listar, crear y actualizar eventos del calendario usando gogcli |
| Duracion | ~25 min |
| Skills utilizados | gogcli calendar |
| Requisitos previos | Configuracion de autenticacion de gogcli completada (start-4-1 finalizado) |

**Flujo de la sesion:**
1. Listar los eventos de hoy y de esta semana
2. Crear nuevos eventos
3. Configurar reuniones recurrentes automaticamente

Al finalizar esta sesion, podra ver y crear eventos del calendario usando gogcli.

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
(check_prereq → `gog auth list`  para verificar estado de autenticacion)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Listar eventos de hoy y esta semana

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Mostrar lista de eventos",
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

Verifiquemos los eventos del calendario:

```bash
# Eventos de hoy
gog calendar list --account your-email@gmail.com --days 1

# Eventos de esta semana (7 dias)
gog calendar list --account your-email@gmail.com --days 7

# Obtener lista de calendarios (verificar IDs disponibles)
gog calendar calendars --account your-email@gmail.com
```

**Resultado esperado**: Se listan los titulos de eventos, horas de inicio, horas de finalizacion y ubicaciones (si estan configuradas).

> **💡 Consejo**: `--days` obtiene eventos para el numero de dias especificado. El calendario predeterminado es `primary`.

**Avanzado: Analisis de programacion con IA**

Pase la lista de eventos obtenida a la IA para su analisis:
```text
Analice el horario de esta semana anterior:
1. Identifique los intervalos de tiempo disponibles
2. Identifique los dias con reuniones concentradas
3. Calcule el tiempo de reuniones por dia
```

---

## 🚀 Step 2: Crear nuevos eventos

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear eventos",
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

Cree nuevos eventos de calendario:

```bash
# Creacion basica de eventos
gog calendar create primary --account your-email@gmail.com \
  --summary "Sesion de estudio de IA" \
  --from "2026-03-15T14:00:00+09:00" \
  --to "2026-03-15T15:00:00+09:00"

# Creacion de evento con ubicacion y descripcion
gog calendar create primary --account your-email@gmail.com \
  --summary "Reunion de equipo" \
  --from "2026-03-16T10:00:00+09:00" \
  --to "2026-03-16T11:00:00+09:00" \
  --location "Sala de reuniones A" \
  --description "Actualizacion de progreso semanal"
```

**Resultado esperado**: Se crean eventos y se reflejan en Google Calendar. Se devuelven los IDs de los eventos.

> **⚠️ Advertencia**: Especifique fechas y horas en formato ISO 8601 (`YYYY-MM-DDTHH:MM:SS+09:00`). Se recomienda incluir el desplazamiento de zona horaria (por ejemplo, `+09:00`).

---

## 🚀 Step 3: Configuracion automatica de reuniones recurrentes

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Configuracion automatica de reuniones recurrentes",
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

Usemos la IA para crear multiples eventos por lotes. Ingrese el siguiente prompt en Cursor:

```text
Utilice el comando gog calendar create para crear las siguientes reuniones recurrentes:

1. Cada lunes 10:00-10:30 "Reunion diaria semanal del equipo" (4 semanas desde la proxima semana)
2. Cada miercoles 14:00-15:00 "Reunion de progreso del proyecto" (4 semanas desde la proxima semana)
3. Cada viernes 17:00-17:30 "Retrospectiva semanal" (4 semanas desde la proxima semana)

Cuenta: your-email@gmail.com
Tambien agregue una descripcion apropiada a cada evento.
```

**Ejemplo de comandos generados por la IA:**
```bash
# Reunion matutina del lunes (4 semanas)
gog calendar create primary --account your-email@gmail.com --summary "Reunion diaria semanal del equipo" --from "2026-03-16T10:00:00+09:00" --to "2026-03-16T10:30:00+09:00" --description "Inicio semanal del equipo completo"
gog calendar create primary --account your-email@gmail.com --summary "Reunion diaria semanal del equipo" --from "2026-03-23T10:00:00+09:00" --to "2026-03-23T10:30:00+09:00" --description "Inicio semanal del equipo completo"
# ... y asi sucesivamente
```

**Resultado esperado**: Se registran 12 eventos (3 tipos x 4 semanas) en el calendario. Verifiquelos en Google Calendar.

> **💡 Consejo**: Al delegar a la IA, puede automatizar tareas manuales repetitivas. Este es el verdadero poder de utilizar asistentes de IA.

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
      {"id": "trouble_1", "label": "Los eventos no se muestran"},
      {"id": "trouble_2", "label": "Error de formato de fecha/hora"},
      {"id": "trouble_3", "label": "No se conoce el ID del calendario"},
      {"id": "trouble_4", "label": "Los eventos creados no se reflejan"}
    ]
  }]
}
```

### Problema 1: "Los eventos no se muestran"
**Causa**: No hay eventos en el periodo objetivo, o el ID del calendario es diferente
**Prompt de solucion**:
```text
Intente un valor mayor de --days (por ejemplo, --days 30).
Tambien verifique los calendarios disponibles con gog calendar calendars.
```

### Problema 2: "Error de formato de fecha/hora"
**Causa**: No esta en formato ISO 8601
**Prompt de solucion**:
```text
Especifique la fecha/hora en formato "YYYY-MM-DDTHH:MM:SS+09:00".
Ejemplo: "2026-03-15T14:00:00+09:00"
Coloque "T" entre la fecha y la hora, e incluya el desplazamiento de zona horaria.
```

### Problema 3: "No se conoce el ID del calendario"
**Causa**: Cuando hay multiples calendarios
**Prompt de solucion**:
```text
Liste con gog calendar calendars --account your-email@gmail.com
y verifique el ID del calendario objetivo.
El calendario principal suele ser "primary".
```

### Problema 4: "Los eventos creados no se reflejan"
**Causa**: Retraso en la respuesta de la API, o cache del calendario
**Prompt de solucion**:
```text
Verifique con gog calendar list. Recargue el navegador en la pagina web de Google Calendar.
Puede haber un retraso de unos segundos.
```

---

## ✅ Punto de control
- [ ] Pudo obtener los listados de eventos de hoy y de esta semana
- [ ] Pudo confirmar la lista de calendarios (IDs de calendario)
- [ ] Pudo crear nuevos eventos (con ubicacion y descripcion)
- [ ] Pudo crear reuniones recurrentes por lotes usando IA


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
Ejecute los siguientes comandos para verificar que las operaciones del calendario funcionen correctamente:
1. gog calendar list --account <su-correo> --days 7
2. Verifique que los resultados incluyan los eventos creados en esta leccion
Verifique que todos los comandos funcionen correctamente.
```

**Resultado esperado**: Los eventos creados se muestran en el listado.

---

## 🎉 Siguientes pasos

Las operaciones de Google Calendar estan completas! En la siguiente leccion, aprendera operaciones de Google Drive.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/start-4-4)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-4-4)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /start-4-4（Operaciones de Google Drive)
- next_window → Abrir nueva ventana con /start-4-4
- finish → Finalizar

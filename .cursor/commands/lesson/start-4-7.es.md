---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-4-1", "start-4-2", "start-4-3", "start-4-4", "start-4-5", "start-4-6"]
level: "intermediate"
tags: ["google", "workspace", "gogcli", "workflow", "automation"]
---

# 🎓 Lesson 4-7: Integracion del flujo de trabajo de secretario de IA

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 4-7: Integracion del flujo de trabajo de secretario de IA**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Construir un flujo de trabajo de secretaria IA combinando Gmail+Calendar+Drive |
| Duracion | ~30 min |
| Skills utilizados | gogcli, check-inbox, google-sync |
| Requisitos previos | Todas las lecciones 4-1 a 4-6 completadas |

**Flujo de la sesion:**
1. Sincronizar datos por lotes con google-sync
2. Extraer tareas de correos con check-inbox
3. Determinar prioridad mediante referencia cruzada con el calendario
4. Generar automaticamente reportes diarios

Al finalizar esta sesion, un flujo de trabajo de secretaria IA que abarca Gmail, Calendar y Drive estara operativo.

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
      {"id": "check_prereq", "label": "Quiero verificar requisitos previos (estado de finalización 4-1 a 4-6)"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → 4-1〜4-6 verificar estado de finalizacion)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Sincronizacion masiva de datos con google-sync

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Sincronización masiva de datos",
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

Use el script google-sync para sincronizar por lotes los datos de Gmail, Calendar y Drive:

```bash
# Instalar dependencias de google-sync
pip install -r data/google-sync/requirements.txt

# Ejecutar sincronizacion de datos
python data/google-sync/scripts/sync_google.py --account your-email@gmail.com
```

**Lo que hace sync_google.py:**
1. **Gmail**: Obtener correos recientes y guardar en formato Markdown en `data/google-sync/data/gmail/`
2. **Calendar**: Obtener eventos proximos y guardar en `data/google-sync/data/calendar/`
3. **Drive**: Guardar metadatos de documentos actualizados recientemente en `data/google-sync/data/docs/`

```bash
# Verificar resultados de sincronizacion
ls -la data/google-sync/data/

# Verificar datos sincronizados de Gmail
ls data/google-sync/data/gmail/ | head -10

# Verificar datos sincronizados de Calendar
ls data/google-sync/data/calendar/
```

**Resultado esperado**: Los datos de Gmail, Calendar y Drive se guardan en el directorio `data/`.

> **💡 Consejo**: Si sync_google.py no existe, tambien puede sincronizar manualmente combinando comandos de gogcli. Pregunte a la IA por los pasos alternativos del Step 1.

**Pasos alternativos (ejecucion directa de gogcli):**
```bash
# Gmail: Obtener correos no leídos
mkdir -p /tmp/google-sync/gmail
gog gmail search "is:unread newer_than:7d" --account your-email@gmail.com > /tmp/google-sync/gmail/unread.txt

# Calendar: Eventos de esta semana
mkdir -p /tmp/google-sync/calendar
gog calendar list --account your-email@gmail.com --days 7 > /tmp/google-sync/calendar/this_week.txt

# Drive: Archivos actualizados recientemente
mkdir -p /tmp/google-sync/drive
gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-07'" --max 20 > /tmp/google-sync/drive/recent.txt
```

---

## 🚀 Step 2: Extraer tareas del correo con check-inbox

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Extraer tareas del correo",
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

Use el skill check-inbox para extraer automaticamente elementos de accion de los correos:

```bash
# Ejecutar script de check-inbox
python skills/check-inbox/scripts/check_inbox.py --account your-email@gmail.com
```

**Lo que hace check-inbox:**
1. Obtener correos recientes
2. La IA analiza el contenido del correo y extrae lo siguiente:
   - **Correos que requieren respuesta** (prioridad: Alta/Media/Baja)
   - **Correos que contienen solicitudes/tareas** (con plazos)
   - **FYI (solo informacion compartida)**
   - **Correos que requieren seguimiento**

**Pasos alternativos (solicitar a la IA directamente):**

Tambien puede hacer que la IA analice los datos de correo obtenidos con gogcli:

```bash
# Obtener correos no leídos
gog gmail search "is:unread newer_than:3d" --account your-email@gmail.com
```

Pegue los resultados en el chat de Cursor:
```text
De la lista de correos anterior, extraiga tareas usando las siguientes categorías:

## 🔴 Urgente (dentro de 24 horas)
- Asunto del correo / Remitente / Acción requerida

## 🟡 Responder esta semana
- Asunto del correo / Remitente / Acción requerida

## 🟢 Solo información (FYI)
- Asunto del correo / Remitente / Resumen

## 📋 Seguimiento
- Asunto del correo / Remitente / Plazo de seguimiento
```

**Resultado esperado**: Los correos se clasifican por categoria y se genera una lista de tareas priorizada.

---

## 🚀 Step 3: Cruzar con calendario para determinar prioridad

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Referencia cruzada con calendario y determinación de prioridad",
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

Cruce las tareas extraidas en el Step 2 con los eventos del calendario para determinar la prioridad:

```bash
# Obtener calendario de esta semana
gog calendar list --account your-email@gmail.com --days 7
```

Combine los datos del calendario obtenidos con la lista de tareas del Step 2 y solicite el analisis de la IA:

```text
Cruce las siguientes dos fuentes de datos y realice una evaluación de prioridad integrada:

[Tareas extraídas del correo]
(Pegue los resultados del Step 2 aquí)

[Calendario de esta semana]
(Pegue la lista del calendario aquí)

Analice desde las siguientes perspectivas:
1. ¿Hay tareas que necesitan preparación justo antes de una reunión?
2. Evitar asignar tareas en días con muchas reuniones
3. Sugerir asignar tareas en espacios de tiempo libre
4. Advertir sobre tareas con plazos próximos
5. Lista de cosas que hacer hoy en preparación para mañana

Genere los resultados en el siguiente formato:

## 📅 Pendientes de hoy (priorizados)
1. [Alto] Nombre de la tarea - Razón
2. [Medio] Nombre de la tarea - Razón
3. [Bajo] Nombre de la tarea - Razón

## 📋 Pendientes de la semana (por día)
### Lunes
- Tarea (libre: recomendado para 10:00-12:00)
### Martes
- ...

## ⚠️ Notas
- Recordatorios de preparación previa a reuniones
- Advertencias de plazos
```

**Resultado esperado**: Las tareas de correo y los eventos del calendario se integran, y se genera una lista de tareas pendientes con prioridades.

---

## 🚀 Step 4: Generar reporte diario automaticamente

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Generación de reporte diario",
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

Integre todos los datos para generar un reporte diario. Ingrese el siguiente prompt en Cursor:

```text
Ejecute los siguientes comandos de gogcli, integre los resultados y genere un reporte diario:

1. gog gmail search "newer_than:1d" --account your-email@gmail.com
2. gog calendar list --account your-email@gmail.com --days 1
3. gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-13'" --max 10

Cree un reporte en el siguiente formato y guarde en output/reports/daily_report_2026-03-14.md:

# 📊 Reporte diario: 2026-03-14

## 📧 Resumen de correos
- Recibidos: X (No leídos: X)
- Requieren respuesta: X
- Correos principales:
  1. [Asunto] de [Remitente] - [Resumen en una línea]

## 📅 Horario de hoy
| Hora | Evento | Ubicación |
|------|--------|----------|
| 10:00-11:00 | xxx | xxx |

## 📁 Archivos actualizados recientemente
- [Nombre del archivo] - [Última modificación]

## ✅ Pendientes de hoy (priorizados)
1. [Alto] xxx
2. [Medio] xxx

## 📝 Notas
- Puntos de interés
```

**Avanzado: Configuracion de ejecucion programada**

Para generar automaticamente reportes diarios cada manana, use el siguiente metodo:

```bash
# Combinar en un script de shell
cat > tools/daily_report.sh << 'SCRIPT'
#!/bin/bash
ACCOUNT="your-email@gmail.com"
DATE=$(date +%Y-%m-%d)

echo "=== Gmail ===" > /tmp/daily_data.txt
gog gmail search "newer_than:1d" --account $ACCOUNT >> /tmp/daily_data.txt

echo "=== Calendar ===" >> /tmp/daily_data.txt
gog calendar list --account $ACCOUNT --days 1 >> /tmp/daily_data.txt

echo "=== Drive ===" >> /tmp/daily_data.txt
gog drive ls --account $ACCOUNT --query "modifiedTime > '$(date -v-1d +%Y-%m-%d)'" --max 10 >> /tmp/daily_data.txt

echo "Recopilación de datos completada: /tmp/daily_data.txt"
echo "En Cursor, ingrese: Por favor lea /tmp/daily_data.txt y genere un reporte diario"
SCRIPT
chmod +x tools/daily_report.sh
```

**Resultado esperado**: El reporte diario se guarda en formato Markdown en `output/reports/`.

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
      {"id": "trouble_1", "label": "El script google-sync no funciona"},
      {"id": "trouble_2", "label": "check-inbox produce un error"},
      {"id": "trouble_3", "label": "Demasiados datos, el procesamiento tarda demasiado"},
      {"id": "trouble_4", "label": "Quiero mejorar la calidad del reporte"}
    ]
  }]
}
```

### Problema 1: "El script google-sync no funciona"
**Causa**: Paquetes de dependencia faltantes, o configuracion del script
**Prompt de solucion**:
```text
Como alternativa, recopile datos directamente usando comandos de gogcli.
Ejecute los comandos en la sección "Pasos alternativos" del Step 1.
```

### Problema 2: "check-inbox produce un error"
**Causa**: Configuracion insuficiente del skill, o fallo en la obtencion de datos de correo
**Prompt de solucion**:
```text
En lugar de check-inbox, obtenga correos con gogcli gmail search
y solicite a la IA que extraiga tareas directamente (ver "Pasos alternativos" del Step 2).
```

### Problema 3: "Demasiados datos, el procesamiento tarda demasiado"
**Causa**: El parametro --max es demasiado grande
**Prompt de solucion**:
```text
Reduzca el valor de --max (recomendado: 10-20).
Acortar el período con --query "newer_than:1d" también puede acelerar el proceso.
```

### Problema 4: "Se desea mejorar la calidad del reporte"
**Causa**: Se necesita mejorar el prompt
**Prompt de solucion**:
```text
Intente agregar lo siguiente a su prompt:
- "Criterios de importancia de correos de negocio: Priorizar correos de gerentes/clientes"
- "Agregar elementos de preparación a cada evento de reunión"
- "Trasladar elementos pendientes incompletos del día anterior"
```

---

## ✅ Punto de control
- [ ] Pudo recopilar datos por lotes con google-sync (o comandos manuales de gogcli)
- [ ] Pudo extraer tareas de correos y clasificar por prioridad
- [ ] Pudo cruzar el calendario y las tareas para crear un To-Do integrado
- [ ] Pudo generar y guardar reportes diarios en formato Markdown


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
Realice la verificación integral del Módulo 4:
1. Verifique el estado de autenticación de la cuenta de Google con gog auth list
2. Verifique que se hayan generado reportes diarios en output/reports/
3. Verifique que todos los siguientes comandos de gogcli funcionen:
   - gog gmail search "newer_than:1d" --account <email>
   - gog calendar list --account <email> --days 1
   - gog drive ls --account <email> --max 3
```

**Resultado esperado**: Todos los comandos funcionan sin errores y se generan reportes diarios.

---

## 🎉 Module 4 Completado！

Felicitaciones. Module 4: Google Workspace Utilization esta completo.

**Habilidades adquiridas:**
- Instalacion y configuracion de autenticacion de gogcli
- Busqueda, visualizacion y analisis de correos de Gmail con IA
- Gestion de eventos de Google Calendar
- Operaciones de archivos de Google Drive
- Obtencion y analisis de datos de Google Sheets
- Flujo de trabajo de secretaria IA integrando Gmail+Calendar+Drive

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_module", "label": "Continuar al Módulo 5 (/start-5-1)"},
      {"id": "review", "label": "Repasar el Módulo 4 (/start-4-1)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_module → /start-5-1（al siguiente modulo)
- review → /start-4-1（Revisar el Module 4 desde el principio)
- finish → Finalizar
